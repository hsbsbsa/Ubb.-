# ADR-0027: Fail-closed Narrative Identity Guard requiring both contracts

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
ADR-0005 introduced a fail-closed gateway guard for a Korean "Style Block". Under ADR-0026 the block must
carry two independent contracts, and the failure of either one produces a different, unacceptable output.

## Decision
The gateway **Narrative Identity Guard** rejects any style-sensitive call unless the request references a
compiled Narrative Identity Block whose manifest includes **both** a valid Output-Language Contract hash
(English) **and** a valid Narrative-Tradition Contract hash (Korean webnovel), the block hash matches the
compiler output for the pinned identity version/role/budget, and the block header is embedded in the
prompt. Error codes: `NARRATIVE_IDENTITY_MISSING`, `OUTPUT_LANGUAGE_CONTRACT_MISSING`,
`TRADITION_CONTRACT_MISSING`, `NARRATIVE_IDENTITY_STALE`, `NARRATIVE_IDENTITY_NOT_EMBEDDED`,
`OUTPUT_LANGUAGE_UNSUPPORTED`. Every call records the identity version, block hash and both contract
hashes. Manuscript-producing roles additionally pass a post-call deterministic output-language check.

## Consequences
Supersedes ADR-0005. The compiler must expose contract hashes separately; the audit record gains two
fields; the prompt regression suite includes the output-language check.
