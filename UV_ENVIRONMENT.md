# UV 环境管理指南

本文档说明如何使用 **uv** 管理 docai-skills 的 Python 环境，**完全不影响系统全局 Python**。

## 🎯 核心优势

- ✅ **隔离环境**：所有依赖安装在项目目录内，不影响系统 Python
- ✅ **快速安装**：uv 比 pip 快 10-100 倍
- ✅ **版本锁定**：通过 `uv.lock` 确保依赖版本一致性
- ✅ **可移植性**：团队成员使用相同环境配置

## 📦 安装 uv（如果尚未安装）

```bash
# macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 Homebrew
brew install uv

# 验证安装
uv --version
```

## 🚀 快速开始

### 1. 初始化项目环境

```bash
cd docai-skills

# 创建虚拟环境并安装依赖
uv sync
```

**这会：**
- 在 `.venv/` 创建隔离的虚拟环境
- 安装 `pyproject.toml` 中的所有依赖
- 生成 `uv.lock` 锁定版本

### 2. 激活环境（可选）

```bash
# 激活虚拟环境
source .venv/bin/activate

# 之后可以直接使用 python
python skills/docai-web2md/tools/convert.py https://example.com

# 退出环境
deactivate
```

### 3. 在隔离环境中运行脚本（推荐方式）

```bash
# 方式 A: 使用 uv run（无需激活环境）
uv run python skills/docai-web2md/tools/convert.py https://example.com

# 方式 B: 使用 uv run 传递参数
uv run python skills/docai-web2summary/tools/summarize.py https://example.com --model sonnet

# 方式 C: 调用已安装的包
uv run python -c "from skills.docai_web2md.tools.convert import WebToMarkdown; print('OK')"
```

## 🔧 日常使用

### 安装新依赖

```bash
# 添加项目依赖（会更新 pyproject.toml 和 uv.lock）
uv add package-name

# 添加开发依赖
uv add --dev package-name

# 移除依赖
uv remove package-name
```

### 更新依赖

```bash
# 更新所有依赖到最新版本
uv sync --upgrade

# 更新特定依赖
uv sync --upgrade-package requests
```

### 查看环境信息

```bash
# 查看当前环境
uv show

# 查看已安装包
uv pip list

# 查看依赖树
uv tree
```

## 🎓 Skill 执行的三种方式

### 方式 1: 使用 uv run（推荐）

```bash
# 无需激活环境，直接执行
uv run python skills/docai-web2md/tools/convert.py https://breezedeus.com

# 保存到文件
uv run python skills/docai-web2md/tools/convert.py https://breezedeus.com -o article.md

# 总结网页
uv run python skills/docai-web2summary/tools/summarize.py https://arxiv.org/abs/2601.04500v1
```

**优点：**
- 自动使用项目虚拟环境
- 无需手动激活
- 脚本化友好

### 方式 2: 激活环境后使用

```bash
# 激活环境
source .venv/bin/activate

# 直接使用 python
python skills/docai-web2md/tools/convert.py https://breezedeus.com

# 退出
deactivate
```

**优点：**
- 开发时更方便
- 可以在 shell 中连续执行多个命令

### 方式 3: 使用绝对路径（不推荐）

```bash
# 直接调用虚拟环境中的 Python
.venv/bin/python skills/docai-web2md/tools/convert.py https://breezedeus.com
```

## 📋 与 Claude Code Skill 的集成

### 问题：Claude Code 调用 Skill 时使用什么环境？

**当前情况：**
- Claude Code 调用 Skill 时，使用的是**系统 Python 环境**
- 不会自动使用 `.venv` 或 `uv run`

### 解决方案

#### 方案 A: 全局安装依赖（简单，但影响全局）

```bash
# 使用 uv 安装到系统（不推荐，但最简单）
uv pip install requests beautifulsoup4 markdownify pymupdf --system
```

#### 方案 B: 修改 Skill 脚本，自动使用 uv 环境（推荐）

在 `tools/convert.py` 开头添加：

```python
#!/usr/bin/env python3
"""
Web to Markdown Converter
使用 uv 环境运行，确保依赖隔离
"""

import sys
import os
import subprocess

def ensure_uv_environment():
    """确保在 uv 虚拟环境中运行"""
    try:
        import requests
        return
    except ImportError:
        # 尝试使用 uv run 重新执行
        script_path = os.path.abspath(__file__)
        uv_cmd = ["uv", "run", "python", script_path] + sys.argv[1:]
        try:
            subprocess.run(uv_cmd, check=True)
            sys.exit(0)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("错误: 缺少依赖包")
            print("请运行: uv sync")
            sys.exit(1)

# 检查环境
ensure_uv_environment()

# 正常导入和执行
import requests
from bs4 import BeautifulSoup
# ... 其余代码
```

#### 方案 C: 创建包装脚本（最灵活）

创建 `run-with-uv.sh`：

```bash
#!/bin/bash
# 包装脚本：确保使用 uv 环境

cd "$(dirname "$0")/.."
uv run python "$@"
```

使用：
```bash
./run-with-uv.sh skills/docai-web2md/tools/convert.py https://example.com
```

## 🛠️ 开发工作流

### 1. 克隆项目后

```bash
git clone <repo>
cd docai-skills
uv sync
```

### 2. 开发新功能

```bash
# 激活环境
source .venv/bin/activate

# 编辑代码
vim skills/docai-web2md/tools/convert.py

# 测试
python skills/docai-web2md/tools/convert.py https://example.com

# 或使用 uv run
uv run python skills/docai-web2md/tools/convert.py https://example.com
```

### 3. 提交代码

```bash
# 确保 uv.lock 是最新的
git add pyproject.toml uv.lock
git commit -m "Update dependencies"
```

## 🔍 故障排除

### 问题 1: "ModuleNotFoundError"

```bash
# 检查是否在虚拟环境中
which python
# 应该显示: .../docai-skills/.venv/bin/python

# 如果不在，重新安装
uv sync

# 或直接使用 uv run
uv run python -c "import requests; print('OK')"
```

### 问题 2: 想要使用系统 Python

```bash
# 临时使用系统 Python（不推荐）
uv run --no-sync python script.py

# 或完全不使用 uv
python script.py  # 需要手动 pip install
```

### 问题 3: 清理环境

```bash
# 删除虚拟环境
rm -rf .venv

# 重新创建
uv sync
```

## 📊 性能对比

| 操作 | pip | uv | 提升 |
|------|-----|----|------|
| 冷缓存安装 | 60s | 2s | 30x |
| 增量安装 | 15s | 0.5s | 30x |
| 冻结依赖 | 10s | 0.2s | 50x |

## 🎯 推荐实践

### 对于个人开发

```bash
# 1. 安装 uv
# 2. 项目初始化
cd docai-skills
uv sync

# 3. 开发时
source .venv/bin/activate
# ... 开发 ...

# 4. 执行脚本
uv run python skills/docai-web2md/tools/convert.py URL
```

### 对于团队协作

```bash
# 1. 克隆项目
git clone <repo>

# 2. 一键安装
uv sync

# 3. 执行（无需激活环境）
uv run python skills/docai-web2md/tools/convert.py URL

# 4. 提交时包含 uv.lock
git add uv.lock pyproject.toml
```

### 对于 Claude Code Skill 集成

```bash
# 方案 1: 安装到系统（一次性）
uv pip install --system requests beautifulsoup4 markdownify pymupdf

# 方案 2: 使用包装脚本（推荐）
# 创建 ~/.claude/skills/docai-web2md/run.sh
#!/bin/bash
cd /path/to/docai-skills
uv run python tools/convert.py "$@"
```

## 📝 总结

**uv 环境管理的核心优势：**

1. **隔离性**：完全不影响系统 Python
2. **速度**：安装速度快 10-100 倍
3. **一致性**：通过 `uv.lock` 确保团队环境一致
4. **简单性**：`uv sync` 一键初始化

**推荐执行方式：**

```bash
# 开发时
uv sync                    # 初始化环境
source .venv/bin/activate  # 激活环境（可选）

# 执行脚本
uv run python skills/docai-web2md/tools/convert.py URL
```

**对于 Claude Code Skill：**
- 优先使用 `uv pip install --system` 安装依赖
- 或创建包装脚本自动使用 uv 环境