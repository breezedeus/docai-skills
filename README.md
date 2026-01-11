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
cp -r skills/docai-web2md ~/.claude/skills/
cp -r skills/docai-web2summary ~/.claude/skills/
```

### 方式 3: 本地开发安装

```bash
# 克隆仓库后，从本地路径安装
/plugin marketplace add /path/to/docai-skills
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

**详见：** [skills/docai-web2md/README.md](skills/docai-web2md/README.md) | [使用指南](skills/docai-web2md/SKILL.md)

---

### docai:web2summary - 网页智能总结

基于 `docai-web2md` 的网页转换能力，结合 AI 生成结构化深度总结。

**核心功能：**
- 🔄 自动转换网页为 Markdown
- 🤖 AI 生成标准化格式总结
- 📋 包含核心洞见、技术细节、性能数据等
- 💾 支持直接保存到文件

**使用：**
```bash
# 基本总结
python skills/docai-web2summary/tools/summarize.py https://mp.weixin.qq.com/s/...

# 指定模型并保存
python skills/docai-web2summary/tools/summarize.py https://arxiv.org/abs/2601.04500v1 --model sonnet -o summary.md
```

**输出格式：**
```
# **标题 | 机构名称**

✔ 一句话总结
✔ **核心洞见**：深度分析
✔ **技术细节/架构创新**：具体实现
✔ **性能数据/实验结果**：具体数字
✔ **应用场景**：实际使用场景
✔ **长期意义/游戏规则改变者**：深层影响
```

**详见：** [skills/docai-web2summary/README.md](skills/docai-web2summary/README.md) | [使用指南](skills/docai-web2summary/SKILL.md)

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
