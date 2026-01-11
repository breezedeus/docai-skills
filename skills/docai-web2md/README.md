# docai-web2md

独立 Python 工具，用于将网页转换为 Markdown 格式，采用**优先级架构**。

> 📖 **文档导航**
> - **SKILL.md** - Claude Code 使用指南（如何调用此技能）
> - **README.md** - 本文档（工具功能说明和独立使用）
> - **tools/convert.py** - 实际转换代码实现
> - **共享参考**: [web-sources.md](../../shared/references/web-sources.md) - 平台支持矩阵

## 核心特性

- ✅ **Jina Reader API 优先** - 零安装，最快最简单（微信公众号除外）
- ✅ **Firecrawl API 支持** - 高级爬虫需求
- ✅ **Python 智能回退** - 以上方法失败时自动切换
- ✅ **arXiv HTML 优先** - 优先获取 HTML 版，失败时回退 PDF
- ✅ **多平台支持** - 微信公众号（直接 Python）、静态博客、动态页面等

## 优先级策略

```python
# 转换流程
输入 URL
    ↓
是 arXiv? → 转换为 HTML URL
    ↓
是微信公众号? → 直接 Python 方法 ⭐
    ↓
尝试 Jina Reader API (快速)
    ↓ (失败)
尝试 Firecrawl API (需要密钥)
    ↓ (失败)
Python 方法 (回退)
    ↓
arXiv? → 下载 PDF 提取
```

**微信公众号特殊处理**：由于 Jina Reader 对微信公众号支持不佳，直接使用 Python 方法以确保最佳效果。

## 快速开始

### 方式 1: 使用 uv（推荐）

```bash
# 1. 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 在 docai-skills 目录初始化环境
cd docai-skills
uv sync

# 3. 执行脚本（无需激活环境）
uv run python skills/docai-web2md/tools/convert.py https://www.breezedeus.com/article/ai-agent-context-engineering
```

### 方式 2: 使用 pip（传统方式）

```bash
# 1. 创建虚拟环境（可选但推荐）
python -m venv .venv
source .venv/bin/activate

# 2. 安装依赖
pip install requests beautifulsoup4 markdownify pymupdf

# 3. 执行脚本
python skills/docai-web2md/tools/convert.py https://www.breezedeus.com/article/ai-agent-context-engineering
```

### 方式 3: Jina Reader API（无需安装）

```bash
# 直接使用 API，无需任何依赖
curl https://r.jina.ai/https://www.breezedeus.com/article/ai-agent-context-engineering
```

### ⚠️ Claude Code Skill 集成

**重要**：Claude Code 调用 Skill 时使用系统 Python，需要额外配置：

```bash
# 使用 uv 安装到系统（不影响项目虚拟环境）
uv pip install --system requests beautifulsoup4 markdownify pymupdf

# 或使用 pip
pip install requests beautifulsoup4 markdownify pymupdf
```

**详见**：[UV_ENVIRONMENT.md](../../UV_ENVIRONMENT.md)

## 命令行使用

```bash
# 基本用法（自动优先级）
python skills/docai-web2md/tools/convert.py https://www.breezedeus.com/article/ai-agent-context-engineering

# 保存到文件
python skills/docai-web2md/tools/convert.py https://www.breezedeus.com/article/ai-agent-context-engineering -o article.md

# 纯文本模式
python skills/docai-web2md/tools/convert.py https://www.breezedeus.com/article/ai-agent-context-engineering --pure-text

# 强制使用 Python 方法（跳过 Jina/Firecrawl）
python skills/docai-web2md/tools/convert.py https://www.breezedeus.com/article/ai-agent-context-engineering --use-python
```

## 优先级架构

```
输入 URL
    ↓
arXiv? → 转换为 HTML URL
    ↓
Jina Reader API (⭐ 零安装)
    ↓ 失败
Firecrawl API (需密钥)
    ↓ 失败
Python 实现 (全能回退)
    ↓
arXiv? → 下载 PDF 提取
    ↓
普通网页 → HTML 解析
```

## 使用示例

```bash
# 静态博客（Jina Reader）
python skills/docai-web2md/tools/convert.py https://www.breezedeus.com/article/ai-agent-context-engineering

# arXiv 论文（HTML 优先，PDF 回退）
python skills/docai-web2md/tools/convert.py https://arxiv.org/abs/2601.04500v1

# 微信公众号（Jina → Python 回退）
python skills/docai-web2md/tools/convert.py https://mp.weixin.qq.com/s/1LfkYdbzymoWxdvdnKeLnA

# X.com/Twitter（Python 动态渲染）
python skills/docai-web2md/tools/convert.py https://x.com/user/status/123
```

## Python API

```python
from skills.docai_web2md.tools.convert import WebToMarkdown

converter = WebToMarkdown()

# 自动优先级（推荐）
markdown = converter.convert("https://www.breezedeus.com/article/ai-agent-context-engineering")

# arXiv 自动处理（HTML → PDF）
paper = converter.convert("https://arxiv.org/abs/2601.04500v1")

# 强制 Python 方法
markdown = converter.convert("https://www.breezedeus.com/article/ai-agent-context-engineering", use_python=True)

# 纯文本输出
text = converter.convert("https://www.breezedeus.com/article/ai-agent-context-engineering", pure_text=True)
```

## 依赖说明

| 方法 | 依赖 | 说明 |
|------|------|------|
| **Jina Reader** | 无 | 只需网络连接 |
| **Firecrawl** | `FIRECRAWL_API_KEY` | 环境变量 |
| **Python 回退** | `requests`, `beautifulsoup4`, `markdownify` | 基础依赖 |
| **PDF 支持** | `pymupdf` | arXiv PDF 提取 |
| **动态页面** | `playwright` | React/Vue SPA |

## 性能参考

- **Jina Reader**: ~1-2 秒
- **Firecrawl**: ~2-5 秒
- **Python 静态**: ~1-2 秒
- **Python 动态**: ~5-10 秒
- **arXiv PDF**: ~2-5 秒

## 与 Skill 的关系

- **SKILL.md**: 指导 Claude 如何使用此工具
- **tools/convert.py**: 实际执行转换的代码
- **README.md**: 本文档（工具使用说明）

## 测试

```bash
# 测试 breezedeus.com 博客
python skills/docai-web2md/tools/convert.py https://www.breezedeus.com/article/ai-agent-context-engineering
```

## 许可证

MIT
