# AWS 環境ルール

## リージョン・コスト

1. **リージョンは `ap-northeast-1`（東京）に固定**。明示指定なくマルチリージョンには触れない。
2. **インフラ費用上限：¥2,000**。AWS 無料プラン（$200／6か月）を主用。`AWS Budgets` で月額 ¥1,500 のアラートを設定済みである前提。

## タグ規約

リソースには必ず以下のタグを付ける：

- `Project=soa-c03-workbook`
- `App=fastapi-todo`
- `Week=<N>`
- `Owner=<user>`

## クリーンアップ

- **作ったら必ずクリーンアップ**。IaC やコマンド列を生成するときは、**末尾に必ず削除手順をセットで提示**すること。
- スタック名は `wk{N}-{purpose}` 形式（例：`wk2-cfn-changeset-demo`、`wk3-todo-fargate`）。

## 高コストサービスの扱い

| サービス | 方針 |
|---|---|
| ALB（約 $0.025/h ≒ 月 $18） | 検証セッションのみ起動 |
| NAT Gateway | 原則使わない（VPC Endpoint で代替） |
| RDS Multi-AZ | Week 3 の練習でのみ短時間起動 |
| EKS コントロールプレーン | 概念学習中心、最小限のみ起動 |
| DynamoDB / Lambda | オンデマンドで安価なので残してよい |

## シークレット管理

- AWS 認証情報・シークレット・PEM・`.env` は **絶対にコミットしない**。`.gitignore` で除外済み。
- 検証用の値も AWS Parameter Store / Secrets Manager に置く。
- うっかりコミットを検出したら、その時点で必ず利用者に警告すること。
