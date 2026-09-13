# ADR-0029: Numeric style thresholds are configuration with calibration status

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Lint thresholds, gate scores, cadence targets and paragraph limits were written as if universal. They are
starting points whose right values depend on genre, project voice, model, and reviewer expectations.

## Decision
Every numeric threshold lives in profile data (never code) with `starting_value`, `calibration_status`
(`uncalibrated` / `contrast_calibrated` / `project_calibrated`), `last_calibrated_at` and `evidence_ref`.
Calibration inputs: the five-class contrast set, reviewer overrides, and per-project accepted-chapter
statistics after ≥ 10 chapters. Changing a threshold creates a new profile version; documentation labels
all numbers as starting values.

## Consequences
Profile schema carries `calibration`; UI shows calibration status; the testing strategy includes a
calibration procedure; no doc may present a threshold as a universal truth.
