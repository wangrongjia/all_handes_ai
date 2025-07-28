# Claude Code + Kiro Spec：别急着生成代码，先让 AI 理解你的需求 - V2EX

**原始链接**: https://www.v2ex.com/t/1145836
**提取时间**: 2025-07-28 10:27:59

---

> 微信公众号地址 欢迎大佬们点点赞 <https://mp.weixin.qq.com/s/_iqouEZoPMpvG156kyJZTA>

# Claude Code + Kiro Spec：别急着生成代码，先让 AI 理解你的需求

最近在研究 Kiro 的时候，发现了一个很有意思的现象。Kiro 的 spec 功能设计得很直接，你说"我要做个评论系统"，它就直接生成 requirements 、design 和 tasks 三个文件。

但真正执行之后，我发现一个问题：**直接从需求到 spec ，生成的内容往往差强人意** 。不是需求理解偏差，就是设计过于粗糙。

这让我想起了传统开发中的一个痛点：需求不清楚就开始写代码，最后做出来的东西完全不是用户想要的。

## 问题的根源：直接 toSpec 的陷阱

### 传统开发中的教训

还记得我之前分享的那套软件工程流程吗？**需求分析(/ask) → 代码实现(/code) → 测试用例(/test) → 代码审查(/review) → 优化调整(/optimize, /refactor)**。

这套流程的核心逻辑很简单：**先把需求搞清楚，再写代码，最后验证** 。但实际操作中，大部分团队都是直接上手写代码，需求文档要么没有，要么写完就束之高阁。

在传统软件开发中，我们都知道一个道理：**需求分析是整个项目的基石** 。如果需求都没搞清楚，后面的设计和实现再精美也是空中楼阁。

我见过太多这样的场景：

  * 产品经理甩过来一个模糊的需求文档

  * 开发直接开始写代码

  * 结果做出来的东西完全不是用户想要的




这种情况下，即使技术实现再完美，最终也是徒劳。

### AI 开发中的相同问题

现在到了 AI 辅助开发的时代，**同样的问题依然存在** 。

很多人使用 Kiro 的时候，流程是这样的：

需求 → 直接 spec → 生成 requirements/design/tasks → 开发

这种做法的问题在于：

  1. **AI 没有充分理解需求背景**

  2. **缺乏交互式的需求澄清过程**

  3. **生成的 spec 往往过于泛化**




就像我之前在 Claude Code 的实践中发现的，不能再随意跳过文档和测试环节，因为后续的命令都依赖前面的输出。同样道理，Kiro 的 spec 生成也不应该跳过需求理解这个关键环节。

## 我的解决方案：/ask + /spec 组合拳

经过一段时间的摸索，我发现了一个更有效的工作流程：

### 第一步：使用/ask 进行需求沟通

在使用`/spec`之前，先用`/ask`和 AI 进行充分的对话。这个过程就像是和产品经理、技术总监进行需求评审会议。

**记住，一定要使用/clear 清理上下文** ，否则被 Claude Code 自动压缩后质量降低非常多。

**举个例子：**

/ask 我想开发一个用户管理系统，你能帮我理解一下具体需要考虑哪些方面吗？

AI 会反问你：

  * 这个系统的目标用户是谁？

  * 需要支持多少用户规模？

  * 有哪些核心功能需求？

  * 有什么特殊的业务规则？

  * 需要集成哪些外部系统？




### 第二步：深入交流，澄清细节

通过多轮对话，让 AI 真正理解你的需求：

/ask 我们的用户管理系统主要面向企业内部，大概 500 人规模，需要支持 RBAC 权限控制，还要能和我们现有的 OA 系统集成

AI 会继续追问：

  * RBAC 的角色层级是怎样的？

  * OA 系统的集成方式是什么？

  * 数据同步的频率要求？

  * 安全性方面有什么特殊要求？




这就像我在 Claude Code 中强制规范化流程一样，**强制你思考那些平时容易忽略的问题** ，比如数据一致性、服务间通信、故障恢复等。

### 第三步：确认理解，生成 spec

经过充分的交流后，AI 对你的需求有了深入理解。这时候再使用`/spec`：

/spec 基于我们刚才的讨论，生成企业用户管理系统的详细规格说明

这时生成的三个 spec files 就会：

  * **[requirements.md](http://requirements.md)** \- 更加贴合实际需求的用户故事

  * **[design.md](http://design.md)** \- 考虑到业务场景复杂性的系统架构

  * **[tasks.md](http://tasks.md)** \- 包含必要技术细节的实现计划




## 实际效果对比

### 直接使用/spec 的结果：

  * 生成的 requirements 往往很泛化

  * design 缺乏针对性的架构考虑

  * tasks 分解不够细致

  * 容易遗漏重要的边界条件




### /ask + /spec 组合的结果：

  * requirements 描述更加精确

  * design 方案考虑更加周全

  * tasks 划分更加合理

  * 包含了业务场景的特殊处理




就像我在 Kiro 的体验中发现的，它不是直接开始写代码，而是先生成三个 spec files 。这种**spec-driven development** 的理念是对的，但前提是 spec 本身要高质量。

## 深层思考：为什么这样更有效？

### 1\. 知识的渐进构建

AI 和人类一样，理解复杂问题需要一个渐进的过程。通过对话，AI 可以：

  * 逐步建立对业务领域的理解

  * 识别潜在的技术风险点

  * 考虑不同方案的权衡




这就像 Claude Code 的 Memory 机制一样，**上下文连续性** 确保生成的代码符合各层级的要求。

### 2\. 上下文的丰富化

每一次`/ask`的交互都在为 AI 提供更丰富的上下文信息。这些信息在后续的`/spec`生成中会发挥重要作用。

就像我在项目 Memory 中记录的那样：技术栈选择理由、非功能性需求分析、潜在风险点识别。这些都需要通过对话来澄清。

### 3\. 需求的双向验证

通过对话，不仅 AI 在理解你的需求，你也在通过 AI 的反馈来完善自己的需求描述。这是一个双向的验证过程。

## 实践建议

### 1\. 不要急于求成

给 AI 足够的时间来理解你的需求。一个好的`/ask`会话可能需要 5-10 轮的交互。

记住 Kiro 的 Agent Hooks 功能，它能自动处理那些琐碎但重要的事情。同样，你也要给 AI 时间来处理需求理解这个重要环节。

### 2\. 提供具体的场景

不要只说"我要做一个系统"，而是说"我要为我们公司的 HR 部门做一个员工管理系统"。

就像我在 Claude Code 中发现的，**具体的上下文信息是代码质量的关键** 。

### 3\. 主动澄清歧义

当 AI 的理解和你的预期不一致时，要主动澄清，不要将就。

这就像代码 review 一样，发现问题要明确指出哪里不符合预期，以及具体的修改建议。

### 4\. 逐步细化

从大的框架开始，逐步细化到具体的功能点。

这个过程就像从全局 Memory 到项目 Memory 再到模块 Memory 的渐进式完善。

## 实际开发案例

举个具体例子，用这套流程开发一个用户认证系统：

### 第一步：需求分析

/ask 我想为我们的企业内部系统开发一个用户认证模块，需要支持 JWT ，你觉得我们应该考虑哪些方面？

通过多轮对话，澄清：

  * 用户规模和并发需求

  * 安全等级要求

  * 与现有系统的集成方式

  * 密码策略和账号管理规则




### 第二步：生成 spec

/spec 基于我们的讨论，生成企业用户认证系统的完整规格说明

这时生成的 spec 会包含：

  * **[requirements.md](http://requirements.md)** \- 明确的用户故事和验收标准

  * **[design.md](http://design.md)** \- 考虑安全性和可扩展性的架构设计

  * **[tasks.md](http://tasks.md)** \- 详细的开发任务分解




### 第三步：基于 spec 开发

有了高质量的 spec ，后续的开发就会非常顺畅。Claude Code 可以基于这些 specs 生成符合要求的代码，而不是凭空想象。

/code @.claude/specs/{feature_name}

## 我的真实感受

用了这套方法后，发现几个明显的好处：

**1\. 提高需求理解准确性** 不会再出现"我以为你要的是这个"的情况。

**2\. 减少返工** 前期把需求和架构想清楚，后面写代码就很少需要大改。

**3\. 提升团队协作效率** 生成的 spec 文档成为团队沟通的基础，避免了各种误解。

**4\. 知识沉淀** 每次的需求澄清过程都会形成文档，后续类似项目可以复用。

当然也有一些成本：

**1\. 学习成本** 需要适应这种工作方式，习惯了直接写代码的开发者可能不太适应。

**2\. 时间投入** 前期需要花更多时间在需求理解上，但这个投入是值得的。

## 总结

从我在 Claude Code 的实践，到现在对 Kiro 的理解，有一个共同的感悟：**AI 工具不是要替代我们思考，而是要让我们思考得更深入、更系统。**

Kiro 的 spec 功能确实强大，但它的真正价值不是快速生成文档，而是帮助我们建立**spec-driven development** 的工作习惯。

而这个习惯的前提是：**你要先让 AI 真正理解你的需求。**

所以，下次使用 Kiro 或者 Claude Code 的时候，别急着`/spec`，先用`/ask`和 AI 聊聊你要做什么。给 AI 足够的上下文，它会给你更好的回报。

记住：**好的代码来自于好的设计，好的设计来自于好的需求理解。**

在 AI 的世界里，这个道理同样适用。

## 配置 spec command

> ~/.claude/commands/[spec.md](http://spec.md)
    
    
    # Requirements Gathering Generation
    
    Workflow Stage: Requirements Gathering
    
    First, generate an initial set of requirements in EARS format based on the feature idea, then iterate with the user to refine them until they are complete and accurate.
    
    Don't focus on code exploration in this phase. Instead, just focus on writing requirements which will later be turned into
    a design.
    
    **Constraints:**
    
    - The model MUST create a '.claude/specs/{feature_name}/requirements.md' file if it doesn't already exist
    - The model MUST generate an initial version of the requirements document based on the user's rough idea WITHOUT asking sequential questions first
    - The model MUST format the initial requirements.md document with:
      - A clear introduction section that summarizes the feature
      - A hierarchical numbered list of requirements where each contains:
        - A user story in the format "As a [role], I want [feature], so that [benefit]"
        - A numbered list of acceptance criteria in EARS format (Easy Approach to Requirements Syntax)
      - Example format:
    [includes example format here]
    - The model SHOULD consider edge cases, user experience, technical constraints, and success criteria in the initial requirements
    - After updating the requirement document, the model MUST ask the user "Do the requirements look good? If so, we can move on to the design." using the 'userInput' tool.
    - The 'userInput' tool MUST be used with the exact string 'spec-requirements-review' as the reason
    - The model MUST make modifications to the requirements document if the user requests changes or does not explicitly approve
    - The model MUST ask for explicit approval after every iteration of edits to the requirements document
    - The model MUST NOT proceed to the design document until receiving clear approval (such as "yes", "approved", "looks good", etc.)
    - The model MUST continue the feedback-revision cycle until explicit approval is received
    - The model SHOULD suggest specific areas where the requirements might need clarification or expansion
    - The model MAY ask targeted questions about specific aspects of the requirements that need clarification
    - The model MAY suggest options when the user is unsure about a particular aspect
    - The model MUST proceed to the design phase after the user accepts the requirements
    
    
    # Design Document Creation Generation
    
    Workflow Stage: Design Document Creation
    
    After the user approves the Requirements, you should develop a comprehensive design document based on the feature requirements, conducting necessary research during the design process.
    The design document should be based on the requirements document, so ensure it exists first.
    
    **Constraints:**
    
    - The model MUST create a '.claude/specs/{feature_name}/design.md' file if it doesn't already exist
    - The model MUST identify areas where research is needed based on the feature requirements
    - The model MUST conduct research and build up context in the conversation thread
    - The model SHOULD NOT create separate research files, but instead use the research as context for the design and implementation plan
    - The model MUST summarize key findings that will inform the feature design
    - The model SHOULD cite sources and include relevant links in the conversation
    - The model MUST create a detailed design document at '.claude/specs/{feature_name}/design.md'
    - The model MUST incorporate research findings directly into the design process
    - The model MUST include the following sections in the design document:
      - Overview
      - Architecture
      - Components and Interfaces
      - Data Models
      - Error Handling
      - Testing Strategy
    - The model SHOULD include diagrams or visual representations when appropriate (use Mermaid for diagrams if applicable)
    - The model MUST ensure the design addresses all feature requirements identified during the clarification process
    - The model SHOULD highlight design decisions and their rationales
    - The model MAY ask the user for input on specific technical decisions during the design process
    - After updating the design document, the model MUST ask the user "Does the design look good? If so, we can move on to the implementation plan." using the 'userInput' tool.
    - The 'userInput' tool MUST be used with the exact string 'spec-design-review' as the reason
    - The model MUST make modifications to the design document if the user requests changes or does not explicitly approve
    - The model MUST ask for explicit approval after every iteration of edits to the design document
    - The model MUST NOT proceed to the implementation plan until receiving clear approval (such as "yes", "approved", "looks good", etc.)
    - The model MUST continue the feedback-revision cycle until explicit approval is received
    - The model MUST incorporate all user feedback into the design document before proceeding
    - The model MUST offer to return to feature requirements clarification if gaps are identified during design
    
    # Implementation Planning Generation
    
    Workflow Stage: Implementation Planning
    
    After the user approves the Design, create an actionable implementation plan with a checklist of coding tasks based on the requirements and design.
    The tasks document should be based on the design document, so ensure it exists first.
    
    **Constraints:**
    
    - The model MUST create a '.claude/specs/{feature_name}/tasks.md' file if it doesn't already exist
    - The model MUST return to the design step if the user indicates any changes are needed to the design
    - The model MUST return to the requirement step if the user indicates that we need additional requirements
    - The model MUST create an implementation plan at '.claude/specs/{feature_name}/tasks.md'
    - The model MUST use the following specific instructions when creating the implementation plan: Convert the feature design into a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step. Focus ONLY on tasks that involve writing, modifying, or testing code.
    - The model MUST format the implementation plan as a numbered checkbox list with a maximum of two levels of hierarchy:
    - Top-level items (like epics) should be used only when needed
    - Sub-tasks should be numbered with decimal notation (e.g., 1.1, 1.2, 2.1)
    - Each item must be a checkbox
    - Simple structure is preferred
    - The model MUST ensure each task item includes:
    - A clear objective as the task description that involves writing, modifying, or testing code
    - Additional information as sub-bullets under the task
    - Specific references to requirements from the requirements document (referencing granular sub-requirements, not just user stories)
    - The model MUST ensure that the implementation plan is a series of discrete, manageable coding steps
    - The model MUST ensure each task references specific requirements from the requirement document
    - The model MUST NOT include excessive implementation details that are already covered in the design document
    - The model MUST assume that all context documents (feature requirements, design) will be available during implementation
    - The model MUST ensure each step builds incrementally on previous steps
    - The model SHOULD prioritize test-driven development where appropriate
    - The model MUST ensure the plan covers all aspects of the design that can be implemented through code
    - The model SHOULD sequence steps to validate core functionality early through code
    - The model MUST ensure that all requirements are covered by the implementation tasks
    - The model MUST offer to return to previous steps (requirements or design) if gaps are identified during implementation planning
    - The model MUST ONLY include tasks that can be performed by a coding agent (writing code, creating tests, etc.)
    - The model MUST NOT include tasks related to user testing, deployment, performance metrics gathering, or other non-coding activities
    - The model MUST focus on code implementation tasks that can be executed within the development environment
    - The model MUST ensure each task is actionable by a coding agent by following these guidelines:
    - Tasks should involve writing, modifying, or testing specific code components
    - Tasks should specify what files or components need to be created or modified
    - Tasks should be concrete enough that a coding agent can execute them without additional clarification
    - Tasks should focus on implementation details rather than high-level concepts
    - Tasks should be scoped to specific coding activities (e.g., "Implement X function" rather than "Support X feature")
    - The model MUST explicitly avoid including the following types of non-coding tasks in the implementation plan:
    - User acceptance testing or user feedback gathering
    - Deployment to production or staging environments
    - Performance metrics gathering or analysis
    - Running the application to test end to end flows. We can however write automated tests to test the end to end from a user perspective.
    - User training or documentation creation
    - Business process changes or organizational changes
    - Marketing or communication activities
    - Any task that cannot be completed through writing, modifying, or testing code
    - After updating the tasks document, the model MUST ask the user "Do the tasks look good?" using the 'userInput' tool.
    - The 'userInput' tool MUST be used with the exact string 'spec-tasks-review' as the reason
    - The model MUST make modifications to the tasks document if the user requests changes or does not explicitly approve.
    - The model MUST ask for explicit approval after every iteration of edits to the tasks document.
    - The model MUST NOT consider the workflow complete until receiving clear approval (such as "yes", "approved", "looks good", etc.).
    - The model MUST continue the feedback-revision cycle until explicit approval is received.
    - The model MUST stop once the task document has been approved.
    
    **This workflow is ONLY for creating design and planning artifacts. The actual implementation of the feature should be done through a separate workflow.**
    
    - The model MUST NOT attempt to implement the feature as part of this workflow
    - The model MUST clearly communicate to the user that this workflow is complete once the design and planning artifacts are created
    - The model MUST inform the user that they can begin executing tasks by opening the tasks.md file, and clicking "Start task" next to task items.
    

* * *

_如果你也在使用 Claude Code 或者 Kiro ，不妨试试这种方法。有什么心得体会，欢迎在评论区分享！_
