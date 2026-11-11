#!/usr/bin/env python3
"""r12f: exact carry-difference cone radii of T12 over 120m steps (m = 1..4), forced clock check.

Same recurrences as calculation/new_structures/T12/cut.py (T12MinimalCarryCone), summed over 120m transitions:
  W (rooted prefix, seam-facing edge): m_(t+1) = m_t - (1 + r_t - gamma_t), r_t = run of 9s ending at the edge.
  U junction side (left edge of a pure band):  l_(t+1) = l_t + 1 + [V_t[l_t mod 3] = 9]
  U centre side (right edge of a pure band):   r_(t+1) = r_t + 1 + [V_t[(-r_t-1) mod 3] = 9] - gamma_t
with V_t = U phase rows (120-periodic), W rows 12-periodic, gamma_t = [t = 0 mod 4].
Also: forced clock (1000)^(30m) on the exact rooted prefix B0 W0^q (seamsat.cone_rows, two inlets agree).
"""
import sys
from pathlib import Path
from itertools import product
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seamsat import cone_rows

s = (Path(__file__).resolve().parent / 't12ref/lat_p12m9.txt').read_text().splitlines()
a = [list(map(int, line.split())) for line in s]
assert a[0] == [12, 34, 9, 10] and a[1] == [1, 0, 0, 0] * 3
W = a[2:14]; Brows = a[26:38]
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


def phases(u, T_=120):
    v = [tuple(u)]
    for t in range(T_): v.append(F(v[-1], G(t)))
    return v


def us():
    return [tuple((9, x, 18 - x)[r:] + (9, x, 18 - x)[:r]) for x in range(0, 19, 2) for r in range(3)]


def w_retreat(steps, q=14):
    m = 34 + 9 * q; s0 = m; hist = {}
    for t in range(steps):
        r = 0
        while W[t % 12][(m - 35 - r) % 9] == 9: r += 1
        d = 1 + r - G(t); hist[d] = hist.get(d, 0) + 1
        m -= d
    return s0 - m, hist


def u_cones(U, steps):
    v = phases(U)
    assert v[120] == tuple(U)
    l = r = 0; L = []; Rr = []
    for t in range(steps):
        w = v[t % 120]
        l += 1 + int(w[l % 3] == 9); r += 1 + int(w[(-r - 1) % 3] == 9) - G(t)
        L.append(l); Rr.append(r)
    return l, r, L, Rr


if __name__ == '__main__':
    assert all(tuple(W[(t + 1) % 12]) == F(tuple(W[t]), G(t)) for t in range(12))
    for m in (1, 2, 3, 4):
        T_ = 120 * m
        rw, hist = w_retreat(T_)
        # check independence of q (only m mod 9 matters; q enters through 34+9q)
        assert all(w_retreat(T_, q)[0] == rw for q in (14, 20, 33, 50))
        per_epoch = [w_retreat(120 * (e + 1))[0] - w_retreat(120 * e)[0] if e else w_retreat(120)[0] for e in range(m)]
        print(f'm={m} steps={T_}: W retreat {rw} (per epoch {per_epoch}) step histogram {sorted(hist.items())}')
        tab = {}
        for i, U in enumerate(us()):
            l, r, L, Rr = u_cones(U, T_)
            tab.setdefault((l, r), []).append(i)
        for (l, r), ids in sorted(tab.items()):
            print(f'   U cone (junction side {l}, centre side {r}): {len(ids)} words, U indices {ids}')
        lmax = max(k[0] for k in tab); rmax = max(k[1] for k in tab)
        print(f'   => max junction-side {lmax}, max centre-side {rmax}, sum {lmax + rmax}')
    # forced clock (1000)^(30m) on the exact rooted prefix, two inlets agree (cone_rows asserts g0==g1==(t%4==0))
    for m in (1, 2, 3):
        T_ = 120 * m
        rw, _ = w_retreat(T_)
        q = (rw + 34 + 9 + 8) // 9 + 2
        rows = cone_rows(list(Brows[0]) + list(W[0]) * q, steps=T_)
        ok = all(rows[t][:34] == Brows[t % 12] for t in range(T_ + 1))
        print(f'clock m={m}: prefix B0 W0^{q}, {T_} steps, clock (1000)^{30*m} forced (both inlets), '
              f'B_t rows == published B rows: {ok}; protected prefix length at t={T_}: {len(rows[T_])} (= 34+9q-{34+9*q-len(rows[T_])})')
        assert ok
