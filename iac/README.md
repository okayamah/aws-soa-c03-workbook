# iac/

FastAPI ToDo アプリを動かすためのインフラ定義。**第一選択は CloudFormation（YAML）**。CDK は補助。Terraform は学習用の対比のみ（`notes/` 側でコード例を扱う）。

## スタック分割方針

アプリのリソースは複数スタックに分割し、依存は `Export`/`ImportValue` で繋ぐ。週が進むごとに `wk{N}-todo-*` でバージョンを増やしていく。

| スタック | 役割 | 例 |
|---|---|---|
| `wk{N}-todo-network` | VPC・Subnet・SG・VPC Endpoint | Week 4 以降 |
| `wk{N}-todo-data` | DynamoDB（PITR 有効・KMS 暗号化） | Week 1〜 |
| `wk{N}-todo-app` | Lambda / API Gateway もしくは ECS Service + ALB | Week 1〜 |
| `wk{N}-todo-monitoring` | CloudWatch Alarms / Dashboard / SNS | Week 1〜 |
| `wk{N}-todo-security` | IAM Role / KMS / Secrets Manager | Week 5 で本格化 |

スタック名規約：`wk{N}-{purpose}`（例：`wk2-todo-data`、`wk3-todo-app-fargate`）

## タグ規約（必須）

全リソースに以下を付与。CloudFormation テンプレ側で `Tags` セクションに統一して書く。

| Key | Value | 用途 |
|---|---|---|
| `Project` | `soa-c03-workbook` | リポジトリ単位 |
| `App` | `fastapi-todo` | アプリ単位 |
| `Week` | `1` 〜 `8` | 週単位の追跡 |
| `Owner` | `<your-handle>` | 多人数になる場合に備える |

## デプロイ手順（典型例）

```powershell
# パラメータ確認
aws cloudformation validate-template `
  --template-body file://iac/cloudformation/wk1-todo-data.yaml

# cfn-lint
cfn-lint iac/cloudformation/wk1-todo-data.yaml

# デプロイ
aws cloudformation deploy `
  --stack-name wk1-todo-data `
  --template-file iac/cloudformation/wk1-todo-data.yaml `
  --capabilities CAPABILITY_NAMED_IAM `
  --region ap-northeast-1 `
  --tags Project=soa-c03-workbook App=fastapi-todo Week=1 Owner=<your-handle>

# Outputs 確認
aws cloudformation describe-stacks `
  --stack-name wk1-todo-data `
  --query "Stacks[0].Outputs" `
  --region ap-northeast-1
```

## クリーンアップ手順（必須・毎日）

```powershell
# 単発削除
aws cloudformation delete-stack --stack-name wk1-todo-app --region ap-northeast-1
aws cloudformation delete-stack --stack-name wk1-todo-data --region ap-northeast-1

# 削除完了待ち
aws cloudformation wait stack-delete-complete --stack-name wk1-todo-app --region ap-northeast-1

# 残存リソースの確認（タグ検索）
aws resourcegroupstaggingapi get-resources `
  --tag-filters Key=Project,Values=soa-c03-workbook `
  --region ap-northeast-1
```

> **絶対ルール**：その日の検証が終わったら `scripts/` のクリーンアップヘルパー（または Claude Code 経由で生成したコマンド列）で必ず全削除する。

## ファイル命名規約

`{stack-prefix}.yaml`
- スタックのプレフィックスをファイル名にする（例：`wk1-todo-data.yaml`）
- Week ごとに増えていくのが正常。古いファイルは「歴史」として残してよい。
- 不要になった検証専用ファイルは `iac/cloudformation/_archive/` へ移動。

## CFn 記述ルール

- 必ず `Description` を書く
- `Parameters` は型・説明・デフォルト・許可値を明示
- `Outputs` は依存される値を Export 付きで出す
- IAM は最小権限。`*` を使う場合はインラインコメントで理由
- すべての対象リソースに `Tags` を付与
- `cfn-lint` を必ず通す
