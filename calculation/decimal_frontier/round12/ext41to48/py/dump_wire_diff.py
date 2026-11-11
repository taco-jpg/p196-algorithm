#!/usr/bin/env python3
"""r12b: analyse a khx dump against a known wire stream (B_t list from `bx -w -nosym`, clock word = khx pattern).
For every kept node (phase t, window x_0..x_{K-1}) compute the first position where x differs from pad(B_{t}) .
usage: dump_wire_diff.py DUMP WITFILE   (WITFILE: the WIT line of bx -w -nosym for the PATTERN word, phase 0 = B_0)"""
import sys, re, collections
dump, wit = sys.argv[1], sys.argv[2]
line = [l for l in open(wit) if l.startswith("WIT")][0]
Bs = [[int(v) for v in grp.split(",")] for grp in re.findall(r"\[([0-9,]+)\]", line)]
P = len(Bs)
hist = collections.Counter(); K = None; n = 0; byphase = collections.Counter()
for l in open(dump):
    if l.startswith("#"):
        m = re.search(r"K=(\d+)", l)
        if m: K = int(m.group(1))
        continue
    head, xs = l.split(":")
    t = int(head.split()[1]); x = [int(v) for v in xs.split()]
    B = Bs[t % P] + [9] * (len(x) - len(Bs[t % P]))
    d = next((i for i in range(len(x)) if x[i] != B[i]), None)
    hist[d if d is not None else "same"] += 1; n += 1
print("K=%d kept=%d  first-difference position histogram (None=identical to padded wire):" % (K, n))
for k in sorted(hist, key=lambda v: (-1 if v == "same" else v)):
    print("  ", k, hist[k])
