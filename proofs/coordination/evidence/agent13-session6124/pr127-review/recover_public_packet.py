#!/usr/bin/env python3
"""Verify the public review packet and optionally extract into a new directory."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile

def sha(data):
    return hashlib.sha256(data).hexdigest()

def verify(path, expected_sha256=None):
    archive = Path(path)
    raw = archive.read_bytes()
    digest = sha(raw)
    if expected_sha256 and digest != expected_sha256:
        raise ValueError("Archive SHA-256 mismatch")
    payload = {}
    with tarfile.open(archive, "r:xz") as tar:
        for member in tar:
            name = PurePosixPath(member.name)
            if not member.isfile() or name.is_absolute() or ".." in name.parts:
                raise ValueError("Unsafe or unsupported archive member")
            if len(name.parts) < 2 or name.parts[0] != "review127-public":
                raise ValueError("Unexpected public archive root")
            relative = str(PurePosixPath(*name.parts[1:]))
            if relative in payload:
                raise ValueError("Duplicate member")
            data = tar.extractfile(member).read()
            if len(data) != member.size:
                raise ValueError("Truncated member")
            payload[relative] = data
    manifest_data = payload.pop("PUBLIC_ARCHIVE_MANIFEST.json")
    manifest = json.loads(manifest_data)
    expected = {row["path"]: row for row in manifest["files"]}
    if len(expected) != len(manifest["files"]) or set(expected) != set(payload):
        raise ValueError("Member coverage mismatch")
    forbidden = set(manifest["forbidden_archive_members"])
    if forbidden.intersection(payload):
        raise ValueError("Excluded local material is an archive member")
    for name, data in payload.items():
        rec = expected[name]
        if len(data) != rec["bytes"] or sha(data) != rec["sha256"]:
            raise ValueError("Member identity mismatch: " + name)
    result = {"status": "PASS", "archive_sha256": digest, "archive_bytes": len(raw),
              "archive_git_blob_sha1": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
              "manifest_sha256": sha(manifest_data),
              "substantive_files_verified": len(payload),
              "substantive_bytes_verified": sum(map(len, payload.values())),
              "archive_members_verified": len(payload) + 1,
              "excluded_material_present_as_member": False,
              "extracted": False, "archive_content_executed": False}
    return payload, manifest_data, result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive")
    parser.add_argument("--expected-sha256")
    parser.add_argument("--extract-to")
    args = parser.parse_args()
    payload, manifest, result = verify(args.archive, args.expected_sha256)
    if args.extract_to:
        root = Path(args.extract_to)
        if root.exists():
            raise ValueError("Destination must not exist")
        root.mkdir(parents=True)
        payload["PUBLIC_ARCHIVE_MANIFEST.json"] = manifest
        for name, data in payload.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(data)
        result["extracted"] = True
        result["extraction_directory"] = str(root)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
