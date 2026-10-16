#!/usr/bin/env python3
"""Replay a hash-pinned Lean module closure into a new, isolated output tree.

This checker reads the supplied repository and contribution package only. It
checks historical Git provenance, exact import closure, forbidden proof tokens,
fresh kernel compilation, endpoint types, and every selected module theorem's
and safe definition's transitive axioms. Unrelated repository changes are recorded rather
than confused with changes to the exact selected source snapshot.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import traceback

ALLOWED = ["propext", "Classical.choice", "Quot.sound"]
NAME = re.compile(r"[A-Za-z_][\w]*(?:\.[A-Za-z_][\w]*)*\Z")
BANNED = re.compile(r"(?<![\w'])\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b(?![\w'])")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def code_only(text: str) -> str:
    result, i, depth, string = [], 0, 0, False
    while i < len(text):
        pair = text[i:i + 2]
        if depth:
            if pair == "/-":
                depth += 1; result.extend("  "); i += 2
            elif pair == "-/":
                depth -= 1; result.extend("  "); i += 2
            else:
                result.append("\n" if text[i] == "\n" else " "); i += 1
        elif string:
            if text[i] == "\\":
                result.extend("  "); i += 2
            else:
                string = text[i] != '"'; result.append("\n" if text[i] == "\n" else " "); i += 1
        elif pair == "/-":
            depth = 1; result.extend("  "); i += 2
        elif pair == "--":
            end = text.find("\n", i)
            end = len(text) if end < 0 else end
            result.extend(" " * (end - i)); i = end
        elif text[i] == '"':
            string = True; result.append(" "); i += 1
        else:
            result.append(text[i]); i += 1
    if depth or string:
        raise ValueError("Unterminated comment or string")
    return "".join(result)


def located(root: Path, relative: str) -> Path:
    path = root / relative
    if Path(relative).is_absolute() or not path.resolve().is_relative_to(root):
        raise ValueError("Source path escapes its declared root: " + relative)
    if path.is_symlink():
        raise ValueError("Symbolic-link source is not accepted: " + relative)
    return path


def audit_source(roots: list[str], modules: list[str], endpoints: list[str]) -> str:
    header = "\n".join("import " + m for m in roots)
    header += "\nimport Lean\nopen Lean Elab Command\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n"
    header += "\n".join("#check " + name for name in endpoints) + "\n"
    header += "run_cmd do\n  let env ← getEnv\n  let selected : List String := " + json.dumps(modules) + "\n"
    return header + """  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut definitionCount := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let origin := env.allImportedModuleNames[idx.toNat]!
      if selected.contains origin.toString then
        match info with
        | .axiomInfo value =>
          if value.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {origin} {name}"
          else
            throwError m!"CUSTOM_AXIOM {origin} {name}"
        | .thmInfo _ =>
          count := count + 1
          let dependencies ← liftCoreM (Lean.collectAxioms name)
          let axl := dependencies.toList
          for axiomName in axl do
            if !(allowed.contains axiomName) then
              throwError m!"DISALLOWED_AXIOM {origin} {name} {axiomName}"
            if !(union.contains axiomName) then
              union := axiomName :: union
          logInfo m!"AUDIT_THEOREM {origin} {name} : {axl}"
        | .defnInfo _ | .opaqueInfo _ =>
          if info.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_DEFINITION {origin} {name}"
          else
            definitionCount := definitionCount + 1
            let dependencies ← liftCoreM (Lean.collectAxioms name)
            let axl := dependencies.toList
            for axiomName in axl do
              if !(allowed.contains axiomName) then
                throwError m!"DISALLOWED_DEFINITION_AXIOM {origin} {name} {axiomName}"
              if !(union.contains axiomName) then
                union := axiomName :: union
            logInfo m!"AUDIT_DEFINITION {origin} {name} : {axl}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
  logInfo m!"FULL_DEFINITION_AUDIT definitions={definitionCount}"
"""


def main() -> int:
    default_package = Path(__file__).resolve().parents[3]
    default_repo = default_package.parents[3]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=default_repo)
    parser.add_argument("--package-root", type=Path, default=default_package)
    parser.add_argument("--manifest", type=Path, default=Path(__file__).resolve().parent / "source-registry.json")
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--auditor", default="Agent #9/horizon-safety independent interval review",
                        help="Truthful identity of the agent or person executing this replay")
    args = parser.parse_args()
    repo, package, lean, manifest_path, output = (p.resolve() for p in (args.repo, args.package_root, args.lean, args.manifest, args.output))
    output.mkdir(parents=True, exist_ok=False)
    source, build, logs = (output / name for name in ("source", "build", "logs"))
    for path in (source, build, logs):
        path.mkdir()
    report = {"auditor": args.auditor, "status": "RUNNING", "commands": [], "sources": {},
              "started_epoch": time.time(), "repository_wide_pass": False, "allowed_axioms": ALLOWED,
              "workflow_sha256": digest(Path(__file__).read_bytes()),
              "invocation": [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]],
              "output_directory_created_new": True, "precompile_object_count": len(list(build.rglob("*.olean"))),
              "lean_trust_level": 0}
    environment = {"PATH": str(lean.parent) + ":/usr/bin:/bin", "LANG": "C.UTF-8", "LEAN_PATH": str(build)}
    report["lean_environment"] = environment
    git_environment = dict(os.environ)
    git_environment["GIT_OPTIONAL_LOCKS"] = "0"

    def save() -> None:
        (output / "verification.json").write_text(json.dumps(report, indent=2) + "\n")

    def command(label: str, argv: list[str], cwd: Path = source, git: bool = False, timeout: int = 1800) -> bytes:
        logfile = logs / (label + ".log")
        start = time.monotonic()
        with logfile.open("wb") as stream:
            try:
                code = subprocess.run(argv, cwd=cwd, env=git_environment if git else environment,
                                      stdout=stream, stderr=subprocess.STDOUT, timeout=timeout).returncode
            except subprocess.TimeoutExpired:
                code = 124
        data = logfile.read_bytes()
        row = {"label": label, "argv": argv, "cwd": str(cwd), "exit_code": code,
               "elapsed_seconds": round(time.monotonic() - start, 6),
               "log": str(logfile.relative_to(output)), "log_sha256": digest(data)}
        report["commands"].append(row); save()
        print(f"{label}: exit={code}, seconds={row['elapsed_seconds']}", flush=True)
        if code:
            raise RuntimeError(f"Command {label} failed; inspect {logfile}")
        return data

    try:
        raw_manifest = manifest_path.read_bytes()
        manifest = json.loads(raw_manifest)
        if manifest["schema_version"] != 1:
            raise ValueError("Unsupported manifest schema")
        (output / "source-manifest.json").write_bytes(raw_manifest)
        report["manifest_sha256"] = digest(raw_manifest)
        report["project"] = manifest["project"]
        report["scope"] = manifest["scope"]
        report["new_modules"] = manifest.get("new_modules", [])
        report["repository_head_before"] = command("repository-head-before", ["git", "rev-parse", "HEAD"], repo, git=True).decode().strip()
        report["repository_status_before"] = command("repository-status-before", ["git", "status", "--porcelain"], repo, git=True).decode()
        version = command("lean-version", [str(lean), "--version"]).decode().strip()
        if not re.fullmatch(r"Lean \(version 4\.19\.0, .*, commit 6caaee842e94, Release\)", version):
            raise ValueError("Unexpected Lean toolchain: " + version)
        runtime = Path(command("lean-prefix", [str(lean), "--print-prefix"]).decode().strip()).resolve()
        runtime_files = sorted(set([lean, runtime / "lib/lean/Init.olean", runtime / "lib/lean/Std.olean", runtime / "lib/lean/Lean.olean",
                                    *list((runtime / "lib/lean").glob("*.so"))]))
        runtime_hashes = {str(p): digest(p.read_bytes()) for p in runtime_files}
        report["compiler"] = {"version": version, "runtime_root": str(runtime), "files": runtime_hashes}
        records = manifest["modules"]
        if not records or any(not NAME.fullmatch(name) for name in records):
            raise ValueError("Empty or invalid module registry")
        snapshots, imports, input_paths = {}, {}, {}
        for name, rec in records.items():
            scope_root = {"repository": repo, "package": package}[rec["base"]]
            path = located(scope_root, rec["path"])
            data = path.read_bytes()
            blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
            if digest(data) != rec["sha256"] or blob != rec["git_blob"]:
                raise ValueError("Source identity differs: " + name)
            provenance = rec.get("historical_provenance")
            if provenance:
                ref = provenance["commit"] + ":" + provenance["path"]
                original_blob = command(name + "-original-blob", ["git", "rev-parse", ref], repo, git=True).decode().strip()
                if original_blob != rec["git_blob"]:
                    raise ValueError("Historical commit/path differs: " + name)
                original_bytes = command(name + "-original-source", ["git", "cat-file", "blob", original_blob], repo, git=True)
                if original_bytes != data:
                    raise ValueError("Historical source bytes differ: " + name)
            code = code_only(data.decode())
            forbidden = BANNED.search(code)
            if forbidden:
                raise ValueError("Forbidden proof token in " + name + ": " + forbidden.group())
            dependencies = [dep for line in re.findall(r"^\s*import\s+([^\n]+)", code, re.M) for dep in line.split()]
            if dependencies != rec["imports"] or any(not NAME.fullmatch(dep) for dep in dependencies):
                raise ValueError("Import manifest mismatch: " + name)
            for dep in dependencies:
                if dep not in records:
                    if dep.split(".")[0] not in {"Lean", "Init", "Std"} or not (runtime / "lib/lean" / (dep.replace(".", "/") + ".olean")).is_file():
                        raise ValueError("Unregistered import: " + dep)
            destination = source / (name.replace(".", "/") + ".lean")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            snapshots[name], imports[name], input_paths[name] = data, dependencies, path
            report["sources"][name] = {**rec, "resolved_path": str(path), "build_sha256": digest(data)}
        roots = manifest["roots"]
        endpoints = manifest["endpoints"]
        if not roots or any(root not in records for root in roots) or not endpoints or any(not NAME.fullmatch(name) for name in endpoints):
            raise ValueError("Invalid root or endpoint list")
        order, visited, active = [], set(), set()

        def visit(name: str) -> None:
            if name not in records or name in visited:
                return
            if name in active:
                raise ValueError("Import cycle: " + name)
            active.add(name)
            for dep in imports[name]:
                visit(dep)
            active.remove(name); visited.add(name); order.append(name)

        for root in roots:
            visit(root)
        if visited != set(records):
            raise ValueError("Manifest modules do not exactly match the selected root closure")
        report["build_order"] = order
        report["roots"] = roots
        report["endpoints"] = endpoints
        save()
        for name in order:
            relative = name.replace(".", "/")
            target = build / (relative + ".olean")
            target.parent.mkdir(parents=True, exist_ok=True)
            command(name, [str(lean), "--trust=0", "-j1", "-DElab.async=false", "-o", str(target), relative + ".lean"])
        audit = audit_source(roots, order, endpoints)
        audit_path = source / "IntervalClosureAudit.lean"
        audit_path.write_text(audit)
        report["audit_source_sha256"] = digest(audit_path.read_bytes())
        audit_log = command("IntervalClosureAudit", [str(lean), "--trust=0", "-j1", "-DElab.async=false", "IntervalClosureAudit.lean"]).decode()
        totals = re.findall(r"^FULL_MODULE_AUDIT theorems=(\d+) union=(.+)$", audit_log, re.M)
        rows = re.findall(r"^AUDIT_THEOREM (\S+) (\S+) : (.*)$", audit_log, re.M)
        if len(totals) != 1 or int(totals[0][0]) != len(rows) or not rows or len({r[1] for r in rows}) != len(rows):
            raise ValueError("Incomplete or duplicate theorem audit")
        if any(row[0] not in records for row in rows):
            raise ValueError("Audit emitted an unexpected module")
        report["audited_theorem_count"] = len(rows)
        report["theorems_by_module"] = dict(sorted(Counter(row[0] for row in rows).items()))
        report["axiom_union"] = totals[0][1]
        report["unsafe_implementation_constants"] = re.findall(r"^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$", audit_log, re.M)
        definition_totals = re.findall(r"^FULL_DEFINITION_AUDIT definitions=(\d+)$", audit_log, re.M)
        definitions = re.findall(r"^AUDIT_DEFINITION (\S+) (\S+) : (.*)$", audit_log, re.M)
        if len(definition_totals) != 1 or int(definition_totals[0]) != len(definitions) or not definitions:
            raise ValueError("Incomplete definition audit")
        if len({row[1] for row in definitions}) != len(definitions) or any(row[0] not in records for row in definitions):
            raise ValueError("Duplicate or unexpected definition audit entry")
        report["audited_safe_definition_count"] = len(definitions)
        report["safe_definitions_by_module"] = dict(sorted(Counter(row[0] for row in definitions).items()))
        report["unsafe_implementation_definitions"] = re.findall(r"^UNSAFE_IMPLEMENTATION_DEFINITION (\S+) (\S+)$", audit_log, re.M)
        report["new_module_theorem_count"] = sum(row[0] in report["new_modules"] for row in rows)
        report["new_module_safe_definition_count"] = sum(row[0] in report["new_modules"] for row in definitions)
        for name, original in snapshots.items():
            if input_paths[name].read_bytes() != original or (source / (name.replace(".", "/") + ".lean")).read_bytes() != original:
                raise ValueError("Selected original or build source changed during replay: " + name)
        if manifest_path.read_bytes() != raw_manifest:
            raise ValueError("Manifest changed during replay")
        if {str(p): digest(p.read_bytes()) for p in runtime_files} != runtime_hashes:
            raise ValueError("Compiler snapshot changed during replay")
        report["all_selected_sources_unchanged"] = True
        report["compiler_snapshot_unchanged"] = True
        report["repository_head_after"] = command("repository-head-after", ["git", "rev-parse", "HEAD"], repo, git=True).decode().strip()
        report["repository_status_after"] = command("repository-status-after", ["git", "status", "--porcelain"], repo, git=True).decode()
        report["status"] = "PASS_SELECTED_SOURCE_CLOSURE"
        print(f"PASS_SELECTED_SOURCE_CLOSURE modules={len(order)} theorems={len(rows)} safe_definitions={len(definitions)}", flush=True)
        return 0
    except Exception as error:
        report["status"] = "FAIL"
        report["error"] = str(error)
        (output / "failure.txt").write_text(traceback.format_exc())
        print("FAIL:", error, flush=True)
        return 1
    finally:
        report["finished_epoch"] = time.time(); save()
        manifest = {str(path.relative_to(output)): {"bytes": path.stat().st_size, "sha256": digest(path.read_bytes())}
                    for path in sorted(output.rglob("*")) if path.is_file() and path.name != "FILES.json"}
        (output / "FILES.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
