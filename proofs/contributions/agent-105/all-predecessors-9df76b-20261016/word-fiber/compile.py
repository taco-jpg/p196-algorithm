#!/usr/bin/env python3
"""Retained source-snapshot Lean compilation for the scoped WordFiber module."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, shutil, subprocess, time

TASK_ROOT = Path(__file__).resolve().parent
WORKTREE = TASK_ROOT.parents[4]
LEAN = Path("/workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean")
BASE = Path("/workspace/scratch/9df76b503b84/agent105-runtime/base-build")
PROFILE_HASH = "fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b"
parser = argparse.ArgumentParser()
parser.add_argument("--dependency", action="store_true")
args = parser.parse_args()
module = "Agent101ProfileExtraction" if args.dependency else "Agent105WordFiber9df76b"
prefix = "dependency-ProfileExtraction" if args.dependency else "attempt"
i = 1
while (TASK_ROOT / (prefix + "-" + str(i).zfill(3))).exists():
    i += 1
attempt = TASK_ROOT / (prefix + "-" + str(i).zfill(3))
attempt.mkdir(parents=True)
build = TASK_ROOT / "build"
build.mkdir(exist_ok=True)
source = WORKTREE / "proofs" / (module + ".lean")
data = source.read_bytes()
source_hash = hashlib.sha256(data).hexdigest()
if args.dependency:
    assert source_hash == PROFILE_HASH, "Published dependency bytes changed"
snapshot = attempt / source.name
snapshot.write_bytes(data)
artifact = attempt / (module + ".olean")
argv = [str(LEAN), "--trust=0", "-j1", "-DElab.async=false", "-o", str(artifact), str(snapshot)]
env = dict(os.environ)
env["LEAN_PATH"] = str(build) + ":" + str(BASE)
started_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
version = subprocess.run([str(LEAN), "--version"], cwd=attempt, env=env, text=True, capture_output=True)
(attempt / "version.stdout.log").write_text(version.stdout)
(attempt / "version.stderr.log").write_text(version.stderr)
t0 = time.monotonic()
proc = subprocess.run(argv, cwd=attempt, env=env, text=True, capture_output=True)
elapsed = time.monotonic() - t0
(attempt / "stdout.log").write_text(proc.stdout)
(attempt / "stderr.log").write_text(proc.stderr)
receipt = dict(module=module, attempt=i, started_at_utc=started_at,
    source=str(source), source_snapshot=str(snapshot), source_sha256=source_hash,
    command=argv, cwd=str(attempt), LEAN_PATH=env["LEAN_PATH"],
    compiler_sha256=hashlib.sha256(LEAN.read_bytes()).hexdigest(),
    version_command=[str(LEAN), "--version"], version_exit_code=version.returncode,
    version_stdout=version.stdout, version_stderr=version.stderr,
    exit_code=proc.returncode, seconds=elapsed, trust=0,
    source_dependency_commit="9bf1b2c35129500da39388727e17523f55fae80e",
    source_dependency_sha256=PROFILE_HASH,
    foundation_cache_reused=str(BASE), foundation_rebuilt=False)
if proc.returncode == 0:
    assert artifact.exists()
    shutil.copyfile(artifact, build / artifact.name)
    receipt["artifact"] = str(build / artifact.name)
    receipt["artifact_sha256"] = hashlib.sha256(artifact.read_bytes()).hexdigest()
(attempt / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
print(proc.stdout, end="")
if proc.stderr:
    print(proc.stderr, end="")
raise SystemExit(proc.returncode)
