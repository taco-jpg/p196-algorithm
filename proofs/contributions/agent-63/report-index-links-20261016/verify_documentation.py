#!/usr/bin/env python3
"""Check the Agent63 documentation increment and exercise the unchanged replay wrapper on synthetic fixtures."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
EVIDENCE.mkdir(exist_ok=True)
BASELINE = "2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5"
NOTE_START = "<!-- AGENT63 HISTORICAL LINK REPAIR 20261016 -->"
NOTE_END = "<!-- END AGENT63 HISTORICAL LINK REPAIR -->"
LINK = re.compile(r"\]\(([^)]+)\)")

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

before_bytes = (ROOT / "before/REPORTS.md").read_bytes()
after_bytes = (ROOT / "after/REPORTS.md").read_bytes()
before = before_bytes.decode("utf-8")
after = after_bytes.decode("utf-8")
old_map_bytes = (ROOT / "before/SOURCE_MAP.json").read_bytes()
new_map_bytes = (ROOT / "after/SOURCE_MAP.json").read_bytes()
old_map = json.loads(old_map_bytes)
new_map = json.loads(new_map_bytes)
baseline_tree = json.loads((EVIDENCE / "baseline-tree.json").read_text())
assert baseline_tree["truncated"] is False
tree = {item["path"]: item for item in baseline_tree["tree"]}
prior_links = LINK.findall(before)
assert len(prior_links) == len(set(prior_links)) == 356
assert all("#" not in link and "://" not in link for link in prior_links)
assert git_blob(before_bytes) == "3e13b819c649f2aee759ee2db9458c5dc4303759"
assert sha(before_bytes) == "9b4b37a2e0c375524093636edd531a62281257bc02d84a8ac52ace3c35e3f623"
assert git_blob(old_map_bytes) == "e5f8d27bf09f50f8b9756bf91dff02e992aa4a32"
assert set(old_map) == set(new_map)
assert old_map["base"] == new_map["base"] == BASELINE
assert old_map["paths"].keys() == new_map["paths"].keys()
changed_keys = [key for key in old_map["paths"] if old_map["paths"][key] != new_map["paths"][key]]
assert changed_keys == ["proofs/REPORTS.md"]
expected_entry = dict(old_map["paths"]["proofs/REPORTS.md"])
expected_entry["current"] = None
assert new_map["paths"]["proofs/REPORTS.md"] == expected_entry
expected_serialization = old_map_bytes.replace(
    b'"current": "proofs/REPORTS.md"', b'"current": null')
assert new_map_bytes == expected_serialization

# Remove only the additive, delimited note, then invert only the pinned URLs.
start = after.index(NOTE_START)
end = after.index(NOTE_END, start) + len(NOTE_END)
assert after[end:end + 2] == "\n\n"
without_note = after[:start] + after[end + 2:]
prefix = f"https://github.com/taco-jpg/p196-algorithm/blob/{BASELINE}/proofs/"
restored = LINK.sub(lambda match: "](" + (
    match.group(1)[len(prefix):] if match.group(1).startswith(prefix) else match.group(1)
) + ")", without_note)
assert restored == before, "Historical prose, labels or ordering changed"
new_links = LINK.findall(without_note)
assert len(new_links) == 356
changed_destinations = sum(a != b for a, b in zip(prior_links, new_links))
assert changed_destinations == 355
assert new_links[0] == "CONSOLIDATION.md"
targets = []
for old_link, new_link in zip(prior_links, new_links):
    path = "proofs/" + old_link
    meta = tree[path]
    record = old_map["paths"][path]
    assert meta["type"] == "blob"
    assert record["oid"] == meta["sha"]
    assert record["mode"] == meta["mode"]
    assert new_link == old_link or new_link == prefix + old_link
    targets.append({
        "original_target": old_link,
        "new_target": new_link,
        "baseline_path": path,
        "git_blob": meta["sha"],
        "mode": meta["mode"],
        "bytes": meta["size"],
        "sha256_from_source_map": record["sha256"],
        "preserved_path": record["preserved"],
    })
(EVIDENCE / "link-targets.json").write_text(json.dumps(targets, indent=2) + "\n")
original_wrapper = (ROOT / "source/replay_original_layout.py").read_bytes()
assert git_blob(original_wrapper) == "4745990a5477a4b6a5c537b368bf78d214ce2622"

# These are small synthetic repositories, not the complete P196 source tree.
# The real wrapper bytes are used unchanged; only tempfile's runtime directory is configured.
fixtures = ROOT / "fixtures"
fixtures.mkdir(exist_ok=True)
fixture_results = []
def run_fixture(name, mapping_after, changed_presentation, corrupt_preserved, expected_return):
    repo = Path(tempfile.mkdtemp(prefix=name + "-", dir=fixtures))
    retained = repo / expected_entry["preserved"]
    current = repo / "proofs/REPORTS.md"
    current.parent.mkdir(parents=True, exist_ok=True)
    current.write_bytes(before_bytes)
    commands = [
        ["git", "init", "-q", str(repo)],
        ["git", "-C", str(repo), "add", "proofs/REPORTS.md"],
        ["git", "-C", str(repo), "-c", "user.name=Agent63 synthetic fixture",
         "-c", "user.email=fixture@example.invalid", "commit", "-q", "-m", "Synthetic baseline"],
    ]
    setup = []
    for command in commands:
        result = subprocess.run(command, capture_output=True, text=True)
        setup.append({"argv": command, "returncode": result.returncode,
                      "stdout": result.stdout, "stderr": result.stderr})
        assert result.returncode == 0, setup
    fixture_base = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    retained.parent.mkdir(parents=True, exist_ok=True)
    retained.write_bytes(before_bytes + (b"\nCORRUPTED FIXTURE\n" if corrupt_preserved else b""))
    current.write_bytes(after_bytes if changed_presentation else before_bytes)
    entry = dict(expected_entry if mapping_after else old_map["paths"]["proofs/REPORTS.md"])
    mapping = {"base": fixture_base, "paths": {"proofs/REPORTS.md": entry}}
    (repo / "proofs/SOURCE_MAP.json").write_text(json.dumps(mapping, indent=2) + "\n")
    wrapper = repo / "proofs/replay_original_layout.py"
    wrapper.write_bytes(original_wrapper)
    assert wrapper.read_bytes() == original_wrapper
    temporary = repo / "temporary"
    temporary.mkdir()
    check = (
        "from pathlib import Path; import hashlib; "
        "p=Path('proofs/REPORTS.md').read_bytes(); "
        f"assert hashlib.sha256(p).hexdigest()=={sha(before_bytes)!r}; "
        "print('REQUESTED_CHECK_RAN_WITH_ORIGINAL_REPORT_BYTES')"
    )
    runner = (
        "import runpy,sys,tempfile; "
        f"tempfile.tempdir={str(temporary)!r}; "
        f"sys.argv={[str(wrapper), '--', sys.executable, '-c', check]!r}; "
        f"runpy.run_path({str(wrapper)!r},run_name='__main__')"
    )
    command = [sys.executable, "-c", runner]
    result = subprocess.run(command, capture_output=True, text=True)
    (EVIDENCE / (name + ".stdout.log")).write_text(result.stdout)
    (EVIDENCE / (name + ".stderr.log")).write_text(result.stderr)
    record = {
        "name": name, "scope": "SYNTHETIC_WRAPPER_FIXTURE",
        "mapping_current_null": mapping_after,
        "presentation_changed": changed_presentation,
        "preserved_copy_corrupted": corrupt_preserved,
        "expected_returncode": expected_return,
        "actual_returncode": result.returncode,
        "requested_check_ran": "REQUESTED_CHECK_RAN_WITH_ORIGINAL_REPORT_BYTES" in result.stdout,
        "wrapper_git_blob": git_blob(original_wrapper),
        "setup_commands": setup,
        "argv": command,
        "stdout_path": name + ".stdout.log", "stderr_path": name + ".stderr.log",
    }
    fixture_results.append(record)
    assert result.returncode == expected_return, record
    if expected_return == 0:
        assert record["requested_check_ran"], record
    else:
        assert not record["requested_check_ran"], record
        assert "Source changed; results for an old hash cannot be applied" in result.stderr, record

run_fixture("original-selection", False, False, False, 0)
run_fixture("changed-report-old-mapping", False, True, False, 2)
run_fixture("changed-report-preserved-selection", True, True, False, 0)
run_fixture("corrupt-preserved-selection", True, True, True, 2)
(EVIDENCE / "wrapper-fixtures.json").write_text(json.dumps(fixture_results, indent=2) + "\n")
result = {
    "status": "PASS",
    "source_snapshot": "10a173cb635fa8d03e357f454232816fc3e77609",
    "publication_base": "116efc60f8d3a29bac4fcf5cdcaf2bbdcdceb3de",
    "historical_baseline": BASELINE,
    "original_relative_links": len(prior_links),
    "changed_destinations": changed_destinations,
    "all_original_targets_present_in_baseline": True,
    "all_targets_match_source_map_blobs_and_modes": True,
    "historical_prose_labels_order_unchanged": True,
    "mapping_entries": len(old_map["paths"]),
    "changed_mapping_entries": changed_keys,
    "mapping_change_is_exactly_current_to_null": True,
    "all_other_mapping_bytes_unchanged": True,
    "wrapper_source_unchanged": True,
    "synthetic_wrapper_cases": [{k: v for k, v in case.items() if k in
        ("name", "actual_returncode", "expected_returncode", "requested_check_ran")}
        for case in fixture_results],
    "files": {
        "before/REPORTS.md": {"bytes": len(before_bytes), "git_blob": git_blob(before_bytes), "sha256": sha(before_bytes)},
        "after/REPORTS.md": {"bytes": len(after_bytes), "git_blob": git_blob(after_bytes), "sha256": sha(after_bytes)},
        "before/SOURCE_MAP.json": {"bytes": len(old_map_bytes), "git_blob": git_blob(old_map_bytes), "sha256": sha(old_map_bytes)},
        "after/SOURCE_MAP.json": {"bytes": len(new_map_bytes), "git_blob": git_blob(new_map_bytes), "sha256": sha(new_map_bytes)},
    },
    "verification_boundaries": {
        "documentation_check": "COMMAND_EXECUTED; EXPECTED_OUTPUT_CONFIRMED",
        "real_wrapper_on_synthetic_repositories": "COMMAND_EXECUTED; EXPECTED_OUTPUT_CONFIRMED",
        "full_original_layout_replay": "NOT_RUN",
        "lean_build_or_axiom_audit": "NOT_RUN",
        "historical_inventory_generation": "NOT_RUN",
        "external_peer_review": "NOT_CLAIMED",
    },
}
(EVIDENCE / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
