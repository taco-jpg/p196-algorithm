#!/usr/bin/env python3
"""Rebuild the pinned Agent #3 three-layer proof and audit every declaration.

Uses Python's standard library and an installed Lean 4.19.0. No downloads,
Git writes, package resolution, or pre-existing contribution oleans are used.
The build directory must be new or empty; previous evidence is never deleted.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
AUDIT_NAMESPACES = {"P196.Agent3.OverflowHorizon", "P196.Agent3.TwoHistory", "P196.Agent3.ThreeLayer"}
FORBIDDEN_IDENTIFIERS = {
    "sorry", "admit", "sorryAx", "axiom", "constant", "unsafe", "partial",
    "opaque", "native_decide", "native_cast", "vm_decide", "implemented_by",
    "extern", "elab", "macro", "syntax", "run_tac", "run_cmd",
    "Lean.ofReduceBool", "Lean.trustCompiler", "debug.skipKernelTC",
}


class VerificationError(Exception):
    """A checked condition failed; retain the complete evidence directory."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_digest(path: Path) -> str:
    return digest(path.read_bytes())


def write_json(path: Path, value: object) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(path)


def code_only(text: str) -> str:
    """Blank strings and nested Lean comments while preserving line numbers."""
    result = list(text)
    index = 0
    depth = 0
    quoted = False
    while index < len(text):
        if depth:
            if text.startswith("/-", index):
                result[index:index + 2] = "  "
                depth += 1
                index += 2
            elif text.startswith("-/", index):
                result[index:index + 2] = "  "
                depth -= 1
                index += 2
            else:
                if text[index] != "\n":
                    result[index] = " "
                index += 1
        elif quoted:
            if text[index] == "\\":
                result[index] = " "
                index += 1
                if index < len(text):
                    if text[index] != "\n":
                        result[index] = " "
                    index += 1
            else:
                quoted = text[index] != '"'
                if text[index] != "\n":
                    result[index] = " "
                index += 1
        elif text.startswith("/-", index):
            result[index:index + 2] = "  "
            depth = 1
            index += 2
        elif text.startswith("--", index):
            end = text.find("\n", index)
            end = len(text) if end == -1 else end
            result[index:end] = " " * (end - index)
            index = end
        elif text[index] == '"':
            result[index] = " "
            quoted = True
            index += 1
        else:
            index += 1
    if depth or quoted:
        raise VerificationError("Unterminated Lean comment or string")
    return "".join(result)


def source_scan(code: str) -> dict:
    violations = []
    for token in re.finditer(r"[A-Za-z_][A-Za-z_0-9'.]*", code):
        if any(token.group() == forbidden or token.group().endswith("." + forbidden)
               for forbidden in FORBIDDEN_IDENTIFIERS):
            violations.append({"token": token.group(), "line": code.count("\n", 0, token.start()) + 1})
    for command in re.finditer(r"(?m)^\s*#\s*(eval|exec|run)\b", code):
        violations.append({"token": command.group().strip(), "line": code.count("\n", 0, command.start()) + 1})
    if violations:
        raise VerificationError("Forbidden proof-source shortcut(s): " + json.dumps(violations))
    return {"result": "PASS", "forbidden_identifiers": sorted(FORBIDDEN_IDENTIFIERS)}


def imports_of(code: str) -> list[str]:
    return [name for line in re.findall(r"(?m)^\s*import\s+([^\n]+)", code) for name in line.split()]


def source_declarations(code: str) -> list[dict]:
    """Record this contribution's explicit declarations, including privates.

    The complete audit is independently enumerated from Lean's compiled
    environment; this source inventory checks coverage of all named exports.
    """
    scopes = []
    declarations = []
    declaration = re.compile(
        r"^\s*((?:(?:private|protected|noncomputable)\s+)*)"
        r"(def|theorem|lemma|abbrev|structure|inductive|class)\s+([A-Za-z_][A-Za-z_0-9'.]*)\b"
    )
    for line_number, line in enumerate(code.splitlines(), 1):
        namespace = re.match(r"^\s*namespace\s+([A-Za-z_][A-Za-z_0-9'.]*)\s*$", line)
        section = re.match(r"^\s*section(?:\s+[A-Za-z_][A-Za-z_0-9']*)?\s*$", line)
        end = re.match(r"^\s*end(?:\s+[A-Za-z_][A-Za-z_0-9'.]*)?\s*$", line)
        if namespace:
            scopes.append(("namespace", namespace.group(1)))
        elif section:
            scopes.append(("section", ""))
        elif end:
            if not scopes:
                raise VerificationError(f"Unmatched end at source line {line_number}")
            scopes.pop()
        match = declaration.match(line)
        if match:
            names = [name for kind, name in scopes if kind == "namespace"]
            full_name = ".".join(names + [match.group(3)])
            if not any(full_name.startswith(prefix + ".") for prefix in AUDIT_NAMESPACES):
                raise VerificationError(f"New declaration outside audited namespace: {full_name}")
            declarations.append({
                "name": full_name, "kind": match.group(2), "line": line_number,
                "private": "private" in match.group(1).split(),
            })
    if scopes:
        raise VerificationError("Unclosed source namespace or section")
    return declarations


def parse_axiom_records(output: str) -> dict[str, list[str]]:
    records = {}
    expression = r"'([^\n]+?)' (?:does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])"
    for match in re.finditer(expression, output):
        name = match.group(1)
        axioms = sorted({part.strip() for part in (match.group(2) or "").split(",") if part.strip()})
        if name in records:
            raise VerificationError(f"Duplicate axiom-audit result: {name}")
        unexpected = set(axioms) - ALLOWED_AXIOMS
        if unexpected:
            raise VerificationError(f"Unexpected axioms for {name}: {sorted(unexpected)}")
        records[name] = axioms
    if re.search(r"\bsorryAx\b|\bLean\.ofReduceBool\b|declaration uses.*sorry", output):
        raise VerificationError("Compiler output contains an untrusted proof shortcut")
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path, help="Lean 4.19.0 executable")
    parser.add_argument("--repo", type=Path, default=HERE.parents[4], help="Repository root containing proofs/")
    parser.add_argument("--build-dir", required=True, type=Path, help="New or empty directory; never automatically erased")
    parser.add_argument("--timeout", type=int, default=600, help="Maximum seconds per compiler command")
    args = parser.parse_args()
    build = args.build_dir.resolve()
    if build.exists() and any(build.iterdir()):
        parser.error("--build-dir must be new or empty; prior evidence will not be erased")
    build.mkdir(parents=True, exist_ok=True)
    modules = build / "modules"
    logs = build / "logs"
    modules.mkdir()
    logs.mkdir()
    repo = args.repo.resolve()
    lean = args.lean.resolve()
    report_path = build / "verification.json"
    report = {
        "schema_version": 2, "status": "RUNNING", "started_utc": utc_now(),
        "invocation": [sys.executable, *sys.argv],
        "verifier": "Agent #3 verification specialist", "repository": str(repo),
        "build_directory": str(build), "fresh_module_directory": str(modules),
        "source_records": [], "commands": [],
        "environment": {
            "platform": platform.platform(), "python_version": sys.version,
            "python_executable": sys.executable, "lean_executable": str(lean),
            "LEAN_PATH": str(modules), "lean_trust_level": 0,
        },
    }
    env = os.environ.copy()
    for name in ("LEAN_PATH", "LEAN_SRC_PATH", "LEAN_SYSROOT", "LEAN_OPTS"):
        env.pop(name, None)
    env["LEAN_PATH"] = str(modules)

    def checkpoint() -> None:
        write_json(report_path, report)

    def command(label: str, argv: list[str]) -> str:
        log = logs / (label + ".log")
        entry = {"label": label, "argv": argv, "cwd": str(modules),
                 "LEAN_PATH": str(modules), "started_utc": utc_now(), "log": str(log)}
        report["commands"].append(entry)
        checkpoint()
        start = time.monotonic()
        try:
            with log.open("wb") as output:
                result = subprocess.run(argv, cwd=modules, env=env, stdout=output,
                                        stderr=subprocess.STDOUT, timeout=args.timeout, check=False)
            entry["exit_code"] = result.returncode
        except subprocess.TimeoutExpired:
            entry["exit_code"] = 124
            entry["timeout_seconds"] = args.timeout
        finally:
            entry["elapsed_seconds"] = round(time.monotonic() - start, 6)
            entry["ended_utc"] = utc_now()
            if log.exists():
                entry["log_sha256"] = file_digest(log)
            checkpoint()
        print(f"{label}: exit {entry.get('exit_code', 'unavailable')} ({entry['elapsed_seconds']:.3f}s)", flush=True)
        if entry.get("exit_code") != 0:
            raise VerificationError(f"Command failed: {label}; see {log}")
        output = log.read_text(errors="replace")
        entry["axiom_records"] = parse_axiom_records(output)
        entry["warnings"] = len(re.findall(r"\bwarning:", output))
        checkpoint()
        return output

    try:
        manifest_path = HERE / "source-pins.json"
        manifest_bytes = manifest_path.read_bytes()
        manifest = json.loads(manifest_bytes)
        if manifest.get("status") != "complete":
            raise VerificationError("Source manifest is not finalized")
        if set(manifest["allowed_axioms"]) != ALLOWED_AXIOMS:
            raise VerificationError("Manifest cannot expand the axiom allowlist")
        if set(manifest["audit_namespaces"]) != AUDIT_NAMESPACES:
            raise VerificationError("Unexpected audit namespaces")
        (build / "source-pins.json").write_bytes(manifest_bytes)
        report["manifest_sha256"] = digest(manifest_bytes)
        report["verifier_sha256"] = file_digest(Path(__file__).resolve())
        report["source_base_commit"] = manifest["source_base_commit"]
        report["claim_commit"] = manifest["claim_commit"]
        report["environment"]["lean_sha256"] = file_digest(lean)
        version = command("lean-version", [str(lean), "--version"]).strip()
        report["environment"]["lean_version"] = version
        if not re.search(r"version\s+4\.19\.0(?:,|\))", version):
            raise VerificationError(f"Expected Lean 4.19.0, obtained {version}")
        if manifest["required_lean_commit"] not in version:
            raise VerificationError(f"Unexpected Lean release commit: {version}")
        prefix = Path(command("lean-prefix", [str(lean), "--print-prefix"]).strip()).resolve()
        report["environment"]["lean_prefix"] = str(prefix)
        report["environment"]["standard_library_roots"] = {}
        for name in ("Init", "Std", "Lean"):
            path = prefix / "lib" / "lean" / (name + ".olean")
            report["environment"]["standard_library_roots"][name] = {"path": str(path), "sha256": file_digest(path)}
        available = {"Std"}
        explicit_exports = set()
        explicit_declarations = []
        audited_modules = []
        for record in manifest["modules"]:
            module = record["module"]
            if not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", module) or module in available:
                raise VerificationError(f"Invalid or repeated module name: {module}")
            source = (repo / record["source"]).resolve()
            if not source.is_relative_to(repo):
                raise VerificationError(f"Source escapes repository: {source}")
            data = source.read_bytes()
            actual = digest(data)
            if actual != record["sha256"]:
                raise VerificationError(f"Source hash mismatch for {module}: expected {record['sha256']}, found {actual}")
            code = code_only(data.decode("utf-8"))
            scan = source_scan(code)
            imports = imports_of(code)
            if imports != record["imports"] or not set(imports) <= available:
                raise VerificationError(f"Unpinned import or wrong build order for {module}: {imports}")
            destination = modules / (module + ".lean")
            destination.write_bytes(data)
            if file_digest(destination) != actual:
                raise VerificationError(f"Copy hash mismatch: {destination}")
            checked = {**record, "resolved_source": str(source), "build_copy": str(destination),
                       "copy_sha256": actual, "source_scan": scan, "bytes": len(data)}
            if record["role"] == "contribution":
                declarations = source_declarations(code)
                public = [item["name"] for item in declarations if not item["private"]]
                if public != record["exports"]:
                    raise VerificationError(f"Source declaration inventory mismatch: {module}")
                declared = [{key: item[key] for key in ("name", "kind", "private")}
                            for item in declarations]
                if declared != record["explicit_declarations"]:
                    raise VerificationError(f"Public/private declaration inventory mismatch: {module}")
                if explicit_exports.intersection(public):
                    raise VerificationError(f"Repeated contribution export in {module}")
                explicit_exports.update(public)
                checked["declarations"] = declarations
                explicit_declarations.extend({"module": module, **item} for item in declarations)
                audited_modules.append(module)
            report["source_records"].append(checked)
            available.add(module)
            checkpoint()

        for record in report["source_records"]:
            module = record["module"]
            command(module, [str(lean), "--trust=0", "-o", module + ".olean", module + ".lean"])
            record["olean_sha256"] = file_digest(modules / (module + ".olean"))
            checkpoint()

        module_literals = ", ".join(json.dumps(module) for module in audited_modules)
        inventory_source = "import Lean\n" + "".join(f"import {module}\n" for module in audited_modules) + f'''
open Lean Elab Command
run_cmd do
  let env ← getEnv
  let auditedModules : List String := [{module_literals}]
  for (name, info) in env.constants.toList do
    if let some index := env.getModuleIdxFor? name then
      let owner := env.header.moduleNames[index]!
      if auditedModules.contains owner.toString then
        let user := (privateToUserName? name).getD name
        let isPrivate := (privateToUserName? name).isSome
        liftIO <| IO.println s!"P196_AUDIT_DECL {{owner}} {{name}} {{user}} {{isPrivate}} {{info.isUnsafe}} {{info.isPartial}}"
'''
        inventory_path = modules / "ExportInventory.lean"
        inventory_path.write_text(inventory_source)
        inventory_output = command("ExportInventory", [str(lean), "--trust=0", "ExportInventory.lean"])
        rows = re.findall(r"(?m)^P196_AUDIT_DECL (\S+) (\S+) (\S+) (true|false) (true|false) (true|false)\s*$", inventory_output)
        compiled_entries = [{"module": owner, "name": name, "user_name": user,
                             "private": private == "true", "unsafe": unsafe == "true",
                             "partial": partial == "true"}
                            for owner, name, user, private, unsafe, partial in rows]
        compiled_names = [entry["name"] for entry in compiled_entries]
        if len(compiled_names) != len(set(compiled_names)):
            raise VerificationError("Repeated declaration in compiled environment inventory")
        if {entry["module"] for entry in compiled_entries} != set(audited_modules):
            raise VerificationError("Compiled inventory does not cover every audited source module")
        implementation_names = {entry["name"] for entry in compiled_entries
                                if entry["unsafe"] or entry["partial"]}
        explicit_compiled = set()
        for declared in explicit_declarations:
            matches = [entry for entry in compiled_entries
                       if entry["module"] == declared["module"]
                       and entry["user_name"] == declared["name"]
                       and entry["private"] == declared["private"]]
            if len(matches) != 1:
                raise VerificationError(f"Missing or ambiguous compiled declaration: {declared}")
            entry = matches[0]
            if entry["unsafe"] or entry["partial"]:
                raise VerificationError(f"An explicit source declaration is unsafe or partial: {declared['name']}")
            declared["compiled_name"] = entry["name"]
            explicit_compiled.add(entry["name"])
        inventory = [name for name in compiled_names if name not in implementation_names]
        if not explicit_compiled <= set(inventory):
            raise VerificationError(f"Unauditable source declarations: {sorted(explicit_compiled - set(inventory))}")
        if not all(re.fullmatch(r"[A-Za-z_][A-Za-z_0-9'.]*", name) for name in inventory):
            raise VerificationError("Unsupported declaration name in generated audit")
        inventory.sort()
        private_inventory = sorted(entry["name"] for entry in compiled_entries
                                   if entry["private"] and entry["name"] in inventory)
        public_inventory = sorted(set(inventory) - set(private_inventory))
        audit_source = "import Lean\n" + "".join(f"import {module}\n" for module in audited_modules)
        audit_source += "\nset_option pp.privateNames true\n\n"
        audit_source += "".join(f"#print axioms {name}\n" for name in public_inventory)
        if private_inventory:
            target_literals = ",\n    ".join(json.dumps(name) for name in private_inventory)
            audit_source += f'''
-- Preserve numeric components of private kernel names through `mkIdent`.
-- This diagnostic elaborates an ordinary #print axioms command for each.
open Lean Elab Command
run_cmd do
  let env ← getEnv
  let targets : List String := [{target_literals}]
  for (name, _) in env.constants.toList do
    if targets.contains name.toString then
      elabCommand (← `(command| #print axioms $(mkIdent name)))
'''
        audit_path = modules / "AllExportedAxioms.lean"
        audit_path.write_text(audit_source)
        audit_output = command("AllExportedAxioms", [str(lean), "--trust=0", "AllExportedAxioms.lean"])
        audits = parse_axiom_records(audit_output)
        if set(audits) != set(inventory):
            raise VerificationError("Compiled export inventory and complete axiom audit differ")
        report["audit"] = {
            "namespaces": sorted(AUDIT_NAMESPACES), "modules": audited_modules,
            "explicit_export_count": len(explicit_exports),
            "explicit_declaration_count": len(explicit_declarations),
            "explicit_private_count": sum(item["private"] for item in explicit_declarations),
            "compiled_export_count": len(compiled_names), "logical_export_count": len(inventory),
            "explicit_exports": sorted(explicit_exports),
            "explicit_declarations": explicit_declarations,
            "generated_exports": sorted(set(inventory) - explicit_compiled),
            "compiler_implementation_exports": sorted(implementation_names),
            "compiled_inventory": sorted(compiled_entries, key=lambda entry: (entry["module"], entry["name"])),
            "records": audits, "allowed_axioms": sorted(ALLOWED_AXIOMS),
            "axiom_union": sorted({axiom for axioms in audits.values() for axiom in axioms}),
            "inventory_source_sha256": file_digest(inventory_path),
            "audit_source_sha256": file_digest(audit_path),
        }
        for record in report["source_records"]:
            for key in ("resolved_source", "build_copy"):
                if file_digest(Path(record[key])) != record["sha256"]:
                    raise VerificationError(f"Source changed during build: {record[key]}")
        report["sources_unchanged_after_build"] = True
        if file_digest(manifest_path) != report["manifest_sha256"]:
            raise VerificationError("Manifest changed during verification")
        if file_digest(Path(__file__).resolve()) != report["verifier_sha256"]:
            raise VerificationError("Verifier changed during verification")
        report["status"] = "PASS"
        print(f"PASS: {len(report['source_records'])} pinned modules; {len(explicit_declarations)} explicit declarations; "
              f"{len(inventory)} logical exports audited", flush=True)
        return 0
    except (VerificationError, OSError, ValueError, KeyError) as error:
        report["status"] = "FAIL"
        report["error"] = str(error)
        print("FAIL: " + str(error), file=sys.stderr, flush=True)
        return 1
    finally:
        report["finished_utc"] = utc_now()
        checkpoint()
        print("Verification report: " + str(report_path), flush=True)


if __name__ == "__main__":
    sys.exit(main())
