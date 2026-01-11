---
name: docai-web2md
description: Convert web pages to Markdown format using priority-based approach (Jina Reader, Firecrawl, Python fallback). Supports arXiv HTML priority, WeChat articles, static blogs, and dynamic pages. Use when needing to convert web content for documentation, knowledge bases, or content archiving.
---

# docai:web2md

## Overview

This skill converts web pages to Markdown format using a **priority-based approach**:

1. **Jina Reader API** (highest priority) - Zero installation, one-line URL
2. **Firecrawl API** (secondary) - Powerful crawling with API key
3. **Python implementation** (fallback) - When API methods unavailable

**Core principle:** Use the simplest, fastest method first. Only fall back to Python when non-Python methods fail or aren't available.

**Real-world tested:**
- ✅ 微信公众号文章 (https://mp.weixin.qq.com/...) - 3395+ characters
- ✅ arXiv 论文 (优先HTML，回退PDF) (https://arxiv.org/abs/...) - 完整提取
- ✅ 静态博客/文档
- ✅ X.com/Twitter posts
- ✅ Medium/Substack articles

## When to Use

- Converting articles for knowledge bases or documentation
- Archiving web content in readable format
- Processing academic papers from arXiv
- Extracting content from social media
- Creating markdown from any web source

**When NOT to use:**
- Need structured data extraction (use specialized parsers)
- Only need page metadata (use simpler tools)
- Need to process thousands of pages (consider rate limits)

## Priority Methods (No Python Required)

### Method 1: Jina Reader API ⭐ Recommended

**Zero installation, works anywhere:**

```bash
# Simply prepend r.jina.ai/ to any URL
https://r.jina.ai/https://www.breezedeus.com/article/ai-agent-context-engineering

# Example:
curl https://r.jina.ai/https://www.breezedeus.com/article/ai-agent-context-engineering
```

**Browser access:**
Just visit `https://r.jina.ai/https://www.breezedeus.com/article/ai-agent-context-engineering` in browser - get clean Markdown instantly.

**Pros:**
- ✅ No installation needed
- ✅ Handles dynamic content (React, Vue, etc.)
- ✅ Clean, well-formatted output
- ✅ Free to use
- ✅ Works with any HTTP client

**Cons:**
- ❌ Requires internet connection
- ❌ Rate limits apply

### Method 2: Firecrawl API

**For advanced crawling and structured extraction:**

```bash
# Install CLI (non-Python)
curl -sSL https://get.firecrawl.dev | bash

# Basic usage
firecrawl scrape https://www.breezedeus.com/article/ai-agent-context-engineering --format markdown

# With API key
export FIRECRAWL_API_KEY=your_key
firecrawl scrape https://www.breezedeus.com/article/ai-agent-context-engineering --format markdown
```

**API usage:**
```bash
curl -X POST https://api.firecrawl.dev/v0/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.breezedeus.com/article/ai-agent-context-engineering", "formats": ["markdown"]}'
```

**Pros:**
- ✅ Handles complex crawling (multiple pages)
- ✅ Structured data extraction
- ✅ JavaScript rendering
- ✅ Batch processing support

**Cons:**
- ❌ Requires API key (free tier available)
- ❌ More complex setup

### Method 3: Browser Extensions

**For manual/one-off conversions:**

- **MarkDownload** (Firefox/Chrome) - One-click Markdown export
- **SingleFile** - Save complete page as HTML, then convert
- **Copy as Markdown** - Convert selected content

**Pros:**
- ✅ No coding required
- ✅ Works offline
- ✅ Good for occasional use

**Cons:**
- ❌ Manual operation
- ❌ Not automatable

### Method 4: Command-Line Tools

**For automation without Python:**

```bash
# pandoc (install from https://pandoc.org/)
curl https://www.breezedeus.com/article/ai-agent-context-engineering | pandoc -f html -t markdown

# lynx (text browser)
lynx -dump -nolist https://www.breezedeus.com/article/ai-agent-context-engineering > output.md

# w3m (text browser)
w3m -dump https://www.breezedeus.com/article/ai-agent-context-engineering > output.md
```

**Pros:**
- ✅ Fast, local processing
- ✅ No Python dependency
- ✅ Scriptable

**Cons:**
- ❌ Installation required
- ❌ May not handle dynamic content

## Python Fallback (When Above Methods Fail)

Use when:
- No internet connection
- Need custom processing
- API methods unavailable
- Need to process local files

### Quick Start

**Option A: Using uv (Recommended)**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize environment
cd docai-skills
uv sync

# Run script
uv run python skills/docai-web2md/tools/convert.py https://www.breezedeus.com/article/ai-agent-context-engineering
```

**Option B: Using pip**
```bash
# Install dependencies
pip install requests beautifulsoup4 markdownify pymupdf

# Run script
python skills/docai-web2md/tools/convert.py https://www.breezedeus.com/article/ai-agent-context-engineering
```

**Option C: For Claude Code Integration**
```bash
# Install to system Python (one-time setup)
uv pip install --system requests beautifulsoup4 markdownify pymupdf
# or
pip install requests beautifulsoup4 markdownify pymupdf
```

### Usage

```bash
# Basic conversion (with uv)
uv run python skills/docai-web2md/tools/convert.py https://www.breezedeus.com/article/ai-agent-context-engineering

# Save to file
uv run python skills/docai-web2md/tools/convert.py https://www.breezedeus.com/article/ai-agent-context-engineering -o article.md

# arXiv paper
uv run python skills/docai-web2md/tools/convert.py https://arxiv.org/abs/2601.04500v1
```

### Python API

```python
from skills.docai_web2md.tools.convert import WebToMarkdown

converter = WebToMarkdown()

# Auto-detects best method
markdown = converter.convert("https://www.breezedeus.com/article/ai-agent-context-engineering")

# Force Python method
markdown = converter.convert("https://www.breezedeus.com/article/ai-agent-context-engineering", use_python=True)
```

## Decision Flowchart

```
Need to convert URL to Markdown?
│
├─ Is it arXiv? (arxiv.org)
│  └─ YES → Convert to HTML URL first
│
├─ Can use Jina Reader? (internet available)
│  └─ YES → Use https://r.jina.ai/URL
│
├─ Have Firecrawl API key?
│  └─ YES → Use Firecrawl API
│
├─ Can install browser extension?
│  └─ YES → Use MarkDownload/SingleFile
│
├─ Have CLI tools (pandoc/lynx)?
│  └─ YES → Use command-line
│
└─ NO → Use Python implementation
    └─ arXiv HTML? → Download PDF and extract
```

## Claude Code Integration

After installing to `~/.claude/skills/`:

```
User: "帮我把 https://www.breezedeus.com/article/ai-agent-context-engineering 转换成 Markdown"

Claude: (uses this skill)
1. Checks if Jina Reader is available
2. If yes, uses https://r.jina.ai/https://www.breezedeus.com/article/ai-agent-context-engineering
3. If no, falls back to Python implementation
4. Returns clean Markdown
```

## Comparison Table

| Method | Installation | Speed | Dynamic Content | Automation | Best For |
|--------|--------------|-------|-----------------|------------|----------|
| Jina Reader | None | Fast | ✅ Yes | ✅ Yes | Quick conversion |
| Firecrawl | API key | Medium | ✅ Yes | ✅ Yes | Complex crawling |
| Browser Extension | One-click | Fast | ✅ Yes | ❌ No | Manual use |
| CLI Tools | Required | Fast | ❌ Limited | ✅ Yes | Local processing |
| Python | Required | Medium | ✅ Yes | ✅ Yes | Custom needs |

**arXiv Special Handling:**
- Priority: HTML URL → Jina Reader → PDF fallback
- Example: `https://arxiv.org/abs/2601.04500v1` → `https://arxiv.org/html/2601.04500v1` → Jina

## Common Mistakes

### ❌ Using Python when Jina Reader works
```bash
# Wrong (overkill)
python convert.py https://www.breezedeus.com/article/ai-agent-context-engineering

# Right (simple)
curl https://r.jina.ai/https://www.breezedeus.com/article/ai-agent-context-engineering
```

### ❌ Not using arXiv HTML priority
```python
# Wrong - goes directly to PDF
url = "https://arxiv.org/pdf/2601.04500v1.pdf"

# Right - HTML first, PDF fallback
url = "https://arxiv.org/abs/2601.04500v1"
# Skill auto-converts to: https://arxiv.org/html/2601.04500v1
# Then falls back to PDF if needed
```

### ❌ Forgetting PyMuPDF for PDF extraction
```bash
# Wrong
python convert.py https://arxiv.org/abs/2601.04500v1
# Error: PDF processing requires PyMuPDF

# Right
pip install pymupdf
python convert.py https://arxiv.org/abs/2601.04500v1
```

## Testing

Test URLs:

1. **Jina Reader**: `https://r.jina.ai/https://www.breezedeus.com/article/ai-agent-context-engineering`
2. **Static**: `https://www.breezedeus.com/article/ai-agent-context-engineering`
3. **arXiv**: `https://arxiv.org/abs/2601.04500v1`
4. **WeChat**: `https://mp.weixin.qq.com/s/1LfkYdbzymoWxdvdnKeLnA`

Expected: Clean Markdown with headings, paragraphs, lists preserved.

## Performance

- **Jina Reader**: ~1-2 seconds (API call)
- **Firecrawl**: ~2-5 seconds (API call)
- **Python static**: ~1-2 seconds
- **Python dynamic**: ~5-10 seconds
- **arXiv HTML**: ~1-2 seconds (via Jina)
- **arXiv PDF**: ~2-5 seconds (Python fallback)

## Future Enhancements

- [ ] CLI tool for marketplace management
- [ ] GitHub integration for skill discovery
- [ ] More non-Python methods
- [ ] Batch processing support
- [ ] arXiv HTML version detection (auto-fallback if no HTML)
