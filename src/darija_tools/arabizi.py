"""Heuristic Arabizi (Latin-script Darija) -> Arabic-script transliteration.

Approach: a curated lexicon of high-frequency Darija words is applied
first, then a transparent character / digraph rule table handles the
long tail. Arabizi spelling is not standardized (the same word has many
spellings), so this is lossy by design -- it targets the common cases,
not perfection. For unseen long-tail words and code-switched loanwords,
pair it with a neural transliterator or manual review (see README).
"""
from __future__ import annotations

import json
import re
from importlib import resources

# Digit "letters" used in Arabizi (e.g. 3 -> ع, 7 -> ح, 9 -> ق).
_DIGIT = {
    "2": "ء",
    "3": "ع",
    "5": "خ",
    "6": "ط",
    "7": "ح",
    "8": "غ",
    "9": "ق",
}

# Multi-character graphemes, checked before single letters.
_MULTI = [
    ("kh", "خ"),
    ("gh", "غ"),
    ("ch", "ش"),
    ("sh", "ش"),
    ("th", "ث"),
    ("dh", "ذ"),
    ("ou", "و"),
]

# Single-letter fallbacks.
_SINGLE = {
    "a": "ا", "b": "ب", "c": "ك", "d": "د", "e": "ي", "f": "ف",
    "g": "گ", "h": "ه", "i": "ي", "j": "ج", "k": "ك", "l": "ل",
    "m": "م", "n": "ن", "o": "و", "p": "پ", "q": "ق", "r": "ر",
    "s": "س", "t": "ت", "u": "و", "v": "ڤ", "w": "و", "x": "كس",
    "y": "ي", "z": "ز",
}

_TOKEN = re.compile(r"[A-Za-z0-9]+|[^A-Za-z0-9]+")


def _load_lexicon() -> dict:
    src = resources.files("darija_tools.data").joinpath("arabizi_lexicon.json")
    with src.open(encoding="utf-8") as fh:
        return json.load(fh)


_LEXICON = _load_lexicon()


def _map_word(word: str) -> str:
    key = word.lower()
    if key in _LEXICON:
        return _LEXICON[key]
    out = []
    i = 0
    while i < len(key):
        pair = key[i : i + 2]
        multi = next((ar for lat, ar in _MULTI if lat == pair), None)
        if multi is not None:
            out.append(multi)
            i += 2
            continue
        ch = key[i]
        out.append(_DIGIT.get(ch) or _SINGLE.get(ch) or ch)
        i += 1
    return "".join(out)


def to_arabic(text: str) -> str:
    """Transliterate Arabizi (Latin-script Darija) to Arabic script.

    Word tokens are mapped via the lexicon then the rule table; runs of
    separators (spaces, punctuation) are preserved unchanged.
    """
    return "".join(
        _map_word(tok) if tok[:1].isalnum() else tok
        for tok in _TOKEN.findall(text)
    )
