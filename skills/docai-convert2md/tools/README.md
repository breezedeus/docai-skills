# Web to Markdown 转换工具

这是一个独立的 Python 工具，用于将网页转换为 Markdown 格式。

## 安装依赖

```bash
# 基础依赖
pip install requests beautifulsoup4 markdownify

# 动态页面支持（可选）
pip install playwright
playwright install chromium
```

## 命令行使用

### 基本用法

```bash
# 转换静态页面
python convert.py https://example.com

# 转换并保存到文件
python convert.py https://example.com --output article.md

# 纯文本模式（无格式）
python convert.py https://example.com --pure-text

# 强制使用浏览器（动态页面）
python convert.py https://x.com/user/status/123 --use-browser
```

### 示例

```bash
# 1. 转换博客文章
python convert.py https://example.com/blog/post-123 -o post.md

# 2. 下载 arXiv 论文
python convert.py https://arxiv.org/abs/2401.12345 -o paper.md

# 3. 转换社交媒体内容
python convert.py https://x.com/OpenAI/status/1700000000000000000 --use-browser

# 4. 批量处理
for url in $(cat urls.txt); do
    python convert.py "$url" --output "docs/$(echo $url | md5).md"
    sleep 1  # 避免请求过快
done
```

## Python API 使用

```python
from convert import WebToMarkdown

converter = WebToMarkdown()

# 基本转换
markdown = converter.convert("https://example.com")

# 纯文本模式
text = converter.convert("https://example.com", pure_text=True)

# 强制浏览器
md = converter.convert("https://x.com/...", use_browser=True)

# arXiv 论文
paper = converter.convert("https://arxiv.org/abs/2401.12345")
```

## 功能特性

✅ **智能检测**
- 自动判断静态/动态页面
- 识别 arXiv 链接并转换
- 检测 SPA 应用

✅ **格式支持**
- Markdown 输出
- 纯文本输出
- 保留标题、列表、代码块

✅ **特殊处理**
- 微信公众号（移动 UA）
- X.com/Twitter
- arXiv 论文
- Medium/Substack

✅ **清理优化**
- 移除脚本和样式
- 过滤广告和 Cookie 提示
- 清理多余空白

## 性能参考

- 静态页面: ~1-2 秒
- 动态页面: ~5-10 秒
- arXiv PDF: ~2-5 秒
- 内存占用: ~100MB（浏览器模式）

## 常见问题

### Q: 提示 Playwright 未安装？
```bash
pip install playwright
playwright install chromium
```

### Q: 某些网站转换为空？
尝试强制使用浏览器：
```bash
python convert.py URL --use-browser
```

### Q: 如何处理登录后的页面？
需要手动获取 cookies：
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
# 运行测试
python convert.py https://example.com

# 检查输出
python convert.py https://example.com --output test.md
cat test.md

# 测试不同场景
python convert.py https://arxiv.org/abs/2401.12345
python convert.py https://x.com/OpenAI/status/1700000000000000000 --use-browser
```

## 许可证

MIT
