#!/usr/bin/env python3
"""Independent finite controls, not a substitute for the all-width proof.

Only standard-library integer arithmetic is used. No producer transition or
certificate code is imported. Every tested source and resulting trace is
retained in a lossless gzip JSON artifact next to this script.
"""
from itertools import product
from pathlib import Path
import gzip
import hashlib
import json

OUT = Path(__file__).resolve().parent


def digits(n, b=10):
    ds = []
    while n:
        n, d = divmod(n, b)
        ds.append(d)
    return ds


def value(ds, b=10):
    return sum(x * b ** i for i, x in enumerate(ds))


def pair(ds):
    return [a + b for a, b in zip(ds, reversed(ds))]


def normalize(q, b=10):
    carry = [0]
    ds = []
    for x in q:
        c, d = divmod(x + carry[-1], b)
        carry.append(c)
        ds.append(d)
    if carry[-1]:
        ds.append(carry[-1])
    assert ds == digits(value(q, b), b)
    return pair(ds), carry, ds


def high(q):
    return bool(q) and q[0] >= 10 and all(9 <= x <= 18 for x in q)


def realize(q):
    L = len(q)
    ds = [0] * L
    for i in range(L // 2):
        ds[i] = min(9, q[i])
        ds[L - 1 - i] = q[i] - ds[i]
    if L % 2:
        assert q[L // 2] % 2 == 0
        ds[L // 2] = q[L // 2] // 2
    assert ds[-1] > 0 and pair(ds) == q
    return value(ds)


records = {"neutral": [], "high": []}
neutral_overflow = 0
for b in range(2, 11):
    for M in range(1, 8):
        half = (M + 1) // 2
        for interior in product(range(2*b - 1), repeat=max(0, half - 1)):
            left = [b-1, *interior]
            p = left + (left[-2::-1] if M % 2 else left[::-1])
            R, c, ds = normalize(p, b)
            item = {"b": b, "p": p, "carry": c, "digits": ds, "pair": R}
            if c[-1] == 1:
                neutral_overflow += 1
                j = next(i for i, x in enumerate(p) if x != b-1)
                assert 1 <= j <= (M-1)//2
                assert p[j] >= b
                assert ds[M-j] == 0 and R[j] == p[j]-b <= b-2
                item["witness_index"] = j
            records["neutral"].append(item)

counts = {}
returns = {}
projection_cases = 0
overlap_three = 0
for L in range(1, 9):
    counts[L] = returns[L] = 0
    half = (L+1)//2
    for left_tuple in product(range(9, 19), repeat=half):
        if left_tuple[0] < 10 or (L % 2 and left_tuple[-1] % 2):
            continue
        left = list(left_tuple)
        q = left + (left[-2::-1] if L % 2 else left[::-1])
        n = realize(q)
        n1 = n + int(str(n)[::-1])
        n2 = n1 + int(str(n1)[::-1])
        P, first_c, ds1 = normalize(q)
        S, second_c, ds2 = normalize(P)
        assert P == pair(digits(n1)) and S == pair(digits(n2))
        a = q[0]-9
        expected_P = [a] + [q[i-1]+q[i]-18 for i in range(1, L)] + [a]
        assert P == expected_P and len(P) == L+1 and first_c[-1] == 1
        item = {"q": q, "realization": n, "n1": n1, "n2": n2,
                "P": P, "S": S, "second_carry": second_c, "returns": high(S)}
        counts[L] += 1
        if high(S):
            returns[L] += 1
            assert second_c[-1] == 0 and len(S) == L+1
            if L >= 3:
                M = L+1
                A, B, C = q[:3]
                x, y = A+B-18, B+C-18
                w = second_c[M-3]
                ell, v = x//10, (y+w)//10
                z = (x+v)//10
                expected = [2*a+z, x%10+(x+v)%10, (y+ell)%10+(y+w)%10]
                assert w in (0, 1) and a+z < 10 and S[:3] == expected
                if L == 3:
                    assert w == 0
                    overlap_three += 1
                item["projection"] = {"w": w, "prefix": expected}
                projection_cases += 1
            else:
                P2, _, _ = normalize(S)
                S2, _, _ = normalize(P2)
                assert not high(S2)
                item["second_two_step_pair"] = S2
        records["high"].append(item)

payload = json.dumps(records, separators=(",", ":")).encode()
compressed = gzip.compress(payload, mtime=0)
(OUT / "exact_controls.json.gz").write_bytes(compressed)
report = {
    "status": "PASS",
    "evidence_kind": "Independent finite arithmetic controls; not an all-width proof or Lean build",
    "command": "python3 proofs/contributions/agent-105/actual-high-return/review/exact_controls.py",
    "neutral_domain": "bases 2..10, every symmetric word of widths 1..7 with exterior b-1; no center-parity restriction",
    "neutral_count": len(records["neutral"]), "neutral_overflow_count": neutral_overflow,
    "high_domain": "every canonical high-region pair word of decimal widths 1..8",
    "high_counts_by_width": counts, "high_returns_by_width": returns,
    "actual_prefix_projection_count": projection_cases,
    "width_three_overlap_return_count": overlap_three,
    "raw_bytes": len(payload), "raw_sha256": hashlib.sha256(payload).hexdigest(),
    "gzip_bytes": len(compressed), "gzip_sha256": hashlib.sha256(compressed).hexdigest(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "recovery": "gzip -dc proofs/contributions/agent-105/actual-high-return/review/exact_controls.json.gz",
}
(OUT / "exact_controls_summary.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
