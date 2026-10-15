#!/usr/bin/env python3
"""Fresh Lean 4.19.0 build and complete axiom audit of the seam contribution.

Every run starts from an empty, isolated build directory. No development
objects or earlier accepted objects are reused. A wrapper is accepted; an
in-process Lean probe records the actual executable and preload libraries.
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
import sys
import tempfile
import time


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
FLAGS = ["-j1", "-DElab.async=false"]
SCHEMA = 1
NEW_MODULES = ["SeamCoefficients", "SeamRuns", "SeamMass", "PartitionMass", "PairResponse",
               "PairClosure", "PartitionDefect"]
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
BASE_SHA256 = "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57"
PROBE = '''def main : IO Unit := do
  IO.println s!"P196_NATIVE={← IO.appPath}"
  IO.println s!"P196_PRELOAD={(← IO.getEnv "LD_PRELOAD").getD ""}"
'''


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def sha_bytes(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def code_only(source: str, *, blank_strings: bool = True) -> str:
    """Blank nested comments, optionally strings, while preserving newlines."""
    result = []
    position = depth = 0
    in_string = False
    while position < len(source):
        char = source[position]
        if depth:
            if source.startswith("/-", position):
                depth += 1
                result.extend("  ")
                position += 2
            elif source.startswith("-/", position):
                depth -= 1
                result.extend("  ")
                position += 2
            else:
                result.append("\n" if char == "\n" else " ")
                position += 1
        elif in_string:
            if char == "\\" and position + 1 < len(source):
                result.extend("  " if blank_strings else source[position:position + 2])
                position += 2
            else:
                result.append(("\n" if char == "\n" else " ") if blank_strings else char)
                position += 1
                if char == '"':
                    in_string = False
        elif source.startswith("/-", position):
            depth = 1
            result.extend("  ")
            position += 2
        elif source.startswith("--", position):
            end = source.find("\n", position)
            if end < 0:
                end = len(source)
            result.extend(" " * (end - position))
            position = end
        elif char == '"':
            in_string = True
            result.append(" " if blank_strings else char)
            position += 1
        else:
            result.append(char)
            position += 1
    require(depth == 0 and not in_string, "Unterminated Lean comment or string")
    return "".join(result)


def source_paths() -> dict[str, Path]:
    paths = {
        "LychrelDigitSums": REPO / "proofs/research/continuation/LychrelDigitSums.lean",
        "IncomingCarrySensitivity": REPO / "proofs/research/main_existence_attempt/renewal_pass/lean/incoming_carry/IncomingCarrySensitivity.lean",
        "RawSymmetryObstruction": REPO / "proofs/research/main_existence_attempt/renewal_pass/lean/raw_symmetry/RawSymmetryObstruction.lean",
        "IncomingCarry": REPO / "proofs/contributions/2026-10-14-collision-formal/IncomingCarry.lean",
        "CarryResponseMass": REPO / "proofs/contributions/2026-10-14-collision-mass/CarryResponseMass.lean",
    }
    paths.update({name: HERE / (name + ".lean") for name in NEW_MODULES + ["All"]})
    return paths


def source_plan(paths: dict[str, Path]):
    blobs, imports, theorem_names = {}, {}, []
    for name, path in paths.items():
        blob = path.read_bytes()
        code = code_only(blob.decode())
        blobs[name] = blob
        direct = [token for line in re.findall(r"^\s*import\s+([^\n]+)", code, re.M)
                  for token in line.split()]
        require(len(direct) == len(set(direct)), f"Duplicate import in {name}")
        require(set(direct) <= set(paths) | {"Std", "Init"}, f"Unapproved import in {name}: {direct}")
        imports[name] = [dependency for dependency in direct if dependency in paths]
        if name == "LychrelDigitSums":
            require(sha_bytes(blob) == BASE_SHA256, "Pinned LychrelDigitSums source changed")
        if name in NEW_MODULES + ["All"]:
            # Only comments are excluded from the forbidden-token check;
            # interpolated strings can contain executable Lean expressions.
            token_source = code_only(blob.decode(), blank_strings=False)
            forbidden = re.findall(r"\b(?:sorry|admit|axiom|native_decide|sorryAx)\b", token_source)
            require(not forbidden, f"Disallowed tokens in {name}: {forbidden}")
            declared = re.findall(r"\b(?:(private)\s+)?(?:theorem|lemma)\s+([\w']+)", code)
            # Private helpers receive compiler-generated names. Their axioms
            # are covered transitively by each exported theorem using them.
            declarations = [identifier for visibility, identifier in declared if not visibility]
            namespaces = re.findall(r"^\s*namespace\s+(\S+)\s*$", code, re.M)
            if declarations:
                require(namespaces == [f"Agent107.{name}"],
                        f"Expected one namespace Agent107.{name}; found {namespaces}")
            if name in NEW_MODULES:
                require(bool(declarations), f"No theorem declarations found in {name}")
            theorem_names.extend(f"Agent107.{name}.{declaration}" for declaration in declarations)
    require(set(imports["All"]) == set(NEW_MODULES), "All.lean must directly import all seven contribution modules")
    require(len(theorem_names) == len(set(theorem_names)), "Duplicate theorem name")
    order, visiting = [], set()

    def visit(name):
        if name in order:
            return
        require(name not in visiting, f"Cyclic project import: {name}")
        visiting.add(name)
        for dependency in imports[name]:
            visit(dependency)
        visiting.remove(name)
        order.append(name)

    visit("All")
    require(set(order) == set(paths), "All.lean import closure does not cover every required source")
    return blobs, imports, order, theorem_names


def checked_output(command, build, environment) -> str:
    result = subprocess.run(command, cwd=build, env=environment, text=True, capture_output=True)
    require(result.returncode == 0,
            f"Compiler probe failed ({result.returncode}): {command}\n{result.stdout}{result.stderr}")
    return result.stdout.strip()


def compiler_identity(lean: Path, build: Path, environment: dict) -> dict:
    version = checked_output([str(lean), "--version"], build, environment)
    require("version 4.19.0," in version, f"Expected Lean 4.19.0: {version}")
    prefix = Path(checked_output([str(lean), "--print-prefix"], build, environment)).resolve(strict=True)
    probe = build / "CompilerProbe.lean"
    probe.write_text(PROBE)
    output = checked_output([str(lean), "--run", str(probe)], build, environment)
    records = dict(line.split("=", 1) for line in output.splitlines() if line.startswith("P196_"))
    require(set(records) == {"P196_NATIVE", "P196_PRELOAD"}, f"Incomplete compiler probe: {output}")
    native = Path(records["P196_NATIVE"]).resolve(strict=True)
    preloads = {}
    for library in re.split(r"[:\s]+", records["P196_PRELOAD"]):
        if library:
            path = Path(library)
            if not path.is_absolute():
                path = build / path
            path = path.resolve(strict=True)
            preloads[str(path)] = file_hash(path)
    runtime = {}
    for relative in ["lib/lean/libleanshared.so", "lib/lean/libleanshared_1.so", "lib/lean/Std.olean"]:
        path = prefix / relative
        if path.is_file():
            runtime[relative] = file_hash(path)
    return {
        "version": version, "invoked_executable": str(lean), "invoked_executable_sha256": file_hash(lean),
        "native_executable": str(native), "native_executable_sha256": file_hash(native),
        "prefix": str(prefix), "runtime_sha256": runtime, "preloaded_library_sha256": preloads,
        "probe_source_sha256": sha_bytes(PROBE.encode()), "probe_output": output, "flags": FLAGS,
    }


def dependency_fingerprints(build: Path, dependencies: list[str]) -> dict:
    return {name: {"source_sha256": file_hash(build / (name + ".lean")),
                   "olean_sha256": file_hash(build / (name + ".olean"))} for name in dependencies}


def parse_axioms(output: str, expected: list[str]) -> dict:
    audited = {}
    pattern = r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)"
    for match in re.finditer(pattern, output, re.S):
        name = match.group(1)
        require(name not in audited, f"Duplicate axiom record: {name}")
        axioms = sorted({item.strip() for item in (match.group(2) or "").split(",") if item.strip()})
        require(set(axioms) <= ALLOWED_AXIOMS, f"Unapproved transitive axioms for {name}: {axioms}")
        audited[name] = axioms
    require(set(audited) == set(expected),
            f"Incomplete axiom audit; missing={sorted(set(expected) - set(audited))}; extra={sorted(set(audited) - set(expected))}")
    return audited


def run(args) -> int:
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output / "verification.json").unlink(missing_ok=True)
    log_path = output / "compile.log"
    log_path.write_text("START: fresh isolated Agent107 verification\n")
    build = args.build_dir.resolve() if args.build_dir else Path(tempfile.mkdtemp(prefix="p196-agent107-fresh-"))
    if build.exists() and any(build.iterdir()):
        log_path.write_text("FAIL: Fresh builds require an empty --build-dir\n")
        raise CheckFailure("Fresh builds require an empty --build-dir")
    build.mkdir(parents=True, exist_ok=True)
    (build / "logs").mkdir()
    manifest_path = build / "manifest.json"
    manifest = {"schema": SCHEMA, "status": "RUNNING", "build_dir": str(build), "modules": {}}
    atomic_json(manifest_path, manifest)
    environment = dict(os.environ, LEAN_PATH=str(build))
    environment.pop("LEAN_SRC_PATH", None)
    environment.pop("LEAN_SYSROOT", None)
    checker_hash = file_hash(Path(__file__))
    try:
        with log_path.open("w") as combined:
            executable = shutil.which(args.lean)
            require(executable is not None, f"Lean executable unavailable: {args.lean}")
            lean = Path(executable).resolve(strict=True)
            identity = compiler_identity(lean, build, environment)
            identity_hash = sha_bytes(json.dumps(identity, sort_keys=True).encode())
            manifest["compiler_identity"] = identity
            manifest["compiler_identity_sha256"] = identity_hash
            manifest["checker_sha256"] = checker_hash
            combined.write(json.dumps(identity, sort_keys=True) + "\n")
            combined.flush()
            paths = source_paths()
            blobs, imports, order, names = source_plan(paths)
            audit_source = "import All\nset_option maxRecDepth 100000\n" + "\n".join(
                "#print axioms " + name for name in names) + "\n"
            blobs["AllAxioms"] = audit_source.encode()
            imports["AllAxioms"] = ["All"]
            order.append("AllAxioms")
            manifest["theorem_names"] = names
            manifest["source_paths"] = {name: str(path.relative_to(REPO)) for name, path in paths.items()}
            manifest["build_order"] = order
            for name, blob in blobs.items():
                (build / (name + ".lean")).write_bytes(blob)
            atomic_json(manifest_path, manifest)
            for name in order:
                before = dependency_fingerprints(build, imports[name])
                command = [str(lean), *FLAGS, "-o", name + ".olean", name + ".lean"]
                print(f"COMPILING {name}", flush=True)
                started = time.monotonic()
                module_log = build / "logs" / (name + ".log")
                with module_log.open("wb") as log:
                    result = subprocess.run(command, cwd=build, env=environment, stdout=log, stderr=subprocess.STDOUT)
                text = module_log.read_text()
                after = dependency_fingerprints(build, imports[name])
                unchanged = (build / (name + ".lean")).read_bytes() == blobs[name]
                if name in paths:
                    unchanged = unchanged and paths[name].read_bytes() == blobs[name]
                accepted = (result.returncode == 0 and unchanged and before == after
                            and "declaration uses 'sorry'" not in text and (build / (name + ".olean")).is_file())
                record = {
                    "module": name, "status": "PASS" if accepted else "FAIL", "exit_code": result.returncode,
                    "seconds": round(time.monotonic() - started, 3), "command": command,
                    "source_sha256": sha_bytes(blobs[name]), "source_unchanged": unchanged,
                    "compiler_identity_sha256": identity_hash, "dependency_fingerprints": before,
                    "dependencies_unchanged": before == after, "log_sha256": file_hash(module_log),
                }
                if (build / (name + ".olean")).is_file():
                    record["olean_sha256"] = file_hash(build / (name + ".olean"))
                manifest["modules"][name] = record
                atomic_json(manifest_path, manifest)
                combined.write("\n" + json.dumps(record, sort_keys=True) + "\n" + text)
                combined.flush()
                require(accepted, f"Compilation or provenance check failed: {name}; see {module_log}")
                print(f"PASS {name} ({record['seconds']}s)", flush=True)
            audited = parse_axioms((build / "logs/AllAxioms.log").read_text(), names)
            for name in order:
                record = manifest["modules"][name]
                require(file_hash(build / (name + ".lean")) == record["source_sha256"], f"Source changed: {name}")
                require(file_hash(build / (name + ".olean")) == record["olean_sha256"], f"Object changed: {name}")
                require(file_hash(build / "logs" / (name + ".log")) == record["log_sha256"], f"Log changed: {name}")
                require(dependency_fingerprints(build, imports[name]) == record["dependency_fingerprints"],
                        f"Dependency changed: {name}")
                if name in paths:
                    require(paths[name].read_bytes() == blobs[name], f"Repository source changed: {name}")
            require(file_hash(Path(__file__)) == checker_hash, "Checker changed during verification")
            require(compiler_identity(lean, build, environment) == identity, "Compiler identity changed during verification")
            manifest.update(status="PASS", theorem_axioms=audited)
            atomic_json(manifest_path, manifest)
            report = {
                "result": "PASS", "schema": SCHEMA, "compiler_identity": identity,
                "checker_sha256": checker_hash, "fresh_dependency_rebuild": True,
                "isolated_project_import_path": True, "imported_development_objects": False,
                "all_sources_objects_logs_dependencies_revalidated": True,
                "build_dir": str(build), "manifest_sha256": file_hash(manifest_path),
                "source_sha256": {str(path.relative_to(REPO)): sha_bytes(blobs[name]) for name, path in paths.items()},
                "modules": [manifest["modules"][name] for name in order],
                "theorem_count": len(audited), "theorem_axioms": audited,
                "axiom_union": sorted({axiom for axioms in audited.values() for axiom in axioms}),
                "all_axioms_source_sha256": sha_bytes(blobs["AllAxioms"]),
                "scope": "Exact finite partition seam and carry response identities; no invariant orbit family, P196, or Lychrel existence claim.",
            }
            combined.write(f"\nPASS: {len(audited)} new theorems transitively audited after fresh rebuild.\n")
            combined.flush()
        report["compile_log_sha256"] = file_hash(log_path)
        atomic_json(output / "verification.json", report)
        print(f"PASS: {len(audited)} theorems; report {output / 'verification.json'}", flush=True)
        return 0
    except Exception as error:
        manifest.update(status="FAIL", error=str(error))
        atomic_json(manifest_path, manifest)
        with log_path.open("a") as log:
            log.write("\nFAIL: " + str(error) + "\n")
        print(f"FAIL: {error}\nBuild evidence retained at {build}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lean", nargs="?", help="Lean 4.19.0 executable or wrapper")
    parser.add_argument("--lean", dest="lean_option", help="Equivalent named Lean executable option")
    parser.add_argument("--build-dir", type=Path, help="Empty build directory to retain for review")
    parser.add_argument("--output-dir", type=Path, default=HERE,
                        help="Report/log directory (default: this contribution directory)")
    args = parser.parse_args()
    require(not (args.lean and args.lean_option), "Specify Lean only once")
    args.lean = args.lean_option or args.lean
    require(bool(args.lean), "A Lean 4.19.0 executable or wrapper is required")
    return run(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (CheckFailure, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
