#!/usr/bin/env python3
"""Independent integer replay: build an explicit integer N_0 (base b digits) from the symmetric-lattice pair word and iterate
N -> N + rev(N) with plain digit arithmetic (no pair words); check no palindrome and the pair-word template at each step."""
import sys, json
sys.path.insert(0, '/home/claude/research/w3_formats/code')
from replay_sym import *

def rev_add(d, b):
    # d: LSB-first digit list (no leading zeros).  returns digits of d + rev(d) (LSB first)
    r = d[::-1]
    out = []; c = 0
    for x, y in zip(d, r):
        s = x + y + c
        out.append(s % b); c = s // b
    if c: out.append(c)
    return out

def split_pair(P, b):
    n = len(P)
    d = [0] * n
    for i in range(n // 2):
        lo = P[i] // 2
        d[i] = lo; d[n - 1 - i] = P[i] - lo
        assert 0 <= d[i] < b and 0 <= d[n - 1 - i] < b, (i, P[i])
    if n % 2:
        assert P[n // 2] % 2 == 0
        d[n // 2] = P[n // 2] // 2
    # leading digit must be >=1
    assert d[-1] >= 1
    return d

def run(b, fn, ri, l0_target, periods, verbose=True):
    rec = parse(fn)[ri]
    L = lattice(rec, b)
    p, nB, m, gam = L['p'], L['nB'], L['m'], L['gam']
    w0 = L['Wt'][0]
    for a in axes(w0):
        # find l0 >= l0_target, l0 = a+1 mod m, such that integer splitting is possible
        l0 = l0_target
        while (l0 % m) != (a + 1) % m: l0 += 1
        for trial in range(2 * m + 2):
            P = build_pair(L['Bt'][0], w0, l0)
            n = len(P)
            ok_split = True
            try:
                d = split_pair(P, b)
            except AssertionError:
                ok_split = False
            if ok_split: break
            l0 += m
        else:
            continue
        N = d
        l = l0
        # N_0 must not be a palindrome
        assert N != N[::-1], 'N_0 is a palindrome'
        steps = p * periods
        for t in range(steps):
            N = rev_add(N, b)                      # N_{t+1}
            if N == N[::-1]:
                print('PALINDROME N_%d' % (t + 1)); return False
            # pair word of N_{t+1} versus the template
            Pn = [N[i] + N[len(N) - 1 - i] for i in range(len(N))]
            tt = (t + 1) % p
            l += gam[t % p]
            Pe = build_pair(L['Bt'][tt], L['Wt'][tt], l)
            if Pn != Pe:
                print('TEMPLATE MISMATCH at step', t + 1); return False
        if verbose:
            print(f'base {b} rec {ri}: axis {a}, l0={l0}, n0={len(d)}: {steps} steps ({periods} periods) with plain integer reverse-and-add: no palindrome, template (B_t, lattice w_t, l_t=l_0+S_t) matches every step; final n={len(N)}')
        return dict(base=b, rec=ri, axis=a, l0=l0, n0=len(d), steps=steps, final_len=len(N), N0_digits_lsb=d)
    return False

if __name__ == '__main__':
    b = int(sys.argv[1]); fn = sys.argv[2]; ri = int(sys.argv[3]); l0 = int(sys.argv[4]); periods = int(sys.argv[5])
    r = run(b, fn, ri, l0, periods)
    print('OK' if r else 'FAIL')
