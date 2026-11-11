#!/usr/bin/env python3
"""r12e: summary of the khxt Task A / family runs: final verdict line, last level with a TOP line, TOP99/TOPUU hits (first level,
exact sizes of the closed parts), kept-set range.  usage: taskA_sum.py ERRFILE [ERRFILE ...]   (the .out file next to it is read too)"""
import sys, re, os
for fe in sys.argv[1:]:
    fo = fe[:-4] + '.out'
    final = open(fo).read().strip().splitlines() if os.path.exists(fo) else []
    finals = [l for l in final if l.startswith('KHXT ')]
    lastK = None; hits99 = []; hitsUU = []; kept = []
    for l in open(fe):
        m = re.match(r'\s+TOP K=(\d+) kept=(\d+) n99=(\d+) c99=(\d) k99=(\d+) nUU=(\d+) cUU=(\d) kUU=(\d+)', l)
        if m:
            K, kp, n99, c99, k99, nUU, cUU, kUU = map(int, m.groups()); lastK = K; kept.append(kp)
            if c99: hits99.append((K, k99))
            if cUU: hitsUU.append((K, kUU))
    name = os.path.basename(fe)[:-4]
    print(f"{name}: last TOP level K={lastK}; kept range {min(kept) if kept else None}..{max(kept) if kept else None}")
    print(f"   TOP99 hits: {len(hits99)}" + (f" (first K={hits99[0][0]}, closed-part sizes {sorted(set(k for _, k in hits99))})" if hits99 else ""))
    print(f"   TOPUU hits: {len(hitsUU)}" + (f" (first K={hitsUU[0][0]}, sizes {sorted(set(k for _, k in hitsUU))})" if hitsUU else ""))
    for l in finals: print("   " + l)
