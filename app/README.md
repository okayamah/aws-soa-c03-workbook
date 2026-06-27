# app/ – FastAPI ToDo Workbook

SOA-C03 学習用に AWS 上で運用する **FastAPI 製の ToDo Web アプリ**。
学習の進行に合わせて毎週リファクタリングして育てる「成果物」を兼ねる。

## 機能（最終形）

- ToDo の CRUD（POST / GET / GET by id / PUT / DELETE）
- ヘルスチェック（`/healthz`）
- 構造化ログ（JSON）
- AWS X-Ray トレース（Week 5）
- 設定値は AWS Systems Manager Parameter Store から取得（Week 2 以降）
- 秘匿値は AWS Secrets Manager（Week 5 以降）

## 技術スタック

- Python 3.12
- FastAPI
- Mangum（Week 1〜2：Lambda 実行用アダプタ）
- boto3（DynamoDB 操作）
- pydantic v2（モデル定義）
- uvicorn（ローカル開発）

## ローカル実行

```powershell
cd app
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
# http://127.0.0.1:8000/docs で Swagger UI
```

## 週ごとの実装ロードマップ

| 週 | 実装するもの | 実行基盤 |
|---|---|---|
| Week 1 | CRUD（メモリ or DynamoDB 直叩き）／ヘルスチェック／ログ | Lambda + API Gateway |
| Week 2 | 設定を SSM Parameter Store 化／環境別パラメータ | Lambda + API Gateway |
| Week 3 | Dockerfile 化／ECS Fargate に移行 | ECS Fargate + ALB |
| Week 4 | （変更なし）／前段に CloudFront | 同上 |
| Week 5 | KMS 暗号化／Secrets Manager 連携／X-Ray 計装 | 同上 |

## 注意

- 認証は実装しない（学習対象が AWS 運用のため）。本番運用を意図しない。
- `.env` は Git 管理しない（`.gitignore` で除外済み）。
- アプリそのものの実装は Week 1 で Claude Code に生成させる。
