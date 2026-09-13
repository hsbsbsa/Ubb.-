# Instructions for engineering agents

This repository currently contains a **planning package** for Yeonjae Studio. Read this file before
changing anything.

## The governing principle

**English is the manuscript language. Korean webnovel is the narrative tradition.**
Reader-facing prose is composed **directly in natural English** and follows Korean serialized-webnovel
structure, pacing, hooks, payoff and genre conventions. The system never generates Korean prose and
translates it, never imitates Korean grammar in English, and never drifts into Western epic-fantasy,
literary-fiction, or traditionally published novel pacing. See ADR-0026 and
`docs/02-narrative-identity/01-narrative-identity-architecture.md`.

## Ground rules

1. **The plan is the spec.** Implement what `docs/` describes. If you must deviate, write an ADR in
   `docs/adr/` (next number, same template) *before* the deviation lands, and update the affected docs and
   `docs/01-requirements/04-traceability-matrix.md` in the same change.
2. **Do not weaken the invariants** listed in `docs/08-delivery/05-implementation-handoff-guide.md` §2
   (canon only from accepted chapters, atomic canon commits, evidence-backed facts, planned ≠ happened,
   rejected drafts quarantined, Narrative Identity Guard on every style-sensitive call, English output
   check on manuscript roles, prompt versioning, context-pack snapshots, durable checkpoints). They are
   the reason the product works.
3. **Schemas are contracts.** `schemas/*.schema.json` define the wire/storage shape of the core objects.
   Generate types from them (or keep Zod definitions in lockstep and test equivalence); do not fork them.
   Text fields are language-neutral with explicit language metadata; do not reintroduce
   language-suffixed primary fields.
4. **Korean is terminology and source culture, not manuscript language.** Korean craft terms (사이다,
   회귀, 상태창…) appear glossed in English in profiles and docs; character names and preserved terms are
   governed by the project's naming and terminology policies. Never machine-translate fixture prose,
   profile rules, or terminology entries; never let a formatter reflow example prose.
5. **No secrets in the repo.** Provider keys live in the secret manager / `.env` (git-ignored). `.env.example`
   may list variable *names* only.
6. **Commit per milestone** with focused messages. Never rewrite published history.
7. **Keep the validator green.** `python tools/validate-planning-package.py` validates schemas and
   examples and scans for contradictory language-output statements; run it before every commit that
   touches `docs/`, `schemas/`, or `examples/`.

## Where to start implementing

`docs/08-delivery/05-implementation-handoff-guide.md` → `docs/08-delivery/01-implementation-roadmap.md`
(Phase 0 first) → `docs/08-delivery/02-backlog.md` (P0 items). Use the fixture story in
`docs/07-quality/02-fixture-story.md` + `examples/fixture/` as the first integration test.

## Repository conventions once code exists (decided in ADR-0001, ADR-0021, ADR-0028)

- pnpm workspace monorepo, TypeScript strict, Node 22 LTS.
- `apps/web` (Next.js), `apps/api` (Fastify), `apps/worker` (Temporal workers), `packages/*` (domain,
  db, gateway, prompts, narrative, prose, context, canon, eval, workflows); `services/grammar-service`
  (optional self-hosted grammar/spelling checker for English).
- Postgres 16 + pgvector is the single system of record. Temporal orchestrates; Postgres holds truth.
- All IDs are UUIDv7; all timestamps UTC; all text UTF-8 NFC-normalized at the boundary; all text
  offsets are Unicode code-point indices into NFC text (ADR-0030).
