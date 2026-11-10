> Part of the `threejs-rendering` skill. Verified against three r187 (2026-10-31); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# 6. Geometry, scale and the asset pipeline

### 6.1 Edges catch light

A mathematically sharp 90° edge has zero area where the normal turns, so it reflects nothing, and real objects always have a radius. A 0.5–2 mm bevel on hand-sized objects (1–5 mm on furniture) creates a strip of rapidly rotating normals. That strip catches the key light and the IBL as a bright specular line, which defines the silhouette. (*Settled practice.*)

- **Micro-bevel:** 2–3 segments, profile 0.5–0.7. Or use `RoundedBoxGeometry( w, h, d, segments, radius )` for procedural boxes, as the r187 AO example does.
- **Weighted normals** (Blender *Weighted Normal* modifier, "Face Area", with *Keep Sharp*): large flat faces keep perfectly flat normals and the bevel strip absorbs all the curvature. Without it, smooth shading smears gradients across the flat faces, and they look "pillowy" or warped in reflections.
- **Export:** keep custom normals and include tangents. In gltf-transform, avoid aggressive `--simplify` on beveled hard-surface models, because the simplifier collapses the bevel first.
- **Normal-map bevels** (baked from high-poly) work at distance but break at silhouettes. Use real geometry for hero objects.

### 6.2 `gltf-transform` production pipeline (v4.5.1)

```bash
# 0) KTX-Software (toktx / ktx) must be on PATH for uastc/etc1s. Check: ktx --version
# 1) Clean + geometry: weld, meshopt, keep the hierarchy for interactivity
gltf-transform optimize in.glb stage1.glb \
  --compress meshopt --meshopt-level high \
  --texture-compress false \
  --simplify false \
  --flatten false --join false \
  --palette false
# 2) High-fidelity data textures -> UASTC (+RDO keeps the file size sane)
gltf-transform uastc stage1.glb stage2.glb \
  --slots "{normalTexture,occlusionTexture,metallicRoughnessTexture,clearcoatNormalTexture}" \
  --level 2 --rdo --rdo-lambda 2 --zstd 18
# 3) Colour textures -> ETC1S (smallest; artefacts hidden by albedo variation)
gltf-transform etc1s stage2.glb out.glb \
  --slots "{baseColorTexture,emissiveTexture,sheenColorTexture}" --quality 160
```

| Choice | Rule |
|---|---|
| **UASTC** | Normals, ORM/roughness, clearcoat normals, anything with smooth gradients. Block artefacts in normals show as faceted specular. Levels 0–4 run from 43.5 to 48.2 dB per the CLI table; 2 is the default. |
| **ETC1S** | Albedo, emissive, masks with noise. Several times smaller than UASTC (typical figures run 4–8×; *belief*, measure on your own textures). Never for normal maps. |
| **Meshopt vs Draco** | Meshopt (the default in `optimize`) decodes faster, compresses animation and morph targets, and gzips well. Draco gives smaller static geometry but slower WASM decode. |
| **`optimize` defaults to override for photoreal work** | `--simplify true` (error 0.0001) eats bevels. `--join` and `--flatten` merge meshes you may need to pick or animate. `--palette` merges materials into palette textures, which destroys per-material roughness detail. `--texture-size 2048` caps textures. |

*Checked:* `gltf-transform optimize --help`, `uastc --help` and `etc1s --help` on 4.5.1 list every flag used above, including `--rdo-lambda` and `--zstd` (range 1–22). KTX-Software is **not installed** on this machine, so the texture commands were not run.

**Loader side:**

```js
// Reuse ONE KTX2Loader instance across the app (multiple active instances spawn duplicate workers and warn)
const ktx2 = new KTX2Loader().detectSupport( renderer ); // call AFTER await renderer.init() on WebGPU
const gltfLoader = new GLTFLoader()
	.setDRACOLoader( new DRACOLoader() )
	.setMeshoptDecoder( MeshoptDecoder )
	.setKTX2Loader( ktx2 );
```

- **CLI ordering rule:** Always put `draco`, `meshopt`, or `optimize` **last** in a command chain. Any subsequent command that rewrites the file decodes Draco/meshopt geometry and writes it back uncompressed.
- **Skinned model cloning:** Never call `gltf.scene.clone()` on a `SkinnedMesh` (copies share the original skeleton and ignore their own animations). Use `SkeletonUtils.clone( gltf.scene )` from `three/addons/utils/SkeletonUtils.js`.
- **MikkTSpace tangents:** glTF normal maps follow MikkTSpace. For procedural or merged geometry, compute matching tangents with `await MikkTSpace.ready; BufferGeometryUtils.computeMikkTSpaceTangents( geom, MikkTSpace );` (from `three/addons/libs/mikktspace.module.js`).
- **Other formats:** Use `USDLoader` (`USDZLoader` deprecated in r179). For `PLYLoader`, convert any `Float64Array` attributes to `Float32BufferAttribute` before upload (WebGL/WebGPU reject 64-bit float vertex buffers).

### 6.2b Programmatic Node.js asset pipeline (`@gltf-transform/functions@4.5.1`)

When building assets inside a Node.js build script (or when the `ktx` / `toktx` CLI is unavailable on CI), run `@gltf-transform/core` + `@gltf-transform/functions` directly:

```js
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { dedup, weld, resample, quantize, prune, meshopt, textureCompress } from '@gltf-transform/functions';
import { MeshoptEncoder } from 'meshoptimizer';
import sharp from 'sharp';

await MeshoptEncoder.ready;
const io = new NodeIO().registerExtensions( ALL_EXTENSIONS ).registerDependencies( {
	'meshopt.encoder': MeshoptEncoder,
} );

const doc = await io.read( 'in.glb' );
await doc.transform(
	dedup(),
	weld(),                                  // indexes un-indexed triangle soup and merges seam duplicates
	resample(),                              // strips redundant collinear animation keyframes
	quantize(),                              // KHR_mesh_quantization (16-bit/8-bit vertex attributes)
	meshopt( { encoder: MeshoptEncoder, level: 'high' } ), // EXT_meshopt_compression (run AFTER weld/quantize)
	textureCompress( { encoder: sharp, targetFormat: 'webp', slots: /^(baseColor|emissive)Texture$/ } ), // fallback when toktx/KTX2 is absent
	prune(),                                 // removes orphaned materials, accessors, and nodes
);
await io.write( 'out.glb', doc );
```

> **Note:** WebP shrinks download size only—unlike KTX2 (`uastc` / `etc1s`), WebP still decodes to full uncompressed RGBA8 in VRAM (`width × height × 4 × 1.33` bytes with mipmaps). Prefer KTX2 whenever `ktx` is available.

### 6.3 First-party 3D Gaussian Splatting (`GaussianSplat`, r187)

Three r187 ships native 3D Gaussian Splatting for `WebGPURenderer` (running on both the Metal/Vulkan/D3D12 WebGPU backend via GPU `CountingSort` up to ~16.7M splats, and the WebGL2 `forceWebGL` fallback via PBO + CPU radix sort). Classic `WebGLRenderer` is **not** supported (`GaussianSplat` extends `InstancedMesh` with `NodeMaterial`).

| Asset / Task | Three.js r187 Module | Notes |
|---|---|---|
| **Renderable splat object** | `import { GaussianSplat } from 'three/addons/objects/GaussianSplat.js'` | Wraps splat geometry (`center`, `covA`, `covB`, `color`), updates view-depth sort automatically (`sortThreshold`, `focalScale`). |
| **Compressed `.spz` (Niantic)** | `import { SPZLoader } from 'three/addons/loaders/SPZLoader.js'` | Smallest standalone splat format (~10× smaller than `.ply`); returns a `GaussianSplat` instance. |
| **`.ply` / `.splat` / `.ksplat`** | `GaussianSplatPLYLoader.js`, `SPLATLoader.js`, `KSPLATLoader.js` under `'three/addons/loaders/'` | Direct loaders for standard 3DGS exports. |
| **glTF `KHR_gaussian_splatting`** | `import { GLTFGaussianSplatLoaderExtension } from 'three/addons/loaders/GLTFGaussianSplatLoaderExtension.js'` | Register via `gltfLoader.register( ( parser ) => new GLTFGaussianSplatLoaderExtension( parser ) )` to mix PBR meshes and splats in one `.glb`. |
| **Procedural splat buffers** | `createGaussianSplatGeometry`, `writeCovariance`, `writeColorBytes` from `'three/addons/utils/GaussianSplatUtils.js'` | Pack custom `centers` (`Float32Array` ×3), `covariances` (`Float32Array` ×6), and `colors` (`Uint8ClampedArray` ×4). |

```js
import { SPZLoader } from 'three/addons/loaders/SPZLoader.js';

const splats = await new SPZLoader().loadAsync( '/captures/courtyard.spz' );
scene.add( splats ); // renders alongside PBR meshes + shadows inside WebGPURenderer
```

For massive out-of-core multi-chunk splat worlds (50M+ splats requiring octree/chunk streaming LOD or spherical harmonics degree > 0 beyond r187's degree-0 base colour), pair Three.js with a streaming LOD splat runtime rather than loading a single monolithic buffer.

### 6.4 Memory disposal

GPU resources are not garbage-collected (even with r187's internal `WeakRef` / `FinalizationRegistry` safety nets, lifecycle soaks only return to baseline on explicit disposal):

```js
function disposeObject( root ) {

	root.traverse( ( o ) => {

		o.dispose?.(); // frees per-object renderer state (InstancedMesh/BatchedMesh/GaussianSplat buffers, WebGPU bindings)
		if ( ! o.geometry ) return;
		o.geometry.disposeBoundsTree?.(); // three-mesh-bvh BVH acceleration structure, if present
		o.geometry.dispose();
		for ( const m of [].concat( o.material ?? [] ) ) {

			for ( const v of Object.values( m ) ) if ( v && v.isTexture ) v.dispose();
			m.dispose();

		}

	} );

}
// also: envRT.dispose(), pmrem.dispose(), storageTex.dispose(), renderTarget.dispose(),
//       composer/pipeline.dispose(), ktx2.dispose(), dracoLoader.dispose(), renderer.dispose()
// verify: renderer.info.memory.{geometries,textures} must return to baseline after unload
```
