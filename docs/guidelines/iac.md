# IaC 方針

## 基本方針

- **第一選択は CloudFormation（YAML）**（試験最重要）。`iac/cloudformation/` に配置。
- 生成時は必ず `cfn-lint` をパスする想定で書く。生成後に「`cfn-lint` の実行コマンド」を併記すること。
- 同じ構成を Terraform / CDK で書いたらどう違うかの **対比解説**を `notes/` 側に併記すると体系化が進む（利用者の希望に応じて）。

## テンプレート規約

- すべてのテンプレに `Description` を入れる。
- `Parameters` には型と説明を付ける。
- `Outputs` には主要 ARN/ID を出す。
- IAM Role/Policy は **最小権限**で書く。`*` を使う場合は理由を必ずコメントする。

## スタック分割

アプリのリソースは複数スタックに分割し、依存は `Export`/`ImportValue` で繋ぐ：

- `wk{N}-todo-network`（VPC 系）
- `wk{N}-todo-data`（DynamoDB 等）
- `wk{N}-todo-app`（Lambda/Fargate 等）
- `wk{N}-todo-monitoring`（CloudWatch 系）
