"""Fresh Lean 4.19 rebuild and a transitive axiom audit of every new theorem.

Run from any directory: python check.py /absolute/path/to/lean-wrapper
No old source is modified. Generated build and audit files stay beside this file.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
COMPILER = Path(sys.argv[1]).resolve()
BUILD = HERE / "fresh_build"
BUILD.mkdir(exist_ok=True)
MODULES = {
    "SafeDelay": "SafeImageDynamics",
    "DecimalSafeRuns": "DecimalSafeRuns",
    "DecimalDelayBridge": "DecimalDelayBridge",
    "PairDelayBridge": "PairDelayBridge",
}
SOURCES = [PROJECT / "continuation/LychrelDigitSums.lean"] + [
    HERE / (name + ".lean") for name in MODULES
]
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def axioms_in(output):
    result = {}
    for match in re.finditer(
            r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|"
            r"does not depend on any axioms)", output, re.S):
        names = {s.strip() for s in (match.group(2) or "").split(",") if s.strip()}
        assert names <= ALLOWED, (match.group(1), names)
        result[match.group(1)] = sorted(names)
    return result


def without_comments(source):
    """Remove nested Lean block comments and ordinary line comments."""
    out, pos, depth = [], 0, 0
    while pos < len(source):
        if source.startswith("/-", pos):
            depth += 1
            pos += 2
        elif depth and source.startswith("-/", pos):
            depth -= 1
            pos += 2
        elif depth:
            pos += 1
        elif source.startswith("--", pos):
            end = source.find("\n", pos)
            pos = len(source) if end < 0 else end
        else:
            out.append(source[pos])
            pos += 1
    assert depth == 0
    return "".join(out)


hashes = {p.name: digest(p) for p in SOURCES}
version = subprocess.run([str(COMPILER), "--version"], capture_output=True,
                         text=True, check=True).stdout.strip()
assert "version 4.19.0" in version, version
env = dict(os.environ, LEAN_PATH=str(BUILD))
for name in [p.stem for p in SOURCES] + ["AllAxioms"]:
    for suffix in (".olean", ".ilean"):
        (BUILD / (name + suffix)).unlink(missing_ok=True)

expected = []
for module, namespace in MODULES.items():
    text = without_comments((HERE / (module + ".lean")).read_text())
    assert not re.search(r"\b(?:sorry|admit|native_decide|axiom)\b", text), module
    expected.extend(namespace + "." + name for name in re.findall(
        r"^theorem\s+(\w+)", text, re.M))

audit_source = "\n".join("import " + m for m in MODULES) + "\n\n"
audit_source += "\n".join("#print axioms " + name for name in expected) + "\n"
(HERE / "AllAxioms.lean").write_text(audit_source)
sources_to_compile = SOURCES + [HERE / "AllAxioms.lean"]
records, logs, audit = [], [version + "\n"], {}
for source in sources_to_compile:
    shutil.copy2(source, BUILD / source.name)
    started = time.monotonic()
    proc = subprocess.run([str(COMPILER), "-o", source.stem + ".olean", source.name],
                          cwd=BUILD, env=env, capture_output=True, text=True)
    record = {"module": source.stem, "exit_code": proc.returncode,
              "seconds": time.monotonic() - started}
    records.append(record)
    output = proc.stdout + proc.stderr
    logs.append(json.dumps(record) + "\n" + output)
    (HERE / "compile.log").write_text("\n".join(logs))
    print(json.dumps(record), flush=True)
    if proc.returncode:
        raise SystemExit(proc.returncode)
    found = axioms_in(output)
    if source.stem == "AllAxioms":
        audit = found

assert set(audit) == set(expected), {"missing": sorted(set(expected) - set(audit))}
assert hashes == {p.name: digest(p) for p in SOURCES}, "a source changed during compilation"
(HERE / "verification.json").write_text(json.dumps({
    "status": "PASS", "compiler": version, "modules": records,
    "source_sha256": hashes, "new_theorems_audited": len(audit),
    "theorem_axioms": audit, "axioms_allowed": sorted(ALLOWED),
    "unconditional_arbitrary_safe_prefixes_proved": True,
    "safe_prefix_family": "candidate(D) = 2 * (10^(2*D+1) - 1), safe at indices 0 through D",
    "exact_pair_safe_image_first_positive_hit_equivalence_proved": True,
    "finite_delay_bound_hypothesis_discharged": False,
    "unbounded_finite_terminating_delays_proved": False,
    "decimal_lychrel_existence_proved": False,
}, indent=2) + "\n")
print(json.dumps({"status": "PASS", "new_theorems_audited": len(audit)}), flush=True)
