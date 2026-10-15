#!/usr/bin/env python3
"""Fresh, exact-source audit of the external 42-theorem raw-symmetry module.

This does not import or execute the preserved upstream checker.  All local
dependencies are rebuilt in an empty temporary directory.  Only source,
compiler output, and the resulting audit report are retained.
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
import time

HERE = Path(__file__).resolve().parent
MODULES = ["LychrelDigitSums", "IncomingCarrySensitivity", "RawSymmetryObstruction"]
EXPECTED = {
    "LychrelDigitSums": "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57",
    "IncomingCarrySensitivity": "52850d75999a8fdad298e2e9da638965472ab6507f88630bf428698576ac631f",
    "RawSymmetryObstruction": "922b660e5b3ac42389cd6ea00885075327d4b44fb315b9cc496e1323890e9c87",
}
IMPORTS = {
    "LychrelDigitSums": ["Std"],
    "IncomingCarrySensitivity": ["LychrelDigitSums"],
    "RawSymmetryObstruction": ["IncomingCarrySensitivity"],
}
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lean_code(text: str) -> str:
    """Mask nested comments and quoted strings while retaining line positions."""
    out = list(text)
    i = 0
    while i < len(text):
        if text.startswith("--", i):
            end = text.find("\n", i)
            end = len(text) if end == -1 else end
        elif text.startswith("/-", i):
            depth, end = 1, i + 2
            while depth:
                assert end < len(text), "Unclosed Lean block comment"
                if text.startswith("/-", end):
                    depth, end = depth + 1, end + 2
                elif text.startswith("-/", end):
                    depth, end = depth - 1, end + 2
                else:
                    end += 1
        elif text[i] == '"':
            end = i + 1
            while end < len(text) and text[end] != '"':
                end += 2 if text[end] == "\\" else 1
            assert end < len(text), "Unclosed Lean string"
            end += 1
        else:
            i += 1
            continue
        for j in range(i, end):
            if text[j] != "\n":
                out[j] = " "
        i = end
    return "".join(out)


def verify_manifest() -> dict:
    manifest = json.loads((HERE / "source_manifest.json").read_text())
    assert manifest["commit"] == "4c3970c04f7997db76f82a5806168b2d0790cfb3"
    for item in manifest["files"]:
        data = (HERE / item["local_path"]).read_bytes()
        assert len(data) == item["bytes"]
        assert sha(data) == item["sha256"], item["local_path"]
        git_blob = b"blob " + str(len(data)).encode() + b"\0" + data
        assert hashlib.sha1(git_blob).hexdigest() == item["git_blob_sha1"]
    return manifest


def run(args: argparse.Namespace) -> dict:
    manifest = verify_manifest()
    clean = {}
    for module in MODULES:
        data = (HERE / "sources" / (module + ".lean")).read_bytes()
        assert sha(data) == EXPECTED[module]
        clean[module] = lean_code(data.decode())
        forbidden = re.findall(r"\b(?:sorry|admit|axiom|native_decide)\b", clean[module])
        assert not forbidden, (module, forbidden)
        imports = re.findall(r"^import\s+(\S+)\s*$", clean[module], re.M)
        assert imports == IMPORTS[module], (module, imports)
    target = clean["RawSymmetryObstruction"]
    assert re.findall(r"^namespace\s+(\S+)", target, re.M) == ["RawSymmetryObstruction"]
    names = re.findall(r"^theorem\s+([A-Za-z_][A-Za-z_0-9']*)\b", target, re.M)
    assert len(names) == len(set(names)) == 42
    assert not re.search(r"^\s*(?:private\s+)?lemma\b", target, re.M)
    qualified = ["RawSymmetryObstruction." + name for name in names]
    upstream = json.loads((HERE / "sources" / "verification.json").read_text())
    assert set(qualified) == set(upstream["theorem_axioms"])
    audit = "import RawSymmetryObstruction\n\n" + "".join(
        "#print axioms " + name + "\n" for name in qualified
    )
    (HERE / "Audit42.lean").write_text(audit)
    logs = HERE / "logs"
    logs.mkdir(exist_ok=True)
    env = os.environ.copy()
    if args.preload:
        env["LD_PRELOAD"] = str(Path(args.preload).resolve())
    lean = str(Path(args.lean).resolve()) if "/" in args.lean else args.lean
    version = subprocess.run([lean, "--version"], env=env, text=True,
                             capture_output=True, check=True)
    compiler = version.stdout.strip()
    assert "version 4.19.0" in compiler, compiler
    (logs / "version.log").write_text(version.stdout + version.stderr)
    records = []
    with tempfile.TemporaryDirectory(prefix="p196-independent-raw-symmetry-") as temp:
        build = Path(temp)
        env["LEAN_PATH"] = str(build)
        for module in MODULES:
            shutil.copyfile(HERE / "sources" / (module + ".lean"), build / (module + ".lean"))
        (build / "Audit42.lean").write_text(audit)
        for module in MODULES + ["Audit42"]:
            command = [lean, "-j1", "-DElab.async=false", "-o", module + ".olean", module + ".lean"]
            start = time.monotonic()
            proc = subprocess.run(command, cwd=build, env=env, text=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            elapsed = time.monotonic() - start
            (logs / (module + ".log")).write_text(proc.stdout)
            records.append({"module": module, "exit_code": proc.returncode,
                            "seconds": round(elapsed, 6), "command": command,
                            "log_sha256": sha(proc.stdout.encode())})
            print(json.dumps(records[-1]), flush=True)
            assert proc.returncode == 0, (module, proc.returncode)
            assert (build / (module + ".olean")).is_file(), module
        output = (logs / "Audit42.log").read_text()
    axioms = {}
    pattern = r"'([^']+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)"
    for match in re.finditer(pattern, output):
        name, values = match.groups()
        assert name not in axioms, name
        axioms[name] = sorted(x.strip() for x in (values or "").split(",") if x.strip())
    assert set(axioms) == set(qualified), (len(axioms), set(qualified) - set(axioms))
    for name, values in axioms.items():
        assert set(values) <= STANDARD_AXIOMS, (name, values)
    assert verify_manifest() == manifest
    return {
        "status": "PASS_FRESH_EXACT_SOURCE_42",
        "repository": manifest["repository"], "commit": manifest["commit"],
        "compiler": compiler, "serialized_elaboration": True,
        "fresh_dependencies": MODULES[:-1], "source_sha256": EXPECTED,
        "source_manifest_sha256": sha((HERE / "source_manifest.json").read_bytes()),
        "checker_sha256": sha(Path(__file__).read_bytes()),
        "generated_audit_sha256": sha((HERE / "Audit42.lean").read_bytes()),
        "modules": records, "new_theorems_audited": len(qualified),
        "theorem_axioms": axioms, "allowed_axioms": sorted(STANDARD_AXIOMS),
        "source_placeholders_custom_axioms_native_decide": "absent",
        "imports_exact": IMPORTS, "all_preserved_bytes_unchanged": True,
        "fresh_build_directory_deleted": True,
        "scope": "42 target declarations audited transitively after exact-source dependency rebuild; not an audit of every renewal module or an all-time invariant."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lean", help="Lean 4.19.0 executable or wrapper")
    parser.add_argument("--preload", help="Optional existing executable-path compatibility shim")
    args = parser.parse_args()
    report = HERE / "independent_verification.json"
    report.write_text(json.dumps({"status": "RUNNING"}) + "\n")
    try:
        result = run(args)
    except Exception as exc:
        report.write_text(json.dumps({"status": "FAIL", "error": repr(exc)}, indent=2) + "\n")
        raise
    report.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "theorems": result["new_theorems_audited"]}))


if __name__ == "__main__":
    main()
