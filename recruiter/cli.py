from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .presentation import render_markdown
from .workflow import build_guarded_prompt, bundle_mode, load_json, parse_response, validate_response, write_or_validate


def prepare(input_path: Path, output_dir: Path) -> int:
    bundle = load_json(input_path)
    mode = bundle_mode(bundle)
    prompt = build_guarded_prompt(bundle)
    snapshot = json.dumps(bundle, indent=2, sort_keys=True) + "\n"
    write_or_validate(output_dir / f"input.{mode}.json", snapshot)
    prompt_name = "evidence-review.prompt.txt" if mode == "real" else "guarded.prompt.txt"
    write_or_validate(output_dir / prompt_name, prompt)
    print(output_dir / prompt_name)
    return 0


def validate(input_path: Path, response_path: Path, output_path: Path | None) -> int:
    bundle = load_json(input_path)
    response = parse_response(response_path.read_text(encoding="utf-8"))
    report = validate_response(bundle, response)
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if output_path is not None:
        write_or_validate(output_path, text)
    print(text, end="")
    return 0 if report["valid"] else 2


def render(
    input_path: Path,
    response_path: Path,
    output_path: Path,
    previous_input_path: Path | None = None,
    previous_response_path: Path | None = None,
) -> int:
    bundle = load_json(input_path)
    response = parse_response(response_path.read_text(encoding="utf-8"))
    previous_bundle = load_json(previous_input_path) if previous_input_path is not None else None
    previous_response = (
        parse_response(previous_response_path.read_text(encoding="utf-8"))
        if previous_response_path is not None
        else None
    )
    text = render_markdown(bundle, response, previous_bundle, previous_response)
    write_or_validate(output_path, text)
    print(output_path)
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Prepare and validate bounded recruiter evidence reviews offline.")
    commands = root.add_subparsers(dest="command", required=True)
    prepare_parser = commands.add_parser("prepare", help="write an immutable guarded prompt and input snapshot")
    prepare_parser.add_argument("--input", type=Path, required=True)
    prepare_parser.add_argument("--output-dir", type=Path, required=True)
    validate_parser = commands.add_parser("validate", help="validate a returned JSON recommendation")
    validate_parser.add_argument("--input", type=Path, required=True)
    validate_parser.add_argument("--response", type=Path, required=True)
    validate_parser.add_argument("--output", type=Path)
    render_parser = commands.add_parser("render", help="write an immutable Markdown review for a validated real response")
    render_parser.add_argument("--input", type=Path, required=True)
    render_parser.add_argument("--response", type=Path, required=True)
    render_parser.add_argument("--output", type=Path, required=True)
    render_parser.add_argument("--previous-input", type=Path)
    render_parser.add_argument("--previous-response", type=Path)
    return root


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "prepare":
            return prepare(args.input, args.output_dir)
        if args.command == "validate":
            return validate(args.input, args.response, args.output)
        return render(args.input, args.response, args.output, args.previous_input, args.previous_response)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
        print(f"error: {error}")
        return 2
