"""Tests for docai-web2md convert module."""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add the tools directory to path so we can import convert
sys.path.insert(
    0, str(Path(__file__).parent.parent / "skills" / "docai-web2md" / "tools")
)
from convert import WebToMarkdown  # noqa: E402


class TestArxivURLs:
    """测试 arXiv URL 检测和转换"""

    def test_is_arxiv_abs(self):
        converter = WebToMarkdown()
        assert converter._is_arxiv("https://arxiv.org/abs/2601.04500v1")

    def test_is_arxiv_pdf(self):
        converter = WebToMarkdown()
        assert converter._is_arxiv("https://arxiv.org/pdf/2601.04500v1.pdf")

    def test_is_arxiv_html(self):
        converter = WebToMarkdown()
        assert converter._is_arxiv("https://arxiv.org/html/2601.04500v1")

    def test_is_not_arxiv(self):
        converter = WebToMarkdown()
        assert not converter._is_arxiv("https://example.com/article")

    def test_convert_abs_to_html(self):
        converter = WebToMarkdown()
        result = converter._convert_arxiv_to_html(
            "https://arxiv.org/abs/2601.04500v1"
        )
        assert result == "https://arxiv.org/html/2601.04500v1"

    def test_convert_pdf_to_html(self):
        converter = WebToMarkdown()
        result = converter._convert_arxiv_to_html(
            "https://arxiv.org/pdf/2601.04500v1.pdf"
        )
        assert result == "https://arxiv.org/html/2601.04500v1"

    def test_convert_html_stays(self):
        converter = WebToMarkdown()
        result = converter._convert_arxiv_to_html(
            "https://arxiv.org/html/2601.04500v1"
        )
        assert result == "https://arxiv.org/html/2601.04500v1"

    def test_convert_abs_to_pdf(self):
        converter = WebToMarkdown()
        result = converter._convert_arxiv_to_pdf(
            "https://arxiv.org/abs/2601.04500v1"
        )
        assert result == "https://arxiv.org/pdf/2601.04500v1.pdf"

    def test_convert_html_to_pdf(self):
        converter = WebToMarkdown()
        result = converter._convert_arxiv_to_pdf(
            "https://arxiv.org/html/2601.04500v1"
        )
        assert result == "https://arxiv.org/pdf/2601.04500v1.pdf"

    def test_convert_pdf_stays(self):
        converter = WebToMarkdown()
        url = "https://arxiv.org/pdf/2601.04500v1.pdf"
        assert converter._convert_arxiv_to_pdf(url) == url


class TestWechatDetection:
    """测试微信公众号检测"""

    def test_is_wechat(self):
        converter = WebToMarkdown()
        assert converter._is_wechat(
            "https://mp.weixin.qq.com/s/XClh6xJmXoXbyBC9lKzPdA"
        )

    def test_is_not_wechat(self):
        converter = WebToMarkdown()
        assert not converter._is_wechat("https://example.com/article")


class TestCleanJinaMarkdown:
    """测试 Jina Markdown 清理"""

    def test_removes_extra_newlines(self):
        converter = WebToMarkdown()
        result = converter._clean_jina_markdown("hello\n\n\n\nworld")
        assert result == "hello\n\nworld"

    def test_removes_trailing_spaces(self):
        converter = WebToMarkdown()
        result = converter._clean_jina_markdown("hello   \nworld")
        assert result == "hello\nworld"

    def test_strips_content(self):
        converter = WebToMarkdown()
        result = converter._clean_jina_markdown("  hello  ")
        assert result == "hello"


class TestURLValidation:
    """测试 URL 校验"""

    def test_invalid_url_raises(self):
        converter = WebToMarkdown()
        with pytest.raises(ValueError, match="无效的 URL"):
            converter.convert("not-a-url")

    def test_ftp_url_raises(self):
        converter = WebToMarkdown()
        with pytest.raises(ValueError, match="无效的 URL"):
            converter.convert("ftp://example.com/file")

    def test_empty_url_raises(self):
        converter = WebToMarkdown()
        with pytest.raises(ValueError, match="无效的 URL"):
            converter.convert("")


class TestDynamicSiteDetection:
    """测试动态网站检测"""

    def test_twitter_is_dynamic(self):
        converter = WebToMarkdown()
        assert converter._is_known_dynamic_site(
            "https://x.com/user/status/123"
        ) is True

    def test_github_is_dynamic(self):
        converter = WebToMarkdown()
        assert converter._is_known_dynamic_site(
            "https://github.com/user/repo"
        ) is True

    def test_wechat_is_not_dynamic(self):
        converter = WebToMarkdown()
        assert converter._is_known_dynamic_site(
            "https://mp.weixin.qq.com/s/abc"
        ) is False

    def test_unknown_site_returns_none(self):
        converter = WebToMarkdown()
        assert converter._is_known_dynamic_site(
            "https://example.com"
        ) is None


class TestToMarkdown:
    """测试 HTML 转 Markdown"""

    def test_basic_html(self):
        converter = WebToMarkdown()
        html = "<html><body><h1>Title</h1><p>Content</p></body></html>"
        result = converter._to_markdown(html)
        assert "Title" in result
        assert "Content" in result

    def test_wechat_article(self):
        converter = WebToMarkdown()
        html = (
            '<html><body>'
            '<h1 id="activity-name">测试文章</h1>'
            '<div id="js_content"><p>正文内容</p></div>'
            '</body></html>'
        )
        result = converter._to_markdown(html)
        assert "测试文章" in result
        assert "正文内容" in result

    def test_removes_scripts(self):
        converter = WebToMarkdown()
        html = (
            "<html><body><p>Content</p>"
            "<script>alert('xss')</script></body></html>"
        )
        result = converter._to_markdown(html)
        assert "alert" not in result


class TestToPlainText:
    """测试纯文本提取"""

    def test_basic_text(self):
        converter = WebToMarkdown()
        html = "<html><body><main><p>Hello World</p></main></body></html>"
        result = converter._to_plain_text(html)
        assert "Hello World" in result

    def test_no_body_fallback(self):
        converter = WebToMarkdown()
        html = "<p>Just a paragraph</p>"
        result = converter._to_plain_text(html)
        assert "Just a paragraph" in result


class TestContextManager:
    """测试上下文管理器"""

    def test_context_manager(self):
        with WebToMarkdown() as converter:
            assert converter.session is not None

    def test_session_close_called(self):
        converter = WebToMarkdown()
        converter.session = MagicMock()
        converter.__exit__(None, None, None)
        converter.session.close.assert_called_once()


class TestParallelConvert:
    """测试并行转换"""

    @patch.object(WebToMarkdown, '_try_jina_reader', return_value="# Jina")
    @patch.object(WebToMarkdown, '_try_firecrawl', return_value=None)
    @patch.object(WebToMarkdown, '_python_convert', return_value="# Python")
    def test_returns_first_success(self, _py, _fc, _jina):
        converter = WebToMarkdown()
        result = converter._parallel_convert("https://example.com", False)
        assert result is not None

    @patch.object(WebToMarkdown, '_try_jina_reader', return_value=None)
    @patch.object(WebToMarkdown, '_try_firecrawl', return_value=None)
    @patch.object(WebToMarkdown, '_python_convert', return_value=None)
    def test_all_fail_returns_none(self, _py, _fc, _jina):
        converter = WebToMarkdown()
        result = converter._parallel_convert("https://example.com", False)
        assert result is None
