#!/usr/bin/env python3
"""Rebuild the pinned 17-module window-weight proof and audit its module origins.

Python 3.10+ and its standard library suffice.  See the adjacent REPRODUCE.md.
The checker never downloads, edits a proof, reuses a project olean, or runs Git
mutations.  A full run requires an explicit Lean binary and mathlib checkout.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import time


EXPECTED_MODULES = (
    "LychrelDigitSums", "Trace", "WholeWord", "Safety", "Indexing",
    "FiniteWords", "FamilyStates", "Agent108WindowDefs",
    "Agent108WindowProducts", "Agent108WindowEndpoints", "Agent108WindowWeights",
    "Agent108WindowFamilyProducts", "Agent108WindowEndpointWeights",
    "Agent108WindowObstruction", "Agent108WindowEmbedding",
    "Agent108WindowFamilyRatio", "Agent108WindowIncoming",
)
ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
ROOT_MODULE = "Agent108WindowIncoming"
LEAN_FLAGS = ("--trust=0", "-j1", "-DElab.async=false")
AUDIT_MODULE = "WindowPackageAxioms"


class CheckFailure(Exception):
    """An input, compilation, or audit requirement was not met."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def repo_file(root: Path, relative: str) -> Path:
    rel = PurePosixPath(relative)
    require(not rel.is_absolute() and ".." not in rel.parts,
            f"Source path is not repository-relative: {relative}")
    result = (root / Path(*rel.parts)).resolve()
    require(result.is_relative_to(root), f"Source path escapes repository: {relative}")
    require(result.is_file(), f"Missing pinned source: {relative}")
    return result


def mask_lean_comments_and_strings(text: str) -> str:
    """Keep line positions while masking nested comments and string contents.

    This supports the pinned sources, not arbitrary Lean parsing.  In particular,
    declaration-origin enumeration below is independent of this source inventory.
    """
    out = list(text)
    i, depth = 0, 0
    in_string = False
    while i < len(text):
        if depth:
            if text.startswith("/-", i):
                out[i:i + 2] = [" ", " "]
                depth += 1
                i += 2
            elif text.startswith("-/", i):
                out[i:i + 2] = [" ", " "]
                depth -= 1
                i += 2
            else:
                if text[i] != "\n":
                    out[i] = " "
                i += 1
        elif in_string:
            if text[i] == "\\":
                out[i] = " "
                if i + 1 < len(text) and text[i + 1] != "\n":
                    out[i + 1] = " "
                i += 2
            else:
                if text[i] == '"':
                    in_string = False
                if text[i] != "\n":
                    out[i] = " "
                i += 1
        elif text.startswith("/-", i):
            out[i:i + 2] = [" ", " "]
            depth = 1
            i += 2
        elif text.startswith("--", i):
            end = text.find("\n", i)
            if end < 0:
                end = len(text)
            out[i:end] = [" "] * (end - i)
            i = end
        elif text[i] == '"':
            out[i] = " "
            in_string = True
            i += 1
        else:
            i += 1
    require(depth == 0 and not in_string, "Unterminated source comment or string")
    return "".join(out)


DECLARATION = re.compile(
    r"^[ \t]*(?:@\[[^\]\n]*\][ \t]*)*"
    r"(?P<modifiers>(?:(?:private|protected|noncomputable|unsafe|partial)[ \t]+)*)"
    r"(?P<kind>def|theorem|lemma|abbrev|axiom|opaque|instance|inductive|structure|class)"
    r"[ \t]+(?P<name>[^\s({:]+)"
)


def source_declarations(module: str, text: str) -> list[dict]:
    """Inventory named declarations in these fixed sources, preserving scopes.

    Counts and exact hashes are pinned.  Namespace/section handling distinguishes
    private declarations with the same short name in different namespaces.
    """
    rows = []
    scopes: list[tuple[str, str]] = []
    for line_number, line in enumerate(mask_lean_comments_and_strings(text).splitlines(), 1):
        opening = re.fullmatch(r"\s*(namespace|(?:noncomputable\s+)?section)(?:\s+(\S+))?\s*", line)
        if opening:
            command, name = opening.groups()
            require(command != "namespace" or bool(name), f"Unnamed namespace in {module}:{line_number}")
            scopes.append(("namespace" if command == "namespace" else "section", name or ""))
            continue
        closing = re.fullmatch(r"\s*end(?:\s+(\S+))?\s*", line)
        if closing:
            require(bool(scopes), f"Unmatched end in {module}:{line_number}")
            _, name = scopes.pop()
            require(not closing[1] or closing[1] == name,
                    f"Scope name mismatch in {module}:{line_number}")
            continue
        declaration = DECLARATION.match(line)
        if declaration:
            modifiers = declaration["modifiers"].split()
            short = declaration["name"]
            namespace = ".".join(name for kind, name in scopes if kind == "namespace")
            full = ".".join(part for part in (namespace, short) if part)
            rows.append({"module": module, "source_line": line_number,
                         "kind": declaration["kind"], "short_name": short,
                         "source_name": full, "private": "private" in modifiers,
                         "modifiers": modifiers})
    require(not scopes, f"Unclosed source scope in {module}")
    return rows


def validate_source(row: dict, data: bytes) -> dict:
    name = row["module"]
    require(len(data) == row["size_bytes"], f"Source size mismatch: {name}")
    require(sha256(data) == row["sha256"], f"Source SHA256 mismatch: {name}")
    require(git_blob(data) == row["git_blob"], f"Source Git blob mismatch: {name}")
    text = data.decode("utf-8")
    clean = mask_lean_comments_and_strings(text)
    imports = re.findall(r"^\s*import[ \t]+(\S+)[ \t]*$", clean, re.MULTILINE)
    require(imports == row["imports"], f"Pinned import list mismatch: {name}")
    declarations = source_declarations(name, text)
    require(len(declarations) == row["explicit_declaration_count"],
            f"Explicit declaration inventory changed in {name}: {len(declarations)}")
    return {**row, "observed_imports": imports, "source_declarations": declarations}


def load_pins(path: Path) -> dict:
    pins = json.loads(path.read_text(encoding="utf-8"))
    require(pins["schema_version"] == 1, "Unsupported pin schema")
    require(pins["root_module"] == ROOT_MODULE, "Unexpected root module")
    require(set(pins["allowed_axioms"]) == ALLOWED_AXIOMS, "Axiom allowlist changed")
    require(pins["lean"]["version"] == "4.19.0", "Unexpected Lean version pin")
    require(pins["lean"]["commit_prefix"] == "6caaee842e94", "Unexpected Lean commit pin")
    rows = pins["sources"]
    names = [row["module"] for row in rows]
    require(len(names) == len(set(names)) == 17, "Expected 17 distinct pinned modules")
    require(set(names) == set(EXPECTED_MODULES), "Unexpected pinned module set")
    require(pins["build_order"] == list(EXPECTED_MODULES), "Unexpected build order")
    require(sum(row["role"] == "original_dependency" for row in rows) == 7,
            "Expected seven original dependencies")
    require(sum(row["role"] == "new_module" for row in rows) == 10,
            "Expected ten new modules")
    by_name = {row["module"]: row for row in rows}
    for row in rows:
        require(re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) is not None,
                f"Invalid SHA256 pin: {row['module']}")
        require(re.fullmatch(r"[0-9a-f]{40}", row["git_blob"]) is not None,
                f"Invalid Git blob pin: {row['module']}")
    done = set()
    for name in pins["build_order"]:
        for dependency in by_name[name]["imports"]:
            if dependency in by_name:
                require(dependency in done, f"Build order violates import: {name} -> {dependency}")
            else:
                require(dependency in {"Std", "Lean", "Init"} or
                        dependency.startswith(("Mathlib.", "Std.", "Lean.", "Init.")),
                        f"Unpinned project import: {name} -> {dependency}")
        done.add(name)
    reachable = set()

    def visit(name: str) -> None:
        if name in reachable:
            return
        reachable.add(name)
        for dependency in by_name[name]["imports"]:
            if dependency in by_name:
                visit(dependency)

    visit(ROOT_MODULE)
    require(reachable == set(EXPECTED_MODULES), "Root import closure does not contain exactly the 17 modules")
    return pins


def verify_sources(pins: dict, repo: Path) -> tuple[dict[str, bytes], list[dict]]:
    data_by_module, records = {}, []
    for row in pins["sources"]:
        data = repo_file(repo, row["repo_path"]).read_bytes()
        records.append(validate_source(row, data))
        data_by_module[row["module"]] = data
    return data_by_module, records


def verify_mathlib_files(root: Path, pin: dict) -> dict:
    manifest_data = (root / "lake-manifest.json").read_bytes()
    toolchain_data = (root / "lean-toolchain").read_bytes()
    require(sha256(manifest_data) == pin["lake_manifest_sha256"], "Mathlib manifest SHA256 mismatch")
    require(sha256(toolchain_data) == pin["lean_toolchain_sha256"], "Mathlib toolchain SHA256 mismatch")
    require(toolchain_data.decode().strip() == "leanprover/lean4:v4.19.0", "Mathlib toolchain mismatch")
    manifest = json.loads(manifest_data)
    require(manifest["name"] == "mathlib" and manifest["packagesDir"] == ".lake/packages",
            "Unexpected Mathlib package layout")
    packages = {package["name"]: package for package in manifest["packages"]}
    require(len(packages) == len(manifest["packages"]) == 8, "Expected eight manifest packages")
    require(set(packages) == {package["name"] for package in pin["dependencies"]},
            "Mathlib dependency package set mismatch")
    for dependency in pin["dependencies"]:
        actual = packages[dependency["name"]]
        require(actual["type"] == "git" and actual["subDir"] is None,
                f"Unsupported package layout: {dependency['name']}")
        require(actual["rev"] == dependency["rev"] and actual["url"] == dependency["url"],
                f"Mathlib dependency pin mismatch: {dependency['name']}")
    return manifest


def make_audit_source(modules: list[str]) -> str:
    module_list = ",\n    ".join(json.dumps(module) for module in modules)
    return '''import Agent108WindowIncoming
import Lean

open Lean Elab Command

private def declarationKind : ConstantInfo → String
  | .axiomInfo _ => "axiom"
  | .defnInfo _ => "definition"
  | .thmInfo _ => "theorem"
  | .opaqueInfo _ => "opaque"
  | .quotInfo _ => "quotient"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"

elab "audit_window_package" : command => do
  let modules : List String := [
    ''' + module_list + ''']
  let env ← getEnv
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let modName := env.header.moduleNames[idx.toNat]!
      if modules.contains modName.toString then
        logInfo s!"METADATA|{modName.toString}|{name.toString}|{declarationKind info}|{info.isUnsafe}|{info.isPartial}"
        if !info.isUnsafe && !info.isPartial then
          logInfo s!"AUDIT_BEGIN|{name.toString}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
          logInfo s!"AUDIT_END|{name.toString}"

audit_window_package
'''


def parse_audit(output: str, modules: set[str], declarations: list[dict]) -> dict:
    metadata = []
    for line in output.splitlines():
        if line.startswith("METADATA|"):
            fields = line.split("|")
            require(len(fields) == 6, f"Invalid audit metadata: {line}")
            _, module, name, kind, unsafe, partial = fields
            require(module in modules, f"Unrequested audit module: {module}")
            require(kind in {"axiom", "definition", "theorem", "opaque", "quotient",
                             "inductive", "constructor", "recursor"},
                    f"Unknown declaration kind: {kind}")
            require(unsafe in {"true", "false"} and partial in {"true", "false"},
                    f"Invalid audit flags: {line}")
            metadata.append({"module": module, "declaration": name, "kind": kind,
                             "unsafe": unsafe == "true", "partial": partial == "true"})
    names = [row["declaration"] for row in metadata]
    require(len(names) == len(set(names)), "Duplicate module-origin declarations")
    require({row["module"] for row in metadata} == modules,
            "Origin audit did not visit every pinned module")
    safe = [row for row in metadata if not row["unsafe"] and not row["partial"]]
    blocks = re.findall(r"^AUDIT_BEGIN\|([^\n]+)\n(.*?)^AUDIT_END\|([^\n]+)$",
                        output, re.MULTILINE | re.DOTALL)
    require(output.count("AUDIT_BEGIN|") == output.count("AUDIT_END|") == len(blocks),
            "Unbalanced or unparsed axiom audit markers")
    reports = {}
    for begin, body, end in blocks:
        require(begin == end and begin not in reports, f"Mismatched/duplicate audit block: {begin}")
        nonempty = re.findall(r"^'(.+)' depends on axioms: \[([^]]*)\]", body, re.MULTILINE)
        empty = re.findall(r"^'(.+)' does not depend on any axioms", body, re.MULTILINE)
        require(len(nonempty) + len(empty) == 1, f"Expected exactly one axiom report for {begin}")
        if nonempty:
            printed, axioms = nonempty[0]
            dependencies = [item.strip() for item in axioms.split(",") if item.strip()]
        else:
            printed, dependencies = empty[0], []
        require(printed == begin, f"Printed axiom declaration does not match its origin marker: {begin}")
        reports[begin] = {"printed_name": printed, "axioms": dependencies}
    require(set(reports) == {row["declaration"] for row in safe},
            "Safe/nonpartial origin set and axiom report set differ")
    safe_reports = [{**row, **reports[row["declaration"]]} for row in safe]
    correspondence = []
    for declaration in declarations:
        full = declaration["source_name"]
        matching = [row for row in safe if row["module"] == declaration["module"] and
                    (row["declaration"] == full or
                     declaration["private"] and row["declaration"].endswith("." + full))]
        require(len(matching) == 1,
                f"Expected one safe origin for {declaration['module']}:{declaration['source_line']} {full}")
        actual = matching[0]["declaration"]
        correspondence.append({**declaration, "declaration": actual, "axioms": reports[actual]["axioms"]})
    unexpected = [{"declaration": row["declaration"],
                   "unexpected_axioms": sorted(set(row["axioms"]) - ALLOWED_AXIOMS)}
                  for row in safe_reports if not set(row["axioms"]) <= ALLOWED_AXIOMS]
    counts = {}
    for module in sorted(modules):
        origins = [row for row in metadata if row["module"] == module]
        counts[module] = {
            "all_origins": len(origins),
            "safe_nonpartial": sum(not row["unsafe"] and not row["partial"] for row in origins),
            "unsafe": sum(row["unsafe"] for row in origins),
            "partial": sum(row["partial"] for row in origins),
            "unsafe_or_partial": sum(row["unsafe"] or row["partial"] for row in origins),
            "explicit_source_declarations": sum(row["module"] == module for row in correspondence),
        }
    return {"pass": not unexpected, "allowed_axioms": sorted(ALLOWED_AXIOMS),
            "module_counts": counts, "all_origin_count": len(metadata),
            "safe_nonpartial_count": len(safe), "explicit_source_count": len(correspondence),
            "origin_metadata": metadata, "safe_axiom_reports": safe_reports,
            "source_correspondence": correspondence,
            "unsafe_or_partial_origins": [row for row in metadata if row["unsafe"] or row["partial"]],
            "unexpected_axioms": unexpected}


class EvidenceRun:
    def __init__(self, root: Path, record: dict):
        root.mkdir(parents=True, exist_ok=False)
        self.root, self.record = root, record
        for name in ("sources", "build", "logs", "inputs"):
            (root / name).mkdir()
        self.record["commands"] = []
        self.save()

    def save(self) -> None:
        write_json(self.root / "verification.json", self.record)

    def command(self, label: str, arguments: list[str], cwd: Path,
                env: dict[str, str], timeout: int) -> str:
        number = len(self.record["commands"]) + 1
        prefix = f"{number:02d}-{label}"
        stdout_path = self.root / "logs" / f"{prefix}.stdout.log"
        stderr_path = self.root / "logs" / f"{prefix}.stderr.log"
        step = {"label": label, "argv": arguments, "cwd": str(cwd),
                "started_utc": utc_now(), "exit_code": None,
                "stdout_log": str(stdout_path.relative_to(self.root)),
                "stderr_log": str(stderr_path.relative_to(self.root))}
        self.record["commands"].append(step)
        self.save()
        print(f"[{number:02d}] {label}", flush=True)
        started = time.monotonic()
        try:
            with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
                result = subprocess.run(arguments, cwd=cwd, env=env, stdout=stdout,
                                        stderr=stderr, timeout=timeout, check=False)
            step["exit_code"] = result.returncode
        except subprocess.TimeoutExpired as error:
            step["timeout_seconds"] = timeout
            raise CheckFailure(f"Command timed out: {label}; logs retained") from error
        finally:
            step["seconds"] = time.monotonic() - started
            step["finished_utc"] = utc_now()
            self.save()
        require(step["exit_code"] == 0,
                f"Command failed ({step['exit_code']}): {label}; inspect {stderr_path} and {stdout_path}")
        return stdout_path.read_text(encoding="utf-8", errors="replace")


def git_snapshot(run: EvidenceRun, label: str, root: Path, expected: str,
                 env: dict[str, str], timeout: int) -> dict:
    head = run.command(label + "-head", ["git", "-C", str(root), "rev-parse", "HEAD"],
                       root, env, timeout).strip()
    require(head == expected, f"Git HEAD mismatch for {label}: {head}")
    tracked = run.command(label + "-tracked-status",
                          ["git", "-C", str(root), "status", "--porcelain=v1", "--untracked-files=no"],
                          root, env, timeout)
    require(not tracked.strip(), f"Tracked Mathlib/dependency changes in {label}")
    return {"root": str(root), "commit": head, "tracked_clean": True,
            "untracked_build_cache_not_source_audited": True}


def full_check(args: argparse.Namespace, pins: dict, repo: Path, pins_path: Path) -> int:
    require(args.lean is not None and args.mathlib_root is not None,
            "A full run requires --lean and --mathlib-root")
    lean = Path(args.lean).expanduser().resolve()
    mathlib = Path(args.mathlib_root).expanduser().resolve()
    require(lean.is_file() and os.access(lean, os.X_OK), "--lean must be an executable Lean binary")
    sysroot = lean.parent.parent
    require((sysroot / "lib/lean/Init.olean").is_file(),
            "Pass the real Lean 4.19.0 binary, not an elan shim or a wrapper")
    require(mathlib.is_dir(), "--mathlib-root must name the pinned Mathlib checkout")
    require(args.timeout_seconds > 0, "--timeout-seconds must be positive")
    if args.evidence:
        evidence = Path(args.evidence).expanduser().resolve()
    else:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        evidence = pins_path.parent / "reproduction" / f"{stamp}-{os.getpid()}"
    require(not evidence.exists(), "Evidence directory already exists; choose a new path")
    require(not repo.is_relative_to(evidence), "Evidence directory must not contain the repository")
    record = {"schema_version": 1, "status": "RUNNING", "pass": False,
              "started_utc": utc_now(), "repository_root": str(repo),
              "evidence_root": str(evidence), "root_module": ROOT_MODULE,
              "build_order": pins["build_order"], "lean_flags": list(LEAN_FLAGS),
              "project_olean_reuse": False, "mathlib_and_toolchain_oleans_reused": True,
              "axiom_audit_scope": "Every safe/nonpartial declaration originating in exactly the pinned 17 modules"}
    run = EvidenceRun(evidence, record)
    print(f"Evidence: {evidence}", flush=True)
    try:
        script = Path(__file__).resolve()
        for path in (script, pins_path, script.with_name("REPRODUCE.md")):
            require(path.is_file(), f"Missing package file: {path.name}")
            shutil.copyfile(path, evidence / "inputs" / path.name)
        record["package_sha256"] = {
            path.name: sha256(path.read_bytes()) for path in
            (script, pins_path, script.with_name("REPRODUCE.md"))}
        data_by_module, source_records = verify_sources(pins, repo)
        record["source_records"] = source_records
        for name, data in data_by_module.items():
            (evidence / "sources" / f"{name}.lean").write_bytes(data)
        record["fresh_build_initially_empty"] = not any((evidence / "build").iterdir())
        require(record["fresh_build_initially_empty"], "New build directory is not empty")
        verify_mathlib_files(mathlib, pins["mathlib"])
        for filename in ("lake-manifest.json", "lean-toolchain"):
            shutil.copyfile(mathlib / filename, evidence / "inputs" / ("mathlib-" + filename))
        package_roots = [mathlib / ".lake/packages" / row["name"]
                         for row in pins["mathlib"]["dependencies"]]
        mathlib_library = mathlib / ".lake/build/lib/lean"
        require(mathlib_library.is_dir(), f"Missing prepared Mathlib olean cache: {mathlib_library}")
        package_libraries = [root / ".lake/build/lib/lean" for root in package_roots]
        record["dependency_cache_directories"] = [
            {"package": row["name"], "library": str(library), "present": library.is_dir()}
            for row, library in zip(pins["mathlib"]["dependencies"], package_libraries)]
        # A selective official cache can omit an unused package such as Cli.
        # All eight source revisions are still checked below.  Lean must resolve
        # every actual import from the explicitly listed existing libraries.
        libraries = [mathlib_library] + [library for library in package_libraries if library.is_dir()]
        external_imports = sorted({dependency for row in pins["sources"] for dependency in row["imports"]
                                   if dependency not in EXPECTED_MODULES})
        record["direct_external_import_oleans"] = []
        for dependency in external_imports:
            relative = Path(*dependency.split(".")).with_suffix(".olean")
            matches = [library / relative for library in [sysroot / "lib/lean", *libraries]
                       if (library / relative).is_file()]
            require(bool(matches), f"Missing directly imported olean: {dependency}")
            record["direct_external_import_oleans"].append({"module": dependency, "path": str(matches[0])})
        env = dict(os.environ)
        env["LEAN_SYSROOT"] = str(sysroot)
        env["LEAN_PATH"] = os.pathsep.join(map(str, [evidence / "build", *libraries]))
        env.pop("LEAN_SRC_PATH", None)
        # Only these Lean-related environment values are logged; inherited secrets are not.
        record["lean_environment"] = {key: env[key] for key in ("LEAN_SYSROOT", "LEAN_PATH")}
        version = run.command("lean-version", [str(lean), "--version"],
                              evidence / "sources", env, args.timeout_seconds).strip()
        require(re.search(r"\bversion 4\.19\.0(?:,|\))", version) is not None,
                f"Lean version mismatch: {version}")
        require("commit " + pins["lean"]["commit_prefix"] in version,
                f"Lean commit mismatch: {version}")
        record["lean"] = {"binary": str(lean), "sha256": sha256(lean.read_bytes()),
                          "version_output": version, "sysroot": str(sysroot)}
        if (repo / ".git").exists():
            record["repository_head"] = run.command("repository-head",
                ["git", "-C", str(repo), "rev-parse", "HEAD"], repo, env, args.timeout_seconds).strip()
        else:
            record["repository_head"] = None
            record["repository_snapshot_disclosure"] = "No .git entry at --repo-root; source byte pins still checked"
        record["mathlib"] = git_snapshot(run, "mathlib", mathlib, pins["mathlib"]["commit"],
                                          env, args.timeout_seconds)
        record["mathlib"]["lake_manifest_sha256"] = pins["mathlib"]["lake_manifest_sha256"]
        record["mathlib"]["dependencies"] = []
        for dependency, root in zip(pins["mathlib"]["dependencies"], package_roots):
            observed = git_snapshot(run, dependency["name"], root, dependency["rev"],
                                    env, args.timeout_seconds)
            record["mathlib"]["dependencies"].append({**dependency, **observed})
        cache_inventory = []
        for library in libraries:
            for path in sorted(library.rglob("*.olean")):
                cache_inventory.append({"library": str(library), "path": str(path.relative_to(library)),
                                        "size_bytes": path.stat().st_size})
        write_json(evidence / "cache-inventory.json", cache_inventory)
        record["cache_disclosure"] = (
            "Pinned Mathlib and eight tracked-clean source checkouts are checked; existing olean caches "
            "and the Lean distribution are prerequisites, not rebuilt here. Cache inventory records "
            "paths and sizes, not a source-to-olean derivation. The 17 project modules are rebuilt.")
        run.save()
        sources, build = evidence / "sources", evidence / "build"
        compiled = []
        for name in pins["build_order"]:
            output = build / f"{name}.olean"
            run.command("compile-" + name,
                        [str(lean), *LEAN_FLAGS, "-o", str(output), f"{name}.lean"],
                        sources, env, args.timeout_seconds)
            require(output.is_file(), f"Lean returned success without an olean for {name}")
            compiled.append({"module": name, "sha256": sha256(output.read_bytes()),
                             "size_bytes": output.stat().st_size})
            record["compiled_oleans"] = compiled
            run.save()
        audit_source = make_audit_source(pins["build_order"])
        (sources / f"{AUDIT_MODULE}.lean").write_text(audit_source, encoding="utf-8")
        record["audit_source_sha256"] = sha256(audit_source.encode())
        audit_output = run.command("audit-module-origins",
            [str(lean), *LEAN_FLAGS, "-o", str(build / f"{AUDIT_MODULE}.olean"), f"{AUDIT_MODULE}.lean"],
            sources, env, args.timeout_seconds)
        declarations = [declaration for row in source_records for declaration in row["source_declarations"]]
        audit = parse_audit(audit_output, set(pins["build_order"]), declarations)
        write_json(evidence / "axiom-audit.json", audit)
        record["audit_summary"] = {key: audit[key] for key in
            ("pass", "all_origin_count", "safe_nonpartial_count", "explicit_source_count",
             "module_counts", "unexpected_axioms")}
        require(audit["pass"], "Unexpected logical axiom; see axiom-audit.json")
        for row in pins["sources"]:
            original = repo_file(repo, row["repo_path"]).read_bytes()
            copied = (sources / f"{row['module']}.lean").read_bytes()
            require(original == copied == data_by_module[row["module"]],
                    f"Pinned source changed during the run: {row['module']}")
        record["all_sources_unchanged_after"] = True
        verify_mathlib_files(mathlib, pins["mathlib"])
        record["mathlib_manifest_unchanged_after"] = True
        for path in (script, pins_path, script.with_name("REPRODUCE.md")):
            require(sha256(path.read_bytes()) == record["package_sha256"][path.name],
                    f"Package file changed during the run: {path.name}")
        record["package_files_unchanged_after"] = True
        record.update(status="PASS", **{"pass": True})
        print(json.dumps({"status": "PASS", "evidence": str(evidence),
                          **record["audit_summary"]}, indent=2), flush=True)
        return 0
    except Exception as error:
        record.update(status="FAIL", **{"pass": False, "error": f"{type(error).__name__}: {error}"})
        print(f"FAIL: {error}\nEvidence retained: {evidence}", file=sys.stderr, flush=True)
        return 1
    except KeyboardInterrupt:
        record.update(status="INTERRUPTED", **{"pass": False})
        print(f"Interrupted; evidence retained: {evidence}", file=sys.stderr, flush=True)
        return 130
    finally:
        record["finished_utc"] = utc_now()
        run.save()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path,
                        help="Repository root; defaults to four parents above this contribution directory")
    parser.add_argument("--pins", type=Path, default=Path(__file__).resolve().with_name("source-pins.json"))
    parser.add_argument("--lean", type=Path, help="Real Lean 4.19.0 binary (not a wrapper or elan shim)")
    parser.add_argument("--mathlib-root", type=Path, help="Pinned Mathlib checkout with its prepared olean caches")
    parser.add_argument("--evidence", type=Path, help="New, nonexistent evidence directory")
    parser.add_argument("--timeout-seconds", type=int, default=3600, help="Per-command timeout (default: 3600)")
    parser.add_argument("--check-inputs", action="store_true",
                        help="Read-only Python pin/source check; no Lean/Git command, build, audit, or output files")
    args = parser.parse_args(argv)
    try:
        pins_path = args.pins.expanduser().resolve()
        pins = load_pins(pins_path)
        repo = (args.repo_root or Path(__file__).resolve().parents[4]).expanduser().resolve()
        require(repo.is_dir(), "Repository root does not exist")
        if args.check_inputs:
            _, records = verify_sources(pins, repo)
            if args.mathlib_root:
                verify_mathlib_files(args.mathlib_root.expanduser().resolve(), pins["mathlib"])
            print(json.dumps({"status": "INPUTS_VERIFIED_ONLY", "proof_compilation_performed": False,
                              "axiom_audit_performed": False, "source_count": len(records),
                              "explicit_declarations_by_module": {
                                  row["module"]: len(row["source_declarations"]) for row in records},
                              "pins_sha256": sha256(pins_path.read_bytes())}, indent=2))
            return 0
        return full_check(args, pins, repo, pins_path)
    except (CheckFailure, OSError, ValueError, KeyError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
