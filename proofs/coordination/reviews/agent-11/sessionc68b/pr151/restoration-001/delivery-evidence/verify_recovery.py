#!/usr/bin/env python3
"""Compare actual recovered bytes to every input, and reproduce the compressed archive."""
import importlib.util
import json
from pathlib import Path
import stat

OUT = Path(__file__).resolve().parent
WORKSPACE = OUT.parents[1]
spec = importlib.util.spec_from_file_location("delivery_bundle_builder", OUT / "build_bundle.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
manifest = json.loads((OUT / "MEMBER_MANIFEST.json").read_text())
records = manifest["records"]
recovered = OUT / "recovery-check-001"
lookup = {}
for rec in records:
    source = WORKSPACE / rec["original_path"]
    target = recovered / rec["archive_path"]
    if source.read_bytes() != target.read_bytes():
        raise ValueError(f"Direct original/recovered byte mismatch: {source}")
    if stat.S_IMODE(source.stat().st_mode) != stat.S_IMODE(target.stat().st_mode):
        raise ValueError(f"Direct original/recovered mode mismatch: {source}")
    lookup[rec["archive_path"]] = target
reproduced = OUT / "reproduction-check-001.tar.xz"
with reproduced.open("xb") as handle:
    builder.build_tar_xz(records, lookup, handle)
archive_path = OUT / manifest["archive"]["path"]
if reproduced.read_bytes() != archive_path.read_bytes():
    raise ValueError("Reproducible archive check failed: compressed bytes differ")
receipt = json.loads((OUT / "recovery-check-001.stdout").read_text())
report = {
    "status": "PASS_ACTUAL_RECOVERY_AND_DETERMINISTIC_COMPRESSED_BYTE_REPRODUCTION",
    "actual_recovery": receipt,
    "direct_comparison": {
        "every_original_file_compared_to_recovered_bytes": True,
        "every_original_mode_compared_to_recovered_mode": True,
        "compared_files": len(records),
        "compared_uncompressed_bytes": sum(r["bytes"] for r in records),
    },
    "deterministic_reproduction": {
        "reconstructed_from": "actual recovered files and complete MEMBER_MANIFEST.json",
        "compressed_bytes_equal_to_original_archive": True,
        "archive": builder.digest(reproduced.read_bytes()),
        "duplicate_local_path": reproduced.name,
        "publication_exclusion_reason": "Exact duplicate generated infrastructure retained locally; original archive/transport already included.",
    },
    "recovery_stdout": builder.digest((OUT / "recovery-check-001.stdout").read_bytes()),
    "recovery_stderr": builder.digest((OUT / "recovery-check-001.stderr").read_bytes()),
    "recovery_tool": builder.digest((OUT / "recover_bundle.py").read_bytes()),
    "verification_tool": builder.digest(Path(__file__).read_bytes()),
    "research_or_verifier_scripts_executed": 0,
    "lean_invocations": 0,
    "remote_operations": 0,
}
result_bytes = builder.jsonbytes(report)
with (OUT / "RECOVERY_AND_REPRODUCIBILITY.json").open("xb") as handle:
    handle.write(result_bytes)
print(result_bytes.decode(), end="")
