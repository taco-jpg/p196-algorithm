from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import time

reviews = Path(__file__).resolve().parent
repo = reviews.parents[4]
proofs = repo / "proofs"
deps = reviews.parent / "dependencies/agent3"
lean = Path("/workspace/scratch/2a8a87fd78df/agent101-runtime/toolchain/lean-4.19.0-linux/bin/lean")
sources = reviews / "counts-sources"
build = reviews / "counts-build"
sources.mkdir(exist_ok=False)
build.mkdir(exist_ok=False)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
target = proofs / "Agent101ProtectedMultiplicity.lean"
frozen = "503dcb1c7d90f031a54caffb89ce8a632edbdc77c9383d06dbacfdbffaf0c1ac"
assert sha(target) == frozen
modules = [
    ("Lychrel196Research", proofs / "Lychrel196Research__c696e0ea3db39d92.lean"),
    ("Agent101DigitPairs", proofs / "Agent101DigitPairs.lean"),
    ("Agent101MultiplicityBounds", proofs / "Agent101MultiplicityBounds.lean"),
    ("Agent101SplitEnumeration", proofs / "Agent101SplitEnumeration.lean"),
    ("Agent101NumericFibers", proofs / "Agent101NumericFibers.lean"),
    ("PeriodObstructions", proofs / "PeriodObstructions__70ce034b31b5b218.lean"),
    ("ActualWordBridge", proofs / "ActualWordBridge__7f032d27940694a8.lean"),
    ("FamilyDefinitions", deps / "FamilyDefinitions.lean"),
    ("FamilyCardinality", deps / "FamilyCardinality.lean"),
    ("Agent101ProtectedMultiplicity", target),
]
registry = []
for module, src in modules:
    snap = sources / (module + ".lean")
    snap.write_bytes(src.read_bytes())
    registry.append({"module": module, "original_source": str(src),
        "snapshot": str(snap), "source_sha256": sha(snap),
        "imports": re.findall(r"^import\s+(.+)$", snap.read_text(), re.M)})
(reviews / "counts-source-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
env = os.environ.copy()
env["LEAN_PATH"] = str(build)
results = []
for item in registry:
    module = item["module"]
    cmd = [str(lean), "-j1", "--trust=0", "-o", str(build / (module + ".olean")), item["snapshot"]]
    t = time.time()
    r = subprocess.run(cmd, cwd=repo, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = reviews / ("counts-" + module + ".log")
    log.write_text(r.stdout)
    result = {"module": module, "command": cmd, "returncode": r.returncode,
        "seconds": time.time() - t, "log": str(log)}
    if r.returncode == 0:
        result["olean_sha256"] = sha(build / (module + ".olean"))
    results.append(result)
    (reviews / "counts-build-results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(result), flush=True)
    if r.returncode:
        print(r.stdout, flush=True)
        raise SystemExit(r.returncode)
exports = re.findall(r"^(?:def|theorem|lemma|abbrev|instance)\s+([A-Za-z0-9_']+)", target.read_text(), re.M)
assert len(exports) == 18
qualified = ["Agent101.Protected." + name for name in exports]
audit = reviews / "counts-Audit.lean"
audit.write_text("import Agent101ProtectedMultiplicity\n\n" +
    "".join("#print axioms " + name + "\n" for name in qualified))
cmd = [str(lean), "-j1", "--trust=0", str(audit)]
r = subprocess.run(cmd, cwd=repo, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(reviews / "counts-axioms.log").write_text(r.stdout)
axioms = sorted(set(a.strip() for group in re.findall(r"depends on axioms: \[([^]]*)\]", r.stdout)
    for a in group.split(",") if a.strip()))
version = subprocess.run([str(lean), "--version"], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
meta = {"result": "PASS" if r.returncode == 0 else "FAIL", "source": str(target),
    "source_sha256": sha(target), "source_unchanged": sha(target) == frozen,
    "compiler": str(lean), "compiler_sha256": sha(lean),
    "lean_version": version.stdout.strip(), "LEAN_PATH": env["LEAN_PATH"],
    "build_policy": "All 10 non-Std source modules rebuilt into a new empty directory; no old project oleans were imported.",
    "reviewer_independence": "Reviewer did not author Agent101ProtectedMultiplicity. Reviewer previously authored Agent101SplitEnumeration, one of its frozen dependencies.",
    "source_registry": registry, "build_results": results,
    "audit_command": cmd, "audit_returncode": r.returncode,
    "exports_count": len(exports), "audited_exports": qualified, "axiom_union": axioms,
    "forbidden_source_tokens": re.findall(r"\b(?:sorry|admit|axiom|native_decide)\b", target.read_text()),
}
(reviews / "counts-verification.json").write_text(json.dumps(meta, indent=2) + "\n")
print(json.dumps({"audit_returncode": r.returncode, "exports_count": len(exports), "axiom_union": axioms}), flush=True)
print(r.stdout, flush=True)
assert sha(target) == frozen
raise SystemExit(r.returncode)
