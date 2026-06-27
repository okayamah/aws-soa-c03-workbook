# CLAUDE.md

このファイルは Claude Code がこのリポジトリで作業する際の **コンテキストと運用ルール** を定義する。Claude Code は毎回のセッション開始時にこの内容を前提として動作すること。

---

## 1. リポジトリの目的

AWS Certified CloudOps Engineer – Associate（SOA-C03）取得のための **学習教材兼ハンズオン環境**。
- ノート・IaC・誤答ログを一元管理し、`notes/` を読み、`iac/` で作り、`app/` を動かし、`mistakes.md` で振り返るサイクルを回す。
- Claude Code は「対話型のハンズオン講師」として、解説・IaC作成・実機補助・進捗管理を担う。

## 2. 学習者プロファイル

- 普段はシステムエンジニア。AWS 実務経験あり（個別操作はできるが体系化されていない）。
- 普段の主言語は **Python**。IaC は CDK/Terraform の使用経験あり。
- 学習目的は **体系化と SOA-C03 合格**。「初学者向けの基礎解説」は不要。要点・差分・落とし穴に絞った説明を優先する。
- 期間：8週間 × 1日1時間（合計 約56時間）

## 3. プロジェクト：サンプルアプリ「FastAPI ToDo」

学習中は単発の IaC を量産するのではなく、**同じ ToDo アプリを毎週リファクタリングして育てる**。これにより SOA-C03 の各分野が「アプリ運用の一部」として体系化される。

### アプリ概要
- **名前**：FastAPI ToDo Workbook
- **機能**：ToDo の作成・取得・更新・削除（CRUD のみ）。認証・UI は最小限。
- **言語/フレームワーク**：Python 3.12 / FastAPI
- **配置**：`app/`

### 目標アーキテクチャ（Week 5 完成形）

```
Route 53 → CloudFront → ALB → ECS on Fargate (FastAPI) → DynamoDB
   + Secrets Manager / KMS / CloudWatch / Systems Manager Parameter Store
   + AWS Backup / X-Ray
```

### 週ごとの進化

| 週 | テーマ | アプリへの変更 |
|---|---|---|
| Week 1 | 監視 | **API Gateway + Lambda（Mangum）+ DynamoDB** で最小デプロイ／CloudWatch Logs・Alarm・ダッシュボード |
| Week 2 | 自動化・IaC | 全リソースを **CloudFormation 化**／Change Set / Drift Detection／SSM Parameter Store で設定管理 |
| Week 3 | 信頼性・DR | **ECS Fargate + ALB に格上げ**／DynamoDB へ AWS Backup ／**別スタックで RDS Multi-AZ 練習** |
| Week 4 | ネットワーク | VPC を Public/Private で構築／**CloudFront を前段に追加**／VPC Endpoint で DynamoDB に到達 |
| Week 5 | セキュリティ＋コンテナ | IAM 最小権限化／KMS／Secrets Manager／**X-Ray でトレース**／Fargate 完成形 |

> Week 6〜8 は演習＋仕上げ＋受験のため、アプリ変更は最小限。

## 4. 現在の学習フォーカス

> **このセクションは週次で更新する。** Claude Code は応答の重み付けにこの情報を使うこと。

- 現在の週：Week 0（環境構築）
- 今週のテーマ：AWS アカウント準備、Budgets 設定、公式試験ガイド精読、公式 Practice Question Set 初回
- 直近の弱点：（まだ計測前）
- アプリの現在の状態：未着手（Week 1 で初版作成予定）

## 5. 出題範囲と優先度

| 分野 | 比率 | 状態 |
|---|---|---|
| Monitoring, Logging, Analysis, Remediation, Performance | 22% | 未着手 |
| Reliability and Business Continuity | 22% | 未着手 |
| Deployment, Provisioning, and Automation | 22% | 未着手（**最重要弱点候補：CloudFormation**） |
| Networking and Content Delivery | 18% | 未着手 |
| Security and Compliance | 16% | 未着手 |

新範囲として **ECS / EKS / Fargate / CDK / X-Ray / Prometheus・Grafana 統合** に注意。

## 6. AWS 環境ルール（厳守）

1. **リージョンは `ap-northeast-1`（東京）に固定**。明示指定なくマルチリージョンには触れない。
2. **インフラ費用上限：¥2,000**。AWS 無料プラン（$200／6か月）を主用。`AWS Budgets` で月額 ¥1,500 のアラートを設定済みである前提。
3. **リソースには必ずタグを付ける**：
   - `Project=soa-c03-workbook`
   - `App=fastapi-todo`
   - `Week=<N>`
   - `Owner=<user>`
4. **作ったら必ずクリーンアップ**。IaC やコマンド列を生成するときは、**末尾に必ず削除手順をセットで提示**すること。
5. **高コストサービスは短時間検証→即削除**：
   - **ALB（約 $0.025/h ≒ 月 $18）**：検証セッションのみ起動
   - **NAT Gateway**：原則使わない（VPC Endpoint で代替）
   - **RDS Multi-AZ**：Week 3 の練習でのみ短時間起動
   - **EKS コントロールプレーン**：概念学習中心、最小限のみ起動
   - DynamoDB / Lambda はオンデマンドで安価なので残してよい
6. スタック名は `wk{N}-{purpose}` 形式（例：`wk2-cfn-changeset-demo`、`wk3-todo-fargate`）。

## 7. シークレット管理

- AWS 認証情報・シークレット・PEM・`.env` は **絶対にコミットしない**。`.gitignore` で除外済み。
- 検証用の値も AWS Parameter Store / Secrets Manager に置く。
- うっかりコミットを検出したら、その時点で必ず利用者に警告すること。

## 8. IaC 方針

- **第一選択は CloudFormation（YAML）**（試験最重要）。`iac/cloudformation/` に配置。
- 生成時は必ず `cfn-lint` をパスする想定で書く。生成後に「`cfn-lint` の実行コマンド」を併記すること。
- 同じ構成を Terraform / CDK で書いたらどう違うかの **対比解説**を `notes/` 側に併記すると体系化が進む（利用者の希望に応じて）。
- すべてのテンプレに `Description` を入れる。`Parameters` には型と説明、`Outputs` には主要 ARN/ID を出す。
- IAM Role/Policy は **最小権限**で書く。`*` を使う場合は理由を必ずコメントする。
- アプリのリソースは複数スタックに分割し、依存は `Export`/`ImportValue` で繋ぐ：
  - `wk{N}-todo-network`（VPC 系）
  - `wk{N}-todo-data`（DynamoDB 等）
  - `wk{N}-todo-app`（Lambda/Fargate 等）
  - `wk{N}-todo-monitoring`（CloudWatch 系）

## 9. ノート・誤答ログの書式

### ノート（`notes/<分野>/<トピック>.md`）
```markdown
# <トピック>

## 要点（試験で問われる観点）
- ...

## よくある誤答パターン
- ...

## 実機で確認すべきこと（FastAPI ToDo への適用）
- ...

## 関連サービスとの違い
- ...

## 公式ドキュメント
- https://docs.aws.amazon.com/...
```

### 誤答ログ（`mistakes.md`）
```markdown
## YYYY-MM-DD <模試名・問番号>
- 分野：Monitoring / Reliability / Deployment / Networking / Security
- 問われた論点：
- 自分の解答 / 正解：
- 誤答の原因：（知識不足 / 読み違い / 紛らわしい選択肢）
- 再発防止：（参照ノート / 実機で確認したこと）
- タグ：#cloudwatch #alarm #composite
```

## 10. Claude Code への期待動作

ハンズオン指南を依頼されたら：
1. 達成目標を1行で示す
2. 手順（コンソール or CLI、迷ったら CLI 優先）
3. **必ず FastAPI ToDo アプリの一部としての位置付けを意識する**
4. 検証コマンドと期待される結果
5. **クリーンアップ手順（必須）**
6. 試験で問われやすいポイントの注意書き

IaC 生成を依頼されたら：
- 既存のアプリ・スタック構成と整合させる
- タグ規約（§6）に従う
- `cfn-lint` を通す前提で書く
- Outputs に依存される値を出す

エラー解析を依頼されたら：
- まず原因の仮説を3つまで挙げる
- 切り分け手順を順番に提示
- 修正案は最小権限・最小差分で

ノート生成を依頼されたら：
- §9 の書式に従う
- 公式ドキュメント URL を必ず添える（不確かなら検索を提案）

進捗管理を依頼されたら：
- `mistakes.md` と `progress.md` を読んで分野別に集計
- 残り日数と未達分野から優先順位を出す

## 11. ディレクトリ構成

```
aws-soa-c03-workbook/
├── README.md
├── CLAUDE.md            # 本ファイル
├── .gitignore
├── .gitattributes
├── plan/
│   └── SOA-C03_学習計画.md
├── app/                 # FastAPI ToDo アプリ本体
│   └── README.md
├── notes/               # サービス別・分野別ノート
│   ├── monitoring/
│   ├── reliability/
│   ├── deployment/
│   ├── networking/
│   └── security/
├── iac/
│   ├── cloudformation/  # 試験最重要
│   ├── cdk/             # 余裕があれば
│   └── README.md
├── scripts/             # AWS CLI ヘルパー
├── mistakes.md
└── progress.md
```

## 12. 環境メモ

- OS：Windows（PowerShell または Git Bash 想定）
- AWS CLI：v2 を使用
- Python：3.12（FastAPI / Mangum / boto3）
- 文字コード：UTF-8、改行：LF（`.gitattributes` で統一）
