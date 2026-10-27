#!/usr/bin/env python3
"""Compare complete decoded generic frontiers with the pinned explicit engine.

Command:
  python3 calculation/agent-111/regular_frontier_controls.py --binary /tmp/agent111_regular

Each subprocess has a 25 second wall cap and 3 GiB address cap. The regular
run intentionally stops after its requested generic layer; a layer-horizon
notice is acceptable ONLY after the requested complete export was printed.
No resource-capped export or count-only equality is accepted. The temporal
unit is kept in the regular engine and repeated explicitly in original Fast.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import resource
import subprocess
import tempfile

import long_center
import regular_center


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def build_explicit(output: Path) -> Path:
    directory = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="agent111-explicit-frontier-") as temp:
        (Path(temp) / "a111_existing.hpp").write_text(long_center.patched_source(), encoding="utf-8")
        subprocess.run(["c++", "-std=c++17", "-O2", "-I", temp,
                        str(directory / "regular_frontier_explicit.cpp"), "-o", str(output)],
                       check=True, timeout=180)
    return output


def run_explicit(binary: Path, base: int, e: str, g: str, v: str,
                 repetitions: int, layer: int, timeout: float = 25) -> subprocess.CompletedProcess[str]:
    command = [str(binary.resolve()), str(base), e * repetitions, g * repetitions, "1", "1",
               "-v", v * repetitions, "-layers", str(layer), "-unit-k", str(v.count("1")),
               "-cap", "300000"]

    def bounds() -> None:
        resource.setrlimit(resource.RLIMIT_AS, (3072 * 1024**2,) * 2)
        resource.setrlimit(resource.RLIMIT_CPU, (math.ceil(timeout) + 1, math.ceil(timeout) + 2))

    return subprocess.run(command, text=True, capture_output=True, timeout=timeout,
                          preexec_fn=bounds, check=False)


def canonical_word(raw: list[dict], unit_k: int, repetitions: int) -> bytes:
    require(len(raw) == unit_k * repetitions, "exported tuple has incorrect segment count")
    encoded = bytearray()
    for position, segment in enumerate(raw):
        require(set(segment) == {"type", "z", "cfg"}, "unexpected segment fields")
        kind, z, cfg = segment["type"], segment["z"], segment["cfg"]
        require(type(kind) is int and kind == position % unit_k, "incorrect segment type sequence")
        require(type(z) is int and -1 <= z <= 123, "z outside signed carry domain")
        require(isinstance(cfg, list) and 0 < len(cfg) <= 144 and len(cfg) % 3 == 0,
                "configuration length outside local temporal domain")
        require(all(type(x) is int and 0 <= x <= 255 for x in cfg), "configuration byte outside domain")
        # These length-delimited byte strings are an injective encoding of
        # the complete decoded word, including signed z and type boundaries.
        encoded.extend((kind, z + 1, len(cfg)))
        encoded.extend(cfg)
    return bytes(encoded)


def parse_words(stdout: str, prefix: str, layer: int, unit_k: int, repetitions: int) -> set[bytes]:
    words = set()
    lines = 0
    for line in stdout.splitlines():
        if not line.startswith(prefix + " "):
            continue
        found = re.search(r"\blayer=(\d+)\b", line)
        require(found is not None and int(found[1]) == layer, "wrong exported layer")
        require(" word=" in line, "word payload missing")
        raw = json.loads(line.split(" word=", 1)[1])
        require(isinstance(raw, list), "word must be a JSON list")
        word = canonical_word(raw, unit_k, repetitions)
        require(word not in words, "duplicate decoded word in purported set")
        words.add(word)
        lines += 1
    require(lines == len(words), "word-set duplicate accounting failure")
    return words


def compare_case(binary: Path, explicit: Path, base: int, e: str, g: str, v: str,
                 repetitions: int, layer: int) -> dict[str, int]:
    unit_k = v.count("1")
    regular = regular_center.run(
        binary, base, e, g, 1, 1, v, generic_only=True, layers=layer,
        cap=500000, edge_cap=12000000, work_cap=150000000,
        timeout=25, memory_mb=3072, export_layer=layer, export_k=repetitions,
        export_limit=300000)
    require(regular.returncode == 0, f"regular export failed: {regular.stderr}")
    allowed = f"UNDECIDED: generic layer horizon={layer}"
    require(not regular.stderr.strip() or regular.stderr.strip() == allowed,
            f"regular export resource or runtime failure: {regular.stderr}")
    completion = re.findall(r"^REGULAR_EXPORT layer=(\d+) k=(\d+) words=(\d+)$",
                            regular.stdout, re.MULTILINE)
    require(len(completion) == 1 and tuple(map(int, completion[0][:2])) == (layer, repetitions),
            "missing completed regular export")
    actual = parse_words(regular.stdout, "REGULAR_WORD", layer, unit_k, repetitions)
    require(len(actual) == int(completion[0][2]), "regular export size does not match complete set")
    del regular

    reference = run_explicit(explicit, base, e, g, v, repetitions, layer)
    require(reference.returncode == 0 and not reference.stderr.strip(),
            f"explicit export failed: {reference.stderr}")
    completion = re.findall(r"^EXPLICIT_DONE layer=(\d+) tuples=(\d+) unit_k=(\d+) repetitions=(\d+)$",
                            reference.stdout, re.MULTILINE)
    require(len(completion) == 1, "missing completed explicit export")
    numbers = tuple(map(int, completion[0]))
    require((numbers[0], numbers[2], numbers[3]) == (layer, unit_k, repetitions),
            "explicit completion has wrong geometry")
    expected = parse_words(reference.stdout, "EXPLICIT_WORD", layer, unit_k, repetitions)
    require(len(expected) == numbers[1], "explicit size does not match complete set")
    require(actual == expected,
            f"COMPLETE FRONTIER MISMATCH b={base} k={repetitions} layer={layer}: "
            f"regular={len(actual)} explicit={len(expected)} "
            f"missing={len(expected - actual)} extra={len(actual - expected)}")
    return {"base": base, "unit_period": len(e), "repetitions": repetitions,
            "layer": layer, "equal_complete_words": len(actual)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--explicit-binary", type=Path)
    args = parser.parse_args()
    cases = []
    cases += [(10, "10100110011", "11100010000", "01000010000", 1, layer) for layer in range(1, 7)]
    cases += [(10, "10100110011", "11100010000", "01000010000", 2, layer) for layer in range(1, 4)]
    # This base-2 unit comes from the known certificate's carry/overflow
    # streams. Positive finite tails are independently covered by the adapter
    # smoke; here arbitrary repeated-unit generic frontiers are compared.
    cases += [(2, "1010", "1010", "0001", k, layer) for k in (1, 2, 3) for layer in (1, 2, 3)]
    results = []
    with tempfile.TemporaryDirectory(prefix="agent111-frontier-controls-") as temp:
        explicit = args.explicit_binary or build_explicit(Path(temp) / "explicit")
        for case in cases:
            result = compare_case(args.binary, explicit, *case)
            results.append(result)
            print("FRONTIER_CASE " + json.dumps(result, sort_keys=True), flush=True)
    directory = Path(__file__).resolve().parent
    names = ("regular.hpp", "regular_center.cpp", "regular_center.py",
             "regular_frontier_controls.py", "regular_frontier_explicit.cpp")
    hashes = {name: hashlib.sha256((directory / name).read_bytes()).hexdigest() for name in names}
    print("FRONTIER_CONTROLS " + json.dumps({
        "complete_set_comparisons": len(results),
        "decoded_words_compared": sum(result["equal_complete_words"] for result in results),
        "largest_complete_frontier": max(result["equal_complete_words"] for result in results),
        "source_sha256": long_center.SOURCE_SHA256,
        "production_and_control_sha256": hashes}, sort_keys=True))
    print("ALL REGULAR FRONTIER CONTROLS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
