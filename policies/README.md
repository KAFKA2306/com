# 共通方針

このディレクトリには、KAFKA2306配下の複数リポジトリにまたがる作業で守る共通方針を置きます。

- [完了条件](completion.md)
- [証拠条件](evidence.md)
- [リポジトリ境界](repository-boundaries.md)
- [破壊的操作](destructive-actions.md)
- [外部情報の検証](source-verification.md)
- [README方針](readme.md)
- [権限](permissions.md)
- [状態報告](status-reporting.md)

各リポジトリは、ドメイン固有の事情に応じて、これより厳しい規則を追加できます。ただし、横断作業において共通方針を暗黙に弱めてはいけません。

READMEは人間向けの正準入口、AGENTS.mdはエージェント向けの操作契約として分離します。リポジトリの責務、利用方法、正準データ、検証、運用、制約が変わる変更では、README更新の要否を必ず確認します。
