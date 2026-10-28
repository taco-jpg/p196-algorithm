#!/usr/bin/env python3
"""orbit2.py -- instrumented reverse-and-add orbit with the extended detector panel (det.py).

scan2(b, digits, T, ...) -> (records, summary).  Records are produced for windows of W consecutive steps starting at
geometric checkpoints; each record has the static panel of the element (det.static_panel), the temporal-frozen
statistics (det.frozen: bottom-frame and centre-frame common prefix with the element q steps earlier, q<=24),
the best anchored single-band template, and the mirror's prediction check.
"""
import sys, os, json, time, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rar, nbs, det

def checkpoints(T, first=60, ratio=1.25, W=6):
    cps = []; t = float(first)
    while t < T - W:
        cps.append(int(t)); t = max(t * ratio, t + 1)
    cps.append(max(first, T - W))
    return sorted(set(c for c in cps if c + W <= T + 1))

def anchored_template(P, b, imax):
    bs = [x for x in rar.bands(P, b, ming=1) if x[0] <= imax]
    if not bs: return None
    i, g, L = max(bs, key=lambda t: (t[1], -t[0]))
    n = len(P)
    return (P[:i].tolist(), P[i + g:n - i - g].tolist(), g, i, L)

def scan2(b, dig, T, W=6, imax=300, tmax=1e9, first=60, ratio=1.25, qmax=24, lrs=True, verbose=False):
    t0 = time.time()
    cps = checkpoints(T, first, ratio, W)
    need = set()
    for c in cps:
        for k in range(-qmax, W): need.add(c + k)
    win = set(c + k for c in cps for k in range(W))
    recs = []; hist = []; histt = []
    d = dig.copy(); pal_at = None; gam_sum = 0; prev_tpl = None
    t_end = 0
    for t in range(T + 1):
        n = len(d); P = rar.pairword(d)
        if rar.is_pal(d): pal_at = t; break
        nd, c = rar.normalize(P, b)
        if c: nd = np.concatenate((nd, np.array([1], dtype=np.int16)))
        gam_sum += c
        if t in need:
            H = P[:(n + 1) // 2].astype(np.int64)
            if t in win:
                r = {'t': t, 'gam': c}
                r.update(det.static_panel(d, P, b, imax=imax, do_lrs=lrs))
                Fb, qb, Fc, qc = det.frozen(H, hist, qmax)
                r.update({'Fb': Fb, 'qb': qb, 'Fc': Fc, 'qc': qc})
                tp = anchored_template(P, b, imax)
                if tp:
                    B, C, g = tp[0], tp[1], tp[2]
                    r['tpl_g'] = g; r['tpl_i'] = tp[3]; r['tpl_Clen'] = len(C)
                    r['pred_ok'] = None
                    if prev_tpl is not None and prev_tpl[0] is not None and prev_tpl[4] == t - 1:
                        pB, pC, pg, pgam = prev_tpl[:4]
                        if len(pB) + len(pC) <= 400:
                            E = nbs.step(b, pB, pC)
                            if E is None: r['pred_ok'] = 'hypfail'
                            else:
                                _, _, B2, C2, u, v = E
                                r['pred_ok'] = bool(B2 == B and C2 == C and g == pg - pgam + u + v)
                    if g >= 2 and len(B) + len(C) <= 200:
                        rr = nbs.run(b, B, C, maxsteps=1500, maxlen=400)
                        r['run'] = rr[0]
                        if rr[0] == 'cycle':
                            es = rr[1]; r['cyc_len'] = len(es)
                            r['cyc_sumgam'] = sum(nbs.gam(b, e[0], e[1]) for e in es)
                            r['cyc_gain'] = sum(e[4] + e[5] for e in es)
                            r['cyc_cert'] = bool(nbs.is_cert(b, es))
                    prev_tpl = (B, C, g, c, t)
                else:
                    r['tpl_g'] = 0; r['tpl_i'] = -1; prev_tpl = (None, None, 0, c, t)
                recs.append(r)
            hist.append(H); histt.append(t)
            if len(hist) > qmax + 2: hist.pop(0); histt.pop(0)
            # history must contain consecutive steps only
            if len(histt) >= 2 and histt[-1] != histt[-2] + 1:
                hist = [H]; histt = [t]
        d = nd; t_end = t
        if time.time() - t0 > tmax: break
    summ = {'summary': True, 'base': b, 'steps_done': t_end + 1, 'final_digits': len(d), 'palindrome_at': pal_at,
            'gam_density': gam_sum / max(1, t_end + 1), 'secs': round(time.time() - t0, 2)}
    return recs, summ

def null_records(b, ns, K=8, seed=0, lrs=True):
    """static panels of K random digit strings for each length in ns."""
    rng = np.random.default_rng(seed)
    out = []
    for n in ns:
        for k in range(K):
            dg = rng.integers(0, b, size=n).astype(np.int16); dg[-1] = rng.integers(1, b)
            P = rar.pairword(dg)
            r = det.static_panel(dg, P, b, do_lrs=lrs); r['null'] = True
            out.append(r)
    return out

def parse_seed(s, b):
    if s.startswith('rnd:'):
        _, nd, rs = s.split(':'); nd = int(nd); rng = np.random.default_rng(int(rs))
        dg = rng.integers(0, b, size=nd).astype(np.int16); dg[-1] = rng.integers(1, b)
        return dg
    return rar.to_digits(int(s), b)

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('base', type=int); ap.add_argument('seed'); ap.add_argument('steps', type=int)
    ap.add_argument('--out'); ap.add_argument('--tmax', type=float, default=1500); ap.add_argument('--W', type=int, default=6)
    a = ap.parse_args()
    dig = parse_seed(a.seed, a.base)
    recs, summ = scan2(a.base, dig, a.steps, W=a.W, tmax=a.tmax)
    summ['seed'] = a.seed
    out = a.out or f'data/scan2_b{a.base}_{a.seed.replace(":", "_")}.jsonl'
    with open(out, 'w') as f:
        for r in recs: f.write(json.dumps(r) + '\n')
        f.write(json.dumps(summ) + '\n')
    print(json.dumps(summ))
