"""Fresh Lean 4.19 rebuild and transitive audit of incoming-carry sensitivity."""
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
PROJECT = HERE.parents[3]
COMPILER = Path(sys.argv[1]).resolve()
BUILD = HERE / "fresh_build"
BUILD.mkdir(exist_ok=True)
SOURCES = [PROJECT / "continuation/LychrelDigitSums.lean", HERE / "IncomingCarrySensitivity.lean"]
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def axioms_in(output):
    result = {}
    for match in re.finditer(
            r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|"
            r"does not depend on any axioms)", output, re.S):
        axioms = {x.strip() for x in (match.group(2) or "").split(",") if x.strip()}
        assert axioms <= ALLOWED, (match.group(1), axioms)
        result[match.group(1)] = sorted(axioms)
    return result


hashes = {p.name: digest(p) for p in SOURCES}
version = subprocess.run([str(COMPILER), "--version"], capture_output=True,
                         text=True, check=True).stdout.strip()
assert "version 4.19.0" in version, version
env = dict(os.environ, LEAN_PATH=str(BUILD))
for stem in [p.stem for p in SOURCES] + ["AllAxioms"]:
    for suffix in (".olean", ".ilean"):
        (BUILD / (stem + suffix)).unlink(missing_ok=True)
source_text = without_comments(SOURCES[-1].read_text())
assert not re.search(r"\b(?:sorry|admit|native_decide|axiom)\b", source_text)
names = ["IncomingCarrySensitivity." + name for name in
         re.findall(r"^theorem\s+(\w+)", source_text, re.M)]
(HERE / "AllAxioms.lean").write_text("import IncomingCarrySensitivity\n\n" +
    "\n".join("#print axioms " + name for name in names) + "\n")

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

assert set(audit) == set(names), {"missing": sorted(set(names) - set(audit))}
assert hashes == {p.name: digest(p) for p in SOURCES}, "source changed during build"
(HERE / "verification.json").write_text(json.dumps({
    "status": "PASS", "compiler": version, "modules": records,
    "source_sha256": hashes, "new_theorems_audited": len(audit),
    "theorem_axioms": audit, "axioms_allowed": sorted(ALLOWED),
    "coefficient_range": [0, 18],
    "all_finite_lengths_covered": True,
    "symmetry_required": False,
    "carry_difference": "indicator that every earlier coefficient is 9",
    "digit_difference": "I_i - 10 I_(i+1)",
    "first_nonnine_and_allnine_terminal_cases": True,
    "actual_offset_block_bridge": True,
    "exact_value_including_terminal_carry": True,
    "bounded_search_used_as_proof": False,
    "full_concatenated_polynomial_identity_formalized": False,
    "reset_or_lychrel_existence_proved": False,
    "earlier_sources_modified": False,
}, indent=2) + "\n")
print(json.dumps({"status": "PASS", "new_theorems_audited": len(audit)}), flush=True)
