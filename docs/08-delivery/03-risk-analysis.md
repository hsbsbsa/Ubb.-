# Risk Analysis

Likelihood (L) / Impact (I): 1 low – 3 high. Owner = subsystem.

| # | Risk | L | I | Mitigation (planned) | Residual / trigger to revisit |
| --- | --- | --- | --- | --- | --- |
| R1 | Prose model produces translated-feel Korean despite style block | 3 | 3 | P-class benchmark gate; style block + exemplars; lint + judge + repair; project exemplar bank grows; different judge family | If nativeness median < 75 after exemplar bank ≥ 50 items → evaluate fine-tuned/open-weight Korean model routing |
| R2 | Style Judge self-preference / miscalibration | 2 | 3 | different family; evidence-first; contrast pairs; monthly editor panel | Spearman < 0.7 → rubric revision |
| R3 | Extraction misses or hallucinates canon items | 2 | 3 | two extractors + deterministic pre-pass; evidence verification; adjudication; human queue for majors; fixture recall tests | disagreement > 25% → prompt work / model change |
| R4 | Context pack misses a critical old fact | 2 | 3 | T1 structured states from canon (not retrieval) for participants; hybrid retrieval; evidence quotes; continuity checker as second net; recall tests | recall@pack < 0.9 on fixture → ranker tuning / reranker |
| R5 | Token budgets too small for ensemble casts / long contracts | 2 | 2 | degradation ladders; T0 overflow error surfaces early; contract size limits | frequent PACK_T1_OVERFLOW → raise budgets/model ctx |
| R6 | Cost per chapter exceeds expectations | 2 | 2 | tiers; caching; early stop; hard limits; prediction calibration | cost > 1.5× tier envelope for 10 chapters → routing review |
| R7 | Provider outages/rate limits stall batches | 2 | 2 | ≥ 2 providers per class; circuit breakers; pause/resume | — |
| R8 | Temporal operational complexity | 2 | 2 | Temporal Cloud option; dev server for local; rehydrate-from-artifacts fallback | — |
| R9 | Korean NLP sidecar accuracy on webnovel register (slang, coined terms) | 2 | 2 | glossary-aware tokenization; user dictionary; fallback heuristics; writer speaker annotations reduce reliance | register accuracy < 95% → analyzer tuning |
| R10 | Over-rigid planning produces dull chapters | 2 | 2 | rolling horizon; candidates for arcs; repetition judge; directions; reader feedback (Beta) | editor ratings on "fun" dimension low → planner prompt work |
| R11 | Knowledge ledger too granular → extraction noise | 2 | 2 | propositions limited to contract/secret-relevant + extractor thresholds; dedupe by embedding + adjudication | ledger growth > 100 props/chapter → tighten rules |
| R12 | Retcon propagation overwhelming users (many stale items) | 2 | 2 | grouped stale reasons; MVP mark-only; Beta patch proposals; importance filter | — |
| R13 | Prompt injection via requirements/imports | 1 | 3 | classifier; untrusted wrapping; gates on outputs consuming untrusted text | — |
| R14 | Copyright exposure (similarity to existing works) | 1 | 3 | provenance-only exemplars; no imitation instructions; similarity screening (Beta); trope-level overlays | — |
| R15 | Data breach of unpublished manuscripts | 1 | 3 | RLS; envelope encryption; secret manager; audit; provider privacy allowlist | — |
| R16 | Schema churn destabilizes generated types | 2 | 1 | schema-first discipline; versioned schemas; contract tests | — |
| R17 | Regression/possession timeline semantics confuse extraction | 2 | 2 | explicit frames + timeline IDs; overlay-specific extractor guidance; fixture traps T7/T8/T15 | — |
| R18 | Human review becomes the bottleneck | 2 | 2 | Semi-auto thresholds; keyboard-first queue; auto-approve for clean chapters | — |
| R19 | Model updates change behavior silently | 2 | 2 | pinned model versions in routing; regression suite on model change | — |
| R20 | Length control drift (chapters too long/short) | 2 | 1 | scene-level targets; tolerance; continuation protocol | — |
