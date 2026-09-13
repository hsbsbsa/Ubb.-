# ADR-0014: Patch-first revision with regression re-checks

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Regenerating whole chapters for small problems is expensive, slow and introduces new errors.

## Decision
Cluster issues by span; repair at the smallest scope (sentence → paragraph → dialogue → scene → chapter);
revisers return span replacements with `changed_claims` and `preserved_facts_ack`; each patch creates a new
version and triggers only the affected checks, plus whole-chapter smoke checks after several patches;
regressions revert the patch; escalation ladders bound the loop.

## Alternatives considered
- Full rewrite on any failure — cost and churn.

## Consequences
Patch tooling, span addressing and incremental lint are core infrastructure.
