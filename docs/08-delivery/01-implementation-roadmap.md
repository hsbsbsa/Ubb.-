# Implementation Roadmap

Phases are sequential with overlapping tails; each has exit criteria tied to the fixture story. Effort is
expressed in engineer-weeks for a 3–4 person team (or equivalent agent capacity); numbers are planning
estimates, not commitments.

## Phase 0 — Foundations (3–4 weeks)

**Goal:** the skeleton every later phase depends on; no story generation yet.

- Monorepo scaffold (pnpm, TS strict, ESLint/Prettier with Korean-safe settings, Vitest), CI (lint, test,
  schema validation, secret scanning), docker-compose (Postgres+pgvector, Temporal dev, sidecar, MinIO,
  OTel).
- `packages/domain`: types generated from `schemas/`; character counting (ADR-0024); StoryClock; IDs.
- `packages/db`: migrations for tenancy, projects, spec, entities, manuscripts, canon (facts/events/
  knowledge/relationships/promises/commits/evidence), packs, llm_calls, budgets; RLS policies; SQL
  functions `canon.commit_delta`, `canon.state_at`, evidence trigger; pgTAP tests.
- `packages/gateway`: adapters (2 providers + mock/replay/fault), routing table, Style Guard, budget guard,
  idempotency, schema validation, audit persistence, OTel.
- `packages/prompts`: registry model, loader, hashing, prompt set pinning; regression runner skeleton.
- Korean NLP sidecar container + client; `nlp_cache`.
- `apps/api` skeleton with auth, workspace RLS middleware, projects CRUD; `apps/worker` with Temporal
  worker bootstrap and a hello workflow.

**Exit:** fixture bible loads into DB via a seed script; a `mock` LLM call through the gateway is
recorded with all audit fields; Style Guard test rejects a style-sensitive call without a block; RLS test
green; canon commit tx test (atomicity, optimistic version) green.

## Phase 1 — Canon core & Korean style core (4–5 weeks)

- `packages/style`: profile compose/compile (base + 8 overlays + overrides), Style Block compiler with
  role budgets and STYLE_TAIL, lint rules (all KL-* in the spec), register check via sidecar, thresholds;
  contrast-pair seed set (60) in tests.
- `packages/canon`: extraction pre-pass (glossary NER, 상태창 numbers, speaker annotations), reconciler,
  evidence verifier, commit orchestration, dependency edges, stale marking, rollback (latest), retcon diff.
- Knowledge ledger queries; relationship/address-term tracking; promise ledger.
- `packages/context`: query planner, structured fetch, lexical + vector retrieval, ranker, compressors,
  renderers, validation, manifest, caching; templates for writer/planner/checker/extractor.
- Summaries L1–L4 generation activities (with `summarizer_min` style block).

**Exit:** with `ReplayProvider` outputs for the fixture, ch.1–ch.20 canon deltas commit and produce the
expected facts/knowledge/relationships (annotated); bitemporal queries answer trap-related questions;
T16 isolation test green; pack recall tests green; lint separates contrast pairs (≥ 90%); register checker
catches T9/T13.

## Phase 2 — Planning & production pipeline (5–6 weeks)

- Workflows: RequirementInterpretation, Concept, StoryBible, SeriesPlanning, PlanningHorizon,
  ChapterProduction (scenes, assembler, deterministic checks, evaluators, RevisionWorkflow), CanonCommit
  child, Batch.
- Prompt families v1 for all MVP roles; regression suite golden cases from the fixture.
- Evaluators + scorecards + issue clustering + patch application + regression re-checks.
- Cost prediction v1, budgets enforcement end-to-end, quality tiers.
- API for all production/plan/canon endpoints; SSE progress.

**Exit:** fixture ch.1–ch.12 produced end-to-end on live models (Standard) in staging with Assisted gates
via API; seeded traps in `ReplayProvider` drafts are detected (T1–T15, T17–T19, T21) and patched or
escalated per spec; chaos suite basic cases green.

## Phase 3 — UI & review experience (4–5 weeks)

- Web app screens per UI plan (Requirements/Assumptions, Concept Compare, Bible + Speech Profiles + Style
  Profile, Plan boards, Chapter Review with issues/evidence/candidates/delta preview/trace, Canon
  inspectors, Jobs/Attention, Costs, Export TXT/DOCX).
- Korean/English i18n for core screens; mobile preview.

**Exit:** UW-1…UW-17 (MVP variants) executable in the UI by a non-operator; usability pass with 2 Korean
authors; export DOCX opens correctly with Korean typography.

## Phase 4 — MVP hardening (3–4 weeks)

- Long-form continuity test (120-chapter compressed) green; live 20-chapter nightly green for 5
  consecutive nights.
- Cost calibration; provider fallback drills; backup/restore runbook; security tests; docs/runbooks.
- Human Korean-editor evaluation round 1 (30 chapters) → threshold tuning.

**Exit:** MVP Definition of Done (`docs/07-quality/03-definition-of-done.md` §3).

## Phase 5 — Public Beta (6–8 weeks)

Autopilot mode with escalation; remaining 8 overlays; automated retcon patch proposals; arbitrary rollback;
reader feedback import (sanitized, soft signals); candidate comparison default for Standard; EPUB +
platform export profiles; members/roles; alerting; PITR; similarity screening; user style preference
learning (semi-automatic); contrast-pair set ≥ 300; 2FA/OAuth providers for Korean users.

## Phase 6 — Production (ongoing)

SLOs, load testing at 3,000 chapters, chaos drills, restore drills, WCAG AA, cross-encoder reranker A/B,
character-drama and slow-burn refinements, cost optimizations (distillation of cheap classifiers), editor
program.

## Dependency graph (high level)

```
P0 foundations ─► P1 canon+style core ─► P2 pipeline ─► P3 UI ─► P4 hardening ─► P5 beta ─► P6 prod
                     └──────── prompt regression suite grows continuously ─────────┘
```
