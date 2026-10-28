#!/usr/bin/env python3
"""Exact integer-DP cross-check of the all-base extreme uniform-band isolation proof.

The proof in results/E2ExtremeUniformIsolation.md, rather than finite tests,
establishes the universal result. No state cap or heuristic is used here.
"""
from collections import defaultdict
import argparse


def uniform_cycles(b):
    nxt = {x: 2 * ((x + (x >= b)) % b)
           for x in range(2*b-1) if x != b-1}
    seen, cycles = set(), set()
    for seed in nxt:
        if seed in seen:
            continue
        path, pos, x = [], {}, seed
        while x in nxt and x not in seen and x not in pos:
            pos[x] = len(path)
            path.append(x)
            x = nxt[x]
        if x in pos:
            c = path[pos[x]:]
            cycles.add(min(tuple(c[k:] + c[:k]) for k in range(len(c))))
        seen.update(path)
    return sorted(cycles, key=lambda v: (len(v),v))


def predecessor_count(b, g, u):
    """Count all cyclic x_t / lower carry / previous Y trajectories entering u."""
    target_carry = int(u >= b)
    target_y = (u + target_carry) % b
    edges = []
    for gt in g:
        trans = defaultdict(list)
        for x in range(2*b-1):
            for lowcarry in (0, 1):
                if (x + lowcarry)//b != target_carry:
                    continue
                if gt and (x + target_carry)%b != target_y:
                    continue
                lower_digit = (x + lowcarry)%b
                options = range(b) if gt else ((x + target_carry)%b,)
                for partner in options:
                    x2 = lower_digit + partner
                    if x2 <= 2*b-2:
                        trans[x].append(x2)
        edges.append(trans)
    total = 0
    for x0 in range(2*b-1):
        counts = {x0: 1}
        for trans in edges:
            out = defaultdict(int)
            for x, n in counts.items():
                for x2 in trans.get(x, ()):
                    out[x2] += n
            counts = out
        total += counts.get(x0, 0)
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', type=int, default=10)
    ap.add_argument('--word', default='001001010101001010101')
    ap.add_argument('--small-controls', action='store_true')
    args = ap.parse_args()
    b = args.base
    g = tuple(map(int, args.word))
    assert b >= 2 and g and set(g) <= {0,1}
    cyc = uniform_cycles(b)
    print('uniform cycles:',cyc)
    print('time-compatible cycles:',[c for c in cyc if len(g)%len(c)==0])
    for u in (0, 2*b-2):
        n = predecessor_count(b,g,u)
        print('base',b,'p',len(g),'uniform target',u,'predecessor paths',n)
        assert n == 1
    if args.small_controls:
        tested = 0
        for b in range(2,15):
            for p in range(1,8):
                for mask in range(1<<p):
                    word = tuple((mask>>t)&1 for t in range(p))
                    assert predecessor_count(b,word,0) == 1
                    assert predecessor_count(b,word,2*b-2) == 1
                    tested += 2
        print('small-control targets tested:',tested)
        assert tested == 6604


if __name__ == '__main__':
    main()
