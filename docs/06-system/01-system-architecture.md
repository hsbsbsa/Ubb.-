# System Architecture

## 1. Overview

```
┌───────────────────────────────── Users (browser) ─────────────────────────────────┐
│  apps/web  (Next.js 15, React, TypeScript) — Korean/English UI, mobile preview     │
└───────────────┬────────────────────────────────────────────────────────────────────┘
                │ HTTPS (REST + SSE for job progress)
┌───────────────▼────────────────────────────────────────────────────────────────────┐
│  apps/api  (Fastify, TypeScript) — AuthN/Z, REST API, validation (JSON Schema),     │
│  workflow start/signal/query via Temporal client, read models, exports              │
└──────┬───────────────────────┬──────────────────────────────┬──────────────────────┘
       │                       │                              │
┌──────▼────────┐    ┌─────────▼──────────┐        ┌──────────▼───────────────────────┐
│ Postgres 16   │    │ Temporal Server    │        │ Object storage (S3-compatible)    │
│ + pgvector    │◄───┤ (durable workflows)│        │ exports, large payload archives   │
│ (RLS, PITR)   │    └─────────┬──────────┘        └──────────────────────────────────┘
└──────▲────────┘              │ task queues
       │             ┌─────────▼──────────────────────────────────────────────────────┐
       │             │ apps/worker (Temporal workers, TypeScript)                      │
       │             │  packages/workflows  – workflow definitions (deterministic)     │
       │             │  packages/context    – pack assembler, retrieval                │
       │             │  packages/canon      – extraction reconcile/verify/commit        │
       │             │  packages/style      – style profiles, compiler, lint, judges    │
       │             │  packages/korean     – tokenization, register analysis (client) │
       │             │  packages/prompts    – registry, templates, regression suite     │
       │             │  packages/gateway    – model gateway (providers, routing, guard) │
       │             │  packages/eval       – evaluators, scorecards, patching          │
       │             │  packages/domain     – types generated from schemas, invariants  │
       │             │  packages/db         – migrations, query layer, RLS helpers      │
       └─────────────┴──────────┬──────────────────────────────┬────────────────────────┘
                                │ HTTP                          │ HTTPS
                     ┌──────────▼───────────┐        ┌──────────▼──────────────────────┐
                     │ Korean NLP sidecar    │        │ LLM / embedding providers       │
                     │ (Python, Kiwi/MeCab)  │        │ (≥2 configured; no-training)    │
                     └──────────────────────┘        └─────────────────────────────────┘
                     Observability: OpenTelemetry → collector → traces/metrics/logs backend
                     Secrets: cloud secret manager → env at boot (never in DB/repo)
```

## 2. Components

### 2.1 apps/web (Next.js)
Screens per `08-ui-plan.md`. Server components for read models; client components for review/editing;
SSE subscription for job progress; mobile-width manuscript preview; Korean typography settings.

### 2.2 apps/api (Fastify)
- Auth (session cookies; OAuth + magic link), workspace scoping middleware setting `app.workspace_id` for
  RLS (`SET LOCAL`), RBAC checks.
- REST resources (`03-api-and-interface-plan.md`), JSON Schema validation on all bodies (schemas from
  `schemas/`).
- Workflow control: start (deterministic workflow IDs), signal (approve/reject/pause/cancel/direction),
  query (progress), list jobs from a read model table updated by workflow activities.
- Read models: denormalized views for inspectors (knowledge matrix as of chapter k, relationship graph,
  promise board, cost dashboards) — SQL views/materialized views refreshed on commit.
- Exports: enqueue `ExportWorkflow`; serve signed URLs.

### 2.3 Temporal (ADR-0003)
- Namespaces per environment; task queues: `planning`, `production`, `evaluation`, `canon`, `export`.
- Workflows are deterministic TypeScript; all I/O in activities. Heartbeats on long LLM activities.
- Search attributes: project_id, chapter_no, kind, status for UI listing fallback.
- Retention: workflow histories 30 days (audit lives in Postgres, not Temporal history).

### 2.4 apps/worker
Hosts activities. Scales horizontally; concurrency limits per task queue; workspace-fair scheduling via a
Postgres-backed token bucket (`llm_concurrency_leases`).

### 2.5 packages/gateway (model gateway)
See `07-model-gateway.md`: provider adapters, routing table by role/class, Style Guard, schema validation,
retries/fallback, cost accounting, prompt caching hints, audit persistence, budget pre-checks.

### 2.6 packages/context
Pack templates, query planning, retrieval (structured/lexical/vector/graph), ranking, compression,
rendering, validation, manifest, caching.

### 2.7 packages/canon
Extraction orchestration helpers (pre-pass), reconciliation, verification, atomic commit, dependency
edges, stale detection, rollback, retcon diff.

### 2.8 packages/style & packages/korean
Style profile compose/compile, lint rules, register check client (sidecar), judge/report merging, exemplar
bank.

### 2.9 Korean NLP sidecar (ADR-0017)
Python FastAPI service wrapping a Korean morphological analyzer (Kiwi preferred; MeCab-ko fallback) with
endpoints: `/analyze` (morphemes, POS, sentence split), `/endings` (sentence-final ending class),
`/honorifics`, `/tokens-for-search`. Stateless; horizontally scalable; version pinned; results cached by
text hash in Postgres (`nlp_cache`) to keep lint incremental.

### 2.10 Postgres 16 + pgvector (ADR-0002)
Single system of record: tenancy, spec, bible, plans, manuscripts, canon, knowledge, promises, packs,
llm_calls audit, budgets, search documents & embeddings, read models. Large payloads (full prompts/outputs
> 64 KB) stored in object storage with hashes in the row.

### 2.11 Object storage
Exports, archived payloads, uploaded user exemplars/documents (scanned + sanitized), backups.

## 3. Cross-cutting

- **Identity**: UUIDv7 everywhere; monotonic per-project counters for chapter numbers and canon versions.
- **Time**: UTC timestamps; story time as `StoryClock` JSON.
- **Text**: NFC at API boundary; character counting per ADR-0024.
- **Tenancy**: RLS on every tenant table; `workspace_id` on every row; tests for isolation.
- **Config**: 12-factor; per-environment routing tables and prompt sets in DB with repo-mirrored sources.
- **Feature flags**: per workspace/project (evaluator sets, tiers, gate policy, experimental prompts).

## 4. Deployment topology

| Environment | Notes |
| --- | --- |
| Local dev | docker-compose: Postgres+pgvector, Temporal dev server, sidecar, MinIO, OTel collector; mock provider for tests |
| Staging | managed Postgres, Temporal Cloud or self-hosted cluster, workers on container platform; real providers with low budgets |
| Production | same as staging with HA Postgres (PITR), autoscaled workers, WAF in front of API, KMS-backed encryption |

## 5. Request/flow examples

1. **Approve chapter**: web → `POST /chapters/{id}/approve` → api validates role → Temporal signal
   `approve` → workflow proceeds to `CanonCommitWorkflow` → activities write canon in one tx → read models
   refreshed → SSE event `chapter.accepted` → UI updates.
2. **Correct canon fact**: web → `POST /canon/facts/{id}/correct` → api starts `CorrectionWorkflow` → impact
   report activity → UI shows → confirm signal → commit → propagation → stale badges appear.

Diagrams: `09-diagrams.md`.
