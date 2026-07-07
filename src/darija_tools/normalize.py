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

# Fold Arabic-Indic (٠-٩, U+0660-0669) and Extended Arabic-Indic / Persian
# (۰-۹, U+06F0-06F9) digits to ASCII 0-9. NFKC does not touch these, so this
# is an opt-in extra rather than something ``form`` already covers.
_DIGITS_TABLE = {
    **{0x0660 + i: str(i) for i in range(10)},
    **{0x06F0 + i: str(i) for i in range(10)},
}


def normalize(
    text: str,
    *,
    strip_diacritics: bool = True,
    strip_tatweel: bool = True,
    unify_letters: bool = True,
    normalize_digits: bool = False,
    form: str = "NFKC",
) -> str:
    """Return a normalized copy of ``text``.

    Args:
        text: input string (Arabic-script Darija/Arabic; Latin passes through).
        strip_diacritics: remove harakat and other combining marks.
        strip_tatweel: remove the kashida elongation character.
        unify_letters: fold alef/ya/ta-marbuta variants to a canonical form.
        normalize_digits: fold Arabic-Indic and Extended Arabic-Indic (Persian)
            digits to ASCII 0-9. Off by default since it changes the digit
            script; NFKC does not do this on its own.
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
    if normalize_digits:
        text = text.translate(_DIGITS_TABLE)
    return text
