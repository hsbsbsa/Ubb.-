# Architecture Decision Records

| ADR | Title |
| --- | --- |
| [0001](0001-typescript-monorepo-with-python-nlp-sidecar.md) | TypeScript monorepo (optional English grammar service) |
| [0002](0002-postgres-single-system-of-record.md) | Postgres 16 + pgvector as the single system of record |
| [0003](0003-temporal-for-durable-workflows.md) | Temporal for durable, resumable workflows |
| [0004](0004-provider-independent-model-gateway.md) | Provider-independent model gateway with role-based routing |
| [0005](0005-fail-closed-style-guard.md) | Fail-closed guard on every style-sensitive call — *superseded by 0027* |
| [0006](0006-bitemporal-facts-with-evidence.md) | Bitemporal facts with mandatory evidence spans |
| [0007](0007-reality-frames.md) | Reality frames on events and derived facts |
| [0008](0008-proposition-centric-knowledge-ledger.md) | Proposition-centric knowledge ledger |
| [0009](0009-accepted-only-canon-with-atomic-commit.md) | Accepted-chapter-only canon, two-extractor reconciliation, atomic commit |
| [0010](0010-tiered-context-packs.md) | Tiered, manifested, deterministic context packs |
| [0011](0011-hybrid-retrieval.md) | Hybrid retrieval: structured + lexical + vector + graph |
| [0012](0012-rolling-horizon-hierarchical-planning.md) | Rolling-horizon hierarchical planning |
| [0013](0013-chapter-contract-as-acceptance-unit.md) | Chapter Contract as the unit of acceptance |
| [0014](0014-patch-first-revision.md) | Patch-first revision with regression re-checks |
| [0015](0015-position-swapped-pairwise-judging.md) | Position-swapped pairwise judging with tie rules and early stop |
| [0016](0016-prompt-registry-with-versioning.md) | Prompt registry with immutable versions and regression gating |
| [0017](0017-korean-nlp-sidecar.md) | Korean morphological analysis sidecar — *superseded by 0028* |
| [0018](0018-hard-budgets-and-quality-tiers.md) | Hard budgets at project/chapter/workflow with quality tiers |
| [0019](0019-assisted-default-mode.md) | Assisted mode as default; Semi-automatic after first arc; Autopilot in Beta |
| [0020](0020-workspace-isolation-with-rls.md) | Workspace isolation with Postgres RLS and envelope encryption |
| [0021](0021-repository-structure.md) | Repository structure for the implementation |
| [0022](0022-immutable-manuscript-versions.md) | Immutable manuscript versions with span addressing |
| [0023](0023-timelines-for-regression.md) | Explicit timelines for regression/possession/alternate realities |
| [0024](0024-nfc-normalization-and-character-counting.md) | NFC normalization and character counting — *superseded by 0030/0034* |
| [0025](0025-exemplar-and-imitation-policy.md) | Exemplar sourcing and non-imitation policy |
| [0026](0026-english-manuscript-korean-webnovel-tradition.md) | **English is the manuscript language; Korean webnovel is the narrative tradition** (governing) |
| [0027](0027-narrative-identity-guard.md) | Fail-closed Narrative Identity Guard requiring both contracts |
| [0028](0028-english-prose-tooling-replaces-korean-nlp.md) | English prose tooling replaces the Korean NLP sidecar |
| [0029](0029-calibration-dependent-thresholds.md) | Numeric style thresholds are configuration with calibration status |
| [0030](0030-unicode-code-point-addressing.md) | One Unicode-safe text addressing system across all runtimes |
| [0031](0031-per-timeline-proposition-truth.md) | Proposition truth is recorded per timeline with validity |
| [0032](0032-material-vs-contextual-dependency-edges.md) | Dependency edges distinguish material from contextual dependencies |
| [0033](0033-active-constraint-set.md) | Hard requirements compiled into a scope-filtered Active Constraint Set |
| [0034](0034-language-neutral-length-model.md) | Language-neutral length model; words are the author-facing unit for English |
| [0035](0035-provider-independent-embedding-migrations.md) | Embedding sets versioned per model with atomic active-set switching |
| [0036](0036-mvp-vertical-slice.md) | MVP re-scoped to a vertical slice with all foundational invariants |

New ADRs: copy `0000-adr-template.md`, take the next number, link it here, and update the traceability
matrix in the same change.
