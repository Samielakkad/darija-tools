# darija-tools

[![CI](https://github.com/Samielakkad/darija-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/Samielakkad/darija-tools/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Small, honest NLP utilities for Moroccan Darija (الدارجة). Built out of the text-normalization and transliteration code I kept re-writing while shipping [jak.ma](https://jak.ma), a live Darija service marketplace.

Darija is the everyday language of ~37M people but is under-served by mainstream Arabic NLP, which targets Modern Standard Arabic. This is the small, dependency-free layer that comes up first in almost any Darija pipeline.

## Install

From source (PyPI release planned):

```bash
git clone https://github.com/Samielakkad/darija-tools
cd darija-tools
pip install -e .
```

Pure Python, no runtime dependencies.

## What's in it

### Normalization

Collapse the orthographic noise that makes Arabic-script matching brittle — diacritics (tashkeel), tatweel/kashida, and alef / ya / ta-marbuta variants.

```python
>>> from darija_tools import normalize
>>> normalize("الأَحْمَر")
'الاحمر'
```

Digit folding is opt-in — Arabic-Indic (`٠-٩`) and Persian (`۰-۹`) digits map to ASCII only when you ask, since NFKC leaves them alone:

```python
>>> normalize("طريق ٧", normalize_digits=True)
'طريق 7'
```

### Arabizi transliteration

Latin-script Darija (`3lach`, `bghit`, `wach`) → Arabic script. A curated lexicon of high-frequency words is applied first, then a transparent rule table handles the long tail.

```python
>>> from darija_tools import to_arabic
>>> to_arabic("3lach bghiti daba")
'علاش بغيتي دبا'
```

Code-switched loanwords (French/English words Darija speakers keep in Latin) otherwise get mangled character-by-character. Opt in to `keep_loanwords=True` to leave a curated set of them untouched:

```python
>>> to_arabic("bghit taxi")                       # default: char rules mangle it
'بغيت تاكسي'
>>> to_arabic("bghit taxi", keep_loanwords=True)  # loanword left in Latin
'بغيت taxi'
```

The loanword set is small and non-exhaustive by design; off by default so existing behaviour is unchanged.

### CLI

```bash
$ darija normalize "الأَحْمَر"
$ darija normalize --normalize-digits --collapse-whitespace "  طريق ٧  "
$ darija translit --keep-loanwords "bghit taxi"
$ echo "3lach bghiti daba" | darija translit
```

All three optional library behaviours are available in the CLI: digit folding
and whitespace collapsing under `normalize`, and curated loanword preservation
under `translit`. They remain off by default to preserve the library defaults.

## Honest limitations

- Arabizi spelling is **not standardized** — the same word has many spellings. The transliterator targets common cases, not perfection. It is a rule-based v0, not a neural model.
- **Loanword coverage is partial.** `keep_loanwords=True` leaves a curated set of common French/English loanwords (`taxi`, `weekend`, `internet`, …) in Latin, but the set is small and non-exhaustive — anything outside it still runs through the rules and will need review.
- Coverage is Moroccan Darija first; other Maghrebi dialects overlap but aren't the target.

## Roadmap

- Grow the Arabizi lexicon (community-verifiable, one batch at a time)
- Grow the loanword set (`keep_loanwords` shipped; set is still small)
- Reverse transliteration (Arabic → Arabizi)
- Trade / city tagging for service-marketplace text
- Optional neural fallback for long-tail transliteration
- PyPI release

## License

MIT — see [LICENSE](LICENSE).
