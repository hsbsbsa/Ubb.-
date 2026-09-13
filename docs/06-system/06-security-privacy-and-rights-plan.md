# Security, Privacy, and Rights Plan

## 1. Threat model (summary)

Assets: unpublished manuscripts, story bibles, prompts, provider keys, user identities, cost budgets.
Adversaries: external attackers (API/web), malicious tenants (cross-tenant access), malicious imported
content (prompt injection via reader comments/documents), insider misuse, provider-side data retention.

## 2. Authentication & authorization

- Email magic-link + OAuth (Google/GitHub/Kakao/Naver in Beta for Korean users); sessions in secure,
  httpOnly, SameSite cookies; API keys (hashed) for automation with scoped permissions.
- RBAC: `owner` (billing, members, deletion, provider settings), `editor` (all story operations),
  `viewer` (read-only inspectors/exports if allowed). Per-project overrides in Beta.
- 2FA optional (Beta), enforced for owners in Production.

## 3. Workspace isolation

- Every tenant table has `workspace_id`; Postgres RLS with `app.workspace_id` set per transaction; API and
  workers use a role without `BYPASSRLS`. Migrations run with a separate role.
- Object storage keys prefixed by workspace; signed URLs short-lived.
- Temporal workflow IDs include workspace; activities re-check ownership before writes.
- Tests: cross-tenant read/write attempts return 0 rows / 403.

## 4. Secrets & encryption

- Secrets (provider keys, DB creds, KMS key refs) in the cloud secret manager; injected as env at boot;
  rotated; never logged. `.env.example` lists names only.
- TLS 1.2+ everywhere; DB and object storage encrypted at rest; **application-level envelope encryption**
  for manuscript text, prompts/outputs archives, and imported documents with per-workspace data keys
  (KMS); key deletion = crypto-shredding for workspace deletion.

## 5. Provider privacy controls

- Provider allowlist per workspace; default only providers with no-training/zero-retention terms.
- Region pinning where offered; per-workspace opt-in for additional providers.
- Payload minimization: packs contain only what the role needs; user identity never sent; project titles
  replaced by IDs in prompts.
- Provider request IDs stored for audit/dispute.

## 6. Prompt-injection & untrusted content

- Untrusted sources: imported reader comments, uploaded documents, web text. Pipeline: virus scan →
  text extraction → NFC → `instruction_injection_classifier` → wrapped `<<UNTRUSTED>>` in user role only →
  never in writer packs → outputs of calls consuming untrusted text are schema-validated and can only
  produce *soft signals* or *proposals* requiring human confirmation.
- Requirements/directions typed by users are also screened (meta-instruction detection) because they are
  interpolated into prompts; flagged items need confirmation.
- Model outputs are data: never executed, never used to construct prompts for other calls without schema
  validation.

## 7. Audit logging

User actions (approve/reject/override/correct/retcon/lock/export/delete/member changes/provider settings)
and system actions (commits, rollbacks) in append-only `audit_log` with actor, target, payload hash;
exportable per workspace.

## 8. Data retention, deletion, backup, recovery

- Retention defaults: manuscripts/canon indefinitely while project exists; llm_calls payloads 180 days
  (configurable; metadata kept); quarantine drafts 90 days; logs 30 days.
- Deletion: project delete → soft delete (30-day grace) → hard delete + crypto-shred; workspace delete
  same; deletion receipts in audit log.
- Backups: daily snapshots (MVP), PITR ≤ 5 min (Production); quarterly restore drills; object storage
  versioning.
- Export: full project export (manuscripts, canon JSON, spec, bible, plans) on demand — also the user's
  portability guarantee.

## 9. Copyright & rights safeguards

- **No scraping** of commercial webnovels; no "in the style of <author/work>" instructions; forbidden by
  policy and by the exemplar provenance requirement (ADR-0025).
- Exemplar sources: project-generated, user-owned (rights confirmation checkbox + record), licensed
  (license reference stored), studio synthetic (reviewed).
- **Similarity screening** (Beta): n-gram/simhash and embedding similarity against user-provided reference
  corpora and, optionally, an external screening service; flagged passages go to review.
- Trope-level conventions are unprotectable ideas; the genre overlays deliberately record abstract
  conventions only.
- Name collision check: generated character/organization names checked against a project-scoped list
  and, optionally, user-provided avoid-lists.

## 10. AI-assistance disclosure & platform policy

- Export options: disclosure text templates (Korean), per-platform policy presets configurable by the user
  (the studio does not assert what any platform requires; it records the user's choice).
- Provenance record per chapter: models used, human edits count, acceptance actor — available for the
  user's own disclosures.

## 11. Application security

- Input validation via JSON Schema; output encoding; CSRF for cookie sessions; rate limiting per user/IP;
  dependency scanning; SAST; secrets scanning in CI; container images minimal; least-privilege DB roles;
  WAF in Production.
- Security tests in CI (`docs/07-quality/01-testing-strategy.md` §Security).
