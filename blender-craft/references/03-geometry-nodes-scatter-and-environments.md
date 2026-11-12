# 03 — Geometry Nodes 5.x, Procedural Scattering, Foliage & Environments

Blender 5.0 and 5.1 turned Geometry Nodes into a full procedural scene, volume, and FX engine. Follow these rules so dense forests, meadows, ruins, and falling petals stay at 60 FPS in the viewport and render cleanly on any isolated frame.

---

## 1. New Blender 5.0 / 5.1 Geometry Nodes Capabilities

1. **Bundles & Closures (5.0+)**:
   - **Bundles** (`Combine Bundle` / `Separate Bundle` / `GeometryNodeGetGeometryBundle`) pack multiple geometries, fields, and material parameters into a single wire—ideal when passing `{trunk_mesh, canopy_points, wind_phase, age_factor}` between modular generator groups without 18-socket spaghetti.
   - **Closures** (`Closure` zone / `Evaluate Closure`) let a master scatter or architecture node group accept custom placement/profile logic from the caller without duplicating the entire scatter modifier.
2. **SDF & Density Volume Grids (5.0–5.1)**:
   - Nodes: `GeometryNodeMeshToSDFGrid`, `GeometryNodePointsToSDFGrid`, `GeometryNodeSDFGridBoolean`, `GeometryNodeSDFGridFillet`, `GeometryNodeGridDilateAndErode`, `GeometryNodeGridToMesh`, `GeometryNodeDistributePointsInGrid`, `GeometryNodeGridAdvect`.
   - **Prime use case**: Fuse modular rock kits, gnarled tree roots, melted wax, snow accumulation, or cave walls via `Mesh to SDF Grid` → `SDF Grid Boolean (Union)` / `SDF Grid Fillet` → `Grid to Mesh` for seamless organic blends with zero boolean intersection seams, or build stylized cumulus cloud banks via `Points to SDF Grid` + 3D noise displacement.
3. **Rig Synergy (`GeometryNodeBoneInfo`, 5.1)**:
   - Read live armature bone transforms directly inside Geometry Nodes to drive procedural cloth ripples, glowing staff energy trails, feather splay, or footsteps in mud/snow without baking Alembic caches.
4. **5.1 Node Tool Asset `idname` Rule**:
   - Custom Geometry Nodes Tool assets saved in older `.blend` libraries should be opened and re-saved in Blender 5.1 so their global unique `idname` metadata registers cleanly.

---

## 2. Closed-Form `Scene Time` FX vs. Particle Physics (Critical Rule)

**Prefer Geometry Nodes driven by `Scene Time` over legacy Particle Systems** for falling cherry petals, autumn leaves, drifting ash/embers, fireflies, snow, rain, and wind-swaying grass:
- **Why legacy particles fail**: Particle physics requires sequential simulation/baking from frame 1. Rendering frame `140` directly in `-b` headless mode (or tweaking wind mid-project) yields empty frames or stale caches; `ps.settings.hair_length` also invisibly scales object instances (`0.01` = microscopic), and `ps.seed` lives on `ParticleSystem`, not `ParticleSettings`.
- **Why closed-form `Scene Time` wins**: Computing position `P(t)` and rotation `R(t)` as pure deterministic math of `Scene Time (Seconds)` + per-point `ID` hash requires **zero baking**, loops or seeks to any frame instantly, and works identically in viewport, MCP `look(mode="frames")`, and headless batch renders:

```text
Point P(i, t):
  x = x0(i) + wind_x * t + amp_x * sin(freq_x * t + phase(i))
  y = y0(i) + wind_y * t + amp_y * cos(freq_y * t + phase(i) * 1.37)
  z = wrap(z0(i) - fall_speed(i) * t, min=z_floor, max=z_ceiling)   # Math Node -> Wrap!
  rot = euler(t * spin_rate_x(i), tilt_base + 0.35 * sin(2.1 * t + phase(i)), t * spin_rate_z(i))
```
Using `Math (Wrap)` on `Z` recycles falling petals/ash infinitely inside the camera frustum volume with a constant point count!

---

## 3. Production Ecosystem Scattering Architecture

Whether building a custom Geometry Nodes scatter setup, using **BagaPie** (`bl_ext.blender_org.Bagapie`, installed & free), or using **Geo-Scatter + Botaniq** (commercial), apply the **5 Laws of Believable Scattering**:

### Law 1 — Never Realize High-Count Instances Prematurely
- Feed a collection of variants (`Collection Info` with `Separate Children = True`, `Reset Children = True`) into `Instance on Points` (`Pick Instance = True`).
- Keep `Realize Instances` **OFF**! `200,000` instanced grass clumps and `4,000` trees consume `< 150 MB` as instances vs. `25+ GB` and viewport lockup if realized.
- Only realize low-count hero meshes when downstream vertex deformation or single-mesh boolean export requires it.

### Law 2 — Ecological Hierarchy & Poisson Disk Clumping (Avoid "CGI Polka Dots")
Uniform white-noise random scatter immediately looks fake. Nature grows in **multi-tier clusters**:
1. **Tier 1 — Canopy / Hero Anchors** (large trees, boulders, ruins): `Distribute Points on Faces (Poisson Disk)`, `Distance Min = 3.5–8.0 m`, driven by broad low-frequency `Noise Texture` (`Scale = 0.04` → `ColorRamp` threshold) so clearings and groves alternate naturally.
2. **Tier 2 — Understory / Shrubs / Saplings**: High density *near* Tier 1 trunks/boulders (`Geometry Proximity` to Tier 1 points mapped via `Map Range`: `0.8 m → 4.5 m` = dense skirt, `> 6 m` = sparse).
3. **Tier 3 — Ground Cover** (clover, ferns, fallen leaves, pebbles, wildflowers): `Poisson Disk` (`Distance Min = 0.12–0.35 m`), clustered in patches by species (yellow flowers in warm sunlit pockets, moss/ferns in damp concave gullies).
4. **Tier 4 — Grass Carpet**: Clump cards (`0.3–0.6 m` patches of 15–40 blades per asset, NOT single individual blades!) with `Scale` randomized `0.65–1.35` and `Z` rotation `0–2π`.

### Law 3 — Abiotic Masks (Slope, Altitude, Curvature, Footpaths)
Multiply selection/density probabilities before `Instance on Points`:
- **Slope Mask**: `dot(Normal, (0, 0, 1))` → steep cliff faces (`dot < 0.65`, i.e., `> 49°`) reject soil/grass/trees and expose bare rock; gentle slopes (`dot > 0.82`) hold deep grass.
- **Normal Alignment**: Mix **Surface Normal** (`20–35%`) with **World `+Z` Up** (`65–80%`) for phototropic plants (trees and flowers grow toward the sky even on a `25°` hillside; rocks, moss, and fallen logs align `85–100%` to the slope normal!).
- **Path / Hero Clearing Mask**: Subtract distance to a Bezier footpath curve or hero character staging Empty (`Geometry Proximity < path_half_width` → density `0`, with short trampled border grass along the verge).

### Law 4 — Camera Frustum & Distance Optimization
For massive vista shots:
- Pass the active camera via `Camera Info` / `Object Info (Camera)`:
  - **Frustum Culling**: Transform candidate points into camera view space; cull points outside the camera FOV cone *(keep a `2–5 m` world-space safety margin behind/beside the camera near-plane so tall off-screen trees still cast shadows into the shot!)*.
  - **Distance Falloff**: Reduce small ground-cover density smoothly beyond `35–60 m` where blades are sub-pixel, letting terrain shader macro-variation carry distant hills.

### Law 5 — Explicit Ground Raycasting & Clean Flower/Foliage Proportions
- **Raycast Trap**: When projecting scattered assets or camera targets onto uneven terrain, **always raycast the explicit terrain object** (`Object Info [Terrain]` → `GeometryNodeRaycast`, or `terrain_obj.ray_cast(...)` in Python), **never** `scene.ray_cast()`, which hits fog volumes, petal emitter planes, and gobo cards!
- **Stylized Flower Geometry Rule**: Keep individual petal width at **~50% of the radial arc spacing** (`π * D / (2 * N_petals)`) so an 8-petal flower shows crisp negative space between petals instead of fusing into a crumpled paper disc; size the center stamen disc relative to petal length (`~0.28–0.38×`), and tilt flower heads `~20°–30°` toward camera (`> 50°` reads as flat confetti on the ground).

---

## 4. Using Installed Free Tools vs. Geo-Scatter & Botaniq

- **Installed Right Now (`Bagapie` + `antlandscape` + `modular_tree` + `ivygen`)**:
  - Press **`J`** in the 3D Viewport with target object(s) selected to open the **BagaPie** pie menu: instant **Scatter**, **Paint Scatter**, **Ivy** (grows climbing vines toward light from a target point), **Array on Curve**, **Cables** (catenary sag between two surfaces), and parametric **Architecture** (walls, stairs, windows, tiles, fences).
  - Use **`A.N.T. Landscape`** (`Add -> Mesh -> Landscape`) for eroded ridges, riverbeds, and strata rocks, and **`Modular Tree`** (`Node Editor -> Mtree`) for custom fantasy trunks/roots.
- **When Geo-Scatter + Botaniq Add Major Value**:
  - **Botaniq (`polygoniq`, managed via `engon`)** provides hundreds of pre-modeled, pre-textured, seasonal (spring/summer/autumn/winter), wind-ready trees, palms, grasses, flowers, mushrooms, and pots so you do not have to model or texture botanical species from scratch.
  - **Geo-Scatter** adds 1-click **Biome** multi-layer presets (load a complete 6-layer forest floor + canopy from Botaniq/Biome packs in one click), advanced wind-wave turbulence fields, shadow-aware frustum culling, and ecosystem clumping UI.
  - **Conflict Warning**: Never install free `Biome-Reader` and paid `Geo-Scatter` simultaneously in the same Blender version—pick one (`Geo-Scatter` supersedes `Biome-Reader`).
  - **`.glb` / Three.js Export Caveat**: Neither Geo-Scatter nor BagaPie should export `100,000` realized high-poly Botaniq trees into a browser `.glb`! Keep web `.glb` worlds to low-poly instanced kits (`export_gpu_instances=True`, `< 5,000` instances of `< 1,500`-tri foliage assets) or render high-density Botaniq/Geo-Scatter scenes in Blender as background plates/videos.
