# ADR-0002: Postgres 16 + pgvector as the single system of record

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Canon commits must be atomic across facts, events, knowledge, relationships, promises, summaries and
search documents. Retrieval needs lexical and vector search. Splitting truth across a graph DB, a vector DB
and a relational DB would make atomic commits and bitemporal queries hard.

## Decision
Use **Postgres 16** as the only system of record: relational canon tables with bitemporal columns,
`tsvector` lexical search fed by the Korean sidecar tokenizer, **pgvector** (HNSW) for embeddings, adjacency
tables for graph hops, RLS for tenancy. Object storage holds large payloads/exports only.

## Alternatives considered
- Dedicated vector DB + Postgres — two-phase consistency problems; more ops.
- Graph DB for entities/events — attractive for hops but breaks single-transaction commits.

## Consequences
Simple atomicity; one backup/restore story; must watch index sizes at 3,000-chapter scale (partitioning
planned in Production).
