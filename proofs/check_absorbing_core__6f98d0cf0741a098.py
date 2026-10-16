"""Independent ordinary-integer audit of exact 0/18 run ancestry."""
from __future__ import annotations

import gzip
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def words():
    for width in range(1, 8):
        if width == 1:
            yield from ((2 * k,) for k in range(1, 10))
            continue
        for first in range(1, 19):
            for suffix in itertools.product(range(19), repeat=width // 2 - 1):
                left = (first,) + suffix
                for middle in (range(0, 19, 2) if width % 2 else (None,)):
                    yield left + (() if middle is None else (middle,)) + left[::-1]


def value(q):
    return sum(v * 10**i for i, v in enumerate(q))


def step(q):
    d = tuple(map(int, str(value(q))[::-1]))
    return tuple(a + b for a, b in zip(d, d[::-1]))


def incoming(q, i):
    return value(q[:i]) // 10**i


def runs(q, c):
    i = 0
    while i < len(q):
        if q[i] != c:
            i += 1
            continue
        start = i
        while i < len(q) and q[i] == c:
            i += 1
        yield start, i


def main():
    records, families = [], []
    counts = {"canonical_words": 0, "zero_runs": 0, "eighteen_runs": 0,
              "overflow_run_controls": 0, "nonempty_descendants": 0,
              "no_overflow_birth_columns": 0}
    for q in words():
        counts["canonical_words"] += 1
        out = step(q)
        gamma = len(out) - len(q)
        if not gamma:
            for i, x in enumerate(q):
                s = incoming(q, i) + incoming(q[::-1], len(q) - 1 - i)
                assert (out[i] == 18) == ((x in (8, 18) and s == 2) or (x == 9 and s == 0))
                assert (out[i] == 0) == ((x in (0, 10) and s == 0) or (x == 9 and s == 2))
                counts["no_overflow_birth_columns"] += 1
        for c in (0, 18):
            for a, b in runs(q, c):
                ell, h = b - a, c // 18
                alpha = incoming(q, a)
                beta = incoming(q[::-1], len(q) - b)
                counts["zero_runs" if c == 0 else "eighteen_runs"] += 1
                counts["overflow_run_controls"] += gamma
                if gamma:
                    aa, bb = a + 1, b
                    assert out[a] != c and out[b] != c
                elif ell == 1:
                    expected = alpha + beta if c == 0 else 16 + alpha + beta
                    assert out[a] == expected
                    aa, bb = (a, b) if alpha == beta == h else (a, a)
                else:
                    aa, bb = a + (alpha != h), b - (beta != h)
                    assert out[a] == (alpha if c == 0 else 17 + alpha)
                    assert out[b - 1] == (beta if c == 0 else 17 + beta)
                assert bb >= aa and bb - aa <= ell - gamma
                assert all(x == c for x in out[aa:bb])
                if bb > aa:
                    counts["nonempty_descendants"] += 1
                    assert aa == 0 or out[aa - 1] != c
                    assert bb == len(out) or out[bb] != c
                    assert (aa, bb) in tuple(runs(out, c))
                records.append({"q": q, "gamma": gamma, "coefficient": c,
                                "run": [a, b], "exterior_carries": [alpha, beta],
                                "descendant": [aa, bb], "next_pair": out})
    for g in (2, 3, 4, 8, 31, 100):
        q = (1, 10, 8) + (18,) * g + (8, 10, 1)
        expected = (3, 0, 18, 17) + (18,) * (g - 2) + (17, 18, 0, 3)
        assert step(q) == expected
        assert q.count(18) == expected.count(18) == g
        families.append({"g": g, "q": q, "next_pair": expected})
    payload = json.dumps({"run_controls": records, "birth_family_controls": families},
                         sort_keys=True, separators=(",", ":")).encode()
    archive = HERE / "absorbing_core_controls.json.gz"
    archive.write_bytes(gzip.compress(payload, mtime=0))
    summary = {"status": "PASS; all-width theorem is separate; no global persistence or palindrome claim",
               "counts": counts, "run_records": len(records), "birth_family_records": len(families),
               "archive": archive.name, "payload_sha256": hashlib.sha256(payload).hexdigest()}
    (HERE / "absorbing_core_results.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
