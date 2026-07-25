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
_ARABIC_LETTERS = r"\u0621-\u063a\u0641-\u064a\u0671-\u06d3\u0750-\u077f"
_ARABIC_WORD = re.compile(rf"[{_ARABIC_LETTERS}]+")
_ARABIC_TOKEN = re.compile(rf"[{_ARABIC_LETTERS}]+|[^{_ARABIC_LETTERS}]+")

# Canonical, readable output for Arabic letters not covered by the word lexicon.
# Arabic short vowels are usually unwritten, so reverse transliteration is also
# lossy. The choices here favor common Moroccan Arabizi spellings.
_ARABIC_SINGLE = {
    "ء": "2",
    "ؤ": "w",
    "ئ": "y",
    "أ": "a",
    "إ": "i",
    "آ": "a",
    "ٱ": "a",
    "ا": "a",
    "ب": "b",
    "ت": "t",
    "ث": "th",
    "ج": "j",
    "چ": "ch",
    "ح": "7",
    "خ": "kh",
    "د": "d",
    "ذ": "dh",
    "ر": "r",
    "ز": "z",
    "ژ": "j",
    "س": "s",
    "ش": "ch",
    "ص": "s",
    "ض": "d",
    "ط": "6",
    "ظ": "d",
    "ع": "3",
    "غ": "gh",
    "ف": "f",
    "ق": "9",
    "ك": "k",
    "ک": "k",
    "ل": "l",
    "م": "m",
    "ن": "n",
    "ه": "h",
    "ة": "a",
    "و": "w",
    "ى": "a",
    "ي": "y",
    "پ": "p",
    "ڤ": "v",
    "گ": "g",
    "ڭ": "g",
    "ݣ": "g",
}


def _load_lexicon() -> dict:
    src = resources.files("darija_tools.data").joinpath("arabizi_lexicon.json")
    with src.open(encoding="utf-8") as fh:
        return json.load(fh)


def _load_loanwords() -> frozenset[str]:
    src = resources.files("darija_tools.data").joinpath("loanwords.json")
    with src.open(encoding="utf-8") as fh:
        return frozenset(w.lower() for w in json.load(fh))


_LEXICON = _load_lexicon()
_REVERSE_LEXICON = {}
for _arabizi, _arabic in _LEXICON.items():
    # JSON order defines the canonical spelling when several Arabizi spellings
    # map to the same Arabic word (for example, wach/wash).
    _REVERSE_LEXICON.setdefault(_arabic, _arabizi)

# French / English loanwords that Darija speakers commonly write in Latin
# script inside otherwise-Arabizi text (e.g. "taxi", "weekend", "internet").
# Small and non-exhaustive by design -- see `keep_loanwords` in `to_arabic`.
_LOANWORDS = _load_loanwords()


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


def to_arabic(text: str, *, keep_loanwords: bool = False) -> str:
    """Transliterate Arabizi (Latin-script Darija) to Arabic script.

    Word tokens are mapped via the lexicon then the rule table; runs of
    separators (spaces, punctuation) are preserved unchanged.

    When ``keep_loanwords`` is True, tokens that match the curated loanword
    set (French/English words Darija speakers keep in Latin, e.g. "taxi",
    "weekend") are left untouched instead of being transliterated
    character-by-character into garbled Arabic. Off by default so existing
    behaviour is unchanged. The set is small and non-exhaustive.
    """
    return "".join(
        _render_token(tok, keep_loanwords) if tok[:1].isalnum() else tok
        for tok in _TOKEN.findall(text)
    )


def _render_token(word: str, keep_loanwords: bool) -> str:
    if len(word) > 1 and word.isdecimal():
        return word
    if keep_loanwords and word.lower() in _LOANWORDS:
        return word
    return _map_word(word)


def to_arabizi(text: str) -> str:
    """Transliterate Arabic-script Darija to a canonical Arabizi spelling.

    Known words use the reverse of the curated lexicon. Unseen Arabic words use
    a deterministic letter table. Punctuation, whitespace, numbers and existing
    Latin text are preserved. Diacritics and tatweel are ignored.
    """
    from .normalize import normalize

    text = normalize(text, unify_letters=False)
    return "".join(
        _map_arabic_word(token) if _starts_with_arabic(token) else token
        for token in _ARABIC_TOKEN.findall(text)
    )


def _starts_with_arabic(token: str) -> bool:
    return _ARABIC_WORD.fullmatch(token) is not None


def _map_arabic_word(word: str) -> str:
    if word in _REVERSE_LEXICON:
        return _REVERSE_LEXICON[word]
    return "".join(_ARABIC_SINGLE.get(char, char) for char in word)
