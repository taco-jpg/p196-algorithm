#!/usr/bin/env python3
"""Agent 4 T2 p23 seven overflows: complete candidate-B census (not Lean)."""
from collections import Counter
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
words = subprocess.check_output(
    [str(HERE / "low_digit_automaton"), "--emit", "23"], text=True
).splitlines()
words = [w for w in words if w.count("1") == 7]
assert len(words) == 64, len(words)
results = []
for w in words:
    try:
        job = subprocess.run(
            [str(HERE / "fixed_g_B_probe"), w, "2000000", "100"],
            capture_output=True, text=True, timeout=7,
        )
    except subprocess.TimeoutExpired:
        results.append((w, "TIMEOUT-UNDECIDED", 0, 0))
        continue
    line = job.stdout.strip().splitlines()[-1] if job.stdout.strip() else "ERROR"
    status = line.split()[0]
    m = re.search(r"depth=(\d+) states=(\d+)", line)
    depth, states = (int(m[1]), int(m[2])) if m else (0, 0)
    results.append((w, status, depth, states))
print("candidate_necklaces=64", flush=True)
print("status_counts=", dict(Counter(z[1] for z in results)), flush=True)
print("max_states_word=", max((r[3], r[0], r[2]) for r in results), flush=True)
for w, status, depth, states in results:
    if status != "EXHAUSTED-NO-B-CYCLE":
        print("UNDECIDED", w, status, depth, states)
if any(z[1] != "EXHAUSTED-NO-B-CYCLE" for z in results):
    sys.exit(1)
print("COMPUTED p23 weight7: all 64 full-B searches exhausted")
