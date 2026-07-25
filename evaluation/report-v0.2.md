# v0.2 transliteration evaluation

This report evaluates `to_arabic()` on a versioned set kept separate
from the unit tests. It is a small, manually curated regression benchmark,
not a blinded study or an estimate for all Moroccan Darija.

## Results

- Phrase exact match: 26/30 (86.7%)
- Whitespace-token exact match: 61/66 (92.4%)
- Mismatched phrases: 4

Run `python evaluation/run.py` to print this report, or use `--check` to verify the committed copy.

## Errors

| ID | Category | Input | Expected | Predicted |
| --- | --- | --- | --- | --- |
| ending-01 | word ending | `khdma mzyana` | `خدمة مزيانة` | `خدمة مزيانا` |
| request-03 | request | `3afak 3tini lma` | `عفاك عطيني الما` | `عافاك عطيني لما` |
| negation-01 | negation | `ma3reftch` | `معرفتش` | `ماعريفتش` |
| direction-01 | direction | `sir ldar` | `سير للدار` | `سير لدار` |

## Reading the failures

Most remaining errors need lexical context: unwritten vowels, the Arabic article, doubled consonants, or `ة` cannot be recovered reliably from a character table. These cases stay in the set so later releases can show an honest change rather than silently replacing difficult data.

The JSONL file records the input, expected Arabic, category and whether curated Latin loanwords should be preserved. Changing an expected value requires a reviewable dataset diff.
