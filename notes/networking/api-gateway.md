# API Gateway（Week 1 Day 3）

> Lambda `wk1-todo-api` の前段に HTTP API を構築し、ToDo API を公開した回の整理。これで Week 1 の最小構成（API Gateway + Lambda + DynamoDB）が完成。

## 要点（試験で問われる観点）

### HTTP API vs REST API（最頻出比較）
| | HTTP API | REST API |
|---|---|---|
| レイテンシ・コスト | 低レイテンシ・**安い**（〜60-70%削減） | 機能豊富だが高コスト |
| デプロイ | `--auto-deploy` で**手動デプロイ不要**にできる | **明示的な `create-deployment` が必須**（ルート変更しても再デプロイ忘れると反映されない） |
| 認可 | JWT オーソライザー / Lambda オーソライザー | IAM / Cognito / Lambda オーソライザー |
| WAF 連携 | **不可** | **可**（REST API の強み） |
| マッピングテンプレート（リクエスト/レスポンス変換） | **不可** | 可 |
| キャッシュ | 不可 | 可 |
| CORS | **組み込みで簡単設定** | 手動設定が必要 |
- 「単純な Lambda プロキシ・コスト重視」→ **HTTP API**、「WAF で保護／レスポンス変換が要る」→ **REST API**、という誘導が定番。

### API 定義とステージ（Stage）の分離
- API 定義（Integration・Route）＝設計図。**ステージを作って初めて公開URLが実在**する。
- `$default` ステージ：**名前が URL に含まれない**特殊ステージ（`.../dev/health` ではなく `.../health`）。
- REST API はルート変更のたびに再デプロイが必要。HTTP API は `--auto-deploy` で自動反映可能（REST API には無い機能）。

### プロキシ統合（AWS_PROXY）
- API Gateway 側でパスごとの変換ロジックを持たず、リクエスト全体を Lambda に丸ごと渡す方式。
- ルーティングの実体はアプリ側（今回は FastAPI/Mangum）に一元化。ルート定義は `ANY /{proxy+}`（1セグメント以上のワイルドカード）で足りる。
- `payload-format-version 2.0` を指定（Lambda 側のイベント形式に対応。Day 2 のテストイベント JSON がこの形式だった）。

### Lambda リソースベースポリシー（実行ロールとは別物）
- `create-integration` / `create-route` だけでは **API Gateway が Lambda を呼ぶ権限は自動で付かない**。
- `aws lambda add-permission --principal apigateway.amazonaws.com --source-arn arn:aws:execute-api:...` が必須。
- 忘れると呼び出し時に **403 Forbidden**。
- [notes/security/iam-role-policies.md](../security/iam-role-policies.md) の実行ロール（Lambda→他サービス）と**向きが逆**：これは「誰が Lambda を呼べるか」を Lambda 側リソースに設定するポリシー。

### スロットリングとカスタムドメイン
- アカウント/リージョンのデフォルトスロットリング：**10,000 rps（バースト 5,000）**。超過は `429 Too Many Requests`。ステージ/ルート単位で個別設定可能。
- 本番公開は自動生成 URL ではなく **カスタムドメイン名（Route 53 + ACM 証明書）**が定石（Week 4 の CloudFront 前段構成に接続）。
- アクセスログはデフォルト無効。「誰がいつ何を呼んだか」の可視化には明示的な設定が必要。

## よくある誤答パターン
- REST API で**ルートを変更したのに反映されない** → **再デプロイ忘れ**（`create-deployment` していない）。
- **WAF を HTTP API に付けようとする** → 不可。WAF が要件に出たら REST API（または CloudFront）に誘導。
- Integration・Route を作っただけで **呼び出せると思い込む** → ステージが無いと公開URLが存在しない。
- `add-permission` を忘れて **403 は実行ロール不足だと誤診断** → これはリソースベースポリシー側の問題。
- **キャッシュ・マッピングテンプレートが必要な要件で HTTP API を選ぶ** → REST API 限定機能。

## 実機で確認すべきこと（FastAPI ToDo への適用）
- **Week 1 Day 3 実施**：`wk1-todo-http-api`（HTTP API・`$default` ステージ・auto-deploy）を Lambda `wk1-todo-api` に `AWS_PROXY` 統合。ルートは `ANY /{proxy+}`。
- `/health`・`POST /todos`・`GET /todos`・`GET /todos/{id}`（404確認）を実 URL で検証。これで Week 1 最小構成（API GW + Lambda + DynamoDB）が完成。
- **PowerShell の落とし穴**：`curl` は `Invoke-WebRequest` のエイリアスで `-X`/`-H`/`-d` を解釈できない。`curl.exe` を明示するか `Invoke-RestMethod -Method Post -ContentType "application/json" -Body '{...}'` を使う（`-Body` はエスケープ不要）。404確認は例外を投げるため `try/catch` が必要。
- **Day 4 以降**：このエンドポイントのメトリクス・アラーム・Dashboard 化（Week 1 本題の監視）。
- **Week 2**：この HTTP API・Integration・Route・Lambda 権限一式を CFn 化（`AWS::ApiGatewayV2::*` リソース）。
- **Week 4**：カスタムドメイン・CloudFront 前段追加時にこの構成へ被せる。

## 関連サービスとの違い
- **HTTP API vs REST API**：上表参照。
- **実行ロール vs Lambda リソースベースポリシー**：「Lambda が何をできるか」 vs 「誰が Lambda を呼べるか」。
- **API Gateway vs ALB**：Lambda 統合ならサーバーレスで API Gateway が主流、EC2/ECS 常駐サービスの負荷分散は ALB（Week 3 で対比）。
- **WebSocket API**（今回未使用）：双方向通信が必要な場合の別プロトコルタイプ。

## 公式ドキュメント
- HTTP API 概要: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html
- HTTP API vs REST API 機能比較: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html
- Lambda プロキシ統合: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
- ステージとデプロイ: https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-how-to-deploy-api-with-console.html
- Lambda リソースベースポリシー（add-permission）: https://docs.aws.amazon.com/lambda/latest/dg/access-control-resource-based.html
- API Gateway のスロットリング: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html
- HTTP API の CORS: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html
