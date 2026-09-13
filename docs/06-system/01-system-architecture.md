# System Architecture

## 1. Overview

```
┌───────────────────────────────── Users (browser) ─────────────────────────────────┐
│  apps/web  (Next.js 15, React, TypeScript) — English UI (Korean UI in Beta),       │
│  mobile-width manuscript preview                                                    │
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
       │             │  packages/narrative  – narrative identity profiles, block        │
       │             │                        compiler, structure lint, judge merging   │
       │             │  packages/prose      – English text analysis: language check,    │
       │             │                        prose lint, register check, length model  │
       │             │  packages/prompts    – registry, templates, regression suite     │
       │             │  packages/gateway    – model gateway (providers, routing, guard) │
       │             │  packages/eval       – evaluators, scorecards, patching          │
       │             │  packages/domain     – types generated from schemas, invariants  │
       │             │  packages/db         – migrations, query layer, RLS helpers      │
       └─────────────┴──────────┬──────────────────────────────┬────────────────────────┘
                                │ HTTP (optional)               │ HTTPS
                     ┌──────────▼───────────┐        ┌──────────▼──────────────────────┐
                     │ grammar-service       │        │ LLM / embedding providers       │
                     │ (optional self-hosted │        │ (≥2 configured; no-training)    │
                     │  English grammar/     │        └─────────────────────────────────┘
                     │  spelling checker)    │
                     └──────────────────────┘
                     Observability: OpenTelemetry → collector → traces/metrics/logs backend
                     Secrets: cloud secret manager → env at boot (never in DB/repo)
```

## 2. Components

### 2.1 apps/web (Next.js)
Screens per `08-ui-plan.md`. Server components for read models; client components for review/editing;
SSE subscription for job progress; mobile-width manuscript preview with serialized-reading typography
(English, locale-aware quotes/dashes).

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
See `07-model-gateway.md`: provider adapters, routing table by role/class, **Narrative Identity Guard**
(fails closed without both the Output-Language Contract and the Narrative-Tradition Contract), post-call
**output-language check** for manuscript roles, schema validation, retries/fallback, cost accounting,
prompt caching hints, audit persistence, budget pre-checks.

### 2.6 packages/context
Pack templates, query planning, retrieval (structured/lexical/vector/graph), ranking, compression,
rendering, validation, manifest, caching, Active Constraint Set consumption, dependency-edge emission with
materiality.

### 2.7 packages/canon
Extraction orchestration helpers (pre-pass), reconciliation, verification, atomic commit, dependency edges
(material/contextual, promotion from claims), stale detection, rollback, retcon diff, per-timeline
proposition truth.

### 2.8 packages/narrative
Narrative Identity profiles (output language, tradition, genre, setting, naming, register policy,
terminology, preferences), composition, Block compiler with role variants and IDENTITY_TAIL, Structure Lint
(ST-*), judge/report merging by dimension, exemplar bank, calibration records.

### 2.9 packages/prose
English text analysis: deterministic **output-language identification**, English Prose Lint (EP-*) with a
lightweight tokenizer/POS tagger, translation-like syntax markers, dialogue-register check (RG-*) against
register digests, naming/terminology registry enforcement, the **length model** (words, code points,
paragraphs, sentences, estimated tokens, reading time — ADR-0034), Unicode code-point addressing utilities
(ADR-0030), and a client for the optional grammar service.

### 2.10 grammar-service (optional, ADR-0028)
Self-hosted English grammar/spelling checker (LanguageTool-class) behind a thin HTTP API. When enabled,
its diagnostics feed `EP-GRM-01`; when disabled, heuristic signals and the Prose Judge cover grammar.
Stateless; version pinned; results cached by text hash in `analysis_cache`.

### 2.11 Postgres 16 + pgvector (ADR-0002)
Single system of record: tenancy, spec, bible, plans, manuscripts, canon, knowledge, promises, packs,
llm_calls audit, budgets, search documents & per-model embedding sets, read models. Large payloads (full
prompts/outputs > 64 KB) stored in object storage with hashes in the row.

### 2.12 Object storage
Exports, archived payloads, uploaded user exemplars/documents (scanned + sanitized), backups.

## 3. Cross-cutting

- **Identity**: UUIDv7 everywhere; monotonic per-project counters for chapter numbers and canon versions.
- **Time**: UTC timestamps; story time as `StoryClock` JSON.
- **Text**: NFC at API boundary; **all offsets are Unicode code-point indices** (ADR-0030) — one
  implementation contract across TypeScript (`Array.from(str)` / code-point iteration, never UTF-16
  indices), Python (`str` indexing), PostgreSQL (`substring`/`char_length` on `text`), and the browser
  (Range mapping via code-point ↔ UTF-16 conversion in `packages/prose`).
- **Language**: manuscript text is English (`language='en'`); non-manuscript text fields carry a
  `language` code where they may vary (intake, directions, native-script names).
- **Tenancy**: RLS on every tenant table; `workspace_id` on every row; tests for isolation.
- **Config**: 12-factor; per-environment routing tables and prompt sets in DB with repo-mirrored sources.
- **Feature flags**: per workspace/project (evaluator sets, tiers, gate policy, experimental prompts).

## 4. Deployment topology

| Environment | Notes |
| --- | --- |
| Local dev | docker-compose: Postgres+pgvector, Temporal dev server, optional grammar-service, MinIO, OTel collector; mock provider for tests |
| Staging | managed Postgres, Temporal Cloud or self-hosted cluster, workers on container platform; real providers with low budgets |
| Production | same as staging with HA Postgres (PITR), autoscaled workers, WAF in front of API, KMS-backed encryption |

## 5. Request/flow examples

1. **Approve chapter**: web → `POST /chapters/{id}/approve` → api validates role → Temporal signal
   `approve` → workflow proceeds to `CanonCommitWorkflow` → activities write canon in one tx → read models
   refreshed → SSE event `chapter.accepted` → UI updates.
2. **Correct canon fact**: web → `POST /canon/facts/{id}/correct` → api starts `CorrectionWorkflow` → impact
   report activity (material dependents; contextual as suggestions) → UI shows → confirm signal → commit →
   propagation → stale badges appear.

Diagrams: `09-diagrams.md`.
