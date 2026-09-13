# Testing Strategy

Principle: **the fixture story is the integration test**. Every subsystem test that touches story content
uses `docs/07-quality/02-fixture-story.md` + `examples/fixture/` so that traps are shared, and failures are
explainable in story terms. Model-dependent tests run against `ReplayProvider` (recorded outputs) in CI and
against live models in a nightly/spend-capped suite.

## 1. Test pyramid

| Layer | Tooling | Runs |
| --- | --- | --- |
| Unit (pure functions: lint rules, compilers, rankers, reconcilers, state machines, SQL functions) | Vitest; pgTAP for SQL functions | every PR |
| Contract (schemas ↔ types ↔ API) | JSON Schema validation of examples; generated types compile; API schema tests | every PR |
| Integration (DB + services: canon commit, pack assembly, retrieval, RLS) | Vitest + testcontainers Postgres/pgvector + sidecar container | every PR |
| Workflow (Temporal test server; MockProvider/ReplayProvider) | Temporal TS testing framework | every PR |
| Prompt regression (live or replayed models) | custom runner; golden assertions | on prompt/model change; nightly |
| End-to-end (fixture story 20 chapters on live models, low budget) | staging | nightly / release |
| Long-form continuity (fixture 120-chapter compressed run with synthetic acceptance) | staging | weekly |
| Chaos/failure recovery | FaultInjectingProvider; worker kills; DB faults | weekly + release |
| Load | k6 against API + synthetic pack assembly on a 3,000-chapter dataset | release |
| Security | RLS tests, authz matrix, injection corpus, dependency & secret scanning | every PR / nightly |
| Human Korean-editor evaluation | blind rating protocol | monthly |

## 2. Unit tests (highlights)

- **Korean lint**: each rule has positive/negative Korean samples (`packages/style/fixtures/lint/*.ko.txt`),
  thresholds per profile; translation-marker list must flag the "translated" side of every contrast pair
  more than the native side.
- **Register classifier**: sentence-final ending classification accuracy ≥ 97% on a labeled set of 1,000
  utterances across levels; honorific feature extraction tests.
- **Style compiler**: determinism (same inputs → same hash), budget shedding order, never-shed sections,
  compile error on overflow, STYLE_TAIL content.
- **Style Guard**: rejects missing/stale/unembedded blocks; passes valid; records versions.
- **StoryClock ordering**, bitemporal helpers, reality frame rules (no facts from `lie/dream/plan`).
- **Reconciler**: agreed / single-source / conflict classification; canonicalization of values; alias
  resolution.
- **Evidence verifier**: exact and fuzzy anchoring; rejects paraphrases.
- **Ranker**: deterministic scores; diversity caps; dedupe vs T1.
- **Budget guard**: reservations, releases, hard stop.
- **Character counting** per ADR-0024 (NFC, spaces, markup exclusion; combining jamo cases).

## 3. Integration tests

- **Atomic canon commit**: fault injected mid-transaction → no partial rows; version unchanged; retry
  succeeds exactly once.
- **Optimistic version check**: two commits racing → one fails with `STALE_CANON`.
- **Rejected-draft isolation**: quarantine content never appears in facts/summaries/packs/exemplars/search.
- **Evidence trigger**: mismatched quote rejected; non-accepted version rejected.
- **RLS**: cross-workspace queries return zero rows for every tenant table (generated test over catalog).
- **Retrieval recall**: fixture contracts → packs must include specified items (recall@pack targets).
- **Pack determinism & validation**: identical inputs → identical hash; T0 byte-equality; prev tail hash.
- **Bitemporal queries**: state at chapter k / as of version v for injuries, locations, ranks (fixture).
- **Knowledge queries**: stance at chapter k per knower; guards; leak detection cases.
- **Migrations**: apply all → fixture load → down last 3 → up; data preserved; performance of indexes.

## 4. Workflow tests

- Chapter pipeline happy path with MockProvider (deterministic outputs) → accepted; trace complete.
- Revision loop: seeded issues → patches → regression → clean; round limit → `needs_attention`.
- Gate policies per mode; signals (approve/reject/request changes/pause/cancel/direction).
- Batch: sequential dependency; pause on review; resume; cancellation mid-scene keeps partial artifacts
  non-canonical.
- Stale canon between evaluation and commit → re-validate path.
- Duplicate start rejected; lease expiry.
- Extraction failure → chapter remains `approved`; retry path.
- Rehydration from artifacts after simulated history loss.

## 5. Prompt regression suite

Golden cases per family (inputs = fixture packs; assertions structured). Examples:
- `style_judge`: native > translated on all contrast pairs; drift flags on the translated set; no blocking
  issue on the native set.
- `continuity_checker`: recall ≥ 0.9 on seeded blocking traps (forgotten injury, wrong location, rank
  regression, inventory impossibility); precision ≥ 0.8 on majors; every issue has span + canon evidence.
- `knowledge_leak_checker`: detects 서하 acting on P1 before ch.58; does not flag narrator knowledge.
- `extractor_a/b`: recover ≥ 95% of the fixture's annotated canon items with valid quotes; zero items from
  `plan` hypotheses that the text did not realize.
- `scene_writer`: outputs schema-valid; lint marker rate ≤ threshold; register accuracy ≥ 95% on speaker
  pairs; length within tolerance on 10 samples.
- `chapter_planner`: contracts validate; no knowledge delta without channel; cadence checks pass.
- Position bias: comparator both-order consistency ≥ 85% on fixture pairs.
Runner records model versions, cost, latency; promotion gate per prompt architecture §5.

## 6. Korean-language and style tests

- Contrast-pair set (seed 60 → 300): lint separation, judge preference, repair effectiveness (after repair,
  the translated variant's lint rate must drop ≥ 60% and judge nativeness rise ≥ 15 points without changing
  claims).
- Speech-level suite: pairs × contexts (e.g., 무협 사형→사매 하게체; 로판 영애→공작 하십시오체; lovers after
  ch.87 반말) generated from the fixture speech profiles; register checker + voice judge accuracy.
- Format drift suite: screenplay/webtoon/markdown/LN samples must be blocked.
- Naming consistency: alias variants flagged.
- Human editor protocol (monthly): 30 chapters, 3 editors, blind 1–5 native-ness + free comments;
  Spearman vs judge; results feed threshold tuning.

## 7. Long-form continuity tests

- **Compressed 120-chapter run**: fixture bible + plans; chapters generated by `ReplayProvider` from a
  recorded corpus with annotated canon; every commit's delta compared to annotations; at chapters 40, 80,
  120: state-at-time, knowledge, and relationship assertions (see fixture traps table); pack recall for
  distant events; summary fidelity (L2/L3 contain the annotated core events).
- **Live 20-chapter run** nightly with a small budget: end-to-end acceptance, zero blocking issues at
  acceptance, style score medians, cost per chapter within tier.

## 8. Failure-recovery & chaos

Inject: provider 5xx/timeouts/429; invalid JSON; truncation; worker kill during scene 2; DB failure during
commit; stale canon race; cancellation during extraction; budget exhaustion mid-revision. Assert: no
duplicate spend beyond one call; no partial canon; resumable; final states correct; audit complete.

## 9. Cost-limit tests

Hard limit reached mid-chapter → pause at activity boundary, no further calls, resume after raise;
prediction accuracy tracked (±30% after calibration); candidate early-stop respected.

## 10. Security tests

RLS matrix; authz per route per role; injection corpus (Korean/English meta-instructions in requirements,
comments, documents) → classifier flags and downstream isolation (no requirement/canon change without
gate); secrets scanning; dependency audit; SSRF/XSS/CSRF suites on API/web.

## 11. Load tests

3,000-chapter synthetic project: pack assembly p95 ≤ 3 s; inspector queries p95 ≤ 500 ms; 8 concurrent
chapter jobs per workspace; Temporal task latency; DB connection pool saturation behavior.

## 12. Definition of test data

- `examples/fixture/` (this repo): bible, spec, contracts, canon delta, knowledge ledger, contrast pairs
  (seed), speech-level cases.
- Recorded model outputs for `ReplayProvider` are produced during implementation and stored in a
  git-LFS or object-storage bucket (not in this planning repo).
