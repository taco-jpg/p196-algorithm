#!/usr/bin/env python3
"""surrogate.py BASE T NORB NSUR OUT.json [named seeds] -- orbit snapshots vs surrogates of their own half pair word.
Surrogates: S1 = random permutation of the cells (keeps the marginal, kills all order), S2 = first-order Markov chain fitted to the
snapshot (keeps marginal + nearest-neighbour transition statistics).  Detectors: runs of 9/0/top/any, periodic stretches, LRS, #9-runs>=3.
Reports mean z-scores of the real snapshot against each surrogate family (z = (real - mean_s)/sd_s), plus the fraction of snapshots with
real value above the surrogate maximum (exceedance)."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rar, det, base10_stats

def detectors(H, b):
    nb = b - 1; out = {}
    st, ln = rar.runs_of(H == nb); out['r9'] = int(ln.max()) if len(ln) else 0
    out['n9ge3'] = int((ln >= 3).sum())
    st, ln = rar.runs_of(H == 0); out['r0'] = int(ln.max()) if len(ln) else 0
    st, ln = rar.runs_of(H == 2 * nb); out['rtop'] = int(ln.max()) if len(ln) else 0
    stc, lnc, vc = rar.const_runs(H); out['rany'] = int(lnc.max())
    for p in (2, 3, 4, 6): out['per%d' % p] = rar.periodic_stretch(H, p)[0]
    out['lrs'] = det.lrs_nonoverlap(H, True)[0]
    return out

def markov_sample(H, K, m, rng):
    cnt = np.zeros((K, K)); np.add.at(cnt, (H[:-1], H[1:]), 1)
    marg = np.bincount(H, minlength=K).astype(float)
    # smooth tiny: rows with no data -> marginal
    rows = cnt.sum(1)
    P = np.where(rows[:, None] > 0, cnt / np.maximum(rows[:, None], 1), marg[None, :] / marg.sum())
    cum = np.cumsum(P, axis=1)
    x = np.empty(m, dtype=np.int64); x[0] = rng.choice(K, p=marg / marg.sum())
    u = rng.random(m)
    for i in range(1, m):
        x[i] = min(int(np.searchsorted(cum[x[i - 1]], u[i])), K - 1)
    return x

if __name__ == '__main__':
    b = int(sys.argv[1]); T = int(sys.argv[2]); NO = int(sys.argv[3]); NS = int(sys.argv[4]); outfn = sys.argv[5]
    named = [int(s) for s in sys.argv[6:]]
    seeds = [('n%d' % x, rar.to_digits(x, b)) for x in named]
    rs, _ = base10_stats.rand_survivors(b, NO, seed=4242)
    seeds += [('r%02d' % i, dg) for i, dg in enumerate(rs)]
    cps = sorted(set(int(x) for x in np.geomspace(300, T, 12)))
    K = 2 * b - 1; rng = np.random.default_rng(99)
    keys = None; Z = {'perm': {}, 'markov': {}}; EX = {'perm': {}, 'markov': {}}; REAL = {}
    t0 = time.time(); nsnap = 0
    for name, dg in seeds:
        d = dg.copy()
        for t in range(T + 1):
            if t in cps:
                n = len(d); H = rar.pairword(d)[:(n + 1) // 2].astype(np.int64); m = len(H)
                real = detectors(H, b)
                for fam in ('perm', 'markov'):
                    sur = []
                    for _ in range(NS):
                        S = rng.permutation(H) if fam == 'perm' else markov_sample(H, K, m, rng)
                        sur.append(detectors(S, b))
                    for k in real:
                        arr = np.array([s[k] for s in sur], dtype=float); mu, sd = arr.mean(), arr.std()
                        z = (real[k] - mu) / sd if sd > 0 else (0.0 if real[k] == mu else np.sign(real[k] - mu) * 9.99)
                        Z[fam].setdefault(k, []).append(float(z)); EX[fam].setdefault(k, []).append(int(real[k] > arr.max()))
                for k in real: REAL.setdefault(k, []).append(real[k])
                nsnap += 1
            d, _, _ = rar.revadd(d, b)
        print(name, nsnap, round(time.time() - t0, 1), flush=True)
    summ = {}
    for fam in ('perm', 'markov'):
        summ[fam] = {k: {'mean_z': float(np.mean(v)), 'frac_z_gt3': float(np.mean(np.array(v) > 3)), 'frac_exceed_max': float(np.mean(EX[fam][k]))} for k, v in Z[fam].items()}
    summ['nsnap'] = nsnap; summ['real_mean'] = {k: float(np.mean(v)) for k, v in REAL.items()}
    json.dump(summ, open(outfn, 'w'), indent=1)
    print(f"snapshots {nsnap}")
    for fam in ('perm', 'markov'):
        print(fam)
        for k in Z[fam]: print(f"  {k:6s} real mean {np.mean(REAL[k]):6.2f}  mean z {summ[fam][k]['mean_z']:+6.2f}  frac z>3 {summ[fam][k]['frac_z_gt3']:.3f}  frac exceed surrogate max {summ[fam][k]['frac_exceed_max']:.3f}")
