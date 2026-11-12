# 05 — UVs, Texel Density, PBR Baking & `.glb` / Three.js Export

Procedural Blender nodes (`Noise`, `Voronoi`, `Musgrave`, `ColorRamp`, `Shader to RGB`, `Ambient Occlusion`, `Raycast`) **never survive `.glb` / `.fbx` export** — glTF 2.0 transports only `Principled BSDF` scalar values and UV-mapped image textures. Follow this exact pipeline whenever assets leave Blender or receive hand-painted textures.

---

## 1. Seam Placement & UV Unwrapping (`univ` + `texel_density_checker`)

1. **Pre-Unwrap Check**: Confirm `obj.scale == (1, 1, 1)` (`Ctrl+A -> Scale`). Unwrapping an unapplied `(1, 1, 8)` shaft squashes UVs 8× lengthwise.
2. **Where to Hide Seams**:
   - **Staffs / Cylinders / Columns**: One longitudinal seam down the **rear/back-camera side** + circular seams tucked inside collar rings, wraps, or socket recesses.
   - **Cloth Wraps / Ribbons / Vines / Trim Mouldings**: Unwrap and immediately run **UniV → Quadrify / Straighten** (`UV Editor -> N -> UniV`) so curved strips become dead-straight rectangular UV islands! Straight strips eliminate diagonal pixel aliasing, pack at `90%+` UV space efficiency, and make woven fabric or wood grain follow the 3D bend automatically.
   - **Hard-Surface / Faceted Crystals**: Mark seams along hard angle transitions (`> 60°`) while keeping contiguous front-facing planes attached where possible.
3. **Texel Density & Bleed Padding**:
   - Use **`Texel Density Checker`** (`Sidebar -> Texel Density`) so a tiny buckle does not get `4096 px/m` next to a blurry `128 px/m` wall:
     - **Interactive Web / Three.js Worlds**: `512 – 1024 px/m` (`1K–2K` atlases)
     - **Hero Props / Close-Up Film Inserts**: `2048 px/m` (`2K–4K` maps)
   - **Island Margin (Padding)**: Always pack with **`0.004 – 0.008`** UV margin (`8–16 px` at `2048×2048`, `4–8 px` at `1024×1024`). Zero-margin islands bleed background/neighbor colors across seams as soon as GPU mipmapping kicks in at medium camera distance!

---

## 2. Procedural-to-PBR & High-to-Low Texture Baking

Use **Ucupaint's built-in baker**, **Mat-Baker** (`bl_ext.blender_org.mat_baker`, installed), or native **Cycles Bake** (`scene.render.engine = 'CYCLES'`, `samples = 16–32` for diffuse/roughness/normal, `64–128` for AO):

### Non-Negotiable Color-Space & Format Table

| Map Channel | `image.colorspace_settings.name` | Bit Depth & Format | Notes |
| :-- | :-- | :-- | :-- |
| **Base Color (Albedo)** | `'sRGB'` | 8-bit PNG | Bake `Diffuse` with **Direct = OFF, Indirect = OFF, Color = ON** so lighting is never baked into PBR albedo! (Exception: intentionally unlit hand-painted anime/mobile diffuse-only assets.) |
| **Roughness** | **`'Non-Color'`** | 8-bit PNG | Leaving Roughness as `'sRGB'` applies a `2.2` gamma curve and makes surfaces look wet/plastic! |
| **Metallic** | **`'Non-Color'`** | 8-bit PNG | Keep binary (`0.0` dielectric or `1.0` raw metal; partial values only on dusty transitions). |
| **ORM Packed (glTF)** | **`'Non-Color'`** | 8-bit PNG | glTF automatically packs `R = Occlusion`, `G = Roughness`, `B = Metallic` when wired through `Separate Color`! |
| **Normal Map** | **`'Non-Color'`** | **16-bit PNG** (or 8-bit dithered) | **OpenGL (`+Y` Swizzle: `+X, +Y, +Z`)** — matches Blender, glTF 2.0, and Three.js natively! (Unreal/DirectX uses `-Y`.) |
| **Height / Displacement** | **`'Non-Color'`** | **16-bit PNG** or **32-bit EXR** | 8-bit height maps cause visible stair-step terracing! |
| **Emission** | `'sRGB'` | 8-bit PNG (or 16-bit EXR for HDR) | Wire to `Principled BSDF.inputs["Emission Color"]`. |

### High-to-Low Normal Bake Checklist
1. Co-locate `_HP` and `_LP` at identical world coordinates `(0, 0, 0)`.
2. Shade Smooth on `_LP` + `Weighted Normal` (if mid-poly) + **`Triangulate` modifier (`Keep Normals = True`)** *before* baking so the triangulation tangent basis matches the exported `.glb` 1:1.
3. Set `Extrusion = 0.01–0.03 m` (just enough to clear the highest sculpt peak; excessive ray distance captures the opposite side of thin fingers/wraps!). For tight wraps or crevices, duplicate `_LP` and push along normals (`Alt+S`) as an explicit **Cage Object**.

---

## 3. Blender (`+Z` Up) to glTF 2.0 / Three.js (`+Y` Up) Export Contract

Blender is right-handed `+X` Right, `+Y` Forward (into scene), `+Z` Up.
glTF 2.0 and Three.js are right-handed `+X` Right, `+Y` Up, `+Z` Toward Viewer (`-Z` Forward).

### Exact Coordinate Bridge (`bpos`)
When authoring procedural layouts in Blender destined for exact Three.js coordinates `(tx, ty, tz)`:
```python
def bpos(tx: float, ty: float, tz: float) -> tuple[float, float, float]:
    """Map Three.js (x_right, y_up, z_toward_viewer) -> Blender (x_right, y_into_scene, z_up)."""
    return (tx, -tz, ty)
```
Exporting with `export_yup=True` and `export_apply=True` rotates `(tx, -tz, ty)` right back to exact `(tx, ty, tz)` in Three.js with **zero runtime offset hacks**.

### Production `.glb` Export Snippet (Blender 5.1+ Verified)

```python
import bpy

def export_clean_glb(
    filepath: str,
    selected_only: bool = False,
    gpu_instances: bool = True,
    draco: bool = False,
):
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format="GLB",
        use_selection=selected_only,
        use_visible=not selected_only,
        export_yup=True,
        export_apply=True,                # Applies modifiers on exported copy (note: skips meshes with Shape Keys unless handled)
        export_texcoords=True,
        export_normals=True,
        export_tangents=True,             # Prevents normal-map seam flips in Three.js!
        export_materials="EXPORT",
        export_image_format="AUTO",       # Preserves PNG/WebP cleanly; compress further via gltf-transform KTX2 if needed
        export_gpu_instances=gpu_instances,  # Emits EXT_mesh_gpu_instancing -> THREE.InstancedMesh!
        export_draco_mesh_compression_enable=draco,
    )
```

### Geometry Nodes & Instancing on `.glb` Export
- **Collection Instances / Alt+D Linked Duplicates**: With `export_gpu_instances=True`, Blender 5.1+ exports `EXT_mesh_gpu_instancing`, which Three.js `GLTFLoader` loads directly as `THREE.InstancedMesh` (1 draw call!).
- **Geometry Nodes Scatters**: Unrealized GN point instances inside a modifier do **not** automatically become `EXT_mesh_gpu_instancing` unless converted to instances or exported as a lightweight JSON transform manifest (`[{pos, rot, scale}, ...]`) when counts exceed `1,000+`. Never `Realize Instances` on `50,000` high-poly foliage meshes into a web `.glb`!
- **Shape Keys + Modifiers**: Blender cannot apply modifiers on meshes carrying Shape Keys (`export_apply=True` skips them); use `SKkeeper` or `Geonode To Shapekey` when facial/morph targets must coexist with Subdivision/Mirror modifiers.
