#!/usr/bin/env python3
"""Validate structural, provenance, and coverage invariants for this skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/model-contract.md",
    "references/runtime-surfaces.md",
    "references/prompt-architecture.md",
    "references/songcraft-and-originality.md",
    "references/examples.md",
    "references/source-coverage.md",
    "references/genre-router.md",
    "scripts/lint_music_prompt.py",
    "scripts/validate_coverage.py",
]
CANONICAL_DOCS = [
    "SKILL.md",
    "references/model-contract.md",
    "references/runtime-surfaces.md",
    "references/prompt-architecture.md",
    "references/songcraft-and-originality.md",
    "references/examples.md",
    "references/source-coverage.md",
    "references/genre-router.md",
]
FAMILY_INDEXES = [
    "index-cinematic-orchestral-epic.md",
    "index-cinematic-pop-ballad.md",
    "index-club-edm-house-trance.md",
    "index-contemporary-folk-acoustic.md",
    "index-country-americana.md",
    "index-dance-pop-disco-funk.md",
    "index-east-asian-ballad-heritage.md",
    "index-east-asian-modern.md",
    "index-electronic-synth-ambient-pop.md",
    "index-general-pop-ballad.md",
    "index-hip-hop-rap.md",
    "index-jazz-swing-big-band.md",
    "index-metal-heavy-rock.md",
    "index-modern-rnb-neo-soul.md",
    "index-pop-alternative-rock.md",
    "index-roots-traditional-global.md",
    "index-soul-blues-gospel.md",
    "index-traditional-vocal-stage.md",
]

CONCEPTS: dict[str, tuple[str, tuple[str, ...]]] = {
    "five-minute creative boundary": (
        "references/model-contract.md",
        (r"up to five minutes", r"implementation ceiling"),
    ),
    "two-input contract": (
        "references/prompt-architecture.md",
        (r"Caption ->", r"Lyrics\s+->"),
    ),
    "three caption sections": (
        "references/prompt-architecture.md",
        (r"Global Metadata", r"Vocal Details", r"Arrangement"),
    ),
    "hosted prompt limit": (
        "references/runtime-surfaces.md",
        (r"2,000 characters",),
    ),
    "hosted lyrics limit": (
        "references/runtime-surfaces.md",
        (r"3,500 characters",),
    ),
    "hosted instrumentals": (
        "references/runtime-surfaces.md",
        (r"is_instrumental: true", r"omit `lyrics`"),
    ),
    "hosted streaming": (
        "references/runtime-surfaces.md",
        (r"streamed output must be hex|streaming supports only.+hex",),
    ),
    "local frame math": (
        "references/runtime-surfaces.md",
        (r"25 frames per second", r"maximum 9,000"),
    ),
    "local nonstreaming": (
        "references/runtime-surfaces.md",
        (r"stream.+must be false",),
    ),
    "local instrumental placeholder": (
        "references/runtime-surfaces.md",
        (r"\[Intro\]", r"\(instrumental\)"),
    ),
    "tag line discipline": (
        "references/prompt-architecture.md",
        (r"tag alone on its line",),
    ),
    "runtime output discrepancy": (
        "references/model-contract.md",
        (r"Diffusers.+44\.1 kHz", r"SGLang.+32 kHz"),
    ),
    "Qwen discrepancy": (
        "references/model-contract.md",
        (r"Qwen3\.5-8B", r"Qwen3-8B"),
    ),
    "community license": (
        "references/model-contract.md",
        (r"MiniMax-Music3 COMMUNITY LICENSE", r"20 million"),
    ),
    "cover boundary": (
        "references/runtime-surfaces.md",
        (r"`music-cover`.+separate|separate.+`music-cover`|`music-cover`.+not an open-weight",),
    ),
    "no language list": (
        "references/model-contract.md",
        (r"Do not invent an official language list",),
    ),
    "official library snapshot": (
        "references/source-coverage.md",
        (r"91410fb657c007ae57c60df8240f5ece5be089c7", r"1,000 complete caption templates"),
    ),
}

ROUTING_LINKS = {
    "references/model-contract.md": r"licensing|deployment guidance",
    "references/runtime-surfaces.md": r"routes 4.9|Serialize",
    "references/prompt-architecture.md": r"prompt-writing|repair",
    "references/songcraft-and-originality.md": r"lyrics|references|scoring picture",
    "references/examples.md": r"payload|formatting pattern",
    "references/source-coverage.md": r"availability|rate limits|installation|licensing",
    "references/genre-router.md": r"official progressive-disclosure",
}

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
TODO_MARKER_RE = re.compile(
    r"\[TODO(?:\]|:)|<TODO>|^\s*(?:[-*]\s*)?TODO(?:\s*:|\s*$)",
    re.IGNORECASE | re.MULTILINE,
)
TEMPLATE_LINK_RE = re.compile(r"`templates/([^`/]+\.txt)`")


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

    for name in FAMILY_INDEXES:
        if not (ROOT / "references" / name).is_file():
            failures.append(f"missing official family index: references/{name}")

    texts = {
        rel: (ROOT / rel).read_text(encoding="utf-8")
        for rel in CANONICAL_DOCS
        if (ROOT / rel).is_file()
    }
    for rel, text in texts.items():
        if TODO_MARKER_RE.search(text):
            failures.append(f"unresolved TODO marker exists in {rel}")

    skill_text = texts.get("SKILL.md", "")
    if skill_text:
        line_count = skill_text.count("\n") + 1
        if line_count > 500:
            failures.append(f"SKILL.md has {line_count} lines; limit is 500")
        keys = frontmatter_keys(skill_text)
        if keys != ["name", "description"]:
            failures.append(f"SKILL.md frontmatter keys must be name, description; found {keys}")
        if not re.search(r"^name:\s*minimax-music-30\s*$", skill_text, re.MULTILINE):
            failures.append("SKILL.md name must be minimax-music-30")
        for rel, cue in ROUTING_LINKS.items():
            linked_lines = [line for line in skill_text.splitlines() if f"]({rel})" in line]
            if not linked_lines:
                failures.append(f"SKILL.md is missing routed link: {rel}")
            elif not any(re.search(cue, line, re.IGNORECASE) for line in linked_lines):
                failures.append(f"SKILL.md link lacks task cue for {rel}")

    agent = ROOT / "agents/openai.yaml"
    if agent.is_file():
        agent_text = agent.read_text(encoding="utf-8")
        for label, pattern in {
            "display name": r'^\s*display_name:\s*"MiniMax Music 3\.0"',
            "short description": r"^\s*short_description:\s*\".{25,64}\"\s*$",
            "default invocation": r"\$minimax-music-30\b",
        }.items():
            if not re.search(pattern, agent_text, re.MULTILINE):
                failures.append(f"agents/openai.yaml is missing valid {label}")

    root_resolved = ROOT.resolve()
    for rel, text in texts.items():
        source = ROOT / rel
        for destination in MARKDOWN_LINK_RE.findall(text):
            if destination.startswith(("#", "http://", "https://", "mailto:")):
                continue
            local_part = destination.split("#", 1)[0]
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

    for label, (rel, patterns) in CONCEPTS.items():
        text = texts.get(rel, "")
        if text and not all(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in patterns):
            failures.append(f"missing sourced concept in {rel}: {label}")

    templates = ROOT / "templates"
    template_files = sorted(templates.glob("*.txt")) if templates.is_dir() else []
    if len(template_files) != 1000:
        failures.append(f"official template count must be 1000; found {len(template_files)}")

    referenced_templates: set[str] = set()
    for name in FAMILY_INDEXES:
        path = ROOT / "references" / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        linked = set(TEMPLATE_LINK_RE.findall(text))
        referenced_templates.update(linked)
        for template in linked:
            if not (templates / template).is_file():
                failures.append(f"broken template link in references/{name}: {template}")
    if len(referenced_templates) != 1000:
        failures.append(
            f"family indexes must reference 1000 unique templates; found {len(referenced_templates)}"
        )
    unindexed = sorted(path.name for path in template_files if path.name not in referenced_templates)
    if unindexed:
        failures.append(f"unindexed templates found: {', '.join(unindexed[:5])}")

    router = texts.get("references/genre-router.md", "")
    for name in FAMILY_INDEXES:
        if f"]({name})" not in router:
            failures.append(f"genre router is missing family link: {name}")

    if failures:
        print("coverage validation: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("coverage validation: PASS")
    print(
        f"checked {len(REQUIRED_FILES)} required files, {len(FAMILY_INDEXES)} family indexes, "
        f"{len(CONCEPTS)} sourced concepts, and {len(template_files)} official templates"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
