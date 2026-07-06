---
name: iac
description: CloudFormation テンプレートの生成・修正・デプロイ手順の提示を行う。「CFn を書いて」「テンプレート作成」「IaC 化」「スタックをデプロイ」と言われたら使用。
---

# IaC 生成（CloudFormation 第一）

テンプレート規約・スタック分割・タグ規約は `.claude/rules/iac.md`（iac/ 配下の作業で自動適用）と [docs/guidelines/iac.md](../../../docs/guidelines/iac.md) に従う。

## 出力手順（必ずこの順）

1. **テンプレート生成**：`iac/cloudformation/wk{N}-todo-{purpose}.yaml` に配置。既存スタックの Outputs（Export/ImportValue）と整合させる
2. **cfn-lint 実行**：保存すると hook が自動実行するが、コマンドも併記する
   ```
   cfn-lint iac/cloudformation/<file>.yaml
   ```
3. **デプロイコマンド**：タグ規約（Project / App / Week / Owner）を必ず付与
   ```
   aws cloudformation deploy --stack-name wk{N}-{purpose} --template-file <file> --capabilities CAPABILITY_NAMED_IAM --region ap-northeast-1 --tags Project=soa-c03-workbook App=fastapi-todo Week={N} Owner=<your-handle>
   ```
4. **Outputs 確認コマンド**
5. **クリーンアップ手順（必須）**：`delete-stack` ＋ `wait stack-delete-complete` ＋ タグ検索での残存確認

## 補足

- Terraform / CDK との対比解説を求められたら notes/ 側に併記する（iac/ には置かない）
- エラー解析を頼まれたら：原因仮説を3つまで → 切り分け手順を順番に → 修正は最小権限・最小差分で
