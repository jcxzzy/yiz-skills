# AI 资讯 RSS 订阅源清单

> 本文件列出 ai-news-digest 技能所有支持的 RSS 源，按分类整理。
> `fetch_rss.py` 脚本内已内嵌默认源列表；如需自定义，可将下列内容保存为 JSON 文件并通过 `--sources` 参数传入。

## 目录
- [官方博客（Official）](#官方博客)
- [科技媒体（Media）](#科技媒体)
- [学术研究（Research）](#学术研究)
- [开发者社区（Community）](#开发者社区)
- [中文资讯（Chinese）](#中文资讯)
- [自定义源 JSON 格式](#自定义源-json-格式)

---

## 官方博客

| 名称 | RSS URL | 说明 |
|------|---------|------|
| OpenAI Blog | `https://openai.com/blog/rss/` | GPT、Sora、o系列模型最新发布 |
| Google DeepMind | `https://deepmind.google/blog/rss.xml` | Gemini、AlphaFold 等研究 |
| Google AI Blog | `https://blog.google/technology/ai/rss/` | Google 产品与 AI 功能 |
| Meta AI | `https://ai.meta.com/blog/rss/` | LLaMA、PyTorch 等开源动态 |
| Microsoft AI Blog | `https://blogs.microsoft.com/ai/feed/` | Azure AI、Copilot 产品 |
| Anthropic Blog | `https://www.anthropic.com/rss.xml` | Claude 系列模型与安全研究 |
| Hugging Face Blog | `https://huggingface.co/blog/feed.xml` | 开源模型、数据集、Spaces |
| NVIDIA AI Blog | `https://blogs.nvidia.com/blog/category/deep-learning/feed/` | GPU 与 AI 基础设施 |
| AWS ML Blog | `https://aws.amazon.com/blogs/machine-learning/feed/` | AWS AI/ML 服务 |

## 科技媒体

| 名称 | RSS URL | 说明 |
|------|---------|------|
| VentureBeat AI | `https://venturebeat.com/category/ai/feed/` | AI 商业与产品新闻 |
| TechCrunch AI | `https://techcrunch.com/category/artificial-intelligence/feed/` | 初创公司与融资动态 |
| The Decoder | `https://the-decoder.com/feed/` | 深度 AI 分析报道 |
| MIT Technology Review | `https://www.technologyreview.com/feed/` | 技术深度报道 |
| Wired AI | `https://www.wired.com/feed/tag/artificial-intelligence/rss` | AI 社会影响分析 |
| The Verge AI | `https://www.theverge.com/ai-artificial-intelligence/rss/index.xml` | 消费级 AI 产品 |
| Ars Technica | `https://feeds.arstechnica.com/arstechnica/technology-lab` | 技术深度评测 |
| MarkTechPost | `https://www.marktechpost.com/feed/` | 论文解读与行业资讯 |
| InfoQ AI | `https://feed.infoq.com/` | 开发者视角的 AI 技术 |
| ZDNet AI | `https://www.zdnet.com/topic/artificial-intelligence/rss.xml` | 企业 AI 应用 |

## 学术研究

| 名称 | RSS URL | 说明 |
|------|---------|------|
| Arxiv cs.AI | `https://arxiv.org/rss/cs.AI` | 人工智能最新论文 |
| Arxiv cs.LG | `https://arxiv.org/rss/cs.LG` | 机器学习最新论文 |
| Arxiv cs.CL | `https://arxiv.org/rss/cs.CL` | 自然语言处理最新论文 |
| Arxiv cs.CV | `https://arxiv.org/rss/cs.CV` | 计算机视觉最新论文 |
| Papers With Code | `https://paperswithcode.com/latest.rss` | 带代码实现的最新论文 |
| Semantic Scholar | `https://www.semanticscholar.org/feed` | 引用量高的 AI 研究 |

## 开发者社区

| 名称 | RSS URL | 说明 |
|------|---------|------|
| Towards Data Science | `https://towardsdatascience.com/feed` | 数据科学与 ML 教程 |
| ML Mastery | `https://machinelearningmastery.com/feed/` | 机器学习实践教程 |
| AI Alignment Forum | `https://www.alignmentforum.org/feed.xml` | AI 安全与对齐研究 |
| LessWrong | `https://www.lesswrong.com/feed.xml` | AI 理性与安全讨论 |
| Fast.ai Blog | `https://www.fast.ai/index.xml` | 深度学习实践 |
| Sebastian Ruder | `https://ruder.io/rss/` | NLP 进展跟踪 |
| Lilian Weng (OpenAI) | `https://lilianweng.github.io/index.xml` | 技术深度博文 |

## 中文资讯

| 名称 | RSS URL | 说明 |
|------|---------|------|
| 机器之心 | `https://www.jiqizhixin.com/rss` | 国内领先 AI 媒体 |
| 量子位 | `https://www.qbitai.com/feed` | AI 产品与研究报道 |
| AI科技评论 | `https://www.atyun.com/feed` | AI 技术评测 |
| 新智元 | `https://feeds.feedburner.com/aivideo` | AI 产业资讯 |

---

## 自定义源 JSON 格式

如需向 `fetch_rss.py` 传入自定义源，将以下格式保存为 `my_sources.json`：

```json
[
  {
    "name": "My Blog",
    "url": "https://example.com/feed.xml",
    "category": "Custom"
  }
]
```

支持的 `category` 值：`Official`、`Media`、`Research`、`Community`、`Chinese`、`General`（或任意自定义值）。

运行示例：

```bash
python fetch_rss.py --days 7 --sources my_sources.json --output articles.json
python generate_report.py --input articles.json --output report.md
```

