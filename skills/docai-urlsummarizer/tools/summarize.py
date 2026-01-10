#!/usr/bin/env python3
"""
URL 内容总结工具

调用 docai-convert2md 将网页转换为 Markdown，然后使用 AI 进行结构化总结。

用法:
    python summarize.py <url> [--model <model_name>] [--output <file>]

示例:
    python summarize.py https://mp.weixin.qq.com/s/XClh6xJmXoXbyBC9lKzPdA
    python summarize.py https://arxiv.org/abs/2601.04500v1 --output summary.md
"""

import sys
import argparse
import json
import os
import subprocess
from pathlib import Path


class URLSummarizer:
    """URL 内容总结器"""

    def __init__(self):
        self.script_dir = Path(__file__).parent
        # skills/docai-urlsummarizer/tools/summarize.py
        # skills/docai-urlsummarizer/
        # skills/
        # docai-skills/
        self.repo_root = self.script_dir.parent.parent.parent

    def convert_to_markdown(self, url):
        """使用 docai-convert2md 转换 URL 为 Markdown"""
        convert_script = self.repo_root / "skills" / "docai-convert2md" / "tools" / "convert.py"

        if not convert_script.exists():
            raise FileNotFoundError(f"转换脚本不存在: {convert_script}")

        try:
            # 调用 docai-convert2md
            result = subprocess.run(
                ["python", str(convert_script), url],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                error_msg = result.stderr.strip()
                if "Jina Reader 失败" in error_msg and "Firecrawl API 密钥未设置" in error_msg:
                    # 如果非Python方法都失败，尝试强制使用Python方法
                    result = subprocess.run(
                        ["python", str(convert_script), url, "--use-python"],
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                    if result.returncode != 0:
                        raise Exception(f"转换失败: {result.stderr}")
                else:
                    raise Exception(f"转换失败: {error_msg}")

            return result.stdout.strip()

        except subprocess.TimeoutExpired:
            raise Exception("转换超时（60秒）")
        except Exception as e:
            raise Exception(f"转换过程出错: {e}")

    def build_summary_prompt(self, markdown_content, url):
        """构建总结提示词"""
        return f"""请总结以下网页内容，按照指定格式输出：

**内容：**
{markdown_content}

**请严格按照以下格式总结：**

# **标题 | 机构名称** (如果来自知名机构)

✔ 一句话总结：体现网页类型和核心差异

✔ **核心洞见**：深度分析，非简单复述

✔ **技术细节/架构创新**：具体的技术实现

✔ **性能数据/实验结果**：具体数字和结果

✔ **应用场景**：实际使用场景

✔ **长期意义/游戏规则改变者**：深层影响分析

**格式要求：**
1. 所有标题加粗，一级标题末尾可加机构名
2. 加粗标记在标点内部：「**内容**」而非 **「内容」**
3. 列表使用 emoji ✔ 代替 - 或 *
4. 末尾包含清理后的原文链接：{url}
5. 不要 Latex 公式，不要索引引用
6. 总字数控制在1000字以内
7. 要有传播力和吸引力，使用生动比喻
8. 突出技术突破和创新点
9. 揭示长期趋势和深层意义

请直接输出总结内容，不要额外说明。"""

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
                timeout=180
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

    def run_ai_summary(self, markdown_content, url, model=None):
        """尝试运行 AI 总结，如果失败返回提示词"""
        try:
            # 尝试使用 claude 命令
            prompt = self.build_summary_prompt(markdown_content, url)

            # 构建 claude 命令
            cmd = ["claude", "--output", "text"]
            if model:
                cmd.extend(["--model", model])
            cmd.extend(["-p", prompt])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180
            )

            if result.returncode == 0:
                return result.stdout.strip()

        except Exception:
            pass

        # 如果 claude 命令不可用，返回提示词
        return None

    def summarize(self, url, model=None, output=None):
        """主总结流程"""
        print(f"🔄 正在转换 URL: {url}", file=sys.stderr)

        # 步骤1：转换为 Markdown
        try:
            markdown = self.convert_to_markdown(url)
            if not markdown:
                raise Exception("转换结果为空")

            print(f"✅ 转换完成，内容长度: {len(markdown)} 字符", file=sys.stderr)

        except Exception as e:
            print(f"❌ 转换失败: {e}", file=sys.stderr)
            return None

        # 步骤2：AI 总结
        print(f"🤖 正在进行 AI 总结...", file=sys.stderr)

        try:
            summary = self.summarize_with_ai(markdown, url, model)
            print(f"✅ 总结完成", file=sys.stderr)
            return summary

        except Exception as e:
            print(f"❌ 总结失败: {e}", file=sys.stderr)
            return None


def main():
    """命令行入口"""
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
        result = summarizer.summarize(args.url, args.model, args.output)

        if result is None:
            print("✗ 总结失败", file=sys.stderr)
            sys.exit(1)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✓ 已保存到: {args.output}", file=sys.stderr)
        else:
            print(result)

    except Exception as e:
        print(f"✗ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()