#!/usr/bin/env python3
"""Package exact remaining Agent12 evidence; never rerun Lean or runtime checks."""
from pathlib import Path
import hashlib
import io
import json
import lzma
import platform
import stat
import tarfile

ROOT = Path("/workspace/scratch/5eac7b9c26af")
OUT = ROOT / "agent12-publication/campaign"
ARCHIVE = OUT / "remaining-support-evidence.tar.xz"
MANIFEST = OUT / "remaining-support-manifest.json"
VERIFICATION = OUT / "remaining-support-verification.json"
RECEIPT = OUT / "PACKAGING_RECEIPT.md"
PACKAGER = OUT / "package_remaining_support.py"
SINGLE_FILES = ["agent12-evidence/open-queue-snapshot.json"]
DIRECTORIES = [
    "agent12-evidence/periodic-ownership",
    "agent12-evidence/successor",
    "agent12-runtime",
]
EXCLUDED = "agent12-runtime/lean-4.19.0-linux.tar.zst"
URL = "https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def collect():
    result = [ROOT / p for p in SINGLE_FILES]
    for directory in DIRECTORIES:
        base = ROOT / directory
        if not base.is_dir() or base.is_symlink():
            raise ValueError("Unexpected input directory: " + str(base))
        for path in base.rglob("*"):
            relative = path.relative_to(ROOT).as_posix()
            if path.is_symlink():
                raise ValueError("Symlink is not allowed: " + relative)
            if path.is_dir():
                continue
            if not path.is_file():
                raise ValueError("Nonregular input: " + relative)
            if relative != EXCLUDED:
                result.append(path)
    result.sort(key=lambda p: p.relative_to(ROOT).as_posix())
    if len(set(result)) != len(result):
        raise ValueError("Duplicate input")
    for path in result:
        if path.is_symlink() or not path.is_file():
            raise ValueError("Nonregular explicit input: " + str(path))
    return result

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    paths = collect()
    contents = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in paths}
    rows = [{
        "path": p.relative_to(ROOT).as_posix(),
        "bytes": len(contents[p.relative_to(ROOT).as_posix()]),
        "sha256": digest(contents[p.relative_to(ROOT).as_posix()]),
        "mode_octal": format(stat.S_IMODE(p.stat().st_mode), "04o"),
    } for p in paths]
    historical = json.loads(contents["agent12-runtime/runtime-receipt.json"])
    comparison = json.loads(contents["agent12-runtime/runtime-archive-check.json"])
    release = json.loads(contents["agent12-runtime/official-release-metadata.json"])
    # Reconcile only retained receipt fields, never the download or installed runtime.
    if not (
        historical["archive_source"] == comparison["source"] == release["asset_url"] == URL
        and historical["archive_bytes"] == comparison["archive_bytes"] == release["asset_size"] == 343842845
        and historical["archive_sha256"] == comparison["archive_sha256"]
        == "6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe"
    ):
        raise ValueError("Retained official archive identity receipts disagree")
    excluded = {
        "path": EXCLUDED,
        "reason": "Reproducible official fixed-version download deliberately omitted",
        "bytes": historical["archive_bytes"],
        "sha256": historical["archive_sha256"],
        "source_url": URL,
        "release_page": release["url"],
        "release_id": release["release_id"],
        "asset_id": release["asset_id"],
        "upstream_api_digest": release["asset_digest"],
        "digest_qualification": historical["checksum_qualification"],
        "identity_basis": [
            "agent12-runtime/runtime-receipt.json",
            "agent12-runtime/runtime-archive-check.json",
            "agent12-runtime/official-release-metadata.json",
        ],
        "historical_recovery_verifier": "agent12-runtime/verify_runtime_archive.py",
        "new_download_or_runtime_check": False,
    }
    manifest = {
        "schema_version": 1,
        "archive": ARCHIVE.name,
        "path_basis": str(ROOT),
        "scope": {"single_files": SINGLE_FILES, "directories": DIRECTORIES},
        "member_count": len(rows),
        "payload_bytes": sum(r["bytes"] for r in rows),
        "members": rows,
        "excluded_download": excluded,
        "normalization": {
            "tar_format": "USTAR",
            "ordering": "Lexical POSIX relative path",
            "member_types": "Regular files only, no link/directory members",
            "uid": 0, "gid": 0, "uname": "", "gname": "", "mtime": 0,
            "mode": "Original permission bits retained",
            "compression": "XZ preset9 CRC64",
        },
        "scope_limit": "Historical runtime smoke and coordination evidence; no new Lean/P196/PR checks",
    }
    write_json(MANIFEST, manifest)
    with lzma.open(ARCHIVE, "wb", format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, preset=9) as compressed:
        with tarfile.open(fileobj=compressed, mode="w|", format=tarfile.USTAR_FORMAT) as bundle:
            for row in rows:
                member = tarfile.TarInfo(row["path"])
                member.type = tarfile.REGTYPE
                member.size = row["bytes"]
                member.mode = int(row["mode_octal"], 8)
                member.uid = member.gid = 0
                member.uname = member.gname = ""
                member.mtime = 0
                bundle.addfile(member, io.BytesIO(contents[row["path"]]))
    # Exactly one full decompression pass checks every member and the XZ footer.
    checked = []
    with lzma.open(ARCHIVE, "rb") as decompressed:
        with tarfile.open(fileobj=decompressed, mode="r|") as bundle:
            for index, member in enumerate(bundle):
                if index >= len(rows):
                    raise ValueError("Unexpected extra member")
                expected = rows[index]
                if not (
                    member.name == expected["path"] and member.isfile()
                    and member.mode == int(expected["mode_octal"], 8)
                    and member.uid == member.gid == member.mtime == 0
                    and member.uname == member.gname == ""
                ):
                    raise ValueError("Member metadata mismatch: " + member.name)
                stream = bundle.extractfile(member)
                if stream is None:
                    raise ValueError("Unreadable member: " + member.name)
                restored = stream.read()
                actual_digest = digest(restored)
                if not (
                    len(restored) == member.size == expected["bytes"]
                    and actual_digest == expected["sha256"]
                ):
                    raise ValueError("Member content mismatch: " + member.name)
                checked.append({
                    "path": member.name, "bytes": len(restored),
                    "sha256": actual_digest, "matched": True, "metadata_matched": True,
                })
        trailing = decompressed.read()
        if trailing and any(trailing):
            raise ValueError("Unexpected nonzero trailing tar bytes")
    if len(checked) != len(rows):
        raise ValueError("Missing archive members")
    archive_data = ARCHIVE.read_bytes()
    result = {
        "schema_version": 1,
        "status": "PASS_LOSSLESS_MEMBER_BY_MEMBER_DECOMPRESSION",
        "archive": ARCHIVE.name,
        "archive_bytes": len(archive_data),
        "archive_sha256": digest(archive_data),
        "manifest": MANIFEST.name,
        "manifest_bytes": MANIFEST.stat().st_size,
        "manifest_sha256": digest(MANIFEST.read_bytes()),
        "packager": PACKAGER.name,
        "packager_bytes": PACKAGER.stat().st_size,
        "packager_sha256": digest(PACKAGER.read_bytes()),
        "member_count": len(rows),
        "payload_bytes": manifest["payload_bytes"],
        "decompression_passes": 1,
        "members": checked,
        "new_lean_execution": False,
        "new_runtime_validation": False,
        "new_p196_proof_execution": False,
        "new_pr_checks": False,
        "remote_writes": False,
        "input_mutations": False,
        "python": platform.python_version(),
        "execution_command": "python " + str(PACKAGER),
        "preexecution_orchestration_failure": {
            "error": "JavaScript SyntaxError: Unexpected token '{'",
            "stage": "Initial tool-call parsing before any packager/file execution",
            "effect": "No archive or packager was created by that failed call; corrected orchestration only",
        },
    }
    write_json(VERIFICATION, result)
    lines = [
        "# Remaining support evidence: packaging and recovery receipt", "",
        "**Result: PASS.** A deterministic lossless archive was created and every member "
        "was checked through one decompression pass against its original byte count, "
        "SHA256 and normalized metadata.", "",
        "## Package identity", "",
        "- Archive: " + ARCHIVE.name,
        "- Compressed bytes: " + str(result["archive_bytes"]),
        "- Archive SHA256: " + result["archive_sha256"],
        "- Regular-file members: " + str(len(rows)),
        "- Original payload bytes: " + str(result["payload_bytes"]),
        "- Complete manifest: " + MANIFEST.name,
        "- Manifest SHA256: " + result["manifest_sha256"],
        "- Verification record: " + VERIFICATION.name,
        "- Retained packager: " + PACKAGER.name,
        "- Packager SHA256: " + result["packager_sha256"], "",
        "## Exact inclusion and preservation", "",
        "Included the single open-queue snapshot; every file in periodic-ownership and "
        "successor; and all regular files in agent12-runtime except the named official "
        "download. This includes RuntimeSmoke.lean and its compiled .olean, the full "
        "runtime-member-checks.json, original commands/receipts/logs, official release "
        "metadata, and the original verification script. Command history, initial failures "
        "and approved remedies are retained inside runtime-receipt.json.", "",
        "All original input bytes and permission bits are preserved. Inputs were read "
        "only. The archive excludes the installed runtime, any repository clone/cache, "
        "the Agent26 archive, other session files and the separately published PR97, "
        "PR157 and PR121 directories. Companion manifest/verification/receipt/packager "
        "files are external to the archive, preserving exactly the requested member scope.", "",
        "Members use USTAR, lexical relative-path order, uid/gid zero, empty uname/gname, "
        "mtime zero and original mode bits. XZ uses preset9 and CRC64 without wall-clock "
        "metadata. Determinism follows from these explicit settings; no optional second "
        "build or second decompression was run.", "",
        "## Historical runtime evidence and limits", "",
        "The original runtime receipt is dated " + historical["recorded_at_utc"] + ". "
        "It records the earlier official Lean4.19.0 comparison of 5,066 members, including "
        "4,605 regular files, version/prefix observations and strict trust0 RuntimeSmoke "
        "compilation with an empty axiom list. It explicitly says P196 verification was "
        "NOT_RUN. These are preserved historical results, not new execution by this task.", "",
        "This packaging task invoked no Lean, Lake, original runtime-verifier, P196 proof, "
        "PR check, download, workflow or remote mutation. RuntimeSmoke.olean is historical "
        "runtime smoke output, not an accepted P196 dependency object.", "",
        "An initial orchestration call failed JavaScript parsing with SyntaxError: "
        "Unexpected token '{' before any file or packager execution. The orchestration "
        "was corrected; there was only one executed archive build and one full "
        "member-by-member decompression/hash check.", "",
        "## Excluded official download: exact recovery identity", "",
        "- Official pinned URL: " + URL,
        "- Official release page: " + release["url"],
        "- GitHub release ID: " + str(release["release_id"]),
        "- GitHub asset ID: " + str(release["asset_id"]),
        "- Filename: " + Path(EXCLUDED).name,
        "- Recorded bytes: " + str(excluded["bytes"]),
        "- Recorded SHA256: " + excluded["sha256"],
        "- Digest qualification: " + historical["checksum_qualification"], "",
        "The upstream release API digest is null. The recorded SHA256 is the original "
        "session's local digest of the fresh fixed-version official HTTPS download; it "
        "is not a separately published upstream checksum. The exact recovery provenance "
        "is retained in runtime-receipt.json, runtime-archive-check.json and "
        "official-release-metadata.json. This excluded download was not read, copied, "
        "rehashed, deleted or downloaded again during packaging.", "",
        "## Recovery instructions (not executed here)", "",
        "1. Verify this evidence archive's SHA256, inspect member paths and extract only "
        "safe relative regular-file members into a new empty recovery directory. Compare "
        "every recovered file's bytes, SHA256 and mode against the complete manifest.",
        "2. Recover the excluded official archive from the exact pinned HTTPS URL above "
        "through the normally authorized download mechanism. Require exactly 343842845 "
        "bytes and the recorded SHA256 before extraction. If either differs, retain the "
        "discrepancy and do not treat the result as the original artifact.",
        "3. Inspect official archive paths and links before extracting into a new isolated "
        "directory. The preserved verify_runtime_archive.py documents the original "
        "complete comparison and historical fixed paths. Inspect/adapt a separate copy "
        "if recovery paths differ; never overwrite the original evidence.",
        "4. Retain normal execution restrictions. This package confers no permission "
        "changes and no new runtime execution authority. Recovery and smoke commands "
        "were not rerun here.", "",
        "## Complete member inventory", "",
        "| Path | Bytes | SHA256 |", "|---|---:|---|",
    ]
    lines.extend("| " + r["path"] + " | " + str(r["bytes"]) + " | " + r["sha256"] + " |" for r in rows)
    lines.extend(["", "Paths are relative to the original Agent12 workspace.", ""])
    RECEIPT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "status": result["status"], "member_count": len(rows),
        "payload_bytes": result["payload_bytes"],
        "files": [{
            "path": str(path), "bytes": path.stat().st_size,
            "sha256": digest(path.read_bytes()),
        } for path in [ARCHIVE, MANIFEST, VERIFICATION, RECEIPT, PACKAGER]],
    }, indent=2))

if __name__ == "__main__":
    main()

