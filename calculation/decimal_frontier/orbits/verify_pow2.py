#!/usr/bin/env python3
"""verify_pow2.py BASE... -- natural seed 1 0 (b-1)^k (b-2) in power-of-2 bases beyond the Lean-proven ones: entry step, mirror cycle, cycleOK, integer replay >=3 cycles."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census, rar, nbs, certseed
def num(ds, b):
    v = 0
    for x in ds: v = v * b + x
    return v
out = json.load(open('data/pow2_beyond32.json')) if os.path.exists('data/pow2_beyond32.json') else {}
for b in map(int, sys.argv[1:]):
    for k in (2, 3):
        ds = [1, 0] + [b - 1] * k + [b - 2]; s = num(ds, b); dg = rar.to_digits(s, b)
        T = 1200
        r = census.run_seed(b, dg, T)
        if r[0] != 'regular': print(b, k, r[0], r[1]); continue
        e, cyc = census.entry_dense(b, dg, T)
        # rebuild edges
        tp = census.tpl_at(rar.pairword(rar.revadd_n(dg, b, T)) if hasattr(rar, 'revadd_n') else None, b) if False else None
        # recompute template at T
        d = dg.copy()
        for t in range(T): d, _, _ = rar.revadd(d, b)
        P = rar.pairword(d); tp = census.tpl_at(P, b)
        rr = nbs.run(b, tp[0], tp[1], maxsteps=3000, maxlen=500)
        es = rr[1]; ok = bool(nbs.cycleOK(b, es, es[0][0], es[0][1])); cert = bool(nbs.is_cert(b, es))
        p = len(es)
        res = {'base': b, 'k': k, 'seed_digits_msb': ds, 'seed_int': s, 'entry': e, 'cycle_len': p, 'sumgam': sum(nbs.gam(b, x[0], x[1]) for x in es),
               'gain': sum(x[4] + x[5] for x in es), 'cycleOK': ok, 'is_cert': cert, 'B_sizes': [len(x[0]) for x in es], 'C_sizes': [len(x[1]) for x in es]}
        # integer replay of the template value for >=3 cycles from several g0
        rep = []
        for g0 in (4, 6, 40):
            okr, pal, bad, gfin = certseed.replay(b, es, g0, 6 * p + 5)
            rep.append({'g0': g0, 'steps': 6 * p + 5, 'pairword_equals_template_every_step': okr, 'palindrome_at': pal, 'first_bad': bad, 'final_g': gfin})
        res['replay'] = rep
        res['edges'] = [[x[0], x[1], x[2], x[3], x[4], x[5]] for x in es]
        out[f'{b}_{k}'] = res
        print(b, k, 'entry', e, 'p', p, 'cycleOK', ok, 'cert', cert, 'sumgam', res['sumgam'], 'gain', res['gain'], 'B', res['B_sizes'][:3], 'C', res['C_sizes'][:3], 'replay', [(r_['g0'], r_['pairword_equals_template_every_step'], r_['palindrome_at']) for r_ in rep], flush=True)
        json.dump(out, open('data/pow2_beyond32.json', 'w'))
