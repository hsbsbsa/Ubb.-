# Story Planning Architecture

## 1. Goals

- Whole-series direction with a **committed ending** and **endgame requirements**, while near-term chapters
  are planned in detail and far chapters remain adjustable (rolling horizon, ADR-0012).
- Plans are **structured objects with validation**, not prose outlines; every chapter has a **Chapter
  Contract** that is the unit of acceptance (ADR-0013).
- Plans are **canon-aware**: they reference facts/events/promises by ID, are validated against canon after
  every commit, and are marked stale when dependencies change.
- Plans are Korean-webnovel-shaped: hook/cadence/payoff structure comes from the Style Profile's structure
  rules (`planner_compact` block) and the genre overlay.
- **Planned ≠ happened**: plan objects live in `plan_*` tables and are stored as `frame=plan` when they
  appear in context; they never appear in canonical event tables until an accepted chapter realizes them.

## 2. Hierarchy

```
Series Blueprint (1)
 └─ Season (2–6 for 200–600 ch; 1 for short works)        "major narrative movement"
     └─ Arc: major (8–30 ch) ─ contains minor arcs (2–6 ch)  "conflict unit"
         └─ Chapter Contract (1 chapter, 4,500–7,000 chars)   "acceptance unit"
             └─ Scene Plan (2–4 per chapter)                    "drafting unit"
Volume = export grouping over chapters (권), not a planning level; default 25 chapters/volume, adjustable.
```

Why not plan volumes: volumes are a publication artifact and their boundaries move with platform needs;
arcs are the narrative unit that carries objectives. Volume boundaries are chosen to land near arc climaxes
by a deterministic rule (prefer boundary within ±2 chapters of a major arc end).

## 3. Series Blueprint (schema: `series-blueprint.schema.json`)

Fields: `story_promise` (what the reader is promised each chapter), `reader_fantasy` (from concept),
`main_conflict`, `protagonist_arc` (start state → end state, 3–5 turning points), `character_arcs[]`
(per key character), `relationship_arcs[]` (pair, start, milestones, end), `progression_arc` (power/rank/
asset curve with milestones bound to chapter ranges; genre cadence), `mysteries[]` (question, answer (secret
proposition ID), reveal window), `foreshadowing_register[]` (planned promises with due windows),
`red_herrings[]` (false trails with resolution), `themes[]`, `ending` (type from user preference; final
state assertions), `endgame_requirements[]` (facts/knowledge states that must hold before the ending can be
written — e.g., "주인공이 흑막의 정체를 알아야 한다", "여주와 남주가 서로의 비밀을 공유한 상태"), `seasons[]`
(summary, objective, entry/exit states, chapter range estimate), `hard_requirement_bindings[]` (which spec
requirements are satisfied where).

Validation: every user mandatory scene is bound to a season/arc; every forbidden development becomes a
`must_not` inherited by all contracts; ending preference realized in `ending`; endgame requirements each
have at least one planned path (arc) that produces them.

## 4. Season & Arc plans (schema: `arc-plan.schema.json`)

Season: objective, thesis, entry state (reference to canon at a chapter), exit state (assertions),
arcs[] outline, promise budget (which blueprint promises open/close here).

Arc (major/minor): `objective`, `conflict`, `antagonistic_force`, `stakes`, `entry_state`, `exit_state`
(assertions to be realized), `participants`, `locations`, `story_time_window`, `beats[]` (ordered; each with
type: setup, escalation, reversal, 사이다, revelation, emotional, progression, climax, aftermath; and target
chapter offset), `promises_opened[]`, `promises_advanced[]`, `promises_paid[]`, `progression_milestones[]`,
`relationship_milestones[]`, `knowledge_changes_planned[]` (who will learn what, when — as `plan` frame),
`cadence_check` (deterministic validation vs overlay: 사이다 interval, progression interval, max 고구마
streak), `risks[]` (continuity risks, e.g., "주인공 왼팔 부상 회복 시점 주의").

Minor arcs nest inside major arcs and map to 2–6 chapters; chapter contracts are generated from minor-arc
beats.

## 5. Rolling horizon

Parameters (project settings): `detail_horizon_chapters` H = 6, `arc_outline_horizon` = 2 arcs, `season
outline` = all.

Triggers for re-planning (`PlanningHorizonWorkflow`):
1. Canon commit of chapter k → ensure contracts exist for k+1..k+H; validate existing contracts against
   the new canon version; adjust or regenerate stale ones; advance arc outlines if the current arc has
   < 2 chapters left.
2. New direction (FR-1.5) → scope-based invalidation (e.g., character-scoped direction invalidates
   contracts where the character participates).
3. User plan edit at level L → children stale.
4. Retcon/correction → dependency edges from canon items to plan items mark stale.
5. Reader feedback (Beta) → soft re-weighting for the next arc outline generation only.

Stale contracts are not silently regenerated in Assisted mode; the UI shows a diff ("이 계약은 canon v128에서
변경된 사실 3개에 의존합니다") and offers regenerate/keep.

## 6. Promise Ledger (schema: `promise.schema.json`)

`Promise { id, type: foreshadowing|mystery|chekhov|relationship_beat|character_goal|world_question|
running_gag|threat|debt, statement_ko, opened_in (chapter/evidence or plan), due_window {min_chapter,
max_chapter or arc ref}, importance: core|major|minor, status: planned|open|advanced|paid|abandoned,
advances[] (chapter refs), payoff (chapter/evidence), related_propositions[], related_entities[] }`

Rules: a `paid` status requires evidence from an accepted chapter (extraction confirms the payoff); a payoff
without any prior `open` promise raises `payoff_without_setup` (major, unless the chapter itself opens and
pays a micro-promise); overdue `core` promises block arc plan approval until scheduled; `abandoned` requires a
user decision and reason (never automatic).

## 7. Chapter Contract (schema: `chapter-contract.schema.json`)

See `02-chapter-contract-specification.md` for every field. Key idea: a contract is validated on three
axes before drafting starts —

1. **Canon validity** (deterministic + retrieval): participants exist and are alive/available at the
   story time; locations reachable from last known locations (travel-time facts if any); states referenced
   (injuries, items, ranks) match canon at `story_time.start`; knowledge deltas are possible (a character
   can only learn something present in canon or introduced in this chapter's `introduces[]`).
2. **Plan validity**: realizes ≥ 1 arc beat; respects arc must/must-not; opens/advances/pays promises as
   scheduled; cadence check passes.
3. **Style validity**: hook type, ending type, local payoff type, dialogue density, scene count within the
   profile's structure rules.

A contract failing validation is fixed by the planner role (one repair call) or escalated.

## 8. Scene Plan (embedded in contract; schema `scene-plan.schema.json`)

Per scene: `objective`, `pov`, `participants`, `location`, `story_time`, `beats[]` (each beat: type,
description_ko, emotional target, information revealed (proposition refs), tags 사이다/감정/정보/유머),
`entry_state`/`exit_state` deltas, `dialogue_density_target`, `length_target_chars`, `opening_beat_type`,
`ending_beat_type`, `continuity_anchors[]` (facts that must appear consistent, with evidence refs),
`must_not[]`, `speaker_pairs[]` (pairs who will talk → speech level/address terms pre-resolved from ledgers
so the writer receives them explicitly).

## 9. Planning roles and calls

| Step | Role | Model class | Candidates |
| --- | --- | --- | --- |
| Blueprint | `series_architect` | reasoning-strong | 2 (Standard), 3 (Premium); pairwise judged |
| Season outline | `season_planner` | reasoning-strong | 1 (+1 on request) |
| Arc plan | `arc_planner` | reasoning-strong | 2 (Standard), judged on objective fit, cadence, promise handling, novelty vs prior arcs (repetition judge) |
| Chapter contract | `chapter_planner` | reasoning-strong or mid | 1 (+repair) |
| Scene plan | `scene_planner` | mid | 1 (+repair) |
| Plan validators | deterministic + `plan_continuity_checker` (mid) | — | — |

Every planner call carries: Story Spec (hard/soft/assumptions labelled), `planner_compact` style block,
relevant blueprint section, parent plan, canon summary at the appropriate tier, promise ledger slice,
protagonist state & progression position, recent arc summaries (L2) for repetition avoidance, and explicit
`must_not[]`.

## 10. Repetition and novelty management

- Arc-level: `repetition_judge` compares the proposed arc to L2 summaries of all prior arcs (structural
  fingerprint: conflict type, antagonist type, setting, resolution type). Score < threshold → planner asked
  for variation with explicit "avoid" list.
- Chapter-level: contract `local_satisfaction` and `ending_type` distributions over the last 10 chapters
  are checked deterministically (no more than 3 identical ending types in a row; vary payoff types).
- Scene-level: deterministic repeated-paragraph checks after drafting (lint `KL-REP-*`).

## 11. Reacting to feedback (Beta)

Imported reader feedback is sanitized (untrusted), classified (pacing, character popularity, confusion,
requests), aggregated into **soft signals** attached to the next arc-outline generation with weights; the
planner reports which signals it acted on. Signals never alter hard requirements or canon.
