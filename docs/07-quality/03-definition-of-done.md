# Definition of Done

## 1. Per backlog item

- Behavior matches the referenced requirement IDs and ADRs; deviations have an ADR.
- Schemas updated first if the wire/storage shape changes; generated types regenerated; examples validate.
- Unit + integration tests added/updated; fixture-story assertions extended when story semantics are
  touched.
- Prompt changes pass the prompt regression suite and record results; prompt version bumped, never edited.
- Observability: new activity/role emits spans + metrics; cost accounted.
- Security: RLS on new tables; inputs schema-validated; no secrets; untrusted text handling respected.
- Docs: affected `docs/` updated; traceability matrix row updated.
- Reviewed by one other engineer (or agent review pass) with the checklist below.

## 2. Per phase (roadmap)

Each phase has explicit exit criteria in `docs/08-delivery/01-implementation-roadmap.md`. A phase is done
when all its P0 backlog items meet §1, the fixture-story checks for that phase pass in CI, and a demo
script for the phase runs end to end on staging.

## 3. MVP done

- All FR items tagged **M/P0** implemented and traced.
- Fixture story: all traps T1–T22 detected as specified; R1/C1/RB1 behave as specified; T16 isolation
  proven.
- Live 20-chapter run (Standard tier) completes with: zero blocking issues at acceptance, median style score
  ≥ 78, cost per accepted chapter within tier envelope, every accepted fact traceable to evidence.
- Chaos suite green; RLS suite green; prompt regression green for the pinned prompt set.
- A user can complete UW-1…UW-17 (MVP variants) in the UI without operator help.
- Runbooks: deploy, restore, rotate secrets, raise budgets, handle `needs_attention`.

## 4. Review checklist (invariants)

1. Canon only from `accepted` versions; commit atomic; version bump optimistic.
2. Every fact/event/knowledge change with evidence (or bible source).
3. Plans never rendered as facts; frames respected.
4. Rejected drafts quarantined; not reachable by assembler/extractor/exemplar/search.
5. Style Guard enforced for style-sensitive roles; style version recorded.
6. Prompt version recorded; no ad-hoc prompt strings in code.
7. Context packs manifested and hashed; T0 validated.
8. Activities idempotent; budgets checked pre-call.
9. Korean text never machine-translated or reflowed by tooling.
10. Tenancy: `workspace_id` + RLS on every new table.
