#!/usr/bin/env python3
"""Replay Agent #117's concrete five-edge abstract inverse path for prefix 2641.

Independent of Python's graph-search order. Validates each edge by the
forward carry equations and by the preserved complete predecessor generator.
This is a FINITE COMPUTATION witness, not an accepted Lean theorem or a
single ordinary-integer reverse-add trajectory.
"""
import json
from pathlib import Path
from legacy_prefix_cycles import Pred, forward_prefixes

HERE = Path(__file__).resolve().parent

def forward_with_carry(s, e):
    low = []
    carry = 0
    for a in s:
        carry, v = divmod(a + carry, 10)
        low.append(v)
    high = [0] * len(s)
    carry = e
    for i in range(len(s)-1, -1, -1):
        carry, high[i] = divmod(s[i] + carry, 10)
    if carry:
        return (low[0] + 1,) + tuple(
            low[i] + high[i-1] for i in range(1, len(s)))
    return tuple(a+b for a,b in zip(low,high))

def main():
    proof = json.loads((HERE / "rank5_witness.json").read_text())
    rows = [tuple(a) for a in proof["path_states"]]
    rank_lookup = {}
    for line in (HERE / "rank_rows_k7_2641.tsv").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        word, rank = line.split("\t")
        rank_lookup[tuple(int(x) for x in word.split(","))] = int(rank)
    pred = Pred(7)
    assert len(rows) == 6 and rows[0][:4] == (2, 6, 4, 1)
    assert [rank_lookup[w] for w in rows] == list(range(5,-1,-1))
    for p, q, e in zip(rows, rows[1:], proof["boundary_carries"]):
        assert q in pred.preds(p), ("missing inverse",p,q)
        assert p in forward_prefixes(q), ("bad candidate",p,q)
        assert forward_with_carry(q,e) == p, ("bad carry",p,q,e)
    print(json.dumps({"finite_status": "PASS",
        "path_edges":len(rows)-1,"initial_rank":rank_lookup[rows[0]],
        "claim":"sharp method lower bound for this abstract graph, NOT actual 196",
        "lean_status":"NOT_RUN"},sort_keys=True))

if __name__ == "__main__":
    main()
