#!/usr/bin/env python3
"""Reconcile Agent104's additive publication indexes without running Lean.

Reads the immutable merged-candidate inventory, preserves its mixed TSV rows,
retains replaced historical bytes when necessary, indexes tracked concurrent
files without promoting their mathematics, and checks final release bytes.
Writes only the explicitly assigned shared records and this directory.
No Git mutation is performed. The final evidence flag is explicit.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REPO = ROOT.parent
REL = "contributions/agent-104/seven-column-kernel/release-integration"
KERNEL = "contributions/agent-104/seven-column-kernel"
SECONDARY = "contributions/agent-104/review-agent4-whole-word"
BASE = "4bdd59bdc8f3e8f0556c3decb0898e6c6f271b29"
INDEX_BASE = "7216a20efaeb08daebbd3a8556ee609e042bf598"
MAIN = "5bd98567b259659fd3195f5aa61617422aa80914"
SOURCE = "957efa326b4b980391046598a0143cb7a7060242"
CLAIM = "8bfcfe69fe240be33fb2ae0e08b289c9bfffb53b"
SNAPSHOT = "agent104-reviewed-739-and-bridge-integration-20261015"
COORD_PATH = "coordination/agent104-739-integrated.json"
SHARED = {"README.md", "FINDINGS.md", "REPRODUCE.md", "REPORTS.md", "PUBLICATION_SCOPE.md",
          "INVENTORY.json", "INVENTORY.tsv", "FILES.md", "MANIFEST.sha256", "release_stats.json", "VALIDATION.json"}
BEGIN = "<!-- BEGIN AGENT104 REVIEWED INTEGRATION -->"
END = "<!-- END AGENT104 REVIEWED INTEGRATION -->"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(path):
    return sha(path.read_bytes())


def put(name, obj):
    (ROOT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def source_bytes(path):
    return git("show", INDEX_BASE + ":proofs/" + path)


def scoped_block(path, text):
    old = (ROOT / path).read_text()
    block = BEGIN + "\n" + text.strip() + "\n" + END
    if BEGIN in old:
        assert old.count(BEGIN) == old.count(END) == 1
        new = old[:old.index(BEGIN)] + block + old[old.index(END) + len(END):]
    else:
        new = old.rstrip() + "\n\n" + block + "\n"
    (ROOT / path).write_text(new)


def report_state(confirmed):
    clean = ROOT / KERNEL / "review-final-clean/independent-verification.json"
    accepted = ROOT / KERNEL / "review-final/acceptance.json"
    c, a = json.loads(clean.read_text()), json.loads(accepted.read_text())
    assert c["status"] == "PASS" and c["source_commit"] == SOURCE
    assert a["status"] == "ACCEPTED_FOR_STATED_739_SCOPE"
    pins = json.loads((ROOT / KERNEL / "integration/module-pins.json").read_text())
    original = json.loads((ROOT / KERNEL / "review-final-clean/verification.json").read_text())
    assert len(pins) == 383
    for module, rec in original["sources"].items():
        assert digest(REPO / rec["original_path"]) == pins[module]
    state = {"status": "PENDING", "source_commit": BASE,
             "scope": "Fresh 383-module merged-source execution; independent review required before PASS"}
    if confirmed:
        folder = ROOT / KERNEL / "integration-verified"
        merged = json.loads((folder / "independent-verification.json").read_text())
        raw = json.loads((folder / "verification.json").read_text())
        assert merged["status"] == "PASS" and raw["status"] == "PASS"
        assert merged["checker_exit_code"] == 0
        assert merged["prior_contribution_objects_reused"] is False
        assert merged["all_sources_objects_logs_and_compiler_pins_rechecked_after_completion"] is True
        assert merged["source_commit"] == raw["source_commit"] == BASE
        assert merged["fresh_source_module_count"] == 383 and merged["audited_theorem_count"] == 7469
        assert merged["checker_report_sha256"] == digest(folder / "verification.json")
        assert json.loads((folder / "source-pins.json").read_text()) == pins
        manifest = json.loads((folder / "final-evidence-manifest.json").read_text())
        for name, record in manifest["files"].items():
            b = (folder / name).read_bytes()
            assert len(b) == record["bytes"] and sha(b) == record["sha256"], name
        actual_files = {str(path.relative_to(folder)) for path in folder.rglob("*") if path.is_file()}
        assert actual_files == set(manifest["files"]) | {"final-evidence-manifest.json"}
        state = {"status": "PASS", "source_commit": BASE,
                 "fresh_source_modules": 383, "audited_theorem_constants": 7469,
                 "raw_report": KERNEL + "/integration-verified/verification.json",
                 "raw_report_sha256": digest(folder / "verification.json"),
                 "independent_report": KERNEL + "/integration-verified/independent-verification.json",
                 "independent_report_sha256": digest(folder / "independent-verification.json"),
                 "scope": "Independent fresh execution on the published merged candidate; source pins still match current checkout"}
    return state, c, a


def docs(state):
    status = ("The independent fresh merged-source verification is **PASS** for the published candidate "
              f"`{BASE}`; the current 383 accepted source pins remain identical." if state["status"] == "PASS" else
              "The contribution is independently reviewed; fresh merged-source verification is **PENDING**. "
              "The integration candidate is not yet labeled a completed main acceptance.")
    scoped_block("README.md", f"""
## Agent 104: reviewed 739-prefix formalization

The [complete 739-prefix Lean theorem]({KERNEL}/README.md) proves that for every
positive ordinary decimal seed A, if orbit A t is a palindrome whose canonical
numeral begins 739, then t ≤ 39. Consequently the orbit of 196 never belongs to
that restricted palindrome family. The final endpoints have no finite-certificate
premises or digit-width bound. This supplies no P196 proof or optimality claim
for 39 and does not formalize the earlier 217/218/620/777 bounds.

The contribution's independent source rebuild checked 383 modules and all 7,469
theorem constants; each transitive axiom set is contained in `propext`,
`Classical.choice`, and `Quot.sound`. A separate reviewer recompiled the exact
endpoint types using explicitly pinned fresh dependencies. {status}
See the [current integration record]({COORD_PATH}) and
[retained acceptance evidence]({KERNEL}/integration/ACCEPTANCE_ADDENDUM.md).
This named update supersedes only the 739 formalization status in the earlier
written/Python seven-column checkpoint; the historical text remains intact.

Agent 104's [separate review of Agent 4's actual-return bridge]({SECONDARY}/README.md)
also retains its semantic review, fresh five-module execution and exact scope
illustrations. The reviewed divisibility-by-eight conclusion requires both an
actual three-column return and the explicit saturated-width-growth equation.
It supplies no such return or growth condition for 196. That review is distinct
from the new 739 merged-source run and does not upgrade other concurrent results.
""")
    scoped_block("FINDINGS.md", f"""
## Agent 104: exact 739 Lean endpoints and separate bridge review

{status}

| Result | Exact scope | Evidence |
|---|---|---|
| 739-prefix palindrome ancestry | Every positive ordinary decimal seed A: if orbit A t is a palindrome beginning 739, then t ≤ 39. No width bound or finite-check premise remains. Attainment and optimality are not asserted. | [Exact theorem types and pins]({KERNEL}/integration/HANDOFF.md), [completed independent acceptance]({KERNEL}/review-final/acceptance.json) |
| Restricted-family avoidance by 196 | At every time t, orbit 196 is not a palindrome beginning 739. This does not settle P196. | `SevenColumnKernel.Finite739.no_196_739_palindrome`; same evidence |
| Terminal pair-sum obstruction | Positive-time admissible pair-word states of width at least three avoid leading pair sums [1,9,6]. These are pair sums, not the decimal digits of 196. | [TerminalObstruction.lean]({KERNEL}/TerminalObstruction.lean); same complete source rebuild |
| Independent review of Agent 4's whole-word bridge | The six `P196.Agent4.WholeWord` exports at source `4ffba5a60b6089075f6e3e4ab5952eb6bc46a4d7` passed semantic review and a five-module fresh build. Their actual-return-time divisibility conclusion retains the saturated-width-growth hypothesis. | [Review acceptance]({SECONDARY}/execution/acceptance.json), [semantic scope]({SECONDARY}/semantic/SEMANTIC_REVIEW.md) |

The 7,469 theorem constants are audit coverage, not a count of independent
results. The earlier seven-column written/Python record remains historical;
only its 739 formalization status is superseded. Concurrent files appear in
the byte inventory without acquiring a new mathematical acceptance label.
""")
    scoped_block("REPRODUCE.md", f"""
## Agent 104: complete 739-prefix Lean theorem

From the repository root, use an absolute official Lean 4.19.0 executable
(release commit `6caaee842e94`) and a nonexistent evidence directory:

```sh
python3 -B proofs/{KERNEL}/check.py "$LEAN_BIN" \\
  --evidence "$AGENT104_EVIDENCE" \\
  --pins proofs/{KERNEL}/integration/module-pins.json \\
  --module Conclusion739 --module TerminalObstruction \\
  --jobs 2 --require-committed
```

Both roots are explicit: the runner's structural defaults do not select the
nested concrete `Conclusion739` aggregate. This rebuilds 383 local source
modules and audits all compiled theorem constants, including private/generated
ones. Allowed transitive theorem axioms are `propext`, `Classical.choice`, and
`Quot.sound`. Each compiler uses one worker and synchronous elaboration;
at most two modules compile concurrently. No memory cap is imposed.

{status} [Source/toolchain pins]({KERNEL}/integration/HANDOFF.md),
[independent clean execution]({KERNEL}/review-final-clean/README.md),
[separate exact endpoint review]({KERNEL}/review-final/endpoint/verification.json),
and [current integration state]({COORD_PATH}) distinguish those executions.
The earlier Python certificate command remains independent finite diagnostics;
its historical "not Lean-formalized" note is superseded only for the 739 family.

The [secondary bridge review]({SECONDARY}/execution/README.md) has separate
reproduction runners, exact source pins and explicit dependency reuse for the
scope illustrations. It is not part of the 383-module 739 build.

Byte indexes for the verified final snapshot can be recreated without a theorem build:

```sh
python3 -B proofs/{REL}/reconcile_release.py --merged-evidence-confirmed
python3 -B proofs/verify_release.py
```

The confirmed flag verifies actual frozen PASS reports and their complete
file set and hashes. Unconfirmed mode is only for pre-PASS preparation;
after a snapshot records PASS, omitting the flag exits before writing and
cannot downgrade its state. The release verifier checks bytes
and local source presence; it does not establish mathematical truth.
""")
    reports = sorted(str(path.relative_to(ROOT)) for path in (ROOT / "contributions/agent-104").rglob("*.md")
                     if path.is_file() and not any(s in path.parts for s in {"__pycache__", "snapshot"}))
    scoped_block("REPORTS.md", "## Agent 104: 739 formalization, integration and bridge review\n\n" +
                 "\n".join(f"- [{name}]({name})" for name in reports))
    scoped_block("PUBLICATION_SCOPE.md", f"""
## Agent 104: complete 739 formalization and separate bridge review

This additive snapshot retains every committed Agent 104 research source,
certificate, generator, successful and failed compiler attempt, historical
unsplit batch, independent semantic/arithmetic diagnostic, complete clean-build
and axiom-audit log, exact endpoint audit, and published secondary bridge-review
artifact. {status} Acceptance applies only to the precise stated results;
there is no P196, infinite-safe-orbit or optimality-of-39 claim.

Original source inventories and mixed six-/seven-field TSV history are preserved.
Any replaced indexed bytes are recovered exactly from Git into a separate
history path, rather than overwritten or silently relabeled. The
[reconciliation record]({REL}/index-reconciliation.json) identifies such cases.
Current tracked concurrent files are included for byte coverage without a new
mathematical review. Earlier publication statistics retain their historical scope.

Runtime installations, compiled `.olean`/`.ilean` and binary objects, Python
caches and duplicate dependency/build trees are excluded. Original sources,
source-recovery maps, complete substantive logs and object/compiler hashes are
retained. [Exact infrastructure references]({REL}/infrastructure-exclusions.json)
record known excluded snapshot/object paths and their evidence; no genuine
research output is intentionally omitted. Lossless compressed evidence has
stored and decoded hashes, sizes and recovery commands in the inventory.
The final file list and manifest cover only tracked proof paths plus explicitly
assigned release files and confirmed frozen merged evidence, not transient work.
""")


def historical_bytes(path, expected):
    for commit in git("rev-list", "--all", "--", "proofs/" + path).decode().splitlines():
        trial = subprocess.run(["git", "show", commit + ":proofs/" + path], cwd=REPO, capture_output=True)
        if trial.returncode == 0 and sha(trial.stdout) == expected:
            return commit, trial.stdout
    raise RuntimeError("Cannot recover historical inventory bytes: " + path)


def exclusions():
    output = []
    for subdir in ("review-final-clean", "integration-verified"):
        source = ROOT / KERNEL / subdir / "verification.json"
        if not source.exists():
            continue
        report = json.loads(source.read_text())
        for module, rec in report.get("sources", {}).items():
            output.append({"path": rec["snapshot"], "context": subdir, "sha256": rec["sha256"],
                "bytes": rec["bytes"], "reason": "Duplicate build snapshot source; exact committed original retained",
                "retained_original": rec["original_path"], "evidence": str(source.relative_to(ROOT))})
            if "object_sha256" in rec:
                output.append({"path": str(Path(rec["snapshot"]).with_suffix(".olean")), "context": subdir,
                    "sha256": rec["object_sha256"], "reason": "Reproducible compiled Lean object; source and substantive compile log retained",
                    "evidence": str(source.relative_to(ROOT))})
        for module, rec in report.get("imported_object_fingerprints", {}).items():
            if module not in report.get("sources", {}):
                output.append({"path": rec["path"], "sha256": rec["sha256"], "context": subdir,
                    "reason": "Pinned official Lean standard-library runtime object; no vendored runtime copy required",
                    "evidence": str(source.relative_to(ROOT))})
    put(REL + "/infrastructure-exclusions.json", {
        "scope": "Known independent 739 snapshot and object exclusions; metadata references, not missing research evidence",
        "records": output,
        "secondary_exact_exclusions": SECONDARY + "/execution/execution-exclusions.tsv",
        "additional_categories": {"__pycache__ and .pyc": "Regenerable Python bytecode, not research output",
            "compiler executable, shared libraries and wrapper binary": "Runtime installation; official archive and executable hashes, shim source and inspection logs retained",
            "duplicate earlier development build objects": "Original sources, failed attempts and substantive logs retained; compiler products are regenerable"}})


def selected_paths(confirmed):
    files = {p[7:] for p in git("ls-files", "proofs").decode().splitlines()}
    files.update(str(p.relative_to(ROOT)) for p in HERE.rglob("*") if p.is_file())
    files.add(COORD_PATH)
    if confirmed:
        folder = ROOT / KERNEL / "integration-verified"
        files.update(str(p.relative_to(ROOT)) for p in folder.rglob("*") if p.is_file())
    for name in files:
        assert (ROOT / name).is_file(), name
        assert "__pycache__" not in Path(name).parts and not name.endswith((".olean", ".ilean", ".pyc", ".so", ".o")), name
    return sorted(files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--merged-evidence-confirmed", action="store_true")
    args = parser.parse_args()
    existing_coord = ROOT / COORD_PATH
    if existing_coord.exists() and not args.merged_evidence_confirmed:
        existing_state = json.loads(existing_coord.read_text()).get("merged_source_verification", {})
        if existing_state.get("status") == "PASS":
            parser.error("This snapshot already records merged-source PASS. Reproduce it with --merged-evidence-confirmed; no files changed.")
    state, clean, accepted = report_state(args.merged_evidence_confirmed)
    contribution = git("rev-parse", "097e2bf").decode().strip()
    coord = {"agent": "Agent #104", "task": "agent104-seven-column-kernel",
        "integration_task": "agent104-integrate-739", "coordination_claim": CLAIM,
        "contribution_commit": contribution, "mathematical_source_commit": SOURCE,
        "latest_reconciled_main": MAIN, "published_merged_candidate": BASE,
        "accepted_import_roots": ["Conclusion739", "TerminalObstruction"],
        "independent_source_review": "ACCEPTED_FOR_STATED_739_SCOPE",
        "merged_source_verification": state,
        "endpoints": accepted["accepted_theorems"],
        "axiom_union": ["propext", "Classical.choice", "Quot.sound"],
        "secondary_review": {"task": "agent104-review-agent4-whole-word", "status": "INDEPENDENTLY-REVIEWED",
            "evidence": SECONDARY + "/execution/acceptance.json",
            "scope": "Actual return and saturated-width-growth hypotheses remain; no return or growth witness for196 supplied"},
        "publication_status": ("VERIFIED_CANDIDATE; final main commit and role disposition are recorded separately on coordination after actual main ref publication" if state["status"] == "PASS" else
                               "PREPARED; final main commit and role disposition are recorded on coordination after confirmed publication"),
        "scope": "739-prefix restricted palindrome family only, plus the separately reviewed Agent4 bridge; no P196 or optimality39 claim",
        "concurrent_byte_index_scope": "Other tracked contributions retained without new mathematical acceptance"}
    put(COORD_PATH, coord)
    docs(state)
    exclusions()
    baseline = json.loads(source_bytes("INVENTORY.json"))
    old_tsv = source_bytes("INVENTORY.tsv").decode()
    reconciliation = []
    rewritten_after_reconciliation = {REL + "/index-reconciliation.json", REL + "/release-integrity.log"}
    for record in baseline:
        if record["publication"] != "retained":
            continue
        path = record["published_path"]
        current = ROOT / path
        if path not in rewritten_after_reconciliation and current.exists() and current.stat().st_size == record["bytes"] and digest(current) == record["sha256"]:
            continue
        commit, data = historical_bytes(path, record["sha256"])
        archived = f"{REL}/historical-index/{record['sha256']}/{Path(path).name}"
        (ROOT / archived).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / archived).write_bytes(data)
        record.update({"published_path": archived, "superseded_published_path": path,
            "original_git_commit": commit,
            "reconciliation_note": "Exact indexed historical bytes retained; current source stays unchanged at its original path"})
        reconciliation.append({"original_path": path, "archive_path": archived, "sha256": sha(data), "bytes": len(data), "commit": commit})
        # Preserve historical six-field rows as historical provenance; update
        # only the seventh physical-path field when that field existed.
        lines = old_tsv.splitlines(keepends=True)
        for i, line in enumerate(lines):
            fields = line.rstrip("\n").split("\t")
            if len(fields) == 7 and fields[2] == record["sha256"] and fields[6] == path:
                fields[6] = archived
                lines[i] = "\t".join(fields) + "\n"
        old_tsv = "".join(lines)
    put(REL + "/index-reconciliation.json", {"baseline_commit": INDEX_BASE, "mathematical_build_candidate": BASE,
        "scope": "Physical byte provenance only; concurrent mathematics not re-reviewed",
        "historical_inventory_records_preserved": len(baseline),
        "historical_tsv_field_counts": dict(collections.Counter(str(len(line.split('\t'))) for line in old_tsv.splitlines())),
        "relocated_historical_records": reconciliation,
        "mixed_tsv_note": "Existing six-/seven-field row formats retained; only physical archive paths changed if necessary"})
    # History snapshots recovered above may themselves be written reports.
    docs(state)
    # Create the retained check record before file enumeration; final exact
    # counts stabilize through two or more byte-verification iterations.
    log = ROOT / REL / "release-integrity.log"
    log.write_text('{"status":"PENDING"}\n')
    stats_base = json.loads(source_bytes("release_stats.json"))
    validation_base = json.loads(source_bytes("VALIDATION.json"))
    previous_report = None
    for iteration in range(5):
        files = selected_paths(args.merged_evidence_confirmed)
        records = list(baseline)
        known = {r.get("published_path") for r in records if r["publication"] == "retained"}
        appended = []
        for name in files:
            if name in known or name in SHARED:
                continue
            data = (ROOT / name).read_bytes()
            own = name.startswith("contributions/agent-104/") or name == COORD_PATH
            record = {"source_path": name, "bytes": len(data), "sha256": sha(data), "publication": "retained",
                "reason": ("Agent104 source, complete research/development evidence, independent review, or scoped publication provenance" if own else
                           "Concurrent tracked proof file retained for exact byte coverage; no new mathematical acceptance by Agent104"),
                "family_report": KERNEL + "/README.md" if own and not name.startswith(SECONDARY) else
                                 SECONDARY + "/README.md" if own else "README.md",
                "published_path": name, "source_snapshot": SNAPSHOT,
                "semantic_status": "Use the source-specific acceptance record and exact hypotheses" if own else "BYTE_INDEX_ONLY_NO_NEW_MATHEMATICAL_REVIEW"}
            if own and name.endswith(".gz"):
                decoded = gzip.decompress(data)
                record.update({"original_path": name[:-3], "original_bytes": len(decoded), "original_sha256": sha(decoded),
                    "compression_format": "gzip", "compressed_bytes": len(data), "compressed_sha256": sha(data),
                    "recovery_command": f"gzip -dc proofs/{name} > /new/output/{Path(name[:-3]).name}"})
            records.append(record)
            appended.append(record)
        put("INVENTORY.json", records)
        columns = ("source_path", "bytes", "sha256", "publication", "reason", "family_report", "published_path")
        (ROOT / "INVENTORY.tsv").write_text(old_tsv.rstrip("\n") + "\n" +
            "".join("\t".join(str(r.get(k, "")) for k in columns) + "\n" for r in appended))
        (ROOT / "FILES.md").write_text("# Complete published file list\n\n"
            "Tracked proof paths and explicitly retained Agent104 integration evidence are listed below. "
            "Byte coverage does not imply mathematical acceptance; exact original-to-stored identities remain in INVENTORY.json.\n\n" +
            "".join(f"- [{name}]({name})\n" for name in files))
        own = [r for r in appended if r["published_path"].startswith("contributions/agent-104/") or r["published_path"] == COORD_PATH]
        concurrent = [r for r in appended if r not in own]
        stats = dict(stats_base)
        stats["agent104_739_integration_update"] = {"published_merged_candidate": BASE, "source_commit": SOURCE,
            "inventory_baseline": INDEX_BASE,
            "contribution_commit": contribution, "integration_parent": MAIN, "merged_source_verification_status": state["status"],
            "source_modules": 383, "audited_theorem_constants": 7469,
            "retained_agent104_files_added_to_inventory": len(own), "retained_agent104_bytes": sum(r["bytes"] for r in own),
            "concurrent_byte_only_records_added": len(concurrent), "concurrent_byte_only_bytes": sum(r["bytes"] for r in concurrent),
            "current_unique_published_files": len(files), "historical_records_preserved": len(baseline),
            "historical_records_relocated_without_changing_bytes": len(reconciliation),
            "existing_aggregate_fields_are_historical": True, "substantive_agent104_research_omissions": 0,
            "infrastructure_exclusions": REL + "/infrastructure-exclusions.json",
            "previous_prepared_checkpoint": stats_base.get("agent104_739_integration_update"),
            "counting_note": "New inventory records include previously unindexed existing tracked files; these are not all newly added Git files. Metadata and exact source copies in audit history are counted by physical path, without claiming independent results."}
        put("release_stats.json", stats)
        validation = dict(validation_base)
        validation["agent104_739_integration_update"] = {"source_commit": SOURCE, "published_merged_candidate": BASE,
            "inventory_baseline": INDEX_BASE,
            "independent_source_clean_build": "PASS", "independent_exact_endpoint_review": "PASS",
            "merged_source_verification": state, "unchanged_accepted_source_pins": 383,
            "secondary_bridge_review": "Separate fresh five-module review and semantic acceptance retained; not part of the383-module run",
            "axiom_union": ["propext", "Classical.choice", "Quot.sound"],
            "release_integrity": previous_report or {"status": "PENDING"},
            "release_integrity_record": REL + "/release-integrity.log", "mathematical_proof_check_by_release_verifier": False,
            "old_tsv_rows_preserved": len(old_tsv.splitlines()) - 1,
            "history_reconciliation": REL + "/index-reconciliation.json", "unrelated_math_reaudited": False,
            "previous_prepared_checkpoint": validation_base.get("agent104_739_integration_update")}
        put("VALIDATION.json", validation)
        (ROOT / "MANIFEST.sha256").write_text("".join(f"{digest(ROOT / name)}  {name}\n" for name in files if name != "MANIFEST.sha256"))
        proc = subprocess.run(["python3", "-B", str(ROOT / "verify_release.py")], cwd=REPO, capture_output=True, text=True)
        if proc.returncode:
            (HERE / "release-integrity-failure.log").write_text(proc.stdout + proc.stderr)
            raise RuntimeError(proc.stdout + proc.stderr)
        result = json.loads(proc.stdout)
        next_log = json.dumps({"command": "python3 -B proofs/verify_release.py", "exit_code": 0,
            "record_scope": "Final current manifest/inventory verification; no mathematical execution", "result": result}, indent=2) + "\n"
        if previous_report == result and log.read_text() == next_log:
            print(json.dumps({"status": "PASS", "merged_source_status": state["status"],
                "release_integrity": result, "retained_agent104_records": len(own), "concurrent_byte_records": len(concurrent),
                "historical_relocations": len(reconciliation), "iterations": iteration + 1}, indent=2))
            return
        previous_report = result
        log.write_text(next_log)
    raise RuntimeError("Release metadata failed to stabilize")


if __name__ == "__main__":
    main()
