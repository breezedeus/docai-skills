# DocAI Skills Marketplace - 项目结构

## 完整目录树

```
docai-skills/
├── README.md                           # 项目总览
├── PROJECT_STRUCTURE.md                # 本文件 - 结构说明
├── pyproject.toml                      # Python 项目配置
├── uv.lock                             # 依赖锁定
│
└── skills/                             # Skill 集合目录
    ├── __init__.py                     # Python 包入口（可选）
    │
    ├── docai-web2md/                   # Skill 1: 网页转 Markdown
    │   ├── SKILL.md                   # ⭐ Claude Code Skill 定义
    │   ├── README.md                  # 工具使用说明
    │   └── tools/
    │       ├── convert.py             # 转换工具实现
    │       └── __init__.py
    │
    └── docai-web2summary/              # Skill 2: 网页智能总结
        ├── SKILL.md                   # ⭐ Claude Code Skill 定义
        ├── README.md                  # 使用说明
        ├── QUICKSTART.md              # 快速开始
        └── tools/
            ├── summarize.py           # 总结工具实现
            └── __init__.py
```

## 核心文件说明

### `skills/docai-web2md/SKILL.md`
**这是什么？**: Claude Code 识别和使用的 skill 定义文件

**格式要求**:
```markdown
---
name: docai-web2md
description: Use when needing to convert web pages to Markdown format
---

# Skill 内容...

## Overview
核心原理

## How to Use This Skill
详细步骤和代码示例
```

**关键点**:
- **YAML frontmatter**: 必须包含 `name` 和 `description`
- **description**: 以 "Use when..." 开头，描述触发条件
- **内容**: 指导 Claude 如何执行任务的步骤和代码
- **TDD 原则**: 遵循测试驱动开发

## 与传统 Python 库的区别

### ❌ 传统方式（我最初错误的做法）
```
skills/
└── my-skill/
    ├── SKILL.md          # 文档
    ├── __init__.py       # Python 包
    ├── core.py           # 实现代码
    └── tests/            # 测试
```

### ✅ 正确的 Claude Code Skill 方式

**基本结构（必需）：**
```
skills/
└── my-skill/
    └── SKILL.md          # ⭐ 唯一必需文件
```

**扩展结构（可选，用于复杂功能）：**
```
skills/
└── my-skill/
    ├── SKILL.md          # Skill 定义
    └── tools/            # 可执行工具
        ├── tool.py
        └── README.md
```

**为什么这样设计？**
- Claude Code skill 是**指导文档**，不是代码库
- Claude 读取文档后，**自己执行**代码
- `tools/` 目录用于需要独立执行的复杂工具
- 简单、直接、易于维护

## Skill 内容结构

### 1. Metadata (必需)
```markdown
---
name: skill-name
description: Use when [触发条件]
---
```

### 2. Overview (简短介绍)
- 这个 skill 做什么
- 核心原则

### 3. When to Use (使用场景)
- 什么时候用
- 什么时候不用

### 4. How to Use (核心 - 详细步骤)
- Step 1: 分析问题
- Step 2: 选择工具
- Step 3: 执行命令/代码
- Step 4: 处理特殊情况

### 5. Common Patterns (常用模式)
- 可复用的代码片段
- 最佳实践

### 6. Common Mistakes (常见错误)
- 错误示例 vs 正确示例
- 帮助避免陷阱

### 7. Testing (测试方法)
- 如何验证 skill 有效
- 测试用例

## 如何使用这些 Skills

### 方式 1: 直接复制到 Claude Code
```bash
# 将 skill 复制到 Claude Code 的 skills 目录
cp -r skills/docai-web2md ~/.claude/skills/

# 重启 Claude Code 或等待自动加载
```

### 方式 2: 通过 CLI 工具（待开发）
```bash
# 未来支持
marketplace install docai-web2md
```

### 方式 3: GitHub 集成（待开发）
```bash
# 从 GitHub 安装
/plugin install github.com/your-username/docai-skills/docai-web2md
```

## 如何调用已安装的 Skill

在 Claude Code 中：
```
用户: "帮我把 https://breezedeus.com 转换成 Markdown"

Claude: (读取 docai-web2md SKILL.md)
1. 分析 URL 类型
2. 选择合适的方法
3. 执行代码
4. 返回结果
```

## 开发新 Skill 的流程

### RED: 写测试场景
```markdown
## Testing
Test with:
1. Static page: https://breezedeus.com
2. Dynamic page: https://x.com/...
3. arXiv: https://arxiv.org/abs/...
```

### GREEN: 写最小 Skill
```markdown
---
name: docai-web2md
description: Use when needing to convert web pages to Markdown
---

# docai:convert2md

## Overview
Converts web pages to Markdown.

## How to Use
[提供基本步骤和代码]
```

### REFACTOR: 优化
- 添加更多示例
- 补充常见错误
- 添加特殊场景处理
- 优化描述和关键词

## 当前项目状态

✅ **已完成**:
- 项目结构创建
- Skill 1: docai-web2md (网页转 Markdown)
- Skill 2: docai-web2summary (网页智能总结)
- 符合 Claude Code skill 规范
- ✅ **微信公众号转换测试通过** (3395 字符)
- ✅ **arXiv 论文提取测试通过**
- ✅ **静态页面转换测试通过**
- ✅ **AI 结构化总结测试通过**

🔄 **待完成**:
- CLI 工具（安装/管理 skills）
- GitHub 集成（自动发现/下载）
- 更多 DocAI skills (pdf-extract, table-recognize, ocr...)

## 下一步建议

### 1. 测试 Skills
```bash
# 复制到 Claude Code
cp -r skills/docai-web2md ~/.claude/skills/
cp -r skills/docai-web2summary ~/.claude/skills/

# 在 Claude Code 中测试
# 输入: "帮我把 https://mp.weixin.qq.com/s/1LfkYdbzymoWxdvdnKeLnA 转换成 Markdown"
# 输入: "请总结这个链接：https://arxiv.org/abs/2601.04500v1"

# 或独立测试工具
uv run python skills/docai-web2md/tools/convert.py https://breezedeus.com
uv run python skills/docai-web2summary/tools/summarize.py https://breezedeus.com
```

### 2. 添加更多 Skills
```bash
skills/
├── docai-web2md/          # ✅ 已完成
├── docai-web2summary/     # ✅ 已完成
├── docai-pdf-extract/         # ⏳ 待创建
├── docai-table-recognize/     # ⏳ 待创建
└── docai-ocr/                 # ⏳ 待创建
```

### 3. 开发 CLI 工具
```python
# marketplace.py
# 功能: search, install, list, update
```

### 4. GitHub 集成
- 创建 GitHub 仓库
- 自动扫描 skills
- 提供安装命令

## 技术栈

| 组件 | 用途 |
|------|------|
| uv | 项目管理（可选） |
| Markdown | Skill 定义格式 |
| GitHub | Skill 存储和分发 |
| CLI 工具 | 安装和管理（待开发） |

## 参考资料

- [Claude Code Skills 规范](https://github.com/anthropics/claude-code-skills)
- [TDD for Skills](https://github.com/anthropics/claude-code-skills/blob/main/skills/writing-skills/SKILL.md)
