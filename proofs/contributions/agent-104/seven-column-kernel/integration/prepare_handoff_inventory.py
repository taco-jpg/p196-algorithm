#!/usr/bin/env python3
"""Read-only Git source comparison; writes only this handoff's inventory files.

No Lean invocation, working-tree source modification, or Git mutation occurs.
Pins intentionally remain fixed when origin/main or the contribution moves.
"""
from __future__ import annotations

import collections
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SOURCE = "957efa326b4b980391046598a0143cb7a7060242"
BASELINE = "95271b2bf55d18715f675d1e7f9d2a31ae1ec945"
MAIN = "4ffba5a60b6089075f6e3e4ab5952eb6bc46a4d7"
COORD = "7ed8bd96bbf711649a3e63d569a58c84ca23e5d2"
PREFIX = "proofs/contributions/agent-104/seven-column-kernel"
CORE = "proofs/research/continuation/LychrelDigitSums.lean"
ROOTS = ["Conclusion739", "TerminalObstruction"]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


def snapshot(commit, *paths):
    with tarfile.open(fileobj=io.BytesIO(git("archive", commit, *paths))) as archive:
        return {m.name: archive.extractfile(m).read() for m in archive if m.isfile()}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def write_json(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def write_tsv(name, columns, rows):
    with (HERE / name).open("w", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(columns)
        writer.writerows(rows)


def main():
    sources = snapshot(SOURCE, PREFIX, CORE)
    previous = snapshot(BASELINE, PREFIX, CORE)
    current_main = snapshot(MAIN, PREFIX, CORE)
    order, records = [], {}

    def visit(module):
        if module in records:
            return
        possibilities = [CORE] if module == "LychrelDigitSums" else [
            f"{PREFIX}/{module}.lean", f"{PREFIX}/certificate/{module}.lean"]
        path = next((p for p in possibilities if p in sources), None)
        if path is None:
            assert module in {"Std", "Lean"}, module
            return
        data = sources[path]
        imports = [m for line in re.findall(r"^import\s+([^\n]+)$", data.decode(), re.M)
                   for m in line.split()]
        for dependency in imports:
            visit(dependency)
        records[module] = {"path": path, "bytes": len(data), "sha256": sha(data),
                           "git_blob_sha1": blob(data), "imports": imports}
        order.append(module)

    for root in ROOTS:
        visit(root)
    assert len(records) == 383, len(records)
    assert records["LychrelDigitSums"]["sha256"] == "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57"
    write_json("module-pins.json", {m: r["sha256"] for m, r in records.items()})
    write_tsv("accepted-sources.tsv", ["module", "path", "bytes", "sha256", "git_blob_sha1"],
              [[m, r["path"], r["bytes"], r["sha256"], r["git_blob_sha1"]]
               for m, r in sorted(records.items())])

    active_paths = {r["path"] for r in records.values()}
    infrastructure = []
    retained = []
    compressed = []
    for path, data in sorted(sources.items()):
        if any(part in {"__pycache__", ".lake", "build", "fresh_build", "root_build"}
               for part in Path(path).parts) or path.endswith((".olean", ".ilean", ".pyc", ".so", ".o")):
            infrastructure.append(path)
            continue
        category = ("accepted_lean_source" if path in active_paths else
                    "retained_research_or_audit_source" if path.endswith((".lean", ".py", ".c", ".sh")) else
                    "report" if path.endswith(".md") else "research_evidence")
        retained.append([path, len(data), sha(data), blob(data), category])
        if path.endswith(".gz"):
            original = gzip.decompress(data)
            compressed.append({"stored_path": path, "stored_bytes": len(data),
                "stored_sha256": sha(data), "original_path": path[:-3],
                "original_bytes": len(original), "original_sha256": sha(original),
                "format": "gzip", "recovery_command": f"gzip -dc '{path}' > '/new/output/{Path(path[:-3]).name}'"})
    assert not infrastructure, infrastructure
    write_tsv("evidence-inventory.tsv", ["path", "bytes", "sha256", "git_blob_sha1", "category"], retained)

    delta = []
    conflicts = []
    for path in sorted(set(previous) | set(sources) | set(current_main)):
        old, new, remote = previous.get(path), sources.get(path), current_main.get(path)
        if old == new:
            continue
        kind = "added" if old is None else "deleted" if new is None else "modified"
        collision = remote != old and remote != new
        if collision:
            conflicts.append(path)
        delta.append([path, kind, sha(old) if old is not None else "",
                      sha(remote) if remote is not None else "", sha(new) if new is not None else "",
                      "conflict" if collision else "no_content_conflict_at_observed_main"])
    write_tsv("source-delta.tsv", ["path", "change", "pr18_sha256", "observed_main_sha256", "pr28_sha256", "three_way_status"], delta)

    shared_paths = ["proofs/README.md", "proofs/FINDINGS.md", "proofs/REPRODUCE.md",
        "proofs/REPORTS.md", "proofs/PUBLICATION_SCOPE.md", "proofs/INVENTORY.json",
        "proofs/INVENTORY.tsv", "proofs/FILES.md", "proofs/MANIFEST.sha256", "proofs/release_stats.json"]
    shared = {path: {"bytes": len(data), "sha256": sha(data), "git_blob_sha1": blob(data)}
              for path, data in snapshot(MAIN, *shared_paths).items()}
    write_json("handoff.json", {
        "task_id": "agent104-seven-column-kernel", "status": "PREPARED_PENDING_REVIEW_AND_SCOPED_INTEGRATION",
        "source_commit": SOURCE, "contribution_branch": "research/agent-104/20261015T0440",
        "followup_pull_request": 28, "previous_pull_request": 18,
        "pr18_merged_source": BASELINE, "observed_main": MAIN, "observed_coordination": COORD,
        "accepted_import_roots": ROOTS, "accepted_local_module_count": len(records),
        "source_pin_file": "module-pins.json", "source_inventory": "accepted-sources.tsv",
        "evidence_inventory": "evidence-inventory.tsv", "source_delta": "source-delta.tsv",
        "evidence_inventory_scope": "1003 committed contribution files plus the existing shared core; no build products, binaries, caches, or duplicate build trees",
        "inventory_counts": {"retained_files": len(retained), "retained_bytes": sum(r[1] for r in retained),
                             "categories": dict(collections.Counter(r[4] for r in retained)),
                             "compressed_originals": len(compressed)},
        "compressed_evidence": compressed,
        "three_way_comparison": {"baseline": BASELINE, "main": MAIN, "incoming": SOURCE,
            "changes": dict(collections.Counter(r[1] for r in delta)), "content_conflicts": conflicts,
            "main_matches_pr18_for_all_preexisting_scoped_paths": all(current_main.get(p) == b for p, b in previous.items()),
            "warning": "Recompute against refreshed main before integration; never replace main with the older contribution tree."},
        "shared_record_baselines": shared,
        "toolchain": {"version": "Lean 4.19.0", "release_commit": "6caaee842e94",
            "linux_archive_sha256": "6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe",
            "linux_binary_sha256": "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023",
            "archive_url": "https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst",
            "host_compatibility": "Documented proc-self-exe readlink shim; official Lean binary and kernel unchanged"},
        "reproduce_argv": ["python3", "-B", f"{PREFIX}/check.py", "/absolute/path/to/lean",
            "--evidence", "/new/nonexistent/path", "--pins", f"{PREFIX}/integration/module-pins.json",
            "--module", "Conclusion739", "--module", "TerminalObstruction", "--jobs", "2", "--require-committed"],
        "exported_endpoints": [
            {"name": "SevenColumnKernel.Finite739.ancestry_bound39", "type": "∀ A P t : Nat, 0 < A → SevenColumnKernel.PalindromeBridge.PalindromeStarts739 P → Lychrel196.orbit A t = P → t ≤ 39"},
            {"name": "SevenColumnKernel.Finite739.no_196_739_palindrome", "type": "∀ t : Nat, ¬ SevenColumnKernel.PalindromeBridge.PalindromeStarts739 (Lychrel196.orbit 196 t)"}],
        "allowed_axioms": ["propext", "Classical.choice", "Quot.sound"],
        "initial_compile": {"status": "PASS_WITH_RECORDED_DEPENDENCY_REUSE",
            "log": f"{PREFIX}/certificate/Conclusion739-aggregate01.log",
            "scope": "Complete numerical endpoints; separate full clean rebuild remains pending"},
        "pending_gates": ["Independent fresh 383-module build and exhaustive theorem axiom audit at the exact source pins",
            "Independent endpoint type check against fresh objects and final semantic review publication",
            "Explicit scoped integration assignment or release/reassignment from existing serialized owner",
            "Refresh main, recompare every accepted source/dependency and preserve unrelated concurrent files",
            "Merged-source replay and publication-record byte verification"],
        "coordination_constraint": {"owner": "Agent #107", "role": "default-branch-integration",
            "scope": "Only reviewed PR #11 and its shared acceptance/publication records.",
            "status": "ACTIVE", "release_policy": "Explicit release; no inferred expiry",
            "this_handoff_claims_role_or_scope_change": False},
        "excluded_infrastructure": ["Compiled .olean/.ilean and binary objects", "Compiler/runtime installation and copied standard library",
            "Duplicate snapshot/build dependency trees", "Python __pycache__ and .pyc", "Operational publishing scratch"],
        "preserve": ["All earlier research and unrelated contributions", "Failed attempts, original dense batches, compiler failures and source history",
            "Historical seven-column written/Python reports; add a named superseding 739-only formal note"],
        "not_claimed": ["Independent full-chain acceptance before review evidence passes", "Default-branch integration",
            "P196", "Decimal Lychrel existence", "Optimality or attainability of bound 39",
            "Lean formalization of bounds for 217, 218, 620, or 777"]
    })
    print(json.dumps({"modules": len(records), "retained_files": len(retained),
                      "changes": len(delta), "content_conflicts": conflicts}))


if __name__ == "__main__":
    main()
