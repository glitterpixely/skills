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

---

### 13.2 Choosing the right draw-call reducer

Each single-material `Mesh` costs 1 draw call per render pass (multiplied by shadow cascades and transmission passes). Target **≤ 150–300 draw calls** for 60 FPS desktop scenes, **≤ 80** on mobile.

| Technique | When to use | Culling & Picking |
|---|---|---|
| **`InstancedMesh`** | Many copies of **one geometry + one material** (trees, bolts, chairs, crowd props). | Single bounding sphere for the whole batch (`computeBoundingSphere()` after moving instances). Raycast returns `hit.instanceId`. |
| **`BatchedMesh`** | Many **different geometries sharing one material** (modular kitbash walls, rocks, props). | Per-instance frustum culling (`perObjectFrustumCulled = true`) and depth sorting (`sortObjects = true`). Single multi-draw on WebGL2 (`WEBGL_multi_draw`). Raycast returns `hit.batchId`. |
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
- **WebGPU `Points` vs `Sprite` + `PointsNodeMaterial`:** WebGPU hardware renders `THREE.Points` at 1 px regardless of `size`. For sized point clouds or particles on `WebGPURenderer`, use `new THREE.Sprite( new THREE.PointsNodeMaterial( { positionNode, size } ) )` with `sprite.count = N`.
- **WebGPU `LineLoop` & thick lines:** `LineLoop` is unsupported on `WebGPURenderer` (repeat the first vertex on a `THREE.Line`). For lines wider than 1 px, use `Line2` from `three/addons/lines/webgpu/Line2.js` with `Line2NodeMaterial` from `three/webgpu`.

---

### 13.5 Common mistakes

| Wrong | Right (r187) | Why |
|---|---|---|
| `webgpuRenderer.info.render.calls` for per-frame draw calls | `webgpuRenderer.info.render.drawCalls` | On `WebGPURenderer`, `render.calls` is cumulative render passes since startup. |
| `batchedMesh.addGeometry( geo )` without `addInstance` | `const id = batchedMesh.addGeometry( geo ); batchedMesh.addInstance( id );` | `BatchedMesh` draws only registered instances of added geometries (r166+). |
| `new THREE.Points( geo, new THREE.PointsMaterial({ size: 8 }) )` on WebGPU | `new THREE.Sprite( new THREE.PointsNodeMaterial({ positionNode, size: 0.2 }) )` with `sprite.count = N` | WebGPU specification locks point primitives to 1.0 px. |
| `storage( buf, MyStruct ).get( 'vel' )` | `storage( buf, MyStruct ).element( 0 ).get( 'vel' )` | r187 #34807 made struct storage buffers array-indexed. |
| `renderer.compile( scene, camera )` | `await renderer.compileAsync( scene, camera )` | Sync `compile()` does not wait for parallel shader compilation to finish before first frame. |
