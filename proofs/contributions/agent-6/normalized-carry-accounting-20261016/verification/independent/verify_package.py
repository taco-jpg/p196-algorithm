#!/usr/bin/env python3
"""Verify packaged evidence bytes. Does not execute Lean or extract any files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tarfile


def check_bytes(data: bytes, record: dict, label: str) -> None:
    actual = {
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "git_blob_sha1": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
    }
    for key, value in actual.items():
        if value != record[key]:
            raise RuntimeError(f"{label}: {key} mismatch")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--check-extracted", type=Path, help="Optional directory containing the extracted normalized-carry-review folder")
    args = parser.parse_args()
    root = args.directory.resolve()
    manifest = json.loads((root / "PORTABLE_MANIFEST.json").read_text())
    archive_path = root / manifest["archive"]["file"]
    check_bytes(archive_path.read_bytes(), manifest["archive"], str(archive_path))
    selected = manifest["included"]
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        if [m.name for m in members] != [r["archive_member"] for r in selected]:
            raise RuntimeError("Archive member inventory differs from manifest")
        for member, record in zip(members, selected):
            if not member.isfile():
                raise RuntimeError(f"Nonregular member: {member.name}")
            path = Path(member.name)
            if path.is_absolute() or ".." in path.parts or path.parts[0] != manifest["archive_root"]:
                raise RuntimeError(f"Invalid member path: {member.name}")
            stream = archive.extractfile(member)
            if stream is None:
                raise RuntimeError(f"Unreadable member: {member.name}")
            check_bytes(stream.read(), record, member.name)
            if args.check_extracted is not None:
                extracted = args.check_extracted / member.name
                check_bytes(extracted.read_bytes(), record, str(extracted))
    for record in manifest["readable_copies"]:
        check_bytes((root / record["file"]).read_bytes(), record, record["file"])
    if len(selected) != manifest["included_file_count"]:
        raise RuntimeError("Selected file count mismatch")
    if sum(r["bytes"] for r in selected) != manifest["included_original_byte_total"]:
        raise RuntimeError("Selected byte total mismatch")
    print(json.dumps({
        "status": "PASS_ARCHIVE_AND_READABLE_COPY_BYTE_VERIFICATION",
        "actual_remote_source_commit": manifest["actual_remote_source_commit"],
        "archive_sha256": manifest["archive"]["sha256"],
        "archive_bytes": manifest["archive"]["bytes"],
        "member_count": len(selected),
        "member_bytes": sum(r["bytes"] for r in selected),
        "readable_copy_count": len(manifest["readable_copies"]),
        "extracted_files_checked": args.check_extracted is not None,
        "lean_executed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
