#!/usr/bin/env python3
"""Lint Suno v6 prompt packages (Style, Lyrics, Exclude) without external dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


STYLE_MAX_CHARS = 1000
LYRICS_MAX_CHARS = 5000

INLINE_NEGATION_RE = re.compile(
    r"\b(?:no\s+(?:drums|vocals|autotune|reverb|guitars|synths|bass|choir)|without\s+\w+|avoid\s+\w+|do\s+not\s+use)\b",
    re.IGNORECASE,
)

PROHIBITED_ARTIST_RE = re.compile(
    r"\b(?:taylor\s+swift|drake|the\s+weeknd|billie\s+eilish|ed\s+sheeran|nirvana|metallica|"
    r"daft\s+punk|skrillex|hans\s+zimmer|john\s+williams|miles\s+davis|miles-style|"
    r"peter-hook|peter\s+hook|larry-carlton|larry\s+carlton|bonham-style|john\s+bonham|"
    r"albini-style|steve\s+albini|scruggs-style|earl\s+scruggs|nile-style|nile\s+rodgers)\b",
    re.IGNORECASE,
)

TAG_LINE_RE = re.compile(r"^\s*(\[[^\]\n]+\])(.*)$")
CONTRADICTORY_TAGS = (
    ("calm", "aggressive"),
    ("whispered", "belted"),
    ("high energy", "low energy"),
)


def read_text(path: str | None) -> str:
    if not path:
        return ""
    return Path(path).read_text(encoding="utf-8")


def lint_style(style: str, require_bpm: bool = False) -> list[str]:
    errors: list[str] = []
    text = style.strip()
    if not text:
        errors.append("style must be non-empty")
        return errors
    if len(text) > STYLE_MAX_CHARS:
        errors.append(f"style is {len(text)} characters; maximum is {STYLE_MAX_CHARS}")
    neg_match = INLINE_NEGATION_RE.search(text)
    if neg_match:
        errors.append(
            f"style contains inline negation ({neg_match.group(0)!r}); move exclusions to Exclude"
        )
    artist_match = PROHIBITED_ARTIST_RE.search(text)
    if artist_match:
        errors.append(
            f"style contains prohibited artist/producer reference ({artist_match.group(0)!r})"
        )
    if require_bpm and not re.search(r"\b\d{2,3}\s*BPM\b", text, re.IGNORECASE):
        errors.append("style is missing an explicit BPM anchor (e.g., 110BPM)")
    return errors


def lint_lyrics(lyrics: str) -> list[str]:
    errors: list[str] = []
    text = lyrics.strip()
    if not text:
        errors.append("lyrics must be non-empty")
        return errors
    if len(text) > LYRICS_MAX_CHARS:
        errors.append(f"lyrics are {len(text)} characters; maximum is {LYRICS_MAX_CHARS}")
    artist_match = PROHIBITED_ARTIST_RE.search(text)
    if artist_match:
        errors.append(
            f"lyrics contain prohibited artist/producer reference ({artist_match.group(0)!r})"
        )

    for line_no, line in enumerate(text.splitlines(), start=1):
        match = TAG_LINE_RE.match(line)
        if match:
            tag_body = match.group(1).lower()
            trailing = match.group(2).strip()
            if trailing:
                errors.append(
                    f"lyrics line {line_no}: place section tag {match.group(1)} alone on its own line"
                )
            for left, right in CONTRADICTORY_TAGS:
                if left in tag_body and right in tag_body:
                    errors.append(
                        f"lyrics line {line_no}: section tag combines contradictory cues ({left!r} vs {right!r})"
                    )
        else:
            if re.search(r"\b24/7\b", line):
                errors.append(
                    f"lyrics line {line_no}: spell out '24/7' as 'twenty four seven' for clean vocal pronunciation"
                )
    return errors


def lint_exclude(exclude: str) -> list[str]:
    errors: list[str] = []
    text = exclude.strip()
    if not text:
        return errors
    if re.search(r"\b(?:do\s+not\s+be\s+generic|make\s+it\s+good)\b", text, re.IGNORECASE):
        errors.append("exclude must list concrete audible traits, not abstract instructions")
    artist_match = PROHIBITED_ARTIST_RE.search(text)
    if artist_match:
        errors.append(
            f"exclude contains prohibited artist/producer reference ({artist_match.group(0)!r})"
        )
    return errors


def run_self_test() -> int:
    cases: list[tuple[str, list[str], int]] = []

    good_style = (
        "Dreamy 80s synth-pop, 110BPM, vintage Juno-106 poly-synths, shimmering 16th-note "
        "arpeggios, ethereal female vocal, hazy nostalgic midnight mood, spacious Lexicon hall "
        "reverb, warm analog chorus modulation"
    )
    good_lyrics = (
        "[Cold Open | dry single voice]\n"
        "Your keys are still beside the sink\n\n"
        "[Chorus | drums drop out]\n"
        "We stay awake twenty four seven"
    )
    good_exclude = "stock risers, trap hi-hat rolls, supersaws, heavy autotune"

    cases.append(("valid 6-stage style", lint_style(good_style, require_bpm=True), 0))
    cases.append(("style inline negation", lint_style("Indie rock, 110BPM, no drums, warm vocal"), 1))
    cases.append(("style artist leak", lint_style("90s grunge, 118BPM, Nirvana and Albini-style room-mic"), 1))
    cases.append(("style missing BPM when required", lint_style("Warm synth pop, lush reverb", require_bpm=True), 1))
    cases.append(("style over 1000 chars", lint_style("x" * 1001), 1))

    cases.append(("valid lyrics", lint_lyrics(good_lyrics), 0))
    cases.append(("lyrics inline text after tag", lint_lyrics("[Verse 1] Walking down the street"), 1))
    cases.append(("lyrics contradictory tag", lint_lyrics("[Verse 1 | Calm, Aggressive]\nOne line"), 1))
    cases.append(("lyrics unexpanded 24/7", lint_lyrics("[Verse 1]\nWorking 24/7 on the line"), 1))

    cases.append(("valid exclude", lint_exclude(good_exclude), 0))
    cases.append(("exclude abstract instruction", lint_exclude("do not be generic, bad mix"), 1))

    failed = 0
    for name, errors, expected_min in cases:
        passed = (not errors) if expected_min == 0 else len(errors) >= expected_min
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}")
        if not passed:
            failed += 1
            for err in errors:
                print(f"  - {err}")
    print(f"Self-test: {len(cases) - failed}/{len(cases)} passed")
    return 1 if failed else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--style")
    parser.add_argument("--style-file")
    parser.add_argument("--lyrics")
    parser.add_argument("--lyrics-file")
    parser.add_argument("--exclude")
    parser.add_argument("--require-bpm", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()

    style = args.style or read_text(args.style_file)
    lyrics = args.lyrics or read_text(args.lyrics_file)
    exclude = args.exclude or ""

    if not (style or lyrics or exclude):
        print("ERROR: provide --style/--style-file, --lyrics/--lyrics-file, --exclude, or --self-test", file=sys.stderr)
        return 2

    errors: list[str] = []
    if style:
        errors.extend(lint_style(style, require_bpm=args.require_bpm))
    if lyrics:
        errors.extend(lint_lyrics(lyrics))
    if exclude:
        errors.extend(lint_exclude(exclude))

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    print("OK: Suno v6 prompt package passed lint checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
