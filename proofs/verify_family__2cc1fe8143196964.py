#!/usr/bin/env python3
"""Finite controls for FAMILY_PROOF.md; they are not the all-width proof."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from verify_witness import coefficient_step, digits, high, pair_word

# Each line is prefix + [18] * (k - loss) + reversed(prefix).
PATTERNS = (
    ((17, 9), 0),
    ((8, 8, 9), 1),
    ((16, 17, 9, 17), 3),
    ((7, 15, 8, 8, 17), 4),
    ((15, 10, 17, 17, 15), 4),
    ((6, 7, 9, 16, 14, 15), 5),
    ((12, 15, 9, 13, 10, 12), 5),
)


def predicted(k: int, t: int) -> tuple[int, ...]:
    if k < 5 or not 0 <= t <= 6:
        raise ValueError("The theorem requires k>=5 and 0<=t<=6")
    prefix, loss = PATTERNS[t]
    return prefix + (18,) * (k - loss) + prefix[::-1]


def run(max_k: int = 256) -> dict:
    if not 5 <= max_k <= 2000:
        raise ValueError("Control bound must lie in 5..2000")
    digest = hashlib.sha256()
    for k in range(5, max_k + 1):
        n = 81 * 10 ** (k + 2) - 1
        q = pair_word(n)
        for t in range(7):
            assert q == predicted(k, t) == pair_word(n), (k, t)
            assert any(x % 2 for x in q), ("missing safety witness", k, t)
            assert str(n) != str(n)[::-1], ("palindrome", k, t)
            if t % 2 == 0:
                assert high(q), ("missed high return", k, t)
            digest.update((f"{k}:{t}:{n}:{','.join(map(str,q))}\n").encode())
            if t < 6:
                q_next, ds = coefficient_step(q)
                next_n = n + int(str(n)[::-1])
                assert ds == digits(next_n)
                n, q = next_n, q_next
    return {"status": "finite formula controls; see written all-width proof",
            "min_k": 5, "max_k": max_k, "families_checked": max_k - 4,
            "pair_words_checked": 7 * (max_k - 4),
            "transitions_compared": 6 * (max_k - 4),
            "trace_sha256": digest.hexdigest()}


if __name__ == "__main__":
    report = run()
    path = Path(__file__).with_name("family_controls.json")
    if path.exists():
        assert json.loads(path.read_text()) == report
    else:
        path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
