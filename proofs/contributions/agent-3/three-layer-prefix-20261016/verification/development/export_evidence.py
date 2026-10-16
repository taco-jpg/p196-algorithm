#!/usr/bin/env python3
"""Copy a completed canonical run's portable evidence without its objects."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", required=True, type=Path)
    args = parser.parse_args()
    verify = Path(__file__).resolve().parents[1]
    build = args.build_dir.resolve()
    report = json.loads((build / "verification.json").read_text())
    assert report["status"] == "PASS"
    assert len(report["source_records"]) == 27
    assert report["audit"]["explicit_declaration_count"] == 231
    assert report["audit"]["logical_export_count"] == 373
    assert all(command["exit_code"] == 0 for command in report["commands"])
    assert sha(verify / "verify.py") == report["verifier_sha256"]
    assert sha(verify / "source-pins.json") == report["manifest_sha256"]
    assert (build / "source-pins.json").read_bytes() == (verify / "source-pins.json").read_bytes()
    evidence = verify / "evidence"
    if evidence.exists() and any(evidence.iterdir()):
        raise RuntimeError("Evidence directory is nonempty; existing records will not be overwritten")
    evidence.mkdir(exist_ok=True)
    (evidence / "logs").mkdir()
    for filename in ("verification.json", "source-pins.json"):
        shutil.copyfile(build / filename, evidence / filename)
    for filename in ("ExportInventory.lean", "AllExportedAxioms.lean"):
        shutil.copyfile(build / "modules" / filename, evidence / filename)
    for command in report["commands"]:
        source = Path(command["log"])
        assert sha(source) == command["log_sha256"]
        shutil.copyfile(source, evidence / "logs" / source.name)
    files = [{"path": str(path.relative_to(evidence)), "bytes": path.stat().st_size,
              "sha256": sha(path)}
             for path in sorted(evidence.rglob("*")) if path.is_file()]
    assert len(files) == 35
    index = {
        "schema_version": 1, "source_run_status": report["status"],
        "mathematical_source_commit": "6ce47fddb10f15b4af1025954f1694825093673d",
        "manifest_sha256": report["manifest_sha256"],
        "verifier_sha256": report["verifier_sha256"],
        "file_count_excluding_index": len(files), "files": files,
    }
    target = evidence / "artifact-index.json"
    target.write_text(json.dumps(index, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "artifact_index": str(target),
                      "indexed_file_count": len(files), "index_sha256": sha(target),
                      "report_sha256": sha(evidence / "verification.json")}, indent=2))


if __name__ == "__main__":
    main()
