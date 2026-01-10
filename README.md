# DocAI Skills Marketplace

一个专注于文档 AI 相关技能的 marketplace，为 Claude Code 提供各种文档处理技能。

## 项目结构

```
docai-skills/
├── skills/                          # Skill 集合
│   └── docai-convert2md/           # 网页转 Markdown skill
│       ├── SKILL.md                # ⭐ Skill 定义（Claude Code 使用）
│       └── tools/                  # 可选：工具脚本
│           ├── convert.py          # 转换工具（可执行）
│           └── README.md           # 工具文档
├── pyproject.toml                  # 项目配置
└── README.md                       # 本文件
```

## 快速开始

### 1. 安装项目

```bash
cd docai-skills
uv sync
```

### 2. 安装 Playwright 浏览器

```bash
playwright install chromium
```

### 3. 测试第一个 Skill

```bash
# 使用转换工具
uv run python skills/docai-convert2md/tools/convert.py https://example.com

# 测试微信公众号（已验证成功）
uv run python skills/docai-convert2md/tools/convert.py https://mp.weixin.qq.com/s/XClh6xJmXoXbyBC9lKzPdA
```

## 已实现的 Skills

### docai:convert2md - 网页转 Markdown

**功能：**
- ✅ 静态页面转换
- ✅ 动态页面（React/Vue SPA）
- ✅ 社交媒体（X.com, Twitter）
- ✅ 微信公众号文章
- ✅ arXiv 论文
- ✅ 纯文本模式

**使用示例：**
```bash
# 命令行使用
python skills/docai-convert2md/tools/convert.py https://example.com -o output.md

# Python API
from skills.docai_convert2md.tools.convert import WebToMarkdown
converter = WebToMarkdown()
markdown = converter.convert("https://example.com/article")
```

**测试结果：** 已验证成功处理微信公众号、arXiv 论文、静态页面
- ✅ 微信公众号：https://mp.weixin.qq.com/s/XClh6xJmXoXbyBC9lKzPdA (3395 字符)
- ✅ arXiv 论文：https://arxiv.org/abs/2401.12345 (完整论文提取)
- ✅ arXiv PDF提取：http://arxiv.org/abs/2601.04500v1 (1778行，带标题)
- ✅ 静态页面：https://example.com

**详见：** [skills/docai-convert2md/README.md](skills/docai-convert2md/README.md) | [测试结果](skills/docai-convert2md/TEST_RESULTS.md)

## 计划中的 Skills

- [ ] **docai:pdf-extract** - PDF 内容提取
- [ ] **docai:table-recognize** - 表格识别与提取
- [ ] **docai:ocr** - 图片文字识别
- [ ] **docai:layout-analyze** - 文档布局分析
- [ ] **docai:doc-classify** - 文档分类

## 如何添加新 Skill

### 1. 遵循 TDD 原则

根据 [superpowers:writing-skills](https://github.com/anthropics/claude-code-skills) 的规范：

```
RED: 先写测试场景 → 观察失败
GREEN: 写最小 skill → 验证通过
REFACTOR: 优化 → 再次验证
```

### 2. Skill 目录结构

**基本结构（必需）：**
```
skills/<skill-name>/
└── SKILL.md              # ⭐ 唯一必需文件
```

**扩展结构（可选，用于复杂功能）：**
```
skills/<skill-name>/
├── SKILL.md              # Skill 定义
└── tools/                # 可执行工具
    ├── tool.py           # Python 脚本
    └── README.md         # 工具文档
```

### 3. SKILL.md 格式

```markdown
---
name: skill-name
description: Use when [触发条件]
---

# Skill Name

## Overview
核心原理

## When to Use
使用场景

## Quick Reference
快速参考表

## Implementation
代码示例

## Common Mistakes
常见错误
```

## 开发工作流

### 安装开发依赖

```bash
uv sync --dev
```

### 运行测试

```bash
# 测试转换工具
uv run python skills/docai-convert2md/tools/convert.py https://example.com

# 测试微信公众号（已验证）
uv run python skills/docai-convert2md/tools/convert.py https://mp.weixin.qq.com/s/XClh6xJmXoXbyBC9lKzPdA

# 查看测试结果
cat skills/docai-convert2md/TEST_RESULTS.md
```

### 代码格式化

```bash
ruff check skills/
black skills/
```

## 与 Claude Code 集成

### 方式 1: 直接复制

```bash
# 将 skill 复制到 Claude Code 的 skills 目录
cp -r skills/docai-convert2md ~/.claude/skills/
```

### 方式 2: 通过 CLI 工具（开发中）

```bash
# 未来支持
/docai-marketplace install docai-convert2md
```

### 方式 3: GitHub 集成（开发中）

```bash
# 从 GitHub 安装
/plugin install github.com/your-username/docai-skills/docai-convert2md
```

## 技术栈

- **Python**: 3.11+
- **HTTP**: requests
- **HTML 解析**: BeautifulSoup4
- **Markdown 转换**: markdownify
- **浏览器自动化**: Playwright
- **依赖管理**: uv

## 贡献指南

欢迎贡献新的 DocAI skills！

1. Fork 本仓库
2. 创建新 skill 目录
3. 遵循 TDD 原则开发
4. 添加测试
5. 提交 PR

## 许可证

MIT License

## 资源

- [Claude Code Skills 文档](https://github.com/anthropics/claude-code-skills)
- [Playwright 文档](https://playwright.dev/python/)
- [BeautifulSoup 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
