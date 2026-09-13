# Examples

Machine-readable examples that conform to `schemas/`. All story content is original fixture material
(*Second Awakening*, see `docs/07-quality/02-fixture-story.md`): **English manuscript prose in the Korean
serialized-webnovel tradition**. Validate with `python tools/validate-planning-package.py`.

```
examples/
  fixture/
    ids.json                          stable fixture UUIDs shared by all fixture files
    story-intake.json                 intake form (English premise; words per chapter; naming/terminology prefs)
    register-profile.seoha.json       Lee Seo-ha's dialogue-register & voice profile with the ch.87 transition
    chapter-contract.ch12.json        full chapter contract (Yu-ri joins / sibling misunderstanding / Mu-jin's leg)
    canon-delta.ch09.json             verified canon delta for ch.9 (injury fact, location supersede, knowledge,
                                      relationship with register, promise advance)
    knowledge-ledger.json             expected knowledge states through season 1, per-timeline truths, guards,
                                      expected leak detections
    contrast-sets.seed.json           five-class contrast sets (kwn_english / western_english / translation_like /
                                      literary / weak_serial) + register cases for calibration tests
  narrative-profiles/
    lang-en.v1.json                   English output-language profile (contract, punctuation, translation markers,
                                      prose lint thresholds, Prose Judge rubric)
    tradition-kr-webnovel.v1.json     Korean serialized-webnovel tradition profile (contract, structure, rhythm,
                                      devices, structure lint thresholds, Structure Judge rubric)
    genre-hunter-gate.v1.json         hunter/gate genre profile (English vocabulary, terminology defaults, devices)
    project-second-awakening.composed.v1.json  composed identity for the fixture project (all eight layers)
```

Notes:
- Evidence offsets satisfy `end − start == len(quote)` in Unicode code points; the actual `start` values are
  placeholders until the fixture manuscripts exist. The validator enforces the length invariant only.
- `knowledge-ledger.json` uses short names (`Do-yoon`, `P1`) and `"chapter.ordinal"` clocks for readability;
  the DB representation uses the ids in `ids.json` and full `storyClock` objects.
- Korean appears in `narrative-profiles/` only as **source terms** in terminology policies (e.g., 헌터 →
  *hunter*); manuscript and working text are English.
- Thresholds in the profiles are **starting values** with `calibration.status = uncalibrated` (ADR-0029).
