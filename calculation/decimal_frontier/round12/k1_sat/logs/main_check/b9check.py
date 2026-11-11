#!/usr/bin/env python3
"""Main-session check of r12d's base-9 positive controls.
(1) runs tsrun.py ret on b9r0/b9r1 (q0=5, K=1, L=4,6,8,10) and re-checks every SAT centre by an own base-9
    digit simulation (no klib, no tsat), also over 3 periods (K=3);
(2) enumerates every legal centre for L=4,6,8 with the own simulation and counts exact returns, so tsat's
    SAT / UNSAT answers are checked in both directions.
usage: b9check.py r12d_copy_dir workers"""
import sys, json, subprocess, re, os, time
from multiprocessing import Pool

J = {}


def init(d):
    for name, fn in (('b9r0', 'cert_b9_rec0.json'), ('b9r1', 'cert_b9_rec1.json')):
        J[name] = json.load(open(os.path.join(d, 'ctrl', fn)))


def step(d, b):
    n = len(d)
    s = [d[i] + d[n - 1 - i] for i in range(n)]
    out = []
    c = 0
    for v in s:
        v += c
        out.append(v % b)
        c = v // b
    while c:
        out.append(c % b)
        c //= b
    return out


def check(name, q0, K, C):
    X = J[name]
    b, g = X['base'], X['gam']
    p = len(g)
    B0, W0 = X['B_t'][0], X['w_t'][0]
    m = len(W0)
    S = 2 * m * p * K // sum(g)
    half = B0 + W0 * q0
    halfT = B0 + W0 * (q0 + K)
    P = half + C + half[::-1]
    T = halfT + C + halfT[::-1]
    d = []
    c = 0
    for v in P:
        v += c
        d.append(v % b)
        c = v // b
    while c:
        d.append(c % b)
        c //= b
    lens = [len(P), len(d)]
    pal = 1 if d == d[::-1] else 0
    for t in range(1, S):
        d = step(d, b)
        lens.append(len(d))
        if d == d[::-1]:
            pal += 1
    n = len(d)
    Pn = [d[i] + d[n - 1 - i] for i in range(n)]
    clock_ok = all(lens[t + 1] - lens[t] == g[t % p] for t in range(S))
    return Pn == T, clock_ok, pal, S


def centre(idx, L, b):
    h, odd = L // 2, L % 2
    r = idx
    mid = []
    if odd:
        mid = [2 * (r % b)]
        r //= b
    half = []
    for _ in range(h):
        half.append(r % (2 * b - 1))
        r //= (2 * b - 1)
    half = half[::-1]
    return half + mid + half[::-1]


def enum_work(a):
    name, L, lo, hi = a
    b = J[name]['base']
    hits = []
    for idx in range(lo, hi):
        C = centre(idx, L, b)
        ok, clk, pal, S = check(name, 5, 1, C)
        if ok:
            hits.append((C, clk, pal))
    return hits


def main():
    d, W = sys.argv[1], int(sys.argv[2])
    init(d)
    py = sys.executable
    print('== (1) tsrun ret + own base-9 simulation', flush=True)
    for name in ('b9r0', 'b9r1'):
        for L in (4, 6, 8, 10):
            out = subprocess.run([py, 'tsrun.py', 'ret', '--lat', name, '--q0', '5', '--K', '1', '--L', str(L)],
                                 cwd=d, capture_output=True, text=True).stdout
            r = [l for l in out.splitlines() if l.startswith('RESULT')]
            if not r:
                print(f'{name} L={L}: NO RESULT\n{out[-500:]}', flush=True)
                continue
            r = r[-1]
            st = r.split()[1]
            msg = f'{name} L={L}: tsat {st}'
            if st == 'SAT':
                C = json.loads(re.search(r'centre0=(\[[^\]]*\])', r).group(1))
                e1, c1, p1, S1 = check(name, 5, 1, C)
                e3, c3, p3, S3 = check(name, 5, 3, C)
                msg += f' C={C} own-sim K=1 (S={S1}) exact={e1} clock={c1} pal={p1}; K=3 (S={S3}) exact={e3} clock={c3} pal={p3}'
            print(msg, flush=True)
    print('== (2) full enumeration with own simulation (q0=5, K=1)', flush=True)
    with Pool(W, initializer=init, initargs=(d,)) as pool:
        for name in ('b9r0', 'b9r1'):
            b = J[name]['base']
            for L in (4, 6, 8):
                t0 = time.time()
                N = (2 * b - 1) ** (L // 2) * (b if L % 2 else 1)
                ch = max(1, N // (W * 4))
                jobs = [(name, L, lo, min(N, lo + ch)) for lo in range(0, N, ch)]
                hits = [h for part in pool.map(enum_work, jobs) for h in part]
                print(f'{name} L={L}: centres={N} exact returns={len(hits)} '
                      f'{[h[0] for h in hits][:6]} clocks_ok={all(h[1] for h in hits)} pal={sum(h[2] for h in hits)} '
                      f'{time.time() - t0:.0f}s', flush=True)
    print('B9CHECK_DONE', flush=True)


if __name__ == '__main__':
    main()
