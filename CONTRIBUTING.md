# Contributing

Contributions should make a real Darija NLP workflow more accurate, transparent, or usable.

## Development

```bash
git clone https://github.com/Samielakkad/darija-tools
cd darija-tools
python -m pip install -e ".[dev]"
python -m ruff check src tests
python -m pytest -q
python -m build
python -m twine check dist/*
```

## Language-data changes

Lexicon and rule changes must include:

- representative input and expected output examples;
- a source or concrete usage context for the proposed Darija form;
- tests for the new behavior and nearby edge cases;
- no copied dataset content unless its license permits redistribution.

Keep additions focused. A small, reviewable batch with evidence is preferred over a large unexplained word dump.

## Pull requests

Open an issue first for changes that alter public behavior. Pull requests must keep existing defaults compatible unless the issue explicitly approves a breaking change. CI must pass on every supported Python version.
