---
name: resume-tailor
description: "针对岗位 JD 定制简历，或生成通用方向简历。分析 JD 关键词、匹配源简历、交互式调整建议、反向诚意审计。HTML（瑞士国际主义风）+ Markdown 双主交付，支持面经联网搜索。触发词：调简历、tailor resume、优化简历、生成简历、通用简历、简历定制、resume for this JD"
version: "3.3"
required_permissions:
  - Read    # 读取源简历、故事库、JD 文本
  - Write   # 写入定制后简历、snapshot、history/
  - Glob    # 自动定位 resume_master.md 和故事库文件
  - WebFetch # 抓取 JD URL
  - WebSearch # 市场调研 + 面经搜索
---

# Resume Tailor v3

**Pseudo Multi-Agent + Blackboard Architecture**

Analyze a job description and tailor the source resume to match, using isolated expert nodes for writing and auditing.

## Trigger Phrases

**⚠️ 优先级规则：所有触发词（含 Mode A / Mode B）先执行 Onboarding Check。**
`resume_master.md` 不存在 → 无论用户说的是 Mode A/B 还是 Init，先进入 Init-A。
`resume_master.md` 已存在 → 按下方分类判断 Mode。

**Init（新用户初始化）：**
- "帮我创建简历" / "我还没有简历" / "从头做简历"
- "建一个故事库" / "帮我整理经历" / "我想记录项目经历"
- "create resume from scratch" / "build my resume"
- 所有触发词，如果检测不到 resume_master.md → 自动进入 Init-A

**Mode A (JD-Targeted):**
- "帮我针对这个 JD 调简历" / "tailor my resume for this JD"
- "优化简历给这个岗位" / "optimize resume for this role"
- Any JD text or URL provided with resume adjustment intent

**Mode B (General-Purpose):**
- "帮我针对产品岗位生成一个通用性的简历"
- "做个通用版简历" / "生成XX方向的简历"
- "make a general resume" / "create a role-oriented resume"
- "简历定制" / "简历优化"

## Onboarding Check（所有流程的前置门卫）

**在执行任何 Mode A / Mode B 流程之前，必须先检查两个资产是否存在：**

```
检查 resume_master.md
    ├─ Glob **/resume_master.md 找到 → 记录路径，进入 Mode Detection
    └─ 未找到 → 🔴 STOP，进入 【Init-A：创建 Master 简历】

检查故事库（仅 Mode B 需要，或 Mode A 的 CP3 量化备援需要）
    ├─ Glob **/项目故事库.md 或 **/story-library.md 找到 → 记录路径
    └─ 未找到 → 在 Mode B 入口 或 CP3 量化追问失败时触发 【Init-B：创建故事库】
```

**🔴 STOP 规则**：
- `resume_master.md` 不存在 → 不论用户要做什么，先完成 Init-A，再继续
- 故事库不存在且用户选择 Mode B → 先完成 Init-B，再进入 Phase G1
- 故事库不存在但用户选择 Mode A → 进入 Mode A，CP3 量化追问如用户无法回答则跳过，**不强制先建故事库**

---

### Init-A：创建 Master 简历（首次使用）

**目标**：从用户已有的任意格式简历（.docx/.pdf/.txt/粘贴文字），生成结构化 `resume_master.md`。

**流程**：

```
Step A1：获取原始简历
  输出：「我没有找到你的简历文件，需要先创建一份 Master 简历作为所有后续定制的基础。
         请选择：
         (1) 粘贴你现有简历的文字内容
         (2) 提供简历文件路径（.docx / .pdf）
         (3) 从头开始，我来引导你填写」
  → 等待用户回复

Step A2：解析原始内容
  - 如果是文件路径 → 用 python-docx 或 pdfplumber 读取全文
  - 如果是粘贴文字 → 直接处理
  - 如果从头填写 → 进入 Step A2b（引导式问卷，见下）

Step A3：结构化提取 → 输出 resume_master.md（见模板）
  - 用标准节段：个人信息 / 教育 / 工作经历 / 项目经历 / 技能 / 证书
  - 每段经历必须包含：公司名、职位、时间区间、bullet 列表（暂时保留原始表述，不升级）
  - 时间格式统一：YYYY.MM – YYYY.MM（或"至今"）
  - 🔴 严禁：在此阶段修改任何数字或添加任何原文没有的描述

Step A4：确认 + 存档
  - 🔴 STOP CP：展示结构化后的 resume_master.md 给用户确认
  - 用户确认 → 写入 {workspace}/resume_master.md
  - 在 .workbuddy/memory/MEMORY.md 中记录 resume_path 字段
  - 输出：「Master 简历已创建并保存到 {path}，后续所有简历定制都以此为基础。」
```

**Step A2b（从头填写引导问卷）**：

每次只问 1 个问题，等用户回答后继续，共 5 轮：

| 轮次 | 问题 |
|------|------|
| 1 | 「你的姓名、邮箱、电话、当前所在城市？」 |
| 2 | 「最高学历：学校、专业、学位、时间？还有其他学历吗？」 |
| 3 | 「最近一段工作/实习经历：公司、职位、时间、主要做了什么（1-3 句话）？」|
| 4 | 「还有其他工作/实习/项目经历吗？请逐条描述（可以多条）。」 |
| 5 | 「技能（如编程语言、工具、软件）？证书（如英语成绩、专业资格）？」 |

收集完成后进入 Step A3。

---

### Init-B：创建故事库（首次 Mode B 使用，或 CP3 量化追问失败时）

**目标**：把每段经历的 STAR 细节、量化数据、追问准备系统化地记录下来，形成简历写作的「唯一事实来源」。

**何时触发**：
- Mode B 入口检测到故事库不存在
- Mode A / Mode B 的 CP3 量化追问 2 轮后用户无法给出数字（主动建议创建，而非强制）

**流程**：

```
Step B1：说明价值
  输出：「故事库是让简历里的每个数字都能在面试中答出来的保障。
         我来引导你把每段经历的细节录入，大约需要 10-20 分钟，
         建好后所有简历版本都从这里取数据。准备好了告诉我。」
  → 等待用户确认

Step B2：逐段录入（每段经历循环一次）
  依次对每段工作/实习/项目经历：

  问题 B2-1：「[经历名称] 的核心成果是什么？有没有具体数字？
              （如：将 X 从 A 提升到 B，节省了 C 小时，影响了 D 个用户）」
  问题 B2-2：「如果没有数字，当时的规模/范围是什么？
              （如：覆盖了几个业务线？团队几个人？项目持续多久？）」
  问题 B2-3：「面试官最可能追问的 1 个问题是什么？你会怎么回答？」

Step B3：生成故事库文件（见模板）
  - 每个经历 = 一个 ## 节，包含：STAR 格式 + 量化数据 + 追问准备
  - 🔴 严禁：推断或填充用户没有提供的数字

Step B4：确认 + 存档
  - 🔴 STOP CP：给用户预览故事库，确认无误后写入文件
  - 写入 {workspace}/project-story-library.md
  - 在 .workbuddy/memory/MEMORY.md 中记录 story_library_path 字段
```

**故事库文件模板**：

```markdown
# 项目故事库

## 经历 1：[公司] · [职位] · [时间区间]

> 技术栈/工具：[列出主要工具]
> 一句话概括：[核心动作 + 量化结果]

### 核心成果（量化）
- [数字/指标 1]：来源：[用户原话]
- [数字/指标 2]：来源：[用户原话]
- 暂无量化数据 → 规模：[范围描述]

### STAR
- **S（背景）**：[情境]
- **T（任务）**：[目标]
- **A（行动）**：[具体做了什么]
- **R（结果）**：[量化结果或过程描述]

### 面试追问准备
- Q：[最可能被追问的问题]
- A：[回答要点]

---
```

---

### Mode A 的故事库接入（CP3 量化备援）

**Mode A 原本只依赖用户回复量化数据，现在补充以下规则：**

在 CP3 量化追问时，**优先顺序**如下：

```
优先级 1：故事库中已有数字 → 直接使用，标注「来源：故事库」
优先级 2：用户在对话中提供数字 → 使用，更新到故事库对应条目
优先级 3：追问 2 轮后用户仍无数字 → 写过程描述，不编造
                                    → 询问「要不要顺便把这段经历录入故事库，下次就有数据了？」
```

---

## Resume Input

On first run, **try auto-detection first**:
1. `Glob **/resume_master.md` in workspace — if found, use it directly
2. If workspace has `resume_master.md` or `.workbuddy/memory/MEMORY.md` with a resume path, follow that
3. **Auto-detect fails → 不是直接报错，而是触发 【Init-A：创建 Master 简历】**

**Story library path** (for Mode B capability matching): `{vault}/project-story-library.md`
- Use `Glob **/项目故事库.md` or `Glob **/story-library.md` to auto-locate
- **Auto-detect fails → 在 Mode B 入口触发 【Init-B：创建故事库】**

Store the resolved paths in workspace memory. **Never modify the original.**

## Mode Detection Protocol（先于 Operating Modes 执行）

在判断进入 Mode A 还是 Mode B 之前，执行以下决策树：

```
用户输入到达
    │
    ├─ 包含完整 JD 文本（≥ 50 字且含职责/要求描述）
    │    → 直接进入 Mode A
    │
    ├─ 包含 URL（http/https 开头）
    │    → WebFetch 获取内容；字数 ≥ 50 字 → Mode A；失败或内容不足 → 走「输入模糊」分支
    │
    ├─ 只有职位名称或方向词（如「数据分析师」「产品岗」< 50 字）
    │    → 输出「我检测到的是职位方向，没有具体 JD。
    │         有 JD 可以粘贴，或者直接告诉我你想做哪个方向，我用 Mode B 帮你生成通用简历。」
    │         → 等待用户回复后再判断 Mode
    │
    └─ 用户明确说「不需要 JD」或「通用简历」
         → 直接进入 Mode B，跳过确认问询
```

**🔴 STOP — 歧义输入不允许自行判断 Mode，必须问用户一次。每个 session 最多触发一次此确认。**

## Operating Modes

Resume Tailor has two operating modes, determined by whether a JD is provided:

### Mode A: JD-Targeted（有 JD 定制）

Full 4-phase pipeline. This is the primary mode.

**Trigger**: User provides a JD (text, URL, or file) alongside resume adjustment intent.

**Flow**: Phase 1 → Phase 2 → Phase 3 → Phase 4 (see Workflow Pipeline below)

### Mode B: General-Purpose（无 JD 通用）

Simplified pipeline when no specific JD is available. Builds a role-oriented resume using capability matching from the story library.

**Trigger**:
- User asks for a resume "for X role" without providing a JD
- "帮我针对产品岗位生成一个通用性的简历"
- "做个通用版简历" / "make a general resume"
- "生成XX方向的简历" / "create a role-oriented resume"

**Flow**:

```
Phase G1: Capability Matching (replaces Phase 1+2)
  1. Identify target role type from user's description (e.g., 产品/数据/商业分析)
  2. Read project story library (唯一事实来源) → follow [[#Story Library Protocol]] for token-efficient extraction
  3. Build capability matching matrix: experience × core role competencies (numbers MUST come from story library)
  4. Rank experiences by match score
  5. Present selection recommendation to user (CP1)

Phase G2: Interactive Refinement (= Phase 3, CP1-CP4)
  **🔴 STOP CP1**: Experience selection → show ranked list → **WAIT for user picks**
  CP2: Skipped (no JD → no gap analysis)
  **🔴 STOP CP3**: Quantification audit (Anti-Filler Rule) → **WAIT for user to confirm or provide numbers**
  **🔴 STOP CP4**: Wording upgrade → show before/after → **WAIT for user approval**

Phase G3: Delivery & Audit (= Phase 4)
  Same physical isolation audit as Mode A.
  Additional Auditor check: "Does this bullet claim something not in the story library?"
```

**Key Differences from Mode A**:
- No JD → No `jd_facts` layer, no ATS keyword matching, no hard requirement alerts
- Story library is the **sole source of truth** — no fabrication, no speculation, no "logical inference"
- If story library lacks data for a bullet → ask user to confirm, never invent
- Simpler matching: role-type competencies instead of JD-specific keywords

**⚠️ Critical Rule for Mode B**: 
> **只做提炼，不做扩展。** Even logically reasonable inferences (e.g., "覆盖从需求定义到上线的完整周期") are FORBIDDEN unless explicitly stated in the story library. Only distill and reorganize what already exists.

## Story Library Protocol（Mode B 专用）

故事库是 Mode B 的唯一事实来源。不读故事库 = 不能生成 Mode B 简历。

### 故事库结构

故事库是一个结构化 Markdown 文件（通常位于 Obsidian vault 或 workspace 中），结构如下：

```
## 项目 N：名称
│
├── > 技术栈：...           ← 工具关键词
├── > 一句话概括：...        ← Phase G1 初筛用这个
├── ### NA：子项目名         ← 每个子项目 = 一段经历
│   ├── STAR（S/T/A/R）     ← 简历 bullet 的法定来源
│   ├── 高频追问准备         ← CP3 量化审计 + Phase 4 审计用
│   └── 方案选择与决策逻辑    ← 面试深度素材
└── ### 面试高频追问          ← 项目级追问
```

### 读取策略（Token高效，分 3 层递进）

**Layer 1 — 扫描标题（`grep "^## 项目"`）**
只读项目编号和名称，不看正文。目的：知道故事库覆盖了哪些经历、缺失哪些。

**Layer 2 — 初筛匹配（读 `> 一句话概括` + `> 技术栈`）**
对目标岗位相关的项目，只读一行概括。目的：2 秒判断这个项目要不要放进简历。

**Layer 3 — 深读（读完整 STAR + 追问）**
对确认入选的项目，读完整子条目。目的：提取真实的 bullet 措辞和量化数据。

❌ **禁止**：一次性读取整个故事库 → 浪费 token 且 Agent 注意力衰减。

### Phase G1：能力匹配矩阵

从 Layer 2 的一行概括中提取每段经历的：
- **核心动作**（做了什么）
- **量化结果**（数字是什么）
- **工具**（技术栈关键词）

然后对目标岗位的核心能力（如数据分析师 = SQL/Python/可视化/AB测试/ETL）逐项打分。**匹配矩阵中的数字必须来自故事库，不能编造。**

### Phase G2 CP3：量化审计

故事库中每个子项目的 STAR "R" 行是量化数据的唯一来源。CP3 追问时：
- 如果故事库已经有数字 → 直接用
- 如果故事库没数字 → 问用户
- 如果用户也答不出 → 用过程描述替代，**绝不编造**

### Phase G3 审计：故事库交叉验证

Auditor 逐条检查每个 resume bullet：“这个 bullet 能在故事库中找到对应证据吗？”

| 审计结果 | 含义 | 处理 |
|---|---|---|
| ✅ 故事库有对应 STAR | 证据充足 | 通过 |
| ⚠️ 故事库有对应条目但 bullet 措辞偏离 | 需要修正 | 回退 CP4 重写 |
| 🔴 故事库无此条目 | 无法面试辩护 | **删除该 bullet** 或让用户手动补故事库 |

## Five Core Principles

| # | Principle | One-Line Definition |
|---|-----------|---------------------|
| 1 | **Hybrid Analysis** | Script extracts hard facts (jd_parser.py), LLM extracts semantics. Cross-validate. |
| 2 | **Fact Conservation** | Strict reverse chronological order. Only inclusion/exclusion allowed. |
| 3 | **Semantic Equivalence** | Cross-credential mapping (IELTS ≈ CET-6). Cultural tone slider by region. |
| 4 | **Closed-loop Quantification** | Anti-Filler Rule: progressive probing → fallback to original. No vague outcomes. |
| 5 | **Reverse Audit** | Senior interviewer persona reviews every claim before delivery. 🔴 Major issues trigger rollback. |

## Architecture Overview

```
engine.py (Orchestrator)
├── Initialize snapshot.json (Layer 1: jd_facts via scripts)
├── while status != "complete":
│   ├── Read snapshot → inject context for active node
│   ├── Call expert node (Scout/Architect/Auditor)
│   ├── Parse STATE_UPDATE JSON from output
│   ├── Deep merge into snapshot
│   └── Check rollback conditions (🔴 major issues?)
├── Render final deliverables (MD + HTML via templates/resume_swiss.html)
└── Archive: sessions/ → history/
```

### Expert Nodes

| Node | File | Responsibility |
|------|------|---------------|
| **Context Scout** | `references/writer_guide.md` (Phase 1 section) | JD extraction, market research, role detection, capability clustering |
| **Resume Architect** | `references/writer_guide.md` (CP1-CP5) | CP1 selection, CP2 gaps, CP3 quantification, CP4 wording upgrade, CP5 draft |
| **Sincerity Auditor** | `references/auditor_guide.md` | Compliance check, sincerity review, mock interview questions, STAR prep |

### State Protocol

All nodes communicate via `context_snapshot.json` (see `schemas/snapshot_schema_v1.json`):
- **Layer 0 (`_meta`)**: Session metadata, turn history, nuance buffer
- **Layer 1 (`jd_facts`)**: Script-populated, read-only after init
- **Layer 2 (`user_decisions`)**: User-confirmed interactions, persistent
- **Layer 3 (`expert_outputs`)**: Node outputs, volatile, can be overwritten

Every node MUST append `STATE_UPDATE JSON` at end of output (see `templates/state_update_template.md`).

## Workflow Pipeline

### Phase 1: Contextual Intelligence

**Node**: Context Scout
**Reference**: `references/writer_guide.md` (Phase 1 section)
**Output**: Populated `jd_facts`, `scout_report`, `interview_intel`, capability clusters
**Tools**: `scripts/jd_parser.py` (with graceful fallback to LLM), `web_search`

1. Accept JD input (URL → fetch, or text directly)
2. Ask user: company name? target region?
3. Run **结构化联网搜索**（3 轮分层，每轮产出必须落地到下游节点）：

| 轮次 | 搜索目标 | 关键词模板 | 产出落地点 |
|------|---------|-----------|-----------|
| **S1 — 面经/面试经验** | 面试官真实追问、高频考点、岗位隐性要求 | `"{公司} {岗位} 面经"` `"{公司} 面试 经验"` `"{岗位} 面试题"` `"{公司} {岗位} 面试 准备"` | → CP3 量化追问定向 + Phase 4c mock 问题真实性 |
| **S2 — 团队/文化/真实工作内容** | 部门风格、实际技术栈、JD 写的 vs 实际做的差距 | `"{公司} {部门} 工作体验"` `"{公司} 技术栈"` `"在 {公司} 做 {岗位} 是怎样体验"` | → Phase 2 技能匹配权重 + CP4 语气 slider 校准 |
| **S3 — 公司动态/业务重点** | 财报方向、新产品线、组织架构变动 | `"{公司} 202X 业务 重点"` `"{公司} 组织架构 调整"` `"{公司} 财报 分析"` | → `risk_warnings`（业务收缩部门标注）+ `capability_clusters` 定向 |

**搜索执行规则**：
- **S1 必须执行**：面经是简历定制的关键上下文，直接影响 CP3 追问方向和 Phase 4c mock 问题的真实性
- **S2 条件执行**：公司知名度高（大厂/独角兽/上市公司）→ 必须执行；小型/冷门公司 → 降级为可选，避免无结果
- **S3 按需执行**：用户表达了目标公司的长期发展关切，或公司近期有重大新闻/裁员/业务调整时触发
- **每轮搜索结果必须至少影响一项下游产出**（见"产出落地点"列），否则标记为无效搜索（违反 A6）
- 搜索结果中提取的关键信息标注 `来源：[搜索关键词]`，存入 `scout_report` 和 `interview_intel`

4. Execute unified context extraction (script + LLM in one pass)
5. Detect role level, region, document type
6. Output consolidated context table + `interview_intel` 卡片（面经摘要 + 面试重点提示 + 文化关键词）+ risk warnings

### Phase 2: Strict Matching

**Node**: Context Scout (continuation) or Architect (if Fast-Track)
**Reference**: Integrated into Phase 1 or `references/writer_guide.md`

1. Read source resume (structured reader for .docx, fallback for .pdf)
2. Semantic matching: Direct + Implicit (with confidence) + Gaps
3. Cross-credential alignment
4. Match score calculation
5. Hard requirement alerts (dealbreakers)

**Match output must classify each JD requirement into one of 5 states:**

| State | Definition | Action |
|-------|-----------|--------|
| ✅ 已覆盖 | Direct, specific, verifiable evidence in resume | Polish wording at CP4 |
| 🟡 弱覆盖 | Related experience exists but lacks depth, specifics, or individual contribution | Probe at CP3 for quantification |
| ⬜ 未覆盖 | No evidence in current materials | Probe at CP3 for hidden experience |
| 🔍 可补充 | User likely has relevant experience not yet captured | Ask targeted questions at CP3 |
| ⛔ 不建议硬凑 | Clearly missing required credentials, industry, tools, or years of experience — no transferable path | Flag honestly. Tell the user: "这条不值得凑，硬写反而暴露缺口" |

**"不建议硬凑" judgment criteria:**
- Missing a hard credential (CPA, specific license, degree requirement)
- Missing required industry experience with no transferable overlap
- Missing required years of experience by a wide margin (e.g., JD asks 5+ years, user has 1)
- Required tool/framework the user has never used and cannot credibly claim

**This state is as important as "已覆盖" — telling the user what NOT to pursue saves them from interview exposure.**

### Phase 3: Dynamic Interaction

**🔴 CHECKPOINT · 🛑 STOP — 进入交互前确认用户在场，收到回复后再推进。**

**Node**: Resume Architect
**Reference**: `references/writer_guide.md`
**Sub-nodes**: `architect_writer` → `architect_quantify` → `architect_wording`
**Checkpoint details**: `references/interaction_checkpoints.md`

#### Step 3a: Three-Tier Routing

| Tier | Score | Flow |
|------|-------|------|
| **Fast-Track** | ≥90% | Draft + suggestions in one pass, skip deep CPs |
| **Full Flow** | 50–89% | CP1→CP2→CP3→CP4 all executed |
| **Alignment Check** | <50% | Confirm intent before proceeding |

#### Step 3b: Checkpoints (Always CP1, CP3, CP4; CP2 in Full Flow)

| CP | Name | What Happens |
|----|------|-------------|
| **🔴 STOP CP1** | Experience Selection | Reverse chronological review, user picks keep/hide. **WAIT for user confirmation before proceeding.** |
| CP2 | Content Gaps | Scenario-based gap filling (implicit matches) |
| **🔴 STOP CP3** | Quantification | Anti-Filler Rule: progressive probing. **WAIT for user to provide numbers or confirm "no data".** |
| **🔴 STOP CP4** | Wording Upgrade | Verb map, cultural tone slider, before→after comparison. **WAIT for user approval before writing draft.** |

**CP3 Progressive Probing Protocol** (when a bullet lacks quantification):

| Round | Question | Example |
|-------|----------|---------|
| 1 (Scope) | "影响了多少人/多少业务线？" | "全公司使用" / "覆盖 3 个 BU" |
| 2 (Comparison) | "改造前后分别是什么状态？用了多久？" | "从 48h 缩短到 12h" |
| 3 (Quality) | "准确率、错误率、客户反馈有变化吗？" | "准确率 99.5%" |
| 4 (Business Impact) | "为公司节省了多少钱/带来多少收入？" | "年节省 2000+ 小时" |

**If user cannot quantify after 2 rounds**: Write process-focused content, never use vague fillers ("实现智能化", "显著提升效率").

**CP4 Cultural Tone Slider**:

| Region | Level | Style | Self-Promotion |
|--------|-------|-------|----------------|
| North America | 5 (Assertive) | Led, Drove, Spearheaded | Results-first |
| UK/Ireland | 4 | Delivered, Managed | Measured confidence |
| DACH | 3 | Contributed to, Responsible for | Fact-focused |
| East Asia | 2 (Collaborative) | 协同, 推进, 支持 | Team-oriented |
| Nordics | 1 (Humble) | Contributed, Improved | Impact-only |

**CP4 Wording Boundary（硬边界 — 措辞升级只改形式，不改事实）**:

| ✅ 允许 | ❌ 禁止 |
|--------|--------|
| 换更强的动词（"参与了"→"主导了"）——**需有故事库/用户确认支撑** | 添加原简历和故事库里都没有的事实性描述 |
| 调整语气（弱→强，根据区域 slider） | 添加新的职责范围（如"覆盖从需求到上线的完整产品周期"——除非有依据） |
| 重组 bullet 结构（结果前置等） | 凭空添加量化数字 |
| 对齐 JD 关键词（原简历有对应概念时） | 为对齐 JD 编造不存在的经验 |

**🔴 如果对某条措辞升级是否越界存疑 → 输出 before/after 并标注「不确定是否有依据」，让用户确认后再写入。**

**Global Interaction Principle**: Every question must include a concrete recommendation. User confirms or overrides — never decides from scratch.

### Phase 4: Delivery & Audit (Physical Isolation)

**Two separate LLM calls — this is the critical architectural guarantee.**

#### Step 4a: Writer Node — Generate Draft

**Node**: Resume Architect (`architect_writer`)
**Formatting**: `references/formatting_rules.md` (contact info, certifications, bullet writing, skills section)
**Input**: All confirmed decisions from Phase 3
**Action**: Generate Markdown draft, save to `history/YYYY-MM-DD_{company}_{role}.md`
**Constraint**: DO NOT self-audit. Just produce the draft.

#### Step 4b: Auditor Node — Compliance Check

**Node**: Sincerity Auditor (`auditor_compliance`)
**Input**: Draft + target region rules
**Action**: Regional compliance (photo, age, PII per region)
**Output**: Compliance table with 🔴 critical violations

#### Step 4c: Auditor Node — Reverse Audit

**Node**: Sincerity Auditor (`auditor_sincerity`)
**Input**: Draft + interviewer persona + JD context + **Phase 1 `interview_intel`（面经摘要 + 面试重点提示）**
**Actions**:
1. Construct senior interviewer persona based on role type **+ Phase 1 S1 面经中提取的面试官风格/高频考点**
2. Review every bullet for: AI trace, logical gap, scope inflation, buzzword defense, cultural mismatch
3. Classify severity: 🔴 MAJOR / 🟡 MINOR / 🟢 INFO
4. For each 🔴 MAJOR: generate mock interview questions + STAR prep sheets
   - **Mock 问题优先取材自 Phase 1 S1 面经**：如面经中提到"面试官喜欢追问 AB 测试细节"，则 mock 问题必须覆盖 AB 测试场景

**If 🔴 MAJOR found**: Set flag `["ROLLBACK"]` in STATE_UPDATE → engine reverts to Phase 3. **🔴 STOP — report findings to user before rollback, let user decide which issues to fix.**

#### Step 4d: Compile & Deliver

1. Run `scripts/diff_audit.py` (source vs tailored change evidence)
2. Run `scripts/ats_checker.py` (ATS compatibility score)
3. Compile final audit log combining all sources
4. Save Markdown draft: `history/{date}_{company}_{role}.md`
5. Render HTML: 将 MD 内容按节段映射到 `templates/resume_swiss.html` 模板变量 → 写入 `history/{date}_{company}_{role}.html`
6. Archive snapshot from `sessions/` to `history/`

> 🛑 **DELIVERY GATE**：Phase 4a Writer → Phase 4b Auditor → Phase 4c Reverse Audit → Phase 4d Compile → Phase 4e Historical Audit，**五步缺一不可**。跳过 Auditor = 未完成交付。

#### HTML 模板变量映射

`templates/resume_swiss.html` 使用 `{{VARIABLE}}` 占位符，渲染时替换：

| 模板变量 | 来源 | 说明 |
|---------|------|------|
| `{{NAME}}` | resume_master.md 个人信息 → 姓名 | 顶部大标题 |
| `{{SUBTITLE_BLOCK}}` | 目标岗位 / 一句话定位 | 可选，无则留空 |
| `{{CONTACT_ITEMS}}` | 邮箱、电话、城市、LinkedIn、GitHub | 各一个 `<span>` |
| `{{SUMMARY_BLOCK}}` | 个人总结段 | 可选，无则留空（含 section-title + 段落） |
| `{{EXPERIENCE_SECTION}}` | 工作经历整节（标题 + 条目） | 每个经历 = 一个 `.exp-item` |
| `{{PROJECTS_SECTION}}` | 项目经历整节 | 可选，结构与 experience 相同 |
| `{{EDUCATION_SECTION}}` | 教育背景整节（标题 + 条目） | 每个学历 = 一个 `.edu-item` |
| `{{SKILLS_SECTION}}` | 技能整节（标题 + skills-grid） | 每个 skill = 一个 `.skill-entry` |
| `{{META_EXTRA}}` | 公司名、日期等元信息 | 非打印区生成信息 |

#### Output Naming Convention

- **项目副标题**：写角色/身份（如"独立开发""个人项目"），**不写课程编号或学校名**（如 ❌"NUS BAP" ❌"课程项目"）。目的是让面试官感知为独立成果而非课堂 toy。
- **地点**：写城市或国家，不写学校。

#### Step 4e: Historical Version Audit ⭐

**每次生成新简历前，必须与历史版本对比。不允许新版本在量化或措辞上比旧版倒退。**

**执行时机**：Phase 4d 编译完成后、交付用户前。

**操作步骤**：
1. `find history/ -name "*.html" -o -name "*.md" | sort -r | head -3` — 取最近 3 份历史简历
2. 逐段对比新简历 vs 最近版本：

| 检查维度 | 方法 | 触发条件 |
|---|---|---|
| **量化倒退** | grep 新简历的每个数字（百分比/时长/金额），确认旧版同 bullet 有该数字 | 旧版有量化数据而新版删除了 → 🔴 |
| **内容回退** | 对比同经历的 bullet 数量和覆盖维度 | 旧版 4 条 bullet 新版 3 条，且缺失的不是刻意删除的 → 🟡 |
| **措辞弱化** | 对比同 bullet 的动词（如"主导"变"参与"、"设计"变"协助"） | 动词降级且无合理解释 → 🟡 |

**处理规则**：
- 🔴 量化倒退 → **必须回退到旧版数字**，除非用户明确要求删除
- 🟡 内容回退/措辞弱化 → **列出差异给用户确认**，由用户决定保留新版还是回退
- 如果旧简历本身有错误（数字不对、经历过时），新版纠正不算倒退

**反例**：新版简历将旧版的"将处理时间从 X 缩短到 Y"简化为"显著提升效率"，丢失了具体量化数据——这就是量化倒退。本条 Protocol 的意义就是防止这类问题：新版本必须在每个维度上 ≥ 旧版本。

3. 输出审计报告：`{date}_{role}_version_audit.md`，列出所有差异及处理建议
4. 🔴 STOP — 展示差异给用户确认后再交付

## Rendering Pipeline

```
Phase 4a Writer → {date}_{company}_{role}.md （Markdown 草稿，始终产出）
                    │
                    ├──→ 直接交付 Markdown
                    │    可读、可 diff、可进 Git 版本审计
                    │    这是简历的「源代码」——所有渲染格式由此衍生
                    │
                    └──→ 模板替换 → {date}_{company}_{role}.html （主交付物）
                         模板：templates/resume_swiss.html
                         渲染方式：renderer.py 解析 MD，填充 {{SECTION}} 级占位符
                         瑞士国际主义风，单文件自包含，零外部依赖
                         浏览器直接打开，Ctrl+P → 保存为 PDF
```

**输出优先级**：

| 格式 | 优先级 | 说明 |
|------|--------|------|
| **Markdown** | 主交付物 | Phase 4a Writer 直接产出，可读、可 diff、可进 Git 版本审计。这是简历的「源代码」 |
| **HTML** | 主交付物 | `templates/resume_swiss.html` 模板渲染，瑞士国际主义风，浏览器直接打开 |
| PDF | 用户侧生成 | 浏览器打开 HTML → Ctrl+P → 保存为 PDF。**不在 pipeline 内自动执行** |
| DOCX | 已移除 | v3.3 起不再作为 pipeline 步骤，移除 WeasyPrint / pandoc / pypandoc 依赖 |

**HTML 模板设计原则**（继承自 guizang-ppt Swiss 风格）：
- 信息优先，零装饰（无阴影、无圆角、无渐变）
- 字体层级：越大越细（name 300 → body 400 → meta 600）
- 单文件自包含，CSS 变量驱动，零外部依赖
- A4 打印优化：`@page { size: A4 }` + `print-color-adjust: exact`
- 字体：Inter (Latin) + Noto Sans SC / Microsoft YaHei (CJK)

**渲染降级**：
- 模板文件缺失 → 直接 Markdown 交付，HTML 生成跳过，不报错不中断
- **零依赖降级**：不需要任何 Python 包。renderer.py 仅使用 Python 标准库（json、re、pathlib）

## Output Structure

```
{resume_directory}/
├── resume_master.md                 # Master resume — NEVER modified
├── project-story-library.md         # 故事库（Mode B 唯一事实来源）
├── schemas/snapshot_schema_v1.json  # Protocol definition
├── templates/
│   ├── resume_swiss.html            # HTML 模板（瑞士国际主义风，v3.3 主模板）
│   └── state_update_template.md
├── references/                      # Expert node guides
│   ├── writer_guide.md
│   ├── auditor_guide.md
│   ├── interaction_checkpoints.md
│   └── audit_log_template.md
├── sessions/{session_id}/           # Runtime snapshots
│   └── snapshot.json
└── history/
    ├── {date}_{company}_{role}.md              # Tailored Markdown（主交付物）
    ├── {date}_{company}_{role}.html            # Tailored HTML（主交付物，瑞士风）
    ├── {date}_{company}_{role}_audit.md        # Audit log
    ├── {date}_{company}_{role}_snapshot.json   # Archived state
    ├── {date}_{company}_{role}_interview_intel.md  # Phase 1 面经情报
    └── ...
```

## Anti-Patterns（NEVER）

| # | 反模式 | 为什么不能做 | 替代做法 |
|---|---|---|---|
| 1 | **捏造或推断经历中的数据** | 简历被面试官追问时无法回答，直接丢 offer | Mode B：故事库没有的数据 → 问用户确认，绝不编造 |
| 2 | **在 Mode B 做"逻辑推断"扩展** | "覆盖从需求定义到上线的完整周期"这类推理即使看起来合理也不允许 | 只做提炼，不做扩展 |
| 3 | **用模糊填充词替代量化数据** | "实现智能化""显著提升效率" = AI 生成痕迹，面试官一眼识别 | CP3 追问 2 轮后用户仍无法提供 → 写过程描述 |
| 4 | **在同一个 LLM 调用里写完又审** | 自写自审 = 零审查效果 | Phase 4 物理隔离：Writer 只写，Auditor 只审，两个独立调用 |
| 5 | **修改原始简历文件** | 源头文件被污染后所有衍生简历都受影响 | 始终从源文件读取到新文件，不在源文件上编辑 |
| 6 | **跳过用户确认直接出最终稿** | 用户没有机会在关键决策点纠正方向 | 每次 CP 必须 WAIT for user confirmation |
| 7 | **Mode B 把故事库内容改写/润色** | 故事库是面试一致性的唯一保证，改写后问答脱节 | Mode B 只做"选取"和"重组"，不改写原 bullet 含义 |
| 8 | **用"建议/可以考虑/根据情况"等软化措辞替代明确的 STOP 标记** | LLM 不识别弱措辞，会继续执行 | 必须用 `🔴 STOP` 或 `🛑 CHECKPOINT` 显性标记 |
| 9 | **生成新版本不与历史版本对比** | 量化数据可能在迭代中丢失（如具体数字退化为模糊描述） | 每次交付前执行 [[#Step 4e Historical Version Audit]]，量化倒退 → 回退到旧版数字 |
| 10 | **用课程/学校标签弱化项目** | "NUS 商业分析项目（BAP）"让人以为是课程 toy，面试官直接打折 | 副标题只写角色身份（"独立开发"/"个人项目"），不写课程编号；地点写城市/国家，不写学校 |
| 11 | **跳过 Phase 4 反向审计直接交付** | 没有独立 Auditor 的简历 = 没有诚意检查，面试时会被追问打穿 | Phase 4 必须 Writer → Auditor 两个独立调用；Auditor 未跑完不能交付 |

## Agent Execution Anti-Patterns（NEVER — Agent 自主执行时）

> 以下反模式来自 Agent 在无监督状态下运行 resume-tailor 时最容易犯的错误，与上方「用户约定层 Anti-Patterns」不同——这些是 **LLM/Agent 主动犯的执行错误**，不是用户约定。

| # | 反模式 | 触发场景 | 为什么不能做 | 正确做法 |
|---|---|---|---|---|
| A1 | **跳过 CP 继续推进** | Agent 认为「用户意图已明确，不需要再问」 | CP 是状态写入节点，跳过意味着 snapshot 里没有 `user_decisions` 记录，后续 Auditor 无法追溯 | 遇到 `🔴 STOP CP*` 标记 → 无论上下文多明确，必须输出 CP 内容并等待用户回复再推进 |
| A2 | **Writer 和 Auditor 在同一个 LLM 调用里完成** | Agent 把 Phase 4a+4b+4c 合并为一段输出 | 自写自审 = 零审查效果，Auditor 不会质疑同一上下文里刚生成的内容 | Phase 4a 输出草稿后，必须切换新的上下文窗口（或新的 prompt 调用）执行 Auditor 节点 |
| A3 | **MODE 判断后未确认就直接推进** | 用户输入「帮我做个产品简历」→ Agent 自判为 Mode B 直接跑 Phase G1 | 如果用户其实有 JD 待贴，浪费了整个 Phase G1 | 初次 MODE 判断后，先输出「我判断你需要 Mode B（无 JD 通用），对吗？」再推进 |
| A4 | **量化追问超过 2 轮仍不落地** | CP3 追问 4 轮后用户还是没数字，Agent 继续追问 | 无限追问体验极差且无意义 | 追问满 2 轮无结果 → 立即切换为过程描述，明确告知用户「本条以过程描述呈现，如后续有数据可补充」 |
| A5 | **STATE_UPDATE 解析失败后静默继续** | JSON parse error → Agent 忽略错误继续下一步 | snapshot 状态不一致，后续所有节点读到的都是脏数据 | JSON 解析失败 → 立即停止，输出原始文本，提示用户「状态同步失败，需要人工确认后继续」 |
| A6 | **web_search 执行了但结果未落地** | 搜索结果未出现在 `scout_report`、`risk_warnings`、`capability_clusters`、或 `interview_intel` 中 | 浪费 token + 用户看到"调研了但没用" | 每轮搜索结果必须至少影响一项下游产出（见 Phase 1 的"产出落地点"列），标注 `来源：[搜索关键词]` |
| A7 | **历史版本审计（Step 4e）在 4d 之前跑** | Agent 重排了执行顺序「先审计再出稿」 | Step 4e 的输入是 4d 编译完成的草稿，提前跑没有内容可比对 | 严格顺序：4a → 4b → 4c → 4d → 4e → 交付。不允许重排 |

## Error Handling

| Error | Primary Action | If Primary Fails |
|-------|---------------|-----------------|
| No resume file | `Glob **/resume_master.md`；找到则直接用，未找到则输出「请提供简历文件路径（.docx/.pdf/.md）」 | 检查 `.workbuddy/memory/MEMORY.md` 中 `resume_path` 字段；仍无 → 停止执行，不猜测 |
| No JD provided | 输出「未检测到 JD，切换到 Mode B（通用方向简历），请确认目标岗位方向」，等用户回复后再推进 | 若用户确认要 JD 模式 → 输出「请直接粘贴 JD 文本」，不尝试自行推断 |
| JD URL fetch fails | 输出「链接无法访问，请直接粘贴 JD 文本」 | 用 `WebFetch` 附加 `User-Agent: Mozilla/5.0 Mobile` 重试一次；仍失败 → 停止，不继续 |
| Story library missing data for a claim | 输出「故事库中缺少[XXX]的数据，请确认或提供」——列出缺失字段，等待回复 | 用户无法确认 → 完整删除该 bullet，不写任何推断性描述 |
| snapshot.json 损坏或缺失 | 备份损坏文件为 `snapshot.json.bak.YYYYMMDD-HHMM`，重建空 snapshot（只保留 `_meta` 层），从 Phase 1 重新开始 | 无法写文件 → 停止，输出「状态文件异常，请手动删除 sessions/ 目录后重试」 |
| STATE_UPDATE JSON parse fail | 在同一上下文注入自纠正 prompt「请只输出合法 JSON，格式：{...}」，重试一次 | 第二次失败 → 从原始输出手动提取关键字段（`status`、`decisions`），跳过 JSON 解析，在 snapshot 中标注 `parse_error: true` |
| 🔴 Major issues in audit | 在 STATE_UPDATE 中写入 `["ROLLBACK"]`，回退到 Phase 3；**在回退前必须向用户输出具体问题列表和对应的 mock 面试问题** | 重新审计仍发现 major → 输出「以下问题建议手动修改或接受风险，请选择」，不再自动回滚 |
| LLM timeout | 用完整 snapshot 重试一次 | 第二次 timeout → 裁剪 snapshot（只保留 `jd_facts` + `user_decisions`，删除 `expert_outputs`），再试一次；三次均失败 → 停止并告知用户 |
| Script failure (jd_parser 等) | Scout 节点用 LLM 直接提取 JD 特征（不依赖脚本），并在输出中标注「脚本降级，LLM 提取」 | LLM 提取也失败 → 输出「请用 3 条 bullet 手动描述 JD 的核心要求」，等用户输入后继续 |

## Dependencies

> v3.3 起渲染管线为零外部依赖（仅 Python 标准库）。简历读取仍需要 python-docx + pdfplumber（解析 .docx/.pdf 源文件）。详见 README.md 的 Dependencies 节。
