from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import time

ev = Path(__file__).resolve().parent
repo = ev.parents[4]
src = repo / "proofs/Agent101PalindromeFibers.lean"
lean = Path("/workspace/scratch/2a8a87fd78df/agent101-runtime/toolchain/lean-4.19.0-linux/bin/lean")
deps = Path("/workspace/scratch/2a8a87fd78df/agent101-numeric-build")
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
frozen = "27ebcd2a7b790d87e45f19e51d0d7e2ff977f297742936503b9552026e3ea633"
assert sha(src) == frozen
assert src.read_bytes() == (ev / "attempts/attempt-006.lean").read_bytes()
exports = re.findall(r"^(?:def|theorem|lemma|abbrev|instance)\s+([A-Za-z0-9_']+)", src.read_text(), re.M)
assert len(exports) == 14
audit = "import Agent101PalindromeFibers\n\n" + "".join(
    f"#print axioms Agent101.{name}\n" for name in exports
)
(ev / "Audit.lean").write_text(audit)
(ev / "exports.json").write_text(json.dumps(["Agent101." + n for n in exports], indent=2) + "\n")
env = os.environ.copy()
env["LEAN_PATH"] = str(ev / "build") + ":" + str(deps)
cmd = [str(lean), "--trust=0", str(ev / "Audit.lean")]
t = time.time()
r = subprocess.run(cmd, cwd=repo, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(ev / "axioms.log").write_text(r.stdout)
version = subprocess.run([str(lean), "--version"], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
dependencies = {}
for module in ["Agent101DigitPairs", "Agent101MultiplicityBounds", "Agent101SplitEnumeration", "Agent101NumericFibers", "Lychrel196Research"]:
    dependencies[module] = {
        "source": str(deps / (module + ".lean")),
        "source_sha256": sha(deps / (module + ".lean")),
        "olean": str(deps / (module + ".olean")),
        "olean_sha256": sha(deps / (module + ".olean")),
    }
    canonical = repo / "proofs" / (module + ".lean")
    if canonical.exists():
        dependencies[module]["canonical_source"] = str(canonical)
        dependencies[module]["canonical_source_sha256"] = sha(canonical)
        dependencies[module]["source_copy_matches_canonical"] = canonical.read_bytes() == (deps / (module + ".lean")).read_bytes()
meta = {
    "source": str(src), "source_sha256": sha(src),
    "accepted_attempt": "attempt-006", "matches_accepted_attempt": True,
    "olean_sha256": sha(ev / "build/Agent101PalindromeFibers.olean"),
    "lean_version": version.stdout.strip(), "command": cmd,
    "lean_path": env["LEAN_PATH"], "returncode": r.returncode,
    "seconds": time.time() - t, "exports_count": len(exports),
    "exports": ["Agent101." + n for n in exports],
    "dependencies": dependencies,
    "forbidden_source_tokens": re.findall(r"\b(?:sorry|admit|axiom|native_decide)\b", src.read_text()),
}
(ev / "verification.json").write_text(json.dumps(meta, indent=2) + "\n")
print(json.dumps(meta, indent=2))
print(r.stdout)
raise SystemExit(r.returncode)
