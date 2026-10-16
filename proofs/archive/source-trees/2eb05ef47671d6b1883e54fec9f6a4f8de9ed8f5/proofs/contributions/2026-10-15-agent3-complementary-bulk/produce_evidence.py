"""Rebuild and independently verify every bounded certificate, without network.

Run: python produce_evidence.py [--output evidence]
This script writes research evidence only; it never modifies Git or publishes.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import tempfile

RAW_HASHES = (
    "de0ee34745f96056e6eedc3f3e543796fa844509b98a72508f6bb6813af50453",
    "7007a01cda6fd9e9feef8a30ca91f22c51316d4584f0536a09150c74d25d0580",
    "8c77b4f053457bd929a11c183999e482c57dca3e995664874bc2bd69650835ed",
    "5d94f43982656df40150da81a6a50862551366449ee08922c7f48e24dffa724c",
    "0491a155022bae6f691e0b8d567d6a3b78160b2124c2af94310e213b90d0c4f4",
    "8917501f07a42d99c6c352b927e89538c466ae9cb4881801bb4c9f7464825212",
)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def compress(data: bytes) -> bytes:
    encoded = bytearray(gzip.compress(data, compresslevel=9, mtime=0))
    encoded[9] = 255  # Platform-independent gzip OS field.
    return bytes(encoded)

def run(command: list[str], cwd: Path) -> bytes:
    result = subprocess.run(command, cwd=cwd, check=True, capture_output=True)
    if result.stderr:
        raise RuntimeError(f"Unexpected stderr from {command[0]}: {result.stderr.decode()}")
    return result.stdout

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("evidence"))
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    manifest = {"scope": "All trimmed even-phase outer states for bounds 0..5; no all-width or P196 claim.",
                "python": platform.python_version(), "compiler": "", "files": [], "sources": {}}
    for name in ("quotient.py", "verify.py", "outer_scan.cpp", "check_ranks.cpp", "produce_evidence.py"):
        manifest["sources"][name] = sha((source / name).read_bytes())
    manifest["compiler"] = run(["g++", "--version"], source).decode().splitlines()[0]
    with tempfile.TemporaryDirectory(prefix="agent3-check-") as temporary:
        temp = Path(temporary)
        for stem in ("outer_scan", "check_ranks"):
            run(["g++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-pedantic",
                 str(source / f"{stem}.cpp"), "-o", str(temp / stem)], source)
        for L, expected in enumerate(RAW_HASHES):
            raw_path = temp / f"ranks-L{L}.bin"
            scan_bytes = run([str(temp / "outer_scan"), str(L), str(raw_path)], source)
            raw = raw_path.read_bytes()
            if sha(raw) != expected:
                raise AssertionError(f"Rank bytes differ from original independently checked snapshot at L={L}")
            checked_bytes = run([str(temp / "check_ranks"), str(L), str(raw_path)], source)
            scan, checked = json.loads(scan_bytes), json.loads(checked_bytes)
            assert scan["valid_states"] == checked["checked_states"]
            assert scan["max_exit_time"] == checked["max_exit_time"]
            assert scan["rank_histogram"] == checked["histogram"]
            for name, data in ((f"scan-L{L}.json", scan_bytes), (f"check-L{L}.json", checked_bytes)):
                (output / name).write_bytes(data)
                manifest["files"].append({"path": name, "bytes": len(data), "sha256": sha(data)})
            zipped = compress(raw)
            name = f"ranks-L{L}.bin.gz"
            (output / name).write_bytes(zipped)
            manifest["files"].append({"path": name, "bytes": len(zipped), "sha256": sha(zipped),
                                      "compression": "gzip", "original_bytes": len(raw),
                                      "original_sha256": sha(raw), "restore": f"gzip -dc {name} > ranks-L{L}.bin"})
    # Preserve all 10,000 literal formula control pairs, not only their digest.
    import verify
    control_records = output / "formula-controls.jsonl.gz"
    result = {"formula_controls": verify.formula_controls(control_records),
              "outer_certificates": [verify.outer_certificate(L) for L in range(4)],
              "untrimmed_controls": [verify.outer_certificate(L, False) for L in range(3)]}
    data = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    (output / "results.json").write_bytes(data)
    manifest["files"].append({"path": "results.json", "bytes": len(data), "sha256": sha(data)})
    zipped = control_records.read_bytes()
    raw = gzip.decompress(zipped)
    assert sha(raw) == "df93bb87eb28247437d6704fd936e196c6f4be2f8a91ccb0e2ea0ce54fcaec5c"
    manifest["files"].append({"path": control_records.name, "bytes": len(zipped), "sha256": sha(zipped),
                              "compression": "gzip", "original_bytes": len(raw), "original_sha256": sha(raw),
                              "restore": "gzip -dc formula-controls.jsonl.gz > formula-controls.jsonl"})
    (output / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"verified": True, "bounds": [0, 1, 2, 3, 4, 5],
                      "formula_controls": result["formula_controls"], "evidence_files": len(manifest["files"])}, sort_keys=True))

if __name__ == "__main__":
    main()
