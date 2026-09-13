# ADR-0024: NFC normalization and Korean character counting

- **Status:** Superseded by ADR-0030 (addressing) and ADR-0034 (length)
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

> **Superseded.** NFC normalization stands; addressing is now specified as Unicode code points across all runtimes, and length uses a language-neutral model with words as the English author-facing unit.

## Context
Length targets are in Korean characters "공백 포함"; offsets must be stable; combining jamo and width
variants break naive counts.

## Decision
Normalize all text to **Unicode NFC** at the API/gateway boundary. Character count = number of Unicode
code points after NFC, **including spaces and punctuation**, excluding markup/section headers and 상태창
block delimiters (block content counts). Report both "공백 포함" and "공백 제외" in the UI.

## Consequences
Single counting utility in `packages/domain`; tests with jamo/width edge cases.
