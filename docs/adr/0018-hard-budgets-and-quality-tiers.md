# ADR-0018: Hard budgets at project/chapter/workflow with quality tiers

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Trial resources are limited; runaway loops must be impossible; users need predictable cost.

## Decision
Enforce **hard limits** pre-call via gateway reservations at workspace/project/chapter/workflow scopes;
pause cleanly at activity boundaries on exhaustion; quality tiers (Economy/Standard/Premium) set candidate
counts, judge depth and routing; predictions shown before batches; cost per accepted chapter / 1,000 accepted words
tracked.

## Alternatives considered
- Soft warnings only — unsafe.

## Consequences
Budget tables and reservation logic in Phase 0; prediction calibration in Phase 4.
