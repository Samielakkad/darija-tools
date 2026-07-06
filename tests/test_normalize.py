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
