#!/usr/bin/env python3
"""Agent 4, T2: exact p23 B positional census. CAPPED/TIMEOUT never count as negatives.

Build low_digit_automaton and fixed_g_B_probe from the parent source PR.
The exceptional stream needs 10M states; all others use a 2M limit.
"""
from collections import Counter
from pathlib import Path
import re
import subprocess
import sys
import time

here = Path(__file__).resolve().parent
low = here / "low_digit_automaton"
probe = here / "fixed_g_B_probe"
words = subprocess.check_output([str(low), "--emit", "23"], text=True).splitlines()
weights = Counter(w.count("1") for w in words)
expected = {6: 1, 7: 64, 8: 463, 9: 731, 10: 239, 11: 4}
assert dict(weights) == expected, weights
hard = "10101010101001001110000"
assert words.count(hard) == 1

results = []
start = time.monotonic()
for i, w in enumerate(words):
    if time.monotonic() - start > 130:
        results.extend((z, "NOT_RUN", 0, 0) for z in words[i:])
        break
    hard_case = w == hard
    cap = "10000000" if hard_case else "2000000"
    limit = 90 if hard_case else 5
    try:
        p = subprocess.run(
            [str(probe), w, cap, "110"],
            capture_output=True, text=True, timeout=limit,
        )
    except subprocess.TimeoutExpired:
        results.append((w, "TIMEOUT-UNDECIDED", 0, 0))
        continue
    line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "ERROR"
    status = line.split()[0]
    if p.returncode not in (0, 3):
        status = "ERROR_EXIT_" + str(p.returncode)
    match = re.search(r"depth=(\d+) states=(\d+)", line)
    depth, states = (int(match[1]), int(match[2])) if match else (0, 0)
    results.append((w, status, depth, states))
    if status == "ACCEPT":
        print("B_CYCLE_CANDIDATE", w, line, flush=True)
        wit = subprocess.run(
            [str(probe), w, cap, "110", "-w"],
            capture_output=True, text=True, timeout=limit,
        )
        print(wit.stdout, flush=True)
    if (i + 1) % 300 == 0:
        print("PROGRESS", i + 1, Counter(q[1] for q in results), flush=True)

print("period=23 initial_binary_necklaces=364724")
print("necessary_survivors=", len(words),
      "weight_counts=", dict(sorted(weights.items())))
print("status_counts=", dict(sorted(Counter(z[1] for z in results).items())))
print("largest=", max((z[3], z[0], z[2]) for z in results))
print("elapsed_seconds=", round(time.monotonic() - start, 2))
for w, status, depth, states in results:
    if status != "EXHAUSTED-NO-B-CYCLE":
        print("UNRESOLVED_OR_ACCEPT", w, status, depth, states)
passed = all(z[1] == "EXHAUSTED-NO-B-CYCLE" for z in results)
print("COMPLETE_COMPUTED_P23_NO_B=", passed)
if not passed:
    sys.exit(1)
