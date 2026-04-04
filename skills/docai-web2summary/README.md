# docai-web2summary

对任意网页 URL 生成结构化总结的 AI Skill。

## 工作流程

1. **获取内容**：调用 `docai-web2md` 将 URL 转为 Markdown
2. **AI 总结**：AI 直接根据 [SKILL.md](SKILL.md) 中的规范完成总结，无需外部脚本
3. **信息卡（可选）**：如需生成图片卡片，使用 [info-card-designer](https://github.com/joeseesun/info-card-designer)

## 使用方式

直接对 AI 说明需求即可：

> 总结这个链接：https://www.breezedeus.com/article/ai-agent-context-engineering

AI 会自动：
- 判断内容类型（论文 / 新闻 / 教程 / 产品 / AI 动态 / 通用）
- 套用对应的总结结构
- 按统一格式输出 Markdown

## 输出格式示例

```markdown
# **给Claude Code装个仪表盘：claude-hud插件深度评测**

✔ 一句话总结：一个让 Claude Code 从黑盒变透明的仪表盘插件...

✔ **核心洞见**：Claude Code 最大的痛点不是功能不足，而是"黑盒"体验...

✔ **技术细节**：基于 Claude Code 原生 statusline API 构建...

✔ **应用场景**：复杂任务重构、CI/CD 调试、长期项目开发...

**原文：** https://mp.weixin.qq.com/s/XClh6xJmXoXbyBC9lKzPdA
```

## 依赖

- `docai-web2md`（获取网页内容）
- [info-card-designer](https://github.com/joeseesun/info-card-designer)（可选，生成信息卡图片）

## 许可证

MIT