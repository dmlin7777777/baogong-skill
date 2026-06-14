<div align="center">

# Resume Tailor

**AI-Powered Resume Tailoring — Not a Polisher, a Coach**

*This project follows a "Coach, not Polisher" philosophy.*

[English](README.md) · [简体中文](README.zh-CN.md)

**v3.4 — 6-Scenario Routing + Fabrication Gate + Stress-Tested Pipeline**

[Changelog →](CHANGELOG.md)

</div>

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

See [CHANGELOG.md](CHANGELOG.md) for the full version history.

| Version | Date | Highlights |
|---------|------|------------|
| **v3.3** | 2026-06 | 3-tier web search, zero-dep rendering, Swiss HTML template, DOCX removed |
| **v3.2** | 2026-05 | Onboarding system, Agent anti-patterns (A1–A7), Darwin 76→92 |
| **v3.1** | 2026-05 | Init-A/B, story library, historical version audit, Darwin 74→91 |
| **v3.0** | 2026-04 | Multi-agent architecture, blackboard state, HTML/DOCX/PDF pipeline |
| **v2.4** | 2026-04 | 4-stage pipeline, Anti-Filler Rule, Reverse Audit |

---

## License

MIT
