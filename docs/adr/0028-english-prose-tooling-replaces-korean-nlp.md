# ADR-0028: English prose tooling replaces the Korean NLP sidecar

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
ADR-0017 planned a Python sidecar for Korean morphological analysis (sentence-final endings, honorific
morphemes, Korean tokenization). Under ADR-0026 manuscripts are English; Korean morphology cannot apply to
them.

## Decision
Remove the Korean NLP sidecar from the architecture. Add `packages/prose` (TypeScript): deterministic
output-language identification, English Prose Lint (EP-*), translation-like syntax markers, dialogue
register check (RG-*) against register digests, naming/terminology registry enforcement, the length model,
and code-point addressing utilities. An **optional** self-hosted English grammar/spelling service
(LanguageTool-class, `services/grammar-service`) may feed `EP-GRM-01`; when disabled, heuristics and the
Prose Judge cover grammar. English full-text search uses PostgreSQL's `english` configuration plus a
per-project thesaurus for registry names/terms.

## Consequences
Supersedes ADR-0017. Removes a service from the deployment; Phase 0/1 backlog items replaced (B-0-8 →
prose package; B-1-4 → register check on English). Korean-language register accuracy tests are replaced by
English register-rendering tests.
