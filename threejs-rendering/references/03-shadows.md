> Part of the `threejs-rendering` skill. Verified against three r187 (2026-10-31); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# 3. Shadow engineering

### 3.1 The configuration chain

```js
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap;  // soft Vogel-disk PCF (r182+); or THREE.VSMShadowMap
renderer.shadowMap.autoUpdate = true;          // false + .needsUpdate = true for static scenes

sun.castShadow = true;
sun.shadow.mapSize.set( 2048, 2048 );          // 4096 on desktop hero shots; 1024 on mobile
sun.shadow.radius = 2;                         // PCF: kernel radius in shadow texels (default 1)
sun.shadow.intensity = 1;                      // r166+; <1 is an artistic cheat, it breaks energy
mesh.castShadow = mesh.receiveShadow = true;
```

| Filter | Mechanism (r187) | Strengths | Failure modes |
|---|---|---|---|
| `PCFShadowMap` | 5 Vogel-disk taps × hardware 2×2 comparison (~20 filtered taps), rotated per pixel by IGN; `radius` scales the disk | Stable, cheap, no light bleeding; noise resolves well under TRAA | Uniform penumbra width: no contact hardening |
| `VSMShadowMap` | Moments + separable blur; `radius` and `blurSamples` (default 8) | Very soft, wide penumbrae; blur cost independent of receivers | **Light bleeding** where occluders overlap. "All shadow receivers will also cast shadows" (constants.js doc). Back faces are not flipped (see §3.3). |
| PCSS (contact hardening) | Not built in. `webgl_shadowmap_pcss` patches the shader chunks with a blocker search | Penumbra grows with blocker distance: very realistic | Two to three times the cost of PCF; maintain the shader patch per release |

### 3.2 Fitting the orthographic shadow frustum

Shadow resolution is spent across `right − left` metres. Fitting a 20 m area instead of 200 m gives 10× sharper shadows at the same `mapSize`.

- **Math.** Transform the 8 corners of the receiver bounds into light view space (`shadow.camera.matrixWorldInverse`; the camera looks down −Z). The light-space AABB then gives: left = min x, right = max x, bottom = min y, top = max y, near = −max z, far = −min z, each padded by a margin.
- **Shimmer** comes from two sources: the frustum size changing as the light rotates, and sub-texel translation. The *stable* mode uses the bounding-sphere diameter (constant under rotation) and snaps the centre to whole texels.

```js
import * as THREE from 'three';

const _corners = Array.from( { length: 8 }, () => new THREE.Vector3() );
const _box = new THREE.Box3();
const _sphere = new THREE.Sphere();
const _c = new THREE.Vector3();

/**
 * Fit a DirectionalLight's orthographic shadow camera to a world-space Box3.
 * mode 'tight'  : light-space AABB of the 8 box corners (best texel density; use for static scenes).
 * mode 'stable' : bounding-sphere square (size invariant under light rotation) + texel snapping
 *                 (no shimmer when the light or the content moves; ~1.4–1.7x lower density).
 * Returns the world-space size of one shadow texel, which drives bias tuning.
 */
export function fitDirectionalShadow( light, worldBox, { mode = 'tight', margin = 0.25 } = {} ) {

	const shadow = light.shadow;
	const cam = shadow.camera;

	light.updateMatrixWorld();
	light.target.updateMatrixWorld();
	shadow.updateMatrices( light ); // positions + orients shadow.camera exactly as the renderer will
	const view = cam.matrixWorldInverse; // world -> light view space (camera looks down -Z)

	let minX, maxX, minY, maxY, minZ, maxZ;

	if ( mode === 'tight' ) {

		const { min, max } = worldBox;
		let i = 0;
		for ( const x of [ min.x, max.x ] ) for ( const y of [ min.y, max.y ] ) for ( const z of [ min.z, max.z ] ) {

			_corners[ i ++ ].set( x, y, z ).applyMatrix4( view );

		}

		_box.setFromPoints( _corners );
		( { x: minX, y: minY, z: minZ } = _box.min );
		( { x: maxX, y: maxY, z: maxZ } = _box.max );

	} else {

		worldBox.getBoundingSphere( _sphere );
		_c.copy( _sphere.center ).applyMatrix4( view );
		const r = _sphere.radius;
		// snap the square's centre to whole texels so rasterisation is stable frame to frame
		const texel = ( 2 * ( r + margin ) ) / shadow.mapSize.x;
		const cx = Math.round( _c.x / texel ) * texel;
		const cy = Math.round( _c.y / texel ) * texel;
		minX = cx - r; maxX = cx + r; minY = cy - r; maxY = cy + r;
		minZ = _c.z - r; maxZ = _c.z + r;

	}

	cam.left = minX - margin;
	cam.right = maxX + margin;
	cam.bottom = minY - margin;
	cam.top = maxY + margin;
	cam.near = - maxZ - margin; // may be negative for an orthographic camera; that is valid
	cam.far = - minZ + margin;
	cam.updateProjectionMatrix();

	return ( cam.right - cam.left ) / shadow.mapSize.x;

}

/** Starting bias values derived from the fitted frustum (tune from here, not from magic numbers). */
export function suggestShadowBias( light, texelWorld ) {

	const depthRange = light.shadow.camera.far - light.shadow.camera.near;
	return {
		normalBias: texelWorld * 1.0, // world units along the surface normal: ~1 texel
		bias: - Math.min( 0.0005, ( 0.25 * texelWorld ) / depthRange ), // normalized depth; ≈ ¼ texel in world units
	};

}

// usage
// const texel = fitDirectionalShadow( sun, new THREE.Box3().setFromObject( receivers ), { mode: 'stable' } );
// Object.assign( sun.shadow, suggestShadowBias( sun, texel ) );
```

*Tested:* `fitShadow.test.mjs` fitted 2,000 random boxes against random light positions in both modes and projected every corner through `shadow.matrix`. All corners landed inside [0, 1]³. In stable mode the frustum width stayed identical across 63 light angles. A mutated copy (margin −1) failed 9,012 corner checks, which shows the test can fail.

**Large worlds: cascaded shadow maps.**
- WebGL: `const csm = new CSM( { camera, parent: scene, cascades: 4, maxFar: 200, mode: 'practical', shadowMapSize: 2048, lightDirection, lightIntensity: 3 } )`. Call `csm.setupMaterial( material )` for every receiving material, `csm.update()` every frame, and `csm.updateFrustums()` on resize or FOV change.
- WebGPU: `light.shadow.shadowNode = new CSMShadowNode( light, { cascades: 4, maxFar: 200, mode: 'practical', lightMargin: 50 } )`.
- r186+: `SunLight` (needs `SunLight.registerNode( SunLightNode )` on WebGPU) gives a turnkey 2-cascade atlas. Its own docs warn it is wrong for small bounded scenes such as dioramas, rooms or model viewers: use a fitted single map there.

### 3.3 Shadow acne and peter-panning: the math behind the numbers

- **`shadow.bias`** is added to the receiver's normalized shadow depth (`shadowCoord.z += bias`). For an orthographic light that depth is linear over `far − near`, so

$$\Delta_{world} = \text{bias} \times (\text{far} - \text{near})$$

  `-0.0005` over a 100 m depth range is a **5 cm** offset: visible peter-panning at a table leg. The same value over a fitted 10 m range is 5 mm. **Tight near/far planes come first. Bias comes second.**
- **`shadow.normalBias`** offsets the lookup position along the world-space normal, in metres. It fixes grazing-angle acne without detaching contact shadows as quickly as depth bias does. Scale it to the texel footprint: normalBias ≈ 0.5–1.5 × texel size, where texel size = (right − left) / mapSize.x. The brief's 0.02–0.05 range is correct for 2–5 cm texels (for example, a 40 m frustum on a 2048 map ≈ 2 cm).
- **Default face culling (`shadowSide`).** In r187 `WebGLShadowMap` renders the **opposite** side for PCF/Basic: FrontSide materials draw back faces into the map. Acne therefore moves to the unlit back side, which N·L already darkens. The cost is peter-panning equal to the object's thickness, and broken shadows from open meshes such as single planes or leaves. For **VSM**, the material's own side is used. For thin or open geometry set `material.shadowSide = THREE.DoubleSide`.
- **Tuning procedure:** (1) fit the frustum; (2) set `normalBias = texel`; (3) raise `|bias|` in steps of 1e-4 only until acne disappears on surfaces facing the light; (4) if contact gaps appear, lower bias and raise `mapSize` or tighten the fit instead. For `SpotLight`, depth is perspective and non-linear, so the effect of bias grows with distance. Raise `shadow.camera.near` and use `shadow.focus` (0–1) to tighten the frustum.

### 3.4 Contact and accumulated shadows (grounding)

| Technique | Implementation | Use |
|---|---|---|
| **Contact shadow plane** | `webgl_shadow_contact` / `webgpu_shadow_contact`: an orthographic camera looks up from the floor, renders a depth-darkened pass of the object, blurs it H/V, and projects the result onto a transparent plane | Product shots, model viewers: the cheapest believable grounding |
| **Screen-space shadows** | `sss( depthNode, camera, mainLight )` (`SSSNode`, WebGPU): ray-marches depth toward the light; `maxDistance` 0.1, `thickness` 0.01, `shadowIntensity` | Fine contact detail that shadow maps miss (fingers on a table, gaps under objects) |
| **GTAO / N8AO** | §5 | Crease and contact occlusion of indirect light |
| **Progressive accumulation** | `ProgressiveLightMap` from `misc/ProgressiveLightMap.js` (WebGL), or the class of the same name exported by `misc/ProgressiveLightMapGPU.js` (WebGPU): `addObjectsToLightMap( objects )`, then `update( camera, blendWindow = 100, blurEdges = true )` per frame while jittering light positions; needs a `uv1` set | Soft area-light shadows baked in seconds at load. R3F equivalent: drei `<AccumulativeShadows>` |
| **Baked AO/shadow textures** | Bake in Blender to `aoMap` on `uv1`; glTF `occlusionTexture` with `texCoord: 1` | Static props and architecture |
