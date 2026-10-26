#!/usr/bin/env python3
"""Random-start scan of the canonical neutral-band map in every base 3..40 (same budget per base).

For each base b: N random starts (B of length 1..LB with B[0]>=1 and entries uniform in [0,2b-2]; C a random symmetric word of
length 0..LC with entries uniform in [0,2b-2]).  Each start is followed with the canonical (maximally trimmed) map
`run(b,B,C)` of calculation/neutral_band_search.py.  A 'cycle' is recorded (it is automatically a certificate: any closed
cycle has sumGain = 1.5*sumGam, see decouple.py) and re-checked with cycleOK.  Per base we print:
    base, starts, breaks, grew, long, cycles, distinct cycles, smallest cycle (edges, |B|+|C|), best sumGam
NOTE: uniform random starts essentially only find cycles whose exterior/interior are tiny (powers of two); cycles such as
bases 11/17/26 need exteriors of length 7-29 and are NOT reachable this way.  Use studio_pipeline.py for the real search.

usage (Mac Studio, 32 cores):   python3 studio_random_scan.py --N 20000000 --jobs 32 --out scan_random.jsonl
quick test:                     python3 studio_random_scan.py --N 20000 --bases 2,4,8,10,11 --jobs 2
runtime: about 15-25 microseconds per start per core in CPython for b~10 (most starts break after 1-3 steps);
         N=2e7 x 38 bases / 32 cores ~ 10-20 min.  Memory: < 100 MB per process (a 'seen' dict per run, <= 3000 steps).
"""
import sys, os, json, random, time, argparse, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nb_mirror import run, cycleOK, is_cert, gam as GAM


def one_base(args):
    b, N, LB, LC, seed, maxsteps, maxlen = args
    rng = random.Random(seed * 1000003 + b)
    cnt = {'break': 0, 'grow': 0, 'long': 0, 'cycle': 0}
    cycles = {}
    hi = 2 * b - 2
    for _ in range(N):
        lb = rng.randint(1, LB)
        B = [rng.randint(1, hi)] + [rng.randint(0, hi) for _ in range(lb - 1)]
        lc = rng.randint(0, LC)
        half = [rng.randint(0, hi) for _ in range((lc + 1) // 2)]
        C = half + half[:lc // 2][::-1]
        r = run(b, B, C, maxsteps=maxsteps, maxlen=maxlen)
        cnt[r[0]] += 1
        if r[0] == 'cycle':
            es = r[1]
            key = (tuple(es[0][0]), tuple(es[0][1]), len(es))
            if key not in cycles:
                ok = cycleOK(b, es, es[0][0], es[0][1])
                cycles[key] = (len(es), len(es[0][0]) + len(es[0][1]), sum(GAM(b, e[0], e[1]) for e in es), ok)
    return b, N, cnt, cycles


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--N', type=int, default=1000000)
    ap.add_argument('--LB', type=int, default=12)
    ap.add_argument('--LC', type=int, default=12)
    ap.add_argument('--bases', default=','.join(map(str, range(3, 41))))
    ap.add_argument('--jobs', type=int, default=2)
    ap.add_argument('--chunks', type=int, default=8, help='split each base into this many seeds/tasks for load balance')
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--out', default='scan_random.jsonl')
    a = ap.parse_args()
    bases = [int(x) for x in a.bases.split(',')]
    per = a.N // a.chunks
    tasks = [(b, per, a.LB, a.LC, a.seed * 100 + c, 500, 120) for b in bases for c in range(a.chunks)]
    t0 = time.time()
    agg = {b: {'starts': 0, 'break': 0, 'grow': 0, 'long': 0, 'cycle': 0, 'cycles': {}} for b in bases}
    with mp.Pool(a.jobs) as pool, open(a.out, 'w') as fo:
        for b, n, cnt, cycles in pool.imap_unordered(one_base, tasks):
            g = agg[b]; g['starts'] += n
            for k in cnt: g[k] += cnt[k]
            for key, v in cycles.items(): g['cycles'][key] = v
            fo.write(json.dumps({'base': b, 'starts': n, 'counts': cnt, 'cycles': [[list(k[0]), list(k[1]), k[2]] + list(v) for k, v in cycles.items()]}) + '\n'); fo.flush()
    print(f"{'base':>4} {'starts':>10} {'breaks':>10} {'grow':>6} {'long':>6} {'cycle-hits':>10} {'distinct':>8} {'smallest(edges,|B|+|C|)':>24} {'cycleOK':>8}")
    for b in bases:
        g = agg[b]
        sm = min(g['cycles'].values(), key=lambda v: (v[1], v[0])) if g['cycles'] else None
        allok = all(v[3] for v in g['cycles'].values()) if g['cycles'] else ''
        print(f"{b:>4} {g['starts']:>10} {g['break']:>10} {g['grow']:>6} {g['long']:>6} {g['cycle']:>10} {len(g['cycles']):>8} {str((sm[0], sm[1])) if sm else '-':>24} {str(allok):>8}")
    print(f"elapsed {time.time()-t0:.0f}s")


if __name__ == '__main__':
    main()
