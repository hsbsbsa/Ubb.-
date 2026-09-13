# Plan Audit

Self-audit of the planning package against the fifteen questions in the brief, plus a contradiction and
gap review. Each answer names the mechanism, the document that specifies it, the schema that carries it,
and the test that proves it.

## 1. The fifteen questions

### Q1. How does the application remember exactly what happened in the previous chapter?
- **Mechanism:** the previous chapter's *accepted* manuscript version is immutable; its last ~2,000
  characters are placed verbatim in T1 of the next chapter's pack, together with its stored L1 summary,
  its recorded ending hook, and the exact state/knowledge/relationship deltas committed from it. The tail
  hash is validated against the accepted version before the call.
- **Docs:** `04-memory-canon/04-context-pack-assembly.md` §4, §2.7. **Schema:**
  `context-pack-manifest` (`prev_chapter_tail`, `prev_chapter_hook`, `validation.prev_tail_hash_ok`).
- **Test:** pack determinism/validation (`07-quality/01` §3); FR-7.13 blocks chapter k until k−1 is accepted.

### Q2. How does it retrieve something important from hundreds of chapters ago?
- **Mechanism:** authoritative state comes from bitemporal structured queries (no ranking needed); older
  events/evidence are recalled by hybrid retrieval (Korean-morpheme BM25 + pgvector kNN fused by RRF +
  graph hops from contract entities/propositions/promises), ranked deterministically with diversity caps,
  and inserted with verbatim evidence quotes. Summaries L2/L3 cover arcs/seasons.
- **Docs:** `04-memory-canon/05-retrieval-and-indexing.md`, `04` §2. **ADR:** 0011.
- **Test:** recall@pack targets on fixture (ch.9 injury recovered at ch.41; ch.23 lie recovered at ch.58).

### Q3. How does it know what each individual character knows?
- **Mechanism:** the knowledge ledger — `knowledge_states(knower, proposition, stance, certainty, source,
  validity, assertion)` for every character plus `narrator` and `reader`. Contracts carry knowledge
  deltas and guards; packs render per-participant 알고 있음/모름/오해/의심 tables; the leak checker verifies.
- **Docs:** `04-memory-canon/03-character-knowledge-architecture.md`. **Schemas:** `knowledge-state`,
  `proposition`, `chapter-contract.knowledge_guards`. **ADR:** 0008.
- **Test:** `examples/fixture/knowledge-ledger.json` expected states; traps T5, T11.

### Q4. How does it distinguish truth, belief, suspicion, lies, and secrets?
- **Mechanism:** objective truth = facts + `proposition.truth_value` (per timeline); belief/suspicion =
  stances `believes_false` (with `believed_value_ko`), `suspects`, `doubts`, `pretends`; lies = `lie`
  frame events that create knowledge stances but never facts; secrets = propositions with owner and
  allowed-knower sets enforced by guards and the commit verifier.
- **Docs:** `04-memory-canon/03` §2, `02` §1.6. **ADRs:** 0007, 0008.
- **Test:** P3 (현석's lie) lifecycle in the ledger; trap T4.

### Q5. How does it distinguish future plans from completed events?
- **Mechanism:** plans live in `plan_*` tables (frame `plan`), never in `events`/`facts`; extraction has no
  access to plans except as labelled hypotheses it must confirm or reject with evidence; packs render plans
  under `[예정 — 아직 일어나지 않음]`; facts cannot have future validity; realized/unrealized status is set
  explicitly after commit.
- **Docs:** `04-memory-canon/02` §3, `05-generation/01` §4 step 9. **Schema:** `canon-delta.hypothesis_results`.
- **Test:** extractor golden case "zero items from unrealized hypotheses"; fixture ch.9 MH-3 unrealized.

### Q6. How are rejected drafts prevented from entering canon?
- **Mechanism:** extraction accepts only `approved` versions (`assert_extractable`); rejected drafts move to
  `quarantine_versions`; the assembler's source allowlist excludes quarantine and non-accepted versions;
  exemplar and search rows are FK/trigger-restricted to accepted versions; nightly assertion job.
- **Docs:** `04-memory-canon/02` §7; `06-system/02` §12. **ADR:** 0009.
- **Test:** trap T16 (distinctive false fact in a rejected draft never appears anywhere).

### Q7. How does an approved chapter update memory?
- **Mechanism:** approve → `CanonCommitWorkflow`: extractor A ∥ B ∥ deterministic pre-pass → reconcile →
  adjudicate conflicts → verify evidence/entities/frames/validity/locks/leaks → single SQL transaction
  `canon.commit_delta` (apply delta, close superseded, bump version with optimistic check, write commit +
  inverse, dependency edges, L1 summary, search docs) → post-commit (embeddings, L2–L4, exemplars,
  promises, horizon re-plan).
- **Docs:** `04-memory-canon/02` §5; `05-generation/01` §4. **Schemas:** `canon-delta`, `canon-commit`.
- **Test:** atomicity fault injection; racing commits; fixture delta ch.9.

### Q8. How are conflicting extractions resolved?
- **Mechanism:** canonicalize + match by key; agreed → accept; single-source ≥ 0.8 with verifiable evidence →
  accept flagged; conflicts → `extraction_adjudicator` with both spans; unresolved majors → human queue
  (commit blocked for that item); items without verifiable quotes rejected.
- **Docs:** `04-memory-canon/02` §5.2–5.3. **Test:** traps T20, T22.

### Q9. How are earlier chapter changes propagated?
- **Mechanism:** `dependency_edges` (artifact → canon item @ version) written at commit/plan/pack time; any
  commit joins touched items to edges → `stale_marks` with reasons; retcon = new version → extraction diff
  → commit retracting old items → propagation; regeneration retracts superseded items in the same commit;
  MVP shows the stale list, Beta proposes patches.
- **Docs:** `04-memory-canon/02` §8–9; `05-generation/01` §6. **Test:** R1, C1, RB1, trap T14.

### Q10. How does every relevant LLM call preserve Korean webnovel style?
- **Mechanism:** style-sensitive roles are registered; the gateway **Style Guard fails closed** if the
  compiled, versioned Style Block (base + genre overlays + project overrides, role-specific variant, with
  participants' speech digests) is missing, stale, or not embedded; STYLE_TAIL recency anchor for
  writer/editor roles; planners get the structure rules so chapter shape is Korean too; every call records
  the style version and block hash.
- **Docs:** `02-korean-style/01` §3–4, `02`. **ADR:** 0005. **Schema:** `llm-call-record.style_block_hash`.
- **Test:** Style Guard unit tests; audit record assertions.

### Q11. How does the system detect Western-style or translation-like drift?
- **Mechanism:** three layers — deterministic Korean lint (translation-marker set TRN-01..20, pronoun
  density, ending repetition, paragraph/sentence length, dialogue/monologue ratios, adverb tags, exposition
  runs, format/LN/English leakage), morphological register check (speech level/honorifics/address terms vs
  ledgers), and an evidence-bound Style Judge (different model family, Korean rubric anchors, drift flags),
  calibrated on contrast pairs and a monthly editor panel.
- **Docs:** `02-korean-style/04`, `05`. **Examples:** `contrast-pairs.seed.json`. **Test:** §6 Korean suite; trap T18.

### Q12. How does it repair errors without unnecessarily rewriting everything?
- **Mechanism:** patch-first revision — issues clustered by span; revisers return span replacements with
  `changed_claims` and `preserved_facts_ack`; only affected checks re-run; regression compares scorecards
  and reverts on regression; escalation ladder sentence → paragraph → dialogue → scene → chapter with
  attempt counters and round limits.
- **Docs:** `05-generation/02` §4; `02-korean-style/05` §3–4. **ADR:** 0014. **Schema:** `patch`.
- **Test:** traps T1–T6 repaired at the specified scope; T17 escalates.

### Q13. How does it remain reliable during long generation workflows?
- **Mechanism:** Temporal workflows with idempotent activities (spend-safe replay via `llm_calls`
  idempotency keys), heartbeats/timeouts, per-error-class retry/fallback/circuit breakers, deterministic
  workflow IDs + target leases, cooperative cancellation with artifact preservation, budget pause at
  activity boundaries, stale-canon re-validation before commit, dead-letter `needs_attention` queue,
  rehydration from artifacts, full tracing.
- **Docs:** `06-system/04-workflow-reliability-plan.md`. **ADR:** 0003. **Test:** chaos suite (§8).

### Q14. How are costs controlled?
- **Mechanism:** hard limits at workspace/project/chapter/workflow enforced pre-call with reservations;
  quality tiers set candidates/judge depth/routing; model classes route cheap roles to cheap models;
  context caching (stable prefixes) and section dedup; early stopping; retry limits; cost prediction before
  batches; cost per accepted chapter and per 1,000 Korean characters tracked.
- **Docs:** `06-system/05-cost-and-observability-plan.md`. **ADR:** 0018. **Schema:** `budget`.
- **Test:** cost-limit tests (§9).

### Q15. How can another engineering agent begin implementation from the plan?
- **Mechanism:** `AGENTS.md` ground rules; `08-delivery/05-implementation-handoff-guide.md` reading order,
  invariants, build order, conventions; `01-implementation-roadmap.md` phases with exit criteria;
  `02-backlog.md` items with acceptance tests; `schemas/` contracts with validated examples; the fixture
  story as the shared integration test; ADRs for every structural decision; traceability matrix.

## 2. Contradiction review (resolved during audit)

| Found | Resolution |
| --- | --- |
| Pipeline §4.1 evaluator row contained an inline design deliberation | Rewritten as a plain list of the seven evaluator calls (`05-generation/01`) |
| Traceability matrix referenced schemas `evidence-span` and `story-clock` as separate files; they are `$defs` in `common.schema.json` | Matrix updated to `common (evidenceRef, storyClock)`; `concept` schema listed but not shipped → marked "(Phase 2)" |
| Fixture ch.9 delta evidence offsets did not satisfy `end − start = len(quote)` | Fixed; validator now enforces the invariant on examples |
| `fact.schema.json` `if/then` on `source` applied to payloads lacking `source` | Conditionals now require the discriminator to be present |
| Scope doc says candidate comparison for chapters is Premium-only in MVP, while FR-4.5 says "M/P0 (config)" | Consistent reading: the *mechanism* ships in MVP (configurable), the *default-on* policy for Standard arrives in Beta; FR-4.5 wording clarified |
| Glossary "Volume" described as planning hierarchy; planning doc treats volumes as export groupings | Glossary aligned: Volume = export unit |

## 3. Gap review

| Potential gap | Status |
| --- | --- |
| Multi-POV chapters and reader-knowledge union | Covered: contract `pov.segments`; reader knower union (`03` §2.2) |
| Off-page knowledge transfer discovered later | Covered: `retroactive_channel` events flagged for review |
| Ensemble casts exceeding pack budgets | Covered: T1 degradation ladder (`05` §7) |
| Unknown genre overlay combinations | Covered: compile warning + bible-gate approval |
| Non-Korean intake producing Latin names | Covered: glossary requires Korean canonical spelling; `KL-LANG-01` |
| User writes chapters manually / imports existing series | Deferred (Q5 in open questions); design path noted |
| Model version drift | Covered: pinned routing + regression suite on model change (R19) |
| Character counting ambiguity | Covered: ADR-0024 |
| Timeline reset semantics for multiple regressions | Covered at model level (ADR-0023); UI in Beta |
| Legal review of overlays' "abstract conventions" | Policy in ADR-0025; a human legal pass is recommended before Beta (open item) |

## 4. Invariant cross-check

Every invariant in the handoff guide §2 has: a design section, a schema field or DB rule, and a test.

| Invariant | Design | Schema/DB | Test |
| --- | --- | --- | --- |
| Canon from accepted only | `02` §4, §7 | `assert_extractable`, partial unique accepted | T16, workflow tests |
| Atomic commit | `02` §5.4 | `canon.commit_delta`, optimistic version | fault injection |
| Evidence-backed | `02` §1.1, §5.3 | evidence trigger; `fact.evidence` minItems | verifier tests |
| Planned ≠ happened | `02` §3 | `hypothesis_results`; no plan frame in facts | extractor goldens |
| Reality frames | `02` §1.6 | `realityFrame` enum; verifier | T7, T8, T15 |
| Quarantine | `02` §7 | `quarantine_versions`; FKs | T16 |
| Style Guard | `02-korean-style/01` §4 | `llm-call-record.style_block_hash` | guard unit tests |
| Prompt versioning | `05-generation/03` | `prompt_version_id` | registry tests |
| Pack snapshots | `04` §1, §2.7 | `context-pack-manifest.validation` | determinism tests |
| Durable checkpoints | `06-system/04` | idempotency keys | chaos suite |
| Tenancy | `06-system/06` §3 | RLS | RLS matrix |
| Korean text as data | AGENTS.md | `_ko` fields | formatter no-op test |
