#!/usr/bin/env python3
"""Deterministic linter for structured, hosted, and native-ComfyUI MiniMax H3 prompts."""

from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


BASE_FIELDS = (
    "integrated_multimodal_description",
    "overall_soundscape",
    "non_diegetic_music",
)
REF_FIELDS = (
    "subject_definitions",
    "summary",
    "retention_analysis",
    "detailed_description",
    "overall_soundscape",
    "non_diegetic_music",
)
MODES = ("auto", "t2va", "i2va", "fl2va", "l2va", "ref2va")
PROFILES = ("structured", "comfyui", "hosted")
REF_LABEL_RE = re.compile(r"<(Subject|Picture|Video|Audio) (\d+)>")
MEDIAISH_TAG_RE = re.compile(
    r"<+[^<>\n]*(?:Subject|Picture|Image|Pic|Video|Audio)\s*#?\s*(?:\d+|N)\b[^<>\n]*>+",
    re.IGNORECASE,
)
DANGLING_MEDIA_TAG_RE = re.compile(
    r"<+\s*(?:Subject|Picture|Image|Pic|Video|Audio)\s*#?\s*(?:\d+|N)\b(?![^<>\n]*>)",
    re.IGNORECASE,
)
LOOSE_MEDIA_TAG_RE = re.compile(
    r"<+\s*(Subject|Picture|Image|Pic|Video|Audio)\s*#?\s*(\d+)\s*>+",
    re.IGNORECASE,
)
SHOT_RE = re.compile(r"\[Shot (\d+)\]")
CUT_TIME_RE = re.compile(r"^\s*At (\d{2}):(\d{2})\.(\d{3}),")
COMFY_TIME_RANGE_RE = re.compile(
    r"\[(-?\d+(?:\.\d+)?)s\s*[-–—]\s*(-?\d+(?:\.\d+)?)s\]",
    re.IGNORECASE,
)
COMFY_CLOCK_RANGE_RE = re.compile(
    r"\bfrom\s+(\d{1,2}:\d{2}(?::\d{2})?\.\d{3})\s+to\s+"
    r"(\d{1,2}:\d{2}(?::\d{2})?\.\d{3})",
    re.IGNORECASE,
)
HOSTED_TIMED_HEADER_RE = re.compile(
    r"(?mi)^[ \t]*(?:[-*][ \t]+)?(?:CUT[ \t]+(\d+)[ \t]*\|[ \t]*)?"
    r"(-?\d+(?:\.\d+)?)[ \t]*(?:s|seconds?)?[ \t]*[-–—][ \t]*"
    r"(-?\d+(?:\.\d+)?)[ \t]*(?:s|seconds?)\b"
    r"[ \t]*(?:(\||—|-|:)[ \t]*([^\n]*))?[ \t]*$"
)
HOSTED_CLOCK_TIMED_HEADER_RE = re.compile(
    r"(?mi)^[ \t]*(?:[-*][ \t]+)?(?:CUT[ \t]+(\d+)[ \t]*\|[ \t]*)?"
    r"(\d{1,2}:\d{2}(?:\.\d{1,3})?)[ \t]*[-–—][ \t]*"
    r"(\d{1,2}:\d{2}(?:\.\d{1,3})?)(?!\d)(?!\.\d)(?!(?::\d))"
    r"[ \t]*(?:(\||—|-|:)[ \t]*)?([^\n]*)[ \t]*$"
)
HOSTED_CLOCK_RANGE_RE = re.compile(
    r"(?i)(?<![A-Za-z0-9_:])(?:CUT\s+(\d+)\s*\|\s*)?"
    r"(\d{1,2}:\d{2}(?:\.\d{1,3})?)[ \t]*[-–—][ \t]*"
    r"(\d{1,2}:\d{2}(?:\.\d{1,3})?)(?!\d)(?!\.\d)(?!(?::\d))[ \t]*(:)?()"
)
HOSTED_CUT_COUNT_RE = re.compile(
    r"\bexactly\s+(\d+)\s+(?:distinct\s+)?cuts?\b", re.IGNORECASE
)
HOSTED_CUT_LIKE_LINE_RE = re.compile(
    r"(?mi)^\s*CUT\s+#?\s*\d+\s*\|[^\n]*$"
)
PARAMETER_DECL_RE = re.compile(
    r'^([A-Z][A-Z0-9_]*)\s*=\s*"([^"\n]*)"\s*$'
)
HOSTED_MEDIA_HANDLE_RE = re.compile(
    r"@(Image|Video|Audio)\s+(\d+)\b", re.IGNORECASE
)
HOSTED_MEDIAISH_HANDLE_RE = re.compile(
    r"@(?:Image|Video|Audio)\s*#?\s*\d+\b", re.IGNORECASE
)
HOSTED_SHOT_HEADER_RE = re.compile(r"(?mi)^\s*Shot\s+\d+\b")
CONTINUOUS_TOPOLOGY_RE = re.compile(
    r"\b(?:one|single)[-\s]+(?:continuous[-\s]+)?take\b|"
    r"\b(?:one|single)[-\s]+continuous[-\s]+shot\b|"
    r"^\s*(?:global(?:\s+rule)?\s*:\s*)?no[-\s]+cuts?\s*[.!]?\s*$",
    re.IGNORECASE | re.MULTILINE,
)
HOSTED_NO_MUSIC_RE = re.compile(
    r"\b(?:no|without)\s+(?:added\s+)?(?:background\s+music|bgm|"
    r"non[-\s]diegetic\s+music|audience[-\s]only\s+music|soundtrack)\b|"
    r"non[-_\s]diegetic\s+music\s*:\s*N\s*/\s*A",
    re.IGNORECASE,
)
HOSTED_POSITIVE_MUSIC_RE = re.compile(
    r"\b(?:add|include|use|play|with|featuring)\b[^.\n]{0,100}"
    r"\b(?:background\s+music|bgm|musical\s+score|orchestral\s+score|"
    r"audience[-\s]only\s+score|soundtrack)\b",
    re.IGNORECASE,
)
HOSTED_NEGATED_MUSIC_REQUEST_RE = re.compile(
    r"\b(?:do\s+not|don't|never)\s+(?:add|include|use|play|feature)\b"
    r"[^.\n;]{0,100}\b(?:background\s+music|bgm|musical\s+score|"
    r"orchestral\s+score|audience[-\s]only\s+score|soundtrack)\b",
    re.IGNORECASE,
)
BPM_RE = re.compile(
    r"(?<![\w.])([+-]?\d+(?:\.\d+)?)\s*BPM\b",
    re.IGNORECASE,
)
TEMPO_ROLE_RE = re.compile(
    r"\b(?:audible(?:\s+(?:music|beat|pulse|clicks?))?|music|musical|score|soundtrack|"
    r"BGM|beat|click[-\s]?track|metronome|silent\s+(?:timing|choreograph\w*|grid)|"
    r"internal\s+(?:beat|pulse|timing|choreograph\w*|grid)|choreograph(?:y|ed|ic)?|"
    r"rhythm(?:ic|ically)?)\b",
    re.IGNORECASE,
)
TEMPO_ATMOSPHERIC_RE = re.compile(
    r"\b(?:BPM|tempo)\b[^.\n]{0,80}\b(?:atmospheric|approximate|loose|not exact)\b|"
    r"\b(?:atmospheric|approximate|loose|not exact)\b[^.\n]{0,80}\b(?:BPM|tempo)\b",
    re.IGNORECASE,
)
QUOTED_TEXT_RE = re.compile(
    r'"[^"\n]*"|“[^”\n]*”|(?<!\w)\'[^\'\n]*\'(?!\w)'
)
BEAT_ANCHOR_RE = re.compile(r"\bBeats?\s+(\d+(?:\.\d+)?)\b", re.IGNORECASE)
BEAT_LIST_RE = re.compile(
    r"\bBeats?\s+(\d+(?:\.\d+)?(?:\s*(?:,|and|&|[-–—])\s*"
    r"(?:and\s+)?\d+(?:\.\d+)?)+)",
    re.IGNORECASE,
)
POSE_THEN_BEAT_BINDING_RE = re.compile(
    r"\bPose\s+(\d+)\b(?:(?!\bPose\s+\d+\b)(?:\d+\.\d+|[^.;\n])){0,100}?"
    r"\bBeat\s+(\d+(?:\.\d+)?)\b",
    re.IGNORECASE,
)
BEAT_THEN_POSE_BINDING_RE = re.compile(
    r"\bBeat\s+(\d+(?:\.\d+)?)\b(?:(?!\bBeat\s+\d+(?:\.\d+)?\b)"
    r"(?:\d+\.\d+|[^.;\n])){0,100}?"
    r"\bPose\s+(\d+)\b",
    re.IGNORECASE,
)
GLOBAL_POSE_BEAT_LIST_RE = re.compile(
    r"\b(?:poses\b|pose\s+locks?\b)[^.;\n]{0,100}?"
    r"(?:\b(?:on|to)[ \t]+|:[ \t]*)Beats?[ \t]+"
    r"(\d+(?:\.\d+)?(?:[ \t]*(?:,|and|&|[-–—])[ \t]*"
    r"(?:and[ \t]+)?\d+(?:\.\d+)?)+)",
    re.IGNORECASE,
)
BEAT_ORIGIN_RE = re.compile(
    r"\bBeat\s+1\b(?:\s+(?:begins?|starts?|lands?|occurs?))?\s+at\s+"
    r"([+-]?\d+(?:\.\d+)?)\s*(?:s|seconds?)\b",
    re.IGNORECASE,
)
BEAT_ORIGIN_CLOCK_RE = re.compile(
    r"\bBeat\s+1\b(?:[ \t]+(?:begins?|starts?|lands?|occurs?))?[ \t]+at[ \t]+"
    r"(\d{1,2}:\d{2}(?:\.\d{1,3})?)(?!\d)(?!\.\d)(?!:\d)",
    re.IGNORECASE,
)
BEAT_THEN_TIME_RE = re.compile(
    r"\bBeat\s+(\d+(?:\.\d+)?)\b[^.;\n]{0,80}?\bat\s+"
    r"(\d+(?:\.\d+)?)\s*(?:s|seconds?)\b",
    re.IGNORECASE,
)
TIME_THEN_BEAT_RE = re.compile(
    r"\bat\s+(\d+(?:\.\d+)?)\s*(?:s|seconds?)\b[^.;\n]{0,80}?"
    r"\b(?:on\s+)?Beat\s+(\d+(?:\.\d+)?)\b",
    re.IGNORECASE,
)
BEAT_THEN_CLOCK_TIME_RE = re.compile(
    r"\bBeat\s+(\d+(?:\.\d+)?)\b[^.;\n]{0,80}?\bat[ \t]+"
    r"(\d{1,2}:\d{2}(?:\.\d{1,3})?)(?!\d)(?!\.\d)(?!:\d)",
    re.IGNORECASE,
)
CLOCK_TIME_THEN_BEAT_RE = re.compile(
    r"\bat[ \t]+(\d{1,2}:\d{2}(?:\.\d{1,3})?)(?!\d)(?!\.\d)(?!:\d)"
    r"[^.;\n]{0,80}?"
    r"\b(?:on[ \t]+)?Beat[ \t]+(\d+(?:\.\d+)?)\b",
    re.IGNORECASE,
)
POSE_LABEL_RE = re.compile(r"\bPose\s+(\d+)\b", re.IGNORECASE)
POSE_COUNT_RE = re.compile(
    r"\b(?:exactly|through)\s+"
    r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)\s+"
    r"(?:(?:numbered|distinct|precise|readable|held|stable|rapid|fast|hero|locked)"
    r"\s*(?:,\s*)?)*"
    r"(?:poses?\b(?!\s+locks?\b)|pose\s+locks?\b)"
    r"(?!\s+(?:(?:per|every|each)\b|at\s+a\s+time\b))",
    re.IGNORECASE,
)
SOURCE_POSE_PREFIX_RE = re.compile(
    r"(?:@(?:Image|Video|Audio)\s+\d+|<(?:Subject|Picture|Video|Audio)\s+\d+>|"
    r"\b(?:source|reference|storyboard|input)\b)[^.;\n]{0,100}"
    r"\b(?:contains?|shows?|depicts?|includes?|has|supplies?)\b[^.;\n]{0,160}$",
    re.IGNORECASE,
)
SOURCE_CLOCK_PREFIX_RE = re.compile(
    r"(?:@(?:Image|Video|Audio)\s+\d+|<(?:Subject|Picture|Video|Audio)\s+\d+>|"
    r"\b(?:source|reference|input)\b)[^.;\n]{0,120}"
    r"\b(?:from|between|segment|subclip|clip|interval|timing|timecodes?|range)\s*:?\s*$",
    re.IGNORECASE,
)
SOURCE_SECTION_MARKER_RE = re.compile(
    r"(?im)^[ \t]*(?:#{1,6}[ \t]*)?"
    r"(?:reference(?:[ \t]+asset)?|source(?:[ \t]+asset)?|input(?:[ \t]+asset)?)"
    r"[ \t]+(?:instructions?|timing|timecodes?|analysis|motion(?:[ \t]+instructions?)?)"
    r"(?:[ \t]*:|[ \t]*$)|"
    r"^[ \t]*@(?:Image|Video|Audio)[ \t]+\d+[^\n]{0,120}"
    r"\b(?:source|reference|input)[- \t]*(?:timing|timecodes?|subclip|interval|range)"
    r"(?:[ \t]*:|[ \t]*$)"
)
TARGET_SECTION_MARKER_RE = re.compile(
    r"(?im)^[ \t]*(?:#{1,6}[ \t]*)?(?:"
    r"(?:core[ \t]+concept|shot[- \t]+by[- \t]+shot[ \t]+description|"
    r"detailed[ \t]+description)(?:[ \t]*:|[ \t]*$)|"
    r"(?:target|output|generated(?:[ \t]+video)?)[ \t]+"
    r"(?:timeline|timing|instructions?|video|prompt|sequence)"
    r"(?:[ \t]*:|[ \t]*$))"
)
DIALOGUE_TOKEN_RE = re.compile(r"</?d>")
LOOSE_DIALOGUE_TAG_RE = re.compile(r"</?\s*[dD]\s*>")
SPEAKER_GROUP_RE = re.compile(r"\(S\d+(?:,S\d+)*\)")
SPEAKER_ID_RE = re.compile(r"S(\d+)")
DIRECT_AUDIO_CUE_RE = re.compile(
    r"<Audio (\d+)>[^.!?\n]{0,180}\b(?:reaches?|contains?|includes?|delivers?|"
    r"features?|plays?|continues?|begins?)\b[^.!?\n]{0,180}\b(?:phrase|lyrics?|line|words?|vocal|"
    r"dialogue|song)\b",
    re.IGNORECASE,
)
TOP_LEVEL_FIELD_RE = re.compile(r"(?m)^([a-z][a-z0-9_]*):")
FIELD_HEADING_RE = re.compile(r"(?m)^([ \t]*)([A-Za-z][A-Za-z0-9_]*):")

I2VA_ALIGNMENT = (
    "For the target video, at 0.00 seconds into the target video, "
    "<Picture 1> (from [Shot 1]) is fully referenced."
)

TASK_TYPES = {
    "keyframe completion",
    "reference generation",
    "video editing",
    "video continuation",
    "audio reuse",
    "audio reference",
}
VISUAL_RETENTION = {
    "fully_preserved",
    "partially_preserved",
    "attribute_transfer",
    "weak_reference",
}
AUDIO_RETENTION = {
    "fully_copy",
    "partially_copy",
    "reference",
    "weak_reference",
}
COUNT_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
}
MAX_LINTER_BPM = 10_000.0


@dataclass(frozen=True)
class Issue:
    level: str
    code: str
    message: str


def add(issues: list[Issue], level: str, code: str, message: str) -> None:
    issues.append(Issue(level, code, message))


def ordinal(raw: str) -> int:
    """Parse an ordinal without allowing pathological digit strings to crash."""
    if len(raw) > 12:
        return 10**12
    return int(raw)


def is_contiguous_from_one(numbers: list[int]) -> bool:
    return bool(numbers) and numbers[0] == 1 and all(
        current == previous + 1 for previous, current in zip(numbers, numbers[1:])
    )


def preview_numbers(numbers: list[int], limit: int = 12) -> str:
    shown = ", ".join(str(number) for number in numbers[:limit])
    return f"[{shown}{', ...' if len(numbers) > limit else ''}]"


def aligned_comfyui_frames(duration: float) -> int:
    requested_frames = max(5, round(duration * 24))
    return requested_frames + (5 - requested_frames % 17) % 17


def lint_media_tag_syntax(text: str, issues: list[Issue]) -> None:
    """Reject media-like angle tags that do not match the provider spelling exactly."""
    seen: set[tuple[int, int]] = set()
    for match in MEDIAISH_TAG_RE.finditer(text):
        if (match.start(), match.end()) in seen:
            continue
        seen.add((match.start(), match.end()))
        token = match.group(0)
        exact = re.fullmatch(r"<(Subject|Picture|Video|Audio) (\d+)>", token)
        if exact:
            parsed = ordinal(exact.group(2))
            if parsed < 1:
                add(
                    issues,
                    "ERROR",
                    "media-tag-ordinal",
                    f"Media ordinals start at 1; `{token}` is invalid.",
                )
            elif exact.group(2) != str(parsed):
                add(
                    issues,
                    "ERROR",
                    "media-tag-format",
                    f"Use canonical ordinal spelling `<{exact.group(1)} {parsed}>`, not `{token}`.",
                )
            continue

        loose = LOOSE_MEDIA_TAG_RE.fullmatch(token)
        if loose:
            media_type = loose.group(1).title()
            canonical_type = "Picture" if media_type in {"Image", "Pic"} else media_type
            canonical = f"<{canonical_type} {loose.group(2)}>"
            add(
                issues,
                "ERROR",
                "media-tag-format",
                f"Use exact provider tag `{canonical}`, not `{token}`.",
            )
        else:
            add(
                issues,
                "ERROR",
                "media-tag-format",
                f"Malformed or unsupported media tag `{token}`.",
            )

    for match in DANGLING_MEDIA_TAG_RE.finditer(text):
        add(
            issues,
            "ERROR",
            "media-tag-format",
            f"Media tag beginning `{match.group(0)}` is missing its closing `>`.",
        )

    for match in LOOSE_DIALOGUE_TAG_RE.finditer(text):
        if match.group(0) not in {"<d>", "</d>"}:
            add(
                issues,
                "ERROR",
                "dialogue-tag-format",
                f"Use exact dialogue tag `<d>` or `</d>`, not `{match.group(0)}`.",
            )


def last_sentence_fragment(text: str) -> str:
    """Return the current sentence without splitting common dotted abbreviations."""
    last_boundary = 0
    for boundary in re.finditer(r"[.!?]\s+", text):
        prefix = text[: boundary.start() + 1]
        if re.search(r"(?:\b[A-Za-z]\.){2,}$", prefix):
            continue
        if re.search(r"\b(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|vs|etc)\.$", prefix, re.IGNORECASE):
            continue
        last_boundary = boundary.end()
    return text[last_boundary:]


def parse_clock_time(value: str, issues: list[Issue]) -> float:
    parts = value.split(":")
    if len(parts) == 2:
        hours = 0
        minutes = int(parts[0])
        seconds = float(parts[1])
    else:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        if minutes >= 60:
            add(
                issues,
                "ERROR",
                "time-range-format",
                f"Clock timestamp `{value}` uses a minutes field above 59.",
            )
    if seconds >= 60:
        add(
            issues,
            "ERROR",
            "time-range-format",
            f"Clock timestamp `{value}` uses a seconds field above 59.999.",
        )
    return hours * 3600 + minutes * 60 + seconds


def parse_declared_count(value: str) -> int:
    lowered = value.lower()
    if lowered in COUNT_WORDS:
        return COUNT_WORDS[lowered]
    return ordinal(value)


def mask_quoted_text(text: str) -> str:
    """Hide quoted visible copy while preserving offsets for nearby-context checks."""
    return QUOTED_TEXT_RE.sub(lambda match: " " * len(match.group(0)), text)


def local_sentence(text: str, start: int, end: int) -> str:
    """Return the sentence-sized context around one match."""
    left = max(text.rfind(marker, 0, start) for marker in (".", "!", "?", "\n"))
    right_candidates = [
        position
        for marker in (".", "!", "?", "\n")
        if (position := text.find(marker, end)) != -1
    ]
    right = min(right_candidates) if right_candidates else len(text)
    return text[left + 1:right]


def clause_prefix(text: str, position: int) -> str:
    """Return the current short clause before a candidate contract."""
    start = max(text.rfind(marker, 0, position) for marker in (".", ";", "\n"))
    return text[start + 1:position]


def source_scoped_pose_count(text: str, match: re.Match[str]) -> bool:
    """Distinguish a source asset's count from the target output's count."""
    prefix = clause_prefix(text, match.start())
    if re.search(r"\b(?:target|output|generated|resulting|create|make)\b", prefix, re.IGNORECASE):
        return False
    return SOURCE_POSE_PREFIX_RE.search(prefix) is not None or source_section_active(
        text, match.start()
    )


def source_section_active(text: str, position: int) -> bool:
    """Return whether the nearest explicit scope heading marks source-only material."""
    source_start = max(
        (match.start() for match in SOURCE_SECTION_MARKER_RE.finditer(text, 0, position)),
        default=-1,
    )
    target_start = max(
        (match.start() for match in TARGET_SECTION_MARKER_RE.finditer(text, 0, position)),
        default=-1,
    )
    return source_start > target_start


def target_section_active(text: str, position: int) -> bool:
    """Return whether the nearest explicit scope heading marks target material."""
    source_start = max(
        (match.start() for match in SOURCE_SECTION_MARKER_RE.finditer(text, 0, position)),
        default=-1,
    )
    target_start = max(
        (match.start() for match in TARGET_SECTION_MARKER_RE.finditer(text, 0, position)),
        default=-1,
    )
    return target_start > source_start


def source_scoped_pose_label(text: str, match: re.Match[str]) -> bool:
    """Ignore Pose N labels that describe a reference rather than the output."""
    prefix = clause_prefix(text, match.start())
    if re.search(r"\b(?:target|output|generated|resulting|create|make)\b", prefix, re.IGNORECASE):
        return False
    return SOURCE_POSE_PREFIX_RE.search(prefix) is not None or source_section_active(
        text, match.start()
    )


def clock_seconds_unchecked(value: str) -> float:
    """Parse an M:SS clock candidate without emitting issues during classification."""
    minutes, seconds = value.split(":")
    return int(minutes) * 60 + float(seconds)


def spans_overlap(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return left[0] < right[1] and right[0] < left[1]


def select_inline_clock_headers(
    text: str,
    duration: float | None,
    excluded_spans: list[tuple[int, int]],
) -> list[re.Match[str]]:
    """Select one conservative inline M:SS timeline, not arbitrary clocks in prose."""
    quoted_spans = [(match.start(), match.end()) for match in QUOTED_TEXT_RE.finditer(text)]
    candidates: list[tuple[re.Match[str], float, float]] = []
    for match in HOSTED_CLOCK_RANGE_RE.finditer(text):
        span = (match.start(), match.end())
        if any(spans_overlap(span, excluded) for excluded in excluded_spans):
            continue
        if any(spans_overlap(span, quoted) for quoted in quoted_spans):
            continue
        if SOURCE_CLOCK_PREFIX_RE.search(clause_prefix(text, match.start())):
            continue
        if source_section_active(text, match.start()):
            continue
        start = clock_seconds_unchecked(match.group(2))
        end = clock_seconds_unchecked(match.group(3))
        candidates.append((match, start, end))

    chains: list[list[tuple[re.Match[str], float, float]]] = []
    for index, candidate in enumerate(candidates):
        if not math.isclose(candidate[1], 0.0, abs_tol=1e-9):
            continue
        chain = [candidate]
        previous_start = candidate[1]
        previous_end = candidate[2]
        explicit_target_scope = target_section_active(text, candidate[0].start())
        for following in candidates[index + 1:]:
            if math.isclose(following[1], 0.0, abs_tol=1e-9):
                break
            if following[1] < previous_start - 1e-6:
                break
            if explicit_target_scope and target_section_active(text, following[0].start()):
                pass
            elif duration is not None and previous_end >= duration - 1e-6:
                break
            elif duration is None:
                if not math.isclose(following[1], previous_end, abs_tol=1e-6):
                    continue
            elif following[1] > duration + max(1.0, duration * 0.25):
                continue
            chain.append(following)
            previous_start = following[1]
            previous_end = following[2]
        if len(chain) >= 2 or explicit_target_scope:
            chains.append(chain)

    if not chains:
        return []

    def chain_score(chain: list[tuple[re.Match[str], float, float]]) -> tuple[int, int, float]:
        endpoint = chain[-1][2]
        reaches_duration = int(
            duration is not None and math.isclose(endpoint, duration, abs_tol=1e-6)
        )
        distance = 0.0 if duration is None else abs(endpoint - duration)
        return reaches_duration, len(chain), -distance

    selected = max(chains, key=chain_score)
    return [match for match, _, _ in selected]


def has_substantive_timed_body(value: str) -> bool:
    """Reject empty or separator-only text between timing headers."""
    return re.search(r"\w", value, re.UNICODE) is not None


def has_unquoted_clock_range(value: str) -> bool:
    """Detect a second phase clock inside a nominally full-line clock header."""
    quoted_spans = [(match.start(), match.end()) for match in QUOTED_TEXT_RE.finditer(value)]
    return any(
        not any(
            spans_overlap((match.start(), match.end()), quoted)
            for quoted in quoted_spans
        )
        for match in HOSTED_CLOCK_RANGE_RE.finditer(value)
    )


def extract_beat_anchors(text: str) -> list[float]:
    """Read singular anchors and every item/range endpoint in `Beats ...` lists."""
    anchors = [float(raw) for raw in BEAT_ANCHOR_RE.findall(text)]
    for match in BEAT_LIST_RE.finditer(text):
        anchors.extend(float(raw) for raw in re.findall(r"\d+(?:\.\d+)?", match.group(1)))
    return anchors


def strictly_increasing(values: list[float]) -> bool:
    return all(current > previous for previous, current in zip(values, values[1:]))


def lint_rhythm_and_pose_contracts(
    text: str,
    duration: float | None,
    issues: list[Issue],
) -> None:
    """Check only deterministic parts of tempo grids and numbered pose contracts."""
    semantic_text = mask_quoted_text(text)
    bpm_matches = list(BPM_RE.finditer(semantic_text))
    bpm_values: list[float] = []
    role_missing = False
    for match in bpm_matches:
        bpm = float(match.group(1))
        if not math.isfinite(bpm):
            add(issues, "ERROR", "tempo-value", "BPM must be a finite number.")
            continue
        if bpm <= 0:
            add(issues, "ERROR", "tempo-value", "BPM must be greater than zero.")
            continue
        if bpm > MAX_LINTER_BPM:
            add(
                issues,
                "ERROR",
                "tempo-value",
                f"{bpm:g} BPM is too large for a meaningful H3 timing grid.",
            )
            continue
        if bpm not in bpm_values:
            bpm_values.append(bpm)
        if TEMPO_ROLE_RE.search(local_sentence(semantic_text, match.start(), match.end())) is None:
            role_missing = True

    bpm_values.sort()
    for bpm in bpm_values:
        if duration is not None:
            beat_seconds = 60 / bpm
            total_beats = duration * bpm / 60
            rendered_beats = (
                str(int(round(total_beats)))
                if math.isclose(total_beats, round(total_beats), abs_tol=1e-9)
                else f"{total_beats:.3f}"
            )
            add(
                issues,
                "INFO",
                "tempo-grid",
                f"{bpm:g} BPM gives {beat_seconds:.6f}s per beat and {rendered_beats} "
                f"beats across {duration:g}s. Verify named locks, cuts, flashes, impacts, "
                "and clicks against one declared beat origin.",
            )

    if bpm_values and role_missing:
        add(
            issues,
            "WARN",
            "tempo-role",
            "At least one BPM declaration does not locally say whether it governs audible "
            "music, a click track, synchronized physical sounds, or a silent/internal "
            "choreography grid.",
        )

    pose_label_matches = [
        match
        for match in POSE_LABEL_RE.finditer(semantic_text)
        if not source_scoped_pose_label(semantic_text, match)
    ]
    pose_labels = [ordinal(match.group(1)) for match in pose_label_matches]
    first_pose_occurrences: list[int] = []
    for pose in pose_labels:
        if pose not in first_pose_occurrences:
            first_pose_occurrences.append(pose)
    if first_pose_occurrences and first_pose_occurrences != list(
        range(1, max(first_pose_occurrences) + 1)
    ):
        add(
            issues,
            "WARN",
            "pose-sequence",
            "Numbered pose locks should first appear once in order from Pose 1; found "
            f"{preview_numbers(first_pose_occurrences)}.",
        )

    declared_pose_counts = [
        parse_declared_count(match.group(1))
        for match in POSE_COUNT_RE.finditer(semantic_text)
        if not source_scoped_pose_count(semantic_text, match)
    ]
    if len(set(declared_pose_counts)) > 1:
        add(
            issues,
            "WARN",
            "pose-count-declaration",
            "The prompt contains conflicting declared pose-lock counts.",
        )
    elif declared_pose_counts:
        declared = declared_pose_counts[0]
        unique_poses = sorted(set(pose_labels))
        if not unique_poses:
            add(
                issues,
                "WARN",
                "pose-count-unmapped",
                f"The prompt declares {declared} poses but does not label the counted locks. "
                "Number them and distinguish held poses from transitional body shapes.",
            )
        elif len(unique_poses) != declared or unique_poses != list(range(1, declared + 1)):
            add(
                issues,
                "WARN",
                "pose-count",
                f"The prompt declares {declared} poses but labels "
                f"{preview_numbers(unique_poses)}. Count every held state and keep transitions "
                "from becoming extra unnumbered locks.",
            )

    beat_anchors = extract_beat_anchors(semantic_text)
    invalid_beats = sorted({beat for beat in beat_anchors if beat < 1})
    if invalid_beats:
        add(
            issues,
            "WARN",
            "beat-ordinal",
            f"Beat numbering is 1-based; invalid anchors: {preview_numbers(invalid_beats)}.",
        )
    pose_beat_map: dict[int, set[float]] = {}
    for match in POSE_THEN_BEAT_BINDING_RE.finditer(semantic_text):
        if not source_scoped_pose_label(semantic_text, match):
            pose_beat_map.setdefault(ordinal(match.group(1)), set()).add(
                float(match.group(2))
            )
    for match in BEAT_THEN_POSE_BINDING_RE.finditer(semantic_text):
        if (
            not source_scoped_pose_label(semantic_text, match)
            and POSE_LABEL_RE.search(clause_prefix(semantic_text, match.start())) is None
        ):
            pose_beat_map.setdefault(ordinal(match.group(2)), set()).add(
                float(match.group(1))
            )

    global_pose_beat_lists = [
        [float(raw) for raw in re.findall(r"\d+(?:\.\d+)?", match.group(1))]
        for match in GLOBAL_POSE_BEAT_LIST_RE.finditer(semantic_text)
        if not source_scoped_pose_label(semantic_text, match)
    ]
    unique_pose_ids = sorted(set(pose_labels))
    mapped_pose_ids = set(pose_beat_map)
    individual_coverage = bool(unique_pose_ids) and set(unique_pose_ids) <= mapped_pose_ids
    individual_beat_sequence = [
        next(iter(pose_beat_map[pose]))
        for pose in unique_pose_ids
        if len(pose_beat_map.get(pose, set())) == 1
    ]
    individual_order_valid = (
        individual_coverage
        and len(individual_beat_sequence) == len(unique_pose_ids)
        and strictly_increasing(individual_beat_sequence)
    )
    matching_global_lists = [
        beat_list
        for beat_list in global_pose_beat_lists
        if len(beat_list) == len(unique_pose_ids)
    ]
    ordered_global_mapping = any(
        strictly_increasing(beat_list) for beat_list in matching_global_lists
    )

    invalid_individual_order = individual_coverage and not individual_order_valid
    invalid_global_order = bool(matching_global_lists) and not ordered_global_mapping
    if invalid_individual_order or invalid_global_order:
        add(
            issues,
            "WARN",
            "pose-beat-order",
            "Sequential pose locks need one strictly increasing Beat anchor per pose; "
            "remove duplicate, descending, or conflicting pose-to-Beat assignments.",
        )

    complete_pose_beat_map = individual_order_valid or ordered_global_mapping
    if (
        bpm_values
        and pose_labels
        and not complete_pose_beat_map
        and not individual_coverage
        and not TEMPO_ATMOSPHERIC_RE.search(semantic_text)
    ):
        missing_pose_ids = sorted(set(unique_pose_ids) - mapped_pose_ids)
        add(
            issues,
            "WARN",
            "rhythm-unmapped",
            "The prompt combines BPM with numbered poses but does not map every Pose N lock "
            f"to a beat; individually unmapped poses: {preview_numbers(missing_pose_ids)}. "
            "Bind each pose to Beat N, provide an ordered pose-lock Beat list of matching "
            "length, or state that tempo is atmospheric rather than exact.",
        )

    origin_candidates: list[float] = []
    for raw in BEAT_ORIGIN_RE.findall(semantic_text):
        origin_candidates.append(float(raw))
    for raw in BEAT_ORIGIN_CLOCK_RE.findall(semantic_text):
        parsed = parse_clock_time(raw, issues)
        if float(raw.split(":")[-1]) < 60:
            origin_candidates.append(parsed)

    origins: list[float] = []
    for origin in origin_candidates:
        if not math.isfinite(origin) or origin < 0:
            add(
                issues,
                "ERROR",
                "beat-origin-value",
                "Beat 1 must begin at a finite, non-negative target-video time.",
            )
        elif duration is not None and origin >= duration - 1e-9:
            add(
                issues,
                "ERROR",
                "beat-origin-value",
                f"Beat 1 at {origin:g}s is outside the visible 0 <= t < {duration:g}s window.",
            )
        else:
            origins.append(origin)
    unique_origins = sorted(set(origins))
    if len(unique_origins) > 1:
        add(
            issues,
            "WARN",
            "beat-origin",
            "The prompt declares more than one time origin for Beat 1.",
        )

    if duration is not None and len(bpm_values) == 1 and len(unique_origins) == 1:
        bpm = bpm_values[0]
        origin = unique_origins[0]
        beat_seconds = 60 / bpm
        outside = sorted(
            {
                beat
                for beat in beat_anchors
                if beat >= 1
                and (
                    origin + (beat - 1) * beat_seconds < -1e-9
                    or origin + (beat - 1) * beat_seconds >= duration - 1e-9
                )
            }
        )
        if outside:
            add(
                issues,
                "WARN",
                "beat-outside-duration",
                f"Beat anchors {preview_numbers(outside)} land outside the visible 0 <= t < "
                f"{duration:g}s window when Beat 1 is at {origin:g}s and tempo is {bpm:g} BPM.",
            )

        explicit_pairs: set[tuple[float, float]] = {
            (float(beat), float(seconds))
            for beat, seconds in BEAT_THEN_TIME_RE.findall(semantic_text)
        }
        explicit_pairs.update(
            (float(beat), float(seconds))
            for seconds, beat in TIME_THEN_BEAT_RE.findall(semantic_text)
        )
        explicit_pairs.update(
            (float(beat), parse_clock_time(clock, issues))
            for beat, clock in BEAT_THEN_CLOCK_TIME_RE.findall(semantic_text)
        )
        explicit_pairs.update(
            (float(beat), parse_clock_time(clock, issues))
            for clock, beat in CLOCK_TIME_THEN_BEAT_RE.findall(semantic_text)
        )
        mismatches: list[str] = []
        for beat, seconds in sorted(explicit_pairs):
            if beat < 1:
                continue
            expected = origin + (beat - 1) * beat_seconds
            if not math.isclose(seconds, expected, abs_tol=0.02):
                mismatches.append(
                    f"Beat {beat:g} at {seconds:g}s (expected about {expected:.3f}s)"
                )
        if mismatches:
            add(
                issues,
                "WARN",
                "beat-time-mismatch",
                "Explicit beat/time mappings disagree with the declared grid: "
                + "; ".join(mismatches[:6])
                + ("; ..." if len(mismatches) > 6 else "")
                + ".",
            )


def dialogue_spans(body: str, issues: list[Issue]) -> list[tuple[int, int, int]]:
    """Return valid top-level dialogue spans while rejecting reversed or nested tags."""
    spans: list[tuple[int, int, int]] = []
    opening: re.Match[str] | None = None
    nested = False
    for token in DIALOGUE_TOKEN_RE.finditer(body):
        if token.group(0) == "<d>":
            if opening is not None:
                nested = True
                add(issues, "ERROR", "dialogue-tags", "Dialogue tags cannot be nested.")
            else:
                opening = token
        elif opening is None:
            add(
                issues,
                "ERROR",
                "dialogue-tags",
                "A `</d>` tag appears before its matching `<d>` tag.",
            )
        else:
            spans.append((opening.end(), token.start(), token.end()))
            opening = None
            nested = False
    if opening is not None or nested:
        add(issues, "ERROR", "dialogue-tags", "A `<d>` tag is not properly closed.")
    return spans


def first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def infer_mode(text: str) -> str:
    first = first_nonempty_line(text)
    if first == "subject_definitions:":
        return "ref2va"
    if first == I2VA_ALIGNMENT:
        return "i2va"
    if first.startswith("How the reference pictures align with the target video —"):
        if "Picture 2" in first:
            return "fl2va"
        return "l2va"
    return "t2va"


def expected_alignment(mode: str, duration: float, final_shot: int) -> str:
    seconds = f"{duration:.2f}"
    if mode == "i2va":
        return I2VA_ALIGNMENT
    if mode == "fl2va":
        return (
            "How the reference pictures align with the target video — "
            "Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; "
            f"Picture 2 (from Shot {final_shot}) aligns with the {seconds}-second mark of the target video."
        )
    if mode == "l2va":
        return (
            "How the reference pictures align with the target video — "
            f"<Picture 1> (from [Shot {final_shot}]) aligns with the {seconds}-second mark of the target video."
        )
    raise ValueError(f"No alignment template for {mode}")


def alignment_shape_matches(line: str, mode: str, final_shot: int) -> bool:
    """Validate the immutable template while leaving final duration unconstrained."""
    if mode == "i2va":
        return line == I2VA_ALIGNMENT
    if mode == "fl2va":
        pattern = (
            r"How the reference pictures align with the target video — "
            r"Picture 1 \(from Shot 1\) aligns with the 0\.00-second mark of the target video; "
            rf"Picture 2 \(from Shot {final_shot}\) aligns with the \d+\.\d{{2}}-second mark of the target video\."
        )
        return re.fullmatch(pattern, line) is not None
    if mode == "l2va":
        pattern = (
            r"How the reference pictures align with the target video — "
            rf"<Picture 1> \(from \[Shot {final_shot}\]\) aligns with the "
            r"\d+\.\d{2}-second mark of the target video\."
        )
        return re.fullmatch(pattern, line) is not None
    return False


def find_sections(
    text: str, fields: Iterable[str], issues: list[Issue]
) -> dict[str, str]:
    fields = tuple(fields)
    matches: dict[str, list[re.Match[str]]] = {}
    for field in fields:
        found = list(re.finditer(rf"(?m)^{re.escape(field)}:", text))
        matches[field] = found
        if not found:
            add(issues, "ERROR", "missing-field", f"Missing `{field}:`.")
        elif len(found) > 1:
            add(
                issues,
                "ERROR",
                "duplicate-field",
                f"`{field}:` appears {len(found)} times; it must appear once.",
            )

    if any(len(matches[field]) != 1 for field in fields):
        return {}

    starts = [matches[field][0].start() for field in fields]
    if starts != sorted(starts):
        add(
            issues,
            "ERROR",
            "field-order",
            "Required fields are not in provider-defined order: " + " -> ".join(fields),
        )

    physical = sorted(
        ((matches[field][0].start(), matches[field][0].end(), field) for field in fields),
        key=lambda item: item[0],
    )
    sections: dict[str, str] = {}
    for index, (_, end, field) in enumerate(physical):
        next_start = physical[index + 1][0] if index + 1 < len(physical) else len(text)
        body = text[end:next_start].strip()
        sections[field] = body
        if not body:
            add(issues, "ERROR", "empty-field", f"`{field}:` has no content.")
    return sections


def lint_structured_semantics(
    sections: dict[str, str], timeline_field: str, issues: list[Issue]
) -> None:
    """Check safe cross-field contradictions in provider-structured prompts."""
    music = sections.get("non_diegetic_music", "").strip()
    if re.search(r"\bN\s*/\s*A\b", music, re.IGNORECASE) and not re.fullmatch(
        r"N\s*/\s*A[.!]?", music, re.IGNORECASE
    ):
        add(
            issues,
            "ERROR",
            "music-conflict",
            "`non_diegetic_music` contains `N/A` plus additional content. Use exactly `N/A` "
            "for no audience-only music, or remove `N/A` and describe the score.",
        )

    timeline = sections.get(timeline_field, "")
    if CONTINUOUS_TOPOLOGY_RE.search(timeline) and len(SHOT_RE.findall(timeline)) > 1:
        add(
            issues,
            "ERROR",
            "topology-conflict",
            "The timeline declares one continuous take/no cuts but contains multiple `[Shot N]` "
            "segments. Keep one `[Shot 1]` and describe continuous phases inside it, or remove the "
            "continuous-take rule.",
        )


def lint_top_level_fields(
    text: str, allowed_fields: Iterable[str], issues: list[Issue]
) -> None:
    """Reject provider-looking headings outside the selected mode's schema."""
    allowed = set(allowed_fields)
    seen: set[tuple[str, str]] = set()
    for match in FIELD_HEADING_RE.finditer(text):
        indent, field = match.groups()
        key = (indent, field)
        if key in seen:
            continue
        seen.add(key)
        if not indent and field in allowed:
            continue
        if field.lower() in allowed:
            add(
                issues,
                "ERROR",
                "field-format",
                f"Required field `{field}:` must use exact lowercase spelling at column 1.",
            )
        else:
            add(
                issues,
                "ERROR",
                "unknown-field",
                f"Unknown top-level field `{field}:` for the selected mode.",
            )


def parse_time(match: re.Match[str]) -> float:
    minutes = int(match.group(1))
    seconds = int(match.group(2))
    millis = int(match.group(3))
    return minutes * 60 + seconds + millis / 1000


def lint_shots(body: str, duration: float | None, issues: list[Issue]) -> int:
    matches = list(SHOT_RE.finditer(body))
    if not matches:
        add(issues, "ERROR", "missing-shot", "Timeline contains no `[Shot 1]` marker.")
        return 1

    numbers = [ordinal(match.group(1)) for match in matches]
    for match, number in zip(matches, numbers):
        if match.group(1) != str(number):
            add(
                issues,
                "ERROR",
                "shot-format",
                f"Use canonical shot marker `[Shot {number}]`, not `{match.group(0)}`.",
            )
    if numbers[0] != 1:
        add(issues, "ERROR", "first-shot", "The first timeline marker must be `[Shot 1]`.")

    if any(number != index for index, number in enumerate(numbers, start=1)):
        add(
            issues,
            "ERROR",
            "shot-sequence",
            "Shot markers must appear once in sequence starting at 1; found "
            f"{preview_numbers(numbers)}.",
        )

    cut_times: list[float] = []
    for index, match in enumerate(matches):
        shot = ordinal(match.group(1))
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        segment = body[match.end():next_start]
        time_match = CUT_TIME_RE.match(segment)
        if shot == 1 and time_match:
            add(issues, "ERROR", "shot-one-time", "`[Shot 1]` must not have a timestamp.")
        elif shot > 1:
            if not time_match:
                add(
                    issues,
                    "ERROR",
                    "missing-cut-time",
                    f"`[Shot {shot}]` must begin `At MM:SS.mmm, ...`.",
                )
            else:
                if int(time_match.group(2)) >= 60:
                    add(
                        issues,
                        "ERROR",
                        "cut-time-format",
                        f"Shot {shot} uses an invalid seconds field; MM:SS.mmm requires SS below 60.",
                    )
                cut_time = parse_time(time_match)
                cut_times.append(cut_time)
                if cut_time <= 0:
                    add(
                        issues,
                        "ERROR",
                        "cut-time-zero",
                        f"Shot {shot} must start after 00:00.000.",
                    )
                if duration is not None and cut_time >= duration:
                    add(
                        issues,
                        "ERROR",
                        "cut-outside-duration",
                        f"Shot {shot} starts at {cut_time:.3f}s, not inside {duration:.2f}s.",
                    )
                elif duration is None and cut_time >= 15:
                    add(
                        issues,
                        "ERROR",
                        "cut-outside-contract",
                        f"Shot {shot} starts at {cut_time:.3f}s, outside H3's maximum 15-second clip.",
                    )

    if any(later <= earlier for earlier, later in zip(cut_times, cut_times[1:])):
        add(issues, "ERROR", "cut-order", "Shot cut timestamps must increase strictly.")

    return max(numbers)


def lint_dialogue(
    text: str,
    sections: dict[str, str],
    timeline_field: str,
    mode: str,
    issues: list[Issue],
) -> list[list[int]]:
    """Validate dialogue placement and return speaker IDs for actual vocal events."""
    for field in sections:
        if field == timeline_field:
            continue
        if DIALOGUE_TOKEN_RE.search(sections.get(field, "")):
            add(
                issues,
                "ERROR",
                "dialogue-layer",
                f"Dialogue or lyrics must stay in `{timeline_field}`, not `{field}`.",
            )

    timeline = sections.get(timeline_field, "")
    spans = dialogue_spans(timeline, issues)
    for content_start, content_end, _ in spans:
        dialogue = timeline[content_start:content_end]
        if not re.fullmatch(r"\[[^\]\n]+\]\s+\S(?:.|\n)*", dialogue):
            add(
                issues,
                "ERROR",
                "dialogue-format",
                "Each `<d>` must contain only `[Language] spoken words`.",
            )

    copied_audio_ids: set[int] = set()
    if mode == "ref2va":
        for line in sections.get("retention_analysis", "").splitlines():
            copied = re.match(
                r"^<Audio (\d+)>.*?:\s*(fully_copy|partially_copy)\b",
                line.strip(),
            )
            if copied:
                copied_audio_ids.add(ordinal(copied.group(1)))

    speaker_events: list[list[int]] = []
    previous_dialogue_end = 0
    for content_start, _, dialogue_end in spans:
        dialogue_start = content_start - len("<d>")
        prior = timeline[:dialogue_start]
        shot_starts = [shot.start() for shot in SHOT_RE.finditer(prior)]
        event_start = max(previous_dialogue_end, shot_starts[-1] if shot_starts else 0)
        event_context = timeline[event_start:dialogue_start]
        # Ownership belongs in the same sentence/clause as the dialogue. This
        # prevents an unrelated speaker or audio mention earlier in the shot
        # from silently satisfying the source requirement.
        sentence_context = last_sentence_fragment(event_context)
        speaker_groups = list(SPEAKER_GROUP_RE.finditer(sentence_context))
        audio_cues = [
            cue
            for cue in DIRECT_AUDIO_CUE_RE.finditer(sentence_context)
            if ordinal(cue.group(1)) in copied_audio_ids
        ]

        latest_speaker = speaker_groups[-1] if speaker_groups else None
        latest_audio = audio_cues[-1] if audio_cues else None
        if latest_speaker is not None and (
            latest_audio is None or latest_speaker.end() > latest_audio.start()
        ):
            source = latest_speaker.group(0)
            speaker_events.append([ordinal(value) for value in SPEAKER_ID_RE.findall(source)])
        elif mode == "ref2va" and latest_audio is not None:
            # Official Ref2VA permits words embedded in directly reused audio to
            # use <Audio N> as the source without inventing a physical speaker.
            speaker_events.append([])
        else:
            exception = (
                " or a directly reused `<Audio N>` source"
                if mode == "ref2va"
                else ""
            )
            add(
                issues,
                "ERROR",
                "dialogue-source",
                "Each `<d>` vocal event needs a nearby `(Sx)` source"
                f"{exception} in the same sentence/event.",
            )
            speaker_events.append([])
        previous_dialogue_end = dialogue_end

    scene_transitions = text.count("<scenetrans>")
    if scene_transitions % 2:
        add(
            issues,
            "WARN",
            "scenetrans-pair",
            "`<scenetrans>` usually appears at connecting points on both sides of a cut; count is odd.",
        )

    return speaker_events


def lint_speakers(
    text: str,
    sections: dict[str, str],
    speaker_events: list[list[int]],
    issues: list[Issue],
) -> None:
    ids: list[int] = []
    for group in SPEAKER_GROUP_RE.findall(text):
        raw_ids = SPEAKER_ID_RE.findall(group)
        parsed_ids = [ordinal(value) for value in raw_ids]
        ids.extend(parsed_ids)
        for raw_id, speaker_id in zip(raw_ids, parsed_ids):
            if raw_id != str(speaker_id):
                add(
                    issues,
                    "ERROR",
                    "speaker-format",
                    f"Use canonical speaker ID `S{speaker_id}`, not `S{raw_id}`.",
                )
        if len(parsed_ids) != len(set(parsed_ids)):
            add(
                issues,
                "ERROR",
                "speaker-duplicate",
                f"Speaker group `{group}` repeats the same speaker ID.",
            )

    if ids:
        present = sorted(set(ids))
        if not is_contiguous_from_one(present):
            add(
                issues,
                "ERROR",
                "speaker-sequence",
                "Speaker IDs must be contiguous from S1; found "
                f"{preview_numbers(present)}.",
            )

    first_occurrences: list[int] = []
    for event in speaker_events:
        for speaker_id in event:
            if speaker_id not in first_occurrences:
                first_occurrences.append(speaker_id)
    if first_occurrences:
        if any(number != index for index, number in enumerate(first_occurrences, start=1)):
            add(
                issues,
                "ERROR",
                "speaker-event-order",
                "Speaker IDs must be assigned by first actual vocal event; "
                f"found first occurrences {preview_numbers(first_occurrences)}.",
            )

    if SPEAKER_GROUP_RE.search(sections.get("retention_analysis", "")):
        add(
            issues,
            "ERROR",
            "speaker-in-retention",
            "Do not write `(Sx)` IDs in `retention_analysis`.",
        )


def lint_alignment(
    text: str,
    mode: str,
    duration: float | None,
    final_shot: int,
    issues: list[Issue],
) -> None:
    lines = text.splitlines()
    first = first_nonempty_line(text)

    if mode == "t2va":
        if first.startswith("For the target video") or first.startswith(
            "How the reference pictures align"
        ):
            add(issues, "ERROR", "t2va-alignment", "T2VA must not use an image-alignment line.")
        if not text.startswith("integrated_multimodal_description:"):
            add(
                issues,
                "ERROR",
                "leading-content",
                "T2VA must begin with `integrated_multimodal_description:`.",
            )
        return

    if mode not in {"i2va", "fl2va", "l2va"}:
        return

    if duration is None and mode in {"fl2va", "l2va"}:
        add(
            issues,
            "WARN",
            "duration-needed",
            f"Pass `--duration` to verify the exact {mode.upper()} alignment line.",
        )
        if not alignment_shape_matches(first, mode, final_shot):
            add(issues, "ERROR", "alignment-line", f"Invalid {mode.upper()} alignment line.")
        else:
            declared_marks = re.findall(
                r"aligns with the (\d+\.\d{2})-second mark", first
            )
            if declared_marks and not 4 <= float(declared_marks[-1]) <= 15:
                add(
                    issues,
                    "ERROR",
                    "alignment-duration-range",
                    "The alignment's final timestamp must be between 4.00 and 15.00 seconds.",
                )
    else:
        alignment_duration = duration if duration is not None else 0.0
        expected = expected_alignment(mode, alignment_duration, final_shot)
        if first != expected:
            add(
                issues,
                "ERROR",
                "alignment-line",
                f"The first line does not exactly match the {mode.upper()} provider template. Expected: {expected}",
            )

    if not lines or lines[0] != first:
        add(
            issues,
            "ERROR",
            "alignment-position",
            "The alignment instruction must be the literal first line, with no leading blank line.",
        )
    if len(lines) < 3 or lines[1] != "" or not lines[2].startswith(
        "integrated_multimodal_description:"
    ):
        add(
            issues,
            "ERROR",
            "alignment-spacing",
            "The alignment instruction must be followed by exactly one blank line, then `integrated_multimodal_description:`.",
        )


def lint_base_reference_labels(text: str, mode: str, issues: list[Issue]) -> None:
    allowed: dict[str, set[str]] = {
        "t2va": set(),
        "i2va": {"<Picture 1>"},
        "fl2va": {"<Picture 1>", "<Picture 2>"},
        "l2va": {"<Picture 1>"},
    }
    used = {f"<{kind} {number}>" for kind, number in REF_LABEL_RE.findall(text)}
    for label in sorted(used - allowed.get(mode, set())):
        add(
            issues,
            "ERROR",
            "reference-label",
            f"{label} is not allowed in {mode.upper()} provider grammar.",
        )


def lint_comfyui_prompt(
    text: str,
    mode: str,
    duration: float | None,
    pictures: int | None,
    videos: int | None,
    audios: int | None,
    standalone_audios: int | None,
    raw_frames: int | None,
    trim_frames: int | None,
    tail_trim_frames: int | None,
    issues: list[Issue],
) -> None:
    """Validate the official native-ComfyUI freeform prompt surface."""
    formal_fields = set(BASE_FIELDS) | set(REF_FIELDS)
    if formal_fields & set(TOP_LEVEL_FIELD_RE.findall(text)):
        add(
            issues,
            "WARN",
            "structured-on-comfyui",
            "Native ComfyUI accepts a freeform prompt; Context-IR field headings are not required.",
        )

    effective_raw_frames: int | None = None
    if raw_frames is not None:
        if raw_frames < aligned_comfyui_frames(4) or raw_frames > aligned_comfyui_frames(15):
            add(
                issues,
                "ERROR",
                "raw-frame-range",
                f"Raw native frame count must be between {aligned_comfyui_frames(4)} and "
                f"{aligned_comfyui_frames(15)} frames for H3's 4–15-second contract.",
            )
        elif (raw_frames - 5) % 17:
            add(
                issues,
                "ERROR",
                "raw-frame-grid",
                "Raw native frame count must satisfy the official `17k+5` grid.",
            )
        else:
            effective_raw_frames = raw_frames
            if duration is not None and raw_frames < round(duration * 24):
                add(
                    issues,
                    "ERROR",
                    "raw-frame-duration",
                    f"{raw_frames} raw frames cannot contain the requested {duration:.3f}s "
                    f"({round(duration * 24)} frames before grid alignment).",
                )
    if effective_raw_frames is None and duration is not None:
        effective_raw_frames = aligned_comfyui_frames(duration)

    labels = [(kind, ordinal(number)) for kind, number in REF_LABEL_RE.findall(text)]
    subject_labels = sorted({number for kind, number in labels if kind == "Subject"})
    if subject_labels:
        add(
            issues,
            "ERROR",
            "subject-on-comfyui",
            "Raw native-ComfyUI prompts map connected media with `<Picture N>`, "
            "`<Video N>`, and `<Audio N>`; do not serialize Context-IR `<Subject N>` labels.",
        )

    media_labels = [(kind, number) for kind, number in labels if kind != "Subject"]
    if mode != "ref2va":
        allowed_endpoint_labels = {
            "t2va": set(),
            "i2va": {("Picture", 1)},
            "fl2va": {("Picture", 1), ("Picture", 2)},
            "l2va": {("Picture", 1)},
        }
        allowed = allowed_endpoint_labels.get(mode, set())
        used_media = set(media_labels)
        for kind, number in sorted(used_media - allowed):
            add(
                issues,
                "ERROR",
                "reference-label",
                f"<{kind} {number}> is not an allowed {mode.upper()} raw-prompt endpoint tag.",
            )
        missing_endpoints = sorted(allowed - used_media)
        if missing_endpoints:
            formatted = ", ".join(f"<{kind} {number}>" for kind, number in missing_endpoints)
            add(
                issues,
                "WARN",
                "endpoint-tag-missing",
                f"The official {mode.upper()} native prompt profile normally names its connected "
                f"endpoint(s): {formatted}.",
            )

        expected_pictures = {
            "t2va": 0,
            "i2va": 1,
            "fl2va": 2,
            "l2va": 1,
        }.get(mode, 0)
        supplied = {
            "pictures": pictures,
            "videos": videos,
            "audios": audios,
            "standalone audios": standalone_audios,
        }
        expected_counts = {
            "pictures": expected_pictures,
            "videos": 0,
            "audios": 0,
            "standalone audios": 0,
        }
        for label, count in supplied.items():
            if count is None:
                continue
            if count < 0:
                add(issues, "ERROR", "media-count", f"Connected {label} cannot be negative.")
            elif count != expected_counts[label]:
                add(
                    issues,
                    "ERROR",
                    "mode-media-count",
                    f"{mode.upper()} expects {expected_counts[label]} connected {label}, not {count}.",
                )
    else:
        if not media_labels:
            add(
                issues,
                "ERROR",
                "missing-media-tags",
                "Native ComfyUI Ref2VA prompts must name connected inputs with exact media tags.",
            )

        supplied_counts = any(
            value is not None for value in (pictures, videos, audios, standalone_audios)
        )
        if not supplied_counts:
            add(
                issues,
                "WARN",
                "media-counts-needed",
                "Pass `--pictures`, `--videos`, and `--audios` to verify connected-media ordinals.",
            )
        else:
            if any(value is None for value in (pictures, videos, audios)):
                add(
                    issues,
                    "WARN",
                    "media-counts-incomplete",
                    "Provide all of `--pictures`, `--videos`, and `--audios` for a complete graph check.",
                )

        counts: dict[str, int | None] = {
            "Picture": pictures,
            "Video": videos,
            "Audio": audios,
        }
        used = {
            kind: {number for label_kind, number in media_labels if label_kind == kind}
            for kind in counts
        }
        declared_picture_count = len(used["Picture"])
        declared_video_count = len(used["Video"])
        declared_audio_count = len(used["Audio"])
        declared_minimum_video_files = max(
            declared_video_count, min(declared_audio_count, 3)
        )
        declared_minimum_standalone_audios = max(0, declared_audio_count - 3)
        declared_minimum_files = (
            declared_picture_count
            + declared_minimum_video_files
            + declared_minimum_standalone_audios
        )
        if declared_minimum_files > 12:
            add(
                issues,
                "ERROR",
                "mixed-media-tags",
                f"The media tags imply at least {declared_minimum_files} mixed files, exceeding 12.",
            )
        video_limit_basis = videos if videos is not None and 0 <= videos <= 3 else 3
        limits = {"Picture": 9, "Video": 3, "Audio": video_limit_basis + 3}

        for kind, ordinals in used.items():
            for number in sorted(ordinals):
                if number < 1 or number > limits[kind]:
                    add(
                        issues,
                        "ERROR",
                        "media-ordinal",
                        f"<{kind} {number}> exceeds the possible native Ref2VA range 1–{limits[kind]}.",
                    )

        valid_counts: dict[str, int] = {}
        for kind, count in counts.items():
            if count is None:
                continue
            if count < 0:
                add(issues, "ERROR", "media-count", f"{kind} count cannot be negative.")
            elif count > limits[kind]:
                add(
                    issues,
                    "ERROR",
                    "media-count",
                    f"{kind} count {count} exceeds the official limit of {limits[kind]}.",
                )
            else:
                valid_counts[kind] = count

        standalone_valid = standalone_audios is None or 0 <= standalone_audios <= 3
        if standalone_audios is not None and not standalone_valid:
            add(
                issues,
                "ERROR",
                "standalone-audio-count",
                "Standalone audio file count must be between 0 and 3.",
            )

        if {"Picture", "Video", "Audio"} <= valid_counts.keys():
            if standalone_audios is not None and standalone_valid:
                if not standalone_audios <= valid_counts["Audio"] <= (
                    standalone_audios + valid_counts["Video"]
                ):
                    add(
                        issues,
                        "ERROR",
                        "audio-map-count",
                        "Total `<Audio N>` ordinals must equal standalone audios plus zero or one "
                        "enabled soundtrack per reference video.",
                    )
                total_files = (
                    valid_counts["Picture"] + valid_counts["Video"] + standalone_audios
                )
                if total_files > 12:
                    add(
                        issues,
                        "ERROR",
                        "mixed-media-count",
                        f"{total_files} mixed files exceeds the official limit of 12.",
                    )
            else:
                minimum_standalone = max(
                    0, valid_counts["Audio"] - valid_counts["Video"]
                )
                minimum_files = (
                    valid_counts["Picture"] + valid_counts["Video"] + minimum_standalone
                )
                maximum_files = (
                    valid_counts["Picture"]
                    + valid_counts["Video"]
                    + min(3, valid_counts["Audio"])
                )
                if minimum_files > 12:
                    add(
                        issues,
                        "ERROR",
                        "mixed-media-count",
                        f"At least {minimum_files} mixed files are implied, exceeding the official limit of 12.",
                    )
                elif maximum_files > 12:
                    add(
                        issues,
                        "WARN",
                        "standalone-audio-count-needed",
                        "Pass `--standalone-audios` to distinguish embedded video soundtracks "
                        "from separate files and verify the 12-file limit.",
                    )

        audio_present = (
            (audios is not None and audios > 0)
            or (standalone_audios is not None and standalone_audios > 0)
            or bool(used["Audio"])
        )
        visual_present = (
            (pictures is not None and pictures > 0)
            or (videos is not None and videos > 0)
            or bool(used["Picture"] or used["Video"])
        )
        if audio_present and not visual_present:
            add(
                issues,
                "ERROR",
                "audio-needs-visual",
                "Official Ref2VA does not allow audio as the sole media input.",
            )

        for kind, count in valid_counts.items():
            ordinals = used[kind]
            for number in sorted(ordinals):
                if number > count:
                    add(
                        issues,
                        "ERROR",
                        "unconnected-media-tag",
                        f"<{kind} {number}> is not connected; {kind.lower()} count is {count}.",
                    )
            # Counts are already bounded by the tiny provider limits, so this
            # diagnostic cannot allocate an unbounded range.
            unreferenced = [number for number in range(1, count + 1) if number not in ordinals]
            if unreferenced:
                formatted = ", ".join(f"<{kind} {number}>" for number in unreferenced)
                add(
                    issues,
                    "WARN",
                    "unreferenced-media",
                    f"Connected media should each receive one explicit job; not referenced: {formatted}.",
                )

    render_duration = (
        effective_raw_frames / 24 if effective_raw_frames is not None else None
    )
    parsed_time_ranges: list[tuple[float, float, str]] = []
    for start_text, end_text in COMFY_TIME_RANGE_RE.findall(text):
        start, end = float(start_text), float(end_text)
        parsed_time_ranges.append((start, end, f"[{start_text}s-{end_text}s]"))
    for clock_match in COMFY_CLOCK_RANGE_RE.finditer(text):
        start_clock, end_clock = clock_match.groups()
        parsed_time_ranges.append(
            (
                parse_clock_time(start_clock, issues),
                parse_clock_time(end_clock, issues),
                clock_match.group(0),
            )
        )

    for start, end, range_label in parsed_time_ranges:
        if start < 0 or end < 0:
            add(
                issues,
                "ERROR",
                "time-range-negative",
                f"Time range `{range_label}` cannot begin before the raw render clock.",
            )
        if end <= start:
            add(issues, "ERROR", "time-range", f"Invalid time range `{range_label}`.")
        if render_duration is not None and end > render_duration + 1e-9:
            add(
                issues,
                "ERROR",
                "time-outside-duration",
                f"Time range ending at {end:.3f}s exceeds the aligned raw render duration "
                f"{render_duration:.3f}s.",
            )

    if trim_frames is not None or tail_trim_frames is not None:
        leading_trim = 0 if trim_frames is None else trim_frames
        trailing_trim = 0 if tail_trim_frames is None else tail_trim_frames
        if leading_trim < 0 or trailing_trim < 0:
            add(issues, "ERROR", "trim-frames", "Leading and trailing trim frames cannot be negative.")
        elif effective_raw_frames is None:
            add(
                issues,
                "WARN",
                "trim-duration-needed",
                "Pass requested `--duration` or explicit `--raw-frames` to calculate the delivery window.",
            )
        else:
            if leading_trim + trailing_trim >= effective_raw_frames:
                add(
                    issues,
                    "ERROR",
                    "trim-frames",
                    f"Combined trim of {leading_trim + trailing_trim} frames leaves nothing "
                    f"from a {effective_raw_frames}-frame render.",
                )
            else:
                delivered_frames = effective_raw_frames - leading_trim - trailing_trim
                add(
                    issues,
                    "INFO",
                    "delivery-window",
                    f"Raw {effective_raw_frames} frames minus {leading_trim} leading and "
                    f"{trailing_trim} trailing trim frames yields "
                    f"{delivered_frames} frames ({delivered_frames / 24:.3f}s); "
                    f"delivery timestamps equal raw timestamps minus {leading_trim / 24:.3f}s.",
                )
                if trailing_trim:
                    retained_raw_endpoint = (effective_raw_frames - trailing_trim) / 24
                    for start, end, range_label in parsed_time_ranges:
                        if end <= retained_raw_endpoint + 1e-9:
                            continue
                        scope = "entirely inside" if start >= retained_raw_endpoint - 1e-9 else "partly inside"
                        add(
                            issues,
                            "WARN",
                            "tail-crop-time-range",
                            f"`{range_label}` lies {scope} the trailing crop, whose "
                            f"retained raw-clock endpoint is {retained_raw_endpoint:.3f}s. "
                            "Keep required beats and payoffs before that endpoint.",
                        )


def lint_hosted_prompt(
    text: str,
    duration: float | None,
    mode: str,
    issues: list[Issue],
) -> None:
    """Validate portable properties of a hosted freeform prompt."""
    if MEDIAISH_TAG_RE.search(text) or DANGLING_MEDIA_TAG_RE.search(text):
        add(
            issues,
            "ERROR",
            "profile-media-handle",
            "Angle-bracket Subject/Picture/Video/Audio labels belong to structured or "
            "native-ComfyUI profiles. Use the hosted surface's documented upload handles.",
        )

    for match in HOSTED_MEDIAISH_HANDLE_RE.finditer(text):
        if HOSTED_MEDIA_HANDLE_RE.fullmatch(match.group(0)) is None:
            add(
                issues,
                "ERROR",
                "hosted-handle-format",
                f"Malformed hosted handle `{match.group(0)}`; use `@Image N`, `@Video N`, "
                "or `@Audio N` with one space before the ordinal.",
            )

    handle_map: dict[str, set[int]] = {"image": set(), "video": set(), "audio": set()}
    for kind, number in HOSTED_MEDIA_HANDLE_RE.findall(text):
        parsed = int(number)
        if parsed < 1:
            add(
                issues,
                "ERROR",
                "hosted-handle-ordinal",
                f"Hosted upload handles are 1-based; use `@{kind.title()} 1` or higher, "
                f"not `@{kind.title()} {number}`.",
            )
            continue
        handle_map[kind.lower()].add(parsed)
    has_handles = any(handle_map.values())
    if mode == "t2va" and has_handles:
        add(
            issues,
            "ERROR",
            "handle-mode",
            "Hosted T2VA is text-only; select the endpoint or Ref2VA mode that matches the "
            "referenced uploads.",
        )
    elif mode in {"i2va", "l2va"} and has_handles:
        if len(handle_map["image"]) != 1 or handle_map["video"] or handle_map["audio"]:
            add(
                issues,
                "ERROR",
                "handle-mode",
                f"Hosted {mode.upper()} requires one image endpoint and no video/audio "
                "reference handles.",
            )
    elif mode == "fl2va" and has_handles:
        if len(handle_map["image"]) != 2 or handle_map["video"] or handle_map["audio"]:
            add(
                issues,
                "ERROR",
                "handle-mode",
                "Hosted FL2VA requires two distinct image endpoints and no video/audio "
                "reference handles.",
            )
    elif mode == "ref2va" and handle_map["audio"] and not (
        handle_map["image"] or handle_map["video"]
    ):
        add(
            issues,
            "ERROR",
            "audio-needs-visual",
            "Hosted Ref2VA audio must be paired with at least one image or video reference.",
        )

    if HOSTED_NO_MUSIC_RE.search(text):
        positive_music_text = HOSTED_NO_MUSIC_RE.sub("", text)
        positive_music_text = HOSTED_NEGATED_MUSIC_REQUEST_RE.sub("", positive_music_text)
        if HOSTED_POSITIVE_MUSIC_RE.search(positive_music_text):
            add(
                issues,
                "WARN",
                "music-conflict",
                "The hosted prompt appears to prohibit background music and request a score or "
                "soundtrack. Resolve the conflict or scope the two rules to different scenes.",
            )

    parameter_headers = list(re.finditer(r"(?m)^PARAMETERS\s*$", text))
    if len(parameter_headers) > 1:
        add(
            issues,
            "ERROR",
            "parameter-header",
            "A hosted prompt may contain only one `PARAMETERS` block.",
        )
    if parameter_headers:
        header = parameter_headers[0]
        block_start = header.end()
        block_end = len(text)
        blank = re.search(r"\n[ \t]*\n", text[block_start:])
        if blank:
            block_end = block_start + blank.start()
        block = text[block_start:block_end]
        declarations: list[tuple[str, str]] = []
        for line in block.splitlines():
            if not line.strip():
                continue
            match = PARAMETER_DECL_RE.fullmatch(line.strip())
            if not match:
                add(
                    issues,
                    "ERROR",
                    "parameter-declaration",
                    "Each line in `PARAMETERS` must use `NAME = \"literal value\"`.",
                )
                continue
            declarations.append((match.group(1), match.group(2)))

        if not declarations:
            add(
                issues,
                "ERROR",
                "parameter-declaration",
                "The `PARAMETERS` block contains no valid declarations.",
            )

        names = [name for name, _ in declarations]
        for name in sorted({name for name in names if names.count(name) > 1}):
            add(
                issues,
                "ERROR",
                "parameter-duplicate",
                f"Parameter `{name}` is declared more than once.",
            )
        body_without_declarations = text[:header.start()] + text[block_end:]
        for name, value in declarations:
            if not value.strip():
                add(
                    issues,
                    "ERROR",
                    "parameter-empty",
                    f"Parameter `{name}` has an empty literal value.",
                )
            if not re.search(rf"\b{re.escape(name)}\b", body_without_declarations):
                add(
                    issues,
                    "WARN",
                    "parameter-unused",
                    f"Parameter `{name}` is declared but never used outside the parameter block.",
                )

    decimal_headers = [
        match
        for match in HOSTED_TIMED_HEADER_RE.finditer(text)
        if not source_section_active(text, match.start())
    ]
    clock_line_headers = [
        match
        for match in HOSTED_CLOCK_TIMED_HEADER_RE.finditer(text)
        if not source_section_active(text, match.start())
        and not has_unquoted_clock_range(match.group(5) or "")
    ]
    excluded_clock_spans = [
        (match.start(), match.end()) for match in clock_line_headers
    ]
    inline_clock_headers = select_inline_clock_headers(
        text,
        duration,
        excluded_clock_spans,
    )
    headers: list[tuple[re.Match[str], bool]] = [
        (match, False) for match in decimal_headers
    ]
    headers.extend((match, True) for match in clock_line_headers)
    headers.extend((match, True) for match in inline_clock_headers)
    headers.sort(key=lambda item: item[0].start())
    for cut_line in HOSTED_CUT_LIKE_LINE_RE.finditer(text):
        stripped = cut_line.group(0).strip()
        if (
            HOSTED_TIMED_HEADER_RE.fullmatch(stripped) is None
            and HOSTED_CLOCK_TIMED_HEADER_RE.fullmatch(stripped) is None
        ):
            add(
                issues,
                "ERROR",
                "cut-header-format",
                f"Malformed hosted CUT header `{cut_line.group(0).strip()}`.",
            )

    declared_counts = [ordinal(value) for value in HOSTED_CUT_COUNT_RE.findall(text)]
    if len(set(declared_counts)) > 1:
        add(
            issues,
            "ERROR",
            "cut-count-declaration",
            "The prompt contains conflicting exact cut-count declarations.",
        )
    elif declared_counts and declared_counts[0] != len(headers):
        add(
            issues,
            "ERROR",
            "cut-count",
            f"The prompt declares exactly {declared_counts[0]} cuts but contains "
            f"{len(headers)} valid timed headers.",
        )

    numbered_cuts = sum(match.group(1) is not None for match, _ in headers)
    numbered_shots = len(HOSTED_SHOT_HEADER_RE.findall(text))
    if CONTINUOUS_TOPOLOGY_RE.search(text) and (numbered_cuts >= 2 or numbered_shots >= 2):
        add(
            issues,
            "ERROR",
            "topology-conflict",
            "A hosted prompt declares one continuous take/no cuts but also contains multiple "
            "numbered CUT or Shot blocks. Use unnumbered timed phases for continuous progression "
            "or remove the continuous-take rule.",
        )

    if not headers:
        return

    ranges: list[tuple[float, float, str]] = []
    numbered = [match.group(1) for match, _ in headers]
    for index, (match, uses_clock) in enumerate(headers):
        if uses_clock:
            start = parse_clock_time(match.group(2), issues)
            end = parse_clock_time(match.group(3), issues)
        else:
            start = float(match.group(2))
            end = float(match.group(3))
        separator = match.group(4)
        inline_content = (match.group(5) or "").strip()
        range_label = match.group(0).strip()
        ranges.append((start, end, range_label))

        if start < 0 or end < 0:
            add(
                issues,
                "ERROR",
                "time-range-negative",
                f"Time range `{range_label}` cannot begin before 0 seconds.",
            )
        if end <= start:
            add(
                issues,
                "ERROR",
                "time-range",
                f"Invalid time range `{range_label}`.",
            )
        if duration is not None and end > duration + 1e-9:
            add(
                issues,
                "ERROR",
                "time-outside-duration",
                f"Time range ending at {end:.3f}s exceeds the requested duration {duration:.3f}s.",
            )
        next_start = headers[index + 1][0].start() if index + 1 < len(headers) else len(text)
        following_body = text[match.end():next_start].strip()
        has_inline_body = has_substantive_timed_body(inline_content) and (
            uses_clock or separator == ":"
        )
        if not has_inline_body and not has_substantive_timed_body(following_body):
            add(
                issues,
                "ERROR",
                "timed-header-body",
                f"Timed header `{range_label}` has no beat description.",
            )

    tolerance = 1e-6
    for (_, previous_end, previous_label), (start, _, current_label) in zip(
        ranges, ranges[1:]
    ):
        if start > previous_end + tolerance:
            add(
                issues,
                "ERROR",
                "timeline-gap",
                f"Timeline gap between `{previous_label}` and `{current_label}`.",
            )
        elif start < previous_end - tolerance:
            add(
                issues,
                "ERROR",
                "timeline-overlap",
                f"Timeline overlap between `{previous_label}` and `{current_label}`.",
            )

    if ranges[0][0] > tolerance:
        add(
            issues,
            "WARN",
            "timeline-start",
            f"The first timed beat begins at {ranges[0][0]:.3f}s rather than 0.000s.",
        )
    if duration is not None and ranges[-1][1] < duration - tolerance:
        add(
            issues,
            "WARN",
            "timeline-end",
            f"The final timed beat ends at {ranges[-1][1]:.3f}s before the requested "
            f"duration {duration:.3f}s.",
        )

    has_numbered = any(number is not None for number in numbered)
    if has_numbered and not all(number is not None for number in numbered):
        add(
            issues,
            "ERROR",
            "cut-numbering",
            "Use numbered `CUT` headers for every timed beat or for none of them.",
        )
    elif has_numbered:
        cut_numbers = [ordinal(number) for number in numbered if number is not None]
        if any(number != index for index, number in enumerate(cut_numbers, start=1)):
            add(
                issues,
                "ERROR",
                "cut-sequence",
                "Hosted `CUT` headers must appear once in sequence starting at 1; found "
                f"{preview_numbers(cut_numbers)}.",
            )


def lint_ref2va(text: str, sections: dict[str, str], issues: list[Issue]) -> None:
    if not text.startswith("subject_definitions:"):
        add(issues, "ERROR", "leading-content", "Ref2VA must begin with `subject_definitions:`.")

    definitions = sections.get("subject_definitions", "")
    def_matches = list(
        re.finditer(r"(?m)^<(Subject|Picture|Video|Audio) (\d+)>([^\n]*)$", definitions)
    )
    defined = [
        f"<{match.group(1)} {match.group(2)}>" for match in def_matches
    ]
    if not defined:
        add(issues, "ERROR", "missing-definitions", "No standalone reference definitions found.")

    for match in def_matches:
        if not re.search(r"\w", match.group(3)):
            add(
                issues,
                "ERROR",
                "empty-definition",
                f"<{match.group(1)} {match.group(2)}> has no definition text.",
            )

    duplicates = sorted({label for label in defined if defined.count(label) > 1})
    for label in duplicates:
        add(issues, "ERROR", "duplicate-label", f"{label} is defined more than once.")

    defined_set = set(defined)
    all_definition_refs = [
        (kind, ordinal(number)) for kind, number in REF_LABEL_RE.findall(definitions)
    ]
    # Picture/Video labels may appear only as inline provenance. Subject and
    # Audio labels always denote tracked items and therefore require their own
    # definition and retention row.
    for kind, number in REF_LABEL_RE.findall(definitions):
        label = f"<{kind} {number}>"
        if kind in {"Subject", "Audio"} and label not in defined_set:
            add(
                issues,
                "ERROR",
                "missing-definition",
                f"{label} is cited inline but requires a standalone definition.",
            )

    ordinals_by_kind: dict[str, list[int]] = {}
    for kind in ("Subject", "Picture", "Video", "Audio"):
        numbers = sorted({number for label_kind, number in all_definition_refs if label_kind == kind})
        ordinals_by_kind[kind] = numbers
        if numbers and not is_contiguous_from_one(numbers):
            add(
                issues,
                "ERROR",
                "label-gap",
                f"{kind} labels must be contiguous from 1; found {preview_numbers(numbers)}.",
            )

    media_limits = {"Picture": 9, "Video": 3, "Audio": 6}
    for kind, limit in media_limits.items():
        numbers = ordinals_by_kind[kind]
        if numbers and (len(numbers) > limit or numbers[-1] > limit):
            add(
                issues,
                "ERROR",
                "media-count",
                f"Structured Ref2VA allows at most {limit} {kind.lower()} ordinals; "
                f"found {preview_numbers(numbers)}.",
            )

    picture_count = len(ordinals_by_kind["Picture"])
    video_count = len(ordinals_by_kind["Video"])
    audio_count = len(ordinals_by_kind["Audio"])
    if audio_count and picture_count + video_count == 0:
        add(
            issues,
            "ERROR",
            "audio-needs-visual",
            "Official Ref2VA does not allow audio as the sole media input.",
        )
    # At most three Audio ordinals may be standalone; up to three more can be
    # soundtracks on reference videos. This is a conservative lower bound on
    # the actual mixed-file count when provenance is not written explicitly.
    minimum_video_files = max(video_count, min(audio_count, 3))
    minimum_standalone_audios = max(0, audio_count - 3)
    minimum_files = picture_count + minimum_video_files + minimum_standalone_audios
    if minimum_files > 12:
        add(
            issues,
            "ERROR",
            "mixed-media-count",
            f"The declared labels imply at least {minimum_files} mixed files, exceeding 12.",
        )

    later_text = "\n".join(
        sections.get(field, "") for field in REF_FIELDS if field != "subject_definitions"
    )
    used_later = {f"<{kind} {number}>" for kind, number in REF_LABEL_RE.findall(later_text)}
    for label in sorted(used_later - defined_set):
        add(
            issues,
            "ERROR",
            "undefined-label",
            f"{label} is used after `subject_definitions` but has no standalone definition.",
        )

    retention = sections.get("retention_analysis", "")
    retention_rows: dict[str, list[str]] = {}
    for line in retention.splitlines():
        row_match = re.match(
            r"^(<(?:Subject|Picture|Video|Audio) \d+>).*?:\s*([a-z_]+)\b",
            line.strip(),
        )
        if row_match:
            retention_rows.setdefault(row_match.group(1), []).append(row_match.group(2))

    for label in defined:
        rows = retention_rows.get(label, [])
        if not rows:
            add(issues, "ERROR", "missing-retention", f"{label} has no retention row.")
        elif len(rows) > 1:
            add(issues, "ERROR", "duplicate-retention", f"{label} has multiple retention rows.")
        else:
            marker = rows[0]
            allowed = AUDIO_RETENTION if label.startswith("<Audio") else VISUAL_RETENTION
            if marker not in allowed:
                add(
                    issues,
                    "ERROR",
                    "retention-marker",
                    f"{label} uses invalid relationship marker `{marker}`.",
                )

    for label in sorted(set(retention_rows) - defined_set):
        add(issues, "ERROR", "orphan-retention", f"{label} has a retention row but no definition.")

    summary = sections.get("summary", "")
    task_match = re.match(r"^\[([^\]]+)\]\s+", summary)
    if not task_match:
        add(issues, "ERROR", "summary-prefix", "Summary must begin with a task-type prefix.")
    else:
        tasks = [part.strip() for part in task_match.group(1).split(" + ")]
        if any(task not in TASK_TYPES for task in tasks):
            invalid = [task for task in tasks if task not in TASK_TYPES]
            add(
                issues,
                "ERROR",
                "task-type",
                "Invalid summary task type(s): " + ", ".join(invalid),
            )
        if len(tasks) != len(set(tasks)):
            add(issues, "ERROR", "task-duplicate", "Do not repeat summary task types.")
        if "video editing" in tasks and not re.match(
            r"^\[[^\]]+\]\s+The target video is an edited version of <Video 1>\.", summary
        ):
            add(
                issues,
                "ERROR",
                "editing-summary",
                "A video-editing summary must begin with the provider's `<Video 1>` sentence.",
            )

        audio_markers = {
            marker
            for label, markers in retention_rows.items()
            if label.startswith("<Audio")
            for marker in markers
        }
        has_audio_copy = bool(audio_markers & {"fully_copy", "partially_copy"})
        has_audio_reference = bool(audio_markers & {"reference", "weak_reference"})
        if "audio reuse" in tasks and not has_audio_copy:
            add(
                issues,
                "ERROR",
                "audio-task-marker",
                "`audio reuse` requires an `<Audio N>` retention row using `fully_copy` or `partially_copy`.",
            )
        if has_audio_copy and "audio reuse" not in tasks:
            add(
                issues,
                "ERROR",
                "audio-marker-task",
                "A copied `<Audio N>` signal requires `audio reuse` in the summary task types.",
            )
        if "audio reference" in tasks and not has_audio_reference:
            add(
                issues,
                "ERROR",
                "audio-task-marker",
                "`audio reference` requires an `<Audio N>` retention row using `reference` or `weak_reference`.",
            )
        if has_audio_reference and "audio reference" not in tasks:
            add(
                issues,
                "ERROR",
                "audio-marker-task",
                "A referenced `<Audio N>` signal requires `audio reference` in the summary task types.",
            )

        has_video_label = any(label.startswith("<Video") for label in defined_set)
        if ("video editing" in tasks or "video continuation" in tasks) and not has_video_label:
            add(
                issues,
                "ERROR",
                "video-task-label",
                "Video editing or continuation requires a standalone `<Video N>` definition.",
            )
        has_picture_label = any(label.startswith("<Picture") for label in defined_set)
        if "keyframe completion" in tasks and not has_picture_label:
            add(
                issues,
                "ERROR",
                "keyframe-task-label",
                "`keyframe completion` requires a standalone `<Picture N>` definition.",
            )

    detailed = sections.get("detailed_description", "")
    first_shot = detailed.find("[Shot 1]")
    if first_shot <= 0 or not detailed[:first_shot].strip():
        add(
            issues,
            "ERROR",
            "ref-style-opening",
            "Ref2VA `detailed_description` needs one or two style sentences before `[Shot 1]`.",
        )

    is_edit = bool(task_match and "video editing" in task_match.group(1).split(" + "))
    word_count = len(re.findall(r"\b[\w'-]+\b", detailed))
    if not is_edit and not 350 <= word_count <= 500:
        add(
            issues,
            "WARN",
            "description-length",
            f"Generation-task `detailed_description` is {word_count} words; the guide normally uses 350–500.",
        )


def lint_prompt(
    text: str,
    mode: str = "auto",
    duration: float | None = None,
    max_chars: int = 7000,
    profile: str = "structured",
    pictures: int | None = None,
    videos: int | None = None,
    audios: int | None = None,
    standalone_audios: int | None = None,
    raw_frames: int | None = None,
    trim_frames: int | None = None,
    tail_trim_frames: int | None = None,
) -> tuple[str, list[Issue]]:
    issues: list[Issue] = []
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")

    if not text.strip():
        return mode, [Issue("ERROR", "empty", "Prompt is empty.")]
    if len(text) > max_chars:
        add(
            issues,
            "WARN",
            "character-limit",
            f"Prompt is {len(text)} characters; the audited hosted-surface cap is {max_chars}. "
            "Verify and enforce the actual target-surface limit.",
        )
    if "```" in text:
        add(issues, "ERROR", "markdown-fence", "Remove Markdown fences from the prompt file.")
    if duration is not None:
        if not math.isfinite(duration):
            add(issues, "ERROR", "duration-number", "Duration must be a finite number.")
            duration = None
        elif not 4 <= duration <= 15:
            add(issues, "ERROR", "duration-range", "H3 duration must be between 4 and 15 seconds.")
            duration = None
        elif profile == "structured" and not float(duration).is_integer():
            add(
                issues,
                "WARN",
                "duration-increment",
                "The audited hosted product uses whole-second increments; verify the target "
                "structured API/local surface before using a fractional duration.",
            )
        elif profile == "comfyui":
            aligned_frames = aligned_comfyui_frames(duration)
            aligned_duration = aligned_frames / 24
            if abs(aligned_duration - duration) > 1e-9:
                add(
                    issues,
                    "WARN",
                    "runtime-duration-snap",
                    f"Native ComfyUI snaps {duration:.3f}s to {aligned_frames} frames "
                    f"({aligned_duration:.3f}s) on its 17k+5 grid.",
                )

    lint_rhythm_and_pose_contracts(text, duration, issues)

    placeholder_patterns = (
        r"\bS\.SS-second\b",
        r"\bShot N\b",
        r"<Subject N>",
        r"<Picture N>",
        r"<Video N>",
        r"<Audio N>",
        r"(?i)@(?:Image|Video|Audio)\s+N\b",
    )
    for pattern in placeholder_patterns:
        if re.search(pattern, text):
            add(issues, "ERROR", "placeholder", f"Unresolved template placeholder matches `{pattern}`.")

    if profile == "hosted":
        if mode == "auto":
            hosted_kinds = {
                kind.lower() for kind, _ in HOSTED_MEDIA_HANDLE_RE.findall(text)
            }
            if hosted_kinds & {"video", "audio"}:
                selected = "ref2va"
            elif "image" in hosted_kinds:
                selected = "ref2va"
                add(
                    issues,
                    "ERROR",
                    "mode-needed",
                    "Image-only hosted prompts are ambiguous among I2VA, L2VA, FL2VA, and "
                    "Ref2VA; pass an explicit `--mode` after assigning each image role.",
                )
            else:
                selected = "t2va"
        else:
            selected = mode
        if raw_frames is not None or trim_frames is not None or tail_trim_frames is not None:
            add(
                issues,
                "ERROR",
                "profile-option",
                "Raw/trim-frame options are native-ComfyUI runtime options; use `--profile comfyui`.",
            )
        if any(value is not None for value in (pictures, videos, audios, standalone_audios)):
            add(
                issues,
                "ERROR",
                "profile-option",
                "Connected-media count options require native-ComfyUI graph ordinals; "
                "hosted upload handles are surface-specific.",
            )
        lint_hosted_prompt(text, duration, selected, issues)
        return selected, issues

    if HOSTED_MEDIAISH_HANDLE_RE.search(text):
        add(
            issues,
            "ERROR",
            "profile-media-handle",
            "`@Image N`, `@Video N`, and `@Audio N` are hosted-surface handles. Use the "
            "structured or native-ComfyUI angle-bracket labels required by this profile.",
        )

    lint_media_tag_syntax(text, issues)

    if profile == "comfyui":
        if mode == "auto":
            labels = REF_LABEL_RE.findall(text)
            kinds = {kind for kind, _ in labels}
            ref_evidence = bool(kinds & {"Subject", "Video", "Audio"}) or any(
                value is not None and value > 0
                for value in (videos, audios, standalone_audios)
            )
            picture_evidence = "Picture" in kinds or (
                pictures is not None and pictures > 0
            )
            if ref_evidence:
                inferred = "ref2va"
            elif picture_evidence:
                inferred = "ref2va"
                add(
                    issues,
                    "ERROR",
                    "mode-needed",
                    "Picture-only native prompts are ambiguous among I2VA, L2VA, FL2VA, "
                    "and Ref2VA; pass an explicit `--mode`.",
                )
            else:
                inferred = "t2va"
        else:
            inferred = mode
        lint_comfyui_prompt(
            text,
            inferred,
            duration,
            pictures,
            videos,
            audios,
            standalone_audios,
            raw_frames,
            trim_frames,
            tail_trim_frames,
            issues,
        )
        return inferred, issues

    if raw_frames is not None or trim_frames is not None or tail_trim_frames is not None:
        add(
            issues,
            "ERROR",
            "profile-option",
            "Raw/trim-frame options are native-ComfyUI runtime options; use `--profile comfyui`.",
        )
    if any(value is not None for value in (pictures, videos, audios, standalone_audios)):
        add(
            issues,
            "ERROR",
            "profile-option",
            "Connected-media count options are native-ComfyUI graph checks; use `--profile comfyui`.",
        )

    inferred = infer_mode(text)
    selected = inferred if mode == "auto" else mode
    if mode != "auto" and mode != inferred:
        add(
            issues,
            "ERROR",
            "mode-mismatch",
            f"Selected mode is {mode.upper()}, but the prompt structure looks like {inferred.upper()}.",
        )

    fields = REF_FIELDS if selected == "ref2va" else BASE_FIELDS
    lint_top_level_fields(text, fields, issues)
    sections = find_sections(text, fields, issues)
    timeline_field = "detailed_description" if selected == "ref2va" else "integrated_multimodal_description"
    final_shot = lint_shots(sections.get(timeline_field, ""), duration, issues) if sections else 1
    if sections:
        lint_structured_semantics(sections, timeline_field, issues)

    if selected == "ref2va":
        if sections:
            lint_ref2va(text, sections, issues)
    else:
        lint_alignment(text, selected, duration, final_shot, issues)
        lint_base_reference_labels(text, selected, issues)

    if sections:
        speaker_events = lint_dialogue(text, sections, timeline_field, selected, issues)
        lint_speakers(text, sections, speaker_events, issues)

    return selected, issues


def run_self_test() -> None:
    examples: list[tuple[str, str, float]] = [
        (
            "t2va",
            "integrated_multimodal_description: [Shot 1] Live-action, cinematic, a lamp switches on.\n\n"
            "overall_soundscape: Quiet room tone and a small switch click.\n\n"
            "non_diegetic_music: N/A\n",
            4.0,
        ),
        (
            "i2va",
            I2VA_ALIGNMENT
            + "\n\nintegrated_multimodal_description: [Shot 1] Live-action, cinematic, the subject in <Picture 1> turns.\n\n"
            "overall_soundscape: Soft room tone.\n\nnon_diegetic_music: N/A\n",
            4.0,
        ),
        (
            "fl2va",
            expected_alignment("fl2va", 8.0, 1)
            + "\n\nintegrated_multimodal_description: [Shot 1] Live-action, cinematic, the pose in Picture 1 develops continuously and lands on Picture 2.\n\n"
            "overall_soundscape: Soft wind.\n\nnon_diegetic_music: N/A\n",
            8.0,
        ),
        (
            "l2va",
            expected_alignment("l2va", 6.0, 1)
            + "\n\nintegrated_multimodal_description: [Shot 1] Live-action, cinematic, fragments settle into <Picture 1>.\n\n"
            "overall_soundscape: A fading impact.\n\nnon_diegetic_music: N/A\n",
            6.0,
        ),
        (
            "ref2va",
            "subject_definitions:\n<Subject 1> is the red ceramic cup in <Picture 1>.\n\n"
            "summary:\n[reference generation] The target video shows <Subject 1> rotating on a table.\n\n"
            "retention_analysis:\n<Subject 1> (appears in [Shot 1]): fully_preserved - its red glaze and shape remain unchanged.\n\n"
            "detailed_description:\nThe target video uses a clean live-action product style.\n"
            "[Shot 1] A red ceramic cup, <Subject 1>, rotates slowly on a table under soft light.\n\n"
            "overall_soundscape:\nQuiet studio room tone.\n\nnon_diegetic_music:\nN/A\n",
            4.0,
        ),
    ]

    for mode, text, duration in examples:
        selected, issues = lint_prompt(text, mode=mode, duration=duration)
        errors = [issue for issue in issues if issue.level == "ERROR"]
        if selected != mode or errors:
            raise AssertionError(f"Self-test failed for {mode}: {errors}")

    invalid = (
        "integrated_multimodal_description: [Shot 1] Live-action. "
        "[Shot 2] At 00:05.000, the camera cuts.\n\n"
        "overall_soundscape: Room tone.\n\nnon_diegetic_music: N/A\n"
    )
    _, issues = lint_prompt(invalid, mode="t2va", duration=5.0)
    if not any(issue.code == "cut-outside-duration" for issue in issues):
        raise AssertionError("Self-test did not catch an out-of-range cut.")

    inconsistent_audio = (
        "subject_definitions:\n<Audio 1> is a copied source track.\n\n"
        "summary:\n[audio reference] The target video follows <Audio 1>.\n\n"
        "retention_analysis:\n<Audio 1>: fully_copy - the complete track is copied.\n\n"
        "detailed_description:\nThe target video uses a clean live-action style.\n"
        "[Shot 1] A light pulses in synchronization with <Audio 1>.\n\n"
        "overall_soundscape:\nThe copied signal from <Audio 1> continues.\n\n"
        "non_diegetic_music:\nN/A\n"
    )
    _, issues = lint_prompt(inconsistent_audio, mode="ref2va", duration=4.0)
    if not any(issue.code in {"audio-task-marker", "audio-marker-task"} for issue in issues):
        raise AssertionError("Self-test did not catch inconsistent audio task/retention roles.")
    if not any(issue.code == "audio-needs-visual" for issue in issues):
        raise AssertionError("Self-test did not catch structured audio-only Ref2VA input.")

    valid_t2va = examples[0][1]
    _, issues = lint_prompt(valid_t2va, mode="t2va", duration=4.5)
    if not any(issue.code == "duration-increment" for issue in issues):
        raise AssertionError("Self-test did not catch a fractional duration.")

    extra_alignment_blank = I2VA_ALIGNMENT + "\n\n\n" + examples[1][1].split("\n\n", 1)[1]
    _, issues = lint_prompt(extra_alignment_blank, mode="i2va", duration=4.0)
    if not any(issue.code == "alignment-spacing" for issue in issues):
        raise AssertionError("Self-test did not catch extra alignment blank lines.")

    reordered_fields = (
        "overall_soundscape: Room tone.\n\n"
        "integrated_multimodal_description: [Shot 1] Live-action.\n\n"
        "non_diegetic_music: N/A\n"
    )
    _, issues = lint_prompt(reordered_fields, mode="t2va", duration=4.0)
    if not any(issue.code == "field-order" for issue in issues):
        raise AssertionError("Self-test did not catch reordered fields.")

    malformed_dialogue = valid_t2va.replace(
        "a lamp switches on.", "a speaker (S1) says <d>English Hello.</d>"
    )
    _, issues = lint_prompt(malformed_dialogue, mode="t2va", duration=4.0)
    if not any(issue.code == "dialogue-format" for issue in issues):
        raise AssertionError("Self-test did not catch malformed dialogue.")

    orphan_references = valid_t2va.replace(
        "a lamp switches on.",
        "<Subject 1> watches <Video 1> while <Audio 1> plays.",
    )
    _, issues = lint_prompt(orphan_references, mode="t2va", duration=4.0)
    if len([issue for issue in issues if issue.code == "reference-label"]) != 3:
        raise AssertionError("Self-test did not catch illegal base-mode reference labels.")

    unowned_dialogue = valid_t2va.replace(
        "a lamp switches on.",
        "a woman says: <d>[English] Hello.</d>",
    )
    _, issues = lint_prompt(unowned_dialogue, mode="t2va", duration=4.0)
    if not any(issue.code == "dialogue-source" for issue in issues):
        raise AssertionError("Self-test did not catch dialogue without a vocal source.")

    valid_unlisted_vocal_verb = valid_t2va.replace(
        "a lamp switches on.",
        "a woman (S1) murmurs, <d>[English] Hello.</d>",
    )
    _, issues = lint_prompt(valid_unlisted_vocal_verb, mode="t2va", duration=4.0)
    errors = [issue for issue in issues if issue.level == "ERROR"]
    if errors:
        raise AssertionError(f"Self-test rejected a valid vocal verb: {errors}")

    reversed_speakers = valid_t2va.replace(
        "a lamp switches on.",
        "a woman (S2) says: <d>[English] First.</d> "
        "A man (S1) replies: <d>[English] Second.</d>",
    )
    _, issues = lint_prompt(reversed_speakers, mode="t2va", duration=4.0)
    if not any(issue.code == "speaker-event-order" for issue in issues):
        raise AssertionError("Self-test did not catch reversed first-vocal-event numbering.")

    unknown_field = valid_t2va.replace(
        "overall_soundscape:",
        "unsupported_field: invented metadata\n\noverall_soundscape:",
    )
    _, issues = lint_prompt(unknown_field, mode="t2va", duration=4.0)
    if not any(issue.code == "unknown-field" for issue in issues):
        raise AssertionError("Self-test did not catch an invented top-level field.")

    direct_audio_dialogue = (
        "subject_definitions:\n<Subject 1> is the blue studio lamp in <Picture 1>.\n"
        "<Audio 1> is a directly reused complete soundtrack.\n\n"
        "summary:\n[reference generation + audio reuse] The target video shows <Subject 1> "
        "following the vocal cue in <Audio 1>.\n\n"
        "retention_analysis:\n<Subject 1> (appears in [Shot 1]): fully_preserved - its blue shade remains unchanged.\n"
        "<Audio 1>: fully_copy - the complete soundtrack is reused.\n\n"
        "detailed_description:\nThe target video uses a clean live-action style.\n"
        "[Shot 1] <Subject 1> pulses. When <Audio 1> reaches the phrase "
        "<d>[English] Begin now.</d>, the light turns blue.\n\n"
        "overall_soundscape:\nThe copied signal from <Audio 1> continues.\n\n"
        "non_diegetic_music:\nN/A\n"
    )
    _, issues = lint_prompt(direct_audio_dialogue, mode="ref2va", duration=4.0)
    errors = [issue for issue in issues if issue.level == "ERROR"]
    if errors:
        raise AssertionError(f"Self-test rejected valid direct-audio dialogue: {errors}")

    comfyui_ref = (
        "Use <Picture 1> for the character identity and <Video 1> for the camera move. "
        "[0s-2s] The character turns. [2s-5s] The camera follows as footsteps and wind continue."
    )
    _, issues = lint_prompt(
        comfyui_ref,
        mode="ref2va",
        duration=5.0,
        profile="comfyui",
        pictures=1,
        videos=1,
        audios=0,
    )
    errors = [issue for issue in issues if issue.level == "ERROR"]
    if errors:
        raise AssertionError(f"Self-test rejected valid native-ComfyUI Ref2VA: {errors}")

    _, issues = lint_prompt(
        "The transparent gaming mouse from <Picture 1> opens exactly on the connected first image.",
        mode="i2va",
        duration=5.0,
        profile="comfyui",
    )
    errors = [issue for issue in issues if issue.level == "ERROR"]
    if errors:
        raise AssertionError(f"Self-test rejected valid native-ComfyUI I2VA endpoint tag: {errors}")

    _, issues = lint_prompt(
        "Begin from <Picture 1>, move continuously, and land exactly on <Picture 2>.",
        mode="fl2va",
        duration=5.0,
        profile="comfyui",
    )
    errors = [issue for issue in issues if issue.level == "ERROR"]
    if errors:
        raise AssertionError(f"Self-test rejected valid native-ComfyUI FL2VA endpoint tags: {errors}")

    _, issues = lint_prompt(
        "A text-only shot incorrectly refers to <Picture 1>.",
        mode="t2va",
        duration=5.0,
        profile="comfyui",
    )
    if not any(issue.code == "reference-label" for issue in issues):
        raise AssertionError("Self-test did not catch an endpoint tag in native-ComfyUI T2VA.")

    malformed_comfyui_tag = comfyui_ref.replace("<Picture 1>", "<Image1>")
    _, issues = lint_prompt(
        malformed_comfyui_tag,
        mode="ref2va",
        duration=5.0,
        profile="comfyui",
        pictures=1,
        videos=1,
        audios=0,
    )
    if not any(issue.code == "media-tag-format" for issue in issues):
        raise AssertionError("Self-test did not catch a malformed native-ComfyUI media tag.")

    nested_dialogue = valid_t2va.replace(
        "a lamp switches on.",
        "a woman (S1) says <d>[English] outer <d>inner.</d></d>",
    )
    _, issues = lint_prompt(nested_dialogue, mode="t2va", duration=4.0)
    if not any(issue.code == "dialogue-tags" for issue in issues):
        raise AssertionError("Self-test did not catch nested dialogue tags.")

    _, issues = lint_prompt(
        valid_t2va.replace("[Shot 1]", "[Shot 01]"),
        mode="t2va",
        duration=4.0,
    )
    if not any(issue.code == "shot-format" for issue in issues):
        raise AssertionError("Self-test did not catch a zero-padded shot marker.")

    valid_abbreviation = valid_t2va.replace(
        "a lamp switches on.",
        "a woman (S1), a U.S. Army medic, says <d>[English] Stay with me.</d>",
    )
    _, issues = lint_prompt(valid_abbreviation, mode="t2va", duration=4.0)
    if any(issue.level == "ERROR" for issue in issues):
        raise AssertionError("Self-test split a dotted abbreviation as a sentence boundary.")

    visible_html = valid_t2va.replace(
        "a lamp switches on.",
        'a screen visibly prints "<video autoplay>".',
    )
    _, issues = lint_prompt(visible_html, mode="t2va", duration=4.0)
    if any(issue.code == "media-tag-format" for issue in issues):
        raise AssertionError("Self-test treated literal HTML as an H3 media tag.")

    _, issues = lint_prompt(
        "Use <Picture 1> as the opening frame.",
        profile="comfyui",
        duration=5.0,
    )
    if not any(issue.code == "mode-needed" for issue in issues):
        raise AssertionError("Self-test silently inferred a picture-only native mode.")

    _, issues = lint_prompt(
        "A text-only scene.",
        mode="t2va",
        profile="comfyui",
        duration=float("nan"),
    )
    if not any(issue.code == "duration-number" for issue in issues):
        raise AssertionError("Self-test did not reject a non-finite duration.")

    _, issues = lint_prompt(
        "[5.00s-5.10s] Hold the final state.",
        mode="t2va",
        profile="comfyui",
        duration=5.0,
    )
    if any(issue.code == "time-outside-duration" for issue in issues):
        raise AssertionError("Self-test compared raw timestamps to the unsnapped request clock.")

    _, issues = lint_prompt(
        "[6.20s-6.50s] Reveal the final state.",
        mode="t2va",
        profile="comfyui",
        duration=6.0,
        raw_frames=158,
        trim_frames=22,
        tail_trim_frames=16,
    )
    if not any(issue.code == "tail-crop-time-range" for issue in issues):
        raise AssertionError("Self-test did not flag a required beat inside the trailing crop.")

    _, issues = lint_prompt(
        "From 00:06.200 to 00:06.500, reveal the final state.",
        mode="t2va",
        profile="comfyui",
        duration=6.0,
        raw_frames=158,
        trim_frames=22,
        tail_trim_frames=16,
    )
    if not any(issue.code == "tail-crop-time-range" for issue in issues):
        raise AssertionError("Self-test missed a natural-clock range inside the trailing crop.")

    _, issues = lint_prompt(
        "[-1s-2s] Begin before the render.",
        mode="t2va",
        profile="comfyui",
        raw_frames=124,
    )
    if not any(issue.code == "time-range-negative" for issue in issues):
        raise AssertionError("Self-test did not reject a negative native time range.")

    _, issues = lint_prompt(
        "Use <Audio 1> for the soundtrack.",
        mode="ref2va",
        duration=5.0,
        profile="comfyui",
        pictures=0,
        videos=0,
        audios=1,
    )
    if not any(issue.code == "audio-needs-visual" for issue in issues):
        raise AssertionError("Self-test did not catch audio-only native-ComfyUI Ref2VA.")

    _, issues = lint_prompt(
        "[0s-1s] Carry the previous motion, then begin the new action.",
        mode="t2va",
        duration=5.0,
        profile="comfyui",
        trim_frames=22,
        tail_trim_frames=6,
    )
    if not any(
        issue.code == "delivery-window" and "96 frames (4.000s)" in issue.message
        for issue in issues
    ):
        raise AssertionError("Self-test did not calculate a trimmed native-ComfyUI delivery window.")

    twelve_file_map = " ".join(
        [f"<Picture {number}>" for number in range(1, 10)]
        + [f"<Video {number}>" for number in range(1, 4)]
        + [f"<Audio {number}>" for number in range(1, 4)]
    )
    _, issues = lint_prompt(
        f"Give every connected source one explicit job: {twelve_file_map}.",
        mode="ref2va",
        duration=5.0,
        profile="comfyui",
        pictures=9,
        videos=3,
        audios=3,
        standalone_audios=0,
    )
    errors = [issue for issue in issues if issue.level == "ERROR"]
    if errors:
        raise AssertionError(f"Self-test miscounted embedded video soundtracks as files: {errors}")

    fifteen_file_map = twelve_file_map + " " + " ".join(
        f"<Audio {number}>" for number in range(4, 7)
    )
    _, issues = lint_prompt(
        f"Use all connected sources: {fifteen_file_map}.",
        mode="ref2va",
        duration=5.0,
        profile="comfyui",
        pictures=9,
        videos=3,
        audios=6,
        standalone_audios=3,
    )
    if not any(issue.code == "mixed-media-count" for issue in issues):
        raise AssertionError("Self-test did not catch a 15-file native-ComfyUI map.")

    dense_ranges = (
        (0.00, 1.10),
        (1.10, 2.20),
        (2.20, 3.20),
        (3.20, 4.10),
        (4.10, 5.20),
        (5.20, 6.20),
        (6.20, 6.90),
        (6.90, 7.90),
        (7.90, 8.60),
        (8.60, 9.60),
        (9.60, 10.30),
        (10.30, 12.30),
        (12.30, 15.00),
    )
    hosted_dense = (
        'PARAMETERS\nSTATUS_TEXT = "[ACTIVE]"\n\n'
        "Create a 15-second trailer with exactly 13 distinct cuts. Use STATUS_TEXT exactly.\n\n"
        + "\n\n".join(
            f"CUT {index:02d} | {start:.2f}-{end:.2f}s | BEAT {index:02d}\n"
            f"Show one distinct composition and one readable state for beat {index}."
            for index, (start, end) in enumerate(dense_ranges, start=1)
        )
    )
    _, issues = lint_prompt(
        hosted_dense,
        mode="ref2va",
        duration=15.0,
        profile="hosted",
    )
    if issues:
        raise AssertionError(f"Self-test rejected a valid dense hosted CUT grid: {issues}")

    hosted_macro_stages = (
        "0.0–2.2s — CHARACTER SELECTION\nThe selection bracket locks onto the hero.\n\n"
        "2.2–5.0s — GEAR SELECTION\nThe bracket becomes the selected equipment tile.\n\n"
        "5.0–7.8s — WEAPON INSPECTION\nThe tile expands into a product view.\n\n"
        "7.8–10.4s — PHASE MODULES\nA leader line becomes the module path.\n\n"
        "10.4–13.0s — READY LOCK-IN\nThe modules compress into summary cards.\n\n"
        "13.0–15.0s — DEPLOY PAYOFF\nThe deploy control resolves and the final state holds."
    )
    _, issues = lint_prompt(
        hosted_macro_stages,
        mode="ref2va",
        duration=15.0,
        profile="hosted",
    )
    if issues:
        raise AssertionError(f"Self-test rejected valid hosted macro stages: {issues}")

    hosted_clock_ranges = (
        "0:00-0:01.5 A blank canvas remains visible, then the cursor begins one stroke.\n"
        "0:01.5-0:04.0: The same cursor completes the drawing and stops before the hold."
    )
    _, issues = lint_prompt(
        hosted_clock_ranges,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if issues:
        raise AssertionError(f"Self-test rejected valid hosted clock ranges: {issues}")

    hosted_inline_clock_ranges = (
        "One continuous process. 0:00-0:01.5 The blank state registers and the tool begins. "
        "0:01.5-0:04.0 The tool completes the result and the final state holds."
    )
    _, issues = lint_prompt(
        hosted_inline_clock_ranges,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if issues:
        raise AssertionError(f"Self-test rejected inline hosted clock ranges: {issues}")

    hosted_colon_clock_ranges = (
        "One continuous process. 0:00-0:01.5: The first action lands. "
        "0:01.5-0:03.0: The second action lands. "
        "0:03.0-0:04.0: The final action resolves."
    )
    _, issues = lint_prompt(
        hosted_colon_clock_ranges,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if issues:
        raise AssertionError(
            f"Self-test truncated fractional clocks before colon separators: {issues}"
        )

    hosted_clock_gap = (
        "0:00-0:01.5: Show the opening state.\n"
        "0:01.6-0:04.0: Resolve the final state."
    )
    _, issues = lint_prompt(
        hosted_clock_gap,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "timeline-gap" for issue in issues):
        raise AssertionError("Self-test missed a gap in hosted clock ranges.")

    hosted_inline_clock_gap = (
        "One continuous process. 0:00-0:01.5 The opening state registers. "
        "0:01.6-0:04.0 The final state lands."
    )
    _, issues = lint_prompt(
        hosted_inline_clock_gap,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "timeline-gap" for issue in issues):
        raise AssertionError("Self-test missed a gap in an inline natural-clock timeline.")

    hosted_inline_clock_overlap = (
        "One continuous process. 0:00-0:02.5 The opening action continues. "
        "0:02.0-0:04.0 The final action overlaps it."
    )
    _, issues = lint_prompt(
        hosted_inline_clock_overlap,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "timeline-overlap" for issue in issues):
        raise AssertionError("Self-test missed overlap in an inline natural-clock timeline.")

    hosted_clock_overrun = "0:00-0:04.1: The action exceeds the delivery window."
    _, issues = lint_prompt(
        hosted_clock_overrun,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "time-outside-duration" for issue in issues):
        raise AssertionError("Self-test missed a hosted clock range outside duration.")

    hosted_source_clock_then_target = (
        "@Video 1 supplies source interval 0:00-0:03.0. "
        "Target timeline: 0:00-0:01.5 The performer enters. "
        "0:01.5-0:04.0 The performer lands and holds."
    )
    _, issues = lint_prompt(
        hosted_source_clock_then_target,
        mode="ref2va",
        duration=4.0,
        profile="hosted",
    )
    if any(issue.code in {"timeline-overlap", "timeline-gap", "timeline-start"} for issue in issues):
        raise AssertionError(f"Self-test treated a source subclip as target timing: {issues}")

    for clock_copy in (
        'A literal door sign reads "OPEN 12:30-13:00".',
        "The source timecode is 00:00:00-00:00:03.",
        'Visible copy reads "0:00-0:04" without defining target timing.',
    ):
        _, issues = lint_prompt(
            clock_copy,
            mode="t2va",
            duration=4.0,
            profile="hosted",
        )
        if any(issue.code.startswith("timeline-") or issue.code.startswith("time-") for issue in issues):
            raise AssertionError(f"Self-test parsed visible/source clock copy as a timeline: {issues}")

    empty_clock_header = "0:00-0:04.0 —"
    _, issues = lint_prompt(
        empty_clock_header,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "timed-header-body" for issue in issues):
        raise AssertionError("Self-test accepted an empty natural-clock header.")

    empty_first_of_two_clock_headers = (
        "CUT 01 | 0:00-0:02.0 |\n"
        "CUT 02 | 0:02.0-0:04.0 | The ending state holds."
    )
    _, issues = lint_prompt(
        empty_first_of_two_clock_headers,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "timed-header-body" for issue in issues):
        raise AssertionError("Self-test let an empty clock header consume the next line.")

    inline_separator_only_body = "0:00-0:02.0 — 0:02.0-0:04.0 The ending lands."
    _, issues = lint_prompt(
        inline_separator_only_body,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "timed-header-body" for issue in issues):
        raise AssertionError("Self-test accepted separator-only inline beat text.")

    source_and_target_clock_blocks = (
        "REFERENCE ASSET INSTRUCTIONS\n"
        "@Video 1 source timing:\n"
        "0:00-0:02.0 The source performer enters.\n"
        "0:02.0-0:04.0 The source performer turns.\n\n"
        "TARGET TIMELINE\n"
        "0:00-0:01.5 The target performer enters.\n"
        "0:01.5-0:04.0 The target performer lands and holds."
    )
    _, issues = lint_prompt(
        source_and_target_clock_blocks,
        mode="ref2va",
        duration=4.0,
        profile="hosted",
    )
    if any(issue.code in {"timeline-overlap", "timeline-gap", "cut-count"} for issue in issues):
        raise AssertionError(f"Self-test merged source and target clock blocks: {issues}")

    official_hosted_three_part = (
        "Reference Asset Instructions\n"
        "@Image 1 defines the character identity and wardrobe.\n\n"
        "Core Concept\n"
        "Create a four-second animation with exactly 2 distinct cuts.\n\n"
        "Shot-by-Shot Description\n"
        "CUT 01 | 0:00-0:02.0 | The character enters frame.\n"
        "CUT 02 | 0:02.0-0:04.0 | The character turns and holds."
    )
    _, issues = lint_prompt(
        official_hosted_three_part,
        mode="ref2va",
        duration=4.0,
        profile="hosted",
    )
    if issues:
        raise AssertionError(f"Self-test over-filtered the official hosted structure: {issues}")

    official_hosted_target_gap = official_hosted_three_part.replace(
        "CUT 02 | 0:02.0-0:04.0", "CUT 02 | 0:02.1-0:04.0"
    )
    _, issues = lint_prompt(
        official_hosted_target_gap,
        mode="ref2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "timeline-gap" for issue in issues):
        raise AssertionError("Self-test hid a target gap after official reference instructions.")

    official_hosted_target_poses = (
        "Reference Asset Instructions\n"
        "@Image 1 defines the character identity.\n\n"
        "Core Concept\n"
        "Create exactly four numbered pose locks.\n\n"
        "Shot-by-Shot Description\n"
        "Pose 1 enters. Pose 2 turns. Pose 3 lowers. Pose 4 holds."
    )
    _, issues = lint_prompt(
        official_hosted_target_poses,
        mode="ref2va",
        duration=4.0,
        profile="hosted",
    )
    if any(issue.code.startswith("pose-") for issue in issues):
        raise AssertionError(f"Self-test hid target poses after reference instructions: {issues}")

    explicit_target_overrun = (
        "Target timeline: 0:00-0:02.0 The action begins. "
        "0:02.0-0:04.0 The payoff lands. 0:04.0-0:05.0 An extra action occurs."
    )
    _, issues = lint_prompt(
        explicit_target_overrun,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "time-outside-duration" for issue in issues):
        raise AssertionError("Self-test ignored an overrun inside an explicit target timeline.")

    explicit_target_far_gap = (
        "Target timeline: 0:00-0:01.0 The action begins. "
        "0:10.0-0:12.0 The next action arrives far too late."
    )
    _, issues = lint_prompt(
        explicit_target_far_gap,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "timeline-gap" for issue in issues):
        raise AssertionError("Self-test ignored a far gap inside an explicit target timeline.")

    counted_poses = (
        "Create exactly 4 numbered pose locks. Pose 1 settles, Pose 2 follows, "
        "Pose 3 follows, and Pose 4 holds."
    )
    _, issues = lint_prompt(
        counted_poses,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if any(issue.code.startswith("pose-") for issue in issues):
        raise AssertionError(f"Self-test rejected a valid pose-count contract: {issues}")

    word_counted_poses = (
        "The performer flows through ten precise poses. "
        + " ".join(f"Pose {index} locks." for index in range(1, 11))
    )
    _, issues = lint_prompt(
        word_counted_poses,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if any(issue.code.startswith("pose-") for issue in issues):
        raise AssertionError(f"Self-test rejected a word-form pose count: {issues}")

    punctuated_word_counted_poses = (
        "The performer flows through ten rapid, precise poses. "
        + " ".join(f"Pose {index} locks." for index in range(1, 11))
    )
    _, issues = lint_prompt(
        punctuated_word_counted_poses,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if any(issue.code.startswith("pose-") for issue in issues):
        raise AssertionError(f"Self-test rejected a punctuated pose count: {issues}")

    source_and_target_pose_counts = (
        "@Video 1 contains exactly ten poses; the target uses exactly four numbered pose "
        "locks. Pose 1 settles. Pose 2 follows. Pose 3 turns. Pose 4 holds."
    )
    _, issues = lint_prompt(
        source_and_target_pose_counts,
        mode="ref2va",
        duration=4.0,
        profile="hosted",
    )
    if any(issue.code in {"pose-count-declaration", "pose-count"} for issue in issues):
        raise AssertionError(f"Self-test confused source and target pose counts: {issues}")

    source_pose_labels_and_target_count = (
        "@Video 1 includes a sequence of exactly ten poses: Pose 1 through Pose 10; "
        "the target uses exactly four numbered pose locks. Pose 1 settles. Pose 2 follows. "
        "Pose 3 turns. Pose 4 holds."
    )
    _, issues = lint_prompt(
        source_pose_labels_and_target_count,
        mode="ref2va",
        duration=4.0,
        profile="hosted",
    )
    if any(issue.code in {"pose-sequence", "pose-count-declaration", "pose-count"} for issue in issues):
        raise AssertionError(f"Self-test counted source Pose labels as target locks: {issues}")

    rate_based_pose_wording = (
        "Use exactly one pose lock per beat. Pose 1 lands, then Pose 2 lands."
    )
    _, issues = lint_prompt(
        rate_based_pose_wording,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if any(issue.code == "pose-count" for issue in issues):
        raise AssertionError(f"Self-test treated a pose rate as a total count: {issues}")

    for rate_word in ("every", "each"):
        _, issues = lint_prompt(
            f"Use exactly one pose lock {rate_word} beat. Pose 1 lands, then Pose 2 lands.",
            mode="t2va",
            duration=4.0,
            profile="hosted",
        )
        if any(issue.code == "pose-count" for issue in issues):
            raise AssertionError(f"Self-test treated `{rate_word} beat` as a pose total: {issues}")

    missing_counted_pose = (
        "Create exactly 4 numbered pose locks. Pose 1 settles, Pose 2 follows, "
        "and Pose 3 holds."
    )
    _, issues = lint_prompt(
        missing_counted_pose,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "pose-count" for issue in issues):
        raise AssertionError("Self-test missed a declared pose-count mismatch.")

    beat_mapped_poses = (
        "An audible 128 BPM fashion beat begins with Beat 1 at 0.00 seconds. "
        "Create exactly 4 numbered pose locks: Pose 1 on Beat 2, Pose 2 on Beat 5, "
        "Pose 3 on Beat 8, and Pose 4 on Beat 11. Beat 32 ends the final hold."
    )
    _, issues = lint_prompt(
        beat_mapped_poses,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if any(issue.level in {"ERROR", "WARN"} for issue in issues):
        raise AssertionError(f"Self-test rejected a valid beat-mapped pose plan: {issues}")
    if not any(issue.code == "tempo-grid" for issue in issues):
        raise AssertionError("Self-test did not report deterministic tempo-grid math.")

    global_beat_mapped_poses = (
        "An audible 128 BPM fashion beat begins with Beat 1 at 0.00 seconds. "
        "Create exactly 3 numbered pose locks. Pose 1 enters. Pose 2 turns. Pose 3 holds. "
        "The pose locks land on Beats 2, 5, and 8."
    )
    _, issues = lint_prompt(
        global_beat_mapped_poses,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if any(issue.code == "rhythm-unmapped" for issue in issues):
        raise AssertionError(f"Self-test rejected an ordered global pose/Beat map: {issues}")

    for invalid_beat_list in ("8, 5, and 2", "2, 2, and 5"):
        invalid_global_pose_beat_order = (
            "An audible 128 BPM fashion beat begins with Beat 1 at 0.00 seconds. "
            "Pose 1 enters. Pose 2 turns. Pose 3 holds. "
            f"The pose locks land on Beats {invalid_beat_list}."
        )
        _, issues = lint_prompt(
            invalid_global_pose_beat_order,
            mode="t2va",
            duration=15.0,
            profile="hosted",
        )
        if not any(issue.code == "pose-beat-order" for issue in issues):
            raise AssertionError(
                f"Self-test accepted a descending/duplicate global pose map: {issues}"
            )

    invalid_individual_pose_beat_order = (
        "An audible 128 BPM fashion beat begins with Beat 1 at 0.00 seconds. "
        "Pose 1 lands on Beat 5. Pose 2 lands on Beat 2."
    )
    _, issues = lint_prompt(
        invalid_individual_pose_beat_order,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if not any(issue.code == "pose-beat-order" for issue in issues):
        raise AssertionError("Self-test accepted a descending individual pose/Beat map.")

    partially_beat_mapped_poses = (
        "An audible 128 BPM fashion beat begins with Beat 1 at 0.00 seconds. "
        "Pose 1 lands on Beat 2. Pose 2 turns. Pose 3 holds."
    )
    _, issues = lint_prompt(
        partially_beat_mapped_poses,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if not any(issue.code == "rhythm-unmapped" and "2, 3" in issue.message for issue in issues):
        raise AssertionError("Self-test accepted a partial pose-to-Beat map.")

    clock_form_beat_mapping = (
        "An audible 128 BPM fashion beat begins with Beat 1 at 0:00.000. "
        "Pose 1 lands at 0:00.469 on Beat 2."
    )
    _, issues = lint_prompt(
        clock_form_beat_mapping,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if any(issue.code in {"rhythm-unmapped", "beat-time-mismatch"} for issue in issues):
        raise AssertionError(f"Self-test rejected a valid clock-form beat mapping: {issues}")

    beat_outside_window = (
        "An audible 128 BPM beat begins with Beat 1 at 0.00 seconds. Beat 33 triggers "
        "the final flash."
    )
    _, issues = lint_prompt(
        beat_outside_window,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if not any(issue.code == "beat-outside-duration" for issue in issues):
        raise AssertionError("Self-test missed a beat anchor outside the duration.")

    fractional_grid_endpoint = (
        "An audible 130 BPM beat begins with Beat 1 at 0.00 seconds. Beat 33 triggers "
        "the final flash before the endpoint."
    )
    _, issues = lint_prompt(
        fractional_grid_endpoint,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if any(issue.code == "beat-outside-duration" for issue in issues):
        raise AssertionError(f"Self-test rejected valid Beat 33 at 130 BPM: {issues}")

    beat_list_outside_window = (
        "An audible 128 BPM beat begins with Beat 1 at 0.00 seconds. "
        "Flashes land on Beats 2, 5, and 35."
    )
    _, issues = lint_prompt(
        beat_list_outside_window,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if not any(issue.code == "beat-outside-duration" and "35" in issue.message for issue in issues):
        raise AssertionError("Self-test missed an out-of-window item in a Beat list.")

    beat_zero = (
        "An audible 128 BPM beat begins with Beat 1 at 0.00 seconds. Beat 0 triggers a flash."
    )
    _, issues = lint_prompt(
        beat_zero,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if not any(issue.code == "beat-ordinal" for issue in issues):
        raise AssertionError("Self-test missed zero-based Beat numbering.")

    invalid_clock_beat_origin = (
        "An audible 128 BPM beat begins with Beat 1 at 0:75. Beat 2 triggers a flash."
    )
    _, issues = lint_prompt(
        invalid_clock_beat_origin,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if not any(issue.code == "time-range-format" for issue in issues):
        raise AssertionError("Self-test accepted an invalid natural-clock Beat origin.")

    negative_beat_origin = (
        "An audible 128 BPM beat begins with Beat 1 at -1 seconds. Beat 2 triggers a flash."
    )
    _, issues = lint_prompt(
        negative_beat_origin,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if not any(issue.code == "beat-origin-value" for issue in issues):
        raise AssertionError("Self-test accepted a negative Beat origin.")

    beat_time_mismatch = (
        "An audible 128 BPM beat begins with Beat 1 at 0.00 seconds. "
        "Pose 1 lands at 1.500 seconds on Beat 2."
    )
    _, issues = lint_prompt(
        beat_time_mismatch,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if not any(issue.code == "beat-time-mismatch" for issue in issues):
        raise AssertionError("Self-test missed an explicit beat/time contradiction.")

    score_only_tempo = "Use an audience-only electronic music track at 128 BPM."
    _, issues = lint_prompt(
        score_only_tempo,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if any(issue.code in {"tempo-role", "rhythm-unmapped"} for issue in issues):
        raise AssertionError(f"Self-test rejected score-only BPM context: {issues}")

    ambiguous_pose_tempo = (
        "A one-take performance at 128 BPM moves through Pose 1, Pose 2, and Pose 3."
    )
    _, issues = lint_prompt(
        ambiguous_pose_tempo,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if not any(issue.code == "tempo-role" for issue in issues):
        raise AssertionError("Self-test missed ambiguous BPM ownership.")
    if not any(issue.code == "rhythm-unmapped" for issue in issues):
        raise AssertionError("Self-test missed BPM poses without Beat N anchors.")

    origin_without_pose_mapping = (
        "An audible 128 BPM beat begins with Beat 1 at 0.00 seconds. "
        "Pose 1 settles. Pose 2 turns. Pose 3 holds."
    )
    _, issues = lint_prompt(
        origin_without_pose_mapping,
        mode="t2va",
        duration=15.0,
        profile="hosted",
    )
    if not any(issue.code == "rhythm-unmapped" for issue in issues):
        raise AssertionError("Self-test treated a Beat 1 origin as a pose-to-beat mapping.")

    for quoted_bpm_copy in (
        'The interface displays the literal text "128 BPM".',
        "The interface displays the literal text '128 BPM'.",
        "The interface displays the literal text “128 BPM” .",
    ):
        _, issues = lint_prompt(
            quoted_bpm_copy,
            mode="t2va",
            duration=15.0,
            profile="hosted",
        )
        if any(issue.code in {"tempo-grid", "tempo-role"} for issue in issues):
            raise AssertionError(f"Self-test treated quoted BPM copy as timing direction: {issues}")

    for invalid_bpm in ("Use a -128 BPM score.", "Use a 999999999999999999999999999999999999999 BPM score."):
        _, issues = lint_prompt(
            invalid_bpm,
            mode="t2va",
            duration=15.0,
            profile="hosted",
        )
        if not any(issue.code == "tempo-value" for issue in issues):
            raise AssertionError(f"Self-test missed an invalid BPM value: {issues}")

    hosted_gap = (
        "0.0–1.9s — OPEN\nShow the opening.\n\n"
        "2.0–4.0s — CLOSE\nShow the close."
    )
    _, issues = lint_prompt(
        hosted_gap, mode="t2va", duration=4.0, profile="hosted"
    )
    if not any(issue.code == "timeline-gap" for issue in issues):
        raise AssertionError("Self-test did not catch a hosted timeline gap.")

    hosted_overlap = (
        "0.0–2.1s — OPEN\nShow the opening.\n\n"
        "2.0–4.0s — CLOSE\nShow the close."
    )
    _, issues = lint_prompt(
        hosted_overlap, mode="t2va", duration=4.0, profile="hosted"
    )
    if not any(issue.code == "timeline-overlap" for issue in issues):
        raise AssertionError("Self-test did not catch a hosted timeline overlap.")

    _, issues = lint_prompt(
        "0.0–4.1s — SHOT\nShow the complete shot.",
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "time-outside-duration" for issue in issues):
        raise AssertionError("Self-test did not catch a hosted range outside duration.")

    hosted_count_mismatch = (
        "Create exactly 3 distinct cuts.\n\n"
        "CUT 01 | 0.0-2.0s | OPEN\nShow the opening.\n\n"
        "CUT 02 | 2.0-4.0s | CLOSE\nShow the close."
    )
    _, issues = lint_prompt(
        hosted_count_mismatch,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "cut-count" for issue in issues):
        raise AssertionError("Self-test did not catch a hosted cut-count mismatch.")

    invalid_parameters = (
        'PARAMETERS\nTITLE = ""\nTITLE = "READY"\n\n'
        "Use TITLE exactly.\n\n0.0–4.0s — TITLE\nShow the title."
    )
    _, issues = lint_prompt(
        invalid_parameters,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "parameter-empty" for issue in issues):
        raise AssertionError("Self-test did not catch an empty hosted parameter.")
    if not any(issue.code == "parameter-duplicate" for issue in issues):
        raise AssertionError("Self-test did not catch a duplicate hosted parameter.")

    hosted_optional_distinct = (
        "Create exactly 2 cuts.\n\n"
        "CUT 01 | 0.0-2.0s | OPEN\nShow the opening.\n\n"
        "CUT 02 | 2.0-4.0s | CLOSE\nShow the close."
    )
    _, issues = lint_prompt(
        hosted_optional_distinct,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if issues:
        raise AssertionError(
            f"Self-test rejected `exactly N cuts` without `distinct`: {issues}"
        )

    hosted_malformed_cuts = (
        "Create exactly 2 cuts.\n\n"
        "CUT 01 | 0.0 to 2.0s | OPEN\nShow the opening.\n\n"
        "CUT 02 | 2.0 to 4.0s | CLOSE\nShow the close."
    )
    _, issues = lint_prompt(
        hosted_malformed_cuts,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "cut-header-format" for issue in issues):
        raise AssertionError("Self-test did not catch malformed hosted CUT headers.")
    if not any(issue.code == "cut-count" for issue in issues):
        raise AssertionError(
            "Self-test let a declared cut count pass without valid hosted CUT headers."
        )

    hosted_surface_handle = (
        "Use @Image 1 as the surface-native identity handle.\n\n"
        "0.0–4.0s — HERO\nPreserve the referenced identity through the final pose."
    )
    _, issues = lint_prompt(
        hosted_surface_handle,
        mode="ref2va",
        duration=4.0,
        profile="hosted",
    )
    if issues:
        raise AssertionError(
            f"Self-test rejected a hosted surface-specific media handle: {issues}"
        )

    hosted_user_guide_timeline = (
        "Reference Asset Instructions\n"
        "@Video 1 is the motion reference. Preserve its action timing.\n\n"
        "Core Concept\nA performer repeats the referenced movement in a quiet studio.\n\n"
        "Shot-by-Shot Description\n"
        "0–2 seconds: Wide shot. The performer enters; footsteps only.\n"
        "2–4 seconds: Medium shot. The movement resolves in a stable pose."
    )
    selected, issues = lint_prompt(
        hosted_user_guide_timeline,
        mode="auto",
        duration=4.0,
        profile="hosted",
    )
    if selected != "ref2va" or issues:
        raise AssertionError(
            f"Self-test rejected or misrouted the official hosted user-guide form: "
            f"{selected}, {issues}"
        )

    hosted_multilingual_timeline = (
        "0–2 seconds: ワイドショット。人物が静かに窓へ歩く。\n"
        "2–4 seconds: لقطة متوسطة. تتوقف الشخصية وتنظر إلى الضوء."
    )
    _, issues = lint_prompt(
        hosted_multilingual_timeline,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if issues:
        raise AssertionError(
            f"Self-test rejected valid multilingual hosted beat prose: {issues}"
        )

    hosted_user_guide_invalid_timeline = (
        "0–3 seconds: Wide shot. Show the opening action.\n"
        "2–5 seconds: Close shot. Show the payoff."
    )
    _, issues = lint_prompt(
        hosted_user_guide_invalid_timeline,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "timeline-overlap" for issue in issues):
        raise AssertionError("Self-test did not catch overlap in `N–N seconds:` syntax.")
    if not any(issue.code == "time-outside-duration" for issue in issues):
        raise AssertionError("Self-test did not catch out-of-range `N–N seconds:` syntax.")

    hosted_bullet_timeline = (
        "- 0–3 seconds: Wide shot. Show the opening action.\n"
        "- 2–5 seconds: Close shot. Show the payoff."
    )
    _, issues = lint_prompt(
        hosted_bullet_timeline,
        mode="t2va",
        duration=5.0,
        profile="hosted",
    )
    if not any(issue.code == "timeline-overlap" for issue in issues):
        raise AssertionError("Self-test missed overlapping bullet-prefixed hosted time ranges.")

    _, issues = lint_prompt(
        "Use @Image 1 as the character reference.\n\n"
        "0–4 seconds: The character turns toward camera.",
        mode="auto",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "mode-needed" for issue in issues):
        raise AssertionError("Self-test did not require a mode for image-only hosted handles.")

    _, issues = lint_prompt(
        "Use <Picture 1> as the identity reference.\n\n"
        "0–4 seconds: Preserve the referenced identity.",
        mode="ref2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "profile-media-handle" for issue in issues):
        raise AssertionError("Self-test did not reject native angle labels in hosted mode.")

    _, issues = lint_prompt(
        "@Audio 1 is the voice reference.\n\n"
        "0–4 seconds: Reperform the supplied line.",
        mode="ref2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "audio-needs-visual" for issue in issues):
        raise AssertionError("Self-test did not reject hosted audio-only Ref2VA.")

    _, issues = lint_prompt(
        "@Video 1 supplies the motion.\n\n0–4 seconds: Follow the motion.",
        mode="i2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "handle-mode" for issue in issues):
        raise AssertionError("Self-test did not reject a video handle in hosted I2VA.")

    _, issues = lint_prompt(
        "Use @Image1 as the character reference.\n\n"
        "0–4 seconds: Preserve the character.",
        mode="ref2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "hosted-handle-format" for issue in issues):
        raise AssertionError("Self-test did not reject malformed hosted handle spacing.")

    _, issues = lint_prompt(
        "Use @Image 0 as the character reference.\n\n"
        "0–4 seconds: Preserve the character.",
        mode="ref2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "hosted-handle-ordinal" for issue in issues):
        raise AssertionError("Self-test did not reject a zero-based hosted media handle.")

    _, issues = lint_prompt(
        "Use @Image N as the character reference.\n\n"
        "0–4 seconds: Preserve the character.",
        mode="ref2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "placeholder" for issue in issues):
        raise AssertionError("Self-test did not reject an unresolved hosted media placeholder.")

    structured_hosted_handle = (
        "integrated_multimodal_description: [Shot 1] Use @Image 1 as the style reference.\n\n"
        "overall_soundscape: Quiet room tone.\n\n"
        "non_diegetic_music: N/A\n"
    )
    _, issues = lint_prompt(
        structured_hosted_handle,
        mode="t2va",
        duration=4.0,
        profile="structured",
    )
    if not any(issue.code == "profile-media-handle" for issue in issues):
        raise AssertionError("Self-test did not reject a hosted handle in structured mode.")

    structured_malformed_hosted_handle = (
        "integrated_multimodal_description: [Shot 1] Use @Image1 as the style reference.\n\n"
        "overall_soundscape: Quiet room tone.\n\n"
        "non_diegetic_music: N/A\n"
    )
    _, issues = lint_prompt(
        structured_malformed_hosted_handle,
        mode="t2va",
        duration=4.0,
        profile="structured",
    )
    if not any(issue.code == "profile-media-handle" for issue in issues):
        raise AssertionError("Self-test did not reject a malformed hosted handle in structured mode.")

    structured_scoped_no_cut = (
        "integrated_multimodal_description: [Shot 1] Keep the opening action continuous with "
        "no cuts inside Shot 1. [Shot 2] At 00:02.000, cut to the established subject and hold.\n\n"
        "overall_soundscape: Continuous room tone.\n\n"
        "non_diegetic_music: N/A.\n"
    )
    _, issues = lint_prompt(
        structured_scoped_no_cut,
        mode="t2va",
        duration=4.0,
        profile="structured",
    )
    if issues:
        raise AssertionError(
            f"Self-test rejected scoped no-cut prose or terminal `N/A.` punctuation: {issues}"
        )

    structured_music_conflict = (
        "integrated_multimodal_description: [Shot 1] A lamp switches on.\n\n"
        "overall_soundscape: A small switch click.\n\n"
        "non_diegetic_music: N/A. Add a triumphant orchestral background score.\n"
    )
    _, issues = lint_prompt(
        structured_music_conflict,
        mode="t2va",
        duration=4.0,
        profile="structured",
    )
    if not any(issue.code == "music-conflict" for issue in issues):
        raise AssertionError("Self-test did not catch a structured no-music conflict.")

    structured_topology_conflict = (
        "integrated_multimodal_description: [Shot 1] One continuous take with no cuts. "
        "The subject crosses the room. [Shot 2] At 00:02.000, the camera cuts to a close-up.\n\n"
        "overall_soundscape: Continuous room tone.\n\n"
        "non_diegetic_music: N/A\n"
    )
    _, issues = lint_prompt(
        structured_topology_conflict,
        mode="t2va",
        duration=4.0,
        profile="structured",
    )
    if not any(issue.code == "topology-conflict" for issue in issues):
        raise AssertionError("Self-test did not catch a structured oner/cut conflict.")

    hosted_topology_conflict = (
        "Create a one-take sequence with no-cuts.\n\n"
        "CUT 01 | 0.0-2.0s | OPEN\nThe subject enters.\n\n"
        "CUT 02 | 2.0-4.0s | CLOSE\nCut to a close-up."
    )
    _, issues = lint_prompt(
        hosted_topology_conflict,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "topology-conflict" for issue in issues):
        raise AssertionError("Self-test did not catch a hosted oner/cut conflict.")

    hosted_music_conflict = (
        "0–4 seconds: Hold on the final product.\n"
        "Non-diegetic music: N/A. Add an orchestral score and soundtrack."
    )
    _, issues = lint_prompt(
        hosted_music_conflict,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if not any(issue.code == "music-conflict" for issue in issues):
        raise AssertionError("Self-test did not flag a hosted no-music/score conflict.")

    hosted_negated_soundtrack = (
        "0–4 seconds: Hold on the final product.\n"
        "Non-diegetic music: N/A. Do not add a soundtrack."
    )
    _, issues = lint_prompt(
        hosted_negated_soundtrack,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if any(issue.code == "music-conflict" for issue in issues):
        raise AssertionError("Self-test treated a negated soundtrack request as positive music.")

    hosted_scoped_music = (
        "0–4 seconds: No music plays in the room; add a restrained audience-only score."
    )
    _, issues = lint_prompt(
        hosted_scoped_music,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if any(issue.code == "music-conflict" for issue in issues):
        raise AssertionError("Self-test confused diegetic scene silence with a no-BGM rule.")

    structured_two_shots = (
        "integrated_multimodal_description: [Shot 1] One shot shows the car. "
        "[Shot 2] At 00:02.000, a close-up shows the wheel.\n\n"
        "overall_soundscape: Road ambience.\n\n"
        "non_diegetic_music: N/A\n"
    )
    _, issues = lint_prompt(
        structured_two_shots,
        mode="t2va",
        duration=4.0,
        profile="structured",
    )
    if any(issue.code == "topology-conflict" for issue in issues):
        raise AssertionError("Self-test treated ordinary `one shot` prose as an oner rule.")

    hosted_cut_prose = (
        "Cut 1 second from the opening hold before rendering.\n"
        "Cut 2 frames from the transition in post.\n\n"
        "0.0–4.0s — HERO\nPreserve the final pose through the complete beat."
    )
    _, issues = lint_prompt(
        hosted_cut_prose,
        mode="t2va",
        duration=4.0,
        profile="hosted",
    )
    if issues:
        raise AssertionError(
            f"Self-test treated ordinary hosted cut-edit prose as malformed headers: {issues}"
        )

    print(
        "SELF-TEST PASS: all modes plus timing, audio-role, duration, alignment, "
        "field, reference-label, dialogue-source, speaker-order, hosted-user-guide, "
        "clock-range, tempo-grid, pose-count, and native-ComfyUI cases"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", nargs="?", help="Prompt text file, or - for stdin")
    parser.add_argument("--profile", choices=PROFILES, default="structured")
    parser.add_argument("--mode", choices=MODES, default="auto")
    parser.add_argument("--duration", type=float, help="Target duration in seconds")
    parser.add_argument("--max-chars", type=int, default=7000)
    parser.add_argument("--pictures", type=int, help="Connected Ref2VA picture count")
    parser.add_argument("--videos", type=int, help="Connected Ref2VA video count")
    parser.add_argument(
        "--audios",
        type=int,
        help="Connected Ref2VA audio ordinal count, including enabled video soundtracks",
    )
    parser.add_argument(
        "--standalone-audios",
        type=int,
        help="Standalone audio file count; excludes soundtracks embedded in reference videos",
    )
    parser.add_argument(
        "--raw-frames",
        type=int,
        help="Actual untrimmed native-ComfyUI frame count on the 17k+5 grid",
    )
    parser.add_argument("--trim-frames", type=int, help="Leading frames removed after native-ComfyUI decode")
    parser.add_argument(
        "--tail-trim-frames",
        type=int,
        help="Trailing frames removed after native-ComfyUI decode",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        run_self_test()
        return 0
    if not args.prompt:
        print("ERROR cli: provide PROMPT.txt, - for stdin, or --self-test", file=sys.stderr)
        return 2

    if args.prompt == "-":
        text = sys.stdin.read()
    else:
        try:
            text = Path(args.prompt).read_text(encoding="utf-8")
        except OSError as exc:
            print(f"ERROR io: {exc}", file=sys.stderr)
            return 2

    selected, issues = lint_prompt(
        text,
        mode=args.mode,
        duration=args.duration,
        max_chars=args.max_chars,
        profile=args.profile,
        pictures=args.pictures,
        videos=args.videos,
        audios=args.audios,
        standalone_audios=args.standalone_audios,
        raw_frames=args.raw_frames,
        trim_frames=args.trim_frames,
        tail_trim_frames=args.tail_trim_frames,
    )
    errors = sum(issue.level == "ERROR" for issue in issues)
    warnings = sum(issue.level == "WARN" for issue in issues)
    print(
        f"Profile: {args.profile} | Mode: {selected.upper()} | Characters: {len(text)} "
        f"| Errors: {errors} | Warnings: {warnings}"
    )
    for issue in issues:
        print(f"{issue.level} {issue.code}: {issue.message}")
    if not issues:
        print("PASS: no structural issues found")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
