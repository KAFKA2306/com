# Registry rules

Registries contain control metadata only. They must remain small, reviewable, and machine validated.

## Repository entries

Add a repository only after confirming its current identifier and responsibility. Use `review-required` when visibility has not been verified. A canonical domain may belong to only one repository.

### GitHub実体の棚卸し

`registry/repositories.json` は承認済みの役割・正準責務を保持し、GitHub APIの取得結果から自動更新しません。実体監査は次で行います。

```bash
KAFKA_GITHUB_TOKEN=... python scripts/audit_repository_inventory.py
python scripts/validate_control_plane.py
python -m unittest discover -s tests -v
```

stableなGitHub repository ID、`managed | observed | excluded | pending_review` の判断、理由、確認日、再確認期限は `registry/repository-inventory-decisions.json` に分離します。差分は `new | missing | renamed | visibility_changed | archived_changed | capability_changed | unclassified` に分類します。

完全snapshot `repository-inventory-audit/snapshot.private.json` はprivate repositoryを含み得るためGitへcommitせず、公開artifactにもuploadしません。公開可能なのはprivate名を除去した `candidate.public.json` と `report.public.md` だけです。

差分が出た場合の判断責任は人間にあります。未登録repositoryについて目的・公開範囲・正準責務の重複を確認し、disposition、理由、`reviewed_at`、`review_due_at` を更新します。`role` / `canonical_for` を変更する必要がある場合だけ、別のレビュー可能な変更として `registry/repositories.json` を更新します。詳細は [`docs/repository-inventory.md`](../docs/repository-inventory.md) を参照してください。

## Service entries

Add a service only after creating a recurring-service issue. Its target repositories and executor must already exist in their registries. Do not register a historical automation merely because configuration files exist.

## Schedule entries

A schedule references a registered service. An active schedule requires an active service. Record an IANA timezone and a human-readable trigger. Execution-engine-specific IDs belong in the service work item or target repository, not here, unless required for recovery.

## Capability entries

Capabilities describe executor classes and their restrictions. They are not credentials and do not grant permission by themselves.
