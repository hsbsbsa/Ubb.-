# ADR-0010: Tiered, manifested, deterministic context packs

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Token limits force trimming; trimming must never drop hard requirements, style rules or critical canon.
Calls must be reproducible and auditable.

## Decision
Assemble packs from role templates with four tiers: T0 mandatory (never trimmed; overflow = error),
T1 critical (compress only via approved lossless renderers; degradation ladder; never dropped), T2 relevant
(ranked, truncated), T3 optional (dropped first). Packs are pure functions of pinned inputs, manifested,
hashed, cached, validated byte-for-byte for T0 before the call. No LLM calls during assembly.

## Alternatives considered
- Single relevance ranking over everything — can drop hard requirements.
- Sending the whole manuscript — impossible at scale; cost.

## Consequences
Precomputed summaries at commit time; template versioning with retrieval regression tests.
