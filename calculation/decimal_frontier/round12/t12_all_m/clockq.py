#!/usr/bin/env python3
"""r12f2: exact clock-forcing threshold q_c(m) of the rooted prefix B0 W0^q (two-inlet rooted cone, the same
recurrence as seam_check.cone / seamsat.cone_rows, AC46/T12): starting from the prefix p = B0 W0^q with an
ARBITRARY continuation, at every step both possible carries entering the prefix from the right are tried; the
overflow gamma_t is forced iff both give the same gamma; the next protected prefix is the common part of both
successor rows.  q_c(m) = least q such that gamma_t is forced and equal to [t%4==0] for all t < 120m.
Also prints, per q, the first step at which the clock is no longer forced, and the protected length at t = 120m."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from seam_check import B, W, norm


def run(q, steps):
    p = list(B) + list(W) * q
    for t in range(steps):
        n = len(p)
        if n == 0:
            return t, 0
        d, _ = norm(p, 0); a0, g0 = norm(p[::-1], 0); a1, g1 = norm(p[::-1], 1)
        if g0 != g1 or g0 != (t % 4 == 0):
            return t, n
        if g0:
            l0 = [d[0] + 1] + [d[i] + a0[n - i] for i in range(1, n)]; l1 = [d[0] + 1] + [d[i] + a1[n - i] for i in range(1, n)]
        else:
            l0 = [d[i] + a0[n - 1 - i] for i in range(n)]; l1 = [d[i] + a1[n - 1 - i] for i in range(n)]
        j = next((i for i in range(n) if l0[i] != l1[i]), n); p = l0[:j]
    return None, len(p)


for m in range(1, 7):
    T = 120 * m; first = None; out = []
    for q in range(0, 12 * m + 12):
        tf, n = run(q, T)
        out.append((q, tf, n))
        if tf is None and first is None:
            first = q
    # monotonicity check
    assert all(out[i][1] is None for i in range(first, len(out))), 'not monotone'
    lost = [(q, tf) for q, tf, n in out if tf is not None]
    print(f'm={m} T={T}: q_c(m) = {first} (clock forced for all t < {T} iff q >= {first}); '
          f'protected prefix at t={T} for q=q_c: {out[first][2]}; first unforced step for q<q_c: '
          f'{[(q, tf) for q, tf in lost[-4:]]}', flush=True)
