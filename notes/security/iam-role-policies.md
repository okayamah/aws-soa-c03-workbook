# IAM ロールとポリシーの構造（Week 1 Day 2）

> Lambda 実行ロール `wk1-todo-lambda-role` を CLI で組み立てた回の整理。ロール＝「制服」のたとえで体系化。

## 要点（試験で問われる観点）

### ロール = 信頼ポリシー + アクセス許可ポリシー
```
ロール（制服）
├─ 信頼ポリシー（Trust Policy）        … 誰がこの制服を着てよいか
└─ アクセス許可ポリシー（Permissions） … 着た人は何ができるか
```
- **信頼ポリシー**：`create-role --assume-role-policy-document` で指定。`Principal` に引き受け主体（`lambda.amazonaws.com` / `ec2.amazonaws.com` / `ecs-tasks.amazonaws.com` 等）、`Action` は `sts:AssumeRole`。
- ロールを引き受けると **STS の一時認証情報**が発行される → コードにアクセスキーを書かない仕組みの根幹。
- 作成直後のロールは**何の権限も持たない**（着られるだけの空の制服）。

### 管理ポリシー vs インラインポリシー
| | 管理ポリシー | インラインポリシー |
|---|---|---|
| コマンド | `attach-role-policy` | `put-role-policy` |
| 実体 | 独立オブジェクト。**複数プリンシパルに再利用可** | ロールに**埋め込み**（1対1） |
| 変更 | 1か所直せば全アタッチ先に反映 | ロールごとに個別修正 |
| 削除時 | ロールを消してもポリシーは残る | ロールと**運命共同体** |
| 向き | 汎用権限・組織標準（例：ログ書き込み） | そのロール固有の**最小権限** |
- AWS 管理ポリシーの ARN は `arn:aws:iam::aws:policy/...`（アカウント部が `aws`）。
- `AWSLambdaBasicExecutionRole` は名前に反して**ポリシー**（logs:CreateLogGroup / CreateLogStream / PutLogEvents のみ）。

### 最小権限の実践（今回の構成）
- 汎用のログ権限 → AWS 管理ポリシーを**アタッチ**（再利用）。
- `Todos` テーブル限定の CRUD（GetItem/PutItem/DeleteItem/Scan、Resource=テーブル ARN）→ **インライン**で密結合。
- `AmazonDynamoDBFullAccess` は全テーブル全操作なので不採用（Week 5 の IAM 最小権限化への布石）。

### ロール削除の順序（付いたままでは消せない）
```
delete-role-policy（インライン削除）→ detach-role-policy（管理を外す）→ delete-role
```

### 運用上の注意
- IAM 変更には**伝播ラグ**あり。ロール作成直後の `lambda create-function` は `cannot be assumed` で失敗することがある → 数秒〜十数秒待って再実行。

## よくある誤答パターン
- 信頼ポリシーとアクセス許可ポリシーの混同。「サービスがロールを引き受けられない」→ **信頼ポリシーの Principal** を疑う（権限ポリシー側ではない）。
- 「Lambda が DynamoDB にアクセスできない」→ ①信頼ポリシーの Principal 誤り ②権限ポリシー不足 ③リソース ARN の絞りすぎ、の切り分け。
- `AWSLambdaBasicExecutionRole` をロールだと思う → **AWS 管理ポリシー**。
- ポリシーが付いたままロール削除 → `DeleteConflict`。先にインライン削除＋管理デタッチ。
- ロールの代わりに**アクセスキーをコード/環境変数に直書き** → ロール＋一時認証情報が正答。

## 実機で確認すべきこと（FastAPI ToDo への適用）
- **Week 1 Day 2 実施**：`wk1-todo-lambda-role` を CLI で作成（trust: lambda.amazonaws.com ／ attach: AWSLambdaBasicExecutionRole ／ inline: todos-table-crud）。ポリシー JSON は `scripts/wk1/` に保存。
- インラインの Resource は `arn:aws:dynamodb:ap-northeast-1:*:table/Todos`（学習用にアカウント部 `*`。本番はアカウント ID 固定が正道）。
- **Week 2**：この構成を CFn（`AWS::IAM::Role` + `Policies`）へ写経して対比する。
- **Week 3**：ECS タスクロール（Principal が `ecs-tasks.amazonaws.com` に変わるだけで構造は同じ）で再確認。
- **Week 5**：IAM 最小権限化の総仕上げで見直し対象。

## 関連サービスとの違い
- **ロール vs ユーザー**：一時認証情報を都度発行 vs 永続認証情報。サービスやクロスアカウントには**ロール**。
- **IAM ポリシー vs リソースベースポリシー**：プリンシパル側に付与 vs リソース側（S3 バケットポリシー、Lambda リソースポリシー等）に付与。
- **実行ロール vs Lambda リソースポリシー**：Lambda が「何をできるか」 vs 「誰が Lambda を呼べるか」（Day 3 の API Gateway 連携で登場）。

## 公式ドキュメント
- IAM ロールの用語と概念: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html
- 管理ポリシーとインラインポリシー: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html
- Lambda 実行ロール: https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html
- ポリシーとアクセス許可: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html
- IAM のベストプラクティス: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
