#!/usr/bin/env python3
"""Install the pinned official discovery-only Z3 wheel into an isolated directory."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import urllib.request
import zipfile

VERSION = "4.15.4.0"
FILENAME = "z3_solver-4.15.4.0-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
EXPECTED_SHA256 = "7e103a6f203f505b8b8b8e5c931cc407c95b61556512d4921c1ddc0b3f41b08e"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--receipt", type=Path, required=True)
    args = ap.parse_args()
    target = args.target.resolve()
    target.mkdir(parents=True, exist_ok=False)
    metadata_url = f"https://pypi.org/pypi/z3-solver/{VERSION}/json"
    with urllib.request.urlopen(metadata_url, timeout=30) as response:
        metadata = json.load(response)
    record = next(x for x in metadata["urls"] if x["filename"] == FILENAME)
    assert record["digests"]["sha256"] == EXPECTED_SHA256
    assert record["url"].startswith("https://files.pythonhosted.org/")
    wheel = target / FILENAME
    with urllib.request.urlopen(record["url"], timeout=60) as response:
        wheel.write_bytes(response.read())
    digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
    assert digest == EXPECTED_SHA256
    packages = target / "packages"
    packages.mkdir()
    with zipfile.ZipFile(wheel) as archive:
        for item in archive.infolist():
            assert (packages / item.filename).resolve().is_relative_to(packages)
        archive.extractall(packages)
    sys.path.insert(0, str(packages))
    import z3
    receipt = {
        "status": "PINNED_DISCOVERY_SOLVER_AVAILABLE",
        "role": "Candidate discovery only; solver outputs are not Lean proofs.",
        "version": VERSION,
        "runtime_version": z3.get_full_version(),
        "metadata_url": metadata_url,
        "wheel_url": record["url"],
        "wheel_sha256": digest,
        "packages": str(packages),
        "library_sha256": hashlib.sha256((packages / "z3/lib/libz3.so").read_bytes()).hexdigest(),
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
