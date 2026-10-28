#!/usr/bin/env python3
"""orbit_scan.py -- run one reverse-and-add orbit, collect detector statistics at checkpoint windows.

usage: orbit_scan.py BASE SEED STEPS [--window W] [--out FILE.jsonl] [--tmax SEC] [--imax I]

Per step (cheap):  n (digits), gam (digit growth).
At checkpoint windows (W consecutive steps starting at geometric grid points): rar.panel statistics,
single-band template (B,C,g) with |B| <= imax, mirror prediction check vs. next observed template,
mirror canonical run (cycle / break / grow / long) from the observed template.
A checkpoint record is a dict; the file is JSON lines, last line = summary record {"summary": ...}.
SEED may be an integer in decimal, or 'rnd:<ndigits>:<rngseed>' (random base-b digit string).
"""
import sys, os, json, time, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rar, nbs

def parse_seed(s, b):
    if s.startswith('rnd:'):
        _, nd, rs = s.split(':'); nd = int(nd); rng = np.random.default_rng(int(rs))
        dg = rng.integers(0, b, size=nd).astype(np.int16); dg[-1] = rng.integers(1, b)
        return dg
    return rar.to_digits(int(s), b)

def checkpoints(T, W):
    cps = set(range(0, min(T, 300) + 1))
    t = 300.0
    while t < T:
        cps.add(int(t)); t *= 1.12
    return sorted(c for c in cps if c <= T)

def anchored_template(P, b, imax):
    bs = [x for x in rar.bands(P, b, ming=1) if x[0] <= imax]
    if not bs: return None
    i, g, L = max(bs, key=lambda t: (t[1], -t[0]))
    n = len(P)
    return (P[:i].tolist(), P[i + g:n - i - g].tolist(), g, i, L)

def scan(b, dig, T, W=10, imax=300, tmax=1e9, dense=False, heavy=True, verbose=False):
    t0 = time.time()
    cps = set(checkpoints(T, W)); cps.add(max(0, T - W + 1))
    if dense: cps = set(range(T + 1))
    # windows: a checkpoint opens a window of W consecutive steps
    wins = set()
    for c in cps:
        for k in range(W): wins.add(c + k)
    recs = []; prev_tpl = None; prev_gam = None
    d = dig.copy(); n_hist = []; gam_hist = []
    pal_at = None
    for t in range(T + 1):
        n = len(d); P = rar.pairword(d)
        if rar.is_pal(d):
            pal_at = t; break
        nd, c = rar.normalize(P, b)
        if c: nd = np.concatenate((nd, np.array([1], dtype=np.int16)))
        gam_hist.append(c); n_hist.append(n)
        if t in wins:
            r = {'t': t, 'gam': c}
            r.update(rar.panel(d, P, b, heavy=heavy and (t in cps)))
            tp = anchored_template(P, b, imax)
            r['tpl_g'] = tp[2] if tp else 0
            r['tpl_i'] = tp[3] if tp else -1
            r['tpl_Clen'] = len(tp[1]) if tp else -1
            r['tpl'] = None
            if tp:
                B, C, g = tp[0], tp[1], tp[2]
                r['tpl'] = [B if len(B) <= 40 else B[:40] + ['..'], C if len(C) <= 40 else C[:40] + ['..']]
                # does the observed template follow the mirror's prediction from the previous observed template?
                r['pred_ok'] = None
                if prev_tpl is not None and prev_tpl[0] is not None and t - 1 in wins:
                    pB, pC, pg, pgam = prev_tpl[0], prev_tpl[1], prev_tpl[2], prev_tpl[3]
                    if len(pB) + len(pC) <= 400:
                        E = nbs.step(b, pB, pC)
                        if E is None: r['pred_ok'] = 'hypfail'
                        else:
                            _, _, B2, C2, u, v = E
                            r['pred_ok'] = bool(B2 == B and C2 == C and g == pg - pgam + u + v)
                # canonical mirror run
                if g >= 2 and len(B) + len(C) <= 200 and (t in cps):
                    rr = nbs.run(b, B, C, maxsteps=1500, maxlen=400)
                    r['run'] = rr[0]
                    if rr[0] == 'cycle':
                        es = rr[1]; r['cyc_len'] = len(es)
                        r['cyc_sumgam'] = sum(nbs.gam(b, e[0], e[1]) for e in es)
                        r['cyc_gain'] = sum(e[4] + e[5] for e in es)
                        r['cyc_cert'] = bool(nbs.is_cert(b, es))
                    else: r['run_t'] = rr[1]
                prev_tpl = (B, C, g, c)
            else:
                prev_tpl = (None, None, 0, c)
            recs.append(r)
        d = nd
        if time.time() - t0 > tmax:
            break
    summ = {'summary': True, 'base': b, 'steps_done': len(gam_hist), 'final_digits': len(d), 'palindrome_at': pal_at,
            'gam_density': float(np.mean(gam_hist)) if gam_hist else None, 'secs': time.time() - t0}
    return recs, summ, gam_hist, n_hist

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('base', type=int); ap.add_argument('seed'); ap.add_argument('steps', type=int)
    ap.add_argument('--window', type=int, default=10); ap.add_argument('--out'); ap.add_argument('--tmax', type=float, default=1100)
    ap.add_argument('--imax', type=int, default=300)
    a = ap.parse_args()
    dig = parse_seed(a.seed, a.base)
    recs, summ, g, nn = scan(a.base, dig, a.steps, a.window, a.imax, a.tmax)
    summ['seed'] = a.seed
    out = a.out or f'data/scan_b{a.base}_{a.seed.replace(":", "_")}.jsonl'
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    with open(out, 'w') as f:
        for r in recs: f.write(json.dumps(r) + '\n')
        f.write(json.dumps(summ) + '\n')
    print(json.dumps(summ))
