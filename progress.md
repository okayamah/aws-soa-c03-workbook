# Progress Tracker

8週間 × 1日1時間 = 約56時間の進捗を記録する。模試スコアと弱点も集約する。

---

## 週次チェックリスト

- [ ] Week 0：環境構築（公式ガイド精読／AWS 設定／リポジトリ整備／公式 Practice Question Set 初回）
- [ ] Week 1：監視＋アプリ初版（API Gateway + Lambda + DynamoDB）
- [ ] Week 2：自動化・IaC（CloudFormation / Systems Manager）
- [ ] Week 3：信頼性・DR（ECS Fargate + ALB へ格上げ／RDS Multi-AZ 練習）
- [ ] Week 4：ネットワーク（VPC / CloudFront / VPC Endpoint）
- [ ] Week 5：セキュリティ＋コンテナ（IAM / KMS / Secrets Manager / X-Ray）
- [ ] Week 6：演習①（Udemy 375問 分野別高速周回）
- [ ] Week 7：演習②＋仕上げ（通し模試 → 受験予約）
- [ ] Week 8：最終調整 → 受験

---

## 模試スコア記録

| 日付 | 模試名 | 分野 | スコア | 所感 |
|---|---|---|---|---|
| YYYY-MM-DD | AWS公式 Practice Question Set | 全分野 | x/y | 初回・温度感把握 |
| | Udemy 375問 #1 | Monitoring | %/% | |
| | Udemy 375問 #2 | Reliability | %/% | |
| | Udemy 375問 #3 | Deployment | %/% | |
| | Udemy 375問 #4 | Networking | %/% | |
| | Udemy 375問 #5 | Security | %/% | |
| | Udemy 375問 #6 通し | 全分野 | %/% | |
| | 公式 Pretest / Practice Exam | 全分野 | %/% | 仕上げ |

### 推移目標

| 周回 | 目標 | 実績 |
|---|---|---|
| 1回目 | 70% | |
| 2回目 | 75% | |
| 3回目 | 80% | |
| 4回目 | **85%（→ 受験予約）** | |

---

## 分野別の到達状況

5段階：☆未着手／★インプット済／★★IaC実機済／★★★演習で正答率 70%／★★★★ 80%以上で安定

| 分野 | 状況 | メモ |
|---|---|---|
| Monitoring, Logging, Analysis, Remediation, Performance | ☆ | |
| Reliability and Business Continuity | ☆ | |
| Deployment, Provisioning, and Automation | ☆ | |
| Networking and Content Delivery | ☆ | |
| Security and Compliance | ☆ | |

---

## アプリ進化ログ（FastAPI ToDo）

| 週 | スタック構成 | デプロイ確認 | 主な追加サービス |
|---|---|---|---|
| Week 1 | API GW + Lambda + DynamoDB | ☐ | CloudWatch（Logs/Metrics/Alarm/Dashboard） |
| Week 2 | （Week 1 と同じ）全 CFn 化 | ☐ | CloudFormation / Change Set / Drift / SSM Parameter Store |
| Week 3 | ECS Fargate + ALB + DynamoDB | ☐ | ECS / ALB / AWS Backup（別途 RDS Multi-AZ 練習） |
| Week 4 | + VPC（Public/Private）+ CloudFront | ☐ | VPC / CloudFront / VPC Endpoint |
| Week 5 | + KMS + Secrets Manager + X-Ray | ☐ | IAM 最小化 / KMS / Secrets Manager / X-Ray |

---

## 週次レトロスペクティブ

### Week 0（YYYY-MM-DD〜YYYY-MM-DD）
- やったこと：
- 学び：
- 次週への持ち越し：

### Week 1 ...
