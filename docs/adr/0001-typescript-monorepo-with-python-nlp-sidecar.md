# ADR-0001: TypeScript monorepo (optional English grammar service)

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
The system spans a web UI, an API, durable workflow workers, and many domain packages (canon, context,
narrative identity, prose analysis, gateway). The system benefits from one language for shared domain
types generated from JSON Schema. English grammar checking, if enabled, is best served by an existing
self-hosted service rather than in-process code.

## Decision
Build a **pnpm TypeScript monorepo** (Node 22 LTS, strict TS): `apps/web` (Next.js), `apps/api` (Fastify),
`apps/worker` (Temporal TS SDK), `packages/*` including `packages/prose` (English text analysis in TS).
An **optional** self-hosted English grammar/spelling service (`services/grammar-service`, LanguageTool-class)
sits behind a thin TS client with a Postgres-backed result cache (ADR-0028).

## Alternatives considered
- All-Python (FastAPI + Temporal Python) — weaker typing story for the large domain model; UI still TS.
- In-process grammar checking only — acceptable for MVP; the optional service adds precision later.

## Consequences
One type system for domain objects; the only polyglot boundary is the optional grammar service, whose
version and caching are part of the lint determinism story. (Amended under ADR-0026/0028.)
