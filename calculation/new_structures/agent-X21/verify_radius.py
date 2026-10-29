#!/usr/bin/env python3
"""Compare the complete folded-digit radius trace with its independent GMP summary."""
import csv
import pathlib
import sys

seed = sys.argv[1]
expected = {
    "196": (8296, 21, 12877, 21, 8),
    "879": (8245, 22, 6353, 22, 5),
    "1997": (8282, 21, 3100, 21, 10),
}[seed]
raw = list(csv.DictReader(open(sys.argv[2], encoding="utf-8")))
assert len(raw) == 20_001
h = [int(x["hamming"]) for x in raw]
n = [int(x["n"]) for x in raw]
ex = [int(x["dist_exp"]) for x in raw]
deficits = [int(x["deficit"]) for x in raw]
assert n[0] == len(seed) and n[-1] == expected[0]
assert all(x > 0 for x in h)
assert min(h) == 1
assert max(deficits) == expected[1] and deficits.index(expected[1]) == expected[2]
stride = 128
half_growth = [n[t+stride] // 2 - n[t] // 2 for t in range(len(n)-stride)]
exp_growth = [ex[t+stride] - ex[t] for t in range(len(n)-stride)]
assert min(half_growth) == expected[3]
assert min(exp_growth) == expected[4]
assert all(x > 0 for x in exp_growth)
assert all(x["macro_drop"] == "0" for x in raw)
assert all(int(x["deficit"]) == int(x["n"]) // 2-int(x["dist_exp"]) for x in raw)
output = pathlib.Path(sys.argv[3])
with output.open("w",encoding="utf-8") as out:
    out.write("t\tdigits\thamming\tdist_decimal_exponent\tdeficit\tdist_first9\n")
    for i in sorted(set(range(0, 20001, 500)) | {expected[2], max(range(len(exp_growth)),key=lambda t: -exp_growth[t])}):
        x=raw[i]
        out.write("\t".join([x["t"],x["n"],x["hamming"],x["dist_exp"],x["deficit"],x["dist_mantissa"]])+"\n")
print(f"FOLDED-DECIMAL PASS seed={seed}: 20001 states, no palindrome, max deficit {expected[1]} at t={expected[2]};")
print(f"every 128-step distance STRICTLY increases, min half-length gain {expected[3]}, min distance exponent gain {expected[4]}.")