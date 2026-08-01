# Lambda × CloudWatch Logs（Week 1 Day 2）

> FastAPI ToDo を Mangum 経由で Lambda にデプロイし、ログ観測までを実施した回の整理。

## 要点（試験で問われる観点）

### Lambda のログの仕組み
- Lambda の stdout / stderr（Python の `logging` 含む）は **CloudWatch Logs に自動転送**される。
- ロググループ名は **`/aws/lambda/<関数名>`** に固定。
- ロググループは**関数作成時ではなく初回実行時**に、**実行ロールの `logs:CreateLogGroup` 権限で遅延作成**される。
  - ログ書き込みは ①`CreateLogGroup` → ②`CreateLogStream` → ③`PutLogEvents` の 3 権限 ＝ **`AWSLambdaBasicExecutionRole`** の中身そのもの。
- 自動作成されたロググループの保持期間は**無期限（Never expire）**。コスト最適化 → `put-retention-policy` で保持日数を設定。
- **関数を削除してもロググループは残る**（料金も残る）→ クリーンアップでは `logs delete-log-group` を別途実行。
- 先に同名ロググループを明示作成しておけば Lambda はそれを使う（**CFn の定石**：`AWS::Logs::LogGroup` を関数とセットで定義し retention を統制。→ Week 2）。
- `REPORT` 行に **Duration / Billed Duration / Max Memory Used** が出る（性能・メモリチューニングの入口）。

### Lambda の標準メトリクス（アラーム対象）
| メトリクス | 用途 |
|---|---|
| `Invocations` | 呼び出し回数 |
| `Errors` | エラー率アラームの対象 |
| `Duration` | 遅延監視・タイムアウト予兆 |
| `Throttles` | 同時実行の枯渇検知 |
| `ConcurrentExecutions` | 同時実行数の監視 |

### Lambda の制限値（数字モノ）
- タイムアウト最大 **15分**／メモリ **128MB〜10GB**（**CPU はメモリに比例**）。
- デプロイパッケージ：zip 直接アップロード **50MB**、展開後 **250MB**。超えるなら **S3 経由 or コンテナイメージ**。
- 環境変数の変更は再デプロイ不要。秘密情報は環境変数直書きせず **SSM Parameter Store / Secrets Manager**。

### パッケージング（Windows 開発の落とし穴）
- ネイティブ依存（pydantic-core 等）は **Lambda と同じ OS/アーキ向けホイール**が必要：
  `pip install --target package --platform manylinux2014_x86_64 --implementation cp --python-version 3.12 --only-binary=:all:`
- Windows でそのまま `pip install` → win_amd64 バイナリが入り Lambda で **ImportError**。
- zip 化は PowerShell 5.1 の `Compress-Archive` を避け `shutil.make_archive`（zip 内パスがバックスラッシュになる罠）。
- boto3 は **Lambda ランタイム同梱**なのでパッケージに含めない。
- pip が requirements.txt を **ロケールエンコーディング（cp932）**で読むため、非 ASCII コメントで `UnicodeDecodeError`。対策：ASCII 化 or `PYTHONUTF8=1`。

### Mangum（アダプターパターン）
- FastAPI は ASGI（常駐サーバー前提）、Lambda は `handler(event, context)` の関数呼び出し。**Mangum が API Gateway の JSON イベント ⇔ ASGI を相互変換**する翻訳アダプター。
- アプリコードは Lambda 専用化しない（`handler = Mangum(app)` を足すだけ）→ Week 3 の Fargate 格上げ時は Uvicorn 起動でそのまま動く。
- 類似：WSGI(Flask)→aws-wsgi、Node(Express)→serverless-http。

## よくある誤答パターン
- 「Lambda のログが CloudWatch に出ない」→ 実行ロールに **`AWSLambdaBasicExecutionRole`（logs 3 権限）が無い**（エラーにならず、ただ出ない）。
- ロググループが**関数作成時にできる**と思う → 初回実行時に遅延作成。invoke 前の `put-retention-policy` は `ResourceNotFoundException`。
- 自動作成ロググループの保持期間をデフォルト 30 日等と思う → **無期限**。
- 関数を消せばログも消えると思う → **ロググループは残る**。
- パッケージが 50MB を超えて直接アップロード失敗 → **S3 経由 or コンテナイメージ**が正答。
- CPU を単独で増やそうとする → **CPU はメモリ設定に比例**（メモリを上げる）。

## 実機で確認すべきこと（FastAPI ToDo への適用）
- **Week 1 Day 2 実施**：`wk1-todo-api`（python3.12 / 256MB / 15s / `TABLE_NAME=Todos`）を CLI デプロイ。実行ロール `wk1-todo-lambda-role`。
- API GW v2 形式のテストイベント（`app/events/*.json`）で `lambda invoke` → `/health` 200、`POST /todos` 201 → DynamoDB `Todos` に反映。
- `aws logs tail /aws/lambda/wk1-todo-api --since 15m` で `START`/`created todo id=...`/`REPORT` を確認。
- 保持期間 7 日を設定（`put-retention-policy`）。
- **Day 3**：API Gateway を前段に付け公開。**Day 4 以降**：`Errors`/`Throttles` にアラーム、Dashboard 化。**Week 2**：CFn 化（ロググループ明示作成方式へ）。

## 関連サービスとの違い
- **CloudWatch Logs vs CloudTrail**：アプリ・サービスのログ vs 「誰が何の API を呼んだか」の監査証跡。
- **logs tail vs Logs Insights**：直近の生ログ追跡 vs クエリ言語での集計・分析（Week 1 後半で扱う）。
- **Lambda vs Fargate（Week 3）**：イベント駆動・従量 vs 常駐コンテナ。Mangum アダプターのおかげでアプリ改修ゼロで移行可能。

## 公式ドキュメント
- Lambda のログ（Python）: https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html
- Lambda 実行ロール: https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html
- Lambda メトリクス: https://docs.aws.amazon.com/lambda/latest/dg/monitoring-metrics.html
- Lambda クォータ: https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html
- Python デプロイパッケージ: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
- ロググループの保持期間: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html
- Mangum（非公式・PyPI）: https://pypi.org/project/mangum/
