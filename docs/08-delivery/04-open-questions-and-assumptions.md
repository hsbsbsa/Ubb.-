# Open Questions and Assumptions

## 1. Decisions made by default (no user input needed; change via ADR)

| # | Decision | Rationale |
| --- | --- | --- |
| A1 | TypeScript monorepo (Next.js, Fastify, Temporal TS SDK); optional self-hosted English grammar service | one language for domain logic; grammar checking is best served by an existing service if wanted |
| A2 | Postgres 16 + pgvector single system of record | transactional canon commits + vectors + lexical search in one place |
| A3 | Temporal for orchestration | durable, resumable, signal-driven; matches gate/pause/cancel needs |
| A4 | **English manuscripts (`en-US` default locale), Korean-webnovel tradition; no translation path** (ADR-0026) | the product requirement; two explicit contracts on every style-sensitive call |
| A5 | Default chapter length 2,500 words, tolerance ±12%; **no mechanical conversion from Korean character counts** — calibration is an implementation requirement (ADR-0034) | English episode length must be calibrated against reading time and the tradition's episode feel |
| A6 | Assisted mode default for bible + first arc, Semi-auto afterwards | quality trust builds; autopilot is Beta |
| A7 | Standard tier default (~20 calls/chapter) | balance of quality and cost |
| A8 | Two extractors + adjudicator on conflicts | reliability of canon is worth ~2 calls |
| A9 | Different model family for judges vs writer when available; Prose and Structure judges are separate calls in every tier | self-preference mitigation; dimension separation |
| A10 | Provider-neutral routing; P-class models qualified on **natural English under Korean-webnovel constraints**, never on Korean-language ability | matches the product |
| A11 | Volumes as export grouping (25 chapters default) | narrative planning uses arcs |
| A12 | Prior-loop knowledge modeled as a timeline + knowledge source; **proposition truth per timeline** (ADR-0031) | prevents "known future" from becoming canon |
| A13 | Content restriction default 15+ | typical serialized-fiction rating; user-adjustable |
| A14 | English UI first; Korean UI localization in Beta | target users write English serials |
| A15 | Naming default `korean_romanized` (Revised Romanization, family–given, hyphenated given names) for modern-Korea settings; `western` for romance fantasy | genre conventions |
| A16 | Terminology default `translate`; romanize only registry-approved terms; Korean script only in explicitly allowed contexts | natural English without untranslated clutter |
| A17 | Dialogue formality preserved as abstract register data and rendered in natural English (no honorific morphemes, no calques) | keeps social hierarchy without translation-like English |
| A18 | All numeric thresholds are starting values with calibration status (ADR-0029) | avoid false universality |
| A19 | Text offsets are Unicode code points everywhere (ADR-0030) | one addressing contract |
| A20 | Dependency edges carry materiality; only material edges mark stale (ADR-0032) | avoids over-staling |

## 2. Questions that genuinely need the product owner (do not block MVP build)

| # | Question | Default until answered |
| --- | --- | --- |
| Q1 | Which LLM providers/models are licensed for the first deployment (and their privacy terms)? Affects the P-class English-under-KWN benchmark and cost model. | Plan supports any; Phase 2 runs the benchmark on available providers and records results |
| Q2 | Target platform(s) for export formatting (chapter header conventions, line breaks, EPUB needs)? | Generic TXT/DOCX profiles; platform presets in Beta |
| Q3 | Is a bilingual reviewer panel (native-quality English judgment + Korean webnovel literacy) available for monthly calibration? | Plan assumes 2–3 reviewers part-time; if not, split the panel by scale and rely more on contrast sets |
| Q4 | Pricing/tenancy model (single-tenant self-hosted vs multi-tenant SaaS)? | Multi-tenant-ready design (RLS); can deploy single-tenant |
| Q5 | Should the user's own previously written English chapters be importable as canon (ingestion of an existing series)? | Not in MVP; design allows: import → treat as accepted versions → extraction → commit (Beta candidate) |
| Q6 | Disclosure requirements of target platforms regarding AI assistance? | User-configurable text; no assertions made by the product |
| Q7 | Spelling locale default for the first users (`en-US` vs `en-GB`)? | `en-US` |
| Q8 | Should Korean-script names ever appear in exports (e.g., a glossary listing 강도윤 next to Kang Do-yoon)? | Off by default; `export_glossary` may include native-script names if the user enables it |
| Q9 | Is an optional self-hosted English grammar service (LanguageTool-class) acceptable in the deployment (licensing/ops)? | Deferred to Beta; heuristics + Prose Judge in MVP |

## 3. Assumptions about the environment

- Node 22 LTS, pnpm 9, Postgres 16, Temporal ≥ 1.24 server / TS SDK ≥ 1.11, pgvector ≥ 0.7. Versions are
  pinned at Phase 0.
- At least two LLM providers with JSON-schema-capable models and ≥ 128k context are reachable from the
  deployment region and can write natural English.
- Object storage is S3-compatible.

## 4. Deferred design topics (tracked, not blocking)

- Cross-encoder reranker choice (Beta).
- Fine-tuning/distillation of cheap classifiers from accumulated judge data (Production).
- Multi-author collaboration semantics on the same project (Future).
- Additional output languages: the Output-Language Profile makes this possible, but it requires a new ADR,
  a new language profile, language-specific lint, and a new benchmark; **not planned** and never a reason
  to weaken the English requirement.
- Reader-facing preview/publishing integrations (Future).
