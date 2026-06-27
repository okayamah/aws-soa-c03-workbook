# aws-soa-c03-workbook

AWS Certified CloudOps Engineer – Associate（**SOA-C03**）取得のための **学習教材兼ハンズオン環境**。
ノート・IaC・誤答ログを 1 リポジトリで管理し、Claude Code を対話型ハンズオン講師として使いながら、**FastAPI 製の ToDo アプリを毎週リファクタリングして育てる** 8 週間学習プロジェクト。

> 旧称：AWS Certified SysOps Administrator – Associate（SOA-C02 の後継／2025年9月30日〜）

---

## 目的・方針

- AWS 実務経験を **体系化し、SOA-C03 取得で対外証明する**。
- 「読む → 書く（IaC）→ 動かす → 振り返る」のサイクルを毎日回す。
- **学習期間：8週間 × 1日1時間（合計 約56時間）**
- **インフラ費用上限：¥2,000**（AWS 無料プランの $200 クレジット範囲内で運用）
- **成果物：8週間の終わりに動作する FastAPI ToDo アプリ＋IaC 一式**

詳細な計画は [`plan/SOA-C03_学習計画.md`](./plan/SOA-C03_学習計画.md)、Claude Code 用ルールは [`CLAUDE.md`](./CLAUDE.md) を参照。

## サンプルアプリ「FastAPI ToDo」

学習中は単発の IaC を量産せず、**同じアプリを毎週リファクタリングして育てる**。SOA-C03 の各分野が「アプリ運用の一部」として体系化される構成。

### 目標アーキテクチャ（Week 5 完成形）

```
Route 53 → CloudFront → ALB → ECS on Fargate (FastAPI) → DynamoDB
   + Secrets Manager / KMS / CloudWatch / Systems Manager Parameter Store
   + AWS Backup / X-Ray
```

### 週ごとの進化

| 週 | テーマ | アプリへの変更 |
|---|---|---|
| Week 1 | 監視 | API Gateway + Lambda（Mangum）+ DynamoDB で最小デプロイ／CloudWatch Logs・Alarm・Dashboard |
| Week 2 | 自動化・IaC | 全リソースを CloudFormation 化／Change Set / Drift Detection／SSM Parameter Store |
| Week 3 | 信頼性・DR | ECS Fargate + ALB に格上げ／DynamoDB へ AWS Backup ／別スタックで RDS Multi-AZ 練習 |
| Week 4 | ネットワーク | VPC を Public/Private で構築／CloudFront を前段に追加／VPC Endpoint |
| Week 5 | セキュリティ＋コンテナ | IAM 最小権限化／KMS／Secrets Manager／X-Ray／Fargate 完成形 |

## 試験概要

| 項目 | 内容 |
|---|---|
| 試験コード | SOA-C03 |
| 問題数 / 時間 | 65問 / 130分 |
| 合格点 | 720 / 1000（約72%） |
| 受験料 | 約 $150 USD |
| 有効期限 | 3年 |
| 実技ラボ | 廃止（選択式のみ） |

### 出題比率

| 分野 | 比率 |
|---|---|
| Monitoring, Logging, Analysis, Remediation, Performance | 22% |
| Reliability and Business Continuity | 22% |
| Deployment, Provisioning, and Automation | 22% |
| Networking and Content Delivery | 18% |
| Security and Compliance | 16% |

## 学習サイクル

```
公式ガイド読了 / Skill Builder 無料コース
   ↓
週次テーマのインプット（毎日：その日のサブトピックを20分）
   ↓
Claude Code 主導で IaC を書いて実機デプロイ（毎日：30分）
   ↓
動作・観察 → ノート化 → クリーンアップ（毎日：10分）
   ↓  ※ ここまでが「日次の micro cycle」
   ↓
週末：Udemy 375問 模試で演習 → 誤答を mistakes.md へ
   ↓
弱点を翌週の日次サイクルへフィードバック
   ↓
通し模試で 80〜85% 安定 → 受験予約
```

## 教材

| 区分 | 教材 | 費用 |
|---|---|---|
| 公式ガイド | AWS CloudOps Engineer – Associate 試験ガイド（PDF） | ¥0 |
| 体系インプット | AWS Skill Builder 無料コース（Exam Readiness 等） | ¥0 |
| 公式問題 | AWS 公式 Practice Question Set（Skill Builder 無料枠） | ¥0 |
| 問題集（メイン） | Udemy「CloudOps エンジニア・アソシエイト 模擬試験問題集 6回分375問」 | 約 ¥1,500〜2,600 |
| 実機環境 | AWS 無料プラン（$200／6か月） | ¥0〜¥2,000 |
| 学習支援 | Claude Code | 既存契約 |

## ディレクトリ構成

```
aws-soa-c03-workbook/
├── README.md                 # 本ファイル
├── CLAUDE.md                 # Claude Code 用コンテキスト・運用ルール
├── .gitignore
├── .gitattributes
├── plan/
│   └── SOA-C03_学習計画.md   # 8週間スケジュール詳細
├── app/                      # FastAPI ToDo アプリ本体（Week 1 で初版作成）
│   └── README.md
├── notes/                    # サービス別・分野別ノート
│   ├── monitoring/
│   ├── reliability/
│   ├── deployment/
│   ├── networking/
│   └── security/
├── iac/                      # 実機検証用 IaC
│   ├── cloudformation/       # 試験最重要
│   ├── cdk/                  # 余裕があれば
│   └── README.md
├── scripts/                  # AWS CLI ヘルパー
├── mistakes.md               # 誤答ログ
└── progress.md               # 週次進捗・模試スコア
```

## セットアップ（Windows）

### 1. 必要ツール

```powershell
# AWS CLI v2（Windows MSI）
# https://awscli.amazonaws.com/AWSCLIV2.msi

aws --version

# Python 3.12
python --version

# cfn-lint
pip install cfn-lint
cfn-lint --version

# Git は導入済み前提
```

### 2. AWS アカウント設定

```powershell
# 学習用の個人 AWS アカウントを作成（無料プラン対象は 2025/7/15 以降の新規）
aws configure
# - Default region name : ap-northeast-1
# - IAM ユーザー＋アクセスキー（最小権限）を推奨。ルートユーザーは使わない
```

### 3. Budgets で予算ガード

- AWS マネジメントコンソール → Billing → Budgets
- **月額 ¥1,500（または $10）** のコストアラートを作成
- 通知先メールを設定

### 4. リポジトリの初期化（Windows / PowerShell）

```powershell
# 改行設定（リポジトリの .gitattributes が正なので、グローバルでは true 推奨）
git config --global core.autocrlf input

# Python 仮想環境（FastAPI 用）
cd app
python -m venv .venv
.venv\Scripts\Activate.ps1
# FastAPI 関連は Week 1 で追加
```

## AWS コスト管理ルール

- **リージョンは `ap-northeast-1` 固定**
- 全リソースに以下のタグを付与
  - `Project=soa-c03-workbook`
  - `App=fastapi-todo`
  - `Week=<N>`
  - `Owner=<user>`
- スタック名は `wk{N}-{purpose}` 形式（例：`wk2-cfn-changeset-demo`、`wk3-todo-fargate`）
- **作ったら必ず削除**。学習が終わったら `aws cloudformation delete-stack` で破棄
- 高コスト常時稼働サービス（NAT Gateway / ALB / RDS / EKS）は短時間検証→即削除
- **NAT Gateway は原則使わず VPC Endpoint で代替**
- 毎日の最後に Claude Code に「今日作ったリソースの掃除」を依頼する習慣を作る

## 進捗トラッカー

詳細は [`progress.md`](./progress.md) で管理。

- [ ] Week 0：環境構築（公式ガイド精読、AWS設定、リポジトリ整備）
- [ ] Week 1：監視＋アプリ初版（API Gateway + Lambda + DynamoDB）
- [ ] Week 2：自動化・IaC（CloudFormation / Systems Manager）
- [ ] Week 3：信頼性・DR（ECS Fargate + ALB へ格上げ／RDS Multi-AZ 練習）
- [ ] Week 4：ネットワーク（VPC / CloudFront / VPC Endpoint）
- [ ] Week 5：セキュリティ＋コンテナ（IAM / KMS / Secrets Manager / X-Ray）
- [ ] Week 6：演習①（Udemy 375問を分野別高速周回）
- [ ] Week 7：演習②＋仕上げ（通し模試 → 受験予約）
- [ ] Week 8：最終調整 → **受験**

### 模試スコア推移目標

| 周回 | 目標正答率 |
|---|---|
| 1回目 | 70% |
| 2回目 | 75% |
| 3回目 | 80% |
| 4回目 | **85%（→ 受験予約）** |

## Claude Code の使い方（要点）

このリポジトリのルートで `claude` を起動すると、`CLAUDE.md` の内容を前提に動作する。よくある依頼例：

```
# ハンズオン指南
「Week 1 のテーマは監視。FastAPI ToDo アプリの最小版を
 API Gateway + Lambda + DynamoDB で立ち上げる手順を、
 CloudWatch ログ・メトリクス・アラームと合わせて出して」

# IaC 作成
「iac/cloudformation/wk2-todo-data.yaml に DynamoDB テーブルを書いて。
 タグ規約に従い、PITR 有効、cfn-lint も通して」

# ノート生成
「notes/monitoring/cloudwatch-logs.md に メトリクスフィルタ /
 サブスクリプションフィルタ / Logs Insights の違いを §9 の書式でまとめて」

# 進捗管理
「mistakes.md の誤答を分野別に集計し、明日1時間でやるべきことを優先順位付きで」

# コスト見守り
「いまアカウントに残っている学習用リソースを CLI で一覧し、
 消すべきものとコマンド列を出して」
```

詳細な運用ルールは [`CLAUDE.md`](./CLAUDE.md) を参照。

## 注意

- 本リポジトリは個人の学習用記録。AWS 試験問題そのものや有料教材の問題文・解説は **コミットしない**。
- 認証情報・PEM・`.env` は絶対にコミットしない。
