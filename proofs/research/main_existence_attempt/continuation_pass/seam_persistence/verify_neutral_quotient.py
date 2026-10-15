"""Independent integer-arithmetic verification of the saved neutral graph.

Imports no search/transition implementation.  DAG rank proves the finite
claim; the symbolic block proof supplies arbitrary gap-length coverage.
"""
from __future__ import annotations

from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def value(w):
    return sum(c * 10**i for i, c in enumerate(w))


def outgoing(w, carry=0):
    return (value(w) + carry) // 10**len(w)


def is_mixed(state):
    b, h = state
    e = outgoing(b)
    return outgoing(h, e) == 1 - e


def canonical_state(s):
    b, h = s
    return bool(h) and (not b or (b[0] > 0 and b[-1] != 9)) and h[0] != 9 and h == h[::-1] and (len(h) % 2 == 0 or h[len(h) // 2] % 2 == 0) and all(0 <= c <= 18 for c in b + h)


def word(s, g):
    b, h = s
    return b + (9,) * g + h + (9,) * g + b[::-1]


def numeric_pair(w):
    d = tuple(map(int, str(value(w))[::-1]))
    return tuple(x + y for x, y in zip(d, d[::-1]))


def key(s):
    return tuple(tuple(a) for a in s)


def derive(s, gap):
    b, h = s
    q = word(s, gap)
    out = numeric_pair(q)
    gamma = len(out) - len(q)
    rb = out[:len(b) + gamma]
    rh = out[len(b) + gap:len(b) + gap + len(h) + gamma]
    assert out == rb + (9,) * (gap - gamma) + rh + (9,) * (gap - gamma) + rb[::-1]
    if all(x == 9 for x in rh):
        return {"kind": "bands_merged", "gamma": gamma, "raw_outer": rb, "raw_middle": rh}
    bn = len(rb)
    while bn and rb[bn - 1] == 9:
        bn -= 1
    hn = 0
    while rh[hn] == 9:
        hn += 1
    target = (rb[:bn], rh[hn:len(rh) - hn])
    delta = len(rb) - bn + hn - gamma
    assert canonical_state(target)
    assert numeric_pair(q) == word(target, gap + delta)
    return {"kind": "edge" if is_mixed(target) else "mixed_carry_lost",
            "gamma": gamma, "target": target, "gap_delta": delta}


def main():
    payload = gzip.decompress((HERE / "neutral_quotient_controls.json.gz").read_bytes())
    archive = json.loads(payload)
    graph = {}
    for row in archive["graph"]:
        s = key(row["state"])
        assert s not in graph and canonical_state(s) and is_mixed(s)
        expected = {k: v for k, v in row.items() if k != "state"}
        for k in ("target",):
            if k in expected:
                expected[k] = key(expected[k])
        for k in ("raw_outer", "raw_middle"):
            if k in expected:
                expected[k] = tuple(expected[k])
        for gap in (2, 5, 17):
            assert derive(s, gap) == expected
        graph[s] = expected
    roots = set()
    for width in (1, 2):
        for b in itertools.product(range(19), repeat=width):
            if b[0] == 0 or b[-1] == 9:
                continue
            for c in range(0, 19, 2):
                s = (b, (c,))
                if is_mixed(s):
                    roots.add(s)
    assert roots == {key(p["initial"]) for p in archive["paths"]}
    rank, visiting = {}, set()

    def get_rank(s):
        if s in rank:
            return rank[s]
        assert s in graph and s not in visiting, "missing target or directed cycle"
        visiting.add(s)
        row = graph[s]
        rank[s] = 1 + get_rank(row["target"]) if row["kind"] == "edge" else 1
        visiting.remove(s)
        return rank[s]

    reached = set()
    minimum_initial_gap = 2
    terminals = Counter()
    for root in roots:
        get_rank(root)
        s, delta = root, 0
        while True:
            reached.add(s)
            row = graph[s]
            delta += row.get("gap_delta", 0)
            minimum_initial_gap = max(minimum_initial_gap, 2 - delta)
            if row["kind"] != "edge":
                terminals[row["kind"]] += 1
                break
            s = row["target"]
    assert reached == set(graph)
    assert archive["cycles"] == []
    summary = {"status": "PASS: independent integer transitions, exhaustive roots/reachability, strict DAG rank",
               "source_payload_sha256": hashlib.sha256(payload).hexdigest(),
               "states": len(graph), "roots": len(roots),
               "maximum_rank": max(rank.values()),
               "rank_edges_checked": sum(r["kind"] == "edge" for r in graph.values()),
               "terminal_counts_from_roots": dict(terminals),
               "uniform_sufficient_initial_gap": minimum_initial_gap,
               "integer_gap_controls": [2, 5, 17],
               "scope": "two mixed9 bands; initial exterior width1or2 and one even middle coefficient; no ordinary-palindrome conclusion"}
    (HERE / "neutral_quotient_verification.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
