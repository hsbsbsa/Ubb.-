# ADR-0001: TypeScript monorepo with a Python Korean-NLP sidecar

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
The system spans a web UI, an API, durable workflow workers, and many domain packages (canon, context,
style, gateway). Korean morphological analysis has mature tooling in Python (Kiwi, MeCab-ko) but the rest
of the system benefits from one language for shared domain types generated from JSON Schema.

## Decision
Build a **pnpm TypeScript monorepo** (Node 22 LTS, strict TS): `apps/web` (Next.js), `apps/api` (Fastify),
`apps/worker` (Temporal TS SDK), `packages/*`. Run Korean morphology as a **stateless Python sidecar**
(FastAPI) with a thin TS client and a Postgres-backed result cache.

## Alternatives considered
- All-Python (FastAPI + Temporal Python) — weaker typing story for the large domain model; UI still TS.
- JS-only Korean analyzers — insufficient accuracy for speech-level/honorific analysis.

## Consequences
One type system for domain objects; a small polyglot boundary confined to the sidecar; sidecar versioning
and caching must be part of the lint determinism story.
