#!/usr/bin/env python3
"""Pack the explicitly scoped PR153 delivery evidence without changing any input."""
import argparse
import base64
import html
import io
import json
import lzma
from pathlib import Path
import re
import resource
import stat
import sys
import tarfile
import urllib.parse

sys.dont_write_bytecode = True
from verify_delivery import identity, require, verify, verify_members

COMMIT = "bc956c407be75566fe815beced3b7d1d14985f62"
PREFIX = "proofs/coordination/evidence/agent20-session16fe/pr153/"
PUBLICATION_FILES = ("DELIVERY_ACTIONS.json", "FORMAL_REVIEW.md", "verify_remote_publication.py")
READBACK_FILES = ("REMOTE_PUBLICATION_READBACK.json", "package-verifier.stdout.log", "package-verifier.stderr.log")
OWN_FILES = ("ARCHIVE_MANIFEST.json", "CONTENT_SCREENING.json", "EXCLUSIONS.json",
             "PACKING_VERIFICATION.json", "PAYLOAD_MANIFEST.json", "README.md",
             "delivery-evidence.tar.xz", "delivery-evidence.tar.xz.b64",
             "pack_delivery.py", "verify_delivery.py")


def json_write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_regular(path):
    require(stat.S_ISREG(path.lstat().st_mode), "Nonregular input: " + str(path))
    return path.read_bytes()


def recursive_files(directory):
    require(directory.is_dir() and not directory.is_symlink(), "Unsafe source directory")
    found = []
    for path in sorted(directory.rglob("*")):
        kind = path.lstat().st_mode
        require(stat.S_ISREG(kind) or stat.S_ISDIR(kind), "Symlink or special source entry")
        if stat.S_ISREG(kind):
            found.append(path)
    return found


def snapshot(root):
    watch = recursive_files(root / "pr153-delivery-watch")
    selected = watch + [root / "pr153-publication" / name for name in PUBLICATION_FILES]
    selected += [root / "pr153-remote-readback" / name for name in READBACK_FILES]
    payload = {str(path.relative_to(root)): read_regular(path) for path in sorted(selected)}
    remote = recursive_files(root / "pr153-remote-readback")
    excluded = {str(path.relative_to(root)): read_regular(path) for path in remote
                if path.name not in READBACK_FILES}
    return payload, excluded


def exclusions(payload, excluded):
    receipt = json.loads(payload["pr153-remote-readback/REMOTE_PUBLICATION_READBACK.json"])
    require(receipt["commit"] == COMMIT and receipt["prefix"] == PREFIX, "Readback publication pin mismatch")
    require(receipt["status"] == "PASS_ALL_REMOTE_BYTES_AND_ARCHIVE_MEMBERS", "Readback status mismatch")
    records = {entry["path"]: entry for entry in receipt["files"]}
    require(len(records) == 14 and receipt["all_remote_bytes_match"] is True, "Incomplete primary readback")
    require(set(excluded) == {"pr153-remote-readback/" + name for name in records} |
            {"pr153-remote-readback/evidence.tar.xz"}, "Unexpected remote readback omission")
    entries = []
    for path, data in sorted(excluded.items()):
        name = path.split("/", 1)[1]
        info = identity(data)
        if name == "evidence.tar.xz":
            require(info == receipt["archive_verification"]["decoded_identity"], "Decoded primary archive mismatch")
            b64 = excluded["pr153-remote-readback/evidence.tar.xz.b64"]
            require(base64.b64decode(b"".join(b64.splitlines()), validate=True) == data,
                    "Excluded primary archive is not the exact published Base64 recovery")
            recovery = {"commit": COMMIT, "path": PREFIX + "evidence.tar.xz.b64", "operation": "Base64 decode"}
            reason = "Exact decoded duplicate of the primary evidence archive already preserved by published Base64."
        else:
            record = records[name]
            require(record["http_status"] == 200 and record["byte_identical"] is True and
                    record["expected"] == record["actual"] == info, "Primary published duplicate mismatch: " + name)
            recovery = {"commit": COMMIT, "path": PREFIX + name, "operation": "Read immutable published file"}
            reason = "Byte-identical local readback of a file already preserved in the immutable primary publication."
        entries.append({"path": path, **info, "reason": reason, "recovery": recovery})
    return {"schema": 1, "file_count": len(entries), "total_bytes": sum(e["bytes"] for e in entries),
            "primary_publication_commit": COMMIT, "files": entries,
            "scope": "Only redundant copies in pr153-remote-readback are excluded. No requested new evidence is omitted.",
            "source_deletions": False}


def all_strings(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from all_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from all_strings(item)
    elif isinstance(value, str):
        yield value


def screen(payload):
    patterns = {
        "private_key": rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
        "github_token": rb"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b",
        "aws_key": rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
        "bearer_credential": rb'(?i)authorization["\s:]+bearer\s+[A-Za-z0-9._~+/-]{24,}',
        "private_prompt_marker": rb"END_ROLE_PROMPT|BEGIN_ROLE_PROMPT|<environment_context>|<permissions instructions>",
    }
    findings = []
    query_records = {}
    hosts = set()
    for path, data in payload.items():
        text = data.decode("utf-8")
        for label, pattern in patterns.items():
            for match in re.finditer(pattern, data):
                findings.append({"path": path, "kind": label, "byte_offset": match.start()})
        values = list(all_strings(json.loads(text))) if path.endswith(".json") else [text]
        for value in values:
            for raw in re.findall(r'https?://[^\s"<>\\]+', value):
                url = urllib.parse.urlsplit(html.unescape(raw.rstrip(".,;)")))
                hosts.add(url.netloc)
                if url.username or url.password:
                    findings.append({"path": path, "kind": "url_embedded_credentials"})
                if not url.query:
                    continue
                keys = tuple(key for key, _ in urllib.parse.parse_qsl(url.query))
                classification = None
                if url.netloc == "api.github.com" and set(keys) <= {"ref", "per_page", "page", "since", "head_sha"} and keys:
                    classification = "Public GitHub source reference or read-only query/pagination parameters"
                elif url.netloc == "api.github.com" and "notifications{" in url.path and not keys:
                    classification = "GitHub notifications URI template, not a credential or transient download"
                elif url.netloc == "avatars.githubusercontent.com" and keys == ("v",):
                    classification = "Public avatar version parameter"
                elif url.netloc == "dashboard.gitguardian.com" and set(keys) <= {"utm_medium", "utm_source", "utm_campaign"} and keys:
                    classification = "Public marketing attribution on a GitGuardian login link"
                if classification is None:
                    findings.append({"path": path, "kind": "unclassified_url_query", "host": url.netloc, "parameter_names": keys})
                key = (url.netloc, keys, classification)
                query_records.setdefault(key, set()).add(path)
    require(not findings, "Content screening requires review: " + json.dumps(findings))
    return {"schema": 1, "status": "PASS_NO_CREDENTIAL_OR_PRIVATE_PROMPT_PATTERNS",
            "files_scanned": len(payload), "bytes_scanned": sum(map(len, payload.values())),
            "method": "UTF-8 raw byte patterns plus JSON-decoded string/HTML-unescaped URL analysis; all requested bytes retained.",
            "pattern_classes": sorted(patterns), "pattern_matches": findings, "url_hosts": sorted(hosts),
            "querystring_classes": [{"host": key[0], "parameter_names": list(key[1]), "classification": key[2],
                                     "files": sorted(files)} for key, files in sorted(query_records.items())],
            "transient_signed_download_urls_found": False, "symlinks_or_special_files_found": False,
            "limitation": "Pattern and URL classification screening is evidence of these specific checks, not an absolute proof of absence of all possible secrets. Public issue/PR text and requested API response metadata remain unmodified."}


def make_archive(payload):
    output = io.BytesIO()
    with lzma.LZMAFile(output, mode="w", format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64,
                       filters=[{"id": lzma.FILTER_LZMA2, "preset": 6, "dict_size": 8 * 1024 * 1024}]) as compressed:
        with tarfile.open(fileobj=compressed, mode="w|", format=tarfile.USTAR_FORMAT) as archive:
            for name, data in sorted(payload.items()):
                member = tarfile.TarInfo(name)
                member.size = len(data)
                member.mode = 0o644
                member.uid = member.gid = member.mtime = 0
                member.uname = member.gname = ""
                member.type = tarfile.REGTYPE
                archive.addfile(member, io.BytesIO(data))
    return output.getvalue()


README = """# PR153 delivery evidence recovery

This separate package preserves the requested delivery records following the primary evidence publication at commit `bc956c407be75566fe815beced3b7d1d14985f62` in `taco-jpg/p196-algorithm`. It is packaging evidence, not a new proof review, Lean execution, merge receipt, or main-writer claim.

## Contents and preservation

The archive contains all 20 files in `pr153-delivery-watch/` (19 raw readbacks and their manifest), the exact `DELIVERY_ACTIONS.json`, `FORMAL_REVIEW.md`, and `verify_remote_publication.py` from `pr153-publication/`, and the primary remote-publication readback report plus both verifier output streams from `pr153-remote-readback/`. Every member is regular and retained byte for byte, including the empty stderr stream. The delivery actions snapshot records its own timestamp; later status/task/comment receipts belong to separate records.

`PAYLOAD_MANIFEST.json` lists every archive member with size, SHA-256 and Git blob SHA-1. `EXCLUSIONS.json` lists every excluded remote-readback duplicate with the same identities and a recovery operation at the immutable primary publication. Those 14 published files and one decoded archive are the only exclusions within the scoped remote-readback directory. No source file was deleted or modified. The initial seven primary packaging files, root documents, coordination status and task were not changed by this packaging work.

`CONTENT_SCREENING.json` records the credential/private-prompt pattern and URL checks. Public GitHub pagination/reference parameters, avatar versions, GitGuardian marketing attribution parameters and GitHub URI templates are retained. No credential pattern or signed transient download URL was found. These specific checks do not imply universal secret detection.

## Verify and recover without network access

Keep the package files together. Python 3 with its standard `lzma` library is sufficient; no Lean, repository checkout, external dependency, credential or network request is used by the recovery verifier.

```bash
python3 verify_delivery.py --package .
python3 verify_delivery.py --package . --extract recovered-delivery
```

The optional extraction target must not already exist. The verifier first checks every inventoried packaging artifact, decodes the wrapped Base64 strictly, compares its archive identity, and checks all member names/order/regular type/metadata/size/SHA-256/Git blob IDs against the complete manifest. It then creates only verified regular files under the fresh destination and reads each back. If the raw `delivery-evidence.tar.xz` is absent, its exact bytes are recovered in memory from the Base64 and verified; the raw archive need not be published twice. The verifier never executes scripts or other payload content.

`ARCHIVE_MANIFEST.json` inventories every other packaging artifact, including the packer and standalone verifier. Its own identity is deliberately excluded to avoid self-reference and must be pinned externally at publication. The primary publication prefix is `proofs/coordination/evidence/agent20-session16fe/pr153/`; recovery of an excluded duplicate uses the exact commit and path in `EXCLUSIONS.json`.

## Deterministic production and boundaries

`pack_delivery.py --root /path/to/original/workspace --output /path/to/new-package` recreates the package from the scoped source paths. Place this packer and `verify_delivery.py` in the otherwise empty new package directory first. It verifies the original 19-file delivery-watch manifest, validates all duplicate exclusion identities against the retained primary readback, and checks that included/excluded sources are unchanged after packing.

The archive uses sorted canonical relative names, USTAR regular entries only, mode 0644, uid/gid/mtime zero and empty owner names. XZ uses LZMA2 preset 6, an 8 MiB dictionary and CRC64. The process address-space ceiling is 256 MiB. Base64 is canonical 76-column ASCII with LF and final LF. Two independent archive constructions must produce identical bytes. The packer verifies the raw and Base64-decoded member inventories before freezing only its ten own packaging artifacts at mode 0444. No archive directories, symlinks, hardlinks or device entries are stored. Original input file modes are unchanged.

`PACKING_VERIFICATION.json` records the completed packaging checks. All source evidence retains its original historical meaning: preserving a successful review/Ready receipt does not manufacture a merge result or authorize this packer to perform a remote action.
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    root, output = args.root.resolve(), args.output.resolve()
    require(output != root and output not in (root / "pr153-publication", root / "pr153-delivery-watch", root / "pr153-remote-readback"),
            "Output overlaps protected input")
    require(output.is_dir() and not output.is_symlink(), "Missing or unsafe output directory")
    require(set(p.name for p in output.iterdir()) == {"pack_delivery.py", "verify_delivery.py"}, "Output must contain only the two scripts")
    _, hard = resource.getrlimit(resource.RLIMIT_AS)
    limit = 256 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (limit if hard < 0 else min(limit, hard), hard))
    payload, excluded = snapshot(root)
    require(len(payload) == 26, "Unexpected requested payload count")
    watch_manifest = json.loads(payload["pr153-delivery-watch/MANIFEST.json"])
    require(len(watch_manifest["files"]) == 19, "Unexpected raw readback count")
    expected_watch = {"pr153-delivery-watch/" + entry["path"]: entry for entry in watch_manifest["files"]}
    require({name for name in payload if name.startswith("pr153-delivery-watch/")} ==
            set(expected_watch) | {"pr153-delivery-watch/MANIFEST.json"}, "Watch manifest coverage mismatch")
    for name, entry in expected_watch.items():
        actual = identity(payload[name])
        require(actual["bytes"] == entry["bytes"] and actual["sha256"] == entry["sha256"], "Watch manifest mismatch: " + name)
    exclusion_report = exclusions(payload, excluded)
    screening = screen(payload)
    entries = [{"path": name, **identity(data)} for name, data in payload.items()]
    manifest = {"schema": 1, "file_count": len(entries), "total_bytes": sum(map(len, payload.values())),
                "files": entries, "source_scope": "Exact requested delivery snapshot; no semantic/proof review repeated.",
                "primary_publication_commit": COMMIT}
    archive = make_archive(payload)
    require(make_archive(payload) == archive, "Deterministic rebuild mismatch")
    require(verify_members(archive, entries) == payload, "Raw member roundtrip mismatch")
    encoded = base64.encodebytes(archive)
    decoded = base64.b64decode(b"".join(encoded.splitlines()), validate=True)
    require(decoded == archive and verify_members(decoded, entries) == payload, "Base64/member roundtrip mismatch")
    require(snapshot(root) == (payload, excluded), "Input membership or bytes changed during packing")
    (output / "delivery-evidence.tar.xz").write_bytes(archive)
    (output / "delivery-evidence.tar.xz.b64").write_bytes(encoded)
    (output / "README.md").write_text(README, encoding="utf-8")
    json_write(output / "PAYLOAD_MANIFEST.json", manifest)
    json_write(output / "EXCLUSIONS.json", exclusion_report)
    json_write(output / "CONTENT_SCREENING.json", screening)
    json_write(output / "PACKING_VERIFICATION.json", {
        "schema": 1, "status": "PASS", "payload_files": len(entries), "payload_bytes": manifest["total_bytes"],
        "excluded_duplicate_files": exclusion_report["file_count"], "excluded_duplicate_bytes": exclusion_report["total_bytes"],
        "watch_manifest_members_verified": 19, "deterministic_two_constructions_equal": True,
        "raw_archive_complete_member_verification": True, "strict_base64_roundtrip": True,
        "decoded_archive_complete_member_verification": True, "all_input_bytes_and_membership_unchanged": True,
        "address_space_limit_bytes": limit, "lzma_dictionary_bytes": 8 * 1024 * 1024,
        "network_used": False, "lean_executed": False, "source_deleted_or_modified": False,
        "freeze_policy": "Only the ten named artifacts owned by this package are set to mode 0444 after successful verification."})
    artifact_entries = [{"path": name, **identity(read_regular(output / name))} for name in sorted(OWN_FILES)
                        if name != "ARCHIVE_MANIFEST.json"]
    json_write(output / "ARCHIVE_MANIFEST.json", {
        "schema": 1, "primary_publication_commit": COMMIT, "archive_identity": identity(archive),
        "base64_identity": identity(encoded), "member_count": len(entries), "payload_bytes": manifest["total_bytes"],
        "artifacts": artifact_entries,
        "self_exclusion": "Only ARCHIVE_MANIFEST.json omits its own identity to avoid self-reference.",
        "determinism": {"tar": "USTAR", "sort": "lexicographic path", "regular_files_only": True,
                        "uid": 0, "gid": 0, "mtime": 0, "mode": "0644", "uname": "", "gname": "",
                        "xz": "LZMA2 preset 6, 8 MiB dictionary, CRC64", "base64": "76 columns, LF, final LF"}})
    result = verify(output)
    require(snapshot(root) == (payload, excluded), "Input bytes changed before freeze")
    for name in OWN_FILES:
        (output / name).chmod(0o444)
    require(all((output / name).stat().st_mode & 0o777 == 0o444 for name in OWN_FILES), "Freeze mode mismatch")
    result["artifacts"] = [{"path": name, **identity(read_regular(output / name))} for name in sorted(OWN_FILES)]
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
