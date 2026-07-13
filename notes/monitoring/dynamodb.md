# DynamoDB（Week 1 Day 1）

> FastAPI ToDo の永続化層。キャパシティ／CloudWatch メトリクス／キー設計／検索／バックアップの基礎を一括整理。

## 要点（試験で問われる観点）

### キャパシティモード
- **オンデマンド（PAY_PER_REQUEST）**：予測不能・スパイキー・新規アプリ向け。設計不要で自動スケール。単価は高いが無駄なし。
- **プロビジョンド + Auto Scaling**：安定・予測可能なワークロード向け。RCU/WCU を見積もる。コスト最適化しやすい。
- 単位：**1 WCU** = 1KB × 1書き込み/秒、**1 RCU** = 4KB の強整合読み取り 1回/秒（結果整合なら 2回/秒 ＝ RCU 半分）。
- キャパシティモードの切替は **24時間に1回**まで。

### キー設計（PK / SK）
- **PK（パーティションキー / HASH）**：項目を一意識別＋保存パーティションを決定。必須。値が**分散する属性**を選ぶ。
- **SK（ソートキー / RANGE）**：同一 PK 内での並べ替え・範囲絞り込み。任意。
- **単純主キー**＝PK のみ（1 PK＝1項目）／**複合主キー**＝PK+SK（同一 PK に複数項目、SK で識別・整列）。
- 王道パターン：**「PK でグループ化、SK で個体識別・並べ替え」**。例）ユーザー単位管理は `PK=user_id, SK=todo_id`。

### セカンダリインデックス（GSI / LSI）
| | GSI（グローバル） | LSI（ローカル） |
|---|---|---|
| PK | 別キーに変更可 | ベースと同じ PK 固定 |
| 作成 | **後からいつでも追加/削除可** | **テーブル作成時のみ** |
| キャパ | 独立（別課金） | ベースと共有 |
| 整合性 | **結果整合性のみ** | **強い整合性も可** |
| 上限 | 20 | 5 |
- 迷ったら **GSI がデフォルト**。LSI は「強整合が要る／要件が作成時に確定」のとき。

### 検索（Query / Scan / GetItem）
- **GetItem**：PK（+SK）指定で1件ピンポイント。最速。
- **Query**：PK 必須指定＋SK 範囲条件。絞り込み検索。効率的。
- **Scan**：全項目を読む。全件処理向け。大テーブルでは遅い・高い。
- 1レスポンス **最大1MB** → `LastEvaluatedKey` を `ExclusiveStartKey` に渡して**ページネーション**で全件取得。

### バックアップ / 復旧
- **PITR**：直近**35日**を**秒単位**で復元。うっかり削除/上書きを数分前に戻す用途。
- **オンデマンドバックアップ**：手動スナップショット、**無期限**保持。長期保管・コンプラ。
- **AWS Backup**：複数サービス横断で集中管理・ライフサイクル・クロスリージョン/アカウント。
- どの復元も**必ず新規テーブルとして**作られる（上書き復元は不可）。

### DynamoDB Streams
- 項目変更（作成/更新/削除）を時系列キャプチャ。保持**24時間**。
- **Streams + Lambda** でイベント駆動（変更検知の第一選択）。
- `StreamViewType`：`KEYS_ONLY` / `NEW_IMAGE` / `OLD_IMAGE` / `NEW_AND_OLD_IMAGES`。
- グローバルテーブル（マルチリージョン複製）は内部で Streams を利用。

## よくある誤答パターン
- **LSI を後から追加**しようとする → 不可（作成時のみ。GSI と混同）。
- キャパシティモードを頻繁に行き来 → **24時間に1回**制約を見落とす。
- Scan に `FilterExpression` を付ければ安くなると思う → **読み取り後**の絞り込みなので**消費キャパは減らない**。
- 復元で**既存の同名テーブルに上書き**しようとする → 常に新規テーブルとして復元。
- GSI を**強整合で読める**と思う → GSI は**結果整合性のみ**。
- `PK=user_id` **単独**で複数 ToDo を保存 → 同一 PK で**上書き**。SK が必要。
- 値の偏る属性（`completed` の true/false 等）を PK に採用 → **ホットパーティション**でスロットル。
- 結果整合なら RCU 半分で済むのに強整合で計算 → RCU 見積もりを誤る。

## 実機で確認すべきこと（FastAPI ToDo への適用）
- **Week 1 Day 1 実施済**：`Todos` テーブル（PK=`id`, `PAY_PER_REQUEST`, ap-northeast-1）を CLI 作成。`put/get-item` で動作確認。
- 書き込み後、`AWS/DynamoDB` 名前空間に `ConsumedWriteCapacityUnits` 等が発行されるのを CloudWatch で確認（数分ラグ）。
- **Day 2 以降**：`ThrottledRequests` に CloudWatch アラーム → SNS 通知を実装（監視の中核）。
- **設計メモ**：ユーザー単位の一覧要件が主役になるなら `PK=user_id, SK=todo_id` 型が向く。横断検索（期限切れ一覧等）は **GSI** で追加。
- **Week 2 予定**：この CLI 作成テーブルを **CloudFormation リソースインポート**でスタック管理下に取り込む（案 B）。

## 関連サービスとの違い
- **PITR vs オンデマンドバックアップ vs AWS Backup**：秒単位35日／無期限任意時点／横断集中管理。
- **Streams + Lambda vs SQS / EventBridge**：DynamoDB の変更検知は Streams が第一選択（SQS/EventBridge に誘導するのはひっかけ）。
- **Query vs Scan vs GetItem**：絞り込み／全件／1件。「効率的に・コスト最適に」と来たら Scan は不正解の合図。
- **GSI vs LSI**：別軸・後付け／同一PKの別ソート・強整合。

## 監視メトリクス早見表（CloudWatch）
| メトリクス | 意味 |
|---|---|
| `ThrottledRequests` | スロットルされたリクエスト総数 |
| `ReadThrottleEvents` / `WriteThrottleEvents` | 読み/書きスロットル発生数 |
| `ConsumedReadCapacityUnits` / `ConsumedWriteCapacityUnits` | 実消費キャパシティ |
| `SuccessfulRequestLatency` | リクエスト遅延 |
| `SystemErrors`(5xx) / `UserErrors`(4xx) | AWS 側 / クライアント側エラー |
- スロットルの原因パーティション特定 → **Contributor Insights for DynamoDB**。

## 公式ドキュメント
- キャパシティモード: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html
- コアコンポーネント（キー）: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html
- パーティションキー設計: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html
- GSI: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html
- LSI: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html
- Query: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html
- Scan: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html
- PITR: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery.html
- バックアップ復元: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/BackupRestore.html
- Streams: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html
- CloudWatch メトリクス: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/metrics-dimensions.html
