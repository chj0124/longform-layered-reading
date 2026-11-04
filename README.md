# Longform Layered Reading

面向各种长文的**信息完整保留型分层优化技能**。默认产物不是摘要或全文搬运，而是「短主线＋具体推导＋完整细节」：长文主阅读路径以 3—5 分钟读完为目标，核心论证直接可读，例子、数据、次要证据和旁支信息完整保留在就近细节层。

格式按结构选择：树状大纲足以表达时使用 Markdown；跨板块、多分支、汇聚或反馈关系难以用缩进表达时，再使用紧凑的单文件交互 HTML。关系类型不能替代具体桥接句，读者不应靠自行补脑理解板块为何相连。

默认使用**日常档**：不强制生成逐项编号底稿，但仍须逐段回查并保留全部有信息量的细节。遇到结构异常、内容存疑、正式交付或逐项核验需求时回退**完整档**，建立正式信息清单与覆盖审计。两档只改变记录和验证强度，不改变正文保真要求。

适用于论说文章、论文、行业报告、访谈、历史与调查叙事，以及混合型长文。

## 安装

将本仓库克隆到当前 Agent 的用户级技能目录。优先使用：

```bash
git clone https://github.com/chj0124/longform-layered-reading.git "$HOME/.agents/skills/longform-layered-reading"
```

若 Agent 使用其他技能目录，请按其文档调整目标路径，并保留 `SKILL.md`、`references`、`scripts`、`examples` 和 `validation` 的完整结构。安装后重新加载会话或技能目录。

也可以复制下面整段话给支持命令执行的 Agent：

```text
请把 GitHub 仓库 https://github.com/chj0124/longform-layered-reading 克隆到当前 Agent 的用户级技能目录，优先使用 ~/.agents/skills/longform-layered-reading；若你的 Agent 使用其他技能目录，请按其文档安装。保留完整目录，重新加载技能后用 validation 中的用例验证安装。
```

## 核心能力

- 记录原文来源、目标读者与实际可读范围，不把片段伪装成全文。
- 日常档按原文顺序逐段回查；完整档建立原文信息清单，每项信息都有唯一主要落位与回溯编号。
- 长文主线以 3—5 分钟为目标，不设原文字数比例；短文不填充时长。
- 区分主线与细节层：核心推导不折叠，次要但有信息量的细节不删除。
- 每个板块回答一个具体理解问题，不只贴「前提／支撑／判断标准」等抽象标签。
- 每个关键连接写清起点内容、推理或条件、终点内容及阅读顺序理由。
- 树状大纲够用就用 Markdown；关系复杂时才升级为紧凑的交互 HTML。
- HTML 避免大留白与孤立卡片，让相关板块邻近可见，同时保留键盘、焦点和移动端可用性。
- 区分原文陈述、作者判断、预测、有限旁证、合理推断和不同人物的声音。
- 交付前核对信息覆盖、具体关系、主线预算、格式选择和实际验证声明。

## 使用

直接提供完整正文、文件或公开链接，例如：

```text
请按 longform-layered-reading 优化这篇长文：主线控制在 3—5 分钟，核心论证完整；每个板块写清回答什么问题、与下一板块怎样具体连接；细节保留在按需层；根据结构选择 Markdown 树状大纲或紧凑交互 HTML：
https://example.com/article
```

也可以指定格式或明确摘要需求：

```text
把这篇访谈优化成紧凑的交互 HTML，保留各方语境、例子、共识和分歧。
这篇报告的层级很简单，用 Markdown 树状大纲呈现，主线和按需细节分开。
把这篇文章压缩成 1000 字摘要；这是明确摘要任务，不要求覆盖全部信息。
```

未指定执行档位时默认日常档。可以明确要求：

```text
用日常档处理这篇文章，保留主线、具体桥接和全部按需细节，不必生成逐项覆盖表。
用完整档处理这篇报告，我需要逐项信息清单、唯一落位和正式验证记录。
```

| 执行档位 | 适用条件 | 核对方式 |
|---|---|---|
| 日常档（默认） | 日常阅读，结构与归属能够稳定梳理 | 轻量内容草图＋逐段回查；不强制正式覆盖表 |
| 完整档 | 结构异常、内容存疑、正式交付或逐项核验 | 完整内容地图＋逐项唯一落位＋相应验证报告 |

未指定格式时：

| 输出形式 | 适用条件 |
|---|---|
| Markdown 分层树状大纲 | 单主线或清晰并列、层级较浅，缩进与编号足以表达关系 |
| 单文件交互 HTML | 多线、跨板块、汇聚、反馈或总览与局部推导需要联动 |
| 对照表（组件） | 多个主体或方案共享稳定、同义的比较维度 |
| 明确摘要 | 仅用户明确要求摘要、速读或压缩时启用 |

## 主线时长估算

Markdown 在主阅读路径首尾放置：

```text
<!-- main-reading-path:start -->
主线内容
<!-- main-reading-path:end -->
```

HTML 在主线路径容器上设置 `data-main-reading-path`。随后运行：

```bash
python3 scripts/estimate_main_path.py <输出文件> --enforce
```

短文允许低于 3 分钟时：

```bash
python3 scripts/estimate_main_path.py <输出文件> --allow-short --enforce
```

结果只是按可配置文本速度计算的估算，不是真实阅读实测，也不包含图示理解成本；核心论证是否完整仍须按清单复核。

## 目录结构

```text
longform-layered-reading/
├── SKILL.md
├── references/
│   ├── content-map.md
│   ├── reading-path.md
│   ├── text-structures.md
│   ├── output-selection.md
│   ├── interaction-patterns.md
│   ├── background-supplements.md
│   └── fidelity-checklist.md
├── assets/
│   └── compact-reading-template.html
├── scripts/
│   └── estimate_main_path.py
├── examples/
│   └── content-map-example.md
└── validation/
    ├── README.md
    ├── scoring-rubric.md
    ├── report-template.md
    ├── cases/
    └── reports/
```

参考文件按执行档位与任务阶段加载，不必每次全部读取。日常 HTML 从 `assets/compact-reading-template.html` 复制并替换内容；修改公共模板或交互后须重新执行完整呈现验证。

## 维护与验证

1. 用无技能的全新上下文运行目标用例，保存基线输出和实际失败。
2. 只针对已观察到的失败修改规则，避免堆入假设性禁令。
3. 用加载技能后的全新上下文重跑相同输入，保存输出。
4. 按 `validation/scoring-rubric.md` 复核，并用报告模板记录与档位匹配的证据；两档对照时检查正文是否存在信息差。
5. 日常 HTML 记录当前产物冒烟检查；修改 HTML 模板或规则时实际检查展开、键盘、焦点、紧凑密度和移动端；未执行即写未验证。
6. 主线阅读时间优先实测；使用脚本时必须标为估算。

仓库提供可复现验证材料，不把未附输出与记录的历史声明当作当前版本已通过验证。

## 许可证

本项目使用 [MIT License](LICENSE)。

## 维护者

GitHub：[`chj0124`](https://github.com/chj0124)
