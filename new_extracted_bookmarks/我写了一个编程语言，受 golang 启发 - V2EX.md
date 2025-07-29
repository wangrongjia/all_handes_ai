# 我写了一个编程语言，受 golang 启发 - V2EX

**原始链接**: [https://www.v2ex.com/t/1132910#reply264](https://www.v2ex.com/t/1132910#reply264)  
**来源网站**: www.v2ex.com  
**提取时间**: 2025-07-29 01:19:23

---

大家好，我是 nature 编程语言的作者，自 2021 年第一次提交以来，一直到今天 nature 编程语言达到了早期可用版本。

* * *


为什么要实现这样一个编程语言?

golang 是我日常工作使用的编程语言，我一次使用 golang 时就被其所惊艳，语法简单，编程思想简洁自由，非常便利的进行交叉编译以及部署，拥有非常优秀且高性能的 runtime 实现，拥有先进的基于 goroutine 的并发风格设计等等。但是 golang 也有一些不方便的地方

  * 语法过于简洁导致表达能力不足
  * 类型系统不够完善
  * 错误处理机制繁琐
  * 自动 GC 和抢占式调度的设计虽然非常优秀，但是也让 go 的应用范围受限。
  * 包管理方式
  * interface{}
  * ...


nature 在设计理念上是对 go 编程语言的延续与改进，并追寻一定的差异性。在改善上述问题的同时，nature 拥有和 go 类似但更简洁的 runtime 、GMP 模型、allocator 、collector 、coroutine 、channel 、std 等等。并且 nature 同样不依赖 llvm ，有着高效的编译速度，方便的交叉编译与部署等，

基于 nature 编程语言已实现的特性，其适用于游戏引擎和游戏开发、科学计算和 AI 、操作系统和物联网、命令行、以及 Web 开发等领域。

当 nature 完成所有特性及优化时，预计 nature 可以在任何场景替代 golang 进行开发(转换为可读 golang 代码，以最低的试错成本的使用 nature ，并可以随时切换回 golang)。并且作为通用编程语言 nature 可以和任何的同类型编程语言进行竞争。[注意这还未完成]

* * *


两年前 nature 编程语言还不能使用，但我依旧在 V2EX 进行了分享，得到了很多鼓励，这是让我坚持到可用版本发布的动力之一。

但我知道, 这依旧有些迟了，我耗费了太久的时间，仅仅是又带来了一个编程语言而已，毕竟这个世界最不缺的就是编程语言。但是当我真的去思考类似 “我还要继续么？我能做好吗？” 这样的问题的时候，我发现我已经走了很远很远的路。

* * *


欢迎体验反馈~

github: <https://github.com/nature-lang/nature>

官网: <https://nature-lang.org/> 首页包含一些语法特性示例，可以直接在 playground 尝试

语法文档: <https://nature-lang.org/docs/syntax>

playground: <https://nature-lang.org/playground> 在线尝试

* * *


贡献指南(点击右上角切换到中文)

<https://nature-lang.org/docs/contribute> 我在文档中详细介绍了 nature 编程语言是如何实现的。

nature 和 golang 一样，有着一个自研的编译器后端, 但 nature 的源码结构和实现非常的简洁。

这让参与 nature 编程语言的贡献变得容易且有趣, 不再只是编译器前端 + llvm ，你可以参与 SSA, SIMD, 寄存器分配，汇编器，链接器等等有趣的工作来验证你的学习成果和想法。你可以通过 issue 表达你的想法，我会指导你参与贡献。

* * *


这是我用 nature 实现的一些小项目, 我很喜欢使用 nature 编写代码的感觉。

<https://github.com/weiwenhao/parker> 轻量打包工具

<https://github.com/weiwenhao/llama.n> Llama2 推理模型 nature 编程语言实现

<https://github.com/weiwenhao/tetris> 绑定 raylib 实现的俄罗斯方块

<https://github.com/weiwenhao/playground> nature 官网的 playground server api 实现

* * *


最后，我正在寻找工作，如果你觉得这个项目还不错，希望能给我一个 star ，这对我有很大的帮助 🙏
