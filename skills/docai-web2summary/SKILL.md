---
name: docai-web2summary
description: Summarize any web URL. Triggers on "summarize/总结/概括/摘要 + URL". Auto-detects content type (paper, news, tutorial, product, AI news) and generates adaptive structured summary.
---

# docai:web2summary

## When to Trigger
User wants to summarize a web page. Common patterns:
- "总结这个链接"、"帮我总结一下"、"概括这篇文章"、"给个摘要"
- "summarize this URL"、"give me a summary of"
- Any URL + intent to understand/extract key points

## How to Execute
```bash
# The script is relative to this skill's directory
python skills/docai-web2summary/tools/summarize.py <URL> [--model <model>] [--output <file>]
```

### Parameters
| Parameter | Required | Description |
|-----------|----------|-------------|
| `url` | Yes | Web page URL |
| `--model` | No | AI model (sonnet, haiku, etc.) |
| `--output` | No | Save to file instead of stdout |

### Examples
```bash
# arXiv paper
python skills/docai-web2summary/tools/summarize.py https://arxiv.org/abs/2601.04500v1

# WeChat article, save to file
python skills/docai-web2summary/tools/summarize.py https://mp.weixin.qq.com/s/... -o summary.md

# Blog post with specific model
python skills/docai-web2summary/tools/summarize.py https://example.com/post --model sonnet
```

## What It Does
1. Converts URL → Markdown (parallel: Jina / Firecrawl / Python)
2. AI auto-detects content type and applies matching summary structure
3. Returns formatted Markdown summary

## Troubleshooting
- **AI unavailable**: Falls back to outputting the prompt for manual use
- **Conversion fails**: Auto-retries with Python fallback method
