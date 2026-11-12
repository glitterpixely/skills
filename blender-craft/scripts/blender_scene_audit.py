#!/usr/bin/env python3
"""
Blender 5.x Production Scene Audit (Gates G1, G2, G3 + Render/Export Preflight).

Usage:
  1. Headless Blender CLI:
     blender -b scene.blend -P <skill>/scripts/blender_scene_audit.py
  2. Inside live MCP `execute_blender_code`:
     import os, runpy
     runpy.run_path(os.path.expanduser("~/.gemini/config/skills/blender-craft/scripts/blender_scene_audit.py"), run_name="__main__")
  3. Standalone stdlib self-test (no Blender required):
     python3 <skill>/scripts/blender_scene_audit.py --self-test
"""

from __future__ import annotations

import json
import os
import sys
from types import SimpleNamespace


DATA_SOCKET_KEYWORDS = (
    "normal",
    "roughness",
    "metallic",
    "specular",
    "displacement",
    "bump",
    "occlusion",
    "orm",
    "arm",
    "ao",
)


def srgb_to_linear(c: float) -> float:
    """Convert an sRGB channel in [0, 1] to scene-linear Rec.709 (IEC 61966-2-1)."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def audit_scene(scene=None, bpy_mod=None, bmesh_mod=None) -> dict:
    if bpy_mod is None:
        import bpy as bpy_mod  # type: ignore
    if bmesh_mod is None:
        try:
            import bmesh as bmesh_mod  # type: ignore
        except ImportError:
            bmesh_mod = None

    scene = scene or bpy_mod.context.scene
    report = {
        "blender_version": getattr(bpy_mod.app, "version_string", "unknown"),
        "filepath": getattr(bpy_mod.data, "filepath", "") or "<unsaved>",
        "scene": scene.name,
        "engine": scene.render.engine,
        "working_space": getattr(getattr(bpy_mod.data, "colorspace", None), "working_space", "unknown"),
        "view_transform": scene.view_settings.view_transform,
        "resolution": f"{scene.render.resolution_x}x{scene.render.resolution_y} ({scene.render.resolution_percentage}%)",
        "unit_scale": scene.unit_settings.scale_length,
        "counts": {
            "meshes": 0,
            "lights": 0,
            "cameras": 0,
            "total_faces": 0,
            "total_verts": 0,
        },
        "warnings": [],
        "errors": [],
    }

    # --- G1: Units, Cameras & Transforms ---
    if abs(scene.unit_settings.scale_length - 1.0) > 1e-4:
        report["warnings"].append(
            f"[G1:Units] unit_settings.scale_length is {scene.unit_settings.scale_length} (expected 1.0m)."
        )

    active_cam = scene.camera
    if active_cam is None:
        report["warnings"].append("[G1:Camera] Scene has no active render camera.")
    elif active_cam.type == "CAMERA":
        cd = active_cam.data
        if cd.clip_start < 0.002:
            report["warnings"].append(
                f"[G1:Camera] '{active_cam.name}' clip_start={cd.clip_start:.5f}m (<0.002m risks Z-fighting)."
            )
        if cd.clip_end <= 1000.0:
            report["warnings"].append(
                f"[G1:Camera] '{active_cam.name}' clip_end={cd.clip_end:.1f}m (default 1000m may clip distant vistas)."
            )

    # --- G1 & G2: Object Transforms & Mesh Topology ---
    for obj in scene.objects:
        if obj.type == "LIGHT":
            report["counts"]["lights"] += 1
        elif obj.type == "CAMERA":
            report["counts"]["cameras"] += 1
        elif obj.type == "MESH" and not obj.hide_render:
            report["counts"]["meshes"] += 1
            sx, sy, sz = obj.scale
            if any(abs(s - 1.0) > 1e-3 for s in (sx, sy, sz)):
                report["warnings"].append(
                    f"[G1:Scale] Mesh '{obj.name}' has unapplied scale ({sx:.3f}, {sy:.3f}, {sz:.3f})."
                )
            if any(s < 0.0 for s in (sx, sy, sz)):
                report["errors"].append(
                    f"[G1:NegScale] Mesh '{obj.name}' has negative scale ({sx:.3f}, {sy:.3f}, {sz:.3f}) -> inverted normals on export!"
                )

            me = obj.data
            n_verts = len(me.vertices)
            n_polys = len(me.polygons)
            report["counts"]["total_verts"] += n_verts
            report["counts"]["total_faces"] += n_polys

            if not me.uv_layers:
                report["warnings"].append(f"[G3:UV] Mesh '{obj.name}' has 0 UV maps.")

            if bmesh_mod is not None and n_polys <= 250_000:
                bm = bmesh_mod.new()
                bm.from_mesh(me)
                loose_v = sum(1 for v in bm.verts if not v.link_edges)
                loose_e = sum(1 for e in bm.edges if not e.link_faces)
                degen_f = sum(1 for f in bm.faces if f.calc_area() < 1e-9)
                non_manifold_e = sum(1 for e in bm.edges if not e.is_manifold and not e.is_boundary)
                bm.free()

                if loose_v or loose_e:
                    report["warnings"].append(
                        f"[G2:Loose] Mesh '{obj.name}' has {loose_v} loose verts and {loose_e} loose edges."
                    )
                if degen_f:
                    report["warnings"].append(
                        f"[G2:Degenerate] Mesh '{obj.name}' has {degen_f} zero-area faces (risks NaN tangents)."
                    )
                if non_manifold_e:
                    report["warnings"].append(
                        f"[G2:NonManifold] Mesh '{obj.name}' has {non_manifold_e} internal non-manifold edges."
                    )

    # --- G3: Materials, Color Spaces & Shader Compatibility ---
    used_mats = {}
    for obj in scene.objects:
        if obj.type == "MESH" and not obj.hide_render:
            for slot in obj.material_slots:
                if slot.material:
                    used_mats[slot.material.name] = slot.material
                else:
                    report["warnings"].append(f"[G3:MatSlot] Mesh '{obj.name}' has an empty material slot.")

    has_shader_to_rgb = False
    for mat in (used_mats[k] for k in sorted(used_mats)):
        if mat.name.startswith("Material.") or mat.name == "Material":
            report["warnings"].append(f"[G3:Naming] Generic material name '{mat.name}'.")
        if not mat.use_nodes or not mat.node_tree:
            continue

        for node in mat.node_tree.nodes:
            if node.type == "SHADER_TO_RGB":
                has_shader_to_rgb = True
                if scene.render.engine == "CYCLES":
                    report["errors"].append(
                        f"[G3:EngineMismatch] Material '{mat.name}' uses ShaderToRGB, which does NOT work in CYCLES!"
                    )
            elif node.type == "TEX_IMAGE":
                img = node.image
                if img is None:
                    report["warnings"].append(
                        f"[G3:EmptyTex] Material '{mat.name}' has an Image Texture node with no image assigned."
                    )
                    continue
                if img.source == "FILE" and img.packed_file is None:
                    abs_p = bpy_mod.path.abspath(img.filepath, library=getattr(img, "library", None))
                    if not os.path.exists(abs_p):
                        report["errors"].append(
                            f"[G3:MissingFile] Image '{img.name}' in '{mat.name}' missing on disk: {abs_p}"
                        )
                cs_name = img.colorspace_settings.name
                if cs_name == "sRGB":
                    for out_sock in node.outputs:
                        for link in out_sock.links:
                            dst_name = (link.to_socket.name or "").lower()
                            dst_node_type = link.to_node.type
                            if dst_node_type in ("NORMAL_MAP", "BUMP", "DISPLACEMENT") or any(
                                kw in dst_name for kw in DATA_SOCKET_KEYWORDS
                            ):
                                report["errors"].append(
                                    f"[G3:ColorSpace] Data map '{img.name}' in '{mat.name}' is set to 'sRGB' instead of 'Non-Color' (linked to {link.to_node.type}.{link.to_socket.name})."
                                )

    if has_shader_to_rgb and scene.view_settings.view_transform != "Standard":
        report["warnings"].append(
            f"[G3:ViewTransform] Scene uses ShaderToRGB cel/anime shading but view_transform is '{scene.view_settings.view_transform}' (consider 'Standard' to prevent AgX desaturation)."
        )

    # --- G3: Blender 5.x Compositor Blank-Frame Trap ---
    comp_ng = getattr(scene, "compositing_node_group", None)
    if scene.use_nodes and comp_ng is not None:
        node_types = {n.type for n in comp_ng.nodes}
        if "GROUP_INPUT" in node_types:
            for n in comp_ng.nodes:
                if n.type == "GROUP_INPUT" and any(out_s.is_linked for out_s in n.outputs):
                    report["errors"].append(
                        f"[G3:Compositor5x] Compositor group '{comp_ng.name}' links from Group Input! In Blender 5.x this short-circuits renders into blank frames; source from CompositorNodeRLayers instead."
                    )
        if "R_LAYERS" not in node_types:
            report["warnings"].append(
                f"[G3:Compositor5x] Compositor group '{comp_ng.name}' has no Render Layers (R_LAYERS) node."
            )
        out_sockets = [
            item.name
            for item in comp_ng.interface.items_tree
            if getattr(item, "item_type", "") == "SOCKET" and getattr(item, "in_out", "") == "OUTPUT"
        ]
        if not out_sockets:
            report["errors"].append(
                f"[G3:Compositor5x] Compositor group '{comp_ng.name}' has 0 OUTPUT sockets on its interface!"
            )

    report["status"] = "FAIL" if report["errors"] else ("WARN" if report["warnings"] else "PASS")
    return report


def _run_self_test() -> int:
    # 1. Verify IEC 61966-2-1 sRGB-to-linear transfer points
    assert abs(srgb_to_linear(0.0) - 0.0) < 1e-9
    assert abs(srgb_to_linear(1.0) - 1.0) < 1e-9
    assert abs(srgb_to_linear(0.5) - 0.21404114) < 1e-6

    mock_bpy = SimpleNamespace(
        app=SimpleNamespace(version_string="5.1.2"),
        data=SimpleNamespace(filepath="test.blend", colorspace=SimpleNamespace(working_space="Linear Rec.709")),
        path=SimpleNamespace(abspath=lambda p, library=None: p),
    )

    # 2. Clean scene -> PASS
    cam_ok = SimpleNamespace(
        name="CAM_Hero",
        type="CAMERA",
        data=SimpleNamespace(clip_start=0.05, clip_end=5000.0),
    )
    mat_ok = SimpleNamespace(
        name="MAT_HeroOak",
        use_nodes=True,
        node_tree=SimpleNamespace(nodes=[]),
    )
    mesh_ok = SimpleNamespace(
        name="GEO_Prop",
        type="MESH",
        hide_render=False,
        scale=(1.0, 1.0, 1.0),
        data=SimpleNamespace(vertices=[0] * 8, polygons=[0] * 6, uv_layers=["UVMap"]),
        material_slots=[SimpleNamespace(material=mat_ok)],
    )
    comp_ok = SimpleNamespace(
        name="Comp_5x",
        nodes=[SimpleNamespace(type="R_LAYERS", outputs=[])],
        interface=SimpleNamespace(
            items_tree=[SimpleNamespace(name="Image", item_type="SOCKET", in_out="OUTPUT")]
        ),
    )
    scene_ok = SimpleNamespace(
        name="Scene",
        render=SimpleNamespace(engine="BLENDER_EEVEE", resolution_x=1920, resolution_y=1080, resolution_percentage=100),
        view_settings=SimpleNamespace(view_transform="AgX"),
        unit_settings=SimpleNamespace(scale_length=1.0),
        camera=cam_ok,
        objects=[cam_ok, mesh_ok],
        use_nodes=True,
        compositing_node_group=comp_ok,
    )
    res_ok = audit_scene(scene=scene_ok, bpy_mod=mock_bpy, bmesh_mod=None)
    assert res_ok["status"] == "PASS", f"Expected PASS on clean fixture, got: {res_ok}"

    # 3. Defective scene -> catches NegScale, sRGB normal map, ShaderToRGB in CYCLES, and 5.x Group Input compositor bug
    bad_norm_link = SimpleNamespace(
        to_socket=SimpleNamespace(name="Color"),
        to_node=SimpleNamespace(type="NORMAL_MAP"),
    )
    bad_tex_node = SimpleNamespace(
        type="TEX_IMAGE",
        image=SimpleNamespace(
            name="T_Wood_N.png",
            source="GENERATED",
            packed_file=True,
            colorspace_settings=SimpleNamespace(name="sRGB"),
        ),
        outputs=[SimpleNamespace(links=[bad_norm_link])],
    )
    s2rgb_node = SimpleNamespace(type="SHADER_TO_RGB")
    mat_bad = SimpleNamespace(
        name="MAT_Bad",
        use_nodes=True,
        node_tree=SimpleNamespace(nodes=[bad_tex_node, s2rgb_node]),
    )
    mesh_bad = SimpleNamespace(
        name="GEO_Flipped",
        type="MESH",
        hide_render=False,
        scale=(-1.0, 1.0, 1.0),
        data=SimpleNamespace(vertices=[0] * 4, polygons=[0] * 1, uv_layers=[]),
        material_slots=[SimpleNamespace(material=mat_bad)],
    )
    comp_bad = SimpleNamespace(
        name="Comp_Broken",
        nodes=[SimpleNamespace(type="GROUP_INPUT", outputs=[SimpleNamespace(is_linked=True)])],
        interface=SimpleNamespace(items_tree=[]),
    )
    scene_bad = SimpleNamespace(
        name="BrokenScene",
        render=SimpleNamespace(engine="CYCLES", resolution_x=1920, resolution_y=1080, resolution_percentage=100),
        view_settings=SimpleNamespace(view_transform="AgX"),
        unit_settings=SimpleNamespace(scale_length=1.0),
        camera=None,
        objects=[mesh_bad],
        use_nodes=True,
        compositing_node_group=comp_bad,
    )
    res_bad = audit_scene(scene=scene_bad, bpy_mod=mock_bpy, bmesh_mod=None)
    assert res_bad["status"] == "FAIL", f"Expected FAIL on defective fixture, got: {res_bad}"
    joined_errors = "\n".join(res_bad["errors"])
    for expected_tag in ("[G1:NegScale]", "[G3:EngineMismatch]", "[G3:ColorSpace]", "[G3:Compositor5x]"):
        assert expected_tag in joined_errors, f"Missing expected error tag {expected_tag} in:\n{joined_errors}"

    print("blender_scene_audit.py self-test: ALL PASS")
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(_run_self_test())
    result = audit_scene()
    print("=== BLENDER 5.x SCENE AUDIT ===")
    print(json.dumps(result, indent=2))
