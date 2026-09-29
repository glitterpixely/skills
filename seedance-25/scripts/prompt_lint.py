#!/usr/bin/env python3
"""Lint a submit-ready Seedance 2.5 prompt against the sourced contracts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Issue:
    severity: str
    code: str
    message: str


@dataclass(frozen=True)
class ReferenceMention:
    kind: str
    number: int | None
    raw: str

    @property
    def effective_number(self) -> int:
        """Treat an unnumbered @Video or @Audio token as the singleton item 1."""

        return 1 if self.number is None else self.number


ROLE_WORDS = re.compile(
    r"\b(defines?|corresponds?|references?|provides?|controls?|inherits?|"
    r"source video|sole editing master|first frame|last frame|keyframe|"
    r"before[- ]transition clip|after[- ]transition clip|transition source|"
    r"transition target|used (?:only )?for|is used|do not use|not used)\b",
    re.IGNORECASE,
)

HANDLE_RE = re.compile(
    r"(?<![\w@])(?:"
    r"@(?P<at_kind>Image|Video|Audio)(?:[ \t]*(?P<at_number>\d+))?"
    r"|\[(?P<bracket_kind>Image|Video|Audio)[ \t]*(?P<bracket_number>\d+)\]"
    r"|<(?P<angle_kind>Image|Video|Audio)[ \t]*(?P<angle_number>\d+)>"
    r")(?!\w)",
    re.IGNORECASE,
)
VIDEO_HANDLE_PATTERN = r"(?:@Video(?:[ \t]*\d+)?|\[Video[ \t]*\d+\]|<Video[ \t]*\d+>)"
IMAGE_HANDLE_PATTERN = r"(?:@Image[ \t]*\d+|\[Image[ \t]*\d+\]|<Image[ \t]*\d+>)"
RANGE_RE = re.compile(
    r"(?P<start>\d+(?:\.\d+)?)\s*(?:sec(?:ond)?s?|s)?\s*[-–—]\s*"
    r"(?P<end>\d+(?:\.\d+)?)\s*(?:sec(?:ond)?s?|s)",
    re.IGNORECASE,
)
TIME_POINT_RE = re.compile(r"\bat\s+(\d+(?:\.\d+)?)\s*(?:s|sec(?:ond)?s?)\b", re.IGNORECASE)
TODO_MARKER_RE = re.compile(r"\bTODO\b", re.IGNORECASE)
TEMPLATE_PLACEHOLDER_RE = re.compile(
    r"<(?:subject|scene|action|event|placeholder|specified|primary|name|N)"
    r"(?:\s+[^<>]+)?>",
    re.IGNORECASE,
)


def add(issues: list[Issue], severity: str, code: str, message: str) -> None:
    issues.append(Issue(severity, code, message))


def infer_mode(text: str) -> str:
    if re.search(
        rf"\bextend(?:s|ed|ing)?\s+(?:{VIDEO_HANDLE_PATTERN}|forward|backward)"
        rf"|\bcontinue\s+from\s+{VIDEO_HANDLE_PATTERN}",
        text,
        re.IGNORECASE,
    ):
        return "extension"
    if re.search(rf"\bedit\s+{VIDEO_HANDLE_PATTERN}|\bsole editing master\b", text, re.IGNORECASE):
        return "edit"
    return "generation"


def reference_mentions(text: str) -> list[ReferenceMention]:
    mentions: list[ReferenceMention] = []
    for match in HANDLE_RE.finditer(text):
        kind = match.group("at_kind") or match.group("bracket_kind") or match.group("angle_kind")
        number_text = match.group("at_number") or match.group("bracket_number") or match.group("angle_number")
        if kind is None:
            continue
        # Dreamina surfaces may expose singleton @Video and @Audio tokens. A
        # bare @Image is not a documented identity-safe handle, so ignore it.
        if number_text is None and kind.lower() == "image":
            continue
        mentions.append(ReferenceMention(kind.lower(), int(number_text) if number_text else None, match.group(0)))
    return mentions


def referenced_handles(text: str) -> dict[str, set[int]]:
    found = {"image": set(), "video": set(), "audio": set()}
    for mention in reference_mentions(text):
        found[mention.kind].add(mention.effective_number)
    return found


def check_counts(
    issues: list[Issue],
    handles: dict[str, set[int]],
    images: int | None,
    videos: int | None,
    audio: int | None,
    video_seconds: float | None,
    audio_seconds: float | None,
) -> None:
    counts = {"image": images, "video": videos, "audio": audio}
    hard = {"image": 30, "video": 10, "audio": 10}
    for kind, count in counts.items():
        if count is not None and count > hard[kind]:
            add(issues, "error", f"{kind.upper()}_LIMIT", f"{count} {kind}s exceeds the hard limit of {hard[kind]}.")
        if count is not None and handles[kind] and max(handles[kind]) > count:
            add(
                issues,
                "error",
                f"MISSING_{kind.upper()}_HANDLE",
                f"Prompt references @{kind.title()} {max(handles[kind])}, but only {count} {kind}(s) were declared available.",
            )

    known_counts = [x for x in (images, videos, audio) if x is not None]
    if len(known_counts) == 3 and sum(known_counts) > 50:
        add(issues, "error", "TOTAL_MATERIAL_LIMIT", f"{sum(known_counts)} total assets exceeds the hard limit of 50.")
    if video_seconds is not None and video_seconds > 30:
        add(issues, "error", "VIDEO_DURATION_LIMIT", f"Reference videos total {video_seconds:g}s; the hard combined limit is 30s.")
    if audio_seconds is not None and audio_seconds > 30:
        add(issues, "error", "AUDIO_DURATION_LIMIT", f"Reference audio totals {audio_seconds:g}s; the hard combined limit is 30s.")

    for kind, count in counts.items():
        if count is None:
            continue
        absent = [n for n in range(1, count + 1) if n not in handles[kind]]
        if absent:
            numbers = ", ".join(str(n) for n in absent)
            add(
                issues,
                "warning",
                "UNACCOUNTED_MATERIAL",
                f"Known {kind} number(s) {numbers} are not mentioned. List inactive items under [Unused Materials].",
            )


def check_roles(issues: list[Issue], text: str, handles: dict[str, set[int]]) -> None:
    bound: set[tuple[str, int]] = set()
    for line in text.splitlines():
        if not ROLE_WORDS.search(line):
            continue
        for mention in reference_mentions(line):
            bound.add((mention.kind, mention.effective_number))

    for kind, numbers in handles.items():
        for number in sorted(numbers):
            if (kind, number) not in bound:
                add(
                    issues,
                    "warning",
                    "UNBOUND_REFERENCE",
                    f"{kind.title()} reference {number} appears without an explicit role or exclusion on the same line.",
                )


def timeline_ranges(text: str) -> list[tuple[float, float]]:
    """Extract documented timeline forms without treating every numeric range as time.

    BytePlus supports both labeled blocks (`0-3s: ...`) and compact inline
    sequences (`0-3 seconds...3-7 seconds...` or `[1s-4s]....`). A lone
    prose range such as "a 5-10 seconds reference clip" is not an event
    timeline and must not participate in gap/overlap checks.
    """

    candidates = list(RANGE_RE.finditer(text))
    accepted: list[tuple[float, float]] = []
    for match in candidates:
        line_prefix = text[text.rfind("\n", 0, match.start()) + 1 : match.start()]
        suffix = text[match.end() : match.end() + 12]
        bracketed = line_prefix.rstrip().endswith("[") and re.match(r"\s*\]", suffix) is not None
        starts_line = re.fullmatch(r"\s*(?:[-*]\s*)?(?:[*_\"'“‘]\s*)?", line_prefix) is not None
        timeline_punctuation = re.match(r"\s*(?:\]|:|—|–|\.{2,})", suffix) is not None
        preceded_by_inline_separator = re.search(r"(?:\.{2,}|\])\s*(?:\[\s*)?$", line_prefix) is not None
        if bracketed or starts_line or timeline_punctuation or preceded_by_inline_separator:
            accepted.append((float(match.group("start")), float(match.group("end"))))
    return accepted


def check_timeline(issues: list[Issue], text: str) -> None:
    ranges = timeline_ranges(text)
    for start, end in ranges:
        if end <= start:
            add(issues, "error", "INVALID_TIME_RANGE", f"Timeline range {start:g}-{end:g}s does not move forward.")
        if not start.is_integer() or not end.is_integer():
            add(issues, "warning", "DECIMAL_TIMESTAMP", f"Use integer-second guidance instead of {start:g}-{end:g}s.")
    for (_, previous_end), (next_start, _) in zip(ranges, ranges[1:]):
        if next_start > previous_end:
            add(issues, "warning", "TIMELINE_GAP", f"Timeline gap between {previous_end:g}s and {next_start:g}s.")
        elif next_start < previous_end:
            add(issues, "error", "TIMELINE_OVERLAP", f"Timeline overlap at {next_start:g}s before the previous range ends at {previous_end:g}s.")
    for value in TIME_POINT_RE.findall(text):
        if not float(value).is_integer():
            add(issues, "warning", "DECIMAL_TIME_POINT", f"Use an integer-second key point instead of {value}s.")
    if re.search(r"\b(?:three|four|five|\d+)\s+(?:times|actions?)\s+per\s+second\b", text, re.IGNORECASE):
        add(issues, "warning", "HIGH_FREQUENCY_ACTION", "Do not use timestamps to demand high-frequency repeated actions.")


def check_anchor_syntax(issues: list[Issue], text: str, anchor_mode: str) -> None:
    """Enforce standalone anchor declarations only for the strict role route."""

    if anchor_mode != "strict":
        return

    exact_line = re.compile(
        rf"^\s*(?P<handle>{IMAGE_HANDLE_PATTERN})\s+is\s+the\s+"
        r"(?P<role>first|last)\s+frame\.\s*$",
        re.IGNORECASE,
    )
    required: set[tuple[str, int]] = set()
    satisfied: set[tuple[str, int]] = set()
    for line in text.splitlines():
        paired_pattern = re.compile(
            rf"(?P<handle>{IMAGE_HANDLE_PATTERN})[^\n]{{0,80}}?\b(?P<role>first|last)\s+frame\b",
            re.IGNORECASE,
        )
        pairs = list(paired_pattern.finditer(line))
        for match in pairs:
            mention = reference_mentions(match.group("handle"))[0]
            required.add((match.group("role").lower(), mention.effective_number))
        if not pairs:
            # Also accept the uncommon reverse wording "the first frame uses
            # [Image 1]" when there is only one unambiguous role and image.
            images = [mention for mention in reference_mentions(line) if mention.kind == "image"]
            roles = [role for role in ("first", "last") if f"{role} frame" in line.lower()]
            if len(images) == 1 and len(roles) == 1:
                required.add((roles[0], images[0].effective_number))
        exact = exact_line.match(line)
        if exact:
            mention = reference_mentions(exact.group("handle"))[0]
            satisfied.add((exact.group("role").lower(), mention.effective_number))

    for role, number in sorted(required - satisfied):
        code = "WEAK_FIRST_FRAME_ROLE" if role == "first" else "WEAK_LAST_FRAME_ROLE"
        add(
            issues,
            "warning",
            code,
            f"Strict anchoring requires a standalone declaration such as '@Image {number} is the {role} frame.'",
        )


def check_target_duration(issues: list[Issue], target_duration: float | None) -> None:
    if target_duration is None:
        return
    if target_duration <= 0:
        add(issues, "error", "TARGET_DURATION_VALUE", "Target duration must be greater than zero seconds.")
    elif target_duration > 30:
        add(
            issues,
            "error",
            "TARGET_DURATION_LIMIT",
            f"Target duration {target_duration:g}s exceeds the documented 30s single-video maximum; segment the story into multiple generated clips.",
        )
        add(
            issues,
            "warning",
            "TARGET_DURATION_SEGMENTATION",
            "Build a multi-clip plan with each generated segment at or below 30 seconds, then join the approved clips.",
        )


def check_mode(issues: list[Issue], text: str, mode: str) -> None:
    low = text.lower()
    if mode == "edit":
        if "sole editing master" not in low:
            add(issues, "error", "EDIT_MASTER", "Editing must define one source video as the sole editing master.")
        if not re.search(r"\b(edit|modify|replace|remove|add|insert|change)\b", low):
            add(issues, "error", "EDIT_TARGET", "Editing must name an edit operation and target.")
        if not re.search(r"\b(only|within|scope|from \d|entire video)\b", low):
            add(issues, "warning", "EDIT_SCOPE", "Define the edited object/category, interval or region, and quantity.")
        if not re.search(r"\b(unchanged|remain unchanged|keep all other|except for)\b", low):
            add(issues, "error", "EDIT_PRESERVATION", "Close the edit scope by stating what remains unchanged.")
        if not re.search(r"\b(inherits?|timeline|appearance timing|motion slot|event order)\b", low):
            add(issues, "warning", "EDIT_INHERITANCE", "State how the edit inherits the source timeline, motion, occlusion, and event order.")
    elif mode == "extension":
        if "source video to extend" not in low:
            add(issues, "error", "EXTENSION_SOURCE", "Extension must identify one source video to extend.")
        forward = "extend forward" in low
        backward = "extend backward" in low
        if forward == backward:
            add(issues, "error", "EXTENSION_DIRECTION", "State exactly one direction: forward or backward.")
        if forward and not re.search(r"first frame of the extended segment.+last frame", low, re.DOTALL):
            add(issues, "error", "FORWARD_BOUNDARY", "Forward extension must continue from the source video's last frame.")
        if backward and not re.search(r"last frame of the extended segment.+first frame", low, re.DOTALL):
            add(issues, "error", "BACKWARD_BOUNDARY", "Backward extension must end at the source video's first frame.")
        if not re.search(r"\b(without duplication|without duplicat|same continuous|single continuous|do not duplicate|no duplication)\b", low):
            add(issues, "warning", "EXTENSION_INSTANCE", "State that each subject remains one continuous instance without duplication or splitting.")
        if not re.search(r"\b(audio state|audio environment|ambience|sound|dialogue|silence)\b", low):
            add(issues, "warning", "EXTENSION_AUDIO", "Describe audio continuity or an explicit silent state at the boundary.")


def check_content(issues: list[Issue], text: str, allow_music: bool, allow_template_placeholders: bool) -> None:
    if TODO_MARKER_RE.search(text):
        add(issues, "error", "PLACEHOLDER", "Prompt contains an unresolved TODO marker.")
    if not allow_template_placeholders and TEMPLATE_PLACEHOLDER_RE.search(text):
        add(issues, "error", "PLACEHOLDER", "Prompt contains an unresolved template placeholder.")
    if re.search(r"```|^#{1,6}\s", text, re.MULTILINE):
        add(issues, "warning", "OUTER_MARKDOWN", "Submit-ready prompt bodies should not include code fences or response headings.")
    if re.search(r"\b(generate|create|render)\b[^\n]{0,50}\b\d+(?:\.\d+)?[- ]second\b", text, re.IGNORECASE):
        add(issues, "warning", "TOTAL_DURATION_PARAMETER", "Set total duration outside the creative prompt; keep only event timing that is creative direction.")
    if re.search(r"\b(?:16:9|9:16|4:3|3:4|1:1|\d{3,4}p|4K|\d+\s*fps)\b", text, re.IGNORECASE):
        add(issues, "warning", "OUTPUT_PARAMETER", "Keep ratio, resolution, and frame-rate settings outside the creative prompt unless they describe an essential source constraint.")
    if re.search(r"\b(frame[- ]accurate|pixel[- ]identical|perfect adherence|no artifacts|guaranteed)\b", text, re.IGNORECASE):
        add(issues, "warning", "UNSUPPORTED_GUARANTEE", "Replace guarantees with observable goals and disclose documented limitations.")
    if not allow_music:
        positive_music = re.search(r"(?<!no )(?<!remove )(?<!without )\b(?:BGM|background music|music plays|instrumental music|soundtrack)\b", text, re.IGNORECASE)
        if positive_music:
            add(issues, "warning", "MUSIC_DEFAULT", "Music is present. Use --allow-music only when the user explicitly requested it.")
    if len(text.strip()) < 40:
        add(issues, "warning", "SPARSE_PROMPT", "Prompt is unusually short; confirm that subject and primary event are explicit.")


def lint(
    text: str,
    mode: str = "auto",
    *,
    images: int | None = None,
    videos: int | None = None,
    audio: int | None = None,
    video_seconds: float | None = None,
    audio_seconds: float | None = None,
    target_duration: float | None = None,
    allow_music: bool = False,
    anchor_mode: str = "semantic",
    allow_template_placeholders: bool = False,
) -> tuple[str, list[Issue]]:
    selected_mode = infer_mode(text) if mode == "auto" else mode
    issues: list[Issue] = []
    handles = referenced_handles(text)
    check_counts(issues, handles, images, videos, audio, video_seconds, audio_seconds)
    check_target_duration(issues, target_duration)
    check_roles(issues, text, handles)
    check_timeline(issues, text)
    check_anchor_syntax(issues, text, anchor_mode)
    check_mode(issues, text, selected_mode)
    check_content(issues, text, allow_music, allow_template_placeholders)
    return selected_mode, issues


def run_self_test() -> None:
    good_edit = """[Edit Goal]
Edit @Video 1. Change only the red lamp to the white lamp from @Image 1.
[Source Video Role]
@Video 1 is the sole editing master. It defines the original scene, camera, occlusion, audio, and event order.
@Image 1 defines only the white lamp's structure. Do not use its background.
[Edit Scope]
Modify only one lamp. Except for that object, all other visible people, props, and background elements remain unchanged.
[Timeline Inheritance]
The white lamp inherits every appearance timing, motion, and occlusion of the red lamp.
"""
    mode, issues = lint(good_edit, "edit", images=1, videos=1, audio=0)
    assert mode == "edit"
    assert not [i for i in issues if i.severity == "error"], issues

    bad_extension = "Extend @Video 1 and add a second copy."
    _, issues = lint(bad_extension, "extension", videos=1)
    codes = {i.code for i in issues}
    assert {"EXTENSION_SOURCE", "EXTENSION_DIRECTION"}.issubset(codes), codes

    timeline = "0-3 seconds: A. 5-7 seconds: B."
    _, issues = lint(timeline)
    assert "TIMELINE_GAP" in {i.code for i in issues}

    inline_timeline = "0-3 seconds...3-7 seconds...9-12 seconds"
    _, issues = lint(inline_timeline)
    assert "TIMELINE_GAP" in {i.code for i in issues}

    bracket_timeline = "[1s-4s]....[4s-8s]....[7s-12s]"
    _, issues = lint(bracket_timeline)
    assert "TIMELINE_OVERLAP" in {i.code for i in issues}

    not_a_timeline = "Use a 5-10 seconds subject-reference clip. Support ratios in the range 0.4-2.5."
    _, issues = lint(not_a_timeline)
    assert not {"INVALID_TIME_RANGE", "TIMELINE_GAP", "TIMELINE_OVERLAP"} & {i.code for i in issues}, issues

    two_reference_durations = "Use a 5-10 seconds subject clip and a 5-10 seconds voice clip."
    _, issues = lint(two_reference_durations)
    assert not {"INVALID_TIME_RANGE", "TIMELINE_GAP", "TIMELINE_OVERLAP"} & {i.code for i in issues}, issues

    _, issues = lint("@Image 31 defines a prop.", images=31)
    assert "IMAGE_LIMIT" in {i.code for i in issues}

    surface_styles = """@Image1 defines the hero's appearance.
[Image 1] defines the same hero's wardrobe.
<Image 1> defines the hero's profile view.
@Video is the before-transition clip and defines its ending composition.
[Video 2] is the after-transition clip and defines its opening composition.
@Audio defines the hero's voice.
[Audio 2] defines the room ambience.
"""
    _, issues = lint(surface_styles, images=1, videos=2, audio=2)
    forbidden = {"MISSING_IMAGE_HANDLE", "MISSING_VIDEO_HANDLE", "MISSING_AUDIO_HANDLE", "UNBOUND_REFERENCE", "PLACEHOLDER"}
    assert not forbidden & {i.code for i in issues}, issues

    semantic_anchor = "Use [Image 1] as the first frame and preserve its opening composition."
    _, semantic_issues = lint(semantic_anchor, images=1, anchor_mode="semantic")
    assert "WEAK_FIRST_FRAME_ROLE" not in {i.code for i in semantic_issues}, semantic_issues
    _, strict_issues = lint(semantic_anchor, images=1, anchor_mode="strict")
    assert "WEAK_FIRST_FRAME_ROLE" in {i.code for i in strict_issues}, strict_issues
    _, exact_issues = lint("[Image 1] is the first frame.", images=1, anchor_mode="strict")
    assert "WEAK_FIRST_FRAME_ROLE" not in {i.code for i in exact_issues}, exact_issues

    _, issues = lint("The room is empty. <a distant bell rings>.")
    assert "PLACEHOLDER" not in {i.code for i in issues}, issues
    _, issues = lint("@Image1 defines <Subject A>.", images=1, allow_template_placeholders=True)
    assert "PLACEHOLDER" not in {i.code for i in issues}, issues

    _, issues = lint("A complete but segmented story prompt.", target_duration=31)
    assert {"TARGET_DURATION_LIMIT", "TARGET_DURATION_SEGMENTATION"}.issubset({i.code for i in issues}), issues
    print("prompt_lint self-test: PASS")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", nargs="?", type=Path, help="UTF-8 text file containing one Seedance 2.5 prompt")
    parser.add_argument("--mode", choices=("auto", "generation", "edit", "extension"), default="auto")
    parser.add_argument("--images", type=int)
    parser.add_argument("--videos", type=int)
    parser.add_argument("--audio", type=int)
    parser.add_argument("--video-seconds", type=float)
    parser.add_argument("--audio-seconds", type=float)
    parser.add_argument("--target-duration", type=float, help="Requested generated-video duration in seconds")
    parser.add_argument("--allow-music", action="store_true")
    parser.add_argument(
        "--anchor-mode",
        choices=("semantic", "strict"),
        default="semantic",
        help="Use strict only when first_frame/last_frame roles require standalone anchor sentences",
    )
    parser.add_argument(
        "--allow-template-placeholders",
        action="store_true",
        help="Permit angle-bracket template fields while linting a reusable prompt template",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        run_self_test()
        return 0
    if args.prompt is None:
        parser.error("prompt file is required unless --self-test is used")

    text = args.prompt.read_text(encoding="utf-8")
    mode, issues = lint(
        text,
        args.mode,
        images=args.images,
        videos=args.videos,
        audio=args.audio,
        video_seconds=args.video_seconds,
        audio_seconds=args.audio_seconds,
        target_duration=args.target_duration,
        allow_music=args.allow_music,
        anchor_mode=args.anchor_mode,
        allow_template_placeholders=args.allow_template_placeholders,
    )
    errors = sum(i.severity == "error" for i in issues)
    warnings = sum(i.severity == "warning" for i in issues)
    if args.as_json:
        print(json.dumps({"mode": mode, "errors": errors, "warnings": warnings, "issues": [asdict(i) for i in issues]}, indent=2))
    else:
        print(f"mode={mode} errors={errors} warnings={warnings}")
        for issue in issues:
            print(f"{issue.severity.upper():7} {issue.code}: {issue.message}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
