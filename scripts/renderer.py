"""
包公.skill — Renderer (v3.4)

Zero-dependency rendering pipeline.
Replaces the old Jinja2/markdown-it/WeasyPrint/pypandoc stack.

Architecture:
  1. Parse Markdown draft into structured sections (h2-delimited)
  2. Convert each section to Swiss-template HTML fragments
  3. Load templates/resume_swiss.html, substitute {{PLACEHOLDER}} blocks
  4. Write filled HTML

Design principles:
  - Zero external Python dependencies.
  - The template is the single source of truth for layout/CSS.
  - Renderer only does content extraction + placeholder filling.
  - Template missing? Deliver raw Markdown, no error.

Entry point:
  render(snapshot_path, output_dir) -> RenderResult
"""

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ── Constants ──

BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
SWISS_TEMPLATE = "resume_swiss.html"

# Section classification: h2 text → section type
_SECTION_KEYS = {
    "summary":    ["总结", "简介", "概要", "summary", "profile", "about"],
    "projects":   ["项目", "学术", "projects", "academic"],
    "education":  ["教育", "学历", "education"],
    "skills":     ["技能", "证书", "skills", "certif"],
    "experience": ["经历", "实习", "工作", "experience", "work", "intern"],
}

# Date patterns: "2024.07 — 至今", "2021.09 — 2024.06", "Jun 2023 – Present"
_DATE_RE = re.compile(
    r'(\d{4}[.\s/]\d{1,2}|[A-Z][a-z]{2,8}\s*\d{4})\s*[–\-—]\s*'
    r'(至今|Present|Current|[A-Z][a-z]{2,8}\s*\d{4}|\d{4}[.\s/]\d{1,2})'
)

# Contact separator: phone | email | github | location
_CONTACT_SEP = re.compile(r'\s*\|\s*')

# Info-status markers that must not leak into deliverables
_INFO_MARKER_RE = re.compile(r'[ \t]*\[[\✓\?\~✓]\][ \t]*')


@dataclass
class RenderResult:
    """Structured result of a rendering pass, compatible with engine.py."""
    success: bool = False
    html_path: Optional[str] = None
    md_path: Optional[str] = None
    warnings: list = field(default_factory=list)
    errors: list = field(default_factory=list)


# ════════════════════════════════════════════════════════
# MARKDOWN PARSER
# ════════════════════════════════════════════════════════

def _classify_section(h2_text: str) -> str:
    """Map h2 heading text to a section type."""
    lower = h2_text.lower().strip()
    for stype, keywords in _SECTION_KEYS.items():
        for kw in keywords:
            if kw in lower:
                return stype
    return "experience"  # default fallback


def _parse_markdown(md_text: str) -> dict:
    """
    Parse a Markdown resume draft into structured data.

    Returns dict with keys:
      name, subtitle, contact_items, sections[].
      Each section: {type, title, entries[]}.
      Each entry: {title, subtitle, date, bullets[]}.
    """
    lines = md_text.strip().split('\n')

    result = {
        "name": "",
        "subtitle": "",
        "contact_items": [],
        "sections": [],
    }

    # ── Phase A: Extract header (before first ##) ──
    header_lines = []
    body_start = 0
    for i, line in enumerate(lines):
        if re.match(r'^##\s', line):
            body_start = i
            break
        header_lines.append(line)
    else:
        body_start = len(lines)

    # Parse header lines
    for line in header_lines:
        line = line.strip()
        if not line:
            continue
        # Skip Markdown horizontal rules
        if re.match(r'^[-*_]{3,}$', line):
            continue
        # h1 → name
        h1_m = re.match(r'^#\s+(.+)', line)
        if h1_m and not result["name"]:
            result["name"] = h1_m.group(1).strip()
            continue
        # Italic line → subtitle
        italic_m = re.match(r'^\*([^*]+)\*$', line) or re.match(r'^_([^_]+)_$', line)
        if italic_m and not result["subtitle"]:
            result["subtitle"] = italic_m.group(1).strip()
            continue
        # Pipe-separated → contact items
        if '|' in line:
            parts = _CONTACT_SEP.split(line)
            result["contact_items"] = [p.strip() for p in parts if p.strip()]
            continue
        # Plain text after name, no subtitle yet → subtitle
        if result["name"] and not result["subtitle"]:
            # Only use as subtitle if it's a short identity line (not full sentence)
            if len(line) < 80 and '。' not in line:
                result["subtitle"] = line
                continue

    # ── Phase B: Parse body sections (## delimited) ──
    current_section = None
    current_lines = []

    for line in lines[body_start:]:
        h2_m = re.match(r'^##\s+(.+)', line)
        if h2_m:
            # Flush previous section
            if current_section is not None:
                _flush_section(current_section, current_lines, result)
            current_section = {
                "type": _classify_section(h2_m.group(1)),
                "title": h2_m.group(1).strip(),
                "entries": [],
                "raw_paragraph": "",
            }
            current_lines = []
        else:
            current_lines.append(line)

    # Flush last section
    if current_section is not None:
        _flush_section(current_section, current_lines, result)

    return result


def _flush_section(section: dict, lines: list, result: dict):
    """Parse accumulated lines into entries for a section."""
    stype = section["type"]
    if stype == "summary":
        # Summary: just concatenate all non-empty lines
        section["raw_paragraph"] = ' '.join(
            l.strip() for l in lines if l.strip()
        )
    else:
        # Experience/Education/Projects/Skills: parse h3 entries + bullets
        _parse_entries(section, lines)

    result["sections"].append(section)


def _auto_prefix(text: str) -> tuple:
    """Auto-extract a bold prefix from plain bullet text.
    Splits on the first colon (Chinese or ASCII) if the prefix part is 2-20 chars.
    Skips URL-like patterns (colon followed by //).
    Returns (prefix, detail). Empty prefix if no natural split found."""
    m = re.match(r'^(.{2,20})[：:]\s*(?!//)(.+)', text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return "", text


def _parse_entries(section: dict, lines: list):
    """Parse h3-delimited entries with bullet points.
    If no h3 headings found (e.g. skills section), all bullets go into one virtual entry."""
    # First pass: detect if any h3 exists
    has_h3 = any(re.match(r'^###\s+', l.strip()) for l in lines)

    if not has_h3:
        # Skills-style: no h3, just bullets — wrap in one virtual entry
        bullets = []
        for line in lines:
            line_s = line.strip()
            if not line_s:
                continue
            bm = re.match(r'^[-*]\s+\*\*(.+?)\*\*\s*[:：]\s*(.+)', line_s)
            if bm:
                bullets.append({"prefix": bm.group(1).strip(), "detail": bm.group(2).strip()})
                continue
            pb = re.match(r'^[-*]\s+(.+)', line_s)
            if pb:
                raw = pb.group(1).strip()
                prefix, detail = _auto_prefix(raw)
                if not prefix:
                    section.setdefault("_warnings", []).append(
                        f"Bullet missing **Prefix**: format: {raw[:50]}"
                    )
                bullets.append({"prefix": prefix, "detail": detail})
        section["entries"] = [{"title": "", "subtitle": "", "date": "", "bullets": bullets}]
        return

    # Has h3: standard entry parsing
    entries = []
    current_entry = None
    current_bullets = []
    current_sub_lines = []

    for line in lines:
        line_stripped = line.strip()
        h3_m = re.match(r'^###\s+(.+)', line_stripped)
        if h3_m:
            if current_entry:
                current_entry["bullets"] = current_bullets
                entries.append(current_entry)
            h3_text = h3_m.group(1).strip()
            h3_date = ""
            h3_date_m = _DATE_RE.search(h3_text)
            if h3_date_m:
                h3_date = h3_date_m.group(0)
                h3_text = _DATE_RE.sub('', h3_text).strip().rstrip('|').strip()
            current_entry = {
                "title": h3_text,
                "subtitle": "",
                "date": h3_date,
                "bullets": [],
            }
            current_bullets = []
            current_sub_lines = []
            continue

        if not current_entry:
            continue

        if not line_stripped:
            if current_sub_lines:
                _flush_sub_info(current_entry, current_sub_lines)
                current_sub_lines = []
            continue

        bullet_m = re.match(r'^[-*]\s+\*\*(.+?)\*\*\s*[:：]\s*(.+)', line_stripped)
        if bullet_m:
            if current_sub_lines:
                _flush_sub_info(current_entry, current_sub_lines)
                current_sub_lines = []
            current_bullets.append({"prefix": bullet_m.group(1).strip(), "detail": bullet_m.group(2).strip()})
            continue

        plain_bullet = re.match(r'^[-*]\s+(.+)', line_stripped)
        if plain_bullet:
            if current_sub_lines:
                _flush_sub_info(current_entry, current_sub_lines)
                current_sub_lines = []
            raw = plain_bullet.group(1).strip()
            prefix, detail = _auto_prefix(raw)
            if not prefix:
                section.setdefault("_warnings", []).append(
                    f"Bullet missing **Prefix**: format: {raw[:50]}"
                )
            current_bullets.append({"prefix": prefix, "detail": detail})
            continue

        # Skip Markdown horizontal rules
        if re.match(r'^[-*_]{3,}$', line_stripped):
            continue
        current_sub_lines.append(line_stripped)

    if current_entry:
        if current_sub_lines:
            _flush_sub_info(current_entry, current_sub_lines)
        current_entry["bullets"] = current_bullets
        entries.append(current_entry)

    section["entries"] = entries


def _flush_sub_info(entry: dict, sub_lines: list):
    """Parse subtitle lines: extract date + org/department/meta."""
    combined = ' '.join(sub_lines).strip()
    if not combined:
        return

    # Extract date from subtitle text
    date_m = _DATE_RE.search(combined)
    if date_m:
        entry["date"] = date_m.group(0)
        combined = _DATE_RE.sub('', combined).strip()

    # Clean pipes
    combined = re.sub(r'\s*\|\s*', ' · ', combined)
    combined = re.sub(r'\s+', ' ', combined).strip()
    entry["subtitle"] = combined


# ════════════════════════════════════════════════════════
# HTML GENERATORS (per section type)
# ════════════════════════════════════════════════════════

def _gen_summary_html(section: dict) -> str:
    """Generate summary section HTML block."""
    text = section.get("raw_paragraph", "")
    if not text:
        return ""
    title = section.get("title", "个人总结")
    return (
        f'<div class="section-title">{title}</div>\n'
        f'<p class="summary-text">{text}</p>\n'
    )


def _gen_entry_section_html(section: dict) -> str:
    """
    Generate HTML for experience / projects / education sections.
    Matches the Swiss template's CSS classes:
      .exp-item > .exp-header (grid: .exp-role + .exp-date) > .exp-sub > .exp-bullets
    """
    title = section.get("title", "")
    entries = section.get("entries", [])
    stype = section.get("type", "experience")

    if not entries:
        return ""

    # Build section
    parts = [f'<div class="section-title">{title}</div>\n']

    for entry in entries:
        parts.append('<div class="exp-item">')

        # Entry header row: role + date (grid)
        entry_title = entry.get("title", "")
        entry_date = entry.get("date", "")
        parts.append('  <div class="exp-header">')
        parts.append(f'    <span class="exp-role">{entry_title}</span>')
        if entry_date:
            parts.append(f'    <span class="exp-date">{entry_date}</span>')
        parts.append('  </div>')

        # Subtitle row (org / department / GPA / location)
        subtitle = entry.get("subtitle", "")
        if subtitle:
            parts.append(f'  <div class="exp-sub">{subtitle}</div>')

        # Bullets
        bullets = entry.get("bullets", [])
        if bullets:
            parts.append('  <ul class="exp-bullets">')
            for b in bullets:
                prefix = b.get("prefix", "")
                detail = b.get("detail", "")
                if prefix:
                    parts.append(
                        f'    <li><span class="bullet-label">{prefix}</span> {detail}</li>'
                    )
                else:
                    parts.append(f'    <li>{detail}</li>')
            parts.append('  </ul>')

        parts.append('</div>\n')

    return '\n'.join(parts)


def _gen_skills_html(section: dict) -> str:
    """Generate skills section HTML block."""
    title = section.get("title", "技能与证书")
    entries = section.get("entries", [])

    parts = [f'<div class="section-title">{title}</div>\n']
    parts.append('<div class="skills-grid">')

    for entry in entries:
        entry_title = entry.get("title", "")
        bullets = entry.get("bullets", [])
        for b in bullets:
            prefix = b.get("prefix", "")
            detail = b.get("detail", "")
            if prefix:
                parts.append(
                    f'  <div class="skill-entry">'
                    f'<span class="skill-label">{prefix}</span> {detail}'
                    f'</div>'
                )
            elif detail:
                parts.append(f'  <div class="skill-entry">{detail}</div>')

    parts.append('</div>')
    return '\n'.join(parts)


# ════════════════════════════════════════════════════════
# TEMPLATE SUBSTITUTION
# ════════════════════════════════════════════════════════

def _load_template() -> str:
    """Load the Swiss HTML template."""
    path = TEMPLATES_DIR / SWISS_TEMPLATE
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text(encoding="utf-8")


def _fill_template(parsed: dict, template: str) -> str:
    """Substitute all {{PLACEHOLDER}} blocks with parsed content."""
    # Header
    html = template.replace("{{NAME}}", parsed.get("name", ""))

    # Subtitle block
    subtitle = parsed.get("subtitle", "")
    if subtitle:
        html = html.replace(
            "{{SUBTITLE_BLOCK}}",
            f'<div class="resume-subtitle">{subtitle}</div>'
        )
    else:
        html = html.replace("{{SUBTITLE_BLOCK}}", "")

    # Contact items
    contacts = parsed.get("contact_items", [])
    if contacts:
        contact_html = '\n    '.join(
            f'<span>{c}</span>' for c in contacts
        )
        html = html.replace("{{CONTACT_ITEMS}}", contact_html)
    else:
        html = html.replace("{{CONTACT_ITEMS}}", "")

    # Section blocks
    sections_by_type = {}
    for s in parsed.get("sections", []):
        stype = s["type"]
        if stype == "summary":
            sections_by_type["summary"] = _gen_summary_html(s)
        elif stype in ("experience", "projects", "education"):
            sections_by_type[stype] = _gen_entry_section_html(s)
        elif stype == "skills":
            sections_by_type["skills"] = _gen_skills_html(s)

    # Fill each section block (or leave empty)
    html = html.replace("{{SUMMARY_BLOCK}}", sections_by_type.get("summary", ""))
    html = html.replace("{{EXPERIENCE_SECTION}}", sections_by_type.get("experience", ""))
    html = html.replace("{{PROJECTS_SECTION}}", sections_by_type.get("projects", ""))
    html = html.replace("{{EDUCATION_SECTION}}", sections_by_type.get("education", ""))
    html = html.replace("{{SKILLS_SECTION}}", sections_by_type.get("skills", ""))

    # Meta
    html = html.replace("{{META_EXTRA}}", "")

    return html


# ════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ════════════════════════════════════════════════════════

def render(snapshot_path: str, output_dir: str = None) -> RenderResult:
    """
    Main rendering entry point — compatible with engine.py v3.x.

    Reads snapshot.json, extracts the Writer's Markdown draft,
    fills the Swiss HTML template, and writes the result.

    Args:
        snapshot_path: Absolute path to context_snapshot.json
        output_dir: Directory for outputs (defaults to session dir)

    Returns:
        RenderResult with html_path and status.
    """
    result = RenderResult()
    snap_path = Path(snapshot_path)

    if not snap_path.exists():
        result.errors.append(f"Snapshot not found: {snapshot_path}")
        return result

    # Load snapshot (READ-ONLY)
    with open(snap_path, "r", encoding="utf-8") as f:
        snapshot_data = json.load(f)

    # Determine output directory
    if output_dir is None:
        output_dir = str(snap_path.parent)
    out = Path(output_dir)

    # Locate draft markdown
    draft_rel_path = snapshot_data.get("expert_outputs", {}).get("writer_draft_path")
    if not draft_rel_path:
        result.errors.append("No writer_draft_path found in snapshot expert_outputs.")
        return result

    draft_full_path = BASE_DIR / draft_rel_path
    if not draft_full_path.exists():
        result.errors.append(f"Draft file not found: {draft_full_path}")
        return result

    md_text = draft_full_path.read_text(encoding="utf-8")
    md_text = _INFO_MARKER_RE.sub('', md_text)

    # Save raw Markdown as deliverable
    md_out = out / "tailored_resume.md"
    md_out.write_text(md_text, encoding="utf-8")
    result.md_path = str(md_out)

    # Load template
    try:
        template = _load_template()
    except FileNotFoundError as e:
        # Graceful degradation: Markdown only
        result.warnings.append(f"Template missing: {e}. Delivering Markdown only.")
        result.success = True
        return result

    # Parse + render
    try:
        parsed = _parse_markdown(md_text)
        for s in parsed.get("sections", []):
            for w in s.pop("_warnings", []):
                result.warnings.append(w)
        html_output = _fill_template(parsed, template)

        html_out = out / "tailored_resume.html"
        html_out.write_text(html_output, encoding="utf-8")
        result.html_path = str(html_out)
        result.success = True

    except Exception as e:
        result.errors.append(f"Rendering failed: {e}")
        result.warnings.append(
            "Fallback: Markdown draft is available for manual formatting."
        )

    return result


# ════════════════════════════════════════════════════════
# DIRECT MARKDOWN RENDERING (no snapshot needed)
# ════════════════════════════════════════════════════════

def render_md(md_path: str, output_dir: str = None) -> RenderResult:
    """
    Render a Markdown draft directly to HTML without a snapshot.

    Args:
        md_path: Absolute path to a Markdown resume draft.
        output_dir: Directory for outputs (defaults to same dir as md_path).

    Returns:
        RenderResult with html_path and status.
    """
    result = RenderResult()
    md_file = Path(md_path)

    if not md_file.exists():
        result.errors.append(f"Markdown file not found: {md_path}")
        return result

    md_text = md_file.read_text(encoding="utf-8")
    md_text = _INFO_MARKER_RE.sub('', md_text)

    if output_dir is None:
        output_dir = str(md_file.parent)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    result.md_path = str(md_file)

    try:
        template = _load_template()
    except FileNotFoundError as e:
        result.warnings.append(f"Template missing: {e}. Delivering Markdown only.")
        result.success = True
        return result

    try:
        parsed = _parse_markdown(md_text)
        for s in parsed.get("sections", []):
            for w in s.pop("_warnings", []):
                result.warnings.append(w)
        html_output = _fill_template(parsed, template)

        html_out = out / (md_file.stem + ".html")
        html_out.write_text(html_output, encoding="utf-8")
        result.html_path = str(html_out)
        result.success = True
    except Exception as e:
        result.errors.append(f"Rendering failed: {e}")
        result.warnings.append("Fallback: Markdown draft is available for manual formatting.")

    return result


# ════════════════════════════════════════════════════════
# CLI INTERFACE
# ════════════════════════════════════════════════════════

def _print_result(result: RenderResult):
    """Pretty-print a RenderResult."""
    print(f"\n{'='*50}")
    print(f"Status: {'SUCCESS' if result.success else 'FAILED'}")
    print(f"\nOutputs:")
    print(f"  Markdown: {result.md_path or 'N/A'}")
    print(f"  HTML:     {result.html_path or 'N/A'}")
    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for w in result.warnings:
            print(f"  ⚠️  {w}")
    if result.errors:
        print(f"\nErrors ({len(result.errors)}):")
        for e in result.errors:
            print(f"  ❌ {e}")


def main():
    """
    CLI entry points:
      renderer.py <snapshot.json> [output_dir]        # snapshot mode (backward compat)
      renderer.py --md <draft.md> [--output output/]   # direct MD mode
    """
    import argparse

    parser = argparse.ArgumentParser(description="包公.skill Renderer v3.4")
    parser.add_argument("source", nargs="?", help="Path to snapshot.json (positional, backward compat)")
    parser.add_argument("output_dir_pos", nargs="?", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--md", dest="md_path", help="Path to Markdown draft (direct rendering, no snapshot)")
    parser.add_argument("--output", "-o", default=None, help="Output directory")
    args = parser.parse_args()

    output_dir = args.output or args.output_dir_pos

    if args.md_path:
        print(f"[Renderer v3.4] Direct MD: {args.md_path}")
        result = render_md(args.md_path, output_dir)
    elif args.source:
        print(f"[Renderer v3.4] Snapshot: {args.source}")
        result = render(args.source, output_dir)
    else:
        parser.error("Provide either a snapshot.json path or --md <draft.md>")
        return 1

    _print_result(result)
    return 0 if result.success else 1


if __name__ == "__main__":
    for _s in (sys.stdout, sys.stderr, sys.stdin):
        _s.reconfigure(encoding="utf-8")
    sys.exit(main())
