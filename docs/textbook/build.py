"""parts/*.html を番号順に結合して soa-c03-textbook.html を生成し、簡易検査を行う。

使い方: python docs/textbook/build.py
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS = ROOT / "parts"
OUT = ROOT / "soa-c03-textbook.html"

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
# SVG の自己終了タグ（<path ... />）は HTMLParser では handle_startendtag で扱われる


class Checker(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "a" and a.get("href", "").startswith("#"):
            self.hrefs.append(a["href"][1:])
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"line {self.getpos()[0]}: 余分な </{tag}>")
            return
        open_tag, line = self.stack.pop()
        if open_tag != tag:
            self.errors.append(f"line {self.getpos()[0]}: </{tag}> が <{open_tag}>（line {line}）と対応しない")


def main() -> int:
    html = "".join(p.read_text(encoding="utf-8") for p in sorted(PARTS.glob("*.html")))
    OUT.write_text(html, encoding="utf-8", newline="\n")

    checker = Checker()
    checker.feed(html)
    problems = list(checker.errors)
    problems += [f"閉じられていない <{t}>（line {ln}）" for t, ln in checker.stack]

    dup = sorted({i for i in checker.ids if checker.ids.count(i) > 1})
    problems += [f"重複 id: {i}" for i in dup]

    ids = set(checker.ids)
    # JS 側で参照するアンカー（クイズとスキル一覧の r: / 第3要素）も検査する
    js_refs = re.findall(r'r: "([\w-]+)"', html) + re.findall(r'"(d[1-5]-[\w-]+)"\] *\]?', html)
    for ref in sorted(set(checker.hrefs + js_refs)):
        if ref and ref not in ids:
            problems.append(f"リンク先なし: #{ref}")

    print(f"wrote {OUT.relative_to(ROOT.parent.parent)} ({OUT.stat().st_size / 1024:.0f} KB)")
    for p in problems:
        print("NG:", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
