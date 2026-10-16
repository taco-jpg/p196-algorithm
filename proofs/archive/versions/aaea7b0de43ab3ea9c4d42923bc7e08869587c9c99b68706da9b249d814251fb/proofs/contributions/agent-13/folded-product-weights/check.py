#!/usr/bin/env python3
"""Clean folded product-weight source build and complete transitive axiom audit.
Reuses only the hash-pinned existing Mathlib source-validation routine.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

CORE_SHA = "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57"
VALIDATOR_SHA = "f658c653e9aba46cf38beac3ac2ffe7b14654d57ebdb7bba33adad5354ad83f6"
FOLDED = {
    "Trace": "0ebded79e1c0ad1dcfe68bb2f9f07745da6d531d1f6647d09ea29489eeefe662",
    "WholeWord": "5d647c31cce3d1c15265a4a86a162c5a68baa48afc2e27ef47ac5c2c5271dc62",
    "Safety": "7457b8cc978ca974dc61841abe2e46afcca7cdb4d94213c7745babd5ec140430",
    "Indexing": "42e6a23bbc66f0e582366a5eb0da8e5ef39ec0b435836c565fa71a645d87f3e3",
}
NEW = ("FiniteWords", "FamilyStates", "Products", "Obstruction")
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}

def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--mathlib", type=Path, required=True)
    parser.add_argument("--library-audit", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    lean, lib, out = args.lean.resolve(strict=True), args.mathlib.resolve(strict=True), args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    here = Path(__file__).resolve().parent
    repo = here.parents[3]
    validator = here.parent / "real-safe-weights/check.py"
    if digest(validator) != VALIDATOR_SHA:
        raise ValueError("The previously audited dependency validator changed.")
    spec = importlib.util.spec_from_file_location("agent13_library_validation", validator)
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load the pinned library validator.")
    shared = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(shared)
    version = subprocess.check_output([str(lean), "--version"], text=True)
    (out / "lean-version.txt").write_text(version)
    if "version 4.19.0," not in version or "6caaee842e94" not in version:
        raise ValueError("Exact Lean 4.19.0 compiler required.")
    library = shared.verify_library(lib, args.library_audit)
    (out / "LIBRARY.json").write_text(json.dumps(library, indent=2) + "\n")
    sources = [("LychrelDigitSums", repo / "proofs/research/continuation/LychrelDigitSums.lean", CORE_SHA)]
    sources += [(n, here.parent / "folded-binary-family" / (n + ".lean"), h) for n, h in FOLDED.items()]
    sources += [(n, here / (n + ".lean"), None) for n in NEW]
    hashes, names, steps = {}, [], []
    roots = [lib / ".lake/build/lib/lean"] + sorted((lib / ".lake/packages").glob("*/.lake/build/lib/lean"))
    with tempfile.TemporaryDirectory(prefix="agent13-product-clean-") as temp:
        build = Path(temp)
        for name, source, expected in sources:
            data = source.read_bytes()
            actual = hashlib.sha256(data).hexdigest()
            if expected is not None and actual != expected:
                raise ValueError(f"Previously checked source changed: {name}")
            hashes[str(source.relative_to(repo))] = actual
            (build / source.name).write_bytes(data)
            if name != "LychrelDigitSums":
                ns = "Agent13FoldedFamily" if name in FOLDED else "Agent13ProductWeights"
                names += [ns + "." + n for n in re.findall(r"^theorem\s+(\w+)", data.decode(), re.MULTILINE)]
        audit = "import Obstruction\n\n" + "\n".join("#print axioms " + n for n in names) + "\n"
        (build / "AllAxioms.lean").write_text(audit)
        (out / "AllAxioms.lean").write_text(audit)
        env = os.environ.copy()
        env["LEAN_PATH"] = ":".join(str(p) for p in [build, *roots])
        for name in [n for n, _, _ in sources] + ["AllAxioms"]:
            cmd = [str(lean), "-o", name + ".olean", name + ".lean"]
            start = time.monotonic()
            try:
                with (out / (name + ".log")).open("wb") as log:
                    result = subprocess.run(cmd, cwd=build, env=env, stdout=log,
                                            stderr=subprocess.STDOUT, timeout=600, check=False)
                status = result.returncode
            except subprocess.TimeoutExpired:
                status = "TIMEOUT_600_SECONDS"
            steps.append({"module": name, "command": cmd, "exit": status,
                          "seconds": round(time.monotonic()-start, 3)})
            (out / "build-steps.json").write_text(json.dumps(steps, indent=2) + "\n")
            if status != 0:
                raise SystemExit(f"Build did not pass: {name}; retained logs give the exact result.")
        text = (out / "AllAxioms.log").read_text()
        reports = re.findall(r"'([^']+)' (?:depends on axioms: \[([^]]*)\]|does not depend on any axioms)", text)
        if {n for n, _ in reports} != set(names) or len(reports) != len(names):
            raise ValueError("Incomplete or duplicate exported-theorem axiom reports.")
        for name, axes in reports:
            actual = {a.strip() for a in axes.split(",") if a.strip()}
            if not actual <= ALLOWED:
                raise ValueError(f"Rejected transitive axioms: {name}: {actual}")
    report = {"agent": 13, "source_snapshot": "c2b6977e43a79caa5ff3bb88801f3ba896986f38",
              "verification": "LEAN_CHECKED; fresh contribution and decimal-core source build; independent review pending",
              "version": version.strip(), "library": library, "source_sha256": hashes,
              "exported_theorems": names, "theorem_count": len(names), "axiom_audits": len(reports),
              "allowed_axioms": sorted(ALLOWED), "steps": steps}
    (out / "RESULT.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
