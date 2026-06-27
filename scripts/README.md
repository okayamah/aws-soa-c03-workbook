# scripts/

AWS CLI ヘルパー類。Claude Code に生成させた便利スクリプトを置く場所。

## 想定するスクリプト

| ファイル | 目的 |
|---|---|
| `cleanup-all.ps1` | `Project=soa-c03-workbook` タグの全リソース／全 CFn スタック削除（破壊的・確認プロンプト付き） |
| `list-resources.ps1` | 学習用リソースをタグ検索で一覧 |
| `cost-check.ps1` | 当月の AWS コストを Cost Explorer 経由で簡易確認 |
| `seed-dynamodb.py` | ToDo アプリの初期データ投入 |

> ファイルは必要になった時点で Claude Code に生成依頼する。最初から作り込まない。
