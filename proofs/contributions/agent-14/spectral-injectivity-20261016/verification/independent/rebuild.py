#!/usr/bin/env python3
"""Independently rebuild the frozen spectral closure and audit safe constants.

This program authors no mathematical theorem. The optional canonical replay uses
the repository verifier without modification and records its different flags.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
import traceback


PROJECT = "agent14-spectral-injectivity"
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
FIXED_PINS = {
    "LychrelDigitSums": "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57",
    "Agent14SpectralWeights": "d691d02f3170db988ac9c5529402f5c09cf83425c7188d78cd0f2a6a8f4568c8",
    "Agent14SpectralInjectivity": "082347eccad303f235a835c65be2dc20062d4457646082575cd192d06601d0c9",
}
VERIFIER_SHA256 = "c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a"
IDENTIFIER = re.compile(r"[A-Za-z_][\w']*(?:\.[A-Za-z_][\w']*)*\Z")
FORBIDDEN = re.compile(r"\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b")


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def masked_source(text):
    """Mask strings and nested comments for lexical source checks."""
    result = []
    index = 0
    depth = 0
    quoted = False
    while index < len(text):
        pair = text[index:index + 2]
        char = text[index]
        if depth:
            if pair == "/-":
                depth += 1
                result.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                result.extend("  ")
                index += 2
            else:
                result.append("\n" if char == "\n" else " ")
                index += 1
        elif quoted:
            if char == "\\":
                result.extend("  ")
                index += 2
            else:
                quoted = char != '"'
                result.append("\n" if char == "\n" else " ")
                index += 1
        elif pair == "/-":
            depth = 1
            result.extend("  ")
            index += 2
        elif pair == "--":
            end = text.find("\n", index)
            end = len(text) if end < 0 else end
            result.extend(" " * (end - index))
            index = end
        elif char == '"':
            quoted = True
            result.append(" ")
            index += 1
        else:
            result.append(char)
            index += 1
    if depth or quoted:
        raise ValueError("Unterminated source comment or string")
    return "".join(result)


def declared_public_names(module, code):
    """Enumerate explicit public declarations in the inspected new namespace."""
    namespaces = re.findall(r"^\s*namespace\s+(\S+)\s*$", code, re.M)
    if namespaces != ["Agent14.Spectral"]:
        raise ValueError("Unexpected namespace organization in " + module)
    stripped = re.sub(r"@\[[^\]]*\]", "", code)
    pattern = re.compile(
        r"^\s*((?:(?:private|protected|noncomputable|partial|unsafe)\s+)*)"
        r"(theorem|lemma|def|abbrev|opaque|structure|inductive)\s+([A-Za-z_][\w']*)",
        re.M,
    )
    names = []
    for modifiers, kind, name in pattern.findall(stripped):
        if "private" not in modifiers.split():
            names.append({"name": "Agent14.Spectral." + name,
                          "source_kind": kind, "module": module})
    if not names or len({record["name"] for record in names}) != len(names):
        raise ValueError("Missing or duplicate public declarations in " + module)
    return names


def axiom_list(text):
    if not text.startswith("[") or not text.endswith("]"):
        raise ValueError("Malformed axiom output: " + text)
    return [part.strip() for part in text[1:-1].split(",") if part.strip()]


def parse_safe_audit(audit_log):
    """Read Lean's pretty-printed axiom arrays, including wrapped lines."""
    pattern = re.compile(r"^SAFE_CONSTANT (\S+) (\S+) (\S+) : (\[[^\]]*\])$", re.M)
    constants = [{"module": mod, "kind": kind, "name": name, "axioms": axiom_list(axs)}
                 for mod, kind, name, axs in pattern.findall(audit_log)]
    summary_pattern = re.compile(r"^FULL_SAFE_AUDIT safe=(\d+) theorem=(\d+) definition=(\d+) opaque=(\d+) other=(\d+) unsafe=(\d+) partial=(\d+) union=(\[[^\]]*\])$", re.M)
    summaries = summary_pattern.findall(audit_log)
    if len(summaries) != 1 or int(summaries[0][0]) != len(constants) or not constants:
        raise ValueError("Safe audit output is absent or incomplete")
    if len({rec["name"] for rec in constants}) != len(constants):
        raise ValueError("Duplicate audited constants")
    keys = ["safe", "theorem", "definition", "opaque", "other", "unsafe", "partial"]
    summary = dict(zip(keys, map(int, summaries[0][:7])))
    summary["axiom_union"] = axiom_list(summaries[0][7])
    unsafe = re.findall(r"^INVENTORY_UNSAFE (\S+) (\S+) (\S+)$", audit_log, re.M)
    partial = re.findall(r"^INVENTORY_PARTIAL (\S+) (\S+) (\S+)$", audit_log, re.M)
    if len(unsafe) != summary["unsafe"] or len(partial) != summary["partial"]:
        raise ValueError("Unsafe or partial inventory count mismatch")
    for kind in ["theorem", "definition", "opaque"]:
        if sum(rec["kind"] == kind for rec in constants) != summary[kind]:
            raise ValueError("Safe audit category count mismatch")
    if sum(rec["kind"] not in {"theorem", "definition", "opaque"} for rec in constants) != summary["other"]:
        raise ValueError("Other safe declaration count mismatch")
    observed_union = {axiom for rec in constants for axiom in rec["axioms"]}
    if observed_union - ALLOWED or observed_union != set(summary["axiom_union"]):
        raise ValueError("Disallowed or inconsistent safe axiom union")
    return constants, summary, unsafe, partial


def parse_public_axioms(public_log, public_names):
    """Require one literal #print axioms result for every explicit public name."""
    records = {}
    pattern = re.compile(r"^'([^']+)' (?:does not depend on any axioms|depends on axioms: (\[[^\]]*\]))$", re.M)
    for match in pattern.finditer(public_log):
        name, axioms = match.groups()
        if name in records:
            raise ValueError("Duplicate public axiom report")
        records[name] = axiom_list(axioms) if axioms else []
    if set(records) != set(public_names):
        raise ValueError("Public #print axioms reports do not cover the complete explicit declaration list")
    if any(set(axioms) - ALLOWED for axioms in records.values()):
        raise ValueError("Disallowed public theorem or definition axiom")
    return records


def safe_audit_source(order, roots):
    return ("\n".join("import " + name for name in roots) + "\nimport Lean\n"
            "open Lean Elab Command\n"
            "set_option maxRecDepth 100000\nset_option maxHeartbeats 0\n"
            "run_cmd do\n  let env ← getEnv\n  let selected : List String := "
            + json.dumps(order) + "\n" + r'''
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut safeCount := 0
  let mut theoremCount := 0
  let mut definitionCount := 0
  let mut opaqueCount := 0
  let mut otherCount := 0
  let mut unsafeCount := 0
  let mut partialCount := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        let kind : String := match info with
          | .axiomInfo _ => "axiom"
          | .thmInfo _ => "theorem"
          | .defnInfo _ => "definition"
          | .opaqueInfo _ => "opaque"
          | .inductInfo _ => "inductive"
          | .ctorInfo _ => "constructor"
          | .recInfo _ => "recursor"
          | .quotInfo _ => "quotient"
        if info.isUnsafe then
          unsafeCount := unsafeCount + 1
          logInfo m!"INVENTORY_UNSAFE {mod} {kind} {name}"
        else if info.isPartial then
          partialCount := partialCount + 1
          logInfo m!"INVENTORY_PARTIAL {mod} {kind} {name}"
        else
          if kind == "axiom" then
            throwError m!"CUSTOM_SAFE_AXIOM {mod} {name}"
          safeCount := safeCount + 1
          if kind == "theorem" then theoremCount := theoremCount + 1
          else if kind == "definition" then definitionCount := definitionCount + 1
          else if kind == "opaque" then opaqueCount := opaqueCount + 1
          else otherCount := otherCount + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {mod} {kind} {name} : {axl}"
          logInfo m!"SAFE_CONSTANT {mod} {kind} {name} : {axl}"
  logInfo m!"FULL_SAFE_AUDIT safe={safeCount} theorem={theoremCount} definition={definitionCount} opaque={opaqueCount} other={otherCount} unsafe={unsafeCount} partial={partialCount} union={union}"
''')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--decimal-sha256", required=True,
                        help="The parent's final approved frozen Decimal source hash")
    parser.add_argument("--canonical", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{64}", args.decimal_sha256):
        raise ValueError("The approved Decimal hash must be a full SHA-256")
    repository = args.repository.resolve(strict=True)
    lean = args.lean.resolve(strict=True)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    logs = output / "logs"
    logs.mkdir()
    stage = output / "source"
    stage.mkdir()
    registry_path = repository / "proofs/Agent14Spectral.registry.json"
    verifier = repository / "proofs/verify_project__214bf7673efe116b.py"
    report = {
        "executed_by": "Agent #14 / runtime specialist",
        "status": "RUNNING",
        "started_at": now(),
        "source_authorship": "Independent verification only; no P196 proof authored",
        "execution_mode": "Approved require_escalated; no runtime adapter",
        "repository_wide_pass": False,
        "author_project_objects_reused": False,
        "independent_lean_flags": ["--trust=0", "-j1", "-DElab.async=false"],
        "approved_decimal_sha256": args.decimal_sha256,
        "commands": [],
        "sources": {},
        "runner_sha256": file_digest(Path(__file__).resolve()),
    }

    def save():
        (output / "verification.json").write_text(json.dumps(report, indent=2) + "\n")

    environment = {"PATH": str(lean.parent) + os.pathsep + os.defpath,
                   "LANG": "C.UTF-8", "LEAN_PATH": str(stage)}

    def run(label, command, cwd):
        log = logs / (label + ".log")
        started_at = now()
        start = time.monotonic()
        timeout_seconds = 2400 if label == "canonical-verifier" else 1800
        with log.open("xb") as stream:
            process = subprocess.Popen(command, cwd=cwd, env=environment,
                                       stdout=stream, stderr=subprocess.STDOUT,
                                       start_new_session=True)
            try:
                code = process.wait(timeout=timeout_seconds)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=5)
                code = 124
        record = {"label": label, "argv": command, "cwd": str(cwd),
                  "started_at": started_at, "finished_at": now(),
                  "elapsed_seconds": round(time.monotonic() - start, 6),
                  "timeout_seconds": timeout_seconds,
                  "exit_code": code, "log": str(log.relative_to(output)),
                  "log_sha256": file_digest(log)}
        report["commands"].append(record)
        save()
        print(label, "exit=" + str(code), flush=True)
        if code != 0:
            raise RuntimeError("Command failed: " + label)
        return log.read_text()

    try:
        report["source_commit_before"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repository, text=True).strip()
        report["source_tree_clean_at_start"] = not subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=no"], cwd=repository)
        registry_bytes = registry_path.read_bytes()
        (output / "registry.snapshot.json").write_bytes(registry_bytes)
        registry = json.loads(registry_bytes)
        report["registry_sha256"] = digest(registry_bytes)
        if registry["schema_version"] != 1 or set(registry["toolchain"]["allowed_axioms"]) != ALLOWED:
            raise ValueError("Unexpected registry schema or axiom policy")
        if registry["toolchain"]["version"] != "4.19.0" or registry["toolchain"]["commit"] != "6caaee842e94":
            raise ValueError("Unexpected toolchain pin")
        project = registry["projects"][PROJECT]
        records = project["modules"]
        frozen = dict(FIXED_PINS, Agent14SpectralDecimal=args.decimal_sha256)
        if set(records) != set(frozen) or project["roots"] != ["Agent14SpectralDecimal"]:
            raise ValueError("The registry does not contain the assigned exact closure")
        report["scope"] = project["scope"]
        originals = {}
        imports = {}
        public = []
        for module, rec in records.items():
            if not IDENTIFIER.fullmatch(module):
                raise ValueError("Invalid module name")
            path = (repository / rec["path"]).resolve(strict=True)
            if not path.is_relative_to(repository):
                raise ValueError("Registered source escapes the repository")
            data = path.read_bytes()
            sha = digest(data)
            blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
            if sha != rec["sha256"] or sha != frozen[module] or blob != rec["git_blob"]:
                raise ValueError("Source pin mismatch: " + module)
            code = masked_source(data.decode())
            if FORBIDDEN.search(code):
                raise ValueError("Forbidden source token: " + module)
            deps = [item for line in re.findall(r"^\s*import\s+([^\n]+)", code, re.M)
                    for item in line.split()]
            if deps != rec["imports"] or any(dep not in records and dep not in {"Std", "Lean", "Init"} for dep in deps):
                raise ValueError("Unexpected import closure: " + module)
            originals[module] = data
            imports[module] = deps
            report["sources"][module] = {"path": rec["path"], "sha256": sha,
                                          "git_blob": blob, "bytes": len(data), "imports": deps}
            if module.startswith("Agent14"):
                public.extend(declared_public_names(module, code))
        endpoints = [name for claim in registry["claims"] if claim["project"] == PROJECT
                     for name in claim.get("endpoints", [])]
        if len(endpoints) != len(set(endpoints)) or not set(endpoints) <= {item["name"] for item in public}:
            raise ValueError("Endpoint coverage is incomplete or duplicated")
        report["public_declarations"] = public
        report["claim_endpoints"] = endpoints
        order = []
        visited = set()
        active = set()

        def visit(module):
            if module in visited or module not in records:
                return
            if module in active:
                raise ValueError("Import cycle")
            active.add(module)
            for dep in imports[module]:
                visit(dep)
            active.remove(module)
            visited.add(module)
            order.append(module)

        for module in project["roots"]:
            visit(module)
        if visited != set(records):
            raise ValueError("Registry has modules outside the selected closure")
        report["build_order"] = order
        version = run("lean-version", [str(lean), "--version"], output).strip()
        if version != "Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)":
            raise ValueError("Unexpected Lean version")
        prefix = Path(run("lean-prefix", [str(lean), "--print-prefix"], output).strip()).resolve()
        runtime_files = [lean, *sorted((prefix / "lib/lean").glob("*.so"))]
        runtime_pins = {str(path): file_digest(path) for path in runtime_files}
        report["runtime"] = {"lean": str(lean), "prefix": str(prefix), "version": version,
                             "files": runtime_pins,
                             "provenance": "Reuses the independently byte-verified official Lean 4.19.0 distribution; no new toolchain extraction"}
        if runtime_pins[str(lean)] != "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023":
            raise ValueError("Lean executable differs from the verified official runtime")
        if args.canonical:
            if file_digest(verifier) != VERIFIER_SHA256:
                raise ValueError("Canonical verifier changed")
            canonical = output / "canonical"
            command = [sys.executable, "-B", str(verifier), "--registry", str(output / "registry.snapshot.json"),
                       "--project", PROJECT, "--lean", str(lean), "--output", str(canonical)]
            run("canonical-verifier", command, repository)
            canonical_report = json.loads((canonical / "verification.json").read_text())
            if canonical_report["status"] != "PASS":
                raise ValueError("Canonical replay did not report scoped PASS")
            report["canonical"] = {"status": "PASS", "verifier_sha256": VERIFIER_SHA256,
                                   "verifier_unmodified": True, "trust_zero_flag": False,
                                   "report": "canonical/verification.json",
                                   "legacy_agent_field": "Agent #1 is retained from the unchanged canonical verifier; actual executor is Agent #14/runtime"}
            canonical_manifest = json.loads((canonical / "FILES.json").read_text())
            for name, rec in canonical_manifest.items():
                if file_digest(canonical / name) != rec["sha256"]:
                    raise ValueError("Canonical evidence changed before object cleanup")
            removed = []
            for path in sorted(canonical.rglob("*")):
                if path.is_file() and not path.is_symlink() and path.suffix in {".olean", ".ilean", ".o"}:
                    removed.append({"path": str(path.relative_to(output)), "bytes": path.stat().st_size,
                                    "sha256": file_digest(path)})
            (output / "canonical-object-cleanup.json").write_text(json.dumps(removed, indent=2) + "\n")
            for rec in removed:
                (output / rec["path"]).unlink()
            report["canonical"]["objects_removed_after_evidence_preservation"] = len(removed)
            save()
        for module in order:
            (stage / (module + ".lean")).write_bytes(originals[module])
        report["fresh_object_count_before_independent_build"] = len(list(stage.glob("*.olean")))
        if report["fresh_object_count_before_independent_build"]:
            raise ValueError("Independent build directory contains cached objects")
        flags = [str(lean), "--trust=0", "-j1", "-DElab.async=false"]
        for module in order:
            run("build-" + module, flags + ["-o", module + ".olean", module + ".lean"], stage)
        audit = stage / "SafeConstantAudit.lean"
        audit.write_text(safe_audit_source(order, project["roots"]))
        audit_log = run("safe-constant-audit", flags + [audit.name], stage)
        constants, audit_summary, unsafe, partial = parse_safe_audit(audit_log)
        public_names = [rec["name"] for rec in public]
        constants_by_name = {rec["name"]: rec for rec in constants}
        if not set(public_names) <= constants_by_name.keys():
            raise ValueError("A public source declaration is missing from the safe audit")
        for declaration in public:
            if constants_by_name[declaration["name"]]["module"] != declaration["module"]:
                raise ValueError("Public declaration has the wrong module origin")
        (output / "safe-constants.json").write_text(json.dumps(constants, indent=2) + "\n")
        (output / "implementation-inventory.json").write_text(json.dumps({"unsafe": unsafe, "partial": partial}, indent=2) + "\n")
        public_source = "\n".join("import " + module for module in project["roots"]) + "\n"
        public_source += "set_option pp.fullNames true\nset_option pp.universes true\nset_option pp.explicit true\n"
        for name in public_names:
            public_source += "#check @" + name + "\n#print axioms " + name + "\n"
        public_audit = stage / "PublicDeclarationAudit.lean"
        public_audit.write_text(public_source)
        public_log = run("public-types-and-axioms", flags + [public_audit.name], stage)
        axiom_records = parse_public_axioms(public_log, public_names)
        (output / "public-axioms.json").write_text(json.dumps(axiom_records, indent=2) + "\n")
        for module, rec in records.items():
            if (repository / rec["path"]).read_bytes() != originals[module]:
                raise ValueError("Original source changed during execution: " + module)
            if (stage / (module + ".lean")).read_bytes() != originals[module]:
                raise ValueError("Staged source changed during execution: " + module)
        if registry_path.read_bytes() != registry_bytes:
            raise ValueError("Registry changed during execution")
        if any(file_digest(Path(path)) != sha for path, sha in runtime_pins.items()):
            raise ValueError("Runtime identity changed during execution")
        report["safe_audit"] = audit_summary
        report["public_type_and_axiom_count"] = len(axiom_records)
        report["public_source_declaration_count"] = len(public_names)
        report["claim_endpoint_count"] = len(endpoints)
        report["objects"] = {path.name: {"bytes": path.stat().st_size, "sha256": file_digest(path)}
                             for path in sorted(stage.glob("*.olean"))}
        report["status"] = "INDEPENDENT_BUILD_AND_AXIOM_PASS"
        report["semantic_review"] = "Separate task; this report records execution and dependency audits"
        return 0
    except Exception as exc:
        report["status"] = "BLOCKED_DISK" if isinstance(exc, OSError) and exc.errno == 28 else "FAIL"
        report["error"] = repr(exc)
        report["traceback"] = traceback.format_exc()
        print(report["traceback"], flush=True)
        return 1
    finally:
        report["finished_at"] = now()
        try:
            save()
            files = {}
            for path in sorted(output.rglob("*")):
                if not path.is_file() or path.is_symlink() or path.suffix in {".olean", ".ilean", ".o", ".pyc"} or path == output / "FILES.json":
                    continue
                files[str(path.relative_to(output))] = {"bytes": path.stat().st_size, "sha256": file_digest(path)}
            (output / "FILES.json").write_text(json.dumps(files, indent=2) + "\n")
        except OSError as exc:
            print("Could not preserve all final evidence:", repr(exc), flush=True)
        print(json.dumps({key: report.get(key) for key in ["status", "error", "safe_audit", "public_type_and_axiom_count", "claim_endpoint_count"]}, indent=2), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
