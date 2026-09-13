# ADR-0022: Immutable manuscript versions with span addressing

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Evidence spans, patches, retcons and rollbacks all need stable references to text.

## Decision
Never edit manuscript text in place; every change is a new version with parent link; exactly one
`accepted` version per chapter; evidence spans are `(version_id, start, end, quote, hash)` verified by a DB
trigger; NFC normalization at ingestion so offsets are stable.

## Consequences
Storage grows with versions (acceptable: text is small); retention policy for non-accepted versions.
