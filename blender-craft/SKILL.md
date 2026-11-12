---
name: blender-craft
description: >-
  Build, light, shade, scatter, bake, animate, and verify 3D props, environments, painterly/cel
  anime scenes, multi-angle AI-video graybox/turnaround plates, and game-ready GLB assets in Blender
  5.x (live MCP or headless bpy/bmesh). Trigger terms: Blender, Blender 5, bpy, bmesh, Geometry
  Nodes, EEVEE, Cycles, cel shading, anime look, 3D blockout, graybox, scatter, foliage, Ucupaint,
  BagaPie, Geo-Scatter, Botaniq, UV unwrap, PBR bake, GLB export, headless Blender.
---

# Blender 5.x Production Craft & Architecture

Rulebook, verified Blender 5.1+ (`Python 3.13`) code recipes, addon playbooks, and diagnostic gates (`G1`–`G5`) for building hero props, procedural environments, painterly/anime renders, multi-angle AI-video reference plates, and clean `.glb` exports.

For end-to-end browser games and interactive Three.js worlds with Playwright WebGL gates, pair this skill with `gemini-4-argon-3d-worlds` and `threejs-rendering`.

---

## Reference Map — Load Only What the Task Needs

| Need | Read |
| :-- | :-- |
| Blender 5.0/5.1+ API breaks (Slotted Actions, Node-Group Compositor, `Python 3.13`), MCP vs Headless `blender -b` | [00-blender5-api-and-gotchas.md](references/00-blender5-api-and-gotchas.md) |
| Metric scale, datum alignment, 5.0+ Working Color Spaces, `AgX` vs `Standard` vs `PBR Neutral`, linear color math, lighting | [01-scene-scale-color-and-lighting.md](references/01-scene-scale-color-and-lighting.md) |
| Hero props, staffs/weapons, curve wraps/vines, SubD vs bevel/weighted-normal stacks, topology health, retopology | [02-modeling-topology-and-hero-props.md](references/02-modeling-topology-and-hero-props.md) |
| Geometry Nodes 5.x (Bundles, Closures, SDF Volume Grids), `Scene Time` FX, camera-culled scattering, foliage & terrain | [03-geometry-nodes-scatter-and-environments.md](references/03-geometry-nodes-scatter-and-environments.md) |
| Photoreal PBR breakup, crystal emission, EEVEE painterly/cel anime (`Shader to RGB` + depth haze + Kuwahara), `Ucupaint` | [04-materials-pbr-stylized-and-anime.md](references/04-materials-pbr-stylized-and-anime.md) |
| Seam hiding, strip quadrifying (`UniV`), texel density, procedural-to-PBR baking, `+Z`→`+Y` `.glb` & GPU instancing export | [05-uvs-baking-and-glb-export.md](references/05-uvs-baking-and-glb-export.md) |
| Lens language, 2-point architectural shift, multi-angle graybox plates & 3-in-1 16:9 turnaround sheets for AI video | [06-cameras-previz-and-ai-video-plates.md](references/06-cameras-previz-and-ai-video-plates.md) |
| Slotted Actions, Rigify/Child-Of prop handoffs, `Bone Info` secondary motion, 5.x Compositor & Resolve EXR passes | [07-animation-rigging-and-compositing.md](references/07-animation-rigging-and-compositing.md) |
| Apple Silicon Metal-RT & EEVEE memory tuning, Outliner hygiene, and the 27-addon installed toolkit + paid upgrade matrix | [08-performance-hygiene-and-addons.md](references/08-performance-hygiene-and-addons.md) |
| Verification gates `G1`–`G5`, 4-angle visual inspection, and Symptom → Root Cause → Fix table | [09-verification-gates-and-diagnostics.md](references/09-verification-gates-and-diagnostics.md) |

---

## Workflow

### Step 1: Choose Execution Surface & Check Live State

1. **Interactive modeling, look-dev, shading, camera framing, or editing an open `.blend`**:
   - Drive the live GUI session through MCP (`get_addon_status` → `get_scene_info` → `execute_blender_code` → `look`).
   - Pass the user's exact verbatim request in `user_prompt` on every MCP call.
   - Keep `telemetry_consent` strictly `False`. Never enable telemetry on client or personal creative files.
2. **Repeatable procedural builders, batch multi-camera renders, `.glb` asset pipelines, or offline audits**:
   - Run headless CLI: `/Applications/Blender.app/Contents/MacOS/Blender -b <scene.blend> -P <script.py>`.
   - Note: `MCP for Blender` cannot start its socket server in `-b` background mode; headless scripts run standalone via `bpy`.
3. **Extension management while GUI Blender is open**:
   - Install packages with `--online-mode --command extension install --no-prefs <pkg>` so CLI runs do not overwrite in-memory `userpref.blend` or permanently flip GUI `Online access` on, then call `bpy.ops.extensions.repo_refresh_all()`, `addon_utils.enable(..., default_set=True)`, and `bpy.ops.wm.save_userpref()` inside the live session.

### Step 2: Classify Target Look & Downstream Medium

Lock this choice **before** creating lights or materials because color management and shader graphs diverge immediately:

| Mode | Engine | View Transform | Core Material Rule |
| :-- | :-- | :-- | :-- |
| **Photoreal / Dark Fantasy** | `CYCLES` (Metal-RT) or `BLENDER_EEVEE` | `AgX` (or `ACES 2.0`) | Principled BSDF with roughness breakup, micro-normal detail, physical light falloff (`01`, `04`) |
| **Stylized PBR / Web `.glb`** | `BLENDER_EEVEE` → glTF | `Khronos PBR Neutral` | Principled BSDF or `Ucupaint` baked to `sRGB` Base Color + `Non-Color` ORM/Normal (`04`, `05`) |
| **Painterly / Cel Anime** | `BLENDER_EEVEE` only | **`Standard`** (mandatory) | `Diffuse BSDF` → `Shader to RGB` → `ColorRamp` → `Emission` + `Camera View Distance` sky haze (`04`) |
| **AI-Video 3D Graybox Plate** | `BLENDER_WORKBENCH` or `BLENDER_EEVEE` | `Standard` | Untextured clay + cavity/ridge + crisp contact shadows; zero gizmos, exact 16:9 framing (`06`) |

### Step 3: Build in Dependency Order

Fixing a downstream step before its foundation wastes hours and breaks UVs/modifiers:

1. **Scale, Datum & Working Space (`01`)**: `1 unit = 1 meter`. Standing props/characters rest at `min_z = 0.0` in local space; radial/handheld props center their grip or pivot deliberately. Set `clip_start = 0.05`, `clip_end = 5000.0` on exterior cameras so distant mountains and cloud banks never silently vanish at `1000m`.
2. **Primary → Secondary → Tertiary Geometry (`02`)**: Block large silhouettes first (70% read), medium structural joins/wraps second (20%), fine carvings/rivets last (10%). Apply scale (`Ctrl+A` → `(1,1,1)`) before any Bevel, UV unwrap, cloth/shrinkwrap, or armature bind.
3. **Instancing & Procedural Scatter (`03`)**: Keep scatter sources at world origin `(0,0,0)` inside a hidden `COL_Sources` collection with applied transforms. Drive falling petals, snow, embers, and wind sway via closed-form Geometry Nodes functions of `Scene Time` rather than particle physics caches so any isolated frame renders deterministically.
4. **UVs Before Baking or Hand-Painting (`05`)**: Mark hidden seams, quadrify curved ribbons/wraps/trims with `UniV`, unify texel density (`Texel Density Checker`), and leave `8–16 px` island padding at `2048×2048`.
5. **Materials & Lighting Together (`01`, `04`)**: Sample reference art in scene-linear space rather than guessing hex codes. Separate foreground, midground, and background with value contrast, rim lighting,Light Linking, or depth-based atmospheric perspective.
6. **Camera & Compositor (`06`, `07`)**: Build `scene.compositing_node_group` with an explicit `NodeSocketColor` output interface and source renders from `CompositorNodeRLayers` (never `NodeGroupInput`).

### Step 4: Run Programmatic & Visual Gates (`G1`–`G5`)

Never treat `Code executed successfully` or a finished CLI exit code as visual approval:

1. Run [`scripts/blender_scene_audit.py`](scripts/blender_scene_audit.py) (headless `-b -P` or inside `execute_blender_code`) to check `G1` (transforms & ground datum), `G2` (non-manifold/loose/degenerate geometry), and `G3` (missing textures, `Non-Color` data map compliance, view transform, compositor traps).
2. Capture and inspect **4 angles** via `look` or rendered PNGs (`G4`):
   - **Hero Camera** (exact render aspect, overlays off)
   - **3/4 Overview** (spatial composition and silhouette balance)
   - **Low-Angle Ground/Contact Check** (proves zero floating or sinking geometry)
   - **Wireframe / Solid Cavity Check** (proves clean edge flow, bevel catchlights, and reasonable density)
3. For rendered files or `.glb` exports (`G5`), verify output dimensions, non-zero pixel variance (catches blank compositor frames), and glTF node/material/UV counts before reporting completion.

---

## Hard Rules (Blender 5.x Non-Negotiables)

1. **Blender 5.x Slotted Actions**: `action.fcurves` does not exist. Use `action.fcurve_ensure_for_datablock(datablock=obj, data_path="location", index=0)` after assigning an `ActionSlot`, or traverse `action.layers[].strips[].channelbags[].fcurves`.
2. **Blender 5.x Node-Group Compositor**: `scene.node_tree` does not exist. Assign `scene.compositing_node_group`, declare `ng.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")`, and read the render from `CompositorNodeRLayers` — sourcing from `NodeGroupInput` short-circuits EEVEE renders into blank frames.
3. **Localization- & Enum-Safe `bpy`**: Look up nodes by `.type` (`"BSDF_PRINCIPLED"`), never `.name`. Menu sockets on 5.x compositor/geometry nodes take Title-Case labels (`"Bloom"`, `"High"`, `"Anisotropic"`), not uppercase RNA constants. Discover dynamic OCIO `view_transform` or `render.engine` values via `try/except TypeError`, because `bl_rna.properties[...].enum_items` under-reports `['NONE']`.
4. **Scene-Linear Colors**: `bpy` shader/light RGBA tuples are scene-linear, not sRGB. Convert sRGB hex values with exact IEC 61966-2-1 piece-wise gamma (`srgb_to_linear`), or sample reference art directly from `bpy.data.images[...].pixels`.
5. **View Transform Lock**: Use `Standard` for cel/painterly anime and color-exact graphic work (`AgX` desaturates bright flat colors into chalky gray). Use `AgX` for HDR photorealism/dark fantasy and `Khronos PBR Neutral` for `.glb` / Three.js parity.
6. **Procedural Shaders Do Not Export to `.glb`**: Any `Shader to RGB`, `Noise`, `Voronoi`, `ColorRamp`, `Ambient Occlusion`, or `Raycast` node graph must be baked into PBR image maps (`Base Color`, `ORM`, `Normal`, `Emission`) via Cycles Bake, `Ucupaint`, or `Mat-Baker` before `bpy.ops.export_scene.gltf()`.
7. **Terrain Raycast Isolation**: Always raycast a specific ground mesh via `Object Info` → `Raycast`, never a scene-wide `scene.ray_cast()` that collides with fog cards, light blockers, or emitter planes.
