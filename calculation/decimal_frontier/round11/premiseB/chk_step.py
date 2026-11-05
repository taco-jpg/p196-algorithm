# Lemma S (column step) + Lemma 1 + Lemma A1, exhaustive: every column v of height H (v_0 >= 1, entries 0..2b-2).
import sys, itertools
from rmodel import *
def run(b, Hmax):
    bad = 0; n = 0; nacc = 0; nA1 = 0
    for H in range(1, Hmax + 1):
        for v in itertools.product(range(2 * b - 1), repeat=H):
            if v[0] == 0: continue
            n += 1
            B = trim(b, v); nb, e1, gm = phi(b, B)
            # A1: padding one more b-1 changes nothing
            nb2, e12, gm2 = phi(b, B + (b - 1,))
            if (nb2, e12, gm2) != (nb, e1, gm): bad += 1; print('A1 FAIL', b, B)
            nA1 += 1
            # Lemma 1 two-sweep form
            n_ = len(B); c = 0; F = []
            for i in range(n_): F.append((B[i] + c) % b); c = (B[i] + c) // b
            dd = [0] * (n_ + 1); dd[n_] = 1 - c; R = [0] * n_
            for i in range(n_ - 1, -1, -1): R[i] = (B[i] + dd[i + 1]) % b; dd[i] = (B[i] + dd[i + 1]) // b
            if n_ == 0: L = [b]
            elif dd[0] == 0: L = [F[i] + R[i] for i in range(n_)]
            else: L = [F[0] + 1] + [F[i] + R[i - 1] for i in range(1, n_)] + [(b - 1) * (1 - c) + (R[n_ - 1] if n_ else 1)]
            if (trim(b, L), c, dd[0]) != (nb, e1, gm): bad += 1; print('L1 FAIL', b, B, L, nb)
            # Lemma S: reach accepting branches of the one-step rule, both overflow bits
            got = set()
            for g in (0, 1):
                for vn, cH, dH, rH in reach_step(b, v, g):
                    if wire_ok(b, g, cH, dH, rH): got.add((g, vn, cH))
            want = {(gm, pad(b, nb, H), e1)} if len(nb) <= H else set()
            if got != want: bad += 1; print('S FAIL', b, v, got, want) if bad < 20 else None
            nacc += len(got)
    print(f'base {b}, H<=%d: {n} columns, {nacc} accepting one-step branches, A1 {nA1}, mismatches {bad}' % Hmax)
    return bad
if __name__ == '__main__':
    tot = 0
    for b, H in [(2, 10), (3, 7), (4, 6), (5, 5), (10, 4), (13, 3)]: tot += run(b, H)
    print('TOTAL MISMATCHES', tot)
