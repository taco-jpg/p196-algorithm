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
previous = json.loads((reviews / "counts-palindrome-verification.json").read_text())
for meta_name in ["counts-verification.json", "counts-palindrome-verification.json"]:
    prior = json.loads((reviews / meta_name).read_text())
    assert prior["result"] == "PASS"
    for item in prior["source_registry"]:
        assert sha(Path(item["snapshot"])) == item["source_sha256"]
    for item in prior["build_results"]:
        assert sha(build / (item["module"] + ".olean")) == item["olean_sha256"]
modules = [
    ("Agent101NonpalindromicFibers", "22e33259394d275175a02a90a887e3fa49af488a3931e3518fc99899a59154e5"),
    ("Agent101ProtectedNonpalindromic", "93aa73770e3a57e89ad8b07eadc580ecd5c13494da8578ecbfcc41078c954df6"),
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
    (reviews / "counts-nonpalindromic-build-results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(result), flush=True)
    if r.returncode:
        print(r.stdout, flush=True)
        raise SystemExit(r.returncode)
target = proofs / "Agent101ProtectedNonpalindromic.lean"
exports = re.findall(r"^(?:def|theorem|lemma|abbrev|instance)\s+([A-Za-z0-9_']+)", target.read_text(), re.M)
assert len(exports) == 10
qualified = ["Agent101.Protected." + name for name in exports]
audit = reviews / "counts-nonpalindromic-Audit.lean"
audit.write_text("import Agent101ProtectedNonpalindromic\n\n" +
    "".join("#print axioms " + name + "\n" for name in qualified))
cmd = [str(lean), "-j1", "--trust=0", str(audit)]
r = subprocess.run(cmd, cwd=repo, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(reviews / "counts-nonpalindromic-axioms.log").write_text(r.stdout)
axioms = sorted(set(a.strip() for group in re.findall(r"depends on axioms: \[([^]]*)\]", r.stdout)
    for a in group.split(",") if a.strip()))
meta = {"result": "PASS" if r.returncode == 0 else "FAIL", "source": str(target),
    "source_sha256": sha(target), "source_unchanged": sha(target) == modules[-1][1],
    "compiler": str(lean), "compiler_sha256": sha(lean),
    "lean_version": previous["lean_version"], "LEAN_PATH": env["LEAN_PATH"],
    "prior_fresh_closure_evidence": str(reviews / "counts-palindrome-verification.json"),
    "prior_fresh_closure_evidence_sha256": sha(reviews / "counts-palindrome-verification.json"),
    "prior_source_snapshots_and_olean_hashes_rechecked": True,
    "build_policy": "Both additional non-Std modules rebuilt from frozen source into the same freshly source-built closure; no pre-existing external project oleans imported.",
    "reviewer_independence": "Reviewer did not author Agent101NonpalindromicFibers or Agent101ProtectedNonpalindromic. Reviewer authored the frozen Agent101SplitEnumeration and Agent101PalindromeFibers dependencies; the current semantic review concerns the new protected nonpalindromic target.",
    "source_registry": registry, "build_results": results,
    "audit_command": cmd, "audit_returncode": r.returncode,
    "exports_count": len(exports), "audited_exports": qualified, "axiom_union": axioms,
    "forbidden_source_tokens": re.findall(r"\b(?:sorry|admit|axiom|native_decide)\b", target.read_text()),
}
(reviews / "counts-nonpalindromic-verification.json").write_text(json.dumps(meta, indent=2) + "\n")
print(json.dumps({"audit_returncode": r.returncode, "exports_count": len(exports), "axiom_union": axioms}), flush=True)
print(r.stdout, flush=True)
for module, expected in modules:
    assert sha(proofs / (module + ".lean")) == expected
raise SystemExit(r.returncode)
