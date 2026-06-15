<div align="center">

# Resume Tailor

**求职教练，不是润色器。每条经历经得起面试追问。**

[English](README.en.md) · [简体中文](README.md)

v3.4 · [更新日志](CHANGELOG.md) · MIT

</div>

## 你什么时候需要它？

- **投递前**：拿到 JD，需要一份针对性简历，但不想编数据
- **面试前**：简历上写了"提升 30%"，面试官追问"怎么算的"你答不上来
- **转行时**：经历不直接匹配 JD，需要找到隐性关联而不是硬编经验

大多数 AI 简历工具帮你**编得更像**。这个工具帮你**真得更强**。

| 传统 AI 改写 | Resume Tailor |
|---|---|
| "显著提升了数据分析效率" | "搭建自动化对账工具，月度核算从 **5 天→6 小时**，覆盖 **12 条业务线**" |
| 缺数据就用空泛形容词填 | 递进式追问引导量化，说不出就保留原文 |
| 什么都"主导" | 每条声明都挑战：*"你是最终决策者吗？"* |
| 一份简历投所有 | 按目标地区调语调/格式/隐私规则 |

---

## 它会交付什么？

你不只得到一份简历，你得到一套**求职攻略包**：

| 交付物 | 格式 | 说明 |
|--------|------|------|
| 定制简历 | HTML + Markdown | 瑞士国际主义风，A4 打印优化，零外部依赖 |
| 审计日志 | Markdown | 每条修改的匹配置信度 + 缺口标记 + 合规预警 |
| 面试准备包 | Markdown | 基于真实面经的 mock 问题 + STAR 笔记 |

**渲染示例**（`templates/resume_swiss.html`）：

```
┌─────────────────────────────────────┐
│  张三                                │
│  高级数据分析师                       │
│  email | phone | github | 上海       │
├─────────────────────────────────────┤
│  个人总结                            │
│  3年互联网数据分析经验...             │
├─────────────────────────────────────┤
│  工作经历                            │
│  美团 | 高级数据分析师  2022.06-至今   │
│  · 数据监控体系：搭建核心指标看板...   │
│  · AB实验平台：主导实验分析框架...     │
├─────────────────────────────────────┤
│  技能与证书                          │
│  编程语言：Python, SQL, R, Scala     │
└─────────────────────────────────────┘
  ↑ 每条 bullet 强制 **前缀**: 详细内容
  ↑ 前缀命中 JD 关键词，面试官一眼看到匹配
```

---

## 快速开始

```
帮我针对这个 JD 调简历
```

就这一句。系统自动完成调研 → 匹配 → 调整 → 审计 → 渲染全流程。

### 触发方式

| 场景 | 说法 |
|------|------|
| JD 定制 | "帮我针对这个 JD 调简历" / "tailor my resume for this JD" |
| 多 JD 批量 | "这几个 JD 分别做简历" / "batch tailor for these JDs" |
| 仅优化 | "帮我优化简历" / "polish my resume" |
| 从零开始 | "帮我创建简历" / "我还没有简历" |
| 分析 JD | "这个岗位需要什么能力" / "analyze this JD" |

---

## 它和同类有什么不同？

| | Resume Tailor | 通用 AI 问答 | SaaS 工具 (Jobscan 等) |
|---|---|---|---|
| 编造阻断 | 10 条硬规则 + 整份 ROLLBACK | 无 | 无 |
| 信息溯源 | `[✓]` 确认 / `[?]` 待确认 / `[~]` 推断 | 无 | 无 |
| 审计隔离 | Writer/Auditor 物理隔离 | 自我审计 | 无审计 |
| 面试准备 | 基于真实面经的 mock 问题 | 通用模板 | 无 |
| 量化引导 | 2 轮递进式追问，说不出就保留原文 | 直接编数字 | 仅关键词匹配 |
| 文化适配 | 自信(北美) → 协同(东亚) → 谦逊(北欧) | 无 | 部分 |
| 安装依赖 | 零依赖（纯 Python 标准库渲染） | N/A | 付费 SaaS |

---

## 安全边界

这个 Skill **不会**：
- 编造你没做过的事（编造阻断门 10 条硬规则）
- 夸大你的角色（动词等级必须有证据支撑）
- 添加你不会的技能（技能必须有使用证明）
- 擅自发送简历（所有修改需你确认）
- 删除你的原始文件（只读源简历，输出到独立目录）

这个 Skill **会在以下节点停下来等你确认**：
1. 公司/地区确认（Phase 1）
2. 经历取舍（CP1）
3. 内容缺口补全（CP2）
4. 量化追问（CP3，最多 2 轮）
5. 措辞升级（CP4）

---

## 工作原理

```
┌─────────────────────────────────────────────────────┐
│  LLM（读 SKILL.md，推动 Phase 前进）                   │
│                                                     │
│  ┌──────────┐    ┌──────────────┐   ┌────────────┐ │
│  │  Scout    │───▶│  Architect    │───▶│  Auditor   │ │
│  │ (调研员)  │    │  (撰写者x2)   │    │(审计员)    │ │
│  └──────────┘    └──────────────┘   └────────────┘ │
│       │                 │                  │        │
│       ▼                 ▼                  ▼        │
│  engine.py: Snapshot（黑板 / 唯一状态源）              │
│  renderer.py: MD → 解析 → HTML（纯标准库）            │
└─────────────────────────────────────────────────────┘
```

| 阶段 | 节点 | 做什么 | 你的角色 |
|------|------|--------|---------|
| 1. 背景 | Scout | JD 解析 + 公司调研 + 面经搜索 | 审阅确认 |
| 2. 匹配 | Architect | 直接匹配 + 隐性匹配 + 置信度 | 审阅匹配表 |
| 3. 调整 | Architect | 经历取舍 + 量化补充 + 措辞升级 | 确认或否决 |
| 4. 审计 | Auditor | 合规检查 + 编造阻断 + 面试官挑战 | 最终审阅 |
| 5. 面试准备 | Auditor | mock 问题 + STAR 笔记 | 审阅准备包 |

6 场景自动路由：A（JD+简历）/ A2（多JD）/ B（仅简历）/ C（仅JD）/ D（信息不足）/ E（造假拒绝）

---

## 开发者文档

<details>
<summary>文件结构</summary>

```
resume-tailor/
├── SKILL.md                    # Skill 定义与工作流路由表
├── README.md                   # 本文件（中文首页）
├── README.en.md                # English documentation
├── examples/                   # 测试 prompt 与预期行为
├── schemas/
│   └── snapshot_schema_v1.json # 快照 Schema v1.2
├── templates/
│   ├── resume_swiss.html       # 瑞士国际主义风模板
│   └── state_update_template.md
├── scripts/
│   ├── engine.py               # 状态管理（Snapshot）
│   ├── renderer.py             # MD → HTML 渲染器
│   ├── jd_parser.py            # JD + 简历结构化提取
│   ├── diff_audit.py           # 源 vs 定制变更分析
│   ├── ats_checker.py          # ATS 兼容性评分
│   ├── main.py                 # 统一 CLI
│   └── utils.py                # 共享工具函数
├── references/                 # 节点指令手册 + 审计清单
├── sessions/                   # 活跃会话（.gitignore）
└── history/                    # 已归档会话
```

</details>

<details>
<summary>依赖项</summary>

渲染管线**零外部依赖**。`renderer.py` 仅用 `json`、`re`、`pathlib`。

```bash
python-docx>=0.8.11    # .docx 读取（非渲染必需）
pdfplumber>=0.10.0     # PDF 读取（非渲染必需）
```

</details>

<details>
<summary>脚本使用</summary>

```bash
# JD 特征提取
python -X utf8 scripts/main.py parse jd.txt --file --resume resume.docx --json

# 源 vs 定制 diff
python -X utf8 scripts/main.py diff --source resume_master.md --tailored tailored.md --json

# ATS 兼容性检查
python -X utf8 scripts/main.py ats --resume tailored.md --keywords "Python,SQL" --region north_america

# Markdown → HTML 渲染
python -X utf8 scripts/renderer.py --md draft.md --output output/
```

</details>

<details>
<summary>自定义样式</summary>

编辑 `templates/resume_swiss.html`，CSS 变量驱动：

```css
:root {
  --ink: #2d3748;          /* 正文颜色 */
  --ink-light: #718096;    /* 次要文字 */
  --fs-body: 11pt;         /* 正文字号 */
  --lh-tight: 1.5;         /* 行高 */
}
```

</details>

---

## 版本历史

见 [CHANGELOG.md](CHANGELOG.md)。

| 版本 | 日期 | 要点 |
|------|------|------|
| **v3.4** | 2026-06 | 6 场景路由、编造阻断门、信息状态标记、面试准备包 |
| **v3.3** | 2026-06 | 三层联网搜索、零依赖渲染、瑞士风 HTML 模板 |
| **v3.2** | 2026-05 | 初始化系统、Agent 反模式、Darwin 76→92 |

---

MIT
