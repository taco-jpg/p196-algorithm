#!/usr/bin/env python3
"""r12f: numeric control of the m-epoch pumping lemma (T12Rooted120CutPumping extended to 120m steps).

For m in (2, 3): q0 = 10m+4, k0 = 90m+10, W cut cW = 52 (after two W copies), U cut cU = 34+9q+|J|+c_m with
c_m = 3*ceil((150m+2+13)/3) (m=2: 315, m=3: 465).  For every one of the 30 U words, random J, a centre C, both
insertion types, genuine big-integer trajectories x (q,k) and y (q+1,k) resp. (q,k+1) are run for 120m steps and
the full-pairword insertion identity pair(y_t) = Insert_(cut, row_t)(pair(x_t)) is checked at EVERY t = 0..120m
(rows: W_(t mod 12) resp. U_(t mod 120)); also gamma_t = [t%4==0] for both, and the cut-protection margins from the
exact fronts (cones_m.py).  Functions copied from calculation/new_structures/T12/cut.py.
"""
import sys
from pathlib import Path
from random import Random
sys.set_int_max_str_digits(10 ** 6)
s = (Path(__file__).resolve().parent / 't12ref/lat_p12m9.txt').read_text().splitlines()
a = [list(map(int, line.split())) for line in s]
W = a[2:14]; B = a[26:38]
G = lambda t: int(t % 4 == 0)
T = lambda x, c: int(x + c >= 10)


def F(w, g):
    m = len(w); lo = [0] * m; hi = [0] * m; z = 0
    for _ in range(2):
        for x in w: z = T(x, z)
    lo[0] = z
    for i in range(1, m): lo[i] = T(w[i - 1], lo[i - 1])
    z = 0
    for _ in range(2):
        for x in w[::-1]: z = T(x, z)
    hi[0] = z
    for i in range(m - 1, 0, -1): hi[i] = T(w[i], hi[(i + 1) % m])
    return tuple((w[i] + lo[i]) % 10 + ((w[i] + hi[(i + 1) % m]) % 10 if not g else (w[(i - 1) % m] + hi[i]) % 10) for i in range(m))


def phases(u):
    v = [tuple(u)]
    for t in range(120): v.append(F(v[-1], G(t)))
    return v


def make(q, k, J, U, C):
    h = B[0] + W[0] * q + list(J) + list(U) * k
    p = h + list(C) + h[::-1]; n = len(p); d = [0] * n
    assert p == p[::-1] and (n % 2 == 0 or p[n // 2] % 2 == 0)
    for i in range(n // 2): d[i] = p[i] - min(9, p[i]); d[n - 1 - i] = min(9, p[i])
    if n % 2: d[n // 2] = p[n // 2] // 2
    return int(''.join(map(str, d[::-1])))


def pair(n):
    s = str(n); return [int(x) + int(y) for x, y in zip(s[::-1], s)]


def ins(p, w, c):
    L = len(p); return p[:c] + list(w) + p[c:L - c] + list(w)[::-1] + p[L - c:]


def main():
    rnd = Random(20261108)
    for m in (2, 3):
        Tm = 120 * m; q0 = 10 * m + 4; k0 = 90 * m + 10; cm = 3 * ((150 * m + 2 + 13 + 2) // 3)
        # margins from the exact fronts: W protected prefix at q0, U cut margins
        wpro = 34 + 9 * q0 - (90 * m + 1)
        print(f'm={m}: q0={q0} k0={k0} c_m={cm}; W protected prefix at t={Tm}: {wpro} = cut 52 + {wpro-52}; '
              f'U cut margins at t={Tm}: left >= {cm-(150*m+2)}, right >= {3*k0-cm-(120*m+2)}', flush=True)
        assert wpro - 52 >= 17 and cm - (150 * m + 2) >= 13 and 3 * k0 - cm - (120 * m + 2) >= 13
        nchk = 0
        for aa in range(0, 19, 2):
            for rot in range(3):
                v = (9, aa, 18 - aa); U = v[rot:] + v[:rot]; ph = phases(U)
                assert ph[120] == tuple(U)
                J = tuple(rnd.randrange(19) for _ in range(rnd.randrange(0, 13)))
                Lc = rnd.choice([1, 2, 5, 8]); hh = [rnd.randrange(19) for _ in range((Lc + 1) // 2)]
                if Lc % 2: hh[-1] &= ~1
                C = hh + hh[::-1] if Lc % 2 == 0 else hh + hh[-2::-1]
                for typ in ('W', 'U'):
                    q, k = q0, k0
                    x = make(q, k, J, U, C); y = make(q + (typ == 'W'), k + (typ == 'U'), J, U, C)
                    c = 52 if typ == 'W' else 34 + 9 * q + len(J) + cm
                    for t in range(Tm + 1):
                        row = W[t % 12] if typ == 'W' else ph[t % 120]
                        assert pair(y) == ins(pair(x), row, c), (m, U, typ, t)
                        nchk += 1
                        if t == Tm: break
                        xx = x + int(str(x)[::-1]); yy = y + int(str(y)[::-1])
                        assert len(str(xx)) - len(str(x)) == G(t) and len(str(yy)) - len(str(y)) == G(t)
                        x, y = xx, yy
        print(f'PASS m={m}: 30 U words x 2 insertion types, insertion identity at every t=0..{Tm} ({nchk} checks), clock (1000)^{30*m}', flush=True)


if __name__ == '__main__':
    main()
