#!/usr/bin/env python3
"""Validate structural, reference-routing, mathematical, and static-probe invariants for threejs-rendering."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REFERENCE_FILES = [
    "references/00-version-gates.md",
    "references/01-color-tonemapping-units.md",
    "references/02-ibl-lighting-gi.md",
    "references/03-shadows.md",
    "references/04-materials.md",
    "references/05-post-processing.md",
    "references/06-geometry-assets.md",
    "references/07-diagnostics-photoreal.md",
    "references/08-stylized-looks.md",
    "references/09-rulebook.md",
    "references/10-evidence-r187.md",
    "references/11-quality-loop.md",
    "references/12-animation-interaction.md",
    "references/13-performance-batching-compute.md",
    "references/14-shaders-tsl.md",
    "references/15-react-three-fiber.md",
]

REQUIRED_FILES = [
    "SKILL.md",
    *REFERENCE_FILES,
    "scripts/check-three-api.mjs",
    "scripts/fit-shadow.mjs",
    "scripts/fit-shadow.test.mjs",
    "scripts/physical.mjs",
    "scripts/validate_coverage.py",
    "scripts/quality/ceiling.example.json",
    "scripts/quality/gate-harness.html",
    "scripts/quality/gates.js",
    "scripts/quality/probe.mjs",
    "scripts/quality/run-gates.mjs",
    "scripts/render-check/harness.html",
    "scripts/render-check/shoot.mjs",
]

CANONICAL_DOCS = ["SKILL.md", *REFERENCE_FILES]

CONCEPTS: dict[str, tuple[str, tuple[str, ...]]] = {
    "r187 baseline version gate": ("references/00-version-gates.md", (r"0\.187\.0", r"RenderPipeline")),
    "measured AgX vs ACES vs Neutral transfer": (
        "references/01-color-tonemapping-units.md",
        (r"0\.2131", r"0\.2145", r"-0\.012 EV", r"\+0\.492 EV"),
    ),
    "sunDirectionFromEquirect azimuth sign & flipY": (
        "references/02-ibl-lighting-gi.md",
        (r"sunDirectionFromEquirect", r"-\s*envRotationY", r"flipY"),
    ),
    "fitDirectionalShadow helper": ("references/03-shadows.md", (r"fitDirectionalShadow", r"PCFShadowMap")),
    "EON rough diffuse BRDF citation": (
        "references/04-materials.md",
        (r"BRDF_EON", r"arXiv:2410\.18026", r"Portsmouth"),
    ),
    "Kaplanyan normal-variance specular AA": (
        "references/04-materials.md",
        (r"normalVarianceRoughness", r"Kaplanyan", r"getGeometryRoughness"),
    ),
    "SSRNode options object and worldDistance alpha": (
        "references/05-post-processing.md",
        (r"worldDistance", r"RecurrentDenoiseNode", r"metalnessNode"),
    ),
    "glTF-Transform CLI and KTX2": ("references/06-geometry-assets.md", (r"gltf-transform", r"KTX2Loader")),
    "photoreal symptom diagnostics": ("references/07-diagnostics-photoreal.md", (r"Symptom", r"normalBias")),
    "TSL Kuwahara and halftone passes": (
        "references/08-stylized-looks.md",
        (r"kuwaharaFilter", r"halftonePass", r"toFloat\(\)"),
    ),
    "consolidated r187 rulebook": ("references/09-rulebook.md", (r"PCFSoftShadowMap", r"RGBELoader")),
    "r187 GPU evidence ledger": ("references/10-evidence-r187.md", (r"2026-11-05 GPU & mathematical verification pass",)),
    "G0-G3 quality gates": ("references/11-quality-loop.md", (r"run-gates\.mjs", r"probe\.mjs")),
    "animation mixer, SkeletonUtils, raycasting, controls": (
        "references/12-animation-interaction.md",
        (r"AnimationMixer", r"SkeletonUtils\.clone", r"castShadowPositionNode", r"getHelper\(\)"),
    ),
    "BatchedMesh and WebGPU compute": (
        "references/13-performance-batching-compute.md",
        (r"BatchedMesh", r"addGeometry", r"addInstance", r"instancedArray", r"\.element\(\s*(?:i|0)\s*\)\.get"),
    ),
    "TSL shader translation and node hooks": (
        "references/14-shaders-tsl.md",
        (r"uniformArray", r"viewportUV", r"normalView", r"opaque_fragment"),
    ),
    "React Three Fiber 9.8 and WebGPU Canvas": (
        "references/15-react-three-fiber.md",
        (r'shadows="percentage"', r"WebGPURenderer", r"state\.clock\.elapsedTime"),
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


def check_physical_selftest(errors: list[str]) -> None:
    proc = subprocess.run(
        ["node", str(ROOT / "scripts" / "physical.mjs")],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or "ALL PASS" not in proc.stdout:
        errors.append(
            f"physical.mjs self-test failed (exit {proc.returncode}):\n{proc.stdout}\n{proc.stderr}"
        )


def check_probe_fixtures(errors: list[str]) -> None:
    probe_script = ROOT / "scripts" / "quality" / "probe.mjs"
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        bad_dir = tmp / "bad"
        clean_dir = tmp / "clean"
        bad_dir.mkdir()
        clean_dir.mkdir()

        (bad_dir / "package.json").write_text(
            json.dumps({"dependencies": {"three": "^0.187.0"}}), encoding="utf-8"
        )
        (bad_dir / "bad.tsx").write_text(
            "\n".join(
                [
                    "import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';",
                    "import { positionGeometry } from 'three/nodes';",
                    "mat.positionNode = positionGeometry;",
                    "scene.add(transformControls);",
                    "const o = pointerLock.getObject();",
                    "#include <output_fragment>",
                    "<Canvas shadows>",
                    "state.clock.getElapsedTime();",
                ]
            ),
            encoding="utf-8",
        )

        (clean_dir / "package.json").write_text(
            json.dumps({"dependencies": {"three": "0.187.0"}}), encoding="utf-8"
        )
        (clean_dir / "clean.tsx").write_text(
            "\n".join(
                [
                    "import * as THREE from 'three/webgpu';",
                    "import { positionLocal } from 'three/tsl';",
                    "import { OrbitControls } from 'three/addons/controls/OrbitControls.js';",
                    "const renderer = new THREE.WebGPURenderer({ forceWebGL: false });",
                    "const pipeline = new THREE.RenderPipeline(renderer);",
                    "const timer = new THREE.Timer();",
                    "scene.add(transformControls.getHelper());",
                    "<Canvas shadows=\"percentage\" />",
                ]
            ),
            encoding="utf-8",
        )

        bad_proc = subprocess.run(
            ["node", str(probe_script), "--root", str(bad_dir)],
            capture_output=True,
            text=True,
            check=False,
        )
        if bad_proc.returncode == 0:
            errors.append("probe.mjs unexpectedly exited 0 on synthetic bad fixture")
        for expected in (
            "three/examples/jsm/",
            "three/nodes",
            "positionGeometry",
            "TransformControls is not an Object3D",
            "getObject()",
            "output_fragment",
            'shadows="percentage"',
            "state.clock.elapsedTime",
        ):
            if expected not in bad_proc.stdout:
                errors.append(f"probe.mjs missed expected diagnostic on bad fixture: {expected}")

        clean_proc = subprocess.run(
            ["node", str(probe_script), "--root", str(clean_dir)],
            capture_output=True,
            text=True,
            check=False,
        )
        if clean_proc.returncode != 0 or "no migration hits" not in clean_proc.stdout:
            errors.append(
                f"probe.mjs failed on synthetic clean fixture (exit {clean_proc.returncode}):\n{clean_proc.stdout}"
            )


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"Missing required file: {rel}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    keys = frontmatter_keys(skill_text)
    if keys != ["name", "description"]:
        errors.append(f"SKILL.md frontmatter keys must be ['name', 'description'], got {keys}")

    skill_lines = len(skill_text.splitlines())
    if skill_lines > 500:
        errors.append(f"SKILL.md has {skill_lines} lines; keep it under 500 lines")

    for ref_rel in REFERENCE_FILES:
        if f"({ref_rel})" not in skill_text:
            errors.append(f"SKILL.md is missing a routing link to {ref_rel}")

    for rel in CANONICAL_DOCS:
        doc_path = ROOT / rel
        text = doc_path.read_text(encoding="utf-8")
        # Strip fenced code blocks before scanning Markdown links
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

    check_physical_selftest(errors)
    check_probe_fixtures(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"OK: {len(REQUIRED_FILES)} files present; {len(CONCEPTS)} concept groups verified; "
        f"physical.mjs and probe.mjs self-tests passed; SKILL.md is {skill_lines} lines."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
