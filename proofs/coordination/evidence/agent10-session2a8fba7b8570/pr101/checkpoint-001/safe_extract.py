#!/usr/bin/env python3
"""Verify a pinned PR101 checkpoint and optionally extract regular files only.

This helper never imports or executes archived source. Pin the receipt hash from
the publishing record; a self-consistent receipt alone is not authentication.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import tarfile


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_name(name):
    require(isinstance(name, str) and name and "\\" not in name and "\0" not in name,
            "Invalid member name")
    p = PurePosixPath(name)
    require(not p.is_absolute() and all(x not in ("", ".", "..") for x in name.split("/"))
            and str(p) == name, "Noncanonical or escaping member path")
    return p


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--receipt-sha256", required=True)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--destination", type=Path,
                        help="A new destination; omitted means verification only")
    args = parser.parse_args()
    require(re.fullmatch(r"[0-9a-f]{64}", args.receipt_sha256) is not None,
            "A pinned lowercase receipt SHA-256 is required")
    receipt_bytes = args.receipt.read_bytes()
    require(sha256(receipt_bytes) == args.receipt_sha256, "Receipt SHA-256 mismatch")
    receipt = json.loads(receipt_bytes)
    archive_path = args.archive or args.receipt.parent / receipt["archive"]["filename"]
    manifest_path = args.manifest or args.receipt.parent / receipt["manifest"]["filename"]
    manifest_bytes = manifest_path.read_bytes()
    require(len(manifest_bytes) == receipt["manifest"]["bytes"] and
            sha256(manifest_bytes) == receipt["manifest"]["sha256"], "Manifest identity mismatch")
    manifest = json.loads(manifest_bytes)
    archive_bytes = archive_path.read_bytes()
    require(len(archive_bytes) == receipt["archive"]["bytes"] and
            sha256(archive_bytes) == receipt["archive"]["sha256"], "Archive identity mismatch")
    entries = manifest["members"]
    names = [row["path"] for row in entries]
    require(names == sorted(set(names)), "Manifest names must be unique and sorted")
    require(len(entries) == receipt["archive"]["member_count"], "Member count mismatch")
    require(sum(row["bytes"] for row in entries) == receipt["archive"]["member_bytes"],
            "Total member byte count mismatch")
    expected = {row["path"]: row for row in entries}
    for row in entries:
        safe_name(row["path"])
        require(isinstance(row["bytes"], int) and row["bytes"] >= 0 and
                row["mode"] in (0o444, 0o555, 0o644, 0o755), "Invalid file metadata")
    verified = {}
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:xz") as archive:
        members = archive.getmembers()
        require([m.name for m in members] == names, "Archive and manifest names/order differ")
        for member in members:
            safe_name(member.name)
            require(member.isfile() and not member.issym() and not member.islnk(),
                    "Only regular files are allowed")
            row = expected[member.name]
            require(member.size == row["bytes"] and member.mode == row["mode"],
                    "Member metadata mismatch: " + member.name)
            stream = archive.extractfile(member)
            require(stream is not None, "Unreadable archive member")
            data = stream.read(row["bytes"] + 1)
            require(len(data) == row["bytes"] and sha256(data) == row["sha256"],
                    "Member content mismatch: " + member.name)
            verified[member.name] = data
    # Verify every byte before creating the destination. Never use extractall.
    if args.destination:
        destination = args.destination.absolute()
        require(not destination.exists() and not destination.is_symlink(),
                "Destination must not already exist")
        for ancestor in destination.parents:
            require(not ancestor.is_symlink(), "Destination ancestry contains a symlink")
        destination.mkdir(parents=False, exist_ok=False)
        for name in names:
            output = destination.joinpath(*safe_name(name).parts)
            output.parent.mkdir(parents=True, exist_ok=True)
            for ancestor in output.parents:
                if ancestor == destination.parent:
                    break
                require(not ancestor.is_symlink(), "Extraction parent became a symlink")
            with output.open("xb") as stream:
                stream.write(verified[name])
            output.chmod(expected[name]["mode"])
    print(json.dumps({"status": "VERIFIED_AND_EXTRACTED" if args.destination else "VERIFIED",
                      "members": len(names), "member_bytes": sum(map(len, verified.values())),
                      "archive_sha256": receipt["archive"]["sha256"],
                      "source_execution": "NONE"}, sort_keys=True))


if __name__ == "__main__":
    main()
