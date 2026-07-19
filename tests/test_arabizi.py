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


def test_highfreq_lexicon_batch():
    # High-frequency words the char/digraph rules get wrong on their own:
    # `e` would insert a spurious ي, `3t` can't infer ط over ت, and a
    # trailing `-a` on these nouns is ة, not ا. The lexicon corrects them.
    assert to_arabic("sme3") == "سمع"
    assert to_arabic("3ti") == "عطي"
    assert to_arabic("3tini") == "عطيني"
    assert to_arabic("meskin") == "مسكين"
    assert to_arabic("meskina") == "مسكينة"
    assert to_arabic("khdma") == "خدمة"
    assert to_arabic("khedma") == "خدمة"


def test_highfreq_batch_is_case_insensitive():
    # Lexicon lookup lowercases first, so caps still resolve.
    assert to_arabic("Meskina") == "مسكينة"


def test_darija_lexicon_batch():
    # These forms need lexical context: the fallback cannot infer ة, omitted
    # vowels, or the conventional spelling of common nouns and phrases.
    expected = {
        "bslama": "بسلامة",
        "sahbi": "صاحبي",
        "chokran": "شكرا",
        "shokran": "شكرا",
        "zwina": "زوينة",
        "9hwa": "قهوة",
        "9ahwa": "قهوة",
        "qahwa": "قهوة",
        "bent": "بنت",
        "weld": "ولد",
        "rajel": "راجل",
    }
    for arabizi, arabic in expected.items():
        assert to_arabic(arabizi) == arabic


def test_darija_lexicon_batch_is_case_insensitive():
    assert to_arabic("BSLAMA SAHBI CHOKRAN ZWINA") == "بسلامة صاحبي شكرا زوينة"


def test_keep_loanwords_off_by_default():
    # Default behaviour unchanged: loanwords still get char-mangled.
    assert to_arabic("taxi") == "تاكسي"
    assert to_arabic("weekend") == "وييكيند"


def test_keep_loanwords_leaves_latin():
    assert to_arabic("taxi", keep_loanwords=True) == "taxi"
    assert to_arabic("weekend", keep_loanwords=True) == "weekend"
    assert to_arabic("internet", keep_loanwords=True) == "internet"


def test_keep_loanwords_is_case_insensitive():
    # Match lowercases, but the original casing is preserved in the output.
    assert to_arabic("WiFi", keep_loanwords=True) == "WiFi"
    assert to_arabic("Facebook", keep_loanwords=True) == "Facebook"


def test_keep_loanwords_in_sentence():
    # Darija words transliterate; the loanword stays Latin. Separators kept.
    assert to_arabic("bghit taxi", keep_loanwords=True) == "بغيت taxi"


def test_keep_loanwords_covers_common_code_switched_terms():
    terms = (
        "abonnement agenda ambulance appartement ascenseur autoroute bureau "
        "cadeau camera chantier chauffeur cinema clinique diplome ecole facture "
        "garage groupe imprimante logiciel machine pharmacie probleme programme "
        "projet quartier radio reunion service station"
    )
    assert to_arabic(terms, keep_loanwords=True) == terms


def test_keep_loanwords_does_not_touch_non_loanwords():
    # A non-loanword is transliterated as usual even with the flag on.
    assert to_arabic("bghit", keep_loanwords=True) == "بغيت"
