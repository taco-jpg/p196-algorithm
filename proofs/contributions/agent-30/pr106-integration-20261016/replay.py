#!/usr/bin/env python3
"""Rebuild exact PR106 source and independently audit it in a new directory.

Usage: python3 replay.py --lean /path/to/lean-4.19.0-linux/bin/lean
       --source-dir /path/to/exact-source-checkout --work-dir /tmp/pr106-new
Only source files are copied; no project olean is reused. This script requires
its adjacent frozen audit harnesses and runtime-components.json. Linux only.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import shutil
import subprocess
import time

COMMIT = "ed9b9048adfdda70f699a8a40997a4330b76dc16"
LEAN_SHA256 = "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023"
RUNTIME_MANIFEST_SHA256 = "8616c028d9329b1232dfd67c2e6747f1690615cec3310399337d7eee91135920"
SOURCES = [
    ("LychrelDigitSums", "LychrelDigitSums__bf5247272a7e3b69.lean", "8a865176625283648a8a20dd2411ed77670eb0a2", "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57"),
    ("Agent106CarryBudget", "Agent106CarryBudget.lean", "8ab159e79cbd601bb0fad884f0ac392574f38d7b", "5eb8d4684584f3941bec9a7ea61b8ca3d7049a8f2ae60d02d64d9e2b6f2b7edc"),
    ("Agent106CongruenceSeed", "Agent106CongruenceSeed.lean", "4af21bdc673ffebfbad5bda77b79fc788f281259", "3c14410f4ccb7a7398c24ba5f24123197dfceb295d09b9aade9b4917e4aa36ed"),
    ("Agent106SparseTarget", "Agent106SparseTarget.lean", "d35c537d35bb12d63d2b338a7b8b8289129b4ae5", "6275b20e7648c309e3e9c3f412e2bbedd4f801f95d4a2b1631c1d1f4ee9bc193"),
    ("Agent106CongruenceObstruction", "Agent106CongruenceObstruction.lean", "1a1d6060087f9ba596d686a1e8ec76f81c8f3475", "c8b4e1567f93e3b8769348b92b33a8e847e4e32440ec6bcc0905f16411d5fb93"),
    ("Agent106CongruenceControls", "Agent106CongruenceControls.lean", "c95c7591e6363d6671818b208e442bf18da97929", "6ef0f20a8a18a0f35264d0007a735aa99b45e0e0f93de1ff865ad708d6cd31f0"),
]
HARNESSES = {
    "Agent30FullAudit.lean": "b3018588eb7ef174f379c7f62b1b7fd933200a8ff93ac5f2557c310aa62192d0",
    "Agent30EndpointTypes.lean": "b99ffbd26265d647e5575dbf6240f21b04f7585c40f79e9a39f52e4c63556707",
}
EXPECTED_IMPORTS = {
    "LychrelDigitSums": ["Std"],
    "Agent106CarryBudget": ["LychrelDigitSums"],
    "Agent106CongruenceSeed": ["LychrelDigitSums"],
    "Agent106SparseTarget": ["LychrelDigitSums"],
    "Agent106CongruenceObstruction": ["Agent106CarryBudget", "Agent106CongruenceSeed", "Agent106SparseTarget"],
    "Agent106CongruenceControls": ["Agent106CongruenceObstruction"],
}
CLEAN_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
FLAGS = ["--trust=0", "-j1", "-DElab.async=false"]

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def file_sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1048576), b""):
            h.update(block)
    return h.hexdigest()

def fail(message):
    raise SystemExit(message)

def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
    resource.setrlimit(resource.RLIMIT_CPU, (900, 900))

def runtime_files(root):
    return {str(p.relative_to(root)): p for p in [root / "bin/lean"] +
            [p for p in (root / "lib").rglob("*") if p.is_file()
             and (p.name.endswith(".olean") or ".so" in p.name)]}

def validate_runtime_manifest(manifest):
    required = {"schema", "scope", "version", "commit_prefix", "archive_sha256_from_existing_runtime_receipt", "archive_revalidated_in_this_run", "measured_utc", "files"}
    if not isinstance(manifest, dict) or set(manifest) != required:
        fail("Invalid runtime manifest keys.")
    if manifest["schema"] != 1 or manifest["version"] != "4.19.0" or manifest["commit_prefix"] != "6caaee842e94":
        fail("Unexpected runtime manifest schema or version.")
    if not isinstance(manifest["files"], list) or len(manifest["files"]) != 1503:
        fail("Unexpected runtime manifest inventory size.")
    seen = set()
    for entry in manifest["files"]:
        if not isinstance(entry, dict) or set(entry) != {"path", "bytes", "sha256"}:
            fail("Invalid runtime component record.")
        name = entry["path"]
        if not isinstance(name, str) or not name or chr(92) in name:
            fail("Invalid runtime component path.")
        path = Path(name)
        if path.is_absolute() or ".." in path.parts or str(path) != name or path.parts[0] not in {"bin", "lib"}:
            fail("Unsafe runtime component path: " + name)
        if name in seen or not isinstance(entry["bytes"], int) or entry["bytes"] < 0:
            fail("Duplicate or invalid runtime component record: " + name)
        if not isinstance(entry["sha256"], str) or re.fullmatch("[0-9a-f]{64}", entry["sha256"]) is None:
            fail("Invalid runtime component digest: " + name)
        seen.add(name)

def verify_runtime(root, manifest):
    validate_runtime_manifest(manifest)
    actual_files = runtime_files(root)
    expected = {entry["path"]: entry for entry in manifest["files"]}
    if set(actual_files) != set(expected):
        fail("Bundled runtime file inventory differs from frozen manifest.")
    actual = []
    for name in sorted(expected):
        path = actual_files[name]
        digest, size = file_sha(path), path.stat().st_size
        if digest != expected[name]["sha256"] or size != expected[name]["bytes"]:
            fail("Bundled runtime identity mismatch: " + name)
        actual.append({"path": name, "bytes": size, "sha256": digest})
    return {"file_count": len(actual), "total_bytes": sum(x["bytes"] for x in actual),
            "inventory_sha256": sha(json.dumps(actual, sort_keys=True).encode())}

def loader_snapshot(lean):
    result = subprocess.run(["/usr/bin/ldd", str(lean)], env=CLEAN_ENV,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    if result.returncode:
        fail("Cannot inventory dynamic loader components: " + result.stderr.decode())
    paths = set()
    for line in result.stdout.decode().splitlines():
        match = re.search(r"(?:=>\s+)?(/[^\s]+)", line)
        if match:
            paths.add(Path(match.group(1)).resolve(strict=True))
        if "not found" in line:
            fail("Unresolved dynamic library: " + line)
    if not paths:
        fail("Empty dynamic loader component inventory.")
    return {"ldd_stdout": result.stdout.decode(),
            "files": [{"path": str(p), "sha256": file_sha(p), "bytes": p.stat().st_size}
                      for p in sorted(paths)]}

def input_snapshot(checked, harness_dir, work, runtime_root, runtime_manifest, lean):
    sources = []
    for module, original, _, _, expected_source_sha, _ in checked:
        staged = work / (module + ".lean")
        original_digest, staged_digest = file_sha(original), file_sha(staged)
        if original_digest != expected_source_sha or staged_digest != expected_source_sha:
            fail("Original or staged source differs from frozen pin: " + module)
        sources.append({"module": module, "original": str(original),
                        "original_sha256": original_digest,
                        "staged_sha256": staged_digest})
    harnesses = [{"file": name, "original_sha256": file_sha(harness_dir / name),
                  "staged_sha256": file_sha(work / name)} for name in HARNESSES]
    for row in harnesses:
        if row["original_sha256"] != HARNESSES[row["file"]] or row["staged_sha256"] != HARNESSES[row["file"]]:
            fail("Original or staged harness differs from frozen pin: " + row["file"])
    manifest_digest = file_sha(harness_dir / "runtime-components.json")
    if manifest_digest != RUNTIME_MANIFEST_SHA256:
        fail("Runtime manifest differs from frozen pin during snapshot.")
    return {"sources": sources, "harnesses": harnesses,
            "replay_sha256": file_sha(Path(__file__).resolve()),
            "runtime_manifest_sha256": manifest_digest,
            "bundled_runtime": verify_runtime(runtime_root, runtime_manifest),
            "loader": loader_snapshot(lean)}

def stable_identity(snapshot):
    copy = dict(snapshot)
    copy["loader"] = {"files": snapshot["loader"]["files"]}
    return copy

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--source-dir", required=True, type=Path)
    parser.add_argument("--work-dir", required=True, type=Path)
    args = parser.parse_args()
    lean = args.lean.resolve(strict=True)
    source = args.source_dir.resolve(strict=True)
    work = args.work_dir.resolve()
    harness_dir = Path(__file__).resolve().parent
    runtime_root = lean.parent.parent
    if work.exists():
        fail("Refusing existing --work-dir; choose a new directory.")
    if file_sha(lean) != LEAN_SHA256:
        fail("Lean executable SHA256 mismatch.")
    runtime_manifest_path = harness_dir / "runtime-components.json"
    if file_sha(runtime_manifest_path) != RUNTIME_MANIFEST_SHA256:
        fail("Runtime component manifest SHA256 mismatch.")
    runtime_manifest = json.loads(runtime_manifest_path.read_text())
    for name, expected in HARNESSES.items():
        if file_sha(harness_dir / name) != expected:
            fail("Frozen audit harness SHA256 mismatch: " + name)
    checked = []
    completed_modules = set()
    for module, filename, blob_expected, sha_expected in SOURCES:
        candidates = [source / "proofs" / filename, source / filename, source / (module + ".lean")]
        selected = next((path for path in candidates if path.is_file()), None)
        if selected is None:
            fail("Missing source: " + filename)
        data = selected.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if blob != blob_expected or sha(data) != sha_expected:
            fail("Exact source identity mismatch: " + str(selected))
        imports = re.findall(r"^import\s+([A-Za-z0-9_.]+)\s*$", data.decode("utf-8"), re.M)
        if imports != EXPECTED_IMPORTS[module]:
            fail("Import list mismatch: " + module)
        if any(name != "Std" and name not in completed_modules for name in imports):
            fail("Import closure or topological order mismatch: " + module)
        completed_modules.add(module)
        checked.append((module, selected, data, blob_expected, sha_expected, imports))
    if completed_modules != set(EXPECTED_IMPORTS):
        fail("Six-module closure incomplete.")
    verify_runtime(runtime_root, runtime_manifest)
    work.mkdir(parents=True)
    manifest = []
    for module, selected, data, blob, digest, imports in checked:
        (work / (module + ".lean")).write_bytes(data)
        manifest.append({"module": module, "input_file": str(selected), "git_blob": blob,
                         "sha256": digest, "bytes": len(data), "imports": imports})
    for name in HARNESSES:
        shutil.copyfile(harness_dir / name, work / name)
    env = dict(CLEAN_ENV)
    env["LEAN_PATH"] = str(work)
    receipt = {"commit": COMMIT, "runtime": str(lean), "runtime_sha256": LEAN_SHA256,
               "runtime_manifest_sha256": RUNTIME_MANIFEST_SHA256, "harness_hashes": HARNESSES,
               "cwd": str(work), "subprocess_environment": env,
               "initial_project_oleans": [], "sources": manifest,
               "address_space_bytes": 4 * 1024**3, "cpu_seconds": 900,
               "timeout_seconds": 960, "start_utc": now(), "complete": False, "commands": []}
    if list(work.glob("*.olean")):
        fail("Unexpected pre-existing project object.")
    receipt["inputs_before"] = input_snapshot(checked, harness_dir, work, runtime_root, runtime_manifest, lean)
    def save():
        (work / "replay-execution.json").write_text(json.dumps(receipt, indent=2) + "\n")
    save()
    def run(label, argv):
        started, wall = now(), time.monotonic()
        try:
            result = subprocess.run(argv, cwd=work, env=env, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, timeout=960, preexec_fn=limits)
            code, stdout, stderr = result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired as exc:
            code, stdout, stderr = 124, exc.stdout or b"", exc.stderr or b""
        row = {"label": label, "argv": argv, "start_utc": started, "end_utc": now(),
               "wall_seconds": time.monotonic() - wall, "returncode": code}
        for stream, data in [("stdout", stdout), ("stderr", stderr)]:
            name = label + "." + stream + ".log"
            (work / name).write_bytes(data)
            row[stream] = {"file": name, "sha256": sha(data), "bytes": len(data)}
        receipt["commands"].append(row)
        save()
        print(json.dumps(row), flush=True)
        if code:
            fail("Replay failed; retained all logs in " + str(work))
        return stdout.decode("utf-8")
    version = run("lean-version", [str(lean), "--version"])
    if "version 4.19.0" not in version or "commit 6caaee842e94" not in version:
        fail("Unexpected runtime version.")
    prefix = run("lean-prefix", [str(lean), "--print-prefix"])
    if Path(prefix.strip()).resolve() != runtime_root:
        fail("Runtime prefix differs from verified distribution root.")
    for module, _, _, _, _, _ in checked:
        run(module, [str(lean)] + FLAGS + ["-o", module + ".olean", module + ".lean"])
    for harness in HARNESSES:
        run(Path(harness).stem, [str(lean)] + FLAGS + [harness])
    summary = json.loads((work / "audit-summary.json").read_text())
    if summary["status"] != "PASS" or summary["endpoint_count"] != 36:
        fail("Audit summary failed.")
    receipt["inputs_after"] = input_snapshot(checked, harness_dir, work, runtime_root, runtime_manifest, lean)
    if stable_identity(receipt["inputs_before"]) != stable_identity(receipt["inputs_after"]):
        save()
        fail("Runtime, source, harness, or dynamic-loader component changed during replay.")
    receipt["complete"] = True
    receipt["end_utc"] = now()
    receipt["audit_summary"] = summary
    receipt["outputs"] = [{"file": path.name, "sha256": file_sha(path), "bytes": path.stat().st_size}
                          for path in sorted(work.glob("*.olean"))]
    save()
    print("EXACT_SOURCE_BUILD_AND_AUDIT_PASS")

if __name__ == "__main__":
    main()

