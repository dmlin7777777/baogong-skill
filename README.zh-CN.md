<div align="center">

# Resume Tailor

**AI 驱动的简历定制 — 不是润色工具，是求职教练**

*本项目遵循"教练而非润色器"的理念。*

[English](README.md) · [简体中文](README.zh-CN.md)

**v3.3 — 渲染管线重构 (HTML/MD 双主交付 + 瑞士国际主义风)

</div>

---

## v3.3 更新内容

### 结构化联网搜索
**Phase 1 从模糊的"市场调研"升级为三层结构化联网搜索策略：**

**S1 — 面经挖掘**
搜索 `"{公司} {岗位} 面经"` / `"{岗位} 面试题"` 等模式，提取：
- 面试官真实追问（不是 JD 上写的要求）
- 高频考点和隐性门槛
- → 驱动 CP3 量化追问方向，让 Phase 4c mock 问题有真实面经做依据

**S2 — 公司文化 & 真实工作内容**
搜索 `"在 {公司} 做 {岗位} 是怎样体验"` / `"{公司} 技术栈"`，提取：
- 实际使用的技术栈（往往和 JD 写的不同）
- 团队风格和文化关键词
- → 校准 Phase 2 技能匹配权重和 CP4 文化语气 slider

**S3 — 业务信号**
搜索 `"{公司} 业务重点"` / `"{公司} 组织架构调整"`，提取：
- 营收重点、新产品线、组织变动
- → 输入 `risk_warnings`（标注业务收缩部门）和 `capability_clusters` 定向

每轮搜索产出落地到指定下游节点（无空转搜索 — 更新的 A6 反模式强制约束）。提取的情报保存为 `history/{date}_{company}_{role}_interview_intel.md`。

### 渲染管线重构 — HTML/MD 双主交付

**旧架构**：MD → markdown-it → Jinja2 → WeasyPrint PDF + pandoc DOCX（4 个 Python 包依赖，Windows 上常不可用）

**新架构**：

| 格式 | 优先级 | 说明 |
|------|--------|------|
| **Markdown** | 主交付物 | Phase 4a Writer 直接产出，可读、可 diff、可进 Git 版本审计 |
| **HTML** | 主交付物 | `templates/resume_swiss.html` 瑞士国际主义风模板，单文件自包含，浏览器直接打开 |
| PDF | 用户侧生成 | 浏览器 Ctrl+P → 保存为 PDF，**不在 pipeline 内自动执行** |
| DOCX | 已移除 | 移除 WeasyPrint / pandoc / pypandoc 全部依赖 |

**HTML 模板设计原则**（继承自 guizang-ppt Swiss 风格）：
- 信息优先，零装饰（无阴影、圆角、渐变）
- 字体层级：越大越细（name 300 → body 400 → meta 600）
- 单文件自包含，CSS 变量驱动，零外部依赖
- A4 打印优化：`@page { size: A4 }` + 浏览器直接打印
- 字体：Inter (Latin) + Noto Sans SC / Microsoft YaHei (CJK)

---

## v3.2 更新内容

**Darwin Skill 5轮优化：76 → 92（+16）**，基于 9 维 SkillLens 评估框架。

### 新增：初始化系统（Onboarding）
首次使用不再卡壳。两条引导式初始化路径：

- **Init-A（Master 简历）**：自动检测已有简历文件 → 结构化 `resume_master.md`；若从零开始，通过 5 轮引导问卷逐条收集
- **Init-B（故事库）**：逐段经历录入 STAR + 量化数据 + 面试追问准备，在 Mode B 入口或 CP3 量化追问失败时触发

### 新增：Agent 执行反模式（A1–A7）
7 条专门针对 LLM 自主执行时的错误防范规则：Writer/Auditor 隔离违规、MODE 判断未确认直接推进、STATE_UPDATE 解析失败静默继续、Phase 执行顺序重排、空转 web_search 等。

### 新增：CP4 措辞边界（Wording Boundary）
硬边界表格——允许项（换动词、调语气、重组 bullet 结构）vs 禁止项（添加原文没有的事实描述、捏造指标、为对齐 JD 编造经历）。存疑时输出 before/after 等用户确认。

### 改进：Mode 检测协议
≥50 字阈值区分真实 JD 与模糊职位名称，歧义输入强制确认一次（每 session 最多触发一次）。

### 改进：错误处理具体化
全部 9 个错误场景改为具体动作指令，消除所有软化措辞；新增 `snapshot.json` 损坏/缺失的备份重建流程。

### 改进：Mode A 故事库接入
CP3 量化优先级链：故事库已有数字 > 用户当场提供 > 2 轮后写过程描述（不编造）。

---

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

### ⏳ 事实守恒
工作经历严格按**时间倒序排列**。不允许按相关性重排——只能保留或隐藏。

### 🌐 文化语调滑块
动词强度自动调整：自信果断（北美）→ 协同低调（东亚）→ 谦逊务实（北欧）。同样的内容，不同的呈现方式。

### ⚖️ 跨证书对齐
雅思 7.5 ≈ 六级 550+。系统跨地区映射证书等价关系，并保留最具说服力的那一个。

---

## 架构：LLM 即编排器 + 黑板状态

Resume Tailor v3.3 以 **LLM 即编排器（LLM-as-Orchestrator）** 的 Skill 方式运行。LLM 读取 `SKILL.md`，自行推进 Phase，按需调用 `scripts/` 工具。没有 Python 进程驱动 LLM — 是 LLM 驱动 Python 工具。

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

## 渲染管线（v3.3）

v3.3 使用**零依赖模板替换管线**：

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

```
Phase 1 — 背景调研与上下文     Scout 解析 JD、提取要求、调研市场
Phase 2 — 语义匹配            Architect 将经历与 JD 逐一比对、提出建议
Phase 3 — 交互式调整           用户确认、填补缺口、量化指标
Phase 4 — 审计交付             独立审计员审查、渲染器生成输出文件
```

| 阶段 | 节点 | 做什么 | 你的角色 |
|------|------|--------|---------|
| **1. 背景** | **Scout** | JD 要求提取、公司调研、风险评估 | 审阅确认 |
| **2. 匹配** | **Architect** | 直接匹配 + 隐性匹配，标注置信度 | 审阅匹配表 |
| **3. 调整** | **Architect** | 经历取舍、缺口补全、量化补充、措辞升级 | 确认或否决每条建议 |
| **4. 审计** | **Auditor** | 物理隔离合规检查 + 面试官画像挑战 | 最终审阅 |

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
├── requirements.txt                      # Python 依赖项（v3.3 — 渲染零依赖）
├── schemas/
│   └── snapshot_schema_v1.json           # 快照 Schema（v1.1 含语义缓冲区）
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
│   ├── auditor_guide.md                  # Auditor 节点指令手册
│   ├── interaction_checkpoints.md        # Phase 3 检查点详情
│   └── audit_log_template.md             # 审计日志输出模板
├── sessions/                             # 活跃会话快照（已 .gitignore）
├── history/                              # 已归档的已完成会话
└── docs/
    └── plans/
        └── 2026-04-15-v3-architecture-design.md  # 完整架构设计文档
```

</details>

<details>
<summary>⚙️ 依赖项</summary>

```bash
# 核心依赖（v3.3 — 渲染零外部依赖）
python-docx>=0.8.11          # .docx 读写
pdfplumber>=0.10.0           # PDF 读取（推荐——最优解析质量）
pyyaml>=6.0                  # Snapshot Schema 的 YAML 支持

# v3.3 已移除
#   jinja2, markdown-it-py, python-markdown, weasyprint, pypandoc
#   — 已被零依赖模板替换管线替代。

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
# JD 特征提取
python scripts/main.py parse jd.txt --file --resume resume.docx --json

# 源简历 vs 定制简历 diff
python scripts/main.py diff --source resume_master.md --tailored tailored.md --json

# ATS 兼容性检查
python scripts/main.py ats --resume tailored.md --keywords "Python,SQL" --region north_america

# 将 Markdown 草稿渲染为瑞士风 HTML
python scripts/renderer.py render --draft draft.md --output output/
```

**注意：** `engine.py` 提供 `Snapshot` 类和 `parse_state_update()`——由 LLM 通过 `python -c "from scripts.engine import Snapshot; ..."` 调用。不存在 Python 驱动的编排循环。LLM 读取 `SKILL.md`，自行推进 Phase，按需调用脚本。

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

### v3.3（当前）— 结构化联网搜索 + 渲染管线重构
- **三层搜索**：S1 面经挖掘 → S2 公司文化/真实工作内容 → S3 业务信号
- **面经情报交付**：`history/{date}_{company}_{role}_interview_intel.md`
- **Phase 4c 集成**：Mock 面试问题取材自真实面经（S1），不再凭空构造
- **渲染管线重构**：HTML（瑞士国际主义风）+ Markdown 双主交付，移除 WeasyPrint / pandoc / DOCX 依赖
- **瑞士风 HTML 模板**：`templates/resume_swiss.html`，CSS 变量驱动，单文件自包含，浏览器直接打印
- **A6 反模式更新**：每轮搜索结果必须落地到指定下游节点，否则不执行
- **CP3 量化定向**：量化追问方向由面试官真实关注点驱动

### v3.2 — Darwin 5轮优化 + 初始化系统
- **Darwin SkillLens 9 维评估**：76 → **92**（+16）via 5 轮优化循环
- **Onboarding Check**：全局前置门卫——`resume_master.md` 缺失 → 先 Init-A 再进入任何流程
- **Init-A（Master 简历）**：3 种录入路径（粘贴/文件/5 轮问卷）→ 结构化 `resume_master.md`
- **Init-B（故事库）**：逐段经历 STAR 录入，含量化数据 + 面试追问准备
- **Agent 执行反模式（A1–A7）**：LLM 特有错误防范（隔离违规、静默失败、顺序重排、空转搜索）
- **CP4 措辞边界**：显式表格——允许项（动词/语气/结构）vs 禁止项（捏造、范围膨胀）
- **Mode 检测协议**：≥50 字阈值 + 歧义输入强制确认
- **Mode A 故事库接入**：CP3 量化优先级链（故事库 > 用户回复 > 过程描述）
- **frontmatter 权限声明**（Read/Write/Glob/WebFetch/WebSearch/Bash）
- **错误处理具体化**：全部 9 个错误场景改为具体动作指令；snapshot 损坏备份重建流程

### v3.1 — 初始化 + 故事库 Mode A 接入
- Init-A（Master 简历创建）+ Init-B（故事库创建）
- Mode A 故事库接入 CP3 量化备援
- 真实执行模拟后暴露缺失初始化路径，版本升级

### v3.0 — 多智能体 + 渲染管线（Darwin 优化前）
- **伪多智能体架构**，隔离的 Scout / Architect / Auditor 节点
- **黑板状态协议**通过 `context_snapshot.json`（4 层 Schema v1.1）
- **HTML 渲染管线**，使用 Jinja2 模板 + CSS 样式
- **WeasyPrint PDF** 输出，带页数溢出检测 → 自动触发压缩指令
- **pypandoc DOCX** 干净转换（无 HTML→Word 格式问题）
- **Darwin Skill 9 维评估**（v3.0 时期）：74.3 → 90.5（+16.2）
- **历史版本审计**（Step 4e）：对比最近 3 版简历，防止量化倒退
- **故事库协议**：3 层递进读取策略 + 审计交叉验证

### v2.4 — 结构性重构
- 4 阶段流水线，3 级路由，统一特征提取
- Anti-Filler Rule、Propose-don't-ask 原则、反向审计
- 影子副本改为按需触发

[完整更新日志 → CHANGELOG.md](CHANGELOG.md)

---

## 许可证

MIT
