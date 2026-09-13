#!/usr/bin/env python3
"""Planning-package consistency check (not application code).

1. Validates every schema in schemas/ against the JSON Schema 2020-12 metaschema.
2. Validates the example instances in examples/ against their schemas.
3. Enforces the evidence-span invariant (end - start == len(quote) in code points).
4. Scans the repository for contradictory language-output statements and stale field names
   (the product composes English manuscripts in the Korean webnovel tradition; see ADR-0026).

Usage:  python tools/validate-planning-package.py
Deps:   jsonschema>=4.18 (pip install jsonschema)
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URI = "https://yeonjae.studio/schemas/"

EXAMPLES = [
    ("examples/fixture/story-intake.json", "story-intake.schema.json"),
    ("examples/fixture/register-profile.seoha.json", "register-profile.schema.json"),
    ("examples/fixture/chapter-contract.ch12.json", "chapter-contract.schema.json"),
    ("examples/fixture/canon-delta.ch09.json", "canon-delta.schema.json"),
    ("examples/narrative-profiles/lang-en.v1.json", "narrative-identity.schema.json"),
    ("examples/narrative-profiles/tradition-kr-webnovel.v1.json", "narrative-identity.schema.json"),
    ("examples/narrative-profiles/genre-hunter-gate.v1.json", "narrative-identity.schema.json"),
    ("examples/narrative-profiles/project-second-awakening.composed.v1.json", "narrative-identity.schema.json"),
]

PAYLOAD_SCHEMAS = {
    "fact": "fact.schema.json",
    "event": "event.schema.json",
    "knowledge_state": "knowledge-state.schema.json",
    "relationship_state": "relationship-state.schema.json",
}

# Statements that contradict the governing principle if they appear anywhere in the package.
# Each entry: (pattern, explanation, strict). Non-strict patterns are exempt on lines that describe a
# prohibition or a replacement (e.g., "never translates into English", "replaces the Korean NLP sidecar").
CONTRADICTION_PATTERNS = [
    (r"output (is )?always Korean", "manuscript output must be English", True),
    (r"natively Korean prose", "manuscript prose is English", True),
    (r"\bnative Korean prose\b", "manuscript prose is English", True),
    (r"\bKorean prose (quality|benchmark|output|for one scene)\b", "prose roles write English", True),
    (r"Korean characters? (per|incl|including)", "length is measured in words for English", True),
    (r"target_chars_per_chapter", "use target_words_per_chapter", True),
    (r"length_target_chars", "use length_target (words)", True),
    (r"english_leakage|English leakage", "English is the output language, never leakage", True),
    (r"\bKL-[A-Z]{2,6}-\d\d\b", "Korean lint rule ids were replaced by EP-*/ST-*/RG-*", True),
    (r"\bkoreanText\b", "use common.schema.json#/$defs/text", True),
    (r"\bspeechLevel\b|speech_level\b", "use dialogue register (abstract) rendered in English", True),
    (r"\bspeech level", "use dialogue register (abstract) rendered in English", False),
    (r"\bStyle Guard\b|StyleGuard", "renamed Narrative Identity Guard", True),
    (r"\bStyle Block\b|style block\b|STYLE_TAIL", "renamed Narrative Identity Block / IDENTITY_TAIL", True),
    (r"Korean NLP sidecar|morphological analyzer|Kiwi|MeCab", "no Korean morphology in the pipeline (ADR-0028)", False),
    (r"translate(d|s)? (it |them )?(into|to) English", "the pipeline never translates into English", False),
    (r"docs/02-korean-style", "directory renamed to docs/02-narrative-identity", True),
    (r"\bspeech-profile\.schema|style-profile\.schema", "schemas renamed to register-profile / narrative-identity", True),
    (r"\bcanonical_name_ko\b|\btext_ko\b|\bsummary_ko\b|\bstatement_ko\b|\bpurpose_ko\b|\bdescription_ko\b|\brationale_ko\b|\bsuggestion_ko\b|\btitle_ko\b", "language-suffixed primary fields were removed", True),
]
NEGATION_CONTEXT = re.compile(
    r"never|does not|do not|must not|cannot|no translation|NO-TRANSLATION|replace|supersed|removed|instead|"
    r"anti-pattern|drift|mirroring|forbid|reject|prohibit|not a criterion|not apply|do not exist|calque",
    re.I,
)

# Files where historical references to the old design are legitimately allowed (they describe the change).
CONTRADICTION_ALLOWLIST = {
    "docs/adr/0026-english-manuscript-korean-webnovel-tradition.md",
    "docs/adr/0027-narrative-identity-guard.md",
    "docs/adr/0028-english-prose-tooling-replaces-korean-nlp.md",
    "docs/adr/0034-language-neutral-length-model.md",
    "docs/adr/0005-fail-closed-style-guard.md",
    "docs/adr/0017-korean-nlp-sidecar.md",
    "docs/adr/0024-nfc-normalization-and-character-counting.md",
    "docs/08-delivery/07-plan-audit.md",
    "docs/08-delivery/08-correction-changelog.md",
    "tools/validate-planning-package.py",
}

HANGUL = re.compile(r"[\uac00-\ud7a3]")
# Files that may contain Korean script (terminology of the tradition, source terms in policies).
HANGUL_ALLOWLIST_PREFIXES = (
    "docs/00-overview/02-glossary.md",
    "docs/02-narrative-identity/",
    "docs/adr/",
    "examples/narrative-profiles/",
    "schemas/narrative-identity.schema.json",
    "README.md",
    "AGENTS.md",
    "docs/00-overview/01-executive-product-definition.md",
    "docs/08-delivery/",
    "docs/07-quality/",
    "docs/05-generation/",
    "docs/06-system/",
    "docs/04-memory-canon/",
    "docs/03-story-planning/",
    "docs/01-requirements/",
)


def load_schemas() -> tuple[dict, Registry]:
    schemas: dict[str, dict] = {}
    registry = Registry()
    for path in sorted(glob.glob(os.path.join(ROOT, "schemas", "*.schema.json"))):
        with open(path, encoding="utf-8") as f:
            schema = json.load(f)
        name = os.path.basename(path)
        schemas[name] = schema
        resource = Resource.from_contents(schema)
        registry = registry.with_resource(schema["$id"], resource)
        registry = registry.with_resource(BASE_URI + name, resource)
    return schemas, registry


def iter_repo_text_files():
    for pattern in ("**/*.md", "**/*.json", "**/*.py", ".env.example"):
        for path in glob.glob(os.path.join(ROOT, pattern), recursive=True):
            rel = os.path.relpath(path, ROOT)
            if rel.startswith(".hoplite") or "/.git/" in path or rel.startswith(".git"):
                continue
            yield rel, path


def main() -> int:
    ok = True
    schemas, registry = load_schemas()

    for name, schema in schemas.items():
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # noqa: BLE001
            ok = False
            print(f"[SCHEMA INVALID] {name}: {exc}")
    print(f"metaschema: {len(schemas)} schemas checked")

    for rel, schema_name in EXAMPLES:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            instance = json.load(f)
        validator = Draft202012Validator(schemas[schema_name], registry=registry)
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        if errors:
            ok = False
            print(f"[INVALID] {rel} vs {schema_name}")
            for err in errors[:20]:
                print("   -", "/".join(map(str, err.path)), ":", err.message[:200])
        else:
            print(f"[ok] {rel} vs {schema_name}")

    # Canon delta payloads: pre-commit objects lack ids/version fields, so validate present fields only.
    with open(os.path.join(ROOT, "examples/fixture/canon-delta.ch09.json"), encoding="utf-8") as f:
        delta = json.load(f)
    for item in delta["items"]:
        schema_name = PAYLOAD_SCHEMAS.get(item["type"])
        if not schema_name:
            continue
        schema = json.loads(json.dumps(schemas[schema_name]))
        schema["required"] = [r for r in schema.get("required", []) if r in item["payload"]]
        errors = list(Draft202012Validator(schema, registry=registry).iter_errors(item["payload"]))
        if errors:
            ok = False
            print(f"[INVALID payload] {item['local_id']} ({item['type']})")
            for err in errors[:10]:
                print("   -", "/".join(map(str, err.path)), ":", err.message[:200])
        else:
            print(f"[ok payload] {item['local_id']} ({item['type']}) vs {schema_name}")

    # Evidence-span invariant (code points).
    def check_evidence(owner: str, ev: dict) -> None:
        nonlocal ok
        if len(ev["quote"]) != ev["end"] - ev["start"]:
            ok = False
            print(f"[EVIDENCE MISMATCH] {owner}: len(quote)={len(ev['quote'])} end-start={ev['end'] - ev['start']}")

    for item in delta["items"]:
        for ev in item.get("evidence", []):
            check_evidence(item["local_id"], ev)
    with open(os.path.join(ROOT, "examples/fixture/chapter-contract.ch12.json"), encoding="utf-8") as f:
        contract = json.load(f)
    for anchor in contract.get("continuity_anchors", []):
        for ev in anchor.get("evidence", []):
            check_evidence(f"anchor {anchor['fact_id']}", ev)

    # Fixture prose must be English: no Hangul in manuscript-like fields of fixture examples.
    for rel in ("examples/fixture/chapter-contract.ch12.json", "examples/fixture/canon-delta.ch09.json",
                "examples/fixture/knowledge-ledger.json", "examples/fixture/register-profile.seoha.json",
                "examples/fixture/contrast-sets.seed.json", "examples/fixture/story-intake.json"):
        text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        if HANGUL.search(text):
            ok = False
            print(f"[NON-ENGLISH FIXTURE TEXT] {rel} contains Hangul; fixture manuscripts/working text must be English")

    # Contradiction scan across the repository.
    hits = 0
    for rel, path in iter_repo_text_files():
        if rel in CONTRADICTION_ALLOWLIST:
            continue
        with open(path, encoding="utf-8", errors="replace") as f:
            for lineno, line in enumerate(f, 1):
                for pattern, why, strict in CONTRADICTION_PATTERNS:
                    if re.search(pattern, line):
                        if not strict and NEGATION_CONTEXT.search(line):
                            continue
                        hits += 1
                        ok = False
                        print(f"[CONTRADICTION] {rel}:{lineno}: /{pattern}/ — {why}\n    {line.strip()[:160]}")
    print(f"contradiction scan: {hits} hit(s)")

    # Schema field-name hygiene: no language-suffixed primary fields.
    for path in glob.glob(os.path.join(ROOT, "schemas", "*.schema.json")):
        text = open(path, encoding="utf-8").read()
        for m in re.finditer(r'"([a-z_]+_ko)"\s*:', text):
            ok = False
            print(f"[STALE FIELD] {os.path.relpath(path, ROOT)}: {m.group(1)}")

    print("RESULT:", "ALL OK" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
