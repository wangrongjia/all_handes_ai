# gpt4o 图像生成的技术讨论(自回归模型又好起来了?) - V2EX

**原始链接**: [https://www.v2ex.com/t/1124516](https://www.v2ex.com/t/1124516)  
**来源网站**: www.v2ex.com  
**提取时间**: 2025-07-29 01:18:24

---

gpt4o 图像生成的特点是，生成时**从上到下** 逐渐清晰化（并不只是显示技巧）

![s1](https://pbs.twimg.com/media/GnFgwuVWoAApVQx?format=png&name=small)

如果使用 diffusion 进行生成，它的过程可能是这样的

![s2](https://pbs.twimg.com/media/GnFi0_uWcAA0Qmq?format=png&name=900x900)

但已知的是 gpt4o 图像生成（似乎）已经转向 autoregressive(自回归模型)+transformer

![s3](https://pbs.twimg.com/media/GnF-rUoWgAA41nZ?format=jpg&name=small)

目前外网也对 gpt4o 的技术进行了猜测，但也没讨论出个结果来（大多是认同转向了 ar 模型）

**自回归模型是要打败 diffusion ，并在多模态领域又好用起来了吗？**

另外，目前开源界似乎还没有什么动静，国内的字节跳动在 ar 的图像生成领域探索得还挺多（发了不少 paper ）
