"""Tests for docai-web2summary summarize module."""
import sys
from pathlib import Path

# Add the tools directory to path so we can import summarize
sys.path.insert(
    0, str(Path(__file__).parent.parent / "skills" / "docai-web2summary" / "tools")
)
from summarize import URLSummarizer  # noqa: E402


class TestBuildSummaryPrompt:
    """测试 prompt 构建"""

    def test_prompt_contains_content(self):
        summarizer = URLSummarizer()
        prompt = summarizer.build_summary_prompt("# Test Content", "https://example.com")
        assert "# Test Content" in prompt

    def test_prompt_loads_from_template(self):
        summarizer = URLSummarizer()
        template_path = summarizer.script_dir / "prompts" / "summary_prompt.txt"
        assert template_path.exists(), "Prompt template file should exist"

    def test_prompt_contains_content_type_sections(self):
        """prompt 模板应包含多种内容类型的总结结构"""
        summarizer = URLSummarizer()
        prompt = summarizer.build_summary_prompt("test", "https://example.com")
        assert "类型A：技术论文/研究" in prompt
        assert "类型B：新闻报道" in prompt
        assert "类型C：教程/指南" in prompt
        assert "类型D：产品发布/评测" in prompt
        assert "类型E：AI 行业动态" in prompt
        assert "类型F：通用" in prompt

    def test_prompt_has_type_detection_instruction(self):
        """prompt 应包含类型判断指令"""
        summarizer = URLSummarizer()
        prompt = summarizer.build_summary_prompt("test", "https://example.com")
        assert "判断内容类型" in prompt


class TestContentTruncation:
    """测试内容截断"""

    def test_max_content_length_defined(self):
        assert URLSummarizer.MAX_CONTENT_LENGTH == 100_000

    def test_timeout_constants_defined(self):
        assert URLSummarizer.TIMEOUT_CONVERT == 30
        assert URLSummarizer.TIMEOUT_CONVERT_RETRY == 60
        assert URLSummarizer.TIMEOUT_AI == 120
