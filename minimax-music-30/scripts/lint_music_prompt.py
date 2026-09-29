#!/usr/bin/env python3
"""Validate MiniMax Music 3 prompt packages without external dependencies."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


SURFACES = ("hosted", "sglang", "diffusers", "comfyui", "prompt-only")
TAG_LINE = re.compile(r"^\s*(\[[^\]\n]+\])(.*)$")
STRUCTURED_HEADINGS = ("Global Metadata", "Vocal Details", "Arrangement")

HOSTED_MODELS = {
    "music-3.0",
    "music-3.0-free",
    "music-cover",
    "music-cover-free",
}
HOSTED_SAMPLE_RATES = {16000, 24000, 32000, 44100}
HOSTED_BITRATES = {32000, 64000, 128000, 256000}
HOSTED_FORMATS = {"mp3", "wav", "pcm"}
LOCAL_REJECTED = {
    "temperature",
    "top_p",
    "top_k",
    "repetition_penalty",
    "ref_audio",
    "ref_text",
    "language",
    "task_type",
}


def read_text(path: str | None) -> str:
    if not path:
        return ""
    return Path(path).read_text(encoding="utf-8")


def type_name(value: Any) -> str:
    return type(value).__name__


def lint_tag_lines(lyrics: str) -> list[str]:
    errors: list[str] = []
    for number, line in enumerate(lyrics.splitlines(), start=1):
        match = TAG_LINE.match(line)
        if match and match.group(2).strip():
            errors.append(
                f"lyrics line {number}: put {match.group(1)} alone on its line; "
                "text after a leading tag can be dropped"
            )
    return errors


def lint_structured_caption(caption: str, require: bool) -> list[str]:
    errors: list[str] = []
    positions = [caption.find(heading) for heading in STRUCTURED_HEADINGS]
    if require and any(position < 0 for position in positions):
        missing = [
            heading
            for heading, position in zip(STRUCTURED_HEADINGS, positions)
            if position < 0
        ]
        errors.append("caption missing structured sections: " + ", ".join(missing))
    if all(position >= 0 for position in positions) and positions != sorted(positions):
        errors.append(
            "structured caption sections must appear in this order: "
            + " -> ".join(STRUCTURED_HEADINGS)
        )
    return errors


def lint_hosted(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    allowed = {
        "model",
        "prompt",
        "lyrics",
        "stream",
        "output_format",
        "audio_setting",
        "lyrics_optimizer",
        "is_instrumental",
        "audio_url",
        "audio_base64",
        "cover_feature_id",
    }
    local_only = {"input", "instructions", "seed", "max_new_tokens", "audio_duration"}
    leaked = sorted(local_only.intersection(payload))
    if leaked:
        errors.append("hosted payload contains local-only fields: " + ", ".join(leaked))
    unknown = sorted(set(payload).difference(allowed))
    if unknown:
        errors.append("hosted payload contains undocumented fields: " + ", ".join(unknown))

    model = payload.get("model")
    if model not in HOSTED_MODELS:
        errors.append(f"hosted model must be one of {sorted(HOSTED_MODELS)}; got {model!r}")
        return errors

    prompt = payload.get("prompt", "")
    lyrics = payload.get("lyrics", "")
    if not isinstance(prompt, str):
        errors.append(f"prompt must be a string; got {type_name(prompt)}")
        prompt = ""
    if not isinstance(lyrics, str):
        errors.append(f"lyrics must be a string; got {type_name(lyrics)}")
        lyrics = ""

    if model.startswith("music-cover"):
        if not 10 <= len(prompt) <= 300:
            errors.append("cover prompt must contain 10-300 characters")
        direct = [key for key in ("audio_url", "audio_base64") if payload.get(key)]
        feature = bool(payload.get("cover_feature_id"))
        if feature and direct:
            errors.append("cover_feature_id is mutually exclusive with audio_url/audio_base64")
        if not feature and len(direct) != 1:
            errors.append("cover request needs exactly one of audio_url or audio_base64")
        if feature and not 10 <= len(lyrics) <= 1000:
            errors.append("cover_feature_id requests require lyrics of 10-1000 characters")
        if lyrics and not 10 <= len(lyrics) <= 1000:
            errors.append("cover lyrics must contain 10-1000 characters")
    else:
        instrumental = payload.get("is_instrumental") is True
        optimizer = payload.get("lyrics_optimizer") is True
        if len(prompt) > 2000:
            errors.append(f"hosted prompt is {len(prompt)} characters; maximum is 2000")
        if instrumental:
            if not 1 <= len(prompt) <= 2000:
                errors.append("hosted instrumental prompt must contain 1-2000 characters")
            if lyrics.strip():
                errors.append("hosted instrumental request should omit lyrics")
        elif not lyrics.strip() and not optimizer:
            errors.append("hosted vocal request needs lyrics or lyrics_optimizer: true")
        if lyrics and not 1 <= len(lyrics) <= 3500:
            errors.append("hosted vocal lyrics must contain 1-3500 characters")

    if lyrics:
        errors.extend(lint_tag_lines(lyrics))

    stream = payload.get("stream", False)
    output_format = payload.get("output_format", "hex")
    if not isinstance(stream, bool):
        errors.append("stream must be a boolean")
    if output_format not in {"url", "hex"}:
        errors.append("output_format must be 'url' or 'hex'")
    if stream is True and output_format != "hex":
        errors.append("hosted streaming supports only output_format: 'hex'")

    setting = payload.get("audio_setting")
    if setting is not None:
        if not isinstance(setting, dict):
            errors.append("audio_setting must be an object")
        else:
            rate = setting.get("sample_rate")
            bitrate = setting.get("bitrate")
            fmt = setting.get("format")
            if rate is not None and rate not in HOSTED_SAMPLE_RATES:
                errors.append(f"unsupported hosted sample_rate: {rate!r}")
            if bitrate is not None and bitrate not in HOSTED_BITRATES:
                errors.append(f"unsupported hosted bitrate: {bitrate!r}")
            if fmt is not None and fmt not in HOSTED_FORMATS:
                errors.append(f"unsupported hosted audio format: {fmt!r}")
    return errors


def lint_sglang(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    allowed = {
        "model",
        "input",
        "instructions",
        "seed",
        "max_new_tokens",
        "response_format",
        "stream",
        "voice",
        "speed",
    }
    forbidden = sorted(LOCAL_REJECTED.intersection(payload))
    if forbidden:
        errors.append("SGLang Music 3 rejects: " + ", ".join(forbidden))
    hosted_only = {"prompt", "lyrics", "lyrics_optimizer", "is_instrumental", "audio_setting"}
    leaked = sorted(hosted_only.intersection(payload))
    if leaked:
        errors.append("SGLang payload contains hosted-only fields: " + ", ".join(leaked))
    unknown = sorted(set(payload).difference(allowed | LOCAL_REJECTED))
    if unknown:
        errors.append("SGLang payload contains undocumented fields: " + ", ".join(unknown))

    model = payload.get("model")
    if not isinstance(model, str) or not model.strip():
        errors.append("SGLang payload needs a non-empty model")
    lyrics = payload.get("input")
    caption = payload.get("instructions")
    if not isinstance(lyrics, str) or not lyrics.strip():
        errors.append("SGLang input must contain non-empty lyrics or an instrumental placeholder")
    else:
        errors.extend(lint_tag_lines(lyrics))
    if not isinstance(caption, str) or not caption.strip():
        errors.append("SGLang instructions must contain a non-empty caption")

    seed = payload.get("seed", 0)
    if not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed <= (2**64 - 1):
        errors.append("seed must be a non-negative 64-bit integer")
    frames = payload.get("max_new_tokens", 9000)
    if not isinstance(frames, int) or isinstance(frames, bool) or not 1 <= frames <= 9000:
        errors.append("max_new_tokens must be an integer from 1 to 9000")
    if payload.get("stream", False) is not False:
        errors.append("SGLang Music 3 requires stream: false")
    if payload.get("response_format", "wav") != "wav":
        errors.append("SGLang Music 3 response_format must be 'wav'")
    if "voice" in payload and payload["voice"] not in (None, "", "default"):
        errors.append("SGLang Music 3 has no selectable voice; describe vocals in instructions")
    if "speed" in payload and payload["speed"] != 1.0:
        errors.append("SGLang Music 3 accepts only speed 1.0; put BPM in instructions")
    return errors


def lint_diffusers(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    allowed = {
        "prompt",
        "lyrics",
        "audio_duration",
        "seed",
        "num_inference_steps",
        "output",
        "output_type",
    }
    unknown = sorted(set(payload).difference(allowed))
    if unknown:
        errors.append("Diffusers payload contains unsupported wrapper fields: " + ", ".join(unknown))
    prompt = payload.get("prompt")
    lyrics = payload.get("lyrics")
    if not isinstance(prompt, str) or not prompt.strip():
        errors.append("Diffusers prompt must be non-empty")
    if not isinstance(lyrics, str) or not lyrics.strip():
        errors.append("Diffusers lyrics must be non-empty; use the local instrumental placeholder")
    else:
        errors.extend(lint_tag_lines(lyrics))
    duration = payload.get("audio_duration", 60.0)
    if not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration <= 0:
        errors.append("audio_duration must be a positive number")
    elif duration > 300:
        errors.append("audio_duration exceeds the supported five-minute creative limit")
    seed = payload.get("seed")
    if seed is not None and (not isinstance(seed, int) or isinstance(seed, bool) or seed < 0):
        errors.append("Diffusers seed must be a non-negative integer")
    return errors


def lint_request(surface: str, payload: dict[str, Any]) -> list[str]:
    if surface == "hosted":
        return lint_hosted(payload)
    if surface == "sglang":
        return lint_sglang(payload)
    if surface == "diffusers":
        return lint_diffusers(payload)
    return [f"request JSON validation is not implemented for surface {surface!r}"]


def frames_for_seconds(seconds: float) -> int:
    if seconds <= 0:
        raise ValueError("seconds must be positive")
    return min(9000, math.ceil(seconds * 25))


def run_self_test() -> int:
    cases: list[tuple[str, list[str], int]] = []

    good_lyrics = "[Verse]\nOne clear line\n[Chorus]\nOne clear hook"
    good_caption = "Global Metadata\nPop.\nVocal Details\nAlto.\nArrangement\nVerse to chorus."
    cases.append(("good tag lines", lint_tag_lines(good_lyrics), 0))
    cases.append(("bad tag line", lint_tag_lines("[Verse] Lost words"), 1))
    cases.append(("ordered caption", lint_structured_caption(good_caption, True), 0))
    cases.append(("missing caption section", lint_structured_caption("Global Metadata", True), 1))

    hosted_good = {
        "model": "music-3.0",
        "prompt": "Warm acoustic pop",
        "lyrics": good_lyrics,
        "output_format": "url",
        "audio_setting": {"sample_rate": 44100, "bitrate": 256000, "format": "mp3"},
    }
    cases.append(("hosted valid", lint_hosted(hosted_good), 0))
    hosted_leak = dict(hosted_good, seed=7)
    cases.append(("hosted local leak", lint_hosted(hosted_leak), 1))
    hosted_long = dict(hosted_good, prompt="x" * 2001)
    cases.append(("hosted prompt length", lint_hosted(hosted_long), 1))
    hosted_instrumental = {
        "model": "music-3.0",
        "prompt": "Instrumental ambient, no vocals",
        "is_instrumental": True,
    }
    cases.append(("hosted instrumental", lint_hosted(hosted_instrumental), 0))

    sglang_good = {
        "model": "MiniMaxAI/MiniMax-Music3",
        "input": good_lyrics,
        "instructions": "Warm acoustic pop",
        "seed": 7,
        "max_new_tokens": 750,
        "response_format": "wav",
        "stream": False,
    }
    cases.append(("sglang valid", lint_sglang(sglang_good), 0))
    cases.append(("sglang bad stream", lint_sglang(dict(sglang_good, stream=True)), 1))
    cases.append(("sglang rejected sampling", lint_sglang(dict(sglang_good, temperature=0.8)), 1))
    cases.append(("duration math", [] if frames_for_seconds(30) == 750 else ["math"], 0))
    cases.append(("duration clamp", [] if frames_for_seconds(500) == 9000 else ["clamp"], 0))

    diffusers_good = {
        "prompt": "Warm acoustic pop",
        "lyrics": good_lyrics,
        "audio_duration": 60.0,
        "seed": 7,
    }
    cases.append(("diffusers valid", lint_diffusers(diffusers_good), 0))
    cases.append(("diffusers too long", lint_diffusers(dict(diffusers_good, audio_duration=301)), 1))

    failed = 0
    for name, errors, expected_minimum in cases:
        passed = (not errors) if expected_minimum == 0 else len(errors) >= expected_minimum
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}")
        if not passed:
            failed += 1
            for error in errors:
                print(f"  - {error}")
    print(f"Self-test: {len(cases) - failed}/{len(cases)} passed")
    return 1 if failed else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--surface", choices=SURFACES)
    parser.add_argument("--caption-file")
    parser.add_argument("--lyrics-file")
    parser.add_argument("--request-json")
    parser.add_argument("--require-structured-caption", action="store_true")
    parser.add_argument("--seconds-to-frames", type=float)
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()
    if args.seconds_to_frames is not None:
        try:
            print(frames_for_seconds(args.seconds_to_frames))
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        return 0
    if not args.surface:
        print("ERROR: --surface is required unless using --self-test or --seconds-to-frames", file=sys.stderr)
        return 2

    errors: list[str] = []
    caption = read_text(args.caption_file)
    lyrics = read_text(args.lyrics_file)
    if args.caption_file:
        require = args.require_structured_caption or args.surface in {"comfyui", "prompt-only"}
        errors.extend(lint_structured_caption(caption, require))
        if args.surface == "hosted" and len(caption) > 2000:
            errors.append(f"hosted caption is {len(caption)} characters; maximum is 2000")
    if args.lyrics_file:
        errors.extend(lint_tag_lines(lyrics))
        if args.surface == "hosted" and len(lyrics) > 3500:
            errors.append(f"hosted lyrics are {len(lyrics)} characters; maximum is 3500")
        if args.surface in {"sglang", "diffusers"} and not lyrics.strip():
            errors.append("local open-weight lyrics must be non-empty")

    if args.request_json:
        try:
            payload = json.loads(read_text(args.request_json))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot read request JSON: {exc}")
        else:
            if not isinstance(payload, dict):
                errors.append("request JSON root must be an object")
            else:
                errors.extend(lint_request(args.surface, payload))

    if not (args.caption_file or args.lyrics_file or args.request_json):
        print("ERROR: provide --caption-file, --lyrics-file, or --request-json", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: MiniMax Music 3 prompt package passed validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
