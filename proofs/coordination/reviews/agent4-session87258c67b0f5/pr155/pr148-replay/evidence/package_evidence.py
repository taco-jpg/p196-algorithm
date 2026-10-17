#!/usr/bin/env python3
"""Package only the three explicitly frozen follow-up roots, once and losslessly."""
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
import time
import traceback

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
SOURCE_NAMES = ["pr148-replay-evidence", "pr155-delivery", "pr167-evidence"]
ARCHIVE = "followup-evidence.tar.xz"
MANIFEST = "publication-manifest.json"
LIMIT = 1024 ** 3
CHUNK = 1024 * 1024
PART_LIMIT = 524288
FILTERS = [{"id": lzma.FILTER_LZMA2, "dict_size": 16 * 1024 ** 2,
            "lc": 3, "lp": 0, "pb": 2, "mode": lzma.MODE_NORMAL,
            "mf": lzma.MF_BT4, "nice_len": 64, "depth": 0}]
SOURCE_PREFIX = "pr148-replay-evidence/canonical-strict-001/agent51-overflow-saturation/source/"
EXCLUSIONS = {
    **{SOURCE_PREFIX + name + ".olean": {
        "category": "regenerable_Lean_object",
        "reason": "Authorized compiled Lean artifact exclusion; source bytes, exact compiler identities, invocation code, result receipts, proof-audit output and substantive logs remain payloads. No Lean execution is repeated."
    } for name in ["LychrelDigitSums", "OverflowDigits", "OverflowWitness", "ResidueSums", "Saturation"]},
    **{"pr148-replay-evidence/combined-tree/objects/" + name: {
        "category": "regenerable_private_Git_tree_object",
        "reason": "Authorized private merge-tree object exclusion; exact tree IDs, complete diff, commands, preservation manifests and immutable map references remain payloads."
    } for name in ["1b/f192ed215d829a1726cab8a61dcfdf89a965b1", "5d/b569370a28249328208eb7fd1540f31128e7f3", "d6/a9dcb8406615e10091e4a8b34e6c0196e7858f"]},
    "pr155-delivery/remote-readback/pr155-evidence.tar.xz": {
        "category": "byte_identical_already_published_transport_copy",
        "reason": "Authorized duplicate exclusion; this file is byte-identical to the existing immutable published PR155 archive. Its original local bytes remain untouched, and the full remote readback receipt remains a payload.",
        "existing_remote_commit": "286545e5717d2cf9de5c94a8066d28b0e55c24ff",
        "existing_remote_path": "proofs/coordination/reviews/agent4-session87258c67b0f5/pr155/evidence/pr155-evidence.tar.xz",
        "existing_remote_url": "https://raw.githubusercontent.com/taco-jpg/p196-algorithm/286545e5717d2cf9de5c94a8066d28b0e55c24ff/proofs/coordination/reviews/agent4-session87258c67b0f5/pr155/evidence/pr155-evidence.tar.xz",
        "expected_sha256": "7074071e389c6f9d70f1ab72cdcb5ca598af48c3e4ffccc58c1484e8e35fb1d7",
        "expected_git_blob": "18b5269920b575977b263eb227cddcdb0c69aadd"
    }
}


def save(name, value):
    with (ROOT / name).open("x") as output:
        json.dump(value, output, indent=2, sort_keys=True)
        output.write("\n")


def digest(path):
    size = path.stat().st_size
    h = hashlib.sha256()
    blob = hashlib.sha1(b"blob " + str(size).encode() + b"\0")
    with path.open("rb") as source:
        for data in iter(lambda: source.read(CHUNK), b""):
            h.update(data)
            blob.update(data)
    return {"bytes": size, "sha256": h.hexdigest(), "git_blob": blob.hexdigest()}


def scan():
    files, directories = [], []
    for root_name in SOURCE_NAMES:
        root = WORKSPACE / root_name
        if not root.is_dir() or root.is_symlink():
            raise RuntimeError("A frozen root is missing or is a link")
        for path in [root, *sorted(root.rglob("*"))]:
            metadata = path.lstat()
            mode = stat.S_IMODE(metadata.st_mode)
            if mode > 0o777:
                raise RuntimeError("Unexpected special permission bits")
            record = {"path": path.relative_to(WORKSPACE).as_posix(),
                      "original_path": str(path), "mode": mode, "mode_octal": format(mode, "04o"),
                      "original_mtime_ns": metadata.st_mtime_ns, "original_ctime_ns": metadata.st_ctime_ns,
                      "original_inode": metadata.st_ino}
            if stat.S_ISDIR(metadata.st_mode):
                directories.append(record)
            elif stat.S_ISREG(metadata.st_mode):
                record.update(digest(path))
                files.append(record)
            else:
                raise RuntimeError(f"Unexpected nonregular input: {record['path']}")
    return {"files": sorted(files, key=lambda x: x["path"]),
            "directories": sorted(directories, key=lambda x: x["path"])}


def resource_state():
    state = {"address_space_limit_bytes": LIMIT,
             "peak_resident_set_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             "disk_available_bytes": os.statvfs(ROOT).f_bavail * os.statvfs(ROOT).f_frsize}
    for key in ("memory.current", "memory.max"):
        path = Path("/sys/fs/cgroup") / key
        if path.exists():
            state["cgroup_" + key] = path.read_text().strip()
    return state


class CheckedReader:
    def __init__(self, source):
        self.source, self.bytes, self.hash = source, 0, hashlib.sha256()

    def read(self, count=-1):
        data = self.source.read(count)
        self.bytes += len(data)
        self.hash.update(data)
        return data


class TarWriter:
    def __init__(self, destination):
        self.destination, self.bytes, self.hash = destination, 0, hashlib.sha256()

    def write(self, data):
        self.bytes += len(data)
        self.hash.update(data)
        return self.destination.write(data)


def compress(payloads, directories):
    members = [(x["path"], "directory", x) for x in directories]
    members += [(x["path"], "file", x) for x in payloads]
    with (ROOT / ARCHIVE).open("xb") as raw:
        with lzma.LZMAFile(raw, "w", format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, filters=FILTERS) as encoded:
            writer = TarWriter(encoded)
            with tarfile.open(fileobj=writer, mode="w|", format=tarfile.PAX_FORMAT, bufsize=CHUNK) as archive:
                for name, kind, record in sorted(members):
                    member = tarfile.TarInfo(name)
                    member.mode = record["mode"]
                    member.uid = member.gid = member.mtime = 0
                    member.uname = member.gname = ""
                    member.pax_headers = {}
                    if kind == "directory":
                        member.type = tarfile.DIRTYPE
                        archive.addfile(member)
                        continue
                    member.size = record["bytes"]
                    fd = os.open(record["original_path"], os.O_RDONLY | os.O_NOFOLLOW)
                    with os.fdopen(fd, "rb") as source:
                        meta = os.fstat(source.fileno())
                        if not stat.S_ISREG(meta.st_mode) or meta.st_size != record["bytes"] or stat.S_IMODE(meta.st_mode) != record["mode"]:
                            raise RuntimeError("Input metadata changed during packaging")
                        reader = CheckedReader(source)
                        archive.addfile(member, reader)
                        if reader.bytes != record["bytes"] or reader.hash.hexdigest() != record["sha256"] or source.read(1):
                            raise RuntimeError("Input bytes changed during packaging")
    return {"bytes": writer.bytes, "sha256": writer.hash.hexdigest()}


def split_parts():
    (ROOT / "parts").mkdir()
    parts, offset = [], 0
    with (ROOT / ARCHIVE).open("rb") as stream:
        while data := stream.read(PART_LIMIT // 4 * 3):
            encoded = base64.b64encode(data)
            index = len(parts) + 1
            path = f"parts/{ARCHIVE}.b64.part-{index:06d}.txt"
            with (ROOT / path).open("xb") as output:
                output.write(encoded)
            parts.append({"index": index, "path": path, "bytes": len(encoded), "characters": len(encoded),
                          "sha256": hashlib.sha256(encoded).hexdigest(), "decoded_bytes": len(data),
                          "decoded_sha256": hashlib.sha256(data).hexdigest(), "decoded_offset": offset})
            offset += len(data)
    return parts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze-confirmed", action="store_true", required=True)
    parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (LIMIT, LIMIT))
    if any((ROOT / name).exists() for name in [ARCHIVE, MANIFEST, "snapshot-before.json", "parts", "recovered-from-parts", "packaging-success.json", "packaging-failure.json"]):
        raise RuntimeError("Refusing to overwrite any earlier packaging attempt")
    start = time.monotonic()
    before_resources = resource_state()
    try:
        before = scan()
        save("snapshot-before.json", before)
        by_path = {x["path"]: x for x in before["files"]}
        if not set(EXCLUSIONS).issubset(by_path):
            raise RuntimeError("One of the nine specifically authorized exclusions is missing")
        excluded = [{**by_path[path], **reason} for path, reason in sorted(EXCLUSIONS.items())]
        for item in excluded:
            for key in ["sha256", "git_blob"]:
                if "expected_" + key in item and item[key] != item["expected_" + key]:
                    raise RuntimeError("The already-published duplicate has an unexpected identity")
        payloads = [{**x, "tar_member": x["path"], "stored_path": ARCHIVE} for x in before["files"] if x["path"] not in EXCLUSIONS]
        if not payloads or len(excluded) != 9:
            raise RuntimeError("Unexpected evidence or exclusion count")
        tar_identity = compress(payloads, before["directories"])
        archive_identity = digest(ROOT / ARCHIVE)
        parts = split_parts()
        manifest = {
            "format_version": 1, "status": "PACKAGED_PENDING_RECOVERY_RECEIPT",
            "scope": "Frozen PR148 replay evidence, PR155 delivery history, and stopped PR167 evidence; packaging only",
            "source_roots": [str(WORKSPACE / x) for x in SOURCE_NAMES],
            "freeze_confirmed": True, "original_file_count": len(before["files"]),
            "original_file_bytes": sum(x["bytes"] for x in before["files"]),
            "payload_count": len(payloads), "payload_bytes": sum(x["bytes"] for x in payloads),
            "payloads": payloads, "directories": before["directories"],
            "excluded_count": len(excluded), "excluded_bytes": sum(x["bytes"] for x in excluded),
            "excluded": excluded, "exclusion_policy": "Only the nine exact parent-authorized paths are excluded; all other regular files and every directory are retained. No source input is deleted or modified.",
            "archive": {"path": ARCHIVE, **archive_identity, "format": "tar.xz", "tar_format": "PAX",
                        "compression": "One XZ/LZMA2 stream with CRC64", "dictionary_bytes": 16 * 1024 ** 2,
                        "compressor_count": 1, "compression_invocations": 1, "filters": FILTERS,
                        "uncompressed_tar": tar_identity,
                        "deterministic_serialization": "Lexically sorted member paths; original permission modes; uid/gid/mtime zero; empty owner names; no source timestamps inside tar; fixed PAX and LZMA2 settings.",
                        "normalized_metadata": "Ownership and timestamps are normalized in tar. Original file modes and bytes are preserved; original mtime/ctime and inode values are retained in this manifest as freeze observations, not restored ownership/time metadata."},
            "base64": {"encoding": "ASCII base64 without whitespace or JSON", "max_characters_per_part": PART_LIMIT,
                       "parts_count": len(parts), "parts": parts},
            "resource_limits": {"address_space_limit_bytes": LIMIT, "compressors": 1, "dictionary_bytes": 16 * 1024 ** 2},
            "recovery": {"script": "recover_evidence.py", "script_sha256": digest(ROOT / "recover_evidence.py")["sha256"],
                         "archive_command": "python3 -B recover_evidence.py --manifest publication-manifest.json --destination /absolute/new/followup-restored",
                         "parts_command": "python3 -B recover_evidence.py --manifest publication-manifest.json --from-parts --destination /absolute/new/followup-restored",
                         "success_receipt": "packaging-success.json"},
            "package_script_sha256": digest(Path(__file__))["sha256"],
            "runtime": {"python": platform.python_version(), "python_executable": sys.executable},
            "mathematical_status": "No new review or Lean execution; every original evidence label and attribution is preserved.",
            "ownership": "Agent28 delivery; Agent51 source; Agent31 main. No additional authority acquired.",
            "remote_operations": False, "publication_status": "LOCAL_ONLY_NOT_PUBLISHED"
        }
        save(MANIFEST, manifest)
        command = [sys.executable, "-B", str(ROOT / "recover_evidence.py"), "--manifest", str(ROOT / MANIFEST),
                   "--from-parts", "--destination", str(ROOT / "recovered-from-parts")]
        save("recovery-command.json", {"argv": command, "cwd": str(ROOT), "resource_limit_inherited_bytes": LIMIT})
        with (ROOT / "recovery.stdout").open("xb") as out, (ROOT / "recovery.stderr").open("xb") as err:
            completed = subprocess.run(command, cwd=ROOT, stdout=out, stderr=err)
        if completed.returncode:
            raise RuntimeError(f"Full recovery failed with exit {completed.returncode}; outputs preserved")
        recovery = json.loads((ROOT / "recovery.stdout").read_text())
        if recovery["status"] != "PASS" or recovery["verified_payload_count"] != len(payloads):
            raise RuntimeError("Recovery did not verify every payload")
        after = scan()
        save("snapshot-after.json", after)
        if before != after:
            raise RuntimeError("Frozen inputs changed; original and final snapshots preserved")
        receipt = {"status": "PASS", "scope": "Lossless packaging and complete recovery only",
                   "archive": manifest["archive"], "manifest_sha256": digest(ROOT / MANIFEST)["sha256"],
                   "payload_count": len(payloads), "payload_bytes": manifest["payload_bytes"],
                   "directories": len(before["directories"]), "excluded_count": len(excluded),
                   "excluded_bytes": manifest["excluded_bytes"], "base64_parts": len(parts),
                   "original_input_file_count": len(before["files"]), "all_frozen_inputs_unchanged": True,
                   "snapshot_before_sha256": digest(ROOT / "snapshot-before.json")["sha256"],
                   "snapshot_after_sha256": digest(ROOT / "snapshot-after.json")["sha256"],
                   "recovery_exit_code": completed.returncode, "recovery": recovery,
                   "resources_before": before_resources, "resources_after": resource_state(),
                   "elapsed_seconds": time.monotonic() - start,
                   "compression_invocations": 1, "second_compression_or_variant": False,
                   "publication_status": "LOCAL_ONLY_NOT_PUBLISHED", "remote_operations": False,
                   "completed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
        save("packaging-success.json", receipt)
        print(json.dumps(receipt, indent=2))
    except BaseException as error:
        if not (ROOT / "packaging-failure.json").exists():
            save("packaging-failure.json", {"status": "FAIL", "error": str(error), "traceback": traceback.format_exc(),
                 "preservation": "All partial outputs and logs retained; no deletions, retries, or extra compression variants performed."})
        raise


if __name__ == "__main__":
    main()
