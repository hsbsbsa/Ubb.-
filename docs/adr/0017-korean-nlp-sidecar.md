# ADR-0017: Korean morphological analysis via a versioned sidecar

- **Status:** Superseded by ADR-0028
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

> **Superseded.** Manuscripts are English (ADR-0026); Korean morphological analysis does not apply. Replaced by English prose tooling.

## Context
Deterministic lint and register checks need sentence-final ending classification, honorific morphemes and
Korean tokenization; LLM-only checks are non-deterministic and costly.

## Decision
Run a Python sidecar (Kiwi preferred; MeCab-ko fallback) exposing analysis endpoints; pin analyzer
version; cache results by text hash; glossary terms registered as user-dictionary entries for
tokenization.

## Alternatives considered
- LLM-based register classification — non-deterministic, expensive.
- Rule-only regex — insufficient for honorific morphology.

## Consequences
Extra service; accuracy tests on a labeled set; user dictionary sync per project.
