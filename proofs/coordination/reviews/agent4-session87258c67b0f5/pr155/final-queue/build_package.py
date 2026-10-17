#!/usr/bin/env python3
"""Freeze by exact inventory, deterministically package, and recover a read-only evidence snapshot."""
import base64
import hashlib
import io
import json
import lzma
import os
from pathlib import Path
import resource
import stat
import tarfile
from recover_archive import verify_and_recover

ROOT = Path("/workspace/scratch/87258c67b0f5/campaign-final-revisit")
OUT = Path("/workspace/scratch/87258c67b0f5/campaign-final-revisit-publication")
LIMIT = 1024 * 1024 * 1024
soft, hard = resource.getrlimit(resource.RLIMIT_AS)
resource.setrlimit(resource.RLIMIT_AS, (min(LIMIT, hard) if hard != resource.RLIM_INFINITY else LIMIT, hard))

def canonical(obj):
    return (json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")

def inventory():
    records = []
    for p in sorted(ROOT.rglob("*"), key=lambda p: p.relative_to(ROOT).as_posix()):
        if p.is_symlink():
            raise ValueError("Symlinks are not allowed: " + str(p))
        if p.is_dir():
            continue
        if not p.is_file():
            raise ValueError("Non-regular source entry: " + str(p))
        body = p.read_bytes()
        rel = p.relative_to(ROOT).as_posix()
        records.append({"relative_path": rel, "original_path": str(p), "archive_path": "campaign-final-revisit/" + rel, "bytes": len(body), "mode": format(stat.S_IMODE(p.stat().st_mode), "04o"), "sha256": hashlib.sha256(body).hexdigest()})
    if not records:
        raise ValueError("Empty source")
    return records

def exclusive_write(name, body):
    with (OUT / name).open("xb") as f:
        f.write(body)

before = inventory()
manifest = {"schema_version": 1, "source_root": str(ROOT), "scope": "Every regular file in the closed campaign-final-revisit evidence root; no evidence exclusions", "file_count": len(before), "total_bytes": sum(x["bytes"] for x in before), "files": before}
manifest_bytes = canonical(manifest)
manifest_sha = hashlib.sha256(manifest_bytes).hexdigest()
exclusive_write("SOURCE_MANIFEST.json", manifest_bytes)
freeze = {"schema_version": 1, "status": "FROZEN_BY_EXACT_CONTENT_AND_MODE_INVENTORY", "source_root": str(ROOT), "source_manifest_sha256": manifest_sha, "files": len(before), "bytes": manifest["total_bytes"], "source_content_or_mode_changes_performed": False, "freeze_mechanism": "Closed writer scope plus exact path/size/mode/SHA256 inventory; before/after packaging and full recovery comparison. Filesystem permission modes are preserved, not rewritten."}
exclusive_write("FREEZE.json", canonical(freeze))
print("FROZEN", len(before), "source files;", manifest["total_bytes"], "bytes")
archive = OUT / "campaign-final-revisit.tar.xz"
if archive.exists():
    raise FileExistsError("Archive already exists; refusing overwrite")
filters = [{"id": lzma.FILTER_LZMA2, "preset": 6, "dict_size": 16 * 1024 * 1024}]
with archive.open("xb") as raw:
    with lzma.LZMAFile(raw, mode="wb", format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, filters=filters) as compressed:
        with tarfile.open(fileobj=compressed, mode="w|", format=tarfile.PAX_FORMAT) as tf:
            payloads = [("PACKAGE_SOURCE_MANIFEST.json", manifest_bytes, 0o644)]
            payloads.extend((x["archive_path"], (ROOT / x["relative_path"]).read_bytes(), int(x["mode"], 8)) for x in before)
            for name, body, mode in payloads:
                ti = tarfile.TarInfo(name=name)
                ti.size = len(body)
                ti.mode = mode
                ti.uid = ti.gid = 0
                ti.uname = ti.gname = ""
                ti.mtime = 0
                ti.pax_headers = {}
                tf.addfile(ti, io.BytesIO(body))
if inventory() != before:
    raise ValueError("Source snapshot changed during packaging; preserved output is invalid")
archive_bytes = archive.read_bytes()
archive_sha = hashlib.sha256(archive_bytes).hexdigest()
archive_git = hashlib.sha1(b"blob " + str(len(archive_bytes)).encode() + b"\0" + archive_bytes).hexdigest()
check_id = int.from_bytes(archive_bytes[6:8], "little") >> 8
if archive_bytes[:6] != b"\xfd7zXZ\x00" or check_id != 4:
    raise ValueError("XZ header does not declare CRC64")
metadata = {"schema_version": 1, "archive": {"filename": archive.name, "bytes": len(archive_bytes), "sha256": archive_sha, "git_blob": archive_git, "format": "XZ containing deterministic POSIX/PAX tar", "compression": "One Python/liblzma LZMA2 compressor; no parallel compression workers", "dictionary_bytes": 16777216, "check": "CRC64", "preset": 6}, "resource_limits": {"virtual_address_space_bytes": LIMIT, "compressors": 1, "compression_threads": 1}, "source_file_count": len(before), "source_bytes": manifest["total_bytes"], "archive_member_count": len(before) + 1, "source_manifest_sha256": manifest_sha, "determinism": {"path_order": "PACKAGE_SOURCE_MANIFEST.json first, then all source files in lexical relative-path order", "tar_mtime": 0, "tar_uid": 0, "tar_gid": 0, "tar_uname": "", "tar_gname": "", "tar_modes": "Original file modes from manifest", "json": "UTF-8, sorted keys, indent 2, one terminal newline", "xz_parameters": "Fixed LZMA2 preset 6, 16 MiB dictionary, CRC64; no timestamp fields", "repeat_compression_performed": False}, "recovery_script_sha256": hashlib.sha256((OUT / "recover_archive.py").read_bytes()).hexdigest(), "build_script_sha256": hashlib.sha256((OUT / "build_package.py").read_bytes()).hexdigest()}
exclusive_write("ARCHIVE_METADATA.json", canonical(metadata))
encoded = base64.b64encode(archive_bytes)
b64info = {"schema_version": 1, "encoding": "RFC4648 standard base64", "piece_count": 1, "payload_characters": len(encoded), "file_bytes_with_terminal_newline": len(encoded) + 1, "limit_characters": 524288, "under_limit": len(encoded) + 1 < 524288, "decoded_bytes": len(archive_bytes), "decoded_sha256": archive_sha, "decoded_git_blob": archive_git}
if len(encoded) + 1 >= 524288:
    raise ValueError("Single base64 piece exceeds requested bound; archive and logs preserved")
exclusive_write("PAYLOAD.b64", encoded + b"\n")
exclusive_write("BASE64_METADATA.json", canonical(b64info))
if base64.b64decode(encoded, validate=True) != archive_bytes:
    raise ValueError("Base64 round-trip mismatch")
recovered = verify_and_recover(archive, OUT / "ARCHIVE_METADATA.json", OUT / "recovered")
after = inventory()
if after != before:
    raise ValueError("Source snapshot changed during recovery")
exact = []
for x in before:
    a, b = ROOT / x["relative_path"], OUT / "recovered" / x["archive_path"]
    if a.read_bytes() != b.read_bytes():
        raise ValueError("Direct recovered-byte comparison failed: " + str(a))
    exact.append(x["relative_path"])
recovered["source_snapshot_unchanged"] = True
recovered["direct_original_vs_recovered_byte_comparisons"] = len(exact)
recovered["base64_exact_roundtrip"] = True
exclusive_write("RECOVERY_VERIFICATION.json", canonical(recovered))
print("ARCHIVE", archive.name, len(archive_bytes), "bytes", archive_sha)
print("BASE64", len(encoded), "characters; one piece below 524288")
print("RECOVERY PASS", len(exact), "exact byte comparisons; source snapshot unchanged")
