---
name: docai-web2summary
description: Use when needing to summarize web content. Runs summarize.py to convert URL to Markdown and generate structured AI summary with core insights, technical details, and performance metrics.
---

# docai:web2summary

## Overview
This skill automatically converts web pages to structured AI summaries:
1. **Converts URL → Markdown** using docai-web2md (Jina Reader → Firecrawl → Python)
2. **Generates AI summary** with standardized format

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

## Output Format
```markdown
# **标题 | 机构名称**

✔ 一句话总结

✔ **核心洞见**：深度分析

✔ **技术细节/架构创新**：具体实现

✔ **性能数据/实验结果**：具体数字

✔ **应用场景**：实际使用

✔ **长期意义/游戏规则改变者**：深层影响

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