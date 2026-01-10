---
name: docai-convert2md
description: Use when needing to convert web pages to Markdown format, especially for dynamic content like React apps, social media posts, or academic papers
---

# docai:convert2md

## Overview

This skill helps you convert web page content to Markdown format. It handles static pages, dynamic JavaScript-rendered content, and specialized sources like arXiv papers and social media posts.

**Core principle:** Use the simplest method that works, but always get complete content - even from JavaScript-rendered pages.

**Real-world tested:**
- ✅ 微信公众号文章 (https://mp.weixin.qq.com/...) - 3395+ characters
- ✅ arXiv 论文 PDF extraction (https://arxiv.org/abs/...) - 1778+ lines with title
- ✅ 静态博客/文档
- ✅ X.com/Twitter posts (with browser)
- ✅ Medium/Substack articles

**PDF Support:** Uses PyMuPDF for arXiv papers - extracts title from metadata and full text with page markers.

## When to Use

- Converting articles for knowledge bases or documentation
- Archiving web content in readable format
- Processing academic papers from arXiv
- Extracting content from social media (X.com, WeChat)
- Creating markdown from any web source

**When NOT to use:**
- Need structured data extraction (use specialized parsers)
- Only need page metadata (use simpler tools)
- Batch processing thousands of pages (consider rate limits)

## How to Use This Skill

### Option 1: Use the Pre-built Tool (Recommended)

The `tools/convert.py` script handles everything for you:

```bash
# Install dependencies
pip install requests beautifulsoup4 markdownify

# Optional: For dynamic pages
pip install playwright
playwright install chromium

# Optional: For arXiv PDF extraction
pip install pymupdf

# Use the tool
python skills/docai-convert2md/tools/convert.py https://example.com

# Save to file
python skills/docai-convert2md/tools/convert.py https://example.com -o article.md

# Pure text mode
python skills/docai-convert2md/tools/convert.py https://example.com --pure-text

# Force browser for dynamic content
python skills/docai-convert2md/tools/convert.py https://x.com/... --use-browser
```

### Option 2: Use Python Directly

```python
from skills.docai_convert2md.tools.convert import WebToMarkdown

converter = WebToMarkdown()

# Basic conversion
markdown = converter.convert("https://example.com")

# With options
markdown = converter.convert(
    "https://arxiv.org/abs/2401.12345",
    pure_text=False,
    use_browser=None  # Auto-detect
)
```

### Option 3: Manual Commands (For Understanding)

**For static pages**:
```bash
python3 -c "
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

url = 'YOUR_URL_HERE'
response = requests.get(url, timeout=30)
soup = BeautifulSoup(response.text, 'html.parser')

for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
    tag.decompose()

print(md(str(soup)))
"
```

**For dynamic pages**:
```bash
python3 -c "
from playwright.sync_api import sync_playwright
from markdownify import markdownify as md
from bs4 import BeautifulSoup

url = 'YOUR_URL_HERE'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url, wait_until='networkidle')
    page.wait_for_timeout(2000)
    html = page.content()
    browser.close()

soup = BeautifulSoup(html, 'html.parser')
for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
    tag.decompose()

print(md(str(soup)))
"
```

**For arXiv papers**:
```bash
# Convert abstract to PDF URL
URL="https://arxiv.org/abs/2401.12345"
PAPER_ID=$(echo $URL | sed 's/.*\///')
PDF_URL="https://arxiv.org/pdf/${PAPER_ID}.pdf"

# Download and extract (requires PyMuPDF)
python3 -c "
import requests, fitz
response = requests.get('$PDF_URL')
with open('paper.pdf', 'wb') as f:
    f.write(response.content)
doc = fitz.open('paper.pdf')
text = ''.join(page.get_text() for page in doc)
print(text)
"
```

## Common Workflows

### Workflow 1: Build a Knowledge Base

```bash
# Create a list of URLs
cat > urls.txt <<EOF
https://example.com/article-1
https://arxiv.org/abs/2401.12345
https://x.com/user/status/123
EOF

# Convert all
mkdir -p knowledge-base
while read url; do
    filename=$(echo $url | sed 's/[^a-zA-Z0-9]/_/g')
    python skills/docai-convert2md/tools/convert.py "$url" \
        --output "knowledge-base/${filename}.md"
    sleep 1
done < urls.txt
```

### Workflow 2: Research Paper Collection

```bash
# Convert arXiv papers
for paper in 2401.12345 2401.67890; do
    python skills/docai-convert2md/tools/convert.py \
        "https://arxiv.org/abs/$paper" \
        --output "papers/paper_$paper.md"
done
```

### Workflow 3: Social Media Archive

```bash
# Archive X.com threads
python skills/docai-convert2md/tools/convert.py \
    "https://x.com/OpenAI/status/1700000000000000000" \
    --use-browser \
    --output "archive/thread.md"
```

## Integration with Claude Code

After installing this skill to `~/.claude/skills/`, you can simply ask:

```
User: "帮我把 https://example.com 转换成 Markdown"

Claude: (uses this skill)
1. Analyzes the URL
2. Determines it's a static page
3. Uses requests + BeautifulSoup
4. Cleans HTML and converts to Markdown
5. Returns the result
```

Or for complex cases:

```
User: "下载这篇 arXiv 论文并提取主要内容: https://arxiv.org/abs/2401.12345"

Claude: (uses this skill)
1. Converts URL to PDF
2. Downloads PDF
3. Extracts text
4. Summarizes key sections
```

## Common Patterns

### Pattern 1: Auto-detect and convert
```python
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from urllib.parse import urlparse

def smart_convert(url):
    # Check if arXiv
    if 'arxiv.org' in url and '/abs/' in url:
        paper_id = url.split('/abs/')[-1]
        url = f"https://arxiv.org/pdf/{paper_id}.pdf"
        # Handle PDF...
        return

    # Check if needs browser
    dynamic = ['x.com', 'twitter.com', 'medium.com', 'weixin.qq.com']
    domain = urlparse(url).netloc

    if any(d in domain for d in dynamic):
        # Use Playwright
        print(f"Using browser for {domain}")
    else:
        # Use requests
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Clean and convert...
        return md(str(soup))
```

### Pattern 2: Batch processing with rate limits
```python
import time

urls = [...]  # Your URLs

for url in urls:
    try:
        # Convert URL...
        print(f"✓ {url}")
    except Exception as e:
        print(f"✗ {url}: {e}")

    time.sleep(1)  # Be nice to servers
```

### Pattern 3: Save to files
```python
import os

markdown = convert_url(url)  # Your conversion function
filename = url.split('/')[-1] or 'index'

with open(f"{filename}.md", 'w') as f:
    f.write(markdown)
```

## Common Mistakes

### ❌ Forgetting to install Playwright browsers
```bash
# Wrong
pip install playwright
# Missing: playwright install chromium

# Right
pip install playwright
playwright install chromium
```

### ❌ Not handling arXiv correctly
```python
# Wrong: Trying to parse abstract page
url = "https://arxiv.org/abs/2401.12345"
# Gets abstract, not full paper

# Right: Convert to PDF first
url = "https://arxiv.org/pdf/2401.12345.pdf"
# Then extract text
```

### ❌ Forgetting PyMuPDF for PDF extraction
```bash
# Wrong: Trying to extract PDF without library
python convert.py https://arxiv.org/abs/2401.12345
# Error: PDF processing requires PyMuPDF

# Right: Install pymupdf first
pip install pymupdf
python convert.py https://arxiv.org/abs/2401.12345
# Success: Full paper extracted
```

### ❌ No timeout handling
```python
# Wrong: Can hang forever
requests.get(url)

# Right: Set timeout
requests.get(url, timeout=30)
```

### ❌ Not cleaning HTML
```python
# Wrong: Converts everything including ads
md(html)

# Right: Remove noise first
soup = BeautifulSoup(html, 'html.parser')
for tag in soup(['script', 'style', 'nav', 'footer']):
    tag.decompose()
md(str(soup))
```

## Testing

Test with these URLs:

1. **Static**: `https://example.com`
2. **Dynamic**: `https://x.com/OpenAI/status/1700000000000000000`
3. **arXiv**: `https://arxiv.org/abs/2401.12345`
4. **Blog**: Any medium.com article

Expected: Clean Markdown with headings, paragraphs, lists preserved.

## Performance Tips

- Static pages: ~1-2 seconds
- Dynamic pages: ~5-10 seconds
- arXiv PDFs: ~2-5 seconds
- Memory: ~100MB for browser mode

For batch processing:
- Add 1-2 second delays between requests
- Cache results to avoid re-processing
- Use parallel processing with rate limits
