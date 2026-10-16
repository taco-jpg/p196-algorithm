#!/usr/bin/env python3
"""Independently read back the completed 17-module run, without executing Lean."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def parse_raw_audit(text: str) -> tuple[dict, dict]:
    """Use a streaming block reader independent of the package's regex parser."""
    metadata, reports = {}, {}
    active, block = None, []
    for line in text.splitlines():
        if line.startswith("METADATA|"):
            require(active is None, "Metadata occurred inside an axiom report")
            parts = line.split("|")
            require(len(parts) == 6, "Malformed declaration metadata")
            _, module, name, kind, unsafe, partial = parts
            require(name not in metadata, "Repeated declaration origin")
            require(unsafe in ("true", "false") and partial in ("true", "false"), "Invalid origin flags")
            metadata[name] = {"module": module, "declaration": name, "kind": kind,
                              "unsafe": unsafe == "true", "partial": partial == "true"}
        elif line.startswith("AUDIT_BEGIN|"):
            require(active is None, "Nested axiom report")
            active, block = line.split("|", 1)[1], []
            require(active not in reports, "Repeated axiom report")
        elif line.startswith("AUDIT_END|"):
            require(active is not None and line.split("|", 1)[1] == active, "Axiom end marker mismatch")
            body = "\n".join(block).strip()
            empty = re.fullmatch(r"'([^']+)' does not depend on any axioms", body)
            nonempty = re.fullmatch(r"'([^']+)' depends on axioms: \[([^\]]*)\]", body, re.S)
            require((empty is None) != (nonempty is None), "Missing or extraneous report content")
            printed = (empty or nonempty).group(1)
            require(printed == active, "Printed declaration name differs from its actual origin")
            axioms = [] if empty else [item.strip() for item in nonempty.group(2).split(",") if item.strip()]
            reports[active] = {"printed_name": printed, "axioms": axioms}
            active, block = None, []
        elif active is not None:
            block.append(line)
        else:
            require(not any(tag in line for tag in ("METADATA|", "AUDIT_BEGIN|", "AUDIT_END|")),
                    "Unparsed audit marker")
    require(active is None, "Unclosed axiom report")
    return metadata, reports


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package", type=Path, required=True)
    ap.add_argument("--evidence", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    package, evidence, output = args.package.resolve(), args.evidence.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    receipt_bytes = (evidence / "verification.json").read_bytes()
    audit_bytes = (evidence / "axiom-audit.json").read_bytes()
    receipt, audit = json.loads(receipt_bytes), json.loads(audit_bytes)
    require(receipt["status"] == "PASS" and receipt["pass"], "Run did not finish successfully")
    package_pins = {
        "check.py": "f046586ae35fe9b0eb8fa3e3f43461cd6c8007243401b2e92d88c71ec6df6633",
        "source-pins.json": "8a7648eff9bb611e5605b2be83555bd7154971416f312be81cdf55505c8a7292",
        "REPRODUCE.md": "f1d1e29581fab92d356401cbc17ad3505600e9c327fe2afc417ce0fe2e6b625c",
    }
    require(receipt["package_sha256"] == package_pins, "Receipt package identity differs from reviewed candidate")
    for name, expected in package_pins.items():
        require(sha((evidence / "inputs" / name).read_bytes()) == expected, "Captured package bytes changed: " + name)
        require(sha((package / name).read_bytes()) == expected, "Current frozen package bytes changed: " + name)
    pins = json.loads((evidence / "inputs/source-pins.json").read_bytes())
    order = pins["build_order"]
    require(len(order) == len(set(order)) == 17, "Not the exact 17-module source closure")
    require(receipt["build_order"] == order, "Run build order differs from its pins")
    require(receipt["fresh_build_initially_empty"] and not receipt["project_olean_reuse"], "Project reuse/freshness disclosure changed")
    require(receipt["mathlib_and_toolchain_oleans_reused"], "External cache reuse was not disclosed")
    require(receipt["all_sources_unchanged_after"] and receipt["package_files_unchanged_after"] and
            receipt["mathlib_manifest_unchanged_after"], "Missing successful end checks")
    commands = receipt["commands"]
    require(len(commands) == 38, "Unexpected command count")
    require(all(step["exit_code"] == 0 for step in commands), "A recorded command did not succeed")
    by_label = {step["label"]: step for step in commands}
    require(len(by_label) == len(commands), "Repeated command label")
    compile_commands = [step for step in commands if step["label"].startswith("compile-")]
    require([step["label"][8:] for step in compile_commands] == order, "Compilation order or completeness differs")
    expected_lean = "Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)"
    require(receipt["lean"]["version_output"] == expected_lean, "Unexpected compiler release")
    require(sha(Path(receipt["lean"]["binary"]).read_bytes()) == receipt["lean"]["sha256"], "Compiler binary changed after execution")
    require((evidence / by_label["lean-version"]["stdout_log"]).read_text().strip() == expected_lean,
            "Raw compiler version does not match the receipt")
    mathlib_root = Path(receipt["mathlib"]["root"])
    expected_cache_rows = [
        {"package": row["name"], "library": str(mathlib_root / ".lake/packages" / row["name"] / ".lake/build/lib/lean"),
         "present": (mathlib_root / ".lake/packages" / row["name"] / ".lake/build/lib/lean").is_dir()}
        for row in pins["mathlib"]["dependencies"]]
    require(receipt["dependency_cache_directories"] == expected_cache_rows, "External library admission differs from the pinned package locations")
    expected_libs = [str(evidence / "build"), str(mathlib_root / ".lake/build/lib/lean")]
    expected_libs += [row["library"] for row in expected_cache_rows if row["present"]]
    require(receipt["lean_environment"]["LEAN_PATH"].split(":") == expected_libs,
            "LEAN_PATH includes an unexpected project or external library path")
    log_pins = {}
    for step in commands:
        for key in ("stdout_log", "stderr_log"):
            relative = Path(step[key])
            require(not relative.is_absolute() and ".." not in relative.parts, "Log path escapes evidence")
            data = (evidence / relative).read_bytes()
            log_pins[str(relative)] = sha(data)
    for step in [*compile_commands, by_label["audit-module-origins"]]:
        require(all(flag in step["argv"] for flag in ("--trust=0", "-j1", "-DElab.async=false")),
                "A project compiler/audit command lacks the reviewed kernel flags")
        require(step["cwd"] == str(evidence / "sources"), "Compiler did not use materialized sources")
        require(step["argv"][0] == receipt["lean"]["binary"], "Compiler binary changed across project commands")
    sources = {}
    repo = Path(receipt["repository_root"])
    for pin in pins["sources"]:
        module = pin["module"]
        data = (evidence / "sources" / (module + ".lean")).read_bytes()
        require(len(data) == pin["size_bytes"] and sha(data) == pin["sha256"], "Materialized source mismatch: " + module)
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(blob == pin["git_blob"], "Materialized Git blob mismatch: " + module)
        require((repo / pin["repo_path"]).read_bytes() == data, "Repository source differs from compiled source: " + module)
        sources[module] = {"sha256": sha(data), "git_blob": blob, "bytes": len(data)}
    objects = {}
    for obj in receipt["compiled_oleans"]:
        data = (evidence / "build" / (obj["module"] + ".olean")).read_bytes()
        require(sha(data) == obj["sha256"] and len(data) == obj["size_bytes"], "Compiled object changed: " + obj["module"])
        objects[obj["module"]] = {"sha256": sha(data), "bytes": len(data)}
    require(set(objects) == set(order), "Missing compiled project objects")
    mathlib_pins = {"mathlib": pins["mathlib"]["commit"],
                    **{row["name"]: row["rev"] for row in pins["mathlib"]["dependencies"]}}
    for name, expected in mathlib_pins.items():
        require((evidence / by_label[name + "-head"]["stdout_log"]).read_text().strip() == expected,
                "Raw dependency revision mismatch: " + name)
        require(not (evidence / by_label[name + "-tracked-status"]["stdout_log"]).read_text().strip(),
                "Raw dependency source status was not clean: " + name)
    require(sha((evidence / "inputs/mathlib-lake-manifest.json").read_bytes()) == pins["mathlib"]["lake_manifest_sha256"],
            "Captured Mathlib manifest differs from the pin")
    require(sha((evidence / "inputs/mathlib-lean-toolchain").read_bytes()) == pins["mathlib"]["lean_toolchain_sha256"],
            "Captured Mathlib toolchain differs from the pin")
    generated = (evidence / "sources/WindowPackageAxioms.lean").read_bytes()
    inspected = (package / "review/package-inspection/final-static-01/GeneratedAudit.lean").read_bytes()
    require(generated == inspected and sha(generated) == receipt["audit_source_sha256"],
            "Executed auditor source differs from the independently inspected generator output")
    raw = (evidence / by_label["audit-module-origins"]["stdout_log"]).read_bytes()
    metadata, reports = parse_raw_audit(raw.decode())
    require({row["module"] for row in metadata.values()} == set(order), "Raw audit lacks an exact selected module")
    safe = {name for name, row in metadata.items() if not row["unsafe"] and not row["partial"]}
    require(safe == set(reports), "Raw safe-origin and axiom-report sets differ")
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    require(all(set(row["axioms"]) <= allowed for row in reports.values()), "A raw report contains a disallowed logical axiom")
    json_metadata = {row["declaration"]: row for row in audit["origin_metadata"]}
    require(json_metadata == metadata and len(json_metadata) == len(audit["origin_metadata"]), "Audit JSON origin metadata differs from raw output")
    for row in audit["safe_axiom_reports"]:
        name = row["declaration"]
        require(row == {**metadata[name], **reports[name]}, "Audit JSON report differs from raw output: " + name)
    require(len(audit["safe_axiom_reports"]) == len(safe), "Audit JSON safe report count differs")
    correspondence = audit["source_correspondence"]
    require(len(correspondence) == 578, "Explicit source correspondence count differs")
    require(len({(row["module"], row["source_line"]) for row in correspondence}) == len(correspondence),
            "Explicit source correspondence is repeated")
    by_module = Counter()
    for row in correspondence:
        name, full = row["declaration"], row["source_name"]
        require(name in safe and metadata[name]["module"] == row["module"], "Source mapped to an unsafe/nonmatching origin")
        require(name == full or row["private"] and name.endswith("." + full), "Source name correspondence mismatch")
        require(row["axioms"] == reports[name]["axioms"], "Source correspondence axioms differ from raw report")
        by_module[row["module"]] += 1
    require(dict(by_module) == {row["module"]: row["explicit_declaration_count"] for row in pins["sources"]},
            "Per-source explicit declaration totals differ from the frozen inventory")
    union = sorted({axiom for row in reports.values() for axiom in row["axioms"]})
    counts = {"all_origins": len(metadata), "safe_nonpartial": len(safe),
              "unsafe": sum(row["unsafe"] for row in metadata.values()),
              "partial": sum(row["partial"] for row in metadata.values()),
              "unsafe_and_partial": sum(row["unsafe"] and row["partial"] for row in metadata.values()),
              "explicit_source": len(correspondence)}
    require((counts["all_origins"], counts["safe_nonpartial"], counts["explicit_source"]) == (2536, 1583, 578),
            "Measured raw full-run totals differ from the observed receipt")
    require(receipt_bytes == (evidence / "verification.json").read_bytes() and audit_bytes == (evidence / "axiom-audit.json").read_bytes(),
            "Evidence summary changed during independent readback")
    result = {"status": "INDEPENDENT_COMPLETED_RUN_READBACK_PASS", "pass": True,
              "reviewer": "Agent #108 runtime delegate, nonauthor of package checker and Incoming",
              "reviewer_started_new_lean_process": False, "reviewer_recompiled_project": False,
              "original_run_started_utc": receipt["started_utc"], "original_run_finished_utc": receipt["finished_utc"],
              "evidence_path": str(evidence), "receipt_sha256": sha(receipt_bytes), "audit_json_sha256": sha(audit_bytes),
              "raw_audit_sha256": sha(raw), "auditor_source_sha256": sha(generated),
              "package_sha256": package_pins, "commands_checked": len(commands),
              "project_compilations_checked": len(compile_commands), "audit_commands_checked": 1,
              "all_command_exit_codes_zero": True, "measured_origin_counts": counts,
              "measured_axiom_union": union, "unexpected_logical_axioms": [],
              "original_explicit_source_count": sum(by_module[name] for name in order[:7]),
              "new_explicit_source_count": sum(by_module[name] for name in order[7:]),
              "source_pins_rechecked": sources, "project_object_pins_rechecked": objects,
              "raw_command_log_sha256": log_pins,
              "external_cache_disclosure": receipt["cache_disclosure"],
              "scope": "Independent readback of the parent-run complete 17-project-source kernel build and full logical module-origin audit; not a rebuild of Lean or Mathlib."}
    (output / "readback-result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "commands_checked", "project_compilations_checked", "measured_origin_counts", "measured_axiom_union", "receipt_sha256", "audit_json_sha256", "raw_audit_sha256")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
