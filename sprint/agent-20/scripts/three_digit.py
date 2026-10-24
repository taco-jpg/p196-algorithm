#!/usr/bin/env python3
"""Recompute ranks of the Lean-claimed three-digit prefix endpoints at widths k=3..7
(sprint agent 20).  Claimed values are the t-bounds of the Lean ancestry theorems
(t <= claimed); ours is min over k of (rank+1), 'inf' if every width has a cycle."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__file__))
from recompute_ranks import Ranker, initial_words, no_overflow_pre
from inverse_long import LazyPred

claims = {"217": 23, "218": 34, "777": 25, "620": 12, "739": 39}
classes = [(1,1,9,8),(2,1,3,23),(2,1,6,10),(2,5,7,16),(2,7,6,31),(2,7,7,31),(2,7,8,31),(3,4,8,16),
 (3,7,7,8),(3,8,4,7),(3,8,5,8),(4,2,6,24),(4,2,9,24),(4,7,4,7),(6,7,4,5),(7,3,7,12),(7,5,5,12),
 (7,7,8,25),(7,8,3,14),(7,8,4,14),(7,8,5,40),(7,8,6,27),(7,8,7,25),(7,8,8,14),(7,8,9,38),
 (8,5,6,38),(8,5,7,25),(8,5,8,36),(8,5,9,36),(9,0,5,11),(9,0,6,11),(9,2,3,7),(9,3,5,10)]
for a,b,c,B in classes:
    claims[f"{a}{b}{c}"] = B
kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 7
rankers = {k: Ranker(LazyPred(k)) for k in range(3, kmax + 1)}
bad = 0
for p, B in claims.items():
    pre = [int(x) for x in p]
    assert no_overflow_pre(pre)
    row = []
    for k in range(3, kmax + 1):
        r = max(rankers[k].get(w) for w in initial_words(pre, k))
        row.append(r)
    best = min(r + 1 for r in row)
    flag = "ok" if best <= B else "OUR BOUND LARGER"
    if best > B: bad += 1
    print(p, "claimed t<=", B, "ranks k=3..%d:" % kmax, row, "best t<=", best, flag, flush=True)
print("mismatches:", bad)
