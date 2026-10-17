#!/usr/bin/env python3
"""Strict, non-executing recovery of PR151 delivery evidence into a NEW directory."""
import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import stat
import tarfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def gitblob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def check(data, record, label):
    for key, actual in [("bytes", len(data)), ("sha256", sha(data)), ("git_blob", gitblob(data))]:
        if key in record and actual != record[key]:
            raise ValueError(f"{label}: {key} mismatch")


def safe_name(name, root):
    p = PurePosixPath(name)
    if p.is_absolute() or ".." in p.parts or not p.parts or p.parts[0] != root:
        raise ValueError(f"Unsafe member path: {name}")
    if str(p) != name or "\\" in name:
        raise ValueError(f"Noncanonical member path: {name}")
    return p


def recover(manifest_path, destination):
    transport = json.loads(manifest_path.read_text())
    base = manifest_path.parent
    destination = destination.absolute()
    if destination.exists():
        raise ValueError("Destination must not exist; recovery never overwrites files")
    encoded = bytearray()
    for rec in transport["parts"]:
        if Path(rec["path"]).name != rec["path"]:
            raise ValueError("Part path must be a single filename")
        data = (base / rec["path"]).read_bytes()
        check(data, rec, rec["path"])
        if len(data) > 240000 or any(c in data for c in b" \t\r\n"):
            raise ValueError("Invalid wrapped or oversize base64 part")
        encoded.extend(data)
    packed = base64.b64decode(encoded, validate=True)
    check(packed, transport["archive"], "decoded archive")
    root = transport["archive_root"]
    with tarfile.open(fileobj=io.BytesIO(packed), mode="r:xz") as tf:
        members = tf.getmembers()
        by_name = {}
        for member in members:
            safe_name(member.name, root)
            if not member.isfile() or member.name in by_name:
                raise ValueError("Archive must contain unique regular files only")
            if member.mode & ~0o777:
                raise ValueError("Special mode bits are forbidden")
            by_name[member.name] = member
        cm = transport["content_manifest"]
        content_data = tf.extractfile(by_name[cm["archive_path"]]).read()
        check(content_data, cm, "embedded content manifest")
        records = json.loads(content_data)["records"] + [cm]
        if set(by_name) != {r["archive_path"] for r in records} or len(records) != len(by_name):
            raise ValueError("Archive member set differs from manifest")
        if len(records) != transport["regular_member_count"]:
            raise ValueError("Regular member count mismatch")
        # Validate every member before creating the destination; never extract links.
        for rec in records:
            member = by_name[rec["archive_path"]]
            check(tf.extractfile(member).read(), rec, member.name)
            if format(member.mode, "04o") != rec["mode"]:
                raise ValueError(f"Mode mismatch: {member.name}")
        destination.mkdir(parents=True, exist_ok=False)
        for rec in records:
            member = by_name[rec["archive_path"]]
            target = destination.joinpath(*safe_name(member.name, root).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as handle:
                handle.write(tf.extractfile(member).read())
            os.chmod(target, member.mode)
        actual_files = sorted(str(p.relative_to(destination)) for p in destination.rglob("*") if p.is_file())
        if actual_files != sorted(by_name):
            raise ValueError("Recovered file set mismatch")
        for rec in records:
            target = destination / rec["archive_path"]
            check(target.read_bytes(), rec, str(target))
            if format(stat.S_IMODE(target.stat().st_mode), "04o") != rec["mode"]:
                raise ValueError(f"Recovered mode mismatch: {target}")
    receipt = {
        "status": "PASS_ACTUAL_RECOVERY_ALL_MEMBERS_ALL_BYTES_AND_MODES",
        "archive": transport["archive"],
        "regular_member_count": len(records),
        "recovered_bytes": sum(r["bytes"] for r in records),
        "strict_base64_roundtrip": True,
        "archive_member_set_exact": True,
        "all_member_bytes_sha256_gitblob_and_modes_verified": True,
        "destination": str(destination),
        "research_or_verifier_scripts_executed": 0,
        "lean_invocations": 0,
    }
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(recover(args.manifest, args.destination), indent=2, sort_keys=True))
