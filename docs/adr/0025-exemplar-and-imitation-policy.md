# ADR-0025: Exemplar sourcing and non-imitation policy

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Style must be learned without copying commercial works or living authors.

## Decision
Exemplars may come only from: the project's own accepted chapters, user-owned text with rights
confirmation, licensed text with license reference, or studio-authored synthetic passages. Prompts never
reference named authors/works as style targets. Genre overlays encode abstract conventions only.
Provenance is stored per exemplar; similarity screening added in Beta.

## Consequences
Cold start relies on synthetic + base rules until the project's exemplar bank grows (expected within
~10 accepted chapters).
