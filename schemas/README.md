# Schemas

JSON Schema 2020-12 contracts for the core objects. `$id`s live under `https://yeonjae.studio/schemas/`;
cross-references use relative names (`common.schema.json#/$defs/...`). Validate with
`python tools/validate-planning-package.py` (requires `jsonschema>=4.18`).

| Schema | Object | Primary docs |
| --- | --- | --- |
| `common.schema.json` | shared defs: uuid, storyClock, realityFrame, evidenceRef, knowerRef, stance, speechLevel, versionRef | glossary |
| `story-intake.schema.json` | user intake form | FR-1.1 |
| `story-spec.schema.json` | normalized requirements (hard/soft/assumption) | FR-1.2–1.5 |
| `style-profile.schema.json` | base / overlay / project style profile | 02-korean-style/02 |
| `speech-profile.schema.json` | per-character speech baseline | FR-2.6 |
| `entity.schema.json` | bible entity identity + descriptive version | 04-memory-canon/02 §1.2 |
| `fact.schema.json` | bitemporal fact with evidence | ADR-0006 |
| `event.schema.json` | canonical event with frame | ADR-0007 |
| `proposition.schema.json` | knowable statement, secrets | ADR-0008 |
| `knowledge-state.schema.json` | knower × proposition × stance | ADR-0008 |
| `relationship-state.schema.json` | directed pair state | FR-7.9 |
| `promise.schema.json` | promise ledger entry | FR-3.4 |
| `series-blueprint.schema.json` | top-level plan | FR-3.2 |
| `arc-plan.schema.json` | arc plan (plan frame) | 03-story-planning/01 §4 |
| `chapter-contract.schema.json` | chapter acceptance unit | ADR-0013 |
| `scene-plan.schema.json` | drafting unit | 03-story-planning/01 §8 |
| `scene-draft.schema.json` | writer output envelope | 05-generation/01 §8 |
| `issue.schema.json` | evaluation finding with evidence | 05-generation/02 §1 |
| `scorecard.schema.json` | merged evaluation | 05-generation/02 |
| `patch.schema.json` | span replacement | ADR-0014 |
| `lint-report.schema.json` | Korean lint + register output | 02-korean-style/04 |
| `comparison-verdict.schema.json` | pairwise judgment | ADR-0015 |
| `canon-delta.schema.json` | extracted/reconciled/verified changes | FR-7.2–7.3 |
| `canon-commit.schema.json` | atomic version bump record | FR-7.4 |
| `context-pack-manifest.schema.json` | pack contents & validation | ADR-0010 |
| `llm-call-record.schema.json` | audit record per call | NFR-A.1 |
| `job.schema.json` | workflow run record | FR-9.4 |
| `budget.schema.json` | spend limits | ADR-0018 |
| `export-request.schema.json` | export job input | FR-10.1 |

## Rules for implementers

1. Generate TypeScript types from these files (e.g., `json-schema-to-typescript`) or maintain Zod schemas
   with an equivalence test; never hand-fork.
2. Adding a field: add here first, bump the schema's documentation, update examples, then code.
3. Enums are closed lists on purpose (frames, stances, severities, speech levels). Extending one is an ADR.
4. Korean text fields end with `_ko`; they are data and are never machine-translated.
