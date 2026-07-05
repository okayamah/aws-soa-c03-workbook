---
paths:
  - "iac/**"
---

# IaC 規約（iac/ 配下の作業時に適用）

- 第一選択は CloudFormation（YAML）。`iac/cloudformation/` に配置。CDK は補助
- すべてのテンプレに `Description` を入れる。`Parameters` には型と説明、`Outputs` には主要 ARN/ID を出す
- IAM Role/Policy は最小権限。`*` を使う場合は理由をコメントする
- スタック名は `wk{N}-{purpose}` 形式。分割は network / data / app / monitoring / security とし、依存は `Export`/`ImportValue` で繋ぐ
- タグ規約（必須・全リソース）：`Project=soa-c03-workbook` `App=fastapi-todo` `Week=<N>` `Owner=<user>`
- 生成・修正したら cfn-lint を必ず通す（保存時 hook でも自動実行される）
- デプロイ手順を出すときは末尾にクリーンアップ手順（delete-stack + 残存確認）を必ず付ける
