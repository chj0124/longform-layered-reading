# Longform Layered Reading

面向各种长文的分层阅读技能。先识别文本的组织方式，再决定使用纯文字、对照表或交互 HTML，避免摘要模板反向扭曲原文逻辑。

适用于论说文章、论文、行业报告、访谈、历史与调查叙事，以及混合型长文。

## 一句话安装：复制给你的 Agent

复制下面整段话并发给支持命令执行的 Agent：

```text
请把 GitHub 仓库 https://github.com/chj0124/longform-layered-reading 克隆到当前 Agent 的用户级技能目录（优先使用 ~/.agents/skills/longform-layered-reading；若你的 Agent 使用其他技能目录，请按其文档安装），保留 SKILL.md 和 references 的完整结构，重新加载技能后用一次长文摘要任务验证安装。
```

仓库已公开，克隆时不需要 GitHub 登录。若 Agent 无法执行命令，也可以按下面的手动步骤安装。

## 核心能力

- 记录原文来源与实际可读范围，不把片段伪装成全文。
- 区分独立支撑、必要前提、共同作用、对照、时间、部分—整体、阐释和延伸外推。
- 保留机制、激励、约束、成本、风险、条件、例外、限制和关键案例。
- 区分原文陈述、作者判断、预测、有限旁证和不同人物的声音。
- 只在知识缺口阻碍理解时就近补充简短背景，并明确标为非原文。
- 用叙述角色、短句和有原文依据的关系图降低理解负担。
- 根据内容选择纯文字、Markdown 对照表或单文件交互 HTML。
- 交付前检查覆盖、关系、归因、分层、数值出处和验证声明。

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
请阅读这篇长文，并按 longform-layered-reading 生成适合它的分层摘要：
https://example.com/article
```

也可以指定输出形式：

```text
把这篇访谈整理成对照表。
把这篇论说文章做成可交互的分层摘要 HTML。
```

未指定格式时，技能按以下原则选择：

| 输出形式 | 适用条件 |
|---|---|
| 纯文字 | 线性阅读足够、层级较浅，交互不会带来理解增益 |
| 对照表 | 多个主体或方案共享稳定、同义的比较维度 |
| 交互 HTML | 存在有价值的多层信息或非线性关系，展开与切换能明显降低阅读负担 |

## 目录结构

```text
longform-layered-reading/
├── SKILL.md
└── references/
    ├── text-structures.md
    ├── output-selection.md
    ├── interaction-patterns.md
    ├── background-supplements.md
    └── fidelity-checklist.md
```

- `SKILL.md`：触发条件、核心原则和不可跳过的工作流。
- `text-structures.md`：不同文本类型的识别信号与内容地图要求。
- `output-selection.md`：输出形式和默认层、支持层的选择契约。
- `interaction-patterns.md`：文本关系到交互结构的映射及 HTML 实现要求。
- `background-supplements.md`：仅在知识缺口阻碍理解时加载，规定背景的归属、预算和就近落位。
- `fidelity-checklist.md`：交付前的覆盖、关系、归因与数值校验。

参考文件按任务需要读取，不必每次全部加载。

## 维护与验证

修改技能时，建议采用以下流程：

1. 用无技能的全新上下文运行目标场景，记录实际失败。
2. 只针对已观察到的失败编写最小规则。
3. 用加载技能后的全新上下文重跑相同场景。
4. 保留基线、输出和独立复核证据，再安装或发布。
5. 修改 HTML 交互规则时，实际检查展开、键盘、焦点、移动端和链接。

当前验证覆盖论说、访谈、研究、叙事、混合文本、不完整输入和 HTML 场景。浏览器 console 采集与合成触屏分发未验证，不应被视为已通过。

## 许可证

本项目使用 [MIT License](LICENSE)。

## 维护者

GitHub：[`chj0124`](https://github.com/chj0124)
