# Narrative Identity Profiles — Specification

Normative companion to `schemas/narrative-identity.schema.json`. Describes the shipped profiles
`lang/en@1` and `tradition/kr-webnovel@1`, how genre overlays and project profiles compose, and the compile
rules for the Narrative Identity Block. **All numeric values are documented starting points, not
universal truths** — they are calibrated per project (ADR-0029, §7).

## 1. Output-Language Profile: `lang/en@1`

| Key | Default | Notes |
| --- | --- | --- |
| `language` | `en` | the only supported manuscript language in MVP/Beta/Production |
| `locale` | `en-US` | `en-GB` selectable per project; drives spelling and quotation conventions |
| `punctuation.dialogue_quotes` | `“ ”` (en-US) / `‘ ’` (en-GB) | straight quotes flagged |
| `punctuation.thought` | italics (`*…*` in draft envelope → export styling) | no quote marks for inner monologue by default |
| `punctuation.dash` | em dash `—` without spaces (en-US) | en dash with spaces (en-GB) |
| `punctuation.ellipsis` | `…` | `...` normalized |
| `numbers.style` | words to nine, numerals from 10; ranks/levels as given (`F-rank`, `Lv. 3`) | genre overlays may override for status text |
| `currency_measurement` | per Setting Profile (won → "won" romanized; metric units) | |
| `tense.narration` | past | present allowed inside status/system text |
| `contract_text` | the Output-Language Contract (architecture §3.1) | versioned text |
| `translation_markers` | list of translation-like syntax patterns (lint §2.3) | data, per version |
| `fluency_thresholds` | starting values for Prose Lint | calibrated |

## 2. Narrative-Tradition Profile: `tradition/kr-webnovel@1`

Structural rules of Korean serialized web fiction, expressed language-neutrally.

### 2.1 Structure

| Key | Starting value | Notes |
| --- | --- | --- |
| `chapter.hook_within_sentences` | 5 | first tension/continuation beat |
| `chapter.opening_types_allowed` | `continue_cliffhanger`, `in_medias_res`, `sharp_dialogue`, `status_update`, `time_skip_with_tension` | |
| `chapter.opening_types_forbidden` | `weather_landscape`, `lore_dump`, `waking_up_routine` | |
| `chapter.scene_count_band` | 2–4 per episode | |
| `chapter.local_payoff_required_any_of` | `satisfaction` (사이다), `revelation`, `emotional_step`, `growth_confirmed`, `humor_beat` | |
| `chapter.ending_types_allowed` | `cliffhanger`, `reveal`, `decision`, `arrival_of_threat`, `emotional_peak`, `quiet_ominous` | |
| `chapter.ending_types_forbidden` | `mid_scene_fade`, `summary_reflection` | |
| `cadence.progression_event_every_chapters` | 4 (genre overrides) | |
| `cadence.satisfaction_every_chapters` | 3 | 사이다 beat interval |
| `cadence.max_frustration_streak` | 3 | 고구마 streak |
| `exposition.max_consecutive_sentences` | 4 | |
| `exposition.lore_via` | `action`, `dialogue`, `status_text`, one flagged `narration_slot` per chapter | |
| `exposition.new_terms_per_chapter_max` | 6 | |

### 2.2 Rhythm (language-neutral targets rendered per output language)

| Key | Starting value | Notes |
| --- | --- | --- |
| `paragraph.max_sentences` | 3 | mobile readability |
| `paragraph.max_words` | 60 narration / 40 dialogue paragraphs | the English rendering of the mobile paragraph norm; calibrated |
| `paragraph.single_line_ok` | true | one-line paragraphs for emphasis |
| `sentence.variance` | high | alternate punches with mid-length sentences |
| `dialogue.ratio_band` | 0.35–0.55 of words inside dialogue | |
| `dialogue.reaction_beats` | interleave | |
| `monologue.ratio_band` | 0.08–0.25 | inner monologue in italics |
| `monologue.hindsight_max_ratio` | 0.20 | regression overlays |

### 2.3 Serial devices (genre profiles enable and shape them)

`status_window`, `system_message`, `ranking_board`, `community_interlude`, `hindsight_monologue`,
`measurement_scene`, `rank_reveal`, `letter`. Each has an English **format grammar** (e.g., status window):

```
[Status Window]
Name: Han Seo-jun   Level: 13   Class: Swordsman
STR 15   AGI 11   VIT 13
Skills: Sword Strike Lv. 3, Evasion Lv. 2
```

### 2.4 Contract text and rubric
`contract_text` = the Narrative-Tradition Contract (architecture §3.2). `rubric` = Structure Judge
dimensions with 1–5 anchors: hook strength; episode payoff; pacing & scene rhythm; exposition control;
dialogue-forwardness; ending pull; serial-device use; cadence fit. Anchor example (ending pull): 5 = "the
last lines create an immediate reason to open the next episode (question, threat, decision, reveal)";
3 = "the chapter ends at a natural stopping point with mild curiosity"; 1 = "the chapter ends on summary or
reflection with no forward pull".

## 3. Genre Profiles (overlays)

Overlay = partial profile that **patches** the composed identity (JSON Merge Patch semantics; arrays
replaced unless key ends with `+` for append). Each overlay includes `reader_fantasy`, `vocabulary`
(English terms + terminology defaults for Korean-origin concepts), `devices`, `cadence` overrides,
`register_notes` (default relationship classes and titles typical of the genre), `taboos`,
`judge_notes`, `lint_thresholds`. The 16 overlays are described in `03-genre-catalog.md`. At most 3
overlays; one `primary` sets structure defaults.

## 4. Setting & Cultural Profile (project)

| Key | Example (fixture) |
| --- | --- |
| `setting_type` | `modern_korea` (alternatives: `secondary_world`, `murim_historical`, `other`) |
| `place_names_policy` | real Seoul districts romanized (`Gangnam`, `Mapo`) |
| `institutions` | Hunter Association, guilds, measurement bureau — described in English |
| `currency` | won (rendered "won", figures in Arabic numerals with commas) |
| `cultural_texture` | `preserve_behaviors_localize_language`: age/seniority-based deference is *shown* (behavior, titles, tone) but expressed in natural English |
| `cultural_reference_policy` | explain in-world when needed; never footnote |

## 5. Naming Profile (project)

| Key | Example (fixture) |
| --- | --- |
| `style` | `korean_romanized` (alternatives: `western`, `invented`, `mixed_by_faction`) |
| `romanization_system` | Revised Romanization |
| `name_order` | family–given (`Kang Do-yoon`) |
| `given_name_hyphenation` | hyphenated (`Do-yoon`) |
| `registry` | per entity: `display_name` (manuscript), `native_script_name` (optional), `romanization`, `short_forms` allowed in narration/dialogue (`Do-yoon`), `aliases` |

Rules: manuscripts use `display_name`/`short_forms` only; native-script names never appear in prose unless
the terminology policy has a `preserve_script` context; the registry is enforced by lint (`EP-NAME-*`).

## 6. Dialogue-Register Policy (project)

Replaces Korean speech-level enforcement with abstract, canonical register data rendered in English.

### 6.1 Axes (per directed pair, with validity)
`formality` 0–4 · `deference` 0–4 · `familiarity` 0–4 · `intimacy` 0–4 · `directness` 0–4 · `public_variant`
(optional overrides in public) · `address_terms[]` (English: "Mr. Park", "Senior Park", "sir", "Do-yoon",
"kid") · `titles[]` ("Vice-Guildmaster", "Chairman") · `contractions` `avoid|neutral|free` ·
`hedging` `high|medium|low`.

### 6.2 Rendering rules (how axes become English)
| Axis state | English rendering guidance |
| --- | --- |
| high formality + high deference (junior → senior/royalty) | full titles or "sir/ma'am", few contractions, requests as questions, no first names |
| moderate formality (colleagues) | surname + title or full name early; contractions neutral; polite directness |
| low formality + high familiarity (friends/peers) | first names/nicknames, contractions free, teasing allowed |
| intimacy milestone (lovers) | first name alone, softer directness, shared shorthand |
| public variant | revert to titles in public even after intimacy ("Hunter Kang" in front of the guild) |
| mockery/anger shift | exaggerated formality or sudden bluntness — must be flagged `intentional_shift` |

The policy also lists **anti-patterns**: honorific suffixes as English morphemes (`-ssi`, `-nim`, `-ah`),
literal kinship terms for non-kin ("older brother" for 형/오빠 used as an address term → render as a name,
nickname, or "hyung" only if the terminology policy romanizes it), and stilted "Have you eaten?" calques.

### 6.3 Relationship-driven changes
Register transitions are canonical facts on `relationship_states` (e.g., "from ch.87 Do-yoon and Seo-ha use
first names; in public they keep surname + title"). The register check reads them at the utterance's story
time.

## 7. Terminology & Romanization Policy (project)

| Field | Values | Example |
| --- | --- | --- |
| `term.source` | Korean-origin concept | 헌터 |
| `term.decision` | `translate` / `romanize` / `gloss_first_use` / `preserve_script` | `translate` → *hunter* |
| `term.english` | fixed English rendering | "hunter", "gate", "awakened", "mana stone" |
| `term.romanized` | if romanized | *sunbae*, *murim*, *gwangho* |
| `term.gloss` | one-line English gloss for first use | "sunbae — a senior colleague or upperclassman" |
| `term.preserve_contexts[]` | where Korean script may appear | in-world signage, epigraph |
| `defaults` | by genre: hunter/gate → translate most; murim → romanize core terms + gloss; romance fantasy → translate (Western titles) | |

Deterministic enforcement: `EP-TERM-01` unapproved untranslated term (romanized token not in registry);
`EP-TERM-02` inconsistent rendering (two spellings for one term); `EP-TERM-03` Korean script outside
preserve contexts (blocking — this is also the output-language check's territory); `EP-TERM-04` gloss
missing on first use when policy requires it.

## 8. User Prose Preferences (project)

Numeric overrides on thresholded keys (validated against sanity ranges), textual preferences
(`{ text, priority: must|prefer, scope }`), forbidden expressions, exemplar policy. Preferences **cannot**
disable or contradict the two contracts (compiler rejects overrides that target contract text or the
output language).

## 9. Compile rules (Narrative Identity Block)

1. Header `<<NARRATIVE_IDENTITY v=<hash> identity=<id>@<ver> role=<role>>>`.
2. Sections in fixed order (architecture §4); the two contracts are always first and never shed.
3. Rendering is table-free English bullets; numeric targets appear as concrete instructions ("keep
   paragraphs to three sentences or fewer").
4. Exemplars (writer/editor only): selected deterministically by `(function_tag, score desc, recency desc)`,
   ≤ 120 words each, wrapped `[EXEMPLAR:hook] … [/EXEMPLAR]`, never more than `exemplar_policy.max_count`.
5. Budget fitting sheds in reverse priority; overflow → compile error.
6. `IDENTITY_TAIL` returned for writer/editor roles.
7. Hash = SHA-256 of the rendered text; manifest lists all profile versions, exemplar IDs, participant
   register digest versions, dropped sections, and the two contract hashes separately (the Guard checks
   both).

## 10. Participant register digest

Per participant (max 6): `display name (short forms) · toward each present counterpart: register summary
(e.g., "formal, deferential — 'Senior Park', no contractions") · verbal habits · forbidden expressions ·
current relationship-driven state (e.g., "since ch.87: first names in private, titles in public")`.
Generated from the relationship and knowledge ledgers at the chapter's story time.

## 11. Calibration (ADR-0029)

Every threshold has: `starting_value`, `calibration_status` (`uncalibrated` / `contrast_calibrated` /
`project_calibrated`), `last_calibrated_at`, `evidence_ref`. Calibration inputs: the five-class contrast set,
reviewer overrides, and per-project accepted-chapter statistics after ≥ 10 chapters. Changing a threshold
creates a new profile version.
