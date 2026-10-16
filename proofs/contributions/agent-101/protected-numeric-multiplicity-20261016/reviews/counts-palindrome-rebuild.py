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
lean = Path("/workspace/scratch/2a8a87fd78df/agent101-runtime/toolchain/lean-4.19.0-linux/bin/lean")
sources = reviews / "counts-sources"
build = reviews / "counts-build"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
previous = json.loads((reviews / "counts-verification.json").read_text())
assert previous["result"] == "PASS"
for item in previous["source_registry"]:
    assert sha(Path(item["snapshot"])) == item["source_sha256"]
for item in previous["build_results"]:
    assert sha(build / (item["module"] + ".olean")) == item["olean_sha256"]
modules = [
    ("Agent101PalindromeFibers", "27ebcd2a7b790d87e45f19e51d0d7e2ff977f297742936503b9552026e3ea633"),
    ("Agent101ProtectedPalindrome", "1a662e360011f41d156efd9b5d62cc2acb18078486bcea6cab52b03aec18d295"),
]
env = os.environ.copy()
env["LEAN_PATH"] = str(build)
registry = []
results = []
for module, expected in modules:
    src = proofs / (module + ".lean")
    assert sha(src) == expected
    snap = sources / (module + ".lean")
    assert not snap.exists()
    snap.write_bytes(src.read_bytes())
    registry.append({"module": module, "source": str(src), "snapshot": str(snap),
        "source_sha256": sha(snap)})
    cmd = [str(lean), "-j1", "--trust=0", "-o", str(build / (module + ".olean")), str(snap)]
    t = time.time()
    r = subprocess.run(cmd, cwd=repo, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = reviews / ("counts-" + module + ".log")
    log.write_text(r.stdout)
    result = {"module": module, "command": cmd, "returncode": r.returncode,
        "seconds": time.time() - t, "log": str(log)}
    if r.returncode == 0:
        result["olean_sha256"] = sha(build / (module + ".olean"))
    results.append(result)
    (reviews / "counts-palindrome-build-results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(result), flush=True)
    if r.returncode:
        print(r.stdout, flush=True)
        raise SystemExit(r.returncode)
target = proofs / "Agent101ProtectedPalindrome.lean"
exports = re.findall(r"^(?:def|theorem|lemma|abbrev|instance)\s+([A-Za-z0-9_']+)", target.read_text(), re.M)
assert len(exports) == 15
qualified = ["Agent101.Protected." + name for name in exports]
audit = reviews / "counts-palindrome-Audit.lean"
audit.write_text("import Agent101ProtectedPalindrome\n\n" +
    "".join("#print axioms " + name + "\n" for name in qualified))
cmd = [str(lean), "-j1", "--trust=0", str(audit)]
r = subprocess.run(cmd, cwd=repo, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(reviews / "counts-palindrome-axioms.log").write_text(r.stdout)
axioms = sorted(set(a.strip() for group in re.findall(r"depends on axioms: \[([^]]*)\]", r.stdout)
    for a in group.split(",") if a.strip()))
meta = {"result": "PASS" if r.returncode == 0 else "FAIL", "source": str(target),
    "source_sha256": sha(target), "source_unchanged": sha(target) == modules[-1][1],
    "compiler": str(lean), "compiler_sha256": sha(lean),
    "lean_version": previous["lean_version"], "LEAN_PATH": env["LEAN_PATH"],
    "prior_fresh_closure_evidence": str(reviews / "counts-verification.json"),
    "prior_fresh_closure_evidence_sha256": sha(reviews / "counts-verification.json"),
    "prior_source_snapshots_and_olean_hashes_rechecked": True,
    "build_policy": "Both additional non-Std modules rebuilt from frozen source into the same freshly source-built closure; no pre-existing external project oleans imported.",
    "reviewer_independence": "Reviewer did not author Agent101ProtectedMultiplicity or Agent101ProtectedPalindrome. Reviewer authored the frozen Agent101SplitEnumeration and Agent101PalindromeFibers dependencies; their recompilation is not represented as an independent semantic review.",
    "source_registry": registry, "build_results": results,
    "audit_command": cmd, "audit_returncode": r.returncode,
    "exports_count": len(exports), "audited_exports": qualified, "axiom_union": axioms,
    "forbidden_source_tokens": re.findall(r"\b(?:sorry|admit|axiom|native_decide)\b", target.read_text()),
}
(reviews / "counts-palindrome-verification.json").write_text(json.dumps(meta, indent=2) + "\n")
print(json.dumps({"audit_returncode": r.returncode, "exports_count": len(exports), "axiom_union": axioms}), flush=True)
print(r.stdout, flush=True)
for module, expected in modules:
    assert sha(proofs / (module + ".lean")) == expected
raise SystemExit(r.returncode)
