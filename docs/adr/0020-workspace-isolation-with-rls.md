# ADR-0020: Workspace isolation with Postgres RLS and envelope encryption

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Unpublished manuscripts are commercially sensitive; multi-tenant SaaS is a likely deployment.

## Decision
`workspace_id` on every tenant table with **RLS** policies; app roles without BYPASSRLS; per-workspace data
keys (KMS envelope) for manuscript/prompt payloads; provider allowlists per workspace; append-only audit.

## Alternatives considered
- Application-level filtering only — one bug leaks data.
- Database-per-tenant — heavy ops for many small tenants.

## Consequences
Generated RLS isolation tests; key management runbooks.
