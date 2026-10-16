#!/usr/bin/env python3
"""Source-pinned author rebuild, not an independent-review claim.

Create an empty object directory, compile the complete import closure and
transitively audit every module-owned kernel-safe declaration. The environment
census method is adapted with attribution from Agent110's independent_rebuild.py;
this driver neither imports that driver nor reuses its compiled objects/results.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def code_only(text: str) -> str:
    """Remove nested comments and quoted strings, retaining line positions."""
    out: list[str] = []
    i = depth = 0
    quoted = False
    while i < len(text):
        if depth:
            if text.startswith("/-", i):
                depth += 1; out.append("  "); i += 2
            elif text.startswith("-/", i):
                depth -= 1; out.append("  "); i += 2
            else:
                out.append("\n" if text[i] == "\n" else " "); i += 1
        elif quoted:
            if text[i] == "\\" and i + 1 < len(text):
                out.append("  "); i += 2
            elif text[i] == '"':
                quoted = False; out.append(" "); i += 1
            else:
                out.append("\n" if text[i] == "\n" else " "); i += 1
        elif text.startswith("/-", i):
            depth = 1; out.append("  "); i += 2
        elif text.startswith("--", i):
            end = text.find("\n", i)
            if end < 0: end = len(text)
            out.append(" " * (end - i)); i = end
        elif text[i] == '"':
            quoted = True; out.append(" "); i += 1
        else:
            out.append(text[i]); i += 1
    if depth or quoted:
        raise ValueError("Unterminated Lean comment or string")
    return "".join(out)


def audit_source(modules: list[str], endpoints: list[str]) -> str:
    imports = "\n".join("import " + name for name in modules)
    names = ", ".join("`" + name for name in modules)
    targets = ", ".join("`" + name for name in endpoints)
    return imports + "\nimport Lean\nopen Lean Elab Command\n\nrun_cmd do\n" + (
        f"  let modules : Array Name := #[{names}]\n"
        f"  let endpoints : Array Name := #[{targets}]\n"
    ) + '''  let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
  let env ← getEnv
  for n in endpoints do
    match env.find? n with
    | none => throwError m!"MISSING_ENDPOINT|{n}"
    | some ci =>
        unless ci.isTheorem && !ci.isUnsafe do
          throwError m!"ENDPOINT_NOT_SAFE_THEOREM|{n}"
        logInfo m!"ENDPOINT|{n}|{ci.type}"
  let mut names : Array Name := #[]
  for (n, _) in env.constants do
    if let some idx := env.getModuleIdxFor? n then
      if modules.contains env.header.moduleNames[idx]! then
        names := names.push n
  let mut safeCount := 0
  let mut theoremCount := 0
  let mut unsafeCount := 0
  for n in names.qsort Name.lt do
    let ci := (env.find? n).get!
    let deps ← collectAxioms n
    if ci.isUnsafe then
      unsafeCount := unsafeCount + 1
      logInfo m!"UNSAFE_COMPILER_ARTIFACT|{n}|{deps.qsort Name.lt |>.toList}"
    else
      for ax in deps do
        unless allowed.contains ax do
          throwError m!"DISALLOWED_AXIOM|{n}|{ax}"
      let kind := if ci.isTheorem then "THEOREM" else "CONSTANT"
      if ci.isTheorem then theoremCount := theoremCount + 1
      safeCount := safeCount + 1
      logInfo m!"AUDIT|{kind}|{n}|{deps.qsort Name.lt |>.toList}"
  logInfo m!"AUDIT_TOTAL|{safeCount}|{theoremCount}|{unsafeCount}"
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path,
                        help="Must not already exist")
    parser.add_argument("--expected-commit", help="Require and verify this Git HEAD")
    args = parser.parse_args()
    repo, lean, output = args.repo.resolve(), args.lean.resolve(), args.output.resolve()
    here = Path(__file__).resolve().parent
    scope_bytes = (here / "SCOPE.json").read_bytes()
    scope = json.loads(scope_bytes)
    output.mkdir(parents=True, exist_ok=False)
    build = output / "objects"
    logs = output / "logs"
    build.mkdir(); logs.mkdir()
    env = os.environ.copy()
    for key in ("LEAN_PATH", "LEAN_SRC_PATH", "LEAN_SYSROOT", "LD_PRELOAD", "LD_LIBRARY_PATH"):
        env.pop(key, None)
    env["LEAN_PATH"] = str(build)
    result = {
        "status": "RUNNING", "agent": 112,
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "verification_level": "AUTHOR_CLEAN_REBUILD_NOT_INDEPENDENT_REVIEW",
        "driver_sha256": digest(Path(__file__).read_bytes()),
        "scope_sha256": digest(scope_bytes), "commands": [], "sources": [],
        "empty_research_object_directory": True, "research_objects_reused": False,
        "lean_binary_sha256": digest(lean.read_bytes()),
        "allowed_axioms": scope["allowed_axioms"],
        "scope": "Only the listed import closure; not a repository-wide PASS",
    }

    def save() -> None:
        (output / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    def run(label: str, argv: list[str]) -> str:
        logfile = logs / (label + ".log")
        started = time.monotonic()
        print("START", label, flush=True)
        with logfile.open("w") as stream:
            process = subprocess.run(argv, cwd=build, env=env, stdout=stream, stderr=subprocess.STDOUT)
        result["commands"].append({"label": label, "argv": argv, "exit_status": process.returncode,
                                   "seconds": round(time.monotonic() - started, 3),
                                   "log": str(logfile.relative_to(output)),
                                   "log_sha256": digest(logfile.read_bytes())})
        save()
        print("END", label, process.returncode, flush=True)
        if process.returncode:
            raise RuntimeError(f"{label} failed; see {logfile}")
        return logfile.read_text()

    try:
        git = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                             capture_output=True, text=True)
        head = git.stdout.strip() if git.returncode == 0 else None
        result["git_head"] = head
        result["source_mode"] = "GIT_HEAD_AND_HASH_PINNED" if head else "HASH_PINNED_ARCHIVE_NO_GIT_HEAD"
        if args.expected_commit and head != args.expected_commit:
            raise ValueError(f"Git HEAD mismatch: {head!r} != {args.expected_commit!r}")
        version = run("version", [str(lean), "--version"])
        if "version 4.19.0" not in version or "6caaee842e94" not in version:
            raise ValueError("Wrong Lean toolchain: " + version)
        result["lean_version"] = version.strip()
        mapping = {row["module"]: row for row in scope["sources"]}
        if len(mapping) != len(scope["sources"]):
            raise ValueError("Duplicate module in scope")
        order: list[str] = []
        visiting: set[str] = set()

        def visit(name: str) -> None:
            if name in order: return
            if name in visiting: raise ValueError("Import cycle: " + name)
            visiting.add(name)
            row = mapping[name]
            path = (repo / row["path"]).resolve()
            if not path.is_relative_to(repo): raise ValueError("Source outside repository")
            data = path.read_bytes()
            if digest(data) != row["sha256"] or blob_id(data) != row["git_blob_sha1"]:
                raise ValueError("Source hash mismatch: " + row["path"])
            if head:
                pin = subprocess.check_output(["git", "-C", str(repo), "rev-parse",
                                               head + ":" + row["path"]], text=True).strip()
                if pin != blob_id(data): raise ValueError("Source differs from Git HEAD: " + name)
            code = code_only(data.decode())
            bad = re.findall(r"\b(?:sorry|admit|axiom|native_decide|ofReduceBool|sorryAx|unsafe|partial)\b|debug\.skipKernelTC", code)
            if bad: raise ValueError(f"Forbidden source tokens in {name}: {bad}")
            deps = [x for line in re.findall(r"^import\s+([^\n]+)", code, re.M) for x in line.split()]
            for dep in deps:
                if dep in mapping: visit(dep)
                elif dep not in scope["core_imports"]: raise ValueError("Unmapped import: " + dep)
            (build / (name + ".lean")).write_bytes(data)
            result["sources"].append({**row, "imports": deps, "bytes": len(data),
                                      "git_blob_verified_at_head": head is not None})
            visiting.remove(name)
            order.append(name)

        visit(scope["root"])
        if set(order) != set(mapping): raise ValueError("Scope contains unreachable modules")
        result["build_order"] = order
        save()
        for name in order:
            run(name, [str(lean), "-j1", "-DElab.async=false", "-o", name + ".olean", name + ".lean"])
        audit = audit_source(order, scope["endpoints"])
        (build / "AuthorEnvironmentAudit.lean").write_text(audit)
        (output / "AuthorEnvironmentAudit.lean").write_text(audit)
        text = run("axioms", [str(lean), "-j1", "-DElab.async=false", "AuthorEnvironmentAudit.lean"])
        match = re.search(r"AUDIT_TOTAL\|(\d+)\|(\d+)\|(\d+)", text)
        if not match: raise ValueError("No complete audit footer")
        result["audit_counts"] = dict(zip(["kernel_safe_constants", "theorems", "unsafe_compiler_artifacts"],
                                         map(int, match.groups())))
        if len(re.findall(r"^ENDPOINT\|", text, re.M)) != len(scope["endpoints"]):
            raise ValueError("Incomplete endpoint census")
        result["status"] = "PASS"
        print("PASS", json.dumps(result["audit_counts"], sort_keys=True), flush=True)
        return 0
    except Exception as exc:
        result["status"] = "FAIL"
        result["error"] = f"{type(exc).__name__}: {exc}"
        print(result["error"], file=sys.stderr, flush=True)
        return 1
    finally:
        result["finished_utc"] = datetime.now(timezone.utc).isoformat()
        save()


if __name__ == "__main__":
    raise SystemExit(main())
