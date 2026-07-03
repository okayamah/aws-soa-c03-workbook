---
name: cleanup
description: 学習用 AWS リソースの棚卸しと削除を行う。「掃除して」「今日のリソースを消す」「残ってるリソースを確認」「クリーンアップ」と言われたら使用。
---

# リソースクリーンアップ

毎日の学習終了時に実行する掃除手順。**削除コマンドは提示のみとし、実行前に必ず対象一覧をユーザーに確認させる。**

## 手順

1. **棚卸し**（read-only。aws-auditor サブエージェントに委譲してよい）
   ```
   aws resourcegroupstaggingapi get-resources --tag-filters Key=Project,Values=soa-c03-workbook --region ap-northeast-1
   aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --region ap-northeast-1
   ```
2. **消すもの / 残すものを分類**して提示（DynamoDB / Lambda はオンデマンドで安価なので残してよい。ALB / NAT GW / RDS / EKS は即削除）
3. **削除コマンド列**
   ```
   aws cloudformation delete-stack --stack-name <stack> --region ap-northeast-1
   aws cloudformation wait stack-delete-complete --stack-name <stack> --region ap-northeast-1
   ```
4. **残存確認**：手順1のタグ検索を再実行し、ゼロ（または意図した残置のみ）を確認
