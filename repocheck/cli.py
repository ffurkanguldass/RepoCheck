import argparse
import sys
from pathlib import Path

from repocheck.core import audit_source
from repocheck.core import render_terminal
from repocheck.core import write_html_report
from repocheck.core import write_json_report


def build_parser():
    parser = argparse.ArgumentParser(
        prog="repocheck",
        description="Audit a repository for reproducibility risk.",
    )
    parser.add_argument("--version", action="version", version="repocheck 0.1.0")
    subparsers = parser.add_subparsers(dest="command")
    for name in ("check", "run"):
        command = subparsers.add_parser(name, help="Audit a repository.")
        command.add_argument("source", nargs="?", default=".")
        command.add_argument("--mode", choices=("fast", "smoke", "full"), default="fast")
        command.add_argument("--smoke", action="store_true", help="Shortcut for --mode smoke.")
        command.add_argument("--report", choices=("terminal", "json", "html", "all"), default="terminal")
        command.add_argument("--output-dir", default=".")
        command.add_argument("--json-path")
        command.add_argument("--html-path")
        command.add_argument("--no-cache", action="store_true")
        command.add_argument("--strict", action="store_true")
    return parser


def main(argv=None):
    parser = build_parser()
    if argv is None:
        argv = sys.argv[1:]
    if argv and argv[0] not in {"check", "run", "-h", "--help", "--version"}:
        argv = ["check"] + argv
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 1
    if args.smoke:
        args.mode = "smoke"
    report = audit_source(args.source, mode=args.mode, use_cache=not args.no_cache)
    print(render_terminal(report))
    output_dir = Path(args.output_dir).resolve()
    if args.report in {"json", "all"}:
        json_path = Path(args.json_path).resolve() if args.json_path else output_dir / "repocheck_report.json"
        write_json_report(report, json_path)
        print(f"JSON report: {json_path}")
    if args.report in {"html", "all"}:
        html_path = Path(args.html_path).resolve() if args.html_path else output_dir / "repocheck_report.html"
        write_html_report(report, html_path)
        print(f"HTML report: {html_path}")
    if args.strict and report.risk_summary.get("high", 0):
        return 2
    if report.smoke and not report.smoke.success:
        return 3
    return 0
