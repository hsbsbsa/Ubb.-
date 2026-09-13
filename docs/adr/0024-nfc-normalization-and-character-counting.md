# ADR-0024: NFC normalization and Korean character counting

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Length targets are in Korean characters "공백 포함"; offsets must be stable; combining jamo and width
variants break naive counts.

## Decision
Normalize all text to **Unicode NFC** at the API/gateway boundary. Character count = number of Unicode
code points after NFC, **including spaces and punctuation**, excluding markup/section headers and 상태창
block delimiters (block content counts). Report both "공백 포함" and "공백 제외" in the UI.

## Consequences
Single counting utility in `packages/domain`; tests with jamo/width edge cases.
