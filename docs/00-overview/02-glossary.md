# Glossary

Terms are used with exactly these meanings across all documents and schemas. Korean equivalents are given
where the Korean term is the natural one in the domain.

## Product & workflow

| Term | Definition |
| --- | --- |
| **Workspace** | Tenant boundary. Owns projects, members, budgets, secrets configuration, audit log. All data is isolated per workspace (RLS). |
| **Project (작품)** | One novel/series. Owns requirements, story bible, plans, chapters, canon, budgets. |
| **Requirement** | A user-provided constraint or wish. Classified as **hard** (must hold; violations block acceptance) or **soft** (preference; weighted in evaluation). |
| **Assumption** | A model- or system-generated decision made to fill a gap in requirements. Stored separately; becomes a requirement only when the user explicitly confirms it. |
| **Story Spec** | The normalized, versioned set of requirements + confirmed assumptions for a project. |
| **Story Bible (설정집)** | Approved reference for the series: characters, speech profiles, world rules, power system, factions, locations, glossary, style profile binding. Versioned. |
| **Series Blueprint** | Top-level plan: story promise, reader fantasy, main conflict, protagonist arc, ending, endgame requirements, season list. |
| **Season / Volume / Arc / Chapter / Scene** | Planning hierarchy. Season (시즌) = major narrative movement; Volume (권) = export unit (~25–50 chapters); Arc (에피소드/장) = conflict unit spanning chapters; Chapter (화/회차) = published unit; Scene = draft unit. See `docs/03-story-planning/`. |
| **Chapter Contract** | Structured specification a chapter must satisfy to be accepted (why it exists, must/must-not, participants, knowledge & state deltas, hook, style profile, length, acceptance criteria). |
| **Planning Horizon** | Number of chapters ahead planned in detail (default 6); arcs ahead planned at outline level (default 2); seasons planned at summary level (all). |
| **Job / Workflow / Activity** | Temporal terms. A *Workflow* is a durable orchestration (e.g., `ChapterProductionWorkflow`); an *Activity* is a retriable unit of work (e.g., one LLM call, one DB commit). A *Job* is the user-visible record of a workflow run. |
| **Operating mode** | Assisted / Semi-automatic / Autopilot — governs which gates require a human. |
| **Gate** | A point where a workflow waits for human approval (or auto-approves per mode + thresholds). |

## Korean style

| Term | Definition |
| --- | --- |
| **Style Profile** | Versioned, structured description of how prose should read for a genre + project (rules, constraints, targets, exemplars, forbidden patterns). Composed from a base profile, genre overlay(s), and project overrides. |
| **Style Block** | The compiled, token-budgeted textual rendering of a Style Profile that is injected into an LLM call. Deterministic function of (profile version, role, budget). |
| **Style Guard** | Gateway middleware that rejects any style-sensitive call lacking a valid Style Block reference and records the style version used. |
| **Korean Lint** | Deterministic checks on Korean text (sentence-ending repetition, pronoun density, translation-ese markers, paragraph length, dialogue ratio, speech-level markers, punctuation). |
| **Style Judge** | Model-based evaluator that scores Korean webnovel-ness and drift, returns evidence spans and repair suggestions. |
| **Drift** | Measurable deviation from the Style Profile: *translation drift* (번역투), *Western exposition drift*, *voice drift* (character speech habits), *format drift* (screenplay/webtoon script), *register drift* (speech level/honorific errors). |
| **Speech level (상대 높임법)** | Korean sentence-final politeness system: 하십시오체, 해요체, 해체(반말), 하게체, 하오체, 해라체. Tracked per character-pair and context. |
| **Speech Profile** | Per-character description of speech: default speech level by addressee, honorific habits, address terms, verbal tics, sentence-length tendencies, forbidden expressions. |
| **Address term (호칭)** | How A refers to / calls B (e.g., 형, 선배, 대리님, 각하, 이름+야). Tracked per directed pair with validity periods. |
| **Exemplar** | A short approved passage used to anchor style. Sources allowed: project's own accepted chapters, user-owned writing, licensed text, studio-authored synthetic exemplars. Never commercial works. |

## Memory & canon

| Term | Definition |
| --- | --- |
| **Canon** | The set of facts, events, states and knowledge established by **accepted** chapters (plus user-locked bible facts). Versioned. |
| **Canon Version** | Monotonic integer per project, incremented by exactly one atomic canon commit. Every job records the canon version it read. |
| **Canon Commit** | Single atomic transaction that applies an approved **Canon Delta** and bumps the canon version. |
| **Canon Delta** | Proposed set of changes (facts, events, state changes, knowledge changes, relationship changes, promises, payoffs) extracted from an accepted chapter, each with evidence. |
| **Fact** | A typed assertion about an entity (attribute or relation) with **validity period** (story time) and **assertion period** (system time), evidence, confidence, and source chapter. Bitemporal. |
| **Evidence Span** | Exact character offsets into an immutable manuscript version, plus the quoted text and a content hash. Every important fact/event/knowledge change links to ≥1. |
| **Canonical Event** | Something that happened in the story, with story-time position, participants, location, and reality frame. |
| **Reality Frame** | Classifier of narrative reality: `canonical`, `flashback` (canonical but past), `dream`, `hallucination`, `lie` (asserted by a character, not true), `hypothetical`, `prediction`, `plan`, `prior_loop` (regression prior timeline), `alternate_timeline`, `non_canonical_draft`. Only `canonical` and `flashback` update objective world state. |
| **Timeline** | A branch of story time. Default `main`; regression/alternate stories add timelines with a divergence point. |
| **Story Time** | In-world time, represented as an ordered **story clock** (chapter-relative ordinal + optional in-world date). |
| **Knowledge Ledger** | Records, per **proposition** and per **knower** (character, narrator, reader), an epistemic stance: `knows`, `suspects`, `believes_false`, `pretends`, `unaware`, `forgot`, with source (how/when learned) and validity. |
| **Proposition** | A canonical statement that can be known/believed (e.g., "주인공은 회귀자다"). Linked to facts/events. |
| **Secret** | A proposition with restricted knowers and an owner; violations (a non-knower acting on it) are *knowledge leaks*. |
| **Promise** | A setup the story owes a payoff for (foreshadowing, mystery, Chekhov's gun, relationship beat). Tracked in the **Promise Ledger** with due window and status. |
| **Payoff** | Resolution of a promise, with evidence. |
| **Summary Tier** | Hierarchical summaries: chapter (L1), arc (L2), season (L3), series (L4). Regenerated from accepted text only. |
| **Context Pack** | The versioned, deterministic bundle of context for one LLM call: tiered, budgeted, with a manifest listing every included item and its canon version. |
| **Tier** | Protection level within a context pack: T0 mandatory (never trimmed), T1 critical (trim only by compression), T2 relevant (rankable/trimmable), T3 optional. |
| **Retcon** | A user-authorized change to accepted canon. Produces a new canon version, marks dependent artifacts stale, may trigger manuscript patches. |
| **Stale** | A job/plan/chapter whose recorded canon version is superseded by a commit that touches something it depends on. |
| **Dependency Edge** | Recorded link "artifact X used canon item Y at canon version V" enabling impact analysis. |

## Generation & quality

| Term | Definition |
| --- | --- |
| **Role** | A named LLM function (e.g., `scene_writer`, `continuity_checker`) with its own prompt family, model routing, schema, budget, style sensitivity. |
| **Prompt Version** | Immutable, content-hashed prompt template + schema + config, registered in the Prompt Registry. Every call records one. |
| **Candidate** | One of N alternative outputs for the same task (concept, plan, scene, chapter). Lives outside canon; at most one becomes the accepted artifact. |
| **Scorecard** | Structured evaluation result: rubric scores, issue list (with evidence, severity, confidence, repair suggestion), pass/fail per acceptance criterion. |
| **Issue** | A single finding: `{kind, severity: blocking|major|minor|note, confidence, claim, chapter_span, conflicting_canon, canon_evidence, repair}`. |
| **Patch** | A targeted edit (sentence / paragraph / dialogue line / scene) applied to a manuscript version, producing a new version; regression-tested. |
| **Manuscript Version** | Immutable text snapshot of a chapter (draft, revision, approved). Evidence spans refer to a specific version. |
| **Acceptance** | The transition of a chapter to `accepted` after gates pass; the only trigger for canon extraction. |
| **Quality Tier** | Budget/quality preset (Economy / Standard / Premium) controlling candidate counts, judge depth, model routing. |
| **Hard Limit** | Spend ceiling that halts workflows when reached; cannot be exceeded by any automatic behavior. |

## Korean webnovel domain (used in style docs)

| Term | Meaning |
| --- | --- |
| 회차 / 화 | Chapter/episode of a serialized webnovel, typically 5,000–6,000 Korean characters including spaces on major platforms. |
| 연재 | Serialization. |
| 사이다 / 고구마 | Reader-slang for cathartic payoff ("cider") vs frustrating suppression ("sweet potato"). Pacing levers. |
| 먼치킨 | Overpowered protagonist. |
| 회귀 / 빙의 / 환생 | Regression / possession / reincarnation — the three core "second chance" premises. |
| 헌터 / 게이트 / 각성자 | Hunter / gate / awakened person — modern-fantasy dungeon-hunter setting vocabulary. |
| 상태창 | Status window — system-fiction UI text embedded in prose. |
| 무협 / 무림 | Martial-arts fiction / the martial world. |
| 로판 | Romance fantasy (로맨스 판타지). |
| 악녀 | Villainess. |
| 현판 | Modern fantasy (현대 판타지). |
| 아카데미 | Academy setting. |
| 번역투 | Translation-ese: Korean that reads like translated text (pronoun overuse, passive constructions, unnatural word order, calque idioms). |
| 종결어미 | Sentence-final ending; repetition of the same ending (e.g., ~했다 ×5) is a common quality defect. |
| 호칭 / 존칭 / 반말 / 존댓말 | Address terms / honorific titles / informal speech / polite speech. |
