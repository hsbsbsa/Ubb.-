# Style Profile Specification

Normative companion to `schemas/style-profile.schema.json`. Describes the base profile
`kr-webnovel-base`, how overlays compose, how overrides work, and the compile rules for Style Blocks.

## 1. Base profile: `kr-webnovel-base@1`

The base encodes conventions shared across Korean serialized web fiction irrespective of genre. Values are
defaults; overlays and overrides adjust them.

### 1.1 Prose (`prose`)

| Key | Default | Notes |
| --- | --- | --- |
| `sentence_length.target_chars` | 28 | mean Korean characters per sentence (incl. spaces) |
| `sentence_length.max_chars` | 90 | longer sentences flagged (warn) |
| `sentence_length.variance` | `high` | rhythm: alternate short punches with mid-length sentences |
| `paragraph.max_sentences` | 3 | mobile readability |
| `paragraph.max_chars` | 180 | narration; dialogue paragraphs shorter |
| `paragraph.single_line_ok` | true | one-sentence paragraphs encouraged for emphasis |
| `ending_variety.max_consecutive_same` | 2 | e.g., ~했다 ×3 in a row = violation |
| `ending_variety.max_ratio_single` | 0.55 | share of any single 종결어미 among narrative sentences |
| `pronoun.third_person_per_1000` | 3 | 그/그녀/그들 as subject/object; zero-anaphora or names preferred |
| `pronoun.forbid_그녀_as_default_subject` | true | 그녀 is a strong translation marker when habitual |
| `tense.narration` | `past` | ~했다 default; present allowed in 상태창/system/inner speech |
| `quotes.dialogue` | `“ ”` | never straight `" "` |
| `quotes.thought` | `‘ ’` | or bare line with 내면 독백 markers per overlay |
| `ellipsis` | `…` | not `...`; ≤ 2 per paragraph |
| `english_leakage` | `forbid` | except system UI text allowed by overlay |
| `hanja_inline` | `forbid` | except 무협 overlay allowances |

### 1.2 Dialogue (`dialogue`)

| Key | Default |
| --- | --- |
| `ratio.band` | 0.35–0.55 (share of characters inside dialogue quotes) |
| `attribution.max_tagged_ratio` | 0.25 (share of utterances with explicit "~라고 말했다"-style tags) |
| `attribution.forbid_adverb_tags` | true (e.g., "조용히 말했다" chains) |
| `reaction_beats` | `interleave` (action/expression beat between utterances) |
| `monologue.ratio.band` | 0.08–0.25 |
| `monologue.format` | `‘ ’` |
| `onomatopoeia` | `moderate` |
| `speech_level_policy` | `from_speech_profiles` (never guess) |

### 1.3 Structure (`structure`)

| Key | Default |
| --- | --- |
| `chapter.hook_within_sentences` | 5 |
| `chapter.opening_types_allowed` | `continue_cliffhanger`, `in_medias_res`, `sharp_dialogue`, `status_update`, `time_skip_with_tension` |
| `chapter.forbid_opening_types` | `weather_landscape`, `lore_dump`, `waking_up_routine` |
| `chapter.scene_count.band` | 2–4 per 5,000–6,000 chars |
| `chapter.local_payoff.required_any_of` | `사이다`, `정보_공개`, `감정_진전`, `성장_확인`, `유머_포인트` |
| `chapter.ending_types_allowed` | `cliffhanger`, `reveal`, `decision`, `arrival_of_threat`, `emotional_peak`, `quiet_ominous` |
| `chapter.ending.forbid` | `mid_scene_fade`, `summary_reflection` |
| `cadence.progression_event_every_chapters` | 4 (overlay adjusts) |
| `cadence.사이다_every_chapters` | 3 |
| `cadence.max_고구마_streak` | 3 |
| `exposition.max_consecutive_sentences` | 4 |
| `exposition.lore_via` | `action`, `dialogue`, `status_text` (narration allowed in flagged 설정 slot ≤ 1 per chapter) |

### 1.4 Forbidden patterns (`forbidden_patterns`)

Categories with severity: `translationese` (major), `light_novel` (major unless overlay allows), `screenplay`
(blocking), `english_leakage` (major), `stale_cliches` (minor). The concrete regex list lives in
`04-korean-lint-rules.md` §3 and is versioned with the profile.

### 1.5 Judge rubric (`rubric`)

Nine dimensions (see architecture §5.3) with 1–5 anchors written in Korean. Example anchor for 번역투 부재:
5 = "번역투 표지가 전혀 없고 주어 생략과 어순이 자연스럽다"; 3 = "간헐적 대명사 주어·피동 표현이 눈에 띈다"; 1 =
"문장마다 '그/그녀'가 주어이고 영어식 어순·관용구 직역이 반복된다".

## 2. Overlays

Overlay = partial profile that **patches** the base (JSON Merge Patch semantics; arrays replaced unless key
ends with `+` for append). Overlays are ordered by the project's genre list; later overlays win on scalar
conflicts, and the compiler records conflicts in the manifest. Each overlay includes:

- `vocabulary` (register lists: preferred terms, discouraged terms, fixed spellings)
- `devices` (structural devices, formatting rules, e.g., 상태창 block grammar)
- `conventions` (reader fantasy emphasis, cadence overrides, POV norms, typical hook/ending types)
- `taboos` (over-used clichés to ration)
- `rubric_notes` (genre-specific judge guidance)
- `lint_thresholds` (overrides)

The 16 shipped overlays are described in `03-genre-catalog.md`. Combination rules: at most 3 overlays; a
`primary` overlay sets structure defaults; secondary overlays contribute vocabulary/devices. Known-good
combos are listed; unknown combos compile with a warning and require bible approval.

## 3. Project overrides

- Numeric overrides on any thresholded key (validated against min/max sanity ranges).
- `preferences[]`: `{ text_ko, priority: must|prefer, scope: all|dialogue|narration|structure }` — rendered
  into the block under 사용자 취향 with must-items first.
- `forbidden_expressions[]`: exact strings or regex, project-specific (e.g., avoid "씩 웃었다" overuse).
- `exemplar_policy`: functions to include, max count, min score, allow_user_exemplars.
- `speech_defaults`: fallback speech level between unknown pairs (default 해요체 between adults of unknown
  relation; overlay may change, e.g., 무협 → 하오체 among 강호 peers).

## 4. Compile rules (Style Block)

1. Header line `<<STYLE v=<hash> profile=<id>@<ver> role=<role>>>`.
2. Sections in fixed order: 핵심 원칙 (5 bullets max), 문장, 대화, 구조 (role-dependent), 설명, 장르 관습, 금지,
   예문 (writer/editor only), 사용자 취향, 참여 인물 화법 (if participants given).
3. Rendering is table-free Korean bullets; numeric targets appear as concrete instructions ("한 문단은 세
   문장을 넘기지 않는다").
4. Exemplars: selected deterministically by `(function_tag, score desc, recency desc)`, truncated to 300
   chars each, wrapped as `[예문:훅]` … `[/예문]`, never more than `exemplar_policy.max_count`.
5. Budget fitting: sections shed in reverse priority (예문 → 장르 관습 detail → 설명) until under budget;
   핵심 원칙, 금지, 참여 인물 화법 are never shed. If still over budget → compile error (caller must raise
   budget), never silent truncation.
6. `STYLE_TAIL`: for writer/editor roles, the compiler also returns a ≤ 60-token Korean reminder of the
   five 핵심 원칙 to be appended at the end of the prompt.
7. Hash = SHA-256 of the rendered text; manifest lists profile version, overlay versions, exemplar IDs,
   participants' speech profile versions, dropped sections.

## 5. Speech profile digest (참여 인물 화법)

Per participant (max 6; more → pick by contract participants + POV): `이름(호칭 변형) · 기본 화계: 대상별 ·
호칭: 대상별 · 말버릇 · 금지 표현 · 현재 관계 상태에 따른 변화 (e.g., 연인 관계 시작 후 반말 전환 ch.87)`.
Generated from the knowledge/relationship ledgers at the chapter's story time, not from the static bible,
so it reflects current canon.

## 6. Versioning & migration

- Base and overlays are versioned semver-like integers; projects pin versions. A new base version does not
  affect existing projects until the user re-binds (a bible change → gate).
- Compiler output for a given `(profile hash, role, budget, exemplar set)` is cached in `style_block_cache`
  with the hash; cache invalidation on any input change is automatic because the key is the content hash.
