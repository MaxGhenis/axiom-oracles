"""The shared executable-receipt tier discriminator is fail closed."""

from __future__ import annotations

import copy

import pytest

from axiom_oracles.executable_receipt_schema import (
    ALLOWED_TIERS,
    RECEIPT_SCHEMA,
    RELEASE_RECEIPT,
    SOURCE_REPRODUCTION,
    ReceiptSchemaError,
    load_receipt_schema,
    receipt_schema_sha256,
    validate_receipt_envelope,
)


def _release_envelope() -> dict:
    return {
        "schema": RECEIPT_SCHEMA,
        "tier": RELEASE_RECEIPT,
        "program": "test/program",
        "engine": {},
        "artifact": {},
        "golden": {},
        "commands": [],
        "timestamp": "2026-08-20T00:00:00Z",
        "workflow": {},
    }


def _source_envelope() -> dict:
    return {
        "schema": RECEIPT_SCHEMA,
        "tier": SOURCE_REPRODUCTION,
        "program": "test/program",
        "generated_by": "test",
        "execution_period": "2026",
        "engine": {},
        "rulespec": {},
        "source_reports": [],
        "compiled_artifacts": [],
        "cases": [],
        "summary": {},
    }


def test_schema_file_and_python_tier_constants_agree():
    schema = load_receipt_schema()

    assert schema["$id"] == RECEIPT_SCHEMA
    assert ALLOWED_TIERS == frozenset(
        schema["$defs"][tier]["properties"]["tier"]["const"]
        for tier in ALLOWED_TIERS
    )
    assert len(receipt_schema_sha256()) == 64


@pytest.mark.parametrize(
    ("document", "required"),
    [
        (_source_envelope(), SOURCE_REPRODUCTION),
        (_release_envelope(), RELEASE_RECEIPT),
    ],
)
def test_each_tier_selects_its_exact_top_level(document: dict, required: str):
    assert validate_receipt_envelope(document, required_tier=required) == required


def test_tier_field_absent_is_rejected():
    document = _release_envelope()
    del document["tier"]

    with pytest.raises(ReceiptSchemaError, match="missing required key 'tier'"):
        validate_receipt_envelope(document, required_tier=RELEASE_RECEIPT)


def test_source_reproduction_cannot_satisfy_release_policy():
    with pytest.raises(ReceiptSchemaError, match="does not satisfy required tier"):
        validate_receipt_envelope(
            _source_envelope(),
            required_tier=RELEASE_RECEIPT,
        )


def test_tier_cannot_smuggle_fields_from_the_other_branch():
    document = copy.deepcopy(_source_envelope())
    document["artifact"] = {}

    with pytest.raises(ReceiptSchemaError, match="unknown key 'artifact'"):
        validate_receipt_envelope(document, required_tier=SOURCE_REPRODUCTION)
