#!/usr/bin/env python3
"""Build the exact p12 regular-language experiment against the pinned local core."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from build_center import SOURCE, SOURCE_SHA256, patched_source


def build(output_dir: Path, sanitize: bool = False, cxx: str = "c++") -> Path:
    output_dir = Path(output_dir).resolve()
    repository = SOURCE.parents[3].resolve()
    if output_dir == repository or repository in output_dir.parents:
        raise ValueError("generated header/binary must be outside the repository")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "cauto118_core.hpp").write_text(patched_source())
    source = Path(__file__).with_name("center_regular.cpp")
    binary = output_dir / "center_regular"
    flags = (["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
             if sanitize else ["-O2"])
    subprocess.run([cxx, "-std=c++17", *flags, "-I", str(output_dir), str(source),
                    "-o", str(binary)], check=True, timeout=180)
    return binary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=Path("/tmp/p196-agent118-regular"))
    parser.add_argument("--sanitize", action="store_true")
    parser.add_argument("--cxx", default="c++")
    args = parser.parse_args()
    binary = build(args.out_dir, args.sanitize, args.cxx)
    print(json.dumps({"binary": str(binary), "upstream_sha256": SOURCE_SHA256,
                      "regular_sha256": hashlib.sha256(
                          Path(__file__).with_name("center_regular.cpp").read_bytes()).hexdigest(),
                      "sanitizers": args.sanitize}, sort_keys=True))


if __name__ == "__main__":
    main()
