from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PASS = "PASS"
FAIL = "FAIL"
UNVERIFIED = "UNVERIFIED"
VALID_STATUSES = {PASS, FAIL, UNVERIFIED}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _index_observations(items: Any, label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(items, list):
        raise ValueError(f"{label} must be an array")
    indexed: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"{label}[{index}] must be an object")
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            raise ValueError(f"{label}[{index}].id must be a non-empty string")
        if item_id in indexed:
            raise ValueError(f"duplicate {label} id: {item_id}")
        status = item.get("status")
        if status not in VALID_STATUSES:
            raise ValueError(f"{label}[{index}].status must be PASS, FAIL, or UNVERIFIED")
        evidence = item.get("evidence", [])
        if not isinstance(evidence, list):
            raise ValueError(f"{label}[{index}].evidence must be an array")
        normalized = {"id": item_id, "status": status, "evidence": evidence}
        if "note" in item:
            if not isinstance(item["note"], str):
                raise ValueError(f"{label}[{index}].note must be a string")
            normalized["note"] = item["note"]
        indexed[item_id] = normalized
    return indexed


def _normalize_specs(items: Any, label: str, *, checks: bool) -> list[dict[str, Any]]:
    if not isinstance(items, list):
        raise ValueError(f"{label} must be an array")
    seen: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"{label}[{index}] must be an object")
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            raise ValueError(f"{label}[{index}].id must be a non-empty string")
        if item_id in seen:
            raise ValueError(f"duplicate {label} id: {item_id}")
        seen.add(item_id)
        spec: dict[str, Any] = {"id": item_id}
        if checks:
            required = item.get("required")
            if not isinstance(required, bool):
                raise ValueError(f"{label}[{index}].required must be a boolean")
            spec["required"] = required
        normalized.append(spec)
    return normalized


def build_manifest(source: Any) -> dict[str, Any]:
    if not isinstance(source, dict):
        raise ValueError("source root must be an object")
    repository = source.get("repository")
    revision = source.get("revision")
    if not isinstance(repository, str) or not repository.strip():
        raise ValueError("repository must be a non-empty string")
    if not isinstance(revision, str) or not revision.strip():
        raise ValueError("revision must be a non-empty string")

    check_specs = _normalize_specs(source.get("checks"), "checks", checks=True)
    criterion_specs = _normalize_specs(
        source.get("acceptance_criteria", []), "acceptance_criteria", checks=False
    )
    observations = _index_observations(source.get("observations", []), "observations")
    criterion_observations = _index_observations(
        source.get("criterion_observations", []), "criterion_observations"
    )

    allowed_check_ids = {item["id"] for item in check_specs}
    unknown_checks = set(observations) - allowed_check_ids
    if unknown_checks:
        raise ValueError(f"observations reference unknown checks: {sorted(unknown_checks)}")
    allowed_criteria_ids = {item["id"] for item in criterion_specs}
    unknown_criteria = set(criterion_observations) - allowed_criteria_ids
    if unknown_criteria:
        raise ValueError(
            f"criterion_observations reference unknown acceptance criteria: {sorted(unknown_criteria)}"
        )

    checks: list[dict[str, Any]] = []
    for spec in check_specs:
        observation = observations.get(spec["id"])
        item: dict[str, Any] = {
            "id": spec["id"],
            "required": spec["required"],
            "status": observation["status"] if observation else UNVERIFIED,
            "evidence": observation["evidence"] if observation else [],
        }
        if observation and "note" in observation:
            item["note"] = observation["note"]
        elif observation is None:
            item["note"] = "No observation was supplied by the producer input."
        checks.append(item)

    criteria: list[dict[str, Any]] = []
    for spec in criterion_specs:
        observation = criterion_observations.get(spec["id"])
        item = {
            "id": spec["id"],
            "status": observation["status"] if observation else UNVERIFIED,
            "evidence": observation["evidence"] if observation else [],
        }
        if observation and "note" in observation:
            item["note"] = observation["note"]
        elif observation is None:
            item["note"] = "No observation was supplied by the producer input."
        criteria.append(item)

    return {
        "schema_version": 1,
        "repository": repository,
        "revision": revision,
        "checks": checks,
        "acceptance_criteria": criteria,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build a deterministic evidence-gate manifest from declared requirements and observations."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    try:
        manifest = build_manifest(load_json(args.source))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"status": UNVERIFIED, "error": str(exc)}, ensure_ascii=False, sort_keys=True))
        return 2

    payload = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
