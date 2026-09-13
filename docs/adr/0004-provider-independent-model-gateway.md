# ADR-0004: Provider-independent model gateway with role-based routing

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Different roles need different model strengths (Korean prose, reasoning, cheap classification, embeddings).
Providers change prices, availability and behavior; the product must not lock into one (e.g., Kimi K3).

## Decision
All model access goes through `packages/gateway`: provider adapters behind one interface; a
**routing table role→[models]** per environment; class-based defaults (R/P/M/C/E); Style Guard, budget
guard, idempotency, schema validation, retries/fallback, cost accounting and audit in the gateway.
Judges use a different model family from the writer when available.

## Alternatives considered
- Direct SDK usage per role — scattered retry/cost/audit logic; lock-in.
- External LLM proxy only — insufficient for Style Guard/budget/idempotency semantics tied to our domain.

## Consequences
A model is data; benchmarks decide class membership; adapters isolate provider quirks.
