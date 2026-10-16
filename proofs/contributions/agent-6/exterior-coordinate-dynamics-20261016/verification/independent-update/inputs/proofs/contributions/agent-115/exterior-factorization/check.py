#!/usr/bin/env python3
"""Agent #115: clean from-source build and axiom audit of the exterior factorization.

Usage: python3 check.py <absolute lean binary> <new empty evidence dir>
Run from the repository root. Copies the unchanged dependency
proofs/contributions/agent-109/outer-projection-bridge/agent7-deps/OuterFinite.lean
and this directory's TARGET.lean, ExteriorFactorizationProof.lean,
ExteriorObservationInjective.lean, ExteriorUpdateLaw.lean, FactAudit.lean
into the evidence directory, compiles them in order with no reused objects, and
accepts only if every audited theorem's axioms are within
{propext, Classical.choice, Quot.sound}.
"""
import hashlib, json, re, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
DEP = REPO / "proofs/contributions/agent-109/outer-projection-bridge/agent7-deps/OuterFinite.lean"
DEP_SHA = "3376873da457c698850f604ddda82aeba3e67f4196e5c33d8142bed945c5f3f6"
ORDER = [("OuterFinite", DEP), ("TARGET", HERE / "TARGET.lean"),
         ("ExteriorFactorizationProof", HERE / "ExteriorFactorizationProof.lean"),
         ("ExteriorObservationInjective", HERE / "ExteriorObservationInjective.lean"),
         ("ExteriorUpdateLaw", HERE / "ExteriorUpdateLaw.lean"),
         ("FactAudit", HERE / "FactAudit.lean")]
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
FORBIDDEN = re.compile(r"\b(sorry|admit|native_decide|sorryAx|ofReduceBool)\b")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    lean, ev = Path(sys.argv[1]), Path(sys.argv[2])
    ev.mkdir(parents=True, exist_ok=False)
    (ev / "src").mkdir(); (ev / "obj").mkdir()
    assert sha(DEP) == DEP_SHA, "dependency hash mismatch"
    libdir = subprocess.run([str(lean), "--print-libdir"], capture_output=True, text=True).stdout.strip()
    env = {"PATH": "/usr/bin:/bin", "LEAN_PATH": f"{ev/'obj'}:{libdir}", "HOME": str(ev)}
    report = {"lean": str(lean), "lean_sha256": sha(lean),
              "version": subprocess.run([str(lean), "--version"], capture_output=True, text=True).stdout.strip(),
              "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "modules": []}
    ok = True
    for name, path in ORDER:
        text = path.read_text()
        dst = ev / "src" / (name + ".lean")
        dst.write_text(text)
        body = re.sub(r"/-.*?-/", "", text, flags=re.S)
        body = re.sub(r"--[^\n]*", "", body)
        if name != "OuterFinite" and FORBIDDEN.search(body):
            ok = False
        cmd = [str(lean), "-DElab.async=false", f"--root={ev/'src'}", str(dst)]
        if name != "FactAudit":
            cmd[1:1] = ["-o", str(ev / "obj" / (name + ".olean"))]
        t = time.time()
        r = subprocess.run(cmd, env=env, capture_output=True, text=True)
        (ev / (name + ".log")).write_text(r.stdout + r.stderr)
        report["modules"].append({"module": name, "source": str(path.relative_to(REPO)),
                                  "sha256": sha(path), "exit": r.returncode,
                                  "seconds": round(time.time() - t, 1)})
        ok = ok and r.returncode == 0
    audit = (ev / "FactAudit.log").read_text()
    axioms = {}
    for m in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]*)\]", audit):
        axioms[m.group(1)] = [a.strip() for a in m.group(2).split(",") if a.strip()]
    for m in re.finditer(r"'([^']+)' does not depend on any axioms", audit):
        axioms[m.group(1)] = []
    report["axioms"] = axioms
    expected = 9
    ok = ok and len(axioms) == expected and all(set(v) <= ALLOWED for v in axioms.values())
    report["status"] = "PASS" if ok else "FAIL"
    report["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (ev / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(report["status"])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
