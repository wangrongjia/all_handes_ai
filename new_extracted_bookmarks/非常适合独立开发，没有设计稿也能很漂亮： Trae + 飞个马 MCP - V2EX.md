# 非常适合独立开发，没有设计稿也能很漂亮： Trae + 飞个马 MCP - V2EX

**原始链接**: [https://www.v2ex.com/t/1133051](https://www.v2ex.com/t/1133051)  
**来源网站**: www.v2ex.com  
**提取时间**: 2025-07-29 01:19:18

---

# 没有设计稿也能很漂亮，非常适合独立开发：Trae + 飞个马 MCP

大家好，我是一名前端工程师，也是开源图片编辑器[vue-fabric-editor](<https://github.com/ikuaitu/vue-fabric-editor>)项目的作者，最近一直在迭代我们的商业版图片编辑器😍，因为团队规模比较小，**没有专门的设计师，就尝试使用 Trae + figma + MCP 来优化页面样式，没想到效果超级棒，真的惊艳到我了，** 非常适合没有设计师提供设计稿的小团队或者独立开发者。

作为一个工作十余年的切图仔，真的觉得是在解放生产力，这里做一下使用的简单介绍，推荐给大家。

# 说明

大部分开发者都希望一键生成，目前看多少还是有点噱头的，直接生成 HTML 可以，但是要生成完整可运行的代码，稍微加点业务逻辑就不行了，但是**换个思路，稍微调整一下步骤，就出现了事半功倍的效果** 。

> 我的思路是先**开发功能，再调整样式** ，使用起来效果就很好。

我们的步骤是先让实习的同事做功能开发，把调用接口和展示逻辑开发完成，**但是一般页面都会素素的，很没有食欲**(别笑，你写也不行...)， 如下图：

![image.png](https://dev-api.kuaitu.cc/uploads/1_43d5619cef.png)

然后我再通过 Trae + figma + MCP 来做样式优化，这是优化完成的效果，下边是调整后的效果：

![image.png](https://dev-api.kuaitu.cc/uploads/2_bf4851338e.png)

样式优化的结果我很满意的，另外我只是在 AI 的结果上做了轻微少量的调整，真的很高效。

# 如何使用

一共分为 5 步，前 2 个步骤只需要设置一次，几分钟搞定，后续直接使用就可以。

  1. 获取 Figma 账号 Token 。
  2. Trae 设置 MCP Token 。
  3. Figma 挑选喜欢的模板
  4. 复制元素链接并交给 AI ，预览结果
  5. 微调 上线。

### 1\. 获取 Figma 账号 Token 。

登录后从设置页面，生成 Token ，权限选择只读。

![20250520094828.png](https://dev-api.kuaitu.cc/uploads/3_951281cf45.png)

![image.png](https://dev-api.kuaitu.cc/uploads/4_8add066a07.png)

![image.png](https://dev-api.kuaitu.cc/uploads/5_27779878ac.png)

### 2\. Trae 设置 MCP Token

搞前端 Trae 还不知道就不说了，这么漂亮的编辑器，用起来很顺手，我是不舍得换了。 AI 对话框点击设置 => MCP ，然后点击添加，搜索 Figma AI Bridge ，安装后设置 Token 就可以了。

![image.png](https://dev-api.kuaitu.cc/uploads/6_0ce5aebf43.png)

![image.png](https://dev-api.kuaitu.cc/uploads/7_2c2230ab65.png)

![image.png](https://dev-api.kuaitu.cc/uploads/8_abea1a7935.png)

好了，这些设置只需要 1 次，设置完以后就不用每次调整了，接下来就是使用了。

### 3\. Figma 挑选喜欢的模板

接下来就很简单了，在 Figma 网站上挑选自己喜欢的模板，我搜索的关键词是 `dashboard`，可以挑选一些和现有页面机构类似的效果图。

![image.png](https://dev-api.kuaitu.cc/uploads/9_e8b421b37a.png)

这是我挑选的几个效果图：

![image.png](https://dev-api.kuaitu.cc/uploads/10_ea63d0d5dd.png)

![image.png](https://dev-api.kuaitu.cc/uploads/11_e9c01241e9.png)

### 4\. 复制元素链接并交给 AI ，预览结果

Figma 可以直接定位到某个元素的链接，我们选中一个区域后，右键复制链接。

![image.png](https://dev-api.kuaitu.cc/uploads/12_1ca418b41c.png)

然后在 Trae 的 AI 对话框中选择智能体，把链接复制上，并选中要调优的代码，把你的需求告诉 AI 。

![image.png](https://dev-api.kuaitu.cc/uploads/13_bdd596094a.png)

![image.png](https://dev-api.kuaitu.cc/uploads/14_c3b0266cc6.png)

### 5\. 微调 上线

相比比较我们自己手写很多样式去调整，AI 的效率很高了，好描述好理解的就交给 AI ，**简单的就自己手动调整一下**(别太懒，AI 再智能就没工作了😂)。

![image.png](https://dev-api.kuaitu.cc/uploads/15_f91a2f45a1.png)

# 结尾

自己也算是一个比较资深的切图仔了，从网页三剑客的 Dreamweaver 写 Table 布局开始，再到 Sublime 的快捷键编写网页，再到 VScode ，再到现在的 AI 类智能编辑器，真的是翻天覆地的变化。

我很认同在某个播客采访中提到的一个观点：**积极的拥抱 AI 吧，未来是属于会用好 AI 的人。**

最后，为我们的开源图片编辑器 <https://github.com/ikuaitu/vue-fabric-editor> 拉个粉，大家 Star 一下吧。

![image.png](https://dev-api.kuaitu.cc/uploads/16_fad324d951.png)
