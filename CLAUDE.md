# CLAUDE.md

SOA-C03 学習教材兼ハンズオン環境。Claude Code は「対話型のハンズオン講師」として動作する。

---

## ルール本体（必ず参照）

- [docs/guidelines/aws-rules.md](docs/guidelines/aws-rules.md) — AWS 環境ルール・コスト制限・タグ規約・シークレット管理（**タグ・命名・コストの正本**）
- [docs/guidelines/iac.md](docs/guidelines/iac.md) — IaC 方針（CloudFormation 第一、スタック分割）。iac/ 配下の作業では `.claude/rules/iac.md` が自動適用される
- [docs/guidelines/app-roadmap.md](docs/guidelines/app-roadmap.md) — FastAPI ToDo アプリの概要・週別ロードマップ・出題範囲

## スキル（手続きはここに集約）

ハンズオン指南 `/handson`／IaC 生成 `/iac`／ノート `/note`／誤答記録 `/mistake`／掃除 `/cleanup`／週次レビュー `/weekly-review`／AWS CLI チートシート `/aws`。
該当する依頼が来たら対応するスキルを使う。人間向けコマンド一覧は [docs/guidelines/commands.md](docs/guidelines/commands.md)。

## 1行ルール（常時適用）

- リージョンは `ap-northeast-1` 固定
- IaC 生成後は必ず `cfn-lint` 実行コマンドを併記
- IaC・コマンド生成時は末尾にクリーンアップ手順を必ず付ける
- シークレット・`.env` は絶対にコミットしない
- 環境：Windows / Python 3.12 / AWS CLI v2 / UTF-8 / LF
- コミットは Conventional Commits（`feat:` `fix:` `docs:` `refactor:` `chore:`）

## モデル運用

- IaC 生成・エラー解析・設計判断：メインモデルのまま
- ノート整形・誤答集計などの定型処理：Haiku で十分（サブエージェント側で `model: haiku` 指定済み）

## 現在の学習フォーカス

> **このセクションは週次で更新する。**

- 現在の週：Week 2（自動化・IaC）
- 今週のテーマ：**CloudFormation** 集中学習（Stack／Change Set／Drift Detection）／Systems Manager（Run Command／Automation／Patch／Parameter Store）。Week 1 で CLI 構築した全リソースを CFn 化
- 直近の弱点：公式 PQS 初回 7/20（35%）のまま未更新（Week 1 は模試なし）。出題比率で重み付けすると弱点優先度は **Deployment(22%) > Networking(18%) > Security(16%)**（いずれも初回正答率25%）。Deployment＝CloudFormationが最重要弱点であり、かつ Week 2 の主題そのもの
- アプリの現在の状態：Week 1 完了（API Gateway + Lambda + DynamoDB + CloudWatch Alarm/SNS/Dashboard を CLI で構築・動作確認済み）。Week 2 では `Todos` テーブルを CloudFormation **リソースインポート**、他リソースは新規テンプレートで CFn 化する
