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
import json
import os
import subprocess
from pathlib import Path


class URLSummarizer:
    """URL 内容总结器"""

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

**请严格按照以下要求总结：**

📋 格式要求
1. 标题格式
* 所有级别的标题都必须加粗
   * 一级标题：`# **标题**`
   * 二级标题：`## **标题**`
   * 三级标题：`### **标题**`
* 如果来自知名机构，在一级标题末尾标识机构名称
   * 格式：`# **标题内容 | 机构名称**`
* 内部标题与前面的内容之间，要加一个空行
2. 加粗文字的标点符号处理
* 加粗标记（`**`）应该在标点符号内部，而不是外部
* ✅ 正确：`「**更聪明地激活**」`、`**更聪明地激活**:`
* ❌ 错误：`**「更聪明地激活」**`、`**更聪明地激活:**`
* ✅ 正确：稀疏高效激活
* ❌ 错误："稀疏高效激活"
3. 链接处理
* 末尾必须包含原文链接
* 格式：`**原文：** <链接>`
* 链接中的查询参数（`?` 后面的部分）需要删除
   * ✅ 正确：`https://example.com/article`
   * ❌ 错误：`https://example.com/article?ncid=ref-inor-399942`
4. 列表格式
* 如果使用 `- `或 `* 无序列表，使用 `emoji ✔ 代替前面的 - 或 * ,末尾加换行（空一行）

📝 内容要求
所有总结内容要基于链接网页中的信息获得，禁止自行推断。
生成结果中不要出现Latex数学公式，不要包含索引或引用。
	1. 核心结构（整体不能超过1000个字，请合理分配输出资源。没有的章节直接删除即可）
	✔ 一句话总结（开篇）:这句话需要体现这个网页的类型，必须有吸引力，体现核心差异
	✔ 核心洞见
	✔ 技术细节/架构创新
	✔ 性能数据/实验结果
	✔ 应用场景
	✔ 长期意义/为什么是游戏规则改变者
	✔ 原文链接（末尾）
	2. 写作风格
	✔ 要有传播力和吸引力
	✔ 提供**深度洞见**，而非简单复述
	✔ 突出技术突破和创新点
	✔ 说明实际应用价值
	✔ 揭示长期趋势和深层意义
	3. 语言特点
	✔ 使用生动的比喻和形象化表达
	✔ 标题和小标题使用 emoji 增强可读性
	✔ 适当使用对比（传统 vs 新方法）
	✔ 突出"最震撼的认知"或核心发现
	
	注意：除了总结的内容外，不要包括任何其他内容。内容中间不要包含原文引用。

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