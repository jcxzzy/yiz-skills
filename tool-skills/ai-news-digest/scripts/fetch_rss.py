#!/usr/bin/env python3
"""
AI News Digest - RSS Feed Fetcher
抓取多个 AI/技术 RSS 源，解析并输出 JSON 格式的聚合内容
用法: python fetch_rss.py [--days N] [--sources SOURCES_FILE] [--output OUTPUT_FILE]
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

# ─────────────────────────────────────────────
# HTML 标签剥离
# ─────────────────────────────────────────────
class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []
    def handle_data(self, data):
        self._parts.append(data)
    def get_text(self):
        return " ".join(self._parts).strip()

def strip_html(html: str) -> str:
    s = _HTMLStripper()
    try:
        s.feed(html or "")
    except Exception:
        pass
    return s.get_text()


# ─────────────────────────────────────────────
# 日期解析
# ─────────────────────────────────────────────
def parse_date(date_str: str) -> datetime | None:
    """尝试解析各种 RSS 日期格式，返回 UTC aware datetime"""
    if not date_str:
        return None
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S GMT",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]
    date_str = date_str.strip()
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


# ─────────────────────────────────────────────
# RSS/Atom 解析
# ─────────────────────────────────────────────
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "media": "http://search.yahoo.com/mrss/",
}

def _text(element, *tags) -> str:
    """从 element 依次查找 tags，返回第一个非空文本"""
    for tag in tags:
        child = element.find(tag)
        if child is not None and child.text:
            return child.text.strip()
    return ""

def parse_feed(xml_bytes: bytes, source_name: str, source_url: str) -> list[dict]:
    """解析 RSS/Atom XML，返回文章列表"""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        print(f"  [WARN] XML parse error for {source_name}: {e}", file=sys.stderr)
        return []

    items = []

    # ── Atom feed ──
    if root.tag == "{http://www.w3.org/2005/Atom}feed" or "feed" in root.tag.lower():
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title = strip_html(_text(entry, "{http://www.w3.org/2005/Atom}title"))
            link_el = entry.find("{http://www.w3.org/2005/Atom}link")
            link = (link_el.get("href") or "") if link_el is not None else ""
            summary_el = entry.find("{http://www.w3.org/2005/Atom}summary") or \
                         entry.find("{http://www.w3.org/2005/Atom}content")
            summary = strip_html(summary_el.text if summary_el is not None else "")
            pub_el = entry.find("{http://www.w3.org/2005/Atom}published") or \
                     entry.find("{http://www.w3.org/2005/Atom}updated")
            pub_str = pub_el.text if pub_el is not None else ""
            if title and link:
                items.append({
                    "title": title,
                    "link": link,
                    "summary": summary[:500],
                    "pub_date": pub_str,
                    "source": source_name,
                    "source_url": source_url,
                })
        return items

    # ── RSS 1.0 / 2.0 ──
    channel = root.find("channel")
    if channel is None:
        channel = root  # RSS 1.0 items 可能在根节点下

    for item in channel.findall("item") or root.findall("item"):
        title = strip_html(_text(item, "title"))
        link = _text(item, "link", "guid")
        # description
        desc_el = item.find("description")
        content_el = item.find(f"{{{NS['content']}}}encoded")
        raw_desc = (content_el.text if content_el is not None else None) or \
                   (desc_el.text if desc_el is not None else "")
        summary = strip_html(raw_desc)
        # date
        pub_str = _text(item, "pubDate", f"{{{NS['dc']}}}date")
        if title and link:
            items.append({
                "title": title,
                "link": link,
                "summary": summary[:500],
                "pub_date": pub_str,
                "source": source_name,
                "source_url": source_url,
            })

    return items


# ─────────────────────────────────────────────
# 网络请求
# ─────────────────────────────────────────────
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AINewsDigest/1.0; +https://github.com)",
    "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml",
}

def fetch_feed(url: str, timeout: int = 15) -> bytes | None:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        print(f"  [WARN] HTTP {e.code} for {url}", file=sys.stderr)
    except urllib.error.URLError as e:
        print(f"  [WARN] URL error for {url}: {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"  [WARN] Error fetching {url}: {e}", file=sys.stderr)
    return None


# ─────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────
def load_sources(path: str) -> list[dict]:
    """加载 JSON 格式的 sources 文件"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run(days: int, sources: list[dict], output_file: str | None):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    all_articles = []
    errors = []

    for src in sources:
        name = src.get("name", "Unknown")
        url = src.get("url", "")
        category = src.get("category", "General")
        if not url:
            continue
        print(f"  Fetching [{category}] {name} ...", file=sys.stderr)
        raw = fetch_feed(url)
        if raw is None:
            errors.append({"source": name, "url": url})
            continue

        items = parse_feed(raw, name, url)
        for item in items:
            item["category"] = category
            dt = parse_date(item["pub_date"])
            item["parsed_date"] = dt.isoformat() if dt else None
            # 过滤日期
            if dt and dt < cutoff:
                continue
            all_articles.append(item)

    # 按日期排序（最新在前）
    def sort_key(a):
        return a["parsed_date"] or "0000"
    all_articles.sort(key=sort_key, reverse=True)

    result = {
        "fetch_time": datetime.now(timezone.utc).isoformat(),
        "days_window": days,
        "total_articles": len(all_articles),
        "failed_sources": errors,
        "articles": all_articles,
    }

    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"\n✅ Saved {len(all_articles)} articles to {output_file}", file=sys.stderr)
    else:
        print(output_json)


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI News RSS Fetcher")
    parser.add_argument("--days", type=int, default=3,
                        help="抓取最近 N 天的内容（默认 3）")
    parser.add_argument("--sources", type=str,
                        default=None,
                        help="JSON 格式的 RSS 源文件路径（默认使用内嵌源列表）")
    parser.add_argument("--output", type=str, default=None,
                        help="输出 JSON 文件路径（默认输出到 stdout）")
    args = parser.parse_args()

    if args.sources:
        sources = load_sources(args.sources)
    else:
        # 内嵌默认源（与 references/rss_sources.md 保持一致）
        sources = [
            # ── 大厂官方博客 ──
            {"name": "Google DeepMind",     "url": "https://deepmind.google/blog/rss.xml",                      "category": "Official"},
            {"name": "Microsoft AI Blog",   "url": "https://blogs.microsoft.com/ai/feed/",                      "category": "Official"},
            {"name": "Hugging Face Blog",   "url": "https://hf-mirror.com/blog/feed.xml",                      "category": "Community"},
            # ── 科技媒体 ──
            {"name": "TechCrunch AI",       "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "category": "Media"},
            {"name": "The Decoder",         "url": "https://the-decoder.com/feed/",                             "category": "Media"},
            {"name": "MIT Technology Review","url": "https://www.technologyreview.com/feed/",                    "category": "Media"},
            {"name": "Ars Technica AI",     "url": "https://feeds.arstechnica.com/arstechnica/technology-lab",  "category": "Media"},
            {"name": "MarkTechPost",        "url": "https://www.marktechpost.com/feed/",                        "category": "Media"},
            # ── 学术/研究 ──
            {"name": "Arxiv CS.AI",         "url": "https://arxiv.org/rss/cs.AI",                               "category": "Research"},
            {"name": "Arxiv CS.LG",         "url": "https://arxiv.org/rss/cs.LG",                               "category": "Research"},
            {"name": "Arxiv CS.CL",         "url": "https://arxiv.org/rss/cs.CL",                               "category": "Research"},
            {"name": "Papers With Code",    "url": "https://paperswithcode.com/latest.rss",                     "category": "Research"},
            # ── 开发者/社区 ──
            {"name": "Towards Data Science","url": "https://towardsdatascience.com/feed",                       "category": "Community"},
            {"name": "ML Mastery",          "url": "https://machinelearningmastery.com/feed/",                  "category": "Community"},
            {"name": "AI Alignment Forum",  "url": "https://www.alignmentforum.org/feed.xml",                   "category": "Community"},
            {"name": "LangChain Blog",      "url": "https://blog.langchain.dev/rss/",                           "category": "Community"},
            {"name": "Lilian Weng",         "url": "https://lilianweng.github.io/index.xml",                   "category": "Community"},
            # ── 中文 ──
            {"name": "机器之心",             "url": "https://www.jiqizhixin.com/rss",                            "category": "Chinese"},
            {"name": "量子位",               "url": "https://www.qbitai.com/feed",                               "category": "Chinese"},
            {"name": "InfoQ AI 中文",        "url": "https://www.infoq.cn/topic/35/feed",                        "category": "Chinese"},
        ]

    run(args.days, sources, args.output)

