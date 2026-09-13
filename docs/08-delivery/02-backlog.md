# Prioritized Development Backlog

IDs `B-<phase>-<n>`. Priority P0/P1/P2 within phase. Each item lists requirement refs and acceptance
(tests). Estimates in ideal engineer-days (d).

## Phase 0 — Foundations

| ID | P | Item | Refs | Acceptance | Est |
| --- | --- | --- | --- | --- | --- |
| B-0-1 | P0 | Monorepo scaffold, CI, docker-compose, lint rules that never reflow Korean | ADR-0001/0021 | CI green on empty packages; Korean fixture files unchanged by formatter | 3d |
| B-0-2 | P0 | Schema → TypeScript type generation + example validation | NFR-I.1 | all `examples/**/*.json` validate; types compile | 2d |
| B-0-3 | P0 | Character counting, NFC boundary, StoryClock ordering utilities | NFR-F.1, ADR-0024 | unit tests incl. jamo edge cases | 2d |
| B-0-4 | P0 | DB migrations v1 (tenancy, projects, spec, entities, manuscripts, canon, packs, llm_calls, budgets) + RLS | data arch §1–9, NFR-E.3 | pgTAP: RLS isolation; constraints | 6d |
| B-0-5 | P0 | `canon.commit_delta` SQL function (atomic, optimistic version) + evidence trigger | FR-7.4, NFR-B.3, NFR-F.2 | fault-injection tests; racing commits | 4d |
| B-0-6 | P0 | Gateway: adapters ×2 + mock/replay/fault, routing table, Style Guard, budget guard, idempotency, schema validation, audit rows, OTel | FR-9.6, FR-6.2, NFR-A.1, NFR-D.1 | guard tests; idempotent replay; cost accounting | 8d |
| B-0-7 | P0 | Prompt registry + loader + hashing + prompt sets + regression runner skeleton | ADR-0016, NFR-I.2 | version immutability tests | 4d |
| B-0-8 | P0 | Korean NLP sidecar (analyze/endings/honorifics/tokens) + client + cache | ADR-0017 | accuracy tests on labeled set | 5d |
| B-0-9 | P0 | API skeleton: auth, workspace middleware, projects CRUD; worker bootstrap | FR-11.1/11.2 | authz matrix tests | 5d |
| B-0-10 | P1 | Seed script: load fixture bible/spec/contracts | fixture | seed idempotent | 2d |

## Phase 1 — Canon core & Korean style core

| ID | P | Item | Refs | Acceptance | Est |
| --- | --- | --- | --- | --- | --- |
| B-1-1 | P0 | Style profile model, base + 8 overlays as data, compose (merge patch), validation | FR-6.1 | compose tests; conflict manifest | 4d |
| B-1-2 | P0 | Style Block compiler (roles, budgets, shedding, TAIL, hash, cache) | FR-6.3 | determinism; overflow error | 4d |
| B-1-3 | P0 | Lint rules KL-* incl. translation markers, repetition (simhash), format, glossary | FR-6.4, FR-6.10, FR-5.1 | rule fixtures; contrast pairs separation ≥ 90% | 8d |
| B-1-4 | P0 | Register check (speaker resolution, level classification, profile/relationship comparison, shift tags) | FR-6.5 | T9/T13/T21 fixtures | 6d |
| B-1-5 | P0 | Exemplar bank (accepted-only FK, provenance, selection) | FR-6.9, ADR-0025 | trigger tests | 2d |
| B-1-6 | P0 | Extraction pre-pass (glossary NER w/ offsets, 상태창 numbers, utterance annotations) | FR-7.2 | fixture recall | 4d |
| B-1-7 | P0 | Reconciler (canonicalize, match, classify agreed/single/conflict) | FR-7.3 | T20/T22 fixtures | 4d |
| B-1-8 | P0 | Evidence verifier (exact/fuzzy anchoring, entity resolution, frame rules, future-validity check, locked-fact & leak pre-checks) | FR-7.3, FR-7.6, FR-7.8 | rejects paraphrase; blocks plan-frame; T7 | 4d |
| B-1-9 | P0 | Commit orchestration + dependency edges + stale marking + rollback(latest) + retcon diff | FR-7.4, 7.12, 7.15, 7.16 | R1/C1/RB1 | 6d |
| B-1-10 | P0 | Knowledge ledger service (stances, channels, guards, queries) | FR-7.7/7.8 | knowledge matrix fixture | 4d |
| B-1-11 | P0 | Relationship & address-term tracking; promise ledger service | FR-7.9, FR-3.4 | fixtures | 3d |
| B-1-12 | P0 | Retrieval: search_documents pipeline, Korean tokenization, embeddings, hybrid query, ranker | FR-8.3 | recall@pack targets | 6d |
| B-1-13 | P0 | Context assembler: query plan, tiers, compressors, renderer, validation, manifest, cache; MVP templates | FR-8.1/8.2/8.4/8.5 | determinism; T0 validation; degraded paths | 8d |
| B-1-14 | P0 | Summaries L1–L4 activities | FR-7.11 | fidelity tests | 2d |
| B-1-15 | P1 | Timelines (prior loop, divergence flags) | FR-7.10, ADR-0023 | T8/T15 fixtures | 3d |

## Phase 2 — Planning & production pipeline

| ID | P | Item | Refs | Acceptance | Est |
| --- | --- | --- | --- | --- | --- |
| B-2-1 | P0 | RequirementInterpretation workflow + prompts + conflict detection + injection classifier | FR-1.1–1.7, FR-11.4 | fixture spec reproduces hard/soft/assumption split | 4d |
| B-2-2 | P0 | Concept workflow (N candidates, pairwise both orders, tie rules) | FR-2.1, ADR-0015 | position-bias tests | 3d |
| B-2-3 | P0 | StoryBible workflow (specialists, glossary, speech profiles, style binder, consistency checker, bible commit v1) | FR-2.2–2.7 | fixture bible reproduced structurally | 6d |
| B-2-4 | P0 | SeriesPlanning + PlanningHorizon workflows; promise scheduling; plan validators; cadence checks | FR-3.1–3.8 | contracts validate; stale on commit | 8d |
| B-2-5 | P0 | ChapterProduction workflow: preflight, scene plan, scene writer loop, assembler, deterministic checks | FR-4.1–4.4 | happy path w/ mock | 6d |
| B-2-6 | P0 | Evaluators (7) + scorecard merge + severity policy + issue clustering | FR-5.1–5.4 | trap detections | 8d |
| B-2-7 | P0 | RevisionWorkflow: revisers, patch application, regression re-checks, limits, escalation | FR-5.5/5.6, FR-6.8 | T1–T6 repaired; T17 escalates | 6d |
| B-2-8 | P0 | CanonCommit child workflow (extract ∥, reconcile, adjudicate, verify, commit, post-commit) | FR-7.2–7.4 | fixture deltas | 4d |
| B-2-9 | P0 | Gates per mode; signals approve/reject/request-changes/override; change_request_interpreter | FR-4.9, ADR-0019 | workflow tests | 4d |
| B-2-10 | P0 | Batch workflow; pause/cancel/resume; leases; stale-canon re-validation | FR-4.7, FR-7.12/7.13, NFR-B | chaos cases | 4d |
| B-2-11 | P0 | Regeneration/Retcon/Correction workflows (MVP scope) + dependency report | FR-4.8, FR-7.14/7.15 | R1/C1 | 4d |
| B-2-12 | P0 | Budgets & cost prediction v1; quality tiers; usage aggregation | FR-9.1–9.3 | hard-limit tests | 4d |
| B-2-13 | P0 | API endpoints for plans/production/canon/jobs/costs; SSE | API plan | contract tests | 6d |
| B-2-14 | P0 | Prompt regression golden cases from fixture (all MVP roles) | NFR-I.2 | suite runs in CI (replay) | 5d |
| B-2-15 | P1 | Candidate comparison for chapters (Premium) + early stop | FR-4.5 | tests | 3d |
| B-2-16 | P1 | Export TXT/DOCX workflow | FR-10.1 | Korean typography check | 3d |

## Phase 3 — UI

| ID | P | Item | Refs | Est |
| --- | --- | --- | --- | --- |
| B-3-1 | P0 | App shell, auth, workspace/project navigation, i18n (ko/en) | NFR-H | 4d |
| B-3-2 | P0 | Requirements & Assumption Review; Directions composer with re-plan preview | UW-1, UW-7 | 5d |
| B-3-3 | P0 | Concept Compare | UW-2 | 3d |
| B-3-4 | P0 | Bible screens incl. speech profile matrix, style profile + block preview, locks | UW-3 | 7d |
| B-3-5 | P0 | Plan boards & contract editor with validation panel | UW-4 | 6d |
| B-3-6 | P0 | Chapter Review (manuscript mobile view, issues w/ evidence, scorecard, candidates, delta preview, trace) | UW-5, 11, 12, 17 | 10d |
| B-3-7 | P0 | Canon inspectors (timeline, entity state, knowledge matrix, relationships, promises, commits/stale) | UW-8, 13 | 9d |
| B-3-8 | P0 | Jobs/Attention with SSE; Costs; Budgets; Export | UW-6, 14, 15, 16 | 6d |
| B-3-9 | P1 | Retcon/regeneration flows with dependency reports | UW-9, 10 | 3d |

## Phase 4 — Hardening

| ID | P | Item | Est |
| --- | --- | --- | --- |
| B-4-1 | P0 | Long-form 120-chapter replay test; nightly live 20-chapter run | 5d |
| B-4-2 | P0 | Chaos suite completion; provider fallback drills | 4d |
| B-4-3 | P0 | Backup/restore, secret rotation, runbooks | 3d |
| B-4-4 | P0 | Security test suite; dependency & secret scanning gates | 3d |
| B-4-5 | P0 | Human editor evaluation round; threshold tuning; contrast set to 120 | 4d |
| B-4-6 | P1 | Cost calibration; dashboards | 3d |

## Phase 5 — Beta (summary items)

Autopilot & escalation (5d) · 8 overlays (8d) · automated retcon patches (6d) · arbitrary rollback (4d) ·
feedback import & signals (6d) · EPUB/platform exports (4d) · members/roles (4d) · alerting/PITR (4d) ·
similarity screening (5d) · preference learning (6d) · contrast set 300 (ongoing) · OAuth Kakao/Naver, 2FA
(3d).
