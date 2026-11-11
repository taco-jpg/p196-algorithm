#!/usr/bin/env python3
"""r12d verify_hit.py -- paranoid replay of a template-return candidate (fixed centre or wall + core).
Two independent implementations at EVERY step:
  (1) klib.pairword_step on the pairword (repo reference),
  (2) plain Python integers N -> N + int(str(N)[::-1]) (digit string reversal), pairword recomputed from str(N).
Checks: pairwords agree at every step; str(N) is never a palindrome; at every multiple of the period S the
pairword equals the template exactly; the clock (overflow) equals g at every step.  Runs >= max(20000, 3S) steps.
Writes the cycle data (pairwords of one period, overflow word, N0) as JSON for a Lean check.
usage: verify_hit.py fixed LAT q0 K C(comma)        [--steps N] [--out file.json]
       verify_hit.py wall  LAT q0 S Kb r core J(comma) h0 [--steps N] [--out file.json]"""
import sys, os, json, time, argparse
if hasattr(sys, 'set_int_max_str_digits'): sys.set_int_max_str_digits(0)
from tsat import load_lattice, steps_per_block
from tsrun import core_orbit
_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(_HERE, 'repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation'),   # Studio work dir copy
           os.path.join(_HERE, '../../lattice_kinks/edge_relaxation')):                              # repository layout
    if os.path.exists(os.path.join(_p, 'klib.py')): sys.path.insert(0, _p); break
from klib import pairword_step


def seed_from_pairword(P):
    """a decimal digit string d (LSB first) with d_i + d_(n-1-i) = P_i (the same construction as bigint2.py)"""
    n = len(P); d = [0] * n
    for i in range((n + 1) // 2):
        j = n - 1 - i
        if i == j:
            assert P[i] % 2 == 0; d[i] = P[i] // 2
        else:
            hi = min(9, P[i]); d[j] = hi; d[i] = P[i] - hi
    assert d[-1] != 0, 'leading digit zero'
    return int(''.join(map(str, d[::-1])))


def pw(N):
    s = str(N)[::-1]; n = len(s)        # LSB first
    return [int(s[i]) + int(s[n - 1 - i]) for i in range(n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('kind', choices=['fixed', 'wall'])
    ap.add_argument('args', nargs='+')
    ap.add_argument('--steps', type=int, default=20000)
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    if a.kind == 'fixed':
        latn, q0, K, C = a.args[0], int(a.args[1]), int(a.args[2]), list(map(int, a.args[3].split(',')))
        lat = load_lattice(latn); S = steps_per_block(lat, K)
        def tmpl(j):
            hh = lat.B[0] + lat.W[0] * (q0 + j * K); return hh + C + hh[::-1]
    else:
        latn, q0, S, Kb, r, core = a.args[0], int(a.args[1]), int(a.args[2]), int(a.args[3]), int(a.args[4]), int(a.args[5])
        J = list(map(int, a.args[6].split(','))); h0 = int(a.args[7])
        lat = load_lattice(latn); b = lat.b
        G = sum(lat.g[t % lat.p] for t in range(S)); dh = G - 2 * lat.m * Kb
        orb = core_orbit(core, b, S)
        assert orb[S] == core
        part = lat.W[0][:r]
        def tmpl(j):
            hh = lat.B[0] + lat.W[0] * (q0 + j * Kb)
            return hh + part + J + [core] * (h0 + j * dh) + J[::-1] + part[::-1] + hh[::-1]
    assert lat.b == 10, 'integer replay is decimal'
    steps = max(a.steps, 3 * S)
    steps = ((steps + S - 1) // S) * S
    P = tmpl(0); N = seed_from_pairword(P); assert pw(N) == P
    t0 = time.time(); bad = []; returns = []; cyc = [P]; gams = []
    for t in range(steps):
        P, gam = pairword_step(P)
        N = N + int(str(N)[::-1])
        s = str(N)
        if s == s[::-1]: bad.append(('PALINDROME', t + 1)); break
        if pw(N) != P: bad.append(('PAIRWORD_MISMATCH', t + 1)); break
        if gam != lat.g[t % lat.p]: bad.append(('CLOCK', t + 1))
        if t < S: cyc.append(P); gams.append(gam)
        if (t + 1) % S == 0:
            ok = P == tmpl((t + 1) // S); returns.append(ok)
            if not ok: bad.append(('NO_RETURN', t + 1)); break
    res = dict(kind=a.kind, args=a.args, period=S, steps=t + 1, digits_final=len(str(N)), returns=len(returns),
               all_returns=all(returns) and len(returns) == steps // S, failures=bad, seconds=round(time.time() - t0, 1))
    print('VERIFY', json.dumps(res), flush=True)
    if a.out and not bad:
        json.dump(dict(res, gam=gams, pairwords_one_period=cyc, N0=str(seed_from_pairword(tmpl(0)))), open(a.out, 'w'))
        print('WROTE', a.out)


if __name__ == '__main__':
    main()
