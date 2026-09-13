# ADR-0015: Position-swapped pairwise judging with tie rules and early stop

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
LLM judges show position bias and self-preference; more candidates cost more.

## Decision
Compare candidates pairwise in **both orders**; consistent winner wins; inconsistency → third run with
shuffled rubric order; ties → higher scorecard → fewer patches (cheaper). Judges use a different model
family from the writer when available and never see the writer's exemplars. **Early stop**: skip further
candidates when the first meets the early-stop threshold with no major issues.

## Alternatives considered
- Single-order judging — biased.
- Absolute scoring only — poorly calibrated across candidates.

## Consequences
2× comparison calls when N=2; budget-aware candidate policy per tier.
