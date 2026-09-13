# Retrieval and Indexing

## 1. Sources and indexes

| Source (accepted/canonical only) | Index type | Notes |
| --- | --- | --- |
| `facts` | B-tree `(project, entity, attribute, valid_from)`, `(project, timeline, valid_from)`; partial index on `retracted_at_version IS NULL` | authoritative state queries |
| `events` | B-tree `(project, timeline, story_clock)`, GIN on participants array | temporal & participant queries |
| `knowledge_states` | B-tree `(project, knower, proposition, valid_from)` | ledger queries |
| `relationship_states` | B-tree `(project, from, to, valid_from)` | pair queries |
| `promises` | B-tree `(project, status, due_min, due_max)`, GIN on related_entities | due-window queries |
| `search_documents` | `tsvector` (Korean tokens via sidecar morphological analyzer → nouns/verb stems) GIN; `embedding vector(1024)` HNSW (cosine) | over: L1/L2/L3 summaries, event summaries, evidence quotes (≤ 240 chars), proposition statements, entity descriptions |
| `edges` | adjacency `(project, from_kind, from_id, rel, to_kind, to_id)` | graph hops |

Document granularity for `search_documents`: one row per event, per evidence-bearing fact (quote), per L1
summary, per L2/L3 summary, per proposition, per entity description version. Each row carries `story_clock`,
`chapter_no`, `entity_ids[]`, `kind`, `importance`, `canon_version_added`, `manuscript_version_id`.

## 2. Query types

1. **State-at-time** (structured): current facts for entity set at story clock; used for T1. No ranking.
2. **Temporal neighborhood** (structured): events within ±N chapters or the current arc for participants.
3. **Semantic recall** (hybrid): query strings built from the contract (`purpose_ko`, must_happen
   descriptions, proposition statements, promise statements) → BM25 over Korean tokens + vector kNN →
   Reciprocal Rank Fusion → top 60 → ranker (§2.3 of pack assembly).
4. **Graph expansion**: from top items and contract entities: entity→events (last 5 per pair of
   participants), event→propositions, promise→setup events; capped at 40 items.
5. **Evidence fetch**: for each selected fact/event, load evidence quotes (≤ 240 chars trimmed at sentence
   boundaries) from the immutable version.

## 3. Korean tokenization

The sidecar (ADR-0017; Kiwi or MeCab-ko class analyzer) provides morphemes; the lexical index stores
nouns, proper nouns (glossary-aware, so coined terms are single tokens), verb/adjective stems, and
numerals. Glossary aliases are expanded at query time (synonym expansion) so "성검" and "빛의 검" hit the same
item when both are registered aliases. Names are indexed with all aliases.

## 4. Embeddings

Provider-independent embedding role (`embedder`) with a multilingual model good at Korean (candidates
recorded in ADR-0004; the chosen model per environment is configuration). Vector dimension fixed per
project (`embedding_model_version` on rows); model change triggers a re-embedding job (versioned rows
allow coexistence during migration). Embeddings are built **only** from accepted/canonical content at
commit time (post-commit activity).

## 5. Reranking

MVP: deterministic weighted ranker (pack assembly §2.3). Beta: optional cross-encoder reranker (role
`reranker`, cheap model) over top 60 for T2 when the template enables it; A/B measured by retrieval tests.

## 6. Retrieval tests (fixture-driven)

For the fixture story (`docs/07-quality/02-fixture-story.md`), the suite defines **recall targets**: for a
contract at chapter 41 referencing 세라핀's poison scar (established ch.9), the pack must include the
ch.9 fact + evidence; for the reveal in ch.58, the pack must include the `lie` event from ch.23 and the
`believes_false` row. Recall@pack ≥ 0.95 for `core` items; ≥ 0.85 for `major`.

## 7. Failure modes

| Failure | Mitigation |
| --- | --- |
| Alias drift (new nickname not registered) | `KL-NAME-02` unknown proper noun → extraction proposes alias → entity linking improves |
| Embedding model outage | lexical + structured only; manifest flags `degraded` |
| Index lag after commit | commit tx writes `search_documents` rows synchronously (lexical); embeddings async with `embedding_pending` flag; ranker treats pending rows as lexical-only |
| Huge participant sets (academy ensemble) | T1 degradation ladder: full states for POV + top-4 participants, compact rows for others |
