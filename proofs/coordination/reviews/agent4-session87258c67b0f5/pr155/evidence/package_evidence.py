#!/usr/bin/env python3
"""Create a deterministic, lossless PR155 publication after explicit freeze."""
import argparse
import base64
import datetime
import hashlib
import json
import lzma
import os
from pathlib import Path
import platform
import resource
import stat
import subprocess
import sys
import tarfile
import traceback

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "pr155-evidence"
BASELINE = ROOT.parent / "pr155-publication"
ADDRESS_SPACE_LIMIT = 1536 * 1024 * 1024
ARCHIVE_NAME = "pr155-evidence.tar.xz"
MANIFEST_NAME = "publication-manifest.json"
CHUNK = 1024 * 1024
BASE64_LIMIT = 524288
FILTERS = [{"id": lzma.FILTER_LZMA2, "dict_size": 64 * 1024 * 1024,
            "mode": lzma.MODE_NORMAL, "mf": lzma.MF_BT4,
            "nice_len": 64, "depth": 0}]


def digest_file(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for data in iter(lambda: stream.read(CHUNK), b""):
            h.update(data)
    return h.hexdigest()


def write_json(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def excluded_reason(relative):
    parts = relative.parts
    if parts[:2] == ("combined-tree-review", "objects"):
        return "Regenerable private Git merge-tree object database; commands, inputs, tree identities, manifests, complete patches, and raw tree listings are retained."
    if "__pycache__" in parts:
        return "Regenerable Python bytecode cache; Python sources are retained."
    if relative.suffix in (".olean", ".ilean"):
        return "Regenerable Lean compiled artifact; sources, compiler instructions, substantive logs, failures, and audit evidence are retained."
    return None


def scan():
    payloads, excluded, directories = [], [], []
    for current, dirs, files in os.walk(SOURCE, followlinks=False):
        current = Path(current)
        for name in sorted(dirs):
            path = current / name
            relative = path.relative_to(SOURCE)
            if path.is_symlink():
                raise RuntimeError(f"Unexpected symbolic link directory: {relative}")
            directories.append(relative.as_posix())
        for name in sorted(files):
            path = current / name
            relative = path.relative_to(SOURCE)
            metadata = path.lstat()
            if not stat.S_ISREG(metadata.st_mode):
                raise RuntimeError(f"Unexpected nonregular evidence member: {relative}")
            record = {"path": relative.as_posix(), "bytes": metadata.st_size,
                      "sha256": digest_file(path), "mode": stat.S_IMODE(metadata.st_mode)}
            reason = excluded_reason(relative)
            if reason:
                record["reason"] = reason
                excluded.append(record)
            else:
                record["tar_member"] = "pr155-evidence/" + relative.as_posix()
                record["stored_path"] = ARCHIVE_NAME
                payloads.append(record)
    payloads.sort(key=lambda entry: entry["path"])
    excluded.sort(key=lambda entry: entry["path"])
    return payloads, excluded, sorted(directories)


class CheckedReader:
    def __init__(self, stream):
        self.stream = stream
        self.hash = hashlib.sha256()
        self.bytes = 0

    def read(self, size=-1):
        data = self.stream.read(size)
        self.hash.update(data)
        self.bytes += len(data)
        return data


def make_archive(payloads, path):
    with path.open("xb") as raw:
        with lzma.LZMAFile(raw, "w", format=lzma.FORMAT_XZ,
                           check=lzma.CHECK_CRC64, filters=FILTERS) as compressed:
            with tarfile.open(fileobj=compressed, mode="w|", format=tarfile.PAX_FORMAT,
                              bufsize=CHUNK) as archive:
                for entry in payloads:
                    source = SOURCE / entry["path"]
                    descriptor = os.open(source, os.O_RDONLY | os.O_NOFOLLOW)
                    with os.fdopen(descriptor, "rb") as stream:
                        metadata = os.fstat(stream.fileno())
                        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size != entry["bytes"]:
                            raise RuntimeError(f"Source metadata changed: {entry['path']}")
                        member = tarfile.TarInfo(entry["tar_member"])
                        member.size = entry["bytes"]
                        member.mode = entry["mode"]
                        member.uid = member.gid = member.mtime = 0
                        member.uname = member.gname = ""
                        member.pax_headers = {}
                        reader = CheckedReader(stream)
                        archive.addfile(member, reader)
                        if reader.bytes != entry["bytes"] or reader.hash.hexdigest() != entry["sha256"]:
                            raise RuntimeError(f"Source bytes changed during compression: {entry['path']}")
                        if stream.read(1):
                            raise RuntimeError(f"Source grew during compression: {entry['path']}")


def make_parts(archive):
    directory = ROOT / "parts"
    directory.mkdir()
    result = []
    offset = 0
    with archive.open("rb") as stream:
        number = 1
        while True:
            data = stream.read(BASE64_LIMIT // 4 * 3)
            if not data:
                break
            encoded = base64.b64encode(data)
            assert len(encoded) <= BASE64_LIMIT
            name = f"parts/{ARCHIVE_NAME}.b64.part-{number:06d}.txt"
            with (ROOT / name).open("xb") as output:
                output.write(encoded)
            result.append({"index": number, "path": name, "bytes": len(encoded),
                           "characters": len(encoded), "sha256": hashlib.sha256(encoded).hexdigest(),
                           "decoded_bytes": len(data), "decoded_offset": offset,
                           "decoded_sha256": hashlib.sha256(data).hexdigest()})
            offset += len(data)
            number += 1
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze-confirmed", action="store_true",
                        help="Required: the parent explicitly sent FREEZE and stopped evidence edits.")
    args = parser.parse_args()
    if not args.freeze_confirmed:
        parser.error("Refusing to inspect or compress evidence before explicit FREEZE")
    resource.setrlimit(resource.RLIMIT_AS, (ADDRESS_SPACE_LIMIT, ADDRESS_SPACE_LIMIT))
    if not SOURCE.is_dir() or SOURCE.is_symlink():
        raise RuntimeError("Expected a regular evidence directory at the fixed source path")
    reserved = [ROOT / name for name in [ARCHIVE_NAME, MANIFEST_NAME, "parts", "snapshot.json",
                "recovered-from-parts", "packaging-failure.json", "packaging-success.json"]]
    if any(path.exists() for path in reserved):
        raise RuntimeError("Refusing to overwrite an existing packaging attempt or result")
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        payloads, excluded, directories = scan()
        baseline_snapshot = json.loads((BASELINE / "snapshot.json").read_text())
        if (payloads, excluded, directories) != (baseline_snapshot["payloads"], baseline_snapshot["excluded"], baseline_snapshot["directories"]):
            raise RuntimeError("Frozen evidence differs from the original 16 MiB snapshot")
        if not payloads:
            raise RuntimeError("Evidence snapshot unexpectedly contains no payloads")
        snapshot = {"source": str(SOURCE), "payloads": payloads, "excluded": excluded,
                    "directories": directories, "created_utc": started}
        write_json(ROOT / "snapshot.json", snapshot)
        archive = ROOT / ARCHIVE_NAME
        make_archive(payloads, archive)
        after_payloads, after_excluded, after_directories = scan()
        if (payloads, excluded, directories) != (after_payloads, after_excluded, after_directories):
            raise RuntimeError("Evidence tree changed during packaging; retain this failed attempt and freeze again")
        archive_sha256 = digest_file(archive)
        parts = make_parts(archive)
        manifest = {
            "format_version": 1, "agent": "Agent #4", "scope": "PR155 publication evidence only",
            "status": "PACKAGED", "source_directory": str(SOURCE),
            "verification_receipt": "packaging-success.json is created only after complete successful recovery from the base64 parts.",
            "freeze_confirmed": True, "snapshot_utc": started,
            "payload_count": len(payloads), "payload_bytes": sum(x["bytes"] for x in payloads),
            "payloads": payloads, "excluded": excluded,
            "excluded_count": len(excluded), "excluded_bytes": sum(x["bytes"] for x in excluded),
            "excluded_directory_metadata": "Empty directories and directory metadata are not payload files; each regular evidence file is either retained or individually listed as an allowed exclusion.",
            "source_directories": directories,
            "archive": {"path": ARCHIVE_NAME, "bytes": archive.stat().st_size,
                        "sha256": archive_sha256, "format": "tar.xz", "tar_format": "PAX",
                        "compression": "XZ/LZMA2 with CRC64", "dictionary_bytes": 64 * 1024 * 1024,
                        "compressor_count": 1, "filters": FILTERS,
                        "deterministic_metadata": "Sorted member paths; original permission mode; uid/gid/mtime zero; empty user/group names; no timestamps in the archive payload metadata."},
            "base64": {"max_characters_per_part": BASE64_LIMIT, "encoding": "ASCII base64 without whitespace",
                       "parts_count": len(parts), "parts": parts},
            "recovery": {"script": "recover_evidence.py",
                         "script_sha256": digest_file(ROOT / "recover_evidence.py"),
                         "archive_command": "python recover_evidence.py --manifest publication-manifest.json --destination /absolute/new/pr155-restored",
                         "parts_command": "python recover_evidence.py --manifest publication-manifest.json --from-parts --destination /absolute/new/pr155-restored"},
            "package_script_sha256": digest_file(Path(__file__)),
            "runtime": {"python": platform.python_version()},
            "execution_limits": {"address_space_bytes": ADDRESS_SPACE_LIMIT, "compressor_count": 1},
            "variant": {"baseline_archive_sha256": digest_file(BASELINE / ARCHIVE_NAME),
                        "baseline_manifest_sha256": digest_file(BASELINE / MANIFEST_NAME),
                        "baseline_snapshot_sha256": digest_file(BASELINE / "snapshot.json"),
                        "baseline_dictionary_bytes": 16777216, "payload_inventory_matches_baseline": True,
                        "baseline_disposition": "Preserved operational serialization of the same frozen payload; not deleted or modified."},
            "publication_status": "LOCAL_ONLY_NOT_PUBLISHED",
            "mathematical_status": "Packaging verifies byte preservation only; substantive research statuses are retained unchanged."
        }
        write_json(ROOT / MANIFEST_NAME, manifest)
        recovery_command = [sys.executable, "-B", str(ROOT / "recover_evidence.py"),
                            "--manifest", str(ROOT / MANIFEST_NAME), "--from-parts",
                            "--destination", str(ROOT / "recovered-from-parts")]
        with (ROOT / "recovery.stdout").open("xb") as out, (ROOT / "recovery.stderr").open("xb") as err:
            result = subprocess.run(recovery_command, stdout=out, stderr=err)
        if result.returncode:
            raise RuntimeError(f"Recovery check failed with exit {result.returncode}; all outputs retained")
        recovery = json.loads((ROOT / "recovery.stdout").read_text())
        if recovery.get("verified_payload_count") != len(payloads) or recovery.get("status") != "PASS":
            raise RuntimeError("Recovery result did not verify every retained payload")
        receipt = {"status": "PASS", "publication_status": "LOCAL_ONLY_NOT_PUBLISHED",
                   "archive_sha256": archive_sha256, "archive_bytes": archive.stat().st_size,
                   "manifest_sha256": digest_file(ROOT / MANIFEST_NAME),
                   "payload_count": len(payloads), "payload_bytes": sum(x["bytes"] for x in payloads),
                   "base64_parts": len(parts), "recovery_command": recovery_command,
                   "recovery_exit_code": result.returncode, "recovery": recovery,
                   "source_unchanged_during_packaging": True,
                   "source_matches_original_snapshot": True,
                   "address_space_limit_bytes": ADDRESS_SPACE_LIMIT,
                   "process_peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   "children_peak_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   "determinism": "Deterministic tar metadata and compression parameters fixed; no second compression claimed.",
                   "completed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
        write_json(ROOT / "packaging-success.json", receipt)
        print(json.dumps(receipt, indent=2))
    except BaseException as error:
        failure = {"status": "FAIL", "error": str(error), "traceback": traceback.format_exc(),
                   "preservation": "No outputs deleted; partial archive and all attempt evidence retained.",
                   "observed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
        if not (ROOT / "packaging-failure.json").exists():
            write_json(ROOT / "packaging-failure.json", failure)
        raise


if __name__ == "__main__":
    main()
