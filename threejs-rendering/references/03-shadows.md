> Part of the `threejs-rendering` skill. Verified against three r187 (`0.187.0`); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

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
| `PCFShadowMap` | 5 Vogel-disk taps × hardware 2×2 comparison (~20 filtered taps), rotated per pixel by IGN; `radius` scales the disk | Stable, cheap, no light bleeding; noise resolves well under TRAA/TAAU | Uniform penumbra width: no contact hardening |
| `VSMShadowMap` | Moments + separable blur; `radius` and `blurSamples` (default 8) | Very soft, wide penumbrae; blur cost independent of receivers | **Light bleeding** where occluders overlap. "All shadow receivers will also cast shadows" (`constants.js`). Back faces are not flipped (see §3.3). |
| PCSS (contact hardening) | Not built in. `webgl_shadowmap_pcss` patches the shader chunks with a blocker search | Penumbra grows with blocker distance: very realistic | Two to three times the cost of PCF; maintain the shader patch per release |

### 3.2 Fitting the orthographic shadow frustum (zero-import helper)

Shadow resolution is spent across `right − left` metres. Fitting a 20 m area instead of 200 m gives 10× sharper shadows at the same `mapSize`.

- **Math.** Transform the 8 corners of the receiver bounds into light view space (`shadow.camera.matrixWorldInverse`; the camera looks down −Z). The light-space AABB then gives: `left = minX`, `right = maxX`, `bottom = minY`, `top = maxY`, `near = −maxZ`, `far = −minZ`, each padded by `margin`.
- **Shimmer & texel-snap compensation.** Shimmer comes from frustum width changing under light rotation and sub-texel centre drift. In `stable` mode, use the bounding-sphere radius `r` (invariant under rotation) and solve `halfW = (r + margin) + 0.5 * texel` with `texel = (2 * halfW) / N` → `texel = 2 * (r + margin) / (N − 1)`. That keeps width 100% invariant, aligns the snap step to exact texel width, and guarantees `|cx − p.x| ≤ 0.5 * texel` never clips box corners even at `margin = 0`.

```js
// Zero-import helper (matches scripts/fit-shadow.mjs)
export function fitDirectionalShadow( light, worldBox, { mode = 'tight', margin = 0.25 } = {} ) {

	const shadow = light.shadow;
	const cam = shadow.camera;
	const { min, max } = worldBox;
	const p = min.clone();

	light.updateMatrixWorld();
	light.target.updateMatrixWorld();
	shadow.updateMatrices( light ); // positions + orients shadow.camera exactly as the renderer will
	const view = cam.matrixWorldInverse; // world -> light view space (camera looks down -Z)

	const r = 0.5 * Math.hypot( max.x - min.x, max.y - min.y, max.z - min.z );
	const eps = Math.max( 1e-5, r * 1e-5 );

	if ( mode === 'tight' ) {

		let minX = Infinity, maxX = - Infinity, minY = Infinity, maxY = - Infinity, minZ = Infinity, maxZ = - Infinity;
		for ( const x of [ min.x, max.x ] ) for ( const y of [ min.y, max.y ] ) for ( const z of [ min.z, max.z ] ) {

			p.set( x, y, z ).applyMatrix4( view );
			if ( p.x < minX ) minX = p.x; if ( p.x > maxX ) maxX = p.x;
			if ( p.y < minY ) minY = p.y; if ( p.y > maxY ) maxY = p.y;
			if ( p.z < minZ ) minZ = p.z; if ( p.z > maxZ ) maxZ = p.z;

		}

		const pad = margin + eps;
		cam.left = minX - pad; cam.right = maxX + pad;
		cam.bottom = minY - pad; cam.top = maxY + pad;
		cam.near = - maxZ - pad; cam.far = - minZ + pad;

	} else {

		p.set( 0.5 * ( min.x + max.x ), 0.5 * ( min.y + max.y ), 0.5 * ( min.z + max.z ) ).applyMatrix4( view );
		const padR = r + margin + eps;
		const nx = Math.max( 2, shadow.mapSize.x ), ny = Math.max( 2, shadow.mapSize.y );
		const texelX = ( 2 * padR ) / ( nx - 1 ), texelY = ( 2 * padR ) / ( ny - 1 );
		const halfW = 0.5 * nx * texelX, halfH = 0.5 * ny * texelY;
		const cx = Math.round( p.x / texelX ) * texelX, cy = Math.round( p.y / texelY ) * texelY;
		cam.left = cx - halfW; cam.right = cx + halfW;
		cam.bottom = cy - halfH; cam.top = cy + halfH;
		cam.near = - ( p.z + padR ); cam.far = - ( p.z - padR );

	}

	cam.updateProjectionMatrix();
	shadow.updateMatrices( light ); // ensures light.shadow.matrix is immediately up to date on return
	return ( cam.right - cam.left ) / shadow.mapSize.x;

}

export function suggestShadowBias( light, texelWorld ) {

	const depthRange = light.shadow.camera.far - light.shadow.camera.near;
	return {
		normalBias: texelWorld * 1.0, // world units along the surface normal: ~1 texel
		bias: - Math.min( 0.0005, ( 0.25 * texelWorld ) / depthRange ), // normalized depth; ≈ ¼ texel in world units
	};

}
```

*Tested:* `scripts/fit-shadow.test.mjs` fitted 2,000 random boxes (including `margin = 0` and coarse `64×64` shadow maps) against random light positions in both modes and projected every corner through `light.shadow.matrix` without a second `updateMatrices()` call. All corners landed inside `[0, 1]³`, `stable` width had `1` distinct value across 63 light angles, and a negative-margin check clipped all 8 corners.

**Large worlds: cascaded & tiled shadow maps.**
- **WebGL CSM:** `const csm = new CSM( { camera, parent: scene, cascades: 4, maxFar: 200, mode: 'practical', shadowMapSize: 2048, lightDirection, lightIntensity: 3 } )` (`'three/addons/csm/CSM.js'`). Call `csm.setupMaterial( material )` for every receiving material, `csm.update()` every frame, and `csm.updateFrustums()` on resize or FOV change.
- **WebGPU CSM:** `light.shadow.shadowNode = new CSMShadowNode( light, { cascades: 4, maxFar: 200, mode: 'practical', lightMargin: 50 } )` (`'three/addons/csm/CSMShadowNode.js'`).
- **WebGPU Tiled Shadows (`TileShadowNode`):** `light.shadow.shadowNode = new TileShadowNode( light, { tilesX: 2, tilesY: 2 } )` (`'three/addons/tsl/shadows/TileShadowNode.js'`) splits a large static or semi-static directional frustum into high-resolution tiles without cascade seam transitions.
- **r186+ `SunLight`:** `'three/addons/lights/SunLight.js'` (needs `SunLight.registerNode( SunLightNode )` on WebGPU) gives a turnkey 2-cascade directional atlas for outdoor landscapes. For bounded rooms, dioramas, or product viewers, use a single fitted `DirectionalLight` instead.

### 3.3 Shadow acne, peter-panning and transparent shadow casters

- **`shadow.bias`** is added to the receiver's normalized shadow depth (`shadowCoord.z += bias`). For an orthographic light that depth is linear over `far − near`, so

$$\Delta_{world} = \text{bias} \times (\text{far} - \text{near})$$

  `-0.0005` over a 100 m depth range is a **5 cm** offset: visible peter-panning at a table leg. The same value over a fitted 10 m range is 5 mm. **Tight near/far planes come first. Bias comes second.**
- **`shadow.normalBias`** offsets the lookup position along the world-space normal, in metres. Scale it to the texel footprint: `normalBias ≈ 0.5–1.5 × texelWorld`, where `texelWorld = (right − left) / mapSize.x`.
- **Default face culling (`shadowSide`).** In r187 both `WebGLShadowMap` and `WebGPURenderer` render the **opposite** side for PCF/Basic: `FrontSide` materials draw back faces into the map, moving acne onto unlit back faces at the cost of peter-panning on paper-thin geometry. For **VSM**, the material's own side is used. For thin or open meshes (leaves, cloth, planes) set `material.shadowSide = THREE.DoubleSide`.
- **Cutout, stochastic, and tinted shadows (`WebGPURenderer`):**
  - Foliage/grate cutouts: `material.alphaTest = 0.5` automatically clips the shadow map.
  - Soft dithered cutouts without sorting: `material.alphaHash = true` casts stippled stochastic shadows too.
  - Colored glass / stained-glass shadows: set `renderer.shadowMap.transmitted = true` and assign `material.castShadowNode = vec4( tintRGB, shadowOpacity )` on the transmissive caster. (Note: for opaque `NodeMaterialInstance` meshes, see `§4.7` so `materialReference` does not run on `ShadowMaterial`.)
- **Tuning procedure:** (1) fit the frustum; (2) set `normalBias = texel`; (3) raise `|bias|` in steps of 1e-4 only until acne disappears on surfaces facing the light; (4) if contact gaps appear, lower bias and raise `mapSize` or tighten the fit instead. For `SpotLight`, raise `shadow.camera.near` and use `shadow.focus` (0–1) to tighten the perspective frustum.

### 3.4 Contact and accumulated shadows (grounding)

| Technique | Implementation | Use |
|---|---|---|
| **Contact shadow plane** | `webgl_shadow_contact` / `webgpu_shadow_contact`: an orthographic camera looks up from the floor, renders a depth-darkened pass of the object, blurs it H/V, and projects the result onto a transparent plane | Product shots, model viewers: the cheapest believable grounding |
| **Screen-space shadows** | `sss( depthNode, camera, mainLight )` (`'three/addons/tsl/display/SSSNode.js'`, WebGPU): ray-marches depth toward the light; `maxDistance` 0.1, `thickness` 0.01, `shadowIntensity` | Fine contact detail that shadow maps miss (fingers on a table, gaps under objects) |
| **GTAO / N8AO** | §5 | Crease and contact occlusion of indirect light |
| **Progressive accumulation** | `ProgressiveLightMap` from `'three/addons/misc/ProgressiveLightMap.js'` (WebGL) or `'three/addons/misc/ProgressiveLightMapGPU.js'` (WebGPU): `addObjectsToLightMap( objects )`, then `update( camera, blendWindow = 100, blurEdges = true )` per frame while jittering light positions; needs a `uv1` set | Soft area-light shadows baked in seconds at load. R3F WebGL equivalent: drei `<AccumulativeShadows>` |
| **Baked AO/shadow textures** | Bake in Blender to `aoMap` on `uv1`; glTF `occlusionTexture` with `texCoord: 1` | Static props and architecture |
