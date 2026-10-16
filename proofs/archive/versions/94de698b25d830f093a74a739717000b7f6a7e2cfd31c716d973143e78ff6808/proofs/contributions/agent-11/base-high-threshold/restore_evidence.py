#!/usr/bin/env python3
"""Verify lossless development/audit evidence; optionally restore to a fresh directory."""
from __future__ import annotations
import argparse
import hashlib
import json
import lzma
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
PINS = {
    "development-records.json.xz": "160a71416aa089e2a013ad08c36cebe8d0cf5d41337348c662dedb65b179376e",
    "audit-records.json.xz": "76fa57c48f71738a91d9eb64c5e4ebebdc3157d2a14951963d60b8d9ad04b2f2",
}

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def load(name: str):
    data = (HERE / "evidence" / name).read_bytes()
    if sha(data) != PINS[name]:
        raise ValueError(f"Evidence archive hash mismatch: {name}")
    return json.loads(lzma.decompress(data, format=lzma.FORMAT_XZ, memlimit=128*1024*1024))

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="restore all original bytes into this new directory")
    parser.add_argument("--source-dir", type=Path, default=HERE,
                        help="five-module source directory at checkpoint 42a165aac1028d261dd4b1bd245c2e169748ff39")
    args = parser.parse_args()
    recovered: dict[str, bytes] = {}
    def retain(name: str, data: bytes, digest: str | None = None) -> None:
        p = PurePosixPath(name)
        if p.is_absolute() or ".." in p.parts or str(p) != name or name in recovered:
            raise ValueError(f"Unsafe or duplicate evidence path: {name}")
        if digest is not None and sha(data) != digest:
            raise ValueError(f"Restored evidence hash mismatch: {name}")
        recovered[name] = data
    attempts = load("development-records.json.xz")
    for item in attempts:
        if PurePosixPath(item["base"]).name != item["base"]:
            raise ValueError("Source base must be a plain filename")
        original = (args.source_dir / item["base"]).read_bytes()
        if sha(original) != item["base_sha256"]:
            raise ValueError(f"Source changed: use the pinned checkpoint source for {item['base']}")
        lines = original.decode("utf-8").splitlines(keepends=True)
        last_end = 0
        for start, end, replacement in item["edits"]:
            if not (last_end <= start <= end <= len(lines)) or not all(isinstance(x,str) for x in replacement):
                raise ValueError("Malformed lossless source edit")
            last_end = end
        for start, end, replacement in reversed(item["edits"]):
            lines[start:end] = replacement
        retain("development/" + item["path"], "".join(lines).encode("utf-8"), item["sha256"])
        retain("development/" + item["log_name"], item["log"].encode("utf-8"))
    audits = load("audit-records.json.xz")
    for item in audits["files"]:
        retain(item["path"], item["text"].encode("utf-8"), item["sha256"])
    if len(attempts) != 15 or len(audits["files"]) != 24 or len(recovered) != 54:
        raise ValueError("Unexpected evidence coverage")
    index = {
        "source_snapshot": audits["source_snapshot"],
        "verified_ci_commit": audits["verified_ci_commit"],
        "ci_run_id": audits["ci_run_id"],
        "ci_artifact_id": audits["ci_artifact_id"],
        "ci_zip_sha256": audits["ci_zip_sha256"],
        "files": [{"path": k, "bytes": len(v), "sha256": sha(v)} for k,v in sorted(recovered.items())],
        "independent_semantic_review": False,
        "meaning": "Exact retained historical evidence, not a new Lean execution or semantic review.",
    }
    if args.out is not None:
        out = args.out.resolve()
        out.mkdir(parents=True, exist_ok=False)
        for name, data in recovered.items():
            target = out / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        (out / "evidence-index.json").write_text(json.dumps(index, indent=2) + "\n")
    print(f"VERIFIED: {len(attempts)} development snapshots with exact logs, {len(audits['files'])} audit files; {len(recovered)} original research files")

if __name__ == "__main__":
    main()
