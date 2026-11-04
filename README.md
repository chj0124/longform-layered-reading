# Longform Layered Reading

面向各种长文的**信息完整保留型分层优化技能**。默认产物不是摘要、概括或全文搬运，而是原文的交互式优化版本：先梳理原文脉络作为一级骨架，再用逻辑关系连接骨架，把机制、例子、过程、数据、引语、条件、例外、限制和次要证据完整保留在对应节点的下一级。

默认交付单文件交互 HTML，结合可视化信息图表与统一逻辑符号。一级只放短标题、短句节点和关系，不放长段长句；下级承载完整细节。语气与文风可中性化，但信息、立场强度、不确定性和归属必须保留。

适用于论说文章、论文、行业报告、访谈、历史与调查叙事，以及混合型长文。

## 一句话安装：复制给你的 Agent

复制下面整段话并发给支持命令执行的 Agent：

```text
请把 GitHub 仓库 https://github.com/chj0124/longform-layered-reading 克隆到当前 Agent 的用户级技能目录（优先使用 ~/.agents/skills/longform-layered-reading；若你的 Agent 使用其他技能目录，请按其文档安装），保留 SKILL.md、references、examples 和 validation 的完整结构，重新加载技能后用 validation 中的用例验证安装。
```

仓库已公开，克隆时不需要 GitHub 登录。若 Agent 无法执行命令，也可以按下面的手动步骤安装。

## 核心能力

- 记录原文来源、目标读者与实际可读范围，不把片段伪装成全文。
- 建立原文信息清单和内容地图，每项信息都有输出落位与回溯编号。
- 默认完整保留有信息量的内容；完全重复的信息可合并，但不得静默遗漏细节。
- 以「一级骨架 → 逻辑连接 → 下级细节」重组原文，而不是用概览替代正文。
- 一级只放短句和关系；所有层级都避免长段长句，必要引语可原样保留。
- 默认提供单文件交互 HTML，并使用信息图表、引导符号和渐进展开降低阅读密度。
- 显化「主张—理由—证据／例子—推理—结论」，保留前提、反驳、限制与例外。
- 将独立支撑、前提链、连续论证、共同作用、对照、反馈、时间和局部—整体等关系可视化。
- 区分例子的说明、证据、反例或类比作用，不把举例自动当证明。
- 区分原文陈述、作者判断、预测、有限旁证和不同人物的声音。
- 只在知识缺口阻碍目标读者理解时就近补充简短背景，并明确标为非原文。
- 交付前核对信息覆盖、归因、分层、短句短段、图形和实际验证声明。

## 安装

将本仓库克隆到运行环境的用户技能目录：

```bash
git clone https://github.com/chj0124/longform-layered-reading.git "$HOME/.agents/skills/longform-layered-reading"
```

在 Windows 的 Kimi Code 中，对应目录为：

```text
C:\Users\<用户名>\.agents\skills\longform-layered-reading\
```

安装后重新加载会话或技能目录，使技能出现在可用列表中。

## 使用

直接提供完整正文、文件或公开链接，例如：

```text
请按 longform-layered-reading 优化这篇长文：不要总结或遗漏细节；先抽取短句骨架，再标明骨架间的逻辑，把原文信息完整放到对应节点的下一级，交付单文件交互 HTML：
https://example.com/article
```

也可以指定读者、输出形式或明确摘要需求：

```text
把这篇访谈优化成交互 HTML，保留各方语境、例子、共识和分歧，一级不要出现长段。
这篇短文的结构很简单，用分层树状大纲呈现即可，所有细节仍须保留。
把这篇报告压缩成 1000 字摘要；这是明确摘要任务，不要求覆盖全部信息。
```

未指定格式时，技能按以下原则选择：

| 输出形式 | 适用条件 |
|---|---|
| 单文件交互 HTML | 默认；以一级短句骨架、逻辑关系、信息图表和下级完整细节呈现原文 |
| 分层树状大纲 | 用户指定，或原文确为单主线、层级浅且无需交互与图形时 |
| 对照表（组件） | 多个主体或方案共享稳定、同义的比较维度时，嵌入 HTML 或大纲 |
| 明确摘要 | 仅用户明确要求摘要、速读或压缩时启用，不与默认原文优化混同 |

## 目录结构

```text
longform-layered-reading/
├── SKILL.md
├── references/
│   ├── content-map.md
│   ├── text-structures.md
│   ├── output-selection.md
│   ├── interaction-patterns.md
│   ├── background-supplements.md
│   └── fidelity-checklist.md
├── examples/
│   └── content-map-example.md
└── validation/
    ├── README.md
    ├── scoring-rubric.md
    ├── report-template.md
    └── cases/
```

- `SKILL.md`：触发条件、核心原则和不可跳过的工作流。
- `content-map.md`：原文信息编号、骨架、关系、输出落位和覆盖清单模板。
- `text-structures.md`：不同文本类型的识别信号与不可省略的信息。
- `output-selection.md`：原文优化／明确摘要、分层结构、短句短段、逻辑符号与可视化契约。
- `interaction-patterns.md`：文本关系到交互结构的映射及 HTML 实现要求。
- `background-supplements.md`：仅在知识缺口阻碍理解时加载，规定背景的归属、预算和落位。
- `fidelity-checklist.md`：交付前的信息覆盖、关系、归因、分层和数值校验。
- `examples/`：可回认的内容地图与分层输出示例。
- `validation/`：合成测试用例、评分门槛和实际验证记录模板。

参考文件按任务阶段加载，不必每次全部读取。

## 维护与验证

修改技能时采用以下流程：

1. 用无技能的全新上下文运行 `validation/cases/` 中的目标场景，保存基线输出和实际失败。
2. 只针对已观察到的失败编写或修改规则，避免把假设性禁令继续堆入技能。
3. 用加载技能后的全新上下文重跑相同用例，保存输出。
4. 按 `validation/scoring-rubric.md` 独立复核，并用 `validation/report-template.md` 记录证据。
5. 修改 HTML 交互规则时，实际检查展开、键盘、焦点、移动端和链接；未执行的检查明确写为未验证。

仓库提供的是**可复现验证材料**，不把未附输出与记录的历史声明当作当前版本已通过验证。每次修订只有存在对应验证报告时，才能声称相应场景已经通过。

## 许可证

本项目使用 [MIT License](LICENSE)。

## 维护者

GitHub：[`chj0124`](https://github.com/chj0124)
