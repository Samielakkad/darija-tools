"""Command-line interface for darija-tools."""
from __future__ import annotations

import argparse
import sys

from . import __version__
from .arabizi import to_arabic, to_arabizi
from .normalize import normalize


def _print_text(value: str) -> None:
    """Print Unicode text even when Windows starts with a legacy code page."""
    encoding = getattr(sys.stdout, "encoding", None)
    if encoding is not None:
        try:
            value.encode(encoding)
        except UnicodeEncodeError:
            reconfigure = getattr(sys.stdout, "reconfigure", None)
            if reconfigure is None:
                raise
            reconfigure(encoding="utf-8")
    print(value)


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
    p_norm.add_argument(
        "--normalize-digits",
        action="store_true",
        help="fold Arabic-Indic and Persian digits to ASCII",
    )
    p_norm.add_argument(
        "--collapse-whitespace",
        action="store_true",
        help="collapse whitespace runs and trim the result",
    )

    p_tr = sub.add_parser("translit", help="Arabizi (Latin) -> Arabic script")
    p_tr.add_argument("text", nargs="?", help="text (reads stdin if omitted)")
    p_tr.add_argument(
        "--keep-loanwords",
        action="store_true",
        help="preserve curated French and English loanwords in Latin script",
    )

    p_rev = sub.add_parser("arabizi", help="Arabic script -> canonical Arabizi")
    p_rev.add_argument("text", nargs="?", help="text (reads stdin if omitted)")

    args = parser.parse_args(argv)
    text = args.text if args.text is not None else sys.stdin.read().rstrip("\n")

    if args.command == "normalize":
        _print_text(
            normalize(
                text,
                normalize_digits=args.normalize_digits,
                collapse_whitespace=args.collapse_whitespace,
            )
        )
    elif args.command == "translit":
        _print_text(to_arabic(text, keep_loanwords=args.keep_loanwords))
    else:  # arabizi
        _print_text(to_arabizi(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
