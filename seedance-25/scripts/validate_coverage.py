#!/usr/bin/env python3
"""Validate structural and source-coverage invariants for the Seedance 2.5 skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/source-boundaries.md",
    "references/prompt-architecture.md",
    "references/task-contracts.md",
    "references/optimizer-runtime.md",
    "references/examples.md",
    "references/media-evidence.md",
    "references/source-coverage.md",
    "references/desk-prompt-patterns.md",
    "scripts/prompt_lint.py",
    "scripts/validate_coverage.py",
]

CANONICAL_DOCS = [
    "SKILL.md",
    "references/source-boundaries.md",
    "references/prompt-architecture.md",
    "references/task-contracts.md",
    "references/optimizer-runtime.md",
    "references/examples.md",
    "references/media-evidence.md",
    "references/source-coverage.md",
    "references/desk-prompt-patterns.md",
]

# Each concept is checked in the document that owns the operational rule. This
# prevents an incidental mention in examples, the coverage ledger, or validator
# source code from masking a missing task contract.
CONCEPTS: dict[str, tuple[str, tuple[str, ...]]] = {
    "30 second generated-video maximum": ("references/source-boundaries.md", (r"one generated video up to 30 seconds",)),
    "combined 50-asset limit": ("references/source-boundaries.md", (r"up to 50 combined.+reference assets",)),
    "30 image limit": ("references/source-boundaries.md", (r"\|\s*Images\s*\|\s*Up to 30",)),
    "10 video limit": ("references/source-boundaries.md", (r"\|\s*Videos\s*\|\s*Up to 10",)),
    "10 audio limit": ("references/source-boundaries.md", (r"\|\s*Audio\s*\|\s*Up to 10",)),
    "30 second video reference total": (
        "references/source-boundaries.md",
        (r"\|\s*Videos\s*\|[^\n]*combined duration at most 30 seconds",),
    ),
    "30 second audio reference total": (
        "references/source-boundaries.md",
        (r"\|\s*Audio\s*\|[^\n]*combined duration at most 30 seconds",),
    ),
    "editing duration minus one": ("references/task-contracts.md", (r"duration=-1",)),
    "adaptive ratio": ("references/task-contracts.md", (r"ratio=adaptive",)),
    "mov continuity": ("references/task-contracts.md", (r"\bmov\b",)),
    "integer timestamps": ("references/prompt-architecture.md", (r"integer-second",)),
    "timestamp limitation": ("references/source-boundaries.md", (r"frame-accurate timestamp adherence",)),
    "0.3 second editing drift": ("references/task-contracts.md", (r"0\.3 seconds",)),
    "0.4 to 2.5 aspect range": ("references/source-boundaries.md", (r"0\.4.+2\.5",)),
    "multi-reference order": (
        "references/prompt-architecture.md",
        (r"Define each material's role.+Map subjects.+Group by type.+Create subject profiles.+Select references by scene",),
    ),
    "unused materials": ("references/prompt-architecture.md", (r"\[Unused Materials\]",)),
    "sole editing master": ("references/task-contracts.md", (r"sole editing master",)),
    "forward extension": ("references/task-contracts.md", (r"extend forward",)),
    "backward extension": ("references/task-contracts.md", (r"extend backward",)),
    "first frame exact syntax": ("references/task-contracts.md", (r"@Image\s+(?:1|N) is the first frame",)),
    "last frame exact syntax": ("references/task-contracts.md", (r"@Image\s+(?:2|N) is the last frame",)),
    "ordered keyframes": ("references/task-contracts.md", (r"in order as keyframes",)),
    "15 storyboard panels": ("references/task-contracts.md", (r"15 or fewer|no more than 15",)),
    "coarse blockout": ("references/task-contracts.md", (r"coarse blockout",)),
    "fine blockout": ("references/task-contracts.md", (r"fine blockout",)),
    "one click": ("references/task-contracts.md", (r"one-click",)),
    "seamless transition": ("references/task-contracts.md", (r"seamless transition",)),
    "audio syntax": (
        "references/prompt-architecture.md",
        (r"\|\s*Dialogue\s*\|\s*`\{\}`", r"\|\s*Sound effects\s*\|\s*`<>`"),
    ),
    "no guarantee boundary": ("references/source-boundaries.md", (r"pixel-identical",)),
    "provider optimizer version": ("references/source-boundaries.md", (r"0\.3\.3",)),
    "source URL Lark": (
        "references/source-boundaries.md",
        (r"https://bytedance\.larkoffice\.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh",),
    ),
    "source URL BytePlus": (
        "references/source-boundaries.md",
        (r"https://docs\.byteplus\.com/en/docs/ModelArk/2607689",),
    ),
}

ROUTING_LINKS = {
    "references/source-boundaries.md": r"factual limits|task locking|ModelArk fields",
    "references/prompt-architecture.md": r"prompt shape|reference binding|timestamps",
    "references/task-contracts.md": r"editing|extension|first/last frames",
    "references/optimizer-runtime.md": r"ambiguous|missing|unreadable|numerous materials",
    "references/examples.md": r"source-derived patterns|examples",
    "references/media-evidence.md": r"visual-output evidence|51 images|22 videos",
    "references/source-coverage.md": r"revising|auditing|validate_coverage",
    "references/desk-prompt-patterns.md": r"Clip-desk craft|physics origin|fight repair|extension-ready",
}

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
TODO_MARKER_RE = re.compile(
    r"\[TODO(?:\]|:)|<TODO>|^\s*(?:[-*]\s*)?TODO(?:\s*:|\s*$)",
    re.IGNORECASE | re.MULTILINE,
)


def frontmatter_keys(text: str) -> list[str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return []
    keys = []
    for line in match.group(1).splitlines():
        if line and not line.startswith((" ", "\t", "-")) and ":" in line:
            keys.append(line.split(":", 1)[0].strip())
    return keys


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

    # Scan authored documentation only, not validator/linter source containing
    # the literal marker regex. Ordinary prose such as "TODO placeholders" is
    # not itself an unresolved marker.
    for rel, text in texts.items():
        if TODO_MARKER_RE.search(text):
            failures.append(f"unresolved TODO marker exists in {rel}")

    skill = ROOT / "SKILL.md"
    if skill.is_file():
        skill_text = skill.read_text(encoding="utf-8")
        line_count = skill_text.count("\n") + 1
        if line_count > 500:
            failures.append(f"SKILL.md has {line_count} lines; progressive-disclosure limit is 500")
        keys = frontmatter_keys(skill_text)
        if keys != ["name", "description"]:
            failures.append(f"SKILL.md frontmatter keys must be exactly name, description; found {keys}")

        route_match = re.search(
            r"^## Load only the needed references\s*$\n(?P<body>.*?)(?=^##\s)",
            skill_text,
            re.IGNORECASE | re.MULTILINE | re.DOTALL,
        )
        if not route_match:
            failures.append("SKILL.md is missing the progressive-disclosure routing section")
        else:
            route_lines = route_match.group("body").splitlines()
            for rel, cue_pattern in ROUTING_LINKS.items():
                candidates = [line for line in route_lines if f"]({rel})" in line]
                if not candidates:
                    failures.append(f"SKILL.md routing section is missing link: {rel}")
                elif not any(re.search(cue_pattern, line, re.IGNORECASE) for line in candidates):
                    failures.append(f"SKILL.md routing link lacks its task cue: {rel}")

    agents = ROOT / "agents/openai.yaml"
    if agents.is_file():
        agents_text = agents.read_text(encoding="utf-8")
        for label, pattern in {
            "display name": r"^\s*display_name:\s*[\"']?Seedance 2\.5",
            "short description": r"^\s*short_description:\s*.+",
            "default skill invocation": r"\$seedance-25\b",
        }.items():
            if not re.search(pattern, agents_text, re.IGNORECASE | re.MULTILINE):
                failures.append(f"agents/openai.yaml is missing {label}")

    # Resolve every local Markdown link in canonical documentation. Anchors and
    # remote URLs are outside this filesystem integrity check.
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
        text = texts.get(rel)
        if text is None:
            continue
        if not all(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in patterns):
            failures.append(f"missing sourced concept in {rel}: {label}")

    media = ROOT / "references/media-evidence.md"
    if media.is_file():
        media_text = media.read_text(encoding="utf-8")
        for number in range(1, 52):
            token = f"image_{number:03d}"
            if token not in media_text:
                failures.append(f"missing visual evidence entry: {token}")
        for number in range(52, 74):
            token = f"video_{number:03d}"
            if token not in media_text:
                failures.append(f"missing video evidence entry: {token}")

    if failures:
        print("coverage validation: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("coverage validation: PASS")
    print(
        f"checked {len(REQUIRED_FILES)} required files, {len(ROUTING_LINKS)} routing links, "
        f"{len(CONCEPTS)} sourced concepts, 51 images, and 22 videos"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
