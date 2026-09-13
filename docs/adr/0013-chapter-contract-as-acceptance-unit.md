# ADR-0013: Chapter Contract as the unit of acceptance

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
Evaluators need an objective specification to judge a chapter; planners need a structured output; canon
needs to know what was planned vs realized.

## Decision
Every chapter has a structured **Chapter Contract** (schema) with purpose, must/must-not, participants,
deltas, shape, risks, guards and acceptance criteria; it is validated on canon/plan/style axes before
drafting and is the reference for contract-compliance judging and realized/unrealized marking after commit.

## Alternatives considered
- Prose outlines — unverifiable.

## Consequences
Contract editing UI; planner prompt complexity; strong evaluation anchor.
