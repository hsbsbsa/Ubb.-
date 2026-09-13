# Character-Knowledge Architecture

## 1. Why a ledger, not a summary

Regression, possession, hidden identity, mystery, political intrigue, romance misunderstandings, and
misunderstanding comedy all depend on *who knows what, when, and how confidently*. Free-text summaries
cannot answer "does Seo-ha know that Do-yoon is the regressor as of chapter 88?" reliably. The knowledge
ledger makes this a query.

## 2. Model (ADR-0008)

### 2.1 Propositions
`propositions { id, project_id, statement (English), kind: identity|event|location|ability|intent|relationship|
world_rule|secret|other, truth: [{ timeline_id, value: true|false|unknown, valid_from?, valid_to? }],
linked_fact_ids[], linked_event_ids[], secret: { owner_ids[], allowed_knower_ids[], reveal_plan_ref? } | null,
created_in (chapter/commit) }`.

**Truth is per timeline** (ADR-0031): a proposition has one truth entry per timeline it is asserted on
(e.g., "the Gangnam break kills 200 people" is `true` on `prior_loop_1` and `false` on `main`); a timeline
without an entry inherits from its parent timeline up to the divergence point. Truth entries carry
validity so a proposition can become true later in story time ("Seo-ha is A-rank").

Propositions are **canonical statements** — atomic, entity-linked, written in English working text.
Extractors propose new propositions; reconciliation deduplicates by embedding + entity-overlap +
adjudication.

### 2.2 Knowers
`knowers`: any character entity, plus two pseudo-knowers per project: `narrator` (what the narration has
stated on the page) and `reader` (what the reader can infer; ≥ narrator; includes dramatic-irony items).
Multi-POV stories: the reader knows the union of all POVs' revealed information.

### 2.3 Knowledge states (bitemporal)
```
knowledge_states {
  id, project_id, timeline_id, knower_id, proposition_id,
  stance: knows | suspects | believes_false | pretends | unaware | forgot | doubts,
  believed_value?,             -- for believes_false: what they think instead (English working text)
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
- `believes_false` — holds a wrong value (`believed_value`) — the misunderstanding engine.
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
explicit constraints ("Seo-ha does not yet know Do-yoon is a regressor. Do not let her speak or act as if
she does."); the
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
  require "reader knows, heroine does not" states (romance-fantasy misunderstanding beats).

## 5. Uses in the pipeline

| Consumer | Query |
| --- | --- |
| Chapter contract validation | Every `knowledge_delta` from→to stance is legal (e.g., `unaware → knows` requires a channel in the contract's scenes; `knows → unaware` illegal except `forgot` with mechanism) |
| Context pack (T1) | For each participant: stances on all contract propositions + all secrets they are guarded from + top-K recent knowledge changes; rendered as a compact table: `character · proposition · stance · evidence (chapter)` |
| Writer prompt | Explicit "knows / unaware / believes falsely / suspects" lists per participant (English); guards as hard prohibitions |
| Leakage checker | For each utterance/action by character X referencing proposition P where X is `unaware/believes_false`, flag `knowledge_leak` with span + ledger row evidence |
| Misunderstanding comedy / romance | `believes_false` rows with `believed_value` are surfaced to writer as the engine of the scene; resolution requires a channel event |
| Regression | `prior_loop_memory` source rows for the regressor; `diverged` flag computed when a proposition's `main` truth differs from its `prior_loop` truth; writer receives a "what has changed since the first life" list |
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
| Character learns a lie and believes it | `believes_false` with `believed_value` = lie content; liar `knows` truth; `lie` event links both |
| Character suspects a lie | `doubts` on the false proposition + `suspects` on the true one |
| Two characters share a secret; one tells a third off-page (mentioned later) | extraction on the later chapter creates `knows` with `source.kind=told`, `event` = new off-page event with frame `canonical` and `story_clock` approximate (precision `approx`) — allowed but flagged `retroactive_channel` for review |
| Amnesia | `forgot` rows closing prior `knows`; recovery creates new `knows` with channel `remembered` |
| Regressor's foreknowledge proves wrong | prior_loop fact remains on its timeline; main-timeline fact differs; ledger keeps `knows` (prior-loop) + `doubts` on applicability; `diverged=true` surfaced |
| Reader-only knowledge (dramatic irony) | `reader.knows`, all characters `unaware` — leakage checker protects it |
| Narrator unreliable (rare; must be a spec requirement) | narrator stance `believes_false` allowed only if spec flag `unreliable_narrator=true` |
