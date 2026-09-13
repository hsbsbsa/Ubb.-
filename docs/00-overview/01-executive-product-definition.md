# Executive Product Definition — Yeonjae Studio (연재 스튜디오)

## 1. One-paragraph definition

Yeonjae Studio is a stateful, resumable, auditable **AI production studio for Korean webnovels**. A user
supplies a premise and a set of requirements (genre, characters, world concept, tropes, forbidden
developments, audience, tone, romance preferences, progression system, ending preference, chapter count,
target Korean characters per chapter, mandatory scenes, content restrictions) and, later, running
directions and corrections. The studio turns those inputs into a story specification, a story bible, a
hierarchical series plan, per-chapter contracts, natively Korean serialized prose, edited and
continuity-checked chapters, a canonical story memory that stays coherent across hundreds or thousands of
chapters, and an exportable manuscript. It does this with many purposeful, individually audited LLM calls
orchestrated by durable workflows over a canonical story database — never with one enormous prompt or one
long chat.

## 2. The two problems this product exists to solve

### 2.1 "It reads like a translated Western novel"

Earlier attempts (a Kimi K3 experiment among them) produced fiction that was Korean in vocabulary but
Western in bones: long descriptive paragraphs, pronoun-heavy sentences (그/그녀), adverb-tagged dialogue,
metaphor chains, literary exposition, slow hooks, no serial momentum. A single "write like a Korean webnovel"
instruction does not survive a multi-call pipeline. Yeonjae Studio solves this **architecturally**:

- A versioned, genre-aware **Style Profile** is compiled into a **Style Block** that is *mandatory* on every
  style-sensitive LLM call. The model gateway **fails closed** if a style-sensitive call lacks it
  (ADR-0005).
- Style is enforced at three layers: generation (style block + project's own approved exemplars),
  **deterministic Korean lint** (sentence-ending repetition, pronoun density, translation-ese markers,
  paragraph length, dialogue ratio, speech-level consistency), and a **model-based Korean webnovel style
  judge** with evidence spans, calibrated on contrast pairs.
- Drift is repaired at the **passage level** with targeted patches, not by regenerating chapters.

### 2.2 "It forgets what happened"

The model is never the memory. The application holds **canon** in Postgres: bitemporal facts with exact
manuscript evidence, canonical events with reality frames (canonical / flashback / dream / lie /
prediction / plan / prior-loop), a proposition-centric **knowledge ledger** that records what each
character (and the narrator and the reader) knows, suspects, falsely believes, or pretends, relationship
states, timelines, promise ledger, and hierarchical summaries. A **Context Pack** for every chapter is
assembled deterministically from canon under a token budget with protected tiers, versioned, and recorded.
Only an **accepted** chapter may update canon, through a two-extractor reconciliation with evidence
verification and a single **atomic canon commit**. Rejected drafts never touch canon.

## 3. Who it is for

| Persona | Need | How the studio serves it |
| --- | --- | --- |
| **Solo webnovel author (primary)** | Produce a long serialized novel from a concept, keep control over story truth, fix mistakes without rewriting everything | Assisted mode with approval gates, canon inspector, corrections/retcons, targeted regeneration |
| **Small studio / editor** | Run several series, review quality and continuity, keep costs predictable | Workspaces, review queues, scorecards, budgets, audit trail |
| **Platform / publisher team (later)** | Export-ready manuscripts, disclosure options, rights provenance | Export profiles, AI-assistance disclosure, provenance records |

Not for: readers (no reading app), translation, or imitation of specific authors/works.

## 4. Product principles

1. **Application-owned truth.** Canon lives in the database, with evidence. The model proposes; the system
   verifies and commits.
2. **Korean-first, genre-aware.** Korean webnovel form is a design constraint at every layer, not a prompt.
3. **Planned ≠ happened.** Plans, predictions, dreams, lies and rejected drafts are stored in their own
   frames and can never be mistaken for canon.
4. **Purposeful calls.** Every LLM call has a role, a versioned prompt, a context pack, a schema, a budget
   and an audit record. Volume of calls is not a proxy for quality.
5. **Repair locally.** Prefer a sentence/paragraph/scene patch over a chapter rewrite; regression-test the
   patch.
6. **Durable and resumable.** Any workflow can be paused, crash, or be cancelled and resume from the last
   checkpoint without duplicating spend or corrupting state.
7. **Human in control.** Assisted mode is the default. Autopilot is opt-in with hard budgets and
   escalation.
8. **Provider-independent.** Any capable model can fill any role via the gateway; different roles use
   different models.
9. **Rights-respecting.** No scraping or imitation of commercial works or living authors; exemplars are
   project-generated, user-owned or licensed; provenance recorded.

## 5. What the studio produces (artifact chain)

```
Requirements ─► Story Spec (hard / soft / assumptions) ─► Concept candidates ─► Story Bible
   (characters + speech profiles, world, power system, factions, glossary, style profile)
   ─► Series Blueprint (promise, ending, endgame requirements, seasons)
   ─► Season plan ─► Arc plans ─► Chapter Contracts ─► Scene Plans
   ─► Korean draft ─► evaluations ─► targeted revisions ─► approved chapter
   ─► canon extraction + verification ─► atomic canon commit
   ─► summaries / embeddings / promise updates / horizon re-planning
   ─► Export (per volume / whole series; TXT, DOCX, EPUB, platform-formatted)
```

## 6. Operating modes

| Mode | Who approves what | When to use |
| --- | --- | --- |
| **Assisted (default, MVP)** | Human approves assumptions, bible, series blueprint, each arc plan, and each chapter | First arc of any series; high-stakes chapters |
| **Semi-automatic (MVP)** | Human approves bible/blueprint/arc plans; chapters auto-accepted when scorecard ≥ tier threshold and no blocking issues; otherwise queued for review | Steady-state production |
| **Autopilot (Beta)** | Human approves bible/blueprint; arcs and chapters auto-accepted within budget; hard escalation on blocking issues, budget exhaustion, or repeated low quality | Long backlists, trusted configurations |

Recommended initial mode: **Assisted for the story bible and the first arc, then Semi-automatic.**

## 7. Success criteria (product level)

- A 200-chapter series produced in Semi-automatic mode has **zero unresolved blocking continuity issues**
  at export and every critical fact traces to accepted manuscript text.
- Korean human editors rate ≥ 80% of sampled chapters as "reads as native Korean webnovel of this genre"
  (style score rubric in `docs/02-korean-style/05-style-drift-detection-and-repair.md`).
- Chapter regeneration or a retcon in chapter *k* lists every dependent later chapter and plan within
  seconds; nothing silently stays inconsistent.
- Any workflow interrupted at any step resumes without duplicate spend beyond one in-flight call.
- Cost per accepted chapter stays within the project's configured tier; hard limits are never exceeded.

## 8. Explicit non-goals

- Reader-facing distribution, comments hosting, monetization.
- Imitating a named author, series, or platform hit; training on scraped commercial novels.
- Real-time collaborative editing (Google-Docs style) in MVP.
- Translation into other languages (may be a future export add-on; never the generation path).
- General-purpose chat with the model about the novel (a constrained "ask the canon" inspector exists instead).

## 9. Key decisions at a glance (see `docs/adr/`)

TypeScript monorepo (ADR-0001) · Postgres 16 + pgvector as single system of record (ADR-0002) · Temporal
for durable workflows (ADR-0003) · provider-independent model gateway (ADR-0004) · fail-closed Style Guard
(ADR-0005) · bitemporal facts with evidence (ADR-0006) · reality frames (ADR-0007) · proposition-centric
knowledge ledger (ADR-0008) · accepted-chapter-only canon with two-extractor reconciliation and atomic
commit (ADR-0009) · tiered context packs (ADR-0010) · hybrid retrieval (ADR-0011) · rolling-horizon
hierarchical planning (ADR-0012) · chapter contract as unit of acceptance (ADR-0013) · patch-first revision
(ADR-0014) · position-swapped pairwise candidate judging (ADR-0015) · prompt registry with versioning
(ADR-0016) · Korean NLP sidecar (ADR-0017) · hard budgets (ADR-0018) · Assisted as default mode (ADR-0019)
· workspace isolation with RLS (ADR-0020) · repository structure (ADR-0021) · immutable manuscript versions
(ADR-0022) · timelines for regression loops (ADR-0023) · NFC normalization and character counting
(ADR-0024) · exemplar and imitation policy (ADR-0025).
