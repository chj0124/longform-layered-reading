---
name: longform-layered-reading
description: Use when the user asks to optimize a long-form text into a clearer interactive reading experience without losing its information, expose its hidden logic or argumentation, or explicitly summarize, restructure, or present it. Default to a complete, layered, single-file interactive HTML version with a sparse skeleton, explicit logical links, visual information structures, and source details retained under the appropriate nodes. Use another format only when the user requests it or a genuinely simple source needs no interaction.
---

# Longform Layered Reading

## 核心原则

目标是**信息完整保留的原文分层优化版**：不是摘要，不是概括，也不是把全文机械搬入 HTML。默认交付单文件交互 HTML，以「一级骨架 → 骨架间的逻辑 → 下级原文信息」组织阅读。原文中的机制、例子、过程、数据、引语、条件、例外、限制、次要证据和旁支信息都不得因压缩或“非核心”而遗漏；完全重复的信息可合并，措辞可重写，顺序可重排，但信息、立场强度、不确定性、评价归属与论证含义不得改变。

一级只放短标题、短句节点和关系，不塞长段、长句或全部细节。细节挂在对应骨架节点的下一级，按需展开，但核心正文与论证链必须能连续阅读。交互 HTML、可视化信息图表和逻辑符号共同服务于理解；形式不得创造原文没有的逻辑。用户明确要求摘要时另走摘要模式，不得与原文优化版混同。用户要求优先。

## 强制步骤

1. **获取文本、任务、读者与边界**：记录标题、作者、来源、实际可读范围、阅读模式和用户约束；明确目标读者及其背景。用户未说明时，默认“能阅读通用中文、缺乏该领域专门背景的读者”，不得据此反复追问。内容地图先填“可读范围”：全文或片段。若用户称完整而文本仅局部编号、无收束标志，输出须声明“仅基于所提供片段”并请求原文；不得交付伪装全文的摘要或优化版。
2. **判定文本类型**（可无结论／混合型）→ 加载 `references/text-structures.md`。
3. **建立信息清单与内容地图** → 加载 `references/content-map.md`。先为原文信息单元编号，再建立骨架、关系和输出落位；每个信息单元必须有去向。默认原文优化版不得用“次要”“离题”“不服务主线”作为删除理由。原文未明说的推理只能标为“推断（非原文明述）”。按目标读者审查知识缺口，有缺口才加载 `references/background-supplements.md`。
4. **设计分层正文、HTML 交互与可视化** → 加载 `references/output-selection.md` 和 `references/interaction-patterns.md`；仅在用户指定非 HTML 时不加载后者。先完成一级骨架与关系，再把细节放入对应下级，不得在写作过程中把所有信息重新堆回一级。
5. **交付前校验** → 加载 `references/fidelity-checklist.md` 逐项通过。先核对信息覆盖清单，再检查归因、关系、分层、短句短段、图形、交互和实际验证声明。预测须显式归属作者，不得并入事实链。

## 结构契约

```text
一句话主线（短句，仅作导航）
├─ 骨架 A：本部分回答什么
│  ├─ 逻辑标签／关系说明
│  └─ 下级：原文细节、例子、数据、条件与出处
├─ 骨架 B：本部分回答什么
│  └─ 下级：原文细节、引语、过程与限制
└─ 结论／延伸判断（分开归属）
```

骨架之间可使用经图例定义的符号，例如 `∥` 表示并列、`→` 表示顺序、`⇒` 表示推理、`↻` 表示反馈；符号必须同时配文字标签，不得只靠颜色或图形传义。

## 快速参考

完整保留信息，而非只保留“重点”；一级是短骨架，细节在下一级；默认交互 HTML；复杂逻辑必须可视化；所有信息单元可回溯；引导符号全篇一致；推断须标注；语气可变，立场强度、情感所承载的信息与不确定性不变；先后≠因果；相关≠因果；未验证不得声称已验证。

## 常见错误

把优化版做成摘要、概括或全文搬运；遗漏次要细节、旁支信息、限制或例外；一级堆长段长句；细节脱离所属骨架；默认退成纯文字；复杂逻辑只写线性文字；用卡片和颜色冒充关系图；把举例自动当证明；把推断写成原文；预测入事实链；选择普遍化；强造和解；片段伪装全文；表维度不稳；展开重复；丢语境；错挂或编造日期；数值无出处；没有覆盖清单却声称“无遗漏”。

## 重点回归风险

① 为追求简洁再次滑向摘要；② 一级节点写成包含全部细节的长段；③ 只呈现骨架，丢失下级原文信息；④ “事实宣告”式预测被写成事实；⑤ 片段被伪装成全文；⑥ 交互展开后没有新信息，或核心正文被全部折叠。
