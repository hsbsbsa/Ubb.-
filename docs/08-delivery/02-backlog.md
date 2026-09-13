# Prioritized Development Backlog

IDs `B-<phase>-<n>`. Priority P0/P1/P2 within phase. Each item lists requirement refs and acceptance
(tests). Estimates in ideal engineer-days (d). Scope follows the MVP vertical slice (ADR-0036).

## Phase 0 — Foundations

| ID | P | Item | Refs | Acceptance | Est |
| --- | --- | --- | --- | --- | --- |
| B-0-1 | P0 | Monorepo scaffold, CI (incl. planning-package validator), docker-compose, formatter rules that never reflow fixture prose/terminology data | ADR-0001/0021 | CI green on empty packages; fixture files unchanged by formatter | 3d |
| B-0-2 | P0 | Schema → TypeScript type generation + example validation | NFR-I.1 | all `examples/**/*.json` validate; types compile | 2d |
| B-0-3 | P0 | Code-point addressing utilities + cross-runtime conformance vector; length model; NFC boundary; StoryClock ordering | NFR-F.1, ADR-0030, ADR-0034 | conformance vector green in TS + SQL; length model tests | 3d |
| B-0-4 | P0 | DB migrations v1 (tenancy, projects, spec + active constraint sets, entities/naming, register profiles, terminology, manuscripts w/ language constraint, canon incl. proposition truths, dependency edges w/ materiality, embedding sets, packs, llm_calls, budgets) + RLS | data arch, NFR-E.3, ADR-0031/0032/0033/0035 | pgTAP: RLS isolation; constraints | 7d |
| B-0-5 | P0 | `canon.commit_delta` SQL function (atomic, optimistic version) + evidence trigger (code-point semantics) | FR-7.4, NFR-B.3, NFR-F.2 | fault-injection tests; racing commits; non-BMP evidence | 4d |
| B-0-6 | P0 | Gateway: adapters ×2 + mock/replay/fault, routing table, **Narrative Identity Guard (both contracts)**, **output-language check**, budget guard, idempotency, schema validation, audit rows (identity + contract hashes), OTel | FR-9.6, FR-6.2, FR-4.10, NFR-A.1, NFR-D.1, ADR-0027 | guard tests (missing either contract); language check rejects Korean mock output; idempotent replay; cost accounting | 8d |
| B-0-7 | P0 | Prompt registry + loader + hashing + prompt sets + regression runner skeleton | ADR-0016, NFR-I.2 | version immutability tests | 4d |
| B-0-8 | P0 | `packages/prose` core: language identification, English tokenizer/POS, registry primitives, grammar-service client interface (service optional) | ADR-0028 | language-id accuracy on test set; interface mockable | 4d |
| B-0-9 | P0 | API skeleton: auth, workspace middleware, projects CRUD; worker bootstrap | FR-11.1/11.2 | authz matrix tests | 5d |
| B-0-10 | P1 | Seed script: load fixture bible/spec/contracts/profiles | fixture | seed idempotent | 2d |

## Phase 1 — Canon core & narrative identity core

| ID | P | Item | Refs | Acceptance | Est |
| --- | --- | --- | --- | --- | --- |
| B-1-1 | P0 | Narrative identity model (8 layers), `lang/en` + `tradition/kr-webnovel` + 4 genre profiles as data, composition (merge patch), validation, calibration records | FR-6.1, FR-6.13, ADR-0026/0029 | compose tests; conflict manifest; preferences cannot override contracts | 5d |
| B-1-2 | P0 | Narrative Identity Block compiler (roles, budgets, shedding, IDENTITY_TAIL, hash, separate contract hashes, cache) | FR-6.3 | determinism; contracts always first/never shed; overflow error | 4d |
| B-1-3 | P0 | English Prose Lint EP-* incl. translation markers, calques, honorific morphemes, locale, registry, repetition (simhash), format | FR-6.4, FR-6.10, FR-5.1 | rule fixtures; contrast-set separation ≥ 90% | 8d |
| B-1-4 | P0 | Structure Lint ST-* (hook, opening/ending classifiers, payoff markers, exposition runs, ratios, cadence windows, device grammar) | FR-6.6, FR-3.8 | `western_english`/`weak_serial` flagged ≥ 80% | 5d |
| B-1-5 | P0 | Dialogue-register check RG-* (expected register from policy + relationship state; rendered-register features; shift tags) | FR-6.5 | T9/T13/T21 fixtures; register cases | 5d |
| B-1-6 | P0 | Exemplar bank (accepted-only FK, provenance, selection; English) | FR-6.9, ADR-0025 | trigger tests | 2d |
| B-1-7 | P0 | Extraction pre-pass (registry NER w/ code-point offsets, status-window numbers, utterance annotations) | FR-7.2 | fixture recall | 4d |
| B-1-8 | P0 | Reconciler (canonicalize, match, classify agreed/single/conflict) incl. `proposition_truth` items | FR-7.3, ADR-0031 | T20/T22 fixtures; P5 truth on main | 4d |
| B-1-9 | P0 | Evidence verifier (exact/fuzzy anchoring on code points, entity resolution via registry, frame rules, future-validity check, locked-fact & leak pre-checks) | FR-7.3, FR-7.6, FR-7.8 | rejects paraphrase; blocks plan-frame; T7 | 4d |
| B-1-10 | P0 | Commit orchestration + dependency edges (materiality, claim-based promotion) + stale marking + rollback(latest) + retcon diff | FR-7.4, 7.12, 7.15, 7.16, 7.18, ADR-0032 | R1 (material vs contextual)/C1/RB1 | 6d |
| B-1-11 | P0 | Knowledge ledger service (stances, channels, guards, per-timeline truth queries) | FR-7.7/7.8 | knowledge matrix fixture | 4d |
| B-1-12 | P0 | Relationship & register tracking; promise ledger service | FR-7.9, FR-3.4 | fixtures | 3d |
| B-1-13 | P0 | Retrieval: search_documents pipeline (English FTS + registry thesaurus), embedding sets + re-embed job + active flip, hybrid query, ranker | FR-8.3, ADR-0035 | recall@pack targets; set-switch test | 6d |
| B-1-14 | P0 | Context assembler: query plan, tiers, Active Constraint Set consumption, compressors, renderer, validation (both contract hashes), manifest w/ materiality, cache; MVP templates | FR-8.1/8.2/8.4/8.5, ADR-0033 | determinism; T0 validation; degraded paths | 8d |
| B-1-15 | P0 | Summaries L1–L4 activities (English) | FR-7.11 | fidelity tests | 2d |
| B-1-16 | P1 | Timelines (prior loop, divergence flags via per-timeline truth) | FR-7.10, ADR-0023/0031 | T8/T15 fixtures | 3d |
| B-1-17 | P0 | Active Constraint Set compiler (scope filter, dedupe, cap, overflow error) | FR-1.8, ADR-0033 | cap tests | 3d |

## Phase 2 — Planning & production pipeline

| ID | P | Item | Refs | Acceptance | Est |
| --- | --- | --- | --- | --- | --- |
| B-2-1 | P0 | RequirementInterpretation workflow (any input language → English working text) + conflict detection + injection classifier (incl. attempts to change output language) | FR-1.1–1.8, FR-11.4 | fixture spec reproduces hard/soft/assumption split | 4d |
| B-2-2 | P0 | Concept workflow (N candidates, pairwise both orders, tie rules) | FR-2.1, ADR-0015 | position-bias tests | 3d |
| B-2-3 | P0 | StoryBible workflow (specialists, register profiles, naming registry, terminology policy, identity binder, consistency checker, bible commit v1) | FR-2.2–2.8 | fixture bible reproduced structurally | 7d |
| B-2-4 | P0 | SeriesPlanning + PlanningHorizon workflows; promise scheduling; plan validators; cadence checks; Active Constraint Set per chapter | FR-3.1–3.8 | contracts validate; stale on material commits | 8d |
| B-2-5 | P0 | ChapterProduction workflow: preflight, scene plan (register pre-resolution), scene writer loop with **output-language gate**, assembler, deterministic checks | FR-4.1–4.4, FR-4.10 | happy path w/ mock; Korean-output mock rejected | 6d |
| B-2-6 | P0 | Evaluators (contract, continuity, knowledge, promise, **prose**, **structure**, genre, voice, repetition) + scorecard sections + severity policy + clustering by dimension | FR-5.1–5.4, FR-5.7 | trap detections incl. T23–T29 | 9d |
| B-2-7 | P0 | RevisionWorkflow: dimension-targeted revisers, patch application, regression re-checks (no cross-dimension regression), limits, escalation | FR-5.5/5.6, FR-6.8 | T1–T6, T18, T23–T25 repaired at spec'd scope; T17 escalates | 6d |
| B-2-8 | P0 | CanonCommit child workflow (extract ∥, reconcile, adjudicate, verify, commit, edge promotion, post-commit) | FR-7.2–7.4 | fixture deltas | 4d |
| B-2-9 | P0 | Gates per mode; signals approve/reject/request-changes/override; change_request_interpreter | FR-4.9, ADR-0019 | workflow tests | 4d |
| B-2-10 | P0 | Batch workflow; pause/cancel/resume; leases; stale-canon re-validation | FR-4.7, FR-7.12/7.13, NFR-B | chaos cases | 4d |
| B-2-11 | P0 | Regeneration/Retcon/Correction workflows (MVP scope) + dependency report (material/contextual) | FR-4.8, FR-7.14/7.15 | R1/C1 | 4d |
| B-2-12 | P0 | Budgets & cost prediction v1 (words); quality tiers; usage aggregation | FR-9.1–9.3 | hard-limit tests | 4d |
| B-2-13 | P0 | API endpoints for plans/production/canon/jobs/costs; SSE | API plan | contract tests | 6d |
| B-2-14 | P0 | Prompt regression golden cases from fixture (all MVP roles) incl. contrast sets + output-language assertions | NFR-I.2 | suite runs in CI (replay) | 5d |
| B-2-15 | P0 | P-class model benchmark harness (English-under-KWN) and routing table publication | gateway §3 | benchmark report recorded | 3d |
| B-2-16 | P1 | Candidate comparison for chapters (mechanism; off by default) + early stop | FR-4.5 | tests | 3d |
| B-2-17 | P1 | Export TXT/DOCX workflow (locale typography, romanized-term glossary) | FR-10.1 | typography check | 3d |

## Phase 3 — UI

| ID | P | Item | Refs | Est |
| --- | --- | --- | --- | --- |
| B-3-1 | P0 | App shell, auth, workspace/project navigation, English UI (i18n scaffolding) | NFR-H | 4d |
| B-3-2 | P0 | Requirements & Assumption Review; Directions composer with re-plan preview | UW-1, UW-7 | 5d |
| B-3-3 | P0 | Concept Compare | UW-2 | 3d |
| B-3-4 | P0 | Bible screens incl. register profile matrix, naming registry, terminology policy, narrative identity + block preview (both contracts), locks | UW-3 | 8d |
| B-3-5 | P0 | Plan boards & contract editor with validation panel | UW-4 | 6d |
| B-3-6 | P0 | Chapter Review (manuscript mobile view, per-dimension scorecard, issues w/ evidence, candidates, delta preview, trace) | UW-5, 11, 12, 17 | 10d |
| B-3-7 | P0 | Canon inspectors (timeline w/ per-timeline truth, entity state, knowledge matrix, relationships w/ register, promises, commits/stale + review-suggested) | UW-8, 13 | 9d |
| B-3-8 | P0 | Jobs/Attention with SSE; Costs; Budgets; Export | UW-6, 14, 15, 16 | 6d |
| B-3-9 | P1 | Retcon/regeneration flows with dependency reports | UW-9, 10 | 3d |

## Phase 4 — Hardening

| ID | P | Item | Est |
| --- | --- | --- | --- |
| B-4-1 | P0 | Long-form 120-chapter replay test; nightly live 20-chapter run (zero output-language failures) | 5d |
| B-4-2 | P0 | Chaos suite completion; provider fallback drills | 4d |
| B-4-3 | P0 | Backup/restore, secret rotation, runbooks | 3d |
| B-4-4 | P0 | Security test suite; dependency & secret scanning gates | 3d |
| B-4-5 | P0 | Bilingual reviewer evaluation round; threshold calibration to `contrast_calibrated`; contrast set to 100 | 4d |
| B-4-6 | P1 | Cost calibration; dashboards | 3d |

## Phase 5 — Beta (summary items)

Autopilot & escalation (5d) · 6 genre profiles (6d) · automated retcon patches (6d) · arbitrary rollback
(4d) · feedback import & signals (6d) · EPUB/platform exports (4d) · members/roles (4d) · alerting/PITR
(4d) · similarity screening (5d) · optional grammar-service integration (3d) · semi-automatic threshold
calibration (5d) · contrast set 200 (ongoing) · Korean UI localization (4d) · OAuth providers, 2FA (3d).
