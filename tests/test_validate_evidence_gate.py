from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_evidence_gate", ROOT / "scripts" / "validate_evidence_gate.py"
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


BASE_MANIFEST = {
    "schema_version": 1,
    "repository": "KAFKA2306/com",
    "revision": "e42cc5cd32cdff8ace3402a719be0862dcca62c0",
    "checks": [
        {
            "id": "unit-tests",
            "required": True,
            "status": "PASS",
            "evidence": [
                {"url": "https://github.com/KAFKA2306/com/actions/runs/1"}
            ],
        },
        {
            "id": "optional-note",
            "required": False,
            "status": "UNVERIFIED",
            "evidence": [],
        },
    ],
    "acceptance_criteria": [
        {
            "id": "exact-revision",
            "status": "PASS",
            "evidence": [{"path": "artifacts/revision.txt"}],
        }
    ],
}


class EvidenceGateTests(unittest.TestCase):
    def test_all_required_items_pass(self) -> None:
        status, reasons = validator.evaluate_gate(copy.deepcopy(BASE_MANIFEST))
        self.assertEqual("PASS", status)
        self.assertEqual([], reasons)

    def test_required_pass_without_evidence_is_unverified(self) -> None:
        manifest = copy.deepcopy(BASE_MANIFEST)
        manifest["checks"][0]["evidence"] = []
        status, reasons = validator.evaluate_gate(manifest)
        self.assertEqual("UNVERIFIED", status)
        self.assertTrue(any("no evidence" in reason for reason in reasons))

    def test_any_explicit_fail_fails_gate(self) -> None:
        manifest = copy.deepcopy(BASE_MANIFEST)
        manifest["checks"][1]["status"] = "FAIL"
        status, reasons = validator.evaluate_gate(manifest)
        self.assertEqual("FAIL", status)
        self.assertTrue(any("optional-note" in reason for reason in reasons))

    def test_required_unverified_stays_unverified(self) -> None:
        manifest = copy.deepcopy(BASE_MANIFEST)
        manifest["acceptance_criteria"][0]["status"] = "UNVERIFIED"
        status, reasons = validator.evaluate_gate(manifest)
        self.assertEqual("UNVERIFIED", status)
        self.assertTrue(any("exact-revision" in reason for reason in reasons))

    def test_duplicate_item_id_is_unverified(self) -> None:
        manifest = copy.deepcopy(BASE_MANIFEST)
        manifest["acceptance_criteria"][0]["id"] = "unit-tests"
        status, reasons = validator.evaluate_gate(manifest)
        self.assertEqual("UNVERIFIED", status)
        self.assertTrue(any("duplicate gate item id" in reason for reason in reasons))


if __name__ == "__main__":
    unittest.main()
