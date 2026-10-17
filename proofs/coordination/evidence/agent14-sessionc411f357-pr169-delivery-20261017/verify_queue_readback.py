#!/usr/bin/env python3
"""Read immutable published Git blobs and verify the full queue archive.

No proof compilation or remote mutation is performed. The local repository must
contain the specified commit; ordinary public promisor blob reads may occur.
"""
import argparse
import datetime
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

PREFIX = "proofs/coordination/evidence/agent14-sessionc411f357-pr169-delivery-20261017/"
EXPECTED = [
    ("CENSUS_53.md", 45018, "677ba8d969fb4cf09edcac3aeed9e1e0bec7f0a8207250f25338b1075dc00295", "5c7d49c769cbbc704ef61315f217a4ca67e466ac"),
    ("QUEUE_FOLLOWUP.md", 7685, "43a847af5e14690b088f00576c4ced6ae5566de26ec4508f1a5b8d0d3806b3ac", "4623913066fe2b4f529fbec814a9aed031bf9680"),
    ("QUEUE_FOLLOWUP_MANIFEST.json", 6075, "aceb859d8ad3775b290fa8d4670061a6cc7290e72c0efb922098dddcc34ec833", "f2047a2344d448ed680c03e3f0628e19f5f7c2ed"),
    ("QUEUE_FOLLOWUP_RECORDS.tar.xz", 865832, "e726a239ca3dac74fd4873f4d32e88ed4a56cf5362ad150f84c08a4b3eadd614", "0aa732787785346f5de2ccb4ae940b736fea5115"),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--commit", default="d059639daa6ca28c784a4f292997b5e4a5e96610")
    ap.add_argument("--output", required=True)
    a = ap.parse_args()
    records = []
    contents = {}
    for name, size, digest, git_blob in EXPECTED:
        argv = ["git", "-c", "credential.helper=", "-c", "core.askPass=", "cat-file", "blob", a.commit + ":" + PREFIX + name]
        p = subprocess.run(argv, cwd=a.repo, capture_output=True, check=False)
        record = {"path": PREFIX + name, "argv": argv, "exit_code": p.returncode, "stderr": p.stderr.decode(errors="replace"), "bytes": len(p.stdout), "sha256": sha(p.stdout), "git_blob": blob(p.stdout)}
        record["exact"] = p.returncode == 0 and (len(p.stdout), sha(p.stdout), blob(p.stdout)) == (size, digest, git_blob)
        records.append(record)
        if not record["exact"]:
            raise RuntimeError(json.dumps(record))
        contents[name] = p.stdout
    manifest = json.loads(contents["QUEUE_FOLLOWUP_MANIFEST.json"])
    expected = {e["path"]: e for e in manifest["files"]}
    recovered = []
    with tarfile.open(fileobj=io.BytesIO(contents["QUEUE_FOLLOWUP_RECORDS.tar.xz"]), mode="r:xz") as tf:
        members = tf.getmembers()
        assert len(members) == len(expected) == 20
        assert {m.name for m in members} == set(expected)
        for member in members:
            assert member.isfile()
            data = tf.extractfile(member).read()
            e = expected[member.name]
            assert (len(data), sha(data), blob(data)) == (e["bytes"], e["sha256"], e["git_blob"])
            recovered.append({"path": member.name, "bytes": len(data), "sha256": sha(data), "git_blob": blob(data), "exact": True})
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=a.repo, capture_output=True, text=True, check=True).stdout.strip()
    result = {
        "schema": "agent14-queue-followup-remote-readback-v1",
        "readback_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "evidence_commit": a.commit,
        "all_four_published_files_exact": True,
        "files": records,
        "all_twenty_archive_members_exact": True,
        "original_bytes": sum(e["bytes"] for e in recovered),
        "archive_members": recovered,
        "source_checkout_head": head,
        "source_checkout_head_unchanged": head == "d37aa2f2af91f2a073d741999310305bf626b77e",
        "proof_execution": "NOT_RUN",
        "remote_mutations": 0,
        "scope": "Actual public Git object bytes and full lossless member recovery. This does not assert a PR merge or mathematical review of the queue.",
    }
    Path(a.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("files", "archive_members")}))


if __name__ == "__main__":
    main()
