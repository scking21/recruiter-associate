#!/usr/bin/env python3
"""Prepare six downloaded ElevenLabs scene files for the existing demo.

The helper accepts one audio file per scene under ``public/audio-elevenlabs``
or one full narration file with five explicit cut offsets. It never edits
``script.json`` or the checked-in ``src/timing.json``. It normalizes each file
to 48 kHz mono PCM, derives contiguous scene timings from measured audio
durations with the original lead and tail, and writes a separate timing
manifest and caption sidecar. It does not call a provider and never
time-stretches audio.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


FPS = 30
LEAD_SECONDS = 0.60
TAIL_SECONDS = 0.73
LEAD_FRAMES = round(LEAD_SECONDS * FPS)
TAIL_FRAMES = round(TAIL_SECONDS * FPS)
SCENE_IDS = ("Intro", "Inputs", "Findings", "Validation", "Multiplayer", "Closing")
INPUT_EXTENSIONS = (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".webm")


class PreparationError(RuntimeError):
    """A local input, format, or timing contract failed."""


def run_checked(command: list[str], *, label: str) -> str:
    try:
        completed = subprocess.run(
            command,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as error:
        raise PreparationError(f"{label} requires {command[0]} on PATH") from error
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or "").strip().splitlines()
        suffix = detail[-1] if detail else "unknown command failure"
        raise PreparationError(f"{label} failed: {suffix}") from error
    return completed.stdout.strip()


def probe_duration(path: Path) -> float:
    raw = run_checked(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ],
        label=f"ffprobe {path.name}",
    )
    try:
        duration = float(raw)
    except ValueError as error:
        raise PreparationError(f"{path.name} has no numeric duration") from error
    if not math.isfinite(duration) or duration <= 0:
        raise PreparationError(f"{path.name} has invalid duration {duration!r}")
    return duration


def find_input(input_dir: Path, scene_id: str) -> Path:
    stem = scene_id.lower()
    matches = [
        input_dir / f"{stem}{extension}"
        for extension in INPUT_EXTENSIONS
        if (input_dir / f"{stem}{extension}").is_file()
    ]
    if not matches:
        expected = ", ".join(f"{stem}{extension}" for extension in INPUT_EXTENSIONS[:3])
        raise PreparationError(f"missing {scene_id} narration in {input_dir} (expected {expected} or another supported audio extension)")
    if len(matches) > 1:
        names = ", ".join(path.name for path in matches)
        raise PreparationError(f"multiple {scene_id} inputs found: {names}; keep exactly one")
    return matches[0]


def load_contract(project_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    script_path = project_dir / "script.json"
    timing_path = project_dir / "src" / "timing.json"
    try:
        script = json.loads(script_path.read_text(encoding="utf-8"))
        timing = json.loads(timing_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PreparationError(f"could not read script/timing contract: {error}") from error
    if not isinstance(script, list) or [item.get("id") for item in script] != list(SCENE_IDS):
        raise PreparationError("script.json must contain the six expected scenes in order")
    scenes = timing.get("scenes") if isinstance(timing, dict) else None
    if not isinstance(scenes, list) or [item.get("id") for item in scenes] != list(SCENE_IDS):
        raise PreparationError("src/timing.json must contain the six expected scenes in order")
    for item in script:
        phrases = item.get("phrases")
        if not isinstance(phrases, list) or not phrases or any(not isinstance(text, str) or not text.strip() for text in phrases):
            raise PreparationError(f"{item['id']} must have nonempty narration phrases")
    return script, scenes, timing


def normalize_audio(source: Path, target: Path, start: float | None = None, end: float | None = None) -> None:
    command = ["ffmpeg", "-v", "error", "-y", "-i", str(source)]
    if start is not None and end is not None:
        command.extend(["-ss", f"{start:.6f}", "-t", f"{end - start:.6f}"])
    command.extend(
        [
            "-map",
            "0:a:0",
            "-vn",
            "-af",
            "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-ar",
            "48000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(target),
        ]
    )
    run_checked(
        command,
        label=f"normalize {source.name}",
    )


def caption_chunks(phrases: list[str]) -> list[str]:
    chunks: list[str] = []
    for phrase in phrases:
        words = phrase.split()
        chunks.extend(" ".join(words[index : index + 11]) for index in range(0, len(words), 11))
    return chunks


def proportional_captions(phrases: list[str], start: int, duration: int) -> list[dict[str, Any]]:
    chunks = caption_chunks(phrases)
    if not chunks:
        return []
    weights = [max(1, len(chunk.split())) for chunk in chunks]
    total_weight = sum(weights)
    raw_lengths = [duration * weight / total_weight for weight in weights]
    lengths = [max(1, math.floor(value)) for value in raw_lengths]
    while sum(lengths) > duration:
        index = max(range(len(lengths)), key=lambda item: (lengths[item], -item))
        if lengths[index] == 1:
            raise PreparationError("caption duration is too short for the narration text")
        lengths[index] -= 1
    while sum(lengths) < duration:
        index = max(range(len(lengths)), key=lambda item: (raw_lengths[item] - lengths[item], -item))
        lengths[index] += 1
    output: list[dict[str, Any]] = []
    cursor = start
    for text, length in zip(chunks, lengths):
        output.append({"from": cursor, "to": cursor + length, "text": text})
        cursor += length
    return output


def timestamp(frame: int) -> str:
    milliseconds = round(frame / FPS * 1000)
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, millis = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"


def parse_cuts(raw: str, duration: float) -> list[float]:
    parts = [part.strip() for part in raw.split(",") if part.strip()]
    if len(parts) != len(SCENE_IDS) - 1:
        raise PreparationError(f"--cuts requires exactly five comma-separated seconds, got {len(parts)}")
    try:
        cuts = [float(part) for part in parts]
    except ValueError as error:
        raise PreparationError("--cuts must contain numeric seconds") from error
    if any(not math.isfinite(cut) for cut in cuts):
        raise PreparationError("--cuts must contain finite seconds")
    if any(cut <= 0 or cut >= duration for cut in cuts):
        raise PreparationError(f"--cuts must fall strictly inside the full narration duration ({duration:.3f}s)")
    if any(right <= left for left, right in zip(cuts, cuts[1:])):
        raise PreparationError("--cuts must be strictly increasing")
    boundaries = [0.0, *cuts, duration]
    if any((right - left) < 0.1 for left, right in zip(boundaries, boundaries[1:])):
        raise PreparationError("each full-track scene segment must be at least 0.1 seconds")
    return cuts


def write_json(path: Path, value: Any, *, force: bool) -> None:
    if path.exists() and not force:
        raise PreparationError(f"refusing to overwrite {path}; pass --force after reviewing it")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, help="download directory (default: video/public/audio-elevenlabs)")
    parser.add_argument("--full-input", type=Path, help="one full narration file; combine with --cuts")
    parser.add_argument("--cuts", help="five strictly increasing full-track cut times in seconds, comma-separated")
    parser.add_argument("--output-dir", type=Path, help="normalized WAV directory (default: video/public/audio-elevenlabs-normalized)")
    parser.add_argument("--timing-out", type=Path, help="derived timing JSON (default: video/src/timing.elevenlabs.json)")
    parser.add_argument("--srt-out", type=Path, help="derived caption sidecar (default: video/output/roletrace-demo.elevenlabs.srt)")
    parser.add_argument("--force", action="store_true", help="replace generated outputs after reviewing the inputs")
    args = parser.parse_args(argv)

    project_dir = Path(__file__).resolve().parent
    input_dir = (args.input_dir or project_dir / "public" / "audio-elevenlabs").resolve()
    output_dir = (args.output_dir or project_dir / "public" / "audio-elevenlabs-normalized").resolve()
    timing_out = (args.timing_out or project_dir / "src" / "timing.elevenlabs.json").resolve()
    srt_out = (args.srt_out or project_dir / "output" / "roletrace-demo.elevenlabs.srt").resolve()

    try:
        for executable in ("ffmpeg", "ffprobe"):
            if shutil.which(executable) is None:
                raise PreparationError(f"{executable} is required on PATH")
        script, visual_scenes, _original_timing = load_contract(project_dir)
        if args.full_input is not None and args.input_dir is not None:
            raise PreparationError("use either --full-input or --input-dir, not both")
        if args.full_input is not None and not args.cuts:
            raise PreparationError("--full-input requires --cuts")
        if args.full_input is None and args.cuts:
            raise PreparationError("--cuts requires --full-input")
        if args.full_input is not None:
            full_input = args.full_input.resolve()
            if not full_input.is_file():
                raise PreparationError(f"full narration does not exist: {full_input}")
            full_duration = probe_duration(full_input)
            cuts = parse_cuts(args.cuts, full_duration)
            boundaries = [0.0, *cuts, full_duration]
            input_paths = {scene_id: full_input for scene_id in SCENE_IDS}
            trim_windows = {
                scene_id: (boundaries[index], boundaries[index + 1])
                for index, scene_id in enumerate(SCENE_IDS)
            }
            input_mode = "full_track_explicit_cuts"
            source_dir = os.path.relpath(full_input.parent, project_dir)
        else:
            if not input_dir.is_dir():
                raise PreparationError(f"input directory does not exist: {input_dir}")
            input_paths = {item["id"]: find_input(input_dir, item["id"]) for item in script}
            trim_windows = {scene_id: (None, None) for scene_id in SCENE_IDS}
            cuts = None
            input_mode = "per_scene_files"
            source_dir = os.path.relpath(input_dir, project_dir)
        if output_dir.exists() and not output_dir.is_dir():
            raise PreparationError(f"output path is not a directory: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)
        target_paths = {scene_id: output_dir / f"{scene_id.lower()}.wav" for scene_id in SCENE_IDS}
        if not args.force:
            existing = [str(path) for path in (*target_paths.values(), timing_out, srt_out) if path.exists()]
            if existing:
                raise PreparationError("refusing to overwrite generated output(s): " + ", ".join(existing) + "; pass --force after reviewing them")

        temp_paths: dict[str, Path] = {}
        try:
            for scene_id, source in input_paths.items():
                handle = tempfile.NamedTemporaryFile(prefix=f".{scene_id.lower()}.", suffix=".wav", dir=output_dir, delete=False)
                temporary = Path(handle.name)
                handle.close()
                temp_paths[scene_id] = temporary
                start, end = trim_windows[scene_id]
                normalize_audio(source, temporary, start, end)

            normalized_durations = {scene_id: probe_duration(path) for scene_id, path in temp_paths.items()}
            script_by_id = {item["id"]: item for item in script}
            generated_scenes: list[dict[str, Any]] = []
            captions: list[dict[str, Any]] = []
            report: list[dict[str, Any]] = []
            scene_cursor = 0
            for scene_id in SCENE_IDS:
                duration_frames = math.ceil(normalized_durations[scene_id] * FPS)
                scene_start = scene_cursor
                scene_duration = LEAD_FRAMES + duration_frames + TAIL_FRAMES
                clip_start = scene_start + LEAD_FRAMES
                scene_captions = proportional_captions(script_by_id[scene_id]["phrases"], clip_start, duration_frames)
                captions.extend(scene_captions)
                generated_scenes.append(
                    {
                        "id": scene_id,
                        "from": scene_start,
                        "duration": scene_duration,
                        "clips": [
                            {
                                "src": f"audio-elevenlabs-normalized/{scene_id.lower()}.wav",
                                "from": clip_start,
                                "duration": duration_frames,
                                "text": " ".join(script_by_id[scene_id]["phrases"]),
                            }
                        ],
                    }
                )
                report.append(
                    {
                        "id": scene_id,
                        "input": input_paths[scene_id].name,
                        "trim_seconds": None if trim_windows[scene_id][0] is None else [
                            round(trim_windows[scene_id][0], 3),
                            round(trim_windows[scene_id][1], 3),
                        ],
                        "duration_seconds": round(normalized_durations[scene_id], 3),
                        "scene_from_frame": scene_start,
                        "scene_duration_frames": scene_duration,
                        "audio_duration_frames": duration_frames,
                    }
                )
                scene_cursor += scene_duration

            if scene_cursor < 60 * FPS:
                raise PreparationError(
                    f"combined replacement narration is {scene_cursor / FPS:.3f}s; "
                    "all six scenes together must be at least 60 seconds"
                )

            generated_timing = {
                "duration": scene_cursor,
                "fps": FPS,
                "scenes": generated_scenes,
                "captions": captions,
                "audio_replacement": {
                    "input_mode": input_mode,
                    "source_dir": source_dir,
                    "normalized_dir": os.path.relpath(output_dir, project_dir),
                    "full_track_cuts_seconds": None if cuts is None else [round(cut, 3) for cut in cuts],
                    "lead_seconds": LEAD_SECONDS,
                    "tail_seconds": TAIL_SECONDS,
                    "caption_alignment": "proportional_by_word_count_approximate",
                    "time_stretch": False,
                },
            }
            srt = "\n\n".join(
                f"{index}\n{timestamp(item['from'])} --> {timestamp(item['to'])}\n{item['text']}"
                for index, item in enumerate(captions, start=1)
            ) + "\n"
            write_json(timing_out, generated_timing, force=args.force)
            if srt_out.exists() and not args.force:
                raise PreparationError(f"refusing to overwrite {srt_out}; pass --force after reviewing it")
            srt_out.parent.mkdir(parents=True, exist_ok=True)
            srt_out.write_text(srt, encoding="utf-8")
            for scene_id, temporary in temp_paths.items():
                os.replace(temporary, target_paths[scene_id])
        finally:
            for temporary in temp_paths.values():
                temporary.unlink(missing_ok=True)
    except (OSError, PreparationError, json.JSONDecodeError) as error:
        print(f"elevenlabs preparation refused: {error}", file=sys.stderr)
        return 2

    print(json.dumps({"timing": str(timing_out), "captions": str(srt_out), "scenes": report}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
