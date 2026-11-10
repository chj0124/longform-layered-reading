#!/usr/bin/env python3
"""Estimate a marked main path and finalize renderer-neutral Markdown.

Markdown estimation requires main-reading-path:start/end comments in the work
file. HTML requires a data-main-reading-path container. Plain text is read in
full. The estimate never measures diagram comprehension or proves argument
completeness.

--finalize converts a Markdown work file into a delivery file by removing
internal markers and downgrading M/D fragment links to numbered text labels.
--check-delivered checks a finished Markdown file without requiring markers.
Fenced code blocks are never rewritten or treated as stray markup.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable

START = "<!-- main-reading-path:start -->"
END = "<!-- main-reading-path:end -->"
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
ANCHOR = re.compile(r"<a\s+id=[\"']([md]\d+)[\"']\s*></a>", re.I)
NAV_LINK = re.compile(r"\[([^]]+)\]\(#([md]\d+)\)", re.I)
FRAGMENT_LINK = re.compile(r"\]\(#[^)]+\)")
RAW_TAG = re.compile(r"</?[A-Za-z][^>]*>")


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


def process_outside_fences(text: str, transform: Callable[[str, int], str]) -> str:
    """Apply transform to non-fence lines, preserving fenced code verbatim."""
    output: list[str] = []
    fence_char: str | None = None
    fence_length = 0
    for line_number, line in enumerate(text.splitlines(keepends=True), 1):
        marker = re.match(r"^[ \t]{0,3}(`{3,}|~{3,})", line)
        if marker:
            output.append(line)
            token = marker.group(1)
            if fence_char is None:
                fence_char = token[0]
                fence_length = len(token)
            elif token[0] == fence_char and len(token) >= fence_length:
                fence_char = None
                fence_length = 0
            continue
        if fence_char is not None:
            output.append(line)
        else:
            output.append(transform(line, line_number))
    return "".join(output)


def delivery_errors(text: str) -> list[str]:
    """Find markup that is unsafe in the default renderer-neutral delivery."""
    errors: list[str] = []

    def check(line: str, line_number: int) -> str:
        if "<!--" in line or "-->" in line:
            errors.append(f"第 {line_number} 行：残留 HTML 注释或内部校验标记")
        if RAW_TAG.search(line):
            errors.append(f"第 {line_number} 行：残留未确认可渲染的原始 HTML 标签")
        if FRAGMENT_LINK.search(line):
            errors.append(f"第 {line_number} 行：残留未验证的页内链接")
        return line

    process_outside_fences(text, check)
    return errors


def finalize_markdown(text: str) -> tuple[str, dict[str, int]]:
    """Create delivery Markdown, failing rather than losing navigation targets."""
    stats = {"main_markers_removed": 0, "anchors_removed": 0, "navigation_labels_converted": 0}

    def convert(line: str, line_number: int) -> str:
        for marker, key in ((START, "main_markers_removed"), (END, "main_markers_removed")):
            count = line.count(marker)
            stats[key] += count
            line = line.replace(marker, "")
        if not line.strip():
            return ""

        line, anchor_count = ANCHOR.subn("", line)
        stats["anchors_removed"] += anchor_count

        def downgrade(match: re.Match[str]) -> str:
            label, target = match.group(1), match.group(2)
            if target.lower() not in label.lower():
                raise ValueError(
                    f"第 {line_number} 行：页内链接文字 {label!r} 未包含目标编号 {target}；"
                    "请先补入编号，避免转成文字导航后丢失目标"
                )
            stats["navigation_labels_converted"] += 1
            return f"**{label}**"

        return NAV_LINK.sub(downgrade, line)

    result = process_outside_fences(text, convert)
    errors = delivery_errors(result)
    if errors:
        raise ValueError("交付稿检查失败：\n" + "\n".join(errors))
    return result, stats


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
    parser = argparse.ArgumentParser(description="估算主阅读路径，并生成或检查阅读器中立的 Markdown 交付稿")
    parser.add_argument("path", type=Path)
    parser.add_argument("--cjk-per-minute", type=int, default=350)
    parser.add_argument("--latin-words-per-minute", type=int, default=180)
    parser.add_argument("--allow-short", action="store_true", help="短文允许低于 3 分钟")
    parser.add_argument("--enforce", action="store_true", help="超出预算时返回非零状态")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--finalize", type=Path, metavar="OUTPUT", help="从带标记的 Markdown 工作稿生成交付稿")
    parser.add_argument("--check-delivered", action="store_true", help="只检查 Markdown 交付稿，不做时长估算")
    args = parser.parse_args()

    if args.cjk_per_minute <= 0 or args.latin_words_per_minute <= 0:
        parser.error("阅读速度参数必须大于 0")
    if args.finalize and args.check_delivered:
        parser.error("--finalize 与 --check-delivered 不能同时使用")

    if args.check_delivered:
        try:
            if args.path.suffix.lower() != ".md":
                raise ValueError("--check-delivered 只支持 .md 文件")
            errors = delivery_errors(args.path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError) as exc:
            print(f"错误：{exc}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps({"delivery_check": "passed" if not errors else "failed", "errors": errors}, ensure_ascii=False, indent=2))
        elif errors:
            print("Markdown 交付检查：未通过\n" + "\n".join(errors))
        else:
            print("Markdown 交付检查：通过（无残留校验注释、原始 HTML 标签或未验证页内链接；围栏代码块未改动）")
        return 1 if errors else 0

    if args.finalize:
        if args.path.suffix.lower() != ".md" or args.finalize.suffix.lower() != ".md":
            parser.error("--finalize 的输入和输出都必须是 .md 文件")
        if args.path.resolve() == args.finalize.resolve():
            parser.error("交付稿不得覆盖带校验标记的工作稿")

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

    if args.enforce and (too_long or too_short):
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"主线文本估算：{minutes:.2f} 分钟；3—5 分钟文本预算：未通过")
        return 2

    if args.finalize:
        try:
            delivery, stats = finalize_markdown(args.path.read_text(encoding="utf-8"))
            args.finalize.parent.mkdir(parents=True, exist_ok=True)
            args.finalize.write_text(delivery, encoding="utf-8")
        except (OSError, UnicodeError, ValueError) as exc:
            print(f"错误：{exc}", file=sys.stderr)
            return 1
        result["delivery"] = {"path": str(args.finalize), "check": "passed", **stats}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"汉字：{result['cjk_characters']}；英文／数字词元：{result['latin_or_number_tokens']}")
        print(f"主线文本估算：{minutes:.2f} 分钟（非实测，不含图示理解成本）")
        print(f"3—5 分钟文本预算：{'通过' if result['within_budget'] else '未通过'}")
        if args.finalize:
            print(f"Markdown 交付稿：已生成并通过检查：{args.finalize}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
