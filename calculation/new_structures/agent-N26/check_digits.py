#!/usr/bin/env python3
"""Independent least-significant-first digit-list replay; no GMP or pairword stepping."""
import argparse
import re

def read_rows(path):
    lines = open(path, encoding='ascii').read().splitlines()
    rows = [[list(map(int, m.split(','))) for m in re.findall(r'\[([^\]]+)\]', line)] for line in lines]
    assert len(rows[0]) == 39 and len(rows[1]) == 20
    assert all(len(row) == 8 and all(0 <= x <= 18 for x in row) for part in rows for row in part)
    return rows

def initial_digits(path, cyc, copies):
    half = [r[0] for r in path] + [r[0] for r in cyc] * copies
    low = [min(z, 9) for z in half]
    high = [z - min(z, 9) for z in half]
    d = low + high[::-1]
    assert d[-1] > 0
    return d

def one_step(d):
    c, out = 0, []
    for x, y in zip(d, reversed(d)):
        z = x + y + c
        out.append(z % 10)
        c = z // 10
    if c:
        out.append(c)
    assert out[-1] > 0
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('data')
    ap.add_argument('--copies', type=int, default=10)
    ap.add_argument('--steps', type=int, default=700)
    ap.add_argument('--watch', type=int, default=39)
    args = ap.parse_args()
    path, cyc = read_rows(args.data)
    d = initial_digits(path, cyc, args.copies)
    start = len(d)
    for t in range(args.steps + 1):
        if d == d[::-1]:
            raise AssertionError(f'palindrome at {t}')
        for i in range(args.watch):
            actual = d[i] + d[-1-i]
            expect = path[i][t % 8]
            if actual != expect:
                raise AssertionError(f'bulk first mismatch t={t} col={i} actual={actual} expected={expect}')
        if t < args.steps:
            n = len(d)
            d = one_step(d)
            assert len(d) == n + (1 if t % 2 == 0 else 0), t
    print(f'PASS independent digit-list steps={args.steps} copies={args.copies} watch={args.watch} seed_digits={start} final_digits={len(d)}')

if __name__ == '__main__':
    main()
