# 06 — Cinematography, Multi-Angle Graybox Plates & AI-Video Previz

Blender is an unbeatable spatial-continuity engine for **Seedance 2.5**, **MiniMax H3**, **Kling**, and **Midjourney** workflows: a 10-minute 3D blockout locks exact room geography across 180° over-the-shoulder (OTS) cuts, steep low-angle hero shots, and 3-in-1 turnaround sheets where 2D-only generators hallucinate walls, props, or rear costume details.

---

## 1. Lens & Focal Length Storytelling (`36mm` Full-Frame Sensor Standard)

Keep `camera.data.sensor_width = 36.0` so focal lengths map 1:1 to real full-frame cinema glass:

| Focal Length | Spatial & Emotional Effect | Best Shot Use |
| :-- | :-- | :-- |
| **`18 – 24 mm`** | Expands interior volume, exaggerates z-axis speed and towering height; distorts faces if `< 0.8 m` away | Dynamic action lunges, cavernous dragon lairs, sweeping ceiling-to-floor reveals |
| **`28 – 35 mm`** | Natural wide-narrative cinema master (`35mm` anamorphic feel); keeps environment context around two characters | Master 2-shots, corridor tracking, courtyard staging plates |
| **`50 mm`** | Neutral human perspective compression | Medium dialogue, prop handoffs, tabletop/workbench views |
| **`75 – 105 mm`** | Flattering facial proportions, strong background separation, compressed spatial depth | OTS reverse close-ups, character portrait panels, hero weapon turntables |
| **`135 – 200 mm`** | Near-isometric compression, monumental distant scale (huge moon/castle behind small figure) | Extreme macro inserts (crystal facet, blade lock, eye reflection), 3-in-1 turnaround sheets |

### True Two-Point Architectural Verticals (`shift_x` / `shift_y`)
Tilting a wide `24mm` camera upward (`rotation_euler.x = 102°`) makes vertical pillars and walls converge inward like falling dominoes.
- **Architectural / Ghibli / Interior Rule**: Set `camera.rotation_euler.x = math.radians(90.0)` (dead level with the horizon!) and frame high ceilings or tall towers by raising **`camera.data.shift_y`** (`+0.08` to `+0.25`)! Every vertical wall and doorway stays perfectly parallel to the frame edge.

---

## 2. Multi-Angle 3D Graybox Plates for Seedance 2.5 & Image Generators

When cutting between multiple angles inside complex architecture (taverns, shrines, throne rooms, bridges, village lanes):

1. **Fast Blockout (`archimesh` + `Bagapie` + Primitives)**:
   - Build only **major spatial anchors** at real metric scale: floor elevation steps, walls, windows/arches, furniture silhouettes, foreground occlusion pillars, and mannequin capsules/cylinders (`1.72 m` tall) marking Character A and Character B positions + eyelines.
   - Leave surfaces **untextured neutral clay** (`#B8B8B8` linear `~0.48`) — noisy textures in a graybox confuse downstream image-to-image style transfer!
2. **Crisp Depth & Form Read (`Workbench` or Clean `EEVEE`)**:
   - **Option A — Workbench Clay + Cavity + Shadow** (fastest, zero shader setup):
     - `scene.render.engine = "BLENDER_WORKBENCH"`
     - Enable `show_cavity = True` (`cavity_type = "BOTH"`, crisp ridge + valley AO) and `show_shadows = True` aligned to the scene's actual key-light direction!
   - **Option B — EEVEE Soft Key + Window Gobos**:
     - Best when strong directional sunlight beams, window shafts, or practical lantern pools must lock lighting continuity across every cut.
3. **Multi-Camera Coverage Setup**:
   - Create named cameras for the entire `[Cut to]` cluster in one `.blend` file:
     - `CAM_01_Master_Wide` (`32mm`)
     - `CAM_02_OTS_A_to_B` (`65mm`, placed just over Mannequin A's right shoulder—respecting the **180° line of action** so Character A stays screen-left and Character B stays screen-right across every reverse!)
     - `CAM_03_OTS_B_to_A` (`65mm`, symmetric reverse on the **same side** of the 180° axis!)
     - `CAM_04_Insert_Low` (`85mm`)
   - Render all cameras cleanly via `bpy.ops.render.render(write_still=True)` (never viewport screen-grabs with grid lines, 3D cursor, camera wireframes, or orange selection outlines!).

---

## 3. 3-in-1 `16:9` Composite Turnaround Rig (`[3/4 Rear | Front | Macro]`)

Compresses three reference angles of a 3D prop, weapon, creature, or character into a **single `1920×1080` or `3840×2160` (`16:9`) `@Image` slot** for Seedance 2.5 so 180° reverse shots never hallucinate the back of a weapon, cape, or hairpiece:

1. **Background**: Flat solid neutral `#E0E0E0` (or `#FFFFFF` when specified) world background under `scene.view_settings.view_transform = "Standard"` so the background pixel value renders exact and uniform with zero vignette!
2. **Lens**: Long `85–120 mm` (or `ORTHO`) to eliminate wide-angle nose/pommel distortion.
3. **Three Sub-Renders (`640×1080` or `1280×2160` each, stitched losslessly left-to-right into exact `16:9`)**:
   - **Left Panel**: `3/4 Rear` (`yaw = +145°`) — locks rear silhouette, cape/scabbard/wrap seam, and back-of-head/shaft construction.
   - **Center Panel**: `Front Full-Length` (`yaw = 0°`) — full silhouette from toe/pommel to crown/finial inside frame with `6–8%` breathing margin.
   - **Right Panel**: `Extreme Macro Hero Detail` — tight close-up on the face portrait or primary arcane crystal/hilt mechanism.
4. **360° Video Turnaround (`turnaround_camera`)**:
   - Select the hero prop root (`StaffRoot`) and invoke the installed **Turnaround Camera** extension (or animate an orbit Empty `0° → 360°` with **`LINEAR`** F-Curve interpolation over frames `1..120`, rendering frames `1..119` so frame `120` does not duplicate frame `1` on loop!).

---

## 4. Camera Motion & Delivery Discipline

- **Full-Frame `16:9` Purity**:
  - Set `render.resolution_x = 1920` (or `3840`), `render.resolution_y = 1080` (or `2160`), `render.resolution_percentage = 100`, `pixel_aspect_x = pixel_aspect_y = 1.0`.
  - **Never bake black letterbox bars** into plates destined for AI video generators or Resolve timelines unless explicitly requested.
- **Motivated Camera Rigging (`add_camera_rigs` + `camera_shakify`)**:
  - Parent cameras to an **Aim Empty** (`Track To` constraint: `-Z` track axis, `Y` up) or use **Add Camera Rigs (Dolly / Crane)** rather than keyframing raw camera Euler angles (which causes curved arc wobble and gimbal drift).
  - Add subtle organic life to static or tracking cinema shots with **Camera Shakify** (`Camera Properties -> Camera Shakify -> Investigation / Handheld Subtle`, `Influence = 0.12–0.30` — keep restraint high; `1.0` looks like an earthquake).
- **Cut-Free Action Span Timing**:
  - When rendering animated 3D action takes or previz at `24 fps`, sustain clean, readable single-camera motion across `60–96` frames (`2.5–4.0 s`) per shot rather than hyper-cutting sub-second fragments.
