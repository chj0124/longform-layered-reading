#!/usr/bin/env python3
"""Validate the machine-checkable parts of a full-mode content map.

This checks the information table and coverage counts only. It cannot prove
that the delivered prose preserves or correctly attributes every source item.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ID_RE = re.compile(r"^S(\d{3})$")
NODE_RE = re.compile(r"^N\d{2}(?:\.\d+)?$")
MERGE_RE = re.compile(r"^合并→(S\d{3})$")
COUNT_LABELS = {
    "total": "原文信息单元总数",
    "kept": "已保留／改写数",
    "merged": "已合并且无信息损失数",
    "unread": "未读数",
    "unplaced": "未落位数",
}


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(line: str) -> bool:
    return bool(line.strip()) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells(line))


def find_information_table(lines: list[str]) -> tuple[list[str], list[dict[str, str]], list[str]]:
    errors: list[str] = []
    for index, line in enumerate(lines):
        header = cells(line)
        if "信息 ID" not in header or "主要输出节点" not in header:
            continue
        if index + 1 >= len(lines) or not is_separator(lines[index + 1]):
            return header, [], ["信息清单表头后缺少 Markdown 分隔行"]
        rows: list[dict[str, str]] = []
        for row_line in lines[index + 2 :]:
            if not row_line.strip().startswith("|"):
                break
            row = cells(row_line)
            if len(row) != len(header):
                errors.append(f"信息表列数不一致：{row_line.strip()}")
                continue
            rows.append(dict(zip(header, row)))
        return header, rows, errors
    return [], [], ["未找到包含「信息 ID」和「主要输出节点」的信息清单表"]


def coverage_counts(lines: list[str]) -> tuple[dict[str, int], list[str]]:
    values: dict[str, int] = {}
    errors: list[str] = []
    for key, label in COUNT_LABELS.items():
        matches = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(label + "："):
                matches.append(stripped.split("：", 1)[1].strip())
        if len(matches) != 1:
            errors.append(f"覆盖统计「{label}」应出现 1 次，实际为 {len(matches)} 次")
            continue
        if not re.fullmatch(r"\d+", matches[0]):
            errors.append(f"覆盖统计「{label}」必须是非负整数，实际为「{matches[0]}」")
            continue
        values[key] = int(matches[0])
    return values, errors


def validate(text: str) -> tuple[list[str], dict[str, int]]:
    lines = text.splitlines()
    header, rows, errors = find_information_table(lines)
    required = {"信息 ID", "主要输出节点", "交叉引用（可选）", "主线／细节", "处理方式"}
    missing = sorted(required - set(header))
    if missing:
        errors.append("信息清单缺少列：" + "、".join(missing))
        return errors, {}

    ids = [row.get("信息 ID", "") for row in rows]
    if not rows:
        errors.append("信息清单没有数据行")
    for row_number, source_id in enumerate(ids, start=1):
        if not ID_RE.fullmatch(source_id):
            errors.append(f"第 {row_number} 个信息 ID 格式错误：「{source_id}」，应为 S001 这类格式")
    duplicates = sorted(source_id for source_id, count in Counter(ids).items() if count > 1)
    if duplicates:
        errors.append("信息 ID 重复：" + "、".join(duplicates))
    for row_number, source_id in enumerate(ids, start=1):
        expected = f"S{row_number:03d}"
        if source_id != expected:
            errors.append(f"信息 ID 不连续：第 {row_number} 行应为 {expected}，实际为「{source_id}」")

    known_ids = set(ids)
    kept = 0
    merged = 0
    unplaced = 0
    for row_number, row in enumerate(rows, start=1):
        source_id = row.get("信息 ID", f"第 {row_number} 行")
        primary = row.get("主要输出节点", "")
        if not primary or primary in {"—", "-"}:
            unplaced += 1
            errors.append(f"{source_id} 缺少主要输出节点")
        elif not NODE_RE.fullmatch(primary):
            unplaced += 1
            errors.append(f"{source_id} 的主要输出节点必须只有一个 N01 或 N02.1 形式的节点，实际为「{primary}」")

        cross = row.get("交叉引用（可选）", "")
        if cross not in {"", "—", "-"}:
            for node in re.split(r"[、，,；;]\s*", cross):
                if not NODE_RE.fullmatch(node):
                    errors.append(f"{source_id} 的交叉引用格式错误：「{node}」")

        layer = row.get("主线／细节", "")
        if layer not in {"M", "D"}:
            errors.append(f"{source_id} 的主线／细节只能填 M 或 D，实际为「{layer}」")

        treatment = row.get("处理方式", "")
        if treatment in {"保留", "改写"}:
            kept += 1
        else:
            match = MERGE_RE.fullmatch(treatment)
            if not match:
                errors.append(f"{source_id} 的处理方式只能是保留、改写或合并→Sxxx，实际为「{treatment}」")
                continue
            merged += 1
            target = match.group(1)
            if target == source_id:
                errors.append(f"{source_id} 不能合并到自身")
            elif target not in known_ids:
                errors.append(f"{source_id} 的合并目标 {target} 不存在")

    counts, count_errors = coverage_counts(lines)
    errors.extend(count_errors)
    actual = {
        "total": len(rows),
        "kept": kept,
        "merged": merged,
        "unplaced": unplaced,
    }
    for key, expected in actual.items():
        if key in counts and counts[key] != expected:
            errors.append(f"覆盖统计「{COUNT_LABELS[key]}」为 {counts[key]}，按信息表应为 {expected}")
    if "unplaced" in counts and counts["unplaced"] != 0:
        errors.append("原文优化版的未落位数必须为 0")
    if {"total", "kept", "merged"} <= counts.keys() and counts["total"] != counts["kept"] + counts["merged"]:
        errors.append("原文信息单元总数必须等于已保留／改写数与已合并且无信息损失数之和")
    return errors, counts


def main() -> int:
    parser = argparse.ArgumentParser(description="校验完整档内容地图的信息清单与覆盖统计")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        text = args.path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1

    errors, counts = validate(text)
    if errors:
        for error in errors:
            print(f"错误：{error}", file=sys.stderr)
        print(f"内容地图结构校验：未通过（{len(errors)} 项）", file=sys.stderr)
        return 1
    print(
        "内容地图结构校验：通过；"
        f"信息单元 {counts['total']}，保留／改写 {counts['kept']}，"
        f"合并 {counts['merged']}，未读 {counts['unread']}，未落位 {counts['unplaced']}"
    )
    print("注意：本脚本不代替输出文本的双向回查与归属审计。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
