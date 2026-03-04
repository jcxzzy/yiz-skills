#!/usr/bin/env python3
"""读取 RSS 数据并输出结构化摘要供 Claude 分析"""
import json, sys, os, collections
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

data_file = os.path.join(os.environ.get('TEMP', '/tmp'), 'ai_today.json')
with open(data_file, encoding='utf-8') as f:
    data = json.load(f)

articles = data['articles']
by_cat = collections.defaultdict(list)
for a in articles:
    by_cat[a['category']].append(a)

print('=== 抓取统计 ===')
print(f'数据窗口: {data["days_window"]} 天')
print(f'抓取时间: {data["fetch_time"]}')
print(f'文章总数: {data["total_articles"]}')
for cat, arts in sorted(by_cat.items()):
    print(f'  {cat}: {len(arts)} 篇')
if data.get('failed_sources'):
    print(f'失败来源: {[s["source"] for s in data["failed_sources"]]}')

def clean(s):
    return s.encode('utf-8', errors='replace').decode('utf-8') if s else ''

def p(label, items, title_len=90, summary_len=200):
    print(f'\n{"="*60}')
    print(f'=== {label} ===')
    print(f'{"="*60}')
    for a in items:
        print(f'\n【{clean(a.get("source",""))}】 {clean(a["title"])[:title_len]}')
        print(f'链接: {a["link"]}')
        print(f'时间: {a.get("parsed_date","")[:16]}')
        if a.get('summary'):
            print(f'摘要: {clean(a["summary"])[:summary_len]}')

p('官方公告 (Official)', by_cat['Official'][:8])
p('学术研究 (Research)', by_cat['Research'][:25], summary_len=180)
p('科技媒体 (Media)', by_cat['Media'][:15])
p('开发者社区 (Community)', by_cat['Community'][:10])
p('中文资讯 (Chinese)', by_cat['Chinese'][:10], summary_len=200)


