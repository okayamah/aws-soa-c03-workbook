---
name: handson
description: Week N のハンズオン演習・実機デプロイを指南する。「ハンズオン」「実機で試す」「今日の演習」「Week N を進めたい」「〜を立ち上げる手順」と言われたら使用。
---

# ハンズオン指南

CLAUDE.md の「現在の学習フォーカス」と [docs/guidelines/aws-rules.md](../../../docs/guidelines/aws-rules.md) を前提に、以下の構成で必ず出力する：

1. **達成目標を1行**で示す
2. **手順**（コンソール or CLI、迷ったら CLI 優先）
3. **FastAPI ToDo アプリの一部としての位置付け**を明示する（[docs/guidelines/app-roadmap.md](../../../docs/guidelines/app-roadmap.md) の週別ロードマップと整合させる）
4. **検証コマンドと期待される結果**
5. **クリーンアップ手順（必須）**。削除コマンド＋残存確認（/cleanup と同じ書式）
6. **試験で問われやすいポイント**の注意書き

## 注意

- リージョンは `ap-northeast-1` 固定。タグ規約・コスト上限は aws-rules.md に従う
- 高コストサービス（ALB / NAT GW / RDS / EKS）は「検証セッションのみ起動→即削除」を手順に織り込む
- 手順の終わりに、確認した内容を notes/ へ記録するなら /note を案内する
