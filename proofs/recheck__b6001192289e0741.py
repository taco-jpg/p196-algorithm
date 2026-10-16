#!/usr/bin/env python3
"""Rebuild the pinned external overlap gate without editing its sources.

Requires Lean 4.19.0. By default reads the original paths in this checkout.
--source-dir accepts a flat directory containing the exact pinned sources.
Build products are isolated in a fresh temporary directory and discarded.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time


HERE = Path(__file__).resolve().parent
ALLOWED = {"propext", "Quot.sound", "Classical.choice"}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def without_comments(source):
    # Sufficient for this pinned Lean source: it contains no string literals.
    assert '"' not in source, "review lexical handling if source gains strings"
    position = depth = 0
    output = []
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
            output.append(source[position])
            position += 1
    assert depth == 0, "unclosed comment"
    return "".join(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--source-dir", type=Path)
    parser.add_argument("--repo-root", type=Path, default=HERE.parents[2])
    args = parser.parse_args()
    manifest = json.loads((HERE / "source_manifest.json").read_text())
    sources = {}
    for entry in manifest["sources"]:
        name = entry["name"]
        path = args.source_dir / name if args.source_dir else args.repo_root / entry["path"]
        data = path.read_bytes()
        assert sha256(data) == entry["sha256"], f"SHA256 mismatch: {name}"
        assert git_blob_sha(data) == entry["git_blob_sha"], f"Git blob mismatch: {name}"
        sources[name] = data

    lean = str(args.lean.resolve())
    version = subprocess.run([lean, "--version"], capture_output=True, text=True, check=True).stdout.strip()
    assert "version 4.19.0," in version, version
    gate = without_comments(sources["DelayedOverlapGate.lean"].decode())
    forbidden = re.findall(r"\b(?:sorry|admit|native_decide|axiom|sorryAx)\b", gate)
    assert not forbidden, forbidden
    declarations = ["DelayedOverlapGate." + name for name in re.findall(r"^theorem\s+(\w+)", gate, re.M)]
    assert len(declarations) == len(set(declarations)) == 49
    generated_audit = "import DelayedOverlapGate\n\n" + "\n".join("#print axioms " + n for n in declarations) + "\n"
    # Compare independent declaration discovery against the published audit list.
    assert generated_audit.encode() == sources["AllAxioms.lean"]
    published_report = json.loads(sources["verification.json"])
    modules = [entry["name"] for entry in manifest["sources"] if entry.get("compile")]
    records, logs, audited = [], [version + "\n"], {}

    with tempfile.TemporaryDirectory(prefix="p196-independent-gate-") as temporary:
        build = Path(temporary)
        environment = dict(os.environ, LEAN_PATH=str(build))
        for name in modules:
            (build / name).write_bytes(sources[name])
        audit_name = "IndependentGateAxioms.lean"
        (build / audit_name).write_text(generated_audit, encoding="utf-8")
        for name in modules + [audit_name]:
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
            assert proc.returncode == 0, f"compilation failed: {name}"
            assert "declaration uses 'sorry'" not in output
            if name == audit_name:
                for match in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", output, re.S):
                    theorem = match.group(1)
                    assert theorem not in audited, f"duplicate axiom report: {theorem}"
                    axioms = {value.strip() for value in (match.group(2) or "").split(",") if value.strip()}
                    assert axioms <= ALLOWED, (theorem, axioms)
                    audited[theorem] = sorted(axioms)

    assert set(audited) == set(declarations)
    assert audited == published_report["theorem_axioms"]
    # Re-read inputs to guard against concurrent edits during the build.
    for entry in manifest["sources"]:
        path = args.source_dir / entry["name"] if args.source_dir else args.repo_root / entry["path"]
        assert path.read_bytes() == sources[entry["name"]]
    result = dict(
        status="PASS", audited_commit=manifest["commit"], compiler=version,
        source_manifest_sha256=sha256((HERE / "source_manifest.json").read_bytes()),
        checker_sha256=sha256(Path(__file__).resolve().read_bytes()),
        all_source_bytes_match_remote_git_blobs=True, fresh_temporary_build=True,
        imported_precompiled_project_modules=False, original_files_modified=False,
        modules=records, theorem_count=len(audited), theorem_axioms=audited,
        axiom_union=sorted({value for values in audited.values() for value in values}),
        all_49_axiom_sets_match_published_report=True,
        gate_source_forbidden_tokens_absent=True,
        runtime_note="This environment used a libc readlink adapter only for numeric own-PID executable lookup; Lean parser, elaborator, kernel, and libraries were not changed.",
        mathematical_scope="Finite two-step overlap gate under its stated parameter domain; no recurrent family, all-time safety, or decimal Lychrel existence conclusion.",
    )
    (HERE / "verification.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(dict(status="PASS", theorem_count=len(audited))), flush=True)


if __name__ == "__main__":
    main()
