# ADR-0030: One Unicode-safe text addressing system across all runtimes

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Evidence spans, patches, lint violations and UI highlights all address text by offsets. TypeScript
strings index UTF-16 code units, PostgreSQL `substring` on `text` counts code points, Python indexes code
points, and browsers work with DOM ranges — a mismatch corrupts evidence verification on any
non-BMP character (emoji, some CJK) and on combining sequences.

## Decision
All stored offsets are **Unicode code-point indices into the NFC-normalized text**, half-open
`[start, end)`. Implementations: PostgreSQL `substring(text from start+1 for end-start)` /
`char_length`; TypeScript via a code-point index (`Array.from(str)` or a cached code-point→UTF-16 offset
map in `packages/prose`), never raw `slice`; Python `str` slicing; browser highlights convert code-point
offsets to UTF-16 offsets before creating DOM ranges. Grapheme clusters are **not** the unit (they are
locale/version dependent); NFC normalization at ingestion keeps combining sequences stable. A shared
conformance test vector (ASCII, curly quotes, em dashes, emoji, combining marks, Hangul in registry names)
runs in every runtime.

## Consequences
Supersedes the addressing part of ADR-0024. Evidence trigger semantics are unambiguous; a small utility
package is mandatory in every runtime.
