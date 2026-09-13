# Chapter Contract Specification

Normative companion to `schemas/chapter-contract.schema.json`. A contract is created by `chapter_planner`,
validated deterministically and by `plan_continuity_checker`, approved per operating mode, and then drives
scene planning, drafting, evaluation, and acceptance. **The chapter is accepted only if the contract's
acceptance criteria are satisfied.**

## 1. Identity and lineage

| Field | Meaning |
| --- | --- |
| `id`, `project_id`, `chapter_number` | UUIDv7; chapter numbers are contiguous positive integers within the project (renumbering on deletion is an explicit operation) |
| `version` | Contract version; edits create new versions |
| `arc_id`, `minor_arc_id`, `season_id` | Parents |
| `beat_refs[]` | Arc beats this chapter realizes |
| `spec_version`, `bible_version`, `style_profile_version`, `canon_version_planned_at` | Inputs pinned when the contract was produced |
| `status` | `draft`, `validated`, `approved`, `stale`, `superseded`, `realized` |
| `stale_reasons[]` | Populated by dependency invalidation |

## 2. Purpose

| Field | Meaning |
| --- | --- |
| `purpose_ko` | One or two sentences: why this chapter exists in the series |
| `reader_experience_ko` | The intended felt experience (e.g., "통쾌함 뒤에 불안") |
| `arc_objective_contribution` | Which arc objective(s) it advances and how |

## 3. Requirements (inherited + local)

| Field | Meaning |
| --- | --- |
| `must_happen[]` | Events/beats that must occur; each with `kind` (event, revelation, decision, progression, relationship, comedic beat), `description_ko`, optional `proposition_ids`, `entity_ids`, and `verifiable_by` (extraction rule or judge criterion) |
| `must_not_happen[]` | Inherited forbidden developments (spec/arc) + local (e.g., "아직 정체 공개 금지") with source references |
| `required_scenes[]` | User-mandated scenes bound to this chapter (spec references) |
| `hard_requirement_refs[]` | Spec requirement IDs that apply here (content restrictions always included) |

## 4. Cast, setting, time

| Field | Meaning |
| --- | --- |
| `pov` | `{ character_id, person: 1st|3rd_limited|3rd_omniscient(restricted by profile) }`; multi-POV chapters list segments |
| `participants[]` | `{ character_id, role_in_chapter: protagonist|antagonist|ally|foil|cameo, on_page: bool }` |
| `mentioned_only[]` | Characters referenced but absent |
| `locations[]` | Location IDs with order; travel legitimacy validated against last known locations |
| `story_time` | `{ start: StoryClock, end: StoryClock, elapsed_hint_ko }` on the chapter's timeline |
| `timeline_id` | Default main; regression stories set explicitly |

## 5. Deltas (planned; frame = plan until realized)

| Field | Meaning |
| --- | --- |
| `knowledge_deltas[]` | `{ knower_id (character|narrator|reader), proposition_id or new_proposition_ko, from_stance, to_stance, how_ko }` — validated: the proposition must exist in canon or in `introduces[]`; the knower must be able to learn it in this chapter (present or informed via a listed channel) |
| `state_deltas[]` | `{ entity_id, attribute (location|injury|item|rank|resource|status|ability), from, to, when_in_chapter }` |
| `relationship_deltas[]` | `{ from_id, to_id, axis (trust|affection|respect|hostility|dependency), direction, magnitude, address_term_change?, speech_level_change? }` |
| `introduces[]` | New entities/propositions this chapter may create (names pre-registered in glossary with fixed spelling) |
| `setups[]` | Promise IDs opened/advanced with how |
| `payoffs[]` | Promise IDs paid with how |
| `progression` | `{ milestone_id?, magnitude, mechanism_ko }` if a progression beat occurs |

## 6. Shape

| Field | Meaning |
| --- | --- |
| `emotional_movement` | `{ start_ko, end_ko, peak_ko }` |
| `conflict` | `{ type: external|internal|interpersonal|social, description_ko, reversal?: description_ko }` |
| `local_satisfaction[]` | ≥ 1 of `사이다`, `정보_공개`, `감정_진전`, `성장_확인`, `유머_포인트` with description |
| `ending_state_ko` | Where things stand at the last line |
| `hook` | `{ type: from profile.ending_types_allowed, description_ko, question_raised_ko }` |
| `opening` | `{ type: from profile.opening_types_allowed, description_ko }` |
| `scene_count` | Integer within profile band |
| `dialogue_density_target` | Number within profile band |
| `monologue_density_target` | Number within band |
| `length_target_chars` | From project default or override; tolerance from profile |
| `style_profile_version` | Pinned |
| `tone_notes_ko[]` | Chapter-specific tone directions |

## 7. Risk and validation

| Field | Meaning |
| --- | --- |
| `continuity_risks[]` | `{ description_ko, related_fact_ids[], mitigation_ko }` (e.g., 부상 상태, 인벤토리, 위치, 시간 경과, 비밀 유지) |
| `continuity_anchors[]` | Facts (IDs + evidence) that must be respected and that the context pack must include at T1 |
| `knowledge_guards[]` | `{ character_id, must_not_know_proposition_ids[] }` — used by the leakage checker and injected as explicit constraints to the writer |
| `validation` | `{ canon_ok, plan_ok, style_ok, issues[] , validated_at_canon_version }` |

## 8. Acceptance criteria

`acceptance_criteria[]`: each `{ id, kind: deterministic|judge|human, description_ko, check_ref }`.
Auto-populated: all `must_happen` (judge: contract compliance with evidence), all `must_not_happen` (judge +
lexical), length (deterministic), lint thresholds (deterministic), style score ≥ tier threshold (judge),
register violations = 0 blocking (deterministic), continuity blocking = 0 (judge with evidence), knowledge
leaks = 0 (judge), promise handling as planned (extraction pre-pass), hook present (judge). Plus user-added
criteria.

Acceptance rule: all `deterministic` pass; all `judge` pass or overridden by a human with recorded reason;
`human` criteria satisfied by explicit approval (Assisted) or auto-approval policy (Semi-auto/Autopilot).

## 9. Example (abridged, fixture story chapter 12)

See `examples/fixture/chapter-contract.ch12.json`.
