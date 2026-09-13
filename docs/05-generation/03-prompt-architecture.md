# Prompt Architecture

## 1. Prompt Registry (ADR-0016)

`packages/prompts` holds **prompt families** (one per role). Each family has immutable **versions**:

```
prompt_versions {
  id, family, version (semver), content_hash,
  system_template, user_template (templating with strict variable allowlist),
  output_schema_ref (schemas/… or inline JSON Schema), style_sensitive bool, style_block_role,
  model_routing_policy_ref, default_params { temperature, max_tokens, top_p, seed? },
  guards { max_input_tokens, requires_pack_template, forbids_untrusted_in_system: true },
  changelog_ko, created_by, created_at, status: draft|candidate|active|deprecated,
  regression_result_ref
}
```

- Templates are stored in the repo (`packages/prompts/families/<role>/vX.Y.Z/`) and mirrored into the DB
  at deploy with hash verification; the DB is the runtime source; the repo is the review surface.
- A project pins the `active` version set at job start (`prompt_set_version`) so a long batch does not
  change prompts mid-run unless the user opts in.
- Every `llm_calls` row records `prompt_version_id` + `content_hash`.
- Promotion: `draft → candidate` (regression suite green) → `active` (manual) → `deprecated`.

## 2. Prompt anatomy (all roles)

```
[SYSTEM]
 1. Role identity & mission (Korean for prose roles; English/Korean mixed acceptable for analytic roles)
 2. Non-negotiables: output schema; no content outside JSON; evidence rules; "do not invent canon"
 3. <<STYLE v=…>> block (style-sensitive roles)   ← Style Guard verifies presence
 4. Safety/content restriction summary (from spec; hard)
[USER]
 5. Context Pack sections in template order (stable → volatile), each with a heading and provenance tags
    [사실 v128 ch.12] / [예정] / [요약 L2] / [증거 ch.9 ¶14]
 6. Task instruction (what to produce now), including explicit constraints from the contract
 7. Output schema reminder (short) + STYLE_TAIL (writer/editor)
```
Rules:
- **No conversation history.** Each call is single-turn (system + user). Multi-step refinements are
  separate calls with explicit inputs.
- **Provenance tags on every context item** so the model can distinguish canon, plan, summary, evidence,
  untrusted.
- **Untrusted text** only in the user message, wrapped in `<<UNTRUSTED source=…>>` and preceded by an
  instruction to treat it as data; never in system.
- **Language**: prose-role instructions in Korean (reduces register drift); analytic roles may use English
  headers but Korean for domain terms and examples.
- **Few-shot**: analytic roles use 1–2 compact schema examples (synthetic); prose roles rely on the style
  block exemplars only (avoid double-anchoring).

## 3. Structured output strategy

- Provider-native JSON schema mode where available; else "JSON only" instruction + robust parser.
- Validation with the registered JSON Schema; on failure: `json_repairer` (cheap model, sees the invalid
  output + schema + error) ×2 → regenerate ×1 → fail step with diagnostics.
- Prose in `text_ko` fields with escaping handled by the SDK; large prose outputs may use a two-part format
  (JSON header + delimited text block) if a provider's JSON mode degrades Korean prose quality — the
  gateway normalizes both into the same envelope (`scene-draft.schema.json`).
- Truncation: `max_tokens` set from the length target × 1.4 safety factor (Korean tokens/char ratio
  calibrated per model); `finish_reason=length` → continuation protocol (see pipeline §8).

## 4. Role-specific prompt notes

| Role | Key instructions | Anti-patterns to enforce |
| --- | --- | --- |
| `scene_writer` | Write only the current scene; continue seamlessly from the provided previous text; obey speaker pairs' speech levels; use the knowledge lists (알고 있음/모름/오해); emit `speaker_annotations` and `claims` (facts the scene asserts) | no recap of previous chapter; no lore dumps; no English; no headings |
| `chapter_assembler` | Edit only seams; return seam patches, not full text | rewriting scenes |
| `line_editor` (Premium/pass on request) | Korean polish within meaning; return paragraph patches | changing facts (must ack) |
| `continuity_checker` | For each suspected issue, quote chapter span and cite the canonical item + evidence; state confidence; propose minimal repair | vague criticism; unsupported claims |
| `knowledge_leak_checker` | Enumerate participant utterances/actions that presuppose knowledge; check against the table | flagging narrator knowledge as character knowledge |
| `extractor_a` | Entity-first sweep: for each entity present, list state/attribute/knowledge changes with quotes | inventing off-page events |
| `extractor_b` | Event-first sweep: chronological events, participants, frames, then derived facts/knowledge | paraphrased quotes |
| `extraction_adjudicator` | Decide between conflicting items using only the provided spans; may reject both | picking without quoting |
| `style_judge` | Score with Korean anchors; evidence paragraph IDs before scores; list drift flags | praising exemplar phrasing (no exemplars given) |
| `summarizer_l1` | ≤ 350 chars; plot + state changes + hook; canonical names; no evaluation | including plans |
| `chapter_planner` | Produce a contract satisfying arc beats, cadence, and promise schedule; every knowledge delta needs a channel | scheduling reveals that guards forbid |
| `change_request_interpreter` | Convert free-text change request into patch tasks with spans or contract edits | rewriting whole chapter |

## 5. Prompt regression suite

For each family: a set of **golden cases** (inputs: fixture packs; expected: structured assertions such as
"issue with kind=knowledge_leak on paragraph 14", "no format drift", "score for translated variant <
native variant", "extractor recovers injury fact with quote"). Running the suite on every new version
produces `regression_result_ref`; promotion requires: no regression on blocking assertions; ≥ parity on
scores; cost/latency deltas reported. Suite runs against the configured models for the role and records
model versions (prompts are model-sensitive; a model change also triggers the suite).

## 6. Versioned prompt sets

`prompt_sets { id, name, mapping role→prompt_version_id, model_routing_ref }`. Projects pin a set; batches
pin at start; per-call override for experiments is recorded. Changing the set mid-project is an explicit
user action with a note in the audit log.

## 7. Security in prompts

- System prompts are static templates; no user text is interpolated into system positions except the
  content-restriction summary, which is generated from enumerated spec fields (not free text).
- Free-text requirements appear in the user message under `[요구사항 hard/soft]` with an instruction that
  they describe the *story*, not the assistant's behavior; a classifier (`instruction_injection_classifier`,
  cheap) flags requirement/direction texts that look like meta-instructions ("ignore previous rules") for
  human review before they enter the spec.
