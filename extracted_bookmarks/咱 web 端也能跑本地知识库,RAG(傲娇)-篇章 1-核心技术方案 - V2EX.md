# 咱 web 端也能跑本地知识库,RAG(傲娇)-篇章 1-核心技术方案 - V2EX

**原始链接**: https://www.v2ex.com/t/1129675#reply13
**提取时间**: 2025-07-28 10:24:16

---

核心技术方案如下

transfomerjs + indexdb

## **知识库与 RAG 介绍**

可能有些小伙伴对这两玩意不太清楚,大致介绍下

### **知识库(偏狭义上或特定领域下的知识库)**

知识库我觉得算是一个赛道方向,现在有很多家如 dify,openai 等等,包括阿里等平台,都有提供这类功能服务,通过将用户文本**向量化**(将文本变成数字),存储到数据库中,最后在搜索时,可通过文本再**向量化** ,达到语义化搜索(向量相似度计算),最后将相应匹配的文本交给 AI 回答.

这样做的好处就是,当你存储的文本如果是 "我想吃苹果", 而你搜索的文本是"我吃苹果"或者"我超级 tm 的想吃苹果"时,是能够搜索到的.

### **RAG**

而 RAG,则是实现这样知识库的一个手段,如向量化,分片文本,文本预处理,巴拉巴拉的

### **划重点,圈起来,要考的地方**

向量化,向量化,向量化

## **回归正题**

### **向量化**

通过 transfomerjs 来处理文本向量化,这样咱就完成了最基础也是最核心的地方,参考代码如下
    
    
    import { env, pipeline } from '@huggingface/transformers';
    // Create a pipeline for feature extraction, using the full-precision model (fp32)
    const pipe = await pipeline('feature-extraction', 'your-model-name', {
        dtype: "fp32",
    });
    const output = await pipe(inputTexts, { pooling: 'mean', normalize: true })
    
    

文档链接: <https://huggingface.co/docs/transformers.js/pipelines>

### **存储与搜索**

而由于是在 web 端,要能存储大量数据的方案,也只有 indexdb 了(好像是可以存储电脑总硬盘量百分之五十哦,记不太清楚了)

但这有个问题,向量化的数据怎么存储到 indexdb 并保证搜索呢???

要知道,大部分服务端存储向量数据方案,是有专门的向量数据库的,而 indexDB 是类似于 Mongodb 的 JSON 存储,这咋玩???

咱们不妨把心思放野一点, 自己实现个最基础的向量数据库试下呢

思路也有,而我,采用了 LSH 方案,细节太多了,后续可以单开篇章来讲,感兴趣的可以直接看源码

啥,你觉得这个技术栈不靠谱,看下面!!!

## **成果**

**代码已开源**

[github.com/Yoan98/Ncurator](https://github.com/Yoan98/Ncurator)

**想看实际演示?这里**

[www.ncurator.com](https://www.ncurator.com/)

**有啥能证明这个玩意靠谱呢?这里**

1.上了阮一峰的周刊 [科技爱好者周刊（第 337 期）：互联网创业几乎没了](https://www.ruanyifeng.com/blog/2025/02/weekly-issue-337.html)

2.上了 DeepSeek 的集成推荐 <https://github.com/deepseek-ai/awesome-deepseek-integration>
