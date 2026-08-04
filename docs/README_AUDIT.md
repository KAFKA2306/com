# README監査台帳

この文書は、KAFKA2306配下のREADMEを「日本語・最新・人間向け」の共通契約へ移行する作業の進捗を記録します。

正準の作業項目はIssue #3です。READMEの内容そのものは各リポジトリが所有し、この台帳には状態、確認日、PR、merge、残件だけを記録します。

> **監査基準日:** 2026年8月5日  
> **GitHub接続で確認したownerリポジトリ数:** 100  
> **初回確認済み:** 36  
> **未確認または再監査待ち:** 64  
> **README更新・merge済み:** 16  
> **初回確認で全面改稿を保留:** 19  
> **snapshot・fork再監査:** 1

## 状態の意味

| 状態 | 意味 |
|---|---|
| `merged` | READMEを実体と照合して更新し、default branchへ反映済み |
| `in-progress` | READMEまたは関連する実行契約を修正中 |
| `initial-review-current` | 初回確認では日本語・人間向け情報が相当程度あり、全面改稿を保留 |
| `incident` | README監査で製品、data、CIの障害を検出し、別Issueで追跡 |
| `false-positive-corrected` | 監査側の誤判定を訂正し、原因と再発防止を記録済み |
| `pending` | 未監査 |
| `snapshot-or-fork-review` | 上流、差分、同期方針、licenseを中心に再監査する対象 |

`initial-review-current`は最終合格ではありません。実装、公開URL、主要command、制約をさらに深く照合する場合があります。

## 更新・merge済み

| リポジトリ | 状態 | 反映 | 主な変更 |
|---|---|---|---|
| `KAFKA2306/com` | merged | PR #4 / `ad86533d18abd7d3c394c5f68f818fe59ddd6e20` | ChatGPT-first管理modelを日本語で説明し、共通README契約を追加 |
| `KAFKA2306/KAFKA2306` | merged | PR #1 / `4eba0bb81ee6f3c96dfb7454748f7fe9a48248f5` | profileを現役・正準project中心へ刷新 |
| `KAFKA2306/prompt-vault` | merged | PR #18 | data、block、生成、検証、公開境界を説明。絶対pathを除去 |
| `KAFKA2306/investor` | merged | PR #19 / `854918ae3476c8dbce33aa014688cf8ee072eca7` | AAARTSだけでなく企業知識DB、金利・為替DB、Pagesを含む統合研究基盤の現状へ更新 |
| `KAFKA2306/WealthAudit` | merged | PR #7 | 実績と予測、非公開入力、Drive同期、再計算監査を説明 |
| `KAFKA2306/travel` | merged | PR #7 | 英語READMEを日本語化し、複数viewと公式確認経路を整理 |
| `KAFKA2306/vlog` | merged | PR #19 / `107d6f1a32ca7cb28fa6b18c30b5305e2edaa708` | Human Memory v2、証拠・記憶・公開物の境界、現在の移行状態を説明 |
| `KAFKA2306/vrc_cast_event_calender` | merged | PR #23、PR #24 / `1af46af777c66bdad86080a902391837be447fbe` | README新設後、source/deploy境界とsnapshot整合CIを追加。0 byte誤記を訂正 |
| `KAFKA2306/aboutkafka` | merged | PR #2 | 2024年の旧React/Viteプロフィール試作であり、現在のプロフィール正準ではないことを明示 |
| `KAFKA2306/financial-services-plugins` | merged | PR #1 | Anthropic由来の旧snapshotであること、現行上流、独自差分、同期方針を明示 |
| `KAFKA2306/AdaptiveWearGeneratorPro` | merged | PR #2 | 2025年の旧Blender addon、nested source、品質制約、`image2outfit`との境界を説明 |
| `KAFKA2306/backend` | merged | PR #2 / `aca4606b49e5037174b9808c6257059a7e9f39d7` | READMEとguideだけの未実装構想であり、Next.js、FastAPI、Workers、Celery、DB、deploymentが存在しないことを明示 |
| `KAFKA2306/econalert` | merged | PR #1 / `dfcc5658ef86f7aad09742c1ac3ac456271a9875` | code・workflow・testがない未実装の経済指標通知構想として訂正 |
| `KAFKA2306/fx` | merged | PR #1 / `f48ec0d7f7e82aa2db7bd64e453b92c20bc4bf9a` | data collector、model、backtest、risk管理がない2024年のFX相対価値研究構想として訂正 |
| `KAFKA2306/imura` | merged | PR #1 / `9a3b574702d16ece9cea2629a005df249738adcb` | READMEだけのprivate design noteと明示し、原文・要約・解釈・identity・`investor`統合候補を整理 |
| `KAFKA2306/333` | merged | PR #3 / `5602ecf04a3c44a785a15870227dd992f7411fa9` | raw data不在時の固定投資結論を除去し、未計算Pages、README契約test、CI整合を追加 |

## 作業中・障害・訂正履歴

| リポジトリ | 状態 | 作業 | 残件 |
|---|---|---|---|
| `KAFKA2306/investor` | incident | Issue #20 | 既存の全体TypeScript test/type/Biome/Python負債とdashboard dependency auditを継続。README PRでは解消済みと扱っていない |
| `KAFKA2306/vrc_cast_event_calender` | false-positive-corrected | Issue #22 closed | Contents APIの大容量本文省略を0 byteと誤判定。Actions実測、README訂正、deploy snapshot CI追加で是正 |
| `KAFKA2306/333` | incident-resolved | Issue #2 closed / PR #3 | 未計算なのに固定結論を表示していた状態を解消。Ruff、Black、mypy、pytestがActions run `30924897374`で成功 |

### `vrc_cast_event_calender`誤判定の訂正証拠

GitHub Actions run `30904241278`で、`events.json`は次の状態と確定しました。

- 1,949,391 bytes
- 601 events
- payload: `object.events`
- SHA-256: `bfa05322318ea350626e7e4a847dd62b034c6c25f751e26e9848ffae8183956f`
- health、event ontology、ontology auditの件数はすべて601

connectorの空content表示だけで実ファイルsizeを判断しないことを再発防止とします。

### `333`の是正証拠

PR #3ではREADMEだけでなく、生成template、Pages、workflow、契約testを同時に修正しました。CIで露呈した既存のBlack不整合6fileと、現行mypyで不要になったPyYAMLの`type: ignore` 2箇所も修正しました。

- Actions run: `30924897374`
- Ruff: success
- Black: success
- mypy: success
- pytest: success
- merge commit: `5602ecf04a3c44a785a15870227dd992f7411fa9`

## 初回確認で全面改稿を保留したリポジトリ

| リポジトリ | 状態 | 初回判定 |
|---|---|---|
| `KAFKA2306/agent-resources` | initial-review-current | 日本語で目的、導入、skill、securityを説明 |
| `KAFKA2306/CrewTrade` | initial-review-current | 日本語で研究catalog、data、評価、公開を説明 |
| `KAFKA2306/image2outfit` | initial-review-current | 日本語で制作life cycle、完了条件、成果物を説明 |
| `KAFKA2306/bonus` | initial-review-current | 日本語で公開分析、data、操作、検証を説明 |
| `KAFKA2306/boothitemmanager` | initial-review-current | 日本語で商品管理、比較、来歴、公開を説明 |
| `KAFKA2306/investor2` | initial-review-current | 日本語で企業業績予測、証拠、構造、公開を説明 |
| `KAFKA2306/semiconductor-earnings-model` | initial-review-current | 日本語で半導体決算model、data、検証を説明 |
| `KAFKA2306/pal-atlas` | initial-review-current | 日本語でlocal-first記録、schema、検証を説明 |
| `KAFKA2306/anime` | initial-review-current | 日本語で作品data、更新、公開、制約を説明 |
| `KAFKA2306/know` | initial-review-current | 日本語でontology、schema、生成、利用方法を説明 |
| `KAFKA2306/daily-arXiv-ai-enhanced` | initial-review-current | 日本語で論文収集、生成、公開、secret境界を説明 |
| `KAFKA2306/2511youtuber` | initial-review-current | 日本語で動画候補、生成、公開、運用を説明 |
| `KAFKA2306/2510youtuber` | initial-review-current | 日本語で動画候補、生成、公開、運用を説明 |
| `KAFKA2306/bodogenomikata2` | initial-review-current | 日本語でルール根拠付き回答、data、UI、検証を説明 |
| `KAFKA2306/cast_event_cal` | initial-review-current | 日本語で収集・生成正準とdeploy repoへの同期を説明 |
| `KAFKA2306/kakeibo` | initial-review-current | 日本語で家計data、非公開境界、処理方法、制約を説明 |
| `KAFKA2306/auto-invest` | initial-review-current | 日本語で自動投資研究、実行境界、risk、検証を説明 |
| `KAFKA2306/expense2` | initial-review-current | 日本語でexpense data処理、利用方法、構造、制約を説明 |
| `KAFKA2306/adaptive_wear_generator_pro` | initial-review-current | 日本語で公開研究実装、品質監査、legacy/private版との境界を説明 |

## snapshot・fork再監査

| リポジトリ | 状態 | 確認事項 |
|---|---|---|
| `KAFKA2306/expense` | snapshot-or-fork-review | KAFKA独自製品ではなく上流由来に見えるため、upstream、取得時点、独自差分、license、同期方針を確認する |

## 次の優先順

1. READMEが存在しない、READMEだけで実装済みを装う、placeholderや固定数値を含むリポジトリ
2. 現在も頻繁に更新される正準リポジトリ
3. GitHub PagesまたはCloudflare Pagesを公開しているリポジトリ
4. 金融、投資、個人data、外部APIなど誤認時の影響が大きいリポジトリ
5. 同一目的の重複リポジトリ
6. fork、source snapshot、upstream mirror
7. 停止中・archive候補・小規模実験

次の監査batchでは、未確認64件から金融・公開site・README-only・重複候補を先に抽出し、実体とREADMEの不一致が大きいものから個別Issue・PRへ分離します。

## 監査手順

1. default branchのREADMEを読む
2. 最近のmerge、主要設定、package、Taskfile、workflow、公開URLを確認する
3. READMEの目的、機能、command、構造、正準、公開、制約と実体を照合する
4. 大容量fileはContents APIの表示だけでsizeや内容を判断せず、checkout、blob metadata、CIで確認する
5. 不足があればリポジトリごとのbranch・PRで修正する
6. CIまたは適切な実体確認を行う
7. merge後にdefault branchのREADMEを読み戻す
8. この台帳とIssue #3へ証拠を記録する

README監査で製品障害を発見した場合、READMEへ隠さず記載し、障害修正は別Incidentへ分離します。監査側の誤りを発見した場合も、履歴を消さず訂正内容と原因を残します。
