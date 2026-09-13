# Scope and Release Tiers

Four tiers: **MVP** (internal usable product, one workspace, a few power users), **Public Beta** (invited
external authors), **Production** (paying customers, SLAs), **Future** (roadmap ideas, not committed).

The rule for MVP scoping: **do not over-engineer, but never postpone the foundations** that cannot be
retrofitted — canon management, temporal state, character knowledge, evidence provenance, Korean style
enforcement, prompt versioning, context construction, rejected-draft isolation, durable checkpoints, atomic
canon commits. Everything on that list is MVP.

## 1. Tier matrix

Legend: ✅ in tier · ◐ partial (noted) · ⏩ later tier · — not planned

### 1.1 Product surface

| Capability | MVP | Beta | Prod | Future |
| --- | --- | --- | --- | --- |
| Create project; minimal or advanced requirement intake (structured form + free text) | ✅ | ✅ | ✅ | |
| Requirement interpretation → Story Spec with hard/soft/assumption classification | ✅ | | | |
| Assumption review (confirm / edit / reject each) | ✅ | | | |
| Concept candidates (2–3) with comparison view | ✅ | | | |
| Story bible generation & editing; fact locking | ✅ | | | |
| Series blueprint, season, arc plans; rolling-horizon chapter contracts | ✅ | | | |
| Chapter generation (single) with full pipeline | ✅ | | | |
| Chapter batch generation (sequential, N chapters) | ✅ | | | |
| Running directions ("from now on…", "in the next arc…") | ✅ | | | |
| Candidate comparison for chapters (N=2) | ◐ Premium tier only | ✅ | ✅ | |
| Continuity warnings, quality scorecards, evidence view | ✅ | | | |
| Canon inspector: facts, timeline, character state history, knowledge matrix, relationships, promises | ✅ | | | |
| User corrections to canon (fact edit with cascade analysis) | ✅ | | | |
| Retcon workflow (change accepted chapter text + canon, propagate) | ◐ mark-stale + manual patches | ✅ automated patch proposals | ✅ | |
| Chapter regeneration (with dependency report) | ✅ | | | |
| Approve / reject / request-changes on chapters | ✅ | | | |
| Cost dashboard (project, chapter, workflow; per accepted chapter & per 1k Korean chars) | ✅ | | | |
| Pause / cancel / resume jobs | ✅ | | | |
| Export TXT / DOCX per volume and whole series | ✅ | ✅ +EPUB, platform profiles | ✅ | |
| Operating modes | Assisted, Semi-auto | +Autopilot | | |
| Reader feedback import (manual paste, sanitized) | — | ✅ | ✅ | |
| Multiple projects per workspace, members & roles | ◐ owner + editor | ✅ | ✅ | |
| Korean UI localization | ◐ key screens | ✅ | ✅ | |
| "Ask the canon" constrained Q&A inspector | — | ✅ | ✅ | |
| Alternate timelines UI (regression loops) | ◐ data model + basic view | ✅ | ✅ | |
| Real-time collaborative editing | — | — | — | ✅ |
| Cover/illustration generation | — | — | — | ✅ |
| Platform direct publishing | — | — | — | ✅ |
| Translation export | — | — | — | ✅ |

### 1.2 Korean style system

| Capability | MVP | Beta | Prod | Future |
| --- | --- | --- | --- | --- |
| Style Profile model (base + genre overlay + project override), versioned | ✅ | | | |
| Genre overlays shipped | 8 core (hunter/gate, system-progression, regression, modern fantasy, murim, romance fantasy, villainess, academy) | +8 (possession, reincarnation, dungeon, apocalypse/survival, management, idol/entertainment, game-world, comedy) | +character drama, slow-burn romance refinements | community/custom overlays |
| Style Block compiler with role-specific budgets | ✅ | | | |
| Style Guard (fail-closed) in gateway | ✅ | | | |
| Deterministic Korean Lint (ending repetition, pronoun density, translation-ese markers, paragraph/sentence length, dialogue ratio, punctuation, format drift) | ✅ | | | |
| Speech-level & honorific consistency check (rule + morphological analyzer) | ✅ | ✅ improved coverage | | |
| Model-based Style Judge with evidence spans | ✅ | | | |
| Passage-level style repair | ✅ | | | |
| Project exemplar bank (from accepted chapters + user-owned) | ✅ | | | |
| Contrast-pair calibration set for judge | ◐ seed set (~60 pairs) | ✅ 300+ | ✅ | |
| Character speech profiles & voice-drift detection | ✅ | | | |
| User style preference learning from edits | — | ◐ | ✅ | |

### 1.3 Memory, canon, knowledge

| Capability | MVP | Beta | Prod | Future |
| --- | --- | --- | --- | --- |
| Immutable manuscript versions with evidence spans | ✅ | | | |
| Bitemporal facts (validity + assertion) | ✅ | | | |
| Canonical events with reality frames | ✅ | | | |
| Knowledge ledger (character/narrator/reader × proposition × stance) | ✅ | | | |
| Relationship states with history; address-term tracking | ✅ | | | |
| Timeline model incl. alternate timelines | ✅ data model; UI basic | ✅ | | |
| Promise ledger | ✅ | | | |
| Hierarchical summaries L1–L4 | ✅ | | | |
| Two-extractor canon extraction + reconciliation + evidence verification | ✅ | | | |
| Atomic canon commit, canon versions, stale detection, dependency edges | ✅ | | | |
| Context pack assembler (tiers, ranking, compression, manifest, caching) | ✅ | | | |
| Hybrid retrieval (structured + lexical + vector + graph hops) | ✅ | ✅ tuned reranker | | |
| Rollback to canon version | ◐ read-only time travel + rollback of last commit | ✅ arbitrary | | |
| Retcon propagation with automated patch proposals | ◐ | ✅ | | |

### 1.4 Platform

| Capability | MVP | Beta | Prod | Future |
| --- | --- | --- | --- | --- |
| Model gateway: providers, routing, retries, fallback, structured-output validation, cost accounting | ✅ | | | |
| Prompt registry with versioning & regression suite | ✅ | | | |
| Temporal workflows with checkpoints, idempotency, cancellation | ✅ | | | |
| Budgets & hard limits (project/chapter/workflow), cost prediction | ✅ | ✅ better prediction | | |
| Observability: traces per call, structured logs, metrics, dashboards | ✅ | ✅ alerting | ✅ SLOs | |
| Auth (email + OAuth), workspace RLS, RBAC (owner/editor/viewer) | ✅ | ✅ SSO optional | | |
| Encryption at rest/in transit, secret manager | ✅ | | | |
| Audit log | ✅ | | | |
| Backups & PITR; restore drills | ◐ daily | ✅ PITR | ✅ drills | |
| Data retention, deletion, full export | ◐ export; deletion basic | ✅ | ✅ | |
| Provider privacy controls (no-training flags, regional routing) | ✅ config | ✅ | | |
| Prompt-injection defenses for imported text | ✅ | | | |
| Similarity check against user-provided corpus | — | ✅ | ✅ + optional external service | |
| AI-assistance disclosure options in export | ◐ | ✅ | | |
| Load testing, chaos testing | — | ◐ | ✅ | |

## 2. MVP definition (what "done" looks like)

A single workspace user can: create a project from a 3-paragraph Korean premise + form; review and confirm
assumptions; pick a concept; approve a story bible with locked facts; approve a series blueprint and first
arc plan; generate chapter 1 → N in Semi-automatic mode with Assisted gates on the first arc; see scorecards
and continuity issues with evidence; correct a fact and see the dependency report; regenerate a chapter;
inspect character knowledge and relationships; view costs; pause/resume/cancel; export a volume as DOCX.
The **fixture story** (`docs/07-quality/02-fixture-story.md`) passes all continuity traps end to end.

## 3. Deferred by design (and why it is safe to defer)

| Deferred | Why safe | Prerequisite kept in MVP |
| --- | --- | --- |
| Autopilot | Same pipeline; only gate policy differs | Mode enum + gate policy abstraction |
| Automated retcon patch proposals | Dependency edges + stale marking exist; patches are the same patch primitive used in revision | Dependency edges, patch primitive |
| Reader feedback import | Sanitization pipeline reused from imported documents | Untrusted-text sanitizer |
| EPUB/platform export | Export from the same manuscript versions | Export service abstraction |
| Similarity service | Provenance + exemplar policy already prevent imitation by construction | Exemplar provenance |
| Arbitrary rollback | Canon versions + deltas are already stored; inverse application is engineering effort | Deltas stored with inverse |
