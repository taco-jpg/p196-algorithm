#!/usr/bin/env python3
"""census.py BASE_LO BASE_HI NSEEDS T [minlen maxlen] -- random seed census of regularization.
For every base: NSEEDS random seeds (uniform digits, length minlen..maxlen), orbit of T steps.
A seed is 'dead' if a palindrome is hit, 'regular' if at T/2 and T the pair word has a single-band template with |B|+|C|<=150,
g >= 0.25*n, and g(T) > g(T/2); the regular ones are re-run densely to find the entry step (last step at which the observed
template stopped following the mirror prediction, +1) and the canonical mirror cycle (cycle length, sum gam, gain, cert?)."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rar, nbs

def tpl_at(P, b, imax=150):
    bs = [x for x in rar.bands(P, b, ming=1) if x[0] <= imax]
    if not bs: return None
    i, g, L = max(bs, key=lambda t: (t[1], -t[0])); n = len(P)
    return (P[:i].tolist(), P[i + g:n - i - g].tolist(), g, i)

def run_seed(b, dig, T):
    d = dig.copy(); chk = {T // 2: None, T: None}
    for t in range(T + 1):
        if rar.is_pal(d): return ('dead', t, None)
        P = rar.pairword(d)
        if t in chk:
            tp = tpl_at(P, b); chk[t] = (tp, len(d))
        d, _, c = rar.revadd(d, b)
    (t1, n1), (t2, n2) = chk[T // 2], chk[T]
    if t1 and t2 and len(t2[0]) + len(t2[1]) <= 150 and t2[2] >= 0.25 * n2 and t2[2] > t1[2]:
        return ('regular', T, (t2[0], t2[1]))
    return ('other', T, (t2[2] if t2 else 0, n2))

def entry_dense(b, dig, T):
    d = dig.copy(); prev = None; last_bad = -1; info = None; ok = []
    for t in range(T + 1):
        P = rar.pairword(d); tp = tpl_at(P, b)
        good = False
        if tp is not None and prev is not None and prev[0] is not None:
            pB, pC, pg, pgam = prev
            if len(pB) + len(pC) <= 400:
                E = nbs.step(b, pB, pC)
                if E is not None:
                    _, _, B2, C2, u, v = E
                    good = (B2 == tp[0] and C2 == tp[1] and tp[2] == pg - pgam + u + v)
        if not good: last_bad = t
        nd, c = rar.normalize(P, b)
        if c: nd = np.concatenate((nd, np.array([1], dtype=np.int16)))
        prev = (tp[0], tp[1], tp[2], c) if tp else (None, None, 0, c)
        if t == T: info = tp
        d = nd
    entry = last_bad + 1
    cyc = None
    if info:
        rr = nbs.run(b, info[0], info[1], maxsteps=3000, maxlen=500)
        if rr[0] == 'cycle':
            es = rr[1]; cyc = {'len': len(es), 'sumgam': sum(nbs.gam(b, e[0], e[1]) for e in es), 'gain': sum(e[4] + e[5] for e in es),
                               'cert': bool(nbs.is_cert(b, es)), 'B0': es[0][0], 'C0': es[0][1]}
        else: cyc = {'run': rr[0], 't': rr[1]}
    return entry, cyc

if __name__ == '__main__':
    lo, hi, NS, T = map(int, sys.argv[1:5]); mn = int(sys.argv[5]) if len(sys.argv) > 5 else 3; mx = int(sys.argv[6]) if len(sys.argv) > 6 else 6
    out = open(f'data/census_{lo}_{hi}.jsonl', 'a')
    for b in range(lo, hi + 1):
        rng = np.random.default_rng(1000 + b); t0 = time.time()
        cnt = {'dead': 0, 'regular': 0, 'other': 0}; regs = []
        for s in range(NS):
            nd = int(rng.integers(mn, mx + 1)); dg = rng.integers(0, b, size=nd).astype(np.int16); dg[-1] = rng.integers(1, b)
            st, t, info = run_seed(b, dg, T)
            cnt[st] += 1
            if st == 'regular':
                e, cyc = entry_dense(b, dg, T)
                regs.append({'seed': rar.to_int(dg, b), 'entry': e, 'cyc': cyc})
        res = {'base': b, 'NS': NS, 'T': T, 'counts': cnt, 'regular': regs, 'secs': round(time.time() - t0, 1)}
        out.write(json.dumps(res) + '\n'); out.flush()
        ents = sorted(r['entry'] for r in regs)
        print(f"b={b} dead={cnt['dead']} regular={cnt['regular']} other={cnt['other']} entries(min/med/max)={ents[0] if ents else None}/{ents[len(ents)//2] if ents else None}/{ents[-1] if ents else None} cycs={sorted(set((r['cyc'].get('len'), r['cyc'].get('sumgam'), r['cyc'].get('cert')) for r in regs if r['cyc']))[:5]} {res['secs']}s", flush=True)
