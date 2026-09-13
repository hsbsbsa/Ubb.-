# Operations Runbooks (outline)

The MVP Definition of Done requires these runbooks to exist. This outline fixes their scope so they are
written during Phase 4 alongside the systems they describe.

| Runbook | Trigger | Must cover |
| --- | --- | --- |
| **Deploy** | release | migration order (forward-only; verify on staging fixture DB), prompt-set promotion, routing-table publish, worker rollout with in-flight workflow compatibility (Temporal versioning), smoke test (fixture chapter with ReplayProvider) |
| **Restore** | data loss / corruption | PITR target selection, object storage version alignment, canon-version consistency check (`projects.canon_version` vs `canon_commits`), Temporal namespace state vs DB (rehydrate-from-artifacts), post-restore integrity queries |
| **Secret rotation** | schedule / incident | provider keys (dual-key window), DB credentials, KMS data-key rotation (re-wrap, no re-encrypt), session secret (forced re-login) |
| **Provider incident** | error-rate alert | circuit-breaker status, manual re-route of a class, pausing batches, resuming after recovery, cost reconciliation of duplicate-risk calls |
| **needs_attention triage** | queue growth | classification by failure class; standard actions (retry step, regenerate, accept-with-override, edit manually, raise budget, revalidate contract, review extraction conflicts); escalation to engineering when the same class repeats |
| **Budget & limits** | budget alert / user request | raising limits, per-chapter overrides, verifying reservation leaks (`reserved_cents` vs in-flight calls) |
| **Canon repair** | disagreement spike / user report | reading a chapter's trace, rolling back the latest commit, running correction workflow, regenerating summaries and embeddings for a range, promoting/demoting dependency edges |
| **Output-language incident** | any `EP-LANG-01` failure in production | inspect the call's identity block and contract hashes, confirm the Guard passed, review model/provider, re-route the P-class role, add a regression case |
| **Threshold calibration** | monthly / after reviewer round | run contrast-set calibration, review override clusters, publish a new profile version with `calibration_status`, monitor gates for 48h |
| **Prompt/model change** | new version | regression suite run (incl. five-class contrast sets and output-language assertions), P-class benchmark if a writer model changes, staged promotion, monitoring prose/structure metrics for 24h |
| **Tenant offboarding** | deletion request | soft-delete → grace → hard delete → crypto-shred; audit receipt; export before deletion |
