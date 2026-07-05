#!/usr/bin/env python3
"""PreToolUse(Bash) hook: aws CLI のリージョンを ap-northeast-1 に強制する。

aws-rules.md「リージョンは ap-northeast-1 固定」の強制版。
グローバル系サービス（CloudFront 用 ACM 等）は us-east-1 を許可する。
"""
import json
import re
import sys

ALLOWED_REGION = "ap-northeast-1"

# us-east-1 の指定を許可するサービス（グローバル/バージニア固定のもの）
GLOBAL_SERVICES = {
    "acm",            # CloudFront 用証明書は us-east-1 必須
    "budgets",
    "ce",             # Cost Explorer
    "cloudfront",
    "iam",
    "organizations",
    "route53",
    "sts",
    "wafv2",          # CLOUDFRONT スコープ
}


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if data.get("tool_name") != "Bash":
        sys.exit(0)

    cmd = data.get("tool_input", {}).get("command", "")
    if not re.search(r"\baws\s", cmd):
        sys.exit(0)

    service_match = re.search(r"\baws\s+([a-z0-9-]+)", cmd)
    service = service_match.group(1) if service_match else ""

    for region in re.findall(r"--region[=\s]+([a-z0-9-]+)", cmd):
        if region == ALLOWED_REGION:
            continue
        if region == "us-east-1" and service in GLOBAL_SERVICES:
            continue
        print(
            f"BLOCKED: --region {region} が指定されています。"
            f"本プロジェクトは {ALLOWED_REGION} 固定です（docs/guidelines/aws-rules.md）。"
            "グローバル系サービス（ACM for CloudFront / CE / IAM 等）のみ us-east-1 を許可しています。",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
