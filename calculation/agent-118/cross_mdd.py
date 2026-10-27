#!/usr/bin/env python3
"""Cross-reproduce Agent 111's P33 result and Agent 116's base20 positive.

This uses Agent 118's required-current-coefficient image from PR369, distinct
from Agent 111's delayed-output image. It is corroboration, not new discovery.
"""
import argparse
import json
from pathlib import Path
import resource
import subprocess
import sys

from check_center import parse_witness


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def limits():
    memory = 4 * 1024**3
    resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    args = parser.parse_args()
    binary = str(args.binary.resolve())
    command = [sys.executable, str(Path(__file__).with_name("run_mdd.py")), binary,
               "--e", "10100110011" * 3, "--g", "11100010000" * 3,
               "--v", "01000010000" * 3, "--ops", "200000000", "--seconds", "120"]
    run = subprocess.run(command, capture_output=True, text=True, timeout=130)
    require(run.returncode == 0, "P33 run incomplete: " + run.stdout + run.stderr)
    result = json.loads(run.stdout)
    require(result["status"] == "NONE", "P33 result differs from Agent111")
    expected = {"jstar": "5", "period": "1", "mlo": "67", "classes": "2",
                "hits": "0", "tails": "12", "scope": "allm"}
    require(all(result["done"].get(k) == v for k, v in expected.items()),
            "P33 complete-tail metadata mismatch")
    counts = [int(dict(item.split("=", 1) for item in line.split()[1:])["tuples"])
              for line in result["stdout"].splitlines() if line.startswith("MDD_LAYER ")]
    require(counts == [42875, 657443, 34755075, 414911363, 752450435, 752450435],
            "P33 exact frontier counts differ from Agent111")
    print(json.dumps({"check": "agent111_P33_corroboration", "status": "PASS",
                      "frontiers": counts, "done": result["done"],
                      "wall_seconds": result["wall_seconds"],
                      "peak_child_rss_kib": result["peak_child_rss_kib"]}, sort_keys=True))

    command = [binary, "20", "10100101", "10001000", "27", "27",
               "-v", "00100000", "-w", "--compare", "-ops", "20000000",
               "-cap", "1000000"]
    run = subprocess.run(command, capture_output=True, text=True, timeout=30,
                         preexec_fn=limits)
    require(run.returncode == 0, "base20 control incomplete: " + run.stdout + run.stderr)
    hits = [line for line in run.stdout.splitlines() if line.startswith("FEASIBLE ")]
    done = [line for line in run.stdout.splitlines() if line.startswith("MDD_DONE ")]
    require(len(hits) == len(done) == 1, "base20 completion/witness missing")
    require(parse_witness(hits[0]) == (20, 8, 27), "base20 independent replay mismatch")
    fields = dict(item.split("=", 1) for item in done[0].split()[1:])
    require(fields.get("status") == "hit" and fields.get("comparisons") == "14",
            "base20 complete explicit-frontier comparisons missing")
    print(json.dumps({"check": "credited_agent116_base20_positive", "status": "PASS",
                      "witness_edges_replayed": 8, "exact_frontier_comparisons": 14,
                      "done": fields}, sort_keys=True))


if __name__ == "__main__":
    main()
