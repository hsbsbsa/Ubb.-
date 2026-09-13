# Diagrams

Mermaid sources. Render with any Mermaid-capable viewer.

## 1. System context

```mermaid
flowchart LR
  U[Author / Editor] -->|HTTPS| WEB[apps/web Next.js]
  WEB -->|REST + SSE| API[apps/api Fastify]
  API --> PG[(Postgres 16 + pgvector\nsingle system of record)]
  API --> TEMP[Temporal]
  TEMP --> WK[apps/worker\nworkflows + activities]
  WK --> PG
  WK --> GW[packages/gateway\nStyle Guard · Budget · Audit]
  GW --> P1[LLM Provider A]
  GW --> P2[LLM Provider B]
  GW --> EMB[Embedding provider]
  WK --> NLP[Korean NLP sidecar]
  WK --> S3[(Object storage)]
  API --> S3
  WK --> OTEL[OpenTelemetry]
  API --> OTEL
```

## 2. Chapter production workflow (sequence)

```mermaid
sequenceDiagram
  participant UI
  participant API
  participant WF as ChapterProductionWorkflow
  participant CTX as ContextAssembler
  participant GW as Gateway
  participant EV as Evaluators
  participant RV as RevisionWorkflow
  participant CC as CanonCommitWorkflow
  participant DB as Postgres

  UI->>API: POST /chapters/{n}:generate
  API->>WF: start (deterministic id, lease)
  WF->>DB: preflight: prev accepted? budget? canon_version_read
  WF->>GW: scene_planner (pack.scene_planner)
  loop each scene
    WF->>CTX: assemble pack.scene_writer (T0..T3, manifest)
    CTX-->>WF: pack (hash, manifest)
    WF->>GW: scene_writer (StyleGuard ✓, budget ✓)
    GW-->>WF: scene draft (schema-valid)
    WF->>DB: save draft version, lint, register
  end
  WF->>GW: chapter_assembler
  WF->>EV: deterministic checks + judges (parallel)
  EV-->>WF: Scorecard (issues w/ evidence)
  alt blocking/major issues
    WF->>RV: patch-first revision (≤ max rounds)
    RV-->>WF: new version + regression results
  end
  WF->>UI: gate (Assisted) — review
  UI->>API: approve
  API->>WF: signal approve
  WF->>CC: start child
  CC->>GW: extractor_a ∥ extractor_b
  CC->>CC: reconcile, adjudicate conflicts, verify evidence
  CC->>DB: ATOMIC COMMIT (delta, version+1, edges, L1)
  CC-->>WF: committed
  WF->>DB: post-commit (embeddings, exemplars, promises, horizon signal)
  WF-->>UI: chapter.accepted (SSE)
```

## 3. Canon commit (state machine of a chapter)

```mermaid
stateDiagram-v2
  [*] --> planned
  planned --> drafting
  drafting --> drafted
  drafted --> evaluating
  evaluating --> revising: blocking/major
  evaluating --> review_pending: clean
  revising --> evaluating
  revising --> needs_attention: rounds exhausted
  review_pending --> approved: approve
  review_pending --> revising: request changes
  review_pending --> rejected: reject
  approved --> extracting
  extracting --> reconciling
  reconciling --> verifying
  verifying --> committing
  committing --> accepted: tx ok
  committing --> approved: tx fail (canon untouched)
  accepted --> stale: dependency changed
  accepted --> retconned: retcon
  accepted --> superseded: regeneration accepted
  rejected --> [*]: versions quarantined
```

## 4. Memory layers and data flow

```mermaid
flowchart TB
  subgraph Inputs
    REQ[Story Spec\nhard/soft/assumptions]
    BIB[Story Bible\n+ locked facts]
    PLAN[Plans\n(frame=plan)]
  end
  subgraph Canon["Canon (accepted chapters only)"]
    MV[Manuscript versions\n(immutable)]
    FACT[Facts (bitemporal)\n+ evidence spans]
    EVT[Events + reality frames]
    KNOW[Knowledge ledger]
    REL[Relationships]
    PROM[Promise ledger]
    SUM[Summaries L1–L4]
    IDX[Lexical + vector index]
  end
  subgraph Quarantine
    QD[Rejected drafts / candidates]
    FB[Raw feedback]
  end
  REQ --> PACK[Context Pack Assembler]
  BIB --> PACK
  PLAN -->|labelled 예정| PACK
  FACT --> PACK
  EVT --> PACK
  KNOW --> PACK
  REL --> PACK
  PROM --> PACK
  SUM --> PACK
  IDX --> PACK
  MV -->|prev chapter tail| PACK
  PACK --> LLM[LLM roles]
  LLM --> DRAFT[Draft versions]
  DRAFT -->|accepted| MV
  MV -->|extract → reconcile → verify| DELTA[Canon Delta]
  DELTA -->|atomic commit| FACT
  DELTA --> EVT
  DELTA --> KNOW
  DELTA --> REL
  DELTA --> PROM
  DELTA --> SUM
  SUM --> IDX
  DRAFT -->|rejected| QD
  QD -.->|never| PACK
  FB -.->|never| PACK
```

## 5. Context pack tiers

```mermaid
flowchart LR
  T0[T0 Mandatory\nhard reqs · style block · contract\nlocked facts · guards · glossary · L4] --> FIT[Budget fitting]
  T1[T1 Critical\nprev chapter tail+L1 · states · knowledge\nrelationships · arc plan · promises due · timeline] --> FIT
  T2[T2 Relevant\nretrieved events/facts/evidence · L2/L3 · voice exemplars] --> RANK[Rank + dedupe] --> FIT
  T3[T3 Optional\nextra exemplars · minor entities] --> FIT
  FIT --> VAL[Validate T0 byte-equality\nstyle hash · prev tail hash · sources allowlist]
  VAL --> MAN[Manifest + hash → store]
  MAN --> CALL[Gateway call]
```

## 6. Knowledge ledger example (regression + hidden identity)

```mermaid
flowchart TB
  P1["명제 P1: 도윤은 회귀자다 (true)"]
  P2["명제 P2: 서하는 공작가의 사생아다 (true, secret)"]
  P3["명제 P3: 도윤은 첩자다 (false — 카일이 퍼뜨린 거짓)"]
  DY[도윤] -->|knows (prior_loop_memory)| P1
  SH[서하] -->|unaware → suspects ch.31 → knows ch.58| P1
  KL[카일] -->|knows (told by 백작 ch.17)| P2
  SH -->|unaware until ch.72| P2
  RD[reader] -->|knows ch.17| P2
  SH -->|believes_false ch.23 → doubts ch.40 → knows false ch.58| P3
  KL -->|knows it is false (liar)| P3
```

## 7. Retcon propagation

```mermaid
sequenceDiagram
  participant U as User
  participant W as RetconWorkflow
  participant C as Canon
  participant D as DependencyEdges
  U->>W: retcon ch.12 (new text)
  W->>W: new version → evaluators (excluding items from old version)
  W->>U: review delta diff
  U->>W: approve
  W->>C: commit: retract old items, insert new (version+1)
  C->>D: touched item ids
  D-->>W: dependents (ch.13–ch.40 contracts/chapters)
  W->>U: stale list with reasons (MVP) / patch proposals (Beta)
```
