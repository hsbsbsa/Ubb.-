# ADR-0012: Rolling-horizon hierarchical planning

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
A flat list of hundreds of chapter summaries is brittle and unreactive; no plan at all loses direction.

## Decision
Plan Series Blueprint (committed ending + endgame requirements) → Seasons → Arcs (major/minor) → Chapter
Contracts → Scenes, with detail decreasing with distance: contracts for the next 6 chapters, arc outlines
for 2 arcs, seasons for the whole series. Re-plan on commits, directions, edits, corrections. Volumes are
export groupings.

## Alternatives considered
- Full upfront chapter list — rigid; huge invalidation on any change.
- Pure improvisation — no ending, drift.

## Consequences
PlanningHorizonWorkflow after each commit (amortized 1–2 calls); stale marking via dependency edges.
