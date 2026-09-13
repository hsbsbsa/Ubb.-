# ADR-0035: Embedding sets are versioned per model with atomic active-set switching

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
pgvector columns have a fixed dimension; embedding providers/models differ in dimension and semantics. A
provider change must not require a destructive migration or mixed-model similarity.

## Decision
Introduce `embedding_sets { model_id, provider, dimension, status }` with embeddings stored per set
(partitioned table keyed by set; each partition's `vector(n)` matches its set's dimension; HNSW per
partition). Exactly one set is active per project. A model change creates a new set, runs an idempotent,
budgeted re-embed job over accepted content, passes the fixture recall test, then flips `active`
atomically; old sets are retired after a grace period. Retrieval never mixes sets.

## Consequences
Slightly more storage during migration; provider independence for embeddings; NFR-F.5 updated.
