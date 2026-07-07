from darija_tools.normalize import normalize


def test_strips_diacritics_and_unifies_alef():
    assert normalize("الأَحْمَر") == "الاحمر"


def test_removes_tatweel():
    assert normalize("كتـــب") == "كتب"


def test_taa_marbuta_folds_to_haa():
    assert normalize("مدينة") == "مدينه"


def test_unify_letters_can_be_disabled():
    assert normalize("أحمد", unify_letters=False) == "أحمد"


def test_is_idempotent():
    once = normalize("الأَحْمَر")
    assert normalize(once) == once


def test_latin_passes_through():
    assert normalize("Casa 2026") == "Casa 2026"


def test_digits_are_kept_by_default():
    # Arabic-Indic digits survive unless normalize_digits is asked for.
    assert normalize("٢٠٢٦") == "٢٠٢٦"


def test_normalize_arabic_indic_digits():
    assert normalize("٢٠٢٦", normalize_digits=True) == "2026"


def test_normalize_extended_arabic_indic_digits():
    # Extended Arabic-Indic (Persian) range U+06F0-06F9.
    assert normalize("۰۱۲۳۴۵۶۷۸۹", normalize_digits=True) == "0123456789"


def test_normalize_digits_leaves_ascii_and_letters():
    assert normalize("طريق ٧ km", normalize_digits=True) == "طريق 7 km"
