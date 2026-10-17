#!/usr/bin/env python3
"""Seal the already collected ownership artifacts; no remote reads or source operations."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
names = [
    "README.md",
    "FINAL_OWNERSHIP_MEMO.md",
    "HISTORICAL_PR167_AVAILABLE_MEMO.md",
    "TASK_PATH_BLOB_MATRIX.md",
    "COVERAGE.json",
    "TASK_OBSERVATIONS.json",
    "COMMENT_OBSERVATIONS.json",
    "DELTA_RECEIPT.json",
    "SUPERSESSION.json",
    "seal.py",
]
coverage = json.loads((root / "COVERAGE.json").read_text())
prs = [row["pr"] for row in coverage["records"]]
assert len(prs) == 53 and len(set(prs)) == 53
assert coverage["covered"] == 53 and coverage["missing"] == [] and coverage["unexpected"] == []
assert coverage["coordination_ref"] == "eec6257643218217e41af2c29265d16a7b26811a"
entries = []
for name in names:
    data = (root / name).read_bytes()
    entries.append({
        "path": name,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
    })
manifest = {
    "schema_version": 1,
    "scope": "Local ownership evidence prepared exclusively from previously collected observations; no new remote verification.",
    "snapshot": coverage["coordination_ref"],
    "coverage": {"prs": 53, "unique": 53, "missing": [], "unexpected": [], "delivery_or_integration": 51, "active_source": 2},
    "files": entries,
    "excluded_to_avoid_recursion": ["MANIFEST.json", "PACKAGING_COMMAND.txt", "PACKAGING_STDOUT.json", "PACKAGING_EXIT_CODE.txt"],
}
data = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()
(root / "MANIFEST.json").write_bytes(data)
print(json.dumps({
    "result": "ARTIFACTS_SAVED",
    "snapshot": coverage["coordination_ref"],
    "coverage": manifest["coverage"],
    "manifest_path": str(root / "MANIFEST.json"),
    "manifest_sha256": hashlib.sha256(data).hexdigest(),
    "files": entries,
}, ensure_ascii=False, indent=2))

