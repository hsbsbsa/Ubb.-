# ADR-0033: Hard requirements are compiled into a scope-filtered Active Constraint Set

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
T0 must never be trimmed, but a long project accumulates hundreds of hard requirements and directions.
Rendering the raw list in T0 would eventually overflow the pack budget.

## Decision
Requirements and directions carry scope (series / season / arc / chapter range / entities). For each
chapter, `PlanningHorizonWorkflow` compiles an **Active Constraint Set**: in-scope hard requirements,
content restrictions and locked facts, deduplicated, superseded items removed, grouped by category, each
with its stable requirement ID, rendered once and hashed, bounded by a configurable cap (starting 1,200
tokens). Exceeding the cap raises `CONSTRAINTS_OVERFLOW` and asks the user to consolidate (with merge
suggestions) — never silent trimming. Contracts reference the set by id + hash; packs validate the bytes.

## Consequences
New table `active_constraint_sets`; FR-1.8; T0 size is bounded regardless of project length.
