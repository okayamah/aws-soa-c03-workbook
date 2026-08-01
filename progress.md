# Progress Tracker

8週間 × 1日1時間 = 約56時間の進捗を記録する。模試スコアと弱点も集約する。

---

## 週次チェックリスト

- [x] Week 0：環境構築（公式ガイド精読／AWS 設定／リポジトリ整備／公式 Practice Question Set 初回）※GuardDuty は有料のためコスト方針で見送り
- [x] Week 1：監視＋アプリ初版（API Gateway + Lambda + DynamoDB）
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
| 2026-07-09 | AWS公式 Practice Question Set | 全分野 | 7/20 (35%) | 初回。全分野で知識不足が顕著。特に Deployment/Security/Networking が 25% |
| （Week 1 は模試なし） | — | — | — | ハンズオン中心の週。模試は Week 6 以降に本格実施予定 |
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
| Monitoring, Logging, Analysis, Remediation, Performance | ★★ | Lambda/DynamoDB/API Gateway を実機構築、CloudWatch Alarm・SNS・Dashboard まで動作確認済み（CLI）。CFn 化は Week 2 |
| Reliability and Business Continuity | ☆ | 未着手（Week 3 予定） |
| Deployment, Provisioning, and Automation | ☆ | 未着手（Week 2 で CloudFormation 集中学習：最重要弱点） |
| Networking and Content Delivery | ★ | API Gateway（HTTP API）のみ実機構築・検証済み。VPC/Route53/CloudFront 等は未着手 |
| Security and Compliance | ★ | IAM ロール・ポリシー（信頼ポリシー/管理ポリシー/インライン）のみ実機構築済み。Organizations/SCP/KMS/GuardDuty 等は未着手 |

---

## アプリ進化ログ（FastAPI ToDo）

| 週 | スタック構成 | デプロイ確認 | 主な追加サービス |
|---|---|---|---|
| Week 1 | API GW + Lambda + DynamoDB | ☑ | CloudWatch（Logs/Metrics/Alarm/Dashboard） |
| Week 2 | （Week 1 と同じ）全 CFn 化 | ☐ | CloudFormation / Change Set / Drift / SSM Parameter Store |
| Week 3 | ECS Fargate + ALB + DynamoDB | ☐ | ECS / ALB / AWS Backup（別途 RDS Multi-AZ 練習） |
| Week 4 | + VPC（Public/Private）+ CloudFront | ☐ | VPC / CloudFront / VPC Endpoint |
| Week 5 | + KMS + Secrets Manager + X-Ray | ☐ | IAM 最小化 / KMS / Secrets Manager / X-Ray |

---

## 週次レトロスペクティブ

### Week 0（〜2026-07-09）
- やったこと：AWS アカウント初期設定（MFA/IAMユーザー/Budgets/CloudTrail/Config）、公式試験ガイド精読、公式 Practice Question Set 初回（7/20, 35%）
- 学び：Deployment / Security / Networking が特に弱い（各25%）。GuardDuty は有料化タイミングの都合でコスト方針上見送り
- 次週への持ち越し：Week 1 監視ハンズオンへ

### Week 1（2026-07-13〜2026-08-02）
- やったこと：
  - Day 1：DynamoDB `Todos` テーブル作成（オンデマンド課金）、CloudWatch メトリクス発行確認
  - Day 2：FastAPI を Mangum 経由で Lambda にデプロイ、IAM 実行ロール構築、CloudWatch Logs 確認
  - Day 3：API Gateway（HTTP API）で公開、Lambda プロキシ統合・リソースベースポリシー
  - Day 4：CloudWatch アラーム3本（Lambda Errors / DynamoDB ThrottledRequests / API Gateway 5xx）+ SNS 通知 + Dashboard。アラーム発火の実機確認まで実施
  - 詳細な実行コマンドは [docs/handson-log/wk1.md](docs/handson-log/wk1.md)、体系ノートは notes/monitoring・notes/networking・notes/security に集約
- 学び：
  - Windows 特有の詰まりどころ（pip の cp932 デコードエラー、Lambda 向けクロスプラットフォームパッケージング、PowerShell の curl エイリアス）が実務上の落とし穴として蓄積できた
  - IAM ロール＝信頼ポリシー＋アクセス許可ポリシーの構造、CloudWatch Alarm は SNS 経由でしか通知できない、など Security/Monitoring 分野の基礎が実機を通じて定着
  - 実カレンダーでは Week 1 相当に約3週間を要した（1日1時間ペースなら本来数日で終わる分量）。ペース維持ができているか要注意
- 次週への持ち越し：
  - Week 2：Todos テーブルは CloudFormation **リソースインポート**で取り込み（案B、Resource Import の実地学習を兼ねる）、Lambda・API Gateway・IAM・CloudWatch Alarm/SNS/Dashboard 一式を新規 CFn テンプレートで再構築
  - mistakes.md は Week 0 以降更新なし。Week 2 も模試は実施しない想定（ハンズオン中心が継続）

### Week 2 ...
