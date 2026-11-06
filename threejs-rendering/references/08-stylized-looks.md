> Part of the `threejs-rendering` skill. Verified against three r187 (2026-10-31); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# 8. Stylized and hybrid looks on the same pipeline

Photorealism is the default target. The skill must also handle deliberate departures from it: toon/cel, anime, outlines, painterly, low-poly, pixel art, retro, and hybrid "stylized-real". The rule that keeps these looks robust is **depart on purpose, one layer at a time**. A look is a set of choices on four layers: shading, edges, colour and post. Everything else in §1–§6 still applies: the linear workflow, metres, fitted shadows, asset compression and disposal.

### 8.1 What stays and what changes

| Layer | Photoreal default | Stylized departure | Keep regardless |
|---|---|---|---|
| Shading | Physical BRDF, IBL | Quantized ramps, unlit art-directed shading, flat facets | Linear working space; hex colours read as sRGB |
| Edges | None (silhouettes from lighting) | Ink lines: inverted hull, screen-space depth/normal edges, geometric lines | Lines thicken with DPR: scale widths by `renderer.getPixelRatio()` |
| Colour | AgX / Neutral, HDR → display | **Palette fidelity**: `NeutralToneMapping`, or `NoToneMapping` when every value stays ≤ 1; LUT grade after tone mapping | `outputColorSpace = SRGBColorSpace` |
| Post | AO, SSR, TRAA, DOF, bloom, grain | Pixelation, posterize, Bayer dither, halftone, Kuwahara, CRT | Display-space effects run after `renderOutput()` |

> [!IMPORTANT]
> **AgX shifts stylized palettes.** Its inset matrix desaturates, and its sigmoid lifts shadows. A brand-orange cel band authored as `#ff7a2a` will not come out as `#ff7a2a`. For flat-colour styles use `NoToneMapping`, which passes colour through untouched up to 1.0 (it clips above), or `NeutralToneMapping`, which compresses only near white.

### 8.2 Toon, cel and anime shading

**Built-in toon (multi-light, receives shadows):** `MeshToonMaterial` (WebGL) / `MeshToonNodeMaterial` (WebGPU). `gradientMap` maps N·L to discrete light levels. Its docs require `NoColorSpace`, and without `NearestFilter` the bands blur into gradients.

```js
function makeToonRamp( levels = [ 0.18, 0.55, 1.0 ] ) {

	const data = new Uint8Array( levels.map( ( v ) => Math.round( v * 255 ) ) );
	const tex = new THREE.DataTexture( data, data.length, 1, THREE.RedFormat );
	tex.minFilter = THREE.NearestFilter;
	tex.magFilter = THREE.NearestFilter;
	tex.generateMipmaps = false;
	tex.needsUpdate = true;
	return tex; // NoColorSpace (default): the values are light levels, not colours

}

const toon = new THREE.MeshToonNodeMaterial( { color: 0xff8a5c, gradientMap: makeToonRamp() } );
```

- **2 bands** read as anime/cel; **3–4 bands** read as illustrated. The lowest level sets how dark the shadow side gets: keep it ≥ 0.15 so form survives.
- Toon shadows want hard edges: `shadow.radius = 1` and a tight frustum. Soft PCF penumbrae fight the banding.
- IBL still adds smooth ambient. For pure cel, lower `scene.environmentIntensity` to 0.1–0.3, or remove the environment.

**Art-directed anime shading (unlit, one key light, full control):** when the look needs a hue-shifted shadow colour, a hard terminator and a rim light, own the lighting in TSL on an unlit material:

```js
import * as THREE from 'three/webgpu';
import { uniform, normalWorld, positionWorld, cameraPosition, dot, smoothstep, mix, max, float, color, texture, uv } from 'three/tsl';

const keyDir = uniform( new THREE.Vector3( 0.4, 0.8, 0.45 ).normalize() ); // world space, toward the key light
const shadeTint = uniform( new THREE.Color( 0x7a6a9e ) );   // hue-shifted shadow multiplier, never black
const rimColor = uniform( new THREE.Color( 0xfff1e0 ) );
const bandEdge = uniform( 0.0 );                             // N·L where light becomes shadow
const bandSoft = uniform( 0.02 );                            // half-width of the terminator blend

function animeMaterial( baseMap = null ) {

	const m = new THREE.MeshBasicNodeMaterial();             // unlit: the shader owns the lighting
	const albedo = baseMap ? texture( baseMap, uv() ).rgb : color( 0xffd9c4 );
	const V = cameraPosition.sub( positionWorld ).normalize();
	const ndl = dot( normalWorld, keyDir );
	const lit = smoothstep( bandEdge.sub( bandSoft ), bandEdge.add( bandSoft ), ndl );
	const base = mix( albedo.mul( shadeTint ), albedo, lit );
	const fresnel = float( 1 ).sub( max( dot( normalWorld, V ), 0 ) );
	const rim = smoothstep( 0.62, 0.66, fresnel ).mul( lit );  // rim only on the lit side
	m.colorNode = base.add( rimColor.mul( rim ).mul( 0.6 ) );
	return m;

}
```

The trade-off: `MeshBasicNodeMaterial` receives **no shadow maps** and ignores scene lights. Copy `keyDir` from the sun every frame (`sun.position` minus `sun.target.position`, normalized). Use built-in toon wherever cast shadows matter.

**Anime production techniques** (*settled practice* in real-time anime rendering; none of these are three.js built-ins):
- **Face normals:** transfer normals from a sphere or ellipsoid proxy onto the face mesh (Blender *Data Transfer* modifier, custom normals). The cel terminator then sweeps cleanly across the face instead of breaking around the nose and eye sockets.
- **Face shadow SDF maps:** a greyscale threshold texture authored per face. Compute the light angle in head space (atan2 of the light direction projected on the head's XZ plane, relative to head-forward). Shade a pixel when `threshold < angle01`. Mirror the UV.x for light from the other side. This gives the hand-drawn nose and cheek shadow shapes.
- **Hair highlight:** a Kajiya-Kay band along the strand tangent, `pow( sqrt( 1 − dot(T,H)² ), exponent )`, or a painted highlight strip shifted along UV.v by `dot( N, V )`.
- **Shadow colour:** multiply by a hue-shifted tint (cooler, more saturated). Never darken toward grey or black.

### 8.3 Lines and outlines

| Method | API (r187) | Width behaviour | Catches | Cost and gotchas |
|---|---|---|---|---|
| Inverted hull | WebGPU `toonOutlinePass( scene, camera, color, thickness = 0.003, alpha )`; WebGL `OutlineEffect( renderer, { defaultThickness: 0.003, defaultColor: [0,0,0] } )`, per material `material.userData.outlineParameters = { thickness, color, alpha, visible }` | Grows with object size and distance unless compensated | Silhouettes only | `toonOutlinePass` outlines **only `MeshToonMaterial`/`MeshToonNodeMaterial`** (`ToonOutlinePassNode`: `isMeshToonMaterial || isMeshToonNodeMaterial`). It extrudes along `normalLocal`, so hard-edged meshes split at seams: smooth the normals, or bake smoothed normals into a custom attribute for a custom hull. About 2× draw calls. |
| Screen-space depth + normal edges | Custom TSL on `pass()` MRT (below); `pixelationPass` has the same idea built in | Constant pixel width | Silhouettes **and** creases | One fullscreen pass; needs a normal MRT; thresholds must scale with depth |
| Luminance edges | `sobel( node )` | Constant | Colour edges (texture detail too) | Noisy on textured surfaces; best for posterized styles |
| Selection outline | `outline( scene, camera, { selectedObjects, edgeThickness, edgeGlow, downSampleRatio } )` → `visibleEdge` / `hiddenEdge` (WebGL: `OutlinePass`) | Constant, soft | Selected objects, including occluded parts | UI highlighting, not ink lines |
| Geometric lines | `EdgesGeometry( geom, thresholdAngle )` → `LineSegmentsGeometry` + `LineSegments2` + `LineMaterial` (WebGL) / `Line2NodeMaterial` (WebGPU); `linewidth` in pixels, or world units with `worldUnits: true` | Exact | Feature edges by angle | CAD/technical look; set `LineMaterial.resolution` on resize (WebGL) |

**Screen-space ink lines (WebGPU):** relative depth threshold plus normal discontinuity over 4 neighbours:

```js
import { pass, mrt, output, normalView, screenUV, screenSize, vec2, vec4, float, abs, max, step, dot, mix, uniform, packNormalToRGB, unpackRGBToNormal, perspectiveDepthToViewZ, reference, Fn } from 'three/tsl';

const lineColor = uniform( new THREE.Color( 0x1b1420 ) );
const lineWidthPx = uniform( 1.0 );
const depthThreshold = uniform( 0.02 );   // relative: 2 % of the centre depth
const normalThreshold = uniform( 0.4 );   // summed (1 − n·n') over 4 neighbours
const passNear = reference( 'near', 'float', camera ); // the SCENE camera; global cameraNear/cameraFar
const passFar = reference( 'far', 'float', camera );   // resolve to the post quad's camera and break viewZ

const scenePass = pass( scene, camera );
scenePass.setMRT( mrt( { output, normal: packNormalToRGB( normalView ) } ) );
const sceneColor = scenePass.getTextureNode( 'output' );
const sceneNormal = scenePass.getTextureNode( 'normal' );
const sceneDepth = scenePass.getTextureNode( 'depth' );

const edgeMask = Fn( () => {

	const px = vec2( lineWidthPx ).div( screenSize );
	const viewDepth = ( o ) => perspectiveDepthToViewZ( sceneDepth.sample( screenUV.add( o ) ).r, passNear, passFar ).negate();
	const normalAt = ( o ) => unpackRGBToNormal( sceneNormal.sample( screenUV.add( o ) ).rgb );
	const zc = viewDepth( vec2( 0 ) ).toVar();
	const nc = normalAt( vec2( 0 ) ).toVar();
	let dz = float( 0 ), dn = float( 0 );
	for ( const o of [ vec2( px.x, 0 ), vec2( px.x.negate(), 0 ), vec2( 0, px.y ), vec2( 0, px.y.negate() ) ] ) {

		dz = dz.add( abs( viewDepth( o ).sub( zc ) ) );
		dn = dn.add( float( 1 ).sub( dot( normalAt( o ), nc ) ) );

	}

	return max( step( depthThreshold.mul( zc ), dz ), step( normalThreshold, dn ) );

} )();

renderPipeline.outputNode = mix( sceneColor, vec4( lineColor, 1 ), edgeMask );
```

- The depth threshold is **relative** (`depthThreshold × centre depth`). An absolute threshold draws lines everywhere in the distance and nowhere up close.
- Multiply `lineWidthPx` by `renderer.getPixelRatio()` so lines keep the same visual weight on retina displays.
- The JS loop runs at graph-build time and unrolls into 4 samples per buffer.
- **Rendered on r187 (WebGPU):** with this code, the ink pass outlines silhouettes and creases on every material. `toonOutlinePass` on the same scene draws no outline around the unlit sphere. (The jagged dark strip on the cube's left face appears in both renders, so it comes from the test scene's shadowing, not the outline method.) The pixel pass came out clean with an orthographic camera.


### 8.4 Painterly, comic and graphic looks

Algorithms (none ship as nodes in r187; build them in TSL, mostly on top of `pass()` output):

| Look | Technique | Parameters / cost |
|---|---|---|
| Oil paint | **Kuwahara filter**: split the neighbourhood into 4 quadrants (classic) or 8 sectors (generalized/anisotropic), take each region's mean and variance, output the mean of the lowest-variance region. The anisotropic variant orients the kernel along the structure tensor, which gives brush-stroke flow. | Radius 4–8 px; cost ∝ radius². **Run at half resolution**, then upsample. |
| Watercolour | Edge darkening (pigment pooling) from a depth/normal edge mask, paper texture multiplied in screen space, colour bleeding with a small noise-offset blur, granulation noise in the darks | Paper texture tiled at 1:1 screen pixels |
| Comic / halftone | Rotated dot grid in `screenCoordinate`; dot radius from luminance or N·L (r187 example `webgpu_tsl_halftone`: grid UV `= screenCoordinate.xy / screenSize.yy × count`, `count` 140–180, `radius` 0.8) | Combine with 2-band toon + ink lines |
| Hatching | Tonal art maps: 4–6 hatch textures of increasing density, blended by luminance; triplanar or screen-space mapping | Mipmapped TAMs keep stroke density constant with distance |
| Posterized / graphic | `posterize( color, steps )` + `bayerDither( color, steps )` (`three/addons/tsl/math/Bayer.js`), `lut3D( node, lut, size, intensity )` with `LUTCubeLoader` / `LUT3dlLoader` / `LUTImageLoader` | Apply after `renderOutput()`, as `webgpu_postprocessing_3dlut` does |

### 8.5 Low-poly, pixel art and retro

**Low-poly:**
- Facets: `flatShading: true` on the material, or `geometry.toNonIndexed()` + `computeVertexNormals()`.
- Colour: vertex colours (glTF `COLOR_0` is linear) or a palette texture with `NearestFilter`.
- Lighting: `MeshStandardMaterial` at roughness 0.8–1, a strong soft key, GTAO on.
- Depth: `scene.fog = new THREE.Fog( skyColor, near, far )` with the same colour as the background.
- Bevels are the exception here: crisp facets *are* the look.

**Pixel art (3D rendered as pixels):**
- Pass: WebGPU `pixelationPass( scene, camera, pixelSize = 6, normalEdgeStrength = 0.3, depthEdgeStrength = 0.4 )`; WebGL `RenderPixelatedPass`. Both render at 1/pixelSize resolution, so they are very cheap, and they add depth/normal edge highlights.
- **Orthographic camera + frustum snapping** (`pixelAlignFrustum` in `webgpu_postprocessing_pixel`): offset `left/right/top/bottom` by the sub-pixel fraction of the camera position along its right/up vectors. Without it, every camera move makes pixels "swim".
- Textures: `NearestFilter` for min and mag, `generateMipmaps = false`, texel density matched to the pixel size.
- **No** MSAA, TRAA, FXAA, DOF or blurred bloom: they destroy the pixel grid. Quantize colour with `posterize` and `bayerDither( color, steps )` after `renderOutput()`.
- Integer upscaling: `renderer.setPixelRatio( 1 )` and CSS `image-rendering: pixelated` on the canvas.

**PS1 / retro:**
- `retroPass( scene, camera, { affineDistortion } )` gives PS1 affine texture warping; 0 disables it.
- Chain `bayerDither( retro, steps )` → `posterize( …, steps )` with `steps` 16–32, then CRT helpers from `three/addons/tsl/display/CRT.js`: `scanlines( color, intensity 0.3, count 240 )`, `colorBleeding( color, 0.002 )`, `barrelUV( curvature 0.1 )`.
- Vertex snapping (*belief*: the usual technique, not a stock node): quantize clip-space XY to a low virtual resolution in the vertex stage.

### 8.6 Hybrid "stylized-real"

Most production work sits here: Pixar/Fortnite-style, clay renders, Arcane-style painted realism, miniatures. **Keep the physical light transport and stylize shape, colour and lighting design.** Viewers accept exaggerated shapes and saturated colour, but they read broken energy (glowing shadows, flat ambient) as cheap.

| Look | Keep physical | Stylize |
|---|---|---|
| Stylized-real (animated feature) | PBR, IBL, shadows, GTAO, bloom, DOF, AgX or Neutral | Exaggerated proportions, saturated albedo inside the plausible range (linear ≤ 0.8), strong back/rim lights, simplified textures, LUT grade |
| Clay render | Everything | One albedo (~0.6 linear), `roughness 0.6`, `diffuseRoughness 0.8–1` (r187), studio HDRI, strong GTAO, soft key |
| Painted realism | PBR lighting and shadows | Hand-painted albedo with baked light accents, lower normal-map strength, Kuwahara at radius 3–4 px on top, paper/brush overlay |
| Miniature / tilt-shift | PBR | High camera, very short DOF ramp (`blurRamp` 0.3–0.8 m) on a scene authored at real scale, saturated grade |
| Product "hero" stylization | PBR + Neutral tone mapping (brand colours) | Seamless gradient backdrop, rim lights, contact-shadow plane, no grain |

### 8.7 Stylized diagnostics

| Symptom | Cause | Fix |
|---|---|---|
| Toon bands blurred into gradients | `gradientMap` with linear filtering or mipmaps | `NearestFilter` min/mag, `generateMipmaps = false` |
| Cel colours look washed or shifted | AgX or ACES on flat-colour art | `NoToneMapping` (values ≤ 1) or `NeutralToneMapping` |
| Smooth ambient fill fighting the bands | Full-strength IBL | `environmentIntensity` 0.1–0.3, or unlit art-directed shading |
| Outline missing on some objects | `toonOutlinePass` skips non-toon materials | Toon materials on those meshes, or screen-space edges |
| Outline breaks at hard edges | Hull extruded along split normals | Smoothed normals for the hull, or screen-space edges |
| Lines too thick far away / too thin close | Hull thickness in object/clip space | Screen-space edges (constant px), or scale hull thickness by distance |
| Lines everywhere in the distance | Absolute depth threshold | Relative threshold (× centre depth) |
| Lines vanish on retina screens | Pixel width not scaled by DPR | `lineWidthPx × renderer.getPixelRatio()` |
| Pixel art swims or shimmers when the camera moves | Sub-pixel camera motion | Orthographic camera + `pixelAlignFrustum` snapping |
| Pixel art looks soft | MSAA, TAA, FXAA, linear texture filtering, fractional DPR | Disable AA; `NearestFilter`; `setPixelRatio( 1 )`; CSS `image-rendering: pixelated` |
| Blotchy anime face shading | Raw sculpted normals | Normal transfer from a sphere proxy; face SDF shadow map |
| Grey, dead shadows in a stylized scene | Shadow colour = darkened albedo | Hue-shifted `shadeTint` (cooler, more saturated) |
