#!/usr/bin/env python3
"""r12e: analyse a khxt -coreproj file: ANC lines (k, |kept_k|, #ancestors of the final kept set at level k) and the ancestor
windows at level K-D.  Reports the ancestor profile, per-phase branch positions of the ancestor prefix tree, and for every ancestor
window the smallest position-period q (1..60) of its digits on [lo, k) if any (eventually periodic tail test).
usage: core_stats.py FILE [lo]"""
import sys, collections
fn = sys.argv[1]; lo = int(sys.argv[2]) if len(sys.argv) > 2 else None
anc = []; nodes = []
for l in open(fn):
    if l.startswith('ANC'):
        _, k, n, a = l.split(); anc.append((int(k), int(n), int(a)))
    elif l.startswith('#'):
        continue
    elif ':' in l:
        h, xs = l.split(':'); hh = h.split()
        nodes.append((int(hh[1]), int(hh[2]), int(hh[3]), int(hh[0]), [int(v) for v in xs.split()]))
K = anc[-1][0]
print(f"final K={K}; ancestor profile (k: kept_k / ancestors_k):")
step = max(1, K // 40)
print('  ' + '  '.join(f"{k}:{n}/{a}" for k, n, a in anc if k % step == 0 or k == K))
if not nodes: sys.exit()
kd = len(nodes[0][4]); P = max(t for t, *_ in nodes) + 1
print(f"ancestor windows at level {kd}: {len(nodes)} nodes, {P} phases")
byt = collections.defaultdict(list)
for t, o0, o1, idx, x in nodes: byt[t].append(x)
print("nodes per phase:", [len(byt[t]) for t in range(P)])
# branch positions of the prefix tree, phase 0..2
for t in range(min(4, P)):
    xs = sorted(byt[t]); bp = collections.Counter()
    for a, b2 in zip(xs, xs[1:]):
        d = next((i for i in range(kd) if a[i] != b2[i]), kd); bp[d] += 1
    print(f"phase {t}: branch positions (first difference between neighbours in sorted order): {sorted(bp.items())[:40]}")
# eventual periodicity of each window on [lo, kd)
if lo is None: lo = kd // 2
per = collections.Counter(); ex = {}
for t, o0, o1, idx, x in nodes:
    q0 = None
    for q in range(1, 61):
        if all(x[i] == x[i + q] for i in range(lo, kd - q)): q0 = q; break
    per[q0] += 1
    if q0 not in ex: ex[q0] = (t, x[-3 * (q0 or 10):])
print(f"position-period of the window digits on [{lo},{kd}) (None = no period <= 60):", sorted(per.items(), key=lambda z: (z[0] is None, z[0] or 0)))
for q, (t, tail) in sorted(ex.items(), key=lambda z: (z[0] is None, z[0] or 0)):
    print(f"  example q={q} phase {t}: tail {' '.join(map(str, tail))}")
# top digits of ancestors
print("top-digit histogram of ancestors:", sorted(collections.Counter(x[-1] for *_, x in nodes).items()))
