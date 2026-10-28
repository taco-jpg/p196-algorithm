#!/usr/bin/env python3
"""base10_stats.py BASE T NRAND OUT [named seeds...]  -- extended-panel orbit scans for named seeds + NRAND random Lychrel-candidate seeds
(random 10..30-digit numbers that survive 400 steps without a palindrome), plus static null panels (random digit strings of the
same length as the orbit element at each checkpoint).  One JSON line per window record; gzip output."""
import sys, os, json, time, gzip
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rar, orbit2

def survives(b, dig, steps=400):
    d = dig.copy()
    for t in range(steps):
        if rar.is_pal(d): return False
        d, _, _ = rar.revadd(d, b)
    return not rar.is_pal(d)

def rand_survivors(b, k, seed=777, lo=10, hi=30):
    rng = np.random.default_rng(seed); out = []; heads = set(); tried = 0
    while len(out) < k:
        tried += 1
        nd = int(rng.integers(lo, hi + 1)); dg = rng.integers(0, b, size=nd).astype(np.int16); dg[-1] = rng.integers(1, b)
        if not survives(b, dg): continue
        d = dg.copy()
        for _ in range(40): d, _, _ = rar.revadd(d, b)
        key = d.tobytes()
        if key in heads: continue
        heads.add(key); out.append(dg)
    return out, tried

if __name__ == '__main__':
    b = int(sys.argv[1]); T = int(sys.argv[2]); NR = int(sys.argv[3]); outfn = sys.argv[4]
    named = [int(s) for s in sys.argv[5:]]
    seeds = [('n%d' % x, rar.to_digits(x, b)) for x in named]
    rs, tried = rand_survivors(b, NR)
    print('random survivors', len(rs), 'tried', tried, flush=True)
    seeds += [('r%02d' % i, dg) for i, dg in enumerate(rs)]
    with gzip.open(outfn, 'wt') as f:
        for name, dg in seeds:
            t0 = time.time()
            recs, summ = orbit2.scan2(b, dg, T, W=4, tmax=900)
            ns = sorted(set(r['n'] for r in recs))
            for r in recs:
                r['seedname'] = name; r['base'] = b
                f.write(json.dumps(r) + '\n')
            summ['seedname'] = name; summ['seed'] = rar.to_int(dg, b) if len(dg) < 60 else None
            f.write(json.dumps(summ) + '\n')
            f.flush()
            print(name, summ['steps_done'], summ['final_digits'], summ['palindrome_at'], round(time.time() - t0, 1), flush=True)
