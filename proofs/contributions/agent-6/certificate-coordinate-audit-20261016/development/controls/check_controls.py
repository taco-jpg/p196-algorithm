"""Retain each author source and raw log before checking with pinned Lean."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("module", choices=["CertificateControls", "CertificateControlsAudit"],
                    nargs="?", default="CertificateControls")
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
scratch = Path(__file__).resolve().parent
task = root / "agent6-checker/proofs/contributions/agent-6/certificate-coordinate-audit-20261016"
source = (task if args.module == "CertificateControls" else scratch) / (args.module + ".lean")
lean = root / "runtime-agent6/lean-4.19.0-linux/bin/lean"
lean_sha = hashlib.sha256(lean.read_bytes()).hexdigest()
assert lean_sha == "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023"
baseline = root / "runtime-agent6/review-certificate/baseline"
assert (baseline / "OBJECTS_READY.json").is_file()
paths = [scratch / "build", root / "agent6-checker-dev/objects",
         root / "landscape-agent6/checker-dev/attempt-001", baseline / "build/objects"]
paths[0].mkdir(parents=True, exist_ok=True)
assert (paths[1] / "CertificateFilter.olean").is_file()
assert (paths[2] / "CertificateCoordinates.olean").is_file()
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
           "-o", str(paths[0] / (args.module + ".olean")), str(attempt / source.name)]
dependencies = []
seen = set()
for folder in paths:
    for path in sorted(folder.glob("*.olean")):
        if path.name in seen or path.stem == args.module:
            continue
        seen.add(path.name)
        data = path.read_bytes()
        dependencies.append({"path": str(path), "bytes": len(data),
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
record = {"actor": "Agent #6", "role": "author", "module": args.module,
          "source_path": str(source), "source_bytes": len(raw),
          "source_sha256": hashlib.sha256(raw).hexdigest(),
          "compiler_sha256": lean_sha, "argv": command, "cwd": str(attempt),
          "lean_path": list(map(str, paths)), "dependency_oleans": dependencies,
          "baseline_source_manifest_sha256": hashlib.sha256(
              (baseline / "source-manifest.json").read_bytes()).hexdigest(),
          "started_unix": started, "elapsed_seconds": time.time() - started,
          "exit_code": exit_code, "timed_out": timed_out}
(attempt / "verification.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({k: v for k, v in record.items() if k != "dependency_oleans"}, indent=2))
print((attempt / "compile.log").read_text())
raise SystemExit(exit_code)
