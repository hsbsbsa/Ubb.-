# Model Gateway

`packages/gateway` is the only path to any LLM or embedding provider (ADR-0004).

## 1. Responsibilities

1. **Provider adapters** — uniform request/response for chat-completion-style APIs (OpenAI-compatible,
   Anthropic-style, Google-style, and OpenAI-compatible self-hosted/open-weight endpoints incl. Kimi-class
   models). Adapters normalize: messages, JSON-schema mode, max tokens, stop, seed, streaming (not used for
   production calls except UI previews), usage & cached-token reporting, request IDs, finish reasons.
2. **Routing** — `routing_table { role → [ {model_id, provider, priority, params_overrides, max_ctx,
   price_in, price_out, price_cached, supports_json_schema, tokenizer_hint} ] }` per environment/workspace.
   Class-based defaults (R/P/M/C/E) with role overrides. Constraints: `judge.family != writer.family` when
   available; extractor B family ≠ A when available.
3. **Style Guard** — see Korean style architecture §4; fail-closed.
4. **Budget guard** — pre-call reservation against project/chapter/workflow budgets; release on completion.
5. **Idempotency** — `idempotency_key` lookup in `llm_calls`; returns stored output when completed.
6. **Structured output** — schema attach (native mode) or instruction; validation; repair loop
   coordination (repair is itself a gateway call with role `json_repairer`).
7. **Retries/fallback/circuit breakers** — per reliability plan.
8. **Truncation detection** — `finish_reason=length` surfaced; continuation helper.
9. **Cost accounting** — usage × price table → `cost_cents`; cached tokens priced separately.
10. **Audit** — persist `llm_calls` row (inputs/outputs to encrypted object storage beyond 64 KB) with all
    NFR-A fields; OpenTelemetry span.
11. **Concurrency** — workspace/provider token buckets; fairness across projects.
12. **Privacy** — provider allowlist per workspace; payload minimization checks (no user identity).

## 2. Request contract

```ts
type GatewayRequest = {
  workspaceId; projectId; jobId; activityId; idempotencyKey;
  role: RoleName;                         // determines class, style sensitivity, schema, params
  promptVersionId: string;                // registry
  pack: { id; hash; renderedSystem; renderedUser; tokenEstimate };
  styleBlockRef?: { hash; profileVersionId; role };   // required if role.style_sensitive
  outputSchemaRef?: string;
  params?: Partial<ModelParams>;          // bounded by prompt version guards
  budgetScope: { projectId; chapterJobId?; workflowId };
  untrustedSegments?: Array<{ start; end; source }>;   // must be inside user message
};
type GatewayResponse = {
  llmCallId; modelId; provider; output: { text?: string; json?: unknown }; finishReason;
  usage: { input; output; cached }; costCents; latencyMs; schemaValid: boolean; attempts: number;
};
```

## 3. Model class benchmarks (selection procedure, not vendor choice)

Before a model is routed to class **P**, it must pass the **Korean prose benchmark**: contrast-pair
preference by human raters, lint marker rate on fresh generations ≤ threshold, register accuracy on speech
profile tests ≥ 95%, and length control within ±12% on 20 samples. Class **R** candidates are validated on
the continuity fixture (recall/precision of seeded traps). Class **M** on schema validity rate ≥ 98% and
extraction fixture recall. Results recorded in `docs/adr/` amendments or an ops runbook (not user-facing).

## 4. Provider-independence checklist

- No provider SDK types leak outside `packages/gateway/adapters/*`.
- Prompts are provider-neutral; provider-specific system prompt quirks handled by adapter transforms.
- Tokenizer differences: per-model tokenizer hint used for budget estimates; manifests record estimate
  source.
- JSON mode differences handled by adapter; fallback to instruction-mode + repair.
- Prices and context limits are data (routing table), not code.

## 5. Local/test providers

`MockProvider` (deterministic canned outputs keyed by prompt hash for tests), `ReplayProvider` (replays
recorded `llm_calls` for regression tests without spend), `FaultInjectingProvider` (chaos tests).
