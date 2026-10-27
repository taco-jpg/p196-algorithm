#!/usr/bin/env python3
"""Guarded decimal P25/G8 exterior census using the audited tuple engine.

Complete fixed-weight coverage is regenerated before every batch. Caps,
timeouts and unprocessed words remain UNDECIDED. Any exterior acceptance
is independently replayed; a matching center and Lean check remain separate.
Runtime dependency: the source files in Agent116's PR375.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

import fixed_weight_coverage
from p20_independent import call_solver, positive_controls, replay_witness, require

HERE = Path(__file__).resolve().parent
TUPLE_SHA256 = "98f1e1afa74f7bbe085b003719644252012d3d400fa2e52a319443204f8652d9"


def period25_control(binary):
    g = "10000" * 5
    command = [str(binary), "16", g, "--states", "1000000", "--seconds", "30",
               "--memory-mib", "4096", "--prefix-width", "2", "--witness"]
    process = subprocess.run(command, capture_output=True, text=True,
                             check=True, timeout=35)
    result = json.loads(process.stdout)
    require(result["period"] == 25 and result["g"] == g and
            result["status"] in ("BOUNDED_WIDTH_ONLY", "EXHAUSTED"),
            "P25 control was incomplete or malformed")
    hit = next((hit for hit in result["accepts"] if hit["e"] == g), None)
    require(hit is not None and hit["width"] == 2, "P25 positive stream missing")
    return replay_witness(16, g, hit)


def run(binary, args):
    started = time.monotonic()
    source_hash = hashlib.sha256((HERE / "exterior_tuple.cpp").read_bytes()).hexdigest()
    require(source_hash == TUPLE_SHA256, "tuple source changed; repeat the audit first")
    controls = positive_controls(binary, args.states, max(30, args.seconds))
    long_control = period25_control(binary)
    coverage, _, payload = fixed_weight_coverage.census(
        25, 8, 1000000, time.monotonic() + 60)
    words = payload.splitlines()
    require(len(words) == coverage["surviving_necklaces"], "incomplete coverage payload")
    selected = words
    if args.only:
        require(args.only in words, "the selected g is outside the covered scope")
        selected = [args.only]
    deadline = time.monotonic() + args.batch_seconds
    records = []
    for number, g in enumerate(selected, 1):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            record = {"base": 10, "g": g, "status": "NOT_RUN_UNDECIDED",
                      "complete": False, "accepts": []}
        else:
            record = call_solver(binary, 10, g, args.states,
                                 min(args.seconds, remaining), witness=True)
            if record["accepts"]:
                record["independent_witness_replay"] = [
                    replay_witness(10, g, hit) for hit in record["accepts"]]
                print(json.dumps({"B_ONLY_ACCEPT": g,
                                  "carry_streams": [hit["e"] for hit in record["accepts"]],
                                  "complete": record["complete"]}), flush=True)
        records.append(record)
        if args.progress and number % 30 == 0:
            print(json.dumps({"processed": number, "selected": len(selected),
                              "terminal_counts": dict(Counter(r["status"] for r in records))}),
                  flush=True)
    complete_scope = len(selected) == len(words)
    finished = all(record["complete"] for record in records)
    accepted = any(record["accepts"] for record in records)
    negative = complete_scope and finished and not accepted
    counts = Counter(record["status"] for record in records)
    reached = [record for record in records if "states" in record]
    largest = max(reached, key=lambda r: r["states"]) if reached else None
    verdict = ("COMPUTED_P25_G8_EXTERIOR_NEGATIVE" if negative else
               "B_ONLY_ACCEPTED" if accepted else "UNDECIDED_PARTIAL_SCOPE")
    result = {"status": verdict, "period": 25, "overflow_weight": 8,
              "scope": "Base10 P25/G8 exterior returns only; no C/Lean/decimal theorem.",
              "tuple_source_sha256": source_hash, "coverage": coverage,
              "complete_requested_necklace_scope": complete_scope,
              "selected_words": len(selected), "terminal_counts": dict(counts),
              "positive_control_count": len(controls),
              "positive_streams_replayed": sum(len(c["witnesses"]) for c in controls),
              "positive_edges_replayed": sum(w["edges"] for c in controls for w in c["witnesses"]),
              "period25_positive_control": long_control,
              "total_state_records": sum(r["states"] for r in reached),
              "max_graph": None if largest is None else {
                  k: largest[k] for k in ("g", "states", "max_depth", "peak_rss_mib")},
              "max_peak_rss_mib": max((r["peak_rss_mib"] for r in reached), default=0),
              "unresolved": [r["g"] for r in records if not r["complete"]],
              "accepted_g": [r["g"] for r in records if r["accepts"]],
              "elapsed_seconds": round(time.monotonic() - started, 6),
              "records": records}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "records"}, sort_keys=True),
          flush=True)
    return 0 if negative or accepted else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path)
    parser.add_argument("--states", type=int, default=2000000)
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--batch-seconds", type=float, default=1100)
    parser.add_argument("--only", help="one covered lexicographically least g word")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not (1 <= args.states <= 20000000 and 0 < args.seconds <= 1190 and
            0 < args.batch_seconds <= 1500):
        parser.error("invalid time/state budget")
    if args.binary:
        raise SystemExit(run(args.binary.resolve(), args))
    with tempfile.TemporaryDirectory(prefix="agent116-p25-") as directory:
        binary = Path(directory) / "exterior_tuple"
        subprocess.run(["c++", "-O3", "-std=c++17", "-Wall", "-Wextra", "-pedantic",
                        str(HERE / "exterior_tuple.cpp"), "-o", str(binary)],
                       check=True, timeout=90)
        raise SystemExit(run(binary, args))


if __name__ == "__main__":
    main()
