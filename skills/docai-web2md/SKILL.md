---
name: docai-web2md
description: Convert any web URL to Markdown. Triggers on "转成Markdown/转换/网页转Markdown/convert to Markdown + URL". Handles static sites, dynamic SPAs, WeChat, arXiv, Twitter/X.
---

# docai:web2md

## When to Trigger
User wants to convert a web page to Markdown. Common patterns:
- "把这个链接转成 Markdown"、"网页转 Markdown"、"提取网页内容"
- "convert this URL to Markdown"、"get the content of this page"
- Any URL + intent to extract/read content (without summarization)

If user wants summary, use docai-web2summary instead.

## How to Execute
```bash
python skills/docai-web2md/tools/convert.py <URL> [--use-python] [-o <file>]
```

### Parameters
| Parameter | Required | Description |
|-----------|----------|-------------|
| `url` | Yes | Web page URL |
| `--use-python` | No | Force Python method (skip Jina/Firecrawl) |
| `-o` / `--output` | No | Save to file instead of stdout |

### Examples
```bash
# Basic conversion (parallel: Jina / Firecrawl / Python)
python skills/docai-web2md/tools/convert.py https://example.com/article

# arXiv paper (auto HTML priority, PDF fallback)
python skills/docai-web2md/tools/convert.py https://arxiv.org/abs/2601.04500v1

# Save to file
python skills/docai-web2md/tools/convert.py https://mp.weixin.qq.com/s/... -o article.md

# Force Python method
python skills/docai-web2md/tools/convert.py https://example.com --use-python
```

## What It Does
Three methods run in parallel, returning the first successful result:
1. Jina Reader API (fastest, zero install)
2. Firecrawl API (if key configured)
3. Python fallback (requests + BeautifulSoup + Playwright for SPAs)

Special cases handled automatically: WeChat → Python direct, arXiv → HTML priority, Twitter/X → Playwright.

## Troubleshooting
- **arXiv PDF garbled**: Requires `pymupdf` — `pip install pymupdf`
- **Dynamic page empty**: Script auto-detects SPAs and uses Playwright
- **All methods fail**: Try `--use-python` to bypass API methods
