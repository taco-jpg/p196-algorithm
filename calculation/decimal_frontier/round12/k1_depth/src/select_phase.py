#!/usr/bin/env python3
"""r12g select_phase.py -- per-phase sizes of a cyclic-set file and the cheapest start phase for kfwd.
cost(phi) = |Cyc(Kb)[phi]| * |TopCyc(k)[(t,par)]|   (or * 19^k, halved-ish for odd n, without a top file)
usage: select_phase.py CYCFILE Kb M k [TOPFILE]"""
import sys
import numpy as np
fn, Kb, M, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
top = sys.argv[5] if len(sys.argv) > 5 else None
PS = 100 if Kb <= 20 else 118
a = np.fromfile(fn, dtype=np.uint64).reshape(-1, 2)
ph = (a[:, 1] >> np.uint64(PS - 64)).astype(np.int64)
u, c = np.unique(ph, return_counts=True)
tc = {}
if top:
    b = np.fromfile(top, dtype=np.uint64).reshape(-1, 2)
    tp = (b[:, 1] >> np.uint64(36)).astype(np.int64)
    tu, tcnt = np.unique(tp, return_counts=True)
    tc = dict(zip(tu.tolist(), tcnt.tolist()))
rows = []
for p, n in zip(u.tolist(), c.tolist()):
    par = p % 2; q = p // 2; j = q % M; t = q // M
    tn = tc.get(t * 2 + par, 0) if top else (19 ** k if par == 0 else 19 ** (k - 1) * 10)
    rows.append((n * tn, t, j, par, n, tn))
rows.sort()
print(f'{fn}: {len(a)} states in {len(u)} phases; per-phase min {c.min()} max {c.max()} mean {c.mean():.0f}')
for r in rows[:8]:
    print(f'  phase t={r[1]} j={r[2]} par={r[3]}: |Cyc|={r[4]} x top {r[5]} = cost {r[0]:.3e}')
print('BEST', rows[0][1], rows[0][2], rows[0][3], rows[0][0])
