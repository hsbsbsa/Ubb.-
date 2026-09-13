# ADR-0005: Fail-closed Style Guard on every style-sensitive call

- **Status:** Superseded by ADR-0027
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

> **Superseded.** The guard now requires both an English Output-Language Contract and a Korean-webnovel Narrative-Tradition Contract; the 'Style Block' is the Narrative Identity Block. Kept for history.

## Context
Previous attempts lost the Korean-webnovel instruction after the first call. A prompt-level convention is
not enforceable across dozens of roles and prompt versions.

## Decision
Mark roles as **style-sensitive** in the registry. The gateway **rejects** any style-sensitive request that
lacks a valid, current Style Block reference embedded in the prompt (`STYLE_BLOCK_MISSING/STALE/NOT_EMBEDDED`)
and records the style profile version and block hash on every call.

## Alternatives considered
- Convention in prompt templates — silently drifts.
- Post-hoc style judge only — detects but does not prevent.

## Consequences
Impossible to forget Korean style at generation time; requires the compiler to be deterministic and fast;
non-style roles are explicitly exempt.
