#!/usr/bin/env python3
"""
HASE v7.0 Developer Toolkit, AST Graph Engine & Memory Ledger
Universal Token-Guided Inference CLI for Calculating, Explaining, Verifying,
Building Codebase Symbol Graphs, and Maintaining Working Memory.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

PLANES: List[Tuple[int, str, str, str]] = [
    (0x01, "arch", "Macro-Architecture", "SOLID design, clean boundaries, separation of concerns, loose coupling."),
    (0x02, "state", "State & Lifecycle", "Concurrency/async safety, immutability, deterministic cleanup, atomic transitions."),
    (0x04, "fault", "Defensive Design", "Input sanitization, boundary checks, explicit error paths, no swallowed errors."),
    (0x08, "perf", "Performance & Big-O", "Low allocation churn, cache locality, optimal complexity, leak prevention."),
    (0x10, "obs", "Observability", "Structured logging, telemetry/metric hooks, error context propagation."),
    (0x20, "test", "Verification & Testing", "Pure logic isolation, mock boundaries. Companion tests required."),
    (0x40, "idiom", "Idiomatic Alignment", "Target language idioms, ecosystem standards, standard library priority."),
    (0x80, "sec", "Security & Zero-Trust", "Injection immunity, secret hygiene, least privilege, safe deserialization."),
]

PLANE_BY_FLAG: Dict[str, Tuple[int, str, str, str]] = {p[1]: p for p in PLANES}
PLANE_BY_BIT: Dict[int, Tuple[int, str, str, str]] = {p[0]: p for p in PLANES}

IGNORED_DIRS: Set[str] = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
    "target",
    ".idea",
    ".vscode",
    ".cursor",
    ".sourcegraph",
    ".agents",
}


def format_hex_byte(val: int) -> str:
    """Format an integer as a clean 2-digit uppercase hex byte string (e.g., 0x4D)."""
    return f"0x{val & 0xFF:02X}"


def calc_state(selected_bits: List[int]) -> int:
    """Compute state by bitwise OR of selected bits."""
    total = 0
    for b in selected_bits:
        total |= b
    return total & 0xFF


def explain_state(val: int) -> Dict[str, Any]:
    """Decode a state byte into active and inactive planes."""
    active = []
    inactive = []
    for bit, slug, name, mandate in PLANES:
        if val & bit:
            active.append({"bit": bit, "hex": format_hex_byte(bit), "slug": slug, "name": name, "mandate": mandate})
        else:
            inactive.append({"bit": bit, "hex": format_hex_byte(bit), "slug": slug, "name": name, "mandate": mandate})
    return {
        "val": val,
        "hex": format_hex_byte(val),
        "active": active,
        "inactive": inactive,
        "requires_tests": bool(val & 0x20),
    }


def parse_state_int(val_str: str) -> int:
    """Parse integer from hex or decimal string."""
    val_str = val_str.strip()
    if val_str.lower().startswith("0x"):
        return int(val_str, 16)
    return int(val_str, 10)


def verify_output(text: str) -> Tuple[bool, List[str]]:
    """
    Verify whether an AI output adheres to the HASE v7.0 protocol.
    Returns (is_valid, list_of_issues).
    """
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    issues: List[str] = []

    if not lines:
        return False, ["Output is empty."]

    # Line 1 Check: [STATE: 0xXX]
    state_match = re.match(r"^\[STATE:\s*(0x[0-9A-Fa-f]{2})\]$", lines[0], re.IGNORECASE)
    if not state_match:
        issues.append(f"Line 1 must be formatted exactly as '[STATE: 0xXX]', found: '{lines[0]}'")
        state_val = 0
    else:
        state_val = int(state_match.group(1), 16)

    # Line 2 Check: [PLAN: Approach | Rationale | Risk -> Mitigation]
    if len(lines) < 2:
        issues.append("Missing Line 2 plan matrix.")
    else:
        plan_line = lines[1]
        if not plan_line.startswith("[PLAN:") or not plan_line.endswith("]"):
            issues.append(f"Line 2 must start with '[PLAN:' and end with ']', found: '{plan_line}'")
        else:
            content = plan_line[6:-1].strip()
            parts = [p.strip() for p in content.split("|")]
            if len(parts) != 3:
                issues.append(
                    f"Line 2 PLAN must have exactly 3 pipe-separated segments (Approach | Rationale | Risk -> Mitigation), found {len(parts)} segments."
                )
            else:
                if "->" not in parts[2]:
                    issues.append("Line 2 PLAN segment 3 must contain 'Risk -> Mitigation' notation.")

    # Check optional Line 3 for [MEM: ...]
    code_start_idx = 2
    if len(lines) > 2 and lines[2].startswith("[MEM:") and lines[2].endswith("]"):
        code_start_idx = 3

    # Check for forbidden stub tokens in code
    full_code = "\n".join(lines[code_start_idx:]) if len(lines) > code_start_idx else ""
    forbidden_stubs = ["TODO:", "FIXME:", "pass  # placeholder", "NotImplementedError()", "NotImplementedException"]
    for stub in forbidden_stubs:
        if stub in full_code:
            issues.append(f"Forbidden placeholder/stub detected: '{stub}'")

    # If testability plane (0x20) is set, verify tests or assertions are present
    if state_val & 0x20:
        has_tests = any(
            t in full_code.lower()
            for t in ["def test_", "test(", "describe(", "assert ", "testing.t", "check(", "expect("]
        )
        if not has_tests:
            issues.append("Plane 0x20 (Testability) is active, but no companion test blocks or assertions were detected.")

    return len(issues) == 0, issues


# ==============================================================================
# AST & CODEBASE TOPOLOGY GRAPH ENGINE
# ==============================================================================

class PySymbolExtractor(ast.NodeVisitor):
    """Extracts symbols, classes, methods, and imports from Python AST."""

    def __init__(self) -> None:
        self.imports: List[str] = []
        self.classes: List[Dict[str, Any]] = []
        self.functions: List[Dict[str, Any]] = []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imports.append(alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ""
        for alias in node.names:
            self.imports.append(f"{module}.{alias.name}" if module else alias.name)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        bases = []
        for b in node.bases:
            if isinstance(b, ast.Name):
                bases.append(b.id)
            elif isinstance(b, ast.Attribute):
                bases.append(f"{ast.unparse(b)}")

        methods: List[str] = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = [a.arg for a in item.args.args if a.arg != "self"]
                ret = f" -> {ast.unparse(item.returns)}" if item.returns else ""
                methods.append(f"{item.name}({', '.join(args)}){ret}")

        self.classes.append({
            "name": node.name,
            "bases": bases,
            "line_start": node.lineno,
            "line_end": getattr(node, "end_lineno", node.lineno),
            "methods": methods,
        })

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._record_func(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._record_func(node, is_async=True)

    def _record_func(self, node: ast.FunctionDef | ast.AsyncFunctionDef, is_async: bool = False) -> None:
        args = []
        for a in node.args.args:
            arg_str = a.arg
            if a.annotation:
                arg_str += f": {ast.unparse(a.annotation)}"
            args.append(arg_str)
        ret = f" -> {ast.unparse(node.returns)}" if node.returns else ""
        prefix = "async def " if is_async else "def "
        self.functions.append({
            "signature": f"{prefix}{node.name}({', '.join(args)}){ret}",
            "name": node.name,
            "line_start": node.lineno,
            "line_end": getattr(node, "end_lineno", node.lineno),
        })


def extract_regex_symbols(file_path: Path, content: str) -> Dict[str, Any]:
    """Lightweight fallback symbol extractor for JS/TS, Go, Rust."""
    ext = file_path.suffix.lower()
    imports: List[str] = []
    symbols: List[str] = []

    lines = content.splitlines()
    line_count = len(lines)

    if ext in {".ts", ".tsx", ".js", ".jsx"}:
        for ln in lines:
            ln_s = ln.strip()
            # Imports
            imp_m = re.match(r"^import\s+.*?from\s+['\"](.*?)['\"]", ln_s)
            if imp_m:
                imports.append(imp_m.group(1))
            # Exported classes / interfaces / types / functions
            exp_m = re.match(r"^export\s+(default\s+)?(class|interface|type|enum|function|const)\s+([A-Za-z0-9_]+)", ln_s)
            if exp_m:
                symbols.append(f"{exp_m.group(2)} {exp_m.group(3)}")
    elif ext == ".go":
        for ln in lines:
            ln_s = ln.strip()
            if ln_s.startswith("import "):
                imports.append(ln_s)
            type_m = re.match(r"^type\s+([A-Za-z0-9_]+)\s+(struct|interface)", ln_s)
            if type_m:
                symbols.append(f"{type_m.group(2)} {type_m.group(1)}")
            func_m = re.match(r"^func\s+(\([^\)]+\)\s+)?([A-Za-z0-9_]+)\s*\(", ln_s)
            if func_m:
                receiver = func_m.group(1) or ""
                symbols.append(f"func {receiver}{func_m.group(2)}")
    elif ext == ".rs":
        for ln in lines:
            ln_s = ln.strip()
            if ln_s.startswith("use "):
                imports.append(ln_s.replace("use ", "").replace(";", ""))
            rs_m = re.match(r"^(pub\s+)?(fn|struct|enum|trait)\s+([A-Za-z0-9_]+)", ln_s)
            if rs_m:
                symbols.append(f"{rs_m.group(2)} {rs_m.group(3)}")

    return {
        "file": str(file_path),
        "lines": line_count,
        "imports": imports[:8],
        "symbols": symbols[:15],
    }


def build_ast_graph(root_path: Path, max_files: int = 400) -> Dict[str, Any]:
    """
    Scans the repository and builds a token-optimized AST symbol graph.
    Returns structured graph dictionary.
    """
    root_path = root_path.resolve()
    parsed_files: List[Dict[str, Any]] = []
    dep_graph: Dict[str, List[str]] = {}

    target_extensions = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs"}

    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS and not d.startswith(".")]
        for fn in sorted(filenames):
            fp = Path(dirpath) / fn
            if fp.suffix.lower() not in target_extensions:
                continue

            rel_path = str(fp.relative_to(root_path)).replace("\\", "/")
            try:
                content = fp.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            lines_count = len(content.splitlines())

            if fp.suffix.lower() == ".py":
                try:
                    tree = ast.parse(content, filename=str(fp))
                    extractor = PySymbolExtractor()
                    extractor.visit(tree)
                    parsed_files.append({
                        "file": rel_path,
                        "lines": lines_count,
                        "imports": extractor.imports[:10],
                        "classes": extractor.classes,
                        "functions": extractor.functions,
                    })
                    dep_graph[rel_path] = extractor.imports[:8]
                except Exception:
                    # Fallback on syntax error
                    info = extract_regex_symbols(fp, content)
                    info["file"] = rel_path
                    parsed_files.append(info)
                    dep_graph[rel_path] = info["imports"]
            else:
                info = extract_regex_symbols(fp, content)
                info["file"] = rel_path
                parsed_files.append(info)
                dep_graph[rel_path] = info["imports"]

            if len(parsed_files) >= max_files:
                break
        if len(parsed_files) >= max_files:
            break

    return {
        "root": str(root_path),
        "total_files": len(parsed_files),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": parsed_files,
        "dependencies": dep_graph,
    }


def export_compact_graph(graph_data: Dict[str, Any]) -> str:
    """Formats the AST graph into a high-density, token-saver Markdown document."""
    lines: List[str] = [
        "# CODEBASE AST TOPOLOGY GRAPH",
        f"*Generated by HASE v7.0 AST Engine | {graph_data.get('total_files', 0)} files indexed*",
        "",
        "## 1. Module Dependency Topology",
    ]

    for fpath, imps in graph_data.get("dependencies", {}).items():
        if imps:
            clean_imps = ", ".join(imps[:6])
            lines.append(f"- `{fpath}` -> [{clean_imps}]")

    lines.append("")
    lines.append("## 2. AST Symbol Hierarchy")

    for f in graph_data.get("files", []):
        fpath = f["file"]
        lines_count = f.get("lines", 0)
        lines.append(f"### `{fpath}` (Lines: 1-{lines_count})")

        # Python classes
        for cls in f.get("classes", []):
            bases = f"({', '.join(cls['bases'])})" if cls.get("bases") else ""
            methods = f": {', '.join(cls['methods'][:5])}" if cls.get("methods") else ""
            lines.append(f"  - `class {cls['name']}{bases}` [L{cls['line_start']}-L{cls['line_end']}]{methods}")

        # Python functions
        for func in f.get("functions", []):
            lines.append(f"  - `{func['signature']}` [L{func['line_start']}-L{func['line_end']}]")

        # Generic symbols (TS/Go/Rust)
        for sym in f.get("symbols", []):
            lines.append(f"  - `{sym}`")

        lines.append("")

    return "\n".join(lines)


# ==============================================================================
# HASE WORKSPACE MEMORY LEDGER
# ==============================================================================

def get_memory_file(workspace_path: Path) -> Path:
    """Returns path to the .hase/memory.json file."""
    return workspace_path / ".hase" / "memory.json"


def load_memory(workspace_path: Path) -> Dict[str, Any]:
    """Loads workspace memory ledger, initializing if missing."""
    mem_file = get_memory_file(workspace_path)
    if mem_file.exists():
        try:
            return json.loads(mem_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "version": "7.0",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "findings": [],
        "invariants": [],
    }


def save_memory(workspace_path: Path, data: Dict[str, Any]) -> None:
    """Persists data to .hase/memory.json."""
    mem_file = get_memory_file(workspace_path)
    mem_file.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    mem_file.write_text(json.dumps(data, indent=2), encoding="utf-8")


def add_memory_finding(
    workspace_path: Path,
    topic: str,
    fact: str,
    files: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Appends an architectural finding to the working memory."""
    mem = load_memory(workspace_path)
    finding_id = f"f-{len(mem['findings']) + 1:03d}"
    entry = {
        "id": finding_id,
        "topic": topic,
        "fact": fact,
        "files": files or [],
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    mem["findings"].append(entry)
    save_memory(workspace_path, mem)
    return entry


def add_memory_invariant(workspace_path: Path, rule: str) -> str:
    """Appends an unchangeable project architectural invariant."""
    mem = load_memory(workspace_path)
    if rule not in mem["invariants"]:
        mem["invariants"].append(rule)
        save_memory(workspace_path, mem)
    return rule


def clear_memory(workspace_path: Path) -> None:
    """Resets working memory."""
    mem = {
        "version": "7.0",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "findings": [],
        "invariants": [],
    }
    save_memory(workspace_path, mem)


# ==============================================================================
# RULE INSTALLATION ENGINE
# ==============================================================================

def install_rules(repo_root: Path, target_dir: Path, tools: List[str]) -> List[str]:
    """Copy appropriate rule files to target project directory and initialize .hase."""
    installed: List[str] = []
    target_dir.mkdir(parents=True, exist_ok=True)

    tool_map = {
        "cursor": [
            (repo_root / ".cursorrules", target_dir / ".cursorrules"),
            (repo_root / ".cursor" / "rules" / "hase.mdc", target_dir / ".cursor" / "rules" / "hase.mdc"),
        ],
        "windsurf": [(repo_root / ".windsurfrules", target_dir / ".windsurfrules")],
        "claude": [(repo_root / "CLAUDE.md", target_dir / "CLAUDE.md")],
        "copilot": [(repo_root / ".github" / "copilot-instructions.md", target_dir / ".github" / "copilot-instructions.md")],
        "cody": [(repo_root / ".sourcegraph" / "hase.rule.md", target_dir / ".sourcegraph" / "hase.rule.md")],
        "cline": [(repo_root / ".clinerules", target_dir / ".clinerules")],
        "aider": [(repo_root / "CONVENTIONS.md", target_dir / "CONVENTIONS.md")],
        "gemini": [
            (repo_root / "GEMINI.md", target_dir / "GEMINI.md"),
            (repo_root / ".agents" / "rules" / "hase.md", target_dir / ".agents" / "rules" / "hase.md"),
        ],
    }

    selected_tools = list(tool_map.keys()) if "all" in tools else [t.lower() for t in tools]

    for tool in selected_tools:
        if tool in tool_map:
            for src, dst in tool_map[tool]:
                if src.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    installed.append(str(dst.relative_to(target_dir)))

    # Initialize .hase context directory
    hase_dir = target_dir / ".hase"
    hase_dir.mkdir(parents=True, exist_ok=True)
    load_memory(target_dir)

    # Build and write codebase AST graph
    try:
        graph = build_ast_graph(target_dir)
        context_md = export_compact_graph(graph)
        (hase_dir / "context.md").write_text(context_md, encoding="utf-8")
        installed.append(".hase/context.md")
    except Exception:
        pass

    return installed


# ==============================================================================
# MAIN CLI DISPATCHER
# ==============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="hase",
        description="HASE v7.0: Token-Guided Inference, AST Graph & Memory Ledger Engine",
    )
    subparsers = parser.add_subparsers(dest="command")

    # Command: calc
    p_calc = subparsers.add_parser("calc", help="Calculate hexadecimal state byte from architectural planes.")
    short_flags = {
        "arch": "-a",
        "state": "-s",
        "fault": "-f",
        "perf": "-p",
        "obs": "-o",
        "test": "-t",
        "idiom": "-i",
        "sec": "-x",
    }
    for bit, slug, name, _ in PLANES:
        p_calc.add_argument(f"--{slug}", short_flags.get(slug), action="store_true", help=f"Activate {name} ({format_hex_byte(bit)})")
    p_calc.add_argument("values", nargs="*", help="Optional integers or plane slugs to add (e.g. 1 4 8 64 or arch fault)")

    # Command: explain
    p_explain = subparsers.add_parser("explain", help="Decode and explain an active HASE state byte.")
    p_explain.add_argument("state", help="State token (e.g. 0x4D, 77, or '[STATE: 0x4D]')")

    # Command: verify
    p_verify = subparsers.add_parser("verify", help="Verify model output for HASE v7.0 protocol compliance.")
    p_verify.add_argument("target", help="File path or raw string to verify.")

    # Command: matrix
    subparsers.add_parser("matrix", help="Display the complete HASE v7.0 8-plane cognitive matrix.")

    # Command: graph
    p_graph = subparsers.add_parser("graph", help="Generate token-optimized AST symbol & dependency topology graph.")
    p_graph.add_argument("--target", "-t", default=".", help="Root directory of repository (default: current directory)")
    p_graph.add_argument("--output", "-o", help="Path to write output file (default: stdout or .hase/context.md)")
    p_graph.add_argument("--json", action="store_true", help="Output machine-readable JSON instead of Markdown")

    # Command: memory
    p_mem = subparsers.add_parser("memory", help="Manage project working memory and architectural invariants.")
    p_mem_sub = p_mem.add_subparsers(dest="mem_action")

    p_mem_sub.add_parser("list", help="List all recorded findings and architectural invariants.")
    p_mem_add = p_mem_sub.add_parser("add", help="Add an architectural finding to memory.")
    p_mem_add.add_argument("--topic", "-t", required=True, help="Domain or topic (e.g. Auth, DB, Performance)")
    p_mem_add.add_argument("--fact", "-f", required=True, help="Specific finding or technical discovery")
    p_mem_add.add_argument("--files", nargs="*", help="Relevant file paths")

    p_mem_inv = p_mem_sub.add_parser("invariant", help="Add an immutable architectural invariant.")
    p_mem_inv.add_argument("rule", help="Invariant statement (e.g. 'All database mutations must use atomic context')")

    p_mem_sub.add_parser("clear", help="Clear working memory findings.")

    # Command: sync
    p_sync = subparsers.add_parser("sync", help="One-command sync: regenerate .hase/context.md and ensure .hase/memory.json is initialized.")
    p_sync.add_argument("--target", "-t", default=".", help="Target project root directory (default: current directory)")

    # Command: init
    p_init = subparsers.add_parser("init", help="Install HASE rules into a target project directory.")
    p_init.add_argument("--target", "-t", default=".", help="Target project root directory (default: current directory)")
    p_init.add_argument(
        "--tools",
        default="all",
        help="Comma-separated list of tools to install (cursor, windsurf, claude, copilot, cody, cline, aider, gemini, all)",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "calc":
        selected_bits: List[int] = []
        for bit, slug, _, _ in PLANES:
            if getattr(args, slug, False):
                selected_bits.append(bit)
        for val in args.values:
            val_clean = val.lower().strip()
            if val_clean in PLANE_BY_FLAG:
                selected_bits.append(PLANE_BY_FLAG[val_clean][0])
            else:
                try:
                    num = parse_state_int(val_clean)
                    selected_bits.append(num)
                except ValueError:
                    print(f"Error: Unknown plane or integer '{val}'", file=sys.stderr)
                    return 1

        state = calc_state(selected_bits)
        hex_str = format_hex_byte(state)
        print(f"State Byte: {hex_str} (Decimal: {state}, Binary: {bin(state)})")
        explanation = explain_state(state)
        print("\nActive Planes:")
        for p in explanation["active"]:
            print(f"  + {p['hex']} [{p['name']}]: {p['mandate']}")
        if not explanation["active"]:
            print("  (None active - 0x00)")
        return 0

    elif args.command == "explain":
        raw = args.state.strip()
        state_match = re.search(r"0x[0-9A-Fa-f]{1,2}", raw)
        if state_match:
            val = int(state_match.group(0), 16)
        else:
            try:
                val = int(raw, 10)
            except ValueError:
                print(f"Error: Could not parse state token '{raw}'", file=sys.stderr)
                return 1

        info = explain_state(val)
        print("==================================================")
        print(f"HASE State Byte: {info['hex']} (Decimal: {info['val']})")
        print("==================================================")
        print("\nACTIVE CONSTRAINTS:")
        for p in info["active"]:
            print(f"  [x] {p['hex']} ({p['bit']:>3}) {p['name']:<24} -> {p['mandate']}")
        if not info["active"]:
            print("  (No constraints active)")

        print("\nINACTIVE PLANES:")
        for p in info["inactive"]:
            print(f"  [ ] {p['hex']} ({p['bit']:>3}) {p['name']:<24}")

        if info["requires_tests"]:
            print("\n[!] Mandate Alert: Bit 0x20 is ACTIVE. Companion unit tests are mandatory.")
        return 0

    elif args.command == "verify":
        target = args.target
        if os.path.exists(target):
            content = Path(target).read_text(encoding="utf-8")
        else:
            content = target

        valid, issues = verify_output(content)
        if valid:
            print("SUCCESS: Output is 100% compliant with HASE v7.0 protocol.")
            return 0
        else:
            print("VERIFICATION FAILED:")
            for issue in issues:
                print(f"  - {issue}")
            return 1

    elif args.command == "matrix":
        print("HASE v7.0 8-PLANE COGNITIVE MATRIX")
        print("-" * 80)
        print(f"{'Bit':<4} {'Hex':<6} {'Dec':<5} {'Plane Name':<25} {'Architectural Mandate'}")
        print("-" * 80)
        for i, (bit, _, name, mandate) in enumerate(PLANES):
            print(f"{i:<4} {format_hex_byte(bit):<6} {bit:<5} {name:<25} {mandate}")
        print("-" * 80)
        return 0

    elif args.command == "graph":
        target = Path(args.target).resolve()
        graph = build_ast_graph(target)

        if args.json:
            result = json.dumps(graph, indent=2)
        else:
            result = export_compact_graph(graph)

        if args.output:
            out_path = Path(args.output).resolve()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(result, encoding="utf-8")
            print(f"AST Codebase Graph generated ({graph['total_files']} files) -> {out_path}")
        else:
            print(result)
        return 0

    elif args.command == "memory":
        workspace = Path(".").resolve()
        action = args.mem_action or "list"

        if action == "list":
            mem = load_memory(workspace)
            print("==================================================")
            print("HASE WORKSPACE MEMORY LEDGER")
            print(f"Last updated: {mem.get('updated_at', 'never')}")
            print("==================================================")
            print("\nARCHITECTURAL INVARIANTS:")
            invariants = mem.get("invariants", [])
            if invariants:
                for idx, inv in enumerate(invariants, 1):
                    print(f"  {idx}. {inv}")
            else:
                print("  (None recorded)")

            print("\nRELEVANT FINDINGS:")
            findings = mem.get("findings", [])
            if findings:
                for f in findings:
                    files_str = f" [Files: {', '.join(f.get('files', []))}]" if f.get("files") else ""
                    print(f"  [{f['id']}] ({f['topic']}) {f['fact']}{files_str}")
            else:
                print("  (No findings stored)")
            return 0

        elif action == "add":
            entry = add_memory_finding(workspace, args.topic, args.fact, args.files)
            print(f"Recorded finding [{entry['id']}] under '{args.topic}'")
            return 0

        elif action == "invariant":
            inv = add_memory_invariant(workspace, args.rule)
            print(f"Recorded architectural invariant: '{inv}'")
            return 0

        elif action == "clear":
            clear_memory(workspace)
            print("Workspace memory cleared.")
            return 0

    elif args.command == "sync":
        target = Path(args.target).resolve()
        hase_dir = target / ".hase"
        hase_dir.mkdir(parents=True, exist_ok=True)
        mem = load_memory(target)
        save_memory(target, mem)
        graph = build_ast_graph(target)
        context_md = export_compact_graph(graph)
        out_path = hase_dir / "context.md"
        out_path.write_text(context_md, encoding="utf-8")
        print("HASE Sync Complete:")
        print(f"  -> AST Topology Graph: {out_path} ({graph['total_files']} files indexed)")
        print(f"  -> Memory Ledger: {get_memory_file(target)} ({len(mem.get('findings', []))} findings, {len(mem.get('invariants', []))} invariants)")
        return 0

    elif args.command == "init":
        repo_root = Path(__file__).resolve().parent.parent
        target_dir = Path(args.target).resolve()
        tool_list = [t.strip() for t in args.tools.split(",") if t.strip()]
        installed = install_rules(repo_root, target_dir, tool_list)
        print(f"Installed {len(installed)} HASE configuration files into: {target_dir}")
        for path in installed:
            print(f"  -> {path}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
