#!/usr/bin/env python3
"""Copy already captured historical bytes after checking their exact pins.

This performs source-identity checks only. It does not run the generator.
"""

import hashlib
import json
from pathlib import Path

WORKSPACE = Path("/workspace/scratch/4ce7c54d31f6")
EVIDENCE = Path(__file__).resolve().parent
DESTINATION = EVIDENCE.parent.parent / "source-preservation"
ARCHIVE = "2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5"
SCOUT = WORKSPACE / "agent3-reconnaissance/three-layer-scout-20261016"
SOURCES = [
    (
        SCOUT / "astra_counting_checkpoint.txt",
        "astra_counting_checkpoint.txt",
        "e9950729ec8ba8b0e8fb1a03010880a9b8cf71ef4315cb89bae57dd2a296c151",
        "6d585173ed8037a88d3d492de14fd03a98da8b5e",
    ),
    (
        WORKSPACE / "p196-history/proofs/astra_counting_nooverflow_depth__b9324f440911b5d7.py",
        "astra_counting_nooverflow_depth.py",
        "ce50b73a2499bc28b4df0e00a0488392eb4f661599ccf0ead496e754c3de0db7",
        "c41f16d9853adf8320db54564385d1b3fe8fde99",
    ),
    (
        SCOUT / "astra_counting_nooverflow_depth_results.json",
        "astra_counting_nooverflow_depth_results.json",
        "a259bc00111a2f8ffd1fa9a601595d2c272802f4533715041dbeaff493b008f6",
        "a69e9817dbc065b74cb94d9c62af90eb0f1bd0cb",
    ),
]

verified = []
for origin, name, expected_sha, expected_blob in SOURCES:
    data = origin.read_bytes()
    actual_sha = hashlib.sha256(data).hexdigest()
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    actual_blob = hashlib.sha1(header + data).hexdigest()
    if (actual_sha, actual_blob) != (expected_sha, expected_blob):
        raise SystemExit(f"Historical source pin mismatch: {name}")
    target = DESTINATION / name
    if target.exists() and target.read_bytes() != data:
        raise SystemExit(f"Refusing to overwrite a different preserved source: {target}")
    verified.append((data, target, {
        "filename": name,
        "sha256": actual_sha,
        "git_blob": actual_blob,
        "bytes": len(data),
        "archive_snapshot": ARCHIVE,
        "archive_path": f"proofs/archive/source-trees/{ARCHIVE}/proofs/research/{name}",
        "copied_from": str(origin),
    }))

DESTINATION.mkdir(parents=True, exist_ok=True)
for data, target, record in verified:
    target.write_bytes(data)

manifest = {
    "status": "PASS",
    "verification_scope": "Exact SHA-256 and Git blob byte identities; no historical generator execution or claim that its full graph was formally checked.",
    "sources": [record for _, _, record in verified],
}
rendered = json.dumps(manifest, indent=2) + "\n"
(DESTINATION / "source_identity.json").write_text(rendered)
(EVIDENCE / "source-preservation.log").write_text(rendered)
print(rendered, end="")
