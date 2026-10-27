#!/usr/bin/env python3
"""Corroborate P25/G8 using an explicitly adapted, pinned Agent4 solver.

The caller supplies the original source fetched from the pinned GitHub commit.
Its Git blob and SHA256 must match. A NEW temporary copy changes only the
period guard from p>24 to p>25; it does not change arithmetic or search logic.
The source is never vendored or modified in a repository. P25/G8 uses 82 of
128 key bits and at most 25 of 32 array slots. This is reuse of Agent4's
implementation, not a new independently authored primary search.

Each process has explicit state, wall-time and address-space bounds. Legacy
ACCEPT stops at the first carry stream, so it is not a full acceptance census.
The very large depth argument cannot precede a <=2,000,000-state cap because
a breadth-first discovery path has at most one edge per newly seen state.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import resource
import subprocess
import tempfile
import time

COMMIT = "6e06c860bc658af484355725d26232c9fa3f285f"
SOURCE_PATH = "calculation/agent-4/fixed_g_B_probe.cpp"
BLOB = "178ef3669c78c68a1b18886afafa68f56a4c5a9f"
SHA256 = "e83add38e34cadb701395a9fd1600f601e70727187afdcd438ff6730ddaffe66"
ANCHOR = b"if(p<1||p>24)return 2;"
REPLACEMENT = b"if(p<1||p>25)return 2;"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def build(source: Path, directory: Path) -> tuple[Path, dict]:
    original = source.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(original)).encode() + b"\0" + original).hexdigest()
    require(blob == BLOB, "original Git blob differs from the reviewed source")
    require(hashlib.sha256(original).hexdigest() == SHA256, "original SHA256 differs")
    require(original.count(ANCHOR) == 1, "guard anchor is not unique")
    changed = original.replace(ANCHOR, REPLACEMENT)
    require(changed.replace(REPLACEMENT, ANCHOR) == original, "adaptation is not guard-only")
    temporary = directory / "agent4_guard25.cpp"
    temporary.write_bytes(changed)
    binary = directory / "agent4_guard25"
    subprocess.run(["c++", "-O3", "-std=c++17", str(temporary), "-o", str(binary)],
                   check=True, timeout=30)
    provenance = {"kind": "provenance", "original_author": "Agent 4",
                  "commit": COMMIT, "source_path": SOURCE_PATH,
                  "original_blob": BLOB, "original_sha256": SHA256,
                  "adapted_sha256": hashlib.sha256(changed).hexdigest(),
                  "adaptation": "exactly p>24 -> p>25 in the admission guard",
                  "target_period": 25, "target_overflow_weight": 8,
                  "target_key_bits": 82, "key_capacity_bits": 128,
                  "target_array_slots": 25, "array_capacity_slots": 32,
                  "accept_semantics": "stops at first accepted carry stream"}
    return binary, provenance


def limited_memory() -> None:
    limit = 4 * 1024 ** 3
    _, hard = resource.getrlimit(resource.RLIMIT_AS)
    if hard != resource.RLIM_INFINITY:
        limit = min(limit, hard)
    resource.setrlimit(resource.RLIMIT_AS, (limit, limit))


def run_word(binary: Path, word: str, states: int, seconds: float) -> dict:
    require(1 <= len(word) <= 25 and set(word) <= {"0", "1"}, "invalid overflow word")
    require(2 * len(word) + 4 * word.count("1") <= 127, "packed key would exceed source guard")
    before = time.monotonic()
    command = [str(binary), word, str(states), "1000000000"]
    try:
        process = subprocess.run(command, capture_output=True, text=True,
                                 timeout=seconds, preexec_fn=limited_memory)
    except subprocess.TimeoutExpired:
        return {"kind": "result", "g": word, "status": "TIMEOUT_UNDECIDED",
                "seconds": round(time.monotonic() - before, 6)}
    status = "PROCESS_ERROR_UNDECIDED"
    fields = {}
    for line in process.stdout.splitlines():
        if line.startswith("EXHAUSTED-NO-B-CYCLE ") and process.returncode == 0:
            status = "EXHAUSTED"
        elif line.startswith("ACCEPT ") and process.returncode == 0:
            status = "ACCEPT"
        elif line.startswith("CAPPED "):
            status = "STATE_CAP_UNDECIDED"
        elif line.startswith("DEPTH-CAPPED-UNDECIDED "):
            status = "DEPTH_CAP_UNDECIDED"
        else:
            continue
        fields = dict(re.findall(r"(\w+)=(\S+)", line))
        require(fields.get("g") == word, "reported overflow word differs")
    for key in ("depth", "states"):
        if key in fields:
            fields[key] = int(fields[key])
    return {"kind": "result", "g": word, "status": status,
            "returncode": process.returncode, "seconds": round(time.monotonic() - before, 6),
            **{key: value for key, value in fields.items() if key != "g"}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--words", type=Path)
    parser.add_argument("--states", type=int, default=2000000)
    parser.add_argument("--seconds", type=float, default=5)
    parser.add_argument("--batch-seconds", type=float, default=900)
    args = parser.parse_args()
    require(1 <= args.states <= 2000000, "state budget must be 1..2000000")
    require(0 < args.seconds <= 5 and 0 < args.batch_seconds <= 900, "invalid time budgets")
    words = []
    if args.words:
        words = [line.strip() for line in args.words.read_text().splitlines() if line.strip()]
        require(len(words) == len(set(words)), "input overflow words are not distinct")
        require(all(len(word) == 25 and word.count("1") == 8 and set(word) <= {"0", "1"}
                    for word in words), "batch must contain only P25/G8 words")
    with tempfile.TemporaryDirectory(prefix="agent116-agent4-replay-") as directory:
        binary, provenance = build(args.source, Path(directory))
        print(json.dumps(provenance, sort_keys=True), flush=True)
        for word, permitted in [("11100010000", {"10100110011"}),
                                ("100010001000", {"101010010101", "010110101001", "100101011010"})]:
            control = run_word(binary, word, 2000000, 5)
            require(control["status"] == "ACCEPT" and control.get("e") in permitted,
                    "known positive control failed")
            control["kind"] = "positive_control"
            print(json.dumps(control, sort_keys=True), flush=True)
        begin = time.monotonic()
        counts = {}
        for word in words:
            remaining = args.batch_seconds - (time.monotonic() - begin)
            if remaining <= 0:
                result = {"kind": "result", "g": word, "status": "UNPROCESSED_UNDECIDED"}
            else:
                result = run_word(binary, word, args.states, min(args.seconds, remaining))
            counts[result["status"]] = counts.get(result["status"], 0) + 1
            print(json.dumps(result, sort_keys=True), flush=True)
        print(json.dumps({"kind": "summary", "words": len(words), "status_counts": counts,
                          "batch_seconds": round(time.monotonic() - begin, 6)}, sort_keys=True))


if __name__ == "__main__":
    main()
