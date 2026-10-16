#!/usr/bin/env python3
"""Record default verification and one fresh extraction of this evidence archive."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


here = Path(__file__).resolve().parent
repo = here.parents[4]
manifest_path = here / "final-independent-manifest.json"
manifest = json.loads(manifest_path.read_text())
helper = here / "final-independent-verify.py"
record_path = here / "final-independent-validation.json"
log_path = here / "final-independent-validation.log"
if record_path.exists() or log_path.exists():
    raise SystemExit("Refusing to overwrite the original validation records")
restore = Path(tempfile.mkdtemp(prefix="agent101-final-independent-restore-"))
records = []
report = {
    "status": "IN_PROGRESS",
    "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    "source_commit": manifest["source_commit"],
    "archive": manifest["archive"],
    "manifest_sha256": digest(manifest_path.read_bytes()),
    "helper_sha256": digest(helper.read_bytes()),
    "restore_directory": str(restore),
    "policy": "Only default member verification, one fresh safe extraction, and comparison with original bytes. No Lean or Git invocation and no repeat of the previously reviewed helper's nine test cases.",
    "commands": records,
}


def save():
    record_path.write_text(json.dumps(report, indent=2) + "\n")


def run(label, args):
    command = [sys.executable, str(helper)] + args
    result = subprocess.run(command, cwd=here, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    rec = {"label": label, "command": command, "cwd": str(here),
           "returncode": result.returncode, "output": result.stdout}
    records.append(rec)
    with log_path.open("a") as log:
        log.write(json.dumps({"label": label, "command": command}) + "\n")
        log.write(result.stdout)
    save()
    if result.returncode:
        report["status"] = "FAIL"
        save()
        raise SystemExit(result.returncode)
    parsed = json.loads(result.stdout)
    assert parsed["members_verified"] == manifest["archive"]["member_count"]
    return parsed


default = run("default-verify-only", [])
assert default["files_written"] == default["identical_files_skipped"] == 0
extracted = run("one-fresh-safe-extraction", ["--extract-to", str(restore)])
assert extracted["files_written"] == manifest["archive"]["member_count"]
assert extracted["identical_files_skipped"] == 0

expected_names = {row["path"] for row in manifest["members"]}
actual_names = {p.relative_to(restore).as_posix() for p in restore.rglob("*") if p.is_file()}
assert actual_names == expected_names
compared = []
for row in manifest["members"]:
    restored = restore / row["path"]
    origin = row["origin"]
    source_root = repo if origin["kind"] == "repository" else Path(manifest["canonical_origin_root"])
    original = source_root / origin["path"]
    actual = restored.read_bytes()
    assert actual == original.read_bytes(), row["path"]
    assert len(actual) == row["bytes"] and digest(actual) == row["sha256"]
    assert not any(restored.name.endswith(s) for s in manifest["excluded_policy"]["filename_endings"])
    compared.append({"path": row["path"], "sha256": row["sha256"], "bytes": len(actual),
                     "restored_equals_original": True})
for item in manifest["sidecar_helpers"]:
    assert digest((here / item["filename"]).read_bytes()) == item["sha256"]
report.update({"status": "PASS", "members_verified": len(compared),
               "members_restored_and_compared_with_original_bytes": len(compared),
               "exact_restored_member_set": True, "original_files_unchanged": True,
               "compiler_objects_and_caches_in_payload": False,
               "prior_archive_member_path_overlap": manifest["prior_archive_member_path_overlap"],
               "comparisons": compared,
               "validation_log_sha256": digest(log_path.read_bytes())})
save()
print(json.dumps({"status": "PASS", "members": len(compared),
                  "archive_sha256": manifest["archive"]["sha256"],
                  "archive_bytes": manifest["archive"]["bytes"],
                  "restored_and_compared": len(compared),
                  "restore_directory": str(restore)}))
