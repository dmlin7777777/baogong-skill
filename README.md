<div align="center">

# Resume Tailor

**AI-Powered Resume Tailoring — Not a Polisher, a Coach**

*This project follows a "Coach, not Polisher" philosophy.*

[English](README.md) · [简体中文](README.zh-CN.md)

**v3.2 — Darwin 5-Round Optimized (92/100) + Onboarding System + Agent Anti-Patterns**

</div>

---

## What's New in v3.2

**Darwin Skill 5-round optimization: 76 → 92 (+16)** across the 9-dimension SkillLens rubric.

### New: Onboarding System
First-time users no longer hit a wall. Two guided initialization paths:

- **Init-A (Master Resume)**: Auto-detect existing resume files → structured `resume_master.md` via 5-round guided questionnaire if starting from scratch
- **Init-B (Story Library)**: Per-experience STAR + quantification + interview prep recording, triggered when Mode B needs it or CP3 quantification fails

### New: Agent Execution Anti-Patterns
7 dedicated A1–A7 rules preventing LLM-specific mistakes: Writer/Auditor isolation violation, MODE misjudgment without confirmation, STATE_UPDATE silent failure, Phase order reordering, and empty web_search calls.

### New: CP4 Wording Boundary
Hard boundary table — what's allowed (verb replacement, tone adjustment, bullet restructuring) vs forbidden (adding facts not in source, fabricating metrics, inventing experience for JD alignment).

### Improved: Mode Detection
≥50-char threshold distinguishes real JDs from vague role names, with mandatory confirmation for ambiguous input.

### Improved: Error Handling
All 9 error cases now have concrete action instructions instead of soft language. New `snapshot.json` corruption recovery with backup-and-rebuild flow.

---

## Why You Need It?

Most AI resume tools **rewrite** your bullets to sound fancy. This one **coaches** you to make them real.

| Traditional AI Rewrite | Resume Tailor |
|---|---|
| ❌ "Significantly improved data analysis efficiency, received team recognition" | ✅ "Built automated reconciliation tool, reducing monthly close cycle from **5 days to 6 hours** across **12 business lines**" |
| Fills vague adjectives when data is missing | Asks targeted questions — or keeps original wording if you can't quantify |
| Optimistic about your role ("Led" everything) | Challenges every claim: *"Were you the decision maker?"* |
| One-size-fits-all output | Adapts tone, format, and privacy rules per target region |

**The difference**: A polished lie gets rejected at the interview. A coached truth gets you hired.

---

## What You Get

You don't just get a tailored resume. You get a **job search toolkit**.

### 📄 Tailored Resume (PDF / HTML / DOCX)
Optimized for the specific JD and target region:
- **PDF**: WeasyPrint-rendered with CSS template (Times New Roman + Microsoft YaHei), single-page layout
- **HTML**: Browser-ready with print-optimized CSS (use Print → Save as PDF if WeasyPrint unavailable)
- **DOCX**: Clean Markdown-to-Word via pypandoc (no style baggage)

### 📊 Audit Log
Every modification is tracked:
- Match score with confidence levels for each JD requirement
- Hard gaps flagged (missing certifications, experience thresholds)
- Compliance warnings (photo/age removal by region)

### 🎙️ Interview Prep Pack
For every significant change on your resume, the system generates:
- **Mock Questions** — what interviewers will likely challenge you on
- **STAR Notes** — structured talking points so you can defend each bullet confidently

---

## Core Principles

These are non-negotiable hard rules baked into every run:

### 🚫 Anti-Filler Rule
Every bullet must follow: **Action + Object + Measurable Outcome**
- No numbers? The system asks progressive probing questions.
- Still no numbers after 2 rounds? Keep original wording — never invent metrics.
- **Rule: A vague outcome is WORSE than no outcome.**

### 🪞 Reverse Audit (Physically Isolated)
Before delivery, an independent Auditor persona reviews every bullet. Writer and Auditor are separate LLM calls — no "self-audit" shortcuts.

### ⏳ Fact Conservation
Work experiences stay in **strict reverse chronological order**. No reordering by relevance — only keep or hide.

### 🌐 Cultural Tone Slider
Verb intensity auto-adjusts: assertive (North America) → collaborative (East Asia) → modest (Nordics). Same facts, different presentation.

### ⚖️ Cross-Credential Alignment
IELTS 7.5 ≈ CET-6 550+. The system maps credentials across regions and keeps the strongest one visible.

---

## Architecture: v3.0 Pseudo-Multi-Agent

Resume Tailor v3.0 uses a **pseudo-multi-agent blackboard architecture**:

```
┌─────────────────────────────────────────────────────┐
│                  engine.py (Orchestrator)            │
│                                                     │
│  ┌──────────┐    ┌──────────────┐   ┌────────────┐ │
│  │  Scout    │───▶│  Architect    │───▶│  Auditor   │ │
│  │ (Research)│    │  (Writer x2)  │    │(Reviewer)  │ │
│  └──────────┘    └──────────────┘   └────────────┘ │
│       │                 │                  │        │
│       ▼                 ▼                  ▼        │
│  context_snapshot.json (Blackboard / Single Source) │
│  ── Facts Layer (JD + Resume + Research)            │
│  ── Decisions Layer (User choices + metadata)       │
│  ── Outputs Layer (Draft + Audit log)               │
│                                                     │
│  ┌──────────────────────────────────────────┐      │
│  │         renderer.py (Rendering Pipeline)  │      │
│  │  MD → preprocess → Jinja2 → PDF/HTML/DOCX│      │
│  └──────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────┘
```

### Expert Nodes

| Node | Role | Key Responsibility |
|------|------|--------------------|
| **Scout** | Research Analyst | JD parsing, market research, capability cluster extraction |
| **Architect (Writer)** | Resume Architect | Experience selection, gap filling, quantification, draft finalization |
| **Architect (Quantify)** | Data Specialist | Metric extraction, progressive quantification probes |
| **Auditor** | Independent Reviewer | Compliance check, interviewer-persona challenge |

### State Protocol

All state lives in `context_snapshot.json` — a layered JSON document:
- **Layer 0 (`_meta`)**: Session metadata, turn history, nuance buffer
- **Layer 1 (`facts`)**: Raw JD + resume + market research
- **Layer 2 (`user_decisions`)**: All user confirmations, overrides, metadata
- **Layer 3 (`outputs`)**: Final draft, audit log, interview prep

---

## Rendering Pipeline

v3.0 introduces a **CSS-first rendering pipeline** that replaces direct python-docx manipulation:

```
Layer 3 Draft (Markdown)
    ↓ Phase 1: Regex Preprocessing
    "**Summary**: detail" → "<span class='bullet-summary'>Summary:</span> detail"
    ↓ Phase 2: MD → HTML Fragment
    markdown-it-py (preferred) / markdown (fallback)
    ↓ Phase 3: Jinja2 Layout
    CSS-inlined complete HTML document
    ↓ Phase 4a: WeasyPrint → PDF (with page overflow detection)
    ↓ Phase 4b: pypandoc → DOCX (clean conversion)
```

**Key Design Decisions:**
- **Jinja2 as glue** — No string concatenation in code. Templates drive layout.
- **WeasyPrint over pdfkit** — Proper Flexbox/Grid + CSS print support.
- **pypandoc for DOCX** — Avoids HTML→Word formatting chaos.
- **Page overflow detection** — If `len(doc.pages) > 1`, triggers Architect's compression instructions.

### CSS Template Features
- **Single-column flow layout**, no icons, centered name header
- **Dual font stack**: Times New Roman (Latin/Digits) + Microsoft YaHei (CJK)
- **Experience format**: Company · **Title** \| Date + *Department* \| Location (flexible 2-row)
- **Bullet style**: `<span class="bullet-summary">Bold summary:</span>` detail text
- **Compact spacing** with dynamic content adjustment (target: ≤1 page)

---

## How It Works

```
Phase 1 — Context & Research     Scout parses JD, extracts requirements, researches market
Phase 2 — Semantic Matching      Architect matches experiences against JD, proposes selections
Phase 3 — Interactive Adjustment User confirms, fills gaps, quantifies metrics
Phase 4 — Audit & Delivery       Independent auditor reviews, renderer produces output
```

| Phase | Node | What Happens | Your Role |
|-------|------|-------------|-----------|
| **1. Context** | **Scout** | JD requirement extraction, company research, risk assessment | Review & confirm |
| **2. Match** | **Architect** | Direct + implicit matching with confidence levels | Review match table |
| **3. Adjust** | **Architect** | Experience selection, gap filling, quantification, wording upgrade | Confirm or override each suggestion |
| **4. Audit** | **Auditor** | Physically isolated compliance check + reviewer persona challenge | Final review |

Every suggestion comes with a **concrete recommendation** — you confirm or override, never decide from scratch.

---

## Quick Start

```bash
# Provide a JD and your resume
"Tailor my resume for this JD"
```

That's it. The skill handles research, matching, adjustment, audit, and rendering in sequence.

---

## Developer Reference

<details>
<summary>📁 File Structure</summary>

```
resume-tailor/
├── SKILL.md                              # Skill definition & workflow routing table
├── README.md                             # This file
├── README.zh-CN.md                       # Chinese documentation
├── requirements.txt                      # Python dependencies (v3.0 + v2.x)
├── schemas/
│   └── snapshot_schema_v1.json           # Snapshot schema (v1.1 with nuance_buffer)
├── templates/
│   ├── resume_template.css               # CSS template (Tech Style, single-column)
│   ├── resume_layout.html.j2             # Jinja2 layout skeleton
│   ├── resume_preview_sample.html        # Preview demo with anonymized data
│   └── state_update_template.md          # STATE_UPDATE JSON template & examples
├── scripts/
│   ├── engine.py                         # Pipeline orchestrator (pseudo-multi-agent loop)
│   ├── renderer.py                       # Rendering pipeline (MD → HTML → PDF/DOCX)
│   ├── jd_parser.py                      # JD + resume structured extraction
│   ├── diff_audit.py                     # Source vs tailored change analysis
│   ├── ats_checker.py                    # ATS compatibility scoring (5-region profiles)
│   ├── main.py                           # v2.x CLI interface (legacy)
│   └── utils.py                          # Shared utilities (JSON validation, PII, etc.)
├── references/
│   ├── writer_guide.md                   # Writer node instruction manual (Phase 1 + CP1-CP5)
│   ├── auditor_guide.md                  # Auditor node instruction manual
│   ├── interaction_checkpoints.md        # Checkpoint details for Phase 3
│   └── audit_log_template.md             # Audit log output template
├── sessions/                             # Active session snapshots (.gitignore'd)
├── history/                              # Archived sessions post-completion
└── docs/
    └── plans/
        └── 2026-04-15-v3-architecture-design.md  # Full architecture design doc
```

</details>

<details>
<summary>⚙️ Dependencies</summary>

```bash
# Core dependencies
jinja2>=3.1.0              # Template engine (rendering pipeline)
markdown-it-py>=3.0.0      # Markdown → HTML (preferred parser)
pypandoc>=1.17             # DOCX generation via pandoc
weasyprint>=60.0           # PDF generation (requires GTK/Pango runtime)

# Optional / fallback
python-markdown>=3.5.0     # Fallback MD parser if markdown-it-py unavailable
pyyaml>=6.0                # YAML support in snapshot schema
```

**Note:** WeasyPrint requires platform-specific runtimes:
- **Windows**: Install GTK+ and Pango via MSYS2 or download binaries
- **macOS/Linux**: Usually available via system package manager
- **Graceful degradation**: If WeasyPrint unavailable, outputs browser-ready HTML with "Print → Save as PDF" prompt.

</details>

<details>
<summary>🔧 Script Usage</summary>

```bash
# Check rendering environment (fonts, WeasyPrint, pandoc)
python scripts/renderer.py check-env

# Render a draft snapshot (snapshot.json → PDF/HTML/DOCX)
python scripts/renderer.py render --snapshot sessions/abc123/snapshot.json --output-dir output/

# Note: engine.py is a library module (not directly runnable).
# It is called via run_orchestration_loop(llm_call_fn, snapshot) from the AI agent.
# For CLI usage, see scripts/main.py (v2.x legacy interface).
```

</details>

<details>
<summary>🎨 Customizing CSS</summary>

Edit `templates/resume_template.css`. Key variables in `:root`:

```css
--primary-color: #1f2937;      /* Text color */
--font-size-base: 9.5pt;       /* Body text size */
--section-gap: 7pt;            /* Space between sections */
--item-gap: 5pt;               /* Space between experience items */
```

The CSS is designed for **A4 portrait, single page**. Adjust spacing variables to fit more or less content.

</details>

---

## Version History

### v3.2 (Current) — Darwin 5-Round Optimization + Onboarding System
- **Darwin SkillLens 9-dim**: 76 → **92** (+16) via 5-round optimization cycle
- **Onboarding Check**: Global pre-flight gate — `resume_master.md` missing → Init-A before anything else
- **Init-A (Master Resume)**: 3 intake paths (paste/file/5-round questionnaire) → structured `resume_master.md`
- **Init-B (Story Library)**: Guided per-experience STAR recording with quantification + interview prep
- **Agent Execution Anti-Patterns (A1–A7)**: LLM-specific error prevention (isolation violations, silent failures, order reordering)
- **CP4 Wording Boundary**: Explicit table of allowed (verb/tone/structure) vs forbidden (fabrication, scope inflation) edits
- **Mode Detection Protocol**: ≥50-char threshold + mandatory confirmation for ambiguous JD input
- **Story library integration in Mode A**: CP3 quantification priority chain (story lib > user reply > process description)
- **Required permissions declaration** in frontmatter (Read/Write/Glob/WebFetch/WebSearch/Bash)
- **Error handling concretized**: All 9 error cases → specific action instructions; snapshot corruption backup-and-rebuild flow

### v3.1 — Onboarding + Story Library Mode A Integration
- Init-A (Master Resume creation) + Init-B (Story Library creation)
- Mode A story library access for CP3 quantification backup
- Version bump after real execution simulation exposed missing initialization path
- **Darwin Skill 9-dim evaluation**: 74.3 → **90.5** (+16.2)
- **Historical version audit** (Step 4e): prevents quantification regression by comparing against last 3 versions
- **Story library protocol**: 3-layer token-efficient extraction + cross-validation in audit
- **9 STOP/CHECKPOINT markers** + 2 delivery gates to prevent autonomous drift
- **Pseudo-multi-agent architecture** with isolated Scout / Architect / Auditor nodes
- **Blackboard state protocol** via `context_snapshot.json` (4-layer schema v1.1)
- **HTML rendering pipeline** with Jinja2 templates + CSS styling
- **WeasyPrint PDF** output with page overflow detection → automatic compression trigger
- **pypandoc DOCX** clean conversion (no HTML→Word formatting issues)
- **Nuance buffer** + **conversation history** for cross-node context continuity

### v2.4 — Structural Refactor
- 4-stage pipeline, 3-tier routing, unified extraction
- Anti-Filler Rule, Propose-don't-ask principle, Reverse Audit
- Shadow Resume moved to on-demand

[Full changelog → CHANGELOG.md](CHANGELOG.md)

---

## License

MIT
