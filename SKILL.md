---
name: resume-tailor
description: "针对岗位 JD 定制简历，或生成通用方向简历。分析 JD 关键词、匹配源简历、交互式调整建议、反向诚意审计。触发词：调简历、tailor resume、优化简历、生成简历、通用简历、简历定制、resume for this JD"
version: "3.0"
---

# Resume Tailor v3

**Pseudo Multi-Agent + Blackboard Architecture**

Analyze a job description and tailor the source resume to match, using isolated expert nodes for writing and auditing.

## Trigger Phrases

**Mode A (JD-Targeted):**
- "帮我针对这个 JD 调简历" / "tailor my resume for this JD"
- "优化简历给这个岗位" / "optimize resume for this role"
- Any JD text or URL provided with resume adjustment intent

**Mode B (General-Purpose):**
- "帮我针对产品岗位生成一个通用性的简历"
- "做个通用版简历" / "生成XX方向的简历"
- "make a general resume" / "create a role-oriented resume"
- "简历定制" / "简历优化"

## Resume Input

On first run, **try auto-detection first**:
1. `Glob **/resume_master.md` in workspace — if found, use it directly
2. If workspace has `源文件/resume_master.md` or `.workbuddy/memory/MEMORY.md` with a resume path, follow that
3. Only if auto-detect fails → ask user to provide their resume file path (.docx preferred, .pdf or .txt acceptable)

**Story library path** (for Mode B capability matching): `{user vault}/01-个人经历/项目故事库.md`
- Use `Glob **/项目故事库.md` to auto-locate the vault
- Fallback: ask user for Obsidian vault path

Store the resolved paths in workspace memory. **Never modify the original.**

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

故事库是 Obsidian vault 中的 `01-个人经历/项目故事库.md`，结构如下：

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

❌ **禁止**：一次性读取整个故事库（1137行）→ 浪费 token 且 Agent 注意力衰减。

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
├── Render final deliverables
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
**Output**: Populated `jd_facts`, `scout_report`, capability clusters
**Tools**: `scripts/jd_parser.py` (with graceful fallback to LLM), `web_search`

1. Accept JD input (URL → fetch, or text directly)
2. Ask user: company name? target region?
3. Run market research (2 targeted web searches)
4. Execute unified context extraction (script + LLM in one pass)
5. Detect role level, region, document type
6. Output consolidated context table + risk warnings

### Phase 2: Strict Matching

**Node**: Context Scout (continuation) or Architect (if Fast-Track)
**Reference**: Integrated into Phase 1 or `references/writer_guide.md`

1. Read source resume (structured reader for .docx, fallback for .pdf)
2. Semantic matching: Direct + Implicit (with confidence) + Gaps
3. Cross-credential alignment
4. Match score calculation
5. Hard requirement alerts (dealbreakers)

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

**Global Interaction Principle**: Every question must include a concrete recommendation. User confirms or overrides — never decides from scratch.

### Phase 4: Delivery & Audit (Physical Isolation)

**Two separate LLM calls — this is the critical architectural guarantee.**

#### Step 4a: Writer Node — Generate Draft

**Node**: Resume Architect (`architect_writer`)
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
**Input**: Draft + interviewer persona + JD context
**Actions**:
1. Construct senior interviewer persona based on role type
2. Review every bullet for: AI trace, logical gap, scope inflation, buzzword defense, cultural mismatch
3. Classify severity: 🔴 MAJOR / 🟡 MINOR / 🟢 INFO
4. For each 🔴 MAJOR: generate mock interview questions + STAR prep sheets

**If 🔴 MAJOR found**: Set flag `["ROLLBACK"]` in STATE_UPDATE → engine reverts to Phase 3. **🔴 STOP — report findings to user before rollback, let user decide which issues to fix.**

#### Step 4d: Compile & Deliver

1. Run `scripts/diff_audit.py` (source vs tailored change evidence)
2. Run `scripts/ats_checker.py` (ATS compatibility score)
3. Compile final audit log combining all sources
4. Render output (see Rendering section below)
5. Archive snapshot from `sessions/` to `history/`

> 🛑 **DELIVERY GATE**：Phase 4a Writer → Phase 4b Auditor → Phase 4c Reverse Audit → Phase 4d Compile → Phase 4e Historical Audit，**五步缺一不可**。跳过 Auditor = 未完成交付。

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

**反例**：2026-05-30 本 skill 在生成数据分析师简历时，第一次写 PwC WIP 用了"显著缩短"，但故事库和旧版简历都有 "48h→12h" 的具体数据——这就是量化倒退。本条 Protocol 存在的意义就是防止这类问题。

3. 输出审计报告：`{date}_{role}_version_audit.md`，列出所有差异及处理建议
4. 🔴 STOP — 展示差异给用户确认后再交付

## Rendering Pipeline

```
Layer 3 Draft (Markdown)
    ↓ Phase 1: Regex Preprocessing
    "**Summary**: detail" → "<span class='bullet-summary'>Summary:</span> detail"
    ↓ Phase 2: MD → HTML Fragment
    markdown-it-py (preferred) / python-markdown (fallback)
    ↓ Phase 3: Jinja2 Layout
    CSS-inlined complete HTML document via templates/resume_layout.html.j2
    ↓ Phase 4a: WeasyPrint → PDF (with page overflow detection)
    ↓ Phase 4b: pypandoc → DOCX (clean conversion)
```

**Graceful degradation**:
- WeasyPrint unavailable → HTML-only output with "Print → Save as PDF" prompt
- pandoc unavailable → raw Markdown export
- markdown-it-py unavailable → python-markdown fallback

CSS template: `templates/resume_template.css` (Tech Style, single-column, A4 portrait)

## Output Structure

```
{resume_directory}/
├── resume_source.docx              # Original — NEVER modified
├── schemas/snapshot_schema_v1.json # Protocol definition
├── templates/state_update_template.md
├── references/                     # Expert node guides
│   ├── writer_guide.md
│   ├── auditor_guide.md
│   ├── interaction_checkpoints.md
│   └── audit_log_template.md
├── sessions/{session_id}/          # Runtime snapshots
│   └── snapshot.json
└── history/
    ├── {date}_{company}_{role}.md           # Tailored Markdown
    ├── {date}_{company}_{role}.docx         # Final deliverable
    ├── {date}_{company}_{role}_audit.md     # Audit log
    ├── {date}_{company}_{role}_snapshot.json# Archived state
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
| 9 | **生成新版本不与历史版本对比** | 量化数据可能在迭代中丢失（如"48h→12h"变成"显著缩短"） | 每次交付前执行 [[#Step 4e Historical Version Audit]]，量化倒退 → 回退到旧版数字 |
| 10 | **用课程/学校标签弱化项目** | "NUS 商业分析项目（BAP）"让人以为是课程 toy，面试官直接打折 | 副标题只写角色身份（"独立开发"/"个人项目"），不写课程编号；地点写城市/国家，不写学校 |
| 11 | **跳过 Phase 4 反向审计直接交付** | 没有独立 Auditor 的简历 = 没有诚意检查，面试时会被追问打穿 | Phase 4 必须 Writer → Auditor 两个独立调用；Auditor 未跑完不能交付 |

## Error Handling

| Error | Primary Action | If Primary Fails |
|-------|---------------|-----------------|
| No resume file | Auto-detect via Glob; ask user if not found | Check `.workbuddy/memory/MEMORY.md` for stored path |
| No JD provided | Switch to Mode B (General-Purpose) | If user confirms they want JD mode → ask them to paste JD text |
| JD URL fetch fails | Ask user to paste text | Try WebFetch with mobile user-agent as fallback |
| Story library missing data for a claim | Ask user to confirm — NEVER fabricate | If user also can't confirm → drop the claim entirely, don't include |
| STATE_UPDATE JSON parse fail | Inject self-correction prompt, retry once | Second failure → manually extract key fields from raw output, skip JSON parsing |
| 🔴 Major issues in audit | ROLLBACK flag → revert to Phase 3 | If re-audit still finds majors → escalate to user: "fix manually or accept risk?" |
| LLM timeout | Retry with same snapshot context | Second timeout → restart with reduced snapshot (trim non-essential context) |
| Script failure (jd_parser etc.) | Degrade gracefully, Scout node handles via LLM | If both script and LLM fail → ask user to manually summarize JD in 3 bullet points |

## Dependencies

### Script Implementation Status

| Script | Status | Description |
|--------|--------|-------------|
| `scripts/engine.py` | ✅ Implemented | Pipeline orchestrator, pseudo multi-agent loop |
| `scripts/renderer.py` | ✅ Implemented | MD → HTML → PDF/DOCX rendering pipeline |
| `scripts/jd_parser.py` | ✅ Implemented | JD feature extraction (regex + heuristic) |
| `scripts/diff_audit.py` | ✅ Implemented | Source vs tailored change comparison |
| `scripts/ats_checker.py` | ✅ Implemented | ATS compatibility validation |
| `scripts/main.py` | ✅ Implemented | CLI entry point |
| `scripts/utils.py` | ✅ Implemented | Shared utilities |

> **Note**: All scripts are functional. The v3.0 architecture (pseudo multi-agent + blackboard) is implemented in `engine.py`. The rendering pipeline with Phase 2.5 tokenization is in `renderer.py`.

### Python Packages

```
# v3.0 Rendering Pipeline (core)
jinja2>=3.1.0              # Template engine
markdown-it-py>=3.0.0      # Markdown → HTML (preferred)
weasyprint>=60.0           # PDF generation (optional, graceful fallback)
pypandoc>=1.17             # DOCX generation (optional, requires pandoc CLI)
pyyaml>=6.0                # Snapshot schema YAML support

# v2.x Resume I/O (still used)
python-docx>=0.8.11        # .docx read/write
pdfplumber>=0.10.0         # PDF reading (primary)

# Optional fallbacks
python-markdown>=3.5.0     # Fallback MD parser
PyPDF2>=3.0.0              # Fallback PDF reader
```
