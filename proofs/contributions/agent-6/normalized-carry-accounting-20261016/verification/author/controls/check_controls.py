"""Retain immutable author attempts and check them with the pinned Lean binary."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import time


parser = argparse.ArgumentParser()
parser.add_argument("module", choices=["CarryControls", "CarryControlsAudit"],
                    nargs="?", default="CarryControls")
parser.add_argument("--extra-lean-path", action="append", default=[])
args = parser.parse_args()
scratch = Path(__file__).resolve().parent
root = scratch.parents[1]
task = root / "agent6-carry/proofs/contributions/agent-6/normalized-carry-accounting-20261016"
source = (task if args.module == "CarryControls" else scratch) / (args.module + ".lean")
lean = root / "runtime-agent6/lean-4.19.0-linux/bin/lean"
lean_sha = hashlib.sha256(lean.read_bytes()).hexdigest()
assert lean_sha == "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023"
baseline = root / "runtime-agent6/review-carry/inherited"
assert (baseline / "OBJECTS_READY.json").is_file()
paths = [Path(path).resolve() for path in args.extra_lean_path]
paths.append(baseline / "objects")
for path in paths:
    assert path.is_dir(), path
assert (paths[-1] / "CertificateCoordinates.olean").is_file()
attempts = scratch / "attempts"
attempts.mkdir(exist_ok=True)
number = 1 + len(list(attempts.glob(args.module + "-*")))
attempt = attempts / f"{args.module}-{number:03d}"
attempt.mkdir()
raw = source.read_bytes()
(attempt / source.name).write_bytes(raw)
env = dict(os.environ)
env["LEAN_PATH"] = os.pathsep.join(map(str, paths))
command = [str(lean), "--trust=0", "-j1", "-DElab.async=false",
           "-o", str(attempt / (args.module + ".olean")), str(attempt / source.name)]
dependencies = []
seen = set()
for folder in paths:
    for path in sorted(folder.glob("*.olean")):
        if path.name in seen or path.stem == args.module:
            continue
        seen.add(path.name)
        data = path.read_bytes()
        dependencies.append({"module": path.stem, "path": str(path),
                             "bytes": len(data),
                             "sha256": hashlib.sha256(data).hexdigest()})
started = time.time()
timed_out = False
with (attempt / "compile.log").open("wb") as log:
    try:
        result = subprocess.run(command, cwd=attempt, env=env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=240)
        exit_code = result.returncode
    except subprocess.TimeoutExpired:
        exit_code = 124
        timed_out = True
record = {
    "actor": "Agent #6", "role": "author", "module": args.module,
    "source_path": str(source), "source_bytes": len(raw),
    "source_sha256": hashlib.sha256(raw).hexdigest(),
    "source_git_blob_sha1": hashlib.sha1(
        b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
    "compiler_sha256": lean_sha, "argv": command, "cwd": str(attempt),
    "lean_path": list(map(str, paths)), "dependency_oleans": dependencies,
    "inherited_objects_ready_sha256": hashlib.sha256(
        (baseline / "OBJECTS_READY.json").read_bytes()).hexdigest(),
    "started_unix": started, "elapsed_seconds": time.time() - started,
    "exit_code": exit_code, "timed_out": timed_out,
}
object_path = attempt / (args.module + ".olean")
if exit_code == 0 and object_path.is_file():
    data = object_path.read_bytes()
    record["output_object"] = {"path": str(object_path), "bytes": len(data),
                               "sha256": hashlib.sha256(data).hexdigest()}
(attempt / "verification.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({k: v for k, v in record.items() if k != "dependency_oleans"}, indent=2))
print((attempt / "compile.log").read_text())
raise SystemExit(exit_code)
