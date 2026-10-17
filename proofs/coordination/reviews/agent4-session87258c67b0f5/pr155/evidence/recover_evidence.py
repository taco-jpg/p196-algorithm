#!/usr/bin/env python3
"""Verify and safely recover every manifest-listed PR155 evidence payload."""
import argparse
import base64
import hashlib
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import re
import tarfile

CHUNK = 1024 * 1024


def safe_relative(value):
    if not isinstance(value, str) or not value or "\\" in value or "\0" in value:
        raise ValueError("Invalid relative member path")
    path = PurePosixPath(value)
    if path.is_absolute() or value != path.as_posix() or any(p in (".", "..") for p in path.parts):
        raise ValueError(f"Unsafe or noncanonical member path: {value!r}")
    return path


def valid_hash(value):
    return isinstance(value, str) and re.fullmatch("[0-9a-f]{64}", value) is not None


def file_hash(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for data in iter(lambda: stream.read(CHUNK), b""):
            result.update(data)
    return result.hexdigest()


def recover(manifest_path, destination, from_parts):
    manifest = json.loads(manifest_path.read_text())
    directory = manifest_path.resolve().parent
    archive_info = manifest["archive"]
    archive_path = directory / safe_relative(archive_info["path"])
    expected = {}
    relative_seen = set()
    for entry in manifest["payloads"]:
        relative = safe_relative(entry["path"])
        member = safe_relative(entry["tar_member"]).as_posix()
        if member != "pr155-evidence/" + relative.as_posix() or member in expected or relative in relative_seen:
            raise ValueError("Duplicate or mismatched manifest member")
        if not isinstance(entry["bytes"], int) or entry["bytes"] < 0 or not valid_hash(entry["sha256"]):
            raise ValueError("Invalid manifest size or digest")
        relative_seen.add(relative)
        expected[member] = entry
    if len(expected) != manifest["payload_count"]:
        raise ValueError("Manifest payload count mismatch")
    if destination.exists() or destination.is_symlink():
        raise FileExistsError("Recovery destination must not already exist")
    destination.mkdir(parents=False)
    if from_parts:
        archive_path = destination / "reconstructed-publication.tar.xz"
        hasher = hashlib.sha256()
        written = 0
        with archive_path.open("xb") as output:
            for number, part in enumerate(manifest["base64"]["parts"], 1):
                if part["index"] != number or part["decoded_offset"] != written:
                    raise ValueError("Invalid base64 part ordering or offset")
                encoded = (directory / safe_relative(part["path"])).read_bytes()
                if len(encoded) != part["bytes"] or len(encoded) > 524288 or hashlib.sha256(encoded).hexdigest() != part["sha256"]:
                    raise ValueError(f"Base64 part identity mismatch: {number}")
                if not encoded.isascii() or len(encoded) != part["characters"]:
                    raise ValueError("Non-ASCII or incorrectly sized base64 part")
                decoded = base64.b64decode(encoded, validate=True)
                if len(decoded) != part["decoded_bytes"] or hashlib.sha256(decoded).hexdigest() != part["decoded_sha256"]:
                    raise ValueError(f"Decoded part identity mismatch: {number}")
                output.write(decoded)
                hasher.update(decoded)
                written += len(decoded)
        if written != archive_info["bytes"] or hasher.hexdigest() != archive_info["sha256"]:
            raise ValueError("Reconstructed archive identity mismatch")
    if archive_path.stat().st_size != archive_info["bytes"] or file_hash(archive_path) != archive_info["sha256"]:
        raise ValueError("Compressed archive identity mismatch")
    payload_root = destination / "pr155-evidence"
    payload_root.mkdir()
    seen = set()
    verified_bytes = 0
    with lzma.LZMAFile(archive_path, "rb") as compressed:
        with tarfile.open(fileobj=compressed, mode="r|", bufsize=CHUNK) as archive:
            for member in archive:
                safe_relative(member.name)
                if not member.isreg() or member.name not in expected or member.name in seen:
                    raise ValueError(f"Unexpected, duplicate, or nonregular tar member: {member.name}")
                entry = expected[member.name]
                if member.size != entry["bytes"]:
                    raise ValueError(f"Tar member size mismatch: {member.name}")
                target = payload_root / safe_relative(entry["path"])
                target.parent.mkdir(parents=True, exist_ok=True)
                descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
                count = 0
                hasher = hashlib.sha256()
                source = archive.extractfile(member)
                if source is None:
                    raise ValueError("Missing tar member stream")
                with source, os.fdopen(descriptor, "wb") as output:
                    for data in iter(lambda: source.read(CHUNK), b""):
                        output.write(data)
                        hasher.update(data)
                        count += len(data)
                if count != entry["bytes"] or hasher.hexdigest() != entry["sha256"]:
                    raise ValueError(f"Recovered payload identity mismatch: {entry['path']}")
                os.chmod(target, entry["mode"] & 0o777)
                seen.add(member.name)
                verified_bytes += count
    if seen != set(expected):
        raise ValueError(f"Missing archive members: {sorted(set(expected) - seen)}")
    if verified_bytes != manifest["payload_bytes"]:
        raise ValueError("Recovered payload byte count mismatch")
    return {"status": "PASS", "archive_sha256": archive_info["sha256"],
            "verified_payload_count": len(seen), "verified_payload_bytes": verified_bytes,
            "recovered_directory": str(payload_root), "recovered_from_base64_parts": from_parts,
            "security": "No extractall; exact manifest allowlist; paths normalized; links and duplicates rejected; exclusive file creation in a new destination."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--from-parts", action="store_true")
    arguments = parser.parse_args()
    result = recover(arguments.manifest, arguments.destination, arguments.from_parts)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
