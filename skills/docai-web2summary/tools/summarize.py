#!/usr/bin/env python3
"""
URL 内容总结工具

调用 docai-web2md 将网页转换为 Markdown，然后使用 AI 进行结构化总结。

用法:
    python summarize.py <url> [--model <model_name>] [--output <file>]

示例:
    python summarize.py https://mp.weixin.qq.com/s/XClh6xJmXoXbyBC9lKzPdA
    python summarize.py https://arxiv.org/abs/2601.04500v1 --output summary.md
"""

import sys
import argparse
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class URLSummarizer:
    """URL 内容总结器"""

    # 超时常量（秒）
    TIMEOUT_CONVERT = 30
    TIMEOUT_CONVERT_RETRY = 60
    TIMEOUT_AI = 120
    # 内容截断上限（字符）
    MAX_CONTENT_LENGTH = 100_000

    def __init__(self):
        self.script_dir = Path(__file__).parent
        # skills/docai-web2summary/tools/summarize.py
        # skills/docai-web2summary/
        # skills/
        # docai-skills/
        self.repo_root = self.script_dir.parent.parent.parent

    def convert_to_markdown(self, url):
        """使用 docai-web2md 转换 URL 为 Markdown"""
        convert_script = self.repo_root / "skills" / "docai-web2md" / "tools" / "convert.py"

        if not convert_script.exists():
            raise FileNotFoundError(f"转换脚本不存在: {convert_script}")

        try:
            # 调用 docai-web2md
            result = subprocess.run(
                [sys.executable, str(convert_script), url],
                capture_output=True,
                text=True,
                timeout=self.TIMEOUT_CONVERT
            )

            if result.returncode != 0:
                error_msg = result.stderr.strip()
                if "Jina Reader 失败" in error_msg and "Firecrawl API 密钥未设置" in error_msg:
                    # 如果非Python方法都失败，尝试强制使用Python方法
                    result = subprocess.run(
                        [sys.executable, str(convert_script), url, "--use-python"],
                        capture_output=True,
                        text=True,
                        timeout=self.TIMEOUT_CONVERT_RETRY
                    )
                    if result.returncode != 0:
                        raise Exception(f"转换失败: {result.stderr}")
                else:
                    raise Exception(f"转换失败: {error_msg}")

            return result.stdout.strip()

        except subprocess.TimeoutExpired:
            raise Exception(f"转换超时（{self.TIMEOUT_CONVERT}秒）")
        except Exception as e:
            raise Exception(f"转换过程出错: {e}")

    def build_summary_prompt(self, markdown_content, url):
        """构建总结提示词（从模板文件加载）"""
        template_path = self.script_dir / "prompts" / "summary_prompt.txt"
        template = template_path.read_text(encoding='utf-8')
        return template.format(markdown_content=markdown_content)

    def summarize_with_ai(self, markdown_content, url, model=None):
        """使用 AI 进行总结"""
        prompt = self.build_summary_prompt(markdown_content, url)

        # 尝试使用 claude 命令
        try:
            # 构建 claude 命令
            cmd = ["claude", "--output", "text"]
            if model:
                cmd.extend(["--model", model])
            cmd.extend(["-p", prompt])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.TIMEOUT_AI
            )

            if result.returncode == 0:
                return result.stdout.strip()

        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        except Exception:
            pass

        # 如果 claude 命令不可用，返回提示词供手动使用
        return f"""⚠️  AI 总结需要手动执行

请使用以下提示词让 AI 总结内容：

{prompt}

---

💡 提示：您可以将上述提示词复制到 Claude Code 或其他 AI 助手中使用"""

    def summarize(self, url, model=None):
        """主总结流程"""
        logger.info("正在转换 URL: %s", url)

        # 步骤1：转换为 Markdown
        try:
            markdown = self.convert_to_markdown(url)
            if not markdown:
                raise Exception("转换结果为空")

            logger.info("转换完成，内容长度: %d 字符", len(markdown))

        except Exception as e:
            logger.error("转换失败: %s", e)
            return None

        # 步骤2：内容截断保护
        if len(markdown) > self.MAX_CONTENT_LENGTH:
            logger.warning("内容过长 (%d 字符)，截断至 %d 字符", len(markdown), self.MAX_CONTENT_LENGTH)
            markdown = markdown[:self.MAX_CONTENT_LENGTH] + "\n\n[... 内容已截断 ...]"

        # 步骤3：AI 总结
        logger.info("正在进行 AI 总结...")

        try:
            summary = self.summarize_with_ai(markdown, url, model)
            logger.info("总结完成")
            return summary

        except Exception as e:
            logger.error("总结失败: %s", e)
            return None


def main():
    """命令行入口"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s',
        stream=sys.stderr,
    )

    parser = argparse.ArgumentParser(
        description='URL 内容总结工具（转换 + AI 总结）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''示例:
  %(prog)s https://mp.weixin.qq.com/s/XClh6xJmXoXbyBC9lKzPdA
  %(prog)s https://arxiv.org/abs/2601.04500v1 --model sonnet --output summary.md
        '''
    )

    parser.add_argument('url', help='要总结的网页 URL')
    parser.add_argument('--model', help='指定 AI 模型（如 sonnet, haiku）')
    parser.add_argument('--output', '-o', help='输出到文件')

    args = parser.parse_args()

    try:
        summarizer = URLSummarizer()
        result = summarizer.summarize(args.url, args.model)

        if result is None:
            logger.error("总结失败")
            sys.exit(1)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            logger.info("已保存到: %s", args.output)
        else:
            print(result)

    except Exception as e:
        logger.error("错误: %s", e)
        sys.exit(1)


if __name__ == '__main__':
    main()