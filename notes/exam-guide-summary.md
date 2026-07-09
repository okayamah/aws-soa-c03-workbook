# SOA-C03 試験ガイド要点整理

## 試験概要

| 項目 | 内容 |
|---|---|
| 正式名称 | AWS Certified CloudOps Engineer - Associate (SOA-C03) |
| 旧名称 | SysOps Administrator - Associate (SOA-C02) |
| 問題形式 | 択一選択 + 複数選択（試験ラボは現在休止中） |
| 設問数 | 採点対象 50問 + 採点対象外 15問 = 計65問 |
| 試験時間 | 130分 |
| 合格スコア | 720 / 1000 |
| 推測ペナルティ | なし（わからなくても必ず回答すべき） |

## コンテンツ分野と重み

| # | 分野 | 比率 | タスク数 |
|---|---|---|---|
| 1 | モニタリング、ログ記録、分析、修復、パフォーマンスの最適化 | **22%** | 3 |
| 2 | 信頼性と事業の継続性 | **22%** | 3 |
| 3 | デプロイ、プロビジョニング、オートメーション | **22%** | 2 |
| 4 | セキュリティとコンプライアンス | 16% | 2 |
| 5 | ネットワークとコンテンツ配信 | 18% | 3 |

> **分野 1・2・3 で合計 66%**。ここが最優先。

---

## 全13タスクと出題スキル

### 分野 1: モニタリング、ログ記録、分析、修復、パフォーマンスの最適化（22%）

#### タスク 1.1: メトリクス、アラーム、フィルターを実装する
| スキル | 内容 | 主要サービス |
|---|---|---|
| 1.1.1 | ワークロード（サーバーレス/コンピューティング/AI）のモニタリング・ログ記録を設定 | CloudWatch, CloudTrail, Managed Prometheus |
| 1.1.2 | EC2/ECS/EKS から メトリクス・ログを収集する CloudWatch エージェントの設定・管理 | CloudWatch Agent |
| 1.1.3 | CloudWatch アラームの設定・トラブルシューティング（複合アラーム、EventBridge 連携含む） | CloudWatch Alarms, EventBridge |
| 1.1.4 | 複数アカウント・リージョンにわたる CloudWatch ダッシュボードの作成・管理 | CloudWatch Dashboards |
| 1.1.5 | SNS 通知の設定、アラームからの SNS 呼び出し | SNS |

#### タスク 1.2: モニタリングと可用性のメトリクスで問題を特定・修復する
| スキル | 内容 | 主要サービス |
|---|---|---|
| 1.2.1 | パフォーマンスメトリクスの分析と修復戦略の自動化 | CloudWatch, Lambda, SSM, CloudTrail, **Kiro**, **AWS DevOps Agent** |
| 1.2.2 | EventBridge でのイベント送信・配信、イベントバスルールのトラブルシューティング | EventBridge |
| 1.2.3 | SSM Automation ランブック（カスタム・事前定義済み）の作成・実行 | Systems Manager Automation |

#### タスク 1.3: コンピューティング・ストレージ・DB のパフォーマンス最適化
| スキル | 内容 | 主要サービス |
|---|---|---|
| 1.3.1 | コンピューティングリソースの最適化、パフォーマンス問題の修復 | Compute Optimizer, リソースタグ |
| 1.3.2 | EBS メトリクス分析、ボリュームタイプの最適化 | EBS |
| 1.3.3 | S3 パフォーマンス戦略の実装・最適化 | DataSync, S3 Transfer Acceleration, マルチパートアップロード, ライフサイクルポリシー |
| 1.3.4 | 共有ストレージの評価・選択・最適化 | EFS, FSx, **S3 Files** |
| 1.3.5 | RDS メトリクスのモニタリング、パフォーマンス設定変更 | RDS Performance Insights, RDS Proxy |
| 1.3.6 | EC2 インスタンスとストレージ・ネットワーク機能の最適化 | EC2 プレイスメントグループ |

> **注意**: タスク 1.3 は SOA-C02 の「第6分野: コストとパフォーマンスの最適化」が再分類されたもの。

---

### 分野 2: 信頼性と事業の継続性（22%）

#### タスク 2.1: スケーラビリティと伸縮性を実装する
| スキル | 内容 | 主要サービス |
|---|---|---|
| 2.1.1 | コンピューティング環境のスケーリングメカニズムの設定・管理 | Auto Scaling, EC2 Auto Scaling |
| 2.1.2 | キャッシュの実装による動的スケーラビリティの強化 | CloudFront, ElastiCache |
| 2.1.3 | マネージド DB のスケーリングの設定・管理 | RDS, DynamoDB |

#### タスク 2.2: 可用性と耐障害性に優れた環境を実装する
| スキル | 内容 | 主要サービス |
|---|---|---|
| 2.2.1 | ELB と Route 53 ヘルスチェックの設定・トラブルシューティング | ELB, Route 53 |
| 2.2.2 | 耐障害性を備えたシステム（マルチ AZ 配置）の設定 | RDS Multi-AZ, ECS, EC2 |

#### タスク 2.3: バックアップと復元の戦略を実装する
| スキル | 内容 | 主要サービス |
|---|---|---|
| 2.3.1 | スナップショットとバックアップの自動化 | AWS Backup, EBS スナップショット, RDS スナップショット |
| 2.3.2 | RTO/RPO/コスト要件を満たすデータベース復元（ポイントインタイムリストアなど） | RDS, DynamoDB |
| 2.3.3 | ストレージサービスのバージョニングの実装 | S3, FSx |
| 2.3.4 | DR 手順とベストプラクティスの実施 | バックアップ&リストア, パイロットライト, ウォームスタンバイ, アクティブ/アクティブ |

---

### 分野 3: デプロイ、プロビジョニング、オートメーション（22%）

#### タスク 3.1: クラウドリソースのプロビジョニングとメンテナンス
| スキル | 内容 | 主要サービス |
|---|---|---|
| 3.1.1 | AMI とコンテナイメージの作成・管理 | EC2 Image Builder, ECR |
| 3.1.2 | CloudFormation と CDK で AWS リソースを作成・管理 | **CloudFormation**, **CDK** |
| 3.1.3 | デプロイの問題の特定・修復（サブネットサイジング、CFn エラー、アクセス許可） | CloudFormation |
| 3.1.4 | 複数リージョン・アカウントへのリソースプロビジョニング | RAM, **CloudFormation StackSets** |
| 3.1.5 | デプロイ戦略の実装（ブルー/グリーン、ローリング、Canary など） | ― |
| 3.1.6 | サードパーティツールでのリソース管理・自動化 | **Terraform**, Git |

#### タスク 3.2: 既存のリソース管理の自動化
| スキル | 内容 | 主要サービス |
|---|---|---|
| 3.2.1 | オペレーションプロセスの自動化 | Systems Manager（Automation, State Manager, Patch Manager） |
| 3.2.2 | イベント駆動型オートメーションの実装 | Lambda, S3 イベント通知, EventBridge, **AWS DevOps Agent** |

---

### 分野 4: セキュリティとコンプライアンス（16%）

#### タスク 4.1: セキュリティ・コンプライアンスのツール・ポリシーの実装・管理
| スキル | 内容 | 主要サービス |
|---|---|---|
| 4.1.1 | IAM の機能の実装（パスワードポリシー、MFA、ロール、フェデレーション、ポリシー条件） | IAM |
| 4.1.2 | アクセス問題のトラブルシューティングと監査 | CloudTrail, IAM Access Analyzer, IAM Policy Simulator |
| 4.1.3 | マルチアカウント戦略の安全な実装 | **Organizations**, **SCP**, **IAM Identity Center** |
| 4.1.4 | Trusted Advisor セキュリティチェックに基づく修復 | Trusted Advisor |
| 4.1.5 | コンプライアンス要件と継続的モニタリングの実施 | AWS Config, **コンフォーマンスパック** |

#### タスク 4.2: データとインフラストラクチャの保護戦略の実装
| スキル | 内容 | 主要サービス |
|---|---|---|
| 4.2.1 | データ分類スキームの実装・適用 | Macie |
| 4.2.2 | 保管時の暗号化の実装・設定・トラブルシューティング | **KMS** |
| 4.2.3 | 転送時の暗号化の実装・設定・トラブルシューティング | **ACM** |
| 4.2.4 | シークレットの安全な保管 | Secrets Manager, SSM Parameter Store |
| 4.2.5 | セキュリティレポートの設定と結果の修復 | Security Hub, GuardDuty, Config, Inspector, **AWS Security Agent** |

---

### 分野 5: ネットワークとコンテンツ配信（18%）

#### タスク 5.1: ネットワーク機能と接続の実装・最適化
| スキル | 内容 | 主要サービス |
|---|---|---|
| 5.1.1 | VPC の設定（サブネット、ルートテーブル、NACL、SG、NAT GW、**Egress-Only IGW**） | VPC |
| 5.1.2 | プライベートネットワーク接続の設定 | **VPC エンドポイント**, **PrivateLink**, VPC ピアリング |
| 5.1.3 | ネットワーク保護サービスの監査 | Route 53 Resolver DNS Firewall, WAF, Shield, **Network Firewall** |
| 5.1.4 | ネットワークアーキテクチャのコスト最適化 | ― |

#### タスク 5.2: ドメイン、DNS サービス、コンテンツ配信の設定
| スキル | 内容 | 主要サービス |
|---|---|---|
| 5.2.1 | DNS の設定 | Route 53 Resolver |
| 5.2.2 | Route 53 のルーティングポリシー・設定・クエリログ記録 | Route 53 |
| 5.2.3 | コンテンツ・サービス配信の設定 | CloudFront, Global Accelerator |

#### タスク 5.3: ネットワーク接続問題のトラブルシューティング
| スキル | 内容 | 主要サービス |
|---|---|---|
| 5.3.1 | VPC 設定のトラブルシューティング（サブネット、ルートテーブル、NACL、SG、**Transit GW**、NAT GW） | VPC |
| 5.3.2 | ネットワークログの収集・解釈 | VPC フローログ, ELB アクセスログ, WAF ログ, CloudFront ログ, コンテナログ |
| 5.3.3 | CloudFront キャッシュの問題の特定・修復 | CloudFront |
| 5.3.4 | ハイブリッド接続・プライベート接続の問題のトラブルシューティング | Site-to-Site VPN, Client VPN, Transit Gateway |
| 5.3.5 | CloudWatch ネットワークモニタリングサービスの設定・分析 | CloudWatch |

---

## SOA-C02 → SOA-C03 の主な変更点

### 重み変更
| 分野 | C02 | C03 | 変化 |
|---|---|---|---|
| 1. モニタリング・パフォーマンス | 20% | **22%** | ↑（旧第6分野のパフォーマンスを吸収） |
| 2. 信頼性 | 16% | **22%** | ↑↑ |
| 3. デプロイ | 18% | **22%** | ↑ |
| 4. セキュリティ | 16% | 16% | → |
| 5. ネットワーク | 18% | 18% | → |
| 6. コスト・パフォーマンス | 12% | **廃止** | 分野1に統合 |

### 追加されたコンテンツ・サービス
- **コンテナ**: Amazon ECR, ECS, EKS が対象に追加
- **IaC**: AWS CDK、Terraform が明示的に対象に
- **AI/ML**: Amazon Bedrock、Kiro、AWS DevOps Agent
- **セキュリティ**: AWS Security Agent、IAM Identity Center の明記
- **ネットワーク**: CloudWatch ネットワークモニタリング、Egress-Only IGW
- **ストレージ**: Amazon S3 Files
- **DR**: パイロットライト、ウォームスタンバイ等の DR パターン明記
- **モニタリング**: Managed Prometheus / Managed Grafana

### 削除されたコンテンツ
- S3 静的ウェブホスティング（タスク 5.2 から削除）
- 旧第6分野（コストとパフォーマンスの最適化）→ タスク 1.3 に再分類

---

## 対象サービス一覧（主要カテゴリ別）

### コンピューティング
EC2, EC2 Image Builder, Lambda

### コンテナ（★新規追加）
ECR, ECS, EKS

### データベース
Aurora, Aurora Serverless v2, DynamoDB, DAX, ElastiCache, RDS, RDS Proxy

### マネジメント・ガバナンス
Auto Scaling, **CDK**, **CloudFormation**, CloudTrail, CloudWatch, Compute Optimizer, Config, Control Tower, **DevOps Agent**, Health Dashboard, **Managed Grafana**, **Managed Prometheus**, Organizations, RAM, Service Catalog, SCP, Systems Manager, Trusted Advisor, **VPC IPAM**

### ネットワーク
Application Recovery Controller, Client VPN, CloudFront, Elastic IP, Global Accelerator, **PrivateLink**, Route 53, **Route 53 Resolver DNS Firewall**, Site-to-Site VPN, Transit Gateway, VPC, VPC エンドポイント, VPC フローログ, VPC ピアリング, **VPC Reachability Analyzer**

### セキュリティ
ACM, EC2 SG, **Egress-Only IGW**, ELB, GuardDuty, IAM Access Analyzer, **IAM Identity Center**, IAM, Inspector, IGW, KMS, **Macie**, **Network Firewall**, NAT GW, NACL, Secrets Manager, **Security Agent**, Security Hub, Shield, WAF

### ストレージ
Backup, EBS, EFS, FSx, S3, Storage Gateway

### その他
Athena, Data Firehose, EventBridge, SNS, SQS, Step Functions, SES, Cost Explorer, Savings Plans, X-Ray, **Kiro**, **Bedrock**, DataSync
