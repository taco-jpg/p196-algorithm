#!/usr/bin/env python3
"""Main-session independent check of r12d's cen3 enumerations (fixed-centre exact returns, decimal p8 lattices).
Own parser of p8_scc.txt, own centre indexing, plain Python integers N -> N + rev(N).
Uses no klib, no cen2/cen3, no tsat.
For every legal palindromic centre C of length L:  P0 = B0 W0^q0 C rev(...),  N + rev(N) = sum P0_i 10^i,
then S-1 further integer steps; compare the final pair word with P(q0+K, C).
Records: returns, first-mismatch index histogram (= cen3 'prefix'), clock deviations, length errors.
usage: indep_enum.py p8_scc.txt cen_log_dir workers"""
import sys, re, time
from multiprocessing import Pool
try:
    sys.set_int_max_str_digits(0)
except AttributeError:
    pass

FN = None
LAT = {}


def load(fn, idx):
    lines = [l for l in open(fn).read().splitlines() if l.startswith('SCC')]
    line = lines[idx]
    g = [int(ch) for ch in re.search(r' g=(\d+) ', line).group(1)]
    pre, cyc = line.split(' cyc=', 1)
    path = pre.split(' path=', 1)[1]
    cols = lambda s: [list(map(int, c.split(','))) for c in re.findall(r'\[([^\]]+)\]', s)]
    B0 = [c[0] for c in cols(path)]
    W0 = [c[0] for c in cols(cyc)]
    return g, B0, W0


def init(fn):
    for li in (0, 1, 2):
        LAT[li] = load(fn, li)


def centre(idx, L):
    h, odd = L // 2, L % 2
    r = idx
    mid = []
    if odd:
        mid = [2 * (r % 10)]
        r //= 10
    half = []
    for _ in range(h):
        half.append(r % 19)
        r //= 19
    half = half[::-1]
    return half + mid + half[::-1]


def ncentres(L):
    return 19 ** (L // 2) * (10 if L % 2 else 1)


def work(a):
    li, K, L, q0, lo, hi = a
    g, B0, W0 = LAT[li]
    p, m = len(g), len(W0)
    S = 2 * m * p * K // sum(g)
    half = B0 + W0 * q0
    halfT = B0 + W0 * (q0 + K)
    hist = {}
    ret = 0
    best = -1
    arg = []
    lenerr = clockdev = pal = 0
    for idx in range(lo, hi):
        C = centre(idx, L)
        P = half + C + half[::-1]
        T = halfT + C + halfT[::-1]
        d = []
        c = 0
        for v in P:
            s = v + c
            d.append(s % 10)
            c = s // 10
        while c:
            d.append(c % 10)
            c //= 10
        s = ''.join(map(str, reversed(d)))          # T(N), most significant digit first
        if len(s) - len(P) != g[0]:
            clockdev += 1
        if s == s[::-1]:
            pal += 1
        M = int(s)
        for t in range(1, S):
            n_prev = len(s)
            M += int(s[::-1])
            s = str(M)
            if len(s) - n_prev != g[t % p]:
                clockdev += 1
            if s == s[::-1]:
                pal += 1
        e = s[::-1]
        n = len(e)
        if n != len(T):
            lenerr += 1
            pre = -1
        else:
            pre = n
            for i in range((n + 1) // 2):
                if int(e[i]) + int(e[n - 1 - i]) != T[i]:
                    pre = i
                    break
            if pre == n:
                ret += 1
        hist[pre] = hist.get(pre, 0) + 1
        if pre > best:
            best = pre
            arg = [idx]
        elif pre == best and len(arg) < 8:
            arg.append(idx)
    return hist, ret, best, arg, lenerr, clockdev, pal


def cen3_log(logdir, li, K, L):
    fn = f'{logdir}/cen_rec{li}_K{K}_L{L}.log'
    res = hist = None
    try:
        for line in open(fn):
            if line.startswith('RESULT'):
                res = dict(tok.split('=', 1) for tok in line.split()[1:] if '=' in tok)
            elif line.startswith('HIST'):
                hist = {int(a): int(b) for a, b in (tok.split(':') for tok in line.split()[1:])}
    except FileNotFoundError:
        return None, None
    return res, hist


def main():
    fn, logdir, W = sys.argv[1], sys.argv[2], int(sys.argv[3])
    init(fn)
    exp = {0: (39, 20), 1: (39, 20), 2: (11, 48)}
    for li in (0, 1, 2):
        g, B0, W0 = LAT[li]
        assert (len(B0), len(W0)) == exp[li], (li, len(B0), len(W0))
        assert g == [1, 0, 1, 0, 1, 0, 1, 0], g
        assert B0[0] >= 1
    cases = [(2, 1, 4, 4), (2, 1, 5, 4), (2, 1, 6, 4), (2, 1, 7, 4), (2, 2, 4, 6), (2, 2, 5, 6), (2, 3, 4, 9), (2, 3, 5, 9)]
    for li in (0, 1):
        cases += [(li, 4, 4, 15), (li, 4, 5, 15), (li, 4, 6, 15), (li, 5, 4, 18), (li, 5, 5, 18), (li, 6, 4, 21), (li, 6, 5, 21)]
    allok = True
    with Pool(W, initializer=init, initargs=(fn,)) as pool:
        for (li, K, L, q0) in cases:
            t0 = time.time()
            N = ncentres(L)
            ch = max(1, N // (W * 4))
            jobs = [(li, K, L, q0, lo, min(N, lo + ch)) for lo in range(0, N, ch)]
            H = {}
            R = LE = CD = PAL = 0
            best = -1
            arg = []
            for hist, ret, b, a, le, cd, pal in pool.map(work, jobs):
                for k, v in hist.items():
                    H[k] = H.get(k, 0) + v
                R += ret
                LE += le
                CD += cd
                PAL += pal
                if b > best:
                    best, arg = b, list(a)
                elif b == best:
                    arg += a
            res, h3 = cen3_log(logdir, li, K, L)
            if res is None:
                cmp = 'NO_CEN3_LOG'
                ok = False
            else:
                ok = (int(res['returns']) == R == 0 and int(res['maxprefix']) == best and h3 == H
                      and int(res['centres']) == N and int(res['argmax_idx']) in arg + [None])
                cmp = (f"cen3 returns={res['returns']} maxprefix={res['maxprefix']} argmax_idx={res['argmax_idx']} "
                       f"centres={res['centres']} hist_equal={h3 == H}")
            allok &= ok
            print(f'CASE rec{li} K={K} L={L} q0={q0} centres={N} | mine returns={R} maxprefix={best} argmax={arg[:4]} '
                  f'lenerr={LE} clockdev={CD} pal={PAL} | {cmp} | {"AGREE" if ok else "DIFFER"} {time.time() - t0:.0f}s',
                  flush=True)
            if not ok:
                print('  mine HIST', ' '.join(f'{k}:{H[k]}' for k in sorted(H)), flush=True)
                if h3:
                    print('  cen3 HIST', ' '.join(f'{k}:{h3[k]}' for k in sorted(h3)), flush=True)
    print('INDEP_ENUM_DONE all_agree=' + str(allok), flush=True)


if __name__ == '__main__':
    main()
