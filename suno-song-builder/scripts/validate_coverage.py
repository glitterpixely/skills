#!/usr/bin/env python3
"""Validate structural, reference-link, and 83-archetype catalog invariants for suno-song-builder."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import prompt_lint  # noqa: E402


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/studio-signal-chain-and-archetypes.md",
    "references/songcraft.md",
    "references/suno-controls.md",
    "references/controllable-song-research.md",
    "scripts/prompt_lint.py",
    "scripts/validate_coverage.py",
]

CANONICAL_DOCS = [
    "SKILL.md",
    "references/studio-signal-chain-and-archetypes.md",
    "references/songcraft.md",
    "references/suno-controls.md",
    "references/controllable-song-research.md",
]

ROUTED_REFERENCES = [
    "references/studio-signal-chain-and-archetypes.md",
    "references/songcraft.md",
    "references/suno-controls.md",
    "references/controllable-song-research.md",
    "scripts/prompt_lint.py",
    "scripts/validate_coverage.py",
]

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
TODO_MARKER_RE = re.compile(
    r"\[TODO(?:\]|:)|<TODO>|^\s*(?:[-*]\s*)?TODO(?:\s*:|\s*$)",
    re.IGNORECASE | re.MULTILINE,
)
ARCHETYPE_ROW_RE = re.compile(
    r"^\|\s*\*\*(\d{2})\*\*\s*\|\s*\*\*([^*]+)\*\*\s*\(\*([^*]+)\*\)\s*\|\s*`(\d{2,3})\s*BPM`\s*\|\s*`([^`]+)`\s*\|$",
    re.MULTILINE,
)


def frontmatter_keys(text: str) -> list[str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return []
    return [
        line.split(":", 1)[0].strip()
        for line in match.group(1).splitlines()
        if line and not line.startswith((" ", "\t", "-")) and ":" in line
    ]


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            failures.append(f"missing required file: {rel}")

    texts = {
        rel: (ROOT / rel).read_text(encoding="utf-8")
        for rel in CANONICAL_DOCS
        if (ROOT / rel).is_file()
    }

    for rel, text in texts.items():
        if TODO_MARKER_RE.search(text):
            failures.append(f"unresolved TODO marker in {rel}")

    skill_text = texts.get("SKILL.md", "")
    if skill_text:
        line_count = skill_text.count("\n") + 1
        if line_count > 500:
            failures.append(f"SKILL.md has {line_count} lines; limit is 500")
        keys = frontmatter_keys(skill_text)
        if keys != ["name", "description"]:
            failures.append(f"SKILL.md frontmatter keys must be ['name', 'description']; found {keys}")
        if not re.search(r"^name:\s*suno-song-builder\s*$", skill_text, re.MULTILINE):
            failures.append("SKILL.md frontmatter name must be suno-song-builder")
        if "Trigger terms:" not in skill_text.split("\n---\n", 1)[0]:
            failures.append("SKILL.md description is missing 'Trigger terms:'")
        for ref in ROUTED_REFERENCES:
            if f"]({ref})" not in skill_text:
                failures.append(f"SKILL.md is missing link to {ref}")

    root_resolved = ROOT.resolve()
    for rel, text in texts.items():
        source = ROOT / rel
        for destination in MARKDOWN_LINK_RE.findall(text):
            if destination.startswith(("#", "http://", "https://", "mailto:", "sidecar://", "conversation://", "file://")):
                continue
            local_part = destination.split("#", 1)[0].strip()
            if not local_part:
                continue
            target = (source.parent / local_part).resolve()
            try:
                target.relative_to(root_resolved)
            except ValueError:
                failures.append(f"local link escapes skill root in {rel}: {destination}")
                continue
            if not target.exists():
                failures.append(f"broken local link in {rel}: {destination}")

    catalog_text = texts.get("references/studio-signal-chain-and-archetypes.md", "")
    rows = ARCHETYPE_ROW_RE.findall(catalog_text)
    if len(rows) != 83:
        failures.append(f"expected 83 sonic archetypes in studio-signal-chain-and-archetypes.md; found {len(rows)}")

    seen_ids: list[int] = []
    bpms: list[int] = []
    for num_str, name, subtitle, bpm_str, prompt_str in rows:
        idx = int(num_str)
        bpm = int(bpm_str)
        seen_ids.append(idx)
        bpms.append(bpm)
        if f"{bpm}BPM" not in prompt_str:
            failures.append(f"archetype #{num_str} ({name.strip()}) prompt string does not match column BPM ({bpm}BPM)")
        lint_errors = prompt_lint.lint_style(prompt_str, require_bpm=True)
        for err in lint_errors:
            failures.append(f"archetype #{num_str} ({name.strip()}): {err}")

    if seen_ids != list(range(1, 84)):
        missing = sorted(set(range(1, 84)) - set(seen_ids))
        failures.append(f"archetype numbering is not contiguous 01..83; missing={missing}")

    if bpms:
        min_bpm, max_bpm = min(bpms), max(bpms)
        if min_bpm != 68 or max_bpm != 174:
            failures.append(f"expected catalog BPM range 68..174; got {min_bpm}..{max_bpm}")

    songcraft_text = texts.get("references/songcraft.md", "")
    for required_section in (
        "## Opt-in parody and lyric adaptation",
        "## Phonetic and pronunciation hygiene for AI singers",
        "### Mode A: 6-Stage Studio Signal Chain",
        "### Mode B: 8-Part Relational Studio Architecture",
    ):
        if required_section not in songcraft_text:
            failures.append(f"references/songcraft.md is missing section: {required_section}")

    if failures:
        print("coverage validation: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("coverage validation: PASS")
    print(
        f"checked {len(REQUIRED_FILES)} required files, {len(rows)} sonic archetypes "
        f"({min(bpms)}–{max(bpms)} BPM), and all relative links"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
