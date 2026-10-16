#!/usr/bin/env python3
"""Independent clean review of Agent #6's exact CoordinateThreshold snapshot.

No source repair, Git mutation, or dependency object reuse is performed.
Execute with the supported sandbox escalation required by the pinned runtime.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import json
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
ORDER = ["OuterFinite", "TARGET", "ExteriorFactorizationProof", "CoordinateThreshold"]
EXPECTED_IMPORTS = {
    "OuterFinite": ["Std"], "TARGET": ["OuterFinite"],
    "ExteriorFactorizationProof": ["TARGET"],
    "CoordinateThreshold": ["ExteriorFactorizationProof"],
}
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    OUT.mkdir(exist_ok=False)
    objects, logs = OUT / "objects", OUT / "logs"
    objects.mkdir()
    logs.mkdir()
    manifest = json.loads((BASE / "source-manifest.json").read_text())
    live_source = Path(manifest["original_source"])
    report = {
        "reviewer": "Agent #6 runtime/reproducibility specialist",
        "review_type": "independent_new_root_review",
        "source_commit": manifest["source_branch_commit"],
        "main_comparison_commit": manifest["main_comparison_commit"],
        "status": "RUNNING", "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "runner_sha256": digest(Path(__file__)),
        "source_manifest_sha256": digest(BASE / "source-manifest.json"),
        "fresh_project_objects": True, "reused_dependency_objects": False,
        "source_repairs": [], "git_mutations": False,
        "original_source": str(live_source),
        "original_source_sha256_snapshot": manifest["original_source_sha256_before"],
        "build_order": ORDER, "commands": [], "modules": manifest["modules"],
    }

    def save() -> None:
        (OUT / "verification.json").write_text(json.dumps(report, indent=2) + "\n")

    def run(label: str, command: list[str], cwd: Path = SOURCE) -> str:
        start = time.monotonic()
        log = logs / (label + ".log")
        env = {"PATH": str(LEAN.parent) + ":/usr/bin:/bin", "LANG": "C.UTF-8", "LEAN_PATH": str(objects)}
        with log.open("wb") as stream:
            try:
                code = subprocess.run(command, cwd=cwd, env=env, stdout=stream,
                                      stderr=subprocess.STDOUT, timeout=900).returncode
            except subprocess.TimeoutExpired:
                code = 124
        report["commands"].append({
            "label": label, "argv": command, "cwd": str(cwd), "environment": env,
            "exit_code": code, "elapsed_seconds": round(time.monotonic() - start, 6),
            "log": str(log.relative_to(BASE)), "log_sha256": digest(log),
        })
        save()
        print(label, "exit=" + str(code), flush=True)
        if code:
            raise RuntimeError("Execution failed: " + label)
        return log.read_text()

    try:
        report["original_source_sha256_before_build"] = digest(live_source)
        if digest(live_source) != manifest["original_source_sha256_before"]:
            raise ValueError("Original source changed after snapshot")
        version = run("lean-version", [str(LEAN), "--version"]).strip()
        if version != "Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)":
            raise ValueError("Pinned toolchain version mismatch")
        prefix = Path(run("lean-prefix", [str(LEAN), "--print-prefix"]).strip())
        compiler_files = [LEAN, *sorted((prefix / "lib/lean").glob("*.so"))]
        compiler_hashes = {str(p): digest(p) for p in compiler_files}
        report["compiler"] = {
            "version": version, "prefix": str(prefix), "files": compiler_hashes,
            "shim_used": False, "same_previously_verified_official_runtime": True,
        }
        sys.dont_write_bytecode = True
        parser_path = BASE.parent / "source-snapshot/p196-algorithm-4b4edf976b2c7a9ba1dad80636c0e21c66350325/proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/verify_project.py"
        spec = importlib.util.spec_from_file_location("pinned_parser", parser_path)
        assert spec is not None and spec.loader is not None
        parser = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(parser)
        report["source_parser"] = {"path": str(parser_path), "sha256": digest(parser_path)}
        exports, declarations = {}, {}
        for entry in manifest["modules"]:
            name = entry["module"]
            path = SOURCE / (name + ".lean")
            data = path.read_bytes()
            if digest(path) != entry["sha256"]:
                raise ValueError("Source SHA-256 mismatch: " + name)
            if hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() != entry["git_blob"]:
                raise ValueError("Source Git blob mismatch: " + name)
            code = parser.code_only(data.decode())
            if re.search(r"(?<![\w'])\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC|unsafe)\b(?![\w'])", code):
                raise ValueError("Forbidden token in reviewed source: " + name)
            imports = [d for line in re.findall(r"^\s*import\s+([^\n]+)", code, re.M) for d in line.split()]
            if imports != EXPECTED_IMPORTS[name]:
                raise ValueError("Import mismatch: " + name)
            namespaces = re.findall(r"^namespace\s+(\S+)", code, re.M)
            if len(namespaces) != 1:
                raise ValueError("Unexpected namespace structure: " + name)
            if re.search(r"^(?:private|protected|noncomputable|opaque|abbrev|instance|inductive)\b", code, re.M):
                raise ValueError("Unexpected declaration syntax; explicitly revise reviewer inventory")
            names = re.findall(r"^(theorem|def|structure)\s+([A-Za-z_][\w']*)", code, re.M)
            declarations[name] = [{"kind": k, "name": namespaces[0] + "." + n} for k, n in names]
            exports[name] = [namespaces[0] + "." + n for k, n in names if k == "theorem"]
        if [len(exports[m]) for m in ORDER] != [3, 0, 26, 16]:
            raise ValueError("Unexpected explicit theorem counts")
        if len(declarations["CoordinateThreshold"]) != 19:
            raise ValueError("Unexpected new-root public declaration count")
        report["explicit_exported_theorems"] = exports
        report["explicit_export_count"] = sum(map(len, exports.values()))
        report["explicit_declarations"] = declarations
        report["explicit_declaration_count"] = sum(map(len, declarations.values()))
        flags = [str(LEAN), "--trust=0", "-j1", "-DElab.async=false"]
        for name in ORDER:
            run(name, flags + ["--root=" + str(SOURCE), "-o", str(objects / (name + ".olean")),
                               str(SOURCE / (name + ".lean"))])
        all_exports = [n for module in ORDER for n in exports[module]]
        all_declarations = [d["name"] for module in ORDER for d in declarations[module]]
        audit_text = "import CoordinateThreshold\nimport Lean\nset_option pp.universes true\n\n"
        audit_text += "\n".join("#check " + n for n in all_declarations) + "\n\n"
        audit_text += "\n".join("#print axioms " + n for n in all_declarations) + "\n"
        (OUT / "ExportAxioms.lean").write_text(audit_text)
        text = run("ExportAxioms", flags + ["--root=" + str(OUT), str(OUT / "ExportAxioms.lean")], OUT)
        actual = {}
        for name, ax in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text):
            if name in actual:
                raise ValueError("Duplicate exported declaration audit: " + name)
            actual[name] = [s.strip() for s in ax.split(",") if s.strip()]
        for name in re.findall(r"'([^']+)' does not depend on any axioms", text):
            if name in actual:
                raise ValueError("Duplicate exported declaration audit: " + name)
            actual[name] = []
        if set(actual) != set(all_declarations) or any(not set(v) <= ALLOWED for v in actual.values()):
            raise ValueError("Exported declaration audit is incomplete or contains excluded axioms")
        report["exported_axioms"] = {n: actual[n] for n in all_exports}
        report["all_explicit_declaration_axioms"] = actual
        (OUT / "exported-axioms.json").write_text(json.dumps(actual, indent=2) + "\n")
        module_audit = '''import CoordinateThreshold
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ["OuterFinite", "TARGET", "ExteriorFactorizationProof", "CoordinateThreshold"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  for mod in selected do
    if !(env.allImportedModuleNames.toList.any (fun n => n.toString == mod)) then
      throwError m!"MISSING_PROJECT_MODULE {mod}"
    logInfo m!"AUDIT_MODULE {mod}"
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        let kind := match info with
          | .axiomInfo _ => "axiom"
          | .thmInfo _ => "theorem"
          | .defnInfo _ => "definition"
          | .opaqueInfo _ => "opaque"
          | .quotInfo _ => "quotient"
          | .inductInfo _ => "inductive"
          | .ctorInfo _ => "constructor"
          | .recInfo _ => "recursor"
        logInfo m!"AUDIT_CONSTANT {mod} {kind} {name}"
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
'''
        (OUT / "ModuleAudit.lean").write_text(module_audit)
        text = run("ModuleAudit", flags + ["--root=" + str(OUT), str(OUT / "ModuleAudit.lean")], OUT)
        audited = re.findall(r"^AUDIT_THEOREM (\S+) (\S+) : (.*)$", text, re.M)
        constants = re.findall(r"^AUDIT_CONSTANT (\S+) (\S+) (\S+)$", text, re.M)
        modules = re.findall(r"^AUDIT_MODULE (\S+)$", text, re.M)
        summary = re.findall(r"^FULL_MODULE_AUDIT theorems=(\d+) union=(.*)$", text, re.M)
        if len(summary) != 1 or int(summary[0][0]) != len(audited) or len({n for m, n, a in audited}) != len(audited):
            raise ValueError("Invalid full module theorem accounting")
        if modules != ORDER or len({n for m, k, n in constants}) != len(constants):
            raise ValueError("Invalid full module constant accounting")
        if not set(all_exports) <= {n for m, n, a in audited}:
            raise ValueError("Module audit misses explicit theorem exports")
        if not set(all_declarations) <= {n for m, k, n in constants}:
            raise ValueError("Module audit misses explicit declarations")
        origins = {n: m for m, k, n in constants}
        for module in ORDER:
            if any(origins[d["name"]] != module for d in declarations[module]):
                raise ValueError("Exported declaration has unexpected module origin")
        report["all_theorem_constants_audited"] = len(audited)
        report["theorem_constant_counts_by_module"] = dict(Counter(m for m, n, a in audited))
        report["module_constant_count"] = len(constants)
        report["module_constant_counts_by_kind"] = {m: dict(Counter(k for mo, k, n in constants if mo == m)) for m in ORDER}
        report["module_origins"] = origins
        report["axiom_union"] = summary[0][1]
        report["unsafe_implementation_axioms"] = re.findall(r"^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$", text, re.M)
        for entry in manifest["modules"]:
            if digest(SOURCE / (entry["module"] + ".lean")) != entry["sha256"]:
                raise ValueError("Staged source changed during verification")
        for path, expected in compiler_hashes.items():
            if digest(Path(path)) != expected:
                raise ValueError("Compiler changed during verification")
        report["original_source_sha256_after_build"] = digest(live_source)
        if digest(live_source) != manifest["original_source_sha256_before"]:
            raise ValueError("Original source changed during verification")
        report["source_unchanged_before_after"] = True
        report["object_files"] = {str(p.relative_to(BASE)): {"bytes": p.stat().st_size, "sha256": digest(p)} for p in sorted(objects.glob("*.olean"))}
        if len(report["object_files"]) != len(ORDER):
            raise ValueError("Unexpected object inventory")
        report["status"] = "PASS"
        report["scope"] = "Independent clean compilation of a new four-module closure, explicit declaration axioms, and all theorem constants selected by imported module origin. Counts distinguish new authored exports, existing dependencies, and generated constants. Semantic scope is documented separately."
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
