# ADR-0011: Hybrid retrieval: structured + lexical + vector + graph

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Vector search alone misses exact entity/time constraints and registry names/terms; structured queries alone
miss thematic relevance.

## Decision
T1 state comes from **structured** bitemporal queries (authoritative). T2 recall uses **BM25 over English
tokens** (registry-aware thesaurus) fused with **pgvector kNN** via RRF, expanded by **graph hops** (entity→event→
proposition→promise), then ranked deterministically with diversity caps. Evidence quotes are fetched
verbatim from immutable versions.

## Alternatives considered
- Vector-only RAG — fails on ranks/dates/inventory specifics.
- Full-text only — misses paraphrase.

## Consequences
English full-text configuration plus per-project thesaurus; embeddings versioned per model (ADR-0035);
recall tests on the fixture.
