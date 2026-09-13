# Yeonjae Studio (연재 스튜디오) — Planning Package

**Status:** Planning complete, implementation not started.
**Purpose of this repository state:** a complete, internally consistent, production-level plan for an AI
Korean-webnovel production studio, written so that an engineering agent can implement it without
redesigning the system.

Yeonjae Studio turns a short premise plus requirements (genre, characters, tropes, forbidden developments,
tone, chapter count, target length in Korean characters, mandatory scenes, content restrictions, running
directions) into a complete serialized Korean webnovel: story specification, story bible, characters,
world, progression rules, series/season/arc plans, chapter contracts, scene plans, Korean prose, editing,
evaluation, revision, continuity management, canon memory, and manuscript export.

It is designed as a **stateful, resumable, auditable novel-production studio** — many purposeful LLM calls
orchestrated by durable workflows over a canonical story database — not one giant prompt or one long chat.

The two problems this plan treats as first-class architecture (not as prompt wording):

1. **Korean webnovel style enforcement** — every style-sensitive LLM call is guaranteed to carry a compiled,
   versioned Korean webnovel style block (genre-aware), with deterministic + model-based drift detection and
   passage-level repair. See `docs/02-korean-style/`.
2. **Long-range context and canon memory** — the application, not the model, is the authoritative memory.
   Temporal facts with evidence, per-character knowledge, planned-vs-happened separation, quarantined
   rejected drafts, atomic canon commits, and deterministic context-pack assembly. See `docs/04-memory-canon/`.

## How to read this package

| If you want to… | Start here |
| --- | --- |
| Understand the product in 10 minutes | `docs/00-overview/01-executive-product-definition.md` |
| Know what is in the MVP vs later | `docs/00-overview/03-scope-and-release-tiers.md` |
| Check requirements | `docs/01-requirements/` |
| Understand Korean style enforcement | `docs/02-korean-style/01-korean-webnovel-style-architecture.md` |
| Understand memory, canon, knowledge | `docs/04-memory-canon/01-context-and-memory-architecture.md` |
| Understand the generation pipeline | `docs/05-generation/01-generation-pipeline.md` |
| Build the system | `docs/06-system/` + `schemas/` + `docs/08-delivery/05-implementation-handoff-guide.md` |
| See why decisions were made | `docs/adr/` |
| Verify the plan answers the hard questions | `docs/08-delivery/07-plan-audit.md` |
| Start implementing | `AGENTS.md`, then `docs/08-delivery/01-implementation-roadmap.md` and `02-backlog.md` |

## Repository layout (planning phase)

```
README.md                      this file
AGENTS.md                      instructions for engineering agents working in this repo
docs/
  00-overview/                 product definition, glossary, scope & tiers
  01-requirements/             functional / nonfunctional requirements, user workflows, traceability
  02-korean-style/             Korean webnovel style architecture, profiles, genre catalog, drift detection, lint rules
  03-story-planning/           hierarchical planning, promise ledger, chapter contracts
  04-memory-canon/             context/memory, canon & temporal state, character knowledge, context packs, retrieval
  05-generation/               generation pipeline, evaluation & revision, prompt architecture, role catalog
  06-system/                   system, data, API, workflow reliability, cost/observability, security/rights, UI
  07-quality/                  testing strategy, fixture story, definition of done
  08-delivery/                 roadmap, backlog, risks, open questions, handoff guide, plan audit
  adr/                         architecture decision records
schemas/                       JSON Schema (2020-12) for the core machine-readable objects
examples/                      example instances of the schemas (fixture story data, style profiles)
tools/                         planning-package validation script (schemas + examples)
```

## Naming

- **Yeonjae (연재)** = "serialization" — the product is a serialized-fiction production studio.
- Documents are written in English for the implementing team; Korean is used where the subject *is*
  Korean (style rules, exemplars, speech levels, fixture prose). Domain terms are defined once in
  `docs/00-overview/02-glossary.md` and used consistently everywhere else.

## Non-goals of this repository state

- No application code, no placeholder prototypes, no prompt files intended for production use.
  Prompt *specifications* and *example* templates appear in docs and `examples/` as design artifacts only.
- No secrets, keys, or credentials. Provider configuration is described, never populated.
