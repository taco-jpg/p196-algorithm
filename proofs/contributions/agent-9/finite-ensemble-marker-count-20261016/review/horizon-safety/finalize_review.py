#!/usr/bin/env python3
"""Validate and preserve the completed independent ensemble gate; never run Lean.

All writes stay inside this review directory. The source scratch run is read
only. Generated objects and redundant build-source copies are recorded by hash
but are not included in the publication packet.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import traceback


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def utc(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, timezone.utc).isoformat()


def main() -> None:
    review = Path(__file__).resolve().parent
    contribution = review.parents[1]
    repo = contribution.parents[3]
    run = Path("/workspace/scratch/8dcaf4a67fa4/agent9-ensemble-review/full-001")
    freeze = json.loads((review / "author-snapshot/AUTHOR_FREEZE.json").read_text())
    registry_path = review / "verification/source-registry.json"
    registry = json.loads(registry_path.read_text())
    raw_report = (run / "verification.json").read_bytes()
    report = json.loads(raw_report)
    raw_audit = (run / "logs/EnsembleAudit.log").read_bytes()
    audit = raw_audit.decode()
    expected = [name for module in freeze["mathematical_modules"] for name in module["exports"]]
    printed = re.findall(r"^'([^']+)' (?:depends on axioms:|does not depend on any axioms)", audit, re.M)
    type_names = ["P196.Agent9.Ensemble." + name for name in re.findall(
        r"^P196\.Agent9\.Ensemble\.([A-Za-z_][\w]*)\b", audit, re.M)]
    assert report["status"] == "PASS_SELECTED_SOURCE_CLOSURE"
    assert printed == type_names == expected == registry["endpoints"]
    assert len(set(expected)) == 100
    assert report["precompile_object_count"] == 0 and report["lean_trust_level"] == 0
    assert report["output_directory_created_new"]
    assert report["all_selected_sources_unchanged"] and report["compiler_snapshot_unchanged"]
    assert report["manifest_sha256"] == sha(registry_path.read_bytes())
    assert report["workflow_sha256"] == sha((review / "verify.py").read_bytes())
    selected = set(registry["modules"])
    assert len(selected) == 16 and set(report["build_order"]) == selected
    compiled = [row for row in report["commands"] if row["label"] in selected]
    assert len(compiled) == 16 and {row["label"] for row in compiled} == selected
    for row in compiled + [row for row in report["commands"] if row["label"] == "EnsembleAudit"]:
        assert row["exit_code"] == 0
        assert all(flag in row["argv"] for flag in ["--trust=0", "-j1", "-DElab.async=false"])
    assert len([row for row in report["commands"] if row["label"] == "EnsembleAudit"]) == 1
    theorem_rows = re.findall(r"^AUDIT_THEOREM (\S+) (\S+) : (\[[^\]]*\])", audit, re.M)
    definition_rows = re.findall(r"^AUDIT_DEFINITION (\S+) (\S+) : (\[[^\]]*\])", audit, re.M)
    assert len(theorem_rows) == report["audited_theorem_count"] == 1505
    assert len(definition_rows) == report["audited_safe_definition_count"] == 239
    assert len(set(row[1] for row in theorem_rows)) == len(theorem_rows)
    assert len(set(row[1] for row in definition_rows)) == len(definition_rows)
    assert Counter(row[0] for row in theorem_rows) == Counter(report["theorems_by_module"])
    assert Counter(row[0] for row in definition_rows) == Counter(report["safe_definitions_by_module"])
    assert set(expected) <= {row[1] for row in theorem_rows + definition_rows}
    permitted = {"propext", "Classical.choice", "Quot.sound"}
    actual_union = set()
    for origin, name, dependencies in theorem_rows + definition_rows:
        assert origin in selected
        assert dependencies.startswith("[") and dependencies.endswith("]"), (name, dependencies)
        axiom_names = {name.strip() for name in dependencies[1:-1].split(",") if name.strip()}
        assert axiom_names <= permitted, (origin, name, dependencies)
        actual_union |= axiom_names
    assert actual_union == permitted
    origins = {row[0] for row in theorem_rows + definition_rows}
    assert selected - origins == set(freeze["permitted_empty_import"]) == {"Lychrel196Research"}
    spec = importlib.util.spec_from_file_location("independent_verifier", review / "verify.py")
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    adapter = registry["modules"]["Lychrel196Research"]
    assert verifier.code_only((repo / adapter["path"]).read_text()).strip() == "import LychrelDigitSums"
    new_hashes, literal_kinds = {}, Counter()
    for module in freeze["mathematical_modules"]:
        name = module["module"]
        data = (contribution / (name + ".lean")).read_bytes()
        assert sha(data) == module["sha256"]
        assert data == (review / "frozen-source" / (name + ".lean")).read_bytes()
        new_hashes[name] = sha(data)
        code = verifier.code_only(data.decode())
        literal_kinds.update(re.findall(r"^\s*(?:noncomputable\s+)?(def|theorem)\s+[A-Za-z_][\w]*\b", code, re.M))
    assert sum(literal_kinds.values()) == 100
    new_origin_theorems = sum(row[0] in new_hashes for row in theorem_rows)
    new_origin_definitions = sum(row[0] in new_hashes for row in definition_rows)
    assert new_origin_theorems == report["new_module_theorem_count"] == 183
    assert new_origin_definitions == report["new_module_safe_definition_count"] == 32

    subreview = review / "subreview"
    subreview.mkdir(exist_ok=False)
    child_command = '''python -c 'pairs = [(0,1),(9,9),(0,0)]; ds = []; exec("for a,b in reversed(pairs):\\n    ds = [a] + ds + [b]"); print({"r":2,"J":1,"q":0,"e":0,"digits_low_first":ds,"value":sum(d*10**i for i,d in enumerate(ds)),"selected_marker":all(ds[1+i] == 9 and ds[len(ds)-1-(1+i)] == 9 for i in range(2)),"word_count":90*(10**4-1)})' '''.rstrip()
    child_stdout = "{'r': 2, 'J': 1, 'q': 0, 'e': 0, 'digits_low_first': [0, 9, 0, 0, 9, 1], 'value': 190090, 'selected_marker': False, 'word_count': 899910}\n"
    (subreview / "arithmetic-command.txt").write_text(child_command + "\n")
    (subreview / "arithmetic-stdout.log").write_text(child_stdout)
    dump(subreview / "ATTRIBUTION.json", {
        "reviewer": "Agent #9/horizon-safety/ensemble_semantics",
        "delegated_by": "Agent #9/horizon-safety",
        "status": "READ_ONLY_SEMANTIC_PASS",
        "reviewed_modules": {name: new_hashes[name] for name in [
            "Agent9FiniteProducts", "Agent9MarkerWords", "Agent9MarkerEnumeration"]},
        "source_hashes_checked_start_and_end": True,
        "findings_relayed_from_completed_subagent": [
            "Fixed-length product, concatenation, and wrapping injectivity hypotheses are explicit.",
            "goodBlocks excludes exactly one entire all-nine r-block; no independent 99-choice restriction.",
            "mem_markerWords proves both directions for all canonical words of the specified width.",
            "Leading nonzero digit, zero units digit, odd center, J=0, and generic r=0 cases are coherent.",
            "No semantic defect or mathematical source edit was requested."
        ],
        "compiler_invocations": 0, "git_mutations": 0, "source_edits": 0,
        "arithmetic_evidence": {
            "cwd": str(repo), "exact_shell_command": child_command,
            "stdout": child_stdout, "exit_code": 0,
            "evidence_origin": "Existing tool result relayed by the completed subagent; not rerun by the main reviewer.",
            "limitation": "One specified digit list and a formula evaluation only. The word_count output is not an exhaustive ensemble cardinality."
        }
    })

    archive = review / "runs/full-001"
    archive.mkdir(parents=True, exist_ok=False)
    retention = {"scratch_run": str(run), "retained": {}, "omitted": {},
                 "policy": "Preserve raw commands, logs, reports, generated audit, and exact source refs. Exclude reproducible binary objects and redundant source copies; five new mathematical snapshots are retained in frozen-source/."}
    for path in sorted(run.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(run)
        data = path.read_bytes()
        identity = {"bytes": len(data), "sha256": sha(data)}
        reason, retained_as = None, None
        if relative.parts[0] == "build":
            reason = "Reproducible compiled object, not part of the compact evidence packet."
        elif relative.parts[0] == "source" and relative.name != "EnsembleAudit.lean":
            module = relative.stem
            reason = "Redundant build-source copy; exact original pin and raw original-source command output are retained."
            if module in new_hashes:
                reason = "Redundant new-source copy; byte-identical frozen author snapshot retained."
                retained_as = "frozen-source/" + relative.name
            elif module in registry["modules"]:
                retained_as = registry["modules"][module]["path"]
        if reason:
            retention["omitted"][str(relative)] = {**identity, "reason": reason, "retained_as": retained_as}
            continue
        destination = archive / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        assert destination.read_bytes() == data
        retention["retained"][str(relative)] = identity
    dump(archive / "RETENTION.json", retention)
    (archive / "RETENTION.md").write_text(
        "# Compact raw-run archive\n\n"
        "verification.json, source-manifest.json, FILES.json, every command log, and source/EnsembleAudit.lean are unchanged copies of the independent scratch run. "
        "FILES.json is the original scratch-run inventory and intentionally also lists omitted files. "
        "RETENTION.json records every included and omitted original path, size, and SHA256. "
        "The omitted files are only reproducible build objects and redundant source copies. "
        "The five new mathematical sources remain in ../../frozen-source/. "
        "Original sources are pinned by historical commit/path/blob/SHA256 and their actual Git source-read logs remain included. "
        "The review-root REVIEW_FILES.json and SHA256SUMS describe the delivered packet. No scratch file was deleted or altered by this archiver.\n")

    origins_table = []
    for name in report["build_order"]:
        origins_table.append({"module": name,
                              "theorems": report["theorems_by_module"].get(name, 0),
                              "safe_definitions": report["safe_definitions_by_module"].get(name, 0),
                              "literal_exports": len(next((m["exports"] for m in freeze["mathematical_modules"] if m["module"] == name), []))})
    dump(review / "verification/postcheck.json", {
        "status": "PASS", "literal_check_type_count": len(type_names),
        "literal_print_axioms_count": len(printed), "exact_frozen_endpoint_order": True,
        "all_literal_exports_in_origin_audit": True, "per_origin": origins_table,
        "only_empty_origin": ["Lychrel196Research"],
        "empty_origin_source_is_original_import_only_adapter": True,
        "all_collected_axiom_lists_independently_parsed": True,
        "axiom_union": sorted(actual_union), "literal_declarations": dict(literal_kinds),
        "raw_audit_sha256": sha(raw_audit),
        "author_mathematical_sources_still_match_freeze": new_hashes,
        "compiler_invocations_in_postcheck": 0
    })
    result = {
        "status": "INDEPENDENT_SEMANTIC_AND_KERNEL_REVIEW_PASS",
        "reviewer": "Agent #9/horizon-safety", "mathematical_author": "Agent #9/coverage_census",
        "semantic_review": "SEMANTIC_REVIEW.md", "source_edits": 0, "git_mutations": 0,
        "full_independent_compiler_gates": 1, "failed_independent_compiler_gates": 0,
        "raw_verification_status": report["status"],
        "source_scope": "Complete 16-module project import closure; official standard Lean runtime is hashed, not source-rebuilt.",
        "compiled_mathematical_modules": len(compiled), "compiled_audits": 1,
        "literal_exports": len(expected), "literal_theorems": literal_kinds["theorem"],
        "literal_definitions": literal_kinds["def"],
        "audited_theorems": len(theorem_rows), "audited_safe_definitions": len(definition_rows),
        "new_origin_theorems": new_origin_theorems, "new_origin_safe_definitions": new_origin_definitions,
        "declaration_bearing_origins": len(origins), "zero_declaration_origins": ["Lychrel196Research"],
        "axiom_union": sorted(actual_union), "all_100_literal_exports_checked_and_printed": True,
        "unsafe_compiler_implementation_axioms_reported": len(report["unsafe_implementation_constants"]),
        "unsafe_compiler_implementation_definitions_reported": len(report["unsafe_implementation_definitions"]),
        "lean_version": report["compiler"]["version"], "lean_trust": 0,
        "precompile_object_count": 0, "source_snapshot_unchanged": True, "runtime_snapshot_unchanged": True,
        "started_utc": utc(report["started_epoch"]), "finished_utc": utc(report["finished_epoch"]),
        "elapsed_seconds": round(report["finished_epoch"] - report["started_epoch"], 6),
        "mathematical_source_sha256": new_hashes,
        "source_registry_sha256": sha(registry_path.read_bytes()),
        "checker_sha256": sha((review / "verify.py").read_bytes()),
        "checker_origin": {
            "path": "proofs/contributions/agent-9/one-step-digit-sum-collapse-20261016/verify.py",
            "sha256": "736235311dd16d5430e44233b9b703712273c1e0b267234071abedba4f0617d8",
            "adaptations": "Generated audit module renamed to EnsembleAudit; default reviewer identity changed."
        },
        "generated_audit_source_sha256": report["audit_source_sha256"],
        "raw_audit_log_sha256": sha(raw_audit), "raw_verification_sha256": sha(raw_report),
        "author_freeze_sha256": sha((review / "author-snapshot/AUTHOR_FREEZE.json").read_bytes()),
        "prior_failure": {
            "kind": "Read-only Git object availability lookup, not a Lean failure",
            "evidence": "preparation-001/", "resolved_by": "Parent fetched the published checkpoint; reviewer performed no Git mutation.",
            "resolved_verification": "preparation-002/"
        },
        "packaging_history": {
            "first_packaging_attempt": "packaging-history/attempt-001/",
            "first_packaging_status": "Failed report parser on a wrapped axiom list; compiler gate unaffected.",
            "resolution": "Parse the complete bracketed axiom list across line breaks and trim each name. All 1744 theorem/safe-definition lists are checked.",
            "successful_attempt": 2, "compiler_invocations_during_packaging": 0,
            "unexecuted_draft": "packaging-history/unexecuted-finalizer-draft-001.py.txt"
        },
        "supplementary_subreview": "subreview/ATTRIBUTION.json",
        "author_gate_independence": "The author's gate and controls are separately attributed. No author objects, author audit result, or finite controls were used to establish this independent PASS.",
        "acceptance": "Exact complete canonical marker-complement count and the direct positive-time 1..R+1 early-hit upper bound under the contract; no semantic correction requested.",
        "finalization_invocation": [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]],
        "finalization_script_sha256": sha(Path(__file__).read_bytes())
    }
    dump(review / "RESULT.json", result)
    lines = [
        "# Independent ensemble review", "", "**PASS: semantic review and one fresh complete Lean kernel gate.**", "",
        "Agent #9/horizon-safety reviewed the five frozen modules authored by Agent #9/coverage_census. All 16 project modules and the generated audit compiled with official Lean 4.19.0 at --trust=0 -j1 -DElab.async=false. The audit checked 100 literal exports, 1,505 theorem constants, and 239 safe definitions. The exact permitted axiom union is propext, Classical.choice, and Quot.sound. No mathematical source change was made.", "",
        "The result covers every canonical width-L integer with no selected mirrored all-nine block, including trailing zero digits, and yields the finite palindrome-hit count upper bound at positive times 1 through R+1. The semantic review explains the exact formula, full numeric completeness, all requested boundaries, and original-result attribution.", "",
        "## Evidence", "",
        "- SEMANTIC_REVIEW.md: complete independent semantic assessment.",
        "- RESULT.json: exact final outcome, counts, source hashes, runtime, attribution, and scope.",
        "- frozen-source/: unchanged snapshots of the five mathematical modules.",
        "- author-snapshot/: author freeze, source statement, pins, audit, and separately attributed author gate metadata.",
        "- verification/source-registry.json and verify.py: independent source registry and replay driver.",
        "- verification/postcheck.json: exact public-export and origin-audit validation.",
        "- runs/full-001/: unchanged raw gate reports, all logs, generated audit, and explicit retention inventory.",
        "- preparation-001/: preserved failed checkpoint lookup before the commit was locally available.",
        "- preparation-002/: successful checkpoint and original-source provenance verification after parent fetched it.",
        "- subreview/: attributed product/word review and the single-example arithmetic command; not a full enumeration.",
        "- packaging-history/: preserved unexecuted draft and the actual packaging-parser failure on a multiline axiom list; no failed Lean gate or mathematical source change.",
        "- REVIEW_FILES.json and SHA256SUMS: inventory of this delivered review packet.", "",
        "## Compiled origin counts", "", "| Module | Theorems | Safe definitions | Literal new exports |", "| --- | ---: | ---: | ---: |"
    ]
    for item in origins_table:
        lines.append(f"| {item['module']} | {item['theorems']} | {item['safe_definitions']} | {item['literal_exports']} |")
    lines += ["", "Lychrel196Research is the exact original import-only adapter; it was freshly compiled and is the only origin with no declarations. Generated/private declarations are included in the theorem and safe-definition totals. Unsafe compiler implementation declarations are separately logged and are not mathematical proof axioms.", "",
              "## Replay", "", "Use a new output directory; the driver intentionally refuses to reuse an existing build tree. Set the repository and review paths to their local locations, then run:", "", "```bash",
              'python3 -B "$REVIEW_PATH"/verify.py ' + chr(92),
              '  --repo "$REPOSITORY_PATH" ' + chr(92),
              '  --package-root "$REVIEW_PATH" ' + chr(92),
              '  --manifest "$REVIEW_PATH"/verification/source-registry.json ' + chr(92),
              '  --lean /tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean ' + chr(92),
              '  --output /workspace/scratch/8dcaf4a67fa4/agent9-ensemble-review/replay-NEW ' + chr(92),
              "  --auditor 'Actual replay reviewer identity'", "```", "",
              "The actual executed command, environment, per-command exit status, elapsed time, and log hash are in runs/full-001/verification.json. The standard Lean runtime is hashed rather than rebuilt from source. This PASS is for the selected project closure, not the entire repository.", ""]
    (review / "README.md").write_text("\n".join(lines))
    included = {}
    for path in sorted(review.rglob("*")):
        if path.is_file() and path.name not in {"REVIEW_FILES.json", "SHA256SUMS"}:
            data = path.read_bytes()
            included[str(path.relative_to(review))] = {"bytes": len(data), "sha256": sha(data)}
    dump(review / "REVIEW_FILES.json", {"reviewer": "Agent #9/horizon-safety", "files": included,
                                       "file_count_excluding_two_manifest_files": len(included),
                                       "bytes_excluding_two_manifest_files": sum(row["bytes"] for row in included.values())})
    sums = []
    for path in sorted(review.rglob("*")):
        if path.is_file() and path.name != "SHA256SUMS":
            sums.append(sha(path.read_bytes()) + "  " + str(path.relative_to(review)))
    (review / "SHA256SUMS").write_text("\n".join(sums) + "\n")
    print(json.dumps({"status": result["status"], "files": len(included) + 2,
                      "review_manifest_sha256": sha((review / "REVIEW_FILES.json").read_bytes()),
                      "sha256sums_sha256": sha((review / "SHA256SUMS").read_bytes()),
                      "result_sha256": sha((review / "RESULT.json").read_bytes()),
                      "raw_verification_sha256": sha(raw_report)}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        here = Path(__file__).resolve().parent
        (here / "finalization-failure.txt").write_text(traceback.format_exc())
        raise
