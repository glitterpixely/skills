> Part of the `threejs-rendering` skill. Verified against three r187 (2026-10-31); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# 15. React Three Fiber 9.8 and `@react-three/drei` 10.7

Targets `@react-three/fiber@9.8.x` (React 19), `@react-three/drei@10.7.x`, and `gltfjsx@6.5.x` on `three@0.186–0.187`. Every photoreal and performance rule in `§1–§9` still applies inside React.

---

### 15.1 Photoreal `<Canvas>` setup (AgX/Neutral, shadows, WebGL2 & WebGPU)

By default, R3F's `<Canvas>` sets `ACESFilmicToneMapping` and maps `<Canvas shadows>` (`true` or `'soft'`) to `PCFSoftShadowMap` (which logs a deprecation/removal warning on r182–r187). Override both explicitly so R3F follows the `threejs-rendering` rulebook:

#### WebGL2 `<Canvas>`

```jsx
import * as THREE from 'three';
import { Canvas } from '@react-three/fiber';

export function SceneCanvas( { children } ) {

	return (
		<Canvas
			shadows="percentage" // maps to THREE.PCFShadowMap without triggering the PCFSoftShadowMap warning
			dpr={ [ 1, 2 ] }
			camera={ { position: [ 0, 1.6, 4.5 ], fov: 45, near: 0.1, far: 100 } }
			gl={ {
				antialias: true,
				toneMapping: THREE.AgXToneMapping, // or THREE.NeutralToneMapping for product/brand accuracy
				toneMappingExposure: 1.0,
			} }
		>
			{ children }
		</Canvas>
	);

}
```

#### WebGPU `<Canvas>` (async `gl` factory + `extend(THREE)`)

Pass an `async (props) => { ... }` factory to `gl`, await `renderer.init()`, and register node materials with `extend(THREE)`:

```jsx
import * as THREE from 'three/webgpu';
import { color } from 'three/tsl';
import { Canvas, extend } from '@react-three/fiber';
import { useMemo } from 'react';

extend( THREE ); // registers meshPhysicalNodeMaterial, meshStandardNodeMaterial, etc.

function HeroMesh() {

	// Build TSL node graphs ONCE in useMemo or module scope (rebuilding every render skips recompile unless needsUpdate=true)
	const albedoNode = useMemo( () => color( 0xc89b6e ), [] );
	return (
		<mesh castShadow receiveShadow>
			<torusKnotGeometry args={ [ 0.6, 0.2, 128, 32 ] } />
			<meshPhysicalNodeMaterial colorNode={ albedoNode } roughness={ 0.25 } clearcoat={ 0.5 } />
		</mesh>
	);

}

export function WebGPUSceneCanvas() {

	return (
		<Canvas
			shadows="percentage"
			dpr={ [ 1, 2 ] }
			camera={ { position: [ 0, 1.5, 4 ], fov: 45 } }
			gl={ async ( props ) => {

				const renderer = new THREE.WebGPURenderer( { ...props, antialias: true } );
				await renderer.init();
				renderer.toneMapping = THREE.AgXToneMapping;
				renderer.toneMappingExposure = 1.0;
				return renderer;

			} }
		>
			<HeroMesh />
		</Canvas>
	);

}
```

> **Note on `state.clock` & `state.renderer`:** `@react-three/fiber@9.8` exposes `state.renderer` as an alias for `state.gl` (and `@react-three/fiber/legacy` if a legacy app must opt out of automatic `ColorManagement`). Internally R3F 9.8 still constructs a `THREE.Clock` on `state.clock`, so three r183+ logs one `THREE.Clock: This module has been deprecated` warning at Canvas startup. Inside `useFrame((state, delta) => ...)`, always use the `delta` parameter and `state.clock.elapsedTime` (never call `state.clock.getElapsedTime()`, which calls `getDelta()` and zeroes the next frame's delta).

---

### 15.2 JSX scene graph, `args`, `<primitive>`, and TypeScript collisions

- **Constructor `args`:** Changing `args={[...]}` destroys and recreates the underlying Three.js instance. Animate scale, transforms, or uniforms instead of mutating geometry `args` each frame.
- **Read-only vector/euler props:** Pass arrays (`position={[1, 2, 3]}`), scalars (`scale={0.5}`), or `Vector3` instances—never plain `{ x, y, z }` objects (throws `Cannot assign to read only property 'position'`).
- **Pierced props:** Use dashed props (`rotation-y={Math.PI}`, `material-roughness={0.3}`, `shadow-mapSize={[2048, 2048]}`, `shadow-normalBias={0.015}`).
- **Mounting loaded/external objects:** Use `<primitive object={model} />`. R3F **never** auto-disposes `<primitive>` objects on unmount; dispose them explicitly when evicting assets.
- **Skinned glTF clones in React:**
  ```jsx
  import * as SkeletonUtils from 'three/addons/utils/SkeletonUtils.js';
  const { scene } = useGLTF( '/character.glb' );
  const clone = useMemo( () => SkeletonUtils.clone( scene ), [ scene ] );
  return <primitive object={ clone } />;
  ```
- **TypeScript tag collisions:** `<line>`, `<audio>`, `<source>`, and `<path>` collide with SVG/HTML intrinsic types in TSX. Write `<threeLine>`, `<threeAudio>`, `<threeSource>`, `<threePath>`.

---

### 15.3 `useFrame` rules and on-demand rendering

1. **Never call `setState` inside `useFrame`:** Mutate refs (`meshRef.current.position.x = ...`) or uniform `.value` properties directly. Calling React `setState` triggers 60 Hz component re-renders.
2. **Positive `renderPriority` disables automatic Canvas rendering:** Passing `useFrame(fn, 1)` tells R3F that your callback owns the render call (`state.gl.render(state.scene, state.camera)` or `pipeline.render()`). Leave priority at `0` (default) for normal animation hooks.
3. **`frameloop="demand"` + transient Zustand subscriptions:** Ideal for product configurators, architectural viewers, and static scenes. React prop/state updates and `<OrbitControls makeDefault />` automatically call `invalidate()`. For high-frequency sliders or external state without React re-renders, subscribe transiently inside `useEffect` and call `invalidate()`:
   ```jsx
   const invalidate = useThree( ( s ) => s.invalidate );
   useEffect( () => useConfigStore.subscribe(
     ( s ) => s.roughness,
     ( v ) => { matRef.current.roughness = v; invalidate(); }
   ), [ invalidate ] );
   ```

---

### 15.3b Post-processing in R3F (WebGL2 `@react-three/postprocessing` vs WebGPU `RenderPipeline`)

- **WebGL2 `<Canvas>` (`@react-three/postprocessing@3.2` + `postprocessing@6.39.6`):** Set `gl={{ toneMapping: THREE.NoToneMapping, reversedDepthBuffer: false }}` on `<Canvas>`, mount `<EffectComposer multisampling={0}>`, keep `<N8AO halfRes={false} />` on r187 (`§5.4`), place `<Bloom luminanceThreshold={1} mipmapBlur />` before `<ToneMapping mode={ToneMappingMode.AGX} />`, and keep `<SMAA />` separate from `<ChromaticAberration />`.
- **WebGPU `<Canvas>` (native TSL `RenderPipeline`):** `@react-three/postprocessing` wraps WebGL `postprocessing` and **cannot** run on `WebGPURenderer`. Instead, construct `THREE.RenderPipeline` (`§5.3`, `§5.5`) and take over R3F's render pass with positive priority `1`:
  ```jsx
  import * as THREE from 'three/webgpu';
  import { pass, renderOutput } from 'three/tsl';
  import { bloom } from 'three/addons/tsl/display/BloomNode.js';
  import { useFrame, useThree } from '@react-three/fiber';
  import { useEffect, useMemo } from 'react';

  export function WebGPUPost() {

    const { gl, scene, camera } = useThree();
    const pipeline = useMemo( () => {

      const p = new THREE.RenderPipeline( gl );
      p.outputColorTransform = false;
      const scenePass = pass( scene, camera );
      const hdr = scenePass.add( bloom( scenePass, 0.18, 0.5, 1.0 ) );
      p.outputNode = renderOutput( hdr );
      return p;

    }, [ gl, scene, camera ] );

    useEffect( () => () => pipeline.dispose(), [ pipeline ] );
    useFrame( () => { pipeline.render(); }, 1 ); // priority 1 disables R3F's default gl.render()
    return null;

  }
  ```

---

### 15.4 `@react-three/drei` 10.7 WebGPU compatibility matrix

Checked against `@react-three/fiber@9.8.2` and `@react-three/drei@10.7.9` on `WebGPURenderer` (native WebGPU + `forceWebGL: true`):

| `drei` Helper | WebGL2 | WebGPU | Notes & Caveats |
|---|---|---|---|
| `useGLTF`, `useTexture`, `useProgress`, `<Preload all />` | Yes | Yes | `useGLTF` auto-wires Draco & Meshopt. Put `<Preload all />` inside `<Suspense>` after models. |
| `<OrbitControls makeDefault />`, `<CameraControls />` | Yes | Yes | `regress` lowers DPR during drags when paired with `<AdaptiveDpr />`. |
| `<Environment files="studio.hdr" />` / `preset="..."` | Yes | Yes | `.hdr` files and presets work on both backends. |
| `<Environment>` with `<Lightformer>` children or `ground` | Yes | **Broken** | `ground` uses a `ShaderMaterial`; `<Environment>` children bake via cube camera that renders black on WebGPU's WebGL2 fallback. Use `.hdr`/`.exr` files on WebGPU. |
| `<Instances>` / `<Instance>`, `<Detailed>` (LOD) | Yes | Yes | Declarative `InstancedMesh` and `THREE.LOD`. |
| `<Bvh firstHitOnly>` | Yes | Yes | Wraps child meshes in `three-mesh-bvh` (`O(log N)` CPU raycasts; crucial for complex glTFs). |
| `<Center>`, `<Bounds fit clip observe>` | Yes | Yes | Do not wrap `drei` `<Text>` inside `<Center>` (`Text` geometry is a unit quad; use `anchorX`/`anchorY`). |
| `<Html portal={overlayRef}>` | Yes | Yes (except `occlude="blending"`) | On React 19.2 + R3F 9.8, always pass `portal={overlayRef}` pointing to a fixed sibling `<div ref={overlayRef} />` outside `<Canvas>` so initial mount is never blank. |
| `<ContactShadows>` | Yes | **No** | Uses `ShaderMaterial` + `onBeforeCompile` blur passes (`not compatible` on `WebGPURenderer`). |
| `<Text>` (troika SDF) | Yes | **No** | Troika injects its SDF shader via `onBeforeCompile`; draws an untextured quad on `WebGPURenderer`. |

---

### 15.5 Generating typed R3F components with `gltfjsx`

```bash
npx gltfjsx@latest model.glb --types --keepnames
```

- **Warning on `gltfjsx --transform`:** Like `gltf-transform optimize` with default flags (`§6.2`), `gltfjsx --transform` runs aggressive simplification, palette merging, WebP color re-encoding, and JPEG normal-map re-encoding. For hero photoreal assets, run the controlled 3-stage `gltf-transform` pipeline from `§6.2` first, then run `npx gltfjsx out.glb --types` **without** `--transform`.

---

### 15.5b Physics (`@react-three/rapier@2.2`) and WebXR (`@react-three/xr@6.6`)

- **Physics (`@react-three/rapier`):** Wrap interactive rigid bodies in `<Suspense>` + `<Physics>` (runs deterministic WASM Rapier on an interpolated fixed timestep). Prefer primitive colliders (`cuboid`, `ball`, `capsule`) or `colliders="hull"` on dynamic bodies; reserve `colliders="trimesh"` for static level geometry. Drive kinematic platforms in `useFrame` via `bodyRef.current?.setNextKinematicTranslation(...)`, never by mutating React `position` props.
- **WebXR (`@react-three/xr` v6):** Create a store outside React with `const xrStore = createXRStore()`, trigger sessions from DOM buttons via `xrStore.enterVR()` / `xrStore.enterAR()`, and wrap scene content in `<XR store={xrStore}><XROrigin position={[0, 0, 2]} />...</XR>` (move `<XROrigin>` for locomotion rather than the headset camera).

---

### 15.6 Common mistakes

| Wrong | Right (r187) | Why |
|---|---|---|
| `<Canvas shadows>` | `<Canvas shadows="percentage">` | Boolean `shadows` selects removed `PCFSoftShadowMap` and logs a warning. |
| `useFrame((state) => { const t = state.clock.getElapsedTime(); })` | `useFrame((state, delta) => { const t = state.clock.elapsedTime; })` | `getElapsedTime()` internally calls `getDelta()`, corrupting `delta` for subsequent subscribers. |
| `useFrame((_, dt) => setAngle((a) => a + dt))` | `useFrame((_, dt) => { ref.current.rotation.y += dt; })` | Calling React `setState` every frame stalls the main thread. |
| `<mesh position={{ x: 0, y: 1, z: 0 }}>` | `<mesh position={[0, 1, 0]}>` | `Object3D.position` is read-only; R3F unpacks arrays via `.fromArray()`. |
| `gl={new THREE.WebGPURenderer()}` | `gl={async (props) => { const r = new THREE.WebGPURenderer(props); await r.init(); return r; }}` | Renderer must bind R3F's canvas props and resolve `await r.init()` before first render. |
