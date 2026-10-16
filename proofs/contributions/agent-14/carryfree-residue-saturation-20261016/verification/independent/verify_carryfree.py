#!/usr/bin/env python3
"""Verify the approved carryfree five-source closure without author objects.

The canonical verifier is copied unchanged into a minimal source snapshot.
Its two read-only Git metadata calls refer to the existing checkout through
explicit environment variables. That snapshot is not a complete repository or
a checkout of the published source checkpoint. Source identity is independently
established from SHA-256 and registered Git blob identities.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
import traceback

from audit_support import (
    ALLOWED, declared_public_names, digest, file_digest, masked_source, now,
    parse_public_axioms, parse_safe_audit, safe_audit_source,
)

BASE = Path(__file__).resolve().parent
MODULES = {
    "LychrelDigitSums",
    "Agent14CarryfreeResidues",
    "Agent14CarryfreeDigits",
    "Agent14CarryfreeCoordinates",
    "Agent14CarryfreeSaturation",
}
FIXED_PINS = {
    "LychrelDigitSums": "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57",
    "Agent14CarryfreeResidues": "7785adc325f7ae100cfcde21238f27d06a558c23d74a3fa03464ea356867ece6",
    "Agent14CarryfreeDigits": "ae394c8a19e6fc497c1cf83fdf77943abd3f0b8fd681e59006bc8f7524f4ece9",
    "Agent14CarryfreeCoordinates": "5c2b5b72f14b8f002719fa77b54b63aef1a2fa644dd379bdb94dec4b3dbfa519",
    "Agent14CarryfreeSaturation": "2427fcac82b20afe208ae2529b1dc9436217395eef63fcceb707447b0064171a",
}
VERIFIER_SHA256 = "c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a"
LEAN_SHA256 = "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023"
VERIFIER_NAME = "verify_project__214bf7673efe116b.py"
IDENTIFIER = re.compile(r"[A-Za-z_][\w']*(?:\.[A-Za-z_][\w']*)*\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
COMMIT = re.compile(r"[0-9a-f]{40}\Z")
FORBIDDEN = re.compile(r"\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b")


def relative_path(root, name):
    relative = Path(name)
    target = (root / relative).resolve()
    if relative.is_absolute() or not target.is_relative_to(root.resolve()):
        raise ValueError("Snapshot path escapes its root: " + name)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(BASE) or output == BASE:
        raise ValueError("All execution evidence must remain in this specialist's directory")
    output.mkdir(parents=True, exist_ok=False)
    logs = output / "logs"
    logs.mkdir()
    stage = output / "source"
    stage.mkdir()
    snapshot = output / "input-snapshot"
    snapshot.mkdir()
    lean = args.lean.resolve(strict=True)
    contract_path = args.contract.resolve(strict=True)
    report = {
        "schema_version": 1,
        "executed_by": "Agent #14 / independent runtime specialist",
        "status": "RUNNING",
        "started_at": now(),
        "source_authorship": "Independent execution and audits only; no mathematical source authored",
        "execution_mode": "Authorized require_escalated, own memory-backed workspace, unmodified runtime",
        "repository_wide_pass": False,
        "whole_repository_checkout_claimed": False,
        "published_checkpoint_checkout_claimed": False,
        "author_project_objects_reused": False,
        "independent_lean_flags": ["--trust=0", "-j1", "-DElab.async=false"],
        "sources": {},
        "commands": [],
    }

    def save():
        (output / "verification.json").write_text(json.dumps(report, indent=2) + "\n")

    environment = {
        "PATH": str(lean.parent) + os.pathsep + os.defpath,
        "LANG": "C.UTF-8",
        "LEAN_PATH": str(stage),
    }

    def run(label, command, cwd, command_environment=None, timeout_seconds=1800):
        log = logs / (label + ".log")
        started_at = now()
        started = time.monotonic()
        with log.open("xb") as stream:
            process = subprocess.Popen(
                command, cwd=cwd, env=command_environment or environment,
                stdout=stream, stderr=subprocess.STDOUT, start_new_session=True,
            )
            timed_out = False
            try:
                code = process.wait(timeout=timeout_seconds)
            except subprocess.TimeoutExpired:
                timed_out = True
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=5)
                code = 124
        record = {
            "label": label, "argv": command, "cwd": str(cwd),
            "started_at": started_at, "finished_at": now(),
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "timeout_seconds": timeout_seconds, "timed_out": timed_out,
            "exit_code": code, "process_returncode": process.returncode,
            "log": str(log.relative_to(output)), "log_sha256": file_digest(log),
        }
        report["commands"].append(record)
        save()
        print(label, "exit=" + str(code), flush=True)
        if code != 0:
            raise RuntimeError("Command failed: " + label)
        return log.read_text()

    try:
        infrastructure = output / "verification-infrastructure"
        infrastructure.mkdir()
        infrastructure_inputs = [
            BASE / "verify_carryfree.py",
            BASE / "audit_support.py",
            BASE / "infrastructure" / VERIFIER_NAME,
        ]
        infrastructure_pins = {}
        for path in infrastructure_inputs:
            data = path.read_bytes()
            (infrastructure / path.name).write_bytes(data)
            infrastructure_pins[str(path)] = digest(data)
        report["infrastructure_sha256"] = infrastructure_pins
        if infrastructure_pins[str(BASE / "infrastructure" / VERIFIER_NAME)] != VERIFIER_SHA256:
            raise ValueError("Canonical verifier identity changed")

        contract_bytes = contract_path.read_bytes()
        contract = json.loads(contract_bytes)
        (output / "approved-contract.snapshot.json").write_bytes(contract_bytes)
        report["contract_sha256"] = digest(contract_bytes)
        additional_frozen_inputs = {}
        for kind in ["author_source_freeze", "mathematical_contract"]:
            pin = contract[kind]
            path = Path(pin["path"]).resolve(strict=True)
            data = path.read_bytes()
            if digest(data) != pin["sha256"]:
                raise ValueError("Additional frozen input differs from its approved pin: " + kind)
            retained = output / (kind + ".snapshot" + path.suffix)
            retained.write_bytes(data)
            additional_frozen_inputs[kind] = (path, data)
            report[kind] = {"path": str(path), "sha256": digest(data),
                            "bytes": len(data), "snapshot": retained.name}
        if contract.get("schema_version") != 1 or contract.get("status") != "FROZEN_SOURCE_INPUTS_APPROVED":
            raise ValueError("No final approved frozen-input contract")
        if set(contract["sources"]) != MODULES:
            raise ValueError("The contract is not the assigned five-module closure")
        for module, sha in FIXED_PINS.items():
            if contract["sources"][module]["sha256"] != sha:
                raise ValueError("Previously frozen source pin changed: " + module)
        for module, rec in contract["sources"].items():
            if not SHA256.fullmatch(rec["sha256"]):
                raise ValueError("Missing full approved source SHA-256: " + module)
        project_name = contract["project"]
        if not IDENTIFIER.fullmatch(project_name.replace("-", "_")):
            raise ValueError("Invalid project name")
        reservation = contract.get("reservation_commit")
        checkpoint = contract.get("published_source_checkpoint")
        if not COMMIT.fullmatch(reservation or "") or (checkpoint is not None and not COMMIT.fullmatch(checkpoint)):
            raise ValueError("Malformed reservation or publication identifier")
        report["reservation_commit"] = reservation
        report["published_source_checkpoint"] = checkpoint
        report["source_checkpoint_binding"] = (
            "The parent's published checkpoint assertion is tied to the exact retained source hashes. "
            "This specialist does not independently fetch or check out that checkpoint."
            if checkpoint else
            "No publication commit was asserted at execution time; exact source SHA-256 and registered Git blob identities are retained."
        )
        registry_path = Path(contract["registry"]["path"]).resolve(strict=True)
        registry_bytes = registry_path.read_bytes()
        if digest(registry_bytes) != contract["registry"]["sha256"]:
            raise ValueError("Approved registry hash mismatch")
        registry = json.loads(registry_bytes)
        (output / "registry.snapshot.json").write_bytes(registry_bytes)
        report["registry_sha256"] = digest(registry_bytes)
        if registry["schema_version"] != 1 or set(registry["toolchain"]["allowed_axioms"]) != ALLOWED:
            raise ValueError("Registry schema or axiom policy differs from the accepted contract")
        if registry["toolchain"]["version"] != "4.19.0" or registry["toolchain"]["commit"] != "6caaee842e94":
            raise ValueError("Registry toolchain pin changed")
        project = registry["projects"][project_name]
        records = project["modules"]
        parent_freeze = json.loads(additional_frozen_inputs["author_source_freeze"][1])
        if parent_freeze["modules"] != records or parent_freeze["project"] != project_name:
            raise ValueError("Parent source-freeze manifest disagrees with the execution registry")
        if parent_freeze["contract_sha256"] != report["mathematical_contract"]["sha256"]:
            raise ValueError("Parent source-freeze manifest disagrees with the mathematical contract")
        if set(records) != MODULES or project["roots"] != ["Agent14CarryfreeSaturation"]:
            raise ValueError("The registry is not the assigned exact root closure")
        if contract["roots"] != project["roots"]:
            raise ValueError("Approved roots and registry roots disagree")
        report["project"] = project_name
        report["scope"] = project["scope"]
        report["catalogue_complete"] = registry["catalogue_complete"]
        originals, source_paths, imports = {}, {}, {}
        public = []
        for module, rec in records.items():
            if rec.get("adapter"):
                raise ValueError("No source adapter is authorized for this closure")
            path = Path(contract["sources"][module]["path"]).resolve(strict=True)
            data = path.read_bytes()
            sha = digest(data)
            blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
            if sha != rec["sha256"] or sha != contract["sources"][module]["sha256"] or blob != rec["git_blob"]:
                raise ValueError("Frozen source or registered blob mismatch: " + module)
            code = masked_source(data.decode())
            if FORBIDDEN.search(code):
                raise ValueError("Forbidden source token in " + module)
            deps = [name for line in re.findall(r"^\s*import\s+([^\n]+)", code, re.M) for name in line.split()]
            if deps != rec["imports"] or any(dep not in records and dep not in {"Std", "Init", "Lean"} for dep in deps):
                raise ValueError("Unregistered import in " + module)
            destination = relative_path(snapshot, rec["path"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            originals[module], source_paths[module], imports[module] = data, path, deps
            report["sources"][module] = {
                "original_path": str(path), "registered_path": rec["path"],
                "sha256": sha, "git_blob": blob, "bytes": len(data), "imports": deps,
            }
            if module.startswith("Agent14"):
                public.extend(declared_public_names(module, code))
        public_names = [rec["name"] for rec in public]
        if len(set(public_names)) != len(public_names):
            raise ValueError("Duplicate explicit public names across modules")
        endpoints = [name for claim in registry["claims"] if claim["project"] == project_name for name in claim.get("endpoints", [])]
        if not endpoints or len(set(endpoints)) != len(endpoints) or not set(endpoints) <= set(public_names):
            raise ValueError("The registered endpoints are absent, duplicated or not covered by the public source audit")
        report["public_declarations"] = public
        if len(endpoints) != parent_freeze["endpoint_count"] or len(endpoints) != 22:
            raise ValueError("Final approved endpoint count differs from the registry")
        report["claim_endpoints"] = endpoints
        order, visited, active = [], set(), set()

        def visit(module):
            if module not in records or module in visited:
                return
            if module in active:
                raise ValueError("Cyclic import closure")
            active.add(module)
            for dep in imports[module]:
                visit(dep)
            active.remove(module)
            visited.add(module)
            order.append(module)

        for root in project["roots"]:
            visit(root)
        if visited != MODULES:
            raise ValueError("A registered source is outside the selected root closure")
        report["build_order"] = order

        snapshot_verifier = snapshot / "proofs" / VERIFIER_NAME
        snapshot_verifier.parent.mkdir(exist_ok=True)
        snapshot_verifier.write_bytes((BASE / "infrastructure" / VERIFIER_NAME).read_bytes())
        snapshot_registry = snapshot / "proofs" / "Agent14Carryfree.registry.json"
        snapshot_registry.write_bytes(registry_bytes)
        if file_digest(snapshot_verifier) != VERIFIER_SHA256:
            raise ValueError("Copied canonical verifier changed")
        version = run("lean-version", [str(lean), "--version"], output).strip()
        if version != "Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)":
            raise ValueError("Unexpected Lean version")
        prefix = Path(run("lean-prefix", [str(lean), "--print-prefix"], output).strip()).resolve()
        runtime_pins = {str(path): file_digest(path) for path in [lean, *sorted((prefix / "lib/lean").glob("*.so"))]}
        if runtime_pins[str(lean)] != LEAN_SHA256:
            raise ValueError("Lean executable differs from the independently verified official distribution")
        report["runtime"] = {
            "lean": str(lean), "prefix": str(prefix), "version": version, "files": runtime_pins,
            "provenance": "Unmodified Lean 4.19.0 distribution independently compared to all 4,617 release archive members earlier in this session; no runtime copy or new download",
            "official_archive_sha256": "6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe",
        }
        git_metadata = contract["git_metadata"]
        git_dir = Path(git_metadata["git_dir"]).resolve(strict=True)
        git_work_tree = Path(git_metadata["work_tree"]).resolve(strict=True)
        if not git_dir.is_dir() or not git_work_tree.is_dir():
            raise ValueError("Existing read-only Git metadata directory is unavailable")
        canonical_environment = dict(environment)
        canonical_environment.update({
            "GIT_DIR": str(git_dir), "GIT_WORK_TREE": str(git_work_tree),
            "GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
        })
        report["canonical_metadata_context"] = {
            "git_dir": str(git_dir), "git_work_tree": str(git_work_tree),
            "git_optional_locks": "0",
            "operations": ["git rev-parse HEAD", "git status --porcelain --untracked-files=no"],
            "interpretation": "These unchanged canonical report fields describe the existing checkout, not the minimal snapshot or the published source checkpoint. The clean field excludes untracked files.",
            "git_mutations_requested": False,
        }
        canonical = output / "canonical"
        run("canonical-verifier", [
            sys.executable, "-B", str(snapshot_verifier), "--registry", str(snapshot_registry),
            "--project", project_name, "--lean", str(lean), "--output", str(canonical),
        ], snapshot, canonical_environment, timeout_seconds=3600)
        canonical_report = json.loads((canonical / "verification.json").read_text())
        canonical_project = canonical_report["projects"][project_name]
        if canonical_report["status"] != "PASS" or canonical_project["status"] != "PASS" or canonical_report["repository_wide_pass"]:
            raise ValueError("The unchanged canonical verifier did not report the expected scoped PASS")
        canonical_commands = canonical_project["commands"]
        if [rec["label"] for rec in canonical_commands] != order + ["ProjectAudit"]:
            raise ValueError("Canonical command coverage differs from the exact closure")
        for rec in canonical_commands:
            if rec["exit_code"] != 0 or rec["argv"][1:3] != ["-j1", "-DElab.async=false"] or any(arg.startswith("--trust") for arg in rec["argv"]):
                raise ValueError("Canonical compiler command unexpectedly changed")
        report["canonical"] = {
            "status": "PASS", "verifier_unmodified": True, "verifier_sha256": VERIFIER_SHA256,
            "trust_zero_flag": False, "actual_flags": ["-j1", "-DElab.async=false"],
            "report": "canonical/verification.json",
            "metadata_checkout_head": canonical_report["source_commit"],
            "metadata_checkout_tracked_clean": canonical_report["source_tree_clean"],
            "legacy_agent_field": "Agent #1 is retained from the historical verifier; the actual executor is Agent #14/runtime",
            "project_objects_reused": False,
        }
        for name, rec in json.loads((canonical / "FILES.json").read_text()).items():
            path = relative_path(canonical, name)
            if path.stat().st_size != rec["bytes"] or file_digest(path) != rec["sha256"]:
                raise ValueError("Canonical evidence manifest does not match its retained files")
        save()

        for module in order:
            (stage / (module + ".lean")).write_bytes(originals[module])
        object_count = sum(path.suffix in {".olean", ".ilean", ".o"} for path in stage.rglob("*"))
        report["fresh_object_count_before_independent_build"] = object_count
        if object_count:
            raise ValueError("A local project object exists before the independent build")
        flags = [str(lean), "--trust=0", "-j1", "-DElab.async=false"]
        for module in order:
            run("build-" + module, flags + ["-o", module + ".olean", module + ".lean"], stage)
        audit_path = stage / "SafeConstantAudit.lean"
        audit_path.write_text(safe_audit_source(order, project["roots"]))
        audit_log = run("safe-constant-audit", flags + [audit_path.name], stage)
        constants, safe_summary, unsafe, partial = parse_safe_audit(audit_log)
        if {rec["module"] for rec in constants} != MODULES:
            raise ValueError("Safe-constant audit does not cover every module origin")
        if any(rec[0] not in MODULES for rec in unsafe + partial):
            raise ValueError("Implementation inventory contains an unselected module")
        constants_by_name = {rec["name"]: rec for rec in constants}
        for declaration in public:
            name = declaration["name"]
            if name not in constants_by_name or constants_by_name[name]["module"] != declaration["module"]:
                raise ValueError("An explicit public declaration is absent, unsafe, partial or has an unexpected module origin")
        if safe_summary["theorem"] != canonical_project["theorem_count"]:
            raise ValueError("Independent and canonical theorem counts disagree")
        canonical_audit_text = (canonical / project_name / "logs" / "ProjectAudit.log").read_text()
        canonical_theorems = {
            name for _module, name in re.findall(r"^AUDIT_THEOREM (\S+) (\S+) : ", canonical_audit_text, re.M)
        }
        if canonical_theorems != {rec["name"] for rec in constants if rec["kind"] == "theorem"}:
            raise ValueError("Independent and canonical theorem identity sets disagree")
        (output / "safe-constants.json").write_text(json.dumps(constants, indent=2) + "\n")
        (output / "implementation-inventory.json").write_text(json.dumps({"unsafe": unsafe, "partial": partial}, indent=2) + "\n")
        public_source = "\n".join("import " + name for name in project["roots"]) + "\n"
        public_source += "set_option pp.fullNames true\nset_option pp.universes true\nset_option pp.explicit true\n"
        for name in public_names:
            public_source += "#check @" + name + "\n#print axioms " + name + "\n"
        public_path = stage / "PublicDeclarationAudit.lean"
        public_path.write_text(public_source)
        public_log = run("public-types-and-axioms", flags + [public_path.name], stage)
        public_axioms = parse_public_axioms(public_log, public_names)
        for name, axioms in public_axioms.items():
            if set(axioms) != set(constants_by_name[name]["axioms"]):
                raise ValueError("Literal public axiom output disagrees with the exhaustive safe audit: " + name)
        (output / "public-axioms.json").write_text(json.dumps(public_axioms, indent=2) + "\n")

        for module, data in originals.items():
            if source_paths[module].read_bytes() != data:
                raise ValueError("Original approved source changed during execution: " + module)
            if relative_path(snapshot, records[module]["path"]).read_bytes() != data:
                raise ValueError("Canonical input snapshot changed during execution: " + module)
            if (stage / (module + ".lean")).read_bytes() != data:
                raise ValueError("Strict source snapshot changed during execution: " + module)
        if registry_path.read_bytes() != registry_bytes or snapshot_registry.read_bytes() != registry_bytes:
            raise ValueError("Registry changed during execution")
        for kind, (path, data) in additional_frozen_inputs.items():
            if path.read_bytes() != data:
                raise ValueError("Additional frozen input changed during execution: " + kind)
        if contract_path.read_bytes() != contract_bytes:
            raise ValueError("Approved input contract changed during execution")
        if any(file_digest(Path(path)) != sha for path, sha in runtime_pins.items()):
            raise ValueError("Runtime changed during execution")
        if any(file_digest(Path(path)) != sha for path, sha in infrastructure_pins.items()):
            raise ValueError("Verification infrastructure changed during execution")
        if file_digest(snapshot_verifier) != VERIFIER_SHA256:
            raise ValueError("Canonical verifier snapshot changed during execution")
        report["safe_audit"] = safe_summary
        report["public_type_and_axiom_count"] = len(public_axioms)
        report["public_source_declaration_count"] = len(public_names)
        report["claim_endpoint_count"] = len(endpoints)
        report["independent_and_canonical_theorem_sets_equal"] = True
        report["objects"] = {
            path.name: {"bytes": path.stat().st_size, "sha256": file_digest(path)}
            for path in sorted(stage.glob("*.olean"))
        }
        report["status"] = "INDEPENDENT_BUILD_AND_AXIOM_PASS"
        report["semantic_review"] = "Separate specialist task; this receipt records execution, exact identities, public signatures and dependency audits"
        return 0
    except Exception as exc:
        report["status"] = "BLOCKED_DISK" if isinstance(exc, OSError) and exc.errno == 28 else "FAIL"
        report["error"] = repr(exc)
        report["traceback"] = traceback.format_exc()
        print(report["traceback"], flush=True)
        return 1
    finally:
        report["finished_at"] = now()
        try:
            save()
            files = {}
            for path in sorted(output.rglob("*")):
                if not path.is_file() or path.is_symlink() or path.suffix in {".olean", ".ilean", ".o", ".pyc"} or path == output / "FILES.json":
                    continue
                files[str(path.relative_to(output))] = {"bytes": path.stat().st_size, "sha256": file_digest(path)}
            (output / "FILES.json").write_text(json.dumps(files, indent=2) + "\n")
        except OSError as exc:
            print("Could not preserve all final evidence:", repr(exc), flush=True)
        print(json.dumps({
            key: report.get(key) for key in [
                "status", "error", "safe_audit", "public_type_and_axiom_count", "claim_endpoint_count",
            ]
        }, indent=2), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
