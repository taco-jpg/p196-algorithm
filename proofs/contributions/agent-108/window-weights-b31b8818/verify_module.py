#!/usr/bin/env python3
"""Record a real Lean build and a transitive axiom audit of one owned module.

Usage: python3 verify_module.py MODULE ATTEMPT
The runtime and build directory may be selected by environment variables.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

evidence = Path(__file__).resolve().parent
proofs = evidence.parents[2]
workspace = proofs.parent.parent
module, attempt = sys.argv[1:3]
source = proofs / (module + ".lean")
group = module.removeprefix("Agent108Window").lower() or "core"
record_dir = evidence / group / ("attempt-" + attempt)
record_dir.mkdir(parents=True, exist_ok=False)
source_bytes = source.read_bytes()
(record_dir / source.name).write_bytes(source_bytes)
build = Path(os.environ.get("AGENT108_LEAN_BUILD", workspace / "agent108-build"))
build.mkdir(parents=True, exist_ok=True)
wrapper = os.environ.get("AGENT108_LEAN", str(workspace / "agent108-runtime/lean-with-mathlib.sh"))
env = os.environ.copy()
env["LEAN_PATH"] = str(build) + (":" + env["LEAN_PATH"] if env.get("LEAN_PATH") else "")
results = []

def run(stage, path, output=None):
    command = [wrapper, "--trust=0"]
    if output:
        command += ["-o", str(output)]
    command += [str(path)]
    result = subprocess.run(command, capture_output=True, text=True, env=env, cwd=proofs)
    (record_dir / (stage + ".stdout.log")).write_text(result.stdout)
    (record_dir / (stage + ".stderr.log")).write_text(result.stderr)
    results.append({"stage": stage, "command": command, "exit_code": result.returncode})
    if result.returncode:
        print(result.stdout + result.stderr)
    return result

olean = build / (module + ".olean")
olean.unlink(missing_ok=True)
compiled = run("compile", source, olean)
declarations = re.findall(r"^(?:noncomputable\s+)?(?:def|theorem|lemma|abbrev)\s+([A-Za-z0-9_']+)", source_bytes.decode(), re.M)
audit = record_dir / (module + "Audit.lean")
audit.write_text("import " + module + "\n" + "\n".join("#print axioms Agent108.WindowWeights." + n for n in declarations) + "\n")
audited = run("audit", audit) if compiled.returncode == 0 else None
record = {
    "module": module,
    "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
    "source_unchanged_during_build": source.read_bytes() == source_bytes,
    "declarations_audited": declarations,
    "results": results,
    "audit_output": audited.stdout if audited else None,
    "status": "LEAN-CHECKED" if audited and audited.returncode == 0 else "WIP",
}
(record_dir / "verification.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
sys.exit(0 if record["status"] == "LEAN-CHECKED" else 1)
