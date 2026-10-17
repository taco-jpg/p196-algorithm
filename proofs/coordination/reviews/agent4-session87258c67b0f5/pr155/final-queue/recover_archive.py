#!/usr/bin/env python3
"""Safely recover and byte-check the exact campaign-final-revisit archive."""
import argparse
import hashlib
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import resource
import stat
import tarfile

LIMIT = 1024 * 1024 * 1024
def constrain_address_space():
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (min(LIMIT, hard) if hard != resource.RLIM_INFINITY else LIMIT, hard))

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()

def safe_path(root, name):
    p = PurePosixPath(name)
    if not name or p.is_absolute() or ".." in p.parts or "." in p.parts or "\\" in name:
        raise ValueError("Unsafe archive path: " + repr(name))
    candidate = root.joinpath(*p.parts)
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise ValueError("Archive path escapes destination")
    return candidate

def verify_and_recover(archive, metadata_path, destination):
    constrain_address_space()
    archive, metadata_path, destination = map(Path, (archive, metadata_path, destination))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    archive_bytes = archive.read_bytes()
    actual_sha = hashlib.sha256(archive_bytes).hexdigest()
    actual_git = hashlib.sha1(b"blob " + str(len(archive_bytes)).encode() + b"\0" + archive_bytes).hexdigest()
    if len(archive_bytes) != metadata["archive"]["bytes"] or actual_sha != metadata["archive"]["sha256"] or actual_git != metadata["archive"]["git_blob"]:
        raise ValueError("Compressed archive identity mismatch")
    if destination.exists():
        raise FileExistsError("Recovery destination must not exist; no overwrite is allowed")
    destination.mkdir(parents=True)
    records, seen, manifest = [], set(), None
    with lzma.open(archive, "rb") as decoded:
        with tarfile.open(fileobj=decoded, mode="r|") as tf:
            for index, member in enumerate(tf):
                if not member.isfile() or member.issym() or member.islnk():
                    raise ValueError("Only ordinary file entries are allowed")
                if member.name in seen:
                    raise ValueError("Duplicate archive member: " + member.name)
                seen.add(member.name)
                target = safe_path(destination, member.name)
                if index == 0:
                    if member.name != "PACKAGE_SOURCE_MANIFEST.json":
                        raise ValueError("Manifest must be the first member")
                    stream = tf.extractfile(member)
                    body = stream.read()
                    if hashlib.sha256(body).hexdigest() != metadata["source_manifest_sha256"]:
                        raise ValueError("Manifest identity mismatch")
                    manifest = json.loads(body)
                    expected = {entry["archive_path"]: entry for entry in manifest["files"]}
                    if len(expected) != len(manifest["files"]):
                        raise ValueError("Manifest contains duplicate paths")
                    if len(expected) != metadata["source_file_count"]:
                        raise ValueError("Manifest file count mismatch")
                    with target.open("xb") as out:
                        out.write(body)
                    os.chmod(target, 0o644)
                    continue
                if member.name not in expected:
                    raise ValueError("Unexpected archive member: " + member.name)
                entry = expected[member.name]
                if member.size != entry["bytes"] or member.mode != int(entry["mode"], 8):
                    raise ValueError("Archive size/mode mismatch: " + member.name)
                if member.uid != 0 or member.gid != 0 or member.mtime != 0 or member.uname or member.gname:
                    raise ValueError("Archive metadata is not canonical")
                target.parent.mkdir(parents=True, exist_ok=True)
                stream = tf.extractfile(member)
                with target.open("xb") as out:
                    remaining = member.size
                    while remaining:
                        block = stream.read(min(65536, remaining))
                        if not block:
                            raise ValueError("Truncated archive member")
                        out.write(block)
                        remaining -= len(block)
                mode = int(entry["mode"], 8)
                if mode & ~0o777:
                    raise ValueError("Special permission bits are not allowed")
                os.chmod(target, mode)
                actual = digest(target)
                if actual != entry["sha256"] or target.stat().st_size != entry["bytes"] or stat.S_IMODE(target.stat().st_mode) != mode:
                    raise ValueError("Recovered byte/mode mismatch: " + member.name)
                records.append({"archive_path": member.name, "bytes": entry["bytes"], "mode": entry["mode"], "sha256": actual, "status": "PASS"})
        # Consume any remaining XZ stream bytes so the stream integrity check is completed.
        while decoded.read(65536):
            pass
    if manifest is None or seen != set(expected) | {"PACKAGE_SOURCE_MANIFEST.json"}:
        raise ValueError("Missing archive members")
    return {"status": "PASS", "archive_sha256": actual_sha, "archive_git_blob": actual_git, "source_files_verified": len(records), "source_bytes_verified": sum(x["bytes"] for x in records), "archive_members": len(seen), "destination": str(destination), "checks": ["Exact compressed byte size, SHA256 and Git blob", "Exact embedded source manifest identity", "All member paths, regular-file type and unique membership", "Canonical tar owner/time and exact original file modes", "Every recovered file size and SHA256", "Complete XZ decompression/integrity check"], "files": records}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("archive")
    p.add_argument("metadata")
    p.add_argument("destination")
    args = p.parse_args()
    print(json.dumps(verify_and_recover(args.archive, args.metadata, args.destination), indent=2))

if __name__ == "__main__":
    main()
