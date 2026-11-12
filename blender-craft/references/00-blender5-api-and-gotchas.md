# 00 — Blender 5.0 / 5.1+ API Breaking Changes, Python 3.13 & Runtime Gotchas

Verified on **Blender 5.1.2 (`Python 3.13.9`, macOS arm64)**. Scripts written for Blender 3.x or 4.0–4.3 fail silently or throw `AttributeError`/`KeyError` on Blender 5.x unless they follow the patterns below.

---

## 1. Slotted & Layered Actions (`action.fcurves` Removed)

Blender 5.0 permanently removed legacy `action.fcurves`. Every `Action` is now hierarchical (`Action → Layers → Strips → Channelbags`) and partitioned by typed `ActionSlot`s so a single Action can animate multiple data-blocks (e.g., camera + target empty + key light) in lockstep.

### Creating Keyframes & Setting Interpolation Safely in 5.x

```python
import bpy
from bpy_extras import anim_utils

def ensure_fcurve_5x(datablock, action_name: str, data_path: str, index: int = 0):
    """Create or fetch an F-Curve on Blender 5.x slotted actions."""
    if datablock.animation_data is None:
        datablock.animation_data_create()

    action = datablock.animation_data.action
    if action is None:
        action = bpy.data.actions.new(name=action_name)
        datablock.animation_data.action = action

    # Ensure a compatible slot is bound to datablock
    if datablock.animation_data.action_slot is None:
        slot = anim_utils.action_get_first_suitable_slot(action, datablock.id_type)
        if slot is None:
            slot = action.slots.new(id_type=datablock.id_type, name=datablock.name)
        datablock.animation_data.action_slot = slot

    return action.fcurve_ensure_for_datablock(
        datablock=datablock, data_path=data_path, index=index
    )

def set_all_keyframes_interpolation(action, mode: str = "LINEAR"):
    """Iterate all F-Curves in a Blender 5.x Action."""
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fcu in bag.fcurves:
                    for kp in fcu.keyframe_points:
                        kp.interpolation = mode
```

- Note: `obj.keyframe_insert(data_path="location", frame=1)` still works directly and auto-creates the default layer, strip, slot, and channelbag; you only need the traversal above when reading or editing F-Curve handles, modifiers (such as Cycles/Noise), or interpolation modes.

---

## 2. Node-Group Compositor (`scene.node_tree` Removed)

`scene.node_tree` and `CompositorNodeComposite` are gone in Blender 5.x. Compositing is stored in `scene.compositing_node_group` (a `CompositorNodeTree` data-block).

### Critical Blank-Frame Trap
1. **Never wire `NodeGroupInput` as the render source.** Connecting `Group Input` instead of a `CompositorNodeRLayers` (`Render Layers`) node causes EEVEE (especially in `-b` headless renders) to short-circuit in ~0.1s and output completely blank transparent/black frames with zero error messages.
2. **Always declare an `"Image"` output socket on `ng.interface` first.** A fresh `CompositorNodeTree` creates `NodeGroupOutput` with only an empty `('', '__extend__', 'CUSTOM')` socket until `ng.interface.new_socket(...)` is called.

### Verified Blender 5.1+ Compositor Builder

```python
import bpy

def build_compositor_5x(scene, use_bloom: bool = True, use_kuwahara: bool = False):
    scene.use_nodes = True
    ng = bpy.data.node_groups.new(name=f"{scene.name}_Compositor", type="CompositorNodeTree")
    ng.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    scene.compositing_node_group = ng

    rl = ng.nodes.new("CompositorNodeRLayers")
    rl.location = (-400, 0)
    last_socket = rl.outputs["Image"]

    if use_kuwahara:
        kuw = ng.nodes.new("CompositorNodeKuwahara")
        kuw.location = (-150, 80)
        kuw.inputs["Type"].default_value = "Anisotropic"  # Title-Case menu socket!
        kuw.inputs["Size"].default_value = 4.0
        ng.links.new(last_socket, kuw.inputs["Image"])
        last_socket = kuw.outputs["Image"]

    if use_bloom:
        glare = ng.nodes.new("CompositorNodeGlare")
        glare.location = (100, 0)
        glare.inputs["Type"].default_value = "Bloom"       # Title-Case, NOT 'BLOOM'
        glare.inputs["Quality"].default_value = "High"
        glare.inputs["Highlights Threshold"].default_value = 1.0
        ng.links.new(last_socket, glare.inputs["Image"])
        last_socket = glare.outputs["Image"]

    out = ng.nodes.new("NodeGroupOutput")
    out.location = (360, 0)
    ng.links.new(last_socket, out.inputs["Image"])
    return ng
```

### Other 5.x Compositor Socket & Node Renames
- **`CompositorNodeAlphaOver`**: Image inputs are now named `"Background"` and `"Foreground"` (plus `"Factor"`, `"Type"`, `"Straight Alpha"`). Avoid positional `inputs[1]`/`inputs[2]` assumptions without checking names, or look up by `"Background"` / `"Foreground"`.
- **Z Combine → Depth Combine**; procedural noise in the compositor must be fed via texture/render pass or shader AOV (no legacy compositor procedural Noise node).
- **Node settings became input sockets**: `Glare`, `Kuwahara`, and `ColorCorrection` expose parameters as `node.inputs[...]` sockets rather than RNA attributes on `node`. Menu sockets require Title-Case UI strings (`"Bloom"`, `"Fog Glow"`, `"Streaks"`, `"Anisotropic"`, `"Classic"`).

---

## 3. Core RNA, Property & Enum Traps in Blender 5.0 / 5.1

1. **No Dictionary-Style Access to `bpy.props` Storage**:
   - Accessing `bpy.props`-registered properties via `scene["my_addon_prop"]` was removed in 5.0. Use standard attribute access (`scene.my_addon_prop`) and `datablock.property_unset("my_addon_prop")`; reserve `obj["key"]` strictly for user Custom Properties.
2. **Bulk Transform Fast Path**:
   - Use `obj.get_transform()` / `obj.set_transform()` when updating thousands of objects in Python to skip redundant dependency-graph callback overhead.
3. **Private Internal Modules Locked Down**:
   - `bl_rna_utils` and `bl_console_utils` are private in 5.0+; rely strictly on `bpy`, `bmesh`, `mathutils`, `bpy_extras`, and `addon_utils`.
4. **Dynamic Enum Under-Reporting (`enum_items` Trap)**:
   - On `scene.render.engine` and OCIO properties (`scene.view_settings.view_transform`, `scene.display_settings.display_device`), reading `.bl_rna.properties[...].enum_items` returns only `['NONE']` or omits engines.
   - Discover valid identifiers safely by catching `TypeError`:
     ```python
     def valid_enum_values(struct, prop_name: str) -> tuple[str, ...]:
         cur = getattr(struct, prop_name)
         try:
             setattr(struct, prop_name, "__PROBE_INVALID__")
         except TypeError as exc:
             # Parses: enum "__PROBE_INVALID__" not found in ('Standard', 'ACES 1.3', ...)
             msg = str(exc)
             start = msg.find("(")
             if start != -1:
                 import ast
                 return tuple(ast.literal_eval(msg[start:]))
         finally:
             setattr(struct, prop_name, cur)
         return (cur,)
     ```
5. **Localization-Safe Node Lookup**:
   - Node `.name` and `.label` change under non-English UI locales (`"Principled BSDF"` becomes localized). Always find nodes by `.type`:
     ```python
     bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
     out  = next(n for n in mat.node_tree.nodes if n.type == "OUTPUT_MATERIAL")
     ```

---

## 4. Execution Surfaces: Live MCP vs. Headless CLI

| Capability | Live GUI + `MCP for Blender` | Headless `/Applications/Blender.app/Contents/MacOS/Blender -b` |
| :-- | :-- | :-- |
| Interactive viewport screenshots (`look`) | Instant (`viewport`, `camera`, `angles`, `frames`) | Not available; must render to disk (`bpy.ops.render.render(write_still=True)`) |
| Works without GUI window open | No (`blender_mcp` refuses `-b` background mode) | Yes — runs cleanly in CI/background on macOS Metal |
| EEVEE rendering on macOS Apple Silicon | Full GPU support | Full GPU support (blank headless frames were caused by the 5.x `Group Input` compositor bug, not EEVEE) |
| Batch multi-scene / `.glb` generation | Possible but mutates user's open session | **Preferred** — isolated process, deterministic state |
| Telemetry safety | Keep `DISABLE_TELEMETRY=true` & `telemetry_consent = False` | No network activity unless script initiates it |

### Multi-Version Addon Directory Trap on macOS
`~/Library/Application Support/Blender/` may hold both `5.1/` and `5.2/` directories. Tools like `mcp-for-blender install-addon` write only to the highest version folder unless overridden with:
```bash
BLENDERMCP_ADDONS_DIR="$HOME/Library/Application Support/Blender/5.1/scripts/addons" uvx mcp-for-blender install-addon
```

### Safe CLI Extension Installation While GUI Blender Is Open
Never let a background CLI process overwrite `userpref.blend` while GUI Blender is running:
```bash
/Applications/Blender.app/Contents/MacOS/Blender --online-mode --command extension install --no-prefs <pkg_id>
```
Then refresh and enable inside the running GUI session (`bpy.ops.extensions.repo_refresh_all()` → `addon_utils.enable("bl_ext.blender_org.<pkg_id>", default_set=True, persistent=True)` → `bpy.ops.wm.save_userpref()`).
