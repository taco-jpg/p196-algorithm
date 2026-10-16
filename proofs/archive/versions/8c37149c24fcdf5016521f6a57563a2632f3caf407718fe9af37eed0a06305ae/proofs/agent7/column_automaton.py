#!/usr/bin/env python3
"""Exact temporal-column automaton for periodic autonomous outer boundaries.

A completed reachability exclusion is all-width for the specified temporal
period/overflow mask, subject to the separately written column-model bridge.
A state cap gives UNKNOWN, not an exclusion. SAT paths receive literal replay.
"""
from __future__ import annotations
from collections import deque
from itertools import product
from pathlib import Path
import argparse, hashlib, json, time


def phase(c):
    if c not in range(1, 18) or c == 9:
        raise ValueError('nonneutral complementary phase required')
    return 2 * (c - 9 * int(c >= 10))


def literal_outer_step(c, B):
    # Independent literal control, also used by Agent #6's exterior audit.
    q = B + (c,) * 2 + (18-c,) * 4 + (c,) * 2 + B[::-1]
    n = 0
    for x in reversed(q):
        n = 10*n + x
    ds = tuple(map(int, str(n)[::-1]))
    raw = tuple(ds[i] + ds[-1-i] for i in range(len(B)+1))
    cp = phase(c)
    while raw and raw[-1] == cp:
        raw = raw[:-1]
    return cp, raw, len(ds)-len(q)


def transitions(state, gamma, positive=False):
    """Enumerate every allowed column, retaining its temporal coefficient word."""
    L, R, H = state
    P = len(gamma)
    out = []
    for x0 in range(1 if positive else 0, 19):
        def visit(j, x, Lnew, Rnew, Hnew, word):
            if (positive and x == 0) or not 0 <= x <= 18:
                return
            lo = (x + L[j]) % 10
            ln = (x + L[j]) // 10
            for rn in (0, 1):
                if (x + rn) // 10 != R[j]:
                    continue
                hi = (x + rn) % 10
                y = lo + (H[j] if gamma[j] else hi)
                target = (Lnew+(ln,), Rnew+(rn,), Hnew+((hi if gamma[j] else 0),))
                if j+1 == P:
                    if y == x0:
                        out.append((target, word+(x,)))
                else:
                    visit(j+1, y, *target, word+(x,))
        visit(0, x0, (), (), (), ())
    return out


def fixed_phase(c, P):
    cs = [c]
    for _ in range(P):
        cs.append(phase(cs[-1]))
    return tuple(cs[:-1]) if cs[-1] == c else None


def audit(P, gamma, c, state_cap=100000):
    cs = fixed_phase(c, P)
    if cs is None:
        raise ValueError('phase does not close')
    gamma = tuple(gamma)
    if len(gamma) != P or any(g not in (0, 1) for g in gamma):
        raise ValueError('invalid overflow mask')
    start = ((0,)*P, gamma, tuple(1 if g else 0 for g in gamma))
    ks = tuple(int(x >= 10) for x in cs)
    target = (ks, ks, tuple(x-9*k if g else 0 for x, k, g in zip(cs, ks, gamma)))
    first = transitions(start, gamma, True)
    queue, ids, parents, edges = deque(), {}, {}, []
    for s, w in first:
        if s not in ids:
            ids[s] = len(ids)
            queue.append(s)
            parents[s] = (None, w)
    reached = None
    while queue:
        s = queue.popleft()
        if s == target:
            reached = s
            break
        for t, w in transitions(s, gamma):
            edges.append((ids[s], t, w))
            if t not in ids:
                if len(ids) >= state_cap:
                    return dict(period=P, initial_phase=c, gamma=list(gamma),
                                status='UNKNOWN_STATE_CAP', states=len(ids),
                                edges=len(edges), state_cap=state_cap)
                ids[t] = len(ids)
                queue.append(t)
                parents[t] = (s, w)
    if reached is not None:
        words, s = [], reached
        while s is not None:
            s, w = parents[s]
            words.append(w)
        words.reverse()
        boundaries = []
        for j, cp in enumerate(cs):
            B = tuple(w[j] for w in words)
            while B and B[-1] == cp:
                B = B[:-1]
            boundaries.append((cp, B))
        for j, s in enumerate(boundaries):
            assert literal_outer_step(*s) == (*boundaries[(j+1) % P], gamma[j])
        return dict(period=P, initial_phase=c, gamma=list(gamma),
                    status='EXACT_OUTER_CYCLE', states=len(ids), width=len(words),
                    boundaries=[[cp, list(B)] for cp, B in boundaries])
    rows = [[list(s[0]), list(s[1]), list(s[2])] for s in ids]
    erows = [[u, ids[v], list(w)] for u, v, w in edges]
    assert all(t in ids for s in ids for t, _ in transitions(s, gamma))
    return dict(period=P, initial_phase=c, gamma=list(gamma),
                status='EXCLUDED_ALL_WIDTHS', states=len(ids), edges=len(edges),
                start=[list(x) for x in start], target=[list(x) for x in target],
                first=[[ids[s], list(w)] for s, w in first], rows=rows,
                edge_rows=erows,
                sha256_rows=hashlib.sha256(json.dumps([rows, erows], separators=(',', ':')).encode()).hexdigest())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--period', type=int, required=True)
    parser.add_argument('--phase', type=int, choices=(2, 6), required=True)
    parser.add_argument('--state-cap', type=int, default=100000)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    results = []
    for gamma in product((0, 1), repeat=args.period):
        start = time.monotonic()
        result = audit(args.period, gamma, args.phase, args.state_cap)
        result['seconds'] = round(time.monotonic()-start, 3)
        results.append(result)
        print({k: v for k, v in result.items() if k not in ('rows', 'edge_rows', 'start', 'target', 'first')}, flush=True)
        args.output.write_text(json.dumps(results, separators=(',', ':'))+'\n')
