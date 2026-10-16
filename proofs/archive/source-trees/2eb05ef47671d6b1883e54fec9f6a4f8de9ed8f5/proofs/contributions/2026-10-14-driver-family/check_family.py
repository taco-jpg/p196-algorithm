#!/usr/bin/env python3
"""Independent explicit-seed and time-index controls; no infinite inference."""

import gzip
import hashlib
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
TRACE = HERE.parent / "2026-10-14-collision-review/driver_trace.bin.gz"
EXPECTED_SHA = "6431d3a11008f81e9249f05187e207a73f9f1dc0e87c897e46030f2a16b02404"


def digits(n):
    return list(map(int, str(n)[::-1]))


def pair(n):
    d = digits(n)
    return [a + b for a, b in zip(d, d[::-1])]


def value(word):
    n = 0
    for c in reversed(word):
        n = 10 * n + c
    return n


def normalized(word):
    d = digits(value(word))
    e = len(d) - len(word)
    assert e in (0, 1)
    return d, e


def seed(r):
    return (10 ** (2*r+6) + 10 ** (2*r+5) + 10 ** (r+5)
            + 8 * 10 ** (r+4) + 7 * 10 ** (r+3))


def step(n):
    return n + int(str(n)[::-1])


def is_pal(n):
    return str(n) == str(n)[::-1]


def driver_step(b, h):
    bd, e = normalized(b)
    hd, f = normalized(h)
    delta = max(e, f)
    bn = [a + c for a, c in zip(bd, bd[::-1])]
    hn = [0] * (len(h) + 2 * delta - e)
    for i, c in enumerate(hd):
        hn[delta - e + i] += c
        hn[len(h) + delta - 1 - i] += c
    return bn, hn, delta


def integer_controls():
    states = 0
    per_parameter = []
    for r in range(1, 65):
        n = seed(r)
        assert len(str(n)) == 2*r+7 and not is_pal(n)
        b, h, gap = [1, 1], [1, 8, 14, 8, 1], r-1
        assert pair(n) == b + [0]*gap + h + [0]*gap + b
        t = 0
        while gap >= 0:
            assert pair(n) == b + [0]*gap + h + [0]*gap + b
            bd, e = normalized(b)
            hd, f = normalized(h)
            event = e == f and bd == bd[::-1] and hd == hd[::-1]
            nxt = step(n)
            assert is_pal(nxt) == event
            b, h, delta = driver_step(b, h)
            states += 1
            t += 1
            if gap == 0 and delta == 1:
                break
            gap -= delta
            n = nxt
            assert pair(n) == b + [0]*gap + h + [0]*gap + b
            assert t <= 4*r+1
        per_parameter.append({"r": r, "verified_positive_iterates_through_contact": t})
    return states, per_parameter


def bad_class(word):
    if all(x <= 9 for x in word):
        return 0
    if word[0] == 11 and all(x in (0, 11) for x in word):
        return 1
    return None


def trace_threshold():
    assert hashlib.sha256(TRACE.read_bytes()).hexdigest() == EXPECTED_SHA
    records = 0
    last_loss = 0
    with gzip.open(TRACE, "rb") as stream:
        assert stream.read(8) == b"P196DRV1"
        while True:
            header = stream.read(16)
            if not header:
                break
            assert len(header) == 16
            t, loss, nb, nh = struct.unpack("<IIII", header)
            b, h = stream.read(nb), stream.read(nh)
            assert len(b) == nb and len(h) == nh
            assert t == records and loss >= last_loss
            bc, hc = bad_class(b), bad_class(h)
            assert bc is None or hc is None or bc != hc
            records += 1
            last_loss = loss
    assert records == 10000 and t == 9999 and loss == 5077
    return {"records": records, "last_driver_time": t,
            "last_spacer_loss": loss, "minimum_certified_parameter": loss+1,
            "minimum_certified_digit_width": 2*(loss+1)+7,
            "certified_nonpalindromic_times": [0, records],
            "trace_sha256": EXPECTED_SHA}


def main():
    transitions, cases = integer_controls()
    report = {"status": "PASS", "parameter_controls": len(cases),
              "integer_transition_controls": transitions,
              "certificate": trace_threshold(), "controls": cases,
              "scope": "Written universal reduction plus finite trace; no all-time claim.",
              "full_transition_audit": "../2026-10-14-collision-audit/"}
    (HERE / "verification.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k: v for k, v in report.items() if k != "controls"}))


if __name__ == "__main__":
    main()
