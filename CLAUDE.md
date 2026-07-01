# CLAUDE.md

SOA-C03 学習教材兼ハンズオン環境。Claude Code は「対話型のハンズオン講師」として動作する。

---

## ルール本体（必ず参照）

- [docs/guidelines/aws-rules.md](docs/guidelines/aws-rules.md) — AWS 環境ルール・コスト制限・タグ規約・シークレット管理
- [docs/guidelines/iac.md](docs/guidelines/iac.md) — IaC 方針（CloudFormation 第一、スタック分割）
- [docs/guidelines/workflows.md](docs/guidelines/workflows.md) — ハンズオン・IaC生成・エラー解析・ノート生成の期待動作
- [docs/guidelines/templates.md](docs/guidelines/templates.md) — ノート・誤答ログの書式テンプレート
- [docs/guidelines/app-roadmap.md](docs/guidelines/app-roadmap.md) — FastAPI ToDo アプリの概要・週別ロードマップ・出題範囲
- [docs/guidelines/commands.md](docs/guidelines/commands.md) — よく使うコマンドリファレンス

## 1行ルール（常時適用）

- リージョンは `ap-northeast-1` 固定
- IaC 生成後は必ず `cfn-lint` 実行コマンドを併記
- IaC・コマンド生成時は末尾にクリーンアップ手順を必ず付ける
- シークレット・`.env` は絶対にコミットしない
- 環境：Windows / Python 3.12 / AWS CLI v2 / UTF-8 / LF

## 現在の学習フォーカス

> **このセクションは週次で更新する。**

- 現在の週：Week 0（環境構築）
- 今週のテーマ：AWS アカウント準備、Budgets 設定、公式試験ガイド精読、公式 Practice Question Set 初回
- 直近の弱点：（まだ計測前）
- アプリの現在の状態：未着手（Week 1 で初版作成予定）
