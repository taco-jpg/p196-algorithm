#!/usr/bin/env python3
"""Fresh Lean 4.19.0 build and compiled-environment axiom audit.

By default, check every top-level .lean file next to this script. Recursively
resolve imports from this directory, proofs/research, and explicit --source-root
directories; runtime imports must exist in the selected Lean installation.
Both --build-dir and --output-dir must be absent or empty. No existing project
.olean files are reused. The audit includes private/generated theorems in the
entire local import closure, not merely names extracted from source text.
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
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
BASE_SHA256 = "f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c"
NATIVE_SHA256 = "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023"
RUNTIME_SHA256 = {
    "lib/lean/libleanshared.so": "2ab605c74c78f9ba4431a7b5305a4b28a9071d8a826f223eb14fe5530f78e14d",
    "lib/lean/libleanshared_1.so": "44bc5837306f8e24a5db0db56d56ca3114415bd65e3b107426d3c93e21d20098",
    "lib/lean/Std.olean": "7d3771da25b893da62564bf8198487ff28f01af5cbd410be88d493a4921b2bb1",
}
READLINK_ADAPTER_SHA256 = "100718efe84a5c605d4752eadf9d9f6b14f38d5adbc82ce00407d378f4d9973d"
MODULE = re.compile(r"[A-Za-z_][\w]*(?:\.[A-Za-z_][\w]*)*")
FORBIDDEN = re.compile(r"\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b")
COMMAND_WORDS = set("import prelude namespace section end open export universe universes variable variables "
                    "theorem lemma def abbrev axiom opaque instance class structure inductive mutual example "
                    "set_option attribute macro syntax elab local scoped infix infixl infixr notation "
                    "initialize builtin_initialize deriving noncomputable unsafe private protected public".split())
PROBE = '''def main : IO Unit := do
  IO.println s!"P196_NATIVE={← IO.appPath}"
  IO.println s!"P196_PRELOAD={(← IO.getEnv "LD_PRELOAD").getD ""}"
'''


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def write_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def code_only(text: str, *, blank_strings: bool = True) -> str:
    """Mask nested comments and optionally strings, preserving line breaks."""
    out, i, depth, string = [], 0, 0, False
    while i < len(text):
        char, pair = text[i], text[i:i + 2]
        if depth:
            if pair in ("/-", "-/"):
                depth += 1 if pair == "/-" else -1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if char == "\n" else " ")
                i += 1
        elif string:
            if char == "\\" and i + 1 < len(text):
                out.extend("  " if blank_strings else text[i:i + 2])
                i += 2
            else:
                out.append(("\n" if char == "\n" else " ") if blank_strings else char)
                string = char != '"'
                i += 1
        elif pair == "/-":
            depth = 1
            out.extend("  ")
            i += 2
        elif pair == "--":
            end = text.find("\n", i)
            end = len(text) if end < 0 else end
            out.extend(" " * (end - i))
            i = end
        elif char == "'" and i + 2 < len(text) and text[i + 2] == "'":
            out.extend("   " if blank_strings else text[i:i + 3])
            i += 3
        elif char == "'" and text[i + 1:i + 2] == "\\":
            end = i + 1
            while end < len(text):
                if text[end] == "\\":
                    end += 2
                    continue
                if text[end] == "'":
                    break
                end += 1
            require(end < len(text), "Unterminated Lean character literal")
            out.extend(" " * (end + 1 - i) if blank_strings else text[i:end + 1])
            i = end + 1
        elif char == '"':
            string = True
            out.append(" " if blank_strings else char)
            i += 1
        else:
            out.append(char)
            i += 1
    require(not depth and not string, "Unterminated Lean comment or string")
    return "".join(out)


def imports(text: str) -> list[str]:
    # Lean's header allows line breaks within imports and multiple import
    # commands on one line. Only ordinary, unquoted module identifiers are
    # supported; unsupported header syntax fails closed during compilation.
    tokens = code_only(text).split()
    result, position = [], 0
    if tokens and tokens[0] == "prelude":
        position += 1
    while position < len(tokens) and tokens[position] == "import":
        position += 1
        start = position
        while position < len(tokens):
            name = tokens[position]
            if name in COMMAND_WORDS or MODULE.fullmatch(name) is None:
                break
            result.append(name)
            position += 1
        require(position > start, "Empty or unsupported Lean import declaration")
    return result


def relative_module(name: str, suffix: str) -> Path:
    require(MODULE.fullmatch(name) is not None, f"Invalid module name: {name}")
    return Path(*name.split(".")).with_suffix(suffix)


def fresh_directory(path: Path) -> None:
    require(not path.exists() or (path.is_dir() and not any(path.iterdir())),
            f"Directory must be absent or empty: {path}")
    path.mkdir(parents=True, exist_ok=True)


def source_plan(selected: list[str], roots: list[Path], prefix: Path):
    paths, blobs, dependencies, standard, order, visiting = {}, {}, {}, set(), [], set()

    def visit(name: str) -> None:
        if name in order or name in standard:
            return
        relative = relative_module(name, ".lean")
        matches = sorted({(root / relative).resolve() for root in roots if (root / relative).is_file()})
        if not matches:
            require((prefix / "lib/lean" / relative.with_suffix(".olean")).is_file(),
                    f"Unresolved import {name}; provide its source directory with --source-root")
            standard.add(name)
            return
        require(len(matches) == 1, f"Ambiguous module {name}: {matches}")
        require(name not in visiting, f"Cyclic import: {name}")
        visiting.add(name)
        path = matches[0]
        blob = path.read_bytes()
        text = blob.decode("utf-8")
        forbidden = FORBIDDEN.findall(code_only(text, blank_strings=False))
        require(not forbidden, f"Disallowed proof token in {path}: {forbidden}")
        if name == "Lychrel196Research":
            require(digest(blob) == BASE_SHA256, "Pinned Lychrel196Research source changed")
        paths[name], blobs[name] = path, blob
        direct = imports(text)
        for imported in direct:
            visit(imported)
        dependencies[name] = [item for item in direct if item in paths]
        visiting.remove(name)
        order.append(name)

    for name in selected:
        visit(name)
    require(set(selected) <= set(paths), "Selected modules must have local source files")
    return paths, blobs, dependencies, sorted(standard), order


def audit_source(modules: list[str]) -> str:
    return "\n".join("import " + name for name in modules) + '''
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := [''' + ", ".join(json.dumps(name) for name in modules) + ''']
  for mod in env.allImportedModuleNames do
    logInfo m!"AUDIT_IMPORT {mod}"
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo value =>
          if value.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else
            throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          logInfo m!"AUDIT_THEOREM {mod} {name}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | _ => pure ()
'''


def run(args) -> int:
    build = args.build_dir.resolve() if args.build_dir else Path(tempfile.mkdtemp(prefix="p196-agent111-"))
    output = args.output_dir.resolve()
    require(build != output and build not in output.parents and output not in build.parents,
            "Build and report directories must be separate, non-nested directories")
    fresh_directory(build)
    fresh_directory(output)
    (output / "logs").mkdir()
    report = {"status": "RUNNING", "schema": 1, "build_dir": str(build),
              "fresh_dependency_rebuild": True, "isolated_project_import_path": True,
              "flags": FLAGS, "allowed_axioms": sorted(ALLOWED_AXIOMS), "commands": [], "sources": {}}
    report_path = output / "verification.json"
    environment = dict(os.environ)
    for key in ("LEAN_PATH", "LEAN_SRC_PATH", "LEAN_SYSROOT"):
        environment.pop(key, None)
    environment["LEAN_PATH"] = str(build)
    checker_hash = sha(Path(__file__))

    def execute(label: str, command: list[str]) -> str:
        log = output / "logs" / Path(*label.split(".")).with_suffix(".log")
        log.parent.mkdir(parents=True, exist_ok=True)
        started = time.monotonic()
        print(f"RUN {label}", flush=True)
        with log.open("wb") as stream:
            result = subprocess.run(command, cwd=build, env=environment, stdout=stream, stderr=subprocess.STDOUT)
        text = log.read_text()
        report["commands"].append({"label": label, "command": command, "exit_code": result.returncode,
                                   "seconds": round(time.monotonic() - started, 3),
                                   "log": str(log.relative_to(output)), "log_sha256": sha(log)})
        write_json(report_path, report)
        require(result.returncode == 0, f"Command failed ({result.returncode}): {label}; see {log}")
        require("declaration uses 'sorry'" not in text, f"Unproved declaration in {label}")
        return text.strip()

    try:
        executable = shutil.which(args.lean)
        require(executable is not None, f"Lean executable unavailable: {args.lean}")
        lean = Path(executable).resolve(strict=True)
        version = execute("compiler-version", [str(lean), "--version"])
        require("version 4.19.0," in version and "commit 6caaee842e94," in version,
                f"Expected official Lean 4.19.0 commit 6caaee842e94: {version}")
        prefix = Path(execute("compiler-prefix", [str(lean), "--print-prefix"])).resolve(strict=True)
        (build / "CompilerProbe.lean").write_text(PROBE)
        probe_output = execute("compiler-probe", [str(lean), *FLAGS, "--run", "CompilerProbe.lean"])
        probe = dict(line.split("=", 1) for line in probe_output.splitlines() if line.startswith("P196_"))
        require(set(probe) == {"P196_NATIVE", "P196_PRELOAD"}, "Incomplete compiler identity probe")
        native = Path(probe["P196_NATIVE"]).resolve(strict=True)
        require(sha(native) == NATIVE_SHA256, "Native executable does not match the recorded official binary")
        fingerprint_paths = [lean, native]
        for name in re.split(r"[:\s]+", probe["P196_PRELOAD"]):
            if name:
                library = Path(name).resolve(strict=True)
                require(sha(library) == READLINK_ADAPTER_SHA256, f"Unrecognized preload library: {library}")
                fingerprint_paths.append(library)
        for name, expected in RUNTIME_SHA256.items():
            library = prefix / name
            require(sha(library) == expected, f"Official Lean runtime fingerprint mismatch: {library}")
            fingerprint_paths.append(library)
        fingerprints = {str(path): sha(path) for path in fingerprint_paths}
        report["compiler"] = {"version": version, "invoked_executable": str(lean), "native_executable": str(native),
                              "prefix": str(prefix), "fingerprints": fingerprints,
                              "probe_source_sha256": digest(PROBE.encode()), "probe_output": probe_output}
        selected = args.module or sorted(path.stem for path in HERE.glob("*.lean"))
        require(selected, "No contribution modules found; use --module to select a module")
        roots = [HERE, REPO / "proofs/research", *[path.resolve() for path in args.source_root]]
        paths, blobs, dependencies, standard, order = source_plan(selected, roots, prefix)
        report.update(selected_modules=selected, build_order=order, runtime_imports=standard, checker_sha256=checker_hash)
        for name, blob in blobs.items():
            destination = build / relative_module(name, ".lean")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(blob)
            report["sources"][name] = {"original_path": str(paths[name]), "source_sha256": digest(blob),
                                       "snapshot": str(destination), "dependencies": dependencies[name]}
        write_json(report_path, report)
        for name in order:
            relative = relative_module(name, ".lean")
            dependencies_before = {dep: sha(build / relative_module(dep, ".olean")) for dep in dependencies[name]}
            execute(name, [str(lean), *FLAGS, "-o", str(relative.with_suffix(".olean")), str(relative)])
            obj = build / relative.with_suffix(".olean")
            require(obj.is_file(), f"Missing compiled object: {name}")
            require(all(sha(build / relative_module(dep, ".olean")) == value for dep, value in dependencies_before.items()),
                    f"Dependency changed while compiling {name}")
            report["sources"][name].update(olean_sha256=sha(obj), dependency_olean_sha256=dependencies_before)
            write_json(report_path, report)
        audit = audit_source(order)
        (build / "AllExportedAxioms.lean").write_text(audit)
        (output / "AllExportedAxioms.lean").write_text(audit)
        text = execute("AllExportedAxioms", [str(lean), *FLAGS, "AllExportedAxioms.lean"])
        require((build / "AllExportedAxioms.lean").read_text() == audit
                and (output / "AllExportedAxioms.lean").read_text() == audit,
                "Generated audit source changed during checking")
        inventory = re.findall(r"^AUDIT_THEOREM (\S+) (\S+)$", text, re.M)
        theorem_modules = {name: module for module, name in inventory}
        require(inventory and len(inventory) == len(theorem_modules), "Empty or duplicate compiled theorem inventory")
        report["unsafe_implementation_axioms"] = [
            {"module": module, "name": name}
            for module, name in re.findall(r"^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$", text, re.M)
        ]
        audited = {}
        for match in re.finditer(r"^'(.+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", text, re.M):
            name = match.group(1)
            require(name not in audited, f"Duplicate axiom record: {name}")
            axioms = sorted(item.strip() for item in (match.group(2) or "").split(",") if item.strip())
            require(set(axioms) <= ALLOWED_AXIOMS, f"Disallowed transitive axioms: {name}: {axioms}")
            audited[name] = axioms
        require(set(audited) == set(theorem_modules), "The compiled theorem inventory and axiom audit differ")
        report["theorems"] = {name: {"module": theorem_modules[name], "axioms": audited[name]} for name in sorted(audited)}
        report["theorem_count"] = len(audited)
        report["theorems_per_module"] = {name: sum(mod == name for mod in theorem_modules.values()) for name in order}
        report["axiom_union"] = sorted({axiom for values in audited.values() for axiom in values})
        imported = sorted(set(re.findall(r"^AUDIT_IMPORT (\S+)$", text, re.M)))
        require(set(order) <= set(imported), "The audit did not import every checked source module")
        report["imported_object_sha256"] = {}
        for name in imported:
            obj = build / relative_module(name, ".olean")
            if not obj.is_file():
                obj = prefix / "lib/lean" / relative_module(name, ".olean")
            require(obj.is_file(), f"Cannot locate imported object: {name}")
            report["imported_object_sha256"][name] = sha(obj)
        for name, record in report["sources"].items():
            require(sha(paths[name]) == record["source_sha256"] and sha(Path(record["snapshot"])) == record["source_sha256"],
                    f"Source changed during checking: {name}")
            require(sha(build / relative_module(name, ".olean")) == record["olean_sha256"], f"Object changed: {name}")
        for command in report["commands"]:
            require(sha(output / command["log"]) == command["log_sha256"], f"Log changed: {command['label']}")
        require(all(sha(Path(path)) == value for path, value in fingerprints.items()), "Compiler runtime changed")
        require(sha(Path(__file__)) == checker_hash, "Checker changed during execution")
        report.update(status="PASS", audit_source_sha256=digest(audit.encode()),
                      local_sources_objects_logs_and_compiler_revalidated=True)
        write_json(report_path, report)
        print(f"PASS: {len(order)} source modules, {len(audited)} theorems; {report_path}", flush=True)
        return 0
    except Exception as error:
        report.update(status="FAIL", error=str(error))
        write_json(report_path, report)
        print(f"FAIL: {error}; evidence retained at {output}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lean", help="Official Lean 4.19.0 executable or transparent host adapter")
    parser.add_argument("--build-dir", type=Path, help="Absent or empty build directory")
    parser.add_argument("--output-dir", type=Path, default=HERE / "verification/latest", help="Absent or empty report directory")
    parser.add_argument("--module", action="append", default=[], help="Select a root module (repeatable)")
    parser.add_argument("--source-root", type=Path, action="append", default=[], help="Additional import source root (repeatable)")
    return run(parser.parse_args())


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
