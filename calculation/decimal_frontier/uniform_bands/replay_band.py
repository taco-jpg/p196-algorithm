#!/usr/bin/env python3
"""Genuine big-integer replay of a 'left end + uniform band + mirror' candidate printed by reach (LEFTEND block).

Builds the number whose lower-half pair word at t=0 is  leftend[x][0] (x < H)  followed by L band cells, for several
band lengths L and both parities of the length n, then runs real reverse-and-add in base B and checks at EVERY step:
  (1) overflow exactly on the clock: len(N_{t+1}) - len(N_t) == clock[t mod T]
  (2) pair word P_x = d_x + d_{n-1-x}: P_x(t) = leftend[x][t mod T] for x < H, and P_x(t) = band value at (t+PH) mod q
      for H <= x < ceil(n/2)  (the band is its own mirror, so this is the whole number)
  (3) N_t is not a palindrome.
Exit code 0 iff every (L, parity) passes.  usage: replay_band.py FIT_LOG [--periods 20] [--lengths 1,2,3,5,8,13,40]
"""
import argparse, re, sys

def parse(path):
    lines = open(path).read().splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith('LEFTEND '))
    hdr = dict(kv.split('=', 1) for kv in lines[i].split()[1:])
    cells = []
    for l in lines[i + 1:]:
        if l.startswith('END LEFTEND'):
            break
        m = re.match(r'cell (\d+):(.*)', l)
        cells.append([int(v) for v in m.group(2).split()])
    B, T = int(hdr['B']), int(hdr['T'])
    clock = [int(hdr['clock'][t % len(hdr['clock'])]) for t in range(T)]
    band = [(int(it.split(':')[0]), int(it.split(':')[1])) for it in hdr['band'].split(',')]
    vals = [r + (B - 1) * c for c, r in band]
    assert len(cells) == int(hdr['H']) and all(len(c) == T for c in cells)
    return B, T, clock, vals, int(hdr['PH']), cells

def build(B, P, n):
    """digits (little-endian) of a length-n number with lower-half pair word P (len ceil(n/2))."""
    d = [0] * n
    for x, p in enumerate(P):
        m = n - 1 - x
        if x == m:
            assert p % 2 == 0, 'odd centre value'
            d[x] = p // 2
        elif x == 0:
            hi = max(1, p - (B - 1)); lo = p - hi
            assert 0 <= lo < B and 1 <= hi < B, 'leading digit'
            d[0], d[m] = lo, hi
        else:
            lo = min(p, B - 1); hi = p - lo
            d[x], d[m] = lo, hi
    return d

def step(B, d):
    n = len(d); out = []; c = 0
    for i in range(n):
        s = d[i] + d[n - 1 - i] + c
        out.append(s % B); c = s // B
    if c:
        out.append(c)
    return out

def pairs(d):
    n = len(d)
    return [d[x] + d[n - 1 - x] for x in range((n + 1) // 2)]

def check(B, T, clock, vals, PH, cells, L, odd, periods):
    H, q = len(cells), len(vals)
    P = [cells[x][0] for x in range(H)] + [vals[PH % q]] * L
    h = len(P); n = 2 * h - 1 if odd else 2 * h
    d = build(B, P, n)
    for t in range(periods * T):
        pw = pairs(d)
        for x, p in enumerate(pw):
            want = cells[x][t % T] if x < H else vals[(t + PH) % q]
            if p != want:
                return f'pair word mismatch at t={t} x={x}: {p} != {want}'
        if d == d[::-1]:
            return f'palindrome at t={t}'
        nd = step(B, d)
        if len(nd) - len(d) != clock[t % T]:
            return f'overflow mismatch at t={t}'
        d = nd
    return 'ok'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fit'); ap.add_argument('--periods', type=int, default=20)
    ap.add_argument('--lengths', default='1,2,3,5,8,13,40')
    a = ap.parse_args()
    B, T, clock, vals, PH, cells = parse(a.fit)
    print(f'replay: base {B}, period {T}, clock {"".join(map(str, clock))}, band values {vals}, phase {PH}, left end H={len(cells)}')
    allok = True
    for L in map(int, a.lengths.split(',')):
        for odd in (False, True):
            r = check(B, T, clock, vals, PH, cells, L, odd, a.periods)
            allok &= (r == 'ok')
            print(f'  band cells L={L:3d} n {"odd " if odd else "even"}: {r}')
    print('REPLAY', 'PASS' if allok else 'FAIL', f'({a.periods} periods = {a.periods * T} steps each)')
    sys.exit(0 if allok else 1)

if __name__ == '__main__':
    main()
