#!/usr/bin/env python3
"""Planning-package consistency check (not application code).

Validates every schema in schemas/ against the JSON Schema 2020-12 metaschema, validates the example
instances in examples/ against their schemas, and enforces the evidence-span invariant
(end - start == len(quote) in code points) that the future DB trigger will enforce.

Usage:  python tools/validate-planning-package.py
Deps:   jsonschema>=4.18 (pip install jsonschema)
"""
from __future__ import annotations

import glob
import json
import os
import sys

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URI = "https://yeonjae.studio/schemas/"

EXAMPLES = [
    ("examples/fixture/story-intake.json", "story-intake.schema.json"),
    ("examples/fixture/speech-profile.seoha.json", "speech-profile.schema.json"),
    ("examples/fixture/chapter-contract.ch12.json", "chapter-contract.schema.json"),
    ("examples/fixture/canon-delta.ch09.json", "canon-delta.schema.json"),
    ("examples/style-profiles/kr-webnovel-base.v1.json", "style-profile.schema.json"),
    ("examples/style-profiles/genre-hunter-gate.v1.json", "style-profile.schema.json"),
]

PAYLOAD_SCHEMAS = {
    "fact": "fact.schema.json",
    "event": "event.schema.json",
    "knowledge_state": "knowledge-state.schema.json",
    "relationship_state": "relationship-state.schema.json",
}


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

    # Evidence-span invariant.
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

    print("RESULT:", "ALL OK" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
