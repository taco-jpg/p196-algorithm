#!/usr/bin/env python3
"""Extend a successful exact canonical fresh build, then audit every module.

This does not modify or impersonate the original canonical verifier. It reuses
only the exact artifacts of a named successful fresh canonical execution, adds
the new source modules, and preserves the original exhaustive audit body.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import time
import traceback

CANONICAL_SHA = "c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a"
BASE_PROJECT = "agent105-uniform-safe-return"
FINAL_PROJECT = "agent105-uniform-integer-return"

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--base-registry", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo, base, out, lean = args.repo.resolve(), args.base.resolve(), args.output.resolve(), args.lean.resolve()
    out.mkdir(parents=True, exist_ok=False)
    source, logs = out / "source", out / "logs"
    source.mkdir(); logs.mkdir()
    report = {
        "executor": "/root/ownership_audit / agent105-8f1107db019a",
        "status": "RUNNING", "build_kind": "Phased exact-source verification",
        "repository_wide_pass": False, "started_at_epoch": time.time(),
        "commands": [], "sources": {}, "reused_fresh_artifacts": {},
        "compiler_arguments": ["--trust=0", "-j1", "-DElab.async=false"],
    }
    def save():
        (out / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    rc = 1
    try:
        original = repo / "proofs/verify_project__214bf7673efe116b.py"
        if digest(original.read_bytes()) != CANONICAL_SHA:
            raise ValueError("Original canonical verifier pin mismatch")
        canonical = runpy.run_path(str(original))
        mask, safe_path, name_pattern = canonical["code_only"], canonical["local_path"], canonical["NAME"]
        report["original_canonical_verifier_sha256"] = CANONICAL_SHA
        regbytes, baseregbytes = args.registry.read_bytes(), args.base_registry.read_bytes()
        reg, basereg = json.loads(regbytes), json.loads(baseregbytes)
        for r in [reg, basereg]:
            if r["schema_version"] != 1 or r["toolchain"]["allowed_axioms"] != canonical["ALLOWED"]:
                raise ValueError("Registry schema or axiom policy mismatch")
        brbytes = (base / "verification.json").read_bytes()
        br = json.loads(brbytes)
        if br["status"] != "PASS" or br["projects"][BASE_PROJECT]["status"] != "PASS":
            raise ValueError("Base is not a successful canonical fresh build")
        if br["registry_sha256"] != digest(baseregbytes):
            raise ValueError("Base registry differs from successful fresh build")
        spec, bs = reg["projects"][FINAL_PROJECT], basereg["projects"][BASE_PROJECT]
        records, brecords = spec["modules"], bs["modules"]
        if len(records) != 26 or len(brecords) != 20 or not set(brecords) <= set(records):
            raise ValueError("Unexpected phased module closure")
        report["base_canonical_report_sha256"] = digest(brbytes)
        report["base_registry_sha256"] = digest(baseregbytes)
        report["registry_sha256"] = digest(regbytes)
        report["source_commit_at_start"] = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
        report["tracked_source_tree_clean_at_start"] = not subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"], cwd=repo)
        version = subprocess.check_output([str(lean), "--version"], text=True).strip()
        if not re.search(r"version 4\.19\.0,.*commit 6caaee842e94, Release", version):
            raise ValueError("Incorrect official runtime")
        for p, expected in br["compiler"]["files"].items():
            if digest(Path(p).read_bytes()) != expected:
                raise ValueError("Runtime changed since fresh base build: " + p)
        if str(lean) not in br["compiler"]["files"]:
            raise ValueError("A different compiler was requested")
        runtime = Path(subprocess.check_output([str(lean), "--print-prefix"], text=True).strip())
        report["compiler"] = br["compiler"]
        originals, imports = {}, {}
        base_source = base / BASE_PROJECT / "source"
        for module, rec in records.items():
            if not name_pattern.fullmatch(module) or rec.get("adapter"):
                raise ValueError("Unexpected module name or adapter")
            path = safe_path(repo, rec["path"])
            data = path.read_bytes()
            if digest(data) != rec["sha256"] or hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() != rec["git_blob"]:
                raise ValueError("Source pin mismatch: " + module)
            code = mask(data.decode())
            if re.search(r"(?<![\w'])\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b(?![\w'])", code):
                raise ValueError("Forbidden source token: " + module)
            deps = [d for line in re.findall(r"^\s*import\s+([^\n]+)", code, re.M) for d in line.split()]
            if deps != rec["imports"] or any(not name_pattern.fullmatch(d) for d in deps):
                raise ValueError("Import identity mismatch: " + module)
            for dep in deps:
                if dep not in records and (dep.split(".")[0] not in {"Std", "Init", "Lean"} or not (runtime / "lib/lean" / (dep.replace(".", "/") + ".olean")).is_file()):
                    raise ValueError("Unregistered import: " + dep)
            originals[module], imports[module] = data, deps
            target = source / (module.replace(".", "/") + ".lean")
            target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
            membership = subprocess.run(["git", "show", "HEAD:" + rec["path"]], cwd=repo, capture_output=True)
            report["sources"][module] = {**rec, "exact_bytes_present_at_head_start": membership.returncode == 0 and membership.stdout == data}
            if module in brecords:
                if any(rec[k] != brecords[module][k] for k in ["path", "sha256", "git_blob", "imports"]):
                    raise ValueError("Base record changed: " + module)
                relative = module.replace(".", "/")
                if (base_source / (relative + ".lean")).read_bytes() != data:
                    raise ValueError("Fresh base snapshot changed: " + module)
                compiled = base_source / (relative + ".olean")
                obj = compiled.read_bytes()
                (source / (relative + ".olean")).write_bytes(obj)
                report["reused_fresh_artifacts"][module] = {"source_sha256": digest(data), "olean_sha256": digest(obj), "olean_bytes": len(obj), "base_path": str(compiled)}
        order, active, seen = [], set(), set()
        def visit(module):
            if module not in records or module in seen: return
            if module in active: raise ValueError("Import cycle")
            active.add(module)
            for dep in imports[module]: visit(dep)
            active.remove(module); seen.add(module); order.append(module)
        for root in spec["roots"]: visit(root)
        if seen != set(records): raise ValueError("Records outside final root closure")
        added = [m for m in order if m not in brecords]
        report["full_build_order"], report["additional_module_build_order"] = order, added
        if len(added) != 6: raise ValueError("Unexpected additional module count")
        env = dict(os.environ); env["LEAN_PATH"] = str(source)
        def run(label, command):
            started = time.monotonic(); log = logs / (label + ".log")
            with log.open("wb") as stream:
                result = subprocess.run(command, cwd=source, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=1800)
            report["commands"].append({"label": label, "argv": command, "exit_code": result.returncode, "elapsed_seconds": time.monotonic() - started, "log_sha256": digest(log.read_bytes())})
            save(); print(label, "exit=" + str(result.returncode), flush=True)
            if result.returncode: raise RuntimeError("Failed " + label)
            return log.read_text()
        for module in added:
            relative = module.replace(".", "/")
            run(module, [str(lean), "--trust=0", "-j1", "-DElab.async=false", "-o", relative + ".olean", relative + ".lean"])
        endpoints = [e for c in reg["claims"] if c["project"] == FINAL_PROJECT for e in c["endpoints"]]
        if len(endpoints) != 115 or any(not name_pattern.fullmatch(e) for e in endpoints):
            raise ValueError("Unexpected final public endpoints")
        base_audit = (base_source / "ProjectAudit.lean").read_text()
        if base_audit.count("  let allowed : List Name :=") != 1:
            raise ValueError("Unexpected original canonical audit structure")
        audit_body = "  let allowed : List Name :=" + base_audit.split("  let allowed : List Name :=", 1)[1]
        audit = "\n".join("import " + m for m in spec["roots"]) + "\nimport Lean\nopen Lean Elab Command\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n" + "\n".join("#check " + e for e in endpoints) + "\nrun_cmd do\n  let env ← getEnv\n  let selected : List String := " + json.dumps(order) + "\n" + audit_body
        (source / "FinalProjectAudit.lean").write_text(audit)
        report["exhaustive_audit_body_sha256"] = digest(audit_body.encode())
        report["exhaustive_audit_body_byte_equal_original_canonical"] = True
        audit_log = run("FinalProjectAudit", [str(lean), "--trust=0", "-j1", "-DElab.async=false", "FinalProjectAudit.lean"])
        summaries = re.findall(r"^FULL_MODULE_AUDIT theorems=(\d+) union=([^\n]*)$", audit_log, re.M)
        declarations = re.findall(r"^AUDIT_THEOREM (\S+) (\S+) : (.*)$", audit_log, re.M)
        if len(summaries) != 1 or int(summaries[0][0]) != len(declarations) or not declarations or len({t[1] for t in declarations}) != len(declarations):
            raise ValueError("Incomplete or duplicate final module-origin audit")
        report["theorem_count"] = len(declarations)
        report["axiom_union"] = summaries[0][1]
        report["endpoints"] = endpoints
        report["unsafe_implementation_axioms"] = re.findall(r"^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$", audit_log, re.M)
        report["theorems_by_module"] = {m: sum(t[0] == m for t in declarations) for m in order}
        for module, rec in records.items():
            if safe_path(repo, rec["path"]).read_bytes() != originals[module] or (source / (module.replace(".", "/") + ".lean")).read_bytes() != originals[module]:
                raise ValueError("Source changed during execution: " + module)
            if module in brecords:
                for p in [base_source / (module.replace(".", "/") + ".olean"), source / (module.replace(".", "/") + ".olean")]:
                    if digest(p.read_bytes()) != report["reused_fresh_artifacts"][module]["olean_sha256"]:
                        raise ValueError("Reused fresh object changed: " + module)
        if args.registry.read_bytes() != regbytes or args.base_registry.read_bytes() != baseregbytes or (base / "verification.json").read_bytes() != brbytes:
            raise ValueError("Registry or base report changed")
        for p, expected in br["compiler"]["files"].items():
            if digest(Path(p).read_bytes()) != expected: raise ValueError("Compiler changed")
        report["source_commit_at_finish"] = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
        report["status"] = "PASS"; rc = 0
    except Exception as error:
        report["status"], report["error"] = "FAIL", str(error)
        (out / "failure.txt").write_text(traceback.format_exc())
        print("FAIL:", error, flush=True)
    finally:
        report["finished_at_epoch"] = time.time(); save()
        files = {str(p.relative_to(out)): {"bytes": p.stat().st_size, "sha256": digest(p.read_bytes())} for p in sorted(out.rglob("*")) if p.is_file() and p.suffix != ".olean" and p.name != "FILES.json"}
        (out / "FILES.json").write_text(json.dumps(files, indent=2) + "\n")
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
