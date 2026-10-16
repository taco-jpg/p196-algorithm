#!/usr/bin/env python3
"""Verify the evidence archive; optionally restore missing files without overwrites."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tarfile


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    if not isinstance(name, str) or not name or "\\" in name or "\0" in name:
        raise ValueError("invalid archive path")
    p = PurePosixPath(name)
    if not p.parts or p.is_absolute() or p.as_posix() != name or any(x in (".", "..") for x in p.parts):
        raise ValueError("non-relative or non-normalized archive path: " + name)
    return p


def verified_payloads(archive, manifest):
    info = manifest["archive"]
    raw = archive.read_bytes()
    if len(raw) != info["bytes"] or sha256(raw) != info["sha256"]:
        raise ValueError("archive size or SHA256 mismatch")
    expected = {}
    for row in manifest["members"]:
        name = row["path"]
        safe_name(name)
        if name in expected or not isinstance(row["bytes"], int) or row["bytes"] < 0:
            raise ValueError("duplicate member or invalid size: " + name)
        if not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]):
            raise ValueError("invalid member SHA256: " + name)
        expected[name] = row
    for name in expected:
        if any(str(parent) in expected for parent in PurePosixPath(name).parents):
            raise ValueError("file and directory path collision: " + name)
    payloads = {}
    with tarfile.open(archive, "r:gz") as tar:
        for member in tar:
            name = member.name
            safe_name(name)
            if not member.isfile() or name in payloads or name not in expected:
                raise ValueError("unexpected, duplicate, or non-regular member: " + name)
            row = expected[name]
            if member.size != row["bytes"]:
                raise ValueError("member size mismatch: " + name)
            stream = tar.extractfile(member)
            if stream is None:
                raise ValueError("unreadable member: " + name)
            with stream:
                data = stream.read()
            if len(data) != row["bytes"] or sha256(data) != row["sha256"]:
                raise ValueError("member SHA256 mismatch: " + name)
            payloads[name] = data
    if set(payloads) != set(expected):
        raise ValueError("archive member set does not match manifest")
    if len(payloads) != info["member_count"]:
        raise ValueError("archive member count mismatch")
    return payloads


def lstat_or_none(path):
    try:
        return path.lstat()
    except FileNotFoundError:
        return None


def check_parent_directories(path):
    for parent in reversed(path.parents):
        st = lstat_or_none(parent)
        if st is not None and not stat.S_ISDIR(st.st_mode):
            raise ValueError("symlink or non-directory ancestor: " + str(parent))


def existing_identical(path, data):
    st = lstat_or_none(path)
    if st is None:
        return False
    if not stat.S_ISREG(st.st_mode) or path.read_bytes() != data:
        raise ValueError("refusing to overwrite existing different file: " + str(path))
    return True


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=here / "final-independent.tar.gz")
    parser.add_argument("--manifest", type=Path, default=here / "final-independent-manifest.json")
    parser.add_argument("--extract-to", type=Path,
                        help="repository root or new directory; absent means verify only")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1:
        raise ValueError("unsupported manifest version")
    payloads = verified_payloads(args.archive, manifest)
    written = skipped = 0
    if args.extract_to is not None:
        root = args.extract_to.absolute()
        # Check EVERY destination before creating any file or directory.
        for name, data in payloads.items():
            dest = root.joinpath(*safe_name(name).parts)
            check_parent_directories(dest)
            existing_identical(dest, data)
        for name, data in payloads.items():
            dest = root.joinpath(*safe_name(name).parts)
            check_parent_directories(dest)
            if existing_identical(dest, data):
                skipped += 1
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            check_parent_directories(dest)
            # Exclusive creation also refuses files appearing after the preflight.
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
            with os.fdopen(os.open(dest, flags, 0o644), "wb") as out:
                out.write(data)
            written += 1
    print(json.dumps({"status": "PASS", "members_verified": len(payloads),
                      "archive_sha256": manifest["archive"]["sha256"],
                      "files_written": written, "identical_files_skipped": skipped}))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, tarfile.TarError) as error:
        print("FAIL: " + str(error), file=sys.stderr)
        sys.exit(1)
