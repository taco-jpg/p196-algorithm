#!/usr/bin/env python3
"""Write cen2 tables for the stacked cap S_t(s) = B2_t W48_t^s B1_t[11:] over the rec1 bulk W20 (HYBRID.md 7b, #481).
cen2 then tests T^80K(Stack(s,r,C)) == Stack(s,r+K,C) directly (exact arithmetic, no reduction to rec1).  usage: mkstack.py s..."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation"))
from klib import load_rec
r1, r2 = load_rec(1), load_rec(2); p = 8
for s in map(int, sys.argv[1:]):
    S = [r2.B[t] + r2.W[t]*s + r1.B[t][11:] for t in range(p)]
    with open(f"stk{s}.tbl", "w") as f:
        f.write(f"{p} {len(S[0])} {len(r1.W[0])}\n" + " ".join(map(str, r1.g)) + "\n")
        for t in range(p): f.write(" ".join(map(str, S[t])) + "\n")
        for t in range(p): f.write(" ".join(map(str, r1.W[t])) + "\n")
    print(f"stk{s}.tbl |S|={len(S[0])}")
