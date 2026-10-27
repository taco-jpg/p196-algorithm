#!/usr/bin/env python3
"""Build the uniform saturated-exterior experiment from pinned existing cores.

Agent 118 PR399 supplies exact automata operations; Agent 108 PR386 supplies
the original four-phase tile builder.  Generated includes stay outside git.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

from build_center import SOURCE, SOURCE_SHA256, patched_source, replace_once

REGULAR = Path(__file__).with_name("center_regular.cpp")
REGULAR_SHA256 = "8b7c00df5282f156bb027dfb5709d4ad82f7af614dec355fc8b6d93a86f27d19"
TILE_COMMIT = "9b3f0c26d3482b93e4f13a6fe9194e8d3dcb1a5f"
TILE_SHA256 = "3463604f5332e2d2bd60686de7f5fac0f3770b2ab09ccc3baa3a96a2615034c3"
TILE_URL = ("https://raw.githubusercontent.com/taco-jpg/p196-algorithm/"
            + TILE_COMMIT + "/calculation/agent-108/saturation_mdd.cpp")


def checked(raw: bytes, expected: str, name: str) -> str:
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected:
        raise RuntimeError(f"UNDECIDED {name}_sha256_mismatch: {actual}")
    return raw.decode("utf-8")


def tile_header(source: str) -> str:
    anchors = ["struct Tile {", "static unsigned long long number(",
               "static bool terminal_symbol(int s)", "struct Node {"]
    if any(source.count(anchor) != 1 for anchor in anchors):
        raise RuntimeError("UNDECIDED tile_source_anchor_mismatch")
    declarations = source[source.index(anchors[0]):source.index(anchors[1])]
    arithmetic = source[source.index(anchors[2]):source.index(anchors[3])]
    return ("// Verbatim pinned arithmetic from Agent108 PR386; no MDD search copied.\n"
            "namespace Tiles108 {\n" + declarations + arithmetic + "}\n")


def build(output_dir: Path, sanitize: bool = False, cxx: str = "c++",
          tiles_source: Path | None = None) -> Path:
    output_dir = Path(output_dir).resolve()
    repository = SOURCE.parents[3].resolve()
    if output_dir == repository or repository in output_dir.parents:
        raise ValueError("generated includes/binary must be outside the repository")
    output_dir.mkdir(parents=True, exist_ok=True)
    regular = checked(REGULAR.read_bytes(), REGULAR_SHA256, "regular_core")
    regular = replace_once(regular, "int main(int argc, char** argv) {",
                           "int center_regular_program118(int argc, char** argv) {")
    if tiles_source is None:
        tiles_source = output_dir / "agent108_saturation_mdd.cpp"
        if not tiles_source.exists():
            with urllib.request.urlopen(TILE_URL, timeout=30) as response:
                raw = response.read()
            checked(raw, TILE_SHA256, "agent108_tiles")
            tiles_source.write_bytes(raw)
    tile_source = checked(Path(tiles_source).read_bytes(), TILE_SHA256, "agent108_tiles")
    (output_dir / "cauto118_core.hpp").write_text(patched_source())
    (output_dir / "regular118_core.hpp").write_text(regular)
    (output_dir / "tiles108_core.hpp").write_text(tile_header(tile_source))
    flags = (["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
             if sanitize else ["-O2"])
    binary = output_dir / "exterior_regular"
    source = Path(__file__).with_name("exterior_regular.cpp")
    subprocess.run([cxx, "-std=c++17", *flags, "-I", str(output_dir), str(source),
                    "-o", str(binary)], check=True, timeout=180)
    return binary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=Path("/tmp/p196-agent118-exterior-regular"))
    parser.add_argument("--tiles-source", type=Path)
    parser.add_argument("--sanitize", action="store_true")
    parser.add_argument("--cxx", default="c++")
    args = parser.parse_args()
    binary = build(args.out_dir, args.sanitize, args.cxx, args.tiles_source)
    print(json.dumps({"binary": str(binary), "upstream_sha256": SOURCE_SHA256,
                      "regular_core_sha256": REGULAR_SHA256, "tiles_sha256": TILE_SHA256,
                      "exterior_sha256": hashlib.sha256(
                          Path(__file__).with_name("exterior_regular.cpp").read_bytes()).hexdigest(),
                      "sanitizers": args.sanitize}, sort_keys=True))


if __name__ == "__main__":
    main()
