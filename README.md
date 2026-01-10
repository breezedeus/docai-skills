# DocAI Skills Marketplace

一个专注于文档 AI 相关技能的 Claude Code Skill 集合。

## 作为 Marketplace 安装

### 方式 1: 通过 Marketplace（推荐）

```bash
# 从 GitHub 安装
/plugin marketplace add breezedeus/docai-skills
```

### 方式 2: 手动安装

```bash
# 复制到 Claude Code 目录
cp -r skills/docai-convert2md ~/.claude/skills/
```

### 方式 3: 本地开发安装

```bash
# 克隆仓库后，从本地路径安装
/plugin marketplace add /path/to/docai-skills
```

## 已实现的 Skills

### docai:convert2md - 网页转 Markdown

将网页链接转换为 Markdown 格式，支持多种平台。

**支持：**
- 静态页面（博客、文档）
- 动态页面（React/Vue SPA）
- 社交媒体（X.com, Twitter）
- 微信公众号文章
- arXiv 论文
- 纯文本模式

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
- ✅ 微信公众号：Jina → Python，~2-5 秒
- ✅ 动态页面：Python，~5-10 秒

**详见：** [skills/docai-convert2md/README.md](skills/docai-convert2md/README.md) | [测试结果](skills/docai-convert2md/TEST_RESULTS.md)

## 计划中的 Skills

- [ ] **docai:pdf-extract** - PDF 内容提取
- [ ] **docai:table-recognize** - 表格识别与提取
- [ ] **docai:ocr** - 图片文字识别
- [ ] **docai:layout-analyze** - 文档布局分析
- [ ] **docai:doc-classify** - 文档分类

## 安装项目（开发环境）

```bash
cd docai-skills
uv sync
```

## 许可证

MIT License
