---
name: docai-web2summary
description: Use when needing to summarize web content. Runs summarize.py to convert URL to Markdown and generate AI summary with adaptive structure based on content type (paper, news, tutorial, product, AI news, general).
---

# docai:web2summary

## Overview
This skill automatically converts web pages to structured AI summaries:
1. **Converts URL → Markdown** using docai-web2md (parallel: Jina Reader / Firecrawl / Python)
2. **Detects content type** (paper, news, tutorial, product, AI news, general)
3. **Generates AI summary** with type-specific structure

**Use when**: User says "summarize this URL", "总结这个链接", "请总结这个文章"

## Quick Action (For Claude Code)
When user provides a URL to summarize:
```bash
# Run this command
python skills/docai-web2summary/tools/summarize.py <URL>

# With options
python skills/docai-web2summary/tools/summarize.py <URL> --model sonnet
python skills/docai-web2summary/tools/summarize.py <URL> --output summary.md
```

## Prerequisites
```bash
# Option 1: uv (recommended)
uv pip install --system requests beautifulsoup4 markdownify pymupdf

# Option 2: pip
pip install requests beautifulsoup4 markdownify pymupdf
```

## Output Format (Adaptive by Content Type)
```markdown
# **标题 | 机构名称**

✔ 一句话总结

（以下章节根据内容类型自动选择）

技术论文 → 核心洞见、技术细节、性能数据、应用场景、长期意义
新闻报道 → 核心事件、关键人物/机构、背景与影响、后续展望
教程指南 → 学习目标、前置条件、关键步骤、注意事项
产品评测 → 产品定位、核心功能、竞品对比、适用人群
AI 动态 → 核心动态、技术要点、行业影响、值得关注的信号
通用 → 核心内容、关键要点、价值与启发

**原文：** <链接>
```

## Examples
```bash
# Basic summary
python skills/docai-web2summary/tools/summarize.py https://arxiv.org/abs/2601.04500v1

# With specific model
python skills/docai-web2summary/tools/summarize.py https://www.breezedeus.com/article/ai-agent-context-engineering --model sonnet

# Save to file
python skills/docai-web2summary/tools/summarize.py https://mp.weixin.qq.com/s/... --output summary.md
```

## Common Issues
- **Missing dependencies**: Run `uv pip install --system requests beautifulsoup4 markdownify pymupdf`
- **AI unavailable**: Script provides manual prompt if claude command fails
- **Conversion fails**: Script auto-falls back to Python method

## Related
- **docai-web2md**: For raw Markdown only
- **docai-web2summary**: This skill (conversion + AI summary)