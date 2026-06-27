# AWS Certified CloudOps Engineer – Associate（SOA-C03）学習計画【8週間・SE向け効率版】

## 1. 目的

- システムエンジニアとしての AWS 経験を **体系化し、SOA-C03 取得という形で対外的に証明**する。
- 取得対象：**AWS Certified CloudOps Engineer – Associate（SOA-C03）**（旧 SysOps Administrator – Associate の後継）。

## 2. 前提と方針

### 前提（学習者プロファイル）
- 普段はシステムエンジニアとして実務に従事。AWS にも触れる機会あり。
- AWS の **個別操作はできるが体系化されていない** 状態を、資格学習で整理する。
- 期間：**最長8週間 × 1日1時間 ＝ 約56時間**。
- インフラ費用上限：**¥2,000 以内**（学習期間中の AWS 課金実費の上限）。

### 方針
- **「体系化＋手を動かす」を軸**に、`公式ガイド → 公式コンテンツ＋Claude Code でハンズオン → 問題演習 → 弱点復習` のサイクル。
- **Udemy ハンズオン講座は採用しない**（理由：実務経験がある SE には冗長／1日1時間では動画消化に時間を食われる／Claude Code で必要な箇所だけピンポイント実機にする方が効率的）。
- 実機は **AWS 無料プラン（$200 クレジット／6か月）** を使用。費用が発生しても ¥2,000 を超えないよう **Budgets で ¥1,500 の予算アラート**を設定。
- 学習物（IaC・ノート・誤答ログ）は **GitHub 1リポジトリで一元管理**し、Claude Code を主たる作業環境にする。
- Skill Builder は **無料コンテンツ（Exam Readiness／公式 Practice Question Set）のみ**利用（有償サブスクは契約しない）。
- 弱点になりやすい **CloudFormation／コンテナ／Backup／Organizations／Systems Manager** に時間を寄せる。

## 3. 出題比率と学習時間配分

| 分野 | 出題比率 | 配分の目安 |
|---|---|---|
| Monitoring, Logging, Analysis, Remediation, Performance | 22% | 12h |
| Reliability and Business Continuity | 22% | 12h |
| Deployment, Provisioning, and Automation | 22% | 12h |
| Networking and Content Delivery | 18% | 10h |
| Security and Compliance | 16% | 10h |
| **合計（学習部分）** | 100% | **約56h** |

> **監視・信頼性・自動化の3分野で 66%**。ここを最優先で固める。SE 経験で既に強い領域は流し、AWS固有のマッピング確認に絞る。

## 4. 使用する教材・講座

| 区分 | 教材・講座 | 役割 | 費用 |
|---|---|---|---|
| 公式ガイド | AWS CloudOps Engineer – Associate 試験ガイド（公式PDF） | 範囲・13タスク・比率把握 | ¥0 |
| 体系インプット | Skill Builder 無料コース（Exam Readiness／Foundational） | 公式の体系説明で穴埋め | ¥0 |
| 公式問題 | AWS 公式 Practice Question Set（Skill Builder 無料枠） | 公式の問われ方を体感 | ¥0 |
| **問題集（メイン）** | **Udemy「AWSトップ講師による CloudOpsエンジニア・アソシエイト模擬試験問題集（6回分375問）」** | 本番形式の演習・弱点把握 | 約¥1,500〜2,600（セール時） |
| 実機環境 | AWS 無料プラン（$200／6か月） | 自分のアカウントで IaC を作って動かす | ¥0〜¥2,000 想定 |
| 学習支援 | **Claude Code** | ハンズオン指南・IaC作成・エラー解決・進捗管理（§7参照） | 既存契約 |

**教材費合計：約 ¥1,500〜2,600（Udemy 1講座のみ）**

## 5. AWS 費用を ¥2,000 以内に抑えるための運用ルール

1. AWS 無料プラン（$200／6か月）のクレジット範囲内で運用する。クレジット消費でアカウントが自動閉鎖されるため、原則 ¥0 で完結する。
2. それでも保険として **AWS Budgets で月額 ¥1,500 のアラート**を設定する。
3. **作ったら必ず削除する**：CloudFormation で作成 → 検証後 `aws cloudformation delete-stack` で破棄。Claude Code に「今日作ったスタックの掃除」をルーチン依頼する。
4. 高コストな常時稼働サービス（NAT Gateway、ALB、RDS の長時間稼働、EKS コントロールプレーン）は**短時間検証→即削除**を徹底する。EKS は概念学習中心にし、深掘りは Skill Builder の無料動画で代替。
5. リージョンは東京（`ap-northeast-1`）に固定。意図しないマルチリージョン課金を防ぐ。

## 6. GitHub リポジトリ

### リポジトリ名 候補（5案）

| 案 | 名称 | コンセプト |
|---|---|---|
| ★1 | **`soa-c03-roadmap`** | 試験コードを軸に "ロードマップ" を含意。中身が学習計画＋IaC＋ノート構成と一致して分かりやすい |
| 2 | `aws-cloudops-prep` | 資格名を素直に表現。汎用的で安全 |
| 3 | `cloudops-cert-lab` | "Lab" を強調し、IaCで実機を触る性格を反映 |
| 4 | `soa-c03-8weeks` | 8週間スプリントである時間制約を名前に込めた |
| 5 | `aws-cloudops-bootcamp` | 集中学習のニュアンスを強調 |

> 推奨は **`soa-c03-roadmap`**（試験コード固有・検索性良好・後から第三者が見ても意図が伝わる）。

### ディレクトリ構成

```
soa-c03-roadmap/
├── README.md                 # 学習計画サマリ・進捗ダッシュボード
├── CLAUDE.md                 # Claude Code 用のコンテキスト（後述）
├── plan/
│   └── SOA-C03_学習計画.md   # 本ドキュメント
├── notes/                    # サービス別・分野別ノート
│   ├── monitoring/
│   ├── reliability/
│   ├── deployment/
│   ├── networking/
│   └── security/
├── iac/                      # 実機検証用 IaC
│   ├── cloudformation/       # 試験で最重要
│   ├── cdk/                  # 余裕があれば
│   └── README.md             # デプロイ＆クリーンアップ手順
├── scripts/                  # AWS CLI ヘルパー（バッチクリーンアップ等）
├── mistakes.md               # 誤答ログ（分野・タグ付きで蓄積）
└── progress.md               # 週次の進捗・模試スコア記録
```

### `CLAUDE.md`（リポジトリのコンテキスト）に書くこと
- 学習者の前提（SE・AWS経験あり・体系化目的）
- 試験範囲と比率、進行中の週、現在の弱点
- ルール：「IaC を作ったらクリーンアップ手順もセットで提示」「リージョンは ap-northeast-1 固定」「Secrets はコミットしない」「最小権限で書く」など
- ノートの書式テンプレ（要点 → よくある誤答 → 公式ドキュメントへのリンク）

## 7. 8週間スケジュール（1日1時間／合計56h）

| 週 | テーマ | 内容（1日1時間×7日） | 主な活動 |
|---|---|---|---|
| **Week 0（準備, 1〜2日）** | 環境構築 | 公式試験ガイド精読／AWSアカウント作成＋Budgets設定／GitHubリポジトリ作成＋`CLAUDE.md`整備／公式 Practice Question Set 1回 | 学習レール敷設 |
| **Week 1** | 監視・運用①（22%の前半） | CloudWatch（メトリクス／アラーム／ロググループ）／SNS／EventBridge を Skill Builder 無料＋公式Docで体系化 | IaC：CloudWatch Alarm をテンプレ化してデプロイ |
| **Week 2** | 自動化・IaC（22%・最重要弱点） | **CloudFormation** を集中学習（Stack／Change Set／Drift Detection）／Systems Manager（Run Command／Automation／Patch／Parameter Store） | IaC：SSMドキュメント＋CFnの組み合わせを実機 |
| **Week 3** | 信頼性・DR（22%） | Auto Scaling／ELB／RDS（Multi-AZ／Read Replica）／AWS Backup／Route53（ヘルスチェック／ルーティング） | IaC：ASG＋ALB＋ヘルスチェックを構築 |
| **Week 4** | ネットワーク（18%） | VPC（SG／NACL／Flow Logs／VPC Endpoint）／Direct Connect／Transit Gateway／CloudFront | IaC：VPC＋エンドポイント構成を CFn 化 |
| **Week 5** | セキュリティ＋コンテナ（16%＋新範囲） | IAM／Organizations／SCP／KMS／Secrets Manager／GuardDuty／**ECS／EKS／Fargate（概念中心）** | IaC：ECS on Fargate の最小構成を CFn で（EKS は概念のみ） |
| **Week 6** | 演習① | Udemy 375問を**分野別に高速周回**（1日約50問）／誤答を `mistakes.md` に蓄積／弱点トピックのみ実機 or Claude Code で再確認 | アウトプット主軸 |
| **Week 7** | 演習②＋仕上げ | 通し模試（時間計測）／公式 Practice Question Set 再挑戦／`mistakes.md` 総ざらい／受験予約 | 仕上げ |
| **Week 8 前半** | 最終調整 | 残課題ピンポイント復習／模試で 80〜85% 安定を確認 | 受験直前 |
| **Week 8 後半** | **受験** | 本番 | — |

### 受験予約ラインの目安
| 周回 | 目標正答率 |
|---|---|
| 1回目 | 70% |
| 2回目 | 75% |
| 3回目 | 80% |
| 4回目 | **85%（→ 受験予約）** |

> 合格ラインは 720/1000（約72%）。本番難易度を踏まえ模試 80〜85% を安全圏とする。

## 8. Claude Code 活用法（Udemyハンズオン講座の代替として機能させる）

Udemy ハンズオン講座を採用しない代わりに、**Claude Code を「対話型のハンズオン講師」として使う**のが本計画の肝。リポジトリをコンテキストにすることで継続的な学習パートナー化できる。

### (1) ハンズオン指南（Udemy ハンズオン講座の代替）
```
「今週は CloudFormation。Stack / Change Set / Drift Detection を試験で問われる観点で
 順番に手を動かして学ぶ手順を出して。手順 → 検証コマンド → 期待される結果 → クリーンアップ の流れで。
 各手順の AWS CLI コマンドと、なぜそれをやるかの意図も併記して」
```

### (2) IaC 作成補助（弱点 CloudFormation を実機で固める）
```
「VPC＋ALB＋ASG＋CloudWatch Alarm を作る CloudFormation テンプレを iac/cloudformation/wk3-asg.yaml に書いて。
 cfn-lint も通して。同じ構成を Terraform で書いたらどう違うかも notes/reliability/asg.md に併記して」
```
Hiroaki さんが普段使う Terraform/CDK との **対比解説**を必ず求めると、体系化が一気に進む。

### (3) 体系化ノートの自動生成
```
「CloudWatch のメトリクスフィルタ／サブスクリプションフィルタ／Logs Insights の違いを
 試験で問われる観点で notes/monitoring/cloudwatch-logs.md にまとめて。
 要点 → よくある誤答 → 公式Docへのリンク の順で」
```

### (4) エラーデバッグ
```
「この CloudFormation デプロイのエラーログを読んで、原因と修正案を最小権限の観点で。
 修正後のテンプレを差分で示して」
```

### (5) コスト見守り＆クリーンアップ
```
「いま自分の AWS アカウントに残っている学習用リソースを CLI で一覧して、
 残しておくべきもの／消すべきもの を分類して。消すコマンド列も出して」
```
**毎日の最後に必ず実行する習慣**にすると ¥2,000 ガードが効く。

### (6) 進捗・弱点管理
```
「mistakes.md の誤答を分野別に集計して、明日の1時間で何をやるべきか優先順位付きで出して」
「残り日数と未着手分野から、今週の学習割り当てを再計算して」
```

### 注意事項
- 認証情報は `.gitignore` で確実に除外（`.aws/`, `*.pem`, `.env` 等）
- AWS Budgets で予算アラート必須
- 破壊的コマンド（`delete-stack`／`terminate-instances` 等）は実行前に内容確認

## 9. 費用合計（再掲）

| 項目 | 金額（目安） |
|---|---|
| Udemy 375問模試 | 約 ¥1,500〜2,600（セール時） |
| AWS 無料プラン | ¥0（保険として上限 ¥2,000） |
| Skill Builder 無料枠 | ¥0 |
| GitHub | ¥0 |
| **学習費用 合計** | **約 ¥1,500〜4,600** |
| 受験料（参考） | 約 $150 USD（約 ¥23,000） |

## 10. 試験概要（参考）

- 65問／130分／1000点満点中 720点で合格（約72%）。ラボ（実技）は廃止。
- テストセンター または オンライン受験。有効期限3年。受験料 約 $150 USD。
