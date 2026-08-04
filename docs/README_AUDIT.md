# README監査台帳

この文書は、KAFKA2306配下のREADMEを「日本語・最新・人間向け」の共通契約へ移行する作業の進捗を記録します。

正準の作業項目はIssue #3です。READMEの内容そのものは各リポジトリが所有し、この台帳には状態、確認日、PR、merge、残件だけを記録します。

> **監査基準日:** 2026年8月4日  
> **GitHub接続で確認したownerリポジトリ数:** 100  
> **初回確認済み:** 14  
> **未確認または再監査待ち:** 86

## 状態の意味

| 状態 | 意味 |
|---|---|
| `merged` | READMEを実体と照合して更新し、default branchへ反映済み |
| `in-progress` | READMEまたは関連する実行契約を修正中 |
| `initial-review-current` | 初回確認では日本語・人間向け情報が相当程度あり、全面改稿を保留 |
| `incident` | README監査で製品またはデータの障害を検出し、別Issueで追跡 |
| `pending` | 未監査 |
| `snapshot-or-fork-review` | 上流、差分、同期方針、licenseを中心に再監査する対象 |

`initial-review-current`は最終合格ではありません。実装、公開URL、主要コマンド、制約をさらに深く照合する場合があります。

## 更新・merge済み

| リポジトリ | 状態 | 反映 | 主な変更 |
|---|---|---|---|
| `KAFKA2306/com` | merged | PR #4 / `ad86533d18abd7d3c394c5f68f818fe59ddd6e20` | 管理モデルを日本語で説明し、共通README契約を追加 |
| `KAFKA2306/KAFKA2306` | merged | PR #1 / `4eba0bb81ee6f3c96dfb7454748f7fe9a48248f5` | profileを現役・正準プロジェクト中心へ刷新 |
| `KAFKA2306/prompt-vault` | merged | PR #18 | データ、block、生成、検証、公開境界を説明。絶対パス除去 |
| `KAFKA2306/WealthAudit` | merged | PR #7 | 実績と予測、非公開入力、Drive同期、再計算監査を説明 |
| `KAFKA2306/travel` | merged | PR #7 | 英語READMEを日本語化し、複数viewと公式確認経路を整理 |
| `KAFKA2306/vrc_cast_event_calender` | merged | PR #23 / `656cbc62117c7355b542b498c1305b80a59fc57d` | READMEを新規作成し、公開面、ontology、既知障害を説明 |

## 作業中・障害あり

| リポジトリ | 状態 | 作業 | 残件 |
|---|---|---|---|
| `KAFKA2306/investor` | in-progress | PR #19 | README刷新とCPU setup分離。既存TypeScript/Biome負債をIssue #20で追跡。CI再検証中 |
| `KAFKA2306/vrc_cast_event_calender` | incident | Issue #22 | default branchの`events.json`が0 byte。health・ontologyと不整合。公開復旧は未完了 |

## 初回確認で全面改稿を保留したリポジトリ

| リポジトリ | 状態 | 初回判定 |
|---|---|---|
| `KAFKA2306/agent-resources` | initial-review-current | 日本語で目的、導入、skill、securityを説明 |
| `KAFKA2306/CrewTrade` | initial-review-current | 日本語で研究カタログ、データ、評価、公開を説明 |
| `KAFKA2306/image2outfit` | initial-review-current | 日本語で制作life cycle、完了条件、成果物を説明 |
| `KAFKA2306/bonus` | initial-review-current | 日本語で公開分析、データ、操作、検証を説明 |
| `KAFKA2306/boothitemmanager` | initial-review-current | 日本語で商品管理、比較、来歴、公開を説明 |
| `KAFKA2306/investor2` | initial-review-current | 日本語で企業業績予測、証拠、構造、公開を説明 |
| `KAFKA2306/semiconductor-earnings-model` | initial-review-current | 日本語で半導体決算モデル、データ、検証を説明 |

## 次の優先順

1. 現在も頻繁に更新される正準リポジトリ
2. GitHub PagesまたはCloudflare Pagesを公開しているリポジトリ
3. READMEがない、英語のみ、URLだけ、旧名称のままのリポジトリ
4. 同一目的の重複リポジトリ
5. fork、source snapshot、upstream mirror
6. 停止中・archive候補・小規模実験

## 監査手順

1. default branchのREADMEを読む
2. 最近のmerge、主要設定、package、Taskfile、workflow、公開URLを確認する
3. READMEの目的、機能、コマンド、構造、正準、公開、制約と実体を照合する
4. 不足があればリポジトリごとのbranch・PRで修正する
5. CIまたは適切な実体確認を行う
6. merge後にdefault branchのREADMEを読み戻す
7. この台帳とIssue #3へ証拠を記録する

README監査で製品障害を発見した場合、READMEへ隠さず記載し、障害修正は別Incidentへ分離します。
