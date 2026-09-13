# Nonfunctional Requirements

## NFR-A Auditability & traceability

| ID | Requirement |
| --- | --- |
| NFR-A.1 | Every LLM call persists: workspace, project, job/workflow id & parent, role, model id + provider + config (temperature, max tokens, seed if any), prompt version hash, context-pack id + manifest hash, canon version read, style profile version, input (full, encrypted at rest), output (full), token usage (input/output/cached), cost, latency, attempt number, error/retry history, schema validation result, evaluation results referencing it, acceptance status of the artifact it produced. |
| NFR-A.2 | Every canon item (fact/event/knowledge/relationship/promise) persists its source manuscript version + evidence spans and the canon commit that introduced/retracted it. |
| NFR-A.3 | Every accepted chapter can be reconstructed as a pipeline trace: contract → pack manifests → drafts → scorecards → patches → acceptance → delta → commit. |
| NFR-A.4 | Audit records are append-only; deletions happen only through retention policies with tombstones. |

## NFR-B Reliability & durability

| ID | Requirement |
| --- | --- |
| NFR-B.1 | Workflows are durable (Temporal). A worker crash at any point resumes from the last completed activity; at most one in-flight LLM call may be repeated. |
| NFR-B.2 | All activities are idempotent via idempotency keys `(workflow_id, step_id, attempt_scope)`; DB writes use upserts keyed by them. |
| NFR-B.3 | Canon commit is a single serializable transaction; partial application is impossible. |
| NFR-B.4 | Provider failures: retries with exponential backoff + jitter, per-error-class policy (429 → backoff+route; 5xx → retry then fallback; timeout → retry with lower max tokens or fallback; invalid JSON → repair attempt ×2 then re-generate ×1 then fail step). |
| NFR-B.5 | Dead-letter: steps that exhaust retries move the job to `needs_attention` with full diagnostics; no silent drop. |
| NFR-B.6 | Cancellation is cooperative and prompt: user cancel is honored within one activity boundary; partial results (drafted scenes) are preserved as non-canonical artifacts. |
| NFR-B.7 | Duplicate job prevention: workflow IDs are deterministic per (project, target, intent, nonce); Temporal's WorkflowIdReusePolicy rejects duplicates; per-target leases prevent parallel edits of the same chapter/plan. |
| NFR-B.8 | RPO ≤ 5 minutes (PITR) in Production; ≤ 24h in MVP (daily snapshot). RTO ≤ 4h Production. |

## NFR-C Performance & scale

| ID | Requirement |
| --- | --- |
| NFR-C.1 | Supports projects with ≥ 3,000 chapters (~18M Korean characters) without degrading context assembly beyond p95 3 s (excluding LLM latency). |
| NFR-C.2 | Context pack assembly for a chapter: p95 ≤ 3 s with warm caches; retrieval queries indexed (entity/time B-trees, GIN for lexical, HNSW for vectors). |
| NFR-C.3 | Chapter production wall time (Standard tier, ~5,500 chars): target ≤ 8 min median, dominated by LLM latency; scene drafting parallelizable where scenes are independent (rare; default sequential). |
| NFR-C.4 | UI reads (inspectors, lists) p95 ≤ 500 ms for projects with 3,000 chapters. |
| NFR-C.5 | Workspace-level concurrency limit for LLM calls (default 8) with fair scheduling across projects. |

## NFR-D Cost

| ID | Requirement |
| --- | --- |
| NFR-D.1 | Hard limits at project/chapter/workflow are enforced pre-call; a call that would exceed remaining budget is not made. |
| NFR-D.2 | Cost estimates before batch runs within ±30% of actual for Standard tier after calibration on ≥ 20 chapters. |
| NFR-D.3 | Context deduplication and provider prompt caching reduce repeated T0/T1 token spend; style blocks and bible excerpts are cache-stable prefixes. |
| NFR-D.4 | Reference targets (Standard tier, 5,500-char chapter): ≤ 14 LLM calls typical, ≤ 22 with one revision round; see `docs/06-system/05-cost-and-observability-plan.md` for the model. |

## NFR-E Security & privacy

| ID | Requirement |
| --- | --- |
| NFR-E.1 | TLS everywhere; AES-256 at rest (DB volume + object storage); application-level encryption for manuscript text and prompts/outputs with per-workspace data keys (envelope encryption via KMS). |
| NFR-E.2 | Secrets in a secret manager; never in DB rows, logs, or repo. |
| NFR-E.3 | Postgres RLS on every tenant table; tests assert cross-tenant reads return zero rows. |
| NFR-E.4 | Provider privacy: only providers/endpoints with no-training/zero-retention terms are enabled by default; per-workspace allowlist; region pinning where offered. |
| NFR-E.5 | Prompt injection: untrusted text always in a data role, wrapped and labelled; instruction-like content classifier; outputs from calls that consumed untrusted text are schema-validated and cannot alter requirements or canon without a human gate. |
| NFR-E.6 | Logs never contain full manuscript text or prompts (only IDs/hashes); full payloads live in encrypted audit storage. |

## NFR-F Data integrity & correctness

| ID | Requirement |
| --- | --- |
| NFR-F.1 | All text NFC-normalized on ingestion; Korean character count defined as Unicode code points after NFC including spaces, excluding markup (ADR-0024). |
| NFR-F.2 | Evidence spans validated on write: quoted text must equal `text[start:end]` of the referenced manuscript version. |
| NFR-F.3 | Facts/events referencing entities must reference existing entity IDs; alias resolution is explicit and logged. |
| NFR-F.4 | Schema-validated structured outputs (JSON Schema 2020-12) for every non-prose call. |
| NFR-F.5 | Migrations forward-only with tested down-paths for the last 3 versions; migration tests run against a fixture DB with a 200-chapter project. |

## NFR-G Observability

| ID | Requirement |
| --- | --- |
| NFR-G.1 | OpenTelemetry traces: workflow → activity → gateway call → provider request; span attributes include role, prompt version, model, canon version, pack id, tokens, cost. |
| NFR-G.2 | Metrics: calls/min, tokens, cost by role/model/project, retry rates, fallback rates, schema failure rate, judge pass rate, revision rounds per chapter, style drift scores, extraction disagreement rate, stale-job rate, queue depths. |
| NFR-G.3 | Dashboards: pipeline health, quality trends per project, cost, provider health. Alerts on error budgets (Beta+). |

## NFR-H Usability & i18n

| ID | Requirement |
| --- | --- |
| NFR-H.1 | UI in Korean and English (Korean-first for text-heavy screens in Beta). All Korean text rendered with mobile-preview mode (narrow column) for chapter review. |
| NFR-H.2 | Every warning displayed with evidence and one-click navigation to the manuscript span and the canon item. |
| NFR-H.3 | Accessibility: keyboard navigation for review queues; WCAG 2.1 AA for core screens (Production). |

## NFR-I Maintainability

| ID | Requirement |
| --- | --- |
| NFR-I.1 | Schemas in `schemas/` are the contract; generated types; contract tests. |
| NFR-I.2 | Prompt changes require passing the prompt regression suite; prompt versions are immutable and content-addressed. |
| NFR-I.3 | Feature flags for evaluator sets, model routing, and gate policies per workspace. |
