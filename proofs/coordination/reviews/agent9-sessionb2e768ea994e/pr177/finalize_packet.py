#!/usr/bin/env python3
"""Freeze the small final delivery packet; no source or proof execution."""
from pathlib import Path
import hashlib
import json
import sys

out = Path(__file__).resolve().parent
root = out.parent
prefix = "proofs/coordination/reviews/agent9-sessionb2e768ea994e/pr177/"
task_path = "proofs/coordination/tasks/agent9-sessionb2e768ea994e-pr177-delivery-20261017.json"
sources = {
    "READINESS_AND_HANDOFF.md": root / "READINESS_AND_HANDOFF.md",
    "stage002-remote-readback.py": root / "stage002-remote-readback.py",
    "stage002-remote-readback.json": root / "stage002-remote-readback.json",
    "queue-availability-refresh.json": root / "queue-availability-refresh/refresh-pr161-pr167-20261017T055043Z.json",
}
for name, source in sources.items():
    (out / name).write_bytes(source.read_bytes())
names = [
    "READINESS_AND_HANDOFF.md", "READINESS_RECEIPT.json", "PR_DESCRIPTION_AFTER.md",
    "registry-endpoint.patch", "registry-corrected.json",
    "stage002-remote-readback.py", "stage002-remote-readback.json",
    "queue-availability-refresh.json", "PREPARATION_ATTEMPTS.json",
    "finalize_packet.py", "TASK_FINAL.json",
]
entries = []
payload = []
for name in names:
    data = (out / name).read_bytes()
    content = data.decode("utf-8")
    repo_path = task_path if name == "TASK_FINAL.json" else prefix + name
    sha = hashlib.sha256(data).hexdigest()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    entries.append({"file": name, "repository_path": repo_path, "bytes": len(data), "sha256": sha, "git_blob": blob})
    payload.append({"path": repo_path, "mode": "100644", "type": "blob", "content": content})
assert next(x for x in entries if x["file"] == "registry-endpoint.patch")["sha256"] == "8dcca936bb19e050e2e8d5cabe7690350e372c4282b8445af068784338fcd229"
task = json.loads((out / "TASK_FINAL.json").read_text())
assert task["status"] == "EXTERNALLY_BLOCKED"
assert not task["active_editing"] and task["delivery_ownership_retained"]
assert not task["readiness"]["actual_draft"] and not task["readiness"]["actual_merged"]
manifest = {
    "schema_version": 1,
    "title": "PR177 actual readiness and external handoff final packet",
    "status": "PASS_LOCAL_BYTES_AND_PREPARED_STATE",
    "scope": "Supplemental delivery metadata, readbacks, exact registry repair and ownership evidence. No source or main mutation, merge, Lean rerun or duplicate formal review.",
    "self_exclusion": "This manifest excludes itself; every other new published file including the canonical task and this executed inventory program is listed.",
    "file_count_excluding_manifest": len(entries),
    "total_bytes_excluding_manifest": sum(x["bytes"] for x in entries),
    "entries": entries,
}
manifest_text = json.dumps(manifest, indent=2) + "\n"
(out / "PACKET_MANIFEST_003.json").write_text(manifest_text)
payload.append({"path": prefix + "PACKET_MANIFEST_003.json", "mode": "100644", "type": "blob", "content": manifest_text})
if "--payload" in sys.argv:
    print(json.dumps({"manifest": manifest, "tree_elements": payload}, ensure_ascii=False))
else:
    print(json.dumps(manifest, indent=2))
