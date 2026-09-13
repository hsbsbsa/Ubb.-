# Genre Catalog and Overlays

Each overlay records **abstract conventions** — reader fantasy, structural devices, vocabulary registers,
cadence, typical hooks/endings, taboos — never the plot, characters, or phrasing of any specific work.
Overlays ship in two waves (MVP: first 8; Beta: next 8) and are stored as data conforming to
`schemas/style-profile.schema.json` (`kind: "overlay"`).

Legend for cadence: **P** = progression event (power/rank/skill/asset gain) every N chapters; **C** = 사이다
beat every N chapters; **H** = dominant hook types.

## MVP overlays

### 1. `genre/hunter-gate` — 헌터·게이트
- **Reader fantasy:** rising from the bottom of a ranked society; hidden power revealed; being needed.
- **Vocabulary:** 게이트, 던전, 각성, 각성자, 헌터, 등급(F~S/SS), 마수/몬스터, 마석, 길드, 협회, 레이드, 각성 능력, 스킬,
  상태창(optional), 보스, 브레이크(던전 브레이크). Fixed spellings recorded in glossary at bible time.
- **Devices:** rank reveal scenes; guild/협회 politics; measurement scenes (측정기); auction/마석 economy;
  broadcast/커뮤니티 reactions (게시판/댓글 interludes allowed, formatted as quoted blocks).
- **Cadence:** P=3, C=3. **H:** in_medias_res, status_update, arrival_of_threat.
- **Taboos to ration:** "측정 오류" cliché more than once; identical "rank shock" reactions.
- **Rubric notes:** action clarity (who/where/what hits), pace over description; community interludes in
  authentic 게시판 register (초성체 sparingly).

### 2. `genre/system-progression` — 시스템·성장
- **Reader fantasy:** legible growth; rules mastered cleverly; numbers going up.
- **Devices:** 상태창 blocks with fixed grammar:
  ```
  [상태창]
  이름: 한서준 / 레벨: 12 / 직업: 검사
  힘 14  민첩 11  체력 13
  스킬: 검격 Lv.3, 회피 Lv.2
  ```
  System messages in `[ ]` with present tense (`[퀘스트가 갱신되었습니다.]`); consistent bracket style;
  numbers tracked as facts (extraction rule: any 상태창 number is a fact with validity).
- **Cadence:** P=2, C=3. **H:** status_update, sharp_dialogue.
- **Rubric notes:** avoid 상태창 walls (> 12 lines) more than once per chapter; system voice consistent.

### 3. `genre/regression` — 회귀
- **Reader fantasy:** foreknowledge used decisively; regret repaired; enemies pre-empted.
- **Devices:** hindsight monologue (‘전생에서는…’), "회귀 전" vs "회귀 후" clearly signposted; countdown to
  known events; divergence tracking (prior-loop facts vs current). **Knowledge architecture matters most
  here**: only the regressor knows prior-loop facts (frame `prior_loop`), and every deviation from the
  known future becomes a canonical event on the `main` timeline.
- **Cadence:** P=3, C=2 (early 사이다 heavy). **H:** continue_cliffhanger, in_medias_res.
- **Taboos:** monologue dumps of the entire previous life; "I remember everything" repetition each chapter.
- **Rubric notes:** hindsight monologue ≤ 20% of a chapter; verify each foreknowledge claim exists in
  `prior_loop` frame canon.

### 4. `genre/modern-fantasy` — 현대 판타지 (현판)
- **Reader fantasy:** competence rewarded in contemporary Korean society; social mobility; recognition.
- **Vocabulary:** contemporary Korean institutions, workplace ranks (사원/대리/과장/팀장/이사), 재벌/대기업
  structures, media/커뮤니티; realistic currency (억/만 원).
- **Devices:** news/커뮤니티 reaction interludes; contracts/negotiations as set pieces.
- **Cadence:** P=4, C=3. **H:** sharp_dialogue, arrival_of_threat.
- **Rubric notes:** workplace speech levels are strict (직급 호칭); avoid Western corporate calques.

### 5. `genre/murim` — 무협·무림
- **Reader fantasy:** mastery through discipline; 강호 honor and rivalry; hidden master revealed.
- **Vocabulary:** 무공, 내공, 기혈, 경지(삼류/이류/일류/절정/초절정/화경/현경/생사경 — scheme chosen per project),
  문파, 세가, 마교, 정파/사파, 검법/도법/장법, 비급, 단전, 운기조식. Hanja allowed in technique names on first
  mention (e.g., 파천검법(破天劍法)).
- **Speech:** 하오체/하게체 among 강호 peers, 존대 to 장로/사부; address terms 소협/대협/선배/사형/사매/장문인.
- **Devices:** technique-naming in fights; 비급 discovery; 강호 rumor scenes; tournaments (비무대회).
- **Cadence:** P=4, C=3. **H:** in_medias_res, arrival_of_threat.
- **Taboos:** anachronistic modern vocabulary; fantasy terms (마나, 스킬).

### 6. `genre/romance-fantasy` — 로맨스 판타지 (로판)
- **Reader fantasy:** being chosen/seen; agency inside a rigid society; slow-burn tension and payoff.
- **Vocabulary:** 황실/공작가/후작/영애/영식/각하/폐하/전하, 사교계, 데뷔탕트, 마탑, 신전. Address conventions strict
  (영애 → 공녀 vs 영애 by rank scheme chosen per project).
- **Speech:** 하십시오체/해요체 in society; shifts to 반말 as intimacy milestones (tracked as relationship
  facts with validity!).
- **Devices:** ball/tea scenes; letter exchanges; misunderstanding beats with dual-POV knowledge (the
  knowledge ledger must hold reader-knows/heroine-doesn't states); internal monologue heavier (ratio band
  0.15–0.35).
- **Cadence:** P (relationship milestone) = 4, C=4. **H:** emotional_peak, reveal, sharp_dialogue.
- **Rubric notes:** emotional interiority natural, not essayistic; avoid Western Regency calques
  ("the ton", curtsy descriptions) — render Korean 로판 society register.

### 7. `genre/villainess` — 악녀
- **Reader fantasy:** rewriting a doomed role; competence and wit; turning the narrative.
- **Devices:** possession/regression into the villainess (combine with `possession`/`regression` overlays);
  "original story (원작)" knowledge as `prior_loop`-like frame `source_story` (treated as prior_loop);
  divergence tracking; social duels in dialogue.
- **Cadence:** C=3 (verbal 사이다), relationship P=4. **H:** sharp_dialogue, reveal.
- **Rubric notes:** dialogue wit and register precision dominate; the heroine's inner voice consistent
  (often 반말 monologue vs formal speech).

### 8. `genre/academy` — 아카데미
- **Reader fantasy:** hidden talent among elites; rivalry → respect; exam/tournament set pieces.
- **Vocabulary:** 입학, 학년, 실기, 이론, 교수/교관, 기숙사, 학생회, 실습, 순위표, 결투/대련.
- **Speech:** 선배/후배 hierarchy; 존댓말 to 교수; peer 반말 by year; address terms by year/rank.
- **Devices:** ranking boards (formatted like 상태창), exam arcs (3–6 chapters), ensemble cast management
  (participant sets larger → context pack must handle 8–10 participants).
- **Cadence:** P=3, C=3. **H:** status_update, sharp_dialogue.

## Beta overlays

### 9. `genre/possession` — 빙의
- Body/identity separation: `knowledge` ledger must model the possessor's outside knowledge (frame
  `source_story` or `prior_life`) vs the body's original memories (may be partial → `forgot`/`unaware`).
- Devices: identity-slip risk scenes; "원래 몸의 주인" backstory reveals; address-term confusion beats.

### 10. `genre/reincarnation` — 환생
- Previous-life expertise (frame `prior_life`, knower = protagonist only); age/register mismatch comedy
  (an adult mind in a child's body: speech level tension is a feature; register checker needs the
  `intentional_shift` flag frequently).

### 11. `genre/dungeon` — 던전
- Floor/level structure; resource management; party dynamics; map/inventory tracking facts; boss cadence
  P=2.

### 12. `genre/apocalypse-survival` — 아포칼립스·생존
- Resource ledger (food, ammo, medicine as inventory facts), injury realism (injury facts must have healing
  timelines), shelter/location facts; grim register but webnovel pacing; C=3 via competence payoffs.

### 13. `genre/management` — 경영·기업
- Numbers as facts (revenue, share, ranks); negotiation set pieces; 회장/대표/본부장 hierarchy; media
  interludes; P=4 (business milestone).

### 14. `genre/idol-entertainment` — 아이돌·연예계
- Stage/broadcast scenes; fan reaction interludes (댓글/SNS register with strict sanitization if imported);
  chart/ranking facts; group speech dynamics (멤버 간 호칭/반말/존댓말 by age).

### 15. `genre/game-world` — 게임 세계
- Game rules as world rules (locked facts); UI text conventions; NPC/player distinction in speech.

### 16. `genre/comedy` — 코미디 (secondary overlay)
- Misunderstanding engine requires knowledge ledger (who believes what); punchline placement rules (end of
  paragraph; 1–2 per scene); no explaining the joke; running gags tracked as promises with `gag` type.

## Later refinements (Production)
- `mode/character-drama` (interiority band up, cadence relaxed, still serial hooks).
- `mode/slow-burn-romance` (relationship milestone cadence 6–8; tension beats every 2 chapters; strict
  "no accidental early confession" as a forbidden development template).

## Combination guide

| Combination | Primary | Notes |
| --- | --- | --- |
| 회귀 + 헌터 | hunter-gate | regression devices layer on hunter cadence; prior-loop knowledge heavy |
| 빙의 + 악녀 + 로판 | romance-fantasy | villainess devices; source_story frame |
| 아카데미 + 시스템 | academy | ranking boards + 상태창 share formatting grammar (must not collide: compiler warns) |
| 무협 + 회귀 | murim | hindsight monologue in 무협 register |
| 현판 + 경영 | modern-fantasy | numbers-as-facts rules |

Unknown combinations compile with a manifest warning and require explicit approval in the bible gate.
