# docai-web2summary

一个智能 URL 内容总结工具，结合了 `docai-web2md` 的网页转换能力和 AI 的结构化总结能力。

## ✨ 功能特性

- 🔄 **自动转换**：调用 `docai-web2md` 将任意网页转换为 Markdown
- 🤖 **AI 总结**：使用 AI 生成符合特定格式的深度总结
- 📋 **标准化输出**：遵循统一的总结格式（核心洞见、技术细节、性能数据等）
- 🎯 **多模型支持**：支持指定不同的 AI 模型（sonnet, haiku 等）
- 💾 **文件输出**：支持直接保存到文件

## 📦 安装依赖

此 skill 依赖于 `docai-web2md`，确保已安装：

```bash
# 在 docai-skills 目录下
/plugin install docai-web2md
```

## 🚀 使用方法

### 基本用法

```bash
# 总结网页内容
python skills/docai-web2summary/tools/summarize.py https://mp.weixin.qq.com/s/XClh6xJmXoXbyBC9lKzPdA
```

### 指定模型

```bash
# 使用特定模型
python skills/docai-web2summary/tools/summarize.py https://arxiv.org/abs/2601.04500v1 --model sonnet
```

### 保存到文件

```bash
# 输出到文件
python skills/docai-web2summary/tools/summarize.py https://www.breezedeus.com/article/ai-agent-context-engineering --output summary.md
```

## 📋 输出格式

总结内容遵循以下结构：

```
# **标题 | 机构名称**

✔ 一句话总结：体现网页类型和核心差异

✔ **核心洞见**：深度分析

✔ **技术细节/架构创新**：具体实现

✔ **性能数据/实验结果**：具体数字

✔ **应用场景**：实际使用场景

✔ **长期意义/游戏规则改变者**：深层影响

**原文：** <链接>
```

## 🔧 工作流程

1. **转换阶段**：调用 `docai-web2md` 将 URL 转换为 Markdown
   - 优先使用 Jina Reader API
   - 失败时使用 Firecrawl API
   - 最终回退到 Python 实现

2. **总结阶段**：构建提示词并调用 AI 进行结构化总结
   - 包含原始 Markdown 内容
   - 指定严格的输出格式
   - 要求深度洞见而非简单复述

## ⚙️ 配置选项

| 参数 | 说明 | 示例 |
|------|------|------|
| `url` | 必需，要总结的网页 URL | `https://example.com/article` |
| `--model` | 可选，指定 AI 模型 | `sonnet`, `haiku` |
| `--output, -o` | 可选，输出文件路径 | `summary.md` |

## 🎯 适用场景

- 📰 **新闻文章**：快速了解技术新闻的核心观点
- 📚 **学术论文**：提取 arXiv 论文的关键贡献
- 📖 **技术博客**：深度分析技术文章的创新点
- 🎯 **产品文档**：总结产品特性和使用场景
- 🔍 **研究资料**：整理长篇研究内容的要点

## 🔍 示例输出

输入：
```bash
python summarize.py https://mp.weixin.qq.com/s/XClh6xJmXoXbyBC9lKzPdA
```

输出：
```markdown
# **给Claude Code装个仪表盘：claude-hud插件深度评测**

✔ 这是一篇技术博客文章，详细介绍了一个能让Claude Code从"盲开"变透明的仪表盘插件...

✔ **核心洞见**：Claude Code最大的痛点不是功能不足，而是"黑盒"体验...

✔ **技术细节/架构创新**：基于Claude Code原生statusline API构建...

✔ **性能数据/实验结果**：Context可视化实时显示token占用率...

✔ **应用场景**：复杂任务重构、CI/CD调试、长期项目开发...

✔ **长期意义/游戏规则改变者**：标志着AI编程助手从"功能增强"向"体验优化"的重要转变...

**原文：** https://mp.weixin.qq.com/s/XClh6xJmXoXbyBC9lKzPdA
```

## ⚠️ 注意事项

1. **依赖要求**：需要安装 `docai-web2md` 及其依赖
2. **网络连接**：需要互联网连接进行网页抓取和 AI 总结
3. **超时设置**：转换限时 60 秒，总结限时 180 秒
4. **内容长度**：建议源内容不超过 50,000 字符
5. **AI 可用性**：如果 `claude` 命令不可用，会返回提示词供手动使用

## 🛠️ 故障排除

### 转换失败
- 检查 URL 是否可访问
- 确认网络连接正常
- 尝试使用 `--use-python` 参数强制 Python 方法

### 总结失败
- 检查 AI 模型是否可用
- 确认 `claude` 命令已正确配置
- 手动使用提供的提示词进行总结

### 依赖缺失
```bash
# 安装 docai-web2md
/plugin install docai-web2md

# 安装 Python 依赖（如果需要）
cd docai-skills
uv sync
```

## 🤝 与 docai-web2md 的关系

`docai-web2summary` 是 `docai-web2md` 的增强版本：

| 功能 | docai-web2md | docai-web2summary |
|------|------------------|---------------------|
| 网页转换 | ✅ | ✅ |
| Markdown 输出 | ✅ | ✅ |
| AI 结构化总结 | ❌ | ✅ |
| 深度洞见分析 | ❌ | ✅ |
| 标准化格式 | ❌ | ✅ |

## 📝 开发计划

- [ ] 支持批量 URL 总结
- [ ] 添加自定义总结模板
- [ ] 集成更多 AI 模型
- [ ] 支持本地文件总结
- [ ] 添加总结质量评分

## 📄 许可证

MIT