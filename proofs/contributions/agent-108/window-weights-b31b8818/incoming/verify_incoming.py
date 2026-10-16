#!/usr/bin/env python3
"""Compile a saved exact Incoming attempt with trust=0 and audit its declarations."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

evidence = Path(__file__).resolve().parent
proofs = evidence.parents[3]
workspace = proofs.parent.parent
source = proofs / "Agent108WindowIncoming.lean"
attempt = evidence / ("attempt-" + sys.argv[1])
attempt.mkdir(parents=True, exist_ok=False)
source_bytes = source.read_bytes()
snapshot = attempt / source.name
snapshot.write_bytes(source_bytes)
build = attempt / "build"
build.mkdir()
wrapper = workspace / "agent108-runtime/lean-with-mathlib.sh"
paths = [
    build,
    workspace / "agent108-runtime/embedding-build/006",
    evidence.parent / "review/independent-family-ratio-051dcb4/build",
    workspace / "agent108-dependencies/build-independent-approved02",
    evidence.parent / "review/independent-algebra-0dd91993/build",
]
env = os.environ.copy()
env["LEAN_PATH"] = ":".join(str(p) for p in paths)
results = []

def run(stage, path, output=None):
    command = [str(wrapper), "--trust=0", "-j1", "-DElab.async=false"]
    if output:
        command += ["-o", str(output)]
    command += [str(path)]
    result = subprocess.run(command, cwd=attempt, env=env, capture_output=True, text=True)
    (attempt / (stage + ".stdout.log")).write_text(result.stdout)
    (attempt / (stage + ".stderr.log")).write_text(result.stderr)
    results.append({"stage": stage, "command": command, "exit_code": result.returncode})
    print(f"{stage}: exit {result.returncode}", flush=True)
    if result.returncode:
        print(result.stdout + result.stderr, flush=True)
    return result

compiled = run("compile", snapshot, build / "Agent108WindowIncoming.olean")
declarations = re.findall(r"^(?:noncomputable\s+)?(?:def|theorem|lemma|abbrev)\s+([A-Za-z0-9_']+)",
                          source_bytes.decode(), re.M)
audit = attempt / "IncomingAudit.lean"
audit.write_text("import Agent108WindowIncoming\n" + "\n".join(
    "#print axioms Agent108.WindowWeights." + name for name in declarations) + "\n")
audited = run("audit", audit) if compiled.returncode == 0 else None
allowed = {"propext", "Classical.choice", "Quot.sound"}
unexpected = set()
if audited:
    for part in re.findall(r"depends on axioms: \[([^\]]*)\]", audited.stdout):
        unexpected.update(x.strip() for x in part.split(",") if x.strip() and x.strip() not in allowed)
dep_names = ["Agent108WindowDefs", "Agent108WindowProducts", "Agent108WindowWeights",
             "Agent108WindowEndpoints", "Agent108WindowEndpointWeights",
             "Agent108WindowObstruction", "Agent108WindowFamilyProducts",
             "Agent108WindowFamilyRatio", "Agent108WindowEmbedding"]
record = {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "kind": "author compile and transitive axiom audit, not independent review",
    "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
    "source_unchanged": source.read_bytes() == source_bytes,
    "LEAN_PATH": env["LEAN_PATH"],
    "mathlib_commit": "c44e0c8ee63ca166450922a373c7409c5d26b00b",
    "original_dependencies_commit": "12a32789056f5eec8247166564ac2ef745c3c9d6",
    "dependency_source_sha256": {
        name: hashlib.sha256((proofs / (name + ".lean")).read_bytes()).hexdigest()
        for name in dep_names
    },
    "results": results,
    "public_declarations_audited": declarations,
    "private_helpers_covered_transitively": ["ofFn_bitsFromList", "sum_choices_get"],
    "unexpected_axioms": sorted(unexpected),
    "status": "PASS" if audited and audited.returncode == 0 and not unexpected else "WIP",
}
(attempt / "verification.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2), flush=True)
sys.exit(0 if record["status"] == "PASS" else 1)
