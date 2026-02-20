# DocAI Skills Marketplace

一个专注于文档 AI 相关技能的 Claude Code Skill 集合。

## 安装到 Claude Code

### GitHub Marketplace（推荐）

```bash
# 1. 添加 marketplace 来源
/plugin marketplace add breezedeus/docai-skills

# 2. 安装具体 skills
/plugin install docai-web2md
/plugin install docai-web2summary

# 3. 或安装所有
/plugin install docai-skills
```

## 已实现的 Skills

### docai:web2md - 网页转 Markdown

将网页链接转换为 Markdown 格式，支持多种平台。

**支持：**
- 静态页面（博客、文档）
- 动态页面（React/Vue SPA）
- 社交媒体（X.com, Twitter）
- 微信公众号文章
- arXiv 论文（HTML 优先，PDF 回退）
- 纯文本模式

**转换方式：** 并行发起 Jina Reader / Firecrawl / Python，取最快成功的结果。

**安装 Python 依赖（仅用于回退方法）：**
```bash
pip install requests beautifulsoup4 markdownify pymupdf
```

**使用：**
```
帮我把 https://www.breezedeus.com/article/ai-agent-context-engineering 转换成 Markdown
```

**测试结果：**
- ✅ arXiv 论文：HTML 优先，~1-3 秒
- ✅ 静态博客：Jina Reader，~1-2 秒
- ✅ 微信公众号：Python 直连，~2-5 秒
- ✅ 动态页面：Python，~5-10 秒

**详见：** [skills/docai-web2md/README.md](skills/docai-web2md/README.md) | [使用指南](skills/docai-web2md/SKILL.md)

---

### docai:web2summary - 网页智能总结

基于 `docai-web2md` 的网页转换能力，结合 AI 生成结构化深度总结。

**核心功能：**
- 🔄 自动转换网页为 Markdown
- 🤖 AI 自动判断内容类型，生成对应结构的总结
- 📋 支持六种内容类型：技术论文、新闻报道、教程指南、产品评测、AI 动态、通用
- 💾 支持直接保存到文件

**使用：**
```bash
# 基本总结
python skills/docai-web2summary/tools/summarize.py https://mp.weixin.qq.com/s/...

# 指定模型并保存
python skills/docai-web2summary/tools/summarize.py https://arxiv.org/abs/2601.04500v1 --model sonnet -o summary.md
```

**输出格式（根据内容类型自适应）：**
```
# **标题 | 机构名称**

✔ 一句话总结

（以下章节根据内容类型自动选择）
✔ 技术论文 → 核心洞见、技术细节、性能数据、应用场景、长期意义
✔ 新闻报道 → 核心事件、关键人物/机构、背景与影响、后续展望
✔ 教程指南 → 学习目标、前置条件、关键步骤、注意事项
✔ 产品评测 → 产品定位、核心功能、竞品对比、适用人群
✔ AI 动态 → 核心动态、技术要点、行业影响、值得关注的信号
✔ 通用 → 核心内容、关键要点、价值与启发

**原文：** <链接>
```

**详见：** [skills/docai-web2summary/README.md](skills/docai-web2summary/README.md) | [使用指南](skills/docai-web2summary/SKILL.md)

## 计划中的 Skills

- [ ] **docai:pdf-extract** - PDF 内容提取
- [ ] **docai:table-recognize** - 表格识别与提取
- [ ] **docai:ocr** - 图片文字识别
- [ ] **docai:layout-analyze** - 文档布局分析
- [ ] **docai:doc-classify** - 文档分类

## 🛠️ 开发环境设置

### 使用 uv（推荐）

```bash
# 1. 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 克隆项目
git clone <repo>
cd docai-skills

# 3. 初始化虚拟环境
uv sync

# 4. 执行脚本（方式 A：使用 uv run）
uv run python skills/docai-web2md/tools/convert.py https://example.com

# 5. 或激活环境后执行（方式 B）
source .venv/bin/activate
python skills/docai-web2md/tools/convert.py https://example.com
```

### 使用 pip（传统方式）

```bash
# 1. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt  # 或手动安装
pip install requests beautifulsoup4 markdownify pymupdf

# 3. 执行脚本
python skills/docai-web2md/tools/convert.py https://example.com
```

### ⚠️ Claude Code Skill 集成

**重要**：Claude Code 调用 Skill 时使用系统 Python，需要额外配置：

```bash
# 选项 1: 安装到系统 Python（一次性）
uv pip install --system requests beautifulsoup4 markdownify pymupdf

# 选项 2: 使用 pip 安装到系统
pip install requests beautifulsoup4 markdownify pymupdf
```

详见：[UV_ENVIRONMENT.md](UV_ENVIRONMENT.md) - 完整的 uv 环境管理指南

## 许可证

MIT License
