#!/usr/bin/env python3
"""r12g verify_kink.py -- paranoid replay of a periodic-centre candidate (a kfwd / kink7 exact cycle), r12d verify_hit protocol.
Builds a genuine number whose folded pair word is  exterior B + lattice row at time t (up to the frame c) + the K-window
(top cell = middle of the number), n = 2h - par, and replays it with TWO independent implementations at every step:
  (1) pair-word step (klib.pairword_step for base 10, own generic step otherwise),
  (2) plain digit arithmetic: base 10 = Python int N + int(str(N)[::-1]); other bases = digit lists (independent code).
Checks at every step: both implementations agree; the number is not a palindrome; the lattice is exact on every folded column
below h-K; and the clock equals g.  Records every return of the top-K window to its initial state (the period).
Runs max(STEPS, 3 periods) steps (default STEPS = 20000).
usage: verify_kink.py LAT K t j par w0 .. w{K-1} [--steps N] [--blocks Q]     LAT in rec0 rec1 rec2 p12m9 b9r0 b9r1"""
import sys, os, json, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation'))
if hasattr(sys, 'set_int_max_str_digits'): sys.set_int_max_str_digits(0)


def load(name):
    if name in ('rec0', 'rec1', 'rec2', 'p12m9'):
        import klib
        L = klib.load(name); return 10, L.g, L.B, L.W
    J = json.load(open(os.path.join(HERE, '../ctrl', {'b9r0': 'cert_b9_rec0.json', 'b9r1': 'cert_b9_rec1.json'}[name])))
    return J['base'], J['gam'], J['B_t'], J['w_t']


def pw_step_generic(P, b):
    O = []; c = 0
    for v in P:
        s = v + c; O.append(s % b); c = s // b
    if c: O.append(c)
    n2 = len(O)
    return [O[i] + O[n2 - 1 - i] for i in range(n2)], n2 - len(P)


def digits_from_pair(P, b):
    n = len(P); d = [0] * n
    for i in range((n + 1) // 2):
        j = n - 1 - i
        if i == j:
            assert P[i] % 2 == 0, 'odd middle cell'; d[i] = P[i] // 2
        else:
            hi = min(b - 1, P[i]); d[j] = hi; d[i] = P[i] - hi
    assert d[-1] != 0, 'leading digit zero'
    return d   # LSB first


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lat'); ap.add_argument('K', type=int); ap.add_argument('t', type=int); ap.add_argument('j', type=int)
    ap.add_argument('par', type=int); ap.add_argument('w', type=int, nargs='+')
    ap.add_argument('--steps', type=int, default=20000); ap.add_argument('--blocks', type=int, default=15)
    a = ap.parse_args()
    b, g, B, W = load(a.lat); p = len(g); nB = len(B[0]); m = len(W[0]); K = a.K; win = a.w; assert len(win) == K
    cell = lambda t, x: B[t % p][x] if x < nB else W[t % p][(x - nB) % m]
    c = nB + a.blocks * m + a.j; h = c + K; n = 2 * h - a.par
    low = [cell(a.t, x) for x in range(c)] + win
    P = low + low[:n // 2][::-1]
    d = digits_from_pair(P, b)
    if b == 10:
        import klib
        step = lambda Q: klib.pairword_step(Q)
        N = int(''.join(map(str, d[::-1])))
    else:
        step = lambda Q: pw_step_generic(Q, b)
        N = list(d)
    t = a.t; returns = []; fail = None; s = 0; maxsteps = a.steps
    key0 = (a.t % p, a.j % m, a.par, tuple(win))
    while s < maxsteps:
        P, gam = step(P)
        if b == 10:
            N = N + int(str(N)[::-1]); dig = [int(ch) for ch in str(N)[::-1]]
        else:   # independent digit-list addition of the reversal
            R = N[::-1]; out = []; cc = 0
            for i in range(len(N)):
                v = N[i] + R[i] + cc; out.append(v % b); cc = v // b
            if cc: out.append(cc)
            N = out; dig = N
        s += 1; t += 1
        nn = len(dig); hh = (nn + 1) // 2
        Pd = [dig[i] + dig[nn - 1 - i] for i in range(nn)]
        if Pd != P: fail = ('PAIRWORD_MISMATCH', s); break
        if dig == dig[::-1]: fail = ('PALINDROME', s); break
        if gam != g[(t - 1) % p]: fail = ('CLOCK', s); break
        if any(P[x] != cell(t, x) for x in range(hh - K)): fail = ('LATTICE_BROKEN', s); break
        key = (t % p, (hh - K - nB) % m, nn % 2, tuple(P[hh - K:hh]))
        if key == key0:
            returns.append(s)
            if len(returns) == 1: maxsteps = max(maxsteps, 3 * s)
    per = returns[0] if returns else None
    ok = fail is None and per is not None and all(r % per == 0 for r in returns) and len(returns) >= 3
    print('VERIFY', json.dumps(dict(lat=a.lat, K=K, t=a.t, j=a.j, par=a.par, window=win, steps=s, digits_final=len(dig),
                                    period=per, returns=len(returns), failure=fail, ok=ok)))


if __name__ == '__main__':
    main()
