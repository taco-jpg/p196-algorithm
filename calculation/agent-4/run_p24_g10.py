#!/usr/bin/env python3
"""Agent 4 T2 p24/weight10: explicitly incomplete full-width B census.

All finite EXHAUSTED results are negative; caps/timeouts are UNDECIDED.
Run this script after building low_digit_automaton and fixed_g_B_probe.
The two still-unresolved words need isolated larger-cap reruns.
"""
from collections import Counter
from pathlib import Path
import subprocess
import re
import sys
import time

home = Path(__file__).resolve().parent
words = subprocess.check_output(
    [str(home / "low_digit_automaton"), "--emit", "24"], text=True
).splitlines()
words = [w for w in words if w.count("1") == 10]
assert len(words) == 685, len(words)
results = []
start = time.monotonic()
for i, word in enumerate(words):
    if time.monotonic() - start > 75:
        results.extend((w, "NOT_RUN", 0, 0) for w in words[i:])
        break
    try:
        p = subprocess.run(
            [str(home / "fixed_g_B_probe"), word, "2000000", "100"],
            capture_output=True, text=True, timeout=5,
        )
    except subprocess.TimeoutExpired:
        results.append((word, "TIMEOUT", 0, 0))
        continue
    line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "ERROR"
    status = line.split()[0]
    if p.returncode not in (0, 3):
        status = "ERROR_EXIT_" + str(p.returncode)
    match = re.search(r"depth=(\d+) states=(\d+)", line)
    depth, states = (int(match[1]), int(match[2])) if match else (0, 0)
    results.append((word, status, depth, states))
    if status == "ACCEPT":
        print("B_CYCLE_CANDIDATE", word, line, flush=True)
    if (i + 1) % 150 == 0:
        print("PROGRESS", i + 1,
              Counter(s for _, s, _, _ in results), flush=True)
print("p24_weight10_necklaces=", 81752)
print("necessary_survivors=", len(words))
print("statuses=", dict(Counter(s for _, s, _, _ in results)))
print("largest=", max((n, w, d) for w, _, d, n in results))
print("elapsed=", round(time.monotonic() - start, 2))
for word, status, depth, states in results:
    if status != "EXHAUSTED-NO-B-CYCLE":
        print("UNDECIDED_OR_ACCEPT", word, status, depth, states)
if any(s != "EXHAUSTED-NO-B-CYCLE" for _, s, _, _ in results):
    sys.exit(1)
print("P24_WEIGHT10_COMPUTED_NEGATIVE_COMPLETE")
