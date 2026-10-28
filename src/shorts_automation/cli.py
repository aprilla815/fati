from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import ConfigError, load_job
from .render import render


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shorts", description="Dikey kısa video iş akışı")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Video tanımını doğrula")
    validate_parser.add_argument("config", type=Path)

    render_parser = subparsers.add_parser("render", help="MP4 video üret")
    render_parser.add_argument("config", type=Path)
    render_parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        job = load_job(args.config)
        if args.command == "validate":
            print(f"Geçerli: {job.slug} ({len(job.scenes)} sahne, {job.duration:.1f} sn)")
            return 0
        output = args.output or Path("output") / f"{job.slug}.mp4"
        result = render(job, output)
        print(f"Oluşturuldu: {result}")
        return 0
    except (ConfigError, RuntimeError) as exc:
        print(f"Hata: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
