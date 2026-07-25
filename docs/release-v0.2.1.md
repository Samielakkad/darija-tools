# darija-tools 0.2.1

This patch release fixes command-line output on Windows terminals that start
with a legacy text encoding such as Windows-1252.

## Fixed

- `darija translit` and `darija normalize` now switch the output stream to
  UTF-8 when its current encoding cannot represent Arabic text.
- A regression test runs the CLI against a Windows-1252 output stream and
  checks the emitted UTF-8 bytes.

The library API and transliteration results are unchanged from 0.2.0.
