#!/usr/bin/env python3
"""Agent #104: clean kernel rebuild of a frozen 620 certificate closure.

This performs a new compiler invocation for every module, including all generic
dependencies. It never reads author .olean files. Existing dependency evidence
is used only as a source-origin map, and each generic source is fetched again
from its pinned Git object. Generated source hashes are checked against the
generator manifest and copied into the previously absent build directory.
The manifest is source identity evidence; Lean supplies the proof check.
"""
from __future__ import annotations

import argparse
import concurrent.futures as futures
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import traceback


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--lean", type=Path, required=True)
    p.add_argument("--dependency-map", type=Path, required=True)
    p.add_argument("--generation-manifest", type=Path, required=True)
    p.add_argument("--source-ref", help="Exact published commit containing every generated source and the generation manifest; mandatory for a full canonical proof check")
    p.add_argument("--stdlib-manifest", type=Path, help="Evidence manifest comparing every standard-library .olean with the pinned official archive; recheck these bytes before and after the proof build")
    p.add_argument("--root-module", action="append", required=True)
    p.add_argument("--endpoint", action="append", default=[])
    p.add_argument("--build", type=Path, required=True)
    p.add_argument("--evidence", type=Path, required=True)
    p.add_argument("--jobs", type=int, default=2)
    p.add_argument("--canonical", action="store_true", help="Delegate the new complete build and audit to the unchanged repository replay wrapper and canonical verifier")
    p.add_argument("--source-check-only", action="store_true", help="Check canonical source transport and import closure without compiling proofs; requires --canonical")
    args = p.parse_args()
    if not 1 <= args.jobs <= 4:
        raise ValueError("Use between one and four independent -j1 compiler processes")
    name_re = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\Z")
    if any(not name_re.fullmatch(n) for n in args.root_module + args.endpoint):
        raise ValueError("Invalid Lean module or endpoint identifier")
    if args.canonical and not args.endpoint:
        raise ValueError("Canonical registration requires explicit exported theorem endpoints")
    if args.source_check_only and not args.canonical:
        raise ValueError("Source transport checking requires the canonical backend")
    if args.canonical and not args.source_check_only and not args.source_ref:
        raise ValueError("A full canonical proof check requires an explicit published --source-ref")
    repo, lean, build, evidence = (v.resolve() for v in (args.repo, args.lean, args.build, args.evidence))
    build.mkdir(parents=True, exist_ok=False)
    evidence.mkdir(parents=True, exist_ok=True)
    logs = evidence / "logs"
    logs.mkdir(exist_ok=False)
    helper_path = Path(__file__).resolve().parents[1] / "author-base/build_base.py"
    spec = importlib.util.spec_from_file_location("agent104_source_audit_helpers", helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    inputs = [Path(__file__).resolve(), helper_path, args.dependency_map.resolve(), args.generation_manifest.resolve()]
    if args.stdlib_manifest:
        inputs.append(args.stdlib_manifest.resolve())
    input_hashes = {str(path): sha(path.read_bytes()) for path in inputs}
    mapping = json.loads(args.dependency_map.read_text())
    manifest = json.loads(args.generation_manifest.read_text())
    report = {"agent": "Agent #104", "specialist": "runtime_scout", "status": "RUNNING", "scope": "new clean Lean kernel rebuild of the exact selected 620 endpoint import closure", "empty_build_at_start": True, "reused_olean_files": [], "roots": args.root_module, "requested_endpoints": args.endpoint, "jobs": args.jobs, "build": str(build), "input_sha256": input_hashes, "commands": [], "started_at_epoch": time.time()}

    def save() -> None:
        (evidence / "build.json").write_text(json.dumps(report, indent=2) + "\n")

    def git(*argv: str) -> bytes:
        return subprocess.check_output(["git", "-C", str(repo), *argv])

    def command(label: str, argv: list[str], env: dict[str, str] | None = None, timeout_seconds: int | None = 1800) -> dict:
        log = logs / (label + ".log")
        start = time.monotonic()
        with log.open("xb") as stream:
            try:
                rc = subprocess.run(argv, cwd=build, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout_seconds).returncode
            except subprocess.TimeoutExpired:
                rc = 124
        data = log.read_bytes()
        return {"label": label, "argv": argv, "exit_code": rc, "elapsed_seconds": round(time.monotonic() - start, 6), "log": str(log.relative_to(evidence)), "log_sha256": sha(data)}

    def record_command(label: str, argv: list[str], env: dict[str, str] | None = None, timeout_seconds: int | None = 1800) -> str:
        rec = command(label, argv, env, timeout_seconds)
        report["commands"].append(rec); save()
        if rec["exit_code"]:
            raise RuntimeError("Command failed: " + label)
        return (evidence / rec["log"]).read_text()

    try:
        version = record_command("000-version", [str(lean), "--version"]).strip()
        if version != "Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)":
            raise ValueError("Unexpected Lean toolchain")
        runtime = Path(record_command("001-prefix", [str(lean), "--print-prefix"]).strip()).resolve()
        compiler_files = [lean, *sorted((runtime / "lib/lean").glob("*.so"))]
        report["compiler"] = {"version": version, "files": {str(f): sha(f.read_bytes()) for f in compiler_files}}
        if args.stdlib_manifest:
            standard = json.loads(args.stdlib_manifest.read_text())
            if standard["status"] != "PASS_BYTE_EXACT_OFFICIAL_STANDARD_LIBRARY" or standard["archive_sha256"] != "6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe":
                raise ValueError("Unexpected standard-library origin manifest")
            actual_standard = {str(path.relative_to(runtime)) for path in (runtime / "lib/lean").rglob("*.olean")}
            if actual_standard != set(standard["records"]):
                raise ValueError("Standard-library module set changed")
            for relative, info in standard["records"].items():
                path = runtime / relative
                if path.is_symlink() or sha(path.read_bytes()) != info["sha256"] or path.stat().st_size != info["bytes"]:
                    raise ValueError("Standard-library module differs from pinned official archive: " + relative)
                report["compiler"]["files"][str(path)] = info["sha256"]
            report["compiler"]["standard_library_origin"] = {"manifest_sha256": sha(args.stdlib_manifest.read_bytes()), "official_archive_sha256": standard["archive_sha256"], "module_count": len(standard["records"])}
        records, snapshots, current_sources = {}, {}, {}
        active = set()
        order = []
        worktree_head = git("rev-parse", "HEAD").decode().strip()
        frozen_head = git("rev-parse", "--verify", "--end-of-options", (args.source_ref or "HEAD") + "^{commit}").decode().strip()
        report["worktree_head_at_freeze"] = worktree_head
        report["selected_source_commit"] = frozen_head
        if args.source_ref:
            manifest_relative = str(args.generation_manifest.resolve().relative_to(repo))
            manifest_bytes = git("show", frozen_head + ":" + manifest_relative)
            if manifest_bytes != args.generation_manifest.read_bytes():
                raise ValueError("Generation manifest differs from the selected published source commit")
            report["published_source"] = {
                "commit": frozen_head,
                "url": "https://github.com/taco-jpg/p196-algorithm/commit/" + frozen_head,
                "generation_manifest_path": manifest_relative,
                "generation_manifest_git_blob": git("rev-parse", frozen_head + ":" + manifest_relative).decode().strip(),
                "generation_manifest_sha256": sha(manifest_bytes),
                "generated_sources_must_match_published_git_objects": True,
            }

        def load(name: str) -> None:
            if name in records:
                return
            if name in active:
                raise ValueError("Import cycle: " + name)
            if not name_re.fullmatch(name):
                raise ValueError("Malformed import: " + name)
            if name.split(".")[0] in {"Std", "Init", "Lean"}:
                if not (runtime / "lib/lean" / (name.replace(".", "/") + ".olean")).is_file():
                    raise ValueError("Missing standard import: " + name)
                return
            active.add(name)
            if name in mapping["modules"]:
                old = mapping["modules"][name]
                source_ref, relative = old["source_ref"], old["source_path"]
                data = git("show", source_ref + ":" + relative)
                blob = git("rev-parse", source_ref + ":" + relative).decode().strip()
                if sha(data) != old["sha256"] or blob != old["git_blob"]:
                    raise ValueError("Generic source origin mismatch: " + name)
                source = repo / relative
                rec = {"source_kind": "pinned_git_object", "source_ref": source_ref, "source_path": relative, "git_blob": blob}
            else:
                if not name.startswith("Agent104Prefix620") or "." in name:
                    raise ValueError("Unregistered nonstandard module: " + name)
                source = repo / "proofs" / (name + ".lean")
                if source.is_symlink():
                    raise ValueError("Generated source cannot be a symbolic link")
                data = source.read_bytes()
                item = manifest["sources"].get(name)
                if args.source_ref and item is None:
                    raise ValueError("Published generated source is not in the generation manifest: " + name)
                if item is not None and (sha(data) != item["sha256"] or len(data) != item["bytes"]):
                    raise ValueError("Generated manifest hash mismatch: " + name)
                relative = str(source.relative_to(repo))
                blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
                rec = {"source_kind": "frozen_author_bytes", "source_path": relative, "git_blob_of_bytes": blob, "generator_manifest_member": item is not None}
                committed = subprocess.run(["git", "-C", str(repo), "rev-parse", frozen_head + ":" + relative], capture_output=True, text=True)
                if committed.returncode == 0 and committed.stdout.strip() == blob:
                    rec.update({"source_kind": "pinned_git_object", "source_ref": frozen_head, "git_blob": blob})
                else:
                    if args.source_ref:
                        raise ValueError("Generated source differs from the selected published Git object: " + name)
                    rec["source_ref"] = None
            if source.read_bytes() != data:
                raise ValueError("Working source differs from exact selected bytes: " + name)
            masked = helper.code_only(data.decode())
            if re.search(r"(?<![\w'])\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b(?![\w'])", masked):
                raise ValueError("Forbidden source token: " + name)
            imports = [word for line in re.findall(r"^\s*import\s+([^\n]+)", masked, re.M) for word in line.split()]
            if name in mapping["modules"] and imports != mapping["modules"][name]["imports"]:
                raise ValueError("Dependency graph changed: " + name)
            rec.update({"module": name, "sha256": sha(data), "bytes": len(data), "imports": imports})
            for dep in imports:
                load(dep)
            active.remove(name)
            records[name], snapshots[name], current_sources[name] = rec, data, source
            target = build / (name.replace(".", "/") + ".lean")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            order.append(name)

        for root in args.root_module:
            load(root)
        frozen = {"schema_version": 1, "worktree_head_at_freeze": worktree_head, "selected_source_commit": frozen_head, "published_source_required": bool(args.source_ref), "source_refs_are_null_for_uncommitted_author_files": not bool(args.source_ref), "roots": args.root_module, "build_order": order, "modules": records}
        (evidence / "source-snapshot.json").write_text(json.dumps(frozen, indent=2) + "\n")
        report["source_snapshot_sha256"] = sha((evidence / "source-snapshot.json").read_bytes())
        report["module_count"] = len(order)
        report["generic_module_count"] = len(set(order) & mapping["modules"].keys())
        report["generated_manifest_modules_not_in_selected_closure"] = sorted(set(manifest["sources"]) - set(order))
        report["build_order"] = order
        save()
        print("FROZEN", "modules=" + str(len(order)), "generic=" + str(report["generic_module_count"]), flush=True)
        if args.canonical:
            # Only source bytes and registry data are prepared here. All Lean
            # compilation and the full axiom audit below are performed by the
            # untouched canonical checker, reached through its untouched wrapper.
            report["jobs"] = 1
            report["verification_backend"] = "unchanged repository canonical verifier through unchanged original-layout replay wrapper"
            global_map_bytes = git("show", frozen_head + ":proofs/SOURCE_MAP.json")
            global_map = json.loads(global_map_bytes)
            selected_map, additions, registry_modules = {}, {}, {}
            stage = build / "canonical-source"
            clone = subprocess.run(["git", "clone", "--shared", "--no-checkout", str(repo), str(stage)], capture_output=True, text=True)
            (logs / "canonical-source-clone.log").write_text(clone.stdout + clone.stderr)
            if clone.returncode:
                raise RuntimeError("Cannot prepare isolated canonical source repository")
            subprocess.run(["git", "-C", str(stage), "update-ref", "HEAD", frozen_head], check=True)

            def stage_file(relative: str, data: bytes) -> None:
                path = stage / relative
                if Path(relative).is_absolute() or not path.resolve().is_relative_to(stage):
                    raise ValueError("Unsafe staged source path")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)

            verifier_origins = {}
            for relative in ("proofs/verify_project.py", "proofs/replay_original_layout.py"):
                data = git("show", frozen_head + ":" + relative)
                blob = git("rev-parse", frozen_head + ":" + relative).decode().strip()
                stage_file(relative, data)
                verifier_origins[relative] = {"source_ref": frozen_head, "git_blob": blob, "sha256": sha(data)}
            verifier_info = global_map["paths"]["proofs/verify_project.py"]
            verifier_selected = verifier_info.get("current") or verifier_info["preserved"]
            verifier_bytes = git("show", frozen_head + ":" + verifier_selected)
            if sha(verifier_bytes) != verifier_info["sha256"]:
                raise ValueError("Canonical backend differs from its preserved map")
            stage_file(verifier_selected, verifier_bytes)
            selected_map["proofs/verify_project.py"] = verifier_info
            verifier_origins["canonical_backend"] = {"source_ref": frozen_head, "source_path": verifier_selected, "git_blob": git("rev-parse", frozen_head + ":" + verifier_selected).decode().strip(), "sha256": sha(verifier_bytes), "original_replay_path": "proofs/verify_project.py"}
            for name in order:
                rec = records[name]
                if name in mapping["modules"]:
                    old = mapping["modules"][name]
                    target_path = old.get("preserved_original_path")
                    if target_path is None:
                        parts = Path(old["source_path"]).parts
                        if parts[:3] != ("proofs", "archive", "versions"):
                            raise ValueError("Unknown generic origin layout")
                        target_path = str(Path(*parts[4:]))
                else:
                    target_path = rec["source_path"]
                blob = hashlib.sha1(f"blob {len(snapshots[name])}\0".encode() + snapshots[name]).hexdigest()
                if target_path in global_map["paths"]:
                    map_rec = global_map["paths"][target_path]
                    if map_rec["sha256"] != rec["sha256"] or map_rec["oid"] != blob:
                        raise ValueError("Existing canonical source map conflicts with selected version: " + name)
                else:
                    map_rec = {"current": rec["source_path"], "preserved": rec["source_path"], "sha256": rec["sha256"], "mode": "100644", "oid": blob}
                    additions[target_path] = map_rec
                selected_map[target_path] = map_rec
                stage_file(map_rec.get("current") or map_rec["preserved"], snapshots[name])
                registry_modules[name] = {"path": target_path, "sha256": rec["sha256"], "git_blob": blob, "imports": rec["imports"]}
            stage_map = {"base": global_map["base"], "paths": selected_map}
            stage_file("proofs/SOURCE_MAP.json", (json.dumps(stage_map, indent=2) + "\n").encode())
            (evidence / "SOURCE_MAP_ADDITIONS.json").write_text(json.dumps({"base": global_map["base"], "paths": additions}, indent=2) + "\n")
            (evidence / "CANONICAL_REPLAY_SOURCE_MAP.json").write_text(json.dumps(stage_map, indent=2) + "\n")
            project = "agent104-prefix620-kernel"
            registry = {"schema_version": 1, "toolchain": {"lean_version": "4.19.0", "allowed_axioms": ["propext", "Classical.choice", "Quot.sound"]}, "catalogue_complete": False, "catalogue_blockers": ["This standalone registry covers only the selected Agent #104 prefix620 certificate closure and does not establish repository-wide coverage."], "projects": {project: {"scope": "Exact selected 620-prefix certificate endpoint closure; see exported theorem types for all quantifiers and hypotheses.", "roots": args.root_module, "modules": registry_modules}}, "claims": [{"id": "agent104-prefix620-endpoints", "project": project, "endpoints": args.endpoint}]}
            registry_path = evidence / "REGISTRY.json"
            registry_path.write_text(json.dumps(registry, indent=2) + "\n")
            canonical_out = build / "canonical-verification"
            report["canonical"] = {"verifier_origins": verifier_origins, "source_stage": str(stage), "output": str(canonical_out), "project": project, "registry_sha256": sha(registry_path.read_bytes()), "replay_source_map_sha256": sha((evidence / "CANONICAL_REPLAY_SOURCE_MAP.json").read_bytes()), "source_map_additions_sha256": sha((evidence / "SOURCE_MAP_ADDITIONS.json").read_bytes()), "canonical_report_agent_literal_identifies_upstream_checker": "Agent #1", "execution_actor": "Agent #104 runtime_scout"}
            save()
            print("CANONICAL_START", "modules=" + str(len(order)), "output=" + str(canonical_out), flush=True)
            canonical_argv = [sys.executable, "-B", str(stage / "proofs/verify_project.py"), "--lean", str(lean), "--registry", str(registry_path), "--project", project, "--output", str(canonical_out)]
            if args.source_check_only:
                canonical_argv.append("--check-only")
            canonical_log = record_command("canonical-verifier", canonical_argv, timeout_seconds=None)
            canonical_result = json.loads((canonical_out / "verification.json").read_text())
            result = canonical_result["projects"][project]
            if args.source_check_only:
                if canonical_result["status"] != "SOURCE_AND_IMPORT_CHECK_ONLY" or result["status"] != "SOURCE_AND_IMPORT_CHECK_ONLY" or result["commands"]:
                    raise ValueError("Canonical source-only check returned an unexpected classification")
                report["canonical"]["report_sha256"] = sha((canonical_out / "verification.json").read_bytes())
                report["compiled_module_count"] = 0
                report["mathematical_proof_check"] = False
                report["status"] = "PASS_CANONICAL_SOURCE_IMPORT_CHECK_ONLY"
                print(report["status"], "modules=" + str(len(order)), flush=True)
                return 0
            if canonical_result["status"] != "PASS" or result["status"] != "PASS" or canonical_result.get("repository_wide_pass"):
                raise ValueError("Canonical verifier did not return the intended scoped PASS")
            commands = result["commands"]
            if len(commands) != len(order) + 1 or [item["label"] for item in commands[:-1]] != order or commands[-1]["label"] != "ProjectAudit" or any(item["exit_code"] for item in commands):
                raise ValueError("Canonical execution does not contain every new module build and the final audit")
            if result["endpoints"] != args.endpoint:
                raise ValueError("Canonical endpoint coverage mismatch")
            for name, data in snapshots.items():
                actual = canonical_out / project / "source" / (name + ".lean")
                if actual.read_bytes() != data or current_sources[name].read_bytes() != data:
                    raise ValueError("Selected source changed during canonical replay: " + name)
            for path, digest in {**input_hashes, **report["compiler"]["files"]}.items():
                if sha(Path(path).read_bytes()) != digest:
                    raise ValueError("Verifier input or compiler changed during canonical replay: " + path)
            if sha(registry_path.read_bytes()) != report["canonical"]["registry_sha256"]:
                raise ValueError("Registry changed during canonical verification")
            workspace = re.findall(r"Original-layout check workspace \(retained\): ([^\n]+)", canonical_log)
            report["canonical"]["replayed_source_workspaces"] = workspace
            report["canonical"]["report_sha256"] = sha((canonical_out / "verification.json").read_bytes())
            report["canonical"]["source_commit_is_replay_baseline"] = canonical_result["source_commit"]
            report["canonical"]["source_tree_clean"] = canonical_result["source_tree_clean"]
            report["compiled_module_count"] = len(order)
            report["theorem_count"] = result["theorem_count"]
            report["axiom_union"] = result["axiom_union"]
            report["unsafe_implementation_axioms"] = result["unsafe_implementation_axioms"]
            retained = evidence / "canonical"
            retained.mkdir(exist_ok=False)
            retained_files = {}
            raw_evidence = [canonical_out / "verification.json", canonical_out / "FILES.json", canonical_out / project / "source/ProjectAudit.lean", *sorted((canonical_out / project / "logs").glob("*.log"))]
            for original in raw_evidence:
                relative = original.relative_to(canonical_out)
                destination = retained / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(original, destination)
                retained_files[str(destination.relative_to(evidence))] = {"sha256": sha(destination.read_bytes()), "bytes": destination.stat().st_size, "original_execution_path": str(original)}
            (evidence / "CANONICAL_RETAINED_FILES.json").write_text(json.dumps(retained_files, indent=2) + "\n")
            report["canonical"]["retained_raw_evidence"] = "CANONICAL_RETAINED_FILES.json"
            report["canonical"]["retained_raw_evidence_manifest_sha256"] = sha((evidence / "CANONICAL_RETAINED_FILES.json").read_bytes())
            report["status"] = "PASS_CANONICAL_SELECTED_620_CLOSURE"
            print(report["status"], "modules=" + str(len(order)), "theorems=" + str(report["theorem_count"]), flush=True)
            return 0
        env = {"PATH": str(lean.parent) + ":/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "LEAN_PATH": str(build)}
        pending, done, running = list(order), set(), {}
        failed = []
        with futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            while pending or running:
                if not failed:
                    ready = [name for name in pending if all(dep not in records or dep in done for dep in records[name]["imports"])]
                    for name in ready[:args.jobs - len(running)]:
                        pending.remove(name)
                        argv = [str(lean), "-j1", "-DElab.async=false", "-o", name + ".olean", name + ".lean"]
                        fut = pool.submit(command, "module-" + name, argv, env)
                        running[fut] = name
                if not running:
                    if failed:
                        raise RuntimeError("Failed module(s): " + ", ".join(failed))
                    raise ValueError("No schedulable module remains")
                completed, _ = futures.wait(running, return_when=futures.FIRST_COMPLETED)
                for fut in completed:
                    name = running.pop(fut)
                    rec = fut.result()
                    report["commands"].append(rec)
                    if rec["exit_code"]:
                        failed.append(name)
                        print("FAILED", name, "exit=" + str(rec["exit_code"]), flush=True)
                    else:
                        done.add(name)
                    report["compiled_module_count"] = len(done)
                    save()
                    if len(done) % 16 == 0 or name in args.root_module:
                        print("COMPILED", str(len(done)) + "/" + str(len(order)), name, flush=True)
            if failed:
                raise RuntimeError("Failed module(s): " + ", ".join(failed))
        audit = helper.audit_source(order)
        audit = audit.replace("import Agent124CodeCert\n", "\n".join("import " + root for root in args.root_module) + "\n", 1)
        endpoint_checks = "\n".join("#check " + name + "\n#print axioms " + name for name in args.endpoint)
        audit = audit.replace("run_cmd do\n", endpoint_checks + "\nrun_cmd do\n", 1)
        audit_name = "Agent104Prefix620IndependentAxiomAudit"
        (build / (audit_name + ".lean")).write_text(audit)
        (evidence / (audit_name + ".lean")).write_text(audit)
        audit_log = record_command("module-origin-axiom-audit", [str(lean), "-j1", "-DElab.async=false", audit_name + ".lean"], env)
        summaries = re.findall(r"^FULL_MODULE_AUDIT theorems=(\d+) union=([^\n]*)$", audit_log, re.M)
        declarations = re.findall(r"^AUDIT_THEOREM (\S+) (\S+) : (.*)$", audit_log, re.M)
        if len(summaries) != 1 or int(summaries[0][0]) != len(declarations) or not declarations or len({item[1] for item in declarations}) != len(declarations):
            raise ValueError("Incomplete module-origin audit")
        report["theorem_count"] = len(declarations)
        report["axiom_union"] = summaries[0][1]
        report["unsafe_implementation_axioms"] = re.findall(r"^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$", audit_log, re.M)
        report["outputs"] = {name: {"source_sha256": sha((build / (name + ".lean")).read_bytes()), "olean_sha256": sha((build / (name + ".olean")).read_bytes())} for name in order}
        for name, data in snapshots.items():
            if current_sources[name].read_bytes() != data or (build / (name + ".lean")).read_bytes() != data:
                raise ValueError("Source changed during independent rebuild: " + name)
        for path, digest in {**input_hashes, **report["compiler"]["files"]}.items():
            if sha(Path(path).read_bytes()) != digest:
                raise ValueError("Verifier input or toolchain changed during rebuild: " + path)
        report["status"] = "PASS_SELECTED_620_CLOSURE"
        print(report["status"], "modules=" + str(len(order)), "theorems=" + str(report["theorem_count"]), flush=True)
        return 0
    except Exception as exc:
        report["status"] = "FAIL"
        report["error"] = str(exc)
        (evidence / "failure.txt").write_text(traceback.format_exc())
        print("FAIL", str(exc), flush=True)
        return 1
    finally:
        report["finished_at_epoch"] = time.time()
        save()


if __name__ == "__main__":
    raise SystemExit(main())
