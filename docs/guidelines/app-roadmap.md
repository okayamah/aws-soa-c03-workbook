# サンプルアプリ「FastAPI ToDo」ロードマップ

## アプリ概要

- **名前**：FastAPI ToDo Workbook
- **機能**：ToDo の作成・取得・更新・削除（CRUD のみ）。認証・UI は最小限。
- **言語/フレームワーク**：Python 3.12 / FastAPI
- **配置**：`app/`

## 目標アーキテクチャ（Week 5 完成形）

```
Route 53 → CloudFront → ALB → ECS on Fargate (FastAPI) → DynamoDB
   + Secrets Manager / KMS / CloudWatch / Systems Manager Parameter Store
   + AWS Backup / X-Ray
```

## 週ごとの進化

| 週 | テーマ | アプリへの変更 |
|---|---|---|
| Week 1 | 監視 | **API Gateway + Lambda（Mangum）+ DynamoDB** で最小デプロイ／CloudWatch Logs・Alarm・ダッシュボード |
| Week 2 | 自動化・IaC | 全リソースを **CloudFormation 化**／Change Set / Drift Detection／SSM Parameter Store で設定管理 |
| Week 3 | 信頼性・DR | **ECS Fargate + ALB に格上げ**／DynamoDB へ AWS Backup ／**別スタックで RDS Multi-AZ 練習** |
| Week 4 | ネットワーク | VPC を Public/Private で構築／**CloudFront を前段に追加**／VPC Endpoint で DynamoDB に到達 |
| Week 5 | セキュリティ＋コンテナ | IAM 最小権限化／KMS／Secrets Manager／**X-Ray でトレース**／Fargate 完成形 |

> Week 6〜8 は演習＋仕上げ＋受験のため、アプリ変更は最小限。

## 出題範囲と優先度

| 分野 | 比率 | 状態 |
|---|---|---|
| Monitoring, Logging, Analysis, Remediation, Performance | 22% | 未着手 |
| Reliability and Business Continuity | 22% | 未着手 |
| Deployment, Provisioning, and Automation | 22% | 未着手（**最重要弱点候補：CloudFormation**） |
| Networking and Content Delivery | 18% | 未着手 |
| Security and Compliance | 16% | 未着手 |

新範囲として **ECS / EKS / Fargate / CDK / X-Ray / Prometheus・Grafana 統合** に注意。
