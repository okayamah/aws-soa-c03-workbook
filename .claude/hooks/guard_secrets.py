#!/usr/bin/env python3
"""PreToolUse(Bash) hook: シークレットらしきファイルの git add をブロックする。

aws-rules.md「シークレット・.env は絶対にコミットしない」の強制版。
exit 2 でツール実行をブロックし、stderr が Claude へのフィードバックになる。
"""
import json
import re
import sys


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if data.get("tool_name") != "Bash":
        sys.exit(0)

    cmd = data.get("tool_input", {}).get("command", "")
    if not re.search(r"\bgit\s+(add|stage)\b", cmd):
        sys.exit(0)

    # .env.example はコミット許可（.gitignore の !.env.example と対応）
    checked = cmd.replace(".env.example", "")

    banned = {
        r"\.env\b": ".env",
        r"\.pem\b": "*.pem",
        r"\.ppk\b": "*.ppk",
        r"(?<![\w.-])credentials(?![\w-])": "credentials",
        r"\.aws[/\\]": ".aws/",
    }
    for pattern, label in banned.items():
        if re.search(pattern, checked, re.IGNORECASE):
            print(
                f"BLOCKED: git add の対象にシークレットらしきパス（{label}）が含まれています。"
                "docs/guidelines/aws-rules.md のシークレット管理ルールに従い、"
                "対象ファイルを確認してから個別パス指定でやり直してください。",
                file=sys.stderr,
            )
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
