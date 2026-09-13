# Requirements Traceability Matrix

Maps each functional requirement group to design documents, schemas, ADRs, backlog items, and tests.
Keep this file updated in the same change as any requirement/design change (AGENTS.md rule 1).

| Requirement(s) | Design | Schemas | ADRs | Backlog | Tests (strategy §) |
| --- | --- | --- | --- | --- | --- |
| FR-1.1–1.7 intake & spec | UW-1; `05-generation/01` §2.1; `03-prompt-architecture` §7 | `story-intake`, `story-spec` | 0019 | B-2-1, B-3-2 | §4 workflow; §10 injection |
| FR-2.1 concepts | `05-generation/01` §2.2; `02-eval` §5 | `concept`, `comparison-verdict` | 0015 | B-2-2, B-3-3 | §5 position bias |
| FR-2.2–2.7 bible, locks, speech profiles | `05-generation/01` §2.3; `02-korean-style/02` §5; `04-memory-canon/02` §1 | `entity`, `speech-profile`, `style-profile` | 0006, 0025 | B-2-3, B-3-4 | §3 bitemporal; §6 speech-level |
| FR-3.1–3.9 hierarchical planning, promises, contracts | `03-story-planning/01`, `02` | `series-blueprint`, `arc-plan`, `chapter-contract`, `scene-plan`, `promise` | 0012, 0013 | B-2-4, B-3-5 | §4; §5 chapter_planner |
| FR-4.1–4.9 production pipeline | `05-generation/01` §4–6 | `scene-draft`, `patch`, `job` | 0003, 0014, 0015 | B-2-5, 2-9, 2-10, 2-11, 2-15 | §4; §8 chaos |
| FR-5.1–5.8 evaluation & revision | `05-generation/02` | `issue`, `scorecard`, `patch` | 0014 | B-2-6, B-2-7, B-2-14 | §5 regression; §2 lint |
| FR-6.1–6.12 Korean style | `02-korean-style/01`–`05` | `style-profile`, `speech-profile`, `lint-report` | 0005, 0017, 0025 | B-1-1…1-5 | §2, §6 |
| FR-7.1–7.17 memory/canon/knowledge | `04-memory-canon/01`–`03` | `fact`, `event`, `knowledge-state`, `relationship-state`, `canon-delta`, `canon-commit`, `common` (evidenceRef, storyClock) | 0006, 0007, 0008, 0009, 0022, 0023 | B-0-5, B-1-6…1-11, 1-15, B-2-8 | §3 integration; §7 long-form |
| FR-8.1–8.5 context packs | `04-memory-canon/04`, `05` | `context-pack-manifest` | 0010, 0011 | B-1-12, B-1-13 | §3 recall/determinism |
| FR-9.1–9.6 budgets, jobs, audit, gateway | `06-system/05`, `07`, `04` | `llm-call-record`, `job`, `budget` | 0004, 0018 | B-0-6, B-2-12, B-3-8 | §8, §9 |
| FR-10.1–10.4 export & rights | `06-system/06` §9–10; UW-16 | `export-request` | 0025 | B-2-16, B-3-8 | manual + unit |
| FR-11.1–11.5 security & tenancy | `06-system/06` | — | 0020 | B-0-4, B-0-9, B-4-4 | §10 |
| NFR-A auditability | `06-system/05` §5, `07` §1 | `llm-call-record`, `context-pack-manifest` | 0004, 0016 | B-0-6 | §3 |
| NFR-B reliability | `06-system/04` | `job` | 0003 | B-2-10, B-4-2 | §8 |
| NFR-C performance | `06-system/02` §14, `04-memory-canon/05` | — | 0002 | B-4-x, load | §11 |
| NFR-D cost | `06-system/05` | `budget` | 0018 | B-2-12 | §9 |
| NFR-E security/privacy | `06-system/06` | — | 0020 | B-0-4, B-4-4 | §10 |
| NFR-F integrity | `06-system/02` §12 | `common` (evidenceRef, storyClock) | 0022, 0024 | B-0-3, B-0-5 | §2, §3 |
| NFR-G observability | `06-system/05` §5 | `llm-call-record` | — | B-0-6, B-4-6 | — |
| NFR-H usability/i18n | `06-system/08` | — | — | B-3-1 | usability pass |
| NFR-I maintainability | `05-generation/03`; AGENTS.md | all | 0016, 0021 | B-0-2, B-0-7 | §1 contract |

## Hard-question coverage (from the brief)

| # | Question | Where answered |
| --- | --- | --- |
| 1 | Remember previous chapter exactly | `04-memory-canon/04` §4 |
| 2 | Retrieve from hundreds of chapters ago | `04-memory-canon/05`; `04` §2 |
| 3 | Know what each character knows | `04-memory-canon/03` |
| 4 | Truth/belief/suspicion/lies/secrets | `04-memory-canon/03` §2, `02` §1.6 |
| 5 | Future plans vs completed events | `04-memory-canon/02` §3; ADR-0007 |
| 6 | Rejected drafts never enter canon | `04-memory-canon/02` §7; ADR-0009 |
| 7 | Approved chapter updates memory | `04-memory-canon/02` §5; `05-generation/01` §4 step 9 |
| 8 | Conflicting extractions resolved | `04-memory-canon/02` §5.2 |
| 9 | Earlier chapter changes propagate | `04-memory-canon/02` §8–9 |
| 10 | Every relevant call preserves Korean style | `02-korean-style/01` §3–4; ADR-0005 |
| 11 | Detect Western/translation drift | `02-korean-style/04`, `05` |
| 12 | Repair without rewriting everything | `02-korean-style/05` §3; `05-generation/02` §4; ADR-0014 |
| 13 | Reliability in long workflows | `06-system/04` |
| 14 | Cost control | `06-system/05`; ADR-0018 |
| 15 | Another agent can begin | `08-delivery/05`, `01`, `02`; `schemas/`, `examples/` |

Full audit: `docs/08-delivery/07-plan-audit.md`.
