from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_evidence_manifest", ROOT / "scripts" / "build_evidence_manifest.py"
)
assert SPEC and SPEC.loader
producer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(producer)

VALIDATOR_SPEC = importlib.util.spec_from_file_location(
    "validate_evidence_gate", ROOT / "scripts" / "validate_evidence_gate.py"
)
assert VALIDATOR_SPEC and VALIDATOR_SPEC.loader
validator = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(validator)


class EvidenceManifestProducerTests(unittest.TestCase):
    def test_complete_observations_build_passing_manifest(self) -> None:
        source = producer.load_json(ROOT / "tests" / "fixtures" / "evidence_gate" / "source-pass.json")
        manifest = producer.build_manifest(source)
        self.assertEqual("PASS", manifest["checks"][0]["status"])
        self.assertEqual("UNVERIFIED", manifest["checks"][1]["status"])
        self.assertFalse(manifest["checks"][1]["required"])
        self.assertEqual(("PASS", []), validator.evaluate_gate(manifest))

    def test_missing_required_observations_become_unverified(self) -> None:
        source = producer.load_json(ROOT / "tests" / "fixtures" / "evidence_gate" / "source-missing.json")
        manifest = producer.build_manifest(source)
        status, reasons = validator.evaluate_gate(manifest)
        self.assertEqual("UNVERIFIED", status)
        self.assertTrue(any("unit-tests" in reason for reason in reasons))
        self.assertTrue(any("artifact-complete" in reason for reason in reasons))

    def test_unknown_observation_is_rejected(self) -> None:
        source = {
            "repository": "KAFKA2306/com",
            "revision": "3" * 40,
            "checks": [{"id": "known", "required": True}],
            "observations": [{"id": "unknown", "status": "PASS", "evidence": []}],
        }
        with self.assertRaisesRegex(ValueError, "unknown checks"):
            producer.build_manifest(source)

    def test_duplicate_observation_is_rejected(self) -> None:
        source = {
            "repository": "KAFKA2306/com",
            "revision": "4" * 40,
            "checks": [{"id": "known", "required": True}],
            "observations": [
                {"id": "known", "status": "PASS", "evidence": []},
                {"id": "known", "status": "PASS", "evidence": []},
            ],
        }
        with self.assertRaisesRegex(ValueError, "duplicate observations id"):
            producer.build_manifest(source)


if __name__ == "__main__":
    unittest.main()
