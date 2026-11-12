#!/usr/bin/env python3
"""Validate structural, reference-routing, privacy, and audit self-test invariants for blender-craft."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REFERENCE_FILES = [
    "references/00-blender5-api-and-gotchas.md",
    "references/01-scene-scale-color-and-lighting.md",
    "references/02-modeling-topology-and-hero-props.md",
    "references/03-geometry-nodes-scatter-and-environments.md",
    "references/04-materials-pbr-stylized-and-anime.md",
    "references/05-uvs-baking-and-glb-export.md",
    "references/06-cameras-previz-and-ai-video-plates.md",
    "references/07-animation-rigging-and-compositing.md",
    "references/08-performance-hygiene-and-addons.md",
    "references/09-verification-gates-and-diagnostics.md",
]

REQUIRED_FILES = [
    "SKILL.md",
    *REFERENCE_FILES,
    "scripts/blender_scene_audit.py",
    "scripts/validate_coverage.py",
]

CANONICAL_DOCS = ["SKILL.md", *REFERENCE_FILES]

CONCEPTS: dict[str, tuple[str, tuple[str, ...]]] = {
    "Blender 5.x Slotted Actions & Node-Group Compositor": (
        "references/00-blender5-api-and-gotchas.md",
        (
            r"fcurve_ensure_for_datablock",
            r"compositing_node_group",
            r"CompositorNodeRLayers",
            r"new_socket",
            r"Anisotropic",
        ),
    ),
    "Blender 5.0+ working color spaces, view transforms & IEC sRGB math": (
        "references/01-scene-scale-color-and-lighting.md",
        (
            r"Linear Rec\.709",
            r"Linear Rec\.2020",
            r"ACEScg",
            r"Khronos PBR Neutral",
            r"12\.92",
            r"0\.04045",
        ),
    ),
    "Non-destructive modifier ordering, Shrinkwrap spiral curves & bmesh hygiene": (
        "references/02-modeling-topology-and-hero-props.md",
        (
            r"Weighted Normal",
            r"Shrinkwrap",
            r"extra_curve_objectes",
            r"recalc_face_normals",
        ),
    ),
    "Geometry Nodes 5.x Bundles, Closures, SDF Grids, Scene Time FX & Poisson scatter": (
        "references/03-geometry-nodes-scatter-and-environments.md",
        (
            r"GeometryNodeMeshToSDFGrid",
            r"GeometryNodeSDFGridFillet",
            r"GeometryNodeBoneInfo",
            r"Scene Time",
            r"Poisson Disk",
            r"Realize Instances",
        ),
    ),
    "PBR roughness breakup, 5.1 ShaderNodeRaycast, EEVEE ShaderToRGB anime & Ucupaint": (
        "references/04-materials-pbr-stylized-and-anime.md",
        (
            r"ShaderNodeRaycast",
            r"ShaderNodeShaderToRGB",
            r"View Distance",
            r"CompositorNodeKuwahara",
            r"ucupaint",
        ),
    ),
    "UniV quadrify, Non-Color PBR baking & glTF +Z to +Y GPU instancing bridge": (
        "references/05-uvs-baking-and-glb-export.md",
        (
            r"Non-Color",
            r"export_yup=True",
            r"export_gpu_instances",
            r"EXT_mesh_gpu_instancing",
        ),
    ),
    "Architectural two-point shift_y, multi-angle graybox & 3-in-1 16:9 turnarounds": (
        "references/06-cameras-previz-and-ai-video-plates.md",
        (
            r"shift_y",
            r"BLENDER_WORKBENCH",
            r"180°",
            r"turnaround_camera",
        ),
    ),
    "Multi-slot Actions, Child Of handoffs & MultiLayer EXR Cryptomatte": (
        "references/07-animation-rigging-and-compositing.md",
        (
            r"Child Of",
            r"GeometryNodeBoneInfo",
            r"OpenEXR",
            r"Cryptomatte",
        ),
    ),
    "Apple Silicon MetalRT optimization, Outliner naming & addon stack": (
        "references/08-performance-hygiene-and-addons.md",
        (
            r"METAL",
            r"orphans_purge",
            r"Bagapie",
            r"Geo-Scatter",
            r"Botaniq",
        ),
    ),
    "Gates G1-G5 & diagnostic symptom table": (
        "references/09-verification-gates-and-diagnostics.md",
        (
            r"Gate `G1`",
            r"Gate `G4`",
            r"Gate `G5`",
            r"Symptom",
        ),
    ),
}

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def frontmatter_keys(text: str) -> list[str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return []
    keys = []
    for line in match.group(1).splitlines():
        if line and not line.startswith((" ", "\t", "-")) and ":" in line:
            keys.append(line.split(":", 1)[0].strip())
    return keys


def frontmatter_description(text: str) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return ""
    lines = match.group(1).splitlines()
    desc_lines: list[str] = []
    in_desc = False
    for line in lines:
        if line.startswith("description:"):
            in_desc = True
            rest = line.split(":", 1)[1].strip()
            if rest not in ("", ">", ">-", "|", "|-"):
                desc_lines.append(rest.strip("'\""))
        elif in_desc:
            if line.startswith((" ", "\t")):
                desc_lines.append(line.strip())
            else:
                break
    return " ".join(desc_lines).strip()


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    keys = frontmatter_keys(skill_text)
    if keys != ["name", "description"]:
        errors.append(f"SKILL.md frontmatter keys must be ['name', 'description'], got {keys}")

    desc = frontmatter_description(skill_text)
    if not desc or len(desc) > 480:
        errors.append(
            f"SKILL.md description length is {len(desc)} chars; keep between 1 and 480 chars to fit Antigravity context budget"
        )
    if "Trigger terms:" not in desc:
        errors.append("SKILL.md description must include 'Trigger terms:' for skill routing")

    skill_lines = len(skill_text.splitlines())
    if skill_lines > 500:
        errors.append(f"SKILL.md has {skill_lines} lines; keep it under 500 lines")

    for ref_rel in REFERENCE_FILES:
        if f"({ref_rel})" not in skill_text:
            errors.append(f"SKILL.md is missing a routing link to {ref_rel}")

    for rel in REQUIRED_FILES:
        if rel == "scripts/validate_coverage.py":
            continue
        file_text = (ROOT / rel).read_text(encoding="utf-8")
        if "/Users/" in file_text:
            errors.append(f"{rel} contains a machine-specific '/Users/' path")

    for rel in CANONICAL_DOCS:
        doc_path = ROOT / rel
        text = doc_path.read_text(encoding="utf-8")
        prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for match in MARKDOWN_LINK_RE.finditer(prose):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            resolved = (doc_path.parent / target_path).resolve()
            if not resolved.exists():
                errors.append(f"{rel} has broken relative link: {target}")

    for label, (owner_rel, patterns) in CONCEPTS.items():
        text = (ROOT / owner_rel).read_text(encoding="utf-8")
        for pat in patterns:
            if not re.search(pat, text, re.IGNORECASE | re.DOTALL):
                errors.append(f"Missing concept '{label}' ({pat}) in {owner_rel}")

    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "blender_scene_audit.py"), "--self-test"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or "ALL PASS" not in proc.stdout:
        errors.append(
            f"blender_scene_audit.py --self-test failed (exit {proc.returncode}):\n{proc.stdout}\n{proc.stderr}"
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"OK: {len(REQUIRED_FILES)} files present; {len(CONCEPTS)} concept groups verified; "
        f"description is {len(desc)} chars; SKILL.md is {skill_lines} lines; "
        f"blender_scene_audit.py --self-test passed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
