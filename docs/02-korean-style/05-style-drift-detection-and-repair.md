# Style Drift Detection and Repair

## 1. Detection pipeline (per manuscript version)

```
draft/version text
  │
  ├─► Korean Lint (deterministic)  ───────────────► LintReport (metrics + violations w/ spans)
  ├─► Register Check (morph + ledgers) ──────────► RegisterReport (KL-REG-* w/ spans)
  ├─► Style Judge (LLM, judge_rubric block)  ────► StyleReport (scores, drift_flags, issues w/ spans)
  └─► Voice Judge (LLM; participants' speech profiles + voice exemplars) ► VoiceReport
                                                   │
                                                   ▼
                                Issue merge & span clustering ──► Scorecard.style section
```

- Lint and register run first and their results are **given to the judges** (so judges spend attention on
  what rules cannot see: unnatural collocations, essayistic interiority, Western scene rhythm, humor
  timing).
- Judges are asked to output **evidence paragraph IDs**; issues without a resolvable span are downgraded to
  `note` and cannot block.
- The voice judge gets, per participant, up to 3 **voice exemplars** (accepted utterances with high voice
  score) and the speech profile digest; it flags utterances that "could be anyone" or contradict tics.

## 2. Scoring and gating

`style_score` (0–100) = weighted: judge nativeness 50%, lint composite 25% (1 − normalized violation
density), register 15%, voice 10%. Gate thresholds by quality tier: Economy ≥ 70, Standard ≥ 78,
Premium ≥ 84. Any `blocking` style violation (format drift `KL-FMT-01`, screenplay/webtoon script,
truncation) fails regardless of score. Drift flags of type `translation` or `western_exposition` at judge
confidence ≥ 0.7 across ≥ 30% of paragraphs → `major` chapter-level issue → triggers scene-level repair
plan instead of per-paragraph patches.

## 3. Repair strategy (patch-first)

| Cluster size / kind | Action | Context given to reviser |
| --- | --- | --- |
| Single sentence (ending repetition, pronoun, marker) | `sentence_patch` | editor block, span ± 1 sentence, rule text |
| Paragraph (rhythm, exposition run, adverb tags) | `paragraph_patch` | editor block, paragraph ± 1, speech digests if dialogue |
| Utterance register (KL-REG) | `dialogue_patch` | editor block, utterance + surrounding beats, pair's speech level/address terms at story time, reason if shift allowed |
| Scene-level drift (judge flags ≥ 30% of scene paragraphs) | `scene_rewrite` | writer block, scene plan, previous scene tail, facts-in-scene list (must preserve), length target |
| Chapter-level drift (> 40% paragraphs) or 2 failed scene rewrites | `chapter_regenerate` (counts against candidate budget) | full writer context pack |

The reviser output is structured: `{ span_id, new_text, changed_claims: [...], preserved_facts_ack: [...] }`.
`changed_claims` non-empty → continuity re-check on the span. `preserved_facts_ack` must list every fact ID
supplied as must-preserve; missing acks → patch rejected (cheap deterministic guard).

## 4. Regression testing of patches

After applying patches to create version v+1:
1. Re-lint changed paragraphs ± 1 and chapter metrics.
2. Register check on changed utterances.
3. If any `changed_claims` or fact-bearing span: continuity checker on the changed spans with the delta of
   claims (not the whole chapter).
4. After ≥ 3 patches or any `scene_rewrite`: whole-chapter Style Judge smoke (cheaper model allowed) and
   whole-chapter repetition check (a patch can introduce a repeated phrase).
5. Compare scorecards v vs v+1: **no metric may regress beyond tolerance** (e.g., nativeness −3) and no new
   blocking/major issue; otherwise revert the offending patch and try an alternate repair once, then
   escalate.

## 5. Escalation & human review

- Max style repair rounds per chapter: 2 (Standard), 3 (Premium). Beyond: chapter to review queue with the
  residual style issues, side-by-side of original vs patched, and a "accept with notes" option (records an
  override).
- Every human override is a data point for calibration (see §7).

## 6. Anti-self-preference and position bias

- Judge prompts never include the writer's exemplars; the judge model for gating is by default a **different
  model family** from the writer (routing rule `judge.model != writer.model` when available).
- Pairwise candidate comparisons run both orders; disagreement → third judge or tie → prefer the lower-cost
  candidate (documented in ADR-0015).
- Judges are asked for evidence before scores (evidence-first JSON field ordering) to reduce
  score-then-rationalize behavior.

## 7. Calibration

- **Contrast-pair set**: studio-authored pairs (native webnovel vs translated-feel rendering of identical
  content) across genres; MVP seed ≈ 60 pairs, Beta ≥ 300. The judge must rank the native version higher in
  ≥ 95% of pairs; lint must produce a higher marker rate on the translated version in ≥ 90%.
- **Editor panel**: monthly blind rating of 30 sampled chapters (1–5). Target Spearman ≥ 0.8 between judge
  nativeness and editor ratings; drift of > 0.1 triggers rubric/prompt review.
- **Override analysis**: human overrides of style issues cluster → threshold tuning proposals per profile
  version.

## 8. Failure modes and mitigations

| Failure | Mitigation |
| --- | --- |
| Judge rewards its own dialect (self-preference) | different model family; rubric anchors in Korean; contrast-pair tests |
| Lint false positives in stylized passages (e.g., deliberate repetition for effect) | writer can tag `stylistic_repeat` on a paragraph in the structured draft; tag must be sparse (≤ 2/chapter) and judge confirms |
| Repair introduces contradictions | `changed_claims` → continuity re-check; must-preserve acks |
| Repair loops on the same span | span-level attempt counter; escalate to scene rewrite |
| Genre-specific formats (상태창) trip format rules | system blocks parsed separately before lint |
| Non-Korean input premise leads to English proper nouns | glossary requires Korean canonical spelling at bible time; `KL-LANG-01` allows only glossary-listed Latin tokens |
