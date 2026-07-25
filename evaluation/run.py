"""Reproduce the versioned Arabizi-to-Arabic evaluation report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from darija_tools import to_arabic

ROOT = Path(__file__).resolve().parent
DATASET = ROOT / "held_out_v0.2.jsonl"
REPORT = ROOT / "report-v0.2.md"


def load_cases() -> list[dict]:
    return [
        json.loads(line)
        for line in DATASET.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def percent(numerator: int, denominator: int) -> str:
    return f"{100 * numerator / denominator:.1f}%"


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def evaluate(cases: list[dict]) -> tuple[dict, list[dict]]:
    errors = []
    exact = 0
    matched_tokens = 0
    total_tokens = 0

    for case in cases:
        prediction = to_arabic(
            case["input"], keep_loanwords=case.get("keep_loanwords", False)
        )
        if prediction == case["expected"]:
            exact += 1
        else:
            errors.append({**case, "prediction": prediction})

        expected_tokens = case["expected"].split()
        predicted_tokens = prediction.split()
        total_tokens += max(len(expected_tokens), len(predicted_tokens))
        matched_tokens += sum(
            expected == predicted
            for expected, predicted in zip(expected_tokens, predicted_tokens)
        )

    metrics = {
        "cases": len(cases),
        "exact": exact,
        "tokens": total_tokens,
        "matched_tokens": matched_tokens,
    }
    return metrics, errors


def render_report(cases: list[dict]) -> str:
    metrics, errors = evaluate(cases)
    lines = [
        "# v0.2 transliteration evaluation",
        "",
        "This report evaluates `to_arabic()` on a versioned set kept separate",
        "from the unit tests. It is a small, manually curated regression benchmark,",
        "not a blinded study or an estimate for all Moroccan Darija.",
        "",
        "## Results",
        "",
        (
            f"- Phrase exact match: {metrics['exact']}/{metrics['cases']} "
            f"({percent(metrics['exact'], metrics['cases'])})"
        ),
        (
            f"- Whitespace-token exact match: {metrics['matched_tokens']}/"
            f"{metrics['tokens']} "
            f"({percent(metrics['matched_tokens'], metrics['tokens'])})"
        ),
        f"- Mismatched phrases: {len(errors)}",
        "",
        (
            "Run `python evaluation/run.py` to print this report, or use `--check` "
            "to verify the committed copy."
        ),
        "",
        "## Errors",
        "",
        "| ID | Category | Input | Expected | Predicted |",
        "| --- | --- | --- | --- | --- |",
    ]
    lines.extend(
        "| {id} | {category} | `{input}` | `{expected}` | `{prediction}` |".format(
            **{key: escape_cell(str(value)) for key, value in error.items()}
        )
        for error in errors
    )
    lines.extend(
        [
            "",
            "## Reading the failures",
            "",
            (
                "Most remaining errors need lexical context: unwritten vowels, the "
                "Arabic article, doubled consonants, or `ة` cannot be recovered "
                "reliably from a character table. These cases stay in the set so "
                "later releases can show an honest change rather than silently "
                "replacing difficult data."
            ),
            "",
            (
                "The JSONL file records the input, expected Arabic, category and "
                "whether curated Latin loanwords should be preserved. Changing an "
                "expected value requires a reviewable dataset diff."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    report = render_report(load_cases())
    if args.write_report:
        REPORT.write_text(report, encoding="utf-8")
    elif args.check:
        if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != report:
            raise SystemExit("evaluation/report-v0.2.md is out of date")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
