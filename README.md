<div align="center">

# Resume Tailor

**AI-Powered Resume Tailoring — Not a Polisher, a Coach**

*This project follows a "Coach, not Polisher" philosophy.*

[English](README.md) · [简体中文](README.zh-CN.md)

**v3.3 — Rendering Pipeline Refactor (HTML+MD Dual Delivery + Swiss Design)**

</div>

---

## What's New in v3.3

### Structured Web Search
**Phase 1 upgraded from vague "market research" to a 3-tier structured web search strategy:**

**S1 — Interview Experience Mining**
Searches for `"{Company} {Role} interview experience"` / `"{Role} interview questions"` patterns to extract:
- What interviewers actually ask (not what the JD says)
- High-frequency checkpoints and hidden requirements
- → Drives CP3 quantification direction and makes Phase 4c mock questions authentic

**S2 — Company Culture & Real Work**
Searches for `"Working at {Company} as {Role}"` / `"{Company} tech stack"` to extract:
- Actual tech stack (often different from JD requirements)
- Team style and cultural keywords
- → Calibrates Phase 2 skill matching weights and CP4 cultural tone slider

**S3 — Business Signals**
Searches for `"{Company} business focus"` / `"{Company} org changes"` to extract:
- Revenue priorities, new product lines, org restructuring
- → Feeds `risk_warnings` (flag contracting departments) and `capability_clusters` targeting

Each search tier's output lands on a specific downstream node (no empty searches — enforced by updated A6 anti-pattern). Extracted insights saved as `{date}_{company}_{role}_interview_intel.md` in `history/`.

### Rendering Pipeline Refactor — HTML/MD Dual Delivery

**Old**: MD → markdown-it → Jinja2 → WeasyPrint PDF + pandoc DOCX (4 Python package dependencies, frequently broken on Windows)

**New**:

| Format | Priority | Notes |
|--------|----------|-------|
| **Markdown** | Primary | Direct output from Phase 4a Writer. Readable, diffable, Git-friendly |
| **HTML** | Primary | `templates/resume_swiss.html` Swiss International Style, single-file, zero deps |
| PDF | User-side | Browser Ctrl+P → Save as PDF. **Not auto-generated in pipeline** |
| DOCX | Removed | WeasyPrint / pandoc / pypandoc dependencies fully removed |

**HTML template design** (inspired by guizang-ppt Swiss style):
- Information-first, zero decoration (no shadows, radius, gradients)
- Typographic hierarchy: weight inversely proportional to size (300 → 400 → 600)
- Single-file, CSS variable-driven, no external dependencies
- A4 print-optimized: `@page { size: A4 }` + browser-native printing
- Fonts: Inter (Latin) + Noto Sans SC / Microsoft YaHei (CJK)

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

### 📄 Tailored Resume (HTML / Markdown)
Optimized for the specific JD and target region:
- **HTML**: Swiss International Style (`templates/resume_swiss.html`), single-file, zero dependencies, A4 print-optimized
- **Markdown**: Readable, diffable, Git-friendly — the "source code" of your resume
- **PDF**: Not auto-generated. Use browser Ctrl+P → Save as PDF from the HTML file

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

## Architecture: LLM-as-Orchestrator + Blackboard State

Resume Tailor v3.3 runs as an **LLM-as-orchestrator** skill. The LLM reads `SKILL.md`, advances through phases, and calls `scripts/` tools as needed. No Python process drives the LLM — the LLM drives the Python tools.

```
┌─────────────────────────────────────────────────────┐
│  LLM (reads SKILL.md, advances through Phases)      │
│                                                     │
│  ┌──────────┐    ┌──────────────┐   ┌────────────┐ │
│  │  Scout    │───▶│  Architect    │───▶│  Auditor   │ │
│  │ (Research)│    │  (Writer x2)  │    │(Reviewer)  │ │
│  └──────────┘    └──────────────┘   └────────────┘ │
│       │                 │                  │        │
│       ▼                 ▼                  ▼        │
│  engine.py: Snapshot (Blackboard / Single Source)   │
│  ── jd_facts layer (JD + Resume + Research)         │
│  ── user_decisions layer (User choices + metadata)  │
│  ── expert_outputs layer (Draft + Audit log)        │
│                                                     │
│  ┌──────────────────────────────────────────┐      │
│  │    renderer.py: MD → parse → HTML          │      │
│  │    (pure stdlib, zero dependencies)        │      │
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

All state lives in `snapshot.json` — a layered JSON document:
- **Layer 0 (`_meta`)**: Session metadata, turn history, nuance buffer
- **Layer 1 (`jd_facts`)**: Raw JD + resume + research data
- **Layer 2 (`user_decisions`)**: All user confirmations, overrides, preferences
- **Layer 3 (`expert_outputs`)**: Node outputs (scout report, draft, audit log)

---

## Rendering Pipeline (v3.3)

v3.3 uses a **zero-dependency template substitution pipeline**:

```
Phase 4a Writer Output (Markdown)
    ↓
renderer.py: Parse Markdown into structured sections
  - h1 → name + contact items
  - h2 → section boundaries (summary/experience/education/skills)
  - h3 → entry titles
  - **Prefix**: detail → bullet label + body
    ↓
Template substitution → templates/resume_swiss.html
  {{NAME}} {{SUBTITLE_BLOCK}} {{CONTACT_ITEMS}}
  {{SUMMARY_BLOCK}} {{EXPERIENCE_SECTION}}
  {{PROJECTS_SECTION}} {{EDUCATION_SECTION}}
  {{SKILLS_SECTION}}
    ↓
Filled HTML (Swiss International Style)
  Single-file, pure Python stdlib, no external packages
  Browser Ctrl+P → Save as PDF
```

**Key Design Decisions:**
- **Template substitution over Jinja2** — No template engine. Simple `str.replace()` with Python stdlib.
- **Section-level placeholders** — {{EXPERIENCE_SECTION}} carries full HTML block, not per-field templates.
- **No PDF/DOCX dependencies** — Browser handles PDF conversion natively. DOCX dropped entirely.
- **renderer.py is pure stdlib** — `json`, `re`, `pathlib` only. No pip install needed.

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
├── requirements.txt                      # Python dependencies (v3.3 — zero-dependency rendering)
├── schemas/
│   └── snapshot_schema_v1.json           # Snapshot schema (v1.1 with nuance_buffer)
├── templates/
│   ├── resume_swiss.html                 # Swiss International Style template (CSS variable-driven)
│   └── state_update_template.md          # STATE_UPDATE JSON template & examples
├── scripts/
│   ├── engine.py                         # State management (Snapshot, Snapshot, parse_state_update)
│   ├── renderer.py                       # MD → HTML renderer (pure stdlib)
│   ├── jd_parser.py                      # JD + resume structured extraction
│   ├── diff_audit.py                     # Source vs tailored change analysis
│   ├── ats_checker.py                    # ATS compatibility scoring (5-region profiles)
│   ├── main.py                           # Unified CLI (parse / diff / ats)
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
# Core dependencies (v3.3 — zero-dependency rendering)
python-docx>=0.8.11          # .docx reading and writing
pdfplumber>=0.10.0           # PDF reading (recommended — best quality)
pyyaml>=6.0                  # YAML support in snapshot schema

# Removed in v3.3
#   jinja2, markdown-it-py, python-markdown, weasyprint, pypandoc
#   — replaced by zero-dependency template substitution pipeline.

# Optional fallbacks (auto-detected at runtime)
#   PyPDF2>=3.0.0            — Python native PDF fallback, no system dependency
#   pdftotext (CLI)          — https://poppler.freedesktop.org/
```

**Note:** The rendering pipeline has zero external dependencies.
- `renderer.py` uses only Python stdlib (`json`, `re`, `pathlib`).
- HTML is the primary output format. PDF is generated via browser Ctrl+P.
- `python-docx` and `pdfplumber` are only needed for **reading** source resumes — not for output generation.

</details>

<details>
<summary>🔧 Script Usage</summary>

```bash
# JD feature extraction
python scripts/main.py parse jd.txt --file --resume resume.docx --json

# Diff source vs tailored resume
python scripts/main.py diff --source resume_master.md --tailored tailored.md --json

# ATS compatibility check
python scripts/main.py ats --resume tailored.md --keywords "Python,SQL" --region north_america

# Render Markdown draft to Swiss-style HTML
python scripts/renderer.py render --draft draft.md --output output/
```

**Note:** `engine.py` provides the `Snapshot` class and `parse_state_update()` — called by the LLM via `python -c "from scripts.engine import Snapshot; ..."`. There is no Python-driven orchestration loop. The LLM reads `SKILL.md`, advances through phases, and calls scripts as tools.

</details>

<details>
<summary>🎨 Customizing Style</summary>

Edit `templates/resume_swiss.html`. All styles are inline in the `<style>` block, driven by CSS custom properties in `:root`:

```css
:root {
  --ink: #2d3748;              /* Body text color */
  --ink-light: #718096;        /* Secondary text */
  --rule: #e2e8f0;             /* Divider line color */
  --fs-body: 11pt;             /* Body text size */
  --lh-tight: 1.5;             /* Line height */
  --sp-3: 10px;                /* Section spacing */
  --grid-col-gap: 10px;        /* Date column gap */
}
```

The template is designed for **A4 portrait, single page**. Adjust `--fs-body` and padding values to fit more or less content.

</details>

---

## Version History

### v3.3 (Current) — Structured Web Search + Rendering Refactor
- **3-tier search**: S1 interview experience mining → S2 company culture/real work → S3 business signals
- **Interview intel delivery**: `{date}_{company}_{role}_interview_intel.md` stored in `history/`
- **Phase 4c integration**: Mock interview questions now sourced from real interview experiences (S1)
- **Rendering refactor**: HTML (Swiss International Style) + Markdown dual delivery; WeasyPrint/pandoc/DOCX removed
- **Swiss HTML template**: `templates/resume_swiss.html`, CSS variable-driven, single-file, browser-native printing
- **A6 anti-pattern updated**: Every search round must land on a specific downstream node or don't run
- **CP3 quantification targeting**: Quantification questions informed by what interviewers actually ask

### v3.2 — Darwin 5-Round Optimization + Onboarding System
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
