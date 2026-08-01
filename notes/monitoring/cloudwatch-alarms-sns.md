# CloudWatch アラーム × SNS × Dashboard（Week 1 Day 4）

> Lambda / DynamoDB / API Gateway の主要メトリクスにアラームを張り、SNS で通知、Dashboard で可視化した回の整理。Week 1「監視」の総仕上げ。

## 要点（試験で問われる観点）

### CloudWatch Alarm はメールを送れない → 必ず SNS を経由
```
CloudWatch Alarm（しきい値超過を検知）→ SNS Topic（Publish）→ 購読者へ配信（Email/SMS/Lambda/SQS/HTTPS…）
```
- アラームの `--alarm-actions` に **SNS トピック ARN** を指定するのが唯一の通知経路。EventBridge や ChatBot と組み合わせる高度な構成もこの上に成り立つ。
- **AWS のあらゆる通知の出口は基本 SNS**（GuardDuty、Budgets、Auto Scaling 通知なども同様）と覚えると横断的に効く。

### SNS = Pub/Sub モデル（発行者と購読者は疎結合）
- **Topic**：メッセージの送り先となる箱（今回：`wk1-todo-alerts`）。
- **Publish**：誰か（CloudWatch Alarm 等）がトピックにメッセージを送る。
- **Subscribe**：1つのトピックに **複数の購読者・複数プロトコル**を同時登録できる（Email / SMS / Lambda / SQS / HTTP(S) / モバイルプッシュ）。「メールと Slack と Lambda で同時に自動対処」も同じトピックへの多重購読で実現。
- **Email 購読は Confirm 必須**：`subscribe` 直後は `PendingConfirmation`。確認メールの「Confirm subscription」リンクをクリックするまで配信されない（知らない宛先への迷惑配信を防ぐ仕組み）。Lambda/SQS 購読は確認不要で即有効、という対比が問われることがある。

### アラームの状態遷移と評価ロジック
- 状態は3種類：**`OK` / `ALARM` / `INSUFFICIENT_DATA`**。
- `--period`（集計間隔）× `--evaluation-periods`（連続何回で判定）で構成。一時的なスパイクで鳴らしたくない → `evaluation-periods` を増やす。
- **`--treat-missing-data`**：データ点が来ない場合の扱い。`notBreaching`（異常扱いしない）/ `breaching` / `ignore` / `missing`。呼び出しが常時発生しない Lambda/API では **`notBreaching` が定石**（データが無い＝異常、ではない）。
- **複合アラーム（Composite Alarm）**：複数アラームを AND/OR で束ね、「本当に危険な時だけ」通知する上位機能（発展論点）。

### Dashboard は可視化のみ、アラート機能は無い
- CloudWatch Dashboard は**メトリクスをグラフ化して見るだけ**の機能。しきい値通知はできない（それはアラームの役割）→ **Dashboard とアラームは別物**という区別が問われる。
- ウィジェットは `metrics` 配列に `[Namespace, MetricName, DimensionName, DimensionValue, {stat: ...}]` を並べて定義。
- コスト：**最初の3ダッシュボードまで無料**、4つ目以降 $3/月/ダッシュボード。

### 監視した3層のメトリクス
| 層 | Namespace | 主要メトリクス | 今回のアラーム |
|---|---|---|---|
| Lambda | `AWS/Lambda` | Invocations / Errors / Throttles / Duration | `Errors ≥ 1`（5分, Sum） |
| DynamoDB | `AWS/DynamoDB` | ConsumedRead/WriteCapacityUnits / ThrottledRequests | `ThrottledRequests ≥ 1`（5分, Sum） |
| API Gateway | `AWS/ApiGateway` | Count / 4xx / 5xx / Latency | `5xx ≥ 1`（5分, Sum） |
- API Gateway のメトリクス次元は **`ApiId`**（HTTP API・REST API 共通の namespace `AWS/ApiGateway`）。

## よくある誤答パターン
- CloudWatch Alarm から**直接メール送信できると誤解** → 必ず SNS 経由。
- SNS の Email 購読を作った直後に**通知が届くと思い込む** → Confirm 待ちの `PendingConfirmation` 状態。
- データが来ない状態を**即異常（ALARM）だと誤解** → `INSUFFICIENT_DATA`。`treat-missing-data` 未設定だと意図せずアラームが鳴る/鳴らないの誤判定に繋がる。
- **Dashboard 自体が通知してくれると誤解** → Dashboard は可視化専用、通知機能なし。
- 一時的なスパイクで頻繁に誤報 → `evaluation-periods` を1のままにしている（複数期間の連続超過に直すのが対策）。

## 実機で確認すべきこと（FastAPI ToDo への適用）
- **Week 1 Day 4 実施**：SNS トピック `wk1-todo-alerts` を作成しメール購読。Lambda `Errors`／DynamoDB `ThrottledRequests`／API Gateway `5xx` の3アラームを作成し、同一トピックに集約。`wk1-todo-dashboard` で3層を1画面に可視化（[scripts/wk1/dashboard.json](../../scripts/wk1/dashboard.json)）。
- 不正ペイロードで Lambda を invoke し、`Errors` アラームが `OK → ALARM` に遷移して通知メールが届くことを実際に確認。
- **Week 2**：この3アラーム＋SNSトピックを CloudFormation（`AWS::CloudWatch::Alarm` / `AWS::SNS::Topic`）に写経。
- **Week 3**：Auto Scaling のスケーリングポリシーのトリガーとして CloudWatch アラームを再利用する構成に接続。
- **Week 5**：同じ SNS トピックを GuardDuty Finding 通知にも再利用できる（セキュリティ通知の統合）。

## 関連サービスとの違い
- **CloudWatch Alarm vs Dashboard**：しきい値監視・通知トリガー vs 可視化のみ。
- **SNS vs SQS**：即時プッシュ配信（Pub/Sub、複数購読者に同時配信） vs ポーリング型キュー（1メッセージを1コンシューマーが取り出す）。
- **CloudWatch Logs vs メトリクス/アラーム**：ログは生イベントの記録、アラームは集計値のしきい値監視（[lambda-cloudwatch-logs.md](lambda-cloudwatch-logs.md) 参照）。
- **単一アラーム vs Composite Alarm**：個別しきい値監視 vs 複数アラームの論理演算による高次判定。

## 公式ドキュメント
- CloudWatch アラームの仕組み: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html
- アラームの状態と欠損データの扱い: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-effective-states
- 複合アラーム: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Create_Composite_Alarm.html
- SNS の概要（Pub/Sub）: https://docs.aws.amazon.com/sns/latest/dg/welcome.html
- SNS サブスクリプション: https://docs.aws.amazon.com/sns/latest/dg/sns-create-subscribe-endpoint-to-topic.html
- CloudWatch Dashboard: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Dashboards.html
- Lambda メトリクス: https://docs.aws.amazon.com/lambda/latest/dg/monitoring-metrics.html
- DynamoDB メトリクス: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/metrics-dimensions.html
- API Gateway メトリクス: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-metrics-and-dimensions.html
