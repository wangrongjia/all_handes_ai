#!/usr/bin/env python3
"""
书签内容提取器
从HTML书签链接中提取内容并转换为Markdown格式
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

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BookmarkExtractor:
    def __init__(self, output_dir="extracted_bookmarks"):
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # 初始化html2text转换器
        self.h = html2text.HTML2Text()
        self.h.ignore_links = False
        self.h.ignore_images = False
        self.h.body_width = 0  # 不限制行宽
        
    def extract_links_from_html(self, html_content):
        """从HTML内容中提取链接"""
        links = []
        # 使用正则表达式提取所有的<a>标签
        pattern = r'<a href="([^"]+)">([^<]+)</a>'
        matches = re.findall(pattern, html_content)
        
        for url, title in matches:
            # 过滤掉一些不需要的链接
            if self.is_valid_url(url):
                links.append({
                    'url': url,
                    'title': title.strip()
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
            response.encoding = response.apparent_encoding or 'utf-8'
            return response.text
        except Exception as e:
            logger.error(f"获取 {url} 失败: {str(e)}")
            return None
    
    def extract_main_content(self, html_content, url):
        """提取网页主要内容"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 移除不需要的元素
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # 尝试找到主要内容区域
            main_content = None
            
            # V2EX特殊处理
            if 'v2ex.com' in url:
                # 尝试找到帖子内容
                content_selectors = [
                    '.topic_content',
                    '.cell[id^="r_"]',
                    '.box .cell',
                    'div[class*="topic"]'
                ]
                for selector in content_selectors:
                    elements = soup.select(selector)
                    if elements:
                        main_content = elements[0]
                        break
            
            # 通用内容提取
            if not main_content:
                content_selectors = [
                    'article',
                    'main',
                    '.content',
                    '.post-content',
                    '.entry-content',
                    '#content',
                    '.main-content'
                ]
                
                for selector in content_selectors:
                    element = soup.select_one(selector)
                    if element:
                        main_content = element
                        break
            
            # 如果还是没找到，使用body
            if not main_content:
                main_content = soup.find('body')
            
            if main_content:
                # 转换为markdown
                markdown_content = self.h.handle(str(main_content))
                return markdown_content.strip()
            
            return None
            
        except Exception as e:
            logger.error(f"提取内容失败: {str(e)}")
            return None
    
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
            
            # 创建Markdown内容
            markdown_content = f"""# {title}

**原始链接**: {url}
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
        
        # 过滤V2EX链接
        v2ex_links = [link for link in links if 'v2ex.com' in link['url']]
        logger.info(f"其中 {len(v2ex_links)} 个V2EX链接")
        
        success_count = 0
        
        for i, link in enumerate(v2ex_links, 1):
            logger.info(f"处理第 {i}/{len(v2ex_links)} 个链接")
            
            # 获取网页内容
            html_content = self.fetch_content(link['url'])
            if not html_content:
                continue
            
            # 提取主要内容
            content = self.extract_main_content(html_content, link['url'])
            if not content:
                logger.warning(f"无法提取内容: {link['url']}")
                continue
            
            # 保存为Markdown
            if self.save_markdown(link['title'], link['url'], content):
                success_count += 1
            
            # 添加延迟避免被封
            time.sleep(2)
        
        logger.info(f"处理完成! 成功提取 {success_count}/{len(v2ex_links)} 个文件")

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
<a href="https://www.v2ex.com/t/1143223#reply100">高三毕业生出国留学求助 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1143631#reply21">$v2ex 都买了吗？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1143676#reply27">请问 2025 还有 DDD 成功有名的公司案例吗? - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1143804">问大家一个问题，闲鱼那么多光明正大卖盗版的为啥没人管？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1143846">装修房子，求大家给提一些建议 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1143850">求职，开发 转 软件实施或软件技术支持 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1143874">外包 offer 二选一 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1143879">水深火热的美国人民，只有 Direct Peer 的运营商是正常速度，没有 Direct Peer 都是百兆，出国更是 ADSL - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1143930">技术入股怎么跟老板谈 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1144046">以婚化债，都成产业链了 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1144407">2025 年 7 月，中国大陆居民如何尽可能合法且方便的获取并使用虚拟币？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1144414">来自一个京东外卖众包的吐槽！~ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1144443">vscode 历经几个版本的更新，现在 AI 体验已经相当不错了 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1144435">最近在研究欧洲出海，做了个欧洲电商出海资料站，欢迎一起交流踩坑 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1144238#reply81">低学历没技能该何去何从 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1144388#reply23">使用 Claude Code 中转商的风险 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1144188#reply131">近视手术的一些分享 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/982914">我的至暗时刻，大批微信小程序遭破解，多年心血被盗版。 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1144553#reply12">微信小游戏如何防止被破解 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1144459#reply32">纠纷双方报警进入派出所，大家分析下，在线等 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1144851#reply48">把每天的 V2 热帖都转成播客 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1144769#reply96">房东和雇佣的马仔抢我取证的手机不违法？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1144952#reply151">快 30 了，想润 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1145135#reply33">搞出了一套批量生产 AI 插画的系统，用它接过单，不过客户给价太低没继续做下去。 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1145013#reply100">Manus 彻底撤出中国，社交账号清空同时官网拒绝中国 IP 访问 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1145279#reply35">说说自己在小红书和某平台找过的陪玩，搭子和地陪的经历。方便大家理解 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1145468#reply30">智能马桶好用吗？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1145558#reply3">尝试 WPF 的桌面开发后，感觉 electron 真好 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1145836">Claude Code + Kiro Spec：别急着生成代码，先让 AI 理解你的需求 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1145750#reply36">Claude-code 是否真的可以投入生产 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1145809#reply274">夫妻矛盾 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146449#reply62">程序员转行从事餐饮业近十年，有问必答。 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146397#reply92">人到中年，还是没躲过这一刀， 被裁了，但是...... - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146360#reply38">油管为什么不给我流量？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146461#reply8">各位是收到 offer 马上提离职还是等背调完成？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146624#reply14">AI Coding "新时代的剥削工具" - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146397#reply119">人到中年，还是没躲过这一刀， 被裁了，但是...... - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146540#reply46">怀疑自己是不是真的很冷漠 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146449#reply108">程序员转行从事餐饮业近十年，有问必答。 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146625#reply105">工作 6 年，攒了 50 万存款，可以回家躺平或者寻找人生新的意义吗？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146614#reply82">不情愿刷 leetcode 是否一定程度上能鉴定一个人对码农这个职业的兴趣和"资质" - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146548#reply171">[求助帖] 小孩子性格倔强、软硬不吃、油盐不进该怎么教育呀 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146774#reply117">黄仁勋：我总感觉公司快要倒闭了 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146820#reply56">工作上的事情求助一下,感谢。 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146817#reply77">兄弟们，昨晚追尾了出租车，私了给了 1200，各位以后雨天开车小心点。 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146791#reply51">我看了一组数据，男性死亡中位数的年龄是 67.7，而女性的是 79.7 岁，相差 12 岁。 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1146808#reply58">记一次误诊经历 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1147051#reply17">9 月 15 正式实施的《租房租赁条例》这么解读？ - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1147151#reply72">今天提一个关于情侣的问题 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1147090#reply53">裸辞了，打算转行干家装 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1147362#reply26">都说就业环境差，可是为什么招人这么难呢 - 招聘有感 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1147296#reply42">小团队开发测试环境怎么解决 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1147320#reply65">如何看待近期懂车帝高速驾驶辅助测试榜单 - V2EX</a><br/>
<a href="https://v2ex.com/t/484768">有什么好玩容易上手的桌游推荐？ - V2EX</a><br/>
<a href="https://www.chipstrat.com/p/gpu-networking-basics-part-1">GPU 网络基础，第一部分 - 作者：奥斯汀·莱昂斯 - Chipstrat --- GPU Networking Basics, Part 1 - by Austin Lyons - Chipstrat</a><br/>
<a href="https://www.v2ex.com/t/1148014#reply62">为什么大部分人会觉得 24 节气是农历专有 - V2EX</a><br/>
<a href="https://www.v2ex.com/t/1147996#reply12">你会买你们公司的产品么？ - V2EX</a><br/>'''
    
    # 创建提取器并处理书签
    extractor = BookmarkExtractor()
    extractor.process_bookmarks(bookmark_html)

if __name__ == "__main__":
    main()