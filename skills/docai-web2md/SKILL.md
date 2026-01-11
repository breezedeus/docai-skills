---
name: docai-web2md
description: Use when needing to convert web pages to Markdown format. Uses priority-based approach (Jina Reader → Firecrawl → Python) to handle static blogs, dynamic pages, social media, and arXiv papers.
---

# docai:web2md

## Overview
Converts web pages to Markdown with automatic priority-based method selection:
1. **Jina Reader API** (fastest, zero install) - except WeChat
2. **Firecrawl API** (advanced crawling)
3. **Python fallback** (when APIs unavailable)

**Special handling**: WeChat articles → Python directly (best results)

**Use when**: User says "convert to Markdown", "转成 Markdown", "网页转 Markdown"

## Quick Action (For Claude Code)
When user provides a URL to convert:
```bash
# Method 1: Jina Reader (recommended - no install)
curl https://r.jina.ai/<URL>

# Method 2: Python script (if Jina unavailable)
python skills/docai-web2md/tools/convert.py <URL>
```

## Prerequisites (Python Method Only)
```bash
# Option 1: uv (recommended)
uv pip install --system requests beautifulsoup4 markdownify pymupdf

# Option 2: pip
pip install requests beautifulsoup4 markdownify pymupdf
```

## Usage Examples
```bash
# Basic conversion
python skills/docai-web2md/tools/convert.py https://www.breezedeus.com/article/ai-agent-context-engineering

# Save to file
python skills/docai-web2md/tools/convert.py https://www.breezedeus.com/article/ai-agent-context-engineering -o article.md

# arXiv paper (auto HTML priority)
python skills/docai-web2md/tools/convert.py https://arxiv.org/abs/2601.04500v1

# Force Python method
python skills/docai-web2md/tools/convert.py <URL> --use-python
```

## Supported Platforms
- ✅ Static blogs & documentation (Jina/Python)
- ✅ React/Vue dynamic pages (Python)
- ✅ WeChat articles (微信公众号) - Python direct
- ✅ X.com / Twitter (Python)
- ✅ arXiv papers (HTML → PDF fallback)
- ✅ Medium/Substack (Python)

## Common Issues
- **Missing dependencies**: Install with `uv pip install --system requests beautifulsoup4 markdownify pymupdf`
- **arXiv PDF**: Requires `pymupdf` for PDF extraction
- **Dynamic pages**: May need Python method if Jina fails

## Related
- **docai-web2summary**: For AI-powered summaries (conversion + analysis)
