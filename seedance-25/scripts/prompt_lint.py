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
    r"(?:\b(defines?|corresponds?|references?|provides?|controls?|inherits?|"
    r"source video|sole editing master|first frame|last frame|keyframe|"
    r"before[- ]transition clip|after[- ]transition clip|transition source|"
    r"transition target|used (?:only )?for|is used|do not use|not used)\b"
    r"|定义|对应|参考|提供|控制|继承|源视频|唯一编辑主视频|主视频|首帧|尾帧|关键帧|"
    r"仅用于|用于|不要使用|不使用|切勿使用)",
    re.IGNORECASE,
)

KIND_NORM = {
    "image": "image",
    "图片": "image",
    "图": "image",
    "video": "video",
    "视频": "video",
    "audio": "audio",
    "音频": "audio",
}

HANDLE_RE = re.compile(
    r"(?<![A-Za-z0-9_@])(?:"
    r"@(?P<at_kind>Image|Video|Audio|图片|图|视频|音频)(?:[ \t]*(?P<at_number>\d+))?(?![A-Za-z0-9_])"
    r"|\[(?P<bracket_kind>Image|Video|Audio|图片|图|视频|音频)[ \t]*(?P<bracket_number>\d+)\]"
    r"|<(?P<angle_kind>Image|Video|Audio)[ \t]*(?P<angle_number>\d+)>"
    r")",
    re.IGNORECASE,
)
VIDEO_HANDLE_PATTERN = (
    r"(?:@(?:Video|视频)(?:[ \t]*\d+)?|\[(?:Video|视频)[ \t]*\d+\]|<Video[ \t]*\d+>)"
)
IMAGE_HANDLE_PATTERN = (
    r"(?:@(?:Image|图片|图)[ \t]*\d+|\[(?:Image|图片|图)[ \t]*\d+\]|<Image[ \t]*\d+>)"
)
RANGE_RE = re.compile(
    r"(?:(?P<start_mm>\d{1,2}):(?P<start_ss>\d{2}(?:\.\d+)?)\s*[-–—]\s*"
    r"(?P<end_mm>\d{1,2}):(?P<end_ss>\d{2}(?:\.\d+)?))"
    r"|(?:(?P<start>\d+(?:\.\d+)?)\s*(?:sec(?:ond)?s?|s)?\s*[-–—]\s*"
    r"(?P<end>\d+(?:\.\d+)?)\s*(?:sec(?:ond)?s?|s))",
    re.IGNORECASE,
)


def _match_bounds(match: re.Match[str]) -> tuple[float, float]:
    if match.group("start_mm") is not None:
        start = int(match.group("start_mm")) * 60 + float(match.group("start_ss"))
        end = int(match.group("end_mm")) * 60 + float(match.group("end_ss"))
        return start, end
    return float(match.group("start")), float(match.group("end"))


TIME_POINT_RE = re.compile(r"\bat\s+(\d+(?:\.\d+)?)\s*(?:s|sec(?:ond)?s?)\b", re.IGNORECASE)
TODO_MARKER_RE = re.compile(r"\bTODO\b", re.IGNORECASE)
TEMPLATE_PLACEHOLDER_RE = re.compile(
    r"(?:<(?:subject|scene|action|event|placeholder|specified|primary|name|N|"
    r"original\s+object/region|whole\s+video(?:\s+or\s+exact\s+scope)?|scope|target|"
    r"speaker(?:\s+or\s+sound\s+category|/sound)?|video\s+type)(?:\s+[^<>]+)?>"
    r"|<[AB]>)",
    re.IGNORECASE,
)
SHOT_HEADER_PREFIX_RE = re.compile(
    r"(?:\b(?:Shot|Stage)\s+\d+|(?:镜头|分镜|阶段)\s*\d+)\s*(?:[([（]|[,|:：]\s*)\s*$",
    re.IGNORECASE,
)
CJK_CHAR_RE = re.compile(r"[\u4e00-\u9fff]")


def add(issues: list[Issue], severity: str, code: str, message: str) -> None:
    issues.append(Issue(severity, code, message))


def infer_mode(text: str) -> str:
    if re.search(
        rf"\bextend(?:s|ed|ing)?\s+(?:{VIDEO_HANDLE_PATTERN}|forward|backward)"
        rf"|\bcontinue\s+from\s+{VIDEO_HANDLE_PATTERN}"
        rf"|(?:向前|向后|正向|反向)?(?:延长|延展|续写)\s*{VIDEO_HANDLE_PATTERN}"
        rf"|{VIDEO_HANDLE_PATTERN}\s*(?:为|是)?(?:待延长|要延长|用于延长)的?源视频",
        text,
        re.IGNORECASE,
    ):
        return "extension"
    if re.search(
        rf"\bedit\s+{VIDEO_HANDLE_PATTERN}|\bsole editing master\b"
        rf"|(?:编辑|修改)\s*{VIDEO_HANDLE_PATTERN}|唯一编辑主视频",
        text,
        re.IGNORECASE,
    ):
        return "edit"
    return "generation"


def reference_mentions(text: str) -> list[ReferenceMention]:
    mentions: list[ReferenceMention] = []
    for match in HANDLE_RE.finditer(text):
        kind = match.group("at_kind") or match.group("bracket_kind") or match.group("angle_kind")
        number_text = match.group("at_number") or match.group("bracket_number") or match.group("angle_number")
        if kind is None:
            continue
        norm_kind = KIND_NORM.get(kind.lower())
        if norm_kind is None:
            continue
        # Dreamina surfaces may expose singleton @Video and @Audio tokens. A
        # bare @Image / @图 is not a documented identity-safe handle, so ignore it.
        if number_text is None and norm_kind == "image":
            continue
        mentions.append(ReferenceMention(norm_kind, int(number_text) if number_text else None, match.group(0)))
    return mentions


def referenced_handles(text: str) -> dict[str, set[int]]:
    found: dict[str, set[int]] = {"image": set(), "video": set(), "audio": set()}
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
    mode: str = "generation",
) -> None:
    counts = {"image": images, "video": videos, "audio": audio}
    hard = {"image": 30, "video": 10, "audio": 10}
    for kind, count in counts.items():
        if count is not None and count > hard[kind]:
            add(issues, "error", f"{kind.upper()}_LIMIT", f"{count} {kind}s exceeds the hard limit of {hard[kind]}.")
        elif count is None and handles[kind] and max(handles[kind]) > hard[kind]:
            add(
                issues,
                "error",
                f"{kind.upper()}_LIMIT",
                f"Prompt references @{kind.title()} {max(handles[kind])}, exceeding the hard limit of {hard[kind]}.",
            )
        if count is not None and handles[kind] and max(handles[kind]) > count:
            add(
                issues,
                "error",
                f"MISSING_{kind.upper()}_HANDLE",
                f"Prompt references @{kind.title()} {max(handles[kind])}, but only {count} {kind}(s) were declared available.",
            )

    known_counts = [x for x in (images, videos, audio) if x is not None]
    total_handle_refs = sum(len(v) for v in handles.values())
    if len(known_counts) == 3 and sum(known_counts) > 50:
        add(issues, "error", "TOTAL_MATERIAL_LIMIT", f"{sum(known_counts)} total assets exceeds the hard limit of 50.")
    elif len(known_counts) < 3 and total_handle_refs > 50:
        add(
            issues,
            "error",
            "TOTAL_MATERIAL_LIMIT",
            f"Prompt references {total_handle_refs} distinct assets, exceeding the hard combined limit of 50.",
        )

    if video_seconds is not None and video_seconds > 30:
        add(issues, "error", "VIDEO_DURATION_LIMIT", f"Reference videos total {video_seconds:g}s; the hard combined limit is 30s.")
    elif mode == "edit" and video_seconds is not None and video_seconds < 4.0:
        add(
            issues,
            "error",
            "EDIT_VIDEO_MIN_DURATION",
            f"Edit source video is {video_seconds:g}s; BytePlus ModelArk video editing requires 4-30s.",
        )
    elif video_seconds is not None and 0 < video_seconds < 2.0:
        add(
            issues,
            "error",
            "VIDEO_MIN_DURATION",
            f"Reference video is {video_seconds:g}s; documented minimum per video is 2s.",
        )

    if audio_seconds is not None and audio_seconds > 30:
        add(issues, "error", "AUDIO_DURATION_LIMIT", f"Reference audio totals {audio_seconds:g}s; the hard combined limit is 30s.")
    elif audio_seconds is not None and 0 < audio_seconds < 2.0:
        add(
            issues,
            "error",
            "AUDIO_MIN_DURATION",
            f"Reference audio is {audio_seconds:g}s; documented minimum per audio clip is 2s.",
        )

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


def timeline_matches(text: str) -> list[re.Match[str]]:
    """Extract documented timeline forms without treating every numeric range as time.

    Supports labeled blocks (`0-3s: ...`), inline sequences (`0-3 seconds...3-7 seconds...`),
    bracketed windows (`[1s-4s]....`), and Shot/Stage/镜头 headers (`Shot 2 (3-6s):`,
    `Stage 1 (0-4s):`, `镜头 1 (0-2s):`). Prose ranges like "a 5-10 seconds clip"
    are excluded.
    """

    candidates = list(RANGE_RE.finditer(text))
    accepted: list[re.Match[str]] = []
    for match in candidates:
        line_prefix = text[text.rfind("\n", 0, match.start()) + 1 : match.start()]
        suffix = text[match.end() : match.end() + 12]
        bracketed = line_prefix.rstrip().endswith("[") and re.match(r"\s*\]", suffix) is not None
        starts_line = re.fullmatch(r"\s*(?:[-*]\s*)?(?:[*_\"'“‘]\s*)?", line_prefix) is not None
        timeline_punctuation = re.match(r"\s*(?:\]|:|：|—|–|\.{2,})", suffix) is not None
        preceded_by_inline_separator = re.search(r"(?:\.{2,}|\])\s*(?:\[\s*)?$", line_prefix) is not None
        shot_header = (
            SHOT_HEADER_PREFIX_RE.search(line_prefix) is not None
            and re.match(r"\s*(?:[)\]）]|[.:：—–])", suffix) is not None
        )
        if bracketed or starts_line or timeline_punctuation or preceded_by_inline_separator or shot_header:
            accepted.append(match)
    if len(accepted) >= 2:
        first_start, first_end = _match_bounds(accepted[0])
        second_start, second_end = _match_bounds(accepted[1])
        first_prefix = text[text.rfind("\n", 0, accepted[0].start()) + 1 : accepted[0].start()]
        is_shot_container = SHOT_HEADER_PREFIX_RE.search(first_prefix) is not None
        if (
            is_shot_container
            and second_start == first_start
            and second_end < first_end
            and all(_match_bounds(m)[1] <= first_end for m in accepted[1:])
        ):
            return accepted[1:]
    return accepted


def timeline_ranges(text: str) -> list[tuple[float, float]]:
    return [_match_bounds(m) for m in timeline_matches(text)]


DIALOGUE_RE = re.compile(
    r"(?:(?:\b(?:line(?:\s+\d+)?|lines|says|said|asks|asked|shouts|shouted|whispers|whispered|speaks|spoke|murmurs|murmured|replies|replied|yells|yelled|barks|barked|calls|called|mutters|muttered|exclaims|exclaimed|snaps|snapped|dialogue)\b"
    r"|台词|对白|(?:开口|低语|冷笑|嘱咐|[说问喊喝叫讲唱念吼叹骂笑答怒])道?|[说问喊叫吼])"
    r"(?:\s*\([^()]{0,220}\)|\s*（[^（）]{0,220}）|[^\n:：,，\"“「]{0,90}){0,2}[:：,，]\s*[\"“「](?P<quoted>[^\"”」]{1,280})[\"”」])"
    r"|\{(?P<braced>[^{}\n]+)\}",
    re.IGNORECASE,
)
LATIN_WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿ]+)?")
DIALOGUE_WPS_WARN = 2.0
CLIP_MAX_DIALOGUE_LINES = 3
CLIP_MAX_TIMED_SHORT_LINES = 5
CLIP_MAX_DIALOGUE_WORDS = 24
CLIP_MAX_DRAMA_DIALOGUE_LINES = 10
CLIP_MAX_DRAMA_DIALOGUE_WORDS = 43


def _spoken_word_equivalents(spoken: str) -> float:
    """Count Latin words plus CJK characters (~0.45 English word-equivalents per CJK char)."""

    return len(LATIN_WORD_RE.findall(spoken)) + 0.45 * len(CJK_CHAR_RE.findall(spoken))


def check_dialogue_density(issues: list[Issue], text: str) -> None:
    """Warn when timed shots or whole multi-shot clips carry too much speech.

    Craft heuristic from desk-continuity-and-coverage.md, not a first-party cap.
    Supports both Latin words and CJK characters, and deduplicates top-level
    transcript blocks when `[Shot list]` / `[分镜列表]` is present.
    """

    shot_list_split = re.split(
        r"^\s*\[(?:Shot\s+list|分镜列表|镜头列表|分镜)\]\s*$",
        text,
        maxsplit=1,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    dialogue_scope = (
        shot_list_split[1]
        if len(shot_list_split) == 2 and DIALOGUE_RE.search(shot_list_split[1])
        else text
    )
    all_dialogues = list(DIALOGUE_RE.finditer(dialogue_scope))
    total_lines = len(all_dialogues)
    line_word_counts = [
        _spoken_word_equivalents(d.group("quoted") or d.group("braced") or "")
        for d in all_dialogues
    ]
    total_words = sum(line_word_counts)
    matches = timeline_matches(text)
    durations = [_match_bounds(m)[1] - _match_bounds(m)[0] for m in matches]
    total_timed_seconds = sum(d for d in durations if d > 0)

    speaking_windows = 0
    for index, match in enumerate(matches):
        block_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        if DIALOGUE_RE.search(text[match.end() : block_end]):
            speaking_windows += 1

    is_timed_slow_dialogue_drama = (
        len(durations) >= 5
        and total_timed_seconds >= 24.0
        and speaking_windows >= 4
        and bool(line_word_counts)
        and all(w <= 8.5 for w in line_word_counts)
        and (total_words / total_timed_seconds) <= 1.5
    )

    if is_timed_slow_dialogue_drama:
        max_lines = CLIP_MAX_DRAMA_DIALOGUE_LINES
        max_words = CLIP_MAX_DRAMA_DIALOGUE_WORDS
    elif matches and all(w <= 5.5 for w in line_word_counts):
        max_lines = CLIP_MAX_TIMED_SHORT_LINES
        max_words = CLIP_MAX_DIALOGUE_WORDS
    else:
        max_lines = CLIP_MAX_DIALOGUE_LINES
        max_words = CLIP_MAX_DIALOGUE_WORDS

    if total_lines > max_lines or total_words > max_words:
        display_words = f"{total_words:g}"
        add(
            issues,
            "warning",
            "CLIP_DIALOGUE_OVERLOAD",
            f"Clip contains {total_lines} spoken line(s) ({display_words} word-equivalents total). "
            f"Above {CLIP_MAX_DIALOGUE_LINES} lines / {CLIP_MAX_DIALOGUE_WORDS} words in general clips (or {CLIP_MAX_DRAMA_DIALOGUE_LINES} short clauses / {CLIP_MAX_DRAMA_DIALOGUE_WORDS} words in a 25-30s timed dialogue drama) risks TTS prosody compression; "
            "tighten clauses, keep per-shot pace < 1.8 words/s, use Dreamina Long Video, or split across two generations if preferred.",
        )

    for index, match in enumerate(matches):
        start, end = _match_bounds(match)
        duration = end - start
        if duration <= 0:
            continue
        block_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.end() : block_end]
        words = 0.0
        for dialogue in DIALOGUE_RE.finditer(block):
            spoken = dialogue.group("quoted") or dialogue.group("braced") or ""
            words += _spoken_word_equivalents(spoken)
        wps_limit = 2.5 if is_timed_slow_dialogue_drama else DIALOGUE_WPS_WARN
        if words and words / duration >= wps_limit:
            add(
                issues,
                "warning",
                "DIALOGUE_DENSITY",
                f"{start:g}-{end:g}s carries {words:g} spoken word-equivalents ({words / duration:.1f} words/s). "
                "Aim for 1.0-1.5 words/s (below 2.0 words/s, or <= 2.4 words/s when split into short clauses in a slow dialogue drama) so TTS prosody stays natural and unhurried.",
            )


NEGATED_EFFECT_RE = {
    "freeze frames": re.compile(
        r"(?:\bno\b|\bnot\b|\bwithout\b|\bavoid\b|不要|没有|不是|非|无|禁止|避免)[^\n.。;；]{0,30}?"
        r"(?:freeze[- ]?frames?|freezes?|定格)(?!\s*(?:except|save\s+for|other\s+than|除了))",
        re.IGNORECASE,
    ),
    "slow motion": re.compile(
        r"(?:\bno\b|\bnot\b|\bwithout\b|\bavoid\b|不要|没有|不是|非|无|禁止|避免)[^\n.。;；]{0,30}?"
        r"(?:slow[- ]?motion|slow[- ]?mo\b|慢动作|慢镜头)(?!\s*(?:except|save\s+for|other\s+than|除了))",
        re.IGNORECASE,
    ),
}
SCOPED_EXCEPTION_RE = re.compile(
    r"(?:\bexcept(?:\s+for)?\b|\bsave\s+for\b|\bother\s+than\b|除了)[^\n.。;；]{0,60}?"
    r"(?:slow[- ]?motion|slow[- ]?mo\b|speed[- ]?ramp|bullet[- ]?time|freeze[- ]?frames?|hit[- ]?stop|慢动作|慢镜头|子弹时间|定格)",
    re.IGNORECASE,
)
POSITIVE_EFFECT_RE = {
    "freeze frames": re.compile(r"hit[- ]?stop|freeze[- ]?frames?|定格", re.IGNORECASE),
    "slow motion": re.compile(r"slow[- ]?motion|slow[- ]?mo\b|speed[- ]?ramp|bullet[- ]?time|慢动作|慢镜头|子弹时间", re.IGNORECASE),
}


def check_negation_conflicts(issues: list[Issue], text: str) -> None:
    """Warn when an Avoid-style negation is contradicted elsewhere in the prompt."""

    for effect, negated in NEGATED_EFFECT_RE.items():
        if not negated.search(text):
            continue
        if SCOPED_EXCEPTION_RE.search(text):
            continue
        remainder = negated.sub(" ", text)
        positive = POSITIVE_EFFECT_RE[effect].search(remainder)
        if positive:
            add(
                issues,
                "warning",
                "NEGATION_CONFLICT",
                f"The prompt excludes {effect} but also asks for '{positive.group(0)}'. "
                "Remove one side, or rewrite the effect as an impact flash plus a camera jolt.",
            )


NEGATED_MORPH_RE = re.compile(
    r"(?:\bno\b|\bnot\b|\bwithout\b|\bavoid\b|\bnever\b|不要|没有|不是|非|无|禁止|避免)"
    r"[^\n.。;；]{0,30}?(?:变形|\bmorph(?:s|ed|ing)?\b|\bshape[- ]?shift(?:s|ed|ing)?\b)",
    re.IGNORECASE,
)
POSITIVE_MORPH_RE = re.compile(
    r"变形|\bmorph(?:s|ed|ing)?\s+into\b|\bshape[- ]?shift(?:s|ed|ing)?\s+into\b",
    re.IGNORECASE,
)
STYLE_2D_RE = re.compile(
    r"\b2D\s+(?:cel|anime|animation|hand[- ]drawn)\b|\bcel[- ]shaded\b|\bcel[- ]painted\b|\bgouache\b"
    r"|\bhand[- ]drawn\s+2D\b|赛璐璐|手绘2D|二维动画",
    re.IGNORECASE,
)
AIRBRUSH_PAINTERLY_RE = re.compile(
    r"\bairbrush(?:ed)?\b|\bsemi[- ]realistic\b|\blineless\b|厚涂|半写实|柔光厚涂",
    re.IGNORECASE,
)
NEGATED_AIRBRUSH_RE = re.compile(
    r"(?:\bno\b|\bnot\b|\bwithout\b|\bavoid\b|\bexclude\b|\bnever\b|不要|没有|不是|非|无|禁止|避免)"
    r"[^\n.。;；]{0,60}?(?:\bairbrush(?:ed)?(?:\s+rendering|\s+shading)?\b|\bsemi[- ]realistic\b|\blineless\b|厚涂|半写实|柔光厚涂)",
    re.IGNORECASE,
)
CEL_OUTLINE_RE = re.compile(
    r"\bcel[- ](?:shaded|painted)\b|\b2D\s+stylized\s+anime\b|\bflat\s+cel\b|赛璐璐|平涂",
    re.IGNORECASE,
)
NEGATED_CEL_RE = re.compile(
    r"(?:\bno\b|\bnot\b|\bwithout\b|\bavoid\b|\bnever\b|不要|没有|不是|非|无|禁止|避免)"
    r"[^\n.。;；]{0,45}?(?:\bcel[- ](?:shaded|painted|shading)\b|\b2D\s+stylized\s+anime\b|\bflat\s+cel\b|赛璐璐|平涂)",
    re.IGNORECASE,
)
NEGATED_CARTOON_OVERACT_RE = re.compile(
    r"(?:\bno\b|\bnot\b|\bwithout\b|\bavoid\b|\bnever\b|不要|没有|不是|非|无|禁止|避免)"
    r"[^\n.。;；]{0,90}?(?:\bsing[- ]song\s+lilt\b|\boffended\s+gasp\b|\bstartled\s+yelp\b|\binhales?\s+excitedly\b|\bhigh[- ]pitched\s+voice\s+that\s+cracks\b|\beyes\s+(?:snapping\s+)?wide\s+into\s+(?:\w+\s+)?circles\b|\bbrows\s+shooting\s+into\b|\bpuffs?\s+(?:her|his|their)\s+(?:\w+\s+)?cheeks\b|\bpuffed\s+balloon\s+cheeks\b)",
    re.IGNORECASE,
)
CARTOON_OVERACT_RE = re.compile(
    r"\bsing[- ]song\s+lilt\b|\boffended\s+gasp\b|\bstartled\s+yelp\b|\binhales?\s+excitedly\b|\bhigh[- ]pitched\s+voice\s+that\s+cracks\b|\beyes\s+(?:snapping\s+)?wide\s+into\s+(?:\w+\s+)?circles\b|\bbrows\s+shooting\s+into\b|\bpuffs?\s+(?:her|his|their)\s+(?:\w+\s+)?cheeks\b",
    re.IGNORECASE,
)
NEGATED_PROSODY_FLATTENER_RE = re.compile(
    r"(?:\bno\b|\bnot\b|\bwithout\b|\bavoid\b|\bnever\b|不要|没有|不是|非|无|禁止|避免)"
    r"[^\n.。;；]{0,60}?(?:\bdeadpan\b|\bmonotone\b|\bflat\s+(?:voice|tone|delivery|resignation)\b)",
    re.IGNORECASE,
)
PROSODY_FLATTENER_RE = re.compile(
    r"\bdeadpan\s+(?:voice|tone|delivery)\b|\bmonotone\s+(?:voice|tone|delivery)\b|\bflat\s+(?:voice|tone|delivery|resignation)\b|\bkeep\s+(?:her|his|their)\s+expressions?\s+subtle,\s+cool,\s+and\s+deadpan\b",
    re.IGNORECASE,
)
SPLIT_DIALOGUE_CUT_RE = re.compile(
    r"\{[^{}\n]*?[-–—]\s*[\"”']?\s*\}[^{}]{0,260}?\[Cut\s+to\][^{}]{0,360}?\{\s*[\"“']?\s*[-–—]",
    re.IGNORECASE | re.DOTALL,
)
NEGATED_LENS_RE = re.compile(
    r"(?:\bno\b|\bnot\b|\bwithout\b|\bavoid\b|\bnever\b|不要|没有|不是|非|无|禁止|避免)"
    r"[^\n.。;；]{0,30}?(?:\bbokeh\b|\bshallow\s+depth\s+of\s+field\b|\banamorphic\s+lens\b|\bf/\d(?:\.\d)?\b|景深虚化|大光圈虚化|背景虚化)",
    re.IGNORECASE,
)
LIVE_ACTION_LENS_RE = re.compile(
    r"\bbokeh\b|\bshallow\s+depth\s+of\s+field\b|\banamorphic\s+lens\b|\bf/\d(?:\.\d)?\b|景深虚化|大光圈虚化|背景虚化",
    re.IGNORECASE,
)
UNSUPPORTED_HANDLE_RE = re.compile(
    r"<<<\s*(?:Image|Video|Audio|图片|视频|音频)\s*\d*\s*>>>|@\[[^\]\n]+\]|<\s*(?:视频|图片|音频)\s*\d*\s*>",
    re.IGNORECASE,
)
EDIT_REF_TRAP_RE = re.compile(
    rf"(?<!not\s)(?<!不要)(?:\breferences?\s+{VIDEO_HANDLE_PATTERN}"
    rf"|\buse\s+{VIDEO_HANDLE_PATTERN}\s+as\s+a?\s*reference"
    rf"|参考\s*(?:{VIDEO_HANDLE_PATTERN}|<\s*视频\s*\d*\s*>))",
    re.IGNORECASE,
)
NEGATED_STALEMATE_RE = re.compile(
    r"(?:\bno\b|\bnot\b|\bwithout\b|\bavoid\b|\bnever\b|不要|没有|不是|非|无|禁止|避免|不在)"
    r"[^\n.。;；]{0,35}?(?:对波僵持|僵持结束|死死对视|stalemate|lock\s+glares)",
    re.IGNORECASE,
)
STALEMATE_CLASH_RE = re.compile(
    r"硬生生对撞[^。;\n]{0,80}?死死对视"
    r"|\bclash(?:es|ing)?\s+point[- ]blank\b[^.\n]{0,120}?\block(?:ing)?\s+glares\b"
    r"|\block(?:ed|ing)?\s+in\s+a\s+stalemate\b",
    re.IGNORECASE,
)
NEGATED_PASSIVE_PURSUIT_RE = re.compile(
    r"(?:\bno\b|\bnot\b|\bwithout\b|\bavoid\b|\bnever\b|不要|没有|不是|非|无|禁止|避免)"
    r"[^\n.。;；]{0,40}?\b(?:runs?|running|jogs?|jogging|chases?|chasing|follows?|following)\s+(?:stiffly\s+|upright\s+)?(?:after|behind)\b",
    re.IGNORECASE,
)
PASSIVE_PURSUIT_SENTENCE_RE = re.compile(
    r"[^.\n;；。]*\b(?:runs?|jogs?|chases?|follows?)\s+(?:stiffly\s+|upright\s+)?(?:after|behind)\s+(?:him|her|it|them|the\s+\w+)[^.\n;；。]*",
    re.IGNORECASE,
)
ACTIVE_CATCH_VERB_RE = re.compile(
    r"\b(?:lunges?|lunging|reaches?|reaching|grabs?|grabbing|snatches?|snatching|scoops?|scooping|sweeps?|sweeping|dives?|diving|swipes?|swiping|yanks?|yanking|cupped\s+hands)\b",
    re.IGNORECASE,
)
OPENING_SETTLE_IN_ACTION_RE = re.compile(
    r"\bsettl(?:e|es|ing)\b[^\n.。;；]{0,50}?\bbefore\s+the\s+(?:chase|fight|battle|combat|action|pursuit|duel)\b",
    re.IGNORECASE,
)
EXCLUSION_BLOCK_RE = re.compile(
    r"(?:^\s*\[(?:Strictly\s+exclude|Exclusions?|Technical\s+Exclusions?|Avoid|严格排除|排除项?|避免|禁忌)\]\s*$"
    r"|^\s*(?:Strictly\s+exclude|Avoid|严格排除|排除|避免)\s*[:：])"
    r"(?P<body>.*?)(?=^\s*\[[^\]\n]+\]\s*$|\Z)",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)
BLOATED_EXCLUSION_WORDS_WARN = 80
NEGATED_MUSIC_CLAUSE_RE = re.compile(
    r"(?:\bno\b|\bnot\b|\bwithout\b|\bremove\b|\bexclude\b|\bnever\b|\bzero\b|不要|没有|无|禁止|不含|不加)"
    r"(?:[^.!?;；。\n]|\n(?!\s*(?:\n|[-*•\[]))){0,160}?(?:\b(?:BGM|background\s+music|music(?:\s+plays)?|instrumental(?:\s+music|\s+texture|\s+score)?|soundtrack|score)\b|配乐|背景音乐|伴奏|音乐|弦乐|钢琴曲)"
    r"|\b(?:soundtrack|audio)\s+(?:is\s+only|consists\s+(?:solely|only|entirely)\s+of|contains\s+only)\b"
    r"(?!(?:[^.!?;；。\n]|\n(?!\s*(?:\n|[-*•\[]))){0,140}?(?:\b(?:music|BGM|score|melody|piano|strings|cello|violin|synth|orchestral)\b|配乐|背景音乐|伴奏|弦乐|钢琴))"
    r"(?:[^.!?;；。\n]|\n(?!\s*(?:\n|[-*•\[]))){0,160}",
    re.IGNORECASE,
)
POSITIVE_MUSIC_RE = re.compile(
    r"\b(?:BGM|background\s+music|music\s+plays|instrumental\s+(?:music|score|texture)|soundtrack)\b"
    r"|(?:配乐|背景音乐|器乐伴奏|弦乐伴奏|钢琴伴奏|钢琴曲)"
    r"|\([^()\n]{0,120}?\b(?:music|melody|instrumental|piano|strings|cello|violin|synth|orchestral|bgm|ost|score)\b[^()\n]{0,120}?\)"
    r"|[（(][^（）()\n]{0,80}?(?:配乐|旋律|弦乐|钢琴|伴奏|器乐)[^（）()\n]{0,80}?[）)]",
    re.IGNORECASE,
)
NO_SUBTITLES_RE = re.compile(
    r"\b(?:no|without|exclude)\s+(?:visible\s+|burned[- ]in\s+|on[- ]screen\s+)?subtitles?\b"
    r"|\bsubtitles?\s*:\s*none\b|无字幕|不要字幕|不加字幕|不含字幕|禁止字幕|【[^】\n]+】",
    re.IGNORECASE,
)


def check_craft_heuristics(issues: list[Issue], text: str, mode: str) -> None:
    """Warn on field-observed prompt traps documented in desk-prompt-patterns.md."""

    bad_handle = UNSUPPORTED_HANDLE_RE.search(text)
    if bad_handle:
        add(
            issues,
            "warning",
            "UNSUPPORTED_HANDLE_SYNTAX",
            f"Un-normalized handle '{bad_handle.group(0)}' found; use active surface handles such as '@Image 1', '@Video 1', or '@Audio 1'.",
        )

    for excl_match in EXCLUSION_BLOCK_RE.finditer(text):
        body = excl_match.group("body") or ""
        excl_words = round(len(LATIN_WORD_RE.findall(body)) + 0.5 * len(CJK_CHAR_RE.findall(body)))
        if excl_words > BLOATED_EXCLUSION_WORDS_WARN:
            add(
                issues,
                "warning",
                "BLOATED_EXCLUSION_LIST",
                f"Exclusion block contains ~{excl_words} word-equivalents (recommended <= {BLOATED_EXCLUSION_WORDS_WARN} words / 3-5 hard rules). "
                "Seedance's decoder-only LLM text encoder processes the full prompt in one token stream, so long lists of banned props/garments/gestures inject those nouns into spatial MMDiT multi-modality self-attention; move wardrobe/prop invariance into affirmative character/scene locks.",
            )
            break

    if mode == "generation":
        morph_remainder = NEGATED_MORPH_RE.sub(" ", text)
        morph_match = POSITIVE_MORPH_RE.search(morph_remainder)
        if morph_match:
            add(
                issues,
                "warning",
                "MORPH_TOKEN_RISK",
                f"'{morph_match.group(0)}' can trigger slow mesh melting during transformations; prefer '闪切' ('flash-cut') with an impact flash and identical pose lock.",
            )

        stalemate_remainder = NEGATED_STALEMATE_RE.sub(" ", text)
        if STALEMATE_CLASH_RE.search(stalemate_remainder):
            add(
                issues,
                "warning",
                "STALEMATE_CLASH_ENDING",
                "Ending on a mutual clash/glare lock freezes the final beat into a generic split-screen stalemate; dedicate the last 4-5 shots to a decisive finishing chain (break projectile -> shatter guard & land clean hit -> wide knockdown -> winner lands in foreground with defeated opponent downed in background).",
            )

        pursuit_remainder = NEGATED_PASSIVE_PURSUIT_RE.sub(" ", text)
        for clause_match in PASSIVE_PURSUIT_SENTENCE_RE.finditer(pursuit_remainder):
            clause = clause_match.group(0)
            if not ACTIVE_CATCH_VERB_RE.search(clause):
                add(
                    issues,
                    "warning",
                    "PASSIVE_PURSUIT_RISK",
                    f"Passive pursuit phrasing ('{clause.strip()[:60]}...') renders as stiff upright jogging with passive arms; pair pursuit with active upper-body catch mechanics (lunging with cupped hands, sweeping arms, pulling vines) and a narrow miss.",
                )
                break

        if OPENING_SETTLE_IN_ACTION_RE.search(text):
            add(
                issues,
                "warning",
                "OPENING_SETTLE_IN_ACTION",
                "Putting a 'settling before the chase/fight/action' beat in Shot 1 wastes the first 2-3s standing still; open fast-paced clips in medias res on the immediate physical trigger.",
            )

        ranges = timeline_ranges(text)
        durations = [end - start for start, end in ranges if end > start]
        is_one_take = re.search(
            r"(?:\bShot\s+1|镜头\s*1)\s*[([（]\s*0\s*[-–—]\s*\d+\s*s\s*[)\]）]\s*[:：]\s*\[[^\]]*(?:one\s+continuous\s+take|一镜到底)",
            text,
            re.IGNORECASE,
        )
        if (
            len(durations) >= 5
            and sum(durations) >= 20.0
            and not is_one_take
            and not DIALOGUE_RE.search(text)
            and all(d >= 4.0 for d in durations[:-1])
        ):
            add(
                issues,
                "warning",
                "SLUGGISH_UNIFORM_TIMING",
                "All non-final timed shot windows are 4-6s long, which stretches action/chases into slow motion and causes early static holds. Prefer untimed 'Shot N' (8-12 readable cuts) with 'Cut as <action>' triggers, or accordion 1-3s windows with a <=3s final payoff.",
            )

    cel_unnegated = NEGATED_CEL_RE.sub(" ", text)
    airbrush_unnegated = NEGATED_AIRBRUSH_RE.sub(" ", text)
    if AIRBRUSH_PAINTERLY_RE.search(airbrush_unnegated) and CEL_OUTLINE_RE.search(cel_unnegated):
        add(
            issues,
            "warning",
            "AIRBRUSH_CEL_CONFLICT",
            "Mixing airbrushed/semi-realistic painterly style with 'cel-shaded'/'cel-painted'/'2D stylized anime' pulls non-anchor cuts into hard black outlines and flat cartoon fills.",
        )

    overact_unnegated = NEGATED_CARTOON_OVERACT_RE.sub(" ", text)
    overact_match = CARTOON_OVERACT_RE.search(overact_unnegated)
    if overact_match:
        add(
            issues,
            "warning",
            "CARTOON_OVERACTING_RISK",
            f"'{overact_match.group(0)}' can synthesize loud cartoon gasps or distort semi-realistic faces (bug-eyes / balloon cheeks); prefer grounded conversational delivery and natural micro-expressions.",
        )

    flattener_unnegated = NEGATED_PROSODY_FLATTENER_RE.sub(" ", text)
    flattener_match = PROSODY_FLATTENER_RE.search(flattener_unnegated)
    if flattener_match and DIALOGUE_RE.search(text):
        add(
            issues,
            "warning",
            "PROSODY_FLATTENER_RISK",
            f"'{flattener_match.group(0)}' flattens TTS prosody into a robotic monotone and freezes the face; use grounded conversational inflection instead.",
        )

    if SPLIT_DIALOGUE_CUT_RE.search(text):
        add(
            issues,
            "warning",
            "SPLIT_DIALOGUE_ACROSS_CUT",
            "A spoken sentence appears split across a '[Cut to]' boundary, which resets TTS prosody at the seam; keep each spoken sentence self-contained inside one on-camera shot.",
        )

    if STYLE_2D_RE.search(cel_unnegated):
        lens_remainder = NEGATED_LENS_RE.sub(" ", text)
        lens_match = LIVE_ACTION_LENS_RE.search(lens_remainder)
        if lens_match:
            add(
                issues,
                "warning",
                "STYLE_2D_LENS_CONFLICT",
                f"2D animation style combined with optical lens/DOF term '{lens_match.group(0)}' can pull renders toward 3D-CG or fake tilt-shift; use 2D layer/multiplane terms instead.",
            )


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
    if re.search(
        r"\b(?:three|four|five|six|seven|eight|nine|ten|\d+)\s+(?:times|actions?)\s+per\s+second\b"
        r"|\bflashing\s+(?:five|six|seven|eight|nine|ten|\d+)\s+times\s+consecutively\b"
        r"|每秒\s*(?:[三四五六七八九十]|\d+)\s*次|连闪[五六七八九十\d]+次",
        text,
        re.IGNORECASE,
    ):
        add(issues, "warning", "HIGH_FREQUENCY_ACTION", "Do not demand high-frequency repeated actions per second or 5+ consecutive flashes in one beat.")


def check_anchor_syntax(issues: list[Issue], text: str, anchor_mode: str) -> None:
    """Enforce standalone anchor declarations only for the strict role route."""

    if anchor_mode != "strict":
        return

    exact_line = re.compile(
        rf"^\s*(?P<handle>{IMAGE_HANDLE_PATTERN})\s+is\s+the\s+"
        r"(?P<role>first|last)\s+frame\.\s*$"
        rf"|^\s*(?P<cn_handle>{IMAGE_HANDLE_PATTERN})\s*(?:为|是)(?P<cn_role>首帧|尾帧)[。.]?\s*$",
        re.IGNORECASE,
    )
    required: set[tuple[str, int]] = set()
    satisfied: set[tuple[str, int]] = set()
    for line in text.splitlines():
        paired_pattern = re.compile(
            rf"(?P<handle>{IMAGE_HANDLE_PATTERN})[^\n]{{0,80}}?(?:\b(?P<role>first|last)\s+frame\b|(?P<cn_role>首帧|尾帧))",
            re.IGNORECASE,
        )
        pairs = list(paired_pattern.finditer(line))
        for match in pairs:
            mention = reference_mentions(match.group("handle"))[0]
            raw_role = (match.group("role") or match.group("cn_role") or "").lower()
            norm_role = "first" if raw_role in ("first", "首帧") else "last"
            required.add((norm_role, mention.effective_number))
        if not pairs:
            images = [mention for mention in reference_mentions(line) if mention.kind == "image"]
            roles = [role for role in ("first", "last") if f"{role} frame" in line.lower()]
            if "首帧" in line and "first" not in roles:
                roles.append("first")
            if "尾帧" in line and "last" not in roles:
                roles.append("last")
            if len(images) == 1 and len(roles) == 1:
                required.add((roles[0], images[0].effective_number))
        exact = exact_line.match(line)
        if exact:
            handle_str = exact.group("handle") or exact.group("cn_handle")
            raw_role = (exact.group("role") or exact.group("cn_role") or "").lower()
            norm_role = "first" if raw_role in ("first", "首帧") else "last"
            mention = reference_mentions(handle_str)[0]
            satisfied.add((norm_role, mention.effective_number))

    for role, number in sorted(required - satisfied):
        code = "WEAK_FIRST_FRAME_ROLE" if role == "first" else "WEAK_LAST_FRAME_ROLE"
        add(
            issues,
            "warning",
            code,
            f"Strict anchoring requires a standalone declaration such as '@Image {number} is the {role} frame.'",
        )


def check_target_duration(issues: list[Issue], target_duration: float | None, long_video: bool = False) -> None:
    if target_duration is None:
        return
    max_duration = 180.0 if long_video else 30.0
    if target_duration <= 0:
        add(issues, "error", "TARGET_DURATION_VALUE", "Target duration must be greater than zero seconds.")
    elif target_duration > max_duration:
        if long_video:
            add(
                issues,
                "error",
                "TARGET_DURATION_LIMIT",
                f"Target duration {target_duration:g}s exceeds the 180s Dreamina Long Video maximum; segment the story into multiple clips.",
            )
        else:
            add(
                issues,
                "error",
                "TARGET_DURATION_LIMIT",
                f"Target duration {target_duration:g}s exceeds the default 30s single-video maximum; segment the story into multiple clips or pass --long-video for Dreamina 30-180s Long Video mode.",
            )
        add(
            issues,
            "warning",
            "TARGET_DURATION_SEGMENTATION",
            f"Build a multi-clip plan with each generated segment at or below {max_duration:g} seconds, then join the approved clips.",
        )


def check_mode(issues: list[Issue], text: str, mode: str) -> None:
    low = text.lower()
    if mode == "edit":
        if "sole editing master" not in low and "唯一编辑主视频" not in text:
            add(issues, "error", "EDIT_MASTER", "Editing must define one source video as the sole editing master ('唯一编辑主视频').")
        if not (
            re.search(r"\b(edit|modify|replace|remove|add|insert|change)\b", low)
            or re.search(r"编辑|修改|替换|移除|删除|增加|添加|插入|改为|换成", text)
        ):
            add(issues, "error", "EDIT_TARGET", "Editing must name an edit operation and target.")
        if not (
            re.search(r"\b(only|within|scope|from \d|entire video|throughout)\b", low)
            or re.search(r"仅|只|范围|全片|整个视频|全程|在第?\s*\d", text)
        ):
            add(issues, "warning", "EDIT_SCOPE", "Define the edited object/category, interval or region, and quantity.")
        if not (
            re.search(r"\b(unchanged|remain unchanged|keep all other|except for)\b", low)
            or re.search(r"保持不变|不变|除.{1,40}外", text)
        ):
            add(issues, "error", "EDIT_PRESERVATION", "Close the edit scope by stating what remains unchanged.")
        if not (
            re.search(r"\b(inherits?|timeline|appearance timing|motion slot|event order)\b", low)
            or re.search(r"继承|时间线|出场时间|动作轨迹|事件顺序|运镜", text)
        ):
            add(issues, "warning", "EDIT_INHERITANCE", "State how the edit inherits the source timeline, motion, occlusion, and event order.")
    elif mode == "extension":
        has_source = "source video to extend" in low or bool(
            re.search(r"(?:待延长|要延长|用于延长)的?源视频|源视频[^\n。]{0,18}延长", text)
        )
        if not has_source:
            add(issues, "error", "EXTENSION_SOURCE", "Extension must identify one source video to extend.")
        forward = "extend forward" in low or bool(re.search(r"向后延长|往后延长|正向延长|向后续写", text))
        backward = "extend backward" in low or bool(re.search(r"向前延长|往前延长|反向延长|向前续写", text))
        if forward == backward:
            add(issues, "error", "EXTENSION_DIRECTION", "State exactly one direction: forward ('向后延长') or backward ('向前延长').")
        if forward and not (
            re.search(r"first frame of the extended segment.+last frame", low, re.DOTALL)
            or re.search(r"延长.{0,12}首帧.{0,30}(?:尾帧|最后一帧)", text, re.DOTALL)
        ):
            add(issues, "error", "FORWARD_BOUNDARY", "Forward extension must continue from the source video's last frame.")
        if backward and not (
            re.search(r"last frame of the extended segment.+first frame", low, re.DOTALL)
            or re.search(r"延长.{0,12}(?:尾帧|最后一帧).{0,30}首帧", text, re.DOTALL)
        ):
            add(issues, "error", "BACKWARD_BOUNDARY", "Backward extension must end at the source video's first frame.")
        if not (
            re.search(r"\b(without duplication|without duplicat|same continuous|single continuous|do not duplicate|no duplication)\b", low)
            or re.search(r"不重复|不分裂|同一连续|单一连续", text)
        ):
            add(issues, "warning", "EXTENSION_INSTANCE", "State that each subject remains one continuous instance without duplication or splitting.")
        if not (
            re.search(r"\b(audio state|audio environment|ambience|sound|dialogue|silence|audio)\b", low)
            or re.search(r"音频|环境音|声音|音效|对白|静音|无声", text)
        ):
            add(issues, "warning", "EXTENSION_AUDIO", "Describe audio continuity or an explicit silent state at the boundary.")
    if mode in ("edit", "extension") and EDIT_REF_TRAP_RE.search(text):
        add(
            issues,
            "warning",
            "EDIT_REFERENCE_TRAP",
            "Do not phrase the editing master or extension source as 'Reference @Video N' ('参考 <视频N>'); use 'Edit @Video N' or 'Extend @Video N' so the task router does not misclassify the job as ordinary reference generation.",
        )


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
    if DIALOGUE_RE.search(text) and not NO_SUBTITLES_RE.search(text):
        add(
            issues,
            "warning",
            "MISSING_NO_SUBTITLES",
            "Spoken dialogue is present without 'No subtitles.' (or explicit 【...】 subtitle binding); append 'No subtitles.' ('无字幕') to prevent burned-in caption artifacts.",
        )
    if not allow_music:
        music_remainder = text
        for _ in range(3):
            music_remainder = NEGATED_MUSIC_CLAUSE_RE.sub(" ", music_remainder)
        if POSITIVE_MUSIC_RE.search(music_remainder):
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
    long_video: bool = False,
    allow_music: bool = False,
    anchor_mode: str = "semantic",
    allow_template_placeholders: bool = False,
) -> tuple[str, list[Issue]]:
    selected_mode = infer_mode(text) if mode == "auto" else mode
    issues: list[Issue] = []
    handles = referenced_handles(text)
    check_counts(issues, handles, images, videos, audio, video_seconds, audio_seconds, mode=selected_mode)
    check_target_duration(issues, target_duration, long_video=long_video)
    check_roles(issues, text, handles)
    check_timeline(issues, text)
    check_dialogue_density(issues, text)
    check_negation_conflicts(issues, text)
    check_craft_heuristics(issues, text, selected_mode)
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

    # Bilingual Chinese edit routing & contract check (F07)
    cn_edit = """[编辑目标]
编辑 @视频1。在全片范围内，仅将快递员头盔替换为 @图片1 的复古铜制面罩头盔。
[源视频角色]
@视频1 为唯一编辑主视频，定义人物动作、机位运镜、遮挡关系、原始声音与事件顺序。
@图片1 仅定义铜制头盔结构；不要使用其背景。
[修改范围与保留]
仅修改这一顶头盔；除该头盔外，其余所有人物、服装、摩托车与霓虹街道背景均保持不变。
[时间线继承]
新头盔完整继承原头盔在 @视频1 时间线中的全部转头轨迹、反光与遮挡。"""
    cn_mode, cn_issues = lint(cn_edit, "auto", images=1, videos=1, audio=0, video_seconds=6.7)
    assert cn_mode == "edit", cn_mode
    assert not cn_issues, cn_issues

    # Bilingual Chinese forward extension routing & contract check (F07)
    cn_ext = """@视频1 为待延长的源视频。@图片1 仅定义隧道外的雪山河谷远景；不要使用其替换起始边界帧。
向后延长 @视频1。延长段首帧紧接 @视频1 的最后一帧，保持红色蒸汽火车的行驶速度、车侧跟拍机位、煤烟方向与铁轨轰鸣音频状态。
随后火车冲出隧道进入阳光山谷，全程保持同一连续火车个体不重复、不分裂，无配乐，无字幕。"""
    ext_mode, ext_issues = lint(cn_ext, "auto", images=1, videos=1, video_seconds=5.0)
    assert ext_mode == "extension", ext_mode
    assert not ext_issues, ext_issues

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

    # Stage N & 镜头 N decimal/gap headers (F08)
    stage_decimal = "Stage 1 (0-3.5s): A walks in.\nStage 2 (4.5-8s): A sits down."
    _, issues = lint(stage_decimal)
    assert {"DECIMAL_TIMESTAMP", "TIMELINE_GAP"}.issubset({i.code for i in issues}), issues

    not_a_timeline = "Use a 5-10 seconds subject-reference clip. Support ratios in the range 0.4-2.5."
    _, issues = lint(not_a_timeline)
    assert not {"INVALID_TIME_RANGE", "TIMELINE_GAP", "TIMELINE_OVERLAP"} & {i.code for i in issues}, issues

    two_reference_durations = "Use a 5-10 seconds subject clip and a 5-10 seconds voice clip."
    _, issues = lint(two_reference_durations)
    assert not {"INVALID_TIME_RANGE", "TIMELINE_GAP", "TIMELINE_OVERLAP"} & {i.code for i in issues}, issues

    _, issues = lint("@Image 31 defines a prop.", images=31)
    assert "IMAGE_LIMIT" in {i.code for i in issues}

    # Unflagged hard asset caps & edit video min duration (F08)
    _, issues = lint("@Image 40 defines only the hero's cloak; do not use its background.")
    assert "IMAGE_LIMIT" in {i.code for i in issues}, issues
    _, issues = lint(good_edit, "edit", images=1, videos=1, video_seconds=2.5)
    assert "EDIT_VIDEO_MIN_DURATION" in {i.code for i in issues}, issues

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
    _, issues = lint("Edit @Video 1. Within <whole video or exact scope>, change only <original object/region> from <A> to <B>.", "edit")
    assert "PLACEHOLDER" in {i.code for i in issues}, issues

    _, issues = lint("A complete but segmented story prompt.", target_duration=31)
    assert {"TARGET_DURATION_LIMIT", "TARGET_DURATION_SEGMENTATION"}.issubset({i.code for i in issues}), issues
    _, issues = lint("A complete Dreamina Long Video story prompt.", target_duration=120, long_video=True)
    assert "TARGET_DURATION_LIMIT" not in {i.code for i in issues}, issues
    _, issues = lint("An over-limit Long Video story prompt.", target_duration=181, long_video=True)
    assert "TARGET_DURATION_LIMIT" in {i.code for i in issues}, issues

    shot_headers = "Shot 1 (0-3s): A walks in.\nShot 2 (4-6s): A sits down."
    _, issues = lint(shot_headers)
    assert "TIMELINE_GAP" in {i.code for i in issues}, issues

    crowded = 'Shot 1 (0-3s): Sasha lifts the bag.\nSasha\'s line (excited): "Oh my god, look at this! Should we get it?"\nShot 2 (3-8s): Kira squints.\nKira\'s line (unsure): "Hmm, you think she\'ll like it?"'
    _, issues = lint(crowded)
    density = [i for i in issues if i.code == "DIALOGUE_DENSITY"]
    assert len(density) == 1 and "0-3s" in density[0].message, issues
    assert "MISSING_NO_SUBTITLES" in {i.code for i in issues}, issues

    # CJK & comma-quoted dialogue density (F07)
    cjk_crowded = "镜头 1 (0-2s): 守卫举起长矛喝道：“站住，深更半夜你们几个到底是什么人，快把通行腰牌拿出来检查！” 无字幕。"
    _, issues = lint(cjk_crowded)
    assert "DIALOGUE_DENSITY" in {i.code for i in issues}, issues
    assert "MISSING_NO_SUBTITLES" not in {i.code for i in issues}, issues

    comma_quote = 'Shot 1 (0-2s): Mara turns and says, "Wait right here until I check the cellar door Lock." No subtitles.'
    _, issues = lint(comma_quote)
    assert "DIALOGUE_DENSITY" in {i.code for i in issues}, issues

    braced = "0-2s: The guard speaks. {Halt, who goes there, stranger, at this hour?}"
    _, issues = lint(braced)
    assert "DIALOGUE_DENSITY" in {i.code for i in issues}, issues

    bare_quotes = 'Shot 1 (0-2s): A sign reads "Grand Opening Sale Today Only Everything Must Go Now".'
    _, issues = lint(bare_quotes)
    assert "DIALOGUE_DENSITY" not in {i.code for i in issues}, issues

    freeze_conflict = "Avoid: no slow motion, no freeze frames. Each blast gets a two-frame hit-stop."
    _, issues = lint(freeze_conflict)
    assert "NEGATION_CONFLICT" in {i.code for i in issues}, issues
    _, issues = lint("Avoid: no freeze frames.\n反应堆炸开，两帧定格，然后镜头加速。")
    assert "NEGATION_CONFLICT" in {i.code for i in issues}, issues
    _, issues = lint("Avoid: no slow motion. Speed ramp on every blast.")
    assert "NEGATION_CONFLICT" in {i.code for i in issues}, issues
    clean = "Avoid: no freeze frames. Each hit lands with an impact flash and a camera jolt. 两帧冲击停顿（不是定格）。"
    _, issues = lint(clean)
    assert "NEGATION_CONFLICT" not in {i.code for i in issues}, issues

    _, issues = lint("Reference @Video 1 and replace the lamp.", "edit", videos=1)
    assert "EDIT_REFERENCE_TRAP" in {i.code for i in issues}, issues
    _, issues = lint("参考 @Video 1 向后延长视频。", "extension", videos=1)
    assert "EDIT_REFERENCE_TRAP" in {i.code for i in issues}, issues
    _, issues = lint(good_edit, "edit", images=1, videos=1, audio=0)
    assert "EDIT_REFERENCE_TRAP" not in {i.code for i in issues}, issues

    _, issues = lint("女战士变形为机甲，冲向巨龙。")
    assert "MORPH_TOKEN_RISK" in {i.code for i in issues}, issues
    _, issues = lint("The warrior morphs into a giant obsidian mecha.")
    assert "MORPH_TOKEN_RISK" in {i.code for i in issues}, issues
    _, issues = lint("闪白 → 发光线稿 → 闪切 2D 漫画 → 落定为机甲。不要变形，no morphing.")
    assert "MORPH_TOKEN_RISK" not in {i.code for i in issues}, issues

    _, issues = lint("Hand-drawn 2D cel-shaded anime style. Medium close-up with creamy bokeh and shallow depth of field.")
    assert "STYLE_2D_LENS_CONFLICT" in {i.code for i in issues}, issues
    _, issues = lint("Hand-drawn 2D cel-shaded anime style over a painted gouache background. Avoid: no bokeh, no shallow depth of field.")
    assert "STYLE_2D_LENS_CONFLICT" not in {i.code for i in issues}, issues

    # Negated airbrush symmetry fix (F08)
    _, issues = lint("Pure 2D cel-shaded anime animation across the whole courtyard. Avoid: no airbrushed rendering, no semi-realistic shading.")
    assert "AIRBRUSH_CEL_CONFLICT" not in {i.code for i in issues}, issues
    _, issues = lint("Lineless airbrushed semi-realistic digital painting mixed with crisp 2D cel-shaded anime fills.")
    assert "AIRBRUSH_CEL_CONFLICT" in {i.code for i in issues}, issues

    # Room-tone foley whitelist & parenthetical/CJK music detection (F08)
    _, issues = lint("A potter shapes wet clay on a wheel in dawn light. The soundtrack consists solely of wet clay squelches, wheel hum, and quiet room tone.")
    assert "MUSIC_DEFAULT" not in {i.code for i in issues}, issues
    _, issues = lint("A lone traveller crosses the snowfield at dusk. (low cello melody swells softly)")
    assert "MUSIC_DEFAULT" in {i.code for i in issues}, issues
    _, issues = lint("黄昏雪原上旅人独行，远处响起低沉弦乐伴奏。")
    assert "MUSIC_DEFAULT" in {i.code for i in issues}, issues

    _, issues = lint("Dynamic tracking shot. Character <<<Image1>>> sprints across a roof.")
    assert "UNSUPPORTED_HANDLE_SYNTAX" in {i.code for i in issues}, issues
    _, issues = lint("Character @[ref1] enters the room.")
    assert "UNSUPPORTED_HANDLE_SYNTAX" in {i.code for i in issues}, issues
    _, issues = lint("参考 <视频1> 的运镜轨迹。")
    assert "UNSUPPORTED_HANDLE_SYNTAX" in {i.code for i in issues}, issues

    _, issues = lint('She inhales excitedly and speaks in a sing-song lilt: {"Hello there!"} No subtitles.')
    assert "CARTOON_OVERACTING_RISK" in {i.code for i in issues}, issues
    _, issues = lint('She speaks in a flat tone: {"Hello there."} No subtitles.')
    assert "PROSODY_FLATTENER_RISK" in {i.code for i in issues}, issues
    _, issues = lint('Shot 1: She speaks: {"Double the pumpkins, lock the moon—"} Cut as the drop falls.\n[Cut to]\nShot 2: Her voice continues: {"—Halloween stays till next June!"} No subtitles.')
    assert "SPLIT_DIALOGUE_ACROSS_CUT" in {i.code for i in issues}, issues

    overloaded_clip = 'Shot 1: {"Line one here."} Shot 2: {"Line two here."} Shot 3: {"Line three here."} Shot 4: {"Line four here."} No subtitles.'
    _, issues = lint(overloaded_clip)
    assert "CLIP_DIALOGUE_OVERLOAD" in {i.code for i in issues}, issues

    nested_one_take = """@Image 1 defines the streamer and her room.
Shot 1 (0-30s): [Front camera of her phone, one continuous take]
0-4s: She sits at her desk. {"Room tour. Try not."}
4-8s: She lifts the phone off its stand.
8-9s: One step brings her to the shelf.
9-13s: She presents the doll. {"She judges everyone."}
13-17s: She shows the jar. {"He is all smiles."}
17-21s: She leans by the portrait. {"Family resemblance."}
21-24s: She turns back. {"And the scariest? Me."}
24-25s: One second of total silence.
25-28s: Autofocus hunts and softens into blur.
28-30s: Focus snaps back onto her face. No subtitles."""
    _, issues = lint(nested_one_take, images=1)
    assert not {"TIMELINE_OVERLAP", "TIMELINE_GAP", "CLIP_DIALOGUE_OVERLOAD", "DIALOGUE_DENSITY"} & {i.code for i in issues}, issues

    scoped_ramp = "Avoid: no slow motion except one brief speed ramp at the final impact. Shot 15 (24-25s): Palm hits the floor with a brief speed ramp at contact."
    _, issues = lint(scoped_ramp)
    assert "NEGATION_CONFLICT" not in {i.code for i in issues}, issues

    mmss_and_pipe_headers = """0:00-0:04
Night walk.
0:04-0:07
Close-up of note.
0:08-0:10
Car drives away."""
    _, issues = lint(mmss_and_pipe_headers)
    assert "TIMELINE_GAP" in {i.code for i in issues}, issues

    comma_and_pipe_shots = "Shot 1 | 0-2s. First strike.\nShot 2, 2-4s. Second strike."
    assert timeline_ranges(comma_and_pipe_shots) == [(0.0, 2.0), (2.0, 4.0)]

    _, issues = lint("Shot 20: 红围巾角少年的赤金重拳与六眼黄袍法师的青金晶矛在两人面门之间硬生生对撞，红瞳与六只金竖瞳死死对视。")
    assert "STALEMATE_CLASH_ENDING" in {i.code for i in issues}, issues

    _, issues = lint("The fire spirit bolts across the grass and the forest nymph runs after him across the clearing.")
    assert "PASSIVE_PURSUIT_RISK" in {i.code for i in issues}, issues

    sluggish = "Shot 1 (0-5s): A.\nShot 2 (5-10s): B.\nShot 3 (10-15s): C.\nShot 4 (15-21s): D.\nShot 5 (21-27s): E.\nShot 6 (27-30s): F."
    _, issues = lint(sluggish)
    assert "SLUGGISH_UNIFORM_TIMING" in {i.code for i in issues}, issues

    _, issues = lint("Shot 1: Wide shot settling briefly on the clearing before the chase erupts.")
    assert "OPENING_SETTLE_IN_ACTION" in {i.code for i in issues}, issues

    slow_drama = """Shot 1 (0-6s): He sets the fork down.
Dialogue (the composer, low gravelly baritone, measured and unhurried): "So, Stephan."
Dialogue (after a brief pause): "Das Huhn ist gut."
Shot 2 (6-11s): Stephan nods once.
Dialogue (Stephan, calm baritone, quiet and measured): "Sehr gut, Herr van Beethoven."
Shot 3 (11-16s): He reaches for the cup.
Dialogue (the composer, slightly quieter, almost to himself): "Die Kartoffeln auch."
Dialogue (after a brief pause): "Nicht zu salzig."
Shot 4 (16-22s): He sets the cup down.
Dialogue (the composer, flat and matter-of-fact, a little louder): "Heute morgen war der Arzt da."
Shot 5 (22-28s): Stephan looks across the table.
Dialogue (Stephan, very quiet, careful): "Und?"
Dialogue (the composer, quiet, dry): "Wie immer."
[Audio]
No score, no\nsoundtrack, no ambient music. The soundtrack is only the two voices and room tone. No subtitles."""
    _, issues = lint(slow_drama)
    assert not {
        "CLIP_DIALOGUE_OVERLOAD",
        "DIALOGUE_DENSITY",
        "SLUGGISH_UNIFORM_TIMING",
        "MUSIC_DEFAULT",
        "MISSING_NO_SUBTITLES",
    } & {i.code for i in issues}, issues

    bloated_excl = (
        "Shot 1 (0-5s): A man sits at a table.\n[Strictly exclude]\n"
        + " ".join(["no modern props or extra plates or forks or spoons or knives"] * 9)
    )
    _, issues = lint(bloated_excl)
    assert "BLOATED_EXCLUSION_LIST" in {i.code for i in issues}, issues

    cn_bloated_excl = "镜头 1 (0-5s): 男子坐在桌前。\n[严格排除]\n" + "不要现代餐具、不要多余盘子叉子勺子、不要外套领结手杖、" * 12 + "\n[分镜]\n镜头 2 (5-8s): 他放下水杯。"
    _, issues = lint(cn_bloated_excl)
    assert "BLOATED_EXCLUSION_LIST" in {i.code for i in issues}, issues

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
    parser.add_argument(
        "--long-video",
        action="store_true",
        help="Allow 30-180s target duration for Dreamina web Long Video mode (default cap remains 30s)",
    )
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
        long_video=args.long_video,
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
