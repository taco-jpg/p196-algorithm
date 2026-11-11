#!/usr/bin/env python3
"""r12g2 decay.py -- decay of the exact forward sets |A_n| (kfwd logs, n >= 8 where sizes are exact):
least-squares slope of log|A_n| per step and per frame shift (4 steps), and the lifetime."""
import re, glob, math, os, sys
R = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
print('| run | K | |A_0| | |A_8| | lifetime | decay factor per 4 steps (fit n=8..L-4) | log|A_8| / log(factor^(1/4)) + 8 |')
print('|---|---|---|---|---|---|---|')
for fn in sorted(glob.glob(os.path.join(R, 'logs/fwd/*.log')) + glob.glob(os.path.join(R, 'logs/fwd2/rec*.log'))):
    s = open(fn).read()
    h = re.search(r'K=(\d+) k=(\d+)', s); a0 = re.search(r'A_0: .* = (\d+)', s)
    sz = {int(m.group(1)): int(m.group(2)) for m in re.finditer(r'^STEP (\d+) size (\d+)\s', s, re.M)}
    lt = re.search(r'max lifetime from phi0 = (\d+)', s)
    if not h or not lt or 8 not in sz: continue
    L = int(lt.group(1)); pts = [(n, math.log(v)) for n, v in sz.items() if 8 <= n <= L - 4 and v > 0]
    if len(pts) < 3: continue
    mx = sum(p[0] for p in pts) / len(pts); my = sum(p[1] for p in pts) / len(pts)
    slope = sum((p[0] - mx) * (p[1] - my) for p in pts) / sum((p[0] - mx) ** 2 for p in pts)
    f4 = math.exp(-4 * slope)
    pred = math.log(sz[8]) / (-slope) + 8
    print(f'| {os.path.basename(fn)[:-4]} | {h.group(1)} | {int(a0.group(1)):,} | {sz[8]:,} | {L} | {f4:.2f} | {pred:.0f} |')
