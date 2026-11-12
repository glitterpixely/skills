# 01 — Scene Scale, Datum Contract, Color Management (5.0+) & Lighting

Getting scale, color space, or view transform wrong corrupts bevel widths, physics simulations, light falloff, shadow bias, and palette fidelity simultaneously. Lock all four before modeling or shading.

---

## 1. Metric Scale & Ground Datum Contract

- **Unit Standard**: Keep `scene.unit_settings.system = 'METRIC'` and `scene.unit_settings.scale_length = 1.0` (`1 Blender Unit = 1.0 meter`).
  - Human character: `1.65–1.85 m` tall
  - Two-handed fantasy staff: `1.70–2.10 m` long, shaft diameter `0.032–0.045 m`
  - Interior doorway: `0.90 m × 2.10 m`; ceiling height: `2.70–3.20 m`
- **Apply Scale (`Ctrl+A` → Scale)**:
  - Every mesh and curve object must finish modeling with `obj.scale == (1.0, 1.0, 1.0)` (unless intentionally instanced along an axis without modifiers). Non-uniform scale (`(1.0, 1.0, 4.2)`) skews Bevel modifiers into uneven chamfers, stretches UV islands, and breaks armature/cloth evaluation.
- **Origin & Datum Placement**:
  - **Standing architecture, furniture, trees, characters**: place local origin at bottom-center `(0, 0, 0)` with world/local `min_z == 0.0` so snapping to a floor or terrain point never buries or floats the mesh.
  - **Handheld weapons / staffs**: place local origin at the primary **hand grip center** (`(0, 0, 0)`) or parent sub-parts cleanly under an `Empty` root (`StaffRoot`) with uniform scale `(1, 1, 1)`.
  - **Scatter source assets**: keep at world origin `(0, 0, 0)` with `min_z = 0.0` (or slight `-0.02 m` root embed for trunks/rocks on sloped ground) inside a disabled/hidden `COL_Sources` collection. Never leave a scatter source at `(25, -14, 3)` — some modifiers/exporters inherit instance-collection offsets.
- **Camera Clipping Bounds (`clip_start` / `clip_end`)**:
  - Default `camera.data.clip_end = 1000.0` silently slices off distant mountains, sky domes, and cloud banks in exterior environments.
  - Set `clip_start = 0.05` (or `0.01` for macro prop inserts — **never** `0.0001`, which destroys depth-buffer precision and causes viewport/EEVEE Z-fighting) and `clip_end = 5000.0` (exteriors) or `250.0` (interiors/props). Sync viewport `space_data.clip_end` to match.

---

## 2. Blender 5.0+ Color Management & View Transforms

Blender 5.0 introduced per-file **Working Color Spaces** alongside expanded OCIO View Transforms.

### Working Space (`bpy.data.colorspace.working_space`)
- **`'Linear Rec.709'`** *(default)*: Keep for 95% of EEVEE, stylized/anime, web `.glb` / Three.js, and standard sRGB/Rec.709 video pipelines. Shader math and existing procedural textures assume Rec.709 primaries.
- **`'Linear Rec.2020'`** or **`'ACEScg'`**: Use only when delivering wide-gamut HDR cinema EXRs (e.g., intense saturated neon/fire/laser bounce in Cycles where Rec.709 primaries clip or skew hue in multi-bounce GI).

### View Transform Decision Matrix (`scene.view_settings.view_transform`)

| View Transform | When to Use | Why It Matters |
| :-- | :-- | :-- |
| **`AgX`** *(5.x default)* | Photoreal environments, dark fantasy caves/firelight, dramatic Cycles renders | Compresses intense HDR highlights smoothly toward white without harsh RGB channel clipping ("Notorious Six" skew). **Do not use for flat anime/cel art** — it desaturates mid/high values into milky gray. |
| **`Khronos PBR Neutral`** | Hero props, e-commerce, and **Three.js / `.glb` look-dev** | Preserves exact base-color hue and saturation up to ~0.8 luminance while rolling off specular peaks cleanly. Matches Three.js `NeutralToneMapping`. |
| **`Standard`** | **Painterly/cel anime**, flat editorial illustration, exact brand colors, Seedance graybox/mask plates | Direct linear-to-sRGB curve with zero filmic desaturation. Mandatory whenever `Shader to RGB` ramps or exact sampled reference colors must render as authored. |
| **`ACES 2.0`** / **`ACES 1.3`** | VFX plates graded downstream in an ACES DaVinci Resolve timeline | Matches ACES Output Transform behavior; prefer exporting scene-linear `OpenEXR` (DWAA/ZIP) when grading in Resolve. |
| **`False Color`** | Diagnostic exposure check only | Verifies key/fill ratios and catches blown diffuse albedos before final render. |

---

## 3. The Scene-Linear Color Trap & Reference Palette Sampling

Every RGBA color socket in `bpy` (`inputs["Base Color"].default_value`, `light.color`, `ColorRamp` elements, `material.diffuse_color`) stores **scene-linear** floats, NOT sRGB hex percentages!
- Writing sRGB `(0.95, 0.72, 0.68)` directly into `default_value` renders washed-out chalky pastel.
- Raising values to `** 2.2` naively drifts dark tones; use the exact IEC 61966-2-1 piece-wise formula:

```python
def srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def hex_to_linear_rgba(hex_str: str, alpha: float = 1.0) -> tuple[float, float, float, float]:
    h = hex_str.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    return (srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b), alpha)
```

### Best Practice: Sample Reference Art Directly in Linear Space
Guessing colors from memory produces generic CGI primaries. Load the user's reference frame into `bpy.data.images.load(path)` — Blender automatically linearizes `.pixels` on read — and extract dominant cluster centroids:

```python
import bpy, random

def sample_linear_palette(image_path: str, k: int = 5, stride: int = 16, iters: int = 12):
    img = bpy.data.images.load(image_path, check_existing=True)
    px = img.pixels[:]  # Flat [R, G, B, A, ...] already in scene-linear space
    samples = [
        (px[i], px[i + 1], px[i + 2])
        for i in range(0, len(px), 4 * stride)
        if px[i + 3] > 0.5
    ]
    rng = random.Random(42)
    centers = rng.sample(samples, min(k, len(samples)))
    for _ in range(iters):
        buckets = [[] for _ in centers]
        for s in samples:
            idx = min(range(len(centers)), key=lambda c: sum((s[j] - centers[c][j]) ** 2 for j in range(3)))
            buckets[idx].append(s)
        for idx, b in enumerate(buckets):
            if b:
                n = len(b)
                centers[idx] = tuple(sum(p[j] for p in b) / n for j in range(3))
    # Sort brightest to darkest
    return sorted(centers, key=lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2], reverse=True)
```

### Physically Plausible Albedo Ceiling
In photoreal/dark-fantasy PBR (`AgX` / `Cycles`), real diffuse surfaces never reflect `1.0` white or `0.0` black:
- Fresh snow / white plaster: `0.75–0.85` linear max (`#DCDCDC`–`#ECECEC` sRGB)
- Charcoal / dark bark / black iron albedo: `0.02–0.04` linear min (`#262626`–`#383838` sRGB)
Exceeding `0.85` diffuse albedo blows out indirect bounce and destroys contact shadow contrast.

---

## 4. Lighting Architecture & Separation

1. **Key / Fill / Rim + Motivated Practical**:
   - **Key Light**: Primary directional (`SUN` `2.0–5.0 W/m²` or large soft `AREA` light at `35–55°` elevation, `30–45°` off camera axis) establishing shadow direction. Increase `Light -> Angle` (`1.5°–6°` on Sun) or `AREA` size (`1.5–4.0 m`) for soft shadow penumbras.
   - **Sky / Bounce Fill**: Cool opposing fill (`15–30%` of key energy) via World shader / HDRI (`0.3–0.8` strength) or broad cool `AREA` fill — never flat `1.0` uniform gray World lighting, which kills form modeling.
   - **Rim / Backlight**: Placed behind subject (`135–165°` from camera) at `0.8–2.5×` key intensity to carve silhouette edges (cloth wraps, hair, crystal facets, foliage silhouettes) out from dark or busy backgrounds.
   - **Practical / Hero Core**: Local `POINT` light (`radius = 0.03–0.15 m`) inside glowing crystals, lanterns, or fire orbs so surrounding geometry catches real inverse-square bounce (shader `Emission` alone does not cast direct EEVEE lights onto neighbors without raytraced GI).
2. **Gobos (Cookie Cutters) & Dappled Light**:
   - Even an empty room or simple terrain looks rich when the Key light passes through a canopy/window gobo plane (or `ShaderNodeTexNoise` / leaf alpha mapped onto a Spot/Area light node tree in Cycles, or an off-camera perforated shadow-caster mesh in EEVEE).
3. **Light Linking & Shadow Linking**:
   - Give hero characters or props a dedicated rim light linked exclusively to their collection (`Object Properties -> Shading -> Light Linking`) so the rim highlights the prop/character without scorching the ground or wall behind them.
4. **Interactive Light Painting (`lightpainter`)**:
   - With the installed `Light Painter` extension enabled, paint rim lights, area lights, or sky sun direction directly onto the mesh surface where the specular catchlight should land; the addon solves the 3D light position and angle automatically.
5. **Volumetric Atmosphere vs. Depth Haze**:
   - **Close shafts of light (caves, cathedral windows, forest god-rays)**: Attach `Principled Volume` (`Density = 0.01–0.04`, `Anisotropy = 0.5–0.75`) to a **bounded domain cube** around the frustum — never to the infinite `World` volume, which kills distant HDRI/Sun rays!
   - **Wide exterior vistas / painterly anime**: Prefer shader/compositor `View Distance` / `Mist` pass blending (`04-materials-pbr-stylized-and-anime.md`) — 100× faster, zero volumetric noise, crisp art-directable depth layers.
