---
name: aws
description: このプロジェクトで多用する AWS CLI コマンドのチートシート。「認証通ってる？」「AWSコマンド教えて」「リソース確認」「ログ見たい」「コスト確認」と言われたら使用。
---

# AWS CLI チートシート

本プロジェクト（リージョン `ap-northeast-1` 固定・タグ `Project=soa-c03-workbook`）で頻用するコマンド集。
ユーザーの依頼に該当するセクションのコマンドを提示する。read-only 系はそのまま実行してよいが、**変更系（deploy / delete / put 系）は提示のみとし、実行前に必ず確認を取る**。

## ログイン（認証情報の設定）

```powershell
aws configure                                # IAM ユーザーのアクセスキーを対話設定（本プロジェクトの基本）
aws configure --profile <name>              # 複数アカウント・ユーザーを使い分ける場合
aws sso login --profile <name>              # IAM Identity Center（SSO）利用時のログイン
```

> **注**: IAM ユーザー（アクセスキー）方式ではログイン操作は不要。`aws configure` で一度設定すれば有効。
> 認証エラーが出たら下の `aws sts get-caller-identity` で状態を確認する。
> アクセスキーは `~/.aws/credentials` に保存される。**絶対にコミットしない**。

## 認証・環境確認

```powershell
aws sts get-caller-identity                  # 認証が通っているか（アカウントID・IAMユーザー確認）
aws configure list                           # 使用中のプロファイル・キー・リージョンの出所
aws configure get region                     # デフォルトリージョン（ap-northeast-1 であること）
aws --version                                # AWS CLI v2 であること
```

## リソース棚卸し（タグ検索）

```powershell
# プロジェクトタグが付いた全リソース
aws resourcegroupstaggingapi get-resources `
  --tag-filters Key=Project,Values=soa-c03-workbook --region ap-northeast-1

# 週単位で絞る
aws resourcegroupstaggingapi get-resources `
  --tag-filters Key=Project,Values=soa-c03-workbook Key=Week,Values=1 --region ap-northeast-1
```

## CloudFormation

```powershell
# スタック一覧（稼働中のみ）
aws cloudformation list-stacks `
  --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --region ap-northeast-1

# スタックの詳細・出力値
aws cloudformation describe-stacks --stack-name <stack> --region ap-northeast-1

# デプロイ失敗時のエラー調査（直近イベントから原因を探す）
aws cloudformation describe-stack-events --stack-name <stack> --region ap-northeast-1 `
  --query "StackEvents[?ResourceStatus=='CREATE_FAILED' || ResourceStatus=='UPDATE_FAILED'].[LogicalResourceId,ResourceStatusReason]"

# 検証 → Lint → デプロイの定型（詳細は docs/guidelines/commands.md）
aws cloudformation validate-template --template-body file://iac/cloudformation/<file>.yaml
cfn-lint iac/cloudformation/<file>.yaml
```

## DynamoDB（Week 1〜）

```powershell
aws dynamodb list-tables --region ap-northeast-1
aws dynamodb describe-table --table-name <table> --region ap-northeast-1
aws dynamodb scan --table-name <table> --max-items 10 --region ap-northeast-1   # 中身を少しだけ確認
```

## Lambda

```powershell
aws lambda list-functions --region ap-northeast-1 --query "Functions[].[FunctionName,Runtime,LastModified]"

# テスト実行（結果は out.json に保存）
aws lambda invoke --function-name <fn> --payload '{}' out.json `
  --cli-binary-format raw-in-base64-out --region ap-northeast-1
```

## CloudWatch（Week 1 のテーマ）

```powershell
# ログをリアルタイム追尾（デバッグの主力）
aws logs tail /aws/lambda/<fn> --follow --region ap-northeast-1

# ロググループ一覧
aws logs describe-log-groups --region ap-northeast-1 --query "logGroups[].logGroupName"

# アラーム一覧と現在の状態
aws cloudwatch describe-alarms --region ap-northeast-1 `
  --query "MetricAlarms[].[AlarmName,StateValue,MetricName]"
```

## コスト確認

```powershell
# 今月のコスト（サービス別）。日付は当月に置き換える
aws ce get-cost-and-usage `
  --time-period Start=2026-07-01,End=2026-08-01 `
  --granularity MONTHLY --metrics UnblendedCost `
  --group-by Type=DIMENSION,Key=SERVICE --region us-east-1

# 予算の消化状況（¥1,500 アラート）
aws budgets describe-budgets --account-id $(aws sts get-caller-identity --query Account --output text) --region us-east-1
```

> **注**: Cost Explorer（`ce`）と Budgets は us-east-1 エンドポイント固定。リージョン固定ルールの例外。

## クリーンアップ

削除手順は `/cleanup` スキルに従う（棚卸し → 分類 → 削除 → 残存確認）。
