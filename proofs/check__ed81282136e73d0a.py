#!/usr/bin/env python3
"""Fresh Lean 4.19 rebuild and transitive-axiom audit of the actual spatial path lift."""

import argparse
import hashlib
import gzip
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
    (HERE / "verification.json").unlink(missing_ok=True)
    scalar = HERE.parent / "2026-10-15-scalar-clock-formal"
    sources = [ROOT / "proofs/research/continuation/LychrelDigitSums.lean"] + [
        scalar / (name + ".lean") for name in ("ScalarClock", "ActualScalar", "ScalarOrbit")
    ] + [HERE.parent / "2026-10-14-prefix-extension-formal/PrefixExtension.lean",
         HERE / "ActualPrefixLift.lean", HERE / "ScalarRoot.lean"]
    certificate = HERE.parent / "2026-10-14-component-specific-bound/component_certificates.json.gz"
    certificate_sha256 = digest(certificate.read_bytes())
    assert certificate_sha256 == "ff7a70ee2a6ed677cb9176e212dc0a69acd14eed30425a42b543d7a50823b47e"
    root_job = json.loads(gzip.decompress(certificate.read_bytes()))["jobs"][0]
    root_source = (HERE / "ScalarRoot.lean").read_text()
    table_text = root_source.split("def rootEdges", 1)[1].split("def root :", 1)[0]
    root_edges = [list(map(int, triple)) for triple in re.findall(
        r"\((\d+),\s*(\d+),\s*(\d+)\)", table_text)]
    assert root_edges == root_job["edges"]
    assert root_job["width"] == 1 and len(root_job["vertices"]) == 7
    data = {source.name: source.read_bytes() for source in sources}
    assert digest(data["LychrelDigitSums.lean"]) == BASE_SHA256
    imports = {}
    for name, content in data.items():
        direct = [token for line in re.findall(r"^import\s+([^\n]+)", uncomment(content.decode()), re.M)
                  for token in line.split()]
        assert set(direct) <= {Path(n).stem for n in data} | {"Std", "Init"}
        imports[Path(name).stem] = [n for n in direct if n + ".lean" in data]
    expected = []
    for source in sources[1:]:
        code = uncomment(data[source.name].decode())
        assert not re.search(r"\b(?:sorry|admit|native_decide|axiom|sorryAx)\b", code), source.name
        expected.extend(source.stem + "." + name for name in
                        re.findall(r"^theorem\s+(\w+)", code, re.M))
    assert len(expected) == len(set(expected))
    audit_source = "\n".join("import " + p.stem for p in sources[1:]) + "\n\n"
    imports["AllAxioms"] = [p.stem for p in sources[1:]]
    audit_source += "\n".join("#print axioms " + name for name in expected) + "\n"
    (HERE / "AllAxioms.lean").write_text(audit_source, encoding="utf-8")
    version = subprocess.run([lean, "--version"], capture_output=True, text=True, check=True).stdout.strip()
    assert "version 4.19.0," in version
    records, logs, axioms = [], [version + "\n"], {}
    with tempfile.TemporaryDirectory(prefix="p196-actual-prefix-lift-fresh-") as temporary:
        build = Path(temporary)
        environment = dict(os.environ, LEAN_PATH=str(build))
        for name, content in data.items():
            (build / name).write_bytes(content)
        (build / "AllAxioms.lean").write_text(audit_source, encoding="utf-8")
        for name in [p.name for p in sources] + ["AllAxioms.lean"]:
            stem = Path(name).stem
            def fingerprints():
                return {dep: {"source_sha256": digest((build/(dep+".lean")).read_bytes()),
                              "olean_sha256": digest((build/(dep+".olean")).read_bytes())}
                        for dep in imports[stem]}
            before = fingerprints()
            started = time.monotonic()
            proc = subprocess.run([lean, "-j1", "-DElab.async=false", "-o", stem + ".olean", name],
                                  cwd=build, env=environment, capture_output=True, text=True)
            record = dict(module=stem, exit_code=proc.returncode,
                          seconds=round(time.monotonic()-started, 3),
                          source_sha256=digest((build/name).read_bytes()),
                          dependency_fingerprints=before,
                          dependencies_unchanged=fingerprints() == before,
                          command=[lean,"-j1","-DElab.async=false","-o",stem+".olean",name])
            records.append(record)
            output = proc.stdout + proc.stderr
            record["log_sha256"] = digest(output.encode())
            if proc.returncode == 0:
                record["olean_sha256"] = digest((build/(stem+".olean")).read_bytes())
            logs.append(json.dumps(record) + "\n" + output)
            (HERE / "compile.log").write_text("\n".join(logs), encoding="utf-8")
            print(json.dumps(record), flush=True)
            assert proc.returncode == 0, name
            assert record["dependencies_unchanged"], name
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
        new_theorem_count=sum(name.startswith(("ActualPrefixLift.", "ScalarRoot.")) for name in axioms),
        frozen_root_certificate_sha256=certificate_sha256,
        exact_root_edge_table_matches_frozen_job_zero=True,
        axiom_union=sorted({a for values in axioms.values() for a in values}),
        forbidden_proof_tokens_absent=True, sources_unchanged_during_build=True,
        readlink_compatibility_used="readlink_self.so" in os.environ.get("LD_PRELOAD", ""),
        scope="Constructed actual one-column path lift, interval/component restriction, finite-ID transport interface, exact scalar root and actual first133-vertex lift. Later component data and scalar94/98 hierarchy are not instantiated. No P196 claim.",
    )
    (HERE / "verification.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(dict(status="PASS", theorem_count=len(axioms))), flush=True)


if __name__ == "__main__":
    main()
