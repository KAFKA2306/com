# KAFKA COM

`KAFKA2306/com`は、KAFKA2306配下の複数リポジトリにまたがる仕事を、**人間が理解でき、ChatGPTが実行を支援でき、GitHub上で監査できる形に保つための管理リポジトリ**です。

日常の入口はChatGPTです。ユーザーは自然言語で目的や変更を伝えます。重要な仕事は、会話だけに残さず、このリポジトリのIssueへ「何をするか」「どこまで許可するか」「何をもって完了とするか」「どの証拠で確認したか」を記録します。

> **最終実体確認:** 2026年8月4日  
> **標準タイムゾーン:** Asia/Tokyo  
> **正準の管理対象:** 方針、横断指示、意思決定、定期サービス、障害、完了証拠  
> **正準ではないもの:** ChatGPTの会話履歴、ローカルキュー、スケジューラーの内部状態、各製品の実装コード

---

## このリポジトリが解決する問題

KAFKA2306には、投資分析、財務データ、VRChatイベント、旅行、衣装生成、画像生成、エージェント用スキルなど、目的の異なるリポジトリがあります。個別の実装だけを見ても、次の情報は分散しやすくなります。

- なぜ変更するのか
- どのリポジトリが正準なのか
- 複数リポジトリ間で何が依存しているのか
- ChatGPTへ依頼した仕事がどこまで進んだのか
- 「実装済み」「PR作成済み」「公開確認済み」のどこまで完了したのか
- 定期処理が現在も有効なのか
- 誤った結果や壊れた公開ページをどう記録したのか

`com`は、これらを製品コードから分離して記録します。

---

## 全体の運用モデル

```text
ユーザーがChatGPTへ自然言語で指示
        │
        ▼
comにDirective / Service / Incident / Decisionを記録
        │
        ▼
対象リポジトリで調査・Issue・branch・実装・PR・公開
        │
        ▼
テスト、CI、公開URL、スクリーンショット、一次情報で検証
        │
        ▼
comの作業項目へ証拠を集約
        │
        ▼
受入条件をすべて満たした場合のみ完了
```

### ChatGPTの役割

ChatGPTは通常の操作面です。

- 自然言語の依頼を具体的な作業へ分解する
- 対象リポジトリと現在の状態を確認する
- 必要に応じて最新の一次情報を調査する
- Issue、branch、PR、レビュー、監査を進める
- テスト結果や公開状態を確認する
- 完了していない条件を明示する

ただし、**ChatGPTの会話履歴は正準ではありません**。長期的に必要な判断、制約、進捗、証拠はGitHubへ残します。

### 各製品リポジトリの役割

各製品リポジトリは、その製品固有の実装を所有します。

- ソースコード
- テスト
- ドメイン固有データ
- 画像、モデル、生成物
- リポジトリ内の設計文書
- PR、release、GitHub Pages、Cloudflare Pagesなどの公開物

`com`へ製品コードや正準データを複製しません。

### executorの役割

GitHub Actions、ChatGPTのscheduled task、ローカルWSL、GPU実行環境などは処理を実行する仕組みです。交換可能な実行手段であり、仕事の正準状態ではありません。

---

## 作業項目の4種類

`.github/ISSUE_TEMPLATE/`に4種類のIssue Formがあります。

### Directive

一度限りの変更、調査、移行、複数リポジトリ横断作業に使います。

必須内容:

- 対象リポジトリ
- 目的と背景
- 対象範囲と非対象
- 受入条件
- 必要な証拠
- 許可される最大リスク
- 禁止事項
- 実行時期

### Recurring Service

毎日、毎週、特定条件成立時など、繰り返し行う責務を定義します。

スケジュールだけでなく、次を明示します。

- 何の判断や行動を支援するか
- 一次情報と鮮度の条件
- 正常時に何を記録するか
- 通知しない条件
- 失敗時のIncident条件
- 停止・見直し条件

### Incident

誤った分析、壊れた公開ページ、失敗した定期処理、古い情報の混入、権限境界の逸脱などを記録します。

推測と確定原因を分離し、復旧証拠と再発防止を残します。

### Decision

リポジトリ境界、技術選定、公開方針、正準データ、完了条件など、今後の仕事に影響する判断を記録します。

採用案だけでなく、代替案、根拠、悪影響、見直し時期も残します。

---

## 状態モデル

`registry/portfolio.json`では、作業状態を次の8種類に統一しています。

| 状態 | 意味 |
|---|---|
| `inbox` | 依頼を受けたが、範囲や証拠条件が未確定 |
| `ready` | 実行可能な契約が整った |
| `running` | 実際に作業中 |
| `review` | 実装済みで、検証またはレビュー中 |
| `blocked` | 外部条件、権限、環境不足などで停止 |
| `failed` | 実行または検証に失敗 |
| `done` | 受入条件と証拠をすべて満たした |
| `cancelled` | 意図的に中止 |

PRを作っただけ、CIが通っただけ、設定ファイルを書いただけでは`done`にしません。

---

## 完了の考え方

完了条件は仕事ごとに異なりますが、通常は次の順に確認します。

1. **変更内容** — 対象コードや文書が実際に変更されている
2. **静的検証** — lint、schema、unit testなどが成功している
3. **統合検証** — 必要な依存関係を含めて動作する
4. **公開検証** — Pagesや配布物が実際に更新されている
5. **内容検証** — 表示される数値、文章、画像、リンクが正しい
6. **運用検証** — 定期処理なら実行履歴や失敗時の挙動を確認する
7. **GitHub完了** — PRをmergeし、不要な作業branchを削除する
8. **証拠記録** — IssueへPR、commit、CI、公開URL、一次資料を残す

環境上確認できない項目は、完了扱いにせず制約として記録します。

詳細は[`policies/completion.md`](policies/completion.md)と[`policies/evidence.md`](policies/evidence.md)を参照してください。

---

## リポジトリ境界

`registry/repositories.json`には、現在確認済みの主要リポジトリだけを登録しています。登録は全所有リポジトリを網羅しているとは限りません。

| リポジトリ | 役割 |
|---|---|
| `KAFKA2306/com` | 横断指示、方針、意思決定、障害、証拠の正準 |
| `KAFKA2306/agent-resources` | エージェント用スキルと共通資源の配布 |
| `KAFKA2306/prompt-vault` | プロンプトと生成アセットの製品 |
| `KAFKA2306/investor` | 投資調査、企業知識、財務分析 |
| `KAFKA2306/CrewTrade` | 定量研究カタログと証拠監査 |
| `KAFKA2306/WealthAudit` | 資産分析、警告、予測境界 |
| `KAFKA2306/image2outfit` | 衣装・アバターアセットの制作ライフサイクル |

未登録リポジトリを操作してはいけないという意味ではありません。横断管理上の正準として扱う前に、目的、公開範囲、重複関係を確認するという意味です。

---

## ディレクトリ構成

```text
.github/
  ISSUE_TEMPLATE/       作業項目の入力フォーム
  workflows/            管理契約のCI
policies/                全リポジトリ共通の必須方針
instructions/            ChatGPTやexecutor向けの実行手順
registry/                リポジトリ、サービス、スケジュール、能力の台帳
schemas/                 registryのJSON Schema
scripts/                 決定的な検証スクリプト
playbooks/               繰り返し使う運用手順
docs/                    管理モデルの詳説
docs/adr/                アーキテクチャ意思決定記録
tests/                   管理契約のunit test
```

### README.mdとAGENTS.mdの役割

- **README.md** — 人間がプロジェクト全体を理解するための正準入口
- **AGENTS.md** — AIエージェントが作業するときに守る操作契約

READMEへエージェント専用の細かな命令を詰め込みません。AGENTS.mdだけを読まないと人間が構造を理解できない状態にもしてはいけません。

全リポジトリ共通のREADME方針は[`policies/readme.md`](policies/readme.md)に定義します。

---

## ローカル検証

Python 3.12を推奨します。追加パッケージは不要です。

```bash
python scripts/validate_control_plane.py
python -m unittest discover -s tests -v
```

検証対象:

- registryとschemaの整合
- ID重複
- 正準責務の重複
- 未登録executor参照
- serviceとscheduleの参照関係
- 必須ポリシーとIssue Formの存在

GitHub Actionsでも同じ検証を実行します。

---

## よくある運用

### 複数リポジトリを改善する

1. `com`に親Directiveを作る
2. 対象リポジトリごとにIssueまたはPRを作る
3. 親Directiveから各作業を参照する
4. 各リポジトリで検証・mergeする
5. 親Directiveへ結果と残件を記録する

### 定期処理を追加する

1. Recurring Service Issueで目的と停止条件を定義する
2. executorを選ぶ
3. `registry/services.json`へ追加する
4. 時刻実行なら`registry/schedules.json`へ追加する
5. 実際の初回実行を確認する
6. 実行証拠をIssueへ記録する

現在、`services.json`と`schedules.json`は、監査なしの既存処理を誤って稼働中とみなさないため、空から開始しています。

### 誤った結果を修正する

1. Incidentを作る
2. 誤りの範囲と利用者影響を記録する
3. 必要なら公開を止める、警告を出す、rollbackする
4. 原因を確定する
5. 対象repoで修正する
6. 再発防止のテストや契約を追加する
7. 復旧を実測してIncidentを閉じる

---

## 証拠の原則

次のものは、それ単独では十分な証拠ではありません。

- PR URL — 実装が動く証拠ではない
- unit test成功 — 公開環境が正しい証拠ではない
- 公開URL — 表示内容が正しい証拠ではない
- スケジュール設定 — 定期処理が実行された証拠ではない
- READMEの記述 — リポジトリ実体の証拠ではない

日付、数値、仕様、外部サービスの状態は、最新の公式情報または実測結果と照合します。

---

## セキュリティと非公開情報

このリポジトリは公開されているため、次を保存しません。

- APIキー、token、cookie、認証情報
- メールや会話の全文
- 個人情報
- 非公開の投資ポジション
- ローカル絶対パスを含む実行履歴
- 秘密を含むprompt
- 未加工のexecutorログ

必要な場合は、秘密を含まない要約、hash、GitHub上の限定公開参照などを記録します。

詳細は[`SECURITY.md`](SECURITY.md)を参照してください。

---

## 既知の制約

- `registry/repositories.json`は現在、主要リポジトリの初期登録であり、KAFKA2306所有リポジトリの全件監査は継続中です。
- 定期サービスとscheduleは、実稼働監査を終えたものだけを登録する方針です。
- GitHub接続や実行環境によっては、branch削除、ローカルGPU実行、外部サービスの管理操作を直接行えない場合があります。
- このリポジトリは製品ダッシュボードではありません。公開UIが必要な場合も、管理契約と可視化を分離します。

---

## 主要文書

- [`GOVERNANCE.md`](GOVERNANCE.md) — 権限と意思決定
- [`SECURITY.md`](SECURITY.md) — 機密境界
- [`AGENTS.md`](AGENTS.md) — エージェント操作契約
- [`policies/completion.md`](policies/completion.md) — 完了条件
- [`policies/evidence.md`](policies/evidence.md) — 証拠条件
- [`policies/source-verification.md`](policies/source-verification.md) — 外部情報の検証
- [`policies/repository-boundaries.md`](policies/repository-boundaries.md) — リポジトリ境界
- [`docs/CONTROL_MODEL.md`](docs/CONTROL_MODEL.md) — 管理モデル
- [`docs/WORK_ITEM_CONTRACT.md`](docs/WORK_ITEM_CONTRACT.md) — 作業項目の契約

---

## ライセンス

ライセンス条件は[`LICENSE`](LICENSE)を参照してください。各製品リポジトリのコード、データ、画像、外部素材には、それぞれのライセンスと利用条件が適用されます。
