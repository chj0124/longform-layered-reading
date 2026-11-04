#!/usr/bin/env python3
"""Estimate text-only reading time for a marked main reading path.

Markdown requires main-reading-path:start/end comments. HTML requires a
data-main-reading-path container. Plain text is read in full. The estimate
never measures diagram comprehension or proves argument completeness.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

START = "<!-- main-reading-path:start -->"
END = "<!-- main-reading-path:end -->"
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class MainPathParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.capture_depth = 0
        self.suppress_depth = 0
        self.found = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        if tag in VOID_TAGS:
            if self.capture_depth and not self.suppress_depth and tag == "br":
                self.parts.append(" ")
            return

        self.stack.append(tag)
        if self.capture_depth:
            self.capture_depth += 1
            if self.suppress_depth:
                self.suppress_depth += 1
            elif tag in {"script", "style"} or (tag == "details" and "open" not in attrs):
                self.suppress_depth = 1
        elif "data-main-reading-path" in attrs:
            self.found = True
            self.capture_depth = 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.capture_depth and not self.suppress_depth:
            self.parts.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            return
        # Test documents are expected to be well formed. Recover to the matching
        # tag instead of crashing on a minor HTML nesting error.
        if tag not in self.stack:
            return
        while self.stack:
            current = self.stack.pop()
            if self.capture_depth:
                if self.suppress_depth:
                    self.suppress_depth -= 1
                self.capture_depth -= 1
            if current == tag:
                break

    def handle_data(self, data: str) -> None:
        if self.capture_depth and not self.suppress_depth:
            self.parts.append(data)


def extract(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix in {".html", ".htm"}:
        parser = MainPathParser()
        parser.feed(raw)
        parser.close()
        if not parser.found:
            raise ValueError("HTML 未找到 data-main-reading-path 容器")
        return " ".join(parser.parts)
    if suffix == ".md":
        has_start, has_end = START in raw, END in raw
        if has_start != has_end:
            raise ValueError("Markdown 主线起止标记不成对")
        if not has_start:
            raise ValueError("Markdown 未找到 main-reading-path 起止标记")
        return raw.split(START, 1)[1].split(END, 1)[0]
    return raw


def visible_text(markup: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", markup, flags=re.S)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"^[#>*+\-\s]+", "", text, flags=re.M)
    return re.sub(r"\s+", " ", text).strip()


def estimate(text: str, cjk_rate: int, latin_rate: int) -> dict[str, float | int]:
    cjk = len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]", text))
    latin = len(re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+(?:[.,:/%-]\d+)*", text))
    minutes = cjk / cjk_rate + latin / latin_rate
    return {"cjk_characters": cjk, "latin_or_number_tokens": latin, "estimated_minutes": round(minutes, 2)}


def main() -> int:
    parser = argparse.ArgumentParser(description="估算主阅读路径的文本阅读时间（非实测）")
    parser.add_argument("path", type=Path)
    parser.add_argument("--cjk-per-minute", type=int, default=350)
    parser.add_argument("--latin-words-per-minute", type=int, default=180)
    parser.add_argument("--allow-short", action="store_true", help="短文允许低于 3 分钟")
    parser.add_argument("--enforce", action="store_true", help="超出预算时返回非零状态")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.cjk_per_minute <= 0 or args.latin_words_per_minute <= 0:
        parser.error("阅读速度参数必须大于 0")

    try:
        text = visible_text(extract(args.path))
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1

    result = estimate(text, args.cjk_per_minute, args.latin_words_per_minute)
    minutes = float(result["estimated_minutes"])
    too_long = minutes > 5
    too_short = minutes < 3 and not args.allow_short
    result.update({
        "method": "text_only_estimate_not_measured",
        "cjk_per_minute": args.cjk_per_minute,
        "latin_words_per_minute": args.latin_words_per_minute,
        "within_budget": not too_long and not too_short,
    })

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"汉字：{result['cjk_characters']}；英文／数字词元：{result['latin_or_number_tokens']}")
        print(f"主线文本估算：{minutes:.2f} 分钟（非实测，不含图示理解成本）")
        print(f"3—5 分钟文本预算：{'通过' if result['within_budget'] else '未通过'}")

    if args.enforce and (too_long or too_short):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
