---
name: docai-web2summary
description: Convert web pages to structured AI summaries. Automatically transforms URLs to Markdown via docai-web2md, then generates formatted summaries with core insights, technical details, performance metrics, and long-term impact analysis. Use when needing to quickly understand and extract key information from web content.
---

# docai:web2summary

## Overview

This skill combines **web conversion** and **AI summarization** to transform any web page into a structured, insightful summary:

1. **Conversion Phase**: Uses `docai-web2md` to convert URL → Markdown
   - Priority-based: Jina Reader → Firecrawl → Python fallback
   - Handles arXiv, blogs, social media, dynamic pages

2. **Summary Phase**: AI analyzes Markdown and generates structured output
   - Standardized format with specific sections
   - Focus on insights, not just repetition
   - Configurable AI models

**Core value**: Get deep understanding of web content in seconds, not minutes.

## When to Use This Skill

- **Research**: Quickly understand academic papers, technical articles
- **News**: Extract key points from tech news and blog posts
- **Learning**: Summarize documentation and tutorials
- **Analysis**: Process reports, whitepapers, case studies
- **Knowledge management**: Create structured notes from web sources

**When NOT to use:**
- Need raw Markdown (use `docai-web2md` instead)
- Only need metadata/titles
- Processing thousands of pages (consider batch tools)

## Quick Start

### Basic Usage

```bash
# Summarize any web page
python skills/docai-web2summary/tools/summarize.py https://mp.weixin.qq.com/s/XClh6xJmXoXbyBC9lKzPdA
```

### Advanced Options

```bash
# Use specific AI model
python skills/docai-web2summary/tools/summarize.py https://arxiv.org/abs/2601.04500v1 --model sonnet

# Save to file
python skills/docai-web2summary/tools/summarize.py https://www.breezedeus.com/article/ai-agent-context-engineering --output summary.md

# Use haiku for faster/cheaper summaries
python skills/docai-web2summary/tools/summarize.py https://example.com/blog/post --model haiku
```

## Output Format

All summaries follow this standardized structure:

```markdown
# **标题 | 机构名称**

✔ 一句话总结：体现网页类型和核心差异

✔ **核心洞见**：深度分析，非简单复述

✔ **技术细节/架构创新**：具体的技术实现

✔ **性能数据/实验结果**：具体数字和结果

✔ **应用场景**：实际使用场景

✔ **长期意义/游戏规则改变者**：深层影响分析

**原文：** <链接>
```

## Use Cases & Examples

### Academic Papers (arXiv)
```bash
python skills/docai-web2summary/tools/summarize.py https://arxiv.org/abs/2601.04500v1 --model sonnet
```
**Output focus**: Research contribution, methodology, results, impact

### Technical Blogs
```bash
python skills/docai-web2summary/tools/summarize.py https://www.breezedeus.com/article/ai-agent-context-engineering
```
**Output focus**: Key concepts, implementation details, practical applications

### News Articles
```bash
python skills/docai-web2summary/tools/summarize.py https://techcrunch.com/2024/...
```
**Output focus**: Main announcement, implications, market impact

### Product Documentation
```bash
python skills/docai-web2summary/tools/summarize.py https://docs.example.com/features --model haiku
```
**Output focus**: Core features, use cases, integration patterns

## Workflow Details

### Phase 1: Conversion (via docai-web2md)
```
Input URL
    ↓
arXiv? → HTML URL
    ↓
Jina Reader API (⭐ Zero install)
    ↓ (if fails)
Firecrawl API (needs key)
    ↓ (if fails)
Python implementation
    ↓
arXiv? → PDF download
    ↓
HTML parsing & cleaning
    ↓
Markdown output
```

### Phase 2: AI Summarization
```
Markdown Content
    ↓
Build structured prompt
    ↓
AI analysis (Claude)
    ↓
Extract key insights
    ↓
Format per template
    ↓
Structured summary
```

## Configuration Options

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `url` | ✅ | Web page URL to summarize | `https://example.com/article` |
| `--model` | ❌ | AI model (sonnet/haiku) | `sonnet` |
| `--output, -o` | ❌ | Save to file | `summary.md` |

## Performance & Limits

- **Conversion**: 1-10 seconds (depends on method)
- **AI Analysis**: 5-30 seconds (depends on length)
- **Total Time**: 10-60 seconds per URL
- **Content Limit**: ~50,000 characters after conversion
- **Timeout**: 180 seconds for AI phase

## Dependencies

This skill requires `docai-web2md`:

```bash
# Install from marketplace
/plugin install docai-web2summary

# Or install dependencies manually
cd docai-skills
uv sync
```

**Note**: `docai-web2md` will be automatically installed as a dependency.

## Integration & Extensions

### Works Well With
- **docai-web2md**: Use directly if you only need Markdown
- **Knowledge bases**: Feed summaries into vector databases
- **Research workflows**: Batch process multiple papers
- **Content pipelines**: Automated content curation

### Comparison: web2md vs web2summary

| Feature | web2md | web2summary |
|---------|--------|-------------|
| **Output** | Raw Markdown | Structured summary |
| **Use case** | Content extraction | Insight generation |
| **Processing** | Minimal | AI analysis |
| **Speed** | Fastest | Comprehensive |
| **Best for** | Archiving, editing | Understanding, learning |

## Troubleshooting

### Conversion Issues
- **Check URL accessibility**: Some sites block bots
- **Try Python fallback**: `--use-python` in web2md (indirectly)
- **Network issues**: Ensure internet connectivity

### Summary Issues
- **AI unavailable**: Skill falls back to manual prompt
- **Content too long**: Try shorter articles or specific sections
- **Format issues**: Check output template consistency

### Dependency Issues
```bash
# Verify installation
/plugin list | grep web2summary

# Reinstall if needed
/plugin install docai-web2summary
```

## Advanced Usage

### Python API
```python
from skills.docai_web2summary.tools.summarize import URLSummarizer

summarizer = URLSummarizer()
result = summarizer.summarize(
    url="https://example.com/article",
    model="sonnet",
    output="summary.md"
)
```

### Batch Processing (Manual)
```bash
# Create a simple script
for url in $(cat urls.txt); do
    python skills/docai-web2summary/tools/summarize.py "$url" --output "summaries/$(basename $url).md"
done
```

### Custom Prompts (Future)
Future versions may support:
- Custom summary templates
- Focus areas (technical, business, etc.)
- Output format variations
- Quality scoring

## Example Output

**Input**: `https://mp.weixin.qq.com/s/XClh6xJmXoXbyBC9lKzPdA`

**Output**:
```markdown
# **给Claude Code装个仪表盘：claude-hud插件深度评测**

✔ 这是一篇技术博客文章，详细介绍了一个能让Claude Code从"盲开"变透明的仪表盘插件...

✔ **核心洞见**：Claude Code最大的痛点不是功能不足，而是"黑盒"体验...

✔ **技术细节/架构创新**：基于Claude Code原生statusline API构建...

✔ **性能数据/实验结果**：Context可视化实时显示token占用率...

✔ **应用场景**：复杂任务重构、CI/CD调试、长期项目开发...

✔ **长期意义/游戏规则改变者**：标志着AI编程助手从"功能增强"向"体验优化"的重要转变...

**原文：** https://mp.weixin.qq.com/s/XClh6xJmXoXbyBC9lKzPdA
```

## Future Enhancements

- [ ] Batch URL summarization
- [ ] Custom summary templates
- [ ] Multi-model comparison
- [ ] Local file support
- [ ] Quality scoring
- [ ] Integration with note-taking apps

## Related Skills

- **docai-web2md**: For raw Markdown conversion
- **docai-ocr**: For image-based content
- **docai-pdf-extract**: For PDF-specific processing