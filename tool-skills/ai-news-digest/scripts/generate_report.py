#!/usr/bin/env python3
"""
AI News Digest - Report Generator
从 fetch_rss.py 的 JSON 输出生成 Markdown 报告骨架，供 Claude 进一步润色。
用法: python generate_report.py [--input articles.json] [--output report.md]
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from collections import defaultdict

CATEGORY_LABELS = {
    "Official": "🏢 官方公告",
    "Media": "📰 科技媒体",
    "Research": "🔬 学术研究",
    "Community": "💡 开发者社区",
    "Chinese": "🇨🇳 中文资讯",
    "General": "📌 综合",
}


def format_date(iso_str: str | None) -> str:
    if not iso_str:
        return "日期未知"
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return iso_str


def truncate(text: str, max_chars: int = 200) -> str:
    text = " ".join(text.split())
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "…"


def build_report(data: dict) -> str:
    fetch_time = format_date(data.get("fetch_time"))
    days = data.get("days_window", 3)
    total = data.get("total_articles", 0)
    articles = data.get("articles", [])
    failed = data.get("failed_sources", [])

    # 按分类分组
    by_category: dict[str, list] = defaultdict(list)
    for art in articles:
        cat = art.get("category", "General")
        by_category[cat].append(art)

    lines = []

    # ── 标题 ──
    now_str = datetime.now(timezone.utc).strftime("%Y年%m月%d日")
    lines += [
        f"# AI 资讯日报 · {now_str}",
        "",
        f"> **数据窗口**：最近 {days} 天 &nbsp;|&nbsp; **抓取时间**：{fetch_time} &nbsp;|&nbsp; **总条目**：{total}",
        "",
        "---",
        "",
        "## 📋 执行摘要",
        "",
        "<!-- Claude: 请在此处根据下文内容撰写 3-5 句话的执行摘要，突出最重要的进展与趋势 -->",
        "",
        "---",
        "",
    ]

    # 定义分类顺序
    category_order = ["Official", "Research", "Media", "Community", "Chinese", "General"]

    for cat in category_order:
        if cat not in by_category:
            continue
        label = CATEGORY_LABELS.get(cat, cat)
        arts = by_category[cat]
        lines += [
            f"## {label}",
            "",
        ]
        for art in arts[:30]:  # 每类最多 30 条
            title = art.get("title", "（无标题）")
            link = art.get("link", "")
            source = art.get("source", "")
            pub = format_date(art.get("parsed_date"))
            summary = truncate(art.get("summary", ""), 250)

            lines.append(f"### [{title}]({link})")
            lines.append(f"**来源**: {source} &nbsp;|&nbsp; **时间**: {pub}")
            lines.append("")
            if summary:
                lines.append(f"> {summary}")
                lines.append("")
        lines += ["---", ""]

    # 失败源提示
    if failed:
        lines += [
            "## ⚠️ 获取失败的来源",
            "",
        ]
        for f in failed:
            lines.append(f"- {f['source']}: `{f['url']}`")
        lines += ["", "---", ""]

    # 趋势分析占位
    lines += [
        "## 📈 趋势分析",
        "",
        "<!-- Claude: 根据以上内容，分析本期最显著的 3-5 个技术趋势或行业动向 -->",
        "",
        "### 主要趋势",
        "",
        "1. <!-- 趋势 1 -->",
        "2. <!-- 趋势 2 -->",
        "3. <!-- 趋势 3 -->",
        "",
        "### 值得关注的研究方向",
        "",
        "<!-- 列出 2-3 个本期论文/研究中最有价值的方向 -->",
        "",
        "---",
        "",
        "## 🔭 展望",
        "",
        "<!-- Claude: 基于本期动态，对未来 1-2 周的发展做简短预测 -->",
        "",
        "---",
        "",
        f"*本报告由 AI News Digest 技能自动生成，数据来源于公开 RSS 订阅源。生成时间：{fetch_time}*",
    ]

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Markdown report from RSS JSON")
    parser.add_argument("--input", type=str, default=None,
                        help="fetch_rss.py 输出的 JSON 文件（默认从 stdin 读取）")
    parser.add_argument("--output", type=str, default=None,
                        help="输出 Markdown 文件路径（默认输出到 stdout）")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    report_md = build_report(data)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report_md)
        print(f"✅ Report saved to {args.output}", file=sys.stderr)
    else:
        print(report_md)

