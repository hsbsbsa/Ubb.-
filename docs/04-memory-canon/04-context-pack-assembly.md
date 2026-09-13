# Context Pack Assembly

## 1. Definition

A **Context Pack** is the complete, versioned, manifested input bundle for one LLM call, assembled by
`packages/context` from a **pack template** (per role) against a pinned `(canon_version, spec_version,
bible_version, style_profile_version, template_version)` and a token budget. It is:

- **Deterministic**: same inputs → same bytes → same `pack_hash`.
- **Tiered**: T0 mandatory, T1 critical, T2 relevant, T3 optional (ADR-0010).
- **Manifested**: a JSON manifest lists every included item (kind, id, version, tokens, tier, rank score,
  compression applied) and every dropped item with reason.
- **Validated**: T0 items are re-found byte-for-byte in the rendered prompt; hard requirement IDs are all
  present; style block hash matches; the previous chapter's tail hash matches the accepted version.
- **Cached**: rendered sections cached by content hash; provider prompt caching exploited by ordering
  stable sections first.

Schema: `schemas/context-pack-manifest.schema.json`.

## 2. Pipeline

```
ContractOrTask ─► Query Plan ─► Fetch (structured, lexical, vector, graph) ─► Candidate items
   ─► Rank (per tier rules) ─► Compress (approved compressors) ─► Fit to budget (tier policy)
   ─► Render (role template, section order) ─► Validate ─► Manifest + hash ─► Store ─► Call
```

### 2.1 Query plan derivation (from the chapter contract)
- Entities: participants, mentioned_only, locations, items in state_deltas, abilities in progression.
- Propositions: knowledge_deltas, knowledge_guards, secrets owned by participants.
- Promises: setups/payoffs + all `open` promises whose `due_window` intersects this chapter ±3 or whose
  `related_entities` intersect participants.
- Time: story_time window → events within the arc; last known states before `story_time.start`.
- Keywords: contract text nouns (Korean noun extraction) for lexical search.
- Prior arcs: arcs whose participants intersect ≥ 2 contract participants → L2 summaries.

### 2.2 Fetch (see `05-retrieval-and-indexing.md`)
Structured queries produce **authoritative state** (current facts, knowledge, relationships). Lexical and
vector retrieval produce **relevance candidates** (older events, evidence, summaries). Graph hops expand:
entity → events (last 5 involving each participant pair) → propositions → promises.

### 2.3 Ranking (T2 only)
`score = w_r * relevance(bm25/vector fused via RRF) + w_e * entity_overlap + w_t * temporal_proximity(story
clock distance, decayed) + w_i * importance(item importance: locked/major/minor) + w_p * promise_link +
w_c * contract_keyword_hit`; weights per template version; ties by recency. Items already implied by T1
(e.g., a fact already in the state table) are deduplicated by ID. Diversity: at most 3 items per
(entity, attribute) key; at most 40% of T2 tokens from one source kind.

### 2.4 Compression (approved compressors only)
| Item kind | Compressor | Notes |
| --- | --- | --- |
| Facts/states | table renderer (`인물 · 속성 · 값 · 유효(챕터) · 근거`) | lossless on values |
| Knowledge | stance table | lossless |
| Relationships | pair table with speech level/address terms | lossless |
| Events | one-line `ch.N [frame] 요약` | from stored `summary_ko`; no LLM at pack time |
| Previous chapter | verbatim tail (never compressed) + stored L1 summary | tail length configurable (default 2,000 chars) |
| L2/L3 summaries | stored tiers; choose lowest tier that fits | never generated at pack time |
| Evidence spans | quote trimmed to ≤ 240 chars around the fact | quote boundaries at sentence edges |
| Style block | compiler with role budget | never truncated (compile error instead) |
No LLM call is made during assembly (determinism, cost); all summaries are precomputed at commit time.

### 2.5 Budget fitting
Budget per role (Standard tier, e.g., writer 24k tokens input): T0 first (must fit or `PACK_T0_OVERFLOW`
error → operator must raise budget/model), T1 next (compress via cheaper renderers; if still over, error
`PACK_T1_OVERFLOW` — never drop silently; the template may define a T1 **degradation ladder**, e.g., previous
chapter tail 2,000 → 1,200 chars, knowledge table limited to contract propositions + secrets only), T2 fill
by rank, T3 if room. Token counting uses the target model's tokenizer when available, else a calibrated
Korean estimator (chars × 0.7 ± margin); manifest records both counts.

### 2.6 Rendering
Section order (writer pack) — chosen to maximize provider prefix caching and recency of the most
constraining content:
1. System preamble (role, output schema)
2. `<<STYLE>>` block (stable per project)
3. Story Spec hard requirements + content restrictions (stable)
4. L4 series summary (stable-ish)
5. Bible slice: participants (identity + speech profile digest), locations, glossary slice
6. Arc plan + minor arc beats
7. Canon state tables: participant states, knowledge, relationships, promises due, timeline position
8. Retrieved older canon (T2), each with `ch.N` and evidence quote
9. Previous chapter: L1 summary, then **verbatim tail**, then ending hook
10. Chapter Contract (full) + scene plan (for writer: the current scene highlighted; previous drafted scenes
    of this chapter included verbatim — job-scoped exception to the accepted-only rule)
11. Task instruction + `STYLE_TAIL` + output schema reminder

Untrusted text (imported feedback/documents) never appears in writer packs; where used (planner soft
signals) it is wrapped `<<UNTRUSTED>>…<<END UNTRUSTED>>` with a data-role label.

### 2.7 Validation (pre-call)
- All T0 item IDs present; hard requirement texts byte-equal to spec version.
- `style_block.hash` equals compiled hash; header present in prompt.
- Previous chapter tail hash equals `manuscript_versions.content_hash`-derived slice hash.
- No item from disallowed sources (quarantine tables, non-accepted versions except current job scenes,
  plan items outside the `[예정]` section).
- Manifest token totals ≤ budget.
Failures raise before the call; the job retries assembly once with the degradation ladder, then
`needs_attention`.

## 3. Templates (MVP set)

| Template | Role(s) | T0 | T1 | T2 | Budget (Standard) |
| --- | --- | --- | --- | --- | --- |
| `pack.series_architect` | series_architect | spec (all), planner block, concept | — | — | 8k |
| `pack.arc_planner` | arc_planner | spec hard/soft, planner block, blueprint, season | prior arc L2s, promise ledger (open), protagonist state & progression, cast summary | events of last arc (T2) | 14k |
| `pack.chapter_planner` | chapter_planner | spec hard, planner block, arc plan, contract slot | previous chapter L1 + hook, states/knowledge/relationships for arc participants, promises due, cadence stats last 10 chapters | related older events | 14k |
| `pack.scene_planner` | scene_planner | contract, planner block | previous chapter tail (short), states/knowledge for participants, speech pairs | — | 10k |
| `pack.scene_writer` | scene_writer | as §2.6 | as §2.6 | as §2.6 | 24k (input) |
| `pack.line_editor` | line_editor | editor block, contract shape fields, glossary slice | chapter text (full), speech digests | — | 16k |
| `pack.reviser` | style/dialogue/continuity revisers | editor block, span ± context, issues, must-preserve facts | speech digests for speakers in span | — | 6k |
| `pack.continuity_checker` | continuity_checker | chapter text (paragraph IDs), contract, states/knowledge/relationships/timeline for participants (with evidence quotes), locked facts | retrieved older events/facts by contract entities (T2) | — | 20k |
| `pack.knowledge_leak_checker` | knowledge_leak_checker | chapter text, knowledge table, guards, secrets | — | — | 14k |
| `pack.style_judge` | style_judge, voice_judge | judge block, chapter text, lint report, speech digests (voice) | voice exemplars (voice judge) | — | 14k |
| `pack.extractor` | extractor_a/b | chapter text, glossary/entity registry, contract hypotheses (labelled), pre-pass annotations | — | — | 18k |
| `pack.adjudicator` | extraction_adjudicator | conflicting items, spans ± context | — | — | 6k |
| `pack.summarizer` | summarizer_l1/l2/l3 | summarizer_min block, text or child summaries, glossary | — | — | 12k |

## 4. The previous chapter (special treatment)

For chapter k the pack contains, from chapter k−1's **accepted** version only: (a) L1 summary (≤ 350 chars),
(b) the **last 2,000 characters verbatim** (sentence-aligned; extended backward to the start of the last
scene if that is < 3,000 chars), (c) the recorded `ending_hook` (from k−1's contract/ evaluation), (d) the
state/knowledge/relationship deltas committed from k−1 (so "what just changed" is explicit), (e) elapsed
story time between k−1 end and k start from the contract. If chapter k−1 is not accepted (batch with
review pending), chapter k cannot start (FR-7.13). For k=1, (b) is replaced by the concept's ch.1 hook plan.

## 5. Caching and deduplication

- Section-level cache keyed by content hash (style block, spec block, bible slice, L4 summary).
- Provider prompt caching: stable sections first; the manifest records `cache_prefix_hash` so cost
  accounting can attribute cached tokens.
- Cross-call dedup within a chapter job: scene-writer calls for scenes 2..n reuse identical sections 1–8;
  only sections 9–11 change. Evaluators reuse chapter text as a shared cached section where the provider
  supports it.

## 6. Versioning

Template versions are immutable; changing weights, sections, or degradation ladders creates a new version
and runs the retrieval regression tests (`docs/07-quality/01-testing-strategy.md` §Retrieval). Every call
records `pack_id`, `pack_hash`, `template_version`.

## 7. Failure handling

| Failure | Handling |
| --- | --- |
| Retrieval store timeout | retry ×2; fall back to structured-only T2 (flag `degraded_retrieval` in manifest; evaluators run with full pack later so misses are caught) |
| Embedding service down | lexical + structured only; degraded flag |
| T0 overflow | error → job `needs_attention` with actionable message (e.g., contract too long, too many hard requirements → suggest consolidation) |
| Missing previous chapter acceptance | job waits (Temporal signal) or fails fast per batch policy |
