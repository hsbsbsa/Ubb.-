# API and Interface Plan

REST over HTTPS, JSON bodies validated against `schemas/`. All routes are workspace-scoped by session/API
key; `X-Workspace-Id` header selects the active workspace. Long operations return a `job` and progress is
streamed via SSE `GET /jobs/{id}/events`. Idempotent mutations accept `Idempotency-Key`.

## 1. Resources

### Projects & spec
| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/projects` | create with intake (schema `story-intake`) → starts RequirementInterpretationWorkflow |
| GET | `/projects/{id}` | project summary, status, canon_version, mode, tier, budgets |
| PATCH | `/projects/{id}` | settings (mode, tier, horizons, length target) |
| GET | `/projects/{id}/spec` | current Story Spec (requirements grouped by kind) |
| POST | `/projects/{id}/spec/assumptions/{reqId}:confirm|edit|reject` | assumption review |
| POST | `/projects/{id}/directions` | add running direction → PlanningHorizon re-plan preview + apply |
| GET | `/projects/{id}/directions` | list |

### Concepts & bible
| POST | `/projects/{id}/concepts:generate` | start ConceptWorkflow (n) |
| GET | `/projects/{id}/concepts` | candidates + comparison |
| POST | `/projects/{id}/concepts/{cid}:select` / `:merge` | |
| POST | `/projects/{id}/bible:generate` | StoryBibleWorkflow |
| GET/PATCH | `/projects/{id}/bible/entities/{eid}` | read/edit entity version |
| POST | `/projects/{id}/bible/facts/{fid}:lock|unlock` | |
| GET/PATCH | `/projects/{id}/bible/speech-profiles/{cid}` | |
| GET/PATCH | `/projects/{id}/style-profile` | overlays, overrides; returns compiled block preview |
| POST | `/projects/{id}/bible:approve` | gate signal |

### Plans
| POST | `/projects/{id}/plans/series:generate` | SeriesPlanningWorkflow |
| GET/PATCH | `/projects/{id}/plans/blueprint` | |
| GET | `/projects/{id}/plans/seasons` / `/arcs` / `/arcs/{aid}` | |
| PATCH | `/projects/{id}/plans/arcs/{aid}` | edit (children stale) |
| POST | `/projects/{id}/plans/arcs/{aid}:approve` / `:regenerate` | |
| GET/PATCH | `/projects/{id}/chapters/{n}/contract` | contract read/edit |
| POST | `/projects/{id}/chapters/{n}/contract:approve` / `:regenerate` | |
| GET | `/projects/{id}/promises?status=` | promise ledger |
| PATCH | `/projects/{id}/promises/{pid}` | reschedule/abandon (reason required) |

### Production
| POST | `/projects/{id}/chapters/{n}:generate` | ChapterProductionWorkflow (options: candidates, tier override) |
| POST | `/projects/{id}/chapters:batch` | `{from, to, gate_policy}` → BatchProductionWorkflow |
| GET | `/projects/{id}/chapters` | list with status, score, spend |
| GET | `/projects/{id}/chapters/{n}` | current versions, scorecard summary |
| GET | `/projects/{id}/chapters/{n}/versions/{vid}` | text + lint + scorecard + issues |
| GET | `/projects/{id}/chapters/{n}/candidates` | comparison view |
| POST | `/projects/{id}/chapters/{n}:approve` | signal (optionally `{version_id}` when candidates) |
| POST | `/projects/{id}/chapters/{n}:request-changes` | `{text_ko}` → patch tasks |
| POST | `/projects/{id}/chapters/{n}:reject` | `{reason}` |
| POST | `/projects/{id}/chapters/{n}/issues/{iid}:override` | `{reason}` |
| POST | `/projects/{id}/chapters/{n}:regenerate` | returns dependency report first (`?dry_run=true`) |
| POST | `/projects/{id}/chapters/{n}:retcon` | `{text_ko?|instruction_ko}` |
| GET | `/projects/{id}/chapters/{n}/trace` | pipeline trace (packs, calls, patches, delta) |

### Canon & inspectors
| GET | `/projects/{id}/canon/facts?entity=&attribute=&at_chapter=&as_of_version=` | |
| GET | `/projects/{id}/canon/events?from=&to=&frame=&entity=` | |
| GET | `/projects/{id}/canon/knowledge?knower=&proposition=&at_chapter=` | matrix |
| GET | `/projects/{id}/canon/relationships?from=&to=&at_chapter=` | |
| GET | `/projects/{id}/canon/timeline` | events on story clock, timelines |
| GET | `/projects/{id}/canon/entities/{eid}/state?at_chapter=` | current state view w/ evidence |
| POST | `/projects/{id}/canon/{kind}/{itemId}:correct` | `{new_value, validity, justification_ko}` → impact report (`dry_run`) then commit |
| GET | `/projects/{id}/canon/commits` / `/commits/{v}` | history, deltas |
| POST | `/projects/{id}/canon/commits/{v}:rollback` | MVP: latest only |
| GET | `/projects/{id}/canon/stale` | stale artifacts with reasons |

### Jobs, costs, exports
| GET | `/projects/{id}/jobs` / `/jobs/{jid}` | |
| POST | `/jobs/{jid}:pause|resume|cancel` | |
| GET | `/jobs/{jid}/events` (SSE) | progress |
| GET | `/projects/{id}/costs?group_by=role|model|chapter` | |
| GET | `/projects/{id}/costs/predict?chapters=` | |
| GET/PUT | `/projects/{id}/budgets` | |
| POST | `/projects/{id}/exports` | `{scope, format, options}` → ExportWorkflow |
| GET | `/projects/{id}/exports/{eid}` | status + signed URL |

### Workspace & admin
| GET/PATCH | `/workspaces/{wid}` | settings incl. provider allowlist, privacy flags |
| GET/POST/DELETE | `/workspaces/{wid}/members` | |
| GET | `/workspaces/{wid}/audit-log` | |
| GET | `/admin/prompt-sets` / `/admin/routing` | (operator) |

## 2. Conventions

- Errors: RFC 9457 problem details with `code` (e.g., `PACK_T0_OVERFLOW`, `BUDGET_EXHAUSTED`,
  `STALE_CANON`, `LEASE_HELD`).
- Pagination: cursor-based.
- Versioned API (`/v1`).
- Webhooks (Beta): `chapter.accepted`, `job.needs_attention`, `budget.threshold`.

## 3. Internal interfaces (TypeScript, in `packages/domain`)

```ts
interface ModelGateway {
  call(req: GatewayRequest): Promise<GatewayResponse>;   // enforces StyleGuard, budgets, schema, audit
}
interface ContextAssembler {
  assemble(input: PackInput): Promise<ContextPack>;      // deterministic; throws PackError
}
interface CanonService {
  extract(versionId): Promise<CanonDeltaCandidates>;     // A ∥ B ∥ prepass
  reconcile(cands): Promise<ReconciledDelta>;
  verify(delta, versionId): Promise<VerifiedDelta>;
  commit(delta, expectedVersion): Promise<CanonCommit>;  // single tx
  impact(itemIds, sinceVersion): Promise<ImpactReport>;
}
interface StyleService { compileBlock(profileVersionId, role, budget, participants?): StyleBlock; lint(text, profile): LintReport; }
interface Evaluator { evaluate(versionId, scope?): Promise<Scorecard>; }
interface Reviser { patch(versionId, issueCluster): Promise<PatchResult>; }
```
Workflows call these through activities only.
