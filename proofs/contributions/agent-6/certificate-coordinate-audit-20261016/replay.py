#!/usr/bin/env python3
"""Replay only the pinned Agent6 certificate-coordinate project into a fresh output.

The repository verifier is invoked unchanged.  Its fresh twenty-module build and
module-origin theorem audit are followed by an explicit --trust=0 audit of every
public theorem in the three certificate modules.  Existing evidence is never
overwritten; the finite numerical experiments remain separately classified.
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
import sys
import time
import traceback

sys.dont_write_bytecode = True

TASK = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]
PROJECT = "agent6-certificate-coordinate-audit"
REGISTRY = TASK / "certificate.registry.json"
DEPENDENCIES = TASK / "DEPENDENCIES.json"
VERIFIER = ROOT / "proofs/verify_project__214bf7673efe116b.py"
# Adapted from prior Agent6 replay at remote commit 215ec5e5ad9d34259e5a1a5ce1430de8d6c53d73.
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def public_endpoints(registry: dict) -> list[str]:
    """Use the unchanged verifier's comment masker and include attributes."""
    spec = importlib.util.spec_from_file_location("agent6_pinned_verifier_parser", VERIFIER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load the pinned verifier's source parser")
    parser = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parser)
    project = registry["projects"][PROJECT]
    if project["roots"] != ["CertificateControls"] or len(project["modules"]) != 20:
        raise ValueError("The expected twenty-module CertificateControls closure changed")
    actual = []
    for name, record in project["modules"].items():
        if name not in {"CertificateCoordinates", "CertificateFilter", "CertificateControls"}:
            continue
        source = parser.local_path(ROOT, record["path"])
        code = parser.code_only(source.read_text())
        namespaces = re.findall(r"^namespace\s+(\S+)", code, re.M)
        if namespaces != ["Agent6." + name]:
            raise ValueError("Unexpected namespace structure in " + name)
        names = re.findall(
            r"^[ \t]*(?:@\[[^\]]*\]\s*)*theorem\s+([A-Za-z_][\w']*)", code, re.M
        )
        actual.extend(namespaces[0] + "." + endpoint for endpoint in names)
    listed = [endpoint for claim in registry["claims"] if claim["project"] == PROJECT
              for endpoint in claim.get("endpoints", [])]
    if not actual or len(set(actual)) != len(actual) or len(set(listed)) != len(listed):
        raise ValueError("Missing or duplicate public theorem endpoints")
    if set(actual) != set(listed):
        raise ValueError("Registry endpoints do not equal the attribute-aware source inventory")
    if any(not parser.NAME.fullmatch(endpoint) for endpoint in listed):
        raise ValueError("Invalid endpoint name")
    return listed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True,
                        help="Path to the official Lean 4.19.0 executable (commit 6caaee842e94)")
    parser.add_argument("--output", type=Path, required=True,
                        help="A new output directory; an existing path is rejected")
    args = parser.parse_args()
    lean, output = args.lean.resolve(), args.output.resolve()
    if output.exists():
        parser.error("--output must not already exist")
    if not lean.is_file():
        parser.error("--lean must name an existing executable file")
    dependencies = json.loads(DEPENDENCIES.read_text())
    if sha256(VERIFIER) != dependencies["repository_verifier"]["sha256"]:
        raise ValueError("The pinned repository verifier changed")
    if sha256(REGISTRY) != dependencies["registry"]["sha256"]:
        raise ValueError("The scoped registry changed")
    registry = json.loads(REGISTRY.read_text())
    endpoints = public_endpoints(registry)
    report = {
        "status": "RUNNING", "project": PROJECT, "repository_wide_pass": False,
        "started_at_epoch": time.time(), "runner_sha256": sha256(Path(__file__)),
        "registry_sha256": sha256(REGISTRY), "verifier_sha256": sha256(VERIFIER),
        "lean_executable": str(lean), "lean_executable_sha256": sha256(lean),
        "explicit_public_theorem_count": len(endpoints),
        "verifier_source_modified": False, "git_mutations": False,
        "numeric_experiments_run": False,
    }
    output_created = False
    try:
        command = [sys.executable, str(VERIFIER), "--lean", str(lean),
                   "--registry", str(REGISTRY), "--project", PROJECT,
                   "--output", str(output)]
        print("Running the unchanged verifier for " + PROJECT, flush=True)
        started = time.monotonic()
        verifier_env = dict(os.environ)
        verifier_env["GIT_OPTIONAL_LOCKS"] = "0"
        result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, env=verifier_env, check=False)
        output_created = output.is_dir()
        if output_created:
            verifier_log = output / "replay-verifier.log"
            verifier_log.write_bytes(result.stdout)
        print(result.stdout.decode("utf-8", errors="replace"), end="", flush=True)
        report["verifier_command"] = {
            "argv": command, "exit_code": result.returncode,
            "elapsed_seconds": time.monotonic() - started,
            "log_sha256": hashlib.sha256(result.stdout).hexdigest(),
        }
        if result.returncode:
            raise RuntimeError("The unchanged scoped verifier failed; retained output contains its diagnostics")
        verification = json.loads((output / "verification.json").read_text())
        if verification["status"] != "PASS" or verification["repository_wide_pass"]:
            raise ValueError("Expected scoped PASS without repository-wide acceptance")
        if set(verification["projects"]) != {PROJECT}:
            raise ValueError("Unexpected project selection in verifier output")

        source = output / PROJECT / "source"
        audit = output / "export-audit"
        audit.mkdir(exist_ok=False)
        audit_source = audit / "CertificateExportAudit.lean"
        audit_source.write_text(
            "import CertificateControls\nimport Lean\n"
            "set_option maxRecDepth 100000\nset_option maxHeartbeats 0\n\n"
            + "\n".join("#print axioms " + endpoint for endpoint in endpoints) + "\n"
        )
        audit_command = [str(lean), "--trust=0", "-j1", "-DElab.async=false", str(audit_source)]
        env = dict(os.environ)
        env["LEAN_PATH"] = str(source)
        print("Auditing all public certificate theorem exports with --trust=0", flush=True)
        started = time.monotonic()
        with (audit / "CertificateExportAudit.log").open("wb") as stream:
            audit_result = subprocess.run(audit_command, cwd=audit, env=env,
                                          stdout=stream, stderr=subprocess.STDOUT, check=False)
        log = audit / "CertificateExportAudit.log"
        report["export_audit_command"] = {
            "argv": audit_command, "lean_path": str(source),
            "exit_code": audit_result.returncode,
            "elapsed_seconds": time.monotonic() - started,
            "source_sha256": sha256(audit_source), "log_sha256": sha256(log),
        }
        if audit_result.returncode:
            raise RuntimeError("The trust-zero export audit failed; its raw log is retained")
        text = log.read_text()
        rows = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text)
        actual = {name: [axiom.strip() for axiom in axioms.split(",") if axiom.strip()]
                  for name, axioms in rows}
        without_axioms = re.findall(r"'([^']+)' does not depend on any axioms", text)
        if len(actual) != len(rows) or len(set(without_axioms)) != len(without_axioms):
            raise ValueError("Duplicate export audit records")
        if set(actual) & set(without_axioms):
            raise ValueError("Conflicting export audit records")
        actual.update({name: [] for name in without_axioms})
        if set(actual) != set(endpoints):
            raise ValueError("The export audit is incomplete")
        if any(not set(axioms) <= ALLOWED for axioms in actual.values()):
            raise ValueError("A public theorem uses a disallowed axiom")
        (audit / "exported-axioms.json").write_text(json.dumps(actual, indent=2) + "\n")
        report["exported_axioms"] = actual
        report["axiom_union"] = sorted({axiom for axioms in actual.values() for axiom in axioms})
        report["source_commit"] = verification["source_commit"]
        report["status"] = "PASS"
        print("PASS: scoped project build and all " + str(len(endpoints)) + " public theorem export audits", flush=True)
        return 0
    except Exception as error:
        report["status"] = "FAIL"
        report["error"] = str(error)
        if output_created:
            (output / "replay-failure.txt").write_text(traceback.format_exc())
        print("FAIL: " + str(error), file=sys.stderr, flush=True)
        return 1
    finally:
        if output_created:
            report["finished_at_epoch"] = time.time()
            (output / "replay-verification.json").write_text(json.dumps(report, indent=2) + "\n")
            files = {str(path.relative_to(output)): {"bytes": path.stat().st_size, "sha256": sha256(path)}
                     for path in sorted(output.rglob("*")) if path.is_file()
                     and path.suffix not in {".olean", ".ilean", ".o"}
                     and path.name != "REPLAY_FILES.json"}
            (output / "REPLAY_FILES.json").write_text(json.dumps(files, indent=2) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
