# ADR-0026: English is the manuscript language; Korean webnovel is the narrative tradition

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** principal architects (product, software, AI systems, data, Korean webnovel production)

## Context
The product's purpose was misunderstood in the first planning pass: the plan required Korean-language
manuscripts. The actual product requirement is **English-language prose, composed directly in English,
that follows Korean serialized-webnovel narrative structure, pacing, hooks, payoff, progression cadence,
reader gratification and genre conventions**. Two failure modes must be prevented at once: Western-novel
drift (fluent English with traditionally published pacing) and translation-like English (English that
imitates Korean grammar, honorifics, or idiom). The product is not a translator.

## Decision
1. **Output language and narrative tradition are separate, explicit, versioned contracts.** The
   Output-Language Profile (`lang/en`, locale `en-US`/`en-GB`) carries the Output-Language Contract; the
   Narrative-Tradition Profile (`tradition/kr-webnovel`) carries the Narrative-Tradition Contract.
2. Eight separable profile layers compose the **Narrative Identity**: output language & locale; narrative
   tradition; genre profile(s); setting & cultural profile; character naming profile; social hierarchy &
   dialogue-register policy; terminology & romanization policy; user prose preferences.
3. **English is the required output language** in MVP, Beta and Production. The architecture keeps the
   language an explicit contract (so another language could be added by a future ADR) but nothing in the
   plan may weaken or obscure the English requirement.
4. **No translation path exists.** No role, prompt, workflow step or fallback may generate non-English
   manuscript text; a deterministic output-language check gates every manuscript-producing call.
5. Korean appears in the system only as terminology of the tradition (glossed), as source terms in the
   terminology policy, and as optional native-script names in the naming registry — never as manuscript
   prose and never as grammar imitated in English.
6. Governing requirement IDs: OUTPUT-EN-001, STYLE-KWN-001, STYLE-GUARD-001, EVAL-SEPARATION-001,
   NO-TRANSLATION-001 (`docs/01-requirements/01-functional-requirements.md` §FR-0).

## Alternatives considered
- Korean manuscripts translated to English by a final step — rejected: produces translation-like English,
  doubles cost, and is not the product.
- A single "write like a Korean webnovel in English" instruction — rejected: does not survive a multi-call
  pipeline (the same failure as the original Kimi K3 attempt).

## Consequences
Repository-wide correction (docs, schemas, examples, fixtures, tests, roadmap). Supersedes the
Korean-manuscript assumptions in ADR-0005 (guard), ADR-0017 (Korean NLP), ADR-0024 (character counting).
