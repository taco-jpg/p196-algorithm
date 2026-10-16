#!/usr/bin/env python3
"""Independent source-only six-module rebuild and exhaustive compiled theorem audit.

The Mathlib cache is an explicit pinned compiled dependency, not a source rebuild.
Run from an exact review checkout; --out must name a new directory.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import time
import traceback

sys.dont_write_bytecode = True
SOURCE_COMMIT = "122367d4935f0b4cd9e0bee19e4121ec66b3164b"
MATHLIB_COMMIT = "c44e0c8ee63ca166450922a373c7409c5d26b00b"
MANIFEST_SHA256 = "5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752"
ARCHIVE_SHA256 = "6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe"
COMPILER_SHA256 = "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023"
EXACT_TYPES_SHA256 = "79ff0637667b95ff4b411a6c9ce57880c325769b39fb44285de9fa4e2563200c"
FIXTURE_COMMIT = "ab6768ef000358b5f81c6807db674dc7515819c9"
REVIEW = "proofs/contributions/agent-104/review-agent13-real-weights"
MODULES = ("LychrelDigitSums", "Family", "TargetSafety", "Counting", "Weights", "SqrtBound")
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
EXPORTS = ("predecessor_le", "mem_safeFiber_iff", "full_safe_fiber_finite", "incoming_nonneg",
           "family_sum_le_incoming", "finite_family_weight_lower", "incoming_weight_lower",
           "incoming_weight_ratio", "no_uniform_multiplier", "not_exists_uniform_bound",
           "target_size_bound_nat", "target_size_bound_real", "family_size_scaled_power",
           "sqrt_scale_lt_family_size", "incoming_weight_sqrt_lower")
FORBIDDEN = re.compile(r"\b(?:sorry|admit|axiom|native_decide|sorryAx|ofReduceBool|ofReduceNat|"
                       r"unsafe|run_cmd|elab|macro|implemented_by|extern|skipKernelTC)\b")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args])


def code_only(text: str) -> str:
    """Mask nested comments and strings, preserving source line positions."""
    out, i, depth, string = [], 0, 0, False
    while i < len(text):
        pair = text[i:i + 2]
        if depth:
            if pair == "/-":
                depth += 1; out.extend("  "); i += 2
            elif pair == "-/":
                depth -= 1; out.extend("  "); i += 2
            else:
                out.append("\n" if text[i] == "\n" else " "); i += 1
        elif string:
            if text[i] == "\\":
                out.extend("  "); i += 2
            else:
                string = text[i] != '"'
                out.append("\n" if text[i] == "\n" else " "); i += 1
        elif pair == "/-":
            depth = 1; out.extend("  "); i += 2
        elif pair == "--":
            end = text.find("\n", i)
            end = len(text) if end < 0 else end
            out.extend(" " * (end - i)); i = end
        elif text[i] == '"':
            string = True; out.append(" "); i += 1
        else:
            out.append(text[i]); i += 1
    if depth or string:
        raise ValueError("Unterminated comment or string")
    return "".join(out)


def make_audit() -> str:
    selected = ", ".join(json.dumps(m) for m in (*MODULES, "ExactTypes"))
    exports = ", ".join(json.dumps("Agent13SafeWeights." + n) for n in EXPORTS)
    return '''import ExactTypes
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := [''' + selected + ''']
  let exports : List String := [''' + exports + ''']
  for mod in env.allImportedModuleNames do
    let path ← liftIO <| findOLean mod
    logInfo m!"AUDIT_IMPORT {mod} {path}"
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
          if exports.contains name.toString then
            logInfo m!"AUDIT_EXPORT_TYPE {name}\n{info.type}"
            logInfo m!"AUDIT_EXPORT_RAW_TYPE {name}\n{repr info.type}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | _ => pure ()
'''


def verify_official_archive(archive: Path, prefix: Path) -> dict[str, str]:
    if sha(archive) != ARCHIVE_SHA256:
        raise ValueError("Official Lean archive SHA256 mismatch")
    expected = [prefix / "bin/lean", *sorted((prefix / "lib/lean").glob("*.so")),
                *sorted((prefix / "lib/lean").rglob("*.olean")),
                prefix / "src/lean/Lean/Util/CollectAxioms.lean"]
    wanted = {"lean-4.19.0-linux/" + str(p.relative_to(prefix)): p for p in expected}
    pins = {}
    with subprocess.Popen(["zstd", "-dc", str(archive)], stdout=subprocess.PIPE) as proc:
        assert proc.stdout is not None
        with tarfile.open(fileobj=proc.stdout, mode="r|") as tf:
            for member in tf:
                if member.name not in wanted:
                    continue
                stream = tf.extractfile(member)
                if stream is None:
                    raise ValueError(f"Non-file archive member: {member.name}")
                member_sha = hashlib.file_digest(stream, "sha256").hexdigest()
                path = wanted[member.name]
                if sha(path) != member_sha:
                    raise ValueError(f"Installed official member mismatch: {path}")
                pins[str(path)] = member_sha
        proc.stdout.close()
        if proc.wait() != 0:
            raise ValueError("Official archive decompression failed")
    if set(pins) != {str(p) for p in expected}:
        raise ValueError("Official archive did not cover all selected installed members")
    return pins


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--mathlib", type=Path, required=True)
    parser.add_argument("--lean-archive", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    project, logs, controls, originals = [out / p for p in ("project", "logs", "controls", "original-sources")]
    for path in (project, logs, controls, originals):
        path.mkdir()
    report = {"status": "IN_PROGRESS", "source_commit": SOURCE_COMMIT,
              "started_at_utc": datetime.now(timezone.utc).isoformat(),
              "fresh_source_rebuild": True, "local_modules": list(MODULES),
              "prior_local_objects_reused": False, "mathlib_source_rebuild": False,
              "compiled_mathlib_cache_reused": True, "build_workers": 1,
              "allowed_axioms": sorted(ALLOWED), "commands": [], "sources": {}}
    env = dict(os.environ)
    for key in ("LEAN_PATH", "LEAN_SRC_PATH", "LEAN_SYSROOT"):
        env.pop(key, None)
    env["LEAN_PATH"] = str(project)

    def save() -> None:
        write(out / "verification.json", report)

    def run(label: str, command: list[str], cwd: Path = project) -> str:
        log = logs / (label + ".log")
        started = time.monotonic()
        with log.open("wb") as stream:
            proc = subprocess.Popen(command, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT)
            _, status, usage = os.wait4(proc.pid, 0)
            proc.returncode = os.waitstatus_to_exitcode(status)
        rec = {"label": label, "command": command, "cwd": str(cwd), "exit_code": proc.returncode,
               "seconds": round(time.monotonic() - started, 3), "maximum_resident_set_kib": usage.ru_maxrss,
               "user_seconds": usage.ru_utime, "system_seconds": usage.ru_stime,
               "log": str(log.relative_to(out)), "log_sha256": sha(log)}
        report["commands"].append(rec); save(); print(json.dumps(rec), flush=True)
        if proc.returncode != 0:
            raise RuntimeError(f"{label} failed with exit {proc.returncode}; exact log retained")
        return log.read_text()

    try:
        repo, lean, lib = args.repo.resolve(strict=True), args.lean.resolve(strict=True), args.mathlib.resolve(strict=True)
        review_commit = git(repo, "rev-parse", "HEAD").decode().strip()
        if os.environ.get("GITHUB_SHA", review_commit) != review_commit:
            raise ValueError("Review checkout differs from hosted run SHA")
        report["review_commit"] = review_commit
        report["source_tree"] = git(repo, "rev-parse", SOURCE_COMMIT + "^{tree}").decode().strip()
        report["hosted_run"] = {key: os.environ.get(key) for key in ("GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT", "GITHUB_REPOSITORY", "GITHUB_REF", "GITHUB_SHA")}
        if os.environ.get("LD_PRELOAD") or os.environ.get("LD_LIBRARY_PATH"):
            raise ValueError("Unexpected dynamic-library override; direct official compiler required")
        for rel in (REVIEW + "/execution/check.py", REVIEW + "/execution/source-pins.json",
                    REVIEW + "/semantic/ExactTypes.lean", ".github/workflows/agent104-real-weights-review.yml"):
            blob = git(repo, "show", review_commit + ":" + rel)
            if (repo / rel).read_bytes() != blob:
                raise ValueError(f"Review control differs from committed source: {rel}")
            (controls / Path(rel).name).write_bytes(blob)
        if Path(__file__).resolve().read_bytes() != (controls / "check.py").read_bytes():
            raise ValueError("Executed checker differs from committed review checker")
        pins = json.loads((controls / "source-pins.json").read_text())
        if pins["source_commit"] != SOURCE_COMMIT or set(pins["modules"]) != set(MODULES):
            raise ValueError("Incorrect accepted source pin inventory")
        for module in MODULES:
            pin = pins["modules"][module]
            blob = git(repo, "show", SOURCE_COMMIT + ":" + pin["path"])
            if digest(blob) != pin["sha256"] or len(blob) != pin["bytes"]:
                raise ValueError(f"Source SHA256/length mismatch: {module}")
            code = code_only(blob.decode())
            if FORBIDDEN.search(code):
                raise ValueError(f"Disallowed source escape in {module}")
            imports = re.findall(r"^\s*import\s+([A-Za-z0-9_.]+)\s*$", code, re.MULTILINE)
            for imported in imports:
                if imported in MODULES and MODULES.index(imported) >= MODULES.index(module):
                    raise ValueError(f"Invalid local topological order: {module}/{imported}")
                if imported not in MODULES and not (imported == "Std" or imported.startswith("Mathlib.")):
                    raise ValueError(f"Unexpected external source import: {module}/{imported}")
            target = project / (module + ".lean")
            target.write_bytes(blob)
            original = originals / pin["path"]
            original.parent.mkdir(parents=True, exist_ok=True); original.write_bytes(blob)
            report["sources"][module] = {**pin, "imports": imports,
                "git_blob_sha1": git(repo, "rev-parse", SOURCE_COMMIT + ":" + pin["path"]).decode().strip(),
                "snapshot": str(target.relative_to(out))}
        original_checker = pins["author_checker"]
        blob = git(repo, "show", SOURCE_COMMIT + ":" + original_checker["path"])
        if digest(blob) != original_checker["sha256"]:
            raise ValueError("Original checker provenance mismatch")
        (originals / "author-check.py").write_bytes(blob)
        exact = (controls / "ExactTypes.lean").read_bytes()
        if digest(exact) != EXACT_TYPES_SHA256 or FORBIDDEN.search(code_only(exact.decode())):
            raise ValueError("Exact-types harness changed or has disallowed escapes")
        if git(repo, "show", FIXTURE_COMMIT + ":" + REVIEW + "/semantic/ExactTypes.lean") != exact:
            raise ValueError("Exact-types harness differs from independently published fixture commit")
        (project / "ExactTypes.lean").write_bytes(exact)
        report["exact_types_sha256"] = digest(exact)
        report["exact_types_original_fixture_commit"] = FIXTURE_COMMIT
        report["snapshot_complete_before_build"] = True
        report["snapshot_initial_object_count"] = len(list(project.glob("*.olean")))
        if report["snapshot_initial_object_count"] != 0:
            raise ValueError("Fresh project unexpectedly contains compiled objects")
        version = run("lean-version", [str(lean), "--version"]).strip()
        prefix = Path(run("lean-prefix", [str(lean), "--print-prefix"]).strip()).resolve()
        if not re.search(r"version 4\.19\.0,.*commit 6caaee842e94, Release", version) or sha(lean) != COMPILER_SHA256:
            raise ValueError("Compiler is not the pinned official Lean4.19.0 binary")
        archive_pins = verify_official_archive(args.lean_archive.resolve(strict=True), prefix)
        write(out / "official-archive-members.json", archive_pins)
        report["compiler"] = {"version": version, "path": str(lean), "sha256": sha(lean),
                              "prefix": str(prefix), "archive_sha256": ARCHIVE_SHA256,
                              "independently_compared_archive_members": len(archive_pins)}
        shutil.copyfile(prefix / "src/lean/Lean/Util/CollectAxioms.lean", controls / "Lean-CollectAxioms.lean")
        if git(lib, "rev-parse", "HEAD").decode().strip() != MATHLIB_COMMIT or sha(lib / "lake-manifest.json") != MANIFEST_SHA256:
            raise ValueError("Mathlib commit or exact manifest differs from pin")
        manifest = json.loads((lib / "lake-manifest.json").read_text())
        shutil.copyfile(lib / "lake-manifest.json", out / "mathlib-lake-manifest.json")
        packages = {p["name"]: p["rev"] for p in manifest["packages"]}
        library_roots = [lib / ".lake/build/lib/lean"]
        source_roots = {str(library_roots[0]): lib}
        for name, commit in [("mathlib", MATHLIB_COMMIT), *sorted(packages.items())]:
            checkout = lib if name == "mathlib" else lib / ".lake/packages" / name
            if git(checkout, "rev-parse", "HEAD").decode().strip() != commit:
                raise ValueError(f"Wrong dependency commit: {name}")
            run("clean-" + name, ["git", "diff", "--exit-code", "HEAD", "--", "*.lean", "lake-manifest.json", "lakefile.toml", "lean-toolchain"], checkout)
            if name != "mathlib":
                root = checkout / ".lake/build/lib/lean"
                if root.exists():
                    library_roots.append(root); source_roots[str(root)] = checkout
        report["library"] = {"mathlib_commit": MATHLIB_COMMIT, "manifest_sha256": MANIFEST_SHA256,
                             "dependency_commits": packages, "official_compiled_cache_reused": True,
                             "source_rebuild_claimed": False, "search_roots": list(source_roots)}
        roots = [project, *library_roots, prefix / "lib/lean"]
        env["LEAN_PATH"] = os.pathsep.join(str(p) for p in roots[:-1])
        report["LEAN_PATH"] = env["LEAN_PATH"]
        initial_objects = {str(p.resolve()): sha(p) for root in roots[1:] for p in sorted(root.rglob("*.olean"))}
        write(out / "dependency-object-pins-before.json", initial_objects)
        for module in (*MODULES, "ExactTypes"):
            run(module, [str(lean), "-j1", "-DElab.async=false", "-o", module + ".olean", module + ".lean"])
            if module in report["sources"]:
                report["sources"][module]["object_sha256"] = sha(project / (module + ".olean"))
        local_objects = {str((project / (m + ".olean")).resolve()): sha(project / (m + ".olean")) for m in (*MODULES, "ExactTypes")}
        (project / "AllCompiledAxioms.lean").write_text(make_audit())
        output = run("AllCompiledAxioms", [str(lean), "-j1", "-DElab.async=false", "AllCompiledAxioms.lean"])
        declarations = re.findall(r"^AUDIT_THEOREM (\S+) (\S+)$", output, re.MULTILINE)
        names = {name: module for module, name in declarations}
        if len(names) != len(declarations) or not names:
            raise ValueError("Empty or duplicated compiled theorem inventory")
        audited = {}
        records = [(n, sorted(a.strip() for a in axes.split(",") if a.strip())) for n, axes in
                   re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", output)]
        records += [(n, []) for n in re.findall(r"'([^']+)' does not depend on any axioms", output)]
        for name, axes in records:
            if name in audited or not set(axes) <= ALLOWED:
                raise ValueError(f"Duplicate or disallowed theorem axiom report: {name}: {axes}")
            audited[name] = axes
        if set(audited) != set(names):
            raise ValueError("Theorem inventory and transitive axiom reports do not match exactly")
        for name in EXPORTS:
            if names.get("Agent13SafeWeights." + name) not in ("Weights", "SqrtBound"):
                raise ValueError(f"Missing intended export: {name}")
            if names.get("Agent104.RealWeightsExactTypes." + name + "_type") != "ExactTypes":
                raise ValueError(f"Missing exact type witness: {name}")
        for marker in ("AUDIT_EXPORT_TYPE", "AUDIT_EXPORT_RAW_TYPE"):
            emitted = re.findall(r"^" + marker + r" (\S+)$", output, re.MULTILINE)
            if len(emitted) != len(EXPORTS) or set(emitted) != {"Agent13SafeWeights." + n for n in EXPORTS}:
                raise ValueError(f"Missing/duplicate elaborated export type output: {marker}")
        unsafe = re.findall(r"^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$", output, re.MULTILINE)
        if {n for _, n in unsafe} & {a for axes in audited.values() for a in axes}:
            raise ValueError("Unsafe implementation axiom occurs in accepted theorem dependencies")
        imported = {}
        for module, raw in re.findall(r"^AUDIT_IMPORT (\S+) (.+)$", output, re.MULTILINE):
            path = Path(raw).resolve(strict=True)
            expected = next((root / (module.replace(".", "/") + ".olean") for root in roots
                             if (root / (module.replace(".", "/") + ".olean")).is_file()), None)
            if expected is None or expected.resolve() != path or module in imported:
                raise ValueError(f"Unaccounted/duplicate actual imported object: {module}: {path}")
            before = local_objects.get(str(path), initial_objects.get(str(path)))
            if before is None or sha(path) != before:
                raise ValueError(f"Imported object changed or was not pinned before use: {module}")
            record = {"path": str(path), "bytes": path.stat().st_size, "sha256": before}
            if path.is_relative_to(project):
                record["origin"] = "fresh local source build"
            elif path.is_relative_to(prefix):
                if archive_pins.get(str(path)) != before:
                    raise ValueError(f"Imported official object differs from archive: {module}")
                record["origin"] = "verified official Lean archive"
            else:
                record["origin"] = "explicit pinned Mathlib/dependency compiled cache"
                root = next(root for root in library_roots if path.is_relative_to(root))
                source_root = source_roots[str(root)]
                source = source_root / (module.replace(".", "/") + ".lean")
                record["source_commit"] = git(source_root, "rev-parse", "HEAD").decode().strip()
                if not source.is_file():
                    raise ValueError(f"Imported cached module has no corresponding pinned source: {module}")
                rel = str(source.relative_to(source_root))
                committed = git(source_root, "show", "HEAD:" + rel)
                if source.read_bytes() != committed:
                    raise ValueError(f"Imported dependency source differs from commit: {module}")
                record["source_path"] = rel; record["source_sha256"] = digest(committed)
            imported[module] = record
        if not set((*MODULES, "ExactTypes")) <= set(imported):
            raise ValueError("Missing fresh local object in actual import inventory")
        for module, rec in report["sources"].items():
            if sha(out / rec["snapshot"]) != rec["sha256"] or sha(project / (module + ".olean")) != rec["object_sha256"]:
                raise ValueError(f"Local source/object changed during audit: {module}")
        for path, expected in archive_pins.items():
            if sha(Path(path)) != expected:
                raise ValueError(f"Official installed member changed during audit: {path}")
        if sha(project / "ExactTypes.lean") != EXACT_TYPES_SHA256:
            raise ValueError("Exact type source changed during run")
        for rec in report["commands"]:
            if sha(out / rec["log"]) != rec["log_sha256"]:
                raise ValueError("Command log changed during audit")
        report.update({"status": "PASS", "all_15_exact_types_checked": True,
            "all_15_elaborated_and_raw_expression_types_retained": True,
            "theorem_count": len(names), "contribution_closure_theorem_count": sum(m in MODULES for m in names.values()),
            "theorems_per_module": dict(sorted(Counter(names.values()).items())),
            "theorems": {n: {"module": names[n], "axioms": audited[n]} for n in sorted(names)},
            "export_axioms": {"Agent13SafeWeights." + n: audited["Agent13SafeWeights." + n] for n in EXPORTS},
            "unsafe_implementation_axioms": unsafe, "unsafe_implementation_axioms_in_accepted_dependencies": [],
            "imported_objects": imported, "source_object_compiler_log_stability_checked": True,
            "audit_source_sha256": sha(project / "AllCompiledAxioms.lean")})
    except Exception as exc:
        report["status"] = "FAIL"
        report["failure"] = str(exc)
        (logs / "failure-traceback.log").write_text(traceback.format_exc())
        print(traceback.format_exc(), file=sys.stderr, flush=True)
    finally:
        report["finished_at_utc"] = datetime.now(timezone.utc).isoformat(); save()
        write(out / "artifact-inventory.json", {
            "status": report["status"], "source_commit": SOURCE_COMMIT,
            "files": {str(p.relative_to(out)): {"bytes": p.stat().st_size, "sha256": sha(p)}
                      for p in sorted(out.rglob("*")) if p.is_file()},
            "inventory_excludes_itself": True,
            "included": "Exact six original sources; fresh source snapshot and all newly built local objects; ExactTypes and exhaustive audit source; original author checker as provenance only; review controls; full raw compiler/audit/failure logs; source, compiler, archive, dependency and actual imported-object pins.",
            "excluded": "Downloaded official archive, toolchain installation, full Mathlib/dependency checkouts and caches are reproducible external infrastructure; exact commits/manifest/archive checksum and object hashes are retained. No prior author artifact or local object is used as independent execution evidence. Infrastructure setup logs are uploaded beside this directory by the workflow.",
        })
    print(report["status"], flush=True)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
