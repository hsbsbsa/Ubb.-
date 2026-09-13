# Instructions for engineering agents

This repository currently contains a **planning package** for Yeonjae Studio. Read this file before
changing anything.

## Ground rules

1. **The plan is the spec.** Implement what `docs/` describes. If you must deviate, write an ADR in
   `docs/adr/` (next number, same template) *before* the deviation lands, and update the affected docs and
   `docs/01-requirements/04-traceability-matrix.md` in the same change.
2. **Do not weaken the invariants** listed in `docs/08-delivery/05-implementation-handoff-guide.md` §2
   (canon only from accepted chapters, atomic canon commits, evidence-backed facts, planned ≠ happened,
   rejected drafts quarantined, style guard on every style-sensitive call, prompt versioning, context-pack
   snapshots, durable checkpoints). They are the reason the product works.
3. **Schemas are contracts.** `schemas/*.schema.json` define the wire/storage shape of the core objects.
   Generate types from them (or keep Zod definitions in lockstep and test equivalence); do not fork them.
4. **Korean text is data, not decoration.** Never "translate" Korean examples, style rules, or fixture prose
   into English; never let a linter reflow them.
5. **No secrets in the repo.** Provider keys live in the secret manager / `.env` (git-ignored). `.env.example`
   may list variable *names* only.
6. **Commit per milestone** with focused messages. Never rewrite published history.

## Where to start implementing

`docs/08-delivery/05-implementation-handoff-guide.md` → `docs/08-delivery/01-implementation-roadmap.md`
(Phase 0 first) → `docs/08-delivery/02-backlog.md` (P0 items). Use the fixture story in
`docs/07-quality/02-fixture-story.md` + `examples/fixture/` as the first integration test.

## Repository conventions once code exists (decided in ADR-0001, ADR-0021)

- pnpm workspace monorepo, TypeScript strict, Node 22 LTS.
- `apps/web` (Next.js), `apps/api` (Fastify), `apps/worker` (Temporal workers), `packages/*` (domain,
  db, gateway, prompts, style, korean, context, canon, eval, workflows).
- Postgres 16 + pgvector is the single system of record. Temporal orchestrates; Postgres holds truth.
- All IDs are UUIDv7; all timestamps UTC; all text UTF-8 NFC-normalized at the boundary.
