#!/usr/bin/env python3
"""runtrack_batch.py OUT.json T L0 NRAND base1 base2 ... -- run tracker on natural candidates (first 3) + NRAND random survivors for each base."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rar, runtrack, base10_stats
out = sys.argv[1]; T = int(sys.argv[2]); L0 = int(sys.argv[3]); NR = int(sys.argv[4]); bases = [int(x) for x in sys.argv[5:]]
cands = json.load(open('data/candidates_unique.json'))
res = {}
for b in bases:
    seeds = [('c%d' % n, rar.to_digits(n, b)) for n in cands.get(str(b), [])[:3]]
    rs, _ = base10_stats.rand_survivors(b, NR, seed=900 + b)
    seeds += [('r%02d' % i, dg) for i, dg in enumerate(rs)]
    allt = []; t0 = time.time(); per = []
    for name, dg in seeds:
        tracks, pal, steps = runtrack.track(b, dg, T, L0)
        s = runtrack.summarize(b, tracks, T, L0)
        per.append({'name': name, 'steps': steps, 'pal': pal, 'summary': s})
        for tr in tracks:
            allt.append((tr['vals'][0][0] == b - 1, tr['death'] - tr['birth'] + 1, tr['len0'], tr['maxlen']))
    A = np.array(allt)
    neu = A[A[:, 0] == 1]
    summ = {'ntracks': len(A), 'neutral_n': len(neu), 'neutral_life_mean': float(neu[:, 1].mean()), 'neutral_life_max': int(neu[:, 1].max()),
            'neutral_maxlen_max': int(neu[:, 3].max()),
            'life_by_len0': {int(l): [int((neu[:, 2] == l).sum()), float(neu[neu[:, 2] == l, 1].mean()), int(neu[neu[:, 2] == l, 1].max())] for l in sorted(set(neu[:, 2].astype(int)))}}
    res[b] = {'summary': summ, 'per': per, 'secs': round(time.time() - t0, 1)}
    print(b, json.dumps(summ)[:600], res[b]['secs'], flush=True)
    json.dump(res, open(out, 'w'))
