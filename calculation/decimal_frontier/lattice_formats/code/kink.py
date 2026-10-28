#!/usr/bin/env python3
"""Window formulation of the centre ("kink") problem for a periodic-band exterior.
Lower half of the palindromic pair word, window of K positions below the centre.
fwd_window = exact one-step map on the window (validated against big-int reverse-and-add in test)."""
import sys, random
BASE = 10

def fwd_window(Pw, n, gam, c0, b=BASE):
    """Pw[i] = P(x), x = h-K+i, i=0..K-1, h = ceil(n/2).  c0 = carry into position h-K.
    returns (Pn, delta, Oup, Odn) where Pn[i'] valid for i'>=2 (x = h'-K+i'), delta=h'-h."""
    K = len(Pw); h = (n + 1) // 2
    cu = [0] * (K + 1); cu[0] = c0; Oup = [0] * K
    for i in range(K):
        s = Pw[i] + cu[i]
        cu[i + 1] = 1 if s >= b else 0
        Oup[i] = s - b * cu[i + 1]
    odd = n % 2 == 1
    cd = [0] * K; Odn = [0] * K
    if odd:
        Odn[K - 1] = Oup[K - 1]
        cd[K - 2] = cu[K]
        top = K - 2
    else:
        cd[K - 1] = cu[K]
        top = K - 1
    for i in range(top, -1, -1):
        if i < top:
            cd[i] = 1 if Pw[i + 1] + cd[i + 1] >= b else 0
        Odn[i] = (Pw[i] + cd[i]) % b
    n2 = n + gam; h2 = (n2 + 1) // 2; delta = h2 - h
    Pn = [None] * K
    for i2 in range(2, K):
        i = i2 + delta
        if i >= K + 1: continue
        if gam == 0:
            up = Oup[i]
            part = Oup[i] if (odd and i == K - 1) else Odn[i]
        else:
            if i <= K - 1: up = Oup[i]
            else: up = Odn[K - 1]
            part = Odn[i - 1]
        Pn[i2] = up + part
    return Pn, delta, Oup, Odn

def digits_pairs(P, b=BASE):
    M = sum(p * b ** x for x, p in enumerate(P))
    O = []
    while M:
        M, r = divmod(M, b); O.append(r)
    n2 = len(O)
    return O, [O[x] + O[n2 - 1 - x] for x in range(n2)]

def test(N=3000, seed=1):
    rng = random.Random(seed)
    bad = 0
    for it in range(N):
        n = rng.randint(30, 90)
        half = [rng.randint(0, 18) for _ in range((n + 1) // 2)]
        # leading coefficient must be >=1 (P[0]=P[n-1])
        half[0] = rng.randint(1, 18)
        P = half + half[: n // 2][::-1]
        assert len(P) == n and P == P[::-1]
        # bias to produce 9-runs sometimes
        if rng.random() < 0.3:
            for _ in range(rng.randint(1, 3)):
                a = rng.randint(1, len(half) - 1); L = rng.randint(1, 6)
                for j in range(a, min(len(half), a + L)): half[j] = 9
            P = half + half[: n // 2][::-1]
        O, Pnew = digits_pairs(P)
        gam = len(O) - n
        assert gam in (0, 1)
        K = rng.randint(6, (n + 1) // 2 - 1)
        h = (n + 1) // 2
        x0 = h - K
        # carry into x0
        c = 0
        for x in range(x0):
            c = 1 if P[x] + c >= BASE else 0
        Pw = P[x0:h]
        Pn, delta, _, _ = fwd_window(Pw, n, gam, c)
        h2 = (len(O) + 1) // 2
        for i2 in range(2, K):
            x = h2 - K + i2
            if Pn[i2] is None: continue
            if Pn[i2] != Pnew[x]:
                bad += 1
                print('MISMATCH', n, gam, K, i2, Pn[i2], Pnew[x]); break
    print('window formula tests', N, 'bad', bad)

if __name__ == '__main__':
    test(int(sys.argv[1]) if len(sys.argv) > 1 else 3000)
