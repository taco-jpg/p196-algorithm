"""Deterministic controls and exhaustive outer-factor escape certificates.

Run: python verify.py [--max-outer 3] [--output results.json]
No third-party libraries. Capped pilot searches are retained in pilot.py.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
from quotient import (ADMISSIBLE, PHASES, State, actual_step, make_word,
                      outer_step, pair, quotient_step)


def formula_controls() -> dict:
    rng = random.Random(196)
    digest = hashlib.sha256()
    tests = 0
    for _ in range(2000):
        c = rng.choice(ADMISSIBLE)
        B = tuple(rng.randrange(19) for _ in range(rng.randrange(8)))
        if B and B[0] == 0:
            B = (1,) + B[1:]
        A = tuple(rng.randrange(19) for _ in range(rng.randrange(8)))
        half = tuple(rng.randrange(19) for _ in range(rng.randrange(5)))
        C = half + ((2 * rng.randrange(10),) if rng.randrange(2) else ()) + half[::-1]
        s = State(c, B, A, C)
        e = quotient_step(s)
        for g, h in ((2, 2), (2, 3), (3, 2), (4, 5), (8, 7)):
            q = make_word(s, g, h)
            target = make_word(e.target, g + e.delta_g, h + e.delta_h)
            assert actual_step(q) == target
            val = sum(x * 10 ** i for i, x in enumerate(q))
            digits = tuple(map(int, str(val)[::-1]))
            assert pair(digits) == target
            assert len(target) == len(q) + e.overflow
            digest.update(json.dumps([q, target], separators=(",", ":")).encode() + b"\n")
            tests += 1
    return {"tests": tests, "seed": 196, "record_sha256": digest.hexdigest(),
            "methods": ["quotient", "direct normalization", "literal decimal evaluation"]}


def outer_certificate(L: int, trimmed: bool = True) -> dict:
    """Enumerate every state, verify an exit rank, and retain a sharp path.

    A row digest pins the complete deterministic certificate, which the
    script regenerates. No rank is assumed without following the actual map.
    """
    if not 0 <= L <= 3:
        raise ValueError("Python enumeration is deliberately capped at length 3")
    blocks = [()]
    for j in range(1, L + 1):
        blocks.extend((a,) + rest for a in range(1, 19)
                      for rest in itertools.product(range(19), repeat=j - 1))
    states = [(c, B) for c in PHASES for B in blocks
              if not trimmed or not B or B[-1] != c]
    edges = {s: outer_step(*s)[:2] for s in states}
    rank: dict = {}
    for s in states:
        path, on_path = [], set()
        t = s
        while t in edges and t not in rank:
            if t in on_path:
                raise AssertionError(f"A returned outer cycle was found: {t!r}")
            on_path.add(t)
            path.append(t)
            t = edges[t]
        r = rank.get(t, 0)
        for v in reversed(path):
            r += 1
            rank[v] = r
    # Independent row-by-row rank verification, not just a search count.
    for s, t in edges.items():
        assert rank[s] == 1 + rank.get(t, 0)
        assert t in edges or len(t[1]) > L
    digest = hashlib.sha256()
    for s in states:
        row = [s[0], list(s[1]), edges[s][0], list(edges[s][1]), rank[s]]
        digest.update(json.dumps(row, separators=(",", ":")).encode() + b"\n")
    longest = max(states, key=rank.__getitem__)
    witness = []
    t = longest
    while t in edges:
        witness.append([t[0], list(t[1])])
        t = edges[t]
    witness.append([t[0], list(t[1])])
    return {"max_outer_length": L, "trimmed": trimmed, "states": len(states),
            "max_exit_time": rank[longest], "cycles": 0,
            "rank_histogram": dict(sorted(Counter(rank.values()).items())),
            "rows_sha256": digest.hexdigest(), "sharp_outer_path": witness,
            "scope": "All encoded outer states only; no restriction on A,C or gap sizes in the written factor bridge."}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--max-outer", type=int, choices=range(4), default=3)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = {"formula_controls": formula_controls(),
              "outer_certificates": [outer_certificate(L) for L in range(args.max_outer + 1)],
              "untrimmed_controls": [outer_certificate(L, False) for L in range(min(2, args.max_outer) + 1)]}
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")

if __name__ == "__main__":
    main()
