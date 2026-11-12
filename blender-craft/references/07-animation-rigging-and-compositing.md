# 07 — Slotted Animation, Rigging, Secondary Motion & 5.x Compositing

---

## 1. Slotted Actions & Animation Polish in Blender 5.x

1. **Shared Multi-Object Slotted Actions**:
   - In Blender 5.x, one `Action` (e.g., `ACT_Shot03_Strike`) can hold synchronized slots for `RIG_Hero`, `GEO_ArcaneStaff`, `CAM_Shot03`, and `LGT_CrystalBurst`! That keeps timing changes locked in a single Action/NLA strip instead of drifting across four separate data-blocks.
   - Always inspect and set interpolation via `action.layers -> strips -> channelbags -> fcurves` (`00-blender5-api-and-gotchas.md`).
2. **Interpolation Choice**:
   - **Turntables, looping shader/wind drivers, constant camera tracks**: `'LINEAR'` (default `'BEZIER'` eases in/out and stalls at loop boundaries!).
   - **Character & prop performance**: `'BEZIER'` (`AUTO_CLAMPED` handles to prevent overshoot wobble) with deliberate **anticipation → snappy spacing → overshoot/settle**, or stepped `'CONSTANT'` / **On-Twos** (hold every 2 frames at `24 fps` = `12 fps` anime character animation against smooth `24 fps` panning camera backgrounds!).
3. **Prop Pickup / Handoff Without Popping (`Child Of` Constraint)**:
   - Never reparent an object mid-scene. Add a **`Child Of`** constraint on `StaffRoot` targeting the character's `hand_ik.R` bone, click **Set Inverse**, and keyframe `Influence` `1.0 → 0.0` alongside visual-transform keys (`Insert Visual LocRot`) on the exact release frame.

---

## 2. Rigify & Procedural Secondary Motion (`Bone Info`)

- **Rigify (`rigify`, enabled)**:
  - Add meta-rigs (`Add -> Armature -> Rigify Meta-Rigs`), align bones in Edit Mode with **X-Axis Mirror** ON, keep slight natural bend (`2°–5°`) in knees and elbows so IK pole vectors know which direction to bend, apply scale `(1,1,1)` on both mesh and metarig, and generate the rig.
- **Soft Chains (Tassels, Lanterns, Ribbons, Hair, Cloaks)**:
  - For deterministic viewport/render playback without cloth-cache headaches: rig 3–5 bone chains with damped rotational follow-through or read bone velocity inside Geometry Nodes via **`GeometryNodeBoneInfo`** (new in Blender 5.1) to bend trailing ribbons, tassels, or magic embers procedurally in real time!

---

## 3. Blender 5.x Compositing & DaVinci Resolve EXR Handoff

### Linear vs. Display Order Inside `scene.compositing_node_group`
Order matters physically in the 5.x Node-Group Compositor:
1. **`CompositorNodeRLayers`** (`Render Layers` — **never** `NodeGroupInput`!)
2. **Scene-Linear Physical Optical Passes**:
   - `Kuwahara` (`Type = "Anisotropic"`, `Size = 3–5`) — painterly brush abstraction (stylized scenes only)
   - `Defocus` / Depth-of-Field *(prefer real Camera `Depth of Field` in EEVEE/Cycles over post Z-defocus to avoid halo artifacts on foreground silhouettes!)*
   - `Glare` (`Type = "Bloom"` or `"Fog Glow"`, `Quality = "High"`, `Highlights Threshold = 0.9–1.5`) — operates on linear HDR values `> 1.0`
3. **Atmosphere / Mist Blend**:
   - Enable `View Layer -> Passes -> Data -> Mist` (`scene.world.mist_settings.start`, `.depth`, `.falloff = 'QUADRATIC'`). Blend `RLayers.outputs["Mist"]` via `Mix (RGBA)` to inject subtle aerial depth tint across complex multi-material scenes in a single node!
4. **Subtle Lens Finish (Restrained!)**:
   - Never slap heavy chromatic aberration, aggressive barrel distortion, or fake watermarks onto clean renders. Keep `Lens Distortion` dispersion `≤ 0.008` if used at all.
5. **`NodeGroupOutput`** (`ng.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")`).

### Multi-Layer EXR Export for DaVinci Resolve Finishing
When finishing color, glow, micro-texture, and SFX in **DaVinci Resolve**:
- Render **16-bit Half-Float `OpenEXR MultiLayer`** (`DWAA` compression for compact beauty+passes, or lossless `ZIP` / `PIZ` when Cryptomatte masks are included — never lossy `DWAA` on Cryptomatte ID channels!):
  - Enable `Combined`, `Mist` / `Depth`, `Emission`, `Shadow Catcher` (if compositing), and `Cryptomatte (Object + Material)` on the View Layer.
  - Keep `Color Management -> Follow Scene` on PNG previews, while EXRs preserve full unclipped scene-linear dynamic range for Resolve CDL/color-wheel grading.
