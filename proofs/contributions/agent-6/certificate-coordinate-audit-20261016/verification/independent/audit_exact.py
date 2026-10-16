#!/usr/bin/env python3
"""Independent complete module-origin and axiom audit of an exact fresh build.

Every project theorem and safe definition is checked with Lean.collectAxioms
and also printed with #print axioms. JSON records prevent pretty-print wrapping
from silently truncating the inventory; a separate multiline parser must agree.
No theorem source or Git object is written by this audit.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent
LEAN = RUNTIME / "lean-4.19.0-linux/bin/lean"
PARSER = RUNTIME / "source-snapshot/p196-algorithm-4b4edf976b2c7a9ba1dad80636c0e21c66350325/proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/verify_project.py"
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
FLAGS = [str(LEAN), "--trust=0", "-j1", "-DElab.async=false"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def parse_printed_axioms(text: str) -> dict[str, list[str]]:
    # The name capture deliberately includes apostrophes, e.g. append_inj_left'.
    # The list capture deliberately spans physical lines until its closing ']'.
    entries = [(n, [a.strip() for a in ax.split(",") if a.strip()])
               for n, ax in re.findall(r"^'(.+)' depends on axioms:\s*\[([^\]]*)\]", text, re.M)]
    entries += [(n, []) for n in re.findall(r"^'(.+)' does not depend on any axioms$", text, re.M)]
    if len(entries) != len({n for n, _ in entries}):
        raise ValueError("Duplicate #print axioms entry")
    result = dict(entries)
    if any(not set(ax) <= ALLOWED for ax in result.values()):
        raise ValueError("Unapproved axiom in complete #print output")
    return result


def json_records(text: str, prefix: str) -> list[dict]:
    return [json.loads(line[len(prefix) + 1:]) for line in text.splitlines() if line.startswith(prefix + " ")]


def main() -> int:
    base = Path(sys.argv[1]).resolve()
    assert base.is_relative_to(HERE)
    source, build = base / "source", base / "build"
    audit = base / "audit"
    audit.mkdir(exist_ok=False)
    logs = audit / "logs"
    logs.mkdir()
    objects = build / "objects"
    manifest = json.loads((base / "source-manifest.json").read_text())
    compilation = json.loads((build / "compilation.json").read_text())
    if compilation["status"] != "COMPILED_PENDING_INDEPENDENT_AXIOM_AUDIT":
        raise ValueError("Fresh compilation has not completed successfully")
    order = manifest["build_order"]
    env = {"PATH": str(LEAN.parent) + ":/usr/bin:/bin", "LANG": "C.UTF-8", "LEAN_PATH": str(objects)}
    report = {
        "status": "RUNNING", "started_utc": utc(),
        "reviewer": "Agent #6 runtime/reproducibility specialist", "same_project_affiliation": True,
        "review_type": manifest["review_type"], "source_branch_commit": manifest["source_branch_commit"],
        "source_branch_tree": manifest.get("source_branch_tree"),
        "runner_path": str(Path(__file__).resolve()), "runner_sha256": sha(Path(__file__)),
        "source_manifest_sha256": sha(base / "source-manifest.json"),
        "compilation_receipt_sha256": sha(build / "compilation.json"),
        "all_project_objects_freshly_compiled_for_this_review": True,
        "allowed_axioms": sorted(ALLOWED), "build_order": order, "commands": [],
        "source_repairs": [], "git_mutations": False, "shim_used": False,
        "historical_receipt_correction": {
            "prior_scope": "Agent116 final historical 1991-theorem audit, broader than this closure",
            "truncated_manifest_lists": 25, "complete_raw_log_entries": 1991,
            "complete_raw_log_axiom_union": sorted(ALLOWED),
            "meaning": "Line-parser defect only; complete raw lists contain no additional axiom. No theorem failure or source repair.",
        },
    }

    def save() -> None:
        (audit / "verification.json").write_text(json.dumps(report, indent=2) + "\n")

    def run(label: str, argv: list[str]) -> str:
        start = time.monotonic()
        log = logs / (label + ".log")
        with log.open("wb") as stream:
            try:
                code = subprocess.run(argv, cwd=audit, env=env, stdout=stream,
                                      stderr=subprocess.STDOUT, timeout=900).returncode
            except subprocess.TimeoutExpired:
                code = 124
        report["commands"].append({"label": label, "argv": argv, "cwd": str(audit),
            "environment": env, "exit_code": code, "elapsed_seconds": round(time.monotonic()-start, 6),
            "log": str(log.relative_to(base)), "log_sha256": sha(log)})
        save()
        print(label, "exit=" + str(code), flush=True)
        if code:
            raise RuntimeError("Audit execution failed: " + label)
        return log.read_text()

    def check_integrity() -> None:
        if sha(base / "source-manifest.json") != compilation["source_manifest_sha256"]:
            raise ValueError("Source manifest changed since fresh compilation")
        for rec in manifest["modules"]:
            name = rec["module"]
            staged = source / (name + ".lean")
            if sha(staged) != rec["sha256"] or Path(rec["path"]).read_bytes() != staged.read_bytes():
                raise ValueError("Source changed: " + name)
        for p, expected in compilation["compiler"]["files"].items():
            if sha(Path(p)) != expected:
                raise ValueError("Compiler changed: " + p)
        if {p.stem for p in objects.glob("*.olean")} != set(order):
            raise ValueError("Object census changed")
        for name, rec in compilation["objects"].items():
            if sha(objects / (name + ".olean")) != rec["sha256"]:
                raise ValueError("Compiled object changed: " + name)

    try:
        check_integrity()
        report["compiler"] = compilation["compiler"]
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location("pinned_inventory_parser", PARSER)
        assert spec is not None and spec.loader is not None
        parser = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(parser)
        report["source_parser"] = {"path": str(PARSER), "sha256": sha(PARSER)}
        named, private, anonymous_instances = {}, {}, {}
        header = re.compile(r"^[ \t]*(?:(?:@\[[^\]]*\])[ \t\n]*)*(?:(private|protected|noncomputable)[ \t]+)?(theorem|def|structure|abbrev|opaque|inductive|instance)[ \t]+([A-Za-z_][\w'.]*)", re.M)
        for rec in manifest["modules"]:
            mod = rec["module"]
            code = parser.code_only((source / (mod + ".lean")).read_text())
            namespaces = re.findall(r"^namespace\s+(\S+)", code, re.M)
            if len(namespaces) != 1:
                raise ValueError("Inventory requires explicit namespace review: " + mod)
            entries = header.findall(code)
            if any(vis in {"protected", "noncomputable"} for vis, kind, n in entries):
                raise ValueError("Inventory requires explicit declaration-visibility review: " + mod)
            named[mod] = [{"kind": kind, "name": namespaces[0] + "." + n}
                          for vis, kind, n in entries if vis != "private"]
            private[mod] = [{"kind": kind, "source_name": namespaces[0] + "." + n}
                            for vis, kind, n in entries if vis == "private"]
            anonymous_instances[mod] = len(re.findall(r"^instance\s*(?=\()", code, re.M))
        explicit = [d["name"] for mod in order for d in named[mod]]
        exports = {mod: [d["name"] for d in named[mod] if d["kind"] == "theorem"] for mod in order}
        if len(explicit) != len(set(explicit)):
            raise ValueError("Duplicate explicit declaration inventory")
        report["explicit_named_declarations"] = named
        report["explicit_public_theorem_exports"] = exports
        report["explicit_public_theorem_count"] = sum(len(v) for v in exports.values())
        report["private_source_declarations"] = private
        report["anonymous_instance_source_counts"] = anonymous_instances
        imports = "\n".join("import " + m for m in manifest["roots"]) + "\nimport Lean\n"
        public_audit = imports + "set_option pp.universes true\n\n"
        public_audit += "\n".join("#check " + n for n in explicit) + "\n"
        public_audit += "\n".join("#print axioms " + n for n in explicit) + "\n"
        (audit / "ExplicitExports.lean").write_text(public_audit)
        output = run("ExplicitExports", FLAGS + ["--root=" + str(audit), str(audit / "ExplicitExports.lean")])
        explicit_axioms = parse_printed_axioms(output)
        if set(explicit_axioms) != set(explicit):
            raise ValueError("Explicit exported declaration axiom census mismatch")
        report["explicit_named_declaration_count"] = len(explicit)
        (audit / "explicit-axioms.json").write_text(json.dumps(explicit_axioms, indent=2) + "\n")
        module_audit = imports + '''open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := MODULE_SELECTION
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  for mod in selected do
    if !(env.allImportedModuleNames.toList.any (fun n => n.toString == mod)) then
      throwError m!"MISSING_PROJECT_MODULE {mod}"
    logInfo m!"AUDIT_MODULE_JSON {(Json.mkObj [("module", toJson mod)]).compress}"
  let mut count : Nat := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        let kind := match info with
          | .axiomInfo _ => "axiom"
          | .thmInfo _ => "theorem"
          | .defnInfo _ => "definition"
          | .opaqueInfo _ => "opaque"
          | .quotInfo _ => "quotient"
          | .inductInfo _ => "inductive"
          | .ctorInfo _ => "constructor"
          | .recInfo _ => "recursor"
        let origin := [("module", toJson mod.toString), ("kind", toJson kind), ("name", toJson name.toString)]
        logInfo m!"AUDIT_CONSTANT_JSON {(Json.mkObj origin).compress}"
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM_JSON {(Json.mkObj origin).compress}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          let record := origin ++ [("axioms", toJson (axl.map Name.toString))]
          logInfo m!"AUDIT_THEOREM_JSON {(Json.mkObj record).compress}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | .defnInfo _ =>
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          let record := origin ++ [("axioms", toJson (axl.map Name.toString))]
          if info.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_DEFINITION_JSON {(Json.mkObj record).compress}"
          else
            if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_DEFINITION_AXIOMS {mod} {name} : {axl}"
            logInfo m!"AUDIT_SAFE_DEFINITION_JSON {(Json.mkObj record).compress}"
            elabCommand (← `(command| #print axioms $(mkIdent name)))
        | .opaqueInfo _ =>
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          if info.isUnsafe then throwError m!"UNEXPECTED_UNSAFE_OPAQUE {mod} {name}"
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_OPAQUE_AXIOMS {mod} {name} : {axl}"
          let record := origin ++ [("axioms", toJson (axl.map Name.toString))]
          logInfo m!"AUDIT_SAFE_OPAQUE_JSON {(Json.mkObj record).compress}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT_JSON {(Json.mkObj [("theorem_count", toJson count), ("axiom_union", toJson (union.map Name.toString))]).compress}"
'''
        module_audit = module_audit.replace("MODULE_SELECTION", json.dumps(order))
        (audit / "ModuleAudit.lean").write_text(module_audit)
        output = run("ModuleAudit", FLAGS + ["--root=" + str(audit), str(audit / "ModuleAudit.lean")])
        constants = json_records(output, "AUDIT_CONSTANT_JSON")
        theorems = json_records(output, "AUDIT_THEOREM_JSON")
        safe_defs = json_records(output, "AUDIT_SAFE_DEFINITION_JSON")
        unsafe_defs = json_records(output, "UNSAFE_IMPLEMENTATION_DEFINITION_JSON")
        unsafe_axioms = json_records(output, "UNSAFE_IMPLEMENTATION_AXIOM_JSON")
        safe_opaque = json_records(output, "AUDIT_SAFE_OPAQUE_JSON")
        selected = json_records(output, "AUDIT_MODULE_JSON")
        # A single exact end marker is mandatory; unknown/malformed JSON fails.
        summary = json_records(output, "FULL_MODULE_AUDIT_JSON")
        if [r["module"] for r in selected] != order or len(summary) != 1:
            raise ValueError("Missing/repeated module or final audit record")
        if len({r["name"] for r in constants}) != len(constants):
            raise ValueError("Duplicate module-origin constant")
        by_name = {r["name"]: r for r in constants}
        for label, records, kind in [("theorem", theorems, "theorem"), ("definition", safe_defs + unsafe_defs, "definition"), ("axiom", unsafe_axioms, "axiom"), ("opaque", safe_opaque, "opaque")]:
            if {r["name"] for r in records} != {r["name"] for r in constants if r["kind"] == kind}:
                raise ValueError("Incomplete kind inventory: " + label)
            if len(records) != len({r["name"] for r in records}):
                raise ValueError("Repeated kind inventory: " + label)
        if summary[0]["theorem_count"] != len(theorems):
            raise ValueError("Theorem total mismatch")
        checked = theorems + safe_defs + safe_opaque
        full_axioms = parse_printed_axioms(output)
        if set(full_axioms) != {r["name"] for r in checked}:
            raise ValueError("Full #print axiom census differs from structured environment census")
        for rec in checked:
            if set(full_axioms[rec["name"]]) != set(rec["axioms"]) or not set(rec["axioms"]) <= ALLOWED:
                raise ValueError("Printed/structured axiom disagreement: " + rec["name"])
            if by_name[rec["name"]]["module"] != rec["module"]:
                raise ValueError("Axiom record origin disagreement")
        private_origins = {}
        for mod in order:
            for declaration in named[mod]:
                n = declaration["name"]
                if n not in by_name or by_name[n]["module"] != mod:
                    raise ValueError("Explicit declaration has wrong/missing module origin: " + n)
                if declaration["kind"] == "theorem" and n not in {r["name"] for r in theorems}:
                    raise ValueError("Explicit theorem absent from full audit: " + n)
                if n in full_axioms and set(full_axioms[n]) != set(explicit_axioms[n]):
                    raise ValueError("Independent explicit/full axiom passes disagree: " + n)
            for declaration in private[mod]:
                matches = [r for r in constants if r["module"] == mod and r["name"].startswith("_private." + mod + ".") and r["name"].endswith("." + declaration["source_name"])]
                kind = {"def": "definition", "abbrev": "definition", "structure": "inductive"}.get(declaration["kind"], declaration["kind"])
                if len(matches) != 1 or matches[0]["kind"] != kind:
                    raise ValueError("Private source declaration origin missing/ambiguous")
                private_origins[declaration["source_name"]] = matches[0]["name"]
        report["private_declaration_origins"] = private_origins
        report["all_theorem_constants_audited"] = len(theorems)
        report["safe_definitions_axiom_audited"] = len(safe_defs)
        report["safe_opaque_constants_audited"] = len(safe_opaque)
        report["unsafe_implementation_definition_count"] = len(unsafe_defs)
        report["unsafe_implementation_axioms"] = unsafe_axioms
        report["module_constant_count"] = len(constants)
        report["theorem_constant_counts_by_module"] = {m: sum(r["module"] == m for r in theorems) for m in order}
        report["safe_definition_counts_by_module"] = {m: sum(r["module"] == m for r in safe_defs) for m in order}
        report["module_constant_counts_by_kind"] = {m: dict(Counter(r["kind"] for r in constants if r["module"] == m)) for m in order}
        report["axiom_union"] = sorted({a for r in checked for a in r["axioms"]})
        report["multiline_print_parser_agrees_with_structured_lean_records"] = True
        (audit / "module-constants.json").write_text(json.dumps(constants, indent=2) + "\n")
        (audit / "full-module-axioms.json").write_text(json.dumps(checked, indent=2) + "\n")
        (audit / "unsafe-implementation-definitions.json").write_text(json.dumps(unsafe_defs, indent=2) + "\n")
        check_integrity()
        report["source_objects_compiler_unchanged_before_after"] = True
        report["status"] = "PASS"
        report["scope"] = "Fresh exact-source compilation followed by named source export checks, all theorem and safe-definition axiom checks, complete module-origin census, private helper coverage, generated unsafe implementation inventory, and independent multiline/structured axiom agreement. This is dependency verification, not a new proof claim. Semantic review is separate."
        print("PASS", len(order), "modules", len(theorems), "theorem constants", len(safe_defs), "safe definitions", flush=True)
        return 0
    except Exception as error:
        report["status"] = "FAIL"
        report["error"] = str(error)
        (audit / "failure.txt").write_text(traceback.format_exc())
        print("FAIL", error, flush=True)
        return 1
    finally:
        report["finished_utc"] = utc()
        save()


if __name__ == "__main__":
    raise SystemExit(main())
