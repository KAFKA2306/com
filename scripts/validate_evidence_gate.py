from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PASS = "PASS"
FAIL = "FAIL"
UNVERIFIED = "UNVERIFIED"
EXIT_CODES = {PASS: 0, FAIL: 1, UNVERIFIED: 2}
REVISION_RE = re.compile(r"^(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
REPOSITORY_RE = re.compile(r"^[^/\s]+/[^/\s]+$")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _validate_evidence(evidence: Any, prefix: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(evidence, list):
        return [f"{prefix}.evidence must be an array"]

    for index, item in enumerate(evidence):
        item_prefix = f"{prefix}.evidence[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_prefix} must be an object")
            continue

        allowed = {"url", "path", "sha256", "note"}
        extra = set(item) - allowed
        if extra:
            errors.append(f"{item_prefix} has unsupported keys: {sorted(extra)}")

        has_url = isinstance(item.get("url"), str) and bool(item["url"].strip())
        has_path = isinstance(item.get("path"), str) and bool(item["path"].strip())
        if has_url == has_path:
            errors.append(f"{item_prefix} must contain exactly one of url or path")

        if "sha256" in item:
            sha256 = item["sha256"]
            if not isinstance(sha256, str) or not SHA256_RE.fullmatch(sha256):
                errors.append(f"{item_prefix}.sha256 must be 64 hexadecimal characters")

        if "note" in item and not isinstance(item["note"], str):
            errors.append(f"{item_prefix}.note must be a string")

    return errors


def _validate_gate_item(item: Any, prefix: str, *, criterion: bool) -> list[str]:
    errors: list[str] = []
    if not isinstance(item, dict):
        return [f"{prefix} must be an object"]

    allowed = {"id", "status", "evidence", "note"}
    if not criterion:
        allowed.add("required")
    extra = set(item) - allowed
    if extra:
        errors.append(f"{prefix} has unsupported keys: {sorted(extra)}")

    item_id = item.get("id")
    if not isinstance(item_id, str) or not item_id.strip():
        errors.append(f"{prefix}.id must be a non-empty string")

    if not criterion and not isinstance(item.get("required"), bool):
        errors.append(f"{prefix}.required must be a boolean")

    status = item.get("status")
    if status not in {PASS, FAIL, UNVERIFIED}:
        errors.append(f"{prefix}.status must be PASS, FAIL, or UNVERIFIED")

    errors.extend(_validate_evidence(item.get("evidence"), prefix))

    if "note" in item and not isinstance(item["note"], str):
        errors.append(f"{prefix}.note must be a string")

    return errors


def validate_manifest(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest root must be an object"]

    allowed = {"schema_version", "repository", "revision", "checks", "acceptance_criteria"}
    extra = set(data) - allowed
    if extra:
        errors.append(f"manifest has unsupported keys: {sorted(extra)}")

    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    repository = data.get("repository")
    if not isinstance(repository, str) or not REPOSITORY_RE.fullmatch(repository):
        errors.append("repository must use owner/name form")

    revision = data.get("revision")
    if not isinstance(revision, str) or not REVISION_RE.fullmatch(revision):
        errors.append("revision must be an exact 40- or 64-character hexadecimal commit SHA")

    checks = data.get("checks")
    if not isinstance(checks, list) or not checks:
        errors.append("checks must be a non-empty array")
        checks = []

    criteria = data.get("acceptance_criteria", [])
    if not isinstance(criteria, list):
        errors.append("acceptance_criteria must be an array")
        criteria = []

    seen_ids: set[str] = set()
    for index, item in enumerate(checks):
        prefix = f"checks[{index}]"
        errors.extend(_validate_gate_item(item, prefix, criterion=False))
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            item_id = item["id"].strip()
            if item_id in seen_ids:
                errors.append(f"duplicate gate item id: {item_id}")
            elif item_id:
                seen_ids.add(item_id)

    for index, item in enumerate(criteria):
        prefix = f"acceptance_criteria[{index}]"
        errors.extend(_validate_gate_item(item, prefix, criterion=True))
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            item_id = item["id"].strip()
            if item_id in seen_ids:
                errors.append(f"duplicate gate item id: {item_id}")
            elif item_id:
                seen_ids.add(item_id)

    return errors


def evaluate_gate(data: Any) -> tuple[str, list[str]]:
    validation_errors = validate_manifest(data)
    if validation_errors:
        return UNVERIFIED, validation_errors

    checks = data["checks"]
    criteria = data.get("acceptance_criteria", [])
    all_items: list[tuple[str, dict[str, Any], bool]] = []

    for item in checks:
        all_items.append((item["id"], item, item["required"]))
    for item in criteria:
        all_items.append((item["id"], item, True))

    failed = [item_id for item_id, item, _ in all_items if item["status"] == FAIL]
    if failed:
        return FAIL, [f"failed item: {item_id}" for item_id in failed]

    reasons: list[str] = []
    for item_id, item, required in all_items:
        if not required:
            continue
        if item["status"] != PASS:
            reasons.append(f"required item is not PASS: {item_id} ({item['status']})")
        if not item["evidence"]:
            reasons.append(f"required item has no evidence: {item_id}")

    if reasons:
        return UNVERIFIED, reasons
    return PASS, []


def _result_payload(data: Any, status: str, reasons: list[str]) -> dict[str, Any]:
    repository = data.get("repository") if isinstance(data, dict) else None
    revision = data.get("revision") if isinstance(data, dict) else None
    return {
        "gate_status": status,
        "repository": repository,
        "revision": revision,
        "reasons": reasons,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate and evaluate a KAFKA2306 evidence-gate manifest."
    )
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args(argv)

    try:
        data = load_json(args.manifest)
    except (OSError, json.JSONDecodeError) as exc:
        payload = _result_payload({}, UNVERIFIED, [str(exc)])
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return EXIT_CODES[UNVERIFIED]

    status, reasons = evaluate_gate(data)
    print(json.dumps(_result_payload(data, status, reasons), ensure_ascii=False, sort_keys=True))
    return EXIT_CODES[status]


if __name__ == "__main__":
    sys.exit(main())
