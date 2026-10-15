#!/usr/bin/env python3
"""Exhaust all canonical high pair words of widths <=9, without prefix pruning."""
from __future__ import annotations
import hashlib
import base64
import zlib
from itertools import product
import json
from pathlib import Path
from verify_witness import coefficient_step, high, pair_word


def words(width: int):
    if width == 1:
        for c in (10, 12, 14, 16, 18):
            yield (c,)
        return
    for tail in product(range(9, 19), repeat=width//2-1):
        for outside in range(10, 19):
            half = (outside,) + tail
            centers = ((c,) for c in (10, 12, 14, 16, 18)) if width % 2 else ((),)
            for center in centers:
                yield half + center + half[::-1]


def minimum_realization(q: tuple[int, ...]) -> int:
    ds = [0] * len(q)
    for i in range(len(q)//2):
        ds[-1-i] = max(0, q[i] - 9)
        ds[i] = q[i] - ds[-1-i]
    if len(q) % 2:
        ds[len(q)//2] = q[len(q)//2] // 2
    n = sum(d * 10**i for i, d in enumerate(ds))
    assert pair_word(n) == q
    return n


def classify(q: tuple[int, ...]) -> tuple[bool, int]:
    """Safe means all six positive outputs are nonpalindromic."""
    for t in range(1, 7):
        q, ds = coefficient_step(q)
        if ds == ds[::-1]:
            return False, -t
        if t % 2 == 0 and not high(q):
            return False, t
    return True, 6


def run() -> dict:
    counts = []
    accepted = []
    audit_hash = hashlib.sha256()
    raw_codes = bytearray()
    for width in range(1, 10):
        count = 0
        hits = 0
        for q in words(width):
            count += 1
            ok, code = classify(q)
            raw_codes.append((0 if ok else code) % 256)
            audit_hash.update((f"{width}:{','.join(map(str,q))}:{ok}:{code}\n").encode())
            if ok:
                hits += 1
                n = minimum_realization(q)
                assert str(n) != str(n)[::-1]
                accepted.append({"width": width, "q": list(q), "minimum_seed": str(n)})
        expected = 5 if width == 1 else 9 * 10**(width//2-1) * (5 if width % 2 else 1)
        assert count == expected
        counts.append({"width": width, "canonical_words": count, "safe_three_return_words": hits})
    total = sum(row["canonical_words"] for row in counts)
    assert total == 59999
    vector = {"encoding": "zlib-compressed signed int8, then base64",
              "row_order": "width 1..9; words(width) order in enumerate_minimal.py",
              "codes": "0=accepted; -t=first palindrome; +t=first even-time H failure",
              "entries": len(raw_codes),
              "decoded_sha256": hashlib.sha256(raw_codes).hexdigest(),
              "data_base64": base64.b64encode(zlib.compress(raw_codes, 9)).decode()}
    vector_path = Path(__file__).with_name("minimality_outcomes.json")
    if vector_path.exists():
        assert json.loads(vector_path.read_text()) == vector
    else:
        vector_path.write_text(json.dumps(vector, indent=2) + "\n")
    minimum = min(int(row["minimum_seed"]) for row in accepted)
    assert minimum == 809999999
    return {"status": "complete finite exhaustion through width nine; not Lean-certified",
            "scope": "canonical initial Q in H; all six positive outputs safe; Q at 2,4,6 in H",
            "total_canonical_words": total, "counts": counts,
            "accepted": sorted(accepted, key=lambda r: int(r["minimum_seed"])),
            "minimum_seed": str(minimum), "classification_sha256": audit_hash.hexdigest()}


if __name__ == "__main__":
    result = run()
    path = Path(__file__).with_name("minimality_exhaustion.json")
    if path.exists():
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
