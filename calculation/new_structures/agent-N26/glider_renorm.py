#!/usr/bin/env python3
"""Two-sector moving-frame renormalisation test for the N26 decimal p8 shield.

Independent least-significant-first digit addition.
Compare 105 frames t=88*c+4+r, r=-16..88, at pair columns j=38..38+width.
"""
import argparse
from check_digits import read_rows, initial_digits, one_step

def frames(path, cyc, copies, width):
    d = initial_digits(path, cyc, copies)
    origin = 88 * copies + 4
    snapshots = []
    for t in range(origin + 89):
        if t >= origin - 16:
            assert len(d) // 2 >= 38 + width
            snapshots.append([d[j] + d[-1 - j] for j in range(38, 38 + width)])
        d = one_step(d)
    assert len(snapshots) == 105
    return snapshots

def lcp(a, b):
    for k, (u, v) in enumerate(zip(a, b)):
        if u != v:
            return k
    return min(len(a), len(b))

def report(f0, f1):
    counts = [lcp(a, b) for a, b in zip(f0, f1)]
    return min(counts), counts[16], counts[-1], max(counts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data')
    parser.add_argument('--c', type=int, default=40)
    parser.add_argument('--width', type=int, default=300)
    args = parser.parse_args()
    assert args.c >= 10 and 1 <= args.width <= 300
    path, cyc = read_rows(args.data)
    f = {z: frames(path, cyc, z, args.width) for z in (args.c, args.c + 1, args.c + 2)}
    print('copies,delta,min_lcp,r0_lcp,r88_lcp,max_lcp')
    for delta in (1, 2):
        values = report(f[args.c], f[args.c + delta])
        print(f'{args.c},{delta},' + ','.join(map(str, values)))

if __name__ == '__main__':
    main()
