#!/usr/bin/env python3
"""Verify and restore a single-file or multipart UTF-8 research evidence bundle."""

import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_bytes(data, expected_bytes, expected_sha256, label):
    require(len(data) == expected_bytes, f"{label}: byte count mismatch")
    require(hashlib.sha256(data).hexdigest() == expected_sha256,
            f"{label}: SHA-256 mismatch")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    outer = json.loads(args.package.read_bytes().decode("utf-8"))
    if outer["format"] == "p196-gzip-parts-utf8-files-v1":
        pieces = []
        names = set()
        for part in outer["payload_parts"]:
            name = part["path"]
            require(name and Path(name).name == name and name not in {".", ".."}
                    and "\\" not in name and name not in names,
                    f"Unsafe or duplicate payload part: {name!r}")
            names.add(name)
            data = (args.package.parent / name).read_bytes()
            check_bytes(data, part["bytes"], part["sha256"], name)
            pieces.append(data)
        encoded = b"".join(pieces)
    else:
        require(outer["format"] == "p196-gzip-utf8-files-v1", "Unknown package format")
        encoded = outer["payload_gzip_base64"]
    compressed = base64.b64decode(encoded, validate=True)
    check_bytes(compressed, outer["compressed_payload_bytes"],
                outer["compressed_payload_sha256"], "Compressed payload")
    payload = gzip.decompress(compressed)
    check_bytes(payload, outer["uncompressed_payload_bytes"],
                outer["uncompressed_payload_sha256"], "Uncompressed payload")
    inner = json.loads(payload.decode("utf-8"))
    require(inner["format"] == "utf8-files-v1", "Unknown inner format")
    require(len(inner["files"]) == outer["file_count"], "File count mismatch")
    verified = {}
    for entry in inner["files"]:
        name = entry["path"]
        relative = PurePosixPath(name)
        require(name and relative.parts and not relative.is_absolute() and str(relative) == name
                and ".." not in relative.parts and "\\" not in name,
                f"Unsafe or noncanonical path: {name!r}")
        require(name not in verified, f"Duplicate path: {name}")
        data = entry["content_utf8"].encode("utf-8")
        check_bytes(data, entry["bytes"], entry["sha256"], name)
        verified[name] = data
    for name in verified:
        for parent in PurePosixPath(name).parents:
            require(str(parent) not in verified, f"File/directory conflict: {name}")
    output = args.out.resolve()
    require(not output.exists(), "Output directory must not already exist")
    output.mkdir(parents=True)
    for name, data in verified.items():
        destination = output.joinpath(*PurePosixPath(name).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as stream:
            stream.write(data)
    print(json.dumps({"status": "RESTORED_AND_HASH_VERIFIED", "files": len(verified),
                      "output": str(output)}, sort_keys=True))


if __name__ == "__main__":
    main()
