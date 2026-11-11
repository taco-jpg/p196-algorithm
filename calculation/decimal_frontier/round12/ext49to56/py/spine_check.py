#!/usr/bin/env python3
"""r12e: spine analysis of a khxt -coreproj dump (ancestor windows at one level).  For each phase, group the windows; report the
pairwise first-difference positions, test eventual position-periodicity with periods up to QMAX on [lo, k), and test whether
one lineage is a time shift of another (window at phase t of lineage B == window at phase t+s of lineage A)."""
import sys, collections
fn = sys.argv[1]; lo = int(sys.argv[2]); QMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 300
nodes = {}
for l in open(fn):
    if l.startswith('#') or l.startswith('ANC') or ':' not in l: continue
    h, xs = l.split(':'); hh = h.split()
    nodes[int(hh[0])] = (int(hh[1]), int(hh[2]), int(hh[3]), tuple(int(v) for v in xs.split()))
k = len(next(iter(nodes.values()))[3]); P = max(v[0] for v in nodes.values()) + 1
print(f"{len(nodes)} ancestor nodes at level {k}, {P} phases")
# edges among ancestors: how many out-edges per node
oc = collections.Counter((v[1] >= 0) + (v[2] >= 0) for v in nodes.values()); print("out-degree histogram (within ancestors):", dict(oc))
# periodicity with large q
per = collections.Counter()
for i, (t, o0, o1, x) in nodes.items():
    q0 = None
    for q in range(1, QMAX + 1):
        if lo + q >= k: break
        if all(x[j] == x[j + q] for j in range(lo, k - q)): q0 = q; break
    per[q0] += 1
print(f"position periods on [{lo},{k}) up to {QMAX}:", dict(per))
# digit statistics of the upper part: fraction of 9s, value histogram
vals = collections.Counter(d for (t, o0, o1, x) in nodes.values() for d in x[lo:])
print("digit histogram on [lo,k):", sorted(vals.items()))
# time-shift relation between lineages: build per phase the sorted list of windows truncated to the common core depth kc
