#!/usr/bin/env python3
"""Agent #2: replay PR140's exact thirteen-module closure and scoped audits.

Inputs are authoritative source snapshots, not a complete repository checkout.
The executable audit traverses project declarations and records the pinned
standard-library boundary. It is not a global runtime or complexity audit.
Every output directory is new; prior attempts and logs are never overwritten.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import time
import traceback

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "source"
HEAD = "1c1bff874c915d90d2820090e028b40002145375"
BASE = "74a1c3922eb7af438fe40b23d2105ad07556e3f5"
PREFIX = "proofs/contributions/agent-102/affine-parameter-intervals-20261016/"
PROJECT = "agent102-affine-parameter-intervals"
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
LEAN_SHA256 = "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023"
EXECUTABLE_ROOTS = [
    "Agent102.ParameterSets.CountExpr.pieces",
    "Agent102.ParameterSets.comparisonRegion",
    "Agent102.ParameterSets.ltRegion",
    "Agent102.ParameterSets.leRegion",
    "Agent102.ParameterSets.eqRegion",
    "Agent102.ParameterSets.equalityRegions",
    "Agent102.ParameterSets.palindromeRegions",
    "Agent102.ParameterSets.equivalentRegions",
    "Agent102.ParameterSets.hasEqualParameter",
    "Agent102.ParameterSets.hasUnequalParameter",
    "Agent102.ParameterSets.everyParameterEqual",
    "Agent102.ParameterSets.everyParameterUnequal",
    "Agent102.ParameterSets.hasPalindromicParameter",
    "Agent102.ParameterSets.hasNonpalindromicParameter",
    "Agent102.ParameterSets.everyParameterPalindromic",
    "Agent102.ParameterSets.everyParameterNonpalindromic",
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def main() -> int:
    if not __debug__:
        raise RuntimeError("Python optimization disables verification assertions; run without -O and without PYTHONOPTIMIZE.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    build, logs = out / "build", out / "logs"
    build.mkdir()
    logs.mkdir()
    lean = args.lean.resolve()
    report = {
        "agent": "Agent #2", "session": "acfe54025bfc",
        "source_head": HEAD, "observed_main_base": BASE,
        "source_kind": "exact-commit source snapshot; not a full repository checkout",
        "status": "PREPARING", "started_at_epoch": time.time(),
        "commands": [], "source_files": {}, "build_started_empty": True,
        "delivery_owner": "Agent #29/session1f13321af678",
        "combined_reviewer": "Agent #11/sessionc68b",
        "source_owner": "Agent #102", "main_write_slot": False,
        "repository_wide_pass": False,
        "scope": "13-module build, 140 literal reports, full module-origin audit, 16 project executable roots",
    }

    def save() -> None:
        write_json(out / "verification.json", report)

    def run(label: str, command: list[str], cwd: Path = build) -> str:
        start = time.monotonic()
        log = logs / (label + ".log")
        # No credentials, repository auth, prior project search paths, or shell.
        env = {"PATH": str(lean.parent) + ":/usr/bin:/bin", "LANG": "C.UTF-8", "LEAN_PATH": str(build)}
        with log.open("wb") as stream:
            try:
                result = subprocess.run(command, cwd=cwd, env=env, stdout=stream,
                                        stderr=subprocess.STDOUT, timeout=180)
                rc = result.returncode
            except subprocess.TimeoutExpired:
                rc = 124
        report["commands"].append({"label": label, "argv": command,
            "cwd": str(cwd), "environment": env, "exit_code": rc,
            "elapsed_seconds": round(time.monotonic() - start, 6),
            "log": str(log.relative_to(out)), "log_sha256": sha256(log.read_bytes())})
        save()
        print(label + " exit=" + str(rc), flush=True)
        if rc:
            raise RuntimeError("Command failed: " + label + "; see retained log")
        return log.read_text()

    try:
        registry_path = SOURCE / "proofs/Agent102ParameterSets.registry.json"
        registry_bytes = registry_path.read_bytes()
        registry = json.loads(registry_bytes)
        assert registry["schema_version"] == 1
        assert registry["toolchain"]["version"] == "4.19.0"
        assert set(registry["toolchain"]["allowed_axioms"]) == ALLOWED
        report["registry"] = {"path": str(registry_path.relative_to(SOURCE)),
                              "sha256": sha256(registry_bytes), "git_blob": blob(registry_bytes)}
        (out / "Agent102ParameterSets.registry.json").write_bytes(registry_bytes)
        spec = registry["projects"][PROJECT]
        modules = spec["modules"]
        assert len(modules) == 13
        expected = [n for claim in registry["claims"] if claim["project"] == PROJECT
                    for n in claim["endpoints"]] + registry["literal_audit_extra_endpoints"]
        assert len(expected) == len(set(expected)) == 140
        report["expected_literal_endpoints"] = expected
        report["selected_modules"] = list(modules)
        report["executable_roots"] = EXECUTABLE_ROOTS
        report["executable_scope_boundary"] = "Selected project declaration types and bodies; external Std/Init/Lean declarations are recorded frontier nodes, not recursively audited runtime code. Arbitrary comparisonRegion callback implementations are outside this check."
        helper_path = SOURCE / "proofs/verify_project__214bf7673efe116b.py"
        helper_spec = importlib.util.spec_from_file_location("inspected_source_parser", helper_path)
        helper = importlib.util.module_from_spec(helper_spec)
        helper_spec.loader.exec_module(helper)
        originals = {}
        for name, record in modules.items():
            assert re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name)
            path = (SOURCE / record["path"]).resolve()
            assert path.is_relative_to(SOURCE.resolve())
            body = path.read_bytes()
            assert sha256(body) == record["sha256"], name + " SHA256 mismatch"
            assert blob(body) == record["git_blob"], name + " Git blob mismatch"
            code = helper.code_only(body.decode())
            assert not re.search(r"\b(sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC|unsafe|initialize|run_cmd|extern|implemented_by)\b|#eval", code), name + " prohibited source command"
            imports = re.findall(r"^\s*import\s+(\S+)\s*$", code, re.M)
            assert imports == record["imports"], name + " imports mismatch"
            originals[name] = body
            (build / (name + ".lean")).write_bytes(body)
            report["source_files"][name] = {"path": record["path"], "bytes": len(body),
                "sha256": sha256(body), "git_blob": blob(body), "imports": imports,
                "source_url": "https://raw.githubusercontent.com/taco-jpg/p196-algorithm/" + HEAD + "/" + record["path"]}
        order, active, seen = [], set(), set()
        def visit(name: str) -> None:
            if name not in modules:
                assert name in {"Std", "Init", "Lean"}
                return
            assert name not in active, "import cycle"
            if name in seen:
                return
            active.add(name)
            for dependency in modules[name]["imports"]:
                visit(dependency)
            active.remove(name)
            seen.add(name)
            order.append(name)
        for root in spec["roots"]:
            visit(root)
        assert seen == set(modules)
        report["build_order"] = order
        literal = (SOURCE / (PREFIX + "audit/LiteralAudit.lean")).read_bytes()
        literal_names = re.findall(r"^#print axioms (\S+)\s*$", literal.decode(), re.M)
        assert len(literal_names) == len(set(literal_names)) == 140
        assert set(literal_names) == set(expected)
        (build / "LiteralAudit.lean").write_bytes(literal)
        selection = json.dumps(list(modules))
        module_check = "\n  for wanted in selected do\n    if !(env.allImportedModuleNames.any (fun n => n.toString == wanted)) then\n      throwError m!\"MISSING_SELECTED_MODULE {wanted}\"\n"
        for audit_name in ["ModuleOriginAudit", "ExecutableDependencyAudit"]:
            original = (SOURCE / (PREFIX + "independent-piecewise/final-001/source/" + audit_name + ".lean")).read_text()
            audit = original.replace("import ReviewerControls\n", "import Agent102ParameterSetControls\n")
            audit, replaced = re.subn(r"  let selected : List String := \[[^\n]*\]", "  let selected : List String := " + selection + module_check, audit)
            assert replaced == 1
            if audit_name == "ExecutableDependencyAudit":
                root_list = ",\n      ".join("``" + name for name in EXECUTABLE_ROOTS)
                audit, replaced = re.subn(r"  for root in \[.*?\] do", "  for root in [" + root_list + "] do\n    if (env.find? root).isNone then throwError m!\"MISSING_EXECUTABLE_ROOT {root}\"\n    match env.getModuleIdxFor? root with\n    | none => throwError m!\"MISSING_ROOT_ORIGIN {root}\"\n    | some idx =>\n      let mod := env.allImportedModuleNames[idx.toNat]!\n      if !(selected.contains mod.toString) then throwError m!\"UNSELECTED_ROOT_ORIGIN {root} {mod}\"", audit, flags=re.S)
                assert replaced == 1
                audit = audit.replace("      if let some info := env.find? name then", "      if (env.find? name).isNone then throwError m!\"MISSING_EXECUTABLE_DEP {root} {name}\"\n      if let some info := env.find? name then")
                audit = audit.replace("    logInfo m!\"EXECUTABLE_DEPENDENCY_CHECK", "          else\n            logInfo m!\"EXECUTABLE_EXTERNAL_BOUNDARY {root} {mod} {name}\"\n    logInfo m!\"EXECUTABLE_DEPENDENCY_CHECK")
                assert "``List.range, ``List.replicate" in audit
                assert "``Agent102.word, ``Agent102.wordAt, ``Agent102.ParameterSets.CountExpr.value" in audit
            (build / (audit_name + ".lean")).write_text(audit)
            report.setdefault("audit_templates", {})[audit_name] = {"original_sha256": sha256(original.encode()), "adapted_sha256": sha256(audit.encode()), "changes": "Select all thirteen modules; import the real closure root; validate selected-module presence. Executable audit additionally selects sixteen public roots, rejects absent constants and records external frontier nodes."}
        assert not list(build.glob("*.olean"))
        report["runner_sha256"] = sha256(Path(__file__).read_bytes())
        if args.prepare_only:
            report["status"] = "PREPARED_NOT_RUN"
            save()
            return 0
        compiler_before = sha256(lean.read_bytes())
        assert compiler_before == LEAN_SHA256, "compiler hash mismatch"
        version = run("lean-version", [str(lean), "--version"]).strip()
        assert "version 4.19.0," in version and "commit 6caaee842e94, Release" in version
        runtime = Path(run("lean-prefix", [str(lean), "--print-prefix"]).strip())
        compiler_files = [lean, *sorted((runtime / "lib/lean").glob("*.so"))]
        compiler_hashes = {str(p): sha256(p.read_bytes()) for p in compiler_files}
        report["compiler"] = {"version": version, "files": compiler_hashes}
        report["status"] = "RUNNING"
        save()
        flags = [str(lean), "--trust=0", "-j1", "-DElab.async=false"]
        for name in order:
            run(name, flags + ["-o", name + ".olean", name + ".lean"])
        literal_log = run("LiteralAudit", flags + ["-o", "LiteralAudit.olean", "LiteralAudit.lean"])
        parsed = re.findall(r"'([^']+)' (?:does not depend on any axioms|depends on axioms: \[([^\]]*)\])", literal_log)
        assert len(parsed) == 140 and {n for n, _ in parsed} == set(expected)
        literal_results = []
        for name, values in parsed:
            axioms = [s.strip() for s in values.split(",") if s.strip()]
            assert set(axioms) <= ALLOWED, name + " disallowed literal axioms"
            literal_results.append({"theorem": name, "axioms": axioms})
        write_json(out / "literal-results.json", literal_results)
        origin_log = run("ModuleOriginAudit", flags + ["-o", "ModuleOriginAudit.olean", "ModuleOriginAudit.lean"])
        declarations = re.findall(r"^AUDIT_THEOREM (\S+) (\S+) : (.*)$", origin_log, re.M)
        totals = re.findall(r"^FULL_MODULE_AUDIT theorems=(\d+) union=([^\n]*)$", origin_log, re.M)
        assert len(totals) == 1 and int(totals[0][0]) == len(declarations)
        assert len(declarations) == len({n for _, n, _ in declarations}) and declarations
        assert set(expected) <= {n for _, n, _ in declarations}
        report["literal_theorem_count"] = len(parsed)
        report["module_origin_theorem_count"] = len(declarations)
        report["axiom_union"] = totals[0][1]
        report["unsafe_implementation_axioms"] = re.findall(r"^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$", origin_log, re.M)
        exec_log = run("ExecutableDependencyAudit", flags + ["-o", "ExecutableDependencyAudit.olean", "ExecutableDependencyAudit.lean"])
        exec_results = re.findall(r"^EXECUTABLE_DEPENDENCY_CHECK (\S+) project_constants=(\d+) forbidden=0$", exec_log, re.M)
        assert len(exec_results) == len(EXECUTABLE_ROOTS)
        assert {n for n, _ in exec_results} == set(EXECUTABLE_ROOTS)
        assert all(int(count) > 0 for _, count in exec_results)
        report["executable_results"] = [{"root": n, "project_constants": int(c), "forbidden": 0} for n, c in exec_results]
        for name, record in modules.items():
            assert (SOURCE / record["path"]).read_bytes() == originals[name]
            assert (build / (name + ".lean")).read_bytes() == originals[name]
        for path, digest in compiler_hashes.items():
            assert sha256(Path(path).read_bytes()) == digest
        report["status"] = "PASS"
        return 0
    except Exception as error:
        report["status"] = "FAILED"
        report["error"] = str(error)
        (out / "failure.txt").write_text(traceback.format_exc())
        print("FAILED: " + str(error), flush=True)
        return 1
    finally:
        report["finished_at_epoch"] = time.time()
        save()
        files = {str(p.relative_to(out)): {"bytes": p.stat().st_size, "sha256": sha256(p.read_bytes())}
                 for p in sorted(out.rglob("*")) if p.is_file() and p.suffix != ".olean" and p.name != "FILES.json"}
        write_json(out / "FILES.json", files)


if __name__ == "__main__":
    raise SystemExit(main())
