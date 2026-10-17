#!/usr/bin/env python3
"""Recover the unchanged PR104 support archive from its verified byte slices."""
import hashlib
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
manifest = json.loads((root / "MULTIPART.json").read_text(encoding="utf-8"))
if len(sys.argv) != 2:
    raise SystemExit("Usage: python RECOVER_ARCHIVE.py OWNED_OUTPUT_DIRECTORY")
chunks = []
offset = 0
for item in manifest["parts"]:
    data = (root / item["path"]).read_bytes()
    if item["offset"] != offset or len(data) != item["bytes"]:
        raise SystemExit("Part size or offset mismatch: " + item["path"])
    if hashlib.sha256(data).hexdigest() != item["sha256"]:
        raise SystemExit("Part SHA-256 mismatch: " + item["path"])
    blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    if blob != item["git_blob"]:
        raise SystemExit("Part Git blob mismatch: " + item["path"])
    chunks.append(data)
    offset += len(data)
data = b"".join(chunks)
if len(data) != manifest["archive_bytes"] or hashlib.sha256(data).hexdigest() != manifest["archive_sha256"]:
    raise SystemExit("Original archive identity mismatch")
blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
if blob != manifest["archive_git_blob_identity"]:
    raise SystemExit("Original archive Git identity mismatch")
output = Path(sys.argv[1])
output.mkdir(parents=True, exist_ok=True)
target = output / manifest["archive"]
if target.exists():
    if target.read_bytes() != data:
        raise SystemExit("Refusing to overwrite different existing output")
else:
    with target.open("xb") as stream:
        stream.write(data)
print(json.dumps({"status": "PASS_ARCHIVE_RECOVERED", "path": str(target), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}))
