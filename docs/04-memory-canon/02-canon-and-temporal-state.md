# Canon and Temporal-State Architecture

## 1. Core objects

### 1.1 Manuscript versions (immutable)
`manuscript_versions { id, project_id, chapter_id, version_no, kind: draft|revision|candidate|approved|
accepted|retconned, text (NFC), char_count, content_hash, parent_version_id, created_by_job_id, status }`.
Text is never edited in place; a patch creates a new version. **Exactly one** version per chapter may be
`accepted` at a time (partial unique index). Evidence spans reference `(manuscript_version_id, start, end,
quote, quote_hash)`; on write the DB trigger verifies `substr(text, start, end-start) = quote`.

### 1.2 Entities
`entities { id, project_id, type: character|location|organization|item|ability|term|event_anchor|
timeline, canonical_name_ko, aliases[], status: active|retired|merged_into, created_from (bible|extraction|
user) }`. Entity **versions** carry editable descriptive fields; identity is the ID. Merging entities
(duplicate detection) rewrites references in a canon commit.

### 1.3 Facts (bitemporal)
```
facts {
  id, project_id, timeline_id, entity_id, attribute, value_json, value_text_ko,
  valid_from  StoryClock, valid_to  StoryClock | null,      -- story time
  asserted_at_version int, retracted_at_version int | null, -- canon version (system time)
  source: bible|extraction|user_correction|retcon, confidence, locked bool,
  frame: canonical|flashback|prior_loop|alternate_timeline,  -- facts exist only in reality-bearing frames
  evidence_span_ids[] (≥1 unless source=bible), commit_id, superseded_by_fact_id
}
```
Attribute families (extensible enum): `identity.*` (name, age, gender, appearance), `status.location`,
`status.injury`, `status.condition`, `status.alive`, `power.rank`, `power.level`, `power.stat.*`,
`power.ability.*`, `inventory.item` (value = item entity + qty), `resource.*` (money, mana), `affiliation.*`,
`role.*`, `world.rule.*`, `relation.*` (mirrored in relationship_states), `speech.*` (speech profile facts).

**Validity semantics**: `valid_to = null` = still true; a new fact for the same `(entity, attribute[, key])`
closes the prior one at `valid_from` of the new (story time) **and** records `superseded_by`. Facts are
never deleted; retractions set `retracted_at_version` (system time) so "as of canon version v" queries work.

### 1.4 Story clock
`StoryClock { chapter_no: int, ordinal: int, world_date?: iso-like string or era-relative, precision:
exact|approx|unknown }`. Ordering: `(timeline_id, world_date if comparable, chapter_no, ordinal)`.
Elapsed-time facts (`world.time.elapsed_since_prev`) are extracted where prose states them; unknown
precision is allowed and reported as a continuity risk.

### 1.5 Events
`events { id, project_id, timeline_id, story_clock_start, story_clock_end, frame, summary_ko, type,
location_id, participants[] (entity, role), asserted_at_version, retracted_at_version, evidence_span_ids[],
source_chapter_id, narrated_in_chapter_ids[] }`.

### 1.6 Reality frames (ADR-0007)
| Frame | Mutates objective state? | Who may know it | Typical extraction cue |
| --- | --- | --- | --- |
| `canonical` | yes | anyone present / informed | ordinary narration |
| `flashback` | yes (at its own past story time) | as canonical at that time | 회상, 과거 시점 |
| `dream` | no | dreamer (as dream) | 꿈, 깨어났다 |
| `hallucination` | no | experiencer | 환각/환청 |
| `lie` | no; creates knowledge stance `believes_false` for deceived hearers if they believe it | speaker knows truth; hearers per outcome | dialogue asserting a non-fact |
| `hypothetical` | no | thinker | 만약 …라면 |
| `prediction` | no | thinker | 예측/예감 |
| `plan` | no | planner | (from plan tables, not extraction) |
| `prior_loop` | yes on the prior timeline; no on main | regressor only (plus anyone told) | 회귀 전/전생 |
| `alternate_timeline` | yes on that timeline | per timeline | branch scenes |
| `source_story` | as prior_loop for possession/villainess "원작" | possessor | 원작에서는 |
| `non_canonical_draft` | never stored in canon | — | quarantine only |

Rule enforced by verifier: **only `canonical`, `flashback`, `prior_loop` (on its timeline), and
`alternate_timeline` (on its timeline) may produce facts or state changes.** `lie` produces knowledge
stances, never facts. `dream/hallucination/hypothetical/prediction` produce knowledge items for the
experiencer only and may open promises (e.g., prophetic dream → promise type `mystery`).

### 1.7 Timelines (ADR-0023)
`timelines { id, project_id, name, parent_timeline_id, divergence_clock, kind: main|prior_loop|alternate }`.
Facts/events carry `timeline_id`. Regression: the story starts with `prior_loop` timeline populated by
extraction from the regressor's recollections (frame `prior_loop`), and `main` from chapter 1. Queries for
"what is true now" use `main`; "what does the protagonist expect" joins `prior_loop` facts as knowledge with
stance `knows` (source: memory of prior loop) and adds `diverged=true` when a `main` event contradicts.

## 2. Canon version and commits

`canon_commits { id, project_id, version (monotonic per project), parent_version, source: bible|
chapter_acceptance|user_correction|retcon|rollback|merge_entities, chapter_id?, manuscript_version_id?,
delta_json (forward), inverse_json, actor (job/user), created_at, item_counts }`. `projects.canon_version`
is updated in the same transaction with an optimistic check (`WHERE canon_version = parent_version`).

## 3. Planned ≠ happened

- Plans live in `plan_*` tables; the assembler renders them under an explicit heading `[예정 — 아직 일어나지
  않음]` and never in the "현재 상태/지금까지 일어난 일" sections.
- Extraction is forbidden from reading plans (its context has none) — it only sees the accepted text,
  glossary, and entity registry. So it cannot "confirm" a planned event that the text did not realize.
- After commit, `PlanningHorizonWorkflow` compares the delta against the contract's planned deltas and
  marks each planned item `realized|partially_realized|unrealized` — explicit, never inferred.
- Facts have no `future` validity: `valid_from` must be ≤ the chapter's `story_time.end`. Predictions are
  frame `prediction` knowledge items.

## 4. Chapter lifecycle (state machine)

```
planned ─► drafting ─► drafted ─► evaluating ─► revising ─► review_pending ─► approved ─► extracting
   ─► reconciling ─► verifying ─► committing ─► accepted ─► (stale | retconned | superseded)
                      │ (blocking issues after max rounds) └► needs_attention
rejected (any pre-accepted state via user) → versions quarantined
```
Only `accepted` versions feed canon. `approved` is the human/policy gate; `accepted` is set inside the
atomic commit transaction. If extraction/verification fails, the chapter stays `approved` with the failure
recorded and a retry available; canon is untouched.

## 5. Extraction, reconciliation, verification

### 5.1 Extraction (two independent passes)
Inputs: accepted text (with paragraph IDs), glossary + entity registry (IDs, canonical names, aliases),
chapter contract **planned deltas as hypotheses labelled 계획 — 검증 필요** (allowed here because the extractor
must return `realized/unrealized` per hypothesis with evidence — but the extractor's own output is the
source of truth, not the plan), knowledge guards, story clock of the chapter, deterministic pre-pass output
(NER mentions with offsets, 상태창 numbers, utterance speaker/level annotations).

Output (`canon-delta.schema.json`): candidate items each with `type`, payload, `frame`, `story_clock`,
`evidence[] {paragraph_id, quote}`, `confidence`. Extractor A and B use different prompts (A: entity-first
sweep; B: event-timeline-first sweep) and, when routing allows, different model families.

### 5.2 Reconciliation (deterministic first)
Items are canonicalized (entity IDs resolved via aliases, values normalized, story clocks compared) and
matched by `(type, entity/proposition/pair, attribute/kind, story_clock window)`:
- **Agreed** (same value, compatible evidence) → accepted with `confidence = max`.
- **Only-in-one** with confidence ≥ 0.8 and verifiable evidence → accepted as `single_source` (flagged in
  UI); < 0.8 → adjudicate.
- **Conflict** (same key, different value) → adjudicator call with the exact spans of both claims and the
  surrounding paragraphs; adjudicator must pick or reject with evidence; still unresolved → **human queue**
  (commit blocked for that item only if it is `major`; `minor` items dropped with record).
- Importance: items touching locked facts, knowledge of secrets, injuries/death, rank, inventory, and
  relationship level changes are `major`.

### 5.3 Verification (deterministic)
- Every evidence quote must be found at the given paragraph (exact after NFC; fallback fuzzy ≥ 0.98 with
  re-anchoring, else reject item).
- Entity IDs must exist or be in `introduces[]`; unknown names → proposed new entity requiring approval in
  Assisted mode (auto in Autopilot with `provisional=true`).
- Frame rules (§1.6) enforced; `plan`-frame items forbidden; validity must not start in the future.
- Consistency pre-check against current canon: contradictions with **locked** facts → blocking (the chapter
  should not have been approved; this is the last line of defense and returns the chapter to
  `needs_attention`); contradictions with unlocked facts → recorded as `supersedes` (state change) if the
  chapter narrates a change, else flagged as `unexplained_contradiction` (major → human queue).
- Knowledge leak check: any `knows` stance created for a character w.r.t. a secret they are guarded from,
  without a channel event in this chapter → blocking.

### 5.4 Commit
Single transaction: insert facts (closing superseded), events, knowledge states (closing superseded),
relationship states, promise updates, propositions, new entities, L1 summary, evidence spans; write
`canon_commits` with delta + inverse; bump version with optimistic check; write dependency edges (chapter →
every canon item read by its pack at the recorded version); set manuscript version `accepted`; set chapter
status `accepted`. Any failure → rollback → chapter remains `approved`, job `needs_attention`.

## 6. Queries the system must answer (and how)

| Query | SQL sketch |
| --- | --- |
| Current state of entity E at story clock C on timeline T (as of latest canon) | `facts WHERE entity=E AND timeline=T AND valid_from<=C AND (valid_to IS NULL OR valid_to>C) AND retracted_at_version IS NULL` |
| Same, as canon stood at version V | add `asserted_at_version<=V AND (retracted_at_version IS NULL OR retracted_at_version>V)` |
| Injury history | facts with `attribute LIKE 'status.injury%'` ordered by valid_from |
| Who was where at C | facts `status.location` valid at C |
| Events involving E in arc range | events join participants, `story_clock BETWEEN` |
| Contradiction check for new fact F | overlapping-validity facts with same key and different value not marked superseded |

## 7. Isolation of rejected drafts (hard guarantees)

1. Extraction activities accept only `manuscript_version_id` whose `kind='approved'` and whose chapter is
   in state `approved`; the DB function `assert_extractable(version_id)` raises otherwise.
2. Candidate and rejected versions are stored with `kind in (candidate, draft, revision)` and, upon
   rejection, moved to `quarantine_versions` (same shape, different table) by the workflow; the context
   assembler's source allowlist contains no quarantine tables and no non-accepted versions except the
   **current chapter's own prior scenes** during drafting (explicitly scoped by job).
3. Search documents/embeddings are only built from accepted versions and canon items; a nightly job
   asserts no `search_documents` row references a non-accepted version.
4. Exemplar bank rows require `manuscript_version.kind='accepted'` (FK + check).
5. Tests: fixture includes a rejected draft containing a distinctive false fact ("주인공의 왼팔이 절단됐다");
   the suite asserts that fact never appears in facts, summaries, packs, or exemplars.

## 8. Dependencies, staleness, propagation

- `dependency_edges { dependent_kind: chapter|plan|summary|pack, dependent_id, canon_item_kind, canon_item_id,
  canon_version_read }` written at commit (for chapters) and at plan/pack creation (for plans/packs).
- On any canon commit, the commit's touched item IDs are joined to `dependency_edges`; dependents with
  `canon_version_read < new_version` get `stale=true` with `stale_reasons` (item + change kind).
- **Stale job detection**: a running job re-checks before commit that no intervening commit touched its
  dependency set (`SELECT ... FROM canon_commits WHERE version > read_version AND items && deps`); if so,
  it re-validates the contract (cheap) and either continues (no conflict) or restarts from planning.
- **Conflicting parallel jobs**: `target_leases (project_id, target_kind, target_id, job_id, expires_at)`
  taken before drafting; batch runs are sequential by design.
- **Propagation modes**: mark-only (MVP default) → user reviews stale list; auto-revalidate (Beta) runs
  `plan_continuity_checker` on stale contracts and `continuity_checker` on stale accepted chapters, producing
  patch proposals.

## 9. Retcons, corrections, rollback

- **User correction**: edit canon item → commit `source=user_correction` (closing/replacing the item;
  evidence optional but a `justification_ko` required) → dependency propagation → optional manuscript patch
  task if the text now contradicts canon (detected by running the continuity checker on the source chapter
  span).
- **Retcon**: new manuscript version of an accepted chapter (patched or rewritten) → `approved` → extraction
  diff against items sourced from the old version → commit that retracts old items and inserts new ones →
  old version `retconned` → propagation.
- **Rollback (MVP)**: apply `inverse_json` of the latest commit in one transaction (new commit
  `source=rollback`); chapter returns to `approved` with its version `approved` (not accepted). Beta:
  arbitrary version = sequential inverse application with conflict detection.
- **Regeneration**: `ChapterProductionWorkflow(supersedes=version)`; on acceptance, the commit retracts all
  canon items sourced from the superseded version in the same transaction.

## 10. Special narrative structures

| Structure | Handling |
| --- | --- |
| Flashback chapter | Events frame `flashback` with story clock in the past; facts valid from that past time; contract marks `story_time` accordingly; knowledge items for the narrating character unaffected |
| Dream sequence | frame `dream`; knowledge for dreamer only; may open promises |
| Hypothetical/imagination | frame `hypothetical`; no facts |
| Lies | `lie` event + knowledge stances (`believes_false` for deceived hearers) + speaker `knows` truth |
| Predictions/prophecy | frame `prediction` knowledge; promise opened |
| Regression loop restart | new timeline `prior_loop_n` created from `main` at divergence; `main` reset semantics documented in ADR-0023 (rare; default: one prior loop) |
| Alternate POV retelling of a known event | event `narrated_in_chapter_ids` appended; new knowledge for the new POV character extracted |
| Hidden identity | proposition "X는 Y다" with secret knower set; extraction of any `knows` for others requires a channel event |
