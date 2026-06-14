# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [3.3] - 2026-06-14

### Added
- **3-tier structured web search** in Phase 1 replacing vague "market research":
  - S1 — Interview experience mining: searches `"{Company} {Role} interview experience"` / `"{Role} interview questions"` to extract real interviewer checkpoints and hidden requirements
  - S2 — Company culture & real work: searches `"Working at {Company} as {Role}"` / `"{Company} tech stack"` to calibrate Phase 2 skill matching weights and CP4 cultural tone slider
  - S3 — Business signals: searches `"{Company} business focus"` / `"{Company} org changes"` to feed `risk_warnings` and `capability_clusters` targeting
  - Search results saved as `{date}_{company}_{role}_interview_intel.md` in `history/`
- **Phase 4c integration**: Mock interview questions now sourced from real interview experiences (S1)
- **A6 anti-pattern updated**: Every search round must land on a specific downstream node or don't run

### Changed
- **Rendering pipeline refactor — zero-dependency template substitution**:
  - **Old**: MD → markdown-it → Jinja2 → WeasyPrint PDF + pandoc DOCX (4 external package dependencies)
  - **New**: MD → `renderer.py` (pure stdlib: json/re/pathlib) → template substitution → HTML
  - Removed dependencies: jinja2, markdown-it-py, python-markdown, weasyprint, pypandoc
- **HTML template** replaced with Swiss International Style (`templates/resume_swiss.html`):
  - Information-first, zero decoration (no shadows, radius, gradients)
  - Typographic hierarchy: weight inversely proportional to size (300 → 400 → 600)
  - Single-file, CSS variable-driven, no external dependencies
  - A4 print-optimized: `@page { size: A4; margin: 0 }` + browser-native printing
  - Fonts: Inter (Latin) + Noto Sans SC / Microsoft YaHei (CJK)
- **Template placeholders**: Switched from per-field Jinja2 templates to section-level `{{PLACEHOLDER}}` blocks (e.g. `{{EXPERIENCE_SECTION}}` carries full HTML)
- **DOCX removed** as an output format entirely. PDF is now user-side via browser Ctrl+P
- **`output_format` schema default** changed from `"docx"` to `"html"`; `"docx"` enum value removed
- **Delivery priority**: Markdown primary (Phase 4a Writer direct output) + HTML primary (rendered output)

### Fixed
- **Print cutoff on date column**: `@page { margin }` + browser print dialog margins caused double compression → fixed with `@page { margin: 0 }` + body padding as margin
- **Date regex**: Extended to match "Present", "Current", and "至今" patterns in addition to numeric dates
- **Skills section parsing**: Fixed crash when skills section has no h3 subheadings — now wraps all bullets as a virtual entry

## [3.2] - 2026-05-31

### Added
- **Darwin Skill 5-round optimization**: 76 → **92** (+16) on the 9-dimension SkillLens rubric
- **Onboarding Check**: Global pre-flight gate — `resume_master.md` missing → Init-A before anything else
- **Init-A (Master Resume)**: 3 intake paths (paste/file/5-round questionnaire) → structured `resume_master.md`
- **Init-B (Story Library)**: Guided per-experience STAR recording with quantification + interview prep
- **Agent Execution Anti-Patterns (A1–A7)**: LLM-specific error prevention rules:
  - A1: Writer/Auditor isolation violation
  - A2: MODE misjudgment without confirmation
  - A3: STATE_UPDATE silent failure
  - A4: Phase order reordering
  - A5-A7: Empty web_search calls, quantification fabrication, confirmation skipping
- **CP4 Wording Boundary**: Explicit table of allowed (verb/tone/structure) vs forbidden (fabrication, scope inflation) edits
- **Mode Detection Protocol**: ≥50-char threshold distinguishes real JDs from vague role names; mandatory confirmation for ambiguous input
- **Required permissions declaration** in frontmatter (Read/Write/Glob/WebFetch/WebSearch/Bash)

### Changed
- **Error handling concretized**: All 9 error cases → specific action instructions; snapshot corruption backup-and-rebuild flow added
- **Mode A story library integration**: CP3 quantification priority chain (story lib > user reply > process description)
- **All `error:` language** replaced with structured primary/fallback action columns

## [3.1] - 2026-05-30

### Added
- **Init-A (Master Resume creation)**: Auto-detect existing resume files → structured `resume_master.md`; or 5-round guided questionnaire from scratch
- **Init-B (Story Library creation)**: Per-experience STAR + quantification + interview prep recording
- **Darwin Skill 9-dim evaluation**: 74.3 → 90.5 (+16.2)
- **Historical version audit (Step 4e)**: Prevents quantification regression by comparing against last 3 versions
- **Story library protocol**: 3-layer token-efficient extraction + cross-validation in audit
- **9 STOP/CHECKPOINT markers** + 2 delivery gates to prevent autonomous drift
- **Pseudo-multi-agent architecture** with isolated Scout / Architect / Auditor nodes
- **Blackboard state protocol** via `context_snapshot.json` (4-layer schema v1.1)
- **HTML rendering pipeline** with Jinja2 templates + CSS styling
- **WeasyPrint PDF** output with page overflow detection → automatic compression trigger
- **pypandoc DOCX** clean conversion (no HTML→Word formatting issues)
- **Nuance buffer** + **conversation history** for cross-node context continuity

## [3.0.3] - 2026-05-31

### Added
- **Historical Version Audit (Step 4e)** — compare new resume vs last 3 versions before delivery
  - Three check dimensions: quantification regression 🔴, content loss 🟡, wording weakening 🟡
  - Example: "显著缩短" → "48h→12h" prevention — concrete case from 2026-05-30 session
- **Anti-Pattern #9**: "never skip historical comparison"

## [3.0.2] - 2026-05-31

### Added
- **Story Library Protocol** — 3-layer token-efficient extraction for Mode B
  - Layer 1: grep `^## 项目` headers
  - Layer 2: read `> 一句话概括` for initial matching
  - Layer 3: read full STAR + interview Q&A for selected items
- **Audit cross-validation table**: every resume bullet checked against story library (✅/⚠️/🔴)

## [3.0.1] - 2026-05-31

### Added
- **6-round Darwin optimization**: 74.3 → **90.5** (+16.2)
- **9 STOP/CHECKPOINT visual markers** at all interaction checkpoints
- **Anti-Patterns section** in SKILL.md: 9 explicit prohibitions (fabrication, self-audit, vague fillers, skipping confirmation, historical regression, etc.)
- **Auto-detect resume paths**: Glob-based `resume_master.md` discovery + story library path resolution
- **Dual-column Error Handling**: primary action + secondary fallback for all 8 error scenarios

### Changed
- **Resume Input flow**: "always ask user" → 3-step auto-detection
- **Error Handling table**: single "Action" → "Primary + If Fails" dual-column
- **README/CHANGELOG**: updated with optimization results

## [3.0.0] - 2026-04-15

### Added
- **Pseudo-Multi-Agent Architecture**: Isolated expert nodes (Scout / Architect / Auditor) with blackboard state management via `context_snapshot.json`
- **4-Layer Snapshot Schema (v1.1)**: `_meta` / `facts` / `user_decisions` / `outputs` with JSON Schema validation
- **HTML Rendering Pipeline** (`scripts/renderer.py`):
  - Phase 1: Regex preprocessing for bullet summary pattern (`**Summary**: detail` → `<span class="bullet-summary">`)
  - Phase 2: Markdown → HTML conversion via markdown-it-py (with markdown fallback)
  - Phase 3: Jinja2 template layout with CSS inlining
  - Phase 4a: WeasyPrint PDF output with `len(doc.pages)` overflow detection → triggers Architect compression
  - Phase 4b: pypandoc DOCX output (clean MD→Word, avoids HTML→Word formatting chaos)
- **Jinja2 Layout Template** (`templates/resume_layout.html.j2`): HTML skeleton with inline CSS injection and hidden render metadata
- **CSS Template v3.0** (`templates/resume_template.css`): Tech Style, single-column flow layout:
  - Dual font stack: Times New Roman (Latin/Digits) + Microsoft YaHei (CJK)
  - Flexible 2-row experience header: Company · **Title** \| Date + *Department* \| Location
  - `.bullet-summary` bold prefix styling for structured bullets
  - Compact spacing with dynamic content adjustment (target ≤1 page)
  - Print optimization (`@page`, `break-inside: avoid`, color-adjust)
- **Nuance Buffer**: Layer 2 field for caching unstructured but important context between nodes
- **Conversation History Compression**: Last 3 turns auto-injected into node prompts for continuity
- **Mandatory Experience Metadata Enforcement**: Writer Guide CP1 now enforces 5-field completeness (Company, Title, Department, Date, Location)
- **Environment Check Function**: `check_rendering_environment()` detects fonts (Windows/macOS/Linux), WeasyPrint availability, pandoc installation
- **Writer Guide CP5 Section**: Complete draft finalization guide with rendering-aware Markdown rules, allowed/disallowed syntax tables, self-check checklist
- **Architecture Design Document**: `docs/plans/2026-04-15-v3-architecture-design.md` (full system design)

### Changed
- **SKILL.md**: Streamlined from monolithic instructions to ~220-line routing table (delegates detail work to reference guides)
- **engine.py**: Replaced placeholder `render_deliverables()` with actual renderer.py integration; added `record_turn()`, `add_nuance()`, `get_context_for_node()` methods
- **STATE_UPDATE Template**: New example showing `metadata_completeness` tracking and `experience_metadata` structure
- **README.md / README.zh-CN.md**: Fully rewritten for v3.0 architecture

### Fixed
- **Regex Bug**: Bullet summary pattern changed from `re.DOTALL` to `re.MULTILINE` with line anchoring — previous greedy matching would consume entire document content
- **Font Detection False Positive**: CJK font check now uses alias-based matching — "Microsoft YaHei" registry entry correctly satisfies both English and Chinese name requirements
- **Duplicate Functions**: Removed redundant `_check_fonts_macos()` and `_check_fonts_linux()` definitions from renderer.py

### Technical Decisions
- Jinja2 chosen over string concatenation for all HTML generation
- WeasyPrint chosen over pdfkit for proper Flexbox/Grid/CSS print support
- pypandoc chosen for DOCX to avoid cross-engine formatting issues
- Renderer follows READ-ONLY contract on snapshot files (returns actions, never writes back)

---

## [2.5] - 2026-04-15

### Added
- Architecture design exploration: pseudo-multi-agent + blackboard pattern
- Design document: v2.5 architecture plan (512 lines)

---

## [2.4] - 2026-04-14

### Added
- 4-stage pipeline (Contextual Intelligence → Strict Matching → Dynamic Interaction → Delivery & Reverse Audit)
- 3-tier routing system (job type / user intent / edge cases)
- Unified feature extraction across all resume formats
- Anti-Filler Rule: every bullet must have Action + Object + Measurable Outcome
- Propose-don't-ask principle: always give concrete recommendations first
- Reverse Audit: physically isolated auditor persona review
- Shadow Resume moved from automatic to on-demand trigger
- README product rewrite with bilingual support (EN/ZH-CN)

---

## [2.3] - Earlier

- Initial skill implementation
- Basic JD parsing and resume matching
