#!/usr/bin/env python3
"""Agent #14 M99-A04: isolated, source-pinned Lean replay (Python 3.10+).

AUTHORING STATUS: UNEXECUTED. This script is not an execution receipt.
It reads existing Git blobs, never fetches the network, never changes the
repository, never reuses project objects, and never launches parallel jobs.

Usage:
  python3 Agent14M99A04Replay.py --self-test
  python3 Agent14M99A04Replay.py --repo /path/to/p196-algorithm \
    --lean /trusted/lean-4.19.0-linux/bin/lean --output /new/outside-repo/path
An independently authenticated compiler digest may additionally be enforced
with --expected-lean-sha256. A version string alone is not authentication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
import unittest

ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
CRITICAL_ENDPOINTS = frozenset({
    "Agent112.TwoPhase.actual_prefix_transport",
    "Agent112.TwoPhase.uniform_band_tail",
    "Agent112.TwoPhase.actual_spatial_step",
    "Agent112.TwoPhase.actual_outside",
    "Agent112.TwoPhase.no_actual_persistent_alternating_band",
    "Agent112.TwoPhase.Numeric.numeric_representation",
    "Agent112.TwoPhase.Numeric.no_numeric_persistent_alternating_band",
    "Agent112.TwoPhase.Numeric.phase_alone_not_overflow_alternation",
    "Agent14.M99A04Review.numeric_endpoint_matches",
})


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git_blob(repo: Path, sha: str) -> bytes:
    require(re.fullmatch(r"[0-9a-f]{40}", sha) is not None, "Invalid Git blob identifier")
    p = subprocess.run(["git", "-C", str(repo), "cat-file", "blob", sha],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    require(p.returncode == 0, "Required pinned Git blob is absent: " + sha)
    require(blob_id(p.stdout) == sha, "Git blob identity mismatch: " + sha)
    return p.stdout


def parse_axioms(text: str, expected: list[str]) -> dict[str, list[str]]:
    """Require one actual Lean axiom answer for each requested endpoint."""
    require(len(expected) == len(set(expected)), "Duplicate required audit endpoint")
    answers: dict[str, list[str]] = {}
    pattern = re.compile(
        r"^'([^'\n]+)' (?:does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])",
        re.MULTILINE,
    )
    for match in pattern.finditer(text):
        name = match.group(1)
        if name not in expected:
            continue
        require(name not in answers, "Duplicate axiom answer: " + name)
        axioms = [x.strip() for x in (match.group(2) or "").split(",") if x.strip()]
        require(set(axioms) <= ALLOWED_AXIOMS, "Disallowed transitive axioms: " + name + ": " + repr(axioms))
        answers[name] = sorted(axioms)
    missing = sorted(set(expected) - set(answers))
    require(not missing, "Missing axiom answers: " + repr(missing))
    return answers


class AuditParserTests(unittest.TestCase):
    def test_empty_and_multiline(self) -> None:
        text = "'a' does not depend on any axioms\n'b' depends on axioms: [propext,\n Quot.sound]\n"
        self.assertEqual(parse_axioms(text, ["a", "b"]), {"a": [], "b": ["Quot.sound", "propext"]})

    def test_missing_is_failure(self) -> None:
        with self.assertRaises(ValueError):
            parse_axioms("'a' does not depend on any axioms\n", ["a", "b"])

    def test_forbidden_is_failure(self) -> None:
        for forbidden in ["sorryAx", "Lean.ofReduceBool", "customClaim"]:
            with self.assertRaises(ValueError):
                parse_axioms("'a' depends on axioms: [" + forbidden + "]\n", ["a"])

    def test_duplicate_is_failure(self) -> None:
        with self.assertRaises(ValueError):
            parse_axioms("'a' does not depend on any axioms\n" * 2, ["a"])


def replay(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve(strict=True)
    supplied_lean = Path(args.lean)
    require(supplied_lean.is_absolute(), "--lean must be an absolute trusted compiler path")
    lean = supplied_lean.resolve(strict=True)
    require(lean.is_file() and os.access(lean, os.X_OK), "Compiler is not executable")
    output = Path(args.output).resolve()
    require(not output.exists(), "Output must not already exist; no cached rebuilds are accepted")
    require(not output.is_relative_to(repo), "Output must be outside the repository")
    manifest_path = Path(args.manifest).resolve(strict=True)
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    require(manifest.get("schema_version") == 1, "Unsupported manifest schema")
    require(set(manifest["allowed_axioms"]) == ALLOWED_AXIOMS, "Axiom policy may not be weakened")
    require(manifest["compiler_arguments"] == ["-j1", "-DElab.async=false"], "Unexpected compiler arguments")
    endpoints = manifest["endpoints"]
    require(len(endpoints) == 25 and len(set(endpoints)) == 25, "Expected 19 source endpoints and six regression endpoints")
    require(CRITICAL_ENDPOINTS <= set(endpoints), "A critical endpoint was omitted")
    require(all(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", n) for n in endpoints), "Invalid endpoint identifier")
    modules = manifest["modules"]
    require(len(modules) == 8, "Exactly the pinned eight-module source closure is required")
    entries = modules + [manifest["scope_fixture"]]
    names = [m["module"] for m in entries]
    require(len(names) == len(set(names)), "Duplicate module name")
    require(all(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", n) for n in names), "Invalid module name")

    output.mkdir(parents=True, exist_ok=False)
    build = output / "build"
    logs = output / "logs"
    build.mkdir()
    logs.mkdir()
    (output / "manifest.json").write_bytes(manifest_bytes)
    (output / "replay_driver.py").write_bytes(Path(__file__).read_bytes())
    report: dict = {
        "status": "RUNNING", "started_at": now(), "inspected_main": manifest["inspected_main"],
        "manifest_sha256": digest(manifest_bytes), "driver_sha256": digest(Path(__file__).read_bytes()),
        "compiler_path": str(lean), "compiler_sha256": digest(lean.read_bytes()),
        "expected_compiler_digest_supplied": bool(args.expected_lean_sha256),
        "compiler_authentication": "Caller must provide a trusted installation; version matching is not authentication",
        "project_object_reuse": False, "commands": [], "sources": [],
        "integration_claimed": False, "new_mathematical_discovery_claimed": False,
    }
    env = dict(os.environ)
    env.pop("LEAN_SYSROOT", None)
    env["LEAN_PATH"] = str(build)

    def checkpoint() -> None:
        (output / "verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    def run(label: str, command: list[str]) -> str:
        started = time.monotonic()
        stamp = now()
        try:
            p = subprocess.run(command, cwd=build, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, timeout=args.timeout)
            data, code, timed_out = p.stdout, p.returncode, False
        except subprocess.TimeoutExpired as exc:
            data, code, timed_out = exc.stdout or b"", None, True
            if isinstance(data, str):
                data = data.encode("utf-8")
        log = logs / (label + ".log")
        log.write_bytes(data)
        report["commands"].append({
            "label": label, "command": command, "cwd": str(build), "LEAN_PATH": str(build),
            "started_at": stamp, "seconds": round(time.monotonic() - started, 6),
            "exit_code": code, "timed_out": timed_out, "log": str(log.relative_to(output)),
            "log_sha256": digest(data),
        })
        checkpoint()
        require(not timed_out, "Process timed out: " + label)
        require(code == 0, "Process failed: " + label + "; see " + str(log))
        text = data.decode("utf-8", errors="strict")
        require(re.search(r"\berror:|declaration uses ['\"]?sorry", text) is None,
                "Lean diagnostic prevents acceptance: " + label)
        return text

    try:
        if args.expected_lean_sha256:
            require(re.fullmatch(r"[0-9a-f]{64}", args.expected_lean_sha256) is not None,
                    "Expected compiler digest must be lowercase SHA-256")
            require(report["compiler_sha256"] == args.expected_lean_sha256, "Compiler digest mismatch")
        version = run("00-version", [str(lean), "--version"]).strip()
        require("version " + manifest["lean_release"] in version, "Wrong Lean release")
        require(manifest["lean_commit_prefix"] in version, "Wrong Lean commit")
        report["compiler_version"] = version

        # Keep provenance records separate from the staged mathematical sources.
        for key, filename in [("original_scope_blob", "original_scope.json"),
                              ("current_registry_blob", "inspected_registry.json")]:
            data = git_blob(repo, manifest[key])
            (output / filename).write_bytes(data)
        registry = json.loads((output / "inspected_registry.json").read_bytes())
        registered = registry["projects"]["consolidation-core"]["modules"]
        for key in ["LychrelDigitSums", "AlternatingScalarBoundary"]:
            item = next(x for x in modules if x["module"] == key)
            require(registered[key]["git_blob"] == item["git_blob"] and
                    registered[key]["sha256"] == item["sha256"],
                    "Current-registry source identity mismatch: " + key)

        staged: set[str] = set()
        builtin_roots = {"Init", "Std", "Lean"}
        for entry in entries:
            name = entry["module"]
            data = git_blob(repo, entry["git_blob"])
            if "sha256" in entry:
                require(digest(data) == entry["sha256"], "SHA-256 mismatch: " + name)
            text = data.decode("utf-8", errors="strict")
            imports = []
            for line in text.splitlines():
                if line.startswith("import "):
                    imports.extend(line.split("--", 1)[0].split()[1:])
            require(imports == entry["imports"], "Pinned import list mismatch: " + name)
            require(all(dep in staged or dep.split(".", 1)[0] in builtin_roots for dep in imports),
                    "Unstaged project dependency: " + name)
            (build / (name + ".lean")).write_bytes(data)
            report["sources"].append({"module": name, "git_blob": entry["git_blob"],
                                      "sha256": digest(data), "bytes": len(data), "imports": imports})
            staged.add(name)
        checkpoint()

        for index, name in enumerate(names, 1):
            run(f"{index:02d}-{name}", [str(lean), "-j1", "-DElab.async=false",
                                        "-o", name + ".olean", name + ".lean"])
            obj = build / (name + ".olean")
            require(obj.is_file(), "Compilation did not produce the expected object: " + name)
            report["sources"][index - 1]["olean_sha256"] = digest(obj.read_bytes())
            checkpoint()

        audit = "import All\nimport Agent14M99A04ScopeRegression\n\n" + "\n".join(
            "#check " + n + "\n#print axioms " + n for n in endpoints) + "\n"
        (build / "Agent14M99A04Audit.lean").write_text(audit, encoding="utf-8")
        text = run("10-endpoint-axioms", [str(lean), "-j1", "-DElab.async=false", "Agent14M99A04Audit.lean"])
        report["endpoint_axioms"] = parse_axioms(text, endpoints)
        report["audit_source_sha256"] = digest(audit.encode("utf-8"))
        report["status"] = "PASS_SCOPED_REBUILD"
        report["verification_level"] = "LEAN-CHECKED; independent interpretation review and integration are separate"
        report["scope"] = "Eight unchanged source modules plus six type/scope regression declarations; not repository-wide verification"
    except Exception as exc:
        report["status"] = "FAILED_NOT_ACCEPTED"
        report["error"] = type(exc).__name__ + ": " + str(exc)
    finally:
        report["finished_at"] = now()
        checkpoint()
        hashes = []
        for path in sorted(output.rglob("*")):
            if path.is_file() and path.name != "SHA256SUMS":
                hashes.append(digest(path.read_bytes()) + "  " + str(path.relative_to(output)))
        (output / "SHA256SUMS").write_text("\n".join(hashes) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "report": str(output / "verification.json")}))
    return 0 if report["status"] == "PASS_SCOPED_REBUILD" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--repo")
    parser.add_argument("--lean")
    parser.add_argument("--output")
    parser.add_argument("--manifest", default=str(Path(__file__).with_name("Agent14M99A04Manifest.json")))
    parser.add_argument("--expected-lean-sha256")
    parser.add_argument("--timeout", type=int, default=900, help="Maximum seconds per compiler process")
    args = parser.parse_args()
    if args.self_test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(AuditParserTests)
        return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1
    parser.error("--repo, --lean and --output are required") if not all([args.repo, args.lean, args.output]) else None
    require(args.timeout > 0, "--timeout must be positive")
    return replay(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print("NOT_ACCEPTED: " + str(exc), file=sys.stderr)
        sys.exit(1)
