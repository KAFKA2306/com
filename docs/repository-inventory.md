# GitHubリポジトリ棚卸し

`registry/repositories.json` は横断管理上の正準役割だけを保持し、GitHub APIの取得結果を自動で昇格させません。GitHub実体の棚卸しは `scripts/audit_repository_inventory.py` で行います。

## 境界

- `registry/repositories.json`: 人間が承認した `role` / `canonical_for` / purpose の正準。
- `registry/repository-inventory-decisions.json`: stableなGitHub repository IDと、`managed | observed | excluded | pending_review` の判断、理由、確認日、再確認期限。
- `repository-inventory-audit/snapshot.private.json`: 1 runだけの完全snapshot。private repositoryを含み得るためGitへcommitせず、公開artifactにもuploadしません。
- `repository-inventory-audit/candidate.public.json`: private名を除去した更新候補。
- `repository-inventory-audit/report.public.md`: private名を除去した人間向け差分。

## 取得と検証

完全なowner inventoryを取得できるread-only tokenを `KAFKA_GITHUB_TOKEN` に設定して実行します。

```bash
KAFKA_GITHUB_TOKEN=... python scripts/audit_repository_inventory.py
python scripts/validate_control_plane.py
python -m unittest discover -s tests -v
```

無認証、HTTPエラー、rate limit、必要field欠落は成功扱いにしません。API取得結果だけで `role` や `canonical_for` を書き換える処理はありません。

差分は次の型へ分類します。

- `new`
- `missing`
- `renamed`
- `visibility_changed`
- `archived_changed`
- `capability_changed`
- `unclassified`

改名はrepository名ではなくstableなrepository IDで判定します。Issues / Pull Requests / Actions / Pages相当のcapabilityもsnapshotへ保存します。

## 人間のレビュー責任

差分が出たら、次の順で確認します。

1. `candidate.public.json` と `report.public.md` を確認する。
2. private repositoryの存在・名称は公開Issue、Pages、公開artifactへ転記しない。
3. 未登録repositoryは目的、公開範囲、既存正準との重複を確認し、`managed | observed | excluded | pending_review` のいずれかを決める。
4. 判断時に `reason`、`reviewed_at`、`review_due_at` を更新する。
5. 正準役割を変える必要がある場合だけ、別のレビュー可能な変更として `registry/repositories.json` を更新する。
6. `python scripts/validate_control_plane.py` とunit testを通してからmergeする。

GitHub Actionsの `Audit repository inventory` は定期・手動のlive audit用です。tokenが設定されていない場合は部分的なpublic inventoryを「成功」として扱わずfail-closedします。公開artifactへはpublic-safeなcandidateとreportだけをuploadし、完全snapshotはjob終了時に削除します。
