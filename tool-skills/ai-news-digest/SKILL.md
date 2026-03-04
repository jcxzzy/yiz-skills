---
name: ai-news-digest
description: 通过抓取大量 AI/技术领域 RSS 订阅源，聚合整理最新 AI 资讯、技术趋势、学术研究和行业动态，输出一份结构完整、观点深刻的中文 AI 资讯报告。当用户要求 AI 资讯摘要、AI 日报、AI 趋势报告、抓取 RSS 总结 AI 新闻、最新 AI 进展或类似需求时触发。
---

# AI 资讯日报技能

本技能通过运行 Python 脚本抓取多个 AI RSS 源，生成结构化报告骨架，再由 Claude 进行分析润色，最终输出完整的 AI 资讯报告。

## 快速工作流

```
Step 1: python scripts/fetch_rss.py --days 3 --output articles.json
Step 2: python scripts/generate_report.py --input articles.json --output report.md
Step 3: Claude 读取 report.md，补全分析，输出最终报告
```

## Step 1：抓取 RSS 数据

```bash
python scripts/fetch_rss.py --days 3 --output articles.json
```

**参数说明：**
- `--days N`：抓取最近 N 天（默认 3，周报用 7）
- `--sources my_sources.json`：使用自定义源列表（可选）
- `--output articles.json`：将结果存入文件

默认涵盖 25+ 个源，覆盖官方博客（OpenAI/DeepMind/Meta/Anthropic）、科技媒体（VentureBeat/TechCrunch/MIT TR）、学术预印本（Arxiv cs.AI/cs.LG/cs.CL）、开发者社区及中文媒体（机器之心/量子位）。完整源列表见 `references/rss_sources.md`。

部分源因网络限制可能失败，脚本会跳过并记录在 `failed_sources` 字段中，不影响整体运行。

## Step 2：生成报告骨架

```bash
python scripts/generate_report.py --input articles.json --output report.md
```

或一步管道完成：

```bash
python scripts/fetch_rss.py --days 3 | python scripts/generate_report.py --output report.md
```

## Step 3：Claude 分析与润色

读取 `report.md` 后，按以下结构补全内容（报告模板见 `assets/report_template.md`）：

| 章节 | 内容要求 |
|------|----------|
| 执行摘要 | 3-5 句话，提炼最重要的 2-3 个进展和核心趋势 |
| 重大突破与核心发布 | 从所有分类中筛出最重要的 5-10 条，加编辑观点 |
| 官方公告 | 列出大厂动态，注明影响面 |
| 学术研究亮点 | 精选 3-5 篇有价值论文，说明创新点 |
| 行业动态 | 媒体报道中的商业/政策/产品动向 |
| 开发者社区 | 值得关注的开源项目、工具、教程 |
| 中文资讯精选 | 国内 AI 生态重要动态 |
| 趋势分析 | 归纳 3-5 个技术/商业趋势，给出判断依据 |
| 展望 | 未来 1-2 周值得关注的事项 |

**写作规范：**
- 语言：中文为主，专有名词保留英文（如 GPT-4o、LoRA）
- 编辑观点标注格式：`> 编辑点评：...`
- 重要程度标记：重大进展 / 值得关注 / 常规更新
- 每类最多精选 5-8 条，宁少勿滥
- 趋势分析基于本期实际内容推断，不捏造

## 典型使用示例

- **日报**：`--days 3`
- **周报**：`--days 7`
- **只看论文**：只展开 Research 分类
- **自定义源**：`--sources my_sources.json`（格式见 `references/rss_sources.md`）

## 输出文件

- `articles.json`：原始抓取数据，含全部文章元数据
- `report.md`：最终 Markdown 报告，可直接分享或发布

## 参考资料

- **RSS 源完整列表**：`references/rss_sources.md`（含自定义源 JSON 格式说明）
- **报告模板**：`assets/report_template.md`（章节结构参考）

## 依赖

Python 标准库（无需安装第三方包）：`urllib`、`xml.etree.ElementTree`、`json`、`html.parser`
Python 版本要求：**3.10+**
