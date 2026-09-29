#!/usr/bin/env python3
"""Validate structural, provenance, and August 11 coverage invariants."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/base-en.txt",
    "references/community-runtime-extensions.md",
    "references/edge-case-playbook.md",
    "references/media-inspection.md",
    "references/model-contract.md",
    "references/official-hosted-prompt-guide.md",
    "references/proven-dense-motion-design.md",
    "references/ref-en.txt",
    "references/runtime-surfaces.md",
    "references/showcase-patterns.md",
    "scripts/lint_h3_prompt.py",
    "scripts/validate_coverage.py",
]

AUTHORED_DOCS = [
    "SKILL.md",
    "references/community-runtime-extensions.md",
    "references/edge-case-playbook.md",
    "references/media-inspection.md",
    "references/model-contract.md",
    "references/official-hosted-prompt-guide.md",
    "references/proven-dense-motion-design.md",
    "references/runtime-surfaces.md",
    "references/showcase-patterns.md",
]

GRAMMAR_HASHES = {
    "references/base-en.txt": "2cfebc096a6e08370f288d468d90b60f7f9bcb938f94bf090816e910e48e75fc",
    "references/ref-en.txt": "1e574f356716ad55612247ffb7bbccbcdb484ad96599d63c7dca1af186b1fab7",
}

EXPECTED_NEW_TITLES = [
    "Hand-Drawn 2.0",
    "Abstract Technology Brand Film",
    "One Becomes Everyone",
    "Chinese Kinetic Typography",
    "TouchDesigner-Style Visual Overlays",
    "AR World Editing",
    "Comedic AR Interaction",
    "Poster-Space Physical Interaction",
    "Premium Peking Duck Product Launch",
    "Hand-Drawn 2D Game",
    "Virtual Pet UI",
    "Robotic Arm Interaction",
    "Precise Office Background Replacement",
    "Anime-Inspired Graphic Film",
]

AUGUST_11_URL = (
    "https://app.notion.com/p/MiniMax-H3-The-Next-Gen-Open-Weight-"
    "Multimodal-Generation-Model-5cdd99c3d331822397f18130e7b480a8"
)

TODO_MARKER_RE = re.compile(
    r"\[TODO(?:\]|:)|<TODO>|^\s*(?:[-*]\s*)?TODO(?:\s*:|\s*$)",
    re.IGNORECASE | re.MULTILINE,
)
LOCAL_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])((?:references|scripts)/[A-Za-z0-9._/-]+\.(?:md|txt|py))"
)
SHOWCASE_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|(?P<body>.*)$", re.MULTILINE)


def frontmatter_keys(text: str) -> list[str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return []
    return [
        line.split(":", 1)[0].strip()
        for line in match.group(1).splitlines()
        if line and not line.startswith((" ", "\t", "-")) and ":" in line
    ]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_patterns(
    failures: list[str],
    text: str,
    rel: str,
    concepts: dict[str, tuple[str, ...]],
) -> None:
    for label, patterns in concepts.items():
        if not all(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in patterns):
            failures.append(f"missing required concept in {rel}: {label}")


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            failures.append(f"missing required file: {rel}")

    texts = {
        rel: (ROOT / rel).read_text(encoding="utf-8")
        for rel in AUTHORED_DOCS
        if (ROOT / rel).is_file()
    }

    for rel, text in texts.items():
        if TODO_MARKER_RE.search(text):
            failures.append(f"unresolved TODO marker exists in {rel}")
        for referenced_rel in sorted(set(LOCAL_PATH_RE.findall(text))):
            target = (ROOT / referenced_rel).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                failures.append(f"local path escapes skill root in {rel}: {referenced_rel}")
                continue
            if not target.exists():
                failures.append(f"broken local path in {rel}: {referenced_rel}")

    skill_text = texts.get("SKILL.md", "")
    if skill_text:
        line_count = skill_text.count("\n") + 1
        if line_count > 500:
            failures.append(f"SKILL.md has {line_count} lines; limit is 500")
        keys = frontmatter_keys(skill_text)
        if keys != ["name", "description"]:
            failures.append(
                f"SKILL.md frontmatter keys must be exactly name, description; found {keys}"
            )
        if not re.search(r"^name:\s*h3-prompt-writing\s*$", skill_text, re.MULTILINE):
            failures.append("SKILL.md name must be h3-prompt-writing")
        require_patterns(
            failures,
            skill_text,
            "SKILL.md",
            {
                "hosted source boundary": (
                    r"official-hosted-prompt-guide\.md",
                    r"hosted.+@Image N.+@Video N.+@Audio N",
                    r"structured.+native-ComfyUI",
                ),
                "current showcase routing": (
                    r"showcase-patterns\.md",
                    r"all 58 current page demonstrations",
                ),
                "procedural and counted-oner routing": (
                    r"edge-case-playbook\.md",
                    r"cursor-.+tool-.+machine-driven construction",
                    r"exact count.+BPM-synchronized choreography.+one-take camera route",
                ),
            },
        )

    agent_path = ROOT / "agents/openai.yaml"
    if agent_path.is_file():
        agent_text = agent_path.read_text(encoding="utf-8")
        for label, pattern in {
            "display name": r'^\s*display_name:\s*["\']?[^"\n]*H3 Prompt Writing',
            "short description": r"^\s*short_description:\s*.+",
            "default skill invocation": r"\$h3-prompt-writing\b",
        }.items():
            if not re.search(pattern, agent_text, re.IGNORECASE | re.MULTILINE):
                failures.append(f"agents/openai.yaml is missing {label}")

    for rel, expected in GRAMMAR_HASHES.items():
        path = ROOT / rel
        if path.is_file():
            actual = sha256(path)
            if actual != expected:
                failures.append(
                    f"immutable grammar hash changed for {rel}: expected {expected}, found {actual}"
                )

    model_contract = texts.get("references/model-contract.md", "")
    if model_contract:
        require_patterns(
            failures,
            model_contract,
            "references/model-contract.md",
            {
                "dated source": (r"August 11, 2026", re.escape(AUGUST_11_URL)),
                "current showcase counts": (
                    r"58\s+Prompt/Input/Output showcase demonstrations",
                    r"35\s+marked partial",
                    r"14\s+demonstrations",
                    r"net increase of 13",
                ),
                "language source split": (
                    r"repository.+11 languages",
                    r"hosted showcase.+TTS",
                    r"more than 40",
                    r"Arabic",
                    r"Do not collapse them into one guarantee",
                ),
                "pricing drift": (
                    r"Input video\s*\|\s*\$0\.08/second",
                    r"Output video\s*\|\s*\$0\.08/second",
                    r"showcase still listed 768p input video at \$0\.09/second",
                ),
            },
        )

    hosted_guide = texts.get("references/official-hosted-prompt-guide.md", "")
    if hosted_guide:
        require_patterns(
            failures,
            hosted_guide,
            "references/official-hosted-prompt-guide.md",
            {
                "dated source": (r"August 11, 2026", re.escape(AUGUST_11_URL)),
                "three-part formula": (
                    r"Reference Asset Instructions",
                    r"Core Concept",
                    r"Shot-by-Shot Description",
                ),
                "hosted upload handles": (
                    r"@Image N",
                    r"@Video N",
                    r"@Audio N",
                    r"upload order",
                ),
                "topology and music pitfalls": (
                    r"one continuous take",
                    r"Non-diegetic music: N/A",
                    r"Do not simultaneously request a score or BGM",
                ),
                "endpoint behavior": (
                    r"opening or ending frame",
                    r"does not automatically insert a cut",
                ),
            },
        )

    edge_cases = texts.get("references/edge-case-playbook.md", "")
    if edge_cases:
        require_patterns(
            failures,
            edge_cases,
            "references/edge-case-playbook.md",
            {
                "tool-causal procedural creation": (
                    r"Tool-Causal Procedural Creation",
                    r"actuator\s*->\s*visible input\s*->\s*immediate tool-consistent effect\s*->\s*retained state",
                    r"not the opening frame",
                    r"fill, undo, stamp, toggle, delete",
                    r"allowed tool vocabulary",
                    r"formal, disciplined presentation.+intentionally crude output",
                    r"audience-only music is present or absent",
                    r"last-second snap",
                    r"not generation-validated capability evidence",
                ),
                "counted beat-mapped performance": (
                    r"Counted, Beat-Mapped Performance Oners",
                    r"cardinality contract",
                    r"beat_seconds\s*=\s*60\s*/\s*BPM",
                    r"total_beats\s*=\s*duration_seconds\s*\*\s*BPM\s*/\s*60",
                    r"precision displayed in the prompt",
                    r"accelerate, brake, settle, and resume",
                    r"collision-free camera route",
                    r"hide a cut.+inside a strobe",
                    r"not generation-validated capability evidence",
                ),
                "current partial count": (
                    r"Thirty-five source-page demonstrations",
                ),
            },
        )

    linter_path = ROOT / "scripts/lint_h3_prompt.py"
    if linter_path.is_file():
        linter_text = linter_path.read_text(encoding="utf-8")
        require_patterns(
            failures,
            linter_text,
            "scripts/lint_h3_prompt.py",
            {
                "hosted clock ranges": (
                    r"HOSTED_CLOCK_TIMED_HEADER_RE",
                    r"HOSTED_CLOCK_RANGE_RE",
                    r"select_inline_clock_headers",
                    r"hosted_clock_ranges",
                    r"hosted_inline_clock_ranges",
                    r"hosted_colon_clock_ranges",
                    r"hosted_clock_gap",
                    r"hosted_inline_clock_gap",
                    r"hosted_inline_clock_overlap",
                    r"hosted_clock_overrun",
                    r"hosted_source_clock_then_target",
                    r"empty_clock_header",
                    r"empty_first_of_two_clock_headers",
                    r"inline_separator_only_body",
                    r"source_and_target_clock_blocks",
                    r"official_hosted_three_part",
                    r"official_hosted_target_gap",
                    r"explicit_target_overrun",
                    r"explicit_target_far_gap",
                ),
                "tempo-grid checks": (
                    r"tempo-grid",
                    r"tempo-role",
                    r"rhythm-unmapped",
                    r"beat-outside-duration",
                    r"beat-time-mismatch",
                    r"pose-beat-order",
                    r"BEAT_ORIGIN_RE",
                    r"BEAT_ORIGIN_CLOCK_RE",
                    r"beat-origin-value",
                    r"beat_list_outside_window",
                    r"global_beat_mapped_poses",
                    r"invalid_global_pose_beat_order",
                    r"invalid_individual_pose_beat_order",
                    r"partially_beat_mapped_poses",
                    r"clock_form_beat_mapping",
                    r"quoted_bpm_copy",
                    r"invalid_bpm",
                    r"invalid_clock_beat_origin",
                    r"negative_beat_origin",
                ),
                "pose-count checks": (
                    r"POSE_COUNT_RE",
                    r"pose-count-unmapped",
                    r"pose-count",
                    r"missing_counted_pose",
                    r"word_counted_poses",
                    r"source_and_target_pose_counts",
                    r"source_pose_labels_and_target_count",
                    r"official_hosted_target_poses",
                    r"rate_based_pose_wording",
                ),
            },
        )

    showcase = texts.get("references/showcase-patterns.md", "")
    rows = list(SHOWCASE_ROW_RE.finditer(showcase)) if showcase else []
    row_numbers = [int(match.group(1)) for match in rows]
    row_texts = [match.group(0) for match in rows]
    if showcase:
        if len(rows) != 58:
            failures.append(f"showcase must contain 58 numeric demo rows; found {len(rows)}")
        expected_ids = set(range(1, 60)) - {20}
        if len(row_numbers) != len(set(row_numbers)) or set(row_numbers) != expected_ids:
            failures.append(
                "showcase must preserve unique source IDs 1-59 except removed ID 20; found "
                + ",".join(str(number) for number in sorted(set(row_numbers)))
            )
        partial_count = sum(bool(re.search(r"\bPartial\b", row)) for row in row_texts)
        if partial_count != 35:
            failures.append(f"showcase must contain 35 Partial demo rows; found {partial_count}")
        if any("Rotating Product Page Reveal" in row for row in row_texts):
            failures.append("removed showcase row is still present: Rotating Product Page Reveal")
        for title in EXPECTED_NEW_TITLES:
            if not any(title in row for row in row_texts):
                failures.append(f"missing August 11 showcase row: {title}")
        if not re.search(r"August 11, 2026", showcase):
            failures.append("showcase-patterns.md is not dated August 11, 2026")

    if failures:
        print("coverage validation: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("coverage validation: PASS")
    print(
        f"checked {len(REQUIRED_FILES)} required files, {len(GRAMMAR_HASHES)} immutable grammar "
        f"hashes, {len(rows)} showcase rows, 35 Partial rows, and "
        f"{len(EXPECTED_NEW_TITLES)} August 11 additions"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
