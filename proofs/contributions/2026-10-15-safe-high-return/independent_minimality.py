#!/usr/bin/env python3
"""Replay every stored outcome via integer arithmetic and a different enumeration.

Does not import the producer or its carry-normalization implementation.
The full signed outcome vector identifies all 59,999 generated words.
"""
from __future__ import annotations
import base64
import hashlib
import json
from pathlib import Path
import zlib

ROOT = Path(__file__).resolve().parent


def pair(n: int) -> tuple[int, ...]:
    # Most-significant order equals least-significant order for the pair word.
    s = str(n)
    return tuple(int(s[i]) + int(s[-1-i]) for i in range(len(s)))


def smallest(q: tuple[int, ...]) -> int:
    # Greedily minimize most-significant digits, not the producer's arithmetic sum.
    ds = ["0"] * len(q)
    for i in range(len(q)//2):
        top = max(0, q[i] - 9)
        ds[i], ds[-1-i] = str(top), str(q[i] - top)
    if len(q) % 2:
        ds[len(q)//2] = str(q[len(q)//2]//2)
    n = int("".join(ds))
    assert len(str(n)) == len(q) and pair(n) == q
    return n


def outcome(n: int) -> int:
    for t in range(1, 7):
        n += int(str(n)[::-1])
        s = str(n)
        if s == s[::-1]:
            return -t
        if t % 2 == 0:
            q = pair(n)
            if q[0] < 10 or any(c < 9 or c > 18 for c in q):
                return t
    return 0


def run() -> dict:
    vector = json.loads((ROOT / "minimality_outcomes.json").read_text())
    raw = zlib.decompress(base64.b64decode(vector["data_base64"]))
    assert len(raw) == vector["entries"] == 59999
    assert hashlib.sha256(raw).hexdigest() == vector["decoded_sha256"]
    checked = bytearray(len(raw))
    offset = 0
    accepted = []
    for width in range(1, 10):
        half_len = width//2
        if width == 1:
            candidates = [(i, (2*d,)) for i, d in enumerate(range(5, 10))]
        else:
            candidates = []
            # Numeric half encoding orders the exterior before the tail;
            # the producer orders the tail before the exterior.
            for half_code in range(10**(half_len-1), 10**half_len):
                chars = str(half_code)
                half = tuple(9 + int(c) for c in chars)
                tail_index = int(chars[1:] or "0")
                outside_index = int(chars[0]) - 1
                centers = [(2*d,) for d in range(5, 10)] if width % 2 else [()]
                for center_index, center in enumerate(centers):
                    index = (tail_index*9 + outside_index)*len(centers) + center_index
                    candidates.append((index, half + center + half[::-1]))
        for index, q in candidates:
            address = offset + index
            assert not checked[address]
            checked[address] = 1
            n = smallest(q)
            result = outcome(n)
            expected = raw[address] if raw[address] < 128 else raw[address] - 256
            assert result == expected, (width, q, result, expected)
            if result == 0:
                accepted.append({"q": list(q), "minimum_seed": str(n)})
        offset += len(candidates)
    assert offset == 59999 and all(checked)
    assert accepted == [{"q": [17,9,18,18,18,18,18,9,17], "minimum_seed": "809999999"}]
    return {"status": "independent literal-integer replay passed",
            "checked_words": offset, "accepted": accepted,
            "complete_outcome_sha256": vector["decoded_sha256"]}


if __name__ == "__main__":
    result = run()
    path = ROOT / "independent_minimality.json"
    if path.exists():
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
