> Part of the `threejs-rendering` skill. Verified against three r187 (2026-10-31); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# 14. Custom shaders and GLSL-to-TSL translation

Prefer **TSL (`three/tsl`) + `*NodeMaterial` (`three/webgpu`)** whenever `WebGPURenderer` is in scope: one TSL graph compiles to both WGSL (WebGPU) and GLSL ES 3.00 (WebGL2 fallback), and hooks into PBR lighting inputs (`colorNode`, `roughnessNode`, `metalnessNode`, `normalNode`, `positionNode`, `castShadowPositionNode`) without breaking IBL, shadows, or MRT post passes (`§4.6`).

Use `onBeforeCompile` or `ShaderMaterial` only when locked to classic `WebGLRenderer`.

---

### 14.1 GLSL ↔ TSL Reference Table (r187)

All TSL symbols import from `'three/tsl'`; node materials import from `'three/webgpu'`. Never import from `'three/nodes'`.

| Concept | GLSL (`ShaderMaterial`) | TSL (`*NodeMaterial`) | r187 Notes / Renames |
|---|---|---|---|
| **Function definition** | `vec3 f( vec2 p ) { ... }` | `const f = Fn( ( [ p ] ) => { ... } );` | Do not use `glslFn` or `wgslFn` (backend-locked). |
| **Updatable uniform** | `uniform float uAmp;` | `const uAmp = uniform( 0.5 );` | Mutate in JS via `uAmp.value = 1.0`. Debug name: `.setName( 'amp' )` (`.label()` deprecated r179). |
| **Uniform array** | `uniform vec3 uPts[8];` | `const uPts = uniformArray( arrayOfVec3 );` | Renamed from `uniforms()` in r168. |
| **Elapsed time / dt** | Manual uniform `uTime` | `time`, `deltaTime` | Auto-updated every frame by the renderer. |
| **2π constant** | `6.2831853` | `TWO_PI` | Renamed from `PI2` in r181. |
| **Vertex attribute** | `attribute vec3 aOffset;` | `attribute( 'aOffset', 'vec3' )` | Per-instance: `instancedBufferAttribute( attr )`. |
| **Varying (VS → FS)** | `varying vec3 vWorldPos;` | `varying( positionWorld, 'vWorldPos' )` or `node.toVarying( 'vWorldPos' )` | Do not import `toVarying` as a standalone function. |
| **Local position** | `position` (`transformed`) | `positionLocal` | Includes skinning, morphs, batching & instancing (`positionGeometry` is raw rest pose). |
| **World position** | `(modelMatrix * vec4(pos,1)).xyz` | `positionWorld` | View-space: `positionView`. |
| **Normals (r187)** | `vNormal` / `normalMatrix * normal` | `normalLocal`, `normalView`, `normalWorld`, `clearcoatNormalView` | **r187 #34517 removed** `transformedNormalView`, `transformedNormalWorld`, `transformedClearcoatNormalView`. |
| **UV & screen coords** | `vUv` / `gl_FragCoord.xy / res` | `uv()`, `uv( 1 )`, `viewportUV` | `viewportTopLeft` renamed to `viewportUV` in r168. |
| **Texture sample** | `texture( map, vUv )` | `texture( map, uvNode )` or `texture( map ).sample( uvNode )` | `.uv()` method renamed to `.sample()` in r172. |
| **Alpha discard** | `if ( n < cut ) discard;` | `n.lessThan( cut ).discard();` | Works inside `Fn( () => { ... } )()`. |
| **Procedural noise** | Custom ashima/simplex GLSL | `mx_noise_float( p )`, `mx_fractal_noise_float( p )`, `mx_worley_noise_float( p )` | Built-in MaterialX noise nodes in `three/tsl`. |

---

### 14.2 Common TSL Node Material Patterns

#### 1. Dissolve with glowing emissive rim (preserving PBR lighting)

Instead of replacing the entire fragment shader with unlit colors, drive `colorNode`, `emissiveNode`, and discard inside `MeshPhysicalNodeMaterial`:

```js
import * as THREE from 'three/webgpu';
import { Fn, color, mix, mx_fractal_noise_float, positionLocal, smoothstep, uniform } from 'three/tsl';

const progress = uniform( 0.35 ).setName( 'dissolveProgress' );
const edgeWidth = uniform( 0.06 );
const edgeColor = color( 0xff5511 ).mul( 8.0 ); // HDR emissive edge for bloom

const noiseNode = mx_fractal_noise_float( positionLocal.mul( 3.0 ) ).mul( 0.5 ).add( 0.5 );

const mat = new THREE.MeshPhysicalNodeMaterial( { roughness: 0.4, metalness: 0.1 } );
mat.colorNode = Fn( () => {

	noiseNode.lessThan( progress ).discard();
	return color( 0x2b303a );

} )();

// Emissive rim only along the dissolve cut:
const rimMask = smoothstep( progress.add( edgeWidth ), progress, noiseNode );
mat.emissiveNode = edgeColor.mul( rimMask );
```

#### 2. View-space Fresnel / rim term (r187 `normalView` + `positionViewDirection`)

```js
import { dot, max, normalView, positionViewDirection, pow, float } from 'three/tsl';

// Both vectors are in view space — never mix normalView with world-space cameraPosition
const nDotV = max( dot( normalView, positionViewDirection ), 0.0 );
const fresnel = pow( float( 1.0 ).sub( nDotV ), 3.0 );
```

#### 3. Inspecting generated WGSL / GLSL

```js
const { vertexShader, fragmentShader } = await renderer.debug.getShaderAsync( scene, camera, mesh );
console.log( fragmentShader );
```

---

### 14.3 Classic `WebGLRenderer`: `onBeforeCompile` and `ShaderMaterial` rules

When running on `WebGLRenderer`:

1. **Extend built-in PBR with `onBeforeCompile` first** (`§4.6`) rather than writing a raw `ShaderMaterial` that loses IBL, shadows, fog, and tone mapping.
   - Key vertex injection anchors: `#include <beginnormal_vertex>` (`vec3 objectNormal`), `#include <begin_vertex>` (`vec3 transformed = vec3( position )`), `#include <project_vertex>`.
   - Key fragment injection anchors: `#include <color_fragment>` (`diffuseColor`), `#include <roughnessmap_fragment>` (`roughnessFactor`), `#include <opaque_fragment>` (final output before tone mapping — there is **no** `#include <output_fragment>`).
   - Always define `material.customProgramCacheKey = () => '...'` when `onBeforeCompile` branches on per-material options.
2. **If you must use `ShaderMaterial`:**
   - Leave `glslVersion` unset (`ShaderMaterial` already compiles as GLSL ES 3.00 and aliases `gl_FragColor`, `attribute`, `varying`, `texture2D`). Setting `glslVersion: THREE.GLSL3` removes `gl_FragColor` and breaks `#include <tonemapping_fragment>`.
   - End the fragment shader with:
     ```glsl
     gl_FragColor = vec4( linearColor, alpha );
     #include <tonemapping_fragment>
     #include <colorspace_fragment>
     ```
     Without those two includes, linear `THREE.Color` uniforms and linear lighting values skip tone mapping and sRGB output encoding.
   - On an `InstancedMesh`, multiply by `instanceMatrix` (`projectionMatrix * modelViewMatrix * instanceMatrix * vec4( position, 1.0 )`).
   - Keep space consistent: `normalMatrix * normal` is **view space**; `cameraPosition` is **world space**. Do not dot them together without transforming both to the same space.

---

### 14.4 Common mistakes

| Wrong | Right (r187) | Why |
|---|---|---|
| `transformedNormalView` / `transformedNormalWorld` in TSL | `normalView` / `normalWorld` | Removed in r187 (#34517). |
| `import { ... } from 'three/nodes'` | `import { ... } from 'three/tsl'` and `'three/webgpu'` | `'three/nodes'` does not exist in package exports. |
| `#include <output_fragment>` in `onBeforeCompile` | `#include <opaque_fragment>` | Chunk is named `opaque_fragment`; `.replace` on `output_fragment` silently no-ops. |
| `ShaderMaterial` on `WebGPURenderer` | `*NodeMaterial` with TSL | `WebGPURenderer` logs `"ShaderMaterial is not compatible"` and drops the shader. |
| `dot( normalize( cameraPosition - vWorldPos ), normalize( normalMatrix * normal ) )` | Use view space for both (`-mvPosition.xyz` and `normalMatrix * normal`) or world space for both | Mixing world-space view vector with view-space normal causes rim lighting to drift as the camera rotates. |
| `ShaderMaterial` without `<tonemapping_fragment>` and `<colorspace_fragment>` | Append both chunks after writing `gl_FragColor` | Raw linear values bypass AgX/Neutral tone mapping and sRGB encoding. |
