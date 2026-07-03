# PC 環境 read-only 収集手順（Claude Code セットアップ監査用）

リモートセッションの Claude Code からは PC 本体が見えないため、以下を **PowerShell で実行して出力を収集**する。
すべて読み取り専用コマンドで、ファイルの中身は Claude Code 設定ファイル以外開かない。

収集した出力は 1 つのテキストにまとめ、チャットに貼り付けるか、本リポジトリの一時ブランチ（例：`audit/pc-snapshot`）に `docs/plan/pc-snapshot.txt` としてコミットして共有する。

> ⚠️ **共有前のマスク必須**：手順 5 の `.claude.json` にはトークンや API キーが含まれる場合がある。指定のプロパティのみ抽出するコマンドを使い、万一 `token` / `key` / `secret` を含む値が出力に混ざったら伏せ字にすること。

---

## 1. ホーム直下の階層（散らかり具合の把握）

```powershell
"=== 1. HOME (depth 1) ==="
Get-ChildItem ~ -Force | Select-Object Mode, LastWriteTime, Name | Format-Table -AutoSize

"=== 1b. ドキュメント / ダウンロード / デスクトップ (depth 1) ==="
Get-ChildItem ~\Documents, ~\Downloads, ~\Desktop -Force -ErrorAction SilentlyContinue |
  Select-Object Mode, LastWriteTime, @{n="Path";e={$_.FullName.Replace($HOME,"~")}} | Format-Table -AutoSize
```

## 2. 開発フォルダのツリー（深さ 2 まで・node_modules 等は除外）

開発プロジェクトを置いているルート（例：`~\dev`、`~\source`、`C:\projects`）に読み替えて実行：

```powershell
"=== 2. DEV TREE (depth 2) ==="
Get-ChildItem <開発ルート> -Directory -Recurse -Depth 2 -Force -ErrorAction SilentlyContinue |
  Where-Object { $_.FullName -notmatch "node_modules|\.venv|__pycache__|\.git($|\\)" } |
  ForEach-Object { $_.FullName.Replace($HOME,"~") }
```

## 3. ~/.claude/（ユーザーグローバル設定）

```powershell
"=== 3. ~/.claude 一覧 ==="
Get-ChildItem ~\.claude -Recurse -Force -ErrorAction SilentlyContinue |
  Select-Object Length, LastWriteTime, @{n="Path";e={$_.FullName.Replace($HOME,"~")}} | Format-Table -AutoSize

"=== 3b. グローバル CLAUDE.md / settings.json / keybindings ==="
Get-Content ~\.claude\CLAUDE.md -ErrorAction SilentlyContinue
Get-Content ~\.claude\settings.json -ErrorAction SilentlyContinue
Get-Content ~\.claude\keybindings.json -ErrorAction SilentlyContinue

"=== 3c. グローバル skills / agents / rules / output-styles の中身 ==="
Get-ChildItem ~\.claude\skills, ~\.claude\agents, ~\.claude\rules, ~\.claude\output-styles -Recurse -File -ErrorAction SilentlyContinue |
  ForEach-Object { "--- $($_.FullName.Replace($HOME,'~')) ---"; Get-Content $_.FullName }
```

## 4. 各プロジェクトの Claude Code 設定の有無

```powershell
"=== 4. プロジェクト別 CLAUDE.md / .claude / .mcp.json ==="
Get-ChildItem <開発ルート> -Directory | ForEach-Object {
  [PSCustomObject]@{
    Project   = $_.Name
    CLAUDEmd  = Test-Path (Join-Path $_.FullName "CLAUDE.md")
    DotClaude = Test-Path (Join-Path $_.FullName ".claude")
    McpJson   = Test-Path (Join-Path $_.FullName ".mcp.json")
    GitRepo   = Test-Path (Join-Path $_.FullName ".git")
  }
} | Format-Table -AutoSize
```

## 5. MCP・プロジェクト登録状況（トークンを除外して抽出）

```powershell
"=== 5. .claude.json の MCP / プロジェクト一覧（キー名のみ）==="
$c = Get-Content ~\.claude.json -Raw | ConvertFrom-Json
"mcpServers:"; $c.mcpServers.PSObject.Properties.Name
"projects:";   $c.projects.PSObject.Properties.Name
```

## 6. Claude Code の診断情報

```powershell
"=== 6. version / doctor ==="
claude --version
claude doctor 2>&1
```

---

## 収集後

出力一式を共有してもらえたら、以下を実施する：

1. PC 全体のディレクトリ診断（命名規則・重複・放置フォルダ・階層の深さ）と理想ツリー＋移動マッピング
2. グローバル CLAUDE.md とプロジェクト CLAUDE.md の重複・矛盾の解消案
3. MCP・プラグイン・output-styles・permissions のグローバル最適化案
4. 移動系の実行プラン（コピー → 検証 → 削除の順序を明記。承認なしに実行しない）
