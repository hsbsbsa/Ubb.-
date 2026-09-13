# Generation Pipeline

## 1. Overview

Three durable workflow families produce the novel:

1. **Setup workflows** (once per project, re-run on major changes): `RequirementInterpretationWorkflow`,
   `ConceptWorkflow`, `StoryBibleWorkflow`, `SeriesPlanningWorkflow`.
2. **Planning workflows** (rolling): `PlanningHorizonWorkflow` (arc outlines, chapter contracts, scene plans).
3. **Production workflows** (per chapter): `ChapterProductionWorkflow`, orchestrated in batches by
   `BatchProductionWorkflow`; plus `CanonCommitWorkflow` (child), `RevisionWorkflow` (child),
   `RetconWorkflow`, `CorrectionWorkflow`, `RegenerationWorkflow`, `ExportWorkflow`.

Every step that calls a model is an **Activity** with: role, prompt version, pack, schema, budget check,
idempotency key, audit record. No activity relies on prior conversation.

## 2. Setup workflows

### 2.1 RequirementInterpretationWorkflow
```
intake(form + free text)
 → A1 requirement_interpreter (mid model): normalize → Story Spec items {text_ko, kind: hard|soft|assumption,
    category, provenance, confidence}; detect conflicts
 → deterministic: schema validate; enforce that content restrictions & explicit "must/must not" are hard
 → A2 assumption_explainer (cheap): one-line rationale per assumption (for UI)
 → gate: assumption review (human in all modes for v1; Autopilot auto-confirms "safe defaults" category)
 → persist Story Spec v1
```
Calls: 2 (+1 if conflicts need a re-pass). Budget: tiny.

### 2.2 ConceptWorkflow
```
 → A1..An concept_generator ×N (reasoning-strong; N=2 Standard, 3 Premium) in parallel, diversity forced
   by distinct "angle" seeds (e.g., 사이다 중심 / 감정선 중심 / 미스터리 중심)
 → A(n+1) concept_comparator pairwise, both orders (reasoning-strong, different family if available)
 → deterministic: aggregate verdicts, detect position inconsistency → tie-break rule (ADR-0015)
 → gate: user selects/merges (merge → A(n+2) concept_merger)
```
Calls: N + C(N,2)×2 (+1). N=2 → 4 calls.

### 2.3 StoryBibleWorkflow
Sequential specialists, each producing schema-validated JSON, each receiving the spec + concept + previous
outputs (as data, not chat):
```
character_designer (protagonist + core cast; identities, goals, flaws, arcs, secrets)
 → speech_profile_designer (per character: speech levels by counterpart, address terms, tics; validated
   against overlay conventions, e.g., 무협 하오체)
 → world_builder (rules, institutions, geography as needed)
 → power_system_designer (ranks, costs, limits, cadence; numbers as facts)
 → faction_designer (if genre needs) → location_designer
 → glossary_compiler (deterministic + 1 call: fixed Korean spellings, aliases, Hanja/English allowances)
 → style_binder (deterministic compose of profile; 1 cheap call proposing overrides from spec tone/prefs)
 → bible_consistency_checker (reasoning-strong): contradictions across sections, missing pieces
 → gate: bible approval (human; Autopilot auto-approves if checker clean)
 → canon commit v1 (source=bible): locked facts + approved bible facts (no evidence spans; source=bible)
```
Calls: ~8–10.

### 2.4 SeriesPlanningWorkflow
```
series_architect ×N (2) → comparator pairwise → gate (blueprint approval)
 → season_planner (all seasons outline) → arc_planner for arc 1 (×2 → judged) and arc 2 (×1)
 → repetition_judge (arc 2 vs arc 1) → chapter_planner for chapters 1..H → plan validators
 → gate (arc 1 approval; contracts per mode)
```
Calls: ~12–16 for a 200-chapter series' initial planning.

## 3. PlanningHorizonWorkflow

Triggered after each canon commit, direction change, plan edit, or correction/retcon. Steps: compute
required horizon; validate existing contracts (deterministic + `plan_continuity_checker` when
dependencies changed); regenerate stale/missing contracts (`chapter_planner`); extend arc outlines when
needed (`arc_planner` + `repetition_judge`); update promise schedule; emit UI diffs. Typical: 1–2 calls per
accepted chapter (amortized).

## 4. ChapterProductionWorkflow (the core)

```
[0] preflight: lease chapter; check previous chapter accepted; check budgets; record canon_version_read;
    validate contract (deterministic + plan_continuity_checker if stale) → if invalid → PlanningHorizon repair
[1] scene_planner → ScenePlan (2–4 scenes) → deterministic validation vs contract & profile
[2] for each scene i (sequential):
      pack.scene_writer(scene i, previous scenes verbatim, previous chapter tail)
      → scene_writer → structured output { text_ko, speaker_annotations[], claims[], intentional_shifts[] }
      → deterministic: truncation, length, lint (scene-level), register check, glossary spelling
      → if scene lint fails hard → one scene_writer retry with violations listed; else continue
[3] chapter_assembler (mid): joins scenes, smooths transitions only at seams (edits limited to ±2
    paragraphs around seams; output = seam patches), proposes chapter title (genre-styled)
[4] deterministic chapter checks: length vs target, lint (chapter), register, repetition (intra + cross
    chapter), format, forbidden lexicon, required-scene markers
[5] evaluation fan-out (parallel activities):
      contract_compliance_judge · continuity_checker · knowledge_leak_checker · relationship_checker
      · world_rule_checker (incl. power/inventory/injury/rank) · promise_checker (uses extraction pre-pass)
      · pacing_hook_judge · style_judge · voice_judge · repetition_judge (scene-level vs L1/L2)
    → Scorecard (merged issues, clustered by span)
[6] decision:
      no blocking & no major → [8]
      else → RevisionWorkflow (child): patch-first repair (see 02-evaluation-and-revision-pipeline.md)
             → re-evaluate affected checks → loop ≤ max_rounds → if still blocking → needs_attention
[7] candidate policy (Premium or on request): steps [1]–[6] run for N candidates (parallel branches with
    the same pack); chapter_comparator pairwise both orders on final versions + scorecards → pick
[8] gate by mode: Assisted → wait for approval signal; Semi-auto → auto-approve if score ≥ threshold and
    no major; Autopilot → auto-approve unless escalation criteria
[9] on approve → CanonCommitWorkflow (child): extractor_a ∥ extractor_b ∥ deterministic pre-pass
    → reconciler → adjudicator (conflicts only) → verifier → atomic commit → post-commit
    (summaries L1 now, L2–L4 refresh if arc/season boundary, embeddings, exemplar candidates,
     promise status, dependency edges, PlanningHorizonWorkflow signal)
[10] release lease; job complete with cost summary
```

### 4.1 Call budget (Standard tier, 3-scene chapter, no candidates)

| Step | Calls | Model class |
| --- | --- | --- |
| scene_planner | 1 | mid |
| scene_writer | 3 (+≤1 retry) | prose-strong |
| chapter_assembler | 1 | mid |
| evaluators | contract 1, continuity 1, knowledge 1, world/relationship/promise merged into continuity pack? No — kept separate for evidence quality but **batched**: `continuity_checker` covers facts/timeline/location/inventory/injury/rank/world rules/relationships (1 call, 20k pack); `knowledge_leak_checker` 1; `promise_checker` 1 (cheap); `pacing_hook_judge` 1 (cheap-mid); `style_judge` 1; `voice_judge` 1 (cheap-mid); `repetition_judge` 1 (cheap) | 7 |
| revision (typical 1 round, 2–4 patches) | 1–3 reviser calls + 1–2 re-checks | mid/prose-strong |
| extraction | 2 extractors + 0–1 adjudicator | mid (one may be prose-strong family for diversity) |
| summaries | L1 1 | cheap |
| **Total** | **≈ 17–22** | |

Economy tier: single extractor pass + deterministic cross-check (B pass only on `major` items), merged
style+voice judge, no pacing judge (lint heuristics only) → ≈ 11–13 calls. Premium: N=2 candidates for
drafting (+writer/assembler/judge calls), two judge families for style, adjudicator always available →
≈ 35–45 calls.

### 4.2 Parallelism
Scenes are sequential (each needs the previous scene's text). Evaluators run in parallel. Extractors run in
parallel. Candidates run as parallel branches. Batches are sequential across chapters.

### 4.3 Determinism & idempotency
Activity idempotency key = `(workflow_id, step_id, scene_i|candidate_j|round_r, attempt_scope)`. A retried
activity first checks `llm_calls` for a completed record with the same key and returns it (no duplicate
spend). Provider `seed` is set when supported, but determinism is not assumed.

## 5. BatchProductionWorkflow

Child workflow per chapter, sequential; between chapters: check budget headroom (predicted next chapter cost
≤ remaining), check stop signals (pause/cancel), apply new directions (signal → PlanningHorizon runs
before the next chapter). Gate policy: `pause_on_review` (default) or `continue_and_queue` (only valid in
Autopilot since later chapters require acceptance — so in practice `continue_and_queue` means the batch
ends at the first chapter requiring review).

## 6. Regeneration, retcon, correction workflows

- **RegenerationWorkflow**: dependency report (deterministic) → user choice → `ChapterProductionWorkflow`
  with `supersedes` → commit retracts superseded items → propagation.
- **RetconWorkflow**: new version (user edit or `retcon_patcher` from description) → deterministic checks →
  evaluators (continuity vs canon *excluding* items sourced from the old version) → approve → extraction
  diff → commit → propagation (mark-only MVP; Beta: `dependency_patch_proposer` per stale chapter).
- **CorrectionWorkflow**: canon item edit → impact report → commit → propagation; optional
  `retcon_patcher` on the source span.

## 7. Roles (summary; full catalog in `04-role-catalog.md`)

Reasoning-strong: series_architect, arc_planner, concept_generator/comparator, bible_consistency_checker,
continuity_checker, extraction_adjudicator, chapter_comparator. Prose-strong (Korean): scene_writer,
style_reviser, dialogue_reviser, scene_rewriter. Mid: chapter_planner, scene_planner, chapter_assembler,
line_editor, extractor_a/b, style_judge, contract_compliance_judge, knowledge_leak_checker. Cheap:
requirement classifier, assumption_explainer, summarizer_l1, promise_checker, repetition_judge,
voice_judge, pacing_hook_judge, title_generator, cost predictor features. Embeddings: embedder.

## 8. Output contracts

All non-prose outputs are JSON validated against `schemas/`; prose outputs are wrapped in a small JSON
envelope (`scene-draft.schema.json`) with `text_ko` plus annotations so that speaker/level/claims metadata
travels with the text. Invalid JSON → `json_repairer` (cheap) ×2 → regenerate ×1 → step failure.
Truncation (`finish_reason=length` or `KL-TRUNC-01`) → continuation call with the last 600 chars as anchor
and remaining length target, ×1; else regenerate the scene with a reduced target.
