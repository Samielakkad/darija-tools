# darija-tools

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

### Arabizi transliteration

Latin-script Darija (`3lach`, `bghit`, `wach`) → Arabic script. A curated lexicon of high-frequency words is applied first, then a transparent rule table handles the long tail.

```python
>>> from darija_tools import to_arabic
>>> to_arabic("3lach bghiti daba")
'علاش بغيتي دبا'
```

### CLI

```bash
$ darija normalize "الأَحْمَر"
$ echo "3lach bghiti daba" | darija translit
```

## Honest limitations

- Arabizi spelling is **not standardized** — the same word has many spellings. The transliterator targets common cases, not perfection. It is a rule-based v0, not a neural model.
- **Loanwords are not detected.** French/English words common in Darija text (`plombier`, `weekend`) get run through the same rules and will need review. Loanword pass-through is on the roadmap.
- Coverage is Moroccan Darija first; other Maghrebi dialects overlap but aren't the target.

## Roadmap

- Grow the Arabizi lexicon (community-verifiable, one batch at a time)
- Loanword detection / pass-through
- Reverse transliteration (Arabic → Arabizi)
- Trade / city tagging for service-marketplace text
- Optional neural fallback for long-tail transliteration
- PyPI release

## License

MIT — see [LICENSE](LICENSE).
