"""
Resume Tailor — Unified CLI Entry Point (v3.3)

Pure argparse layer. All business logic lives in engine.py,
jd_parser.py, diff_audit.py, and ats_checker.py.

Usage:
    python main.py parse --file jd.txt --resume resume.docx --json
    python main.py diff --source-docx source.docx --tailored-docx tailored.md --json
    python main.py ats --resume tailored.md --keywords "Python,SQL" --region north_america --json
"""

import argparse
import json
import os
import sys

# Ensure scripts/ directory is in path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ─── Subcommand handlers (thin wrappers, no sys.argv manipulation) ───


def cmd_parse(args):
    """JD feature extraction."""
    from jd_parser import parse_jd, read_resume_text, print_report, validate_output

    if args.file:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = args.input

    resume_text = read_resume_text(args.resume) if args.resume else None
    analysis = parse_jd(text, resume_text)

    if not validate_output(analysis):
        print(json.dumps({"error": "Output validation failed", "raw_output": str(analysis)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    if args.json:
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    else:
        print_report(analysis)



def cmd_diff(args):
    """Diff source vs tailored resume."""
    from diff_audit import generate_audit

    report = generate_audit(
        source_path=args.source,
        tailored_path=args.tailored,
        source_docx=args.source_docx,
        tailored_docx=args.tailored_docx,
        company=args.company,
        role=args.role,
        jd_source=args.jd_source,
        source_name=args.source_name,
        output_lang=args.lang,
        json_output=args.json,
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Diff audit saved to {args.output}")
    else:
        print(report)


def cmd_ats(args):
    """ATS compatibility check."""
    from ats_checker import run_checks, format_markdown

    try:
        with open(args.resume, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Resume file not found: {args.resume}", file=sys.stderr)
        sys.exit(1)

    # Parse keywords
    keywords = []
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    elif args.keywords_file:
        try:
            with open(args.keywords_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    keywords = data
                elif isinstance(data, dict) and "keywords" in data:
                    keywords = data["keywords"]
        except Exception as e:
            print(f"Warning: Could not read keywords file: {e}", file=sys.stderr)

    result = run_checks(text=text, keywords=keywords, region=args.region)

    if args.json:
        output = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        output = format_markdown(result, lang=args.lang)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"ATS report saved to {args.output}")
    else:
        print(output)



# ─── Argparse setup ───


def main():
    parser = argparse.ArgumentParser(
        description="Resume Tailor v3.3 — Unified CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ─── parse ───
    p_parse = subparsers.add_parser("parse", help="JD feature extraction")
    p_parse.add_argument("input", help="JD text or file path")
    p_parse.add_argument("--file", action="store_true", help="Read from file")
    p_parse.add_argument("--json", action="store_true", help="JSON output")
    p_parse.add_argument("--resume", type=str, default=None, help="Resume file")
    p_parse.set_defaults(func=cmd_parse)

    # ─── diff ───
    p_diff = subparsers.add_parser("diff", help="Diff source vs tailored")
    p_diff.add_argument("--source", type=str, default=None)
    p_diff.add_argument("--tailored", type=str, default=None)
    p_diff.add_argument("--source-docx", type=str, default=None)
    p_diff.add_argument("--tailored-docx", type=str, default=None)
    p_diff.add_argument("--company", default="")
    p_diff.add_argument("--role", default="")
    p_diff.add_argument("--jd-source", default="")
    p_diff.add_argument("--source-name", default="source resume")
    p_diff.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    p_diff.add_argument("--json", action="store_true")
    p_diff.add_argument("--output", default="")
    p_diff.set_defaults(func=cmd_diff)

    # ─── ats ───
    p_ats = subparsers.add_parser("ats", help="ATS compatibility check")
    p_ats.add_argument("--resume", required=True, help="Tailored resume path")
    p_ats.add_argument("--keywords", default="", help="Comma-separated keywords")
    p_ats.add_argument("--keywords-file", default="", help="Keywords JSON file")
    p_ats.add_argument("--region", default="global", help="Target region")
    p_ats.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    p_ats.add_argument("--json", action="store_true")
    p_ats.add_argument("--output", default="", help="Output file path")
    p_ats.set_defaults(func=cmd_ats)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
