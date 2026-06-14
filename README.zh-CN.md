<div align="center">

# Resume Tailor

**AI 驱动的简历定制 — 不是润色工具，是求职教练**

*本项目遵循"教练而非润色器"的理念。*

[English](README.md) · [简体中文](README.zh-CN.md)

**v3.4 — 6 场景路由 + 编造阻断门 + 压测修复

[更新日志 →](CHANGELOG.md)

</div>

## 为什么需要它？

大多数 AI 简历工具只会**改写**你的 bullet 让它听起来很厉害。而这个工具**引导**你让它们变得真实。

| 传统 AI 改写 | Resume Tailor |
|---|---|
| ❌ "显著提升了数据分析效率，获得团队认可" | ✅ "主导搭建自动化对账工具，将月度核算周期从 **5 天缩短至 6 小时**，覆盖 **12 条业务线**" |
| 缺少数据时就用空泛形容词填充 | 用场景化追问引导量化 — 说不出数字就保留原文 |
| 对角色盲目乐观（什么都是"主导"） | 每条声明都挑战你：*"你是最终决策者吗？"* |
| 千篇一律的输出 | 根据目标地区自动调整语调、格式、隐私规则 |

**区别**：一份被精心包装的谎言会在面试中被戳穿。一份经过教练打磨的真实经历能帮你拿到 offer。

---

## 你将得到什么

你不只得到一份定制简历。你得到一套**求职攻略包**。

### 📄 定制简历（HTML / Markdown）
针对特定 JD 和目标地区优化：
- **HTML**：瑞士国际主义风（`templates/resume_swiss.html`），单文件自包含，零外部依赖，A4 打印优化
- **Markdown**：可读、可 diff、可进 Git 版本审计 — 简历的"源代码"
- **PDF**：不在 pipeline 内自动生成。用浏览器 Ctrl+P → 保存为 PDF

### 📊 审计日志
每项修改都有据可查：
- 每个 JD 要求的匹配置信度评分
- 硬性缺口标记（缺失证书、经验门槛）
- 合规预警（按地区提示删除照片/年龄等）

### 🎙️ 面试准备包
对简历上的每一处重大修改，系统自动生成：
- **模拟追问** — 面试官可能会挑战你的问题
- **STAR 笔记** — 结构化回答要点，让你能自信地捍卫每一条经历

---

## 核心原则

这些是写入每一次运行的不可协商的硬规则：

### 🚫 拒绝空话（Anti-Filler Rule）
每条经历必须满足：**动作 + 对象 + 可量化成果**
- 说不出数字？系统用递进式追问引导回忆。
- 追问两轮仍无果？保留原文措辞——绝不编造指标。
- **铁律：空泛的结果比没有结果更差。**

### 🪞 反向审计（物理隔离）
交付前，独立的审计员画像从攻击者视角审视每一条经历。撰写者和审计员是两次独立的 LLM 调用——不存在"自我审计"的偷工减料。

### 🚧 编造阻断门（v3.4）
10 条真实性硬规则逐条检查每个 bullet。任何一条违规 → 整份草稿 ROLLBACK。数字必须有源、动词等级必须有证、技能不能凭空出现、时间线不能矛盾。

### 🔖 信息状态标记（v3.4）
每条声明标注为 `[✓]` 已确认（用户验证）、`[?]` 待确认（提取但未验证）、`[~]` 模型推断（LLM 推导）。推断内容自动升级审计严重度，**禁止**进入最终交付物。

### ⏳ 事实守恒
工作经历严格按**时间倒序排列**。不允许按相关性重排——只能保留或隐藏。

### 🌐 文化语调滑块
动词强度自动调整：自信果断（北美）→ 协同低调（东亚）→ 谦逊务实（北欧）。同样的内容，不同的呈现方式。

### ⚖️ 跨证书对齐
雅思 7.5 ≈ 六级 550+。系统跨地区映射证书等价关系，并保留最具说服力的那一个。

---

## 架构：LLM 即编排器 + 黑板状态

Resume Tailor v3.4 以 **LLM 即编排器（LLM-as-Orchestrator）** 的 Skill 方式运行。LLM 读取 `SKILL.md`，自行推进 Phase，按需调用 `scripts/` 工具。没有 Python 进程驱动 LLM — 是 LLM 驱动 Python 工具。

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
│  ── jd_facts 层（JD + 简历 + 调研）                  │
│  ── user_decisions 层（用户决策 + 元数据）            │
│  ── expert_outputs 层（草稿 + 审计日志）              │
│                                                     │
│  ┌──────────────────────────────────────────┐      │
│  │    renderer.py: MD → 解析 → HTML            │      │
│  │    （纯标准库，零外部依赖）                   │      │
│  └──────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────┘
```

### 专家节点

| 节点 | 角色 | 核心职责 |
|------|------|---------|
| **Scout** | 调研分析师 | JD 解析、市场调研、能力簇提取 |
| **Architect (Writer)** | 简历架构师 | 经历取舍、缺口补全、量化补充、草稿定稿 |
| **Architect (Quantify)** | 数据专员 | 指标提取、递进式量化追问 |
| **Auditor** | 独立审计员 | 合规检查、面试官画像挑战 |

### 状态协议

所有状态存储在 `snapshot.json` —— 一个分层 JSON 文档：
- **Layer 0 (`_meta`)**: 会话元数据、轮次历史、语义缓冲区
- **Layer 1 (`jd_facts`)**: 原始 JD + 简历 + 调研数据
- **Layer 2 (`user_decisions`)**: 所有用户确认、否决、偏好
- **Layer 3 (`expert_outputs`)**: 节点输出（调研报告、草稿、审计日志）

---

## 渲染管线

零依赖模板替换管线：

```
Phase 4a Writer 产出（Markdown）
    ↓
renderer.py: 解析 Markdown 为结构化节段
  - h1 → 姓名 + 联系方式
  - h2 → 节边界（summary/experience/education/skills）
  - h3 → 条目标题
  - **前缀**：详情 → bullet 标签 + 正文
    ↓
模板替换 → templates/resume_swiss.html
  {{NAME}} {{SUBTITLE_BLOCK}} {{CONTACT_ITEMS}}
  {{SUMMARY_BLOCK}} {{EXPERIENCE_SECTION}}
  {{PROJECTS_SECTION}} {{EDUCATION_SECTION}}
  {{SKILLS_SECTION}}
    ↓
填充后的 HTML（瑞士国际主义风）
  单文件，纯 Python 标准库，零外部依赖
  浏览器 Ctrl+P → 保存为 PDF
```

**关键设计决策：**
- **模板替换替代 Jinja2** — 不使用模板引擎。直接 `str.replace()` + Python 标准库。
- **段级占位符** — {{EXPERIENCE_SECTION}} 承载完整 HTML 块，而非逐字段模板。
- **无 PDF/DOCX 依赖** — 浏览器原生处理 PDF 转换。DOCX 完全移除。
- **renderer.py 纯标准库** — 仅用 `json`、`re`、`pathlib`。无需 pip install。

---

## 工作原理

### 6 场景自动路由（v3.4）

系统根据输入自动识别场景并路由至对应流水线：

| 场景 | 输入 | 流水线 |
|------|------|--------|
| **A** | JD + 简历 | 完整定制（Scout → Architect → Auditor → 渲染） |
| **A2** | 多个 JD + 简历 | 批量定制，共享事实底稿 + 跨 JD 差异对比表 |
| **B** | 仅简历 | 故事库驱动的提炼优化（无 JD 匹配） |
| **C** | 仅 JD，无简历 | 建议性输出（缺口分析 + 准备指南） |
| **D** | 信息不足 | 引导式采集（结构化提问后再继续） |
| **E** | 用户要求造假 | 硬拒绝并说明理由 |

### 流水线阶段（Mode A）

| 阶段 | 节点 | 做什么 | 你的角色 |
|------|------|--------|---------|
| **1. 背景** | **Scout** | JD 要求提取、公司调研、面经搜索 | 审阅确认 |
| **2. 匹配** | **Architect** | 直接匹配 + 隐性匹配，标注置信度 | 审阅匹配表 |
| **3. 调整** | **Architect** | 经历取舍、缺口补全、量化补充、措辞升级 | 确认或否决每条建议 |
| **4. 审计** | **Auditor** | 合规检查 + 编造阻断门 + 面试官画像挑战 | 最终审阅 |

每个建议都附带具体方案——你只需要确认或否决，不需要从零开始做决策。

---

## 快速开始

```bash
# 提供 JD 和简历
"帮我针对这个 JD 调简历"
```

就这么简单。系统会自动完成调研、匹配、调整、审计和渲染全流程。

---

## 开发者文档

<details>
<summary>📁 文件结构</summary>

```
resume-tailor/
├── SKILL.md                              # Skill 定义与工作流路由表
├── README.md                             # 英文文档
├── README.zh-CN.md                       # 本文件
├── requirements.txt                      # Python 依赖项（渲染零依赖）
├── schemas/
│   └── snapshot_schema_v1.json           # 快照 Schema（v1.2 含 info_status + 多 JD）
├── templates/
│   ├── resume_swiss.html                 # 瑞士国际主义风模板（CSS 变量驱动）
│   └── state_update_template.md          # STATE_UPDATE JSON 模板与范例
├── scripts/
│   ├── engine.py                         # 状态管理（Snapshot、parse_state_update）
│   ├── renderer.py                       # MD → HTML 渲染器（纯标准库）
│   ├── jd_parser.py                      # JD + 简历结构化提取
│   ├── diff_audit.py                     # 源简历 vs 定制简历变更分析
│   ├── ats_checker.py                    # ATS 兼容性评分（5 地区配置）
│   ├── main.py                           # 统一 CLI（parse / diff / ats）
│   └── utils.py                          # 共享工具函数（JSON 校验、PII 等）
├── references/
│   ├── writer_guide.md                   # Writer 节点指令手册（Phase 1 + CP1-CP5）
│   ├── auditor_guide.md                  # Auditor 节点指令手册（含编造阻断门 B-3）
│   ├── interaction_checkpoints.md        # Phase 3 检查点详情
│   ├── reverse_audit_checklist.md        # B-2/B-3 审计清单 + Mode B 专项规则
│   ├── formatting_rules.md              # 操作级格式指引（联系方式、bullet、技能栏）
│   └── audit_log_template.md             # 审计日志输出模板
├── sessions/                             # 活跃会话快照（已 .gitignore）
└── history/                              # 已归档的已完成会话
```

</details>

<details>
<summary>⚙️ 依赖项</summary>

```bash
# 核心依赖（渲染零外部依赖）
python-docx>=0.8.11          # .docx 读写
pdfplumber>=0.10.0           # PDF 读取（推荐——最优解析质量）

# v3.3+ 已移除
#   jinja2, markdown-it-py, python-markdown, weasyprint, pypandoc

# 可选降级方案（运行时自动检测）
#   PyPDF2>=3.0.0            — Python 原生 PDF 解析，无系统依赖
#   pdftotext (CLI)          — https://poppler.freedesktop.org/
```

**注意：** 渲染管线零外部依赖。
- `renderer.py` 仅使用 Python 标准库（`json`、`re`、`pathlib`）。
- HTML 是主输出格式。PDF 通过浏览器 Ctrl+P 生成。
- `python-docx` 和 `pdfplumber` 仅用于**读取**源简历——不用于生成输出。

</details>

<details>
<summary>🔧 脚本使用</summary>

```bash
# Windows：所有脚本处理中文需 UTF-8 模式
# 添加 -X utf8 参数或设置 PYTHONUTF8=1 环境变量

# JD 特征提取
python -X utf8 scripts/main.py parse jd.txt --file --resume resume.docx --json

# 源简历 vs 定制简历 diff
python -X utf8 scripts/main.py diff --source resume_master.md --tailored tailored.md --json

# ATS 兼容性检查
python -X utf8 scripts/main.py ats --resume tailored.md --keywords "Python,SQL" --region north_america

# 将 Markdown 草稿渲染为瑞士风 HTML
python -X utf8 scripts/renderer.py render --draft draft.md --output output/
```

**注意：** `engine.py` 提供 `Snapshot` 类和 `parse_state_update()`——由 LLM 作为工具调用。不存在 Python 驱动的编排循环。LLM 读取 `SKILL.md`，自行推进 Phase，按需调用脚本。

</details>

<details>
<summary>🎨 自定义样式</summary>

编辑 `templates/resume_swiss.html`。所有样式在 `<style>` 块内，由 `:root` 中的 CSS 自定义属性驱动：

```css
:root {
  --ink: #2d3748;              /* 正文颜色 */
  --ink-light: #718096;        /* 次要文字 */
  --rule: #e2e8f0;             /* 分割线颜色 */
  --fs-body: 11pt;             /* 正文字号 */
  --lh-tight: 1.5;             /* 行高 */
  --sp-3: 10px;                /* 节间距 */
  --grid-col-gap: 10px;        /* 日期列间距 */
}
```

模板设计用于 **A4 纵向，单页排版**。调整 `--fs-body` 和 padding 值来适配更多或更少的内容。

</details>

---

## 版本历史

完整更新日志见 [CHANGELOG.md](CHANGELOG.md)。

| 版本 | 日期 | 要点 |
|------|------|------|
| **v3.4** | 2026-06 | 6 场景路由、编造阻断门、信息状态标记、多 JD 批量定制、压测修复 |
| **v3.3** | 2026-06 | 三层联网搜索、零依赖渲染、瑞士风 HTML 模板、移除 DOCX |
| **v3.2** | 2026-05 | 初始化系统、Agent 反模式（A1–A7）、Darwin 76→92 |
| **v3.1** | 2026-05 | Init-A/B、故事库、历史版本审计、Darwin 74→91 |
| **v3.0** | 2026-04 | 多智能体架构、黑板状态、HTML/DOCX/PDF 管线 |
| **v2.4** | 2026-04 | 四阶段流水线、拒绝空话规则、反向审计 |

---

## 许可证

MIT
