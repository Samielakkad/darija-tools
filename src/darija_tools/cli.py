"""Command-line interface for darija-tools."""
from __future__ import annotations

import argparse
import sys

from . import __version__
from .arabizi import to_arabic
from .normalize import normalize


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="darija", description="Moroccan Darija text tools."
    )
    parser.add_argument(
        "--version", action="version", version=f"darija-tools {__version__}"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_norm = sub.add_parser("normalize", help="normalize Arabic-script text")
    p_norm.add_argument("text", nargs="?", help="text (reads stdin if omitted)")

    p_tr = sub.add_parser("translit", help="Arabizi (Latin) -> Arabic script")
    p_tr.add_argument("text", nargs="?", help="text (reads stdin if omitted)")

    args = parser.parse_args(argv)
    text = args.text if args.text is not None else sys.stdin.read().rstrip("\n")

    if args.command == "normalize":
        print(normalize(text))
    else:  # translit
        print(to_arabic(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
