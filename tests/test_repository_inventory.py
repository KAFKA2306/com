import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "audit_repository_inventory.py"
spec = importlib.util.spec_from_file_location("inventory", MODULE_PATH)
inv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inv)


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.registry = {
            "repositories": [
                {"id": "KAFKA2306/com", "role": "command", "canonical_for": ["portfolio_control"]}
            ]
        }
        self.decisions = {
            "repositories": [
                {
                    "repository_id": 1,
                    "expected_full_name": "KAFKA2306/com",
                    "disposition": "managed",
                    "reason": "control plane",
                    "reviewed_at": "2026-08-10",
                    "review_due_at": "2026-11-10",
                    "expected_visibility": "public",
                    "expected_archived": False,
                    "expected_capabilities": {
                        "issues": True,
                        "actions": True,
                        "pages": True,
                        "pull_requests": True,
                    },
                }
            ]
        }
        self.base = {
            "repository_id": 1,
            "full_name": "KAFKA2306/com",
            "visibility": "public",
            "archived": False,
            "capabilities": {"issues": True, "actions": True, "pages": True, "pull_requests": True},
            "retrieved_at": "2026-08-10T00:00:00Z",
        }

    def test_new_rename_archive_visibility_and_capability(self):
        renamed = dict(
            self.base,
            full_name="KAFKA2306/com-renamed",
            visibility="private",
            archived=True,
            capabilities={"issues": False, "actions": True, "pages": True, "pull_requests": True},
        )
        new = dict(self.base, repository_id=2, full_name="KAFKA2306/new-repo")
        types = [d["type"] for d in inv.classify(self.registry, self.decisions, [renamed, new])]
        self.assertEqual(
            types,
            ["archived_changed", "capability_changed", "new", "renamed", "visibility_changed"],
        )

    def test_private_names_are_redacted_from_public_output(self):
        private = dict(
            self.base,
            repository_id=2,
            full_name="KAFKA2306/secret-name",
            visibility="private",
        )
        public = inv.publicize(
            [{"type": "new", "repository_id": 2, "full_name": "KAFKA2306/secret-name"}],
            [private],
        )
        encoded = json.dumps(public)
        self.assertNotIn("secret-name", encoded)
        self.assertEqual(
            public,
            [{"type": "unclassified", "private_repository_changes_redacted": 1}],
        )

    def test_api_failure_is_not_empty_success(self):
        client = inv.GitHubClient("token", "https://example.invalid")
        with mock.patch.object(client, "get_json", side_effect=inv.AuditError("rate limited")):
            with self.assertRaises(inv.AuditError):
                client.list_owned("KAFKA2306", "2026-08-10T00:00:00Z")

    def test_decisions_do_not_mutate_canonical_registry(self):
        before = json.dumps(self.registry, sort_keys=True)
        inv.classify(self.registry, self.decisions, [self.base])
        self.assertEqual(json.dumps(self.registry, sort_keys=True), before)

    def test_fixture_cli_writes_private_snapshot_and_public_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "registry.json").write_text(json.dumps(self.registry), encoding="utf-8")
            (root / "decisions.json").write_text(json.dumps(self.decisions), encoding="utf-8")
            (root / "fixture.json").write_text(
                json.dumps({"repositories": [self.base]}), encoding="utf-8"
            )
            output = root / "out"
            rc = inv.main(
                [
                    "--registry",
                    str(root / "registry.json"),
                    "--decisions",
                    str(root / "decisions.json"),
                    "--fixture",
                    str(root / "fixture.json"),
                    "--output-dir",
                    str(output),
                    "--retrieved-at",
                    "2026-08-10T00:00:00Z",
                ]
            )
            self.assertEqual(rc, 0)
            self.assertTrue((output / "snapshot.private.json").exists())
            self.assertEqual(
                json.loads((output / "candidate.public.json").read_text())["differences"], []
            )


if __name__ == "__main__":
    unittest.main()
