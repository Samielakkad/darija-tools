from darija_tools.arabizi import to_arabic


def test_lexicon_hits():
    assert to_arabic("bghit") == "بغيت"
    assert to_arabic("wach") == "واش"
    assert to_arabic("chnou") == "شنو"


def test_digit_letters():
    assert to_arabic("3") == "ع"
    assert to_arabic("9") == "ق"


def test_digraphs():
    assert to_arabic("kh") == "خ"
    assert to_arabic("gh") == "غ"


def test_rule_fallback_word():
    # not in the lexicon -> falls through to the char/digraph rules
    assert to_arabic("3lam") == "علام"


def test_separators_preserved():
    assert to_arabic("a-b") == "ا-ب"


def test_sentence():
    assert to_arabic("3lach bghiti daba") == "علاش بغيتي دبا"
