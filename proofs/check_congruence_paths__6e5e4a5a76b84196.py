#!/usr/bin/env python3
"""Audit explicit finite terminating paths, not genuine RAA trajectories.

Their first edge is genuine. Subsequent constructed edges preserve the
modulo-9/modulo-11 laws and the stated growth/predecessor constraints.
The quantitative digit-sum carry budget intentionally fails at a specific
edge for R >= 3, demonstrating the distinction between these conditions.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def reverse(n: int) -> int:
    return int(str(n)[::-1])


def step(n: int) -> int:
    return n + reverse(n)


def width(n: int) -> int:
    return len(str(n))


def digit_sum(n: int) -> int:
    return sum(map(int, str(n)))


def palindrome(n: int) -> bool:
    return str(n) == str(n)[::-1]


def bad(n: int) -> bool:
    digits = list(map(int, str(n)))
    q = [a+b for a, b in zip(digits, reversed(digits))]
    return all(a <= 9 for a in q) or (q[0] == 11 and all(a in (0, 11) for a in q))


def chain(a: int, j: int) -> int:
    exponent = a+j
    return 10**exponent + 990*a + (89 if exponent % 2 else 989)


def terminal(a: int, ell: int) -> int:
    exponent = a+ell+1
    return 10**exponent + (782 if exponent % 2 else 692)


def path(R: int, ell: int) -> tuple[list[int], int]:
    k = 7*R//4+1
    seed = 2*(10**k-1)
    if R == 0:
        return [seed, step(seed)], 0
    first = step(seed)
    assert first == 11*(10**k-1)
    if R == 1:
        a, prefix = 5, [seed, first, 10989]
    else:
        a, prefix = k+2, [seed, first]
    end = terminal(a, ell)
    return prefix + [chain(a, j) for j in range(ell+1)] + [end, step(end)], a


def main() -> None:
    cases = [(0, 0), (1, 1), (1, 5), (2, 0)]
    cases += [(R, ell) for R in list(range(2, 65))+[128, 256]
              for ell in (R, 2*R+3)]
    records = []
    edge_count = mass_failures = protected_cases = 0
    for R, ell in cases:
        values, a = path(R, ell)
        expected_hit = 1 if R == 0 else ell+(5 if R == 1 else 4)
        assert len(values)-1 == expected_hit
        assert all(not palindrome(n) for n in values[:-1])
        assert palindrome(values[-1])
        assert values[1] == step(values[0])
        assert all(n % 99 == 0 for n in values[1:])
        assert all(width(n) >= width(values[0])+t//5 for t, n in enumerate(values))
        failed_mass_edges = []
        for t, (n, out) in enumerate(zip(values, values[1:])):
            edge_count += 1
            assert n < out < 11*n
            assert width(n) <= width(out) <= width(n)+1
            assert out % 9 == (2*n) % 9
            assert out % 11 == (0 if width(n) % 2 == 0 else (2*n) % 11)
            assert palindrome(out) == bad(n)
            assert bad(n) == palindrome(step(n))
            if bad(n):
                assert out == step(n)
            if digit_sum(out) < 2*digit_sum(n)-9*width(n):
                failed_mass_edges.append(t)
                mass_failures += 1
        if R >= 3:
            assert 1 in failed_mass_edges
        if ell >= R or R == 0:
            assert expected_hit > R
            protected_cases += 1
        records.append({
            "R": R, "ell": ell, "chain_label_a": a,
            "first_positive_palindrome_time": expected_hit,
            "safe_through_requested_R": expected_hit > R,
            "digit_sum_lower_bound_failure_edges": failed_mass_edges,
            "states_decimal": list(map(str, values)),
        })
    raw = (json.dumps(records, indent=2)+"\n").encode()
    compressed = gzip.compress(raw, mtime=0)
    raw_path = HERE / "paths.json.gz"
    raw_path.write_bytes(compressed)
    report = {
        "status": "PASS",
        "scope": "Finite explicit constructed paths; only first and terminal edges are required genuine RAA. This does not define an all-input countermap.",
        "case_count": len(records), "edge_count": edge_count,
        "state_count": sum(len(r["states_decimal"]) for r in records),
        "cases_required_safe_through_R": protected_cases,
        "digit_sum_lower_bound_failure_edge_count": mass_failures,
        "R_values": sorted({R for R, _ in cases}),
        "cases": [[R, ell] for R, ell in cases],
        "raw_paths": {
            "stored_path": "paths.json.gz", "compression": "gzip",
            "compressed_bytes": len(compressed),
            "compressed_sha256": hashlib.sha256(compressed).hexdigest(),
            "original_path": "paths.json", "original_bytes": len(raw),
            "original_sha256": hashlib.sha256(raw).hexdigest(),
            "recovery_command": "gzip -dc paths.json.gz > paths.json",
        },
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (HERE / "verification.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k: report[k] for k in
                      ("status", "case_count", "edge_count", "state_count",
                       "digit_sum_lower_bound_failure_edge_count")}))


if __name__ == "__main__":
    main()
