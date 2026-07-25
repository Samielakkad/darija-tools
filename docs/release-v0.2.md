# darija-tools 0.2.0

v0.2 adds the reverse transliteration path and makes the existing direction measurable.

## Added

- `to_arabizi()` converts Arabic-script Darija to one stable Arabizi spelling.
- `darija arabizi` exposes the same operation in the command line.
- A 30-phrase Arabizi-to-Arabic evaluation set is stored separately from the unit tests.
- CI checks the generated accuracy and error report on every change.
- PyPI trusted publishing builds from the tagged commit without a stored API token.

## Evaluation

The frozen v0.2 set scores 26/30 exact phrases (86.7%) and 61/66 exact whitespace-delimited tokens (92.4%). It is a small manually curated regression set, not a population benchmark. All four mismatches are listed in `evaluation/report-v0.2.md`.

## Compatibility

Existing `normalize()` and `to_arabic()` behavior is unchanged. The new public function and command are additive. Python 3.9 through 3.13 remain supported, with no runtime dependencies.

## Known limits

Reverse transliteration is deterministic but cannot reconstruct vowels that are absent from Arabic script. Forward character rules still miss some word endings, articles, doubled consonants and spelling variants; use the error report to see concrete examples.
