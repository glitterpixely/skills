# 02 — Modeling, Topology, Curves & Hero Fantasy Props

Clean modeling comes from strict hierarchy of scale (**70% Primary Silhouette / 20% Secondary Structure / 10% Tertiary Micro-Detail**) and non-destructive modifier ordering.

---

## 1. Non-Destructive Modifier Stack Order

Modifier order is evaluated top-to-bottom. Out-of-order stacks cause shading pinches, UV stretching, and exploding booleans:

### Workflow A — Mid-Poly Hero Props & Game/Web `.glb` Assets (Bevel + Weighted Normal)
Best for staffs, weapons, architectural trim, furniture, chests, crystals, and modular environment kits:
1. **`Mirror`** (`Merge` + `Clipping` enabled) / **`Array`**
2. **`Solidify`** (`Even Thickness = True`, `Rim = Fill`) — for cloth wraps, armor plates, collars, petals
3. **`Boolean`** (`Solver = Exact` for clean watertight intersections, or `Fast`/`Manifold` when `Exact` hits coplanar float edge cases; offset cutter faces by `0.0002 m` so faces are never coplanar)
4. **`Bevel`** (`Limit Method = Angle` at `30°–35°` or `Weight`, `Segments = 2` [with `Profile = 0.5–0.7`] or `3`, **`Clamp Overlap = True`** until overlaps are resolved, `Miter Outer = Arc` to eliminate corner star-poles)
5. **`Weighted Normal`** (`Keep Sharp = True`, `Weight = 50–100`; requires Smooth Shading / Auto Smooth so flat faces stay crisp and specular highlights never warp across large polygons)
6. **`Triangulate`** *(at export time only, `Keep Normals = True`)* so tangent-space normal maps match identically between Blender and Three.js/Unity/Unreal.

### Workflow B — Subdivision Surface (`SubD`) Organic & Close-Up Cinema Hero Assets
Best for sculpted gnarly wood, character faces/hands, curved pottery, flowing ribbons, and creature anatomy:
1. **`Mirror`**
2. **`Shrinkwrap`** *(when conforming wraps/emblems to an underlying form)*
3. **`Solidify`**
4. **`Bevel`** (`Segments = 2`, `Profile = 1.0`!! — `Profile = 1.0` inserts pure quad holding/support loops on either side of marked Bevel-Weight edges without rounding the corner prematurely!)
5. **`Subdivision Surface`** (`Levels Viewport = 1` or `2`, `Render = 2` or `3`, `UV Smooth = Keep Corners`)

> **Rule**: Never stack `Weighted Normal` *before* `Subdivision Surface`, and never leave `Segments = 1` on a shaded `Bevel` without either `Harden Normals` + `Weighted Normal` or custom sharp edges (1-segment bevels smear vertex normals across adjacent large faces).

---

## 2. Curve-Driven Hero Prop Craft (Staffs, Vine Spirals, Cloth Wraps, Filigree)

Twisted shafts, coiled vines, grip wraps, cables, braids, and ornamental filigree are slow and lumpy when box-modeled by hand, and clean and parametric when built from curves:

1. **Spirals, Helices & Knots (`extra_curve_objectes`)**:
   - Enabled in Blender (`Add -> Curve -> Curve Spirals -> Archemedian / Logarithmic / Spheric / Torus` or `Knots -> Celtic / Torus / Braid`).
   - For a vine or ribbon spiraling up a tapered staff shaft:
     1. Generate a `Helix` curve slightly wider than the shaft radius with `36–64` steps per turn.
     2. Add a **`Shrinkwrap`** modifier targeting `ShaftWood` (`Wrap Method = Nearest Surface Point` or `Project`, `Offset = 0.002 m`, `Apply on Spline = True`) so the curve hugs every organic bend and taper of the wood automatically!
2. **Tapering & Tilting Curves**:
   - For organic branches, tendrils, horns, and roots: give the curve `curve.bevel_depth = 0.025`, `curve.bevel_resolution = 4–6`, and vary per-point radius (`point.radius` in `bpy` or `Alt+S` in Edit Mode from `1.0` at base to `0.05` at tip) and tilt (`point.tilt` / `Ctrl+T`).
   - For **flat cloth grip wraps**: bevel the spiral curve with a flat rectangular profile curve (or convert to a ribbon strip → `Shrinkwrap` to shaft → `Solidify` `0.0025 m` → `Bevel` `0.0008 m` → slight overlapping edge rotation so each wrap tucks under the previous turn!).
   - **Auto-Generated Curve UVs**: Blender curve geometry automatically generates clean `0→1` longitudinal UVs along the spline (`use_uv_as_generated` / built-in `UVMap`), meaning wood-grain, rope-braid, and woven-linen textures follow every twist automatically! When converting to mesh (`bpy.ops.object.convert(target='MESH')`), duplicate the live curve into a hidden `COL_Backup_Curves` collection first.

---

## 3. Faceted Crystals, Carvings & Hard-Surface Silhouettes

- **Hero Crystals (`extra_mesh_objects` / `bmesh`)**:
  - Real quartz/arcane crystals are **asymmetric**: start with a 6- or 7-sided prism (uneven face widths via slight per-axis radial jitter `±8%`), taper into an off-center apex point (`5–8` irregular facets meeting at top), add 2–4 smaller daughter crystal shards sprouting from the base socket at `18°–38°` splay angles, and apply a micro-bevel (`0.0015 m`, `Segments = 2`) so every facet edge catches a bright specular highlight.
- **Clean Cylindrical Cutouts & Sockets (`looptools` + `EdgeFlow`)**:
  - Cutting a circular gem socket or rune into a curved cylinder creates shading ripples if supported with raw booleans alone.
  - Select the boundary loop → `LoopTools: Circle` (`Flatten = False` or project onto cylinder) → inset one clean containment ring (`I`) around the hole → run `EdgeFlow: Set Flow` on surrounding longitudinal edges to restore true cylindrical curvature without pinching.

---

## 4. Topology Health Invariants

Before moving to UVs, rigging, or export, every mesh must satisfy:

| Metric | Requirement | Why |
| :-- | :-- | :-- |
| **Scale & Rotation** | `scale == (1, 1, 1)` (`±1e-4`) | Prevents skewed bevels, warped normals, and broken glTF hierarchies |
| **Normals** | 100% outward-consistent (`bmesh.ops.recalc_face_normals`) | Inverted faces turn invisible in back-face-culled game engines (Three.js default `FrontSide`) and render black in booleans/refraction |
| **Non-Manifold Edges** | `0` on closed solids/volumes; intentional boundary edges only on open cloth/foliage cards | Non-manifold T-junctions and internal faces break SubD, 3D printing, SDF volume conversion, and AO baking |
| **Loose Verts / Edges** | `0` (`bmesh` cleanup) | Inflates bounding boxes (`world_bounding_box` miscalculates ground datum!) and breaks skinning |
| **Zero-Area / Degenerate Faces** | `0` (`Merge by Distance = 0.0001 m`) | Produces `NaN` tangents during normal-map baking and Three.js shader compilation |
| **N-Gons (`>4` verts)** | Allowed **only** on dead-flat planar caps guarded by an inset ring; `0` on curved or deforming surfaces | Uncontrolled triangulation across curved N-gons creates diagonal shading creases |

### Fast `bmesh` Mesh Hygiene Snippet

```python
import bpy, bmesh

def clean_mesh_object(obj, merge_dist: float = 1e-4):
    if obj.type != "MESH":
        return
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge_dist)
    loose_verts = [v for v in bm.verts if not v.link_edges]
    if loose_verts:
        bmesh.ops.delete(bm, geom=loose_verts, context="VERTS")
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
```

---

## 5. Sculpt-to-Game / Prop Retopology Pipeline

When organic forms (gnarled roots, creature heads, carved dragon pommels, eroded cliffs) start in Sculpt Mode:
1. Block silhouette with **Snake Hook / Clay Strips / Crease** using Dynamic Topology or Voxel Remesh (`Ctrl+R`, coarse `0.02 m` → medium `0.005 m` — never jump to `0.001 m` before primary proportions read cleanly from 5 meters away).
2. Duplicate the high-poly sculpt (`_HP` suffix).
3. Retopologize the low/mid-poly target (`_LP` suffix):
   - **Manual hero loops** (faces, joints, clean trim borders): `PolyQuilt` (`bl_ext.blender_org.PolyQuilt_Fork` if installed) or Snap-to-Face + `F2` + `LoopTools: Relax`.
   - **Automated clean quad flow**: `Quad Remesher` (commercial gold standard) or Blender's Quadriflow (`bpy.ops.object.quadriflow_remesh(target_faces=4000, use_preserve_sharp=True)`).
4. Unwrap `_LP`, then bake Normal + AO + Curvature from `_HP` → `_LP` (`05-uvs-baking-and-glb-export.md`).
