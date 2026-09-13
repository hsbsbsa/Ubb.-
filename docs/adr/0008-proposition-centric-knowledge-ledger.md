# ADR-0008: Proposition-centric knowledge ledger

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Regression, hidden identity, misunderstandings and intrigue require knowing what each character knows,
suspects, falsely believes or pretends — over time, with sources.

## Decision
Model **propositions** (atomic canonical statements) and **knowledge states** (knower × proposition ×
stance × certainty × source × validity × assertion). Knowers include characters plus pseudo-knowers
`narrator` and `reader`. Secrets are propositions with knower sets; contracts carry knowledge guards.

## Alternatives considered
- Per-character free-text "knows" lists — unqueryable, no history.
- Facts with `known_by[]` arrays — cannot express false beliefs, pretending, or sources.

## Consequences
Extraction needs channel evidence for stance changes; leak detection becomes a query; UI knowledge matrix.
