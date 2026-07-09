# Mistakes Log

Udemy 375問・公式 Pretest・実機ハンズオンで間違えた／迷った論点を蓄積する。
週ごとに分野で集計し、翌週の日次サイクルで再確認する。

タグ規約：`#<service>` `#<topic>` `#<分野>`
例：`#cloudwatch #alarm #monitoring`

---

## テンプレート（コピーして使う）

```markdown
## YYYY-MM-DD <模試名・問番号>
- 分野：Monitoring / Reliability / Deployment / Networking / Security
- 問われた論点：
- 自分の解答 / 正解：
- 誤答の原因：（知識不足 / 読み違い / 紛らわしい選択肢）
- 再発防止：（参照ノート URL / 実機で確認したこと）
- タグ：
```

---

## サンプル（学習開始時の例。実際の記録は下に追加していく）

## 2026-XX-XX 公式 Practice Question Set #3
- 分野：Monitoring
- 問われた論点：CloudWatch メトリクスフィルタ vs サブスクリプションフィルタ の使い分け
- 自分の解答 / 正解：B / D
- 誤答の原因：両者の出力先の違いを覚えていなかった
- 再発防止：notes/monitoring/cloudwatch-logs.md に整理。実機でメトリクスフィルタを作ってカスタムメトリクスを生成、サブスクリプションフィルタで Kinesis に送るところまで確認
- タグ：#cloudwatch #logs #monitoring

---

## 記録（ここから下に追記していく）

### 2026-07-09 AWS公式 Practice Question Set（初回）

**総合スコア：7/20（35%）**

| ドメイン | 正解率 | 問数 |
|---|---|---|
| 1.0 モニタリング・ログ・修復・パフォーマンス | 50% | 4 |
| 2.0 信頼性と事業の継続性 | 50% | 4 |
| 3.0 デプロイ・プロビジョニング・オートメーション | 25% | 4 |
| 4.0 セキュリティとコンプライアンス | 25% | 4 |
| 5.0 ネットワークとコンテンツ配信 | 25% | 4 |

---

## 2026-07-09 公式PQS #3（S3 クロスリージョンレプリケーション）
- 分野：Networking
- 問われた論点：グローバル企業が複数リージョンの S3 から低レイテンシでアクセスするための構成
- 自分の解答 / 正解：送信先バケットのレプリケーションを有効化 / 送信元バケットでクロスリージョンレプリケーションを設定
- 誤答の原因：知識不足。レプリケーションは送信元で設定し、バージョニングが必要という基本を把握していなかった
- 再発防止：notes/networking/ に S3 レプリケーション整理
- タグ：#s3 #replication #networking

## 2026-07-09 公式PQS #4（S3 ゲートウェイ VPC エンドポイント）
- 分野：Networking
- 問われた論点：プライベートサブネットから S3 へ NAT Gateway を使わずアクセスする方法
- 自分の解答 / 正解：S3 ファイルゲートウェイを設定 / S3 ゲートウェイ VPC エンドポイント
- 誤答の原因：知識不足。S3 ゲートウェイ VPC エンドポイントの存在と用途を理解していなかった
- 再発防止：notes/networking/ に VPC エンドポイント（Gateway vs Interface）整理
- タグ：#vpc #endpoint #s3 #networking

## 2026-07-09 公式PQS #5（CloudWatch アラーム → EventBridge → 自動修復）
- 分野：Monitoring
- 問われた論点：CloudWatch アラーム発火時に自動修復する運用上の最小オーバーヘッド構成
- 自分の解答 / 正解：AWS Config ルール / EventBridge + Automation ランブック
- 誤答の原因：知識不足。EventBridge → Systems Manager Automation の自動修復パターンを知らなかった
- 再発防止：notes/monitoring/ に CloudWatch Alarm → EventBridge → SSM Automation パターン整理
- タグ：#cloudwatch #eventbridge #ssm-automation #monitoring

## 2026-07-09 公式PQS #6（SSM Automation でパッチ適用自動化）
- 分野：Deployment
- 問われた論点：複数 EC2 へのパッチ適用・メンテナンスウィンドウ・コンプライアンス報告の自動化
- 自分の解答 / 正解：CloudFormation StackSets / Systems Manager（State Manager + Automation）
- 誤答の原因：知識不足。State Manager と Automation ランブックの使い分けを理解していなかった
- 再発防止：notes/deployment/ に SSM（State Manager / Automation / Patch Manager）整理
- タグ：#ssm #automation #state-manager #deployment

## 2026-07-09 公式PQS #7（Organizations の SCP）
- 分野：Security
- 問われた論点：Organizations で複数アカウントの特定リージョン以外へのアクセスを制限する方法
- 自分の解答 / 正解：各メンバーアカウントで設定 / SCP で aws:RequestedRegion 条件キーを使用
- 誤答の原因：知識不足。SCP の条件キー aws:RequestedRegion でリージョン制限できることを知らなかった
- 再発防止：notes/security/ に SCP のユースケース・条件キー整理
- タグ：#organizations #scp #security

## 2026-07-09 公式PQS #8（Route 53 メール配信のための DNS レコード）
- 分野：Networking
- 問われた論点：SES でメール送信時に SPF を設定するための DNS レコードタイプ
- 自分の解答 / 正解：A レコード（SES サービスの IP アドレスを登録）/ SPF レコード用のカスタム MAIL FROM ドメイン設定
- 誤答の原因：知識不足。SES のメール認証（SPF/DKIM）に必要な DNS レコード設定を理解していなかった
- 再発防止：notes/networking/ に Route 53 + SES の DNS レコード設定整理
- タグ：#route53 #ses #dns #networking

## 2026-07-09 公式PQS #13（Lambda 関数のプロビジョンドコンカレンシー）
- 分野：Deployment
- 問われた論点：Lambda のコールドスタートによるタイムアウトを最小労力で解消する方法
- 自分の解答 / 正解：Lambda 関数のコードを変更 / プロビジョンドコンカレンシーを設定
- 誤答の原因：知識不足。プロビジョンドコンカレンシーがコールドスタート対策であることを知らなかった
- 再発防止：notes/deployment/ に Lambda 実行モデル（コールドスタート / Provisioned Concurrency）整理
- タグ：#lambda #concurrency #deployment

## 2026-07-09 公式PQS #14（VPC フローログ + Ingress-only IGW）
- 分野：Networking
- 問われた論点：インターネットからの VPC へのインバウンドトラフィックをブロックし、アウトバウンドのみ許可する構成
- 自分の解答 / 正解：デフォルト SG のインバウンドルールを制限 / VPC フローログ有効化 + Egress-only IGW
- 誤答の原因：知識不足。Egress-only インターネットゲートウェイ（IPv6 用）の存在を知らなかった
- 再発防止：notes/networking/ に IGW / Egress-only IGW / NAT GW の使い分け整理
- タグ：#vpc #igw #flowlogs #networking

## 2026-07-09 公式PQS #15（IAM クレデンシャルレポート + OIDC IdP）
- 分野：Security
- 問われた論点：IAM ユーザーのアクティビティ監査とバックアップ検証の方法
- 自分の解答 / 正解：IAM ユーザーを監査し Security Token Service で一時認証 / IAM クレデンシャルレポート + OIDC IdP の信頼ポリシー
- 誤答の原因：知識不足。クレデンシャルレポートの内容と OIDC IdP を IAM ロールの信頼ポリシーに使うパターンを理解していなかった
- 再発防止：notes/security/ に IAM 監査ツール（Credential Report / Access Analyzer / OIDC）整理
- タグ：#iam #credential-report #oidc #security

## 2026-07-09 公式PQS #16（S3 イベント通知のプレフィクスフィルタ）
- 分野：Monitoring
- 問われた論点：Lambda 関数の無限ループ（トリガーとファイル出力が同一バケット）を解消する方法
- 自分の解答 / 正解：Lambda のタイムアウトを変更 / S3 イベント通知のプレフィクスフィルタで入出力を分離
- 誤答の原因：知識不足。S3 イベント通知でプレフィクス／サフィックスフィルタが使えることを知らなかった
- 再発防止：notes/monitoring/ に S3 イベント通知の設定（フィルタ・Lambda トリガー）整理
- タグ：#s3 #lambda #event-notification #monitoring

## 2026-07-09 公式PQS #18（CloudWatch Logs → PII 検出は Macie）
- 分野：Security
- 問われた論点：S3 に保存された CloudWatch Logs の個人情報（PII）を検出する方法
- 自分の解答 / 正解：Amazon Macie を有効化 + Lambda で検出 / CloudWatch Logs のデータ保護ポリシーでマスキング
- 誤答の原因：知識不足。CloudWatch Logs のデータ保護ポリシー（PII 自動検出・マスキング）機能を知らなかった
- 再発防止：notes/security/ に PII 検出手段（CloudWatch Logs データ保護 / Macie / Comprehend）整理
- タグ：#cloudwatch-logs #pii #data-protection #security

## 2026-07-09 公式PQS #19（CloudFormation StackSets）
- 分野：Deployment
- 問われた論点：Organizations の複数アカウントに CloudFormation で一括デプロイする方法
- 自分の解答 / 正解：AWS CloudTrail を有効化 / CloudFormation StackSets
- 誤答の原因：知識不足。StackSets が Organizations と連携して複数アカウントに一括デプロイできることを知らなかった
- 再発防止：notes/deployment/ に CloudFormation StackSets（Organizations 連携・OU 単位デプロイ）整理
- タグ：#cloudformation #stacksets #organizations #deployment

## 2026-07-09 公式PQS #20（ALB + Auto Scaling のスケーリングポリシー）
- 分野：Monitoring
- 問われた論点：ALB 配下の EC2 Auto Scaling で CPU 使用率が高い場合のコスト効率の良い対処
- 自分の解答 / 正解：より大きい CPU のインスタンスタイプに変更 / ターゲット追跡スケーリングポリシーを設定
- 誤答の原因：知識不足。ターゲット追跡スケーリングポリシー（Target Tracking）の仕組みを理解していなかった
- 再発防止：notes/monitoring/ に Auto Scaling ポリシー（Target Tracking / Step / Simple）整理
- タグ：#autoscaling #scaling-policy #monitoring
