#!/usr/bin/env python3
"""Fresh Lean 4.19 rebuild and transitive-axiom audit of the actual boundary gate."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ALLOWED = {"propext", "Quot.sound", "Classical.choice"}
BASE_SHA256 = "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def uncomment(source):
    depth = position = 0
    result = []
    while position < len(source):
        if source.startswith("/-", position):
            depth += 1
            position += 2
        elif depth and source.startswith("-/", position):
            depth -= 1
            position += 2
        elif depth:
            position += 1
        elif source.startswith("--", position):
            end = source.find("\n", position)
            position = len(source) if end < 0 else end
        else:
            result.append(source[position])
            position += 1
    assert depth == 0
    return "".join(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path)
    args = parser.parse_args()
    lean = str(args.lean.resolve())
    sources = [ROOT / "proofs/research/continuation/LychrelDigitSums.lean"] + [
        HERE / (name + ".lean") for name in
        ("BoundaryTransducer", "ActualBoundary", "SevenStepOrbit")]
    data = {source.name: source.read_bytes() for source in sources}
    assert digest(data["LychrelDigitSums.lean"]) == BASE_SHA256
    expected = []
    for source in sources[1:]:
        code = uncomment(data[source.name].decode())
        assert not re.search(r"\b(?:sorry|admit|native_decide|axiom|sorryAx)\b", code), source.name
        expected.extend(source.stem + "." + name for name in
                        re.findall(r"^theorem\s+(\w+)", code, re.M))
    assert len(expected) == len(set(expected))
    audit_source = "\n".join("import " + p.stem for p in sources[1:]) + "\n\n"
    audit_source += "\n".join("#print axioms " + name for name in expected) + "\n"
    (HERE / "AllAxioms.lean").write_text(audit_source, encoding="utf-8")
    version = subprocess.run([lean, "--version"], capture_output=True, text=True, check=True).stdout.strip()
    assert "version 4.19.0," in version
    records, logs, axioms = [], [version + "\n"], {}
    with tempfile.TemporaryDirectory(prefix="p196-seven-step-fresh-") as temporary:
        build = Path(temporary)
        environment = dict(os.environ, LEAN_PATH=str(build))
        for name, content in data.items():
            (build / name).write_bytes(content)
        (build / "AllAxioms.lean").write_text(audit_source, encoding="utf-8")
        for name in [p.name for p in sources] + ["AllAxioms.lean"]:
            stem = Path(name).stem
            started = time.monotonic()
            proc = subprocess.run([lean, "-o", stem + ".olean", name],
                                  cwd=build, env=environment, capture_output=True, text=True)
            record = dict(module=stem, exit_code=proc.returncode,
                          seconds=round(time.monotonic()-started, 3))
            records.append(record)
            output = proc.stdout + proc.stderr
            logs.append(json.dumps(record) + "\n" + output)
            (HERE / "compile.log").write_text("\n".join(logs), encoding="utf-8")
            print(json.dumps(record), flush=True)
            assert proc.returncode == 0, name
            assert "declaration uses 'sorry'" not in output
            if name == "AllAxioms.lean":
                for match in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", output, re.S):
                    theorem = match.group(1)
                    assert theorem not in axioms
                    found = {a.strip() for a in (match.group(2) or "").split(",") if a.strip()}
                    assert found <= ALLOWED, (theorem, found)
                    axioms[theorem] = sorted(found)
    assert set(axioms) == set(expected), sorted(set(expected)-set(axioms))
    for source in sources:
        assert source.read_bytes() == data[source.name], f"source changed: {source}"
    result = dict(
        status="PASS", compiler=version, modules=records,
        source_sha256={name: digest(content) for name, content in data.items()},
        checker_sha256=digest(Path(__file__).resolve().read_bytes()),
        all_axioms_source_sha256=digest(audit_source.encode()),
        fresh_temporary_build=True, imported_old_project_oleans=False,
        theorem_count=len(axioms), theorem_axioms=axioms,
        axiom_union=sorted({a for values in axioms.values() for a in values}),
        forbidden_proof_tokens_absent=True, sources_unchanged_during_build=True,
        readlink_compatibility_used="readlink_self.so" in os.environ.get("LD_PRELOAD", ""),
        scope="Exact actual-boundary transducer and finite seven-step return criterion. Controls are whole-word carries. No infinite recurrence or P196 claim.",
    )
    (HERE / "verification.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(dict(status="PASS", theorem_count=len(axioms))), flush=True)


if __name__ == "__main__":
    main()
