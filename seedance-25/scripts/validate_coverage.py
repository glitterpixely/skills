#!/usr/bin/env python3
"""Validate structural, frontmatter, byte-cap, anchor, example-lint, and source-coverage invariants."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prompt_lint  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
MAX_DOC_BYTES = 40_000
MAX_DESCRIPTION_CHARS = 380

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
    "references/desk-continuity-and-coverage.md",
    "references/research-mechanics.md",
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
    "references/desk-continuity-and-coverage.md",
    "references/research-mechanics.md",
]

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
    "8n+1 exact edit frame rule": ("references/task-contracts.md", (r"8n\s*\+\s*1",)),
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
    "ModelArk public model ID": ("references/source-boundaries.md", (r"dreamina-seedance-2-5-260628",)),
    "ModelArk explicit task router": ("references/source-boundaries.md", (r"omni_reference_task_type",)),
    "two-step draft_task promotion": ("references/optimizer-runtime.md", (r"draft_task",)),
    "yuvj420p JPEG fix": ("references/source-boundaries.md", (r"yuvj420p",)),
    "normal human eyes troubleshooting": ("references/source-boundaries.md", (r"normal human eyes",)),
    "Seedance 2.5 evidence boundary": ("references/research-mechanics.md", (r"Evidence Boundary",)),
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
    "references/desk-continuity-and-coverage.md": r"vignettes|continuity|phone-camera|reference-plate",
    "references/research-mechanics.md": r"research-grounded|ByteDance Seed|MMDiT|evidence boundary",
}

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
TODO_MARKER_RE = re.compile(
    r"\[TODO(?:\]|:)|<TODO>|^\s*(?:[-*]\s*)?TODO(?:\s*:|\s*$)",
    re.IGNORECASE | re.MULTILINE,
)
FENCED_BLOCK_RE = re.compile(r"^```[^\n]*\n(.*?)^```\s*$", re.MULTILINE | re.DOTALL)


def parse_frontmatter(text: str) -> tuple[list[str], dict[str, str], str | None]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return [], {}, "missing YAML frontmatter fence"
    raw = match.group(1)
    keys: list[str] = []
    values: dict[str, str] = {}
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(raw)
        if not isinstance(loaded, dict):
            return [], {}, "YAML frontmatter did not parse to a mapping"
        keys = [str(k) for k in loaded.keys()]
        values = {str(k): str(v) for k, v in loaded.items()}
        return keys, values, None
    except ImportError:
        pass
    except Exception as exc:
        return [], {}, f"YAML parse error: {exc}"

    for line in raw.splitlines():
        if line and not line.startswith((" ", "\t", "-")) and ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            keys.append(k)
            values[k] = v
    return keys, values, None


def github_slug(heading: str) -> str:
    cleaned = re.sub(r"`([^`]*)`", r"\1", heading.strip().lower())
    cleaned = re.sub(r"[^\w\s-]", "", cleaned, flags=re.UNICODE)
    cleaned = re.sub(r"\s", "-", cleaned)
    return cleaned


def heading_slugs(markdown_text: str) -> set[str]:
    without_fences = FENCED_BLOCK_RE.sub("", markdown_text)
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    for line in without_fences.splitlines():
        m = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if not m:
            continue
        base = github_slug(m.group(1))
        if not base:
            continue
        if base in counts:
            counts[base] += 1
            slugs.add(f"{base}-{counts[base]}")
        else:
            counts[base] = 0
            slugs.add(base)
    return slugs


def extract_fenced_blocks_under_heading(markdown_text: str, heading_pattern: str) -> list[str]:
    m = re.search(heading_pattern, markdown_text, re.IGNORECASE | re.MULTILINE)
    if not m:
        return []
    start = m.end()
    next_h2 = re.search(r"^##\s+", markdown_text[start:], re.MULTILINE)
    section = markdown_text[start : start + next_h2.start()] if next_h2 else markdown_text[start:]
    return [block.strip() for block in FENCED_BLOCK_RE.findall(section) if block.strip()]


def main() -> int:
    failures: list[str] = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            failures.append(f"missing required file: {rel}")

    texts: dict[str, str] = {}
    slug_map: dict[Path, set[str]] = {}
    for rel in CANONICAL_DOCS:
        path = ROOT / rel
        if not path.is_file():
            continue
        byte_size = path.stat().st_size
        if byte_size > MAX_DOC_BYTES:
            failures.append(
                f"{rel} is {byte_size} bytes; single-call read_file safety cap is {MAX_DOC_BYTES} bytes"
            )
        text = path.read_text(encoding="utf-8")
        texts[rel] = text
        slug_map[path.resolve()] = heading_slugs(text)

    for rel, text in texts.items():
        if TODO_MARKER_RE.search(text):
            failures.append(f"unresolved TODO marker exists in {rel}")

    skill = ROOT / "SKILL.md"
    if skill.is_file():
        skill_text = texts["SKILL.md"]
        line_count = skill_text.count("\n") + 1
        if line_count > 500:
            failures.append(f"SKILL.md has {line_count} lines; progressive-disclosure limit is 500")
        keys, fm_values, fm_err = parse_frontmatter(skill_text)
        if fm_err:
            failures.append(f"SKILL.md frontmatter error: {fm_err}")
        elif keys != ["name", "description"]:
            failures.append(f"SKILL.md frontmatter keys must be exactly name, description; found {keys}")
        else:
            desc = fm_values.get("description", "")
            if len(desc) > MAX_DESCRIPTION_CHARS:
                failures.append(
                    f"SKILL.md description is {len(desc)} chars; keep <= {MAX_DESCRIPTION_CHARS} chars so Antigravity does not exclude it under context budget"
                )
            for token in ("Seedance 2.5", "sd25", "sd25-pe", "即梦"):
                if token not in desc:
                    failures.append(f"SKILL.md description is missing trigger token: {token}")

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
                candidates = [line for line in route_lines if f"]({rel}" in line]
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

    # Resolve every local Markdown link AND verify #anchor slugs.
    root_resolved = ROOT.resolve()
    for rel, text in texts.items():
        source = (ROOT / rel).resolve()
        without_fences = FENCED_BLOCK_RE.sub("", text)
        for destination in MARKDOWN_LINK_RE.findall(without_fences):
            if destination.startswith(("http://", "https://", "mailto:")):
                continue
            if "#" in destination:
                local_part, anchor = destination.split("#", 1)
            else:
                local_part, anchor = destination, ""
            target = source if not local_part else (source.parent / local_part).resolve()
            try:
                target.relative_to(root_resolved)
            except ValueError:
                failures.append(f"local link escapes skill root in {rel}: {destination}")
                continue
            if not target.exists():
                failures.append(f"broken local link in {rel}: {destination}")
                continue
            if anchor:
                target_slugs = slug_map.get(target)
                if target_slugs is None and target.suffix == ".md":
                    target_slugs = heading_slugs(target.read_text(encoding="utf-8"))
                    slug_map[target] = target_slugs
                if target_slugs is not None and anchor.lower() not in target_slugs:
                    failures.append(f"broken #anchor in {rel}: {destination}")

    for label, (rel, patterns) in CONCEPTS.items():
        text = texts.get(rel)
        if text is None:
            failures.append(f"concept owner file unreadable or missing for '{label}': {rel}")
            continue
        if not all(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in patterns):
            failures.append(f"missing sourced concept in {rel}: {label}")

    # Lint compiled submit-ready prompt examples so self-violating examples cannot regress.
    linted_blocks = 0
    for rel, heading_pat in (
        ("references/examples.md", r"^## Canonical submit-ready prompt examples\s*$"),
        ("references/desk-prompt-patterns.md", r"^### Reference implementation \(Valkyrie Mecha vs\. Sea Dragon\)\s*$"),
    ):
        doc_text = texts.get(rel, "")
        blocks = extract_fenced_blocks_under_heading(doc_text, heading_pat)
        if not blocks:
            failures.append(f"no canonical prompt blocks found in {rel}")
            continue
        for idx, block in enumerate(blocks, start=1):
            _, issues = prompt_lint.lint(block, "auto")
            linted_blocks += 1
            if issues:
                summary = "; ".join(f"{i.code}" for i in issues)
                failures.append(f"canonical example #{idx} in {rel} failed prompt_lint: {summary}")

    media = ROOT / "references/media-evidence.md"
    if media.is_file():
        media_text = texts["references/media-evidence.md"]
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
        f"checked {len(REQUIRED_FILES)} required files (<={MAX_DOC_BYTES}B docs), "
        f"{len(ROUTING_LINKS)} routing links, #anchors, {len(CONCEPTS)} sourced concepts, "
        f"{linted_blocks} linted example prompts, 51 images, and 22 videos"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
