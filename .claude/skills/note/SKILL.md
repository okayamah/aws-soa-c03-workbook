---
name: note
description: 学習ノートを notes/<分野>/ に生成・更新する。「ノートにまとめて」「notes に書いて」「〜の違いを整理して」と言われたら使用。
---

# ノート生成

`notes/<分野>/<トピック>.md` に以下の書式で書く。分野は monitoring / reliability / deployment / networking / security のいずれか。

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

## ルール

- **公式ドキュメント URL を必ず添える**。URL が不確かなら憶測で書かず、Web 検索を提案する
- 「実機で確認すべきこと」は FastAPI ToDo アプリへの適用として書く（app-roadmap.md の週と紐付ける）
- 既存ノートがあれば上書きせずセクション単位で追記・更新する
