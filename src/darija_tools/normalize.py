"""Text normalization for Moroccan Darija / Arabic.

Normalization is the first step in almost any Darija NLP pipeline: it
collapses the orthographic variation that makes exact-match and search
brittle -- diacritics (tashkeel), the tatweel/kashida elongation mark,
and the alef / ya / ta-marbuta letter variants.
"""
from __future__ import annotations

import re
import unicodedata

# Harakat / tashkeel and related combining marks.
_DIACRITICS = re.compile(
    r"[ؐ-ًؚ-ٰٟۖ-ۜ۟-۪ۨ-ۭ]"
)
_TATWEEL = "ـ"  # ـ

# Fold common letter variants to a single canonical form.
_LETTER_UNIFY = {
    "آ": "ا",  # آ -> ا
    "أ": "ا",  # أ -> ا
    "إ": "ا",  # إ -> ا
    "ٱ": "ا",  # ٱ -> ا
    "ى": "ي",  # ى -> ي
    "ة": "ه",  # ة -> ه
}
_UNIFY_TABLE = {ord(k): v for k, v in _LETTER_UNIFY.items()}


def normalize(
    text: str,
    *,
    strip_diacritics: bool = True,
    strip_tatweel: bool = True,
    unify_letters: bool = True,
    form: str = "NFKC",
) -> str:
    """Return a normalized copy of ``text``.

    Args:
        text: input string (Arabic-script Darija/Arabic; Latin passes through).
        strip_diacritics: remove harakat and other combining marks.
        strip_tatweel: remove the kashida elongation character.
        unify_letters: fold alef/ya/ta-marbuta variants to a canonical form.
        form: Unicode normalization form applied first (default ``"NFKC"``);
            pass a falsy value to skip it.

    Returns:
        The normalized string.
    """
    if form:
        text = unicodedata.normalize(form, text)
    if strip_tatweel:
        text = text.replace(_TATWEEL, "")
    if strip_diacritics:
        text = _DIACRITICS.sub("", text)
    if unify_letters:
        text = text.translate(_UNIFY_TABLE)
    return text
