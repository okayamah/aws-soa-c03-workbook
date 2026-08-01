# Week 1 ハンズオン実行ログ

> `/handson` で実施したコマンドと一言解説の記録。詳細な解説・試験ポイントは各 `notes/` を参照。
> このファイルは実行履歴（What）、`notes/` は体系化された知識（Why/試験観点）という役割分担。

---

## Day 1 — DynamoDB `Todos` テーブル作成

> 詳細: [notes/monitoring/dynamodb.md](../../notes/monitoring/dynamodb.md)

```powershell
# テーブル作成（オンデマンド課金、PK=id）
aws dynamodb create-table --table-name Todos --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --billing-mode PAY_PER_REQUEST --tags Key=Project,Value=soa-c03-workbook Key=App,Value=fastapi-todo Key=Week,Value=1 Key=Owner,Value=okayamah --region ap-northeast-1

# ACTIVE になるまで待機
aws dynamodb wait table-exists --table-name Todos --region ap-northeast-1

# 動作確認（書き込み→読み取り）
aws dynamodb put-item --table-name Todos --item '{\"id\":{\"S\":\"t-001\"},\"title\":{\"S\":\"買い物\"},\"completed\":{\"BOOL\":false}}' --region ap-northeast-1
aws dynamodb get-item --table-name Todos --key '{\"id\":{\"S\":\"t-001\"}}' --region ap-northeast-1

# 検証：テーブル状態・課金モード
aws dynamodb describe-table --table-name Todos --query "Table.TableStatus" --region ap-northeast-1
aws dynamodb describe-table --table-name Todos --query "Table.BillingModeSummary.BillingMode" --region ap-northeast-1

# 検証：CloudWatch にメトリクスが発行されているか
aws cloudwatch list-metrics --namespace AWS/DynamoDB --dimensions Name=TableName,Value=Todos --region ap-northeast-1
```

**クリーンアップ判断**：`Todos` は Week 3 以降も使う永続資産のため**削除せず継続利用**。Week 2 で CloudFormation リソースインポートの教材にする（案B、[wk2-import-todos-table メモリ](../../CLAUDE.md) 参照）。

---

## Day 2 — FastAPI を Mangum 経由で Lambda にデプロイ

> 詳細: [notes/monitoring/lambda-cloudwatch-logs.md](../../notes/monitoring/lambda-cloudwatch-logs.md)・[notes/security/iam-role-policies.md](../../notes/security/iam-role-policies.md)

```powershell
cd app

# ① Lambda(Linux/Python3.12) 向けに依存パッケージを取得
#    Windows のネイティブビルドを掴まないよう platform/python-version を明示
pip install --target package --platform manylinux2014_x86_64 --implementation cp --python-version 3.12 --only-binary=:all: -r requirements.txt

# ② デプロイ用 zip 作成（Compress-Archive はパス区切りの罠があるため shutil を使用）
copy main.py package\
python -c "import shutil; shutil.make_archive('function', 'zip', 'package')"

cd ..

# ③ Lambda 実行ロール作成（信頼ポリシー → 管理ポリシー → インラインポリシーの順）
aws iam create-role --role-name wk1-todo-lambda-role --assume-role-policy-document file://scripts/wk1/lambda-trust-policy.json --tags Key=Project,Value=soa-c03-workbook Key=App,Value=fastapi-todo Key=Week,Value=1 Key=Owner,Value=okayamah
aws iam attach-role-policy --role-name wk1-todo-lambda-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam put-role-policy --role-name wk1-todo-lambda-role --policy-name todos-table-crud --policy-document file://scripts/wk1/lambda-dynamodb-policy.json

# ④ Lambda 関数作成（IAM 伝播ラグで初回失敗したら数秒待って再実行）
$ROLE_ARN = aws iam get-role --role-name wk1-todo-lambda-role --query Role.Arn --output text
aws lambda create-function --function-name wk1-todo-api --runtime python3.12 --architectures x86_64 --handler main.handler --zip-file fileb://app/function.zip --role $ROLE_ARN --timeout 15 --memory-size 256 --environment "Variables={TABLE_NAME=Todos}" --tags Project=soa-c03-workbook,App=fastapi-todo,Week=1,Owner=okayamah --region ap-northeast-1

# ⑤ 初回 invoke でロググループを遅延作成させてから保持期間を設定
aws lambda invoke --function-name wk1-todo-api --payload fileb://app/events/health.json --region ap-northeast-1 out.json
aws logs put-retention-policy --log-group-name /aws/lambda/wk1-todo-api --retention-in-days 7 --region ap-northeast-1

# 検証：ToDo 作成（DynamoDB 書き込み確認）
aws lambda invoke --function-name wk1-todo-api --payload fileb://app/events/create-todo.json --region ap-northeast-1 out2.json
aws dynamodb scan --table-name Todos --region ap-northeast-1 --query "Count"

# 検証：CloudWatch Logs（START/REPORT 行を確認）
aws logs tail /aws/lambda/wk1-todo-api --since 15m --region ap-northeast-1
```

**Windows 固有の落とし穴**：`requirements.txt` に非 ASCII コメントを書くと pip が `cp932` で読もうとして `UnicodeDecodeError`。コメントは ASCII にするか `$env:PYTHONUTF8 = "1"` を設定。

**クリーンアップ判断**：Lambda・DynamoDB は安価なため**継続利用**（Day 3 で API Gateway から接続するため）。

---

## Day 3 — API Gateway（HTTP API）で公開

> 詳細: [notes/networking/api-gateway.md](../../notes/networking/api-gateway.md)

```powershell
# ① HTTP API 作成
$API_ID = aws apigatewayv2 create-api --name wk1-todo-http-api --protocol-type HTTP --tags Project=soa-c03-workbook,App=fastapi-todo,Week=1,Owner=okayamah --region ap-northeast-1 --query ApiId --output text

# ② Lambda プロキシ統合を作成（AWS_PROXY、payload format 2.0）
$LAMBDA_ARN = aws lambda get-function --function-name wk1-todo-api --query Configuration.FunctionArn --output text --region ap-northeast-1
$INTEGRATION_ID = aws apigatewayv2 create-integration --api-id $API_ID --integration-type AWS_PROXY --integration-uri $LAMBDA_ARN --payload-format-version 2.0 --region ap-northeast-1 --query IntegrationId --output text

# ③ ルート作成（すべてのパス・メソッドを Lambda に丸投げ）
aws apigatewayv2 create-route --api-id $API_ID --route-key 'ANY /{proxy+}' --target "integrations/$INTEGRATION_ID" --region ap-northeast-1

# ④ ステージをデプロイ（$default = URLにステージ名を含めない特殊ステージ、auto-deploy で以後の変更を自動反映）
aws apigatewayv2 create-stage --api-id $API_ID --stage-name '$default' --auto-deploy --region ap-northeast-1

# ⑤ API Gateway から Lambda を呼べるようリソースベースポリシーを付与（これが無いと 403）
aws lambda add-permission --function-name wk1-todo-api --statement-id apigw-invoke --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:ap-northeast-1:<account-id>:$API_ID/*/*/{proxy+}" --region ap-northeast-1

# ⑥ 公開エンドポイント取得
$ENDPOINT = aws apigatewayv2 get-api --api-id $API_ID --query ApiEndpoint --output text --region ap-northeast-1

# 検証（PowerShell では curl は Invoke-WebRequest のエイリアスなので curl.exe か Invoke-RestMethod を使う）
Invoke-RestMethod -Uri "$ENDPOINT/health"
Invoke-RestMethod -Method Post -Uri "$ENDPOINT/todos" -ContentType "application/json" -Body '{"title":"API GW経由","completed":false}'
Invoke-RestMethod -Uri "$ENDPOINT/todos"
```

**クリーンアップ判断**：API Gateway（HTTP API）は無料利用枠内・低コストのため**継続利用**。Week 1 の最小構成（API Gateway + Lambda + DynamoDB）が完成。

---

## Day 4 — CloudWatch アラーム・SNS・Dashboard で監視を仕上げる

> 詳細: [notes/monitoring/cloudwatch-alarms-sns.md](../../notes/monitoring/cloudwatch-alarms-sns.md)

```powershell
# ① Day 3 の API Gateway ID を再取得（新セッションで変数が消えているため）
$API_ID = aws apigatewayv2 get-apis --query "Items[?Name=='wk1-todo-http-api'].ApiId" --output text --region ap-northeast-1

# ② SNS トピック作成＋メール購読（確認メールの Confirm リンクを押すまで通知は届かない）
$TOPIC_ARN = aws sns create-topic --name wk1-todo-alerts --tags Key=Project,Value=soa-c03-workbook Key=App,Value=fastapi-todo Key=Week,Value=1 Key=Owner,Value=okayamah --region ap-northeast-1 --query TopicArn --output text
aws sns subscribe --topic-arn $TOPIC_ARN --protocol email --notification-endpoint *****@gmail.com --region ap-northeast-1

# ③ Lambda Errors アラーム（呼び出しが常時無いため treat-missing-data は notBreaching）
aws cloudwatch put-metric-alarm --alarm-name wk1-todo-lambda-errors --namespace AWS/Lambda --metric-name Errors --dimensions Name=FunctionName,Value=wk1-todo-api --statistic Sum --period 300 --evaluation-periods 1 --threshold 1 --comparison-operator GreaterThanOrEqualToThreshold --treat-missing-data notBreaching --alarm-actions $TOPIC_ARN --tags Key=Project,Value=soa-c03-workbook Key=App,Value=fastapi-todo Key=Week,Value=1 Key=Owner,Value=okayamah --region ap-northeast-1

# ④ DynamoDB ThrottledRequests アラーム
aws cloudwatch put-metric-alarm --alarm-name wk1-todo-dynamodb-throttles --namespace AWS/DynamoDB --metric-name ThrottledRequests --dimensions Name=TableName,Value=Todos --statistic Sum --period 300 --evaluation-periods 1 --threshold 1 --comparison-operator GreaterThanOrEqualToThreshold --treat-missing-data notBreaching --alarm-actions $TOPIC_ARN --tags Key=Project,Value=soa-c03-workbook Key=App,Value=fastapi-todo Key=Week,Value=1 Key=Owner,Value=okayamah --region ap-northeast-1

# ⑤ API Gateway 5xx アラーム
aws cloudwatch put-metric-alarm --alarm-name wk1-todo-apigw-5xx --namespace AWS/ApiGateway --metric-name 5xx --dimensions Name=ApiId,Value=$API_ID --statistic Sum --period 300 --evaluation-periods 1 --threshold 1 --comparison-operator GreaterThanOrEqualToThreshold --treat-missing-data notBreaching --alarm-actions $TOPIC_ARN --tags Key=Project,Value=soa-c03-workbook Key=App,Value=fastapi-todo Key=Week,Value=1 Key=Owner,Value=okayamah --region ap-northeast-1

# ⑥ Dashboard 作成（テンプレートの {{API_ID}} を実値に置換してから投入）
(Get-Content scripts/wk1/dashboard.json) -replace '\{\{API_ID\}\}', $API_ID | Set-Content scripts/wk1/dashboard.rendered.json
aws cloudwatch put-dashboard --dashboard-name wk1-todo-dashboard --dashboard-body file://scripts/wk1/dashboard.rendered.json --region ap-northeast-1

# ⑦ アラーム発火の実機確認（不正ペイロードで Lambda Errors を誘発）
'{"invalid":"payload"}' | Out-File -Encoding utf8 app/events/bad.json
aws lambda invoke --function-name wk1-todo-api --payload fileb://app/events/bad.json --region ap-northeast-1 out3.json

# 検証：アラーム状態・SNS購読・Dashboard反映
aws cloudwatch describe-alarms --alarm-name-prefix wk1-todo --query "MetricAlarms[].{Name:AlarmName,State:StateValue}" --region ap-northeast-1
aws sns list-subscriptions-by-topic --topic-arn $TOPIC_ARN --region ap-northeast-1 --query "Subscriptions[].SubscriptionArn"
aws cloudwatch get-dashboard --dashboard-name wk1-todo-dashboard --region ap-northeast-1 --query DashboardName
```

**⑦の実機確認**：不正ペイロードで Lambda を invoke → `wk1-todo-lambda-errors` が `OK → ALARM` に遷移 → SNS 経由でメール通知が届くことを確認済み。

**クリーンアップ判断**：アラーム3件・SNSトピック・Dashboard はいずれも低コスト（Dashboard は3つ目まで無料）のため**継続利用**。これで Week 1 の実機ハンズオン（DynamoDB → Lambda → API Gateway → 監視）が完成。

---

## Week 1 まとめ

Day 1〜4 で [app-roadmap.md](../guidelines/app-roadmap.md) の Week 1 目標「API Gateway + Lambda + DynamoDB 最小デプロイ／CloudWatch Logs・Alarm・ダッシュボード」を実機構築済み。Week 2（自動化・IaC）では、ここまで CLI で作った各リソースを CloudFormation 化していく（`Todos` テーブルはリソースインポート、他は新規テンプレート）。
