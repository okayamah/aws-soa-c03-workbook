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
