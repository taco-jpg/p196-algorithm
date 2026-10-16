#!/usr/bin/env python3
"""Independent exact-source verification of the published Agent115 update law.

Run using the supported execution escalation required by the pinned Lean
runtime. Every build directory must be new. This runner never changes the
five reviewed source files or Git metadata.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import traceback


BASE = Path(__file__).resolve().parent
SOURCE = BASE / "source"
LEAN = BASE.parent / "lean-4.19.0-linux/bin/lean"
OUT = BASE / "build"
ORDER = ["OuterFinite", "TARGET", "ExteriorFactorizationProof", "ExteriorObservationInjective", "ExteriorUpdateLaw"]
EXPECTED_IMPORTS = {"OuterFinite": ["Std"], "TARGET": ["OuterFinite"],
                    "ExteriorFactorizationProof": ["TARGET"],
                    "ExteriorObservationInjective": ["ExteriorFactorizationProof"],
                    "ExteriorUpdateLaw": ["ExteriorObservationInjective"]}
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    OUT.mkdir(exist_ok=False)
    obj, logs = OUT / "objects", OUT / "logs"
    obj.mkdir()
    logs.mkdir()
    manifest = json.loads((BASE / "source-manifest.json").read_text())
    report = {"reviewer": "Agent #6 runtime/reproducibility specialist",
              "source_commit": manifest["source_branch_commit"],
              "main_comparison_commit": manifest["main_comparison_commit"],
              "status": "RUNNING", "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "runner_sha256": digest(Path(__file__)), "source_manifest_sha256": digest(BASE / "source-manifest.json"),
              "fresh_project_objects": True, "source_repairs": [], "git_mutations": False,
              "build_order": ORDER, "commands": [], "modules": manifest["modules"]}

    def save() -> None:
        (OUT / "verification.json").write_text(json.dumps(report, indent=2) + "\n")

    def run(label: str, command: list[str], cwd: Path = SOURCE) -> str:
        start = time.monotonic()
        log = logs / (label + ".log")
        env = {"PATH": str(LEAN.parent) + ":/usr/bin:/bin", "LANG": "C.UTF-8", "LEAN_PATH": str(obj)}
        with log.open("wb") as stream:
            try:
                code = subprocess.run(command, cwd=cwd, env=env, stdout=stream,
                                      stderr=subprocess.STDOUT, timeout=900).returncode
            except subprocess.TimeoutExpired:
                code = 124
        report["commands"].append({"label": label, "argv": command, "cwd": str(cwd),
                                   "environment": env, "exit_code": code,
                                   "elapsed_seconds": round(time.monotonic() - start, 6),
                                   "log": str(log.relative_to(BASE)), "log_sha256": digest(log)})
        save()
        print(label, "exit=" + str(code), flush=True)
        if code:
            raise RuntimeError("Execution failed: " + label)
        return log.read_text()

    try:
        version = run("lean-version", [str(LEAN), "--version"]).strip()
        if version != "Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)":
            raise ValueError("Pinned toolchain version mismatch")
        prefix = Path(run("lean-prefix", [str(LEAN), "--print-prefix"]).strip())
        compiler_files = [LEAN, *sorted((prefix / "lib/lean").glob("*.so"))]
        compiler_hashes = {str(p): digest(p) for p in compiler_files}
        report["compiler"] = {"version": version, "prefix": str(prefix), "files": compiler_hashes,
                              "shim_used": False, "same_previously_verified_official_runtime": True}
        sys.dont_write_bytecode = True
        parser_path = BASE.parent / "source-snapshot/p196-algorithm-4b4edf976b2c7a9ba1dad80636c0e21c66350325/proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/verify_project.py"
        spec = importlib.util.spec_from_file_location("pinned_parser", parser_path)
        assert spec is not None and spec.loader is not None
        parser = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(parser)
        exports = {}
        for entry in manifest["modules"]:
            name = entry["module"]
            path = SOURCE / (name + ".lean")
            data = path.read_bytes()
            if digest(path) != entry["sha256"]:
                raise ValueError("Source SHA-256 mismatch: " + name)
            if hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() != entry["git_blob"]:
                raise ValueError("Source Git blob mismatch: " + name)
            code = parser.code_only(data.decode())
            if re.search(r"(?<![\w'])\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b(?![\w'])", code):
                raise ValueError("Forbidden token in reviewed source: " + name)
            imports = [d for line in re.findall(r"^\s*import\s+([^\n]+)", code, re.M) for d in line.split()]
            if imports != EXPECTED_IMPORTS[name]:
                raise ValueError("Import mismatch: " + name)
            namespaces = re.findall(r"^namespace\s+(\S+)", code, re.M)
            if len(namespaces) != 1:
                raise ValueError("Unexpected namespace structure: " + name)
            names = re.findall(r"^theorem\s+([A-Za-z_][\w']*)", code, re.M)
            if re.search(r"^(?:private|protected)\s+theorem", code, re.M):
                raise ValueError("Unexpected theorem visibility; revise reviewer inventory explicitly")
            exports[name] = [namespaces[0] + "." + n for n in names]
        report["explicit_exported_theorems"] = exports
        report["explicit_export_count"] = sum(map(len, exports.values()))
        flags = [str(LEAN), "--trust=0", "-j1", "-DElab.async=false"]
        for name in ORDER:
            run(name, flags + ["--root=" + str(SOURCE), "-o", str(obj / (name + ".olean")),
                               str(SOURCE / (name + ".lean"))])
        endpoints = ["Agent115.ExteriorFactorization.rawSucc_values",
                     "Agent115.ExteriorFactorization.successor_observation",
                     "Agent115.ExteriorFactorization.observation_injective",
                     "Agent115.ExteriorFactorization.target"]
        all_exports = [n for module in ORDER for n in exports[module]]
        audit_text = "import ExteriorUpdateLaw\nimport Lean\n\n" + "\n".join("#check " + n for n in endpoints) + "\n\n" + "\n".join("#print axioms " + n for n in all_exports) + "\n"
        (OUT / "ExportAxioms.lean").write_text(audit_text)
        text = run("ExportAxioms", flags + ["--root=" + str(OUT), str(OUT / "ExportAxioms.lean")], OUT)
        actual = {}
        for name, ax in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text):
            if name in actual:
                raise ValueError("Duplicate exported theorem audit: " + name)
            actual[name] = [s.strip() for s in ax.split(",") if s.strip()]
        for name in re.findall(r"'([^']+)' does not depend on any axioms", text):
            if name in actual:
                raise ValueError("Duplicate exported theorem audit: " + name)
            actual[name] = []
        if set(actual) != set(all_exports) or any(not set(v) <= ALLOWED for v in actual.values()):
            raise ValueError("Exported axiom audit is incomplete or contains excluded axioms")
        report["exported_axioms"] = actual
        (OUT / "exported-axioms.json").write_text(json.dumps(actual, indent=2) + "\n")
        module_audit = """import ExteriorUpdateLaw
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ["OuterFinite", "TARGET", "ExteriorFactorizationProof", "ExteriorObservationInjective", "ExteriorUpdateLaw"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
"""
        (OUT / "ModuleAudit.lean").write_text(module_audit)
        text = run("ModuleAudit", flags + ["--root=" + str(OUT), str(OUT / "ModuleAudit.lean")], OUT)
        declarations = re.findall(r"^AUDIT_THEOREM (\S+) (\S+) : (.*)$", text, re.M)
        summary = re.findall(r"^FULL_MODULE_AUDIT theorems=(\d+) union=(.*)$", text, re.M)
        if len(summary) != 1 or int(summary[0][0]) != len(declarations) or len({n for m, n, a in declarations}) != len(declarations):
            raise ValueError("Invalid full module audit accounting")
        audited_names = {n for m, n, a in declarations}
        if not set(all_exports) <= audited_names:
            raise ValueError("Module audit misses explicit theorem exports")
        report["all_theorem_constants_audited"] = len(declarations)
        report["theorem_constant_counts_by_module"] = {m: sum(n == m for n, _, _ in declarations) for m in ORDER}
        report["axiom_union"] = summary[0][1]
        report["unsafe_implementation_axioms"] = re.findall(r"^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$", text, re.M)
        for entry in manifest["modules"]:
            if digest(SOURCE / (entry["module"] + ".lean")) != entry["sha256"]:
                raise ValueError("Source changed during verification")
        for path, expected in compiler_hashes.items():
            if digest(Path(path)) != expected:
                raise ValueError("Compiler changed during verification")
        report["object_files"] = {str(p.relative_to(BASE)): {"bytes": p.stat().st_size, "sha256": digest(p)} for p in sorted(obj.glob("*.olean"))}
        report["status"] = "PASS"
        report["scope"] = "Independent clean compilation and theorem-axiom review of the five exact published dependency modules; no new theorem or global-orbit conclusion."
        return 0
    except Exception as error:
        report["status"] = "FAIL"
        report["error"] = str(error)
        (OUT / "failure.txt").write_text(traceback.format_exc())
        print("FAIL:", error, flush=True)
        return 1
    finally:
        report["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        save()
        inventory = {str(p.relative_to(BASE)): {"bytes": p.stat().st_size, "sha256": digest(p)}
                     for p in sorted(BASE.rglob("*")) if p.is_file() and p.suffix != ".olean" and p.name != "FILES.json"}
        (OUT / "FILES.json").write_text(json.dumps(inventory, indent=2) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
