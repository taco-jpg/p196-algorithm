#!/usr/bin/env python3
"""Independent root review of semantic_scout's fixed FamilyRatio source."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import time

here = Path(__file__).resolve().parent
proofs = here.parents[4]
workspace = proofs.parent.parent
modules = ["Defs", "Products", "Weights", "Endpoints", "EndpointWeights",
           "Obstruction", "FamilyProducts", "FamilyRatio"]
modules = ["Agent108Window" + m for m in modules]
expected = {
    "Agent108WindowDefs": "147ae208dce3b612c6eb23091eab123b77bd46c86d216ab8a6199913015f0aa0",
    "Agent108WindowProducts": "2920c9da6e3c06c40a1d8478fe1af0d87b00627976f53856f75b90de32a1e584",
    "Agent108WindowWeights": "5bc7f457187ad0af4a4f7a340acf7f827b8e89537d73624519805d232c762eae",
    "Agent108WindowEndpoints": "ebabfbfd366729846656ff5a56891c22f9c7f0868fca9c5918be433e5d5fbc22",
    "Agent108WindowEndpointWeights": "21355018606cf7c2cfe8c33a008be815bd546bbafc31be69bc428624de0acab1",
    "Agent108WindowObstruction": "0dd91993667dddac3740ccadd7b2764cc2e6122121f19bd0a8354a9e0507a90a",
    "Agent108WindowFamilyProducts": "d4449500c98887a82dca222af318e8d99e8ef0d1ad5e58719658406c1650fdc8",
    "Agent108WindowFamilyRatio": "051dcb42849d9cffb2fec0de77af138b6d7d6c415ff27d65725dcdf9cfcf7afc",
}
sources, build, logs = [here / n for n in ["sources", "build", "logs"]]
for d in [sources, build, logs]:
    d.mkdir(exist_ok=False)
declarations = []
for module in modules:
    data = (proofs / (module + ".lean")).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected[module]:
        raise RuntimeError("Source drift in " + module + ": " + digest)
    (sources / (module + ".lean")).write_bytes(data)
    for name in re.findall(r"^(?:noncomputable\s+)?(?:def|theorem|lemma|abbrev)\s+([A-Za-z0-9_']+)", data.decode(), re.M):
        declarations.append({"module": module, "name": "Agent108.WindowWeights." + name})
audit = sources / "IndependentFamilyRatioAudit.lean"
audit.write_text("\n".join("import " + m for m in modules) + "\n" +
                 "\n".join("#print axioms " + d["name"] for d in declarations) + "\n")
wrapper = os.environ.get("AGENT108_LEAN", str(workspace / "agent108-runtime/lean-with-mathlib.sh"))
env = os.environ.copy()
env["LEAN_PATH"] = str(build)
steps = []
all_ok = True
for module in modules + ["IndependentFamilyRatioAudit"]:
    command = [wrapper, "--trust=0", "-o", str(build / (module + ".olean")),
               str(sources / (module + ".lean"))]
    started = time.monotonic()
    p = subprocess.run(command, env=env, cwd=sources, capture_output=True, text=True)
    (logs / (module + ".stdout.log")).write_text(p.stdout)
    (logs / (module + ".stderr.log")).write_text(p.stderr)
    step = {"module": module, "command": command, "exit_code": p.returncode,
            "seconds": time.monotonic() - started}
    steps.append(step)
    print(json.dumps({"module": module, "exit_code": p.returncode}), flush=True)
    if p.returncode:
        print(p.stdout + p.stderr, flush=True)
        all_ok = False
        break
allowed = {"propext", "Classical.choice", "Quot.sound"}
correspondence = []
if all_ok:
    output = (logs / "IndependentFamilyRatioAudit.stdout.log").read_text()
    for declaration in declarations:
        pattern = re.escape("'" + declaration["name"] + "'") + r" (.*)"
        found = re.search(pattern, output)
        axioms = None
        if found and found.group(1).startswith("does not depend on any axioms"):
            axioms = []
        elif found:
            match = re.search(r"depends on axioms: \[([^\]]*)\]", found.group(1))
            if match:
                axioms = [s.strip() for s in match.group(1).split(",") if s.strip()]
        ok = axioms is not None and set(axioms) <= allowed
        correspondence.append({**declaration, "axioms": axioms, "pass": ok})
        all_ok = all_ok and ok
result = {"reviewer": "Agent #108 root, independent of FamilyRatio author semantic_scout",
          "scope": "Fixed FamilyRatio statement and complete fresh dependency build; author-source declarations audited",
          "source_sha256": expected, "steps": steps, "public_declarations": correspondence,
          "logical_axiom_allowlist": sorted(allowed), "pass": all_ok}
(here / "review-result.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"pass": all_ok, "public_declarations": len(correspondence)}), flush=True)
raise SystemExit(0 if all_ok else 1)
