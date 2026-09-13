# Role Catalog

Every LLM role is registered with: purpose, model class, style sensitivity (Style Guard), pack template,
output schema, default budget (Standard tier), candidate/retry policy. Model classes map to concrete
models per environment via the gateway routing table (`docs/06-system/07-model-gateway.md`); the plan
never hardcodes a vendor.

Model classes: **R** reasoning-strong · **P** Korean-prose-strong · **M** mid (fast, good structured
output) · **C** cheap/classification · **E** embeddings.

| Role | Purpose | Class | Style block | Pack template | Output schema | Max out tokens | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `requirement_interpreter` | Normalize intake → Story Spec items (hard/soft/assumption), conflicts | M | — | pack.requirements | story-spec.items | 4k | classifier-style; Korean output |
| `assumption_explainer` | One-line rationale per assumption | C | — | inline | strings | 1k | |
| `instruction_injection_classifier` | Flag meta-instructions in user/imported text | C | — | inline | label+score | 0.2k | security |
| `concept_generator` | Concept candidate from spec + angle seed | R | planner_compact | pack.concept | concept | 3k | N=2/3 |
| `concept_comparator` | Pairwise comparison of concepts | R | — | pack.compare | comparison-verdict | 2k | both orders |
| `concept_merger` | Merge selected fields | M | planner_compact | pack.concept | concept | 3k | on request |
| `character_designer` | Cast identities/arcs/secrets | R | planner_compact | pack.bible | bible.characters | 6k | |
| `speech_profile_designer` | Per-character speech levels, address terms, tics | P | writer_full (rules only, no exemplars) | pack.bible | speech-profile[] | 4k | validated vs overlay conventions |
| `world_builder` / `power_system_designer` / `faction_designer` / `location_designer` | Bible sections | R | planner_compact | pack.bible | bible.* | 4–6k | numbers-as-facts |
| `glossary_compiler` | Fixed Korean spellings, aliases, allowances | M | summarizer_min | pack.bible | glossary | 3k | mostly deterministic |
| `style_binder` | Propose profile overrides from tone/preferences | M | — (produces profile) | pack.bible | style-profile.overrides | 1k | |
| `bible_consistency_checker` | Cross-section contradictions | R | — | pack.bible | issue[] | 3k | |
| `series_architect` | Series Blueprint | R | planner_compact | pack.series_architect | series-blueprint | 8k | N=2 |
| `season_planner` | Season outlines | R | planner_compact | pack.series_architect | season[] | 6k | |
| `arc_planner` | Arc plan | R | planner_compact | pack.arc_planner | arc-plan | 6k | N=2 Standard |
| `repetition_judge` | Structural repetition vs prior arcs / recent chapters | C→M | — | pack.repetition | issue[] | 1.5k | |
| `chapter_planner` | Chapter Contract | R/M | planner_compact | pack.chapter_planner | chapter-contract | 5k | +1 repair |
| `plan_continuity_checker` | Validate plan vs canon | M | — | pack.chapter_planner | issue[] | 2k | |
| `scene_planner` | Scene plans | M | planner_compact | pack.scene_planner | scene-plan[] | 3k | |
| `scene_writer` | Korean prose for one scene | P | writer_full + TAIL | pack.scene_writer | scene-draft | length×1.4 | sequential per scene |
| `chapter_assembler` | Seam smoothing + title | M/P | editor_full | pack.line_editor | seam-patches | 2k | |
| `line_editor` | Polish pass (Premium/on request) | P | editor_full | pack.line_editor | paragraph-patches | 6k | must ack facts |
| `contract_compliance_judge` | Must/must-not/hook/POV | M | — | pack.continuity_checker (subset) | scorecard.section | 3k | evidence-first |
| `continuity_checker` | Facts/timeline/location/inventory/injury/rank/world/relationship | R | — | pack.continuity_checker | issue[] | 4k | the most expensive evaluator |
| `knowledge_leak_checker` | Knowledge leaks / dramatic irony violations | M | — | pack.knowledge_leak_checker | issue[] | 3k | |
| `promise_checker` | Setup/payoff handling | C | — | pack.promise | promise-status[] | 1.5k | |
| `pacing_hook_judge` | Hook/ending/pacing/exposition | M | planner_compact | pack.style_judge | scores+issues | 2k | |
| `style_judge` | Korean webnovel style + drift | M (different family from writer) | judge_rubric | pack.style_judge | style-report | 3k | |
| `voice_judge` | Character voice vs speech profiles | C→M | judge_rubric | pack.style_judge | issue[] | 2k | |
| `style_reviser` / `dialogue_reviser` / `continuity_reviser` | Span patches | P | editor_full | pack.reviser | patch | span×1.5 | acks required |
| `scene_rewriter` | Rewrite one scene | P | writer_full + TAIL | pack.scene_writer | scene-draft | length×1.4 | counts as rewrite |
| `chapter_comparator` | Pairwise candidate judging | R (≠ writer family) | — | pack.compare | comparison-verdict | 2k | both orders |
| `change_request_interpreter` | Free text → patch tasks / contract edits | M | — | pack.reviser | change-plan | 2k | |
| `extractor_a` | Entity-first canon extraction | M | — | pack.extractor | canon-delta | 8k | |
| `extractor_b` | Event-first canon extraction | M (other family if possible) | — | pack.extractor | canon-delta | 8k | |
| `extraction_adjudicator` | Resolve conflicts | R | — | pack.adjudicator | adjudication | 2k | conflicts only |
| `summarizer_l1` / `_l2` / `_l3` / `_l4` | Hierarchical summaries | C/M | summarizer_min | pack.summarizer | summary | 0.6–2k | accepted text only |
| `title_generator` | Chapter title (genre style) | C | writer_full (compact) | inline | strings | 0.2k | folded into assembler by default |
| `retcon_patcher` | Patch text for a described retcon | P | editor_full | pack.reviser | patch | 4k | |
| `dependency_patch_proposer` (Beta) | Propose patches for stale later chapters | P | editor_full | pack.reviser | patch[] | 4k | |
| `feedback_classifier` (Beta) | Classify sanitized reader feedback | C | — | inline (untrusted wrapped) | labels | 0.5k | |
| `json_repairer` | Fix invalid structured output | C | — | inline | any | = original | |
| `embedder` | Embeddings for search documents | E | — | — | vector | — | |

## Routing principles

- **Prose (P)** — the highest-leverage choice for Korean nativeness; evaluated per model in the Korean
  style benchmark (contrast pairs + editor ratings) before being routed. At least two P-capable models are
  configured for fallback.
- **Judges** use a **different family** from the writer when available (self-preference mitigation).
- **Extractors A/B** use different prompts and, where budget allows, different families; Economy tier uses
  one family with two prompts.
- **R** roles are few per chapter (continuity_checker, comparator, adjudicator) to control cost.
- Any role may be re-routed by the gateway on outage; the audit records the actual model.
