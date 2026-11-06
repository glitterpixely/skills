> Part of the `threejs-rendering` skill. Verified against three r187 (2026-10-31); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# 7. "Why does my render look fake?": diagnostic table

| Symptom | Root cause | Fix (r187) |
|---|---|---|
| Washed-out, milky, low-contrast colours | sRGB applied twice (post chain + renderer), or albedo tagged `NoColorSpace` | One output transform only: `OutputPass` last (three composer), `renderOutput` once (TSL), `ToneMappingEffect` + `renderer.toneMapping = NoToneMapping` (pmndrs). Albedo `SRGBColorSpace`. N8AO: `gammaCorrection = false` when not last. |
| Oversaturated, crushed darks | Data map tagged `SRGBColorSpace` (normals and roughness get decoded), or tone mapping missing | Data maps → `NoColorSpace`. Set `renderer.toneMapping`. |
| Bright reds/blues turn neon or shift hue at high intensity | ACES hue skew on saturated HDR | `AgXToneMapping` (or `NeutralToneMapping` for products); lower emissive intensity and use bloom instead. |
| Glowing dark edges / halos around objects | SSAO/GTAO radius too large or post-multiplied over direct light; bloom on LDR data; SSR thickness too high | AO through `builtinAOContext`; GTAO `radius` 0.2–0.5 m; N8AO lower `distanceFalloff`; bloom `threshold ≥ 1` on HalfFloat buffers; SSR `thickness` 0.05–0.1. |
| Objects float above the floor | Peter-panning (|bias| × depth range too big) or no contact occlusion | Fit the frustum (§3.2); `bias` from `suggestShadowBias`; add GTAO/N8AO, a contact-shadow plane or `sss()`. |
| Striped / moiré self-shadowing | Shadow acne | Raise `normalBias` to about 1 texel first, then small `bias`; tighten near/far; `shadowSide = DoubleSide` only for open meshes. |
| Blocky or shimmering shadow edges | Frustum too large; frustum moves at sub-texel steps | `fitDirectionalShadow( …, { mode: 'stable' } )`; CSM/`SunLight` for large worlds; `shadow.radius` 2–4; TRAA. |
| Shadows that are uniformly soft or uniformly hard | No contact hardening | PCSS patch (`webgl_shadowmap_pcss`), or baked/progressive shadows for statics. |
| Jagged, sparkling specular highlights | Specular aliasing: high-frequency normals at low roughness | Mipmaps + max anisotropy; Toksvig roughness; TRAA; avoid roughness < 0.1 on detailed normals. |
| "Plastic" metal | `metalness < 1` with white albedo, no environment, or roughness uniform | `metalness: 1`, colour = linear F0 table; always set `scene.environment`; roughness variation (smudges, ORM). |
| "Plastic" or "wax-doll" skin | Uniform roughness, no SSS, too much specular | `ior 1.4`, roughness 0.45–0.6 with a pore-level `specularIntensityMap`, `MeshSSSNodeMaterial` or SSS shader, low warm sheen. |
| Flat, evenly lit interiors; corners as bright as open walls | IBL with no occlusion; ambient or hemisphere light | Remove ambient light. Lightmaps (`channel = 1`), `LightProbeGrid`, GTAO via `builtinAOContext`, `aoMap` on `uv1`; `environmentIntensity` 0.1–0.4 indoors. |
| Light pools look linear or have no hot spot | Legacy `decay` / `distance` values | `decay = 2`, `distance = 0` (or large); set intensities via `.power` in lumens. |
| Glass looks like grey plastic | `opacity`/`transparent` instead of transmission; thickness 0 on solid glass | `transmission: 1`, `ior`, `thickness` in metres, `attenuationColor` / `attenuationDistance`, `dispersion` for gems. |
| Rim of glass or water too dark | IOR too high, or IBL missing | Water `ior 1.333`; ensure `scene.environment`. |
| Razor-sharp CG edges, no highlight lines | 90° edges, smooth-shaded flat faces | Micro-bevels + weighted normals; `RoundedBoxGeometry`. |
| Banding in skies and soft gradients | 8-bit quantisation after tone mapping | Film grain/noise after tone mapping (opacity 0.03–0.08); `material.dithering = true`; HalfFloat buffers. |
| Ghosting / smearing on moving objects | TRAA without correct velocity; MSAA enabled alongside | `velocity` MRT on the pass that feeds TRAA; scene pass `options.samples = 0`; skinned and instanced meshes must write velocity. |
| Everything soft and blurry | DPR capped too low, DOF ramp too short, TAA with no sharpening | DPR 1.5–2 on desktop; derive the DOF ramp from the thin-lens CoC; `SharpenNode` after TRAA if needed. |
| Muddy HDRI reflections, sun missing | Clipped or compressed sun in the HDRI | Paint out the sun and add a `DirectionalLight` along `sunDirectionFromEquirect`; use unclipped 16+-stop HDRIs. |
| AO, SSR or shadow bias "doesn't work" | Scene authored in cm or inches (1 unit ≠ 1 m) | Rescale to metres; every world-space parameter assumes metres. |
| Custom post effect sees no depth (edges everywhere or nowhere, fog wrong) | Global `cameraNear`/`cameraFar` inside a `RenderPipeline` node resolve to the post quad's camera | `reference( 'near', 'float', sceneCamera )` / `reference( 'far', … )`, or `scenePass.getViewZNode()` |
| Console: "PCFSoftShadowMap has been removed" | r186+ | `PCFShadowMap` + `shadow.radius`. |
| `THREE.PostProcessing` deprecation warning | r183+ | `THREE.RenderPipeline`. |
