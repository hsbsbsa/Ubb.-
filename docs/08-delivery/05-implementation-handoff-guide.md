# Implementation Handoff Guide

For the engineering agent (or team) that will build Yeonjae Studio from this plan.

## 1. Read in this order (≈ 2 hours)

1. `README.md`, `AGENTS.md`
2. `docs/00-overview/01-executive-product-definition.md`, `02-glossary.md`, `03-scope-and-release-tiers.md`
3. `docs/01-requirements/01-functional-requirements.md` (skim; use as checklist later)
4. `docs/04-memory-canon/01-…05-…` (the core), then `docs/02-korean-style/01-…05-…`
5. `docs/05-generation/01-generation-pipeline.md`, `02-evaluation-and-revision-pipeline.md`
6. `docs/06-system/02-data-architecture.md`, `07-model-gateway.md`, `04-workflow-reliability-plan.md`
7. `schemas/*.schema.json` + `examples/`
8. `docs/08-delivery/01-implementation-roadmap.md`, `02-backlog.md`
9. `docs/adr/` (all; short)

## 2. Invariants you must never break

1. **Canon only from accepted chapters** (plus bible/user corrections with justification). Extraction reads
   `approved` versions only; commit sets `accepted`.
2. **Atomic canon commit** with optimistic version check; no canon writes outside `canon.commit_delta`.
3. **Evidence-backed facts**: every extracted fact/event/knowledge/relationship change has ≥ 1 verified
   evidence span; bible-sourced facts are marked `source=bible`.
4. **Planned ≠ happened**: plan tables never feed extraction; packs label plans `[예정]`; no future validity.
5. **Reality frames**: only `canonical/flashback/prior_loop/alternate_timeline` produce facts; `lie` →
   knowledge stances only.
6. **Rejected drafts quarantined**: never in packs, extraction, summaries, embeddings, exemplars.
7. **Style Guard**: style-sensitive roles cannot call the gateway without a valid Style Block; version
   recorded.
8. **Prompt versioning**: no inline prompt strings; every call records `prompt_version_id`.
9. **Context pack snapshots**: every call records `pack_id`/`pack_hash`; T0 validated byte-for-byte.
10. **Durable checkpoints & idempotency**: every side effect is an activity with an idempotency key;
    budgets checked before each call.
11. **Tenancy**: RLS on every tenant table.
12. **Korean text is data**: never translated/reflowed by tooling.

## 3. Build order (Phase 0 → 2 detail)

1. Scaffold + schemas → types (B-0-1, B-0-2).
2. DB migrations + `commit_delta` + evidence trigger + RLS (B-0-4, B-0-5). Write pgTAP tests first.
3. Gateway with Mock/Replay/Fault providers and Style Guard (B-0-6). Test the guard before any prompt.
4. Prompt registry (B-0-7). Sidecar (B-0-8). API/worker skeleton (B-0-9). Seed fixture (B-0-10).
5. Style package (B-1-1…1-5). Use `examples/fixture/contrast-pairs.seed.json` in tests from day one.
6. Canon package (B-1-6…1-11, 1-15). Use `examples/fixture/canon-delta.ch09.json` and
   `knowledge-ledger.json` as expected outputs.
7. Retrieval + context assembler (B-1-12, 1-13). Recall tests from fixture.
8. Workflows (B-2-*) — start with `ChapterProductionWorkflow` on MockProvider, then real prompts.

## 4. Conventions

- Package boundaries as in `docs/06-system/01-system-architecture.md`; no cross-imports that bypass
  interfaces in `packages/domain`.
- Errors: typed error codes (`PACK_T0_OVERFLOW`, `STALE_CANON`, `STYLE_BLOCK_MISSING`, `BUDGET_EXHAUSTED`,
  `LEASE_HELD`, `EVIDENCE_MISMATCH`, `FRAME_VIOLATION`, `KNOWLEDGE_LEAK`).
- Korean strings in code are data files (`*.ko.json`), not literals.
- Tests colocated; fixture data imported from `examples/fixture` via a package alias.
- Commit per milestone with messages `feat(scope): …`, `test(scope): …`, `docs(scope): …`.

## 5. Where ambiguity is allowed

- Exact provider/model choices → routing tables (config), validated by the benchmark procedure.
- Exact lint thresholds → profile data; start with the documented defaults, tune via contrast pairs and
  editor feedback.
- UI visual design → follow the UI plan's structure; styling is free.
- Internal function names → free; schema field names → fixed by `schemas/`.

## 6. How to verify you are done with a phase

Run the fixture assertions listed in the roadmap's exit criteria; produce a short report in
`docs/08-delivery/reports/` (one file per phase, e.g. `phase-0.md`) with test results, costs, and any ADRs
added. Keep `python tools/validate-planning-package.py` green whenever schemas or examples change.
