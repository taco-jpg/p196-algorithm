#!/usr/bin/env python3
"""Safely recover and verify the three frozen follow-up evidence roots."""
import argparse
import base64
import hashlib
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import re
import resource
import stat
import tarfile
import traceback

CHUNK = 1024 * 1024
LIMIT = 1024 ** 3
ROOT_NAMES = {"pr148-replay-evidence", "pr155-delivery", "pr167-evidence"}


def safe_path(value):
    if not isinstance(value, str) or not value or "\\" in value or "\0" in value:
        raise ValueError("Invalid relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or value != path.as_posix() or any(x in (".", "..") for x in path.parts):
        raise ValueError("Unsafe or noncanonical relative path")
    return path


def file_identity(path):
    size = path.stat().st_size
    sha = hashlib.sha256()
    blob = hashlib.sha1(b"blob " + str(size).encode() + b"\0")
    with path.open("rb") as stream:
        for data in iter(lambda: stream.read(CHUNK), b""):
            sha.update(data)
            blob.update(data)
    return {"bytes": size, "sha256": sha.hexdigest(), "git_blob": blob.hexdigest()}


def check_identity(path, record):
    actual = file_identity(path)
    for key in ("bytes", "sha256", "git_blob"):
        if key in record and actual[key] != record[key]:
            raise ValueError(f"File identity mismatch: {path.name} ({key})")
    return actual


def validate_records(records, kind):
    result = {}
    for record in records:
        path = safe_path(record["path"])
        if path.parts[0] not in ROOT_NAMES or path.as_posix() in result:
            raise ValueError("Unexpected root or duplicate manifest path")
        if type(record["mode"]) is not int or not 0 <= record["mode"] <= 0o777:
            raise ValueError("Unsupported permission mode")
        if kind == "file":
            if len(path.parts) < 2 or type(record["bytes"]) is not int or record["bytes"] < 0:
                raise ValueError("Invalid file size or path")
            if not re.fullmatch(r"[0-9a-f]{64}", record["sha256"]):
                raise ValueError("Invalid file digest")
            if record["tar_member"] != path.as_posix():
                raise ValueError("Tar member and original relative path differ")
        result[path.as_posix()] = record
    return result


def reconstruct_parts(directory, destination, manifest):
    output_path = destination / "_reconstructed-followup-evidence.tar.xz"
    written = 0
    parts = manifest["base64"]["parts"]
    if len(parts) != manifest["base64"]["parts_count"]:
        raise ValueError("Base64 part count mismatch")
    with output_path.open("xb") as output:
        for index, part in enumerate(parts, 1):
            if part["index"] != index or part["decoded_offset"] != written:
                raise ValueError("Invalid part index or decoded offset")
            path = directory / safe_path(part["path"])
            if path.is_symlink() or path.stat().st_size > 524288:
                raise ValueError("Unsafe or oversized part")
            encoded = path.read_bytes()
            if not encoded.isascii() or len(encoded) != part["bytes"] or len(encoded) != part["characters"]:
                raise ValueError("Invalid ASCII base64 part size")
            if hashlib.sha256(encoded).hexdigest() != part["sha256"]:
                raise ValueError("Base64 part digest mismatch")
            decoded = base64.b64decode(encoded, validate=True)
            if len(decoded) != part["decoded_bytes"] or hashlib.sha256(decoded).hexdigest() != part["decoded_sha256"]:
                raise ValueError("Decoded part identity mismatch")
            output.write(decoded)
            written += len(decoded)
    check_identity(output_path, manifest["archive"])
    return output_path


def decompress_checked(archive_path, destination, manifest):
    target = destination / "_verified-transport.tar"
    expected = manifest["archive"]["uncompressed_tar"]
    ceiling = manifest["payload_bytes"] + 4096 * (manifest["payload_count"] + len(manifest["directories"])) + 10240
    if type(expected["bytes"]) is not int or not 0 < expected["bytes"] <= ceiling:
        raise ValueError("Unreasonable decompressed archive size")
    decoder = lzma.LZMADecompressor(format=lzma.FORMAT_XZ, memlimit=64 * 1024 ** 2)
    total = 0
    with archive_path.open("rb") as source, target.open("xb") as output:
        for compressed in iter(lambda: source.read(CHUNK), b""):
            if decoder.eof:
                raise ValueError("Trailing compressed bytes or multiple XZ streams")
            data = decoder.decompress(compressed, max_length=CHUNK)
            while True:
                total += len(data)
                if total > expected["bytes"]:
                    raise ValueError("Decompressed size exceeds the manifest")
                output.write(data)
                if decoder.eof or decoder.needs_input:
                    break
                data = decoder.decompress(b"", max_length=CHUNK)
            if decoder.eof and decoder.unused_data:
                raise ValueError("Trailing data after the XZ stream")
    if not decoder.eof or decoder.check != lzma.CHECK_CRC64:
        raise ValueError("Incomplete XZ stream or unexpected integrity check")
    check_identity(target, expected)
    return target


def recover(manifest_path, destination, from_parts):
    manifest = json.loads(manifest_path.read_text())
    directory = manifest_path.resolve().parent
    files = validate_records(manifest["payloads"], "file")
    directories = validate_records(manifest["directories"], "directory")
    if set(files) & set(directories) or not ROOT_NAMES.issubset(directories):
        raise ValueError("File/directory collision or missing evidence root")
    if len(files) != manifest["payload_count"] or sum(x["bytes"] for x in files.values()) != manifest["payload_bytes"]:
        raise ValueError("Manifest payload totals disagree")
    for path in [*files, *directories]:
        parent = PurePosixPath(path).parent.as_posix()
        if parent != "." and parent not in directories:
            raise ValueError("Manifest omits a parent directory")
    if not destination.is_absolute() or destination.parent.resolve() != destination.parent:
        raise ValueError("Destination must be absolute under an existing, resolved parent")
    if destination.exists() or destination.is_symlink():
        raise FileExistsError("Recovery destination must be new")
    destination.mkdir(parents=False, mode=0o700)
    archive_path = directory / safe_path(manifest["archive"]["path"])
    if from_parts:
        archive_path = reconstruct_parts(directory, destination, manifest)
    if archive_path.is_symlink():
        raise ValueError("Archive must be a regular local file")
    check_identity(archive_path, manifest["archive"])
    tar_path = decompress_checked(archive_path, destination, manifest)
    seen = set()
    with tarfile.open(tar_path, mode="r:") as archive:
        for member in archive:
            name = safe_path(member.name).as_posix()
            if name in seen or name not in files and name not in directories:
                raise ValueError("Duplicate or unlisted tar member")
            record = files.get(name, directories.get(name))
            if member.mode != record["mode"] or member.uid != 0 or member.gid != 0 or member.mtime != 0 or member.uname or member.gname:
                raise ValueError("Tar metadata differs from deterministic manifest")
            if member.linkname or member.sparse is not None or set(member.pax_headers) - {"path"}:
                raise ValueError("Unexpected link, sparse content, or extended tar metadata")
            target = destination / safe_path(name)
            if name in directories:
                if member.type != tarfile.DIRTYPE or member.size != 0:
                    raise ValueError("Directory member type or size mismatch")
                target.mkdir(mode=0o700)
            else:
                if member.type != tarfile.REGTYPE or member.size != record["bytes"]:
                    raise ValueError("File member type or size mismatch")
                if not target.parent.is_dir() or target.parent.is_symlink():
                    raise ValueError("Unsafe or missing parent directory")
                fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
                source = archive.extractfile(member)
                if source is None:
                    os.close(fd)
                    raise ValueError("Missing regular member data")
                total = 0
                with source, os.fdopen(fd, "wb") as output:
                    for data in iter(lambda: source.read(CHUNK), b""):
                        total += len(data)
                        if total > record["bytes"]:
                            raise ValueError("Member exceeds declared size")
                        output.write(data)
                check_identity(target, record)
                os.chmod(target, record["mode"])
            seen.add(name)
    if seen != set(files) | set(directories):
        raise ValueError("Archive is missing required members")
    for name in sorted(directories, key=lambda x: (len(PurePosixPath(x).parts), x), reverse=True):
        os.chmod(destination / safe_path(name), directories[name]["mode"])
    actual_files = set()
    actual_directories = set()
    for root_name in sorted(ROOT_NAMES):
        root = destination / root_name
        for path in [root, *sorted(root.rglob("*"))]:
            name = path.relative_to(destination).as_posix()
            metadata = path.lstat()
            if stat.S_ISDIR(metadata.st_mode):
                actual_directories.add(name)
                expected_mode = directories[name]["mode"]
            elif stat.S_ISREG(metadata.st_mode):
                actual_files.add(name)
                check_identity(path, files[name])
                expected_mode = files[name]["mode"]
            else:
                raise ValueError("Recovered unexpected special file")
            if stat.S_IMODE(metadata.st_mode) != expected_mode:
                raise ValueError("Recovered permission mode mismatch")
    if actual_files != set(files) or actual_directories != set(directories):
        raise ValueError("Recovered filesystem inventory differs from manifest")
    return {"status": "PASS", "verified_payload_count": len(files),
            "verified_payload_bytes": manifest["payload_bytes"], "verified_directories": len(directories),
            "archive": manifest["archive"], "recovered_from_base64_parts": from_parts,
            "destination": str(destination), "address_space_limit_bytes": LIMIT,
            "decoder_memory_limit_bytes": 64 * 1024 ** 2,
            "peak_resident_set_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "security": "Exact allowlist; canonical paths; no extractall; reject links, sparse/device members, duplicates and traversal; exclusive files in a new destination; full CRC64 stream and tar hash validation; disk rehash of every recovered file and mode."}


def main():
    resource.setrlimit(resource.RLIMIT_AS, (LIMIT, LIMIT))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--from-parts", action="store_true")
    args = parser.parse_args()
    destination_existed = args.destination.exists() or args.destination.is_symlink()
    try:
        result = recover(args.manifest, args.destination, args.from_parts)
    except BaseException as error:
        failure = {"status": "FAIL", "error": str(error), "traceback": traceback.format_exc(),
                   "preservation": "No files deleted; partial recovery remains available for inspection."}
        if not destination_existed and args.destination.is_dir():
            with (args.destination / "_recovery-failure.json").open("x") as stream:
                json.dump(failure, stream, indent=2)
        raise
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
