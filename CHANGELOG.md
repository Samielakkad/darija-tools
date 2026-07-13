# Changelog

All notable changes are documented here. The project follows Semantic Versioning.

## [Unreleased]

### Added

- Trusted PyPI publishing workflow with separated build/publish privileges,
  protected-environment support, and package attestations.
- Package metadata validation and wheel smoke tests in CI.
- Contribution, security, citation, issue, and pull request guidance.
- High-frequency lexicon mappings for greetings, family terms, adjectives,
  and common `9hwa` / `9ahwa` / `qahwa` spellings.

## [0.1.0] - 2026-07-13

### Added

- Arabic-script normalization with opt-in digit and whitespace handling.
- Heuristic Arabizi-to-Arabic transliteration with a curated word lexicon.
- Optional preservation of common French and English loanwords.
- Dependency-free `darija` command-line interface.
- Test matrix for Python 3.9 through 3.13.

[Unreleased]: https://github.com/Samielakkad/darija-tools/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Samielakkad/darija-tools/releases/tag/v0.1.0
