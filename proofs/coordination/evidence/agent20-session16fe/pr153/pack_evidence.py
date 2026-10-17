#!/usr/bin/env python3
"""Deterministic PR153 evidence packaging and complete round-trip verification.

This program never invokes Lean, Git, a shell, or the network. Source files are
read only. Only generated .olean/.pyc/__pycache__ files are excluded, by exact
inventoried path. Use --verify-only to check a delivered package without inputs.
"""
from pathlib import Path, PurePosixPath
import argparse
import base64
import hashlib
import io
import json
import lzma
import os
import re
import resource
import shutil
import stat
import tarfile
import tempfile
from urllib.parse import urlparse


HERE = Path(__file__).resolve().parent
ROOT_NAMES = ("pr153-evidence", "pr153-verifier", "runtime-publication")
AUTHOR_ARCHIVE_SHA256 = "1b0639ca1b28442392cbbcf6b0c4a8d2f861b64873d43e92e6537b38c6b433ca"
MEMORY_CAP = 256 * 1024 * 1024
FILTERS = [{"id": lzma.FILTER_LZMA2, "preset": 6, "dict_size": 8 * 1024 * 1024}]
PATTERNS = {
    "private_key": rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    "github_token": rb"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b",
    "aws_access_key": rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "bearer_credential": rb"(?i)authorization[\"\s:]+bearer\s+[A-Za-z0-9._~+/-]{24,}",
    "signed_url": rb"(?i)https?[^\s\"<>]*[?&](?:x-amz-signature|x-goog-signature|signature|sig|token|access_token)=",
    "unrelated_prompt": rb"END_ROLE_PROMPT|BEGIN_ROLE_PROMPT|<environment_context>|<permissions instructions>",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def write_json(path, value):
    path.write_bytes(json_bytes(value))


def identity(path):
    size = path.stat().st_size
    sha = hashlib.sha256()
    git = hashlib.sha1(f"blob {size}\0".encode())
    observed = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            observed += len(block)
            sha.update(block)
            git.update(block)
    require(size == observed, "File size changed during hashing: " + str(path))
    return {"bytes": size, "sha256": sha.hexdigest(), "git_blob_sha1": git.hexdigest()}


def safe_name(name):
    path = PurePosixPath(name)
    require(name == str(path) and not path.is_absolute() and ".." not in path.parts,
            "Unsafe path: " + repr(name))
    require("\\" not in name and bool(path.parts), "Unsafe path: " + repr(name))
    return path


def scan_content(data, name, hosts):
    for label, expression in PATTERNS.items():
        require(re.search(expression, data) is None, "Content screening finding: " + label + " in " + name)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        require(hashlib.sha256(data).hexdigest() == AUTHOR_ARCHIVE_SHA256,
                "Unexpected binary payload: " + name)
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
            for member in archive:
                safe_name(member.name)
                require(member.isfile(), "Nonregular member in preserved author archive")
                scan_content(archive.extractfile(member).read(), name + "::" + member.name, hosts)
        return "preserved_original_author_gzip_archive"
    for match in re.finditer(r'https?://[^\s"<>`\\]+', text):
        parsed = urlparse(match.group())
        require(not parsed.query, "Unexpected URL query requiring review: " + name)
        require(not parsed.username and not parsed.password, "URL credentials: " + name)
        hosts.add(parsed.netloc)
    return "utf8"


def inventory(workspace, screen=False):
    included, excluded, cache_dirs = [], [], []
    hosts = set()
    for root_name in ROOT_NAMES:
        root = workspace / root_name
        require(root.is_dir() and not root.is_symlink(), "Missing or linked source root: " + root_name)
        for current, dirs, files in os.walk(root, followlinks=False):
            for name in sorted(dirs + files):
                path = Path(current) / name
                info = path.lstat()
                relative = str(path.relative_to(workspace))
                safe_name(relative)
                require(not stat.S_ISLNK(info.st_mode), "Symlink is not allowed: " + relative)
                require(stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode),
                        "Unexpected filesystem object: " + relative)
                if stat.S_ISDIR(info.st_mode):
                    if name == "__pycache__":
                        cache_dirs.append(relative)
                    continue
                row = {"path": relative, **identity(path), "source_mode": f"{stat.S_IMODE(info.st_mode):04o}"}
                if path.suffix == ".olean":
                    row["reason"] = "Generated Lean compiled object; reproducible runtime infrastructure; original retained unchanged."
                    excluded.append(row)
                elif path.suffix == ".pyc" or "__pycache__" in path.relative_to(workspace).parts:
                    row["reason"] = "Generated Python bytecode/cache infrastructure; original retained unchanged."
                    excluded.append(row)
                else:
                    row["archive_mode"] = "0644"
                    if screen:
                        row["content_kind"] = scan_content(path.read_bytes(), relative, hosts)
                    header = tarfile.TarInfo(relative)
                    header.size = row["bytes"]
                    header.tobuf(format=tarfile.USTAR_FORMAT)
                    included.append(row)
    included.sort(key=lambda row: row["path"])
    excluded.sort(key=lambda row: row["path"])
    return included, excluded, sorted(cache_dirs), sorted(hosts)


def verify_archive(stream, expected):
    rows = {row["path"]: row for row in expected}
    observed = []
    total = 0
    with lzma.LZMAFile(stream, "rb") as xz:
        with tarfile.open(fileobj=xz, mode="r|") as archive:
            for member in archive:
                safe_name(member.name)
                require(member.isfile() and not member.issparse(), "Nonregular archive member")
                require(member.name in rows and member.name not in observed, "Unexpected or duplicate member")
                require(member.uid == member.gid == member.mtime == 0 and member.mode == 0o644,
                        "Nondeterministic archive metadata")
                require(member.uname == member.gname == "", "Unexpected archive owner names")
                entry = rows[member.name]
                require(member.size == entry["bytes"], "Archive member length mismatch")
                sha = hashlib.sha256()
                git = hashlib.sha1(f"blob {member.size}\0".encode())
                count = 0
                source = archive.extractfile(member)
                for block in iter(lambda: source.read(1024 * 1024), b""):
                    count += len(block)
                    sha.update(block)
                    git.update(block)
                require(count == entry["bytes"] and sha.hexdigest() == entry["sha256"]
                        and git.hexdigest() == entry["git_blob_sha1"], "Archive member byte identity mismatch")
                total += count
                observed.append(member.name)
    require(observed == sorted(rows), "Archive order or complete member inventory mismatch")
    return {"regular_members": len(observed), "payload_bytes": total,
            "all_paths_sizes_sha256_git_blobs_match": True, "unsafe_or_unlisted_members": 0}


def verify_roundtrip(output, payload):
    archive = output / "evidence.tar.xz"
    encoded = output / "evidence.tar.xz.b64"
    original_identity = identity(archive)
    with archive.open("rb") as source:
        direct = verify_archive(source, payload["files"])
    digest = hashlib.sha256()
    git = hashlib.sha1(f"blob {original_identity['bytes']}\0".encode())
    decoded_size = 0
    lines = 0
    with tempfile.TemporaryFile(dir=output) as decoded:
        with encoded.open("rb") as source:
            for line in source:
                require(line.endswith(b"\n") and 1 <= len(line.rstrip(b"\n")) <= 76,
                        "Invalid Base64 wrapping")
                raw = base64.b64decode(line.rstrip(b"\n"), validate=True)
                require(base64.b64encode(raw) == line.rstrip(b"\n"), "Noncanonical Base64")
                decoded.write(raw)
                digest.update(raw)
                git.update(raw)
                decoded_size += len(raw)
                lines += 1
        require(decoded_size == original_identity["bytes"]
                and digest.hexdigest() == original_identity["sha256"]
                and git.hexdigest() == original_identity["git_blob_sha1"], "Base64 round-trip mismatch")
        decoded.seek(0)
        repeated = verify_archive(decoded, payload["files"])
    require(direct == repeated, "Round-trip archive verification differs")
    return {"status": "PASS_COMPLETE_ARCHIVE_AND_BASE64_ROUNDTRIP", "direct_archive": direct,
            "decoded_archive": repeated, "decoded_archive_identity": original_identity,
            "base64_lines": lines, "base64_wrap_columns": 76, "lean_executed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=HERE.parent)
    parser.add_argument("--output", type=Path, default=HERE)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    cap = MEMORY_CAP if soft == resource.RLIM_INFINITY else min(soft, MEMORY_CAP)
    resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
    output = args.output.resolve()
    workspace = args.workspace.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if args.verify_only:
        manifest = json.loads((output / "ARCHIVE_MANIFEST.json").read_text())
        for artifact in manifest["packaging_artifacts"]:
            require(identity(output / artifact["path"]) == {key: artifact[key] for key in
                    ("bytes", "sha256", "git_blob_sha1")}, "Delivered artifact differs: " + artifact["path"])
        payload = json.loads((output / "PAYLOAD_MANIFEST.json").read_text())
        print(json.dumps(verify_roundtrip(output, payload), indent=2))
        return
    reserved = ["evidence.tar.xz", "evidence.tar.xz.b64", "PAYLOAD_MANIFEST.json",
                "ARCHIVE_MANIFEST.json", "PACKING_VERIFICATION.json"]
    require(not any((output / name).exists() for name in reserved), "Refusing to overwrite a prior package")
    if output != HERE:
        for name in ["pack_evidence.py", "README.md"]:
            require(not (output / name).exists(), "Refusing to overwrite packaging metadata")
            shutil.copyfile(HERE / name, output / name)
    included, excluded, cache_dirs, hosts = inventory(workspace, screen=True)
    paths = {row["path"] for row in included}
    for essential in ["pr153-verifier/VERIFICATION_REPORT.md",
                      "pr153-evidence/source/evidence/development-20261016.tar.gz",
                      "pr153-verifier/audit-continuation/portable/verify_pr153.py"]:
        require(essential in paths, "Required substantive payload missing: " + essential)
    payload = {"schema": 1, "repository": "taco-jpg/p196-algorithm", "pr": 153,
               "source_head": "6641b1ea166fcef0e6f9d1fa23afed7b1f6b8a82",
               "observed_base": "74a1c3922eb7af438fe40b23d2105ad07556e3f5",
               "combined_tree": "6cfa3582ce49216a0fc055f42dba84532a608407",
               "source_roots": list(ROOT_NAMES), "file_count": len(included),
               "payload_bytes": sum(row["bytes"] for row in included), "files": included,
               "excluded_file_count": len(excluded), "excluded_bytes": sum(row["bytes"] for row in excluded),
               "excluded_files": excluded, "excluded_cache_directories": cache_dirs,
               "source_files_deleted": False, "content_screening": {
                   "symlinks_or_nonregular_inputs": 0, "unexpected_binary_inputs": 0,
                   "credential_or_unrelated_prompt_pattern_hits": 0,
                   "urls_with_queries_or_credentials": 0, "observed_url_hosts": hosts}}
    write_json(output / "PAYLOAD_MANIFEST.json", payload)
    archive_path = output / "evidence.tar.xz"
    with archive_path.open("wb") as raw:
        with lzma.LZMAFile(raw, "wb", format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, filters=FILTERS) as xz:
            with tarfile.open(fileobj=xz, mode="w|", format=tarfile.USTAR_FORMAT) as archive:
                for row in included:
                    member = tarfile.TarInfo(row["path"])
                    member.size = row["bytes"]
                    member.uid = member.gid = member.mtime = 0
                    member.mode = 0o644
                    member.uname = member.gname = ""
                    member.type = tarfile.REGTYPE
                    with (workspace / row["path"]).open("rb") as source:
                        archive.addfile(member, source)
    with archive_path.open("rb") as raw, (output / "evidence.tar.xz.b64").open("wb") as encoded:
        for block in iter(lambda: raw.read(57 * 1024), b""):
            text = base64.b64encode(block)
            for pos in range(0, len(text), 76):
                encoded.write(text[pos:pos + 76] + b"\n")
    final_included, final_excluded, final_cache_dirs, _ = inventory(workspace)
    comparable = lambda rows: [{key: value for key, value in row.items() if key != "content_kind"} for row in rows]
    require(comparable(included) == final_included and excluded == final_excluded
            and cache_dirs == final_cache_dirs, "Frozen source inventory changed during packing")
    verification = verify_roundtrip(output, payload)
    verification["source_inventory_rechecked_after_packing"] = True
    verification["source_file_count_including_excluded"] = len(included) + len(excluded)
    verification["process_address_space_cap_bytes"] = cap
    write_json(output / "PACKING_VERIFICATION.json", verification)
    names = ["README.md", "pack_evidence.py", "PAYLOAD_MANIFEST.json", "PACKING_VERIFICATION.json",
             "evidence.tar.xz", "evidence.tar.xz.b64"]
    manifest = {"schema": 1, "status": "FROZEN_COMPLETE_VERIFIED_PACKAGE", "archive": {
                    "path": "evidence.tar.xz", **identity(archive_path), "tar_format": "USTAR",
                    "member_type": "regular_files_only", "member_order": "lexicographic_path",
                    "member_count": len(included), "payload_bytes": payload["payload_bytes"],
                    "uid": 0, "gid": 0, "uname": "", "gname": "", "mtime": 0, "mode": "0644",
                    "compression": "XZ / LZMA2 / CRC64", "lzma2_preset": 6,
                    "lzma2_dictionary_bytes": 8 * 1024 * 1024,
                    "process_address_space_cap_bytes": cap},
                "base64": {"path": "evidence.tar.xz.b64", **identity(output / "evidence.tar.xz.b64"),
                           "wrap_columns": 76, "line_ending": "LF", "final_newline": True},
                "packaging_artifacts": [{"path": name, **identity(output / name)} for name in names],
                "manifest_self_reference": "ARCHIVE_MANIFEST.json is the seventh packaging artifact; it is excluded only from its own hash list.",
                "scope_exclusion": "Coordinator-created INTEGRATION_PACKET.md and delivery context are separate; this script never reads or changes them.",
                "freeze": "All seven packaging files are made read-only after validation; source inputs remain unchanged.",
                "no_remote_writes": True, "lean_executed": False}
    write_json(output / "ARCHIVE_MANIFEST.json", manifest)
    for name in names + ["ARCHIVE_MANIFEST.json"]:
        (output / name).chmod(0o444)
    print(json.dumps({"status": manifest["status"], "payload_files": len(included),
                      "payload_bytes": payload["payload_bytes"], "excluded_files": len(excluded),
                      "excluded_bytes": payload["excluded_bytes"], "archive": manifest["archive"],
                      "base64": manifest["base64"]}, indent=2))


if __name__ == "__main__":
    main()
