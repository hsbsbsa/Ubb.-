# Evaluation and Revision Pipeline

## 1. Evaluation model

Two kinds of checks, one issue format:

- **Deterministic checks** (`packages/style`, `packages/korean`, `packages/canon`): schema validity,
  truncation, length, Korean lint, register, glossary spelling, forbidden lexicon, format drift,
  repetition (intra/cross-chapter simhash), 상태창 grammar, required-scene markers (contract `verifiable_by`
  patterns), numeric consistency for 상태창 numbers vs facts.
- **Model-based evaluators** (roles): contract compliance, continuity (facts/timeline/location/inventory/
  injury/rank/world & power rules/relationships), knowledge leakage, promise handling, pacing & hook, style,
  voice, repetition (semantic).

`Issue` (schema `issue.schema.json`):
```
{ id, source: lint|register|judge:<role>, kind, severity: blocking|major|minor|note, confidence 0..1,
  claim_ko, chapter_span: { manuscript_version_id, paragraph_ids[], start, end, quote },
  conflicting_canon: [{ kind: fact|event|knowledge|relationship|promise|requirement|plan, id, statement_ko }],
  canon_evidence: [{ manuscript_version_id, chapter_no, quote, start, end }],
  repair: { scope: sentence|paragraph|dialogue|scene|chapter|plan|canon, suggestion_ko, must_preserve_fact_ids[] },
  status: open|patched|overridden|dismissed, override_reason?, resolved_in_version_id? }
```
Issues lacking a resolvable `chapter_span` are capped at `note`. Issues asserting a canon conflict must cite
≥ 1 `conflicting_canon` **and** ≥ 1 `canon_evidence` (or the canon item must be `source=bible/locked`); else
they are downgraded to `minor` with `unsupported=true` (never block on unsupported criticism).

## 2. Evaluator specifications

| Evaluator | Detects | Inputs (pack) | Output specifics |
| --- | --- | --- | --- |
| `contract_compliance_judge` | missing must_happen, present must_not_happen, required scene absence, hook/opening type mismatch, POV violation, emotional movement unmet | contract + chapter text | per criterion: pass/fail + evidence paragraph IDs |
| `continuity_checker` | contradictions with facts (identity, location, injury, inventory, rank, resources, abilities), timeline errors (elapsed time, impossible travel, day/night), world-rule & power-system violations, relationship inconsistency (trust/affection direction, address term, speech level vs canon) | chapter text, participant state tables with evidence, locked facts, retrieved older events, timeline position, world rules slice | each issue cites the chapter span and the canonical fact/event + evidence quote |
| `knowledge_leak_checker` | character acts/speaks on knowledge they lack; character unaware of what they know; reader-knowledge violations (spoiling planned reveals) | chapter text, knowledge table for participants, guards, secrets | issue per leak with ledger row IDs |
| `promise_checker` | payoff without setup; planned setup/payoff missing; promise contradicted | contract setups/payoffs, promise ledger slice, extraction pre-pass | status per promise |
| `pacing_hook_judge` | late hook, weak ending, exposition drag, scene sag, missing local payoff | chapter text, contract shape fields, planner-compact style block | scores + spans |
| `style_judge` / `voice_judge` | see Korean style docs | judge block, text, lint report, speech digests, voice exemplars | scores, drift flags, issues |
| `repetition_judge` | scene/arc-level repetition vs recent L1/L2 summaries; repeated jokes/beats | chapter L1 (from pre-pass) + last 10 L1s + current arc L2 | issues with references |

Judges are **evidence-first**: output schemas place `evidence` before `verdict/score`.

## 3. Severity policy

| Severity | Examples | Effect |
| --- | --- | --- |
| blocking | contradiction with locked fact; knowledge leak of a secret; forbidden development present; content restriction violation; format drift (screenplay); truncation; required scene missing; register error toward royalty in strict profile | cannot accept; must patch or regenerate |
| major | contradiction with unlocked fact without narrated change; injury/inventory/rank mismatch; timeline impossibility; payoff without setup; speech-level mismatch; style drift ≥ 30% paragraphs; repeated paragraph; must_happen partially met | must patch or human override with reason |
| minor | lint warns; weak ending (judge medium confidence); exposition run; low-confidence continuity doubts | advisory; auto-patched if cheap and safe (lint-only) |
| note | unsupported criticism; suggestions | logged |

Confidence gating: model-based issues with `confidence < 0.5` are capped at `minor`; `< 0.3` at `note`.
Two independent judges agreeing (Premium) raises confidence by fusion.

## 4. Revision (patch-first)

```
Scorecard issues (open) ─► cluster by span (overlapping/adjacent paragraphs; same scene)
  ─► order: blocking → major → minor; continuity/knowledge before style (content first, then polish)
  ─► for each cluster: choose reviser role by dominant kind
        continuity_reviser (facts/timeline/knowledge)  · dialogue_reviser (register/voice)
        style_reviser (lint/style drift)               · scene_rewriter (scene-scope)
  ─► pack.reviser: editor block, span ± 1 paragraph (scene plan for scene scope), issues + repair hints,
     must_preserve facts (IDs + statements + quotes), speech digests, length budget, glossary
  ─► reviser output { span_id, new_text_ko, changed_claims[], preserved_facts_ack[] , speaker_annotations[] }
  ─► deterministic gate: acks complete; length within ±15% (scene ±10%); glossary; lint on new text;
     register on new utterances; no new forbidden lexicon
  ─► apply → new manuscript version (parent link, patch record)
  ─► regression: re-run affected checks (see below); compare scorecards; revert patch on regression
  ─► loop until no blocking/major or round limit
```

### 4.1 Which checks re-run after a patch
| Patch scope | Re-run |
| --- | --- |
| sentence/paragraph, `changed_claims=[]` | lint + register on span±1; repetition intra-chapter |
| sentence/paragraph, `changed_claims≠[]` | + continuity_checker on the span (delta mode: only changed claims), knowledge_leak_checker if any claim involves a proposition |
| dialogue | + voice_judge on changed utterances |
| scene | full deterministic chapter checks + continuity_checker (full) + style_judge (scene) + contract_compliance (affected criteria) |
| ≥ 3 patches cumulative | style_judge whole chapter (smoke) + repetition (cross-chapter) |

### 4.2 Limits
`max_revision_rounds` (Standard 3, Economy 2, Premium 4); `max_patches_per_round` 6; `max_scene_rewrites`
2; per-span attempt counter 2 → escalate scope. Exhaustion → `needs_attention` with the residual issues,
suggested action (regenerate / accept with override / edit manually).

## 5. Candidate comparison (when N > 1)

- Same pack, same prompt, different seeds/angles (diversity hint for creative steps only; none for
  evaluators).
- Each candidate goes through steps [2]–[6]; only candidates with no blocking issues are compared.
- `chapter_comparator` receives both texts + both scorecards + contract; asked for per-dimension
  preferences (contract fit, continuity risk, style, hook, emotional impact) with evidence; run in **both
  orders**; consistent winner → pick; inconsistent → third run with shuffled dimension order, majority;
  still tied → higher scorecard; still tied → cheaper (fewer patches).
- Early stop: if the first candidate's scorecard ≥ `early_stop_threshold` (Standard 88/100) with no major
  issues, skip generating further candidates (budget saver). Configurable per project.

## 6. Human review integration

Review UI shows: manuscript (mobile view), scorecard, issues (with the evidence links), patch history
(diff per version), candidate comparison, extraction preview (proposed delta). Actions produce signals to
the waiting workflow: `approve`, `request_changes(text)` → `change_request_interpreter` (cheap) converts to
patch tasks (scoped) or, if it invalidates the contract, to a contract edit + regeneration proposal;
`reject(reason)`; `override(issue_ids, reason)`.

## 7. Calibration & regression of evaluators

- Golden fixtures with seeded issues (fixture story traps) → every evaluator prompt version must reach
  recall ≥ 0.9 on blocking traps, precision ≥ 0.8 on major; measured in the prompt regression suite.
- Human override rates per evaluator per kind tracked; > 30% override on a kind → prompt/threshold review.
