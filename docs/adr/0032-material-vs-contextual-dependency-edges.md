# ADR-0032: Dependency edges distinguish material from contextual dependencies

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Writing a dependency edge for every canon item a chapter's context pack included would mark large swaths
of later chapters stale after any small canon change, because T2 retrieval pulls in many items that the
chapter never relied upon.

## Decision
Dependency edges carry `materiality: material | contextual` and a `basis`. T0/T1 items and contract
anchors are material; T2/T3 retrieved items are contextual unless the writer's `claims[]` or the
extractor's evidence show reliance (then promoted to material at commit). Only material edges mark
dependents stale by default; contextual edges produce a "review suggested" mark. Users can promote an
edge to material in the inspector. Impact reports show both classes separately.

## Consequences
Fewer false-stale artifacts; a promotion step in `CanonCommitWorkflow`; inspector UI changes; fixture case
R1 distinguishes the two classes.
