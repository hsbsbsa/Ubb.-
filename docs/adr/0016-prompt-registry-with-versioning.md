# ADR-0016: Prompt registry with immutable versions and regression gating

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Prompts are code with model-dependent behavior; silent edits break calibration and auditability.

## Decision
Prompts live in a registry as **immutable, content-hashed versions** per family with schema, params,
routing policy and regression results; projects/batches pin **prompt sets**; promotion requires the
regression suite; every call records the version.

## Alternatives considered
- Inline prompt strings — unauditable.

## Consequences
Registry tooling and a regression runner are Phase 0/2 work.
