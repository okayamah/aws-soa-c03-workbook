# ノート・誤答ログの書式テンプレート

## ノート（`notes/<分野>/<トピック>.md`）

```markdown
# <トピック>

## 要点（試験で問われる観点）
- ...

## よくある誤答パターン
- ...

## 実機で確認すべきこと（FastAPI ToDo への適用）
- ...

## 関連サービスとの違い
- ...

## 公式ドキュメント
- https://docs.aws.amazon.com/...
```

## 誤答ログ（`mistakes.md`）

```markdown
## YYYY-MM-DD <模試名・問番号>
- 分野：Monitoring / Reliability / Deployment / Networking / Security
- 問われた論点：
- 自分の解答 / 正解：
- 誤答の原因：（知識不足 / 読み違い / 紛らわしい選択肢）
- 再発防止：（参照ノート / 実機で確認したこと）
- タグ：#cloudwatch #alarm #composite
```
