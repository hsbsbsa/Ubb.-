# Korean Lint Rules

Deterministic checks implemented in `packages/korean` (tokenization, morphology via sidecar) and
`packages/style` (rules, thresholds). All rules emit `Violation { rule_id, severity, span, message_ko,
metric_value, threshold }`. Severity defaults come from the bound Style Profile; thresholds are per
profile version. Character counting per ADR-0024 (NFC code points including spaces).

## 1. Preprocessing

1. NFC normalize; strip markup (chapter headers, 상태창 blocks parsed separately as `system_blocks`).
2. Segment paragraphs (blank-line or newline per profile), sentences (Korean sentence splitter tolerant of
   quotes and ellipses), utterances (text within “ ” or ‘ ’ with speaker annotation if present in the
   structured draft).
3. Morphological analysis via sidecar (ADR-0017): POS tags, sentence-final endings, honorific morphemes.
4. Build per-paragraph feature vectors; cache by paragraph hash for incremental re-lint after patches.

## 2. Metric rules

| Rule | Metric | Default warn / fail | Span |
| --- | --- | --- | --- |
| `KL-END-01` Consecutive identical 종결어미 | run length of same ending (normalized: 했다/였다/있었다 grouped as 과거 서술형) | 3 / 4 | sentences in run |
| `KL-END-02` Ending monotony | share of top ending among narrative sentences in a scene | 0.55 / 0.7 | scene |
| `KL-PRO-01` 3rd-person pronoun density | count(그/그녀/그들/그것 as subject/object) per 1,000 chars | 3 / 6 | each occurrence |
| `KL-PRO-02` Sentence-initial 그녀/그 run | consecutive sentences starting with 그/그녀 | 2 / 3 | run |
| `KL-LEN-01` Long sentence | chars per sentence | 90 / 140 | sentence |
| `KL-LEN-02` Long paragraph | chars per paragraph | 180 / 260 (narration); 120 / 180 (dialogue paragraphs) | paragraph |
| `KL-LEN-03` Low rhythm variance | stdev of sentence length within scene below floor | 8 / 5 | scene |
| `KL-DLG-01` Dialogue ratio out of band | share of chars inside dialogue quotes | outside band ±0.05 / ±0.12 | chapter |
| `KL-DLG-02` Adverb-tagged dialogue | share of utterances followed by `[부사] 말했다/대답했다/물었다` | 0.15 / 0.3 | utterance |
| `KL-DLG-03` Tagged attribution ratio | share of utterances with explicit speech tags | 0.25 / 0.4 | chapter |
| `KL-MON-01` Monologue ratio out of band | share of chars in ‘ ’ / marked monologue | band ±0.05 / ±0.12 | chapter |
| `KL-EXP-01` Exposition run | consecutive narration sentences with no action verb/dialogue and ≥1 lore noun | 4 / 7 | run |
| `KL-EXP-02` Lore density | glossary-term introductions per chapter | 6 / 10 | chapter |
| `KL-HOOK-01` Late hook | index of first sentence matching hook features (dialogue, action verb, threat noun, status text) | 5 / 8 | opening |
| `KL-END-03` Weak ending | last paragraph classified `summary_reflection`/`mid_scene_fade` by rule set (no question, threat, decision, reveal, or cut) | warn only → judge confirms | last paragraph |
| `KL-REP-01` Intra-chapter repeated n-gram | 8-gram repeats (excluding names/system text) | 2 / 4 | spans |
| `KL-REP-02` Cross-chapter repeated paragraph | simhash Hamming distance ≤ 6 vs any accepted paragraph | 1 / 1 (fail) | paragraph + matched chapter ref |
| `KL-REP-03` Repeated opening/closing template | ending paragraph n-gram overlap ≥ 0.6 with last 5 accepted chapter endings | warn | last paragraph |
| `KL-SYS-01` 상태창 grammar | block fails overlay grammar (labels, separators, numeric format) | fail | block |
| `KL-SYS-02` 상태창 wall | lines in block > 12, more than once/chapter | warn | block |
| `KL-NAME-01` Glossary spelling | token matches alias-not-canonical or fuzzy variant (Jaro-Winkler ≥ 0.9) of a glossary term | fail | token |
| `KL-NAME-02` Unknown proper noun | capitalized/loanword noun not in glossary appearing ≥ 2 times | warn (extraction may propose new entity) | token |
| `KL-PUNC-01` Quote style | straight quotes, 「」 (unless LN overlay), `"` inside narration | fail | span |
| `KL-PUNC-02` Ellipsis style | `...` or `…` > 2 per paragraph | warn | span |
| `KL-FMT-01` Screenplay/webtoon markers | `S#`, `장면 \d`, `#컷`, `INT.`, `EXT.`, `(내레이션)`, `[대사]` | fail (blocking) | span |
| `KL-FMT-02` Outline markers | markdown bullets/headers inside prose, `1)`, `-` lines | fail | span |
| `KL-LANG-01` English leakage | Latin-script words outside allowed lists (system UI tokens, brand names in glossary) | major | token |
| `KL-LANG-02` Hanja inline | CJK ideographs outside overlay allowances | major | token |
| `KL-LANG-03` LN markers | 「」『』, ー, さん/くん/ちゃん romanized suffixes (~상/~군 as suffix on names), "…!" clusters | major | span |
| `KL-TRN-*` Translation-ese markers | see §3 | per marker | span |
| `KL-LENGTH-01` Chapter length | chars vs target ± tolerance | ±12% warn / ±20% fail | chapter |
| `KL-TRUNC-01` Truncation | ends mid-sentence, unbalanced quotes, missing ending punctuation, generator `finish_reason=length` | fail | end |

## 3. Translation-ese marker set (`KL-TRN-*`)

Each marker: regex/morph pattern, weight, per-1,000-chars threshold contributing to
`translation_marker_rate` (warn 0.8 / fail 1.6) and, for `major`-weighted patterns, an individual violation.

| ID | Pattern (illustrative) | Weight | Note |
| --- | --- | --- | --- |
| TRN-01 | `~에 의해(서)? [동사]` passive agent marker | 1.0 | prefer active |
| TRN-02 | `~할 수 있었다` ×2 within 3 sentences | 0.6 | ability chains ("could") |
| TRN-03 | `그것은 …이었다/였다` sentence-initial `그것은` | 1.0 | "It was…" |
| TRN-04 | `~하는 것을 [동사]` object nominalization chains ≥ 2/sentence | 0.6 | |
| TRN-05 | `~것이다` ×2 consecutive sentences | 0.6 | |
| TRN-06 | `~하기 시작했다` frequency > 3/1,000 | 0.4 | "began to" |
| TRN-07 | `~하지 않을 수 없었다` > 1/1,000 | 0.4 | |
| TRN-08 | `~에도 불구하고` > 1/1,000 | 0.4 | |
| TRN-09 | `~을/를 가지고 있다` for possession of abstract nouns | 0.6 | "have" calque |
| TRN-10 | `~ 중 하나이다/였다` | 0.6 | "one of the" |
| TRN-11 | `나의/너의/그의/그녀의` possessive pronoun before body-part/kin noun (`그의 손`, `그녀의 어머니`) | 0.8 | zero-possessive natural |
| TRN-12 | `숨을 참았다`, `심장이 목까지`, `등골이 서늘` overuse (> 1/chapter for calque idioms list) | 0.5 | idiom calques list maintained per profile |
| TRN-13 | Sentence starting with `그리고/그러나/하지만` > 25% of sentences | 0.4 | |
| TRN-14 | Dialogue tag inversion `"…" 라고 그가 말했다.` with adverb | 0.8 | overlaps KL-DLG-02 |
| TRN-15 | `~ 이상의 어떤 것` / `~ 이상의 무언가` | 0.6 | "something more than" |
| TRN-16 | Long pre-nominal relative clause (≥ 25 chars modifier before head noun) > 3/1,000 | 0.5 | English relative-clause piles |
| TRN-17 | `자신의` repeated as reflexive possessive > 4/1,000 | 0.5 | |
| TRN-18 | Simile marker `마치 … 처럼/같이` > 4/1,000 | 0.3 | metaphor chain proxy |
| TRN-19 | `~이라고 불리는` / `~로 알려진` appositive intros > 2/chapter | 0.5 | Western exposition |
| TRN-20 | `당신` as 2nd-person pronoun in dialogue between characters with known address terms | 1.0 | strong marker unless profile allows (e.g., spouse/로판 formal) |

The list is data (`style-profile.forbidden_patterns` + `lint_thresholds`), not code; changes are profile
versions and go through the prompt/style regression suite (contrast pairs must keep separating).

## 4. Register (speech level / honorific) check — `KL-REG-*`

Pipeline: utterance → speaker & addressee resolution (structured draft annotations first; heuristic
fallback with confidence) → sentence-final ending classification (해라/해/해요/하십시오/하게/하오) →
honorific features (-시-, 님, 께서, 께, 드리다/여쭙다/모시다, 저/제 vs 나/내) → compare with expected
`speech_level(speaker→addressee @ story_time)` from relationship facts + speech profile.

| Rule | Condition | Default severity |
| --- | --- | --- |
| `KL-REG-01` Level mismatch | classified level ≠ expected and utterance not tagged `intentional_shift` | major (blocking if pair is 상급자/왕족 and profile strict) |
| `KL-REG-02` Honorific subject mismatch | -시-/께서 used toward addressee/subject profile marks as non-honored, or missing when required | major |
| `KL-REG-03` Address term mismatch | address term in utterance ∉ allowed terms for pair @ story_time | major |
| `KL-REG-04` Mixed levels in one utterance | 해요 + 해 in same turn without shift tag | minor |
| `KL-REG-05` Self-reference mismatch | 저/제 vs 나/내 inconsistent with level | minor |
| `KL-REG-06` Unresolved speaker | addressee unknown with confidence < 0.6 | note (judge asked to resolve) |

`intentional_shift` tags require a reason code (`anger`, `intimacy_step`, `disguise`, `mockery`,
`public_formality`, `age_reveal`) and the continuity evaluator verifies the reason is supported by the
scene.

## 5. Output & integration

- `LintReport` is stored per manuscript version; metrics feed the scorecard; violations become `Issue`s
  with `source=lint`, `confidence=1.0`.
- Incremental: after a patch, only changed paragraphs ± 1 and chapter-level metrics recompute.
- Thresholds per profile version; the fixture story includes deliberately seeded violations of every rule
  for tests (`docs/07-quality/01-testing-strategy.md` §Korean).
