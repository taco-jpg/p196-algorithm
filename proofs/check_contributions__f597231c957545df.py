#!/usr/bin/env python3
"""Root's independent clean build of the published finite-prefix contributions.

Sources are read without modifying the other contributor's files. All six
modules are rebuilt together once; every new theorem is audited. Defaults
work in the published proofs/research layout. Overrides support a split
local checkout during concurrent publication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lean")
    parser.add_argument("--research-root", type=Path, default=HERE.parents[2])
    parser.add_argument("--contributions-root", type=Path,
                        default=HERE.parents[3] / "contributions")
    args = parser.parse_args()
    lean = str(Path(args.lean).resolve())
    research, contributions = args.research_root, args.contributions_root
    corr = research / "main_existence_attempt/correlation_pass/lean"
    sources = [research / "continuation/LychrelDigitSums.lean"]
    sources += [corr / name for name in
                ("SafeDelay.lean", "DecimalSafeRuns.lean", "DecimalDelayBridge.lean")]
    sources += [contributions / "2026-10-14-safe-prefix/OverflowSafeRuns.lean",
                contributions / "2026-10-14-finite-horizon-density/FiniteHorizonBlocks.lean"]
    hashes = {p.name: digest(p) for p in sources}
    # Compare each exact source to the independently published verification
    # record before compiling. There are no downloaded compiled dependencies.
    for folder in ("2026-10-14-safe-prefix", "2026-10-14-finite-horizon-density"):
        record = json.loads((contributions / folder / "verification.json").read_text())
        for key, value in record["sources"].items():
            assert hashes[Path(key).name] == value["sha256"], key
    version = subprocess.check_output([lean, "--version"], text=True).strip()
    assert "version 4.19.0" in version, version
    names = {}
    for path in sources[-2:]:
        source = path.read_text()
        assert not re.search(r"\b(?:sorry|admit|axiom|native_decide)\b", source)
        names[path.stem] = re.findall(r"^theorem\s+(\w+)", source, re.M)
    expected = {f"{namespace}.{name}" for namespace, group in names.items() for name in group}
    report = HERE / "root_verification.json"
    report.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix="p196-root-contributions-") as tmp:
        build = Path(tmp)
        env = dict(os.environ, LEAN_PATH=str(build))
        with (HERE / "root_compile.log").open("w") as log:
            log.write(version + "\n")
            for source in sources:
                target = build / source.name
                shutil.copyfile(source, target)
                process = subprocess.run([lean, "-o", str(target.with_suffix(".olean")),
                                          str(target)], cwd=build, env=env,
                                         capture_output=True, text=True)
                log.write(f"\n### {source.name}\n{process.stdout}{process.stderr}")
                log.flush()
                assert process.returncode == 0, source.name
            audit_text = "import FiniteHorizonBlocks\n" + "\n".join(
                f"#print axioms {name}" for name in sorted(expected)) + "\n"
            (HERE / "RootAxioms.lean").write_text(audit_text)
            audit_path = build / "RootAxioms.lean"
            audit_path.write_text(audit_text)
            process = subprocess.run([lean, str(audit_path)], cwd=build, env=env,
                                     capture_output=True, text=True)
            log.write(f"\n### RootAxioms.lean\n{process.stdout}{process.stderr}")
            assert process.returncode == 0, "axiom audit"
            audited = {}
            for name, axioms in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",
                                          process.stdout):
                audited[name] = sorted(a.strip() for a in axioms.split(",") if a.strip())
            for name in re.findall(r"'([^']+)' does not depend on any axioms", process.stdout):
                audited[name] = []
            assert set(audited) == expected, (expected, audited)
            assert all(set(axioms) <= ALLOWED for axioms in audited.values())
    assert hashes == {p.name: digest(p) for p in sources}, "source changed during build"
    result = {"status": "PASS", "source_commit": "b7fa911dc4ca943528f5d28b67f3fbd87c9404ca",
              "lean_version": version, "fresh_dependency_rebuild": True,
              "theorem_count": len(expected), "source_sha256": hashes,
              "axiom_audit": audited,
              "scope": "Finite safe prefixes and deterministic mirrored-block safety only; counting and limits remain written proofs."}
    report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"PASS: all {len(expected)} published supporting theorems, clean source rebuild")


if __name__ == "__main__":
    main()
