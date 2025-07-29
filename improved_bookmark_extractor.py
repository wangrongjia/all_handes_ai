#!/usr/bin/env python3
"""
书签内容提取器 (改进版)
从HTML书签链接中提取内容并转换为Markdown格式
参考Obsidian Pluck插件的实现
"""

import re
import os
import time
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import html2text
from datetime import datetime
import logging
import shutil

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImprovedBookmarkExtractor:
    def __init__(self, output_dir="extracted_bookmarks"):
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        })
        
        # 创建输出目录
        if os.path.exists(output_dir):
            # 清空目录
            logger.info(f"清空输出目录: {output_dir}")
            shutil.rmtree(output_dir)
        
        os.makedirs(output_dir, exist_ok=True)
            
        # 初始化html2text转换器
        self.h = html2text.HTML2Text()
        self.h.ignore_links = False
        self.h.ignore_images = False
        self.h.body_width = 0  # 不限制行宽
        self.h.unicode_snob = True  # 保留Unicode字符
        self.h.wrap_links = False  # 不换行链接
        self.h.inline_links = True  # 使用内联链接
        self.h.protect_links = True  # 保护链接
        self.h.mark_code = True  # 标记代码块
        
    def extract_links_from_html(self, html_content):
        """从HTML内容中提取链接"""
        links = []
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找所有的<a>标签
        for a_tag in soup.find_all('a', href=True):
            url = a_tag.get('href')
            title = a_tag.get_text().strip()
            
            # 过滤掉一些不需要的链接
            if self.is_valid_url(url):
                links.append({
                    'url': url,
                    'title': title
                })
        
        return links
    
    def is_valid_url(self, url):
        """检查URL是否有效"""
        try:
            parsed = urlparse(url)
            # 过滤掉一些不需要的URL
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # 过滤掉一些特殊的URL
            skip_domains = ['fssc-test.tineco.com']  # 测试域名等
            if any(domain in parsed.netloc for domain in skip_domains):
                return False
                
            return True
        except:
            return False
    
    def fetch_content(self, url):
        """获取网页内容"""
        try:
            logger.info(f"正在获取: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # 尝试检测编码
            if response.encoding == 'ISO-8859-1':
                # 可能是错误的编码检测，尝试使用apparent_encoding
                response.encoding = response.apparent_encoding
            
            # 如果还是没有正确的编码，默认使用utf-8
            if not response.encoding or response.encoding == 'ISO-8859-1':
                response.encoding = 'utf-8'
                
            return response.text
        except Exception as e:
            logger.error(f"获取 {url} 失败: {str(e)}")
            return None
    
    def clean_html(self, html_content):
        """清理HTML内容，移除不需要的元素"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 移除脚本和样式
        for tag in soup(['script', 'style', 'noscript', 'iframe', 'svg']):
            tag.decompose()
        
        # 移除隐藏元素
        for tag in soup.find_all(style=lambda value: value and ('display:none' in value or 'visibility:hidden' in value)):
            tag.decompose()
        
        # 移除空元素
        for tag in soup.find_all(lambda tag: tag.name not in ['br', 'hr', 'img'] and not tag.contents and not tag.string):
            tag.decompose()
        
        # 移除类名包含特定关键词的元素
        for tag in soup.find_all(class_=lambda value: value and any(x in value.lower() for x in ['nav', 'menu', 'footer', 'comment', 'sidebar', 'widget', 'banner', 'ad', 'header', 'cookie'])):
            tag.decompose()
        
        # 移除ID包含特定关键词的元素
        for tag in soup.find_all(id=lambda value: value and any(x in value.lower() for x in ['nav', 'menu', 'footer', 'comment', 'sidebar', 'widget', 'banner', 'ad', 'header', 'cookie'])):
            tag.decompose()
        
        return str(soup)
    
    def extract_main_content(self, html_content, url):
        """提取网页主要内容"""
        try:
            # 首先清理HTML
            cleaned_html = self.clean_html(html_content)
            soup = BeautifulSoup(cleaned_html, 'html.parser')
            
            # 获取网页标题
            title_tag = soup.find('title')
            title = title_tag.get_text() if title_tag else "无标题"
            
            # 尝试找到主要内容区域
            main_content = None
            
            # 网站特定处理
            domain = urlparse(url).netloc.lower()
            
            # V2EX特殊处理
            if 'v2ex.com' in domain:
                # 尝试找到帖子内容
                content_selectors = [
                    '.topic_content',
                    '.reply_content',
                    '.cell[id^="r_"]',
                    '.box .cell',
                    'div[class*="topic"]'
                ]
                for selector in content_selectors:
                    elements = soup.select(selector)
                    if elements:
                        # 如果找到多个元素，合并它们
                        if len(elements) > 1:
                            # 创建一个新的div来包含所有内容
                            main_content = soup.new_tag('div')
                            # 添加主题内容
                            topic_content = soup.select_one('.topic_content')
                            if topic_content:
                                main_content.append(topic_content)
                                
                            # 添加回复内容
                            for element in soup.select('.reply_content'):
                                # 添加分隔线
                                hr = soup.new_tag('hr')
                                main_content.append(hr)
                                main_content.append(element)
                        else:
                            main_content = elements[0]
                        break
            
            # 知乎特殊处理
            elif 'zhihu.com' in domain:
                content_selectors = [
                    '.RichContent-inner',
                    '.Post-RichTextContainer',
                    '.QuestionAnswer-content',
                    '.AnswerCard'
                ]
                for selector in content_selectors:
                    element = soup.select_one(selector)
                    if element:
                        main_content = element
                        break
            
            # 通用内容提取
            if not main_content:
                content_selectors = [
                    'article',
                    'main',
                    '.article',
                    '.post',
                    '.content',
                    '.post-content',
                    '.entry-content',
                    '.article-content',
                    '.article__content',
                    '.article-body',
                    '.article__body',
                    '.post-body',
                    '.post__body',
                    '#content',
                    '.main-content',
                    '.markdown-body'
                ]
                
                for selector in content_selectors:
                    element = soup.select_one(selector)
                    if element:
                        main_content = element
                        break
            
            # 如果还是没找到，尝试使用启发式方法
            if not main_content:
                # 查找包含最多段落的div
                divs = soup.find_all('div')
                max_p_count = 0
                max_p_div = None
                
                for div in divs:
                    p_count = len(div.find_all('p'))
                    if p_count > max_p_count:
                        max_p_count = p_count
                        max_p_div = div
                
                if max_p_div and max_p_count > 3:  # 至少有3个段落
                    main_content = max_p_div
            
            # 如果还是没找到，使用body
            if not main_content:
                main_content = soup.find('body')
            
            if main_content:
                # 转换为markdown
                markdown_content = self.h.handle(str(main_content))
                
                # 清理markdown内容
                markdown_content = self.clean_markdown(markdown_content)
                
                return {
                    'title': title,
                    'content': markdown_content.strip()
                }
            
            return None
            
        except Exception as e:
            logger.error(f"提取内容失败: {str(e)}")
            return None
    
    def clean_markdown(self, markdown_content):
        """清理Markdown内容"""
        # 移除多余的空行
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        # 修复列表格式
        markdown_content = re.sub(r'(\n\s*[-*]\s+[^\n]+)(\n\s*[^-*\s])', r'\1\n\2', markdown_content)
        
        # 修复标题格式
        markdown_content = re.sub(r'(\n#+)([^#\s])', r'\1 \2', markdown_content)
        
        # 修复链接格式
        markdown_content = re.sub(r'\[([^\]]+)\]\s+\(([^)]+)\)', r'[\1](\2)', markdown_content)
        
        return markdown_content
    
    def sanitize_filename(self, filename):
        """清理文件名"""
        # 移除或替换不合法的字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.strip()
        # 限制长度
        if len(filename) > 100:
            filename = filename[:100]
        return filename
    
    def save_markdown(self, title, url, content):
        """保存为Markdown文件"""
        try:
            # 创建文件名
            safe_title = self.sanitize_filename(title)
            filename = f"{safe_title}.md"
            filepath = os.path.join(self.output_dir, filename)
            
            # 如果文件已存在，添加序号
            counter = 1
            original_filepath = filepath
            while os.path.exists(filepath):
                name, ext = os.path.splitext(original_filepath)
                filepath = f"{name}_{counter}{ext}"
                counter += 1
            
            # 获取域名
            domain = urlparse(url).netloc
            
            # 创建Markdown内容
            markdown_content = f"""# {title}

**原始链接**: [{url}]({url})  
**来源网站**: {domain}  
**提取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

{content}
"""
            
            # 保存文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.info(f"已保存: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"保存文件失败: {str(e)}")
            return False
    
    def process_bookmarks(self, html_content):
        """处理书签"""
        # 提取链接
        links = self.extract_links_from_html(html_content)
        logger.info(f"找到 {len(links)} 个链接")
        
        success_count = 0
        
        for i, link in enumerate(links, 1):
            logger.info(f"处理第 {i}/{len(links)} 个链接: {link['title']}")
            
            # 获取网页内容
            html_content = self.fetch_content(link['url'])
            if not html_content:
                continue
            
            # 提取主要内容
            result = self.extract_main_content(html_content, link['url'])
            if not result:
                logger.warning(f"无法提取内容: {link['url']}")
                continue
            
            # 使用网页标题，如果提取失败则使用书签标题
            title = result['title'] or link['title']
            
            # 保存为Markdown
            if self.save_markdown(title, link['url'], result['content']):
                success_count += 1
            
            # 添加延迟避免被封
            time.sleep(2)
        
        logger.info(f"处理完成! 成功提取 {success_count}/{len(links)} 个文件")

def main():
    # 你的书签HTML内容
    bookmark_html = '''<a href="https://v2ex.com/t/1116255">V 友们求推荐手机卡 - V2EX</a><br/>
<a href="https://we0.ai/zh-CN">We0 -通过 AI 生成应用程序</a><br/>
<a href="https://www.v2ex.com/t/1120037#reply13">[开源] 扫描件 PDF 转 Markdown / EPUB，自动修复 OCR 错误 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1121476#reply13">使用 FFmpeg 和 GPU 实现最简"图片+无损音频=视频"的方法 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1122153#reply2">从零开始开发一个 MCP Server！ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/935608">分享一下我学习英语的经验 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1124615">Grok API 充 $5 终身每月获得 150 美元 API 额度 - V2EX</a><br/>
<a href="https://www.iplaysoft.com/grok.html">手把手教你薅马斯克 xAI 的 Grok 3 大羊毛：充 $5 终身每月获得 150 美元 API 额度！ - 异次元软件下载</a><br/>
<a href="https://console.x.ai/team/35bca65d-22bc-4856-b03a-77c4847f51df/api-keys">API keys | xAI Cloud Console</a><br/>
<a href="https://www.v2ex.com/t/1124507">最近吉卜力风格比较火，那我就做一个… 把吉卜力图片变成视频的工具 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1124516">gpt4o 图像生成的技术讨论(自回归模型又好起来了?) - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1124534">我的第一款 AI 应用–AI 群聊–制作全过程 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1124653">Build 了一个小红书 MCP - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1124691">31 岁了，是在银行继续苟着，还是富贵险中求？兄弟们怎么看 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1124698">风控系统选型求助 - V2EX</a><br/>
<a href="https://ghiblio.art/zh">Ghiblio - 吉卜力风格图像生成器｜完全免费无限生成 ｜ChatGPT 4o驱动</a><br/>
<a href="https://www.v2ex.com/t/1124154#reply271">开发完成一个吉卜力图片生成器，基于 GPT 4o - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1124645#reply26">xdm， 2025 年了还有低于 5 元套餐的手机卡不 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1125133">晚上出去推垃圾筒，发现皓月当空，久违了，大厂被裁八个月的救赎之路 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1125006">肝了一篇 Google Agent2Agent 协议的介绍 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1125750#reply37">『经过 jingguo.org』 一个真正开放的经验分享社区 - V2EX</a><br/>
<a href="https://fssc-test.tineco.com/report/?appId=11ecb24d7e9e6c0ba360657b09d5cc74&serviceName=fssc&menuId=11efff1ccd62191189e1e75b58eabcbd&menuName=&lang=zh_CN&TOKEN=11f02a18f9ab2599a68f7dd13f3551a0&securityFlag=false&timeDelta=223&logoutTargetUrl=https%3A%2F%2Ffssc-test.tineco.com%2Fecs_console%2Findex.html%23%2Flogin&sandboxId=default&origin=https%3A%2F%2Ffssc-test.tineco.com%2Fecs_console%2Findex.html&newHomePageDesignerEnable=false&oauthToken=&openMode=browserTab">编号</a><br/>
<a href="https://www.v2ex.com/t/1130612#reply38">第一次跑 JD 外卖总结 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1131052#reply20">有没有可以抵个税的相关容易比较获得的证书？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1022439#reply119">基于 LangChain 的开源 GPT 向量 + 知识数据库，帮助个人或企业实现自己的专属 AI 问答助手 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1131533">开发了一款视频播放器 Medianex,目前正式开启公测，通过插件化的设计可以支持接入任意云盘，支持自动生成海报墙，支持 Linux 、Windows、Macos，希望您可以喜欢 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1131548">早就听说过 ffmpeg，但是一直不知道有多牛 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1131621#reply42">35 岁+程序员， Gap 10 个月后成功再就业，一点经历分享 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/982974">大佬们，厨房净水器和智能门锁有推荐的吗 价格一千多到三千都可以！ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1056504#reply272">大家都是草台班子😂，我干了这么多年开发，能把跨域问题说清楚的人也没几个😅 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1129675#reply13">咱 web 端也能跑本地知识库,RAG(傲娇)-篇章 1-核心技术方案 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1132458">国内还有活跃的编程 UP 主吗? - V2EX</a><br/>
<a href="https://www.v2ex.com/t/805299">吐槽下小米净水器，体验极差 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1133021">华为云新的 1000 券活动又来了，整理了一下流程 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1133051">非常适合独立开发，没有设计稿也能很漂亮： Trae + 飞个马 MCP - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1133062">大龄小白请教:跨域问题 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1132910#reply264">我写了一个编程语言，受 golang 启发 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1133074#reply46">小孩发烧你们是吃布洛芬观察 2 天还是立马送医院 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1133186#reply202">这个世界无时无刻不再刷新我的三观 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1133227#reply9">刚才网上瞎逛，突然看到这张图片，不知道说什么了 - V2EX</a><br/>
<a href="https://ciechanow.ski/gps/">GPS – Bartosz Ciechanowski --- GPS – Bartosz Ciechanowski</a><br/>
<a href="https://v2ex.com/t/862672">用户可以交互的教程，形式很棒，可问题是怎么制作呢？为神马没有合适的工具？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1134159">折腾了自媒体一年 500 个视频，收入¥2000，我悟了个锤子！ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1134160">数字游民,泰国旅居半年 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1134286#reply26">前置过滤器+净水器+直饮机，可以无脑买小米吗 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1102858#reply28">我研发了一个 AI 智能体变现平台 - xaisite.com - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1134350#reply1">也说说对泰国旅游甚至定居的一点点感受和看法 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1134160#reply59">数字游民,泰国旅居半年 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1135022">jetbrain 系的 ide 有比较好的 ai 编程解决方案吗？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1135034">在英国做实习开发的一些体验分享 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1135040">多少钱能搞个本地大模型环境 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1135100#reply30">广州买哪个牌子电鸡性价比高 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1135063#reply55">路边停车，各位都是如何应对的？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1134914#reply48">湿疹如何治疗？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1135238">国内好多提供 OpenAI 等大模型服务的收费中转站 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1135237">开源了 AI 翻译和深度学习语言的浏览器插件 - 陪读蛙 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1135250#reply18">告别阿里云：一个合作十年以上老用户的心碎经历 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1134678#reply285">颠覆你对学英语的认知！ Ries 如何让你在看 B 站或阅读中「无痛」猛增英语接触 (全程上图) - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1137300#reply199">老哥们，你们的话费一个月都是多少钱？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1137586#reply52">让 AI 根据浏览器请求的路径，现场制作 HTML - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1137799#reply29">贵州不够科技收购开源软件的目的是什么？ - V2EX</a><br/>
<a href="https://zhuanlan.zhihu.com/p/28399704">交通事故----浅谈三不一没有 - 知乎</a><br/>
<a href="https://www.v2ex.com/t/1138160#reply79">小红书现在各种暗广告也太多了吧？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1138465">求推荐 chrome 和 edge 的插件，下载视频 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1138862#reply20">分享下我的几个落地副业，其实赚钱就应该多和年轻一代多沟通交流。 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1139018">失业程序员来柬埔寨创业记录 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1139036">夏天到了，保护腰椎和肩颈，自学游泳开始了，有成功的没？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1139460#reply6">国内有那种聚合搜索影视资源的工具吗？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1139271#reply30">30 岁之后，开发转 PM 是不是必须的呢 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1139800">花两天写了个"张雪峰"提示词，让 AI 免费做志愿规划（附全文） - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1139766">记一次以失败而告终的小区（集体）维权经历 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1140276#reply12">dify 好用吗，还是直接用 mcp 手撸更靠谱 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1140195#reply33">开车被路中间石头顶坏底盘处理（没有豪车命，得了豪车病） - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1140454#reply15">有哪些体力活可以干 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1140580#reply38">上班开车途中被饿了么骑手撞了，一天心情全无 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1140565#reply72">找了个神仙工作，时间多能干点啥？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1140585#reply19">7 年 Java 后端经验，简历求意见 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1140599#reply13">推荐一下大伙用过的免费好用的服务 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1140656#reply206">25 应届，月薪 7k，未来迷茫 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1140738#reply30">如何主动失信，成为黑户。不能网贷借钱 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1140906#reply98">感觉自己被京东和浦发银行骗了。希望广大网友引以为戒。 - V2EX (2)</a><br/>
<a href="https://www.v2ex.com/t/1141852#reply25">上半年干的最重要的一件事：提交了新西兰居民签申请 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1141868#reply34">记录最近一次看病经历，小病熬成大问题，看病真难 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1142365">深夜推荐蟑螂药，效果太好了强烈推荐 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1142258#reply55">在经济条件允许的条件下，尽量吃原研药 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1142748">小红书 App 帖子的图片都是明文传输的，网络提供者可以完全看到你浏览的实际内容 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1142776">Text2SQL（NL2SQL， 大模型问数据库）有什么成熟、准确率高的解决方案？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1142782">怪事一桩 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1142850">电车开了 3 年 发现省钱不省油 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1142888">[广州]连续创业者，技术开发老人求职（二） - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1142868">程序员为什么要出海赚美刀？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1142858">咸鱼出 switch 游戏机现在感觉被骗了 掉包我的内存卡 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1142915">现在的 AI 编程工具，分别是用什么原理生成索引来理解代码库的？哪个工具的效果最好？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1143060">求推荐按流量计费的机场，稳定性价比高 - V2EX (1)</a><br/>
<a href="https://www.v2ex.com/t/1143057">毕业五年，从前端走到裁员，短期过渡？ - V2EX (1)</a><br/>
<a href="https://www.v2ex.com/t/1143223#reply93">高三毕业生出国留学求助 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1143286#reply47">网上卖的 DIY 净水器靠谱吗？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1143351">大家有什么有意思的 telegram 群组或者频道 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1143377#reply44">谈一谈兼职朴朴超市骑手的感想 - V2EX</a><br/>
'''
    
    extractor = ImprovedBookmarkExtractor()
    extractor.process_bookmarks(bookmark_html)

if __name__ == "__main__":
    main()