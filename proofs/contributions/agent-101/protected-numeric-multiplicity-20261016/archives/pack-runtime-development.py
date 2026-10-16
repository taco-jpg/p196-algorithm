#!/usr/bin/env python3
"""Create the byte-preserving runtime evidence archive and external hash manifest."""

from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
from pathlib import Path
import stat
import tarfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


here = Path(__file__).resolve().parent
contribution = here.parent
repo = contribution.parents[3]
assert (repo / "proofs").is_dir()
archive = here / "runtime-development.tar.gz"
manifest_path = here / "manifest.json"
if archive.exists() or manifest_path.exists():
    raise SystemExit("Refusing to overwrite an existing archive or manifest")
prefixes = [contribution / "normalization", contribution / "safety",
            contribution / "dependencies/safe-high"]
excluded_parts = {"__pycache__", ".cache", "cache", ".lake"}
excluded_suffixes = {".olean", ".ilean", ".pyc", ".pyo"}
rows, contents, exclusions = [], {}, []
for prefix in prefixes:
    for path in sorted(prefix.rglob("*")):
        relative = path.relative_to(repo).as_posix()
        st = path.lstat()
        if stat.S_ISLNK(st.st_mode):
            raise SystemExit("Symlinks are not archive evidence: " + relative)
        if stat.S_ISDIR(st.st_mode):
            continue
        if not stat.S_ISREG(st.st_mode):
            raise SystemExit("Non-regular evidence file: " + relative)
        if any(x in excluded_parts for x in path.relative_to(prefix).parts) or path.suffix in excluded_suffixes:
            exclusions.append(relative)
            continue
        data = path.read_bytes()
        contents[relative] = data
        rows.append({"path": relative, "bytes": len(data), "sha256": digest(data)})
rows.sort(key=lambda row: row["path"])
with archive.open("xb") as raw:
    with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as tar:
            for row in rows:
                info = tar.gettarinfo(str(repo / row["path"]), arcname=row["path"])
                info.size = row["bytes"]
                tar.addfile(info, io.BytesIO(contents[row["path"]]))
for row in rows:
    assert digest((repo / row["path"]).read_bytes()) == row["sha256"]
expected_pins = {
    "proofs/Agent101NormalizationValue.lean": "50d2d40d5d8db605b8b6d363bf1d0ec762d8c06983c4bb3384f3e1f3094adac9",
    "proofs/Agent101ProtectedSafety.lean": "7b3f060d84e7b955f47425dc69277ea8d8f2fa94a62db173a47f3a614d2a2eb2",
}
pins = []
for path, sha in expected_pins.items():
    assert digest((repo / path).read_bytes()) == sha
    matches = [row["path"] for row in rows if row["sha256"] == sha]
    assert matches
    pins.append({"path": path, "sha256": sha, "matching_archived_snapshots": matches})
receipt_path = contribution / "safety/attempt-003/author-snapshot-receipt.json"
receipt = json.loads(receipt_path.read_text())
manifest = {
    "schema_version": 1,
    "repository": "taco-jpg/p196-algorithm",
    "created_at_utc": datetime.now(timezone.utc).isoformat(),
    "archive": {"filename": archive.name, "bytes": archive.stat().st_size,
                "sha256": digest(archive.read_bytes()), "format": "gzip-compressed PAX tar",
                "member_count": len(rows), "uncompressed_file_bytes": sum(row["bytes"] for row in rows)},
    "member_path_base": "repository root",
    "source_prefixes": [path.relative_to(repo).as_posix() for path in prefixes],
    "content_policy": "Original file bytes, including empty logs and failed Lean sources, are unchanged. Local originals were retained. No Lean build was run during packaging.",
    "excluded_policy": {"directory_components": sorted(excluded_parts), "suffixes": sorted(excluded_suffixes)},
    "excluded_files": exclusions,
    "accepted_source_pins": pins,
    "evidence_classification": [
        {"prefix": "normalization/attempt-001", "classification": "Preserved failed development attempt in the alternative SafeHigh chain"},
        {"prefix": "normalization/attempt-002", "classification": "Corrected SafeHigh alternative compile PASS; dependency objects reused explicitly"},
        {"prefix": "safety/attempt-001", "classification": "Alternative 20-module SafeHigh closure, complete source build and explicit trust-zero audit PASS"},
        {"prefix": "safety/attempt-002", "classification": "Time-zero helper author compile PASS against the alternative closure"},
        {"prefix": "normalization/attempt-003", "classification": "Final thin Agent3 compatibility exact-hash local author snapshot PASS"},
        {"prefix": "safety/attempt-003", "classification": "Final 21-module exact-hash local author snapshot and explicit trust-zero audit PASS"},
        {"prefix": "dependencies/safe-high", "classification": "Unchanged original sources retained for the alternative chain"},
    ],
    "publication_caveat": {
        "classification": receipt["classification"],
        "recorded_repository_head": receipt["recorded_repository_head"],
        "source_commit_field_meaning": receipt["source_commit_field_meaning"],
        "recorded_source_tree_clean": receipt["recorded_source_tree_clean"],
        "source_tree_clean_limitation": receipt["source_tree_clean_limitation"],
        "new_local_paths_not_yet_published_at_recorded_head": receipt["new_local_paths_not_yet_published_at_recorded_head"],
        "receipt_member": receipt_path.relative_to(repo).as_posix(),
        "receipt_sha256": digest(receipt_path.read_bytes()),
        "note": "Preserved author receipts do not claim that the new 21-module inputs were published at e3802562; later published exact-commit verification is separate.",
    },
    "sidecar_helpers": [{"filename": p.name, "bytes": p.stat().st_size, "sha256": digest(p.read_bytes())}
                        for p in [here / "verify-runtime-development.py", Path(__file__).resolve()]],
    "packaging_command": ["python3", Path(__file__).resolve().relative_to(repo).as_posix()],
    "members": rows,
}
with manifest_path.open("x", encoding="utf-8") as out:
    json.dump(manifest, out, indent=2)
    out.write("\n")
print(json.dumps({"status": "PASS", "archive": manifest["archive"],
                  "manifest_sha256": digest(manifest_path.read_bytes()),
                  "excluded_file_count": len(exclusions)}))
