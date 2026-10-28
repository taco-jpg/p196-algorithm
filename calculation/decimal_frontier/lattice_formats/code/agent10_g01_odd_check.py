#!/usr/bin/env python3
"""Exact independent two-time position-automaton checker for the g=(0,1) parity obstruction.

No floating point, no heuristic pruning. The all-odd-base claim is proved in
reports/Agent10F2OddBaseG01.md; finite checks here are controls, not the proof.
"""
from collections import deque


def edges(b, state, first=False):
    L, H, Y = state
    l0, l1 = L & 1, (L >> 1) & 1
    h0, h1 = H & 1, (H >> 1) & 1
    for x0 in range(1 if first else 0, 2*b-1):
        for c0 in (0, 1):
            if (x0+c0)//b != h0:
                continue
            x1 = (x0+l0) % b + (x0+c0) % b
            if x1 > 2*b-2 or x0 != (x1+l1) % b + Y:
                continue
            for c1 in (0, 1):
                if (x1+c1)//b != h1:
                    continue
                L2 = (x0+l0)//b + 2*((x1+l1)//b)
                H2 = c0 + 2*c1
                Y2 = (x1+c1) % b
                yield (L2, H2, Y2)


def accept(b, state):
    L, H, Y = state
    return all(((L >> t) & 1) + ((H >> t) & 1) == 1 for t in (0, 1)) \
        and Y == (b-1)*((L >> 1)&1)


def reach(b):
    root = (0, 2, 1)
    seen = {root}
    q = deque([(root, 0)])
    found = []
    while q:
        node, d = q.popleft()
        for nxt in edges(b, node, first=(d == 0)):
            if nxt in seen:
                continue
            seen.add(nxt)
            q.append((nxt, d+1))
            if accept(b, nxt):
                found.append((nxt, d+1))
    return len(seen), found, seen


def main():
    for b in range(3, 52, 2):
        for L in (1, 2):
            for H in range(4):
                for Y in range(b):
                    for nxt in edges(b, (L,H,Y)):
                        assert nxt[0] in (1,2), (b,(L,H,Y),nxt)
    cases = 0
    for b in range(3, 302, 2):
        n, found, seen = reach(b)
        assert not found, (b, found)
        assert {L for L,H,Y in seen} <= {0,1,2}
        assert {(L,H,Y) for L,H,Y in seen if L==0} == {(0,2,1)}
        cases += 1
    n26, hits26, _ = reach(26)
    assert hits26 and hits26[0][1] == 8, hits26
    print(f"PASS: {cases} odd bases b=3..301 have no accepting state")
    print(f"PASS: all L=1/2 transition invariants, odd b=3..51")
    print(f"POSITIVE CONTROL: base 26 g=01 first ACCEPT depth {hits26[0][1]}, states {n26}")


if __name__ == '__main__':
    main()
