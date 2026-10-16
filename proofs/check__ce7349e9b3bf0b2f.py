#!/usr/bin/env python3
"""Fresh Lean build and axiom audit for the actual no-four-returns theorem.

Default: rebuild every project source, with bounded phase-check parallelism.
--collect-build: finish/audit an explicitly recorded fresh dependency + rank
build. This avoids repeating the expensive finite kernel checks solely to
collect the final endpoint theorem and its transitive-axiom report.
"""
from __future__ import annotations

import argparse
import concurrent.futures
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
BASE = [ROOT / "proofs/research/continuation/LychrelDigitSums.lean"] + [
    HERE.parent / "2026-10-14-seven-step-formal" / (name + ".lean")
    for name in ("BoundaryTransducer", "ActualBoundary", "SevenStepOrbit")]
BEFORE = ["SixPrefix", "ClockPaths"]
RANK = ["RankData"] + [f"RankChecks{i}" for i in range(7)] + ["RankChecks", "RankCertificate"]
AFTER = ["ActualRank", "NoFourReturns"]
SOURCES = BASE + [HERE / (name + ".lean") for name in BEFORE + RANK + AFTER]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def uncomment(source: str) -> str:
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--collect-build", type=Path)
    parser.add_argument("--workers", default=1, type=int, choices=range(1, 5))
    args = parser.parse_args()
    lean = str(args.lean.resolve())
    data = {p.stem: p.read_bytes() for p in SOURCES}
    assert sha(data["LychrelDigitSums"]) == BASE_SHA256
    imports = {}
    for name, content in data.items():
        names = [item for line in re.findall(r"^import\s+([^\n]+)", uncomment(content.decode()), re.M)
                 for item in line.split()]
        assert set(names) <= set(data) | {"Std", "Init"}, (name, names)
        imports[name] = [item for item in names if item in data]
    imports["AllAxioms"] = ["NoFourReturns"]
    expected = []
    for p in SOURCES[1:]:
        code = uncomment(data[p.stem].decode())
        assert not re.search(r"\b(?:sorry|admit|native_decide|axiom|sorryAx)\b", code), p
        namespace = "RankCertificate" if p.stem.startswith("Rank") else p.stem
        expected.extend(namespace + "." + name for name in re.findall(r"^theorem\s+(\w+)", code, re.M))
    assert len(expected) == len(set(expected))
    audit = "import NoFourReturns\n\n" + "\n".join("#print axioms " + n for n in expected) + "\n"
    (HERE / "AllAxioms.lean").write_text(audit)
    version = subprocess.run([lean, "--version"], capture_output=True, text=True, check=True).stdout.strip()
    assert "version 4.19.0," in version
    temporary = None
    if args.collect_build:
        build = args.collect_build.resolve()
    else:
        temporary = tempfile.TemporaryDirectory(prefix="p196-four-returns-fresh-")
        build = Path(temporary.name)
    env = dict(os.environ, LEAN_PATH=str(build))
    records = {}

    def fingerprints(name: str) -> dict:
        return {dep: {"source_sha256": sha((build/(dep+".lean")).read_bytes()),
                      "olean_sha256": sha((build/(dep+".olean")).read_bytes())}
                for dep in imports[name]}

    def compile_module(name: str) -> dict:
        content = audit.encode() if name == "AllAxioms" else data[name]
        (build / (name + ".lean")).write_bytes(content)
        command = [lean, "-j1", "-DElab.async=false", "-o", name + ".olean", name + ".lean"]
        dependencies_before = fingerprints(name)
        started = time.monotonic()
        proc = subprocess.run(command, cwd=build, env=env, capture_output=True, text=True)
        output = proc.stdout + proc.stderr
        (build / (name + ".log")).write_text(output)
        record = dict(module=name, command=command, seconds=round(time.monotonic()-started, 3),
                      exit_code=proc.returncode, source_sha256=sha(content), log_sha256=sha(output.encode()),
                      dependency_fingerprints=dependencies_before,
                      dependencies_unchanged=fingerprints(name) == dependencies_before)
        print(json.dumps(record), flush=True)
        assert proc.returncode == 0, (name, output)
        assert record["dependencies_unchanged"], name
        assert "declaration uses 'sorry'" not in output
        record["olean_sha256"] = sha((build / (name + ".olean")).read_bytes())
        return record

    if args.collect_build:
        dependencies = json.loads((build / "dependency_build.json").read_text())
        ranks = json.loads((build / "rank_build.json").read_text())
        assert ranks["status"] == "PASS"
        for record in dependencies:
            name = record["module"]
            assert name in [p.stem for p in BASE] + BEFORE
            assert record["source_sha256"] == sha(data[name]) and record["exit_code"] == 0
            records[name] = dict(record)
        assert set(records) == {p.stem for p in BASE} | set(BEFORE)
        for name in RANK:
            record = ranks["modules"][name]
            assert record["exit_code"] == 0 and record["source_unchanged"]
            assert record["source_sha256"] == sha(data[name])
            assert record["olean_sha256"] == sha((build/(name+".olean")).read_bytes())
            assert record["log_sha256"] == sha((build/(name+".log")).read_bytes())
            records[name] = dict(module=name, **record)
        for name in records:
            assert (build/(name+".lean")).read_bytes() == data[name]
            assert records[name]["olean_sha256"] == sha((build/(name+".olean")).read_bytes()), name
            assert records[name]["log_sha256"] == sha((build/(name+".log")).read_bytes()), name
            assert records[name].get("dependencies_unchanged") is True, name
            assert records[name].get("dependency_fingerprints") == fingerprints(name), name
        for name, imported in ranks["imports"].items():
            assert imported["source_sha256"] == sha(data[name])
            assert imported["olean_sha256"] == records[name]["olean_sha256"]
    else:
        for p in BASE:
            records[p.stem] = compile_module(p.stem)
        for name in BEFORE + ["RankData"]:
            records[name] = compile_module(name)
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            results = list(pool.map(compile_module, [f"RankChecks{i}" for i in range(7)]))
        for record in results:
            records[record["module"]] = record
        for name in ["RankChecks", "RankCertificate"]:
            records[name] = compile_module(name)
    for name in AFTER + ["AllAxioms"]:
        records[name] = compile_module(name)
    axioms = {}
    output = (build/"AllAxioms.log").read_text()
    for match in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", output, re.S):
        name = match.group(1)
        assert name not in axioms
        found = {x.strip() for x in (match.group(2) or "").split(",") if x.strip()}
        assert found <= ALLOWED, (name, found)
        axioms[name] = sorted(found)
    assert set(axioms) == set(expected), sorted(set(expected)-set(axioms))
    for p in SOURCES:
        assert p.read_bytes() == data[p.stem], f"source changed: {p}"
    ordered = [p.stem for p in SOURCES] + ["AllAxioms"]
    logs = [version + "\n"]
    for name in ordered:
        logs.append(json.dumps(records[name]) + "\n" + (build/(name+".log")).read_text())
    (HERE/"compile.log").write_text("\n".join(logs))
    report = dict(status="PASS", compiler=version, modules=[records[n] for n in ordered],
        source_sha256={p.name: sha(data[p.stem]) for p in SOURCES},
        checker_sha256=sha(Path(__file__).read_bytes()), all_axioms_source_sha256=sha(audit.encode()),
        compiler_binary_sha256=sha(Path(lean).read_bytes()),
        auxiliary_sha256={name: sha((HERE/name).read_bytes()) for name in
            ("generate_rank_certificate.py", "verify_rank_certificate.py")},
        fresh_project_dependency_build=True, imported_preexisting_project_oleans=False,
        collected_recorded_build=bool(args.collect_build),
        preliminary_build_note=("Earlier asynchronous phase builds exceeded available memory or were stopped to prevent it; no failed phase object was accepted. The recorded successful build uses synchronous elaboration." if args.collect_build else "Fresh build performed by this invocation."),
        theorem_count=len(axioms), theorem_axioms=axioms,
        axiom_union=sorted({a for values in axioms.values() for a in values}),
        forbidden_proof_tokens_absent=True, sources_unchanged_during_build=True,
        readlink_compatibility_used="readlink_self.so" in os.environ.get("LD_PRELOAD", ""),
        finite_domain=dict(phases=7,tail_coefficients_per_position=19,vertices=48013,boolean_controls=96026),
        scope="Actual admissible decimal pair-word orbit: at most 26 prescribed clock transitions, at most three consecutive seven-step 440 returns. Does not imply palindrome occurrence or prove P196.")
    (HERE/"verification.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(dict(status="PASS", theorem_count=len(axioms))), flush=True)
    if temporary:
        temporary.cleanup()


if __name__ == "__main__":
    main()
