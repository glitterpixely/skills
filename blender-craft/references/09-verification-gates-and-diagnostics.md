# 09 — Verification Gates (`G1`–`G5`) & Diagnostic Symptom Table

Never declare a Blender build, material setup, animation, or export finished from `Code executed successfully` alone. Every deliverable passes programmatic audit (`scripts/blender_scene_audit.py`) plus visual inspection (`look` or rendered frames).

---

## 1. The Five Production Gates (`G1`–`G5`)

### Gate `G1` — Scale, Transform & Ground-Datum Integrity
- `scene.unit_settings.scale_length == 1.0` (`METRIC`).
- All visible non-instanced meshes have `scale ≈ (1.0, 1.0, 1.0)` (`|s - 1.0| < 1e-3`), unless explicitly justified.
- Standing props/structures contact their ground/floor datum (`world_min_z` within `±0.005 m` of target surface—zero accidental floating or buried feet/bases).
- Camera `clip_start >= 0.005` and `clip_end` reaches beyond the farthest visible environment geometry.

### Gate `G2` — Mesh & Topology Health
- `0` loose vertices or loose edges on renderable meshes (loose geometry corrupts bounding boxes and skinning).
- `0` zero-area degenerate faces (`area < 1e-8`).
- `0` unintentional non-manifold edges on closed solid volumes (booleans, SDF targets, refractive crystals).
- Outward-consistent normals (no dark/inside-out shading patches or vanished backfaces).

### Gate `G3` — Material, Color Space & Compositor Compliance
- `0` missing external image files (`img.has_data` / `os.path.exists(bpy.path.abspath(img.filepath))` for unpacked file images).
- Every Normal, Roughness, Metallic, Displacement, or packed ORM image texture uses `colorspace_settings.name == 'Non-Color'` (never `'sRGB'`).
- `scene.view_settings.view_transform` matches the look contract (`'Standard'` for cel/painterly anime & exact-hex turnarounds; `'AgX'` for HDR photoreal/dark fantasy; `'Khronos PBR Neutral'` for `.glb` look-dev).
- If `scene.use_nodes` and `scene.compositing_node_group` is active:
  - Contains a `CompositorNodeRLayers` (`Render Layers`) node wired to `NodeGroupOutput` (and **never** wires `NodeGroupInput` as image source!).
  - Declares an `'Image'` output socket on `compositing_node_group.interface`.

### Gate `G4` — Four-Angle Visual Inspection (`look` / Render Check)
Capture and visually inspect with `look` (live MCP) or rendered PNGs (`read_file`):
1. **`camera`** (`shading="rendered"`): Exact render framing, lighting ratio, palette accuracy, silhouette separation, and zero clipped background hills/clouds.
2. **`three_quarter`** overview: Spatial staging, negative space, 70/20/10 detail balance, and no stray scatter source objects sitting visible in the background.
3. **Low-Angle Ground/Join Contact View** (camera near contact plane or prop socket): Confirms wraps hug the shaft, crystals seat cleanly in bezels, and trees/rocks root firmly into terrain without air gaps.
4. **`wireframe` / `solid` cavity check**: Confirms clean bevel catchlights, reasonable polygon density, and zero intersecting/exploding boolean slivers.

### Gate `G5` — Output File & `.glb` Export Verification
- **Rendered Stills / Sequences**: Confirm file exists on disk, exact pixel dimensions (`1920×1080` / `3840×2160`), non-zero RGB standard deviation (catches the 0.1s blank-frame compositor bug or camera-inside-wall occlusion immediately!), and zero viewport gizmo/grid burn-in.
- **`.glb` Exports**: Confirm non-zero file size, zero unbaked procedural-only materials (every exported material has baked image maps or intentional Principled BSDF scalars), and `+Y` Up alignment.

---

## 2. Diagnostic Symptom → Root Cause → Fix Table

| Symptom | Root Cause | Exact Fix |
| :-- | :-- | :-- |
| **Render finishes in ~0.1s and image is completely blank/transparent** | Blender 5.x `scene.compositing_node_group` sources image from `Group Input` or lacks `ng.interface.new_socket("Image", in_out="OUTPUT", ...)` | Replace `Group Input` with `CompositorNodeRLayers`, add `NodeSocketColor` output on `ng.interface`, wire to `NodeGroupOutput.inputs["Image"]` (`00`) |
| **Anime / pastel colors look muddy, gray, or milky** | `view_transform` left at default `'AgX'` OR sRGB floats (`0.9, 0.5, 0.5`) written raw into linear sockets | Set `view_settings.view_transform = 'Standard'` AND convert colors via `srgb_to_linear()` or sample `img.pixels` (`01`, `04`) |
| **Normal map looks shiny/lumpy or seams flip harshly along UV borders** | Normal or Roughness image left at `'sRGB'` color space, or DirectX (`-Y`) green channel used instead of OpenGL (`+Y`), or tangents unexported | Set `img.colorspace_settings.name = 'Non-Color'`; invert G channel if DirectX map; export `.glb` with `export_tangents=True` (`05`) |
| **Distant mountains, sky domes, or clouds are sliced cleanly in half** | Default `camera.data.clip_end = 1000.0` (or viewport `clip_end = 1000.0`) | Raise `camera.data.clip_end = 5000.0` (keep `clip_start >= 0.05` so Z-precision stays clean) (`01`) |
| **Bevel width is uneven (wide on Z, paper-thin on X/Y) or UVs stretch** | Object has unapplied non-uniform scale (e.g., `(0.2, 0.2, 3.5)`) | Apply Scale (`Ctrl+A -> Scale` / `bpy.ops.object.transform_apply(scale=True)`) (`01`, `02`) |
| **Dark diagonal shading smears across flat hard-surface faces** | `Bevel (Segments=1)` or smooth shading without `Weighted Normal` | Set `Bevel Segments = 2` + add `Weighted Normal (Keep Sharp = True)` at bottom of modifier stack (`02`) |
| **Exported `.glb` turns pure white or flat gray in Three.js** | Material relied on Blender-only procedural nodes (`Noise`, `ColorRamp`, `Shader to RGB`, `AO`) | Bake material channels to PBR PNGs (`Ucupaint` / `Mat-Baker` / Cycles Bake) and wire to `Principled BSDF` before export (`05`) |
| **Falling petals/snow render fine in viewport play but missing on headless frame 120** | Legacy Particle System physics cache not baked | Replace particle physics with closed-form Geometry Nodes `Scene Time` position/wrap math (`03`) |
| **Grass or trees spawn floating mid-air above terrain** | Scene-wide `ray_cast` hit a fog volume, gobo plane, or emitter mesh, OR scatter source object isn't at `(0, 0, 0)` | Raycast the specific `Terrain` mesh (`Object Info -> Raycast`) and reset scatter source location to `(0, 0, 0)` in a hidden collection (`03`) |
| **Glowing crystal looks like a flat white 2D sticker** | Uniform `Emission` across entire surface with zero grazing attenuation | Drive `Emission Strength` through inverted `Layer Weight (Facing)` inside a refractive `Transmission` shell + add a real `Point` light + Compositor `Bloom` (`04`) |
