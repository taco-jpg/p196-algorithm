#!/usr/bin/env python3
"""Independent exact-source Lean rebuild and compiled-ownership axiom audit.

Created by Agent #3 runtime/review specialist, who did not author the new
three-layer obstruction, actual-depth, restricted-family, or aggregate proof modules.
Only this evidence directory and a new scratch build directory are written.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
OLD = "proofs/contributions/agent-3/finite-horizon-overflow-20261016"
NEW = "proofs/contributions/agent-3/two-history-20261016"
PREFIX = "proofs/contributions/agent-3/three-layer-prefix-20261016"
BASE_REF = "89287c9d3eb7dd801c2b1a59eff03140d47d24ec"
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
LEAN_SHA = "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023"

# The order is checked against every actual import before compilation.
PINNED = [
 ("PeriodObstructions", "proofs/PeriodObstructions__70ce034b31b5b218.lean", "83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a", False),
 ("ActualWordBridge", "proofs/ActualWordBridge__7f032d27940694a8.lean", "3123e8f86fe751e61307ea528390bd265515a8d69c731f51e2808fb78d0a6ec6", False),
 ("LychrelDigitSums", "proofs/LychrelDigitSums__0810ace083af80c5.lean", "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57", False),
 ("DecimalSafeRuns", "proofs/DecimalSafeRuns__aaaac5a66315c5e2.lean", "2d0e44adfbfa2592b1eaedfb46d2dff3f62db0a2ca05171bb2a7c1a66ec03f22", False),
 ("TemplateStep", "proofs/TemplateStep__8a161b4553714264.lean", "76ad132fec23f9da8733f72a6baf22c3dbfe68d402a8165766bd8d163549d2ed", False),
 ("Compat", "proofs/Compat__a87d4fe51356e8b5.lean", "73dca78232b0c2c048da4d1d182f84b31c0e95bab283fad603fd342bf38616e6", False),
 ("InverseFibers", NEW + "/dependencies/agent9/InverseFibers.lean", "64f4fa5df54d9365b1b3706eceeab3d3f358eb1040a95e3057ac4d9f82806b70", False),
 ("PathCounts", NEW + "/dependencies/agent9/PathCounts.lean", "588890faa1a29739b00dbe660a5f39971ac5087d997550cb9a740194eb592a33", False),
 ("WordBridge", NEW + "/dependencies/agent9/WordBridge.lean", "83594b2cc412382fa2fc6c38979d7ae4a08e4ee49b0e3b46a7453b010c75a611", False),
 ("ActualWords", NEW + "/dependencies/agent9/ActualWords.lean", "c7937f95b80be88cf81268f4eae2c3d1ed066f49fc8cea6c84ce3a78dee7c324", False),
 ("FamilyDefinitions", OLD + "/FamilyDefinitions.lean", "497ffe833495c50e7df5714fd50c0a4835aaf96f71ec8d21fc43102b1468a1d4", True),
 ("FamilyCardinality", OLD + "/FamilyCardinality.lean", "dfded4df411694fcbe50487e7a963f45c7e0abe34e46ed828926aee9f329248d", True),
 ("FiniteHorizonOverflow", OLD + "/FiniteHorizonOverflow.lean", "2499f62660a598e0b48c024e7fbbabca5b079da6178a1c0ea2ea8f110b38ab3d", True),
 ("SafetyBridge", OLD + "/SafetyBridge.lean", "18079ba07cccf1bcc9098320ae62f887ba080896be11bead43de6e7f26573e5e", True),
 ("NormalizedSafety", OLD + "/NormalizedSafety.lean", "6c344b93df1f8574dcf8ecf60c9db09d3f798c3df1b13831713af010c71652c1", True),
 ("FiniteHorizonTheorem", OLD + "/FiniteHorizonTheorem.lean", "3316df9f3ce5baeac971faff53cfe5d6616beebf50c116c5662476c261f0d697", True),
 ("HistoryInterfaces", NEW + "/HistoryInterfaces.lean", "c30d29782c8e68bf49d75bd4c969e04570556fe230f980bc579395d8deb8f60c", True),
 ("TwoLayerCertificate", NEW + "/TwoLayerCertificate.lean", "5caeb408dbb91d855b06afb7b5dcd7f88e2594af691a60f63e76c739ea8f6191", True),
 ("ActualHistories", NEW + "/ActualHistories.lean", "b72d9a6ef082c3d980b3f6f2a9dee64835d38ed32fb7d040abb39b9ea02c6ec4", True),
 ("IntegerInterfaces", NEW + "/IntegerInterfaces.lean", "bc6d2926cd16c43de990ede025b9ba69e50d1e7e2a578044ad65bdf348e8b4fe", True),
 ("HistoryFamily", NEW + "/HistoryFamily.lean", "664992406e3b07beb08a5c120001354a90244ccc814d581228871d29f56cd2d7", True),
 ("HistorySafety", NEW + "/HistorySafety.lean", "16ea25b00f12eed305519eb8de73b564bae5ff3a5ddd255895d5485bebfd33ff", True),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, value: object) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2) + "\n")
    tmp.replace(path)


def strip_comments(text: str) -> str:
    """Preserve line positions, handling nested Lean block comments."""
    out, depth, i = [], 0, 0
    while i < len(text):
        if text.startswith("/-", i):
            depth += 1
            out.append("  ")
            i += 2
        elif depth and text.startswith("-/", i):
            depth -= 1
            out.append("  ")
            i += 2
        elif not depth and text.startswith("--", i):
            end = text.find("\n", i)
            if end < 0:
                end = len(text)
            out.append(" " * (end - i))
            i = end
        else:
            out.append(text[i] if not depth or text[i] == "\n" else " ")
            i += 1
    if depth:
        raise RuntimeError("Unclosed block comment")
    return "".join(out)


def explicit_declarations(text: str) -> list[dict]:
    code = strip_comments(text)
    namespaces = re.findall(r"(?m)^namespace ([^\n]+)$", code)
    if len(namespaces) != 1:
        raise RuntimeError("Expected one explicit contribution namespace")
    pattern = r"(?m)^[ \t]*((?:(?:private|protected|noncomputable|unsafe|partial)[ \t]+)*)" \
        r"(def|abbrev|theorem|lemma|axiom|opaque|constant)\s+([A-Za-z_][A-Za-z_0-9'.]*)"
    declarations = []
    for m in re.finditer(pattern, code):
        declarations.append({"user_name": namespaces[0] + "." + m[3],
            "kind": m[2], "private": "private" in m[1].split(),
            "line": code.count("\n", 0, m.start()) + 1})
    return declarations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--build", required=True, type=Path)
    parser.add_argument("--freeze", required=True, type=Path)
    args = parser.parse_args()
    repo, lean, build = args.repo.resolve(), args.lean.resolve(), args.build.resolve()
    if build.exists() and any(build.iterdir()):
        parser.error("The build directory must be new or empty; previous evidence is preserved.")
    build.mkdir(parents=True, exist_ok=True)
    modules, logs = build / "modules", HERE / "logs"
    modules.mkdir()
    logs.mkdir(exist_ok=True)
    report = {"status": "RUNNING", "reviewer": "Agent #3 runtime and independent review specialist",
        "started_utc": datetime.now(timezone.utc).isoformat(), "repository": str(repo),
        "fresh_build": str(build), "lean_executable": str(lean),
        "invocation": [sys.executable, *sys.argv], "sources": [], "commands": []}
    report_file = HERE / "verification.json"
    env = os.environ.copy()
    for key in ("LEAN_PATH", "LEAN_SRC_PATH", "LEAN_SYSROOT", "LEAN_OPTS"):
        env.pop(key, None)
    env["LEAN_PATH"] = str(modules)
    report["LEAN_PATH"] = str(modules)

    def checkpoint() -> None:
        save(report_file, report)

    def run(label: str, argv: list[str]) -> str:
        start = time.monotonic()
        result = subprocess.run(argv, cwd=modules, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=600)
        output = result.stdout
        log = logs / (label + ".log")
        log.write_text(output)
        report["commands"].append({"label": label, "argv": argv,
            "exit_code": result.returncode, "seconds": round(time.monotonic() - start, 3),
            "log": str(log), "output_sha256": sha(log)})
        checkpoint()
        print(f"{label}: exit {result.returncode} ({time.monotonic() - start:.2f}s)", flush=True)
        if result.returncode:
            raise RuntimeError(f"Compiler command failed: {label}; see {log}")
        if re.search(r"declaration uses.*sorry|\bsorryAx\b|\bLean\.ofReduceBool\b", output):
            raise RuntimeError(f"Untrusted proof dependency in {label}")
        return output

    try:
        if sha(lean) != LEAN_SHA:
            raise RuntimeError("Lean executable hash differs from the verified runtime")
        report["lean_sha256"] = LEAN_SHA
        version = run("00-lean-version", [str(lean), "--version"])
        if "version 4.19.0," not in version or "6caaee842e94" not in version:
            raise RuntimeError("Lean version mismatch")
        report["lean_version"] = version.strip()
        freeze = json.loads(args.freeze.read_text())
        if freeze["baseline_ref"] != BASE_REF:
            raise RuntimeError("Inherited source reference differs from the frozen baseline")
        report["freeze_manifest"] = str(args.freeze.resolve())
        report["freeze_manifest_sha256"] = sha(args.freeze)
        report["inherited_source_ref"] = BASE_REF
        report["freeze_provenance"] = freeze.get("provenance", {})
        pinned = [*PINNED, ("TwoHistoryTheorem", NEW + "/TwoHistoryTheorem.lean",
            "386b181e43ba96a90ca46bc22e40dd05d5cbccf8a683aa5e96e6a5709aa448ee", True)]
        new_modules = ["DeadPrefix", "ActualDepth", "SharpHistoryFamily", "SharpHistoryTheorem"]
        if set(freeze["modules"]) != set(new_modules):
            raise RuntimeError("The frozen module list must be exactly the four assigned sources")
        for name in new_modules:
            pinned.append((name, PREFIX + "/" + name + ".lean", freeze["modules"][name], True))
        ready = {"Std", "Lean"}
        contribution_modules = []
        for module, relative, expected, contribution in pinned:
            source, destination = repo / relative, modules / (module + ".lean")
            data = source.read_bytes()
            actual = hashlib.sha256(data).hexdigest()
            if actual != expected:
                raise RuntimeError(f"Source hash mismatch: {module}: {actual} != {expected}")
            code = strip_comments(data.decode())
            imports = [word for line in re.findall(r"(?m)^import ([^\n]+)", code) for word in line.split()]
            if not set(imports) <= ready:
                raise RuntimeError(f"Unstaged or out-of-order imports for {module}: {set(imports) - ready}")
            record = {"module": module, "source": str(source), "repo_relative_source": relative,
                "sha256": actual, "bytes": len(data), "imports": imports, "contribution": contribution}
            record["git_blob_sha1"] = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            if not relative.startswith(PREFIX + "/"):
                expected_blob = subprocess.check_output(
                    ["git", "rev-parse", BASE_REF + ":" + relative], cwd=repo, text=True).strip()
                if expected_blob != record["git_blob_sha1"]:
                    raise RuntimeError(f"Inherited Git source identity mismatch: {module}")
                record["baseline_ref"] = BASE_REF
                record["baseline_git_blob_verified"] = True
            if contribution:
                forbidden = re.findall(r"\b(?:sorry|admit|sorryAx|native_decide|native_cast|vm_decide|unsafe|partial|axiom|implemented_by|extern|run_cmd|run_tac|elab|macro|syntax|Lean\.ofReduceBool|Lean\.trustCompiler|debug\.skipKernelTC)\b", code)
                if forbidden:
                    raise RuntimeError(f"Forbidden proof-source declaration or shortcut in {module}: {forbidden}")
                record["proof_source_shortcut_scan"] = "PASS"
                contribution_modules.append(module)
                record["explicit_declarations"] = explicit_declarations(data.decode())
            destination.write_bytes(data)
            report["sources"].append(record)
            ready.add(module)
        pins = json.loads((repo / NEW / "dependencies/agent9/SOURCE_PINS.json").read_text())
        for pin in pins:
            record = next(r for r in report["sources"] if r["module"] == pin["module"])
            if record["sha256"] != pin["sha256"]:
                raise RuntimeError(f"Agent9 provenance mismatch for {pin['module']}")
            data = (repo / record["repo_relative_source"]).read_bytes()
            git_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            if git_blob != pin["git_blob"]:
                raise RuntimeError(f"Agent9 Git blob mismatch for {pin['module']}")
        report["agent9_source_pins"] = pins
        checkpoint()
        for index, record in enumerate(report["sources"], 1):
            name = record["module"]
            run(f"{index:02d}-{name}", [str(lean), "--trust=0", "-o", name + ".olean", name + ".lean"])
            record["olean_sha256"] = sha(modules / (name + ".olean"))
            checkpoint()

        owners = ", ".join(json.dumps(m) for m in contribution_modules)
        audit_source = f'''import Lean
import SharpHistoryTheorem
set_option pp.privateNames true
set_option maxRecDepth 100000
set_option maxHeartbeats 0
open Lean Elab Command
run_cmd do
  let env ← getEnv
  let owners : List String := [{owners}]
  for (name, info) in env.constants.toList do
    if let some index := env.getModuleIdxFor? name then
      let owner := env.header.moduleNames[index]!
      if owners.contains owner.toString then
        let user := (privateToUserName? name).getD name
        let isPrivate := (privateToUserName? name).isSome
        liftIO <| IO.println s!"INDEPENDENT_DECL {{owner}} {{name}} {{user}} {{isPrivate}} {{info.isUnsafe}} {{info.isPartial}}"
        unless info.isUnsafe || info.isPartial do
          elabCommand (← `(command| #print axioms $(mkIdent name)))
'''
        (modules / "IndependentOwnershipAudit.lean").write_text(audit_source)
        (HERE / "IndependentOwnershipAudit.lean").write_text(audit_source)
        output = run("28-compiled-ownership-axioms", [str(lean), "--trust=0", "IndependentOwnershipAudit.lean"])
        inventory = []
        for line in output.splitlines():
            if line.startswith("INDEPENDENT_DECL "):
                _, owner, name, user, private, unsafe, partial = line.split()
                inventory.append({"owner": owner, "name": name, "user_name": user,
                    "private": private == "true", "unsafe": unsafe == "true", "partial": partial == "true"})
        inventory.sort(key=lambda r: (r["owner"], r["name"]))
        if len({r["name"] for r in inventory}) != len(inventory):
            raise RuntimeError("Duplicate compiled declaration inventory entries")
        axioms = {}
        expression = r"'([^\n]+?)' (?:does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])"
        for match in re.finditer(expression, output):
            if match[1] in axioms:
                raise RuntimeError("Duplicate axiom result for " + match[1])
            values = sorted({s.strip() for s in (match[2] or "").split(",") if s.strip()})
            if set(values) - ALLOWED:
                raise RuntimeError(f"Nonstandard axioms for {match[1]}: {values}")
            axioms[match[1]] = values
        safe = {r["name"] for r in inventory if not r["unsafe"] and not r["partial"]}
        if set(axioms) != safe:
            raise RuntimeError(f"Audit coverage mismatch: missing={sorted(safe-set(axioms))}, extra={sorted(set(axioms)-safe)}")
        explicit_count = 0
        for record in report["sources"]:
            for declaration in record.get("explicit_declarations", []):
                matches = [r for r in inventory if r["owner"] == record["module"]
                    and r["user_name"] == declaration["user_name"] and r["private"] == declaration["private"]]
                if len(matches) != 1:
                    raise RuntimeError(f"Explicit declaration coverage mismatch: {declaration}")
                match = matches[0]
                if match["unsafe"] or match["partial"] or match["name"] not in axioms:
                    raise RuntimeError(f"Explicit source declaration not fully checked: {declaration}")
                declaration["compiled_name"] = match["name"]
                declaration["axioms"] = axioms[match["name"]]
                explicit_count += 1
        for record in report["sources"]:
            name = record["module"]
            if sha(Path(record["source"])) != record["sha256"] or sha(modules/(name+".lean")) != record["sha256"]:
                raise RuntimeError(f"Source changed during the build: {name}")
            if sha(modules/(name+".olean")) != record["olean_sha256"]:
                raise RuntimeError(f"Compiled artifact changed unexpectedly: {name}")
        save(HERE / "compiled-declarations.json", inventory)
        save(HERE / "axiom-dependencies.json", axioms)
        report["audit"] = {"contribution_modules": contribution_modules,
            "explicit_source_declarations": explicit_count, "compiled_declarations": len(inventory),
            "safe_logical_declarations_audited": len(safe),
            "generated_unsafe_or_partial_declarations": [r for r in inventory if r["unsafe"] or r["partial"]],
            "axiom_union": sorted(set().union(*(set(v) for v in axioms.values()))),
            "complete_inventory_coverage": True, "all_explicit_declarations_safe_and_total": True}
        report["source_hashes_stable_after_build"] = True
        report["module_count"] = len(report["sources"])
        report["status"] = "PASS"
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        checkpoint()
        print(json.dumps({"status": "PASS", "modules": report["module_count"],
            "explicit_declarations": explicit_count, "safe_audited": len(safe),
            "axioms": report["audit"]["axiom_union"]}), flush=True)
        return 0
    except Exception as error:
        report["status"] = "FAIL"
        report["error"] = f"{type(error).__name__}: {error}"
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        checkpoint()
        print(report["error"], file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
