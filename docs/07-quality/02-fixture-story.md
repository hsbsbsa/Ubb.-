# Fixture Story — 『두 번째 각성』 (Second Awakening)

An original fixture designed to exercise every subsystem: regression (prior-loop knowledge), hidden
identity, lies and false beliefs, injuries with lasting effects, inventory hand-offs, rank progression,
speech-level changes tied to relationship milestones, a flashback, a dream, a retcon, delayed payoffs,
divergence from the "known future", and deliberate continuity traps. Machine-readable parts live in
`examples/fixture/`. All names, events and prose are original to this repository.

## 1. Premise and spec (abridged)

- **Genre/overlays:** `regression` (primary devices) + `hunter-gate` (primary structure) + light romance
  line (no overlay; soft preference). Rating 15+. Target 180 chapters × 5,500 chars. Ending: 해피엔딩
  (collapse prevented; protagonist recognized but chooses a quiet life with the people he saved).
- **Premise (user, hard):** F급 포터 강도윤은 10년 뒤 「서울 대붕괴」에서 죽던 순간, 각성 측정을 받던 27세의 아침으로
  회귀한다. 그는 대붕괴의 배후 「감시자」가 헌터협회장 윤재경임을 알지만 증명할 수 없다. 조용히 힘을 키우며 붕괴를
  막으려 하지만, 미래는 그가 개입할 때마다 조금씩 어긋나기 시작한다.
- **Hard requirements:** 도윤은 회귀 사실을 58화 이전에 아무에게도 말하지 않는다 · 박무진은 죽지 않는다(1부) · 감시자의
  정체는 120화 전에 공개되지 않는다 · 로맨스는 슬로번(87화 이전 고백/스킨십 금지) · 잔혹 묘사 제한(15세).
- **Soft:** 사이다 위주, 커뮤니티 반응 인터루드 가끔, 유리 중심 코미디 소량.
- **Assumptions (model-inferred, confirmed in fixture):** 등급 체계 F–S, 상태창 없음(헌터 측정기 수치만), 서울 배경,
  마석 경제.

## 2. Cast and speech profiles

| Character | Role | Baseline speech | Address terms (→ target) | Tics / notes |
| --- | --- | --- | --- | --- |
| **강도윤** (27, F→S) | protagonist, regressor | 해요체 default; 반말 to younger; 하십시오체 to 회장/협회장 | →무진: 「아저씨」(ch.1–13) → 「선배님」(ch.14–) · →서하: 「서하 씨」+해요체 (→ 「서하」+반말 from ch.87) · →유리: 「유리」 반말 · →현석: 「최현석 씨」 해요체 (cold) | short sentences; hindsight monologue ‘전에는…’ ≤ 20%; never explains regression aloud before ch.58 |
| **이서하** (24, B→A healer) | deuteragonist; secret P2 owner | 해요체 to all; 반말 only to 유리 (from ch.13) and to 도윤 from ch.87 | →도윤: 「도윤 씨」 → 「도윤」(ch.87) · →무진: 「무진 선배님」 · →현석: 「부길드장님」 | measured, clinical vocabulary; avoids talking about family |
| **박무진** (45, C급 veteran) | mentor | 반말 to 도윤/유리; 하게체 when serious (「자네」); 해요체 to 서하 | →도윤: 「도윤아」/「자네」 · →서하: 「서하 씨」 | gruff; proverbs; after ch.9 walks with a limp (left leg) |
| **최현석** (31, A급, 백야 부길드장) | antagonist; knows P2 from ch.17; liar (P3) | condescending 반말 to 도윤 (ch.1–59) → forced 하십시오체 in public from ch.60 (`public_formality`) ; 해요체 to 서하 (smooth) | →도윤: 「강도윤」/「F급」 → 「강도윤 헌터님」(ch.60+) | polished; never raises voice |
| **한유리** (19, D급 newbie) | comic relief; misunderstanding engine | 해요체 to 도윤/서하 with slips into 반말 when excited (`emotional_outburst`); 반말 to peers | →도윤: 「도윤 오빠」 · →서하: 「서하 언니」 · →무진: 「무진 아저씨」 (must NOT be 반말 — trap T9) | onomatopoeia heavy; believes 도윤·서하 are siblings ch.12–44 |
| **이태산** (63, 백연그룹 회장) | 서하's father | 하십시오체 in public; 해라체 in private to 현석 | — | appears ch.17, 45, 72 |
| **윤재경** (58, 헌터협회장 = 「감시자」) | hidden antagonist (P4) | 하십시오체 public warmth | — | never on-page as 감시자 before ch.120 |
| 정민재 (측정관) | minor | 해요체 | — | ch.1, 8, 20, 35, 58 |

## 3. Propositions and knowledge (core)

| ID | Statement (truth) | Secret owner | Knowledge timeline |
| --- | --- | --- | --- |
| **P1** | 강도윤은 회귀자다 (true) | 도윤 | 도윤 knows (prior_loop_memory) from ch.1; 서하 unaware → suspects ch.31 (sees him predict a gate pattern) → knows ch.58 (told); 무진 suspects ch.52 → knows ch.66; 유리 unaware through S1; 현석 unaware (S1); reader knows ch.1 |
| **P2** | 이서하는 이태산 회장의 사생아다 (true) | 서하 | 서하 knows (owner); 이태산 knows; 현석 knows ch.17 (told by 이태산); reader knows ch.17; 도윤 unaware → knows ch.72 (told by 서하); 유리 unaware |
| **P3** | 강도윤이 레이드 정보를 브로커에게 팔고 있다 (false; lie by 현석) | — | 현석 knows-false (liar) ch.23; 서하 believes_false ch.23 → doubts ch.40 (sees him refuse a broker) → knows-false ch.58; 유리 unaware; reader knows-false (sees 현석's POV ch.23) |
| **P4** | 윤재경 협회장이 「감시자」다 (true) | 윤재경 | 도윤 knows (prior_loop_memory, cannot prove); everyone else unaware until ch.120; reader knows ch.5 (flashback) |
| **P5** | 강남 게이트 브레이크는 3월 14일에 일어나며 사상자 200명 (prior-loop fact; main diverged) | — | 도윤 knows (prior_loop); main-timeline event: 3월 12일, 사상자 12명 (ch.19) → 도윤 `doubts` applicability; `diverged=true` |
| **P6** | 강도윤과 이서하는 남매다 (false; 유리's misunderstanding) | — | 유리 believes_false ch.12 → knows-false ch.44; 도윤/서하 unaware of her belief until ch.30 (comic beat) |
| **P7** | 낡은 나침반은 숨겨진 게이트를 가리킨다 (true) | — | nobody knows until ch.61 (도윤 learns by witnessing); reader suspects from ch.3 hints |
| **P8** | 서하는 대붕괴에서 죽었다 (prior_loop fact) | — | 도윤 knows (prior_loop); dream ch.27 replays it (frame `dream`) — must not become a main-timeline fact (trap T7) |

## 4. State facts with validity (selection)

| Entity | Attribute | Value | valid_from | valid_to | Evidence chapter |
| --- | --- | --- | --- | --- | --- |
| 도윤 | power.rank | F | ch.1 | ch.8 | ch.1 측정 |
| 도윤 | power.rank | E | ch.8 | ch.20 | ch.8 재측정 |
| 도윤 | power.rank | D | ch.20 | ch.35 | ch.20 |
| 도윤 | power.rank | C | ch.35 | ch.58 | ch.35 |
| 도윤 | power.rank | B | ch.58 | (planned A ch.95) | ch.58 |
| 도윤 | inventory.item | 낡은 나침반 ×1 | ch.3 | ch.30 (given to 서하) | ch.3, ch.30 |
| 서하 | inventory.item | 낡은 나침반 ×1 | ch.30 | ch.61 (returned) | ch.30 |
| 도윤 | resource.money | 1억 2천만 원 | ch.15 | ch.16 | ch.15 마석 매각 |
| 도윤 | resource.money | 2천만 원 | ch.16 | … | ch.16 (단검 1억) |
| 도윤 | inventory.item | 강화 단검 | ch.16 | ch.35 (broken) | |
| 도윤 | inventory.item | 흑철 장검 | ch.36 | … | |
| 도윤 | status.injury | 오른쪽 어깨 관통상 | ch.20 | ch.21 (healed by 서하) | |
| 도윤 | status.injury | 갈비뼈 골절 (3주 회복) | ch.35 | ch.38 (advanced heal) | trap T1 at ch.36 |
| 무진 | status.injury | 왼쪽 다리 마수 독 | ch.9 | ch.14 (poison cleared) | **retcon R1**: originally written 오른쪽 |
| 무진 | status.condition | 왼쪽 다리 흉터·절뚝거림 (영구) | ch.14 | null | trap T6 at ch.22 |
| 서하 | power.rank | B | ch.1 | ch.50 | |
| 서하 | power.rank | A | ch.50 | null | |
| 도윤↔서하 | relationship.speech_level | 해요체/「씨」 | ch.10 | ch.87 | trap T13 at ch.42 |
| 도윤↔서하 | relationship.speech_level | 반말/이름 | ch.87 | null | milestone |
| 도윤→무진 | address_term | 아저씨 | ch.1 | ch.14 | |
| 도윤→무진 | address_term | 선배님 | ch.14 | null | |
| 현석→도윤 | speech_level | 반말 | ch.1 | ch.60 | |
| 현석→도윤 | speech_level | 하십시오체 (public) | ch.60 | null | `public_formality` |

## 5. Timeline & frames

- Main timeline `main`, prior loop `prior_loop_1` (divergence: ch.1 measurement morning).
- ch.5: **flashback** to prior loop (frame `prior_loop` + `flashback`): 무진 dies shielding 도윤; 현석 abandons
  the team; 도윤 sees 윤재경 at the collapse epicenter. Facts land on `prior_loop_1`; knowledge for 도윤.
- ch.18–19: **divergence**: 도윤 anonymously tips the 협회 → break occurs early (3월 12일) with 12 casualties.
- ch.27: **dream** (frame `dream`): 서하 dies as in prior loop. Knowledge for 도윤 only (as dream).
- ch.23: **lie** (frame `lie`): 현석 to 서하 about P3.
- ch.61: compass payoff (promise opened ch.3, importance core, due window ch.55–70).
- ch.11: 무진 mentions a daughter he has not seen in years (promise `character_goal`, due ≤ ch.100; planned
  payoff ch.98).

## 6. Continuity traps (seeded into test drafts; expected detections)

| ID | Chapter | Trap | Expected detection (kind, severity) | Expected repair scope |
| --- | --- | --- | --- | --- |
| T1 | 36 | 도윤 fights at full power the day after rib fracture (ch.35) | continuity/injury, major | scene |
| T2 | 40 | 도윤 called 「D급」 (C since ch.35) | continuity/rank, major (deterministic glossary/rank check catches first) | sentence |
| T3 | 47 | 도윤 uses 나침반 (held by 서하 since ch.30) | continuity/inventory, major | paragraph |
| T4 | 29 | 서하 fully trusts 도윤 while `believes_false(P3)` | knowledge/relationship, major | dialogue/scene |
| T5 | 31 | 서하: 「당신이 회귀자라는 걸 알아요」 (only `suspects`) | knowledge_leak, blocking (secret P1) | dialogue |
| T6 | 22 | 무진 runs upstairs without limp | continuity/injury (permanent condition), major | sentence |
| T7 | 28 | narration treats dream (ch.27) death as real | frame error / continuity, blocking | paragraph |
| T8 | 20 | 도윤 recalls 200 casualties "last month" (prior-loop value) as main event | timeline/divergence, major | sentence |
| T9 | 13 | 유리 uses 반말 to 무진 without shift tag | register KL-REG-01, major | dialogue |
| T10 | 16 | dagger costs 2억 while 도윤 has 1억 2천 | continuity/resource, major | sentence |
| T11 | 45 | 유리 references P2 | knowledge_leak, blocking | dialogue |
| T12 | 50 | paragraph duplicated from ch.35 boss entrance | KL-REP-02, major | paragraph |
| T13 | 42 | 도윤·서하 speak 반말 before ch.87 | register/relationship, major (+ hard requirement slow-burn) | dialogue |
| T14 | 61 | compass payoff when ch.3 regenerated without the compass | promise/payoff_without_setup, major | plan |
| T15 | 19 | break dated 3월 14일 with 200 casualties | timeline/divergence vs contract, blocking (contract must_happen: 12명) | paragraph |
| T16 | 9 (rejected draft) | 「도윤의 왼팔이 절단됐다」 | must never appear in canon/summaries/packs/exemplars | isolation test |
| T17 | 55 | screenplay format | KL-FMT-01, blocking | chapter regenerate |
| T18 | 33 | translation-ese (그녀는…/그것은…/~에 의해) ≥ 30% paragraphs | style drift, major → scene repair; post-repair metrics improve | scene |
| T19 | 18 | 측정 수치 lower than ch.17 without explanation | numeric consistency, major | sentence |
| T20 | 58 (extraction) | Extractor A: 서하 `knows` P1; B: `suspects` | reconciliation conflict → adjudicator picks `knows` with quote 「……회귀자였군요.」 | — |
| T21 | 60 | 현석 keeps 반말 in public after ch.60 milestone | register (expected 하십시오체), major | dialogue |
| T22 | 44 | 유리's misunderstanding resolved but extraction omits knowledge change | extraction recall test (B must catch; reconcile single-source ≥ 0.8) | — |

### Retcon / correction / rollback cases
- **R1 (retcon):** after ch.30 accepted, user retcons ch.9: injured leg 오른쪽 → 왼쪽. Expected: new version;
  fact `무진.status.injury` re-extracted with new evidence; dependents stale: ch.14, 22 (limp descriptions),
  contracts 31–36 referencing the injury; MVP lists them; Beta proposes patches.
- **C1 (correction):** user corrects 유리's age 19 → 20 via canon inspector; impact report lists ch.12 (intro)
  and speech-profile note; commit `source=user_correction` with justification.
- **RB1 (rollback):** rollback of ch.44's commit reopens `유리 believes_false(P6)`; ch.44 returns to
  `approved`; contracts 45–50 stale.

## 7. Prose samples (original; for exemplars and contrast pairs)

### 7.1 Native webnovel register (target) — ch.1 opening (excerpt)
```
측정기가 울었다.

[F]

붉은 글자가 떴다. 십 년 전과 똑같은 글자였다.

“F급이네요. 포터 등록 창구는 왼쪽입니다.”

측정관이 다음 사람을 불렀다. 도윤은 손바닥을 내려다봤다. 떨리지 않았다. 떨릴 이유가 없었다. 이 손이 어디까지 갈
수 있는지, 이 방 안에서 아는 사람은 자기 하나뿐이었으니까.

‘삼월 십이일.’

강남. 그 전에 끝내야 할 일이 세 개였다.
```

### 7.2 Translated-feel contrast (same content; must score lower)
```
측정기는 소리를 냈고, 그것은 F라는 붉은 글자를 표시했다. 그것은 그가 십 년 전에 보았던 것과 정확히 동일한 글자였다.
“당신은 F급입니다. 포터 등록을 위한 창구는 왼쪽에 위치해 있습니다.” 측정관은 조용히 말했다. 그는 그의 손바닥을
내려다보았다. 그의 손은 떨리지 않았다. 그는 이 손이 어디까지 갈 수 있는지를 아는 유일한 사람이었기 때문에, 그는
떨릴 이유를 가지고 있지 않았다. 그는 삼월 십이일에 대해 생각하기 시작했다. 그것은 강남이었다. 그것 이전에 그에
의해 끝내져야만 하는 세 가지 일들이 있었다.
```
Expected lint: TRN-03 ×3, TRN-01, TRN-09, TRN-06, KL-PRO-01 fail, KL-DLG-02, KL-END-01. Judge nativeness
gap ≥ 40 points.

### 7.3 Register sample — 유리 → 무진 (correct) vs trap T9
```
(correct) “아저씨, 저 이거 들어도 돼요? 우와, 진짜 무거워요!”
(trap)    “아저씨, 나 이거 들어도 돼? 우와, 진짜 무겁다!”     ← KL-REG-01 (해체 toward elder without shift tag)
```

### 7.4 Milestone sample — 도윤 → 서하 (ch.86 vs ch.88)
```
ch.86  “서하 씨, 무리하지 마요.”
ch.88  “서하, 무리하지 마.”
```
Register checker must accept both given `relationship.speech_level` validity (ch.87 boundary).

## 8. Chapter map (season 1, abridged)

| Arc | Chapters | Objective | Key commits |
| --- | --- | --- | --- |
| 1 측정실의 F급 | 1–8 | hide, re-enter as porter, meet 무진, compass, flashback, hidden feat, E rank | P1 knowledge; compass promise; prior_loop facts (ch.5) |
| 2 독안개 던전 | 9–20 | 무진 poisoned/healed; 서하 & 유리 join; P6 misunderstanding; 마석→단검; 현석 learns P2; 강남 divergence; D rank | injuries, inventory, money, P2 knowledge (현석/reader), divergence event |
| 3 백야 길드 | 21–35 | shoulder wound/heal; 현석's lie; dream; compass to 서하; boss fight (rib, dagger broken, C) | lie/believes_false; dream frame; inventory transfer; injuries; rank |
| 4 균열 | 36–48 | 장검; recovery; 서하's doubt; P6 resolved; 현석 leverages P2 | doubts; knows-false(P6) |
| 5 진실의 대가 | 49–60 | 서하 A; truth exposed (P3 false; P1 told to 서하); 도윤 B; 현석 public formality | knows(P1) 서하; knows-false(P3); rank; register milestone |
| S2 opener | 61 | compass payoff | promise paid |

Detailed contract example: `examples/fixture/chapter-contract.ch12.json`. Canon delta example (ch.9):
`examples/fixture/canon-delta.ch09.json`. Knowledge ledger excerpt: `examples/fixture/knowledge-ledger.json`.
