# ADR-0021: Repository structure for the implementation

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
The implementation agent needs a fixed layout to avoid redesign.

## Decision
```
apps/web, apps/api, apps/worker
packages/domain (types from schemas, invariants), packages/db (migrations, queries, RLS),
packages/gateway, packages/prompts (families/<role>/vX.Y.Z), packages/style, packages/korean,
packages/context, packages/canon, packages/eval, packages/workflows
services/nlp-sidecar (Python)
schemas/ (contracts), examples/ (fixtures), docs/ (this plan)
```
Package boundaries are enforced by lint rules; cross-package calls go through interfaces in `packages/domain`.

## Consequences
Predictable ownership; schema-first workflow.
