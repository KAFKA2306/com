#!/usr/bin/env python3
"""Audit KAFKA2306 repository inventory without mutating the canonical registry."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API = "https://api.github.com"
DIFF_TYPES = {"new", "missing", "renamed", "visibility_changed", "archived_changed", "capability_changed", "unclassified"}
DISPOSITIONS = {"managed", "observed", "excluded", "pending_review"}


class AuditError(RuntimeError):
    pass


class GitHubClient:
    def __init__(self, token: str, api_url: str = API) -> None:
        if not token:
            raise AuditError("GitHub token is required; refusing to treat an unauthenticated/partial inventory as complete")
        self.token = token
        self.api_url = api_url.rstrip("/")

    def get_json(self, path: str) -> tuple[Any, dict[str, str]]:
        req = urllib.request.Request(
            f"{self.api_url}{path}",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "KAFKA2306-com-repository-inventory",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
                return payload, {k.lower(): v for k, v in response.headers.items()}
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:500]
            raise AuditError(f"GitHub API failed: HTTP {exc.code}: {body}") from exc
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise AuditError(f"GitHub API failed: {exc}") from exc

    def list_owned(self, owner: str, retrieved_at: str) -> list[dict[str, Any]]:
        repos: list[dict[str, Any]] = []
        page = 1
        while True:
            query = urllib.parse.urlencode(
                {
                    "affiliation": "owner",
                    "visibility": "all",
                    "sort": "full_name",
                    "direction": "asc",
                    "per_page": 100,
                    "page": page,
                }
            )
            payload, headers = self.get_json(f"/user/repos?{query}")
            if not isinstance(payload, list):
                raise AuditError("GitHub API returned a non-list repository inventory")
            for raw in payload:
                if raw.get("owner", {}).get("login", "").lower() != owner.lower():
                    continue
                actions_payload, _ = self.get_json(f"/repos/{raw['full_name']}/actions/permissions")
                repos.append(normalize_repository(raw, retrieved_at, bool(actions_payload.get("enabled"))))
            if len(payload) < 100:
                break
            if headers.get("x-ratelimit-remaining") == "0":
                raise AuditError("GitHub API rate limit exhausted before inventory completed")
            page += 1
        return sorted(repos, key=lambda item: (item["full_name"].casefold(), item["repository_id"]))


def normalize_repository(raw: dict[str, Any], retrieved_at: str, actions_enabled: bool) -> dict[str, Any]:
    required = ["id", "full_name", "visibility", "archived", "disabled", "fork", "default_branch", "updated_at"]
    missing = [key for key in required if key not in raw]
    if missing:
        raise AuditError(f"repository payload missing fields: {', '.join(missing)}")
    return {
        "repository_id": int(raw["id"]),
        "full_name": str(raw["full_name"]),
        "visibility": str(raw["visibility"]),
        "archived": bool(raw["archived"]),
        "disabled": bool(raw["disabled"]),
        "fork": bool(raw["fork"]),
        "default_branch": raw["default_branch"],
        "capabilities": {
            "issues": bool(raw.get("has_issues", False)),
            "pull_requests": bool(raw.get("has_pull_requests", True)),
            "actions": actions_enabled,
            "pages": bool(raw.get("has_pages", False)),
        },
        "updated_at": str(raw["updated_at"]),
        "retrieved_at": retrieved_at,
    }


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def classify(registry: dict[str, Any], decisions: dict[str, Any], live: list[dict[str, Any]]) -> list[dict[str, Any]]:
    canonical_names = {entry["id"] for entry in registry["repositories"]}
    decision_by_id = {int(e["repository_id"]): e for e in decisions["repositories"]}
    live_by_id = {int(e["repository_id"]): e for e in live}
    live_by_name = {e["full_name"]: e for e in live}
    diffs: list[dict[str, Any]] = []

    for repo_id, decision in sorted(decision_by_id.items()):
        expected_name = decision["expected_full_name"]
        current = live_by_id.get(repo_id)
        if current is None:
            diffs.append({"type": "missing", "repository_id": repo_id, "expected_full_name": expected_name})
            continue
        if current["full_name"] != expected_name:
            diffs.append(
                {
                    "type": "renamed",
                    "repository_id": repo_id,
                    "expected_full_name": expected_name,
                    "current_full_name": current["full_name"],
                }
            )
        if current["visibility"] != decision["expected_visibility"]:
            diffs.append(
                {
                    "type": "visibility_changed",
                    "repository_id": repo_id,
                    "expected": decision["expected_visibility"],
                    "current": current["visibility"],
                }
            )
        if current["archived"] != decision["expected_archived"]:
            diffs.append(
                {
                    "type": "archived_changed",
                    "repository_id": repo_id,
                    "expected": decision["expected_archived"],
                    "current": current["archived"],
                }
            )
        expected_caps = decision.get("expected_capabilities", {})
        changed = {
            key: {"expected": value, "current": current["capabilities"].get(key)}
            for key, value in expected_caps.items()
            if current["capabilities"].get(key) != value
        }
        if changed:
            diffs.append({"type": "capability_changed", "repository_id": repo_id, "changes": changed})

    decided_ids = set(decision_by_id)
    for current in live:
        if current["repository_id"] not in decided_ids:
            diffs.append(
                {
                    "type": "new" if current["full_name"] not in canonical_names else "unclassified",
                    "repository_id": current["repository_id"],
                    "full_name": current["full_name"],
                    "disposition": "pending_review",
                }
            )

    for name in sorted(canonical_names):
        if name not in live_by_name and not any(d.get("expected_full_name") == name for d in diffs):
            diffs.append(
                {
                    "type": "unclassified",
                    "full_name": name,
                    "reason": "canonical entry has no stable repository identity decision",
                }
            )
    assert all(item["type"] in DIFF_TYPES for item in diffs)
    return sorted(
        diffs,
        key=lambda item: (
            item["type"],
            str(item.get("repository_id", "")),
            item.get("full_name", item.get("expected_full_name", "")),
        ),
    )


def validate_decisions(data: dict[str, Any]) -> None:
    seen: set[int] = set()
    for entry in data.get("repositories", []):
        rid = int(entry["repository_id"])
        if rid in seen:
            raise AuditError(f"duplicate repository_id in decisions: {rid}")
        seen.add(rid)
        if entry.get("disposition") not in DISPOSITIONS:
            raise AuditError(f"invalid disposition for repository_id {rid}")
        for key in ("reason", "reviewed_at", "review_due_at", "expected_full_name"):
            if not entry.get(key):
                raise AuditError(f"missing {key} for repository_id {rid}")


def publicize(diffs: list[dict[str, Any]], live: list[dict[str, Any]]) -> list[dict[str, Any]]:
    visibility = {r["repository_id"]: r["visibility"] for r in live}
    safe: list[dict[str, Any]] = []
    private_count = 0
    for item in diffs:
        rid = item.get("repository_id")
        if rid is not None and visibility.get(rid) == "private":
            private_count += 1
            continue
        safe.append(item)
    if private_count:
        safe.append({"type": "unclassified", "private_repository_changes_redacted": private_count})
    return safe


def render_report(diffs: list[dict[str, Any]], retrieved_at: str) -> str:
    lines = [
        "# Repository inventory audit",
        "",
        f"Retrieved at: `{retrieved_at}`",
        "",
        f"Public-safe differences: **{len(diffs)}**",
        "",
    ]
    if not diffs:
        lines.append("No differences detected.")
    else:
        lines += ["| Type | Repository | Detail |", "|---|---|---|"]
        for item in diffs:
            repo = (
                item.get("current_full_name")
                or item.get("full_name")
                or item.get("expected_full_name")
                or "(redacted)"
            )
            detail = json.dumps(
                {k: v for k, v in item.items() if k not in {"type", "full_name", "current_full_name", "expected_full_name"}},
                ensure_ascii=False,
                sort_keys=True,
            )
            lines.append(f"| `{item['type']}` | `{repo}` | `{detail}` |")
    lines += [
        "",
        "> API取得結果は候補であり、`registry/repositories.json` の `role` / `canonical_for` を自動変更しません。",
        "",
    ]
    return "\n".join(lines)


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="registry/repositories.json")
    parser.add_argument("--decisions", default="registry/repository-inventory-decisions.json")
    parser.add_argument("--output-dir", default="repository-inventory-audit")
    parser.add_argument("--owner", default="KAFKA2306")
    parser.add_argument("--fixture")
    parser.add_argument("--retrieved-at")
    args = parser.parse_args(argv)
    retrieved_at = args.retrieved_at or dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    registry = load_json(Path(args.registry))
    decisions = load_json(Path(args.decisions))
    validate_decisions(decisions)
    if args.fixture:
        live = load_json(Path(args.fixture))["repositories"]
    else:
        token = os.environ.get("KAFKA_GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
        live = GitHubClient(token).list_owned(args.owner, retrieved_at)
    diffs = classify(registry, decisions, live)
    safe_diffs = publicize(diffs, live)
    out = Path(args.output_dir)
    snapshot = {
        "schema_version": 1,
        "retrieved_at": retrieved_at,
        "repository_count": len(live),
        "repositories": live,
    }
    candidate = {"schema_version": 1, "retrieved_at": retrieved_at, "differences": safe_diffs}
    atomic_write(out / "snapshot.private.json", json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    atomic_write(out / "candidate.public.json", json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    atomic_write(out / "report.public.md", render_report(safe_diffs, retrieved_at))
    print(f"inventory audit complete: {len(live)} repositories, {len(safe_diffs)} public-safe differences")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AuditError as exc:
        print(f"repository inventory audit failed: {exc}", file=sys.stderr)
        raise SystemExit(2)
