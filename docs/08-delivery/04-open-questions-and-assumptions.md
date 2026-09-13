# Open Questions and Assumptions

## 1. Decisions made by default (no user input needed; change via ADR)

| # | Decision | Rationale |
| --- | --- | --- |
| A1 | TypeScript monorepo (Next.js, Fastify, Temporal TS SDK) with a Python NLP sidecar | one language for domain logic; Korean morphology tooling is best in Python |
| A2 | Postgres 16 + pgvector single system of record | transactional canon commits + vectors + lexical search in one place |
| A3 | Temporal for orchestration | durable, resumable, signal-driven; matches gate/pause/cancel needs |
| A4 | Default chapter length 5,500 chars (공백 포함), tolerance ±12% | common platform norm; user-adjustable |
| A5 | Assisted mode default for bible + first arc, Semi-auto afterwards | quality trust builds; autopilot is Beta |
| A6 | Standard tier default (~20 calls/chapter) | balance of quality and cost |
| A7 | Two extractors + adjudicator on conflicts | reliability of canon is worth ~2 calls |
| A8 | Different model family for judges vs writer when available | self-preference mitigation |
| A9 | Provider-neutral routing; Kimi-class models allowed via OpenAI-compatible adapter but not required | user's previous provider usable; no lock-in |
| A10 | Volumes as export grouping (25 chapters default) | narrative planning uses arcs |
| A11 | Prior-loop knowledge modeled as a timeline + knowledge source, not as facts on `main` | prevents "known future" from becoming canon |
| A12 | Content restriction default 15+ | typical webnovel platform rating; user-adjustable |
| A13 | Korean UI first for text-heavy screens | target users are Korean authors |
| A14 | Character counting = NFC code points incl. spaces excluding markup | matches platform counters closely; deterministic |

## 2. Questions that genuinely need the product owner (do not block MVP build)

| # | Question | Default until answered |
| --- | --- | --- |
| Q1 | Which LLM providers/models are licensed for the first deployment (and their privacy terms)? Affects P-class benchmark and cost model. | Plan supports any; Phase 0 runs the P-class benchmark on available providers and records results |
| Q2 | Target platform(s) for export formatting (e.g., specific 회차 header conventions, line breaks)? | Generic TXT/DOCX profiles; platform presets in Beta |
| Q3 | Is a human Korean editor panel available for monthly calibration? | Plan assumes 2–3 editors part-time; if not, rely on contrast pairs + author self-ratings |
| Q4 | Pricing/tenancy model (single-tenant self-hosted vs multi-tenant SaaS)? | Multi-tenant-ready design (RLS); can deploy single-tenant |
| Q5 | Should the user's own previously written chapters be importable as canon (ingestion of existing series)? | Not in MVP; design allows: import → treat as accepted versions → extraction → commit (Beta candidate) |
| Q6 | Disclosure requirements of target platforms regarding AI assistance? | User-configurable text; no assertions made by the product |
| Q7 | Preferred Korean morphological analyzer licensing (Kiwi LGPL vs MeCab-ko) for the deployment? | Kiwi default |

## 3. Assumptions about the environment

- Node 22 LTS, pnpm 9, Postgres 16, Temporal ≥ 1.24 server / TS SDK ≥ 1.11, pgvector ≥ 0.7. Versions are
  pinned at Phase 0 in `package.json`/`docker-compose.yml`.
- At least two LLM providers with JSON-schema-capable models and ≥ 128k context are reachable from the
  deployment region.
- Object storage is S3-compatible.

## 4. Deferred design topics (tracked, not blocking)

- Cross-encoder reranker choice (Beta).
- Fine-tuning/distillation of cheap classifiers from accumulated judge data (Production).
- Multi-author collaboration semantics on the same project (Future).
- Reader-facing preview/publishing integrations (Future).
