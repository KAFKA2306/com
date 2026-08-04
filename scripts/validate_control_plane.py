#!/usr/bin/env python3
"""Validate the KAFKA COM control-plane contract with the Python standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO_ID = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")
ALLOWED_ROLES = {"command", "shared-resource", "domain", "archive"}
ALLOWED_VISIBILITY = {"public", "private", "review-required"}
ALLOWED_EXECUTOR_CLASSES = {"orchestrator", "repository_executor", "machine_executor"}
ALLOWED_SERVICE_STATUS = {"proposed", "disabled", "active", "paused", "retired"}
ALLOWED_SCHEDULE_STATUS = {"disabled", "active", "paused", "retired"}
REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "GOVERNANCE.md",
    "SECURITY.md",
    "policies/completion.md",
    "policies/evidence.md",
    "policies/repository-boundaries.md",
    "policies/destructive-actions.md",
    "instructions/chatgpt-operations.md",
    "registry/repositories.json",
    "registry/services.json",
    "registry/schedules.json",
    "registry/capabilities.json",
    "schemas/repository.schema.json",
    "schemas/service.schema.json",
    "schemas/schedule.schema.json",
    ".github/ISSUE_TEMPLATE/directive.yml",
    ".github/ISSUE_TEMPLATE/recurring-service.yml",
    ".github/ISSUE_TEMPLATE/incident.yml",
    ".github/ISSUE_TEMPLATE/decision.yml",
)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _unique(values: list[str], label: str, errors: list[str]) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        errors.append(f"{label} contains duplicates: {', '.join(duplicates)}")


def validate_repository_registry(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["repository registry must be an object"]
    if data.get("schema_version") != 1:
        errors.append("repository registry schema_version must be 1")
    repositories = data.get("repositories")
    if not isinstance(repositories, list) or not repositories:
        return errors + ["repository registry must contain a non-empty repositories array"]

    ids: list[str] = []
    canonical_domains: list[str] = []
    command_ids: list[str] = []
    for index, entry in enumerate(repositories):
        prefix = f"repositories[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        repo_id = entry.get("id")
        if not isinstance(repo_id, str) or not REPO_ID.fullmatch(repo_id):
            errors.append(f"{prefix}.id must use owner/repository form")
        else:
            ids.append(repo_id)
        role = entry.get("role")
        if role not in ALLOWED_ROLES:
            errors.append(f"{prefix}.role is invalid")
        if role == "command" and isinstance(repo_id, str):
            command_ids.append(repo_id)
        if entry.get("visibility_class") not in ALLOWED_VISIBILITY:
            errors.append(f"{prefix}.visibility_class is invalid")
        purpose = entry.get("purpose")
        if not isinstance(purpose, str) or len(purpose.strip()) < 10:
            errors.append(f"{prefix}.purpose must be descriptive")
        capabilities = entry.get("capabilities")
        if not isinstance(capabilities, list) or not all(isinstance(item, str) and item for item in capabilities):
            errors.append(f"{prefix}.capabilities must be a string array")
        elif len(capabilities) != len(set(capabilities)):
            errors.append(f"{prefix}.capabilities must be unique")
        canonical_for = entry.get("canonical_for")
        if not isinstance(canonical_for, list) or not canonical_for or not all(
            isinstance(item, str) and item for item in canonical_for
        ):
            errors.append(f"{prefix}.canonical_for must be a non-empty string array")
        else:
            canonical_domains.extend(canonical_for)

    _unique(ids, "repository ids", errors)
    _unique(canonical_domains, "canonical domains", errors)
    if command_ids != ["KAFKA2306/com"]:
        errors.append("KAFKA2306/com must be the single command repository")
    return errors


def validate_capabilities(data: Any) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return ["capability registry must be an object with schema_version 1"], set()
    executors = data.get("executors")
    if not isinstance(executors, list) or not executors:
        return ["capability registry must contain executors"], set()
    ids: list[str] = []
    for index, entry in enumerate(executors):
        prefix = f"executors[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        executor_id = entry.get("id")
        if not isinstance(executor_id, str) or not SLUG.fullmatch(executor_id):
            errors.append(f"{prefix}.id must be a lowercase slug")
        else:
            ids.append(executor_id)
        if entry.get("class") not in ALLOWED_EXECUTOR_CLASSES:
            errors.append(f"{prefix}.class is invalid")
        for key in ("capabilities", "restrictions"):
            value = entry.get(key)
            if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
                errors.append(f"{prefix}.{key} must be a non-empty string array")
    _unique(ids, "executor ids", errors)
    return errors, set(ids)


def validate_services(data: Any, repository_ids: set[str], executor_ids: set[str]) -> tuple[list[str], set[str], dict[str, str]]:
    errors: list[str] = []
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return ["service registry must be an object with schema_version 1"], set(), {}
    services = data.get("services")
    if not isinstance(services, list):
        return ["service registry services must be an array"], set(), {}
    ids: list[str] = []
    statuses: dict[str, str] = {}
    for index, entry in enumerate(services):
        prefix = f"services[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        service_id = entry.get("id")
        if not isinstance(service_id, str) or not SLUG.fullmatch(service_id):
            errors.append(f"{prefix}.id must be a lowercase slug")
        else:
            ids.append(service_id)
            statuses[service_id] = str(entry.get("status"))
        work_item = entry.get("work_item")
        if not isinstance(work_item, str) or not work_item.startswith("https://github.com/KAFKA2306/com/issues/"):
            errors.append(f"{prefix}.work_item must reference a com issue")
        targets = entry.get("targets")
        if not isinstance(targets, list) or not targets:
            errors.append(f"{prefix}.targets must be non-empty")
        else:
            unknown = sorted(set(targets) - repository_ids)
            if unknown:
                errors.append(f"{prefix}.targets contain unknown repositories: {', '.join(unknown)}")
        if entry.get("executor") not in executor_ids:
            errors.append(f"{prefix}.executor is not registered")
        if entry.get("status") not in ALLOWED_SERVICE_STATUS:
            errors.append(f"{prefix}.status is invalid")
        for key in ("purpose", "evidence_policy", "failure_policy"):
            if not isinstance(entry.get(key), str) or len(entry[key].strip()) < 5:
                errors.append(f"{prefix}.{key} must be descriptive")
    _unique(ids, "service ids", errors)
    return errors, set(ids), statuses


def validate_schedules(data: Any, service_ids: set[str], service_statuses: dict[str, str], executor_ids: set[str]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return ["schedule registry must be an object with schema_version 1"]
    schedules = data.get("schedules")
    if not isinstance(schedules, list):
        return ["schedule registry schedules must be an array"]
    ids: list[str] = []
    for index, entry in enumerate(schedules):
        prefix = f"schedules[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        schedule_id = entry.get("id")
        if not isinstance(schedule_id, str) or not SLUG.fullmatch(schedule_id):
            errors.append(f"{prefix}.id must be a lowercase slug")
        else:
            ids.append(schedule_id)
        service_id = entry.get("service_id")
        if service_id not in service_ids:
            errors.append(f"{prefix}.service_id is not registered")
        if entry.get("executor") not in executor_ids:
            errors.append(f"{prefix}.executor is not registered")
        status = entry.get("status")
        if status not in ALLOWED_SCHEDULE_STATUS:
            errors.append(f"{prefix}.status is invalid")
        if status == "active" and service_statuses.get(str(service_id)) != "active":
            errors.append(f"{prefix} cannot be active unless its service is active")
        timezone = entry.get("timezone")
        trigger = entry.get("trigger")
        if not isinstance(timezone, str) or "/" not in timezone:
            errors.append(f"{prefix}.timezone must be an IANA timezone")
        if not isinstance(trigger, str) or len(trigger.strip()) < 3:
            errors.append(f"{prefix}.trigger must be descriptive")
    _unique(ids, "schedule ids", errors)
    return errors


def validate_issue_forms(root: Path) -> list[str]:
    errors: list[str] = []
    required_markers = {
        "directive.yml": ("name:", "description:", "body:", "Acceptance criteria", "Required evidence"),
        "recurring-service.yml": ("name:", "description:", "body:", "Cadence or condition", "Failure handling"),
        "incident.yml": ("name:", "description:", "body:", "Observed impact", "Evidence"),
        "decision.yml": ("name:", "description:", "body:", "Alternatives", "Consequences"),
    }
    base = root / ".github" / "ISSUE_TEMPLATE"
    for filename, markers in required_markers.items():
        path = base / filename
        if not path.is_file():
            errors.append(f"missing issue form: {path.relative_to(root)}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{path.relative_to(root)} is missing marker: {marker}")
    return errors


def validate_root(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    json_paths = sorted((root / "registry").glob("*.json")) + sorted((root / "schemas").glob("*.json"))
    loaded: dict[Path, Any] = {}
    for path in json_paths:
        try:
            loaded[path] = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON in {path.relative_to(root)}: {exc}")

    repository_data = loaded.get(root / "registry" / "repositories.json")
    capability_data = loaded.get(root / "registry" / "capabilities.json")
    service_data = loaded.get(root / "registry" / "services.json")
    schedule_data = loaded.get(root / "registry" / "schedules.json")

    if repository_data is not None:
        errors.extend(validate_repository_registry(repository_data))
        repository_ids = {entry.get("id") for entry in repository_data.get("repositories", []) if isinstance(entry, dict)}
    else:
        repository_ids = set()

    if capability_data is not None:
        capability_errors, executor_ids = validate_capabilities(capability_data)
        errors.extend(capability_errors)
    else:
        executor_ids = set()

    if service_data is not None:
        service_errors, service_ids, service_statuses = validate_services(service_data, repository_ids, executor_ids)
        errors.extend(service_errors)
    else:
        service_ids, service_statuses = set(), {}

    if schedule_data is not None:
        errors.extend(validate_schedules(schedule_data, service_ids, service_statuses, executor_ids))

    errors.extend(validate_issue_forms(root))
    return errors


def main() -> int:
    errors = validate_root()
    if errors:
        print("KAFKA COM validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("KAFKA COM validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
