#!/usr/bin/env python3
"""Fresh Lean 4.19.0 rebuild and transitive public-theorem axiom audit.

Use an unused --output-dir; existing evidence is never overwritten. The eleven
source modules are compiled from exact copies in a new temporary directory.
Only Python's standard library and the pinned Lean distribution are required.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
PRIOR = HERE.parent / "actual-high-return"
PREREQUISITE_MODULE_COUNT = 8
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
SOURCES = [
    REPO / "proofs/research/continuation/LychrelDigitSums.lean",
    REPO / "proofs/contributions/2026-10-15-high-carry-reduction-formal/HighCarryReduction.lean",
    REPO / "proofs/contributions/2026-10-15-high-return-rank-formal/HighReturnRank.lean",
    PRIOR / "NeutralExterior.lean",
    PRIOR / "HighReturnPrefix.lean",
    PRIOR / "SmallWidth.lean",
    PRIOR / "NumericHigh.lean",
    PRIOR / "ActualHighReturn.lean",
    HERE / "LocalHigh.lean",
    HERE / "ReturnCriterion.lean",
    HERE / "ReturnSafety.lean",
]
IDENT = r"(?:«[^»]+»|[\w']+)(?:\.(?:«[^»]+»|[\w']+))*"
DECL = re.compile(
    rf"^\s*(?:@\[[^\]]*\]\s*)*"
    rf"(?P<mod>(?:(?:private|protected|noncomputable|public)\s+)*)"
    rf"(?P<kind>theorem|lemma)\s+(?P<name>{IDENT})"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def code_only(source: str) -> str:
    """Blank nested comments and string literals while preserving line numbers."""
    out, i, depth, string = [], 0, 0, False
    while i < len(source):
        if depth:
            if source.startswith("/-", i):
                depth += 1
                out.extend("  ")
                i += 2
            elif source.startswith("-/", i):
                depth -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if source[i] == "\n" else " ")
                i += 1
        elif string:
            if source[i] == "\\" and i + 1 < len(source):
                out.extend("\n" if c == "\n" else " " for c in source[i:i + 2])
                i += 2
            else:
                string = source[i] != '"'
                out.append("\n" if source[i] == "\n" else " ")
                i += 1
        elif source.startswith("/-", i):
            depth = 1
            out.extend("  ")
            i += 2
        elif source.startswith("--", i):
            end = source.find("\n", i)
            end = len(source) if end < 0 else end
            out.extend(" " * (end - i))
            i = end
        elif source[i] == '"':
            string = True
            out.append(" ")
            i += 1
        else:
            out.append(source[i])
            i += 1
    if depth or string:
        raise ValueError("Unclosed comment or string")
    return "".join(out)


def public_theorems(source: str) -> list[dict]:
    """Resolve namespaces; fail closed on unsupported declaration formatting.

    This scanner intentionally supports the ordinary namespace/section/theorem
    syntax used by this package. A token census rejects silently missed theorem
    declarations, including multiline modifiers or declarations inside macros.
    Private helper theorems are omitted from #print targets; their dependencies
    are still checked transitively whenever used by a public theorem.
    """
    code = code_only(source)
    forbidden = re.findall(r"\b(?:sorry|admit|axiom|native_decide|sorryAx|ofReduceBool)\b", code)
    if forbidden:
        raise ValueError(f"Forbidden proof/axiom token(s): {sorted(set(forbidden))}")
    generators = re.findall(r"\b(?:macro|macro_rules|elab|elab_rules|syntax|run_cmd|run_meta)\b", code)
    if generators:
        raise ValueError(f"Declaration-generating syntax requires separate enumeration: {sorted(set(generators))}")
    scopes, found, declaration_count = [], [], 0
    for line_number, line in enumerate(code.splitlines(), 1):
        begin = re.match(rf"^\s*(namespace|section)(?:\s+({IDENT}))?\s*$", line)
        finish = re.match(rf"^\s*end(?:\s+({IDENT}))?\s*$", line)
        if begin:
            kind, label = begin.groups()
            if kind == "namespace" and not label:
                raise ValueError(f"Unnamed namespace on line {line_number}")
            scopes.append((kind, label))
        elif finish:
            if not scopes:
                raise ValueError(f"Unmatched end on line {line_number}")
            _, label = scopes.pop()
            if finish[1] and finish[1] != label:
                raise ValueError(f"Mismatched end on line {line_number}: {finish[1]} != {label}")
        declaration = DECL.match(line)
        if declaration:
            declaration_count += 1
            if "private" in declaration["mod"].split():
                continue
            prefix = ".".join(label for kind, label in scopes if kind == "namespace")
            name = declaration["name"]
            name = name[7:] if name.startswith("_root_.") else ".".join(filter(None, [prefix, name]))
            found.append({"name": name, "line": line_number, "kind": declaration["kind"]})
    if scopes:
        raise ValueError(f"Unclosed namespaces/sections: {scopes}")
    census = len(re.findall(rf"\b(?:theorem|lemma)\s+{IDENT}", code))
    if declaration_count != census:
        raise ValueError(f"Unsupported theorem syntax: recognized {declaration_count}, found {census}")
    if not found:
        raise ValueError("No public theorems found")
    return found


def git(*args: str) -> str | None:
    result = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def source_record(path: Path, data: bytes) -> dict:
    relative = str(path.relative_to(REPO))
    blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    head_blob = git("rev-parse", "--verify", f"HEAD:{relative}")
    return {
        "path": relative, "sha256": sha256(data), "bytes": len(data),
        "git_blob_sha1": blob, "head_blob_sha1": head_blob,
        "matches_head": blob == head_blob,
        "last_path_commit": git("log", "-1", "--format=%H", "--", relative),
        "public_theorems": public_theorems(data.decode("utf-8")),
    }


def audit_output(output: str, expected: list[str]) -> dict[str, list[str]]:
    audited = {}
    pattern = r"'(.+?)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)"
    for match in re.finditer(pattern, output, re.S):
        name = match[1]
        if name in audited:
            raise ValueError(f"Duplicate axiom audit for {name}")
        axioms = sorted(a.strip() for a in (match[2] or "").split(",") if a.strip())
        if not set(axioms) <= ALLOWED_AXIOMS:
            raise ValueError(f"Unapproved transitive axioms for {name}: {axioms}")
        audited[name] = axioms
    if set(audited) != set(expected):
        raise ValueError(f"Incomplete axiom audit: missing={sorted(set(expected)-set(audited))}, "
                         f"unexpected={sorted(set(audited)-set(expected))}")
    return audited


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lean", help="Lean 4.19.0 executable (absolute path recommended)")
    parser.add_argument("--output-dir", type=Path, help="New directory for this run's evidence")
    parser.add_argument("--timeout", type=float, default=1800,
                        help="Seconds per compiler invocation; 0 means unlimited (default: 1800)")
    args = parser.parse_args()
    if args.timeout < 0:
        parser.error("--timeout must be nonnegative")
    resolved = shutil.which(args.lean)
    if resolved is None:
        parser.error(f"Lean executable not found: {args.lean}")
    lean = str(Path(resolved).resolve())
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    out = (args.output_dir or HERE / "verification_runs" / f"{stamp}-{os.getpid()}").resolve()
    out.mkdir(parents=True, exist_ok=False)
    logs = out / "logs"
    logs.mkdir()
    report = {
        "status": "RUNNING", "started_utc": stamp,
        "checker_sha256": sha256(Path(__file__).read_bytes()),
        "git_head_at_start": git("rev-parse", "HEAD"),
        "compiler": {"path": lean, "sha256": sha256(Path(lean).read_bytes())},
        "allowed_axioms": sorted(ALLOWED_AXIOMS), "commands": [],
        "theorem_enumeration": "All explicit public theorem/lemma declarations in the eleven sources, "
                               "with namespaces resolved and a theorem-token census to reject omissions. "
                               "Declaration-generating macro/elaborator command tokens are rejected; "
                               "private helper dependencies are audited transitively.",
        "fresh_dependency_rebuild": False,
        "scope": "Fresh compilation of eleven sources, including eight prerequisite modules, "
                 "and transitive axiom audits of every explicit public theorem/lemma. For an "
                 "admissible high pair word, actual two-step high return is equivalent to "
                 "second-step no overflow, original exterior at least 14, and LocalAllowed "
                 "at every actual first-successor position with its determined carry sum. "
                 "For a canonically represented high starting integer, its first and second "
                 "positive outputs are both nonpalindromic exactly when some adjacent source "
                 "sum is at least 28, equivalently some actual first-successor pair coefficient "
                 "is at least 10. This safety equivalence needs no high-return assumption. "
                 "Positive widths including width one and overlapping reflected positions "
                 "are included. No assertion is made about starting-state or later-output "
                 "safety, decimal Lychrel existence, or the 196 conjecture; independent "
                 "mathematical review remains separate.",
    }
    initial: dict[Path, bytes] = {}
    env = dict(os.environ)
    env.pop("LEAN_PATH", None)
    preload = env.get("LD_PRELOAD", "")
    report["runtime_compatibility"] = {
        "LD_PRELOAD": preload,
        "files": [{"path": item, "sha256": sha256(Path(item).read_bytes())}
                  for item in re.split(r"[:\s]+", preload) if item and Path(item).is_file()],
        "LEAN_SYSROOT": env.get("LEAN_SYSROOT"),
    }

    def save() -> None:
        write_json(out / "verification.json", report)

    def run(label: str, command: list[str], cwd: Path, run_env: dict) -> str:
        index = len(report["commands"])
        log = logs / f"{index:02d}-{label}.log"
        record = {"label": label, "argv": command, "cwd": str(cwd),
                  "LEAN_PATH": run_env.get("LEAN_PATH"), "log": str(log.relative_to(out)),
                  "timeout_seconds": args.timeout}
        report["commands"].append(record)
        save()
        started = time.monotonic()
        output = ""
        try:
            process = subprocess.run(command, cwd=cwd, env=run_env, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, text=True,
                                     timeout=args.timeout or None)
            output = process.stdout
            record["exit_code"] = process.returncode
        except subprocess.TimeoutExpired as exc:
            raw = exc.stdout or ""
            output = raw.decode(errors="replace") if isinstance(raw, bytes) else raw
            record["exit_code"] = None
            record["timed_out"] = True
            raise RuntimeError(f"Timed out compiling {label}") from exc
        finally:
            record["seconds"] = round(time.monotonic() - started, 6)
            log.write_text(output)
            record["log_sha256"] = sha256(log.read_bytes())
            save()
        print(f"{label}: exit={process.returncode}, {record['seconds']:.3f}s", flush=True)
        if process.returncode:
            raise RuntimeError(f"Compiler failed for {label}; see {log}")
        return output

    try:
        initial = {path: path.read_bytes() for path in SOURCES}
        report["sources"] = [source_record(path, data) for path, data in initial.items()]
        expected = [entry["name"] for source in report["sources"] for entry in source["public_theorems"]]
        if len(set(expected)) != len(expected):
            raise ValueError("Duplicate public theorem names across sources")
        version = run("version", [lean, "--version"], out, env).strip()
        report["compiler"]["version"] = version
        if not re.search(r"\bversion 4\.19\.0(?:,|\s|\))", version):
            raise ValueError(f"Expected Lean 4.19.0: {version}")
        audit = "\n".join(f"import {path.stem}" for path in SOURCES) + "\n\n"
        audit += "\n".join(f"#print axioms {name}" for name in expected) + "\n"
        (out / "AllAxioms.lean").write_text(audit)
        report["generated_audit_sha256"] = sha256(audit.encode())
        report["compiled_objects"] = {}
        with tempfile.TemporaryDirectory(prefix="agent105-criterion-fresh-") as temp:
            build = Path(temp)
            if any(build.iterdir()):
                raise RuntimeError("Fresh build directory was not empty")
            build_env = dict(env, LEAN_PATH=str(build))
            report["build_directory"] = str(build)
            report["build_initially_empty"] = True
            for path, data in initial.items():
                (build / path.name).write_bytes(data)
            for path in SOURCES:
                target = build / f"{path.stem}.olean"
                if target.exists():
                    raise RuntimeError(f"Unexpected preexisting compiled object: {target}")
                run(path.stem, [lean, "-o", target.name, path.name], build, build_env)
                if not target.is_file():
                    raise RuntimeError(f"Compiler produced no object: {target}")
                report["compiled_objects"][target.name] = {"sha256": sha256(target.read_bytes()),
                                                          "bytes": target.stat().st_size}
            report["fresh_dependency_rebuild"] = True
            (build / "AllAxioms.lean").write_text(audit)
            output = run("AllAxioms", [lean, "AllAxioms.lean"], build, build_env)
            report["axiom_audit"] = audit_output(output, expected)
            for path, data in initial.items():
                if (build / path.name).read_bytes() != data:
                    raise RuntimeError(f"Build source changed during compilation: {path.name}")
        report["public_theorem_count"] = len(expected)
        report["public_theorem_counts"] = {Path(source["path"]).stem: len(source["public_theorems"])
                                            for source in report["sources"]}
        report["prerequisite_public_theorem_count"] = sum(
            len(source["public_theorems"]) for source in report["sources"][:PREREQUISITE_MODULE_COUNT])
        report["new_public_theorem_count"] = sum(
            len(source["public_theorems"]) for source in report["sources"][PREREQUISITE_MODULE_COUNT:])
        report["new_module_theorems"] = {
            Path(source["path"]).stem: [entry["name"] for entry in source["public_theorems"]]
            for source in report["sources"][PREREQUISITE_MODULE_COUNT:]}
        report["status"] = "PASS"
    except (Exception, KeyboardInterrupt) as exc:
        report["status"] = "INTERRUPTED" if isinstance(exc, KeyboardInterrupt) else "FAIL"
        report["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        after = {str(path.relative_to(REPO)): sha256(path.read_bytes()) if path.is_file() else None
                 for path in initial}
        report["source_sha256_after"] = after
        unchanged = all(after[str(path.relative_to(REPO))] == sha256(data) for path, data in initial.items())
        report["source_hashes_unchanged"] = unchanged
        if not unchanged:
            report["status"] = "FAIL"
            report["source_change_error"] = "Source changed during verification"
        report["git_head_at_finish"] = git("rev-parse", "HEAD")
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        try:
            combined = []
            for command in report["commands"]:
                combined.extend([json.dumps(command, sort_keys=True),
                                 (out / command["log"]).read_text() if "log_sha256" in command else "No completed log."])
            (out / "compile.log").write_text("\n\n".join(combined) + "\n")
        except Exception as exc:
            report["status"] = "FAIL"
            report["evidence_write_error"] = f"{type(exc).__name__}: {exc}"
        # Publish the final status only after all evidence writes succeed. Atomic
        # replacement prevents a partial JSON file from being mistaken for PASS.
        save()
    print(f"{report['status']}: {out / 'verification.json'}", flush=True)
    if report["status"] != "PASS":
        print(report.get("error", report.get("source_change_error", "Verification failed")), file=sys.stderr)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
