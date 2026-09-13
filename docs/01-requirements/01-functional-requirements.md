# Functional Requirements

IDs are stable and referenced by the traceability matrix, backlog and tests. Tier column: M = MVP, B =
Beta, P = Production, F = Future. Priority within tier: P0 (must), P1 (should), P2 (could).

## FR-1 Requirement intake & story specification

| ID | Requirement | Tier/Prio |
| --- | --- | --- |
| FR-1.1 | User can create a project with a free-text premise (Korean or English input; output always Korean) and optional structured fields: genre, subgenres, main character, supporting characters, world concept, desired tropes, forbidden developments, target audience, tone, romance preference, power/progression system, ending preference, chapter count, target Korean characters per chapter (공백 포함), mandatory scenes/developments, content restrictions. | M/P0 |
| FR-1.2 | System normalizes intake into a **Story Spec** where every item is classified **hard requirement**, **soft preference**, or **assumption**, with provenance (`user`, `system_default`, `model_inferred`). | M/P0 |
| FR-1.3 | Assumptions are surfaced for review; user can confirm (→ requirement), edit, or reject each. Unconfirmed assumptions remain `assumption` and are labeled as such in all downstream context. | M/P0 |
| FR-1.4 | Story Spec is versioned; each version records who changed what. Downstream plans reference the spec version used. | M/P0 |
| FR-1.5 | User can add **running directions** at any time (e.g., "다음 아크부터 서브 남주 비중 늘려", "이 캐릭터 죽이지 마"). Directions are classified hard/soft, scoped (series/season/arc/chapter-range/character), and take effect from the next unplanned or regenerated unit. | M/P0 |
| FR-1.6 | Content restrictions (age rating, forbidden themes) are hard requirements enforced in evaluation and in export metadata. | M/P0 |
| FR-1.7 | The system detects requirement conflicts (e.g., "no romance" + "romance-fantasy genre") and asks the user to resolve before planning. | M/P1 |

## FR-2 Concept & story bible

| ID | Requirement | Tier/Prio |
| --- | --- | --- |
| FR-2.1 | Generate 2–3 **concept candidates** (logline, story promise, reader fantasy, main conflict, hook of ch.1, ending direction, differentiators), compared with a structured comparison and a recommendation; user selects or merges. | M/P0 |
| FR-2.2 | Generate a **Story Bible**: characters (identity, background, goals, flaws, arc, secrets, **speech profile**), world (rules, geography, institutions, economy where relevant), power/progression system (rules, ranks, costs, limits, progression cadence), factions, locations, glossary of coined terms (with fixed Korean spelling), naming registry. | M/P0 |
| FR-2.3 | User can edit any bible entry; edits are versioned. | M/P0 |
| FR-2.4 | User can **lock** facts (immutable canon); locked facts cannot be changed by generation and any contradiction is a blocking issue. | M/P0 |
| FR-2.5 | Every bible entity has a stable ID and Korean canonical name plus aliases; aliases are used for entity linking in extraction. | M/P0 |
| FR-2.6 | Speech profiles define, per character: default speech level toward each key counterpart, address terms used and received, verbal tics, taboo expressions, register shifts under emotion. Modeled as facts with validity so they can change (e.g., after becoming lovers). | M/P0 |
| FR-2.7 | Bible approval is a gate; generation of plans cannot start before bible v1 is approved (Assisted) or auto-approved (Autopilot). | M/P0 |

## FR-3 Hierarchical story planning

| ID | Requirement | Tier/Prio |
| --- | --- | --- |
| FR-3.1 | Planning hierarchy: Series Blueprint → Seasons → Arcs (major/minor) → Chapters (contracts) → Scenes. Volumes are export groupings mapped onto chapters, not a planning level. | M/P0 |
| FR-3.2 | Series Blueprint holds: story promise, reader fantasy, main conflict, protagonist development arc, key character arcs, key relationship arcs, progression arc (power curve with milestones), mystery/foreshadowing register, ending, **endgame requirements** (what must be true for the ending). | M/P0 |
| FR-3.3 | **Rolling horizon**: chapter contracts exist in detail for the next H chapters (default 6); arcs outlined for the next 2; seasons outlined for the full series. Re-planning is triggered by acceptance of chapters, new directions, retcons, or reader feedback. | M/P0 |
| FR-3.4 | **Promise Ledger**: every setup/foreshadowing/mystery/relationship beat/Chekhov item is recorded with a due window; the planner must schedule payoffs; overdue promises are flagged. | M/P0 |
| FR-3.5 | Each chapter has a **Chapter Contract** (schema `chapter-contract.schema.json`) including: purpose, must-happen, must-not-happen, participants, POV, location(s), story-time window, knowledge deltas, state deltas, relationship deltas, setups, payoffs, emotional movement, conflict/reversal, local satisfaction (사이다/감정/정보), ending state, hook type, style profile ref, length target, continuity risks, acceptance criteria. | M/P0 |
| FR-3.6 | Plans are re-validated against canon after every canon commit; plans that reference changed facts are marked stale with a diff. | M/P0 |
| FR-3.7 | The user can review, edit, approve, or regenerate plans at any level; edits at a higher level mark lower levels stale. | M/P0 |
| FR-3.8 | The planner respects Korean webnovel serial structure: episode-level hook, arc-level 사이다 cadence, progression cadence per genre overlay, cliffhanger frequency targets. | M/P0 |
| FR-3.9 | Reader feedback (Beta) can be imported and attached as *soft* signals to re-planning; never as hard requirements unless promoted by the user. | B/P1 |

## FR-4 Chapter production pipeline

| ID | Requirement | Tier/Prio |
| --- | --- | --- |
| FR-4.1 | Chapter production runs as a durable workflow: contract validation → context pack → scene plan → scene drafting → assembly → deterministic checks → model evaluations → targeted revision loop → gate → acceptance → canon extraction → reconciliation → verification → atomic canon commit → post-commit (summaries, embeddings, promise updates, horizon re-plan). | M/P0 |
| FR-4.2 | Every LLM call receives an explicit **Context Pack** (versioned, manifested) and a versioned prompt; no call relies on prior conversation. | M/P0 |
| FR-4.3 | Scene drafting is per scene with the immediately preceding accepted text (last ≈1,500–2,500 chars) and the preceding drafted scene as continuity anchors. | M/P0 |
| FR-4.4 | Output length is controlled to the target Korean character count ± tolerance (default ±12%); overruns/underruns trigger scene-level adjustments, not full rewrites. | M/P0 |
| FR-4.5 | Candidate generation (N≥2) is available for concepts (always), arc plans (Standard+), scenes/chapters (Premium tier or on user request); candidates are judged pairwise with position swapping; generation stops early when a candidate exceeds the acceptance threshold or budget is reached. | M/P0 (config), B/P1 (chapter-level default) |
| FR-4.6 | Rejected candidates and drafts are stored (for audit and learning) in a quarantined table space that is never read by the context assembler or canon extractor. | M/P0 |
| FR-4.7 | Batch generation: user requests chapters k..k+n; workflow runs sequentially (each chapter depends on the previous commit), pausing at gates per mode; batch can be paused/cancelled with partial completion preserved. | M/P0 |
| FR-4.8 | Chapter regeneration: user regenerates chapter k with optional new directions; system produces a **dependency report** (later chapters/plans whose canon inputs derive from k) before proceeding; later chapters become `stale` pending review. | M/P0 |
| FR-4.9 | User can request changes on a chapter in natural language; the system converts them into patch tasks (scene/paragraph-scoped) rather than regenerating the chapter, unless the change invalidates the contract. | M/P0 |

## FR-5 Evaluation & revision

| ID | Requirement | Tier/Prio |
| --- | --- | --- |
| FR-5.1 | Deterministic checks: schema validity, truncation, length, Korean lint (see FR-6), forbidden content lexicon, named-entity spelling against glossary, required-scene presence markers, repeated paragraph detection (n-gram/simhash against all accepted chapters), status-window format validity (system genres). | M/P0 |
| FR-5.2 | Model-based evaluators: contract compliance, continuity (facts/timeline/location/inventory/injury/rank), knowledge leakage, relationship consistency, world/power-rule compliance, promise tracking, repetition (scene/arc level), pacing & hook quality, Korean style judge, character-voice judge. | M/P0 |
| FR-5.3 | Every issue includes: kind, severity (blocking/major/minor/note), confidence, the claim, the chapter span (exact offsets), conflicting canon fact/event IDs, canon evidence spans, and a recommended repair scope (sentence/paragraph/dialogue/scene/chapter/plan). | M/P0 |
| FR-5.4 | Blocking issues prevent acceptance; majors require repair or explicit user override (recorded); minors/notes are advisory. | M/P0 |
| FR-5.5 | **Patch-first revision**: issues are grouped by span; a reviser produces patches for the affected spans with a context pack limited to the surrounding text and the relevant canon; patches are applied to produce a new manuscript version; the affected checks are re-run (regression test) and a whole-chapter smoke check runs after ≥3 patches or any scene-level patch. | M/P0 |
| FR-5.6 | Revision loop bounded: max rounds per chapter (default 3), max spend; on exhaustion the chapter is escalated to human review with the residual issue list. | M/P0 |
| FR-5.7 | Scorecards are stored per manuscript version and visible in the UI with evidence links. | M/P0 |
| FR-5.8 | Judge calibration: evaluators run against golden fixtures on every prompt change (prompt regression suite). | M/P0 |

## FR-6 Korean webnovel style

| ID | Requirement | Tier/Prio |
| --- | --- | --- |
| FR-6.1 | Style Profile per project composed from base Korean webnovel profile + genre overlays + project overrides; versioned; approved as part of the bible. | M/P0 |
| FR-6.2 | A compiled **Style Block** is attached to every style-sensitive call (planning of scenes/hooks, drafting, editing, revision, style/voice evaluation, summary-for-continuation). Gateway **Style Guard** rejects style-sensitive calls without a valid style block reference. | M/P0 |
| FR-6.3 | Style Block variants per role and budget (writer full, editor full, planner compact, judge rubric form). | M/P0 |
| FR-6.4 | Deterministic Korean Lint metrics with genre-specific thresholds: sentence-ending repetition, 3rd-person pronoun density (그/그녀/그들), translation-ese markers (e.g., "~것이다" chains, "~에 의해" passives, "~할 수 있었다" chains, "그것은", "~하는 것을", inverted relative clause piles), average sentence length & variance, paragraph length distribution, dialogue ratio, internal monologue ratio, adverb-tagged dialogue rate, exposition run length, English/Hanja leakage, screenplay/webtoon-script format markers. | M/P0 |
| FR-6.5 | Honorific and speech-level consistency check: per utterance, detect speaker/addressee, classify speech level, compare with speech profile + relationship state at that story time; flag deviations not marked as intentional register shifts. | M/P0 |
| FR-6.6 | Model-based **Style Judge** scores: native-Korean fluency, webnovel form (hook, rhythm, mobile readability), genre convention fit, dialogue naturalness, translation-ese absence, exposition control; each with evidence spans and repair suggestions. | M/P0 |
| FR-6.7 | Character-voice judge compares utterances to speech profiles and prior accepted utterances (voice exemplars). | M/P0 |
| FR-6.8 | Passage-level **style repair**: only flagged spans are rewritten with a repair context (style block + speech profiles + span + neighbors); regression-linted. | M/P0 |
| FR-6.9 | Exemplar bank: project accepted passages tagged by function (hook, action, banter, status window, emotional beat, cliffhanger) are selectable into the style block; user-owned/licensed exemplars can be added with provenance; no commercial-work exemplars. | M/P0 |
| FR-6.10 | Naming consistency: glossary enforces fixed Korean spellings of names/terms; any variant spelling is a deterministic issue. | M/P0 |
| FR-6.11 | User style preferences (e.g., "문장 더 짧게", "내면 독백 줄여") are stored as project overrides with numeric targets where possible. | M/P0 |
| FR-6.12 | Genre-specific structural devices are supported as first-class formatting: 상태창 blocks, system messages, 무협 technique names, 로판 title/address conventions. | M/P0 |

## FR-7 Memory, canon, knowledge

| ID | Requirement | Tier/Prio |
| --- | --- | --- |
| FR-7.1 | Accepted chapter text is stored as an **immutable manuscript version**; canon references its spans by offsets + quote + hash. | M/P0 |
| FR-7.2 | Canon extraction runs only on accepted chapters and produces a **Canon Delta**: facts (with validity), events (with reality frame, story time, participants, location), state changes (location, injury/status, inventory, rank/power, resources), knowledge changes (knower × proposition × stance × how learned), relationship changes (incl. address terms), promises opened/advanced/paid, unresolved questions, summary L1. | M/P0 |
| FR-7.3 | Two independent extractor passes (different prompt/model where budget allows) are reconciled: agreed items pass; disagreements are adjudicated by a third call with the manuscript spans; unresolved → human queue. Items lacking verifiable evidence (quote not found in text) are rejected. | M/P0 |
| FR-7.4 | **Atomic canon commit**: the reconciled delta is applied in one DB transaction that also bumps `canon_version`, writes dependency edges and the delta record (with inverse); failure leaves canon untouched. | M/P0 |
| FR-7.5 | Facts are bitemporal: `valid_from/valid_to` in story time, `asserted_at/retracted_at` in system time; queries "as of chapter k" and "as known at canon version v" are supported. | M/P0 |
| FR-7.6 | Reality frames on events and derived facts; only `canonical`/`flashback` mutate objective state; `plan`, `prediction`, `dream`, `lie`, `hypothetical`, `prior_loop`, `alternate_timeline` are stored but segregated. | M/P0 |
| FR-7.7 | Knowledge ledger distinguishes objective truth, narrator knowledge, reader knowledge, and per-character `knows / suspects / believes_false / pretends / unaware / forgot`, with source event and validity. | M/P0 |
| FR-7.8 | Secrets: propositions with restricted knower sets; extraction and evaluation detect **knowledge leaks** (character acts on information they cannot have). | M/P0 |
| FR-7.9 | Relationship states per directed pair with type, sentiment axes, trust, power dynamic, address terms, speech level, validity. | M/P0 |
| FR-7.10 | Timeline model: story clock per event, multiple timelines (regression loops) with divergence points; "original timeline" knowledge is attributable to the regressor only. | M/P0 |
| FR-7.11 | Hierarchical summaries L1 (chapter) → L2 (arc) → L3 (season) → L4 (series), regenerated on commit from accepted text; each summary stores the chapter range and canon version. | M/P0 |
| FR-7.12 | Every generation job records `canon_version_read`; before commit, the system checks for intervening commits touching dependencies and marks the job stale (re-validate or re-run) instead of committing over them. | M/P0 |
| FR-7.13 | Conflicting parallel jobs on the same chapter/plan are prevented by per-target leases; batch runs are strictly sequential. | M/P0 |
| FR-7.14 | User corrections: edit a fact/event/knowledge item → new canon version with `source=user_correction`, dependency impact report, optional manuscript patch task. | M/P0 |
| FR-7.15 | Retcons: modify accepted chapter text → new manuscript version → re-extraction diff → canon commit → dependents stale → patch proposals for later chapters (Beta automated; MVP manual list). | M/P0 (basic), B/P1 (automated) |
| FR-7.16 | Rollback of the most recent canon commit (inverse delta) in MVP; arbitrary version rollback in Beta. | M/P1, B/P0 |
| FR-7.17 | Rejected drafts, candidate texts, and non-accepted manuscript versions are excluded from canon, summaries, embeddings used for context, and exemplar banks. | M/P0 |

## FR-8 Context construction

| ID | Requirement | Tier/Prio |
| --- | --- | --- |
| FR-8.1 | Context Pack assembler builds a tiered pack per call role: T0 (hard requirements, content restrictions, style block, chapter contract, locked facts touching participants), T1 (previous chapter tail verbatim + L1 summary, participant current states, participant knowledge relevant to contract, relationships among participants, active promises due, arc objective, timeline position), T2 (ranked retrieved canon: older events, facts, evidence spans; L2/L3 summaries), T3 (optional exemplars, minor entities). | M/P0 |
| FR-8.2 | Budgeting: T0 never trimmed (if over budget → hard error), T1 compressed only via approved compressors, T2 ranked and truncated, T3 dropped first. Assembler validates that each T0 item is present byte-for-byte. | M/P0 |
| FR-8.3 | Retrieval is hybrid: structured queries by entity/time, lexical (Korean tokenized) search, vector search over summaries/events/evidence, and graph hops (entity ↔ event ↔ promise). Query plans are derived from the chapter contract. | M/P0 |
| FR-8.4 | Every pack has a manifest (item IDs, versions, canon version, token counts, ranking scores) stored and referenced by the call audit record; packs are content-hashed for provider prompt caching and deduplication. | M/P0 |
| FR-8.5 | Pack templates per role are versioned and tested (retrieval tests assert that fixture facts are recovered into the pack). | M/P0 |

## FR-9 Operations, budgets, reliability

| ID | Requirement | Tier/Prio |
| --- | --- | --- |
| FR-9.1 | Budgets at project, chapter, and workflow level, with **hard limits**; workflows check remaining budget before every call and stop cleanly (checkpointed) when exhausted. | M/P0 |
| FR-9.2 | Quality tiers (Economy/Standard/Premium) set candidate counts, judge depth, model routing; cost prediction per chapter shown before batch runs. | M/P0 |
| FR-9.3 | Usage tracking per call: tokens in/out/cached, cost, model, latency; aggregated per chapter/workflow/project; cost per accepted chapter and per 1,000 accepted Korean characters. | M/P0 |
| FR-9.4 | Jobs list with status, progress, current step, spend, ETA; pause/cancel/resume; failure reason and residual issues on escalation. | M/P0 |
| FR-9.5 | Full audit record per LLM call (see NFR-A). | M/P0 |
| FR-9.6 | Provider fallback and model routing per role; structured output validation with bounded repair attempts; truncation detection with continuation strategy. | M/P0 |

## FR-10 Export & rights

| ID | Requirement | Tier/Prio |
| --- | --- | --- |
| FR-10.1 | Export accepted chapters as TXT (platform-ready plain text with 회차 headers) and DOCX per volume/series; EPUB and platform-specific profiles in Beta. | M/P0 |
| FR-10.2 | Export includes optional metadata: AI-assistance disclosure text, rights confirmation, glossary appendix. | M/P1 |
| FR-10.3 | Users confirm rights for any uploaded exemplar/reference text; provenance is stored. | M/P0 |
| FR-10.4 | Similarity screening of accepted chapters against user-supplied reference corpus; optional external service integration. | B/P1 |

## FR-11 Security & tenancy

| ID | Requirement | Tier/Prio |
| --- | --- | --- |
| FR-11.1 | Authentication (email magic link + OAuth), sessions, 2FA optional (Beta). | M/P0 |
| FR-11.2 | Workspace isolation via Postgres RLS + application-level scoping; roles owner/editor/viewer. | M/P0 |
| FR-11.3 | Audit log of user actions (approvals, corrections, retcons, exports, deletions). | M/P0 |
| FR-11.4 | Imported text (reader comments, documents) is sanitized and marked untrusted; it is never placed in system/instruction positions and is wrapped with injection-resistant delimiters and classifiers. | M/P0 |
| FR-11.5 | Data export and account/project deletion with retention policy. | M/P1 |
