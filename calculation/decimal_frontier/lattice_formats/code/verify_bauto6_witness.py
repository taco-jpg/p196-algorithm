#!/usr/bin/env python3
"""Independent exact verifier for bauto6's printed root path and directed cycle.

Reads output of bauto6, derives each original carry bit from the printed
coefficient column, and checks each position-automaton transition and closure.
It does not import or execute the C++ recurrence.
"""
import argparse
import re
from itertools import product


def parse_cols(s, p):
    cols = [tuple(int(y) for y in x.split(',')) for x in re.findall(r'\[([^\[\]]+)\]', s)]
    assert all(len(x) == p for x in cols), (p, len(cols))
    return cols


def step(state, x, g, b, root):
    L, H, Y = state
    p = len(g)
    if not all(0 <= v <= 2 * b - 2 for v in x):
        return set()
    if root and 0 in x:
        return set()
    yi = {}
    k = 0
    for t, gt in enumerate(g):
        if gt:
            yi[t] = k
            k += 1
    choices = []
    for t in range(p):
        xt = x[t]
        ln = (L >> t) & 1
        hn = (H >> t) & 1
        next_x = x[(t + 1) % p]
        choices.append([c for c in (0, 1)
                        if (xt + c) // b == hn
                        and ((xt + ln) % b +
                             (Y[yi[t]] if g[t] else (xt + c) % b)) == next_x])
        if not choices[-1]:
            return set()
    LL = sum(((xt + ((L >> t) & 1)) // b) << t for t, xt in enumerate(x))
    out = set()
    for carries in product(*choices):
        HH = sum(c << t for t, c in enumerate(carries))
        YY = tuple((x[t] + carries[t]) % b for t in range(p) if g[t])
        out.add((LL, HH, YY))
    return out


def verify_line(line):
    m = re.search(r'^CYC(?:_PARTIAL)? p=(\d+) g=([01]+) S=(\d+) (?:minc|len_upper_bound)=(\d+) depth=(\d+) states=(\d+) capped=(\d+) path=(.*?) cyc=(.*)$', line.strip())
    if not m:
        raise ValueError('Expected CYC or CYC_PARTIAL record')
    p, gstr, S, length, depth, N, capped, pathstr, cycstr = m.groups()
    p, S, length, depth, N, capped = map(int, (p, S, length, depth, N, capped))
    g = tuple(map(int, gstr))
    assert len(g) == p and sum(g) == S and N > 0
    path, cyc = parse_cols(pathstr, p), parse_cols(cycstr, p)
    assert len(path) == depth and len(cyc) == length and length <= S
    b = args.base
    root = (0, sum(bit << t for t, bit in enumerate(g)), tuple(1 for _ in range(S)))
    states = {root}
    for i, col in enumerate(path):
        states = {nextstate for state in states for nextstate in step(state, col, g, b, state == root)}
        if not states:
            raise AssertionError(f'Invalid path column {i}')
    starts = states.copy()
    # Must return to one of the exact states reached by the printed root path.
    for i, col in enumerate(cyc):
        states = {nextstate for state in states for nextstate in step(state, col, g, b, state == root)}
        if not states:
            raise AssertionError(f'Invalid cycle column {i}')
    assert starts.intersection(states), 'Cycle does not close at the reached state'
    print(f'PASS base={b} p={p} path={len(path)} cycle={len(cyc)} states={N} capped={capped}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('base', type=int)
    parser.add_argument('output', help='File containing full bauto6 output')
    args = parser.parse_args()
    lines = open(args.output).read().splitlines()
    records = [s for s in lines if s.startswith(('CYC ', 'CYC_PARTIAL '))]
    assert records, 'No cycle records to verify'
    for record in records:
        verify_line(record)

