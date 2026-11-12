# 04 — Materials: Photoreal PBR, Painterly/Cel Anime, Grease Pencil 3 & Ucupaint

Always look up shader nodes by `.type` (`"BSDF_PRINCIPLED"`, `"SHADER_TO_RGB"`, etc.), never by `.name`, and assign colors on shader node inputs (`mat.diffuse_color` affects Solid Viewport display only).

---

## 1. Hero PBR Materials (Photoreal & Stylized-Real)

Flat scalar values (`Base Color = brown`, `Roughness = 0.5`) scream "untouched primitive." Every hero material needs **3 layers of variation**:

1. **Roughness Breakup (Most Important Layer)**:
   - Even when albedo is simple, modulate `"Roughness"` across a realistic window (e.g., worn wood `0.38–0.72`; forged bronze `0.18–0.48`; polished crystal `0.03–0.14` with dusty crevices at `0.55`):
     `TexCoord (Object)` → `Noise Texture (Scale=6, Detail=8, Roughness=0.65)` → `Map Range (0→1 to 0.35→0.68)` → `Principled BSDF.inputs["Roughness"]`.
2. **Edge Wear & Cavity Darkening (`ShaderNodeAmbientOcclusion` / `ShaderNodeBevel` / `ShaderNodeRaycast`)**:
   - **Crevice dirt/patina**: `Ambient Occlusion (Inside=False, Distance=0.04)` → `ColorRamp` → multiply `15–30%` darker/warmer tone into `"Base Color"` and raise `"Roughness"` in recessed carvings.
   - **5.1 Screen/Ray Edge & Contact Shading (`ShaderNodeRaycast`)**: New in Blender 5.1 EEVEE & Cycles — fire short rays along `-Normal` (thickness/subsurface glow mask) or `+Normal` (contact proximity mask where roots/rocks meet mud or water) in real time!
   - **Cycles Bevel Shader**: On static hard-surface props without geometric bevels, wire `ShaderNodeBevel (Radius=0.002, Samples=4)` → `BSDF.inputs["Normal"]` to catch micro-edge highlights effortlessly.
3. **Believable Glowing Crystals, Runes & Magic Cores**:
   - Pure flat `Emission (Strength = 10)` turns a faceted crystal into a featureless white silhouette.
   - **Layered Arcane Crystal Recipe**:
     1. Outer shell: `Principled BSDF` with `Transmission Weight = 0.85`, `IOR = 1.54–1.76`, `Roughness = 0.06`, tinted `Coat` or `Layer Weight (Fresnel)` rim tint so facet edges stay crisp and dark/iridescent against the bright interior!
     2. Inner core: Driven by `Layer Weight (Facing, Blend = 0.35)` **inverted** (so emission is strongest deep inside the center and falls off at grazing facet edges!) wired into `"Emission Color"` + `"Emission Strength"` (`3.0–12.0`).
     3. Scene illumination: Place a `POINT` light (`15–35 W`, `radius = 0.04 m`, matching hue) at the crystal's center so nearby wraps, wood, and hands catch real light + specular highlights, and finish with Compositor `Glare ("Bloom")` (`00-blender5-api-and-gotchas.md`).

---

## 2. Painterly & Cel-Shaded Anime Look (EEVEE 5.x Only)

Verified production recipe for high-key, hand-painted anime environments and music videos in **Blender 5.1+**:

### Mandatory Scene Preconditions
1. **Engine**: `scene.render.engine = "BLENDER_EEVEE"` (`ShaderNodeShaderToRGB` does **not** exist in Cycles!).
2. **View Transform**: `scene.view_settings.view_transform = "Standard"` (`AgX` crushes bright anime skies and pastel sakura tones into dull gray).
3. **Sampled Linear Palette**: Sample colors directly from reference art (`sample_linear_palette()` in `01-scene-scale-color-and-lighting.md`) rather than guessing saturated primaries.

### Verified `bpy` Anime Cel + Atmospheric Depth Material Builder

```python
import bpy

def create_anime_cel_material(
    name: str,
    shadow_lin: tuple[float, float, float],
    mid_lin: tuple[float, float, float],
    lit_lin: tuple[float, float, float],
    haze_lin: tuple[float, float, float] = (0.464, 0.644, 0.819),
    haze_start: float = 18.0,
    haze_end: float = 140.0,
    max_haze: float = 0.78,
):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()

    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (760, 0)

    emit = nt.nodes.new("ShaderNodeEmission")
    emit.location = (560, 0)
    nt.links.new(emit.outputs["Emission"], out.inputs["Surface"])

    # Atmospheric perspective (Camera View Distance -> pale sky haze)
    mix_haze = nt.nodes.new("ShaderNodeMix")
    mix_haze.data_type = "RGBA"
    mix_haze.location = (340, 0)
    mix_haze.inputs["B"].default_value = (*haze_lin, 1.0)
    nt.links.new(mix_haze.outputs["Result"], emit.inputs["Color"])

    cam = nt.nodes.new("ShaderNodeCameraData")
    cam.location = (-160, -220)
    map_r = nt.nodes.new("ShaderNodeMapRange")
    map_r.clamp = True
    map_r.location = (80, -220)
    map_r.inputs["From Min"].default_value = haze_start
    map_r.inputs["From Max"].default_value = haze_end
    map_r.inputs["To Min"].default_value = 0.0
    map_r.inputs["To Max"].default_value = max_haze
    nt.links.new(cam.outputs["View Distance"], map_r.inputs["Value"])
    nt.links.new(map_r.outputs["Result"], mix_haze.inputs["Factor"])

    # 3-band Cel Ramp via Diffuse -> Shader to RGB
    diffuse = nt.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    diffuse.location = (-380, 80)

    s2rgb = nt.nodes.new("ShaderNodeShaderToRGB")
    s2rgb.location = (-180, 80)
    nt.links.new(diffuse.outputs["BSDF"], s2rgb.inputs["Shader"])

    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.location = (40, 80)
    ramp.color_ramp.interpolation = "CONSTANT"
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (*shadow_lin, 1.0)
    ramp.color_ramp.elements[1].position = 0.38
    ramp.color_ramp.elements[1].color = (*mid_lin, 1.0)
    hi = ramp.color_ramp.elements.new(0.76)
    hi.color = (*lit_lin, 1.0)

    nt.links.new(s2rgb.outputs["Color"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], mix_haze.inputs["A"])
    return mat
```

### Adding Painterly Brushwork, Outlines & 2D/3D Hybrid Accents
1. **Painterly Edge Softening**: Add a subtle world-space `Noise Texture` (`Scale = 12–30`, factor `0.03–0.06`) added into `s2rgb.outputs["Color"]` *before* the `CONSTANT` `ColorRamp` so shadow terminator lines look like dry-brush gouache edges rather than razor-sharp CAD vectors!
2. **3D Surface Brushstrokes (`brushstroke_tools`)**: Use the installed **Brushstroke Tools** extension to comb layered 3D painterly stroke cards over tree canopies, rocks, or hero garments.
3. **Outlines — Pick the Right Method**:
   - **Inverted Hull (`Solidify` Modifier)**: Fastest, real-time, exports cleanly to `.glb`! Add `Solidify` (`Thickness = -0.003 m`, `Flip Normals = True`, `Material Offset = 1`) with a `Backface Culling = True` dark ink material (`#1E1924`, never pure `#000000` unless graphic noir) in slot 2; modulate thickness with a Vertex Group (`0.0` on delicate eyelashes/lips, `1.0` on outer silhouette).
   - **Grease Pencil 3 (`Line Art` Modifier)**: Best for architectural ink illustration, creases, and hand-drawn boil (`Noise` + `Thickness` modifiers on GP v3 layers; Blender 5.0+ supports native GP motion blur and 5.1 revamped GP fills).
4. **Compositor Kuwahara Pass**: Wire `CompositorNodeKuwahara` (`Type = "Anisotropic"`, `Size = 3–5`) before `Bloom` to unify over-sharp geometry edges into cohesive painted strokes without frame-to-frame flicker.

---

## 3. Layered Hand-Painting & Smart Masks with Ucupaint (`ucupaint`)

With **Ucupaint 3.0+** (`bl_ext.blender_org.ucupaint`, installed & active in `View3D -> Sidebar (N) -> Ucupaint`):
1. Select any unwrapped mesh and create a Ucupaint tree on its Principled BSDF.
2. Stack non-destructive layers just like Substance Painter:
   - **Layer 1**: Base wood/stone/cloth color + roughness
   - **Layer 2**: Procedural `Ambient Occlusion` mask darkening recesses
   - **Layer 3**: `Geometry -> Pointiness / Curvature` mask brightening stylized edge highlights (crucial for stylized fantasy staffs, blades, and rocks!)
   - **Layer 4**: Direct 3D Texture Paint hand-brushed runes, moss, or gradients
3. When finished—especially before `.glb` export—use Ucupaint's **Bake Channels to Image** button to flatten the entire multi-layer stack into standard `Base Color`, `Roughness`, `Metallic`, `Normal`, and `Emission` PNG textures in one click.
