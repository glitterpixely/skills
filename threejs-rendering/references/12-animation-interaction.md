> Part of the `threejs-rendering` skill. Verified against three r187 (2026-10-31); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# 12. Animation, camera controls and raycast interaction

`AnimationMixer`, `Controls` and `Raycaster` run on the CPU and behave identically on `WebGLRenderer` and `WebGPURenderer`.

---

### 12.1 Frame loop and `THREE.Timer` (r183+ replaces `Clock`)

`THREE.Clock` is deprecated in r183. Use `THREE.Timer` and `renderer.setAnimationLoop()` (which hands frames to WebXR when active and awaits `renderer.init()` automatically on `WebGPURenderer`).

```js
const timer = new THREE.Timer();
timer.connect( document ); // clamps delta after tab backgrounding

// For deterministic headless captures / gate harnesses on r187:
// timer._startTime = 0; // Timer subtracts constructor wall-clock _startTime when stepping manually

renderer.setAnimationLoop( ( timestamp ) => {

	timer.update( timestamp ); // call ONCE at the top of the frame
	const dt = timer.getDelta();
	const elapsed = timer.getElapsed();

	mixer?.update( dt );
	controls.update( dt );
	renderer.render( scene, camera );

} );
```

---

### 12.2 Keyframe clips, `AnimationMixer`, crossfades and additive layers

- **Track binding syntax:** `nodeName.objectName[objectIndex].propertyName[propertyIndex]`.
  - `.position[y]` (scalar `NumberKeyframeTrack`), `.position` (`VectorKeyframeTrack`, stride 3), `.quaternion` (`QuaternionKeyframeTrack`, stride 4 — never Euler), `.morphTargetInfluences[smile]` (`NumberKeyframeTrack` — never `StringKeyframeTrack`).
  - `values.length` **must** equal `times.length * itemSize`.
- **Crossfading:**
  ```js
  const mixer = new THREE.AnimationMixer( root );
  const idle = mixer.clipAction( THREE.AnimationClip.findByName( gltf.animations, 'Idle' ) ).play();
  const walk = mixer.clipAction( THREE.AnimationClip.findByName( gltf.animations, 'Walk' ) );

  // Smoothly hand over in 0.35 s (3rd arg true warps timeScales to match cycle length):
  idle.crossFadeTo( walk.reset().play(), 0.35, true );
  ```
- **Additive layering (breathing, recoil, look-at):**
  ```js
  THREE.AnimationUtils.makeClipAdditive( breathClip ); // rebases tracks onto frame 0
  const breath = mixer.clipAction( breathClip );
  breath.setEffectiveWeight( 0.6 ).play(); // layers on top of the base locomotion pose
  ```
- **Mixer teardown:**
  ```js
  mixer.stopAllAction();
  mixer.uncacheRoot( root );
  ```

---

### 12.3 Skeletal rigs, procedural bone overrides and `SkeletonUtils.clone`

1. **Cloning skinned glTFs:** `model.clone()` shares a single `Skeleton` across copies, so clones deform with the original. Always clone with `SkeletonUtils`:
   ```js
   import * as SkeletonUtils from 'three/addons/utils/SkeletonUtils.js';
   const copy = SkeletonUtils.clone( gltf.scene );
   const copyMixer = new THREE.AnimationMixer( copy );
   ```
2. **Procedural bone override order:** `mixer.update( dt )` overwrites every bone animated by active clips. Apply procedural head-turn, aim or IK **after** `mixer.update( dt )`:
   ```js
   mixer.update( dt );
   if ( headBone ) headBone.rotation.y = THREE.MathUtils.damp( headBone.rotation.y, targetYaw, 8, dt );
   ```
3. **Skinned frustum culling:** `SkinnedMesh` computes its bounding sphere once from the rest pose. If root motion moves a character far from origin and it pops out at screen edges, call `skinnedMesh.computeBoundingSphere()` after `mixer.update( dt )` + `root.updateMatrixWorld()`, or set `skinnedMesh.frustumCulled = false` on that mesh only.

---

### 12.4 GPU vertex animation in TSL (`positionNode` + shadow sync)

Always displace from `positionLocal` (which already includes skinning, morph targets, batching and `InstancedMesh` transforms), never `positionGeometry` (raw rest pose).

To make shadows match GPU-displaced vertices, assign `castShadowPositionNode` as well, and recompute or perturb normals if the surface is lit:

```js
import * as THREE from 'three/webgpu';
import { Fn, positionLocal, normalLocal, time, sin, vec3 } from 'three/tsl';

const displace = Fn( () => {

	const wave = sin( positionLocal.x.mul( 4.0 ).add( time.mul( 2.5 ) ) ).mul( 0.12 );
	return positionLocal.add( normalLocal.mul( wave ) );

} );

const mat = new THREE.MeshPhysicalNodeMaterial( { roughness: 0.35 } );
mat.positionNode = displace();
mat.castShadowPositionNode = displace(); // keeps shadow map aligned with displaced vertices
```

---

### 12.5 Raycasting and picking

- **Coordinate normalization:** Always compute NDC relative to `renderer.domElement.getBoundingClientRect()` so scrolled or embedded canvases pick accurately:
  ```js
  const rect = renderer.domElement.getBoundingClientRect();
  pointer.set(
    ( ( e.clientX - rect.left ) / rect.width ) * 2 - 1,
    - ( ( e.clientY - rect.top ) / rect.height ) * 2 + 1
  );
  ```
- **Filter before testing geometry:** Never run `raycaster.intersectObjects( scene.children, true )` on `pointermove`. Enable a dedicated picking layer on interactive meshes (`mesh.layers.enable( 1 )` — do **not** use `.set( 1 )`, which removes the mesh from camera layer `0`) and set `raycaster.layers.set( 1 )`, or pass a small explicit `pickables` array.
- **Hit payload:**
  - `hit.instanceId` — index hit on an `InstancedMesh`
  - `hit.batchId` — instance hit on a `BatchedMesh`
  - `hit.face.normal` — object-space triangle normal (`hit.normal` is the interpolated vertex normal flipped toward the ray)
- **Sub-millisecond raycasts on dense meshes & `BatchedMesh` (`three-mesh-bvh@0.9.18`):** Default `Mesh.raycast` linearly scans every triangle (`O(N)`). Patch `three-mesh-bvh` once at startup so raycasts traverse a Bounding Volume Hierarchy (`O(log N)`):
  ```js
  import { computeBoundsTree, disposeBoundsTree, computeBatchedBoundsTree, acceleratedRaycast } from 'three-mesh-bvh';

  THREE.BufferGeometry.prototype.computeBoundsTree = computeBoundsTree;
  THREE.BufferGeometry.prototype.disposeBoundsTree = disposeBoundsTree;
  THREE.BatchedMesh.prototype.computeBoundsTree = computeBatchedBoundsTree;
  THREE.Mesh.prototype.raycast = acceleratedRaycast;
  THREE.BatchedMesh.prototype.raycast = acceleratedRaycast;

  heroMesh.geometry.computeBoundsTree();
  batchedProps.computeBoundsTree();       // builds per-subgeometry BVHs; intersectObject returns hit.batchId
  raycaster.firstHitOnly = true;          // stops at closest hit instead of collecting all intersections
  // On teardown: geometry.disposeBoundsTree();
  ```
- **GPU-displaced meshes:** `Raycaster` tests CPU geometry and never sees `positionNode` displacement. Raycast against a simple invisible proxy (`mesh.layers.set( 1 )`) or replicate the math on CPU.

---

### 12.6 Camera & object controls (`three/addons/controls/*`)

| Control class | Key rules (r168–r187) |
|---|---|
| **`OrbitControls` / `MapControls`** | Pass `renderer.domElement` to constructor. When `enableDamping = true` or `autoRotate = true`, call `controls.update( timer.getDelta() )` every frame. |
| **`TransformControls`** | Not an `Object3D` (since r169). Add the gizmo via **`scene.add( transformControls.getHelper() )`**. Disable `orbitControls.enabled = ! event.value` inside `'dragging-changed'`. |
| **`DragControls`** | Constructor: `new DragControls( objects, camera, renderer.domElement )`. Access properties via `dragControls.objects` and `dragControls.raycaster` (`getObjects()` / `getRaycaster()` / `activate()` were removed in r168; use `connect( domElement )` / `disconnect()`). |
| **`PointerLockControls`** | Camera is `controls.object` (`getObject()` removed in r168). Call `controls.lock()` inside a user gesture (`click`). |
| **`FlyControls` / `FirstPersonControls`** | **Must** pass `timer.getDelta()` to `controls.update( dt )`; calling `update()` with no argument produces `NaN` camera positions. |
| **`camera-controls` (`camera-controls@3.1`)** | Production upgrade over `OrbitControls` when you need smooth programmatic framing (`controls.fitToBox( boxOrMesh, true )`, `controls.setLookAt( px, py, pz, tx, ty, tz, true )`), dolly-to-cursor, and boundary clamping. Call `CameraControls.install( { THREE } )` once and `controls.update( dt )` each frame. |

---

### 12.7 WebXR (`XRButton`, foveation, hit-test, controllers & hands)

`renderer.setAnimationLoop()` automatically switches from `window.requestAnimationFrame` to `XRSession.requestAnimationFrame` when an immersive VR/AR session starts:

```js
import { XRButton } from 'three/addons/webxr/XRButton.js';

renderer.xr.enabled = true;
renderer.xr.setReferenceSpaceType( 'local-floor' );
renderer.xr.setFoveation( 1.0 ); // lowers peripheral shading rate on Quest / Vision Pro / Pico

document.body.appendChild( XRButton.createButton( renderer, {
	optionalFeatures: [ 'local-floor', 'bounded-floor', 'hand-tracking', 'hit-test', 'layers' ],
} ) );

// Rig rule: XR overwrites camera.position and camera.quaternion every frame from head pose.
// Parent the camera to a rig Group for teleportation, snap-turn, or smooth locomotion:
const rig = new THREE.Group();
rig.add( camera );
scene.add( rig );

const controller0 = renderer.xr.getController( 0 ); // target-ray space for laser / UI pointing
const hand0 = renderer.xr.getHand( 0 );             // articulated XRHand joints
rig.add( controller0, hand0 );
```

- **AR surface placement (`hit-test`):** Request `session.requestReferenceSpace( 'viewer' )` and `session.requestHitTestSource( { space: viewerSpace } )` on `'sessionstart'`, then read `frame.getHitTestResults( hitTestSource )` inside `setAnimationLoop( ( time, frame ) => ... )`.
- **XR performance discipline:** Stereo rendering doubles view passes (`2×` draw calls). Avoid multi-pass screen-space post chains in XR; prefer baked lightmaps / `LightProbeGrid`, `InstancedMesh` / `BatchedMesh`, KTX2 textures, and MSAA on the XR framebuffer.

---

### 12.8 Built-in physics & spatial helpers (`three/addons/*`)

- **Zero-bundler physics addons:** For vanilla scenes (`InstancedMesh` rigid bodies + colliders), Three ships `RapierPhysics` (`'three/addons/physics/RapierPhysics.js'`) and `JoltPhysics` (`'three/addons/physics/JoltPhysics.js'`). Initialize via `const physics = await RapierPhysics(); physics.addScene( scene );`.
- **Lightweight character collision (`Octree`):** When full rigid-body physics is overkill for first-person walkthroughs, build a static world `Octree` (`'three/addons/math/Octree.js'`) with `worldOctree.fromGraphNode( levelScene )` and resolve player `Capsule` (`'three/addons/math/Capsule.js'`) collisions via `worldOctree.capsuleIntersect( playerCapsule )`.
- **Area-weighted surface scatter (`MeshSurfaceSampler`):** Sample uniform or vertex-weight-guided points and normals across terrain/props to populate `InstancedMesh` foliage or decals:
  ```js
  import { MeshSurfaceSampler } from 'three/addons/math/MeshSurfaceSampler.js';
  const sampler = new MeshSurfaceSampler( terrainMesh ).setWeightAttribute( 'color' ).build();
  sampler.sample( tmpPos, tmpNormal );
  ```

---

### 12.9 Common mistakes

| Wrong | Right (r187) | Why |
|---|---|---|
| `new THREE.Clock()` | `new THREE.Timer(); timer.connect( document );` | `Clock` deprecated in r183; `getElapsedTime()` also zeroed subsequent `getDelta()` calls. |
| `scene.add( transformControls )` | `scene.add( transformControls.getHelper() )` | `TransformControls` extends `Controls`, not `Object3D` (r169+). |
| `gltf.scene.clone()` on rigged model | `SkeletonUtils.clone( gltf.scene )` | `Object3D.clone()` shares one `Skeleton` instance across copies. |
| `mesh.layers.set( 1 )` for raycast | `mesh.layers.enable( 1 )` | `.set( 1 )` clears layer `0`, making the mesh invisible to the default camera. |
| `mat.positionNode = positionGeometry.add(...)` | `mat.positionNode = positionLocal.add(...)` | `positionGeometry` is the raw attribute and drops skinning, morphs, batching and instancing. |
| `controls.getObject()` / `drag.getObjects()` | `controls.object` / `drag.objects` | Getter methods removed in r168. |
