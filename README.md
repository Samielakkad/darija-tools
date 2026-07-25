# darija-tools

[![CI](https://github.com/Samielakkad/darija-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/Samielakkad/darija-tools/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/darija-tools)](https://pypi.org/project/darija-tools/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Small, dependency-free text utilities for Moroccan Darija (الدارجة). The rules and word lists are plain files that can be reviewed and tested.

## Install

```bash
pip install darija-tools
```

Python 3.9 or newer is supported.

## Use it

```python
from darija_tools import normalize, to_arabic, to_arabizi

normalize("الأَحْمَر")
# 'الاحمر'

to_arabic("3lach bghiti daba")
# 'علاش بغيتي دبا'

to_arabizi("علاش بغيتي دبا")
# '3lach bghiti daba'
```

`to_arabic()` checks a curated Darija word list, then uses letter and digraph rules for unknown words. Set `keep_loanwords=True` to leave recognized French and English loanwords in Latin script:

```python
to_arabic("bghit taxi", keep_loanwords=True)
# 'بغيت taxi'
```

`to_arabizi()` uses the same lexicon in reverse and chooses one stable spelling when a word has several valid Arabizi forms. Unknown Arabic words use a readable character mapping.

## Command line

```bash
darija normalize "الأَحْمَر"
darija translit "3lach bghiti daba"
darija translit --keep-loanwords "bghit taxi"
darija arabizi "علاش بغيتي دبا"
```

Omit the text argument to read from standard input.

## Evaluation

The v0.2 Arabizi-to-Arabic evaluation contains 30 phrases kept outside the unit tests:

- Phrase exact match: **26/30 (86.7%)**
- Whitespace-token exact match: **61/66 (92.4%)**

The [dataset](https://github.com/Samielakkad/darija-tools/blob/v0.2.0/evaluation/held_out_v0.2.jsonl), [full error report](https://github.com/Samielakkad/darija-tools/blob/v0.2.0/evaluation/report-v0.2.md) and [evaluation script](https://github.com/Samielakkad/darija-tools/blob/v0.2.0/evaluation/run.py) are checked in. CI regenerates the result and fails if the committed report differs.

This is a small, manually curated regression set, not a blinded study or a claim about all Darija text. The four failed phrases remain visible in the report.

## Limits

- Arabizi spelling is not standardized, so transliteration is lossy in both directions.
- Character rules cannot reliably recover unwritten vowels, doubled consonants or word endings.
- Loanword preservation covers a small reviewed list and is opt-in.
- The target is Moroccan Darija; overlap with other Maghrebi dialects is incidental.

## Development

```bash
python -m pip install -e ".[dev]"
python -m ruff check src tests evaluation
python -m pytest -q
python evaluation/run.py --check
python -m build
python -m twine check dist/*
```

See [CONTRIBUTING.md](https://github.com/Samielakkad/darija-tools/blob/main/CONTRIBUTING.md) before changing language rules or data. v0.2 changes are summarized in the [release notes](https://github.com/Samielakkad/darija-tools/blob/v0.2.0/docs/release-v0.2.md).

## License

MIT. See [LICENSE](https://github.com/Samielakkad/darija-tools/blob/main/LICENSE).
