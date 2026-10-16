"""Fresh Lean 4.19 rebuild and full transitive axiom audit of the delayed gate.

Run from any directory: python check.py /absolute/path/to/lean-wrapper
Older source files are copied and checked without modification.
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
PRIOR = PROJECT / "main_existence_attempt/correlation_pass/lean"
SOURCES = [PROJECT / "continuation/LychrelDigitSums.lean"] + [
    PRIOR / (name + ".lean") for name in
    ["SafeDelay", "DecimalSafeRuns", "DecimalDelayBridge", "PairDelayBridge"]
] + [HERE / "DelayedOverlapGate.lean"]
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

source_text = without_comments((HERE / "DelayedOverlapGate.lean").read_text())
assert not re.search(r"\b(?:sorry|admit|native_decide|axiom)\b", source_text)
expected = ["DelayedOverlapGate." + name for name in re.findall(
    r"^theorem\s+(\w+)", source_text, re.M)]
audit_source = "import DelayedOverlapGate\n\n" + "\n".join(
    "#print axioms " + name for name in expected) + "\n"
(HERE / "AllAxioms.lean").write_text(audit_source)

records, logs, audit = [], [version + "\n"], {}
for source in SOURCES + [HERE / "AllAxioms.lean"]:
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
assert hashes == {p.name: digest(p) for p in SOURCES}, "source changed during compilation"
result = {
    "status": "PASS", "compiler": version, "modules": records,
    "source_sha256": hashes, "new_theorems_audited": len(audit),
    "theorem_axioms": audit, "axioms_allowed": sorted(ALLOWED),
    "parameter_domain": "r>=1, 1<=p<=4, u>=1, v>=5, u+v<=8",
    "all_r_gate_transitions_proved": True,
    "outside_coefficient_extension_p_1_through_4_proved": True,
    "coefficient_and_normalized_digit_defects_proved": True,
    "actual_decimal_realizability_discharged": True,
    "every_realization_positive_steps_1_and_2_safe": True,
    "third_step_palindrome_iff": "p<=2 and u=1 and v=5",
    "returned_parameters_outside_gate_domain_proved": True,
    "global_overflow_transport_p_ge_5_formalized": False,
    "recurrent_family_certificate_proved": False,
    "decimal_lychrel_existence_proved": False,
    "older_sources_modified": False,
}
(HERE / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": "PASS", "new_theorems_audited": len(audit)}), flush=True)
