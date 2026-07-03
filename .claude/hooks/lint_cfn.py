#!/usr/bin/env python3
"""PostToolUse(Write|Edit) hook: CloudFormation テンプレート保存時に cfn-lint を自動実行する。

iac.md「生成時は必ず cfn-lint をパスする」の強制版。
lint 失敗時は exit 2 で stderr を Claude に返し、その場で修正させる。
"""
import json
import re
import shutil
import subprocess
import sys


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    file_path = data.get("tool_input", {}).get("file_path", "")
    normalized = file_path.replace("\\", "/")
    if not re.search(r"iac/cloudformation/.+\.ya?ml$", normalized):
        sys.exit(0)

    if shutil.which("cfn-lint") is None:
        print(
            "cfn-lint が見つかりません。`pip install cfn-lint` を実行してから "
            "このテンプレートを lint してください（iac ルールで必須）。",
            file=sys.stderr,
        )
        sys.exit(2)

    result = subprocess.run(
        ["cfn-lint", file_path],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        print(
            f"cfn-lint FAILED: {file_path}\n{result.stdout}\n{result.stderr}\n"
            "上記の指摘を修正してください（iac ルールで cfn-lint パスは必須）。",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
