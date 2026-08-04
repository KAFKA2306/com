from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_control_plane", ROOT / "scripts" / "validate_control_plane.py"
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ControlPlaneValidationTests(unittest.TestCase):
    def test_repository_tree_is_valid(self) -> None:
        self.assertEqual([], validator.validate_root(ROOT))

    def test_duplicate_canonical_domain_is_rejected(self) -> None:
        data = validator.load_json(ROOT / "registry" / "repositories.json")
        changed = copy.deepcopy(data)
        changed["repositories"][1]["canonical_for"] = ["portfolio_control"]
        errors = validator.validate_repository_registry(changed)
        self.assertTrue(any("canonical domains contains duplicates" in error for error in errors))

    def test_second_command_repository_is_rejected(self) -> None:
        data = validator.load_json(ROOT / "registry" / "repositories.json")
        changed = copy.deepcopy(data)
        changed["repositories"][1]["role"] = "command"
        errors = validator.validate_repository_registry(changed)
        self.assertTrue(any("single command repository" in error for error in errors))

    def test_active_schedule_requires_active_service(self) -> None:
        schedule_data = {
            "schema_version": 1,
            "notes": "test",
            "schedules": [
                {
                    "id": "daily-test",
                    "service_id": "test-service",
                    "timezone": "Asia/Tokyo",
                    "trigger": "daily at 07:00",
                    "executor": "chatgpt",
                    "status": "active"
                }
            ]
        }
        errors = validator.validate_schedules(
            schedule_data,
            {"test-service"},
            {"test-service": "disabled"},
            {"chatgpt"},
        )
        self.assertTrue(any("unless its service is active" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
