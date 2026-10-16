#!/usr/bin/env python3
"""Finite four-digit initial-prefix k=7 certificate cross-check, Agent #117.

Reuses byte-for-byte legacy_prefix_cycles.py (source branch research/agent-117/s20261015).
The historical generic initial_states function is THREE-digit specific; this script
correctly handles D=4 and checks every enumerated inverse edge in forward direction.
Finite computation is not a Lean proof and does not prove anything global about 196.
"""
from __future__ import annotations
from collections import Counter, defaultdict, deque
from itertools import product
import hashlib
import json
import sys
import time
import legacy_prefix_cycles as pc

K = 7
PREFIX = "2641"

def four_digit_initial(prefix: str, k: int):
    d = len(prefix)
    head = tuple(map(int, prefix))
    assert 3 <= d <= k and head[0] != 0
    long_rows = {head + tail for tail in product(range(10), repeat=k-d)}
    short_rows = set()
    for n in range(d, k):
        for half in product(range(10), repeat=(n+1)//2):
            row = half + half[:n//2][::-1]
            if row[:d] == head and (not (n % 2) or row[n//2] % 2 == 0):
                short_rows.add(row)
    return long_rows | short_rows, long_rows, short_rows

def certify(prefix=PREFIX, k=K):
    t0 = time.monotonic()
    roots, long_rows, short_rows = four_digit_initial(prefix, k)
    inverse = pc.Pred(k)
    short_inverse = pc.short_table(k)
    seen = set(roots)
    pending = list(roots)
    predecessors = {}
    outgoing = defaultdict(list)
    edges = 0
    while pending:
        p = pending.pop()
        ps = set(short_inverse.get(p, ()))
        if len(p) == k:
            ps.update(inverse.preds(p))
        predecessors[p] = ps
        edges += len(ps)
        for q in ps:
            if len(q) == k:
                assert p in pc.forward_prefixes(q), ("bad-long-edge", q, p)
            else:
                assert pc.F(q) == p, ("bad-short-edge", q, p)
            outgoing[q].append(p)
            if q not in seen:
                seen.add(q)
                pending.append(q)
        if len(seen) > 500_000:
            raise RuntimeError("CAP, not a proof: 500000 states")
    degree = {p: len(predecessors[p]) for p in seen}
    queue = deque(p for p in seen if degree[p] == 0)
    rank = {p: 0 for p in queue}
    while queue:
        q = queue.popleft()
        for p in outgoing[q]:
            degree[p] -= 1
            if degree[p] == 0:
                rank[p] = 1 + max(rank[x] for x in predecessors[p])
                queue.append(p)
    if len(rank) != len(seen):
        return {"status": "UNRANKED", "states": len(seen), "ranked": len(rank)}
    for p, ps in predecessors.items():
        assert rank[p] == (1 + max(rank[q] for q in ps) if ps else 0)
    h = hashlib.sha256()
    for row in sorted(seen):
        h.update(",".join(map(str,row)).encode("ascii"))
        h.update(b":")
        h.update(str(rank[row]).encode("ascii"))
        h.update(b"\n")
    max_init = max(rank[p] for p in roots)
    return {
        "status": "ACYCLIC", "evidence_label": "checked finite computation; not Lean",
        "k": k, "prefix": prefix,
        "initial_long": len(long_rows), "initial_short": len(short_rows),
        "source_shorts": sum(len(s) for s in short_inverse.values()),
        "closure_total": len(seen), "closure_long": sum(len(p)==k for p in seen),
        "closure_short": sum(len(p)<k for p in seen),
        "all_predecessor_edges": edges,
        "max_initial_rank": max_init, "method_bound": max_init+1,
        "rank_distribution": {str(r): c for r,c in sorted(Counter(rank.values()).items())},
        "sorted_rank_rows_sha256": h.hexdigest(),
        "runtime_seconds": round(time.monotonic()-t0,3)
    }

if __name__ == "__main__":
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    sys.exit(0 if result.get("status") == "ACYCLIC" else 1)
