#!/usr/bin/env python3
"""Exact temporal-language predecessors of the decimal N/O neutral tail.

Research computation only. Slot/Tile semantics are transcribed independently
from P196/Core/AlternatingScalarBoundary.lean. Actual exterior conclusions need
the separate bridge. A finite depth cannot be extrapolated to arbitrary width.
The optional compact backend requires NumPy and SciPy.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from itertools import product

SLOTS = list(product(range(2), range(2), range(2), range(-1, 10)))
INDEX = {s: i for i, s in enumerate(SLOTS)}
NEUTRAL = {INDEX[(a, b, 1-a, 10*b-1)] for a, b in product(range(2), repeat=2)}
OUTSIDE = INDEX[(0, 0, 0, 0)]


def tile(o, i, q, r, e, qn):
    """Literal integer Tile predicate, with qn bounded for cyclic traces."""
    a, b, c, z = o
    aa, bb, cc, zz = i
    return (o in INDEX and i in INDEX and 0 <= q <= 18 and 0 <= qn <= 18 and 0 <= r <= 18
            and e in (0, 1) and r == zz + 10*e
            and (r >= 9 or e == 0) and (r <= 9 or e == 1)
            and (q+a)//10 == aa and (q+a)%10 + (q+cc)%10 == r
            and (r+b)//10 == bb and c == (q+cc)//10
            and qn == (r+b)%10 + z + e and 0 <= z+e <= 9)


def tiles():
    """Enumerate exact local transitions (inner, q) -> (outer, qNext)."""
    out = defaultdict(set)
    for oi, o in enumerate(SLOTS):
        a, b, c, z = o
        for q, cc, e in product(range(19), range(2), range(2)):
            aa = (q+a)//10
            r = (q+a)%10 + (q+cc)%10
            bb = (r+b)//10
            zz = r - 10*e
            i = (aa, bb, cc, zz)
            qn = (r+b)%10 + z + e
            if i in INDEX and tile(o, i, q, r, e, qn):
                out[(INDEX[i], q)].add((oi, qn))
    return {k: sorted(v) for k, v in out.items()}


TILES = tiles()


def cyclic_core(n, edges):
    """Keep precisely edges lying in directed cycles (iterative Kosaraju)."""
    adj = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]
    for s, _, t in edges:
        adj[s].append(t)
        rev[t].append(s)
    seen = bytearray(n)
    order = []
    for root in range(n):
        if seen[root]:
            continue
        seen[root] = 1
        stack = [(root, 0)]
        while stack:
            u, j = stack[-1]
            if j == len(adj[u]):
                order.append(u)
                stack.pop()
            else:
                v = adj[u][j]
                stack[-1] = (u, j+1)
                if not seen[v]:
                    seen[v] = 1
                    stack.append((v, 0))
    comp = [-1]*n
    nc = 0
    for root in reversed(order):
        if comp[root] != -1:
            continue
        comp[root] = nc
        stack = [root]
        while stack:
            u = stack.pop()
            for v in rev[u]:
                if comp[v] == -1:
                    comp[v] = nc
                    stack.append(v)
        nc += 1
    kept = {(s, a, t) for s, a, t in edges if comp[s] == comp[t]}
    used = sorted({v for s, _, t in kept for v in (s, t)})
    ids = {v: j for j, v in enumerate(used)}
    return len(used), sorted((ids[s], a, ids[t]) for s, a, t in kept)


def predecessor(n, edges, state_cap=1_000_000):
    """Exact transducer product; accepted words are labels of closed walks."""
    if 19*n > state_cap:
        raise RuntimeError(f"state cap: {19*n}>{state_cap}")
    raw = set()
    for s, inner, t in edges:
        for q in range(19):
            for outer, qn in TILES.get((inner, q), ()):
                raw.add((19*s+q, outer, 19*t+qn))
    return cyclic_core(19*n, raw)


def predecessor_compact(n, edges, state_cap=2_000_000):
    """Same exact product, using packed uint64 edges and SciPy SCCs."""
    import array
    import numpy as np
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import connected_components
    m = 19*n
    if m > state_cap:
        raise RuntimeError(f"state cap: {m}>{state_cap}")
    if m >= 2**31 or m*m*88 >= 2**64:
        raise RuntimeError("packed-edge capacity")
    by_inner = defaultdict(list)
    for (inner, q), opts in TILES.items():
        by_inner[inner].extend((q, outer, qn) for outer, qn in opts)
    raw = array.array('Q')
    for s, inner, t in edges:
        for q, outer, qn in by_inner[inner]:
            raw.append(((19*s+q)*88+outer)*m+(19*t+qn))
    packed = np.unique(np.frombuffer(raw, dtype=np.uint64))
    del raw
    src = (packed//(m*88)).astype(np.int32)
    dst = (packed % m).astype(np.int32)
    adj = csr_matrix((np.ones(len(packed), dtype=np.int16), (src, dst)), shape=(m,m))
    _, comp = connected_components(adj, directed=True, connection='strong')
    del adj
    keep = comp[src] == comp[dst]
    packed = packed[keep]
    src, dst = src[keep], dst[keep]
    used = np.union1d(src, dst)
    src = np.searchsorted(used, src).astype(np.int32)
    dst = np.searchsorted(used, dst).astype(np.int32)
    lab = ((packed//m) % 88).astype(np.int16)
    rows = [(int(s),int(a),int(t)) for s,a,t in zip(src,lab,dst)]
    return len(used), rows


def bisimulation(n, edges):
    """Merge equal finite labelled continuations, preserving path languages.

    In a cyclic graph this preserves arbitrary-period periodic traces, allowing
    a hidden-state period multiple. It need not preserve a specified period.
    """
    adj = [[] for _ in range(n)]
    for s, a, t in edges:
        adj[s].append((a, t))
    cls = [0]*n
    while True:
        sigs = {}
        nxt = []
        for u in range(n):
            sig = tuple(sorted({(a, cls[v]) for a, v in adj[u]}))
            if sig not in sigs:
                sigs[sig] = len(sigs)
            nxt.append(sigs[sig])
        if nxt == cls:
            break
        cls = nxt
    merged = {(cls[s], a, cls[t]) for s, a, t in edges}
    return len(set(cls)), sorted(merged)


def uniform_cycle(n, edges, letter):
    nn, ee = cyclic_core(n, [(s, a, t) for s, a, t in edges if a == letter])
    return nn > 0


def inspect(depth, cap, flip=False, compact=False):
    import time
    import resource
    started = time.monotonic()
    if flip:
        n = 2
        edges = [(a, INDEX[(a, 1-aa, 1-a, 9-10*aa)], aa)
                 for a, aa in product(range(2), repeat=2)]
    else:
        n = 1
        edges = [(0, a, 0) for a in sorted(NEUTRAL)]
    print(f"slots={len(SLOTS)} tile_transitions={sum(map(len,TILES.values()))}", flush=True)
    for d in range(depth+1):
        alphabet = sorted({a for _, a, _ in edges})
        print(f"depth={d} states={n} edges={len(edges)} letters={len(alphabet)} "
              f"outside_periodic={uniform_cycle(n,edges,OUTSIDE)}", flush=True)
        if d <= 2:
            print(" alphabet", [SLOTS[a] for a in alphabet], flush=True)
        if d != depth:
            n, edges = (predecessor_compact if compact else predecessor)(n, edges, cap)
            n, edges = bisimulation(n, edges)
    print(f"completed_depth={depth} seconds={time.monotonic()-started:.3f} "
          f"maxrss_kib={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}", flush=True)


def selftest():
    independent = defaultdict(set)
    for oi, o in enumerate(SLOTS):
        for ii, i in enumerate(SLOTS):
            for q, e in product(range(19), range(2)):
                r = i[3]+10*e
                qn = (r+o[1])%10+o[3]+e
                if tile(o, i, q, r, e, qn):
                    independent[(ii,q)].add((oi,qn))
    if {k: set(v) for k,v in TILES.items()} != dict(independent):
        raise AssertionError("tile enumeration mismatch")
    n, edges = 1, [(0,a,0) for a in sorted(NEUTRAL)]
    from alternating_tiles import NEUTRAL_SPATIAL_CYCLE
    for depth in range(5):
        n1,e1 = predecessor(n,edges)
        n2,e2 = predecessor_compact(n,edges)
        if (n1,e1) != (n2,e2):
            raise AssertionError(f"compact/SCC mismatch at depth {depth+1}")
        n,edges=bisimulation(n1,e1)
        label = INDEX[NEUTRAL_SPATIAL_CYCLE[-1-depth]]
        if not uniform_cycle(n,edges,label):
            raise AssertionError(f"known positive spatial trace lost at depth {depth+1}")
    print("SELFTEST exact_tile_enumeration=1640 compact_standard_depths=5 "
          "known_positive_trace_depths=5 PASS")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--depth", type=int, default=5)
    p.add_argument("--cap", type=int, default=1_000_000)
    p.add_argument("--flip", action="store_true")
    p.add_argument("--compact", action="store_true")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.depth < 0 or a.cap < 1:
        p.error("depth must be nonnegative and cap positive")
    if a.selftest:
        selftest()
    else:
        inspect(a.depth, a.cap, a.flip, a.compact)


if __name__ == "__main__":
    try:
        main()
    except (MemoryError, RuntimeError) as error:
        print(f"UNDECIDED: {error}", file=sys.stderr, flush=True)
        raise SystemExit(2)
