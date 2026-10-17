#!/usr/bin/env python3
"""Recheck the immutable PR164 replay selectors; do not reconstruct a historical receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

SOURCE = "fa2683e489acc7c85e08764450550f7e463041da"
BASELINE = "10a173cb635fa8d03e357f454232816fc3e77609"
DOCS = ("proofs/CONSOLIDATION.md", "proofs/FINDINGS.md")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="A new output directory")
    parser.add_argument("--source", default=SOURCE)
    parser.add_argument("--baseline", default=BASELINE)
    args = parser.parse_args()
    for ref in (args.source, args.baseline):
        if not re.fullmatch(r"[0-9a-f]{40}", ref):
            parser.error("Source and baseline must be full immutable commit IDs")
    repo = args.repo.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    commands = []

    def git(*items: str) -> bytes:
        argv = ["git", "-C", str(repo), *items]
        result = subprocess.run(argv, capture_output=True)
        commands.append({"argv": argv, "exit_code": result.returncode,
                         "stdout_sha256": digest(result.stdout),
                         "stderr": result.stderr.decode(errors="replace")})
        if result.returncode:
            raise RuntimeError("Git command failed: " + repr(commands[-1]))
        return result.stdout

    def entries(ref: str) -> dict:
        result = {}
        for item in git("ls-tree", "-rz", "--full-tree", ref).split(b"\0"):
            if item:
                metadata, path = item.split(b"\t", 1)
                mode, kind, oid = metadata.decode().split()
                result[path.decode()] = {"mode": mode, "kind": kind, "oid": oid}
        return result

    try:
        source_bytes = git("show", args.source + ":proofs/SOURCE_MAP.json")
        baseline_bytes = git("show", args.baseline + ":proofs/SOURCE_MAP.json")
        current, original = json.loads(source_bytes), json.loads(baseline_bytes)
        before, after = entries(args.baseline), entries(args.source)
        assert git_blob(baseline_bytes) == before["proofs/SOURCE_MAP.json"]["oid"]
        assert git_blob(source_bytes) == after["proofs/SOURCE_MAP.json"]["oid"]
        assert current.keys() == original.keys()
        assert current["paths"].keys() == original["paths"].keys()
        expected = json.loads(baseline_bytes)
        uses = []
        for doc in DOCS:
            selecting_keys = sorted(path for path, row in original["paths"].items()
                                    if (row.get("current") or row["preserved"]) == doc)
            assert selecting_keys == [doc], (doc, selecting_keys)
            row = original["paths"][doc]
            assert row["current"] == doc
            expected["paths"][doc]["current"] = None
            preserved = row["preserved"]
            original_doc = git("show", args.baseline + ":" + doc)
            preserved_doc = git("show", args.source + ":" + preserved)
            assert original_doc == preserved_doc
            assert digest(original_doc) == row["sha256"]
            assert git_blob(original_doc) == row["oid"]
            assert before[doc] == after[preserved]
            uses.append({"document": doc, "original_selecting_keys": selecting_keys,
                         "new_selected_path": preserved, "original_bytes": len(original_doc),
                         "sha256": row["sha256"], "git_blob": row["oid"], "mode": row["mode"]})
        assert current == expected, "Changes exceed the two authorized current selectors"
        effective = []
        for path in sorted(original["paths"]):
            old, new = original["paths"][path], current["paths"][path]
            old_selected = old.get("current") or old["preserved"]
            new_selected = new.get("current") or new["preserved"]
            left, right = before[old_selected], after[new_selected]
            assert left == right, path
            assert right["mode"] == old["mode"] and right["oid"] == old["oid"], path
            effective.append([path, old_selected, new_selected, right["mode"], right["oid"]])
        assert len(effective) == 9161
        receipt = {
            "schema_version": 1,
            "status": "PASS_FRESH_IMMUTABLE_SOURCE_SELECTION_CHECK",
            "verification_kind": "Regenerated equivalent selector/replay evidence; not historical-byte recovery",
            "historical_receipt": {"name": "actual-map-selection-uses.json",
                                   "status": "ORIGINAL_RECEIPT_NOT_RECOVERED",
                                   "historical_failed_assertion_raw_bytes": "NOT_RECOVERED",
                                   "original_failure_reproduced_or_authenticated": False},
            "source_commit": args.source,
            "baseline_commit": args.baseline,
            "source_map": {"source_git_blob": git_blob(source_bytes), "source_sha256": digest(source_bytes),
                           "baseline_git_blob": git_blob(baseline_bytes), "baseline_sha256": digest(baseline_bytes),
                           "historical_layout_base": current["base"]},
            "selection_uses": uses,
            "only_two_current_fields_changed": True,
            "unrelated_fields_and_records_unchanged": True,
            "effective_replay_entries_checked": len(effective),
            "all_effective_blob_and_mode_identities_unchanged": True,
            "effective_rows_sha256": digest((json.dumps(effective, separators=(",", ":")) + "\n").encode()),
            "checker_sha256": digest(Path(__file__).read_bytes()),
            "all_git_commands_exit_zero": True,
            "lean_execution": "NOT_RUN",
            "full_original_layout_replay": "NOT_RUN",
            "mathematical_source_modified": False,
            "main_merge_performed": False,
        }
        (output / "actual-map-selection-uses.reverified.json").write_text(json.dumps(receipt, indent=2) + "\n")
        print(json.dumps(receipt, indent=2))
    except Exception as error:
        (output / "failure.json").write_text(json.dumps({"status": "FAILED", "error": repr(error)}, indent=2) + "\n")
        raise
    finally:
        (output / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")


if __name__ == "__main__":
    main()
