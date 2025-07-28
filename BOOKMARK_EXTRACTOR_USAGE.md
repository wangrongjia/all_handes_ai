# 书签内容提取器使用说明

## 概述

`bookmark_extractor.py` 是一个用于从HTML书签中提取网页内容并转换为Markdown格式的Python脚本。

## 功能特点

- 🔍 自动解析HTML书签链接
- 🎯 智能识别V2EX网站链接
- 📄 提取网页主要内容
- 📝 转换为Markdown格式
- 💾 自动保存到本地文件
- 🚫 避免重复文件名冲突
- ⏱️ 请求延迟防止被封

## 安装依赖

```bash
pip install requests beautifulsoup4 html2text
```

## 使用方法

### 1. 准备书签HTML内容

将你的浏览器书签导出为HTML格式，或者直接复制书签的HTML代码。

### 2. 修改脚本中的书签内容

在脚本的 `main()` 函数中，将 `bookmark_html` 变量替换为你的书签HTML内容：

```python
def main():
    # 你的书签HTML内容
    bookmark_html = '''
    <a href="https://example.com">示例链接</a><br/>
    <a href="https://v2ex.com/t/123456">V2EX帖子</a><br/>
    '''
    
    # 创建提取器并处理书签
    extractor = BookmarkExtractor()
    extractor.process_bookmarks(bookmark_html)
```

### 3. 运行脚本

```bash
python bookmark_extractor.py
```

### 4. 查看结果

脚本会在当前目录下创建 `extracted_bookmarks` 文件夹，包含所有提取的Markdown文件。

## 配置选项

### 输出目录

可以在创建 `BookmarkExtractor` 实例时指定输出目录：

```python
extractor = BookmarkExtractor(output_dir="my_bookmarks")
```

### 请求延迟

脚本默认在每个请求之间等待2秒，可以在 `process_bookmarks` 方法中修改：

```python
# 添加延迟避免被封
time.sleep(2)  # 修改这个值来调整延迟时间
```

## 支持的网站

目前脚本针对V2EX网站进行了特殊优化，但也可以处理其他网站的内容。对于V2EX，脚本会：

- 自动识别帖子内容区域
- 提取主要讨论内容
- 保留原始链接信息

## 输出格式

每个生成的Markdown文件包含：

```markdown
# 文章标题

**原始链接**: https://example.com
**提取时间**: 2025-07-28 10:23:16

---

文章内容...
```

## 错误处理

脚本包含完善的错误处理机制：

- 网络请求失败时会记录错误并继续处理下一个链接
- 内容提取失败时会跳过该链接
- 文件保存失败时会记录错误信息

## 注意事项

1. **请求频率**: 脚本包含延迟机制，避免对目标网站造成过大压力
2. **编码问题**: 部分网站可能存在编码问题，脚本会尝试自动处理
3. **文件名处理**: 特殊字符会被替换为下划线，避免文件系统兼容性问题
4. **重复文件**: 如果存在重复标题，会自动添加序号区分

## 扩展功能

### 添加新网站支持

在 `extract_main_content` 方法中添加针对特定网站的内容提取逻辑：

```python
# 新网站特殊处理
if 'newsite.com' in url:
    content_selectors = [
        '.post-content',
        '.article-body'
    ]
    for selector in content_selectors:
        element = soup.select_one(selector)
        if element:
            main_content = element
            break
```

### 自定义过滤规则

在 `is_valid_url` 方法中添加自定义的URL过滤规则：

```python
def is_valid_url(self, url):
    # 添加自定义过滤逻辑
    if 'unwanted-site.com' in url:
        return False
    return True
```

## 故障排除

### 常见问题

1. **依赖包安装失败**: 确保Python版本兼容，使用虚拟环境
2. **网络连接问题**: 检查网络连接，考虑使用代理
3. **编码错误**: 确保系统支持UTF-8编码
4. **权限问题**: 确保有写入文件的权限

### 调试模式

可以修改日志级别来获取更详细的调试信息：

```python
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

## 许可证

此脚本仅供学习和个人使用，请遵守目标网站的使用条款和robots.txt规则。