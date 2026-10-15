#!/usr/bin/env python3
"""Pin-aware, bounded-worker, fresh Lean build and exhaustive theorem axiom audit.

Example:
  python3 check.py /absolute/path/to/lean --evidence /tmp/fresh-check \
    --pins review-clean/stable-pins.json --module TerminalObstruction \
    --module PalindromeBridge --module PrefixCertificate --module FastInverse

The evidence directory must not exist. All selected local imports are copied and
hashed before compilation; no pre-existing local .olean is imported. All theorem
constants belonging to those modules (including private/generated theorems) are
discovered from Lean's compiled environment and audited by actual #print axioms.
The exact base-source pin is mandatory. An optional pins file must cover the
entire selected local import closure exactly. No memory limit is imposed.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import threading
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
CORE = REPO / "proofs/research/continuation/LychrelDigitSums.lean"
CORE_PIN = "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
FORBIDDEN = re.compile(r"(?<![\w'])\b(?:sorry|admit|axiom|native_decide|sorryAx)\b(?![\w'])")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def code_only(text: str) -> str:
    """Mask nested Lean comments and strings, preserving line locations."""
    out, i, depth, string = [], 0, 0, False
    while i < len(text):
        pair = text[i:i + 2]
        if depth:
            if pair == "/-":
                depth += 1
                out.extend("  ")
                i += 2
            elif pair == "-/":
                depth -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
        elif string:
            if text[i] == "\\":
                out.extend("  ")
                i += 2
            else:
                string = text[i] != '"'
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
        elif pair == "/-":
            depth = 1
            out.extend("  ")
            i += 2
        elif pair == "--":
            end = text.find("\n", i)
            end = len(text) if end < 0 else end
            out.extend(" " * (end - i))
            i = end
        elif text[i] == '"':
            string = True
            out.append(" ")
            i += 1
        else:
            out.append(text[i])
            i += 1
    if depth or string:
        raise ValueError("Unterminated comment or string")
    return "".join(out)


def imports(source: str) -> list[str]:
    result = []
    for line in code_only(source).splitlines():
        match = re.match(r"^\s*import\s+(.+)$", line)
        if match:
            for module in match[1].split():
                if not re.fullmatch(r"[A-Za-z_][\w.]*(?:\.[\w]+)*", module):
                    raise ValueError(f"Unsupported import syntax: {line}")
                result.append(module)
    return result


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lean", help="Lean 4.19.0 binary or transparent wrapper")
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--module", action="append", default=[])
    parser.add_argument("--pins", type=Path)
    parser.add_argument("--jobs", type=int, choices=[1, 2], default=1)
    parser.add_argument("--require-committed", action="store_true")
    args = parser.parse_args()
    evidence = args.evidence.resolve()
    evidence.mkdir(parents=True, exist_ok=False)
    snapshot = evidence / "snapshot"
    snapshot.mkdir()
    logdir = evidence / "logs"
    logdir.mkdir()
    report_path = evidence / "verification.json"
    report = {
        "status": "IN_PROGRESS", "fresh_source_rebuild": True,
        "one_build_worker": args.jobs == 1, "parallel_build_workers": args.jobs, "async_elaboration": False,
        "memory_limit_imposed": False,
        "allowed_axioms": sorted(ALLOWED_AXIOMS),
        "sources": {}, "builds": [], "theorems": {},
        "numerical_739_instance_established_by_this_report": False,
        "scope": "Build and axiom validation only; mathematical interpretation requires theorem statements.",
    }
    report["source_commit"] = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    report["require_committed_sources"] = args.require_committed
    write_json(report_path, report)
    env = dict(os.environ)
    for key in ("LEAN_PATH", "LEAN_SRC_PATH", "LEAN_SYSROOT"):
        env.pop(key, None)
    env["LEAN_PATH"] = str(snapshot)

    report_lock = threading.Lock()

    def run(label: str, command: list[str]) -> str:
        log = logdir / f"{label}.log"
        resources = logdir / f"{label}.resources.json"
        started = time.monotonic()
        with log.open("w") as stream:
            proc = subprocess.Popen(command, cwd=snapshot, env=env,
                                    stdout=stream, stderr=subprocess.STDOUT)
            _, status, usage = os.wait4(proc.pid, 0)
            proc.returncode = os.waitstatus_to_exitcode(status)
        write_json(resources, {key: getattr(usage, key) for key in
                               ("ru_utime", "ru_stime", "ru_maxrss", "ru_minflt", "ru_majflt", "ru_nswap")})
        rec = {"label": label, "command": command, "cwd": str(snapshot),
               "exit_code": proc.returncode, "seconds": round(time.monotonic() - started, 3),
               "log": str(log.relative_to(evidence)), "log_sha256": sha(log),
               "resources": str(resources.relative_to(evidence))}
        rec["maximum_resident_set_kib"] = usage.ru_maxrss
        with report_lock:
            report["builds"].append(rec)
            write_json(report_path, report)
        print(json.dumps(rec), flush=True)
        if proc.returncode:
            raise RuntimeError(f"{label} failed with exit {proc.returncode}; see {log}")
        return log.read_text()

    try:
        lean = shutil.which(args.lean)
        if lean is None:
            raise ValueError(f"Lean executable unavailable: {args.lean}")
        lean = str(Path(lean).resolve())
        version = run("version", [lean, "--version"]).strip()
        if not re.search(r"version 4\.19\.0,.*commit 6caaee842e94, Release", version):
            raise ValueError(f"Wrong Lean version: {version}")
        prefix = Path(run("prefix", [lean, "--print-prefix"]).strip()).resolve()
        compiler_paths = [Path(lean), prefix / "bin/lean"]
        compiler_paths += sorted((prefix / "lib/lean").glob("*.so"))
        wrapper_dir = Path(lean).parent
        for name in ("proc-self-compat.c", "proc-self-compat.so"):
            if (wrapper_dir / name).exists():
                compiler_paths.append(wrapper_dir / name)
        report["compiler"] = {"version": version, "wrapper": lean,
                              "prefix": str(prefix),
                              "fingerprints": {str(p): sha(p) for p in compiler_paths},
                              "inherited_LD_PRELOAD": os.environ.get("LD_PRELOAD", "")}
        selected = args.module or sorted(p.stem for p in HERE.glob("*.lean"))
        if not selected:
            raise ValueError("No top-level modules selected")
        report["selected_top_level_modules"] = selected
        pending, order, active, blobs = list(selected), [], set(), {}

        def visit(module: str) -> None:
            if module in blobs:
                return
            if module in active:
                raise ValueError(f"Import cycle at {module}")
            active.add(module)
            path = CORE if module == "LychrelDigitSums" else HERE / (module.replace(".", "/") + ".lean")
            if not path.exists() and (HERE / "certificate" / (module + ".lean")).exists():
                path = HERE / "certificate" / (module + ".lean")
            if not path.exists():
                if (prefix / "lib/lean" / (module.replace(".", "/") + ".olean")).exists():
                    active.remove(module)
                    return
                raise ValueError(f"Unresolved source import: {module}")
            blob = path.read_bytes()
            text = blob.decode()
            forbidden = FORBIDDEN.findall(code_only(text))
            if forbidden:
                raise ValueError(f"Disallowed executable source tokens in {module}: {forbidden}")
            committed = subprocess.run(["git", "show", report["source_commit"] + ":" + str(path.relative_to(REPO))],
                                       cwd=REPO, capture_output=True)
            matches_commit = committed.returncode == 0 and committed.stdout == blob
            if args.require_committed and not matches_commit:
                raise ValueError(f"Source does not match pinned Git commit: {module}")
            source_imports = imports(text)
            for imported in source_imports:
                visit(imported)
            digest = hashlib.sha256(blob).hexdigest()
            if module == "LychrelDigitSums" and digest != CORE_PIN:
                raise ValueError(f"Pinned core SHA mismatch: {digest}")
            blobs[module] = blob
            dest = snapshot / (module.replace(".", "/") + ".lean")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(blob)
            report["sources"][module] = {
                "original_path": str(path.relative_to(REPO)), "sha256": digest,
                "git_blob_sha1": hashlib.sha1(f"blob {len(blob)}\0".encode() + blob).hexdigest(),
                "bytes": len(blob), "imports": source_imports, "matches_source_commit": matches_commit,
                "snapshot": str(dest.relative_to(evidence)),
            }
            active.remove(module)
            order.append(module)

        for module in pending:
            visit(module)
        current_pins = {m: rec["sha256"] for m, rec in report["sources"].items()}
        write_json(evidence / "source-pins.json", current_pins)
        if args.pins:
            pins = json.loads(args.pins.read_text())
            if pins != current_pins:
                raise ValueError(f"Pins mismatch: expected {pins}; snapshot {current_pins}")
            report["external_pins_file"] = str(args.pins.resolve())
            report["external_pins_sha256"] = sha(args.pins)
        report["build_order"] = order
        report["snapshot_complete_before_build"] = True
        write_json(report_path, report)
        remaining, completed = set(order), set()
        active_builds = {}
        local_dependencies = {m: set(report["sources"][m]["imports"]) & set(order) for m in order}
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            while remaining or active_builds:
                ready = [m for m in order if m in remaining and local_dependencies[m] <= completed]
                for module in ready[:args.jobs - len(active_builds)]:
                    relative = module.replace(".", "/")
                    future = pool.submit(run, module,
                        [lean, "-j1", "-DElab.async=false", "-o", relative + ".olean", relative + ".lean"])
                    active_builds[future] = module
                    remaining.remove(module)
                if not active_builds:
                    raise RuntimeError("No buildable module in import graph")
                finished, _ = wait(active_builds, return_when=FIRST_COMPLETED)
                for future in finished:
                    module = active_builds.pop(future)
                    future.result()
                    completed.add(module)
                    with report_lock:
                        report["sources"][module]["object_sha256"] = sha(snapshot / (module.replace(".", "/") + ".olean"))
                        write_json(report_path, report)

        module_strings = ", ".join(json.dumps(m) for m in order)
        audit_text = "\n".join("import " + m for m in selected) + '''
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := [''' + module_strings + ''']
  for mod in env.allImportedModuleNames do
    logInfo m!"AUDIT_IMPORT {mod}"
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else
            throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          logInfo m!"AUDIT_THEOREM {mod} {name}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | _ => pure ()
'''
        audit_path = snapshot / "AllExportedAxioms.lean"
        audit_path.write_text(audit_text)
        report["audit_source_sha256"] = sha(audit_path)
        output = run("AllExportedAxioms", [lean, "-j1", "-DElab.async=false", "AllExportedAxioms.lean"])
        declarations = re.findall(r"^AUDIT_THEOREM (\S+) (\S+)$", output, re.MULTILINE)
        names = {name: module for module, name in declarations}
        if len(names) != len(declarations) or not names:
            raise ValueError("Empty or duplicate compiled theorem inventory")
        audited = {}
        for name, axioms in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", output):
            audited[name] = sorted(a.strip() for a in axioms.split(",") if a.strip())
        for name in re.findall(r"'([^']+)' does not depend on any axioms", output):
            audited[name] = []
        if set(audited) != set(names):
            raise ValueError(f"Incomplete axiom audit: missing {set(names) - set(audited)}; extra {set(audited) - set(names)}")
        for name, axioms in audited.items():
            if not set(axioms) <= ALLOWED_AXIOMS:
                raise ValueError(f"Disallowed transitive axioms: {name}: {axioms}")
        report["unsafe_implementation_axioms"] = re.findall(r"^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$", output, re.MULTILINE)
        report["theorems"] = {name: {"module": names[name], "axioms": audited[name]}
                              for name in sorted(names)}
        report["theorem_count"] = len(names)
        report["theorems_per_module"] = {m: sum(x == m for x in names.values()) for m in order}
        imported_modules = sorted(set(re.findall(r"^AUDIT_IMPORT (\S+)$", output, re.MULTILINE)))
        report["imported_object_fingerprints"] = {}
        for module in imported_modules:
            obj = snapshot / (module.replace(".", "/") + ".olean")
            if not obj.exists():
                obj = prefix / "lib/lean" / (module.replace(".", "/") + ".olean")
            if not obj.exists():
                raise ValueError(f"Cannot fingerprint imported object {module}")
            report["imported_object_fingerprints"][module] = {"path": str(obj), "sha256": sha(obj)}
        for module, rec in report["sources"].items():
            if sha(evidence / rec["snapshot"]) != rec["sha256"]:
                raise ValueError(f"Snapshot changed during build: {module}")
        report["originals_unchanged_at_completion"] = all(
            sha(REPO / rec["original_path"]) == rec["sha256"] for rec in report["sources"].values())
        for path, digest in report["compiler"]["fingerprints"].items():
            if sha(Path(path)) != digest:
                raise ValueError(f"Compiler artifact changed during build: {path}")
        report["status"] = "PASS"
        write_json(report_path, report)
        print(f"PASS: {len(order)} freshly compiled source modules; {len(names)} theorem constants audited", flush=True)
        return 0
    except Exception as exc:
        report["status"] = "FAIL"
        report["failure"] = str(exc)
        write_json(report_path, report)
        print(f"FAIL: {exc}", file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
