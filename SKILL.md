---
name: longform-layered-reading
description: Use when the user asks to optimize a long-form text into a clearer interactive reading experience, expose and study its hidden logic or argumentation, or summarize, restructure, or present it—an essay, paper, industry report, interview, historical or investigative narrative, or a mixture of these. Default to a logic-focused optimized version as a single-file interactive HTML page; use a tree outline only when the source structure is genuinely simple or the user requests another format. Retain details that serve logic or comprehension and remove filler, redundancy, and rhetorical padding.
---

# Longform Layered Reading

## 核心原则

目标是**逻辑驱动的原文优化版**：不是摘要，也不是机械保留全文。默认交付单文件交互 HTML；仅当原文结构实在简单、静态树状大纲已足够时使用大纲。只保留服务于逻辑、论证或理解的内容，删除废话、重复框定与修辞性冗余；例子、过程和次要证据若承担说明或论证作用，必须保留其必要细节。用显式结构、统一引导符号和可视化暴露原文隐藏的逻辑；原文未明说的推理只能标为推断，形式不得创造逻辑。语气和文风可中性化，但不得改变立场强度、不确定性、评价归属或论证含义。用户要求优先。

## 强制步骤

1. **获取文本、任务与边界**：记标题、来源、可读范围，并确认用户要原文优化版、明确摘要，还是重点学习论证；未明确要求时默认原文优化版。内容地图先填“可读范围”：全文或片段。若用户称完整而文本仅局部编号、无收束标志，输出须声明“仅基于所提供片段”并请求原文；不得交付伪装全文的摘要或优化版。
2. **判定文本类型**（可无结论/混合型）→ 加载 `references/text-structures.md`。
3. **建立内容地图**（内部）。必需字段：叙述任务；顶层单元及关系（各单元标叙述角色，核心单元写明回答的问题，并列问题不得合并）；每单元内容/支持/主体/归属/出处；机制、激励、约束、成本、风险、条件、例外、限制、案例及次要证据；例子的语境、过程、结果与论证作用；论证链（主张—理由—证据/例子—推理—结论，含前提、反驳与限制）；每项内容的删留依据（服务何种逻辑或理解）；需要可视化的复杂关系；覆盖清单。原文未明说的推理只能标为推断。零基础或跨领域读者审知识缺口，有缺口才加载 `references/background-supplements.md`。
4. **设计优化结构、HTML 交互与可视化** → 加载 `references/output-selection.md` 和 `references/interaction-patterns.md`；仅在判定为简单树状大纲或用户指定非 HTML 时不加载后者。
5. **交付前校验** → 加载 `references/fidelity-checklist.md` 逐项通过（含复述）。预测须显式归属作者，不得并入事实链。

## 结构示例

品质 ∥ 利他 → 汇聚 → 个人选择。

## 快速参考

默认交互 HTML，简单结构才用树状大纲；所有内容服务逻辑；例子保留必要语境、过程和作用；复杂逻辑必须可视化；引导符号全篇一致；推断须标注，不得暗补成原文；语气可变，立场强度与不确定性不变；先后≠因果；相关≠因果。

## 常见错误

把优化版做成全文搬运或摘要；默认退成纯文字；保留不服务逻辑的废话；删掉承担说明或论证作用的例子过程；复杂逻辑只写线性文字；引导符号含义混乱；把举例自动当证明；把推断写成原文；单线链；预测入事实链；选择普遍化；强造和解；删限制例外差异；片段伪装全文；表维度不稳；展开重复；丢语境；错挂日期；数值无出处。

## 红旗（基线已证实）

① “事实宣告”预测写成事实（argumentative/html）→ 归属规则；② 片段伪装全文（incomplete-source）→ 可读范围规则。
