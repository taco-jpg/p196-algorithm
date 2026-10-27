#!/usr/bin/env python3
"""Exact neutral-tail audit of Agent9.AlternatingScalarBoundary.Tile.

Run from the repository root:
    python3 calculation/agent-106/neutral_tail.py

The finite enumerations are COMPUTED.  The displayed constant spatial loop
refutes unanchored finite-depth predecessor erasure, not a root-connected
exterior or any decimal certificate.  No imports from the search programs.
"""

from collections import defaultdict, deque
from itertools import product


def valid(s):
    a, b, c, z = s
    return a in (0, 1) and b in (0, 1) and c in (0, 1) and -1 <= z <= 9


def tile(x, y, q, r, e, qnext):
    """Literal integer interpretation of every field of the Lean Tile."""
    return (
        valid(x) and valid(y)
        and 0 <= q <= 18 and 0 <= r <= 18 and e in (0, 1)
        and r == y[3] + 10 * e
        and (r >= 9 or e == 0)
        and (r <= 9 or e == 1)
        and (q + x[0]) // 10 == y[0]
        and (q + x[0]) % 10 + (q + y[2]) % 10 == r
        and (r + x[1]) // 10 == y[1]
        and x[2] == (q + y[2]) // 10
        and qnext == (r + x[1]) % 10 + x[3] + e
        and 0 <= x[3] + e <= 9
    )


def neutral(a, b):
    return a, b, 1 - a, 10 * b - 1


SLOTS = tuple(product((0, 1), (0, 1), (0, 1), range(-1, 10)))
NEUTRAL = frozenset(neutral(a, b) for a, b in product((0, 1), repeat=2))
OUTSIDE = (0, 0, 0, 0)
ROOT_8_17 = (0, 1, 1, 7)


def enumerate_tiles():
    """Enumerate bounded qnext as needed for closed temporal traces."""
    result = []
    for x, y in product(SLOTS, repeat=2):
        for q, e in product(range(19), (0, 1)):
            r = y[3] + 10 * e
            qnext = (r + x[1]) % 10 + x[3] + e
            if 0 <= qnext <= 18 and tile(x, y, q, r, e, qnext):
                result.append((x, y, q, r, e, qnext))
    return tuple(result)


def neutral_fiber_formula(x, a, b, q, r, e, qnext):
    """A separate, solved description of the neutral inner-cut fiber."""
    choices = {(9, 1 - a), (4 + 10 * a, a)}
    return (
        valid(x) and 0 <= qnext <= 18
        and x[0] == a and x[1] == b
        and (q, x[2]) in choices
        and r == 9 and e == 1 - b
        and x[3] == qnext - 10 * (1 - b)
        and 0 <= x[3] + e <= 9
    )


def check_fibers():
    tested = accepted = 0
    for a, b in product((0, 1), repeat=2):
        count = 0
        for x, q, e, qnext in product(SLOTS, range(19), (0, 1), range(19)):
            # r is forced by the inner slot and e; other r cannot be a Tile.
            r = neutral(a, b)[3] + 10 * e
            lhs = tile(x, neutral(a, b), q, r, e, qnext)
            rhs = neutral_fiber_formula(x, a, b, q, r, e, qnext)
            assert lhs == rhs, (x, a, b, q, r, e, qnext)
            count += lhs
            tested += 1
        assert count == 20
        accepted += count
    return tested, accepted


def closure(seed, edges):
    adjacency = defaultdict(set)
    for x, y in edges:
        adjacency[x].add(y)
    seen = set(seed)
    queue = deque(seed)
    while queue:
        for y in adjacency[queue.popleft()]:
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return seen


def support_predecessors(support, tiles):
    """Necessary alphabet-only preimage, with cyclic q-time consistency.

    Correlations between successive inner-slot letters are discarded.  This
    is an overapproximation, never an exterior realization procedure.
    """
    edges = [t for t in tiles if t[1] in support]
    reach = [{i} for i in range(19)]
    for _, _, q, _, _, qnext in edges:
        reach[q].add(qnext)
    for k in range(19):
        for i in range(19):
            if k in reach[i]:
                reach[i].update(reach[k])
    return {x for x, _, q, _, _, qnext in edges if q in reach[qnext]}


def main():
    tested, accepted = check_fibers()
    print(f"neutral_fibers: tested={tested} accepted={accepted} PASS")
    tiles = enumerate_tiles()
    assert len(tiles) == 1640
    constant = [t for t in tiles if t[2] == t[5]]
    assert len(constant) == 88
    print(f"bounded_tiles={len(tiles)} constant_time_tiles={len(constant)}")

    # All traces in the following two paths are constant in paired time.
    p, x, s = (0, 1, 0, 1), (0, 1, 0, 4), neutral(0, 1)
    assert tile(p, x, 7, 14, 1, 7)
    assert tile(x, s, 4, 9, 0, 4)
    assert x not in NEUTRAL
    print(f"two_predecessor_erasure_counterexample: {p} -> {x} -> {s} PASS")

    loop = (
        s, (1, 0, 0, 0), (0, 1, 1, 6), (1, 0, 1, 5),
        (1, 0, 1, 8), (1, 0, 0, 3), p, x, s,
    )
    qs = (10, 7, 12, 13, 11, 5, 7, 4)
    rs = (0, 16, 5, 8, 3, 11, 14, 9)
    es = (0, 1, 0, 0, 0, 1, 1, 0)
    for i, (q, r, e) in enumerate(zip(qs, rs, es)):
        assert tile(loop[i], loop[i + 1], q, r, e, q)
    assert loop[0] == loop[-1] and loop[-2] == x
    print("constant_spatial_loop: edges=8 PASS")
    print("loop_slots=" + repr(loop))
    print(f"loop_q={qs} loop_r={rs} loop_e={es}")
    # Repetition gives arbitrarily many spatial predecessors of x, with s
    # immediately inside.  Temporal shifts cannot change a constant trace.
    print("finite_depth_unanchored_erasure: REFUTED by loop repetition")

    edges = [(t[0], t[1]) for t in constant]
    for name, start, expected in (
        ("outside", OUTSIDE, 5), ("root_8_17", ROOT_8_17, 3),
    ):
        seen = closure([start], edges)
        assert len(seen) == expected and not (seen & NEUTRAL)
        print(f"constant_time_{name}: reachable={len(seen)} neutral=0")
    reaches_tail = closure(NEUTRAL, [(y, x) for x, y in edges])
    assert len(reaches_tail) == 32
    print(f"constant_time_tail_predecessors={len(reaches_tail)}")

    current = set(NEUTRAL)
    counts = [len(current)]
    while True:
        nxt = support_predecessors(current, tiles)
        if nxt == current:
            break
        current = nxt
        counts.append(len(current))
    assert counts == [4, 16, 80, 88] and current == set(SLOTS)
    print(f"alphabet_only_predecessor_counts={counts}; full_88_slot_fixed_point")
    print("SCOPE: no root-connected periodic strip or B/C certificate claimed")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
