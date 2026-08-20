"""Shared, fail-closed envelope for tiered executable receipts.

The JSON schema is the coordination surface for certificate consumers.  This
module deliberately enforces only the schema identifier, tier policy, and the
exact top-level branch selected by that tier.  Tier-specific producers retain
their deeper semantic validators: source reproduction re-derives cases and
release receipts authenticate release manifests, commands, and Sigstore bytes.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

RECEIPT_SCHEMA = "axiom_oracles.executable_receipt.v2"
SOURCE_REPRODUCTION = "source_reproduction"
RELEASE_RECEIPT = "release_receipt"
ALLOWED_TIERS = frozenset((SOURCE_REPRODUCTION, RELEASE_RECEIPT))

DEFAULT_SCHEMA_PATH = Path("certificates/executable/receipt.schema.json")
DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[1]


class ReceiptSchemaError(ValueError):
    """A receipt or the shared schema fails the executable envelope contract."""


def receipt_schema_sha256(
    *,
    repo_root: str | Path = DEFAULT_REPO_ROOT,
    schema_path: str | Path = DEFAULT_SCHEMA_PATH,
) -> str:
    """Return the raw-byte digest consumers can pin beside their trust roots."""

    path = _schema_path(repo_root, schema_path)
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        raise ReceiptSchemaError(
            f"receipt schema: cannot read {path} (errno {error.errno})"
        ) from error


def load_receipt_schema(
    *,
    repo_root: str | Path = DEFAULT_REPO_ROOT,
    schema_path: str | Path = DEFAULT_SCHEMA_PATH,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    """Load the strict schema and prove its two discriminators match constants."""

    path = _schema_path(repo_root, schema_path)
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise ReceiptSchemaError(
            f"receipt schema: cannot read {path} (errno {error.errno})"
        ) from error
    digest = hashlib.sha256(raw).hexdigest()
    if expected_sha256 is not None and digest != expected_sha256:
        raise ReceiptSchemaError(
            "receipt schema: raw bytes do not match the configured SHA-256"
        )
    try:
        document = json.loads(
            raw,
            object_pairs_hook=_object_without_duplicate_keys,
            parse_constant=_reject_non_json_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ReceiptSchemaError(f"receipt schema: invalid JSON ({error})") from error
    if _contains_nonfinite_number(document):
        raise ReceiptSchemaError("receipt schema: non-finite number")
    if type(document) is not dict or document.get("$id") != RECEIPT_SCHEMA:
        raise ReceiptSchemaError(
            f"receipt schema: $id must be {RECEIPT_SCHEMA!r}"
        )
    definitions = document.get("$defs")
    if type(definitions) is not dict:
        raise ReceiptSchemaError("receipt schema: $defs must be an object")
    observed: set[str] = set()
    for tier in ALLOWED_TIERS:
        branch = definitions.get(tier)
        properties = branch.get("properties") if type(branch) is dict else None
        tier_property = properties.get("tier") if type(properties) is dict else None
        if type(tier_property) is not dict or tier_property.get("const") != tier:
            raise ReceiptSchemaError(
                f"receipt schema: $defs.{tier}.properties.tier must select {tier!r}"
            )
        observed.add(tier_property["const"])
    if observed != set(ALLOWED_TIERS):
        raise ReceiptSchemaError("receipt schema: tier discriminator set drifted")
    return document


def validate_receipt_envelope(
    document: Any,
    *,
    required_tier: str | None = None,
    repo_root: str | Path = DEFAULT_REPO_ROOT,
    schema_path: str | Path = DEFAULT_SCHEMA_PATH,
    expected_schema_sha256: str | None = None,
    label: str = "receipt",
) -> str:
    """Validate the shared exact top level and consumer-owned tier policy.

    ``required_tier`` is trusted policy supplied by the consumer.  It is an
    equality requirement, not a ranking: a source reproduction receipt never
    satisfies a release receipt requirement.
    """

    if required_tier is not None and required_tier not in ALLOWED_TIERS:
        raise ReceiptSchemaError(
            f"required tier {required_tier!r} is not a recognized executable tier"
        )
    schema = load_receipt_schema(
        repo_root=repo_root,
        schema_path=schema_path,
        expected_sha256=expected_schema_sha256,
    )
    if type(document) is not dict:
        raise ReceiptSchemaError(f"{label}: must be a JSON object")

    schema_value = document.get("schema")
    if schema_value != RECEIPT_SCHEMA:
        raise ReceiptSchemaError(
            f"{label}.schema: expected {RECEIPT_SCHEMA!r}, got {schema_value!r}"
        )
    if "tier" not in document:
        raise ReceiptSchemaError(f"{label}: missing required key 'tier'")
    tier = document["tier"]
    if type(tier) is not str or tier not in ALLOWED_TIERS:
        raise ReceiptSchemaError(
            f"{label}.tier: must be one of {sorted(ALLOWED_TIERS)!r}"
        )
    if required_tier is not None and tier != required_tier:
        raise ReceiptSchemaError(
            f"{label}.tier: {tier!r} does not satisfy required tier "
            f"{required_tier!r}"
        )

    branch = schema["$defs"][tier]
    required = branch.get("required")
    properties = branch.get("properties")
    if type(required) is not list or not all(type(key) is str for key in required):
        raise ReceiptSchemaError(f"receipt schema: $defs.{tier}.required is invalid")
    if type(properties) is not dict or branch.get("additionalProperties") is not False:
        raise ReceiptSchemaError(
            f"receipt schema: $defs.{tier} must declare an exact property set"
        )
    for key in required:
        if key not in document:
            raise ReceiptSchemaError(f"{label}: missing required key {key!r}")
    unknown = sorted(set(document) - set(properties), key=str)
    if unknown:
        raise ReceiptSchemaError(f"{label}: unknown key {unknown[0]!r}")
    return tier


def _schema_path(repo_root: str | Path, schema_path: str | Path) -> Path:
    root = Path(repo_root).resolve()
    candidate = Path(schema_path)
    path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    try:
        path.relative_to(root)
    except ValueError as error:
        raise ReceiptSchemaError("receipt schema path escapes the repository root") from error
    return path


def _object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key {key!r}")
        result[key] = value
    return result


def _reject_non_json_constant(value: str) -> Any:
    raise ValueError(f"non-JSON numeric constant {value!r}")


def _contains_nonfinite_number(value: Any) -> bool:
    if type(value) is float:
        return not math.isfinite(value)
    if type(value) is list:
        return any(_contains_nonfinite_number(item) for item in value)
    if type(value) is dict:
        return any(_contains_nonfinite_number(item) for item in value.values())
    return False
