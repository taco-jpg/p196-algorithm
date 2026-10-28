#!/usr/bin/env python3
"""nested_only.py OUT.json base1 ... -- nested-band lifetime law: B=[B1], C=[x,(b-1)^m,x]; best lifetime over (B1,x) as a function of m.
Uses cpp/tpl eval with large maxlen (templates may grow while alive).  Reports cycles (certificates!) if any."""
import sys, os, json, subprocess, time
import numpy as np
TPL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cpp', 'tpl')
out = sys.argv[1]; bases = [int(x) for x in sys.argv[2:]]
res = json.load(open(out)) if os.path.exists(out) else {}
ms = (8, 16, 32, 64, 128)
for b in bases:
    t0 = time.time(); inp = []; meta = []
    for m in ms:
        for B1 in range(1, 2 * b - 1):
            for x in range(0, 2 * b - 1):
                C = [x] + [b - 1] * m + [x]; inp.append(f"1 {B1} {len(C)} {' '.join(map(str, C))}"); meta.append((m, B1, x))
    o = subprocess.run([TPL, 'eval', str(b), '200000', '100000'], input='\n'.join(inp) + '\n', capture_output=True, text=True).stdout.strip().split('\n')
    best = {}; cyc = {}; other = 0
    for (m, B1, x), l in zip(meta, o):
        k, t, rea, cl, sg, gn = map(int, l.split())
        if k == 0:
            if t > best.get(m, (0,))[0]: best[m] = (t, B1, x)
        elif k == 1: cyc.setdefault(m, []).append((B1, x, t, cl, sg, gn))
        else: other += 1
    ms2 = [m for m in ms if m in best]
    slope = float(np.polyfit(ms2, [best[m][0] for m in ms2], 1)[0]) if len(ms2) >= 3 else None
    res[str(b)] = {'best': best, 'slope': slope, 'ncyc': {m: len(v) for m, v in cyc.items()}, 'cyc_example': {m: v[0] for m, v in cyc.items()}, 'other': other,
                   'ratio_m128': best[128][0] / 128 if 128 in best else None, 'secs': round(time.time() - t0, 1)}
    print(b, 'slope', None if slope is None else round(slope, 2), 'best/m', {m: round(best[m][0] / m, 2) for m in best}, 'cycles', {m: len(v) for m, v in cyc.items()}, 'other', other, flush=True)
    json.dump(res, open(out, 'w'))
