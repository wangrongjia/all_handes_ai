# Build 了一个小红书 MCP - V2EX

**原始链接**: [https://www.v2ex.com/t/1124653](https://www.v2ex.com/t/1124653)  
**来源网站**: www.v2ex.com  
**提取时间**: 2025-07-29 01:18:28

---

昨天花了几个小时 Build 了一个小红书 MCP ，评估过 playwright 和 browser-use ，最后选择了前者，后面我也会支持一下后者就是了，两者各有优缺点，我们的 Project 里会用到这个，比起单出通过请求接口的方式去 fetch 内容，还是模拟用户请求在应对反爬上更加轻松低 effort 。

目前支持了 2 个 tool ，一个 login （也可以通过命令行，方便某些场景提前登录好），一个 search_notes 作搜索 topk 笔记内容和相关的信息

我其实有想过 login 让他返回二维码 base64 ，然后 mcp-client 去 open 这个图给用户扫码，但是考虑到有些场景还要做烦人的验证码二次验证，暂时就没这样尝试了

佬们，轻点骂～

<https://github.com/ifuryst/rednote-mcp>
