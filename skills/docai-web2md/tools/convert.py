#!/usr/bin/env python3
"""
Web to Markdown Converter Tool

优先级方法（非Python优先）：
1. Jina Reader API - 零安装，一行URL转换
2. Firecrawl API - 需要API密钥
3. Python实现 - 以上方法失败时的回退

arXiv 特殊处理：
- 输入: https://arxiv.org/abs/2601.04500v1
- 转换为: https://arxiv.org/html/2601.04500v1
- 优先 Jina Reader，失败则 Python 下载 PDF

用法:
    python convert.py <url> [--pure-text] [--output <file>]

示例:
    python convert.py https://www.breezedeus.com/article/ai-agent-context-engineering
    python convert.py https://arxiv.org/abs/2601.04500v1 --output paper.md
    python convert.py https://x.com/user/status/123 --pure-text
"""

import sys
import argparse
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import os

logger = logging.getLogger(__name__)


class WebToMarkdown:
    """网页转 Markdown 转换器（并行优先级方法）"""

    # 超时常量（秒）
    TIMEOUT_HEAD = 3
    TIMEOUT_JINA = 8
    TIMEOUT_FIRECRAWL = 10
    TIMEOUT_REQUESTS = 15
    TIMEOUT_PLAYWRIGHT = 15000  # 毫秒

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (compatible; DocAI-Converter/1.0)"}
        )
        # 配置重试策略：仅针对 429/5xx，最多 2 次，指数退避
        retry = Retry(
            total=2,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        # 从环境变量获取 Firecrawl API 密钥
        self.firecrawl_api_key = os.environ.get("FIRECRAWL_API_KEY")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def convert(self, url, pure_text=False, use_python=False):
        """转换 URL 到 Markdown（并行优先级方法）

        并行发起 Jina Reader / Firecrawl / Python，取最快成功的结果。
        微信公众号和 --use-python 模式走直连路径。

        Args:
            url: 网页 URL
            pure_text: 是否返回纯文本（无格式）
            use_python: 强制使用Python方法

        Returns:
            str: Markdown 或纯文本内容
        """
        url = url.strip()

        # URL 校验
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError(f"无效的 URL: {url}")

        # arXiv 特殊处理：转换为 HTML URL
        if self._is_arxiv(url):
            url = self._convert_arxiv_to_html(url)

        # 微信公众号：直接使用 Python 方法
        if self._is_wechat(url):
            return self._python_convert(url, pure_text)

        # 强制 Python 模式
        if use_python:
            if self._is_arxiv(url):
                return self._handle_arxiv(url, pure_text)
            return self._python_convert(url, pure_text)

        # 并行发起多种方法，取最快成功的
        result = self._parallel_convert(url, pure_text)
        if result:
            return result

        # 所有并行方法都失败，arXiv 尝试 PDF 回退
        if self._is_arxiv(url):
            return self._handle_arxiv(url, pure_text)

        return None

    def _parallel_convert(self, url, pure_text):
        """并行尝试多种方法，返回最快成功的结果"""
        futures = {}
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures[executor.submit(self._try_jina_reader, url, pure_text)] = "jina"

            if self.firecrawl_api_key:
                futures[
                    executor.submit(self._try_firecrawl, url, pure_text)
                ] = "firecrawl"

            futures[executor.submit(self._python_convert, url, pure_text)] = "python"

            for future in as_completed(futures):
                try:
                    result = future.result()
                except Exception:
                    continue
                if result:
                    for f in futures:
                        f.cancel()
                    return result
        return None

    def _try_jina_reader(self, url, pure_text):
        """尝试使用 Jina Reader API

        用法: https://r.jina.ai/https://www.breezedeus.com/article/ai-agent-context-engineering
        """
        try:
            jina_url = f"https://r.jina.ai/{url}"
            response = self.session.get(jina_url, timeout=self.TIMEOUT_JINA)
            response.raise_for_status()

            content = response.text
            if content and len(content.strip()) > 50:  # 验证有内容
                if pure_text:
                    return content
                # Jina 已经返回不错的 Markdown，稍作清理即可
                return self._clean_jina_markdown(content)
        except Exception as e:
            logger.warning("Jina Reader 失败: %s", e)
        return None

    def _try_firecrawl(self, url, pure_text):
        """尝试使用 Firecrawl API"""
        if not self.firecrawl_api_key:
            logger.info("Firecrawl API 密钥未设置 (FIRECRAWL_API_KEY)")
            return None

        try:
            response = self.session.post(
                "https://api.firecrawl.dev/v0/scrape",
                headers={"Authorization": f"Bearer {self.firecrawl_api_key}"},
                json={"url": url, "formats": ["markdown"]},
                timeout=self.TIMEOUT_FIRECRAWL,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("data", {}).get("markdown"):
                    markdown = data["data"]["markdown"]
                    if pure_text:
                        # 从 Markdown 提取纯文本
                        return re.sub(r"[\*\#\`\[\]\(\)]", "", markdown)
                    return markdown
            else:
                logger.warning("Firecrawl 错误: %s", response.status_code)
        except Exception as e:
            logger.warning("Firecrawl 失败: %s", e)
        return None

    def _python_convert(self, url, pure_text):
        """Python实现（回退方法）"""
        # 自动检测是否需要浏览器
        use_browser = self._needs_browser(url)

        if use_browser:
            content = self._get_with_playwright(url)
            is_pdf = False
        else:
            content, is_pdf = self._get_with_requests(url)

        if is_pdf:
            return self._process_pdf(content, pure_text)

        # HTML 转换
        if pure_text:
            return self._to_plain_text(content)
        else:
            return self._to_markdown(content)

    def _handle_arxiv(self, url, pure_text):
        """arXiv Python回退方法：从HTML URL转为PDF下载"""
        try:
            pdf_url = self._convert_arxiv_to_pdf(url)
            logger.info("arXiv Python回退: 下载PDF %s", pdf_url)
            pdf_content, _ = self._get_with_requests(pdf_url)
            return self._process_pdf(pdf_content, pure_text)
        except Exception as e:
            logger.error("arXiv PDF失败: %s", e)
            return None

    def _clean_jina_markdown(self, markdown):
        """清理 Jina Reader 返回的 Markdown"""
        # 移除多余的空行
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)
        # 移除行尾空格
        markdown = re.sub(r" +\n", "\n", markdown)
        return markdown.strip()

    def _is_arxiv(self, url):
        """检测是否为 arXiv 链接"""
        return "arxiv.org" in url and (
            "/abs/" in url or "/pdf/" in url or "/html/" in url
        )

    def _is_wechat(self, url):
        """检测是否为微信公众号链接"""
        return "weixin.qq.com" in url

    def _convert_arxiv_to_html(self, url):
        """转换 arXiv 链接为 HTML URL"""
        if "/html/" in url:
            return url
        if "/pdf/" in url:
            paper_id = url.split("/pdf/")[-1].split("?")[0].replace(".pdf", "")
            return f"https://arxiv.org/html/{paper_id}"
        paper_id = url.split("/abs/")[-1].split("?")[0]
        return f"https://arxiv.org/html/{paper_id}"

    def _convert_arxiv_to_pdf(self, url):
        """转换 arXiv 链接为 PDF URL"""
        if "/pdf/" in url:
            return url
        if "/html/" in url:
            paper_id = url.split("/html/")[-1].split("?")[0]
            return f"https://arxiv.org/pdf/{paper_id}.pdf"
        paper_id = url.split("/abs/")[-1].split("?")[0]
        return f"https://arxiv.org/pdf/{paper_id}.pdf"

    def _is_known_dynamic_site(self, url):
        """检测是否为已知的动态网站（纯函数，无网络调用）"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        dynamic_domains = [
            "x.com",
            "twitter.com",
            "medium.com",
            "substack.com",
            "github.com",
            "reddit.com",
        ]

        for dynamic in dynamic_domains:
            if domain.endswith(dynamic):
                return True

        if "weixin.qq.com" in domain:
            return False

        return None  # 未知，需要探测

    def _probe_for_spa(self, url):
        """通过 HEAD 请求探测是否为 SPA（有网络调用）"""
        try:
            response = self.session.head(
                url, timeout=self.TIMEOUT_HEAD, allow_redirects=True
            )
            content_type = response.headers.get("content-type", "").lower()

            if "application/json" in content_type:
                return True

            server = response.headers.get("server", "").lower()
            if any(s in server for s in ["nextjs", "vercel", "vite"]):
                return True
        except Exception:
            return True

        return False

    def _needs_browser(self, url):
        """自动检测是否需要浏览器渲染"""
        known = self._is_known_dynamic_site(url)
        if known is not None:
            return known
        return self._probe_for_spa(url)

    def _get_with_requests(self, url):
        """使用 requests 获取静态页面或 PDF

        Returns:
            tuple: (content, is_pdf) - content 为 bytes(PDF) 或 str(HTML)
        """
        response = self.session.get(url, timeout=self.TIMEOUT_REQUESTS)
        response.raise_for_status()
        content_type = response.headers.get("content-type", "").lower()
        is_pdf = "application/pdf" in content_type or url.lower().endswith(".pdf")
        if is_pdf:
            return response.content, True
        return response.text, False

    def _process_pdf(self, pdf_content, pure_text=False):
        """处理 PDF 内容，返回 Markdown 或纯文本（只打开一次文档）"""
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError("PDF 处理需要 PyMuPDF。\n" "请运行: pip install pymupdf")

        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")

            # 提取全文
            text = ""
            for page_num, page in enumerate(doc):
                page_text = page.get_text()
                if page_text.strip():
                    text += f"--- Page {page_num + 1} ---\n\n"
                    text += page_text + "\n\n"
            text = text.strip()

            if pure_text:
                return text

            # 提取标题
            title = None
            metadata = doc.metadata
            if metadata and metadata.get("title"):
                title = metadata["title"]
            elif doc.page_count > 0:
                first_page = doc[0]
                lines = [
                    line.strip()
                    for line in first_page.get_text().split("\n")
                    if line.strip()
                ]
                if lines:
                    title = " ".join(lines[:2])

            if title:
                return f"# {title}\n\n{text}"
            return text
        except Exception as e:
            raise Exception(f"PDF 处理失败: {e}")

    def _get_with_playwright(self, url):
        """使用 Playwright 获取动态页面"""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise ImportError(
                "Playwright 未安装。\n"
                "请运行: pip install playwright && playwright install chromium"
            )

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            # 微信公众号使用移动 UA
            if "weixin.qq.com" in url:
                page.set_extra_http_headers(
                    {
                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0) AppleWebKit/605.1.15"
                    }
                )

            try:
                page.goto(
                    url, wait_until="networkidle", timeout=self.TIMEOUT_PLAYWRIGHT
                )
                page.wait_for_timeout(2000)
                content = page.content()
            finally:
                browser.close()

            return content

    def _to_markdown(self, html):
        """HTML 转 Markdown"""
        soup = BeautifulSoup(html, "html.parser")

        # 提取标题（微信公众号等）
        title = None
        # 尝试多种标题来源
        title_selectors = ["title", "h1#activity-name", ".rich_media_title", "h1"]
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text(strip=True)
                if title:
                    break

        # 查找正文内容（优先级）
        content_elem = None
        content_selectors = [
            "#js_content",  # 微信公众号
            ".rich_media_content",  # 微信公众号
            "#activity-detail",  # 微信公众号
            "article",  # 标准文章
            "main",  # 标准主内容
            ".post-content",  # 博客
            ".article-content",  # 博客
        ]

        for selector in content_selectors:
            elem = soup.select_one(selector)
            if elem and elem.get_text(strip=True):
                content_elem = elem
                break

        # 如果没找到特定内容，使用 body
        if not content_elem:
            content_elem = soup.body or soup

        # 移除噪音元素
        for tag in content_elem(
            ["script", "style", "nav", "footer", "header", "iframe", "aside"]
        ):
            tag.decompose()

        # 移除广告和交互元素
        for tag in content_elem.find_all(
            class_=lambda x: x
            and any(
                w in x.lower()
                for w in [
                    "ad",
                    "banner",
                    "cookie",
                    "consent",
                    "popup",
                    "modal",
                    "share",
                    "like",
                    "comment",
                ]
            )
        ):
            tag.decompose()

        # 移除按钮和链接区域
        for tag in content_elem.find_all(
            class_=lambda x: x
            and any(w in x.lower() for w in ["btn", "button", "share", "reward"])
        ):
            tag.decompose()

        # 移除空段落
        for tag in content_elem.find_all("p"):
            if not tag.get_text(strip=True):
                tag.decompose()

        # 构建最终内容
        if title:
            markdown = f"# {title}\n\n"
        else:
            markdown = ""

        cleaned_html = str(content_elem)
        markdown += md(cleaned_html, heading_style="ATX")

        # 清理多余空白
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)
        markdown = re.sub(r" +\n", "\n", markdown)  # 行尾空格

        return markdown.strip()

    def _to_plain_text(self, html):
        """提取纯文本"""
        soup = BeautifulSoup(html, "html.parser")

        main = soup.find("main") or soup.find("article") or soup.body
        if not main:
            return soup.get_text(separator="\n\n", strip=True)

        for tag in main(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        text = main.get_text(separator="\n\n", strip=True)

        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()


def main():
    """命令行入口"""
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr,
    )

    parser = argparse.ArgumentParser(
        description="将网页转换为 Markdown 格式（优先使用非Python方法）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""优先级方法:
  1. Jina Reader API (https://r.jina.ai/URL) - 零安装
  2. Firecrawl API (需要 FIRECRAWL_API_KEY)
  3. Python实现 (回退)

示例:
  %(prog)s https://www.breezedeus.com/article/ai-agent-context-engineering
  %(prog)s https://arxiv.org/abs/2601.04500v1 --output paper.md
  %(prog)s https://x.com/user/status/123 --pure-text
  %(prog)s https://www.breezedeus.com/article/ai-agent-context-engineering --use-python  # 强制使用Python方法
        """,
    )

    parser.add_argument("url", help="要转换的网页 URL")
    parser.add_argument("--pure-text", action="store_true", help="输出纯文本（无 Markdown 格式）")
    parser.add_argument(
        "--use-python", action="store_true", help="强制使用Python方法（跳过Jina/Firecrawl）",
    )
    parser.add_argument("--output", "-o", help="输出到文件")

    args = parser.parse_args()

    try:
        with WebToMarkdown() as converter:
            result = converter.convert(
                args.url, pure_text=args.pure_text, use_python=args.use_python
            )

            if result is None:
                logger.error("转换失败：所有方法均不可用")
                sys.exit(1)

            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(result)
                print(f"✓ 已保存到: {args.output}")
            else:
                print(result)

    except Exception as e:
        logger.error("错误: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
