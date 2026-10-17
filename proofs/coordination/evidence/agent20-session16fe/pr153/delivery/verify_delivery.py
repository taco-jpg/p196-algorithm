#!/usr/bin/env python3
"""Verify or safely recover the PR153 delivery package using only the standard library."""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import resource
import tarfile


def require(condition, message):
    if not condition:
        raise ValueError(message)


def identity(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob_sha1": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def safe_name(name):
    path = PurePosixPath(name)
    require(bool(name) and not path.is_absolute() and str(path) == name,
            "Noncanonical or absolute archive path")
    require(not any(part in ("", ".", "..") for part in path.parts) and "\\" not in name,
            "Unsafe archive path")
    return path


def verify_members(data, entries):
    expected = {entry["path"]: entry for entry in entries}
    require(len(expected) == len(entries), "Duplicate manifest path")
    require(list(expected) == sorted(expected), "Unsorted payload manifest")
    result = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:xz") as archive:
        for member in archive:
            safe_name(member.name)
            require(member.name not in result and member.name in expected, "Unexpected/duplicate member")
            require(member.isreg() and member.type == tarfile.REGTYPE and not member.linkname,
                    "Nonregular member")
            require(member.uid == member.gid == member.mtime == 0 and member.mode == 0o644,
                    "Unexpected deterministic member metadata")
            require(member.uname == member.gname == "" and not member.pax_headers,
                    "Unexpected owner or extended metadata")
            entry = expected[member.name]
            require(member.size == entry["bytes"], "Member size mismatch")
            stream = archive.extractfile(member)
            require(stream is not None, "Unreadable archive member")
            content = stream.read(entry["bytes"] + 1)
            require(identity(content) == {key: entry[key] for key in identity(content)},
                    "Member identity mismatch: " + member.name)
            result[member.name] = content
    require(list(result) == list(expected), "Archive order or complete membership mismatch")
    return result


def verify(package, extract=None):
    manifest = load_json(package / "ARCHIVE_MANIFEST.json")
    require(manifest["self_exclusion"] == "Only ARCHIVE_MANIFEST.json omits its own identity to avoid self-reference.",
            "Unexpected manifest self-exclusion")
    artifacts = {entry["path"]: entry for entry in manifest["artifacts"]}
    require(len(artifacts) == len(manifest["artifacts"]), "Duplicate artifact identity")
    b64 = (package / "delivery-evidence.tar.xz.b64").read_bytes()
    require(b64.endswith(b"\n") and b"\r" not in b64, "Base64 LF formatting mismatch")
    lines = b64.splitlines()
    require(lines and all(len(line) == 76 for line in lines[:-1]) and 1 <= len(lines[-1]) <= 76,
            "Base64 wrapping mismatch")
    decoded = base64.b64decode(b"".join(lines), validate=True)
    require(base64.encodebytes(decoded) == b64, "Noncanonical Base64 encoding")
    for name, entry in artifacts.items():
        safe_name(name)
        path = package / name
        require(not path.is_symlink(), "Symlink package artifact")
        content = decoded if name == "delivery-evidence.tar.xz" and not path.exists() else path.read_bytes()
        require(identity(content) == {key: entry[key] for key in identity(content)},
                "Package artifact identity mismatch: " + name)
    require(identity(decoded) == manifest["archive_identity"], "Decoded archive identity mismatch")
    archive_path = package / "delivery-evidence.tar.xz"
    direct = archive_path.read_bytes() if archive_path.exists() else decoded
    require(direct == decoded, "Raw and decoded archive differ")
    payload = load_json(package / "PAYLOAD_MANIFEST.json")
    members = verify_members(direct, payload["files"])
    decoded_members = verify_members(decoded, payload["files"])
    require(members == decoded_members, "Decoded member round trip differs")
    require(len(members) == payload["file_count"] == manifest["member_count"], "Member count mismatch")
    require(sum(map(len, members.values())) == payload["total_bytes"], "Payload byte count mismatch")
    if extract is not None:
        require(not extract.exists() and not extract.is_symlink(), "Extraction destination already exists")
        extract.mkdir(parents=True, exist_ok=False)
        for name, content in members.items():
            destination = extract.joinpath(*safe_name(name).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as output:
                output.write(content)
            require(identity(destination.read_bytes()) == identity(content), "Extraction round trip mismatch")
    return {"status": "PASS", "archive": identity(decoded), "members": len(members),
            "payload_bytes": payload["total_bytes"], "metadata_artifacts_verified": len(artifacts),
            "raw_archive_present": archive_path.exists(), "base64_roundtrip": True,
            "member_roundtrip": True, "extracted": str(extract) if extract is not None else None,
            "network_used": False, "lean_executed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--extract", type=Path)
    args = parser.parse_args()
    _, hard = resource.getrlimit(resource.RLIMIT_AS)
    limit = 256 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (limit if hard < 0 else min(limit, hard), hard))
    print(json.dumps(verify(args.package, args.extract), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
