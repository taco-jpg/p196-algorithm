#!/usr/bin/env python3
"""T2 period22: 998 B negatives, one repeated p11 B return, one unresolved g10.

Exact full-width B positional graph; NEVER turn CAPPED/TIMEOUT into a negative.
Depends on corrected source executables in parent Agent 4 PR #323.
"""
from collections import Counter
from pathlib import Path
import subprocess, re, time, sys

here = Path(__file__).resolve().parent
probe = here / "fixed_g_B_probe"
words = subprocess.check_output(
    [str(here / "low_digit_automaton"), "--emit", "22"], text=True
).splitlines()
expected_weights = {6: 4, 7: 107, 8: 445, 9: 392, 10: 51, 11: 1}
assert dict(Counter(w.count("1") for w in words)) == expected_weights
old_g = "11100010000" * 2
hard_g = "1001011100010010111000"
assert old_g in words and hard_g in words
results = []
details = {}
start = time.monotonic()

for i, w in enumerate(words):
    if time.monotonic() - start > 370:
        results.extend((z, "NOT_RUN", 0, 0) for z in words[i:])
        break
    hard_case = w == hard_g
    old_case = w == old_g
    cap = "40000000" if hard_case else ("10000000" if old_case else "2000000")
    limit = 250 if hard_case else (90 if old_case else 5)
    try:
        job = subprocess.run(
            [str(probe), w, cap, "140"],
            capture_output=True, text=True, timeout=limit,
        )
    except subprocess.TimeoutExpired:
        results.append((w, "TIMEOUT_UNDECIDED", 0, 0))
        continue
    line = job.stdout.strip().splitlines()[-1] if job.stdout.strip() else "ERROR"
    status = line.split()[0]
    if job.returncode not in (0, 3):
        status = "ERROR_EXIT_" + str(job.returncode)
    match = re.search(r"depth=(\d+) states=(\d+)", line)
    depth, states = (int(match[1]), int(match[2])) if match else (0, 0)
    results.append((w, status, depth, states))
    details[w] = line
    if (i + 1) % 200 == 0:
        print("PROGRESS", i + 1, Counter(z[1] for z in results), flush=True)

print("period22_all_necklaces=", 190746)
print("necessary_survivors=", len(words),
      "by_weight=", dict(sorted(expected_weights.items())))
print("status_counts=", dict(sorted(Counter(z[1] for z in results).items())))
print("max_states_word=", max((n, w, d) for w, _, d, n in results))
print("elapsed=", round(time.monotonic() - start, 2))
for w, status, depth, states in results:
    if status != "EXHAUSTED-NO-B-CYCLE":
        print("NONNEGATIVE_STATUS", w, status, depth, states, details.get(w, ""))

# Independently replay the only accepted stream: this is NOT a new B period.
B0 = [18, 14, 0, 2, 10, 10, 6, 0, 7, 8, 18, 9, 1, 5, 9,
      6, 4, 3, 12, 10, 10, 12, 13, 10, 13]
def norm(word, c):
    out = []
    for z in word:
        z += c
        out.append(z % 10)
        c = z // 10
    return out, c

B = B0[:]
es, gs = [], []
for i in range(22):
    db, e = norm(B, 0)
    dr, g = norm(B[::-1], 1 - e)
    raw = ([x + y for x, y in zip(db + [9 * (1 - e)], [1] + dr[::-1])]
           if g else [x + y for x, y in zip(db, dr[::-1])])
    while raw and raw[-1] == 9:
        raw.pop()
    B = raw
    es.append(str(e))
    gs.append(str(g))
    if i == 10:
        assert B == B0
assert B == B0
assert "".join(gs) == "11100010000" * 2
assert "".join(es) == "10100110011" * 2
print("KNOWN_P11_B_REPLAY_AT_11_AND_22=", True)

# The prior 11-cycle repetition MUST be recognized as ACCEPT, never 'negative'.
old_record = next((z for z in results if z[0] == old_g), None)
assert old_record is not None and old_record[1] == "ACCEPT", old_record
assert (" e=" + "10100110011" * 2) in details[old_g]

# A full p22 negative is NOT available while hard_g is capped.
allowed = all(
    status == "EXHAUSTED-NO-B-CYCLE"
    or (w == old_g and status == "ACCEPT")
    or (w == hard_g and status in ("CAPPED", "TIMEOUT_UNDECIDED"))
    for w, status, _, _ in results
)
print("SCOPED_PARTIAL_CLASSIFICATION_VALID=", allowed)
if not allowed:
    sys.exit(1)
print("FULL_P22_NO_B_IS_NOT_CLAIMED")
