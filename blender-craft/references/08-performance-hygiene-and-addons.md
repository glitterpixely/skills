# 08 — Apple Silicon Performance, Scene Hygiene & Addon Playbook

---

## 1. Apple Silicon (`macOS arm64`) Metal-RT & EEVEE Optimization

1. **Cycles Metal GPU + Hardware Raytracing (`MetalRT`)**:
   - Ensure `Preferences -> System -> Cycles Render Devices = METAL` with both Apple Silicon GPU and MetalRT enabled, and `scene.cycles.device = 'GPU'`.
   - Set **Adaptive Sampling** (`use_adaptive_sampling = True`, `adaptive_threshold = 0.01–0.025`), `samples = 128–512` (exteriors: `128–256`; dark volumetric interiors: `384–768`), and **OpenImageDenoise (`OIDN`)** (`Prefilter = ACCURATE`, `Passes = ALBEDO_AND_NORMAL`).
   - Clamp fireflies safely (`sample_clamp_indirect = 8.0–12.0`, leave `sample_clamp_direct = 0.0` so sun/crystal specular peaks stay crisp!).
   - Light Paths: `max_bounces = 8`, `diffuse_bounces = 3`, `glossy_bounces = 4`, `transmission_bounces = 8` (raise transmission to `12` when rendering multi-faceted crystals so internal facets never turn black!).
2. **EEVEE 5.x Real-Time Tuning**:
   - Enable `use_raytracing = True` for realistic screen/ray GI and reflections on PBR scenes; turn raytracing **OFF** on pure `Shader to RGB` cel-shaded anime scenes where flat stylized fills and fast 60 FPS playback are desired!
   - Keep `Render -> Simplify` enabled during layout (`Viewport Max Subdivision = 1`, `Viewport Texture Limit = 2048`) while leaving `Render` unthrottled.
3. **Memory & Instancing Discipline (Unified Memory Protection)**:
   - Duplicate repeated props with **`Alt+D`** (`bpy.ops.object.duplicate(linked=True)`) or **Collection Instances**, never `Shift+D` full mesh copies.
   - Check texture sizes before importing 8K Megascans/Poly Haven maps: **1 single uncompressed 8K RGBA float map = 1 GB VRAM**. Use `4K` only on the hero prop inches from the lens, `2K` on mid-ground kits, and `1K` on scattered pebbles/leaves.

---

## 2. Outliner Naming, Collections & `.blend` File Hygiene

### Standard Naming & Collection Hierarchy
```text
Scene Collection
├── COL_01_Hero          (GEO_ArcaneStaff_*, RIG_Hero, Empty roots)
├── COL_02_Environment   (GEO_Terrain, GEO_ShrineArch_*, water planes)
├── COL_03_Scatter       (Geometry Nodes scatter hosts, BagaPie/Geo-Scatter systems)
├── COL_04_FX            (VFX_FallingPetals_GN, bounded volume cubes)
├── COL_05_Lighting      (LGT_Key_Sun, LGT_Rim_Back, LGT_CrystalCore, gobos)
├── COL_06_Cameras       (CAM_01_Master, CAM_02_OTS_A, Aim empties)
└── COL_99_Sources       [Disabled in Viewport & Render!] (scatter prototypes at (0,0,0), cutter booleans, backup curves)
```
- Never leave materials named `Material.001`, `Material.007` or meshes named `Cube.004`, `Cylinder.009`. Name every data-block (`MAT_Shaft_AgedOak`, `MAT_Crystal_Core`).
- **Purge Orphan Data Regularly**:
  ```python
  bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
  ```
- **External Paths**: Use `bpy.ops.file.make_paths_relative()` on project repositories, or `bpy.ops.file.pack_all()` before moving a standalone `.blend` archive.

---

## 3. Installed Addon Playbook (27 Active Modules in Blender 5.1.2)

All 27 modules below are installed and enabled in Blender 5.1.2:

| Category | Module ID | UI Location / Shortcut | Best Use Case |
| :-- | :-- | :-- | :-- |
| **Nodes & Rigging** | `node_wrangler` | Shader/Comp/GN (`Ctrl+T`, `Ctrl+Shift+LMB`) | Instant texture mapping setups & live socket viewer |
| | `rigify` | `Add -> Armature -> Rigify Meta-Rigs` | Full biped, quadruped, wing, tail, and prop rig generation |
| **Scattering, Nature & Arch** | `bl_ext.blender_org.Bagapie` | `3D Viewport -> J` Pie Menu | Free GeoNodes scatter, paint-scatter, climbing ivy, cables, curve arrays, walls/stairs/windows |
| | `bl_ext.blender_org.antlandscape` | `Add -> Mesh -> Landscape` | Eroded mountains, canyons, riverbeds, strata rocks |
| | `bl_ext.blender_org.modular_tree` | `Editor Type -> Mtree Node Tree` | Custom procedural trunks, gnarled fantasy roots, branches & twigs |
| | `bl_ext.blender_org.ivygen` | `Sidebar (N) -> Create -> IvyGen` | Cursor-seeded climbing vines on shrines, walls, and staffs |
| | `bl_ext.blender_org.archimesh` | `Add -> Mesh -> Archimesh` | Instant rooms, doors, arched windows, columns, stairs, curtains, books (ideal for Seedance grayboxes!) |
| **Prop & Mesh Modeling** | `bl_ext.blender_org.looptools` | `Edit Mode -> Right-Click / N -> Edit -> LoopTools` | `Circle`, `Relax`, `Bridge`, `Loft`, `Curve`, `Space` |
| | `bl_ext.blender_org.bool_tool` | `Ctrl+Shift+B` / `Sidebar -> Edit -> Bool Tool` | Live non-destructive Brush Booleans (`Difference`, `Union`, `Slice`) for runes, sockets, carvings |
| | `bl_ext.blender_org.extra_mesh_objects` | `Add -> Mesh -> Diamonds / Rocks / Gears` | Instant faceted gem/crystal bases, rocks, pipe joints, math surfaces |
| | `bl_ext.blender_org.extra_curve_objectes` | `Add -> Curve -> Spirals / Knots / Torus` | Helices, logarithmic spirals, Celtic knots, braids for vine wraps & filigree |
| | `bl_ext.blender_org.f2` | `Edit Mode -> F` on open corner/edge | Rapid quad-strip extension for manual retopology |
| | `bl_ext.blender_org.EdgeFlow` | `Edit Mode -> Edge Menu -> Set Flow / Set Linear` | Smooths inserted edge loops to match surrounding surface curvature without flattening cylinders |
| | `bl_ext.blender_org.modifier_tools` | `Properties -> Modifiers` header buttons | `Apply All`, `Viewport Vis`, `Toggle Stack` across complex modifier stacks |
| **Stylized Paint & Lighting** | `bl_ext.blender_org.ucupaint` | `Sidebar (N) -> Ucupaint` | Substance-style multi-layer painting, AO/curvature masks, color ramps, and 1-click PBR channel baking |
| | `bl_ext.blender_org.lightpainter` | `Left Toolbar (T) -> Light Paint` | Paint rim lights, area lights, gobos, sky sun, and shadow flags directly onto 3D surfaces |
| | `bl_ext.blender_org.brushstroke_tools` | `Sidebar (N) -> Brushstrokes` | Procedural 3D painterly brushstroke layers on meshes for hand-painted / MV looks |
| | `bl_ext.blender_org.sun_position` | `Properties -> World -> Sun Position` | Physically accurate sun azimuth/elevation & golden-hour sky control |
| | `bl_ext.blender_org.tri_lighting` | `Add -> Light -> 3 Point Lights` | Instant key + fill + rim setup framed around the active prop/character |
| **Cameras & Previz** | `bl_ext.blender_org.camera_shakify` | `Camera Properties -> Camera Shakify` | Real motion-captured handheld breathing & cinema lens shake presets |
| | `bl_ext.blender_org.add_camera_rigs` | `Add -> Camera -> Dolly / Crane Camera Rig` | Smooth aim-locked Dolly and Crane camera rigs with DOF target bones |
| | `bl_ext.blender_org.turnaround_camera` | `Sidebar (N) -> View / Turnaround` | 1-click 360° orbit turnaround animation around any selected hero asset |
| | `bl_ext.blender_org.storytools` | `Sidebar (N) -> Storytools` | 3D camera + Grease Pencil storyboard & shot-blocking previz |
| | `bl_ext.blender_org.grease_pencil_tools` | `Sidebar (N) -> Grease Pencil` | Box deform, canvas rotate, and timeline tools for 2D/3D hybrid anime ink |
| **UVs & PBR Baking** | `bl_ext.blender_org.univ` | `UV Editor -> Sidebar (N) -> UniV` | High-speed `Quadrify` (straighten curved wraps/ribbons), `Orient`, `Stack`, `Weld`, `Pack` |
| | `bl_ext.blender_org.texel_density_checker` | `Sidebar (N) -> Texel Density` | Measure and equalize exact `px/m` texel density across modular environment kits |
| | `bl_ext.blender_org.mat_baker` | `Sidebar (N) -> Mat-Baker` | Flatten procedural node materials into export-ready PBR texture sets |

---

## 4. Commercial Addon Upgrade Matrix (When Paid Addons Pay Off)

| Addon | Cost Model | When to Buy vs. When Free Stack Suffices |
| :-- | :-- | :-- |
| **Geo-Scatter** *(or free **Biome-Reader**)* | ~$99 one-time (`Biome-Reader` = $0) | Buy when scattering huge multi-species ecosystems with 1-click Biome presets, wind waves, and camera-shadow frustum culling. For single scenes, ivy, and medium scatters, installed **`BagaPie`** covers 80% for $0. *(Never install Geo-Scatter and Biome-Reader together.)* |
| **Botaniq** *(via free **`engon`** manager)* | ~$49 Lite / ~$129+ Full (`engon` = $0) | Buy when you want 300–700+ ready-to-drop realistic/seasonal trees, shrubs, flowers, grasses, and vines instead of modeling foliage in `Modular Tree`. Pairs natively with `Geo-Scatter`. |
| **Photographer 5** | ~$80 one-time | Buy if rendering dozens of multi-camera plates with physical EV exposure, optical vignetting, anamorphic bokeh, and a built-in per-camera Render Queue. |
| **Quad Remesher** | ~$60 Indie / ~$110 Pro | Best-in-class 1-click clean quad auto-retopology when converting heavy ZBrush/Blender sculpts into clean SubD or game meshes. |
| **SimpleBake** / **UV Packmaster 3** | ~$22 / ~$44 one-time | Worthwhile only if high-volume multi-UDIM game-asset baking & C++ GPU island packing outgrow `Ucupaint` + `Mat-Baker` + `UniV`. |
