# ADR-0031: Proposition truth is recorded per timeline with validity

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Regression and alternate-timeline stories have propositions that are true in the prior loop and false on
the main timeline (the fixture's P5). A single global `truth_value` cannot represent this and produces
false continuity issues or missed divergences.

## Decision
`propositions` no longer carry a global truth value. A child table/array `truth` holds one entry per
timeline `{ timeline_id, value: true|false|unknown, valid_from?, valid_to?, asserted/retracted version,
evidence }`. A timeline without an entry inherits from its parent timeline up to the divergence point.
Knowledge stances reference propositions as before; `diverged` is computed by comparing the regressor's
prior-loop truth with the main-timeline truth at the current story clock.

## Consequences
Schema and data-architecture changes; extractor B emits `proposition_truth` items; the knowledge matrix
UI shows truth per timeline.
