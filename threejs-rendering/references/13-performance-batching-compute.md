> Part of the `threejs-rendering` skill. Verified against three r187 (2026-10-31); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# 13. Performance, instancing, `BatchedMesh` and WebGPU compute

Measure before changing geometry or shaders. Optimize the bottleneck the counters name (draw calls, triangle count, fill rate, shader compile stalls, or CPU frame time).

---

### 13.1 Reading `renderer.info` on WebGL2 vs WebGPU

`renderer.info` resets at the start of each `render()` call when `info.autoReset === true`. Always read it **after** `render()` (or after `pipeline.render()`). When a frame runs multiple render passes manually, set `renderer.info.autoReset = false` and call `renderer.info.reset()` once at the end of the frame.

| Metric | `WebGLRenderer` | `WebGPURenderer` |
|---|---|---|
| **Draw calls (this frame)** | `renderer.info.render.calls` | `renderer.info.render.drawCalls` (`info.render.calls` is cumulative render passes since startup!) |
| **Triangles (this frame)** | `renderer.info.render.triangles` | `renderer.info.render.triangles` |
| **Compute dispatches (this frame)** | — | `renderer.info.compute.frameCalls` |
| **Live GPU buffers / textures** | `info.memory.geometries`, `info.memory.textures` (counts) | Counts **plus** byte estimates: `info.memory.total`, `info.memory.texturesSize`, `info.memory.attributesSize` |

For live pass-by-pass GPU timestamp profiling, TSL shader inspection, and VRAM audits on `WebGPURenderer`, attach Three's first-party `Inspector`:

```js
import { Inspector } from 'three/addons/inspector/Inspector.js';
renderer.inspector = new Inspector(); // assign before await renderer.init()
```

---

### 13.2 Choosing the right draw-call reducer

Each single-material `Mesh` costs 1 draw call per render pass (multiplied by shadow cascades and transmission passes). Target **≤ 150–300 draw calls** for 60 FPS desktop scenes, **≤ 80** on mobile.

| Technique | When to use | Culling & Picking |
|---|---|---|
| **`InstancedMesh`** | Many copies of **one geometry + one material** (trees, bolts, chairs, crowd props). | Single bounding sphere for the whole batch (`computeBoundingSphere()` after moving instances). Raycast returns `hit.instanceId`. |
| **`BatchedMesh`** | Many **different geometries sharing one material** (modular kitbash walls, rocks, props). | Per-instance frustum culling (`perObjectFrustumCulled = true`) and depth sorting (`sortObjects = true`). Single multi-draw on WebGL2 (`WEBGL_multi_draw`). Pair with `computeBatchedBoundsTree` (`§12.5`); raycast returns `hit.batchId`. |
| **`SceneOptimizer.toBatchedMesh()`** | Imported glTF/CAD hierarchies with dozens of separate child `Mesh` nodes sharing materials. | Automatically merges compatible static child meshes into `BatchedMesh` instances per material (**never** call `.toInstancingMesh()` on r187 — it throws `not implemented yet`). |
| **`BundleGroup` (`three/webgpu`)** | Static sub-trees with **mixed materials** whose visibility/pipeline state rarely changes. | Records a reusable `GPURenderBundle` on WebGPU (slashes CPU command-encoding overhead; behaves as a normal `Group` on WebGL2). Increment `bundle.version ++` if children/materials change. |
| **`NodeMaterialInstance` (`three/webgpu`)** | Dozens of meshes needing distinct per-object uniform/texture values without compiling duplicate shader pipelines. | Shares one compiled `NodeMaterial` pipeline across instances (`§4.7`). Use `reference('userData.x', ...)` on `mesh.userData` for shadow-casting `colorNode` props! |
| **`BufferGeometryUtils.mergeGeometries`** | Static, non-interactive geometry clusters that never move individually. | All-or-nothing culling per merged chunk. Merge per room/sector, not across the entire world. |
| **`THREE.LOD`** | High-poly hero meshes viewed across a wide distance range. | Same draw call count; cuts vertex/triangle shading cost at distance. |

#### `InstancedMesh` + per-instance TSL attributes

```js
import * as THREE from 'three/webgpu';
import { instancedBufferAttribute, positionLocal } from 'three/tsl';

const count = 1000;
const mesh = new THREE.InstancedMesh( geometry, material, count );
const dummy = new THREE.Object3D();

for ( let i = 0; i < count; i ++ ) {

	dummy.position.set( ( i % 32 ) * 1.5, 0, Math.floor( i / 32 ) * 1.5 );
	dummy.updateMatrix();
	mesh.setMatrixAt( i, dummy.matrix );
	mesh.setColorAt( i, new THREE.Color().setHSL( ( i * 0.07 ) % 1, 0.5, 0.5 ) );

}

mesh.instanceMatrix.needsUpdate = true;
mesh.instanceColor.needsUpdate = true;
mesh.computeBoundingSphere();

// Optional extra per-instance attribute in TSL:
const phaseAttr = new THREE.InstancedBufferAttribute( new Float32Array( count ), 1 );
const phaseNode = instancedBufferAttribute( phaseAttr );
```

#### `BatchedMesh` (r166+ `addGeometry` + `addInstance` contract)

A geometry added to a `BatchedMesh` renders **only** after `addInstance( geometryId )` is called:

```js
const batched = new THREE.BatchedMesh(
	500,   // maxInstanceCount
	40000, // maxVertexCount across all distinct geometries
	80000, // maxIndexCount
	sharedPhysicalMaterial
);

const rockA = batched.addGeometry( rockGeoA );
const rockB = batched.addGeometry( rockGeoB );
const mat4 = new THREE.Matrix4();

for ( let i = 0; i < 500; i ++ ) {

	const instId = batched.addInstance( i % 2 === 0 ? rockA : rockB );
	batched.setMatrixAt( instId, mat4.makeTranslation( x, y, z ) );

}
```

#### Automatic hierarchy batching (`SceneOptimizer`), `BundleGroup`, and `NodeMaterialInstance` (r187)

```js
import * as THREE from 'three/webgpu'; // BundleGroup & NodeMaterialInstance live in 'three/webgpu', NOT 'three'
import { reference, materialReference } from 'three/tsl';
import { SceneOptimizer } from 'three/addons/utils/SceneOptimizer.js';

// 1) Convert an imported static glTF sub-tree into BatchedMesh instances automatically:
new SceneOptimizer( architecturalGroup ).toBatchedMesh(); // do NOT call .toInstancingMesh() (throws in r187)

// 2) Record a static WebGPU render bundle across mixed-material meshes + NodeMaterialInstance:
const baseMat = new THREE.MeshStandardNodeMaterial( { metalness: 0.25 } );
baseMat.colorNode = reference( 'userData.tint', 'color' );           // Object3D ref survives ShadowMaterial override! (§4.7)
baseMat.roughnessNode = materialReference( 'userData.rough', 'float' );

const bundle = new THREE.BundleGroup();
for ( let i = 0; i < 64; i ++ ) {

	const instMat = new THREE.NodeMaterialInstance( baseMat );
	instMat.userData.rough = 0.15 + ( i % 5 ) * 0.18;
	const mesh = new THREE.Mesh( propGeo, instMat );
	mesh.userData.tint = new THREE.Color().setHSL( i / 64, 0.7, 0.55 );
	mesh.castShadow = true;
	bundle.add( mesh );

}
scene.add( bundle ); // bump `bundle.version++` only if children or material pipelines change
```

> **Experimental GPU-driven WebGPU pipelines (r187):** For extreme GPU-culled million-triangle worlds on WebGPU-only targets, Three r187 also exposes `IndirectStorageBufferAttribute` (`three/webgpu`, compute-written `drawIndirect` / `drawIndexedIndirect` args) plus `MeshletDrawingPipeline` and `VisibilityBufferDrawingPipeline` (`three/addons/pipelines/*`). Keep `BatchedMesh` / `InstancedMesh` whenever WebGL2 fallback parity is required.

---

### 13.3 Eliminating shader compile stalls & CPU frame spikes

1. **Precompile shaders during loading:**
   ```js
   await renderer.compileAsync( scene, camera ); // uses KHR_parallel_shader_compile on WebGL2; pre-builds pipelines on WebGPU
   ```
   Do not flip shader-defining flags at runtime (`material.transparent`, `side`, `flatShading`, `vertexColors`, or assigning/nulling a texture slot for the first time) — toggle uniform values (`opacity`, `normalScale`, `envMapIntensity`) instead.
2. **Freeze static transforms:**
   For static environment meshes that never move after placement:
   ```js
   mesh.matrixAutoUpdate = false;
   mesh.updateMatrix();
   ```
3. **Freeze static shadow maps:**
   If neither the directional light nor the shadow casters move:
   ```js
   sun.shadow.autoUpdate = false;
   sun.shadow.needsUpdate = true;
   ```
4. **Zero allocations inside `setAnimationLoop`:**
   Preallocate scratch `Vector3`, `Matrix4`, `Quaternion`, and `Color` instances at module scope. Allocating inside the frame loop triggers GC pauses every few seconds.
5. **Cap pixel ratio:**
   ```js
   renderer.setPixelRatio( Math.min( window.devicePixelRatio, 2 ) );
   ```

---

### 13.4 WebGPU compute shaders (`instancedArray` & r187 `storage` structs)

Move particle simulation, foliage wind fields, or cloth/fluid updates off the CPU with `renderer.compute()`.

```js
import * as THREE from 'three/webgpu';
import { Fn, instancedArray, instanceIndex, hash, time, sin, cos, TWO_PI, vec3 } from 'three/tsl';

const count = 100_000;
const posBuffer = instancedArray( count, 'vec3' );

const updateParticles = Fn( () => {

	const r = hash( instanceIndex );
	const angle = r.mul( TWO_PI ).add( time.mul( 0.5 ) );
	const radius = r.mul( 6.0 ).add( 1.0 );
	posBuffer.element( instanceIndex ).assign(
		vec3( cos( angle ).mul( radius ), sin( r.mul( 97.0 ).add( time ) ).mul( 0.8 ), sin( angle ).mul( radius ) )
	);

} )().compute( count );

// Render as instanced sprites (WebGPU native Points are locked to 1 px regardless of size):
const mat = new THREE.PointsNodeMaterial( {
	positionNode: posBuffer.toAttribute(),
	size: 0.08,
} );
const particles = new THREE.Sprite( mat );
particles.count = count;
particles.frustumCulled = false; // bounding sphere at origin does not cover GPU buffer bounds
scene.add( particles );

// Inside setAnimationLoop (after await renderer.init()):
renderer.compute( updateParticles );
renderer.render( scene, camera );
```

- **r187 gate (#34807):** Struct storage buffers in TSL are always arrays. Access members via `.element( i ).get( 'member' )` (or `.element( 0 ).get( 'member' )` for singletons), never `storage( buf, Struct ).get( 'member' )`.
- **Workgroup shared memory, barriers, atomics & `StorageTexture` (WebGPU):** For tile reductions, prefix scans, fluid solvers, or procedural textures on `renderer.backend.isWebGPUBackend`, dispatch explicit `[gx, gy, gz]` total invocations and `[wx, wy, wz]` workgroup sizes:
  ```js
  import * as THREE from 'three/webgpu';
  import { Fn, workgroupArray, workgroupBarrier, localId, globalId, atomicAdd, instancedArray, textureStore, float, uint, vec4, If } from 'three/tsl';

  const outTex = new THREE.StorageTexture( 256, 256 );
  const counter = instancedArray( 1, 'uint' ).toAtomic();

  const writeTile = Fn( () => {

    const shared = workgroupArray( 'float', 64 );
    const lid = localId.x;
    shared.element( lid ).assign( float( lid ).div( 64.0 ) );
    workgroupBarrier(); // synchronize shared memory across the 64-thread workgroup (use storageBarrier() for storage buffers)

    If( lid.equal( uint( 0 ) ), () => { atomicAdd( counter.element( 0 ), uint( 1 ) ); } );
    const mirror = shared.element( uint( 63 ).sub( lid ) );
    textureStore( outTex, globalId.xy, vec4( mirror, 0.5, 0.85, 1.0 ) );

  } )().compute( [ 256, 256, 1 ], [ 64, 1, 1 ] );

  await renderer.compute( writeTile ); // sample `outTex` in any NodeMaterial via `texture( outTex )`
  ```
- **WebGPU `Points` vs `Sprite` + `PointsNodeMaterial`:** WebGPU hardware renders `THREE.Points` at 1 px regardless of `size`. For sized point clouds or particles on `WebGPURenderer`, use `new THREE.Sprite( new THREE.PointsNodeMaterial( { positionNode, size } ) )` with `sprite.count = N`.
- **WebGPU `LineLoop` & thick lines:** `LineLoop` is unsupported on `WebGPURenderer` (repeat the first vertex on a `THREE.Line`). For lines wider than 1 px, use `Line2` from `three/addons/lines/webgpu/Line2.js` with `Line2NodeMaterial` from `three/webgpu`.

---

### 13.5 Common mistakes

| Wrong | Right (r187) | Why |
|---|---|---|
| `webgpuRenderer.info.render.calls` for per-frame draw calls | `webgpuRenderer.info.render.drawCalls` | On `WebGPURenderer`, `render.calls` is cumulative render passes since startup. |
| `batchedMesh.addGeometry( geo )` without `addInstance` | `const id = batchedMesh.addGeometry( geo ); batchedMesh.addInstance( id );` | `BatchedMesh` draws only registered instances of added geometries (r166+). |
| `new SceneOptimizer( group ).toInstancingMesh()` | `new SceneOptimizer( group ).toBatchedMesh()` | `.toInstancingMesh()` throws `not implemented yet` in r187. |
| `import { BundleGroup } from 'three'` | `import { BundleGroup } from 'three/webgpu'` | `BundleGroup` and `NodeMaterialInstance` are exported from `'three/webgpu'`, not `'three'`. |
| `materialReference(...)` inside `colorNode` on shadow-casting `NodeMaterialInstance` | `reference( 'userData.tint', 'color' )` on `mesh.userData` | Shadow pass swaps `state.material` to `ShadowMaterial`, making custom material properties `undefined` (`§4.7`). |
| `new THREE.Points( geo, new THREE.PointsMaterial({ size: 8 }) )` on WebGPU | `new THREE.Sprite( new THREE.PointsNodeMaterial({ positionNode, size: 0.2 }) )` with `sprite.count = N` | WebGPU specification locks point primitives to 1.0 px. |
| `storage( buf, MyStruct ).get( 'vel' )` | `storage( buf, MyStruct ).element( 0 ).get( 'vel' )` | r187 #34807 made struct storage buffers array-indexed. |
| `renderer.compile( scene, camera )` | `await renderer.compileAsync( scene, camera )` | Sync `compile()` does not wait for parallel shader compilation to finish before first frame. |
