# コマンドリファレンス

> 詳細・前提は各 README（`app/`・`iac/`・`scripts/`）参照。

## アプリ（ローカル開発）

```powershell
cd app
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt   # Week 1 で作成
uvicorn main:app --reload         # http://127.0.0.1:8000/docs
```

## IaC（CloudFormation）

```powershell
# 検証 → Lint → デプロイ（タグ規約を必ず付与）
aws cloudformation validate-template --template-body file://iac/cloudformation/wk1-todo-data.yaml
cfn-lint iac/cloudformation/wk1-todo-data.yaml
aws cloudformation deploy `
  --stack-name wk1-todo-data `
  --template-file iac/cloudformation/wk1-todo-data.yaml `
  --capabilities CAPABILITY_NAMED_IAM `
  --region ap-northeast-1 `
  --tags Project=soa-c03-workbook App=fastapi-todo Week=1 Owner=<your-handle>
```

## クリーンアップ（毎日必須）

```powershell
aws cloudformation delete-stack --stack-name <stack> --region ap-northeast-1
aws cloudformation wait stack-delete-complete --stack-name <stack> --region ap-northeast-1
# タグで残存リソース確認
aws resourcegroupstaggingapi get-resources `
  --tag-filters Key=Project,Values=soa-c03-workbook --region ap-northeast-1
```
