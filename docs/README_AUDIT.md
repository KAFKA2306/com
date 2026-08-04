# README監査台帳

この文書は、KAFKA2306配下のREADMEを「日本語・最新・人間向け」の共通契約へ移行する作業の正準台帳です。

正準の親作業はIssue #3です。README本文は各repositoryが所有し、この台帳には状態、根拠、反映先、残件を記録します。

> **監査基準日:** 2026年8月5日  
> **GitHub接続で確認したowner repository数:** 100  
> **初回確認済み:** 50  
> **未確認または再監査待ち:** 50  
> **README更新・default branch反映済み:** 28  
> **初回確認で全面改稿を保留:** 21  
> **snapshot・fork再監査:** 1

件数検算:

```text
28 reflected + 21 initial-review-current + 1 snapshot-or-fork-review = 50
100 total - 50 reviewed = 50 remaining
```

## 状態の意味

| 状態 | 意味 |
|---|---|
| `merged` | READMEを実体と照合して更新し、default branchへ反映済み |
| `initial-review-current` | 初回確認では人間向け情報が相当程度あり、全面改稿を保留。最終合格ではない |
| `incident` | README監査で製品・data・CI・security障害を検出し、別Issueで追跡中 |
| `incident-resolved` | README誤認または関連障害を是正し、Issueをclose済み |
| `false-positive-corrected` | 監査側の誤判定を訂正し、原因と再発防止を記録済み |
| `snapshot-or-fork-review` | upstream、取得時点、独自差分、license、同期方針を中心に再監査する対象 |
| `pending` | 未監査 |

## README更新・default branch反映済み

| repository | 状態 | 反映 | 主な変更 |
|---|---|---|---|
| `KAFKA2306/com` | merged | PR #4 / `ad86533d18abd7d3c394c5f68f818fe59ddd6e20` | ChatGPT-first管理modelと共通README契約を日本語で説明 |
| `KAFKA2306/KAFKA2306` | merged | PR #1 / `4eba0bb81ee6f3c96dfb7454748f7fe9a48248f5` | GitHub profileを現在の主要活動へ刷新 |
| `KAFKA2306/prompt-vault` | merged | PR #18 | data、block、生成、検証、公開境界を整理し、絶対pathを除去 |
| `KAFKA2306/investor` | merged | PR #19 / `854918ae3476c8dbce33aa014688cf8ee072eca7` | 企業知識DB、金利・為替DB、Pagesを含む研究基盤の現状へ更新 |
| `KAFKA2306/WealthAudit` | merged | PR #7 | 実績と予測、非公開入力、Drive同期、再計算監査を説明 |
| `KAFKA2306/travel` | merged | PR #7 | 英語READMEを日本語化し、公開viewと公式確認経路を整理 |
| `KAFKA2306/vlog` | merged | PR #19 / `107d6f1a32ca7cb28fa6b18c30b5305e2edaa708` | Human Memory v2、証拠・記憶・公開物の境界を説明 |
| `KAFKA2306/vrc_cast_event_calender` | merged | PR #23、#24 / `1af46af777c66bdad86080a902391837be447fbe` | source/deploy境界とsnapshot整合CIを追加し、0 byte誤記を訂正 |
| `KAFKA2306/aboutkafka` | merged | PR #2 | 2024年の旧profile試作であり、現在のprofile正準ではないことを明示 |
| `KAFKA2306/financial-services-plugins` | merged | PR #1 | Anthropic由来snapshot、現行upstream、独自差分、同期方針を明示 |
| `KAFKA2306/AdaptiveWearGeneratorPro` | merged | PR #2 | 2025年の旧Blender addon、品質制約、`image2outfit`との境界を説明 |
| `KAFKA2306/backend` | merged | PR #2 / `aca4606b49e5037174b9808c6257059a7e9f39d7` | READMEとguideだけの未実装構想として訂正 |
| `KAFKA2306/econalert` | merged | PR #1 / `dfcc5658ef86f7aad09742c1ac3ac456271a9875` | code・workflow・testがない未実装通知構想として訂正 |
| `KAFKA2306/fx` | merged | PR #1 / `f48ec0d7f7e82aa2db7bd64e453b92c20bc4bf9a` | 2024年のFX相対価値研究構想であり、live trading systemではないと明示 |
| `KAFKA2306/imura` | merged | PR #1 / `9a3b574702d16ece9cea2629a005df249738adcb` | private design note、原文・要約・解釈・identity境界を整理 |
| `KAFKA2306/333` | merged | PR #3 / `5602ecf04a3c44a785a15870227dd992f7411fa9` | raw data不在時の固定投資結論を除去し、未計算Pages・契約testを追加 |
| `KAFKA2306/finBI` | merged | PR #3 / `62cc10c04c6fbe305d7b0de05d2819d12dfeeb0f` | 絶対path・設定不整合・旧依存を持つ非稼働legacy prototypeとして訂正 |
| `KAFKA2306/salary` | merged | PR #2 / `8334ffec63e685e10d719ced6db4261ca5299e73` | 2024年2月のNotebook・CSV・third-party scraping snapshotとして訂正 |
| `KAFKA2306/kafin2` | merged | PR #2 / `35fce97d3607f0ff1946004c5a34cbb343e7e6d7` | README-only構想でcode・data・test・deploymentがないことを明示 |
| `KAFKA2306/kafin3` | merged | PR #4 / `5d1e8348f32fc316cd0e2dba13af6d00660fe492` | 旧Completion API・欠落frontendを持つlegacy prototypeとして訂正 |
| `KAFKA2306/uranium` | merged | PR #2 / `83c64f08a77a656815ae24a7c8c8031d70fe33ce` | 2024年10月のticker・価格取得snapshotとしてREADMEを新設 |
| `KAFKA2306/financeLLM` | merged | PR #2 / `926e7cad8763f7f180ddec82db17ae86873970a4` | invalid requirementsと固定pathを持つlegacy RAG実験として訂正 |
| `KAFKA2306/nonfarmpayroll` | merged | PR #2 / `6d1730031f24b7b5757a23f48fd7e86e25718da7` | synthetic改定統計を撤回し、Pagesをanalysis unavailableのfail-closed契約へ変更 |
| `KAFKA2306/tradermade_cfd` | merged | PR #2 / `a8bd59b5a99ecd5f6531d136cc64f5fd2724ca14` | Windows絶対pathと依存欠落を持つ非再現legacy CFD prototypeとして訂正 |
| `KAFKA2306/mstr` | merged | PR #2 / `bfcf15fcdd2e212cfeb19296548c66be587d9da7` | 2024年中心の過去snapshotとし、point-in-time・forward fill制約を明示 |
| `KAFKA2306/oil` | merged | PR #2 / `3eb71dc567e06b5f4846a61f95e491ce6ba7232c` | 固定Sharpe ratio・相関・投資適性の断定を撤回し、価格分析snapshotとして訂正 |
| `KAFKA2306/option` | merged | PR #8 / `5efac91a11b68c3ecc83fc4dbeca66da7ccce60a` | contract-aware計算契約を維持し、正準READMEを日本語化 |
| `KAFKA2306/fin_age_cfd` | merged | direct commit `a1e8f6711543ec7a343e2a2f31a439ce7be5ab28` | READMEを新設し、committed `.venv`・絶対path・system-wide API key設定を明示 |

`fin_age_cfd`は誤認防止を優先してREADMEをdefault branchへ直接追加しました。実装修復は完了しておらず、下記Incidentで追跡します。

## 作業中・障害・訂正履歴

| repository | 状態 | 作業 | 残件 |
|---|---|---|---|
| `KAFKA2306/investor` | incident | Issue #20 | 既存のTypeScript test/type/Biome/Python負債とdashboard dependency auditを継続 |
| `KAFKA2306/nonfarmpayroll` | incident | Issue #1 open / PR #2 merged | status-only Pagesの公開置換確認と、一次sourceの実vintage復旧が残る |
| `KAFKA2306/fin_age_cfd` | incident | Issue #1 open | committed `.venv`除去、相対path化、lock file、`setx /M`廃止、credential確認、clean CIが残る |
| `KAFKA2306/vrc_cast_event_calender` | false-positive-corrected | Issue #22 closed | Contents APIの大容量本文省略を0 byteと誤判定。checkout実測とsnapshot CIで是正 |
| `KAFKA2306/333` | incident-resolved | Issue #2 closed / PR #3 | 固定投資結論を除去し、Ruff・Black・mypy・pytest成功 |
| `KAFKA2306/finBI` | incident-resolved | Issue #2 closed / PR #3 | 存在しないsetup、未定義設定、個人pathを実装済みと読める状態を訂正 |
| `KAFKA2306/salary` | incident-resolved | Issue #1 closed / PR #2 | snapshotを現在の給与pipelineと読める状態を訂正 |
| `KAFKA2306/kafin2` | incident-resolved | Issue #1 closed / PR #2 | README-only構想を稼働中serviceと読める状態を訂正 |
| `KAFKA2306/kafin3` | incident-resolved | Issue #3 closed / PR #4 | 廃止API・欠落frontend・setup不整合を明示 |
| `KAFKA2306/uranium` | incident-resolved | Issue #1 closed / PR #2 | README欠落を解消し、2024年snapshot境界を記録 |
| `KAFKA2306/financeLLM` | incident-resolved | Issue #1 closed / PR #2 | 再現不能なquick startと未検証RAG表現を訂正 |
| `KAFKA2306/tradermade_cfd` | incident-resolved | Issue #1 closed / PR #2 | 絶対path・依存欠落・非再現状態をREADMEへ反映 |
| `KAFKA2306/mstr` | incident-resolved | Issue #1 closed / PR #2 | 過去図表・固定数値を現在値と読める状態を訂正 |
| `KAFKA2306/oil` | incident-resolved | Issue #1 closed / PR #2 | 価格分析から企業品質・投資適性を断定する記述を撤回 |
| `KAFKA2306/option` | incident-resolved | Issue #7 closed / PR #8 | 実装・testと整合するREADMEを日本語化 |

## 主要Incidentの証拠

### `vrc_cast_event_calender`の0 byte誤判定

GitHub Actions run `30904241278`で`events.json`をcheckoutして確認した結果:

- 1,949,391 bytes
- 601 events
- payload: `object.events`
- SHA-256: `bfa05322318ea350626e7e4a847dd62b034c6c25f751e26e9848ffae8183956f`
- health、event ontology、ontology auditはいずれも601件

再発防止として、Contents APIが大容量本文を返さない場合に空fileと判断しません。

### `333`の固定投資結論

PR #3でREADME、生成template、Pages、workflow、契約testを修正しました。Actions run `30924897374`でRuff、Black、mypy、pytestが成功しています。

### `nonfarmpayroll`のsynthetic改定data

監査で次を確認しました。

- BLS初回・第2回・第3回公表値の正準入力が存在しない
- `scripts/03_merge_revisions.py`にBLS入力不在時の`release1 = final`経路がある
- `dashboard.js`に`Math.random()`を使うdemo fallbackがある
- committed summaryとCSVに人工的なrevision値がある

PR #2で未検証数値を撤回し、Pages artifactをstatus-onlyへ変更しました。公開URLの置換確認まではIssue #1をcloseしません。

### `fin_age_cfd`のenvironment・credential負債

- `.venv/Lib/site-packages/`がtracked fileとして存在
- `D:\_investos\CFD`へpath固定
- `bat/set_api_key.bat`が管理者権限で`setx TRADERMADE_API_KEY ... /M`を実行

READMEは反映済みですが、repository hygieneとsecurity修復はIssue #1で継続します。

## 初回確認で全面改稿を保留したrepository

| repository | 状態 | 初回判定 |
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
| `KAFKA2306/bodogenomikata2` | initial-review-current | 日本語で根拠付き回答、data、UI、検証を説明 |
| `KAFKA2306/cast_event_cal` | initial-review-current | 日本語で収集・生成正準とdeploy repositoryへの同期を説明 |
| `KAFKA2306/kakeibo` | initial-review-current | 日本語で家計data、非公開境界、処理方法、制約を説明 |
| `KAFKA2306/auto-invest` | initial-review-current | 日本語で自動投資研究、実行境界、risk、検証を説明 |
| `KAFKA2306/expense2` | initial-review-current | 日本語でexpense data処理、利用方法、構造、制約を説明 |
| `KAFKA2306/adaptive_wear_generator_pro` | initial-review-current | 日本語で公開研究実装、品質監査、legacy/private版との境界を説明 |
| `KAFKA2306/etf` | initial-review-current | 2024年Notebook・pickle snapshot、最新性非保証、Sharpe ratio前提、pickle riskを明示 |
| `KAFKA2306/finAnalist` | initial-review-current | source付き記述pipeline、未実装機能、raw close制約、test方法を説明 |

## snapshot・fork再監査

| repository | 状態 | 確認事項 |
|---|---|---|
| `KAFKA2306/expense` | snapshot-or-fork-review | upstream、取得時点、独自差分、license、同期方針を確認する |

## 次の優先順

1. READMEが存在しない、READMEだけで実装済みを装う、固定数値・placeholderを含むrepository
2. 金融、投資、個人data、外部APIなど誤認時の影響が大きいrepository
3. GitHub PagesまたはCloudflare Pagesを公開するrepository
4. 現在も頻繁に更新される正準repository
5. 同一目的の重複repository
6. fork、source snapshot、upstream mirror
7. 停止中・archive候補・小規模実験

次のbatchは未確認50件から、小規模金融、README-only、公開site、重複候補を優先します。

## 監査手順

1. default branchのREADMEを読む
2. 最近のmerge、主要設定、package、workflow、公開URLを確認する
3. READMEの目的、機能、command、構造、正準data、公開、制約と実体を照合する
4. 大容量fileはContents APIの表示だけでsizeや内容を判断せず、checkout・blob metadata・CIで確認する
5. 不足があればrepositoryごとのIssue・branch・PRで修正する
6. CIまたは適切な実体確認を行う
7. merge後にdefault branchのREADMEを読み戻す
8. この台帳とIssue #3へ証拠を記録する

README監査で製品障害を発見した場合、READMEへ隠さず記載し、実装修復はIncidentへ分離します。監査側の誤りを発見した場合も履歴を消さず、訂正内容・原因・再発防止を残します。
