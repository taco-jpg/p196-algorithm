#!/usr/bin/env python3
"""Exact SAT/UNSAT horizon bracket for repository sat_kink.py (no false Hstart-1).
Requires python-sat/CaDiCaL only for --real searches; --selftest is stdlib-only.
"""
import argparse

class Capped(Exception):
    pass


def exact_boundary(oracle, start, cap):
    """Return (largest SAT H, first UNSAT H) under monotone feasibility.

    A SAT path for H steps restricts to a SAT path for every smaller H.
    UNKNOWN must be raised by the oracle, never translated into UNSAT.
    Return None when the cap is reached before a complete bracket.
    """
    if not (1 <= start <= cap):
        raise ValueError('require 1 <= start <= cap')
    cache = {}
    def sat(h):
        if h not in cache:
            cache[h] = oracle(h)
            if type(cache[h]) is not bool:
                raise ValueError('SAT oracle must return an exact bool, not UNKNOWN')
        return cache[h]
    if not sat(0):
        return (-1, 0)
    if sat(start):
        lo, hi = start, min(cap, 2 * start)
        while sat(hi):
            if hi == cap:
                return None
            lo, hi = hi, min(cap, 2 * hi)
    else:
        lo, hi = 0, start
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if sat(mid):
            lo = mid
        else:
            hi = mid
    return (lo, hi)


def selftest():
    for L in range(-1, 70):
        for start in range(1, 100):
            expected = (-1,0) if L < 0 else (L,L+1)
            got = exact_boundary(lambda h, L=L: h <= L, start, 200)
            assert got == expected, (L,start,got)
    for start in [1, 2, 5, 20, 63]:
        assert exact_boundary(lambda h: True, start, 64) is None
    try:
        exact_boundary(lambda h: None, 5, 64)
        raise AssertionError('UNKNOWN improperly accepted')
    except ValueError:
        pass
    print('PASS: 7029 exact boundary controls; capped/UNKNOWN controls')


def main():
    a = argparse.ArgumentParser()
    a.add_argument('lattice', nargs='?')
    a.add_argument('width', nargs='?', type=int)
    a.add_argument('phase', nargs='?', type=int)
    a.add_argument('Hstart', nargs='?', type=int)
    a.add_argument('--max-horizon', type=int, default=1024)
    a.add_argument('--selftest', action='store_true')
    args = a.parse_args()
    if args.selftest:
        selftest()
        return
    if None in (args.lattice,args.width,args.phase,args.Hstart):
        a.error('lattice width phase Hstart are required')
    # Existing independently validated exact CNF model and one-thread CaDiCaL.
    from sat_kink import load_lat, build, solve
    lat = load_lat(args.lattice)
    def oracle(h):
        enc, _layers, _K, _ns = build(lat,args.width,args.phase,'hor',h)
        result, _model, seconds = solve(enc)
        if type(result) is not bool:
            raise ValueError('solver UNKNOWN is not UNSAT')
        print(f'H={h} {"SAT" if result else "UNSAT"} seconds={seconds:.3f}', flush=True)
        return result
    result = exact_boundary(oracle,args.Hstart,args.max_horizon)
    if result is None:
        print(f'UNDECIDED: all tested horizons SAT through cap {args.max_horizon}')
    else:
        print(f'EXACT: max SAT horizon={result[0]}; first UNSAT horizon={result[1]}')

if __name__ == '__main__':
    main()
