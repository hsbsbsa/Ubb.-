# Examples

Machine-readable examples that conform to `schemas/`. All story content is original fixture material
(『두 번째 각성』, see `docs/07-quality/02-fixture-story.md`). Validate with
`python tools/validate-planning-package.py`.

```
examples/
  fixture/
    ids.json                     stable fixture UUIDs shared by all fixture files
    story-intake.json            intake form for the fixture project
    speech-profile.seoha.json    이서하 speech profile with a ch.87 speech-level transition
    chapter-contract.ch12.json   full chapter contract (유리 합류 / 남매 오해 / 무진 다리 복선)
    canon-delta.ch09.json        verified canon delta for ch.9 (injury fact, location supersede, knowledge, relationship, promise advance)
    knowledge-ledger.json        expected knowledge states through season 1 + guards + expected leak detections
    contrast-pairs.seed.json     native vs translated-feel pairs and register cases for calibration tests
  style-profiles/
    kr-webnovel-base.v1.json     base Korean webnovel profile (rules, thresholds, rubric, forbidden patterns)
    genre-hunter-gate.v1.json    hunter/gate overlay
```

Notes:
- Evidence offsets in fixture files satisfy `end - start == len(quote)`; the actual `start` values are
  placeholders until the fixture manuscripts exist. The validator enforces the length invariant only.
- `knowledge-ledger.json` uses short names (`도윤`, `P1`) and `"chapter.ordinal"` clocks for readability;
  the DB representation uses the ids in `ids.json` and full `storyClock` objects.
