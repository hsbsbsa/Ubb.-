# Character-Knowledge Architecture

## 1. Why a ledger, not a summary

Regression, possession, hidden identity, mystery, political intrigue, romance misunderstandings, and
misunderstanding comedy all depend on *who knows what, when, and how confidently*. Free-text summaries
cannot answer "does 서하가 know that 도윤 is the regressor as of chapter 88?" reliably. The knowledge ledger
makes this a query.

## 2. Model (ADR-0008)

### 2.1 Propositions
`propositions { id, project_id, statement_ko, kind: identity|event|location|ability|intent|relationship|
world_rule|secret|other, truth_value: true|false|unknown (objective, per timeline), linked_fact_ids[],
linked_event_ids[], secret: { owner_ids[], allowed_knower_ids[], reveal_plan_ref? } | null, created_in
(chapter/commit) }`.

Propositions are **canonical statements** — atomic, entity-linked, Korean. Extractors propose new
propositions; reconciliation deduplicates by embedding + entity-overlap + adjudication.

### 2.2 Knowers
`knowers`: any character entity, plus two pseudo-knowers per project: `narrator` (what the narration has
stated on the page) and `reader` (what the reader can infer; ≥ narrator; includes dramatic-irony items).
Multi-POV stories: the reader knows the union of all POVs' revealed information.

### 2.3 Knowledge states (bitemporal)
```
knowledge_states {
  id, project_id, timeline_id, knower_id, proposition_id,
  stance: knows | suspects | believes_false | pretends | unaware | forgot | doubts,
  believed_value_ko?,          -- for believes_false: what they think instead
  pretend_target_ids[]?,       -- for pretends: toward whom
  certainty 0..1,
  source: { kind: witnessed|told|inferred|read|prior_loop_memory|source_story|overheard|deduced|assumed,
            event_id?, informer_id?, chapter_id, evidence_span_ids[] },
  valid_from StoryClock, valid_to StoryClock|null,
  asserted_at_version, retracted_at_version, commit_id
}
```
Stance semantics:
- `knows` — has the true value (or false value if proposition truth is false and they know it is false).
- `suspects` — considers it likely; certainty < threshold.
- `believes_false` — holds a wrong value (`believed_value_ko`) — the misunderstanding engine.
- `pretends` — publicly acts as if a stance they do not hold (`pretend_target_ids`), with true stance in a
  linked row.
- `unaware` — explicit record that a character does **not** know (used for secrets; absence of a row is
  also unaware but explicit rows enable guards and UI clarity).
- `forgot` — previously knew; memory lost (amnesia, possession partial memory).
- `doubts` — knew/believed, now questioning.

A character can have multiple rows per proposition over time (validity intervals) — that is the history.

### 2.4 Secrets and guards
A proposition with `secret != null` has an owner and an allowed knower set at the current story clock.
`knowledge_guards` on a chapter contract list `(character, proposition)` pairs that **must remain
non-knowing** through this chapter (unless the contract plans a reveal). The writer receives guards as
explicit constraints ("서하는 아직 도윤이 회귀자임을 모른다. 이를 아는 듯 말하거나 행동하게 하지 마라"); the
leakage checker verifies utterances/actions against them; extraction verification blocks a `knows` stance
without a channel event.

## 3. Channels: how knowledge changes

Every stance change must cite a **channel**: a canonical event in which the knower witnessed, was told,
read, overheard, inferred (from listed premises), remembered (prior loop), or a plan-frame event realized in
this chapter. The extractor's schema requires `source.kind` and, for `told`, an `informer_id` present in the
scene. Deterministic verification: the informer and knower share a scene (participants at the same
location/story clock) or the channel is remote (letter/message/broadcast) with an event of that type.

## 4. Deriving reader and narrator knowledge

- `narrator.knows(P)` when P is stated in narration or shown on-page.
- `reader.knows(P)` ⊇ narrator; plus items the text makes inferable by dramatic irony (extractor marks
  `reader_infers=true` with evidence). The reader knower supports **dramatic irony checks**: contracts can
  require "reader knows, heroine does not" states (로판 misunderstanding beats).

## 5. Uses in the pipeline

| Consumer | Query |
| --- | --- |
| Chapter contract validation | Every `knowledge_delta` from→to stance is legal (e.g., `unaware → knows` requires a channel in the contract's scenes; `knows → unaware` illegal except `forgot` with mechanism) |
| Context pack (T1) | For each participant: stances on all contract propositions + all secrets they are guarded from + top-K recent knowledge changes; rendered as a compact table: `인물 · 명제 · 상태 · 근거(챕터)` |
| Writer prompt | Explicit "알고 있음 / 모름 / 오해 중 / 의심 중" lists per participant; guards as 금지 |
| Leakage checker | For each utterance/action by character X referencing proposition P where X is `unaware/believes_false`, flag `knowledge_leak` with span + ledger row evidence |
| Misunderstanding comedy / romance | `believes_false` rows with `believed_value_ko` are surfaced to writer as the engine of the scene; resolution requires a channel event |
| Regression | `prior_loop_memory` source rows for the regressor; `diverged` flag computed when main-timeline facts contradict prior-loop facts; writer receives "회귀 전과 달라진 점" list |
| Possession | possessor's `source_story` knowledge vs body's `forgot`/partial memories; identity-slip risk guard |
| Mystery/intrigue | suspects/doubts progression per faction character; planner uses ledger to schedule reveals |
| UI knowledge matrix | propositions × knowers with "as of chapter k" slider |

## 6. Extraction rules for knowledge (summary for extractor prompt design)

1. Emit a knowledge item when the text shows a character learning, inferring, misunderstanding, suspecting,
   forgetting, lying (→ speaker `knows` truth + `lie` event), pretending, or being told something.
2. Cite `paragraph_id` + quote for each item.
3. If a character *acts* on information without an on-page channel, emit `implied_knowledge` with
   `confidence ≤ 0.6` — verification will demand a channel or flag a leak; do not upgrade to `knows`.
4. Never emit knowledge for characters not present or not reached by a remote channel.
5. For narration-only reveals, emit `narrator.knows` and `reader.knows`.
6. For dreams/predictions/hypotheticals, emit knowledge for the experiencer with the proper frame.

## 7. Edge cases

| Case | Handling |
| --- | --- |
| Character learns a lie and believes it | `believes_false` with `believed_value_ko` = lie content; liar `knows` truth; `lie` event links both |
| Character suspects a lie | `doubts` on the false proposition + `suspects` on the true one |
| Two characters share a secret; one tells a third off-page (mentioned later) | extraction on the later chapter creates `knows` with `source.kind=told`, `event` = new off-page event with frame `canonical` and `story_clock` approximate (precision `approx`) — allowed but flagged `retroactive_channel` for review |
| Amnesia | `forgot` rows closing prior `knows`; recovery creates new `knows` with channel `remembered` |
| Regressor's foreknowledge proves wrong | prior_loop fact remains on its timeline; main-timeline fact differs; ledger keeps `knows` (prior-loop) + `doubts` on applicability; `diverged=true` surfaced |
| Reader-only knowledge (dramatic irony) | `reader.knows`, all characters `unaware` — leakage checker protects it |
| Narrator unreliable (rare; must be a spec requirement) | narrator stance `believes_false` allowed only if spec flag `unreliable_narrator=true` |
