#!/usr/bin/env python3
"""Check the complete PR163 evidence packet without executing archived code."""
import base64
import hashlib
import io
import json
import tarfile
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / "ARCHIVE_MANIFEST.json").read_text())
encoded = (root / "verification-evidence.tar.gz.base64").read_bytes()
assert len(encoded) == manifest["base64_bytes"]
assert hashlib.sha256(encoded).hexdigest() == manifest["base64_sha256"]
data = base64.b64decode(encoded, validate=False)
assert len(data) == manifest["archive_bytes"]
assert hashlib.sha256(data).hexdigest() == manifest["archive_sha256"]
assert hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == manifest["archive_git_blob"]
binary = root / manifest["archive"]
if binary.exists():
    assert binary.read_bytes() == data
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
    members = tar.getmembers()
    assert [m.name for m in members] == [r["path"] for r in manifest["members"]]
    for member, expected in zip(members, manifest["members"]):
        assert member.isfile()
        content = tar.extractfile(member).read()
        assert len(content) == expected["bytes"]
        assert hashlib.sha256(content).hexdigest() == expected["sha256"]
print(json.dumps({"status": "PASS", "members": len(members),
                  "original_bytes": manifest["original_bytes"],
                  "archive_bytes": len(data), "executed_archived_code": False}, indent=2))
