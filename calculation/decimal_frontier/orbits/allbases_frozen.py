#!/usr/bin/env python3
"""allbases_frozen.py OUT.json T NRAND base1 ... -- for natural candidates (first 3) + NRAND random survivors per base: windows of the extended panel;
summarise bottom-frame / centre-frame temporal-periodic prefix lengths (Fb, Fc), longest neutral run, template g, per base."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rar, orbit2, base10_stats
out = sys.argv[1]; T = int(sys.argv[2]); NR = int(sys.argv[3]); bases = [int(x) for x in sys.argv[4:]]
cands = json.load(open('data/candidates_unique.json'))
res = {}
for b in bases:
    t0 = time.time()
    seeds = [('c%d' % n, rar.to_digits(n, b)) for n in cands.get(str(b), [])[:3]]
    rs, _ = base10_stats.rand_survivors(b, NR, seed=1300 + b, lo=6, hi=30)
    seeds += [('r%02d' % i, dg) for i, dg in enumerate(rs)]
    Fb = []; Fc = []; r9 = []; gl = []; nn = []; gam = []
    for name, dg in seeds:
        recs, summ = orbit2.scan2(b, dg, T, W=3, tmax=120, lrs=False)
        gam.append(summ['gam_density'])
        for r in recs:
            if r['n'] >= 300:
                Fb.append(r['Fb']); Fc.append(r['Fc']); r9.append(r['r9_max']); gl.append(r['tpl_g']); nn.append(r['n'])
    Fb = np.array(Fb); Fc = np.array(Fc); r9 = np.array(r9); nn = np.array(nn); gl = np.array(gl)
    res[b] = {'nwin': len(Fb), 'Fb_mean': float(Fb.mean()), 'Fb_q99': float(np.quantile(Fb, .99)), 'Fb_max': int(Fb.max()),
              'Fc_mean': float(Fc.mean()), 'Fc_q99': float(np.quantile(Fc, .99)), 'Fc_max': int(Fc.max()),
              'r9_mean': float(r9.mean()), 'r9_max': int(r9.max()), 'tplg_max': int(gl.max()), 'gam_density': float(np.mean(gam)),
              'frac_g_ge_n4': float(np.mean(gl >= nn / 4)), 'secs': round(time.time() - t0, 1)}
    print(b, json.dumps(res[b]), flush=True)
    json.dump(res, open(out, 'w'))
