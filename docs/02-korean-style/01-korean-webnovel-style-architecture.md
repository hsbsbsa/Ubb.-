# Korean Webnovel Style Architecture

## 1. Problem statement

A model asked once to "write a Korean webnovel" drifts back toward its dominant prior — Anglophone literary
fiction — within a few thousand tokens, and completely once the instruction is several calls upstream. The
observed failure modes:

| Drift type | What it looks like | Korean term |
| --- | --- | --- |
| Translation drift | 그/그녀 as sentence subjects every sentence; "~에 의해" passives; "~할 수 있었다" chains; "그것은 …이었다"; calqued idioms ("숨을 참았다", "심장이 목까지 올라왔다"); "~라고 그는 말했다, 조용히" adverb-tagged dialogue | 번역투 |
| Western exposition drift | Multi-paragraph scene-setting before any hook; landscape description; encyclopedic world lore in narration; interiority as essay | 서술 과잉 |
| Literary-register drift | Metaphor chains, nested clauses, long paragraphs, omniscient reflective narration | 문어체 과잉 |
| Format drift | Screenplay (`장면 1. 실내. 밤`), webtoon script (`#컷`), bullet-point outlines instead of prose, English section headers | 형식 이탈 |
| Register drift | Wrong speech level for the pair/context; honorific misuse; address term inconsistency (형 → 오빠 for a male speaker) | 존칭/화계 오류 |
| Voice drift | All characters speak alike; character tics vanish | 캐릭터 어조 붕괴 |
| Genre drift | Hunter fiction without status windows/rank vocabulary; 로판 without title/address conventions; 무협 with fantasy vocabulary | 장르 관습 이탈 |
| Serial drift | No episode hook, no local payoff, no cliffhanger; chapters end mid-scene without tension | 연재 구조 붕괴 |
| Light-novel drift | Japanese LN mannerisms (ー, 「」 quoting, honorific suffixes like -san/-kun, ellipsis-heavy reactions) unless requested | 라노벨 모사 |

The architectural answer has four parts: **(A)** a structured, versioned **Style Profile**; **(B)** a
compiled **Style Block** that is mandatory on every style-sensitive call, enforced by a gateway **Style
Guard**; **(C)** three-layer **detection** (deterministic lint, morphological register check, model-based
judge with evidence); **(D)** **passage-level repair** with regression tests. Style is also fed into
**planning** (hooks, cadence, dialogue density targets) so that structure, not just wording, is Korean.

## 2. Style Profile (data)

Schema: `schemas/style-profile.schema.json`. A profile is composed at bind time:

```
StyleProfile(project) = compose(
  base:      "kr-webnovel-base@vX",          # universal Korean webnovel rules
  overlays:  ["genre/hunter-gate@vY", "genre/regression@vZ", ...],   # ordered; later wins on conflict
  overrides: project_overrides                # user preferences, numeric targets, forbidden patterns
)
```

Contents (all fields typed; free text kept short and imperative, in Korean where it is a rule about Korean):

1. **Identity** — id, version, base/overlay lineage, content hash.
2. **Prose rules (문장 규칙)** — sentence length target & variance; paragraph length (mobile: 1–3 sentences
   typical, max ~120 chars per paragraph for dialogue-heavy passages, ~200 for narration); sentence-ending
   variety rule (no more than 2 consecutive identical 종결어미; ratio limits for ~했다/~였다); pronoun policy
   (3rd-person pronouns 그/그녀 ≤ N per 1,000 chars; prefer name/role/zero-anaphora); tense/aspect defaults
   (past narration, present for 상태창/system); punctuation conventions (Korean quotation marks “ ” for
   dialogue, ‘ ’ for thought; ellipsis as … not ...; dash usage; no English brackets in narration unless
   system text).
3. **Dialogue rules (대화 규칙)** — dialogue ratio target band; short exchanges; minimal attribution tags;
   reaction beats interleaved; honorific/speech-level policy delegates to speech profiles; onomatopoeia
   allowances by genre; internal monologue formatting (‘ ’ or bare line) and ratio band.
4. **Structure rules (구조 규칙)** — chapter opening: hook within first 3–5 sentences (continuation from
   previous cliffhanger or immediate scene tension); scene count band (2–4 per 5,500 chars); local payoff
   requirement (each chapter delivers ≥1 of: 사이다, 정보 공개, 감정 진전, 성장 확인); ending: cliffhanger or
   strong forward pull; cadence targets (progression event every K chapters; 사이다 beat frequency).
5. **Exposition rules (설명 규칙)** — max consecutive exposition sentences; world info only through action/
   dialogue/status text unless in a designated 설정 설명 slot; ban "as you know" dialogue; lore density per
   chapter band.
6. **Genre conventions (장르 관습)** — from overlays: vocabulary registers (헌터/게이트/각성/상태창; 무협 technique
   nomenclature and 강호 address terms; 로판 titles 영애/공작/폐하), structural devices (상태창 formatting, 시스템
   메시지, 회귀 hindsight monologue patterns), reader-fantasy emphasis, taboo clichés to avoid overusing.
7. **Forbidden patterns (금지 패턴)** — regex/lexical lists for translation-ese markers, LN markers, screenplay
   markers, English leakage; each with severity.
8. **Exemplars (예문)** — references to exemplar bank entries by function tag (hook, action, banter, 상태창,
   emotional beat, cliffhanger); only project-generated/user-owned/licensed/synthetic sources
   (ADR-0025).
9. **User preferences (사용자 취향)** — numeric overrides (e.g., `dialogue_ratio.target = 0.45`), textual
   preferences with priority, forbidden expressions list.
10. **Judge rubric (평가 기준)** — the rubric dimensions and anchors the Style Judge uses for this profile
    (so judge and writer share definitions).
11. **Lint thresholds (검사 임계값)** — per-metric warn/fail thresholds derived from base + overlay.

Profiles are **versioned & immutable**; a project binds a profile version; changing overrides creates a new
version. Every call records the version it used.

## 3. Style Block (compiled prompt artifact)

`compileStyleBlock(profile, role, budgetTokens, exemplarSelection) → { text, hash, manifest }`

- Deterministic (same inputs → same bytes) so it is **provider-cache-friendly** and hashable.
- Role variants:
  - `writer_full` (~900–1,400 tokens): rules 2–7 in imperative Korean, 2–4 exemplars, "금지" list.
  - `editor_full` (~700–1,000): rules 2–3, 5, 7 emphasized; exemplar pairs (bad→good).
  - `planner_compact` (~250–400): structure rules 4, genre conventions 6, cadence targets.
  - `judge_rubric` (~500–800): rubric 10 + forbidden patterns 7 + thresholds 11, no exemplars (to reduce
    self-preference toward exemplar phrasing).
  - `summarizer_min` (~120): name/term spellings + register notes only (summaries are not prose but must
    keep Korean canonical names).
- Placement: **immediately after the system preamble and before task-specific content**, as a fenced
  section `<<STYLE v=hash>> … <<END STYLE>>`; a one-line **reminder** of the top 5 rules is appended after
  the user content as a recency anchor (`STYLE_TAIL`) for writer/editor roles.
- The block includes the **speech profile digest** of participating characters when the call is
  character-aware (writer, editor, voice judge, dialogue reviser).

## 4. Style Guard (enforcement)

Gateway middleware (see `docs/06-system/01-system-architecture.md`):

```
if role.style_sensitive and not request.style_block_ref: reject(STYLE_BLOCK_MISSING)
if request.style_block_ref.hash != compile(profile_version, role, budget).hash: reject(STYLE_BLOCK_STALE)
if role.style_sensitive and prompt_text does not contain "<<STYLE v="+hash: reject(STYLE_BLOCK_NOT_EMBEDDED)
record(call.style_profile_version, call.style_block_hash)
```

Style-sensitive roles (must carry a block): scene planner, hook/ending planner, scene writer, chapter
assembler, line editor, style reviser, dialogue reviser, continuity reviser (because it rewrites prose),
style judge, voice judge, pacing judge, chapter summary writer (min variant), title generator, candidate
comparator for prose. Non-style-sensitive (no block; guard skips): requirement interpreter, extraction
roles, evidence verifier, classification roles, cost estimator.

This makes the Korean requirement **structurally impossible to forget**: a call cannot be executed without
it, and the audit record proves which version was present.

## 5. Detection: three layers

### 5.1 Deterministic Korean Lint (`packages/korean`, `packages/style`)

Runs in milliseconds on every draft, patch, and accepted text. Metrics and default thresholds are in
`04-korean-lint-rules.md`. Categories: ending repetition, pronoun density, translation-ese markers,
sentence/paragraph length distribution, dialogue & monologue ratios, adverb-tagged dialogue rate,
exposition run length, English/Hanja/LN/screenplay leakage, punctuation conventions, glossary spelling,
status-window format validity, repeated n-grams (intra-chapter and vs. accepted corpus).

Output: `LintReport { metrics, violations[] }` where each violation has span offsets → directly patchable.

### 5.2 Register check (morphological)

Uses the Korean NLP sidecar (ADR-0017) to segment utterances, identify speaker/addressee (from dialogue
attribution heuristics + writer-emitted **speaker annotations** in the structured draft), classify
sentence-final speech level (하십시오/해요/해/하게/하오/해라) and honorific markers (-시-, 님, 께서, 드리다/
여쭙다 lexicon), then compare against the **speech profile + relationship state at the story time**.
Deviations not marked `intentional_shift` (writers can flag deliberate register changes in the scene
metadata, and evaluators confirm they are motivated) become issues with severity by profile.

### 5.3 Style Judge (model-based, evidence-bound)

Prompt family `style_judge@v` with `judge_rubric` block. Input: chapter (or scene) text with paragraph IDs,
genre overlay names, speech profile digests, and the lint report (so the judge focuses on what lint cannot
see). Output schema: per-dimension score 1–5 with ≥1 evidence paragraph ID per score < 4, list of
`StyleIssue { kind, span, quote, why, repair_hint }`, overall `webnovel_nativeness` 0–100, and a
`drift_flags[]` from the drift taxonomy. Anti-bias measures: the judge never sees exemplars; scores are
calibrated against a **contrast-pair set** (native-webnovel vs translated-feel versions of the same
content; studio-authored) with a target Spearman ≥ 0.8 vs Korean editor rankings; two judge models are
sampled for gate decisions in Premium.

Dimensions: 문장 자연스러움 (native fluency), 번역투 부재, 서술 밀도/설명 통제, 대화 자연스러움 & 화계 정확성, 리듬
(sentence/paragraph rhythm, mobile readability), 연재 구조 (hook, local payoff, ending pull), 장르 관습 적합성,
캐릭터 어조 일관성 (voice judge shares this), 클리셰 남용.

## 6. Repair: passage-level, regression-tested

Issues (lint + register + judge + continuity) are **clustered by span**. For each cluster the reviser gets:
style block (`editor_full`), speech profile digests of speakers in the span, the span ± 1 paragraph, the
issue list with repair hints, hard constraints (facts in the span that must not change; glossary
spellings), and a length budget (± 15% of span). It returns a replacement for exactly the span (structured:
`{span_id, new_text, changed_claims[]}`). The patch is applied to create a new manuscript version; lint +
register check re-run on the patched region + neighbors; the continuity checker re-runs **only if**
`changed_claims` is non-empty or the span contains fact-bearing sentences (detected by the extraction
pre-pass); a whole-chapter style smoke check runs after ≥3 patches or any scene-level patch.

Escalation: if the same span fails twice → scene-level rewrite with the scene plan; if a chapter has > 40%
of paragraphs flagged → chapter-level regeneration (rare; counts against candidate budget).

## 7. Style in planning (structure is style too)

The `planner_compact` block feeds: arc planner (사이다 cadence, progression event cadence), chapter contract
writer (hook type from allowed set, local payoff type, ending type, dialogue density target, scene count
band), scene planner (scene-level beats with 감정선/정보/사이다 tags; POV; opening beat type). Contract fields
`hook`, `local_satisfaction`, `ending_state`, `dialogue_density_target`, `scene_count` are validated
against the profile's structure rules deterministically before drafting.

## 8. Learning without imitation (ADR-0025)

- **Project exemplar bank**: after acceptance, passages that scored ≥ 4.5 on the style judge and were not
  patched are tagged by function and become eligible exemplars (max 12 per function; rotated by recency and
  score). This is the strongest anchor: the model imitates *this project's* approved voice.
- **User-owned/licensed exemplars**: uploaded with rights confirmation and provenance; tagged manually.
- **Synthetic studio exemplars**: authored for the base/genre overlays (short, original, no named
  characters from real works), reviewed by Korean editors.
- **Editor feedback**: reviewer edits on accepted chapters are diffed; systematic changes (e.g., shorten
  paragraphs) propose numeric override updates (Beta: semi-automatic; MVP: manual).
- **Forbidden**: scraping commercial webnovels, named-author "in the style of" instructions, storing
  commercial text as exemplars.

## 9. Metrics that prove it works

- `style.nativeness_score` distribution per project and per chapter (target median ≥ 80/100).
- `lint.translation_marker_rate` (per 1,000 chars; target ≤ 0.8 in base profile).
- `register.violation_rate` (per 100 utterances; target ≤ 1).
- `style.patch_rate` (share of paragraphs patched for style; falling trend expected as exemplar bank grows).
- Human editor spot checks: monthly sample of 30 chapters, blind 1–5 "reads native" rating; target ≥ 4.0 mean.
