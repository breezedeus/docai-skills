# Web to Markdown 转换工具

这是一个独立的 Python 工具，用于将网页转换为 Markdown 格式。

**核心原则：优先使用非Python方法，Python作为回退**

## 优先级方法

1. **Jina Reader API** (⭐ 推荐) - 零安装，一行URL转换
2. **Firecrawl API** - 需要API密钥，功能强大
3. **Python实现** - 以上方法失败时的回退

## 安装依赖

```bash
# 基础依赖（仅用于Python回退方法）
pip install requests beautifulsoup4 markdownify

# PDF支持（arXiv论文）
pip install pymupdf

# 动态页面支持（可选，Python回退）
pip install playwright
playwright install chromium
```

## 命令行使用

### 基本用法（自动优先级）

```bash
# 使用优先级方法（自动尝试Jina Reader）
python convert.py https://example.com

# 转换并保存到文件
python convert.py https://example.com --output article.md

# 纯文本模式（无格式）
python convert.py https://example.com --pure-text
```

### 强制使用Python方法

```bash
# 跳过Jina/Firecrawl，直接使用Python实现
python convert.py https://example.com --use-python
```

### Jina Reader（零安装方法）

```bash
# 直接在浏览器中访问
https://r.jina.ai/https://example.com

# 或使用 curl
curl https://r.jina.ai/https://example.com
```

### 示例

```bash
# 1. 转换博客文章（自动使用Jina Reader）
python convert.py https://example.com/blog/post-123 -o post.md

# 2. 下载 arXiv 论文（PDF提取）
python convert.py https://arxiv.org/abs/2401.12345 -o paper.md

# 3. 强制使用Python方法（动态页面）
python convert.py https://x.com/OpenAI/status/1700000000000000000 --use-python

# 4. 批量处理（优先级方法）
for url in $(cat urls.txt); do
    python convert.py "$url" --output "docs/$(echo $url | md5).md"
    sleep 1
done
```

## Python API 使用

```python
from convert import WebToMarkdown

converter = WebToMarkdown()

# 基本转换（自动优先级）
markdown = converter.convert("https://example.com")

# 纯文本模式
text = converter.convert("https://example.com", pure_text=True)

# 强制使用Python方法
md = converter.convert("https://x.com/...", use_python=True)

# arXiv 论文
paper = converter.convert("https://arxiv.org/abs/2401.12345")

# 使用 Firecrawl（需要设置环境变量 FIRECRAWL_API_KEY）
# converter.firecrawl_api_key = "your-key"
```

## 功能特性

✅ **优先级架构**
- Jina Reader API 优先（零安装）
- Firecrawl API 次之（需API密钥）
- Python实现作为回退

✅ **格式支持**
- Markdown 输出
- 纯文本输出
- 保留标题、列表、代码块

✅ **特殊处理**
- 微信公众号（移动 UA）
- arXiv 论文（PDF提取）
- X.com/Twitter
- Medium/Substack

✅ **清理优化**
- 移除脚本和样式
- 过滤广告和 Cookie 提示
- 清理多余空白

## 性能参考

- **Jina Reader**: ~1-2 秒（API调用）
- **Firecrawl**: ~2-5 秒（API调用）
- **Python静态**: ~1-2 秒
- **Python动态**: ~5-10 秒
- **arXiv PDF**: ~2-5 秒

## 常见问题

### Q: 为什么优先使用 Jina Reader？
**A:** 零安装、速度快、无需配置，适合大多数场景。

### Q: 如何使用 Firecrawl？
```bash
export FIRECRAWL_API_KEY=your_key
python convert.py https://example.com
```

### Q: 某些网站转换为空？
**A:** 尝试强制使用Python方法：
```bash
python convert.py URL --use-python
```

### Q: 如何处理登录后的页面？
**A:** 需要手动获取 cookies：
```python
converter.session.cookies.set('session', 'your-cookie')
```

### Q: 支持批量处理吗？
```bash
# 简单的批量处理脚本
while read url; do
    python convert.py "$url" --output "output/$(date +%s).md"
    sleep 1
done < urls.txt
```

## 与 Claude Code Skill 的关系

这个工具是 `docai-convert2md` skill 的**可执行部分**。

**Skill 定义** (`../SKILL.md`):
- 指导 Claude 如何使用这个工具
- 提供使用场景和最佳实践
- 包含错误处理指南

**工具** (`convert.py`):
- 实际执行转换的代码
- 可以独立使用
- 也可以被 Claude 调用

## 开发和测试

```bash
# 运行测试（自动优先级）
python convert.py https://example.com

# 检查输出
python convert.py https://example.com --output test.md
cat test.md

# 测试不同场景
python convert.py https://arxiv.org/abs/2401.12345
python convert.py https://example.com --use-python  # 强制Python方法
```

## 许可证

MIT
