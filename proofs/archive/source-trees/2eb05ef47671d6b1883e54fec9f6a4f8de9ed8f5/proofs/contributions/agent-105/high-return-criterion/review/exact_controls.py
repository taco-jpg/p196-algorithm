#!/usr/bin/env python3
"""Independent, finite controls of FULL_HIGH_RETURN.md section 2.

Enumerates all symmetric high coefficient words of widths 1 through 10,
including words with an unrealizable odd center.  Every record is retained.
This finite computation is not a theorem and does not check Lean compilation.
"""

from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MAX_WIDTH = 10


def pair_word(n):
    ds = tuple(map(int, reversed(str(n))))
    return tuple(x + y for x, y in zip(ds, reversed(ds)))


def reverse_add(n):
    return n + int(str(n)[::-1])


def polynomial(q):
    return sum(x * 10**i for i, x in enumerate(q))


def high(q):
    return q[0] >= 10 and all(9 <= x <= 18 for x in q)


def canonical_realization(q):
    if len(q) % 2 and q[len(q) // 2] % 2:
        return None
    ds = [0] * len(q)
    for i in range(len(q) // 2):
        ds[i], ds[-1-i] = q[i] - 9, 9
    if len(q) % 2:
        ds[len(q) // 2] = q[len(q) // 2] // 2
    return polynomial(ds)


def main():
    totals = Counter()
    by_width = {}
    failures = []
    representatives = {}
    raw_path = HERE / "exact_controls.jsonl.gz"
    with gzip.GzipFile(filename=str(raw_path), mode="wb", mtime=0) as raw:
        for width in range(1, MAX_WIDTH + 1):
            counts = Counter()
            for outer in range(10, 19):
                for tail in itertools.product(range(9, 19), repeat=(width - 1) // 2):
                    half = (outer,) + tail
                    q = half + half[:width // 2][::-1]
                    assert len(q) == width and high(q)
                    residual = tuple(x - 9 for x in q)
                    p = ((residual[0],) + tuple(residual[i-1] + residual[i]
                         for i in range(1, width)) + (residual[0],))
                    first_value = polynomial(q)
                    actual_p = pair_word(first_value)
                    second_value = polynomial(p)
                    s = pair_word(second_value)
                    carries = [0]
                    for x in p:
                        carries.append((x + carries[-1]) // 10)
                    u = tuple(carries[i] + carries[len(p) - 1 - i]
                              for i in range(len(p)))
                    conditions = {
                        "no_second_overflow": carries[-1] == 0,
                        "outer_at_least_14": outer >= 14,
                        "allowed_coefficients": all(x in (4,5,6,7,8,9,14,15,16,17,18) for x in p),
                        "four_fourteen_carry": all(x not in (4,14) or y >= 1 for x, y in zip(p, u)),
                        "nine_carry": all(x != 9 or y <= 1 for x, y in zip(p, u)),
                    }
                    checks = {
                        "high_carry_formula": p == actual_p,
                        "actual_carry_width": len(str(second_value)) == len(p) + carries[-1],
                        "full_iff": high(s) == all(conditions.values()),
                    }
                    if carries[-1] == 0:
                        table_s = tuple(2*x+y if x < 9 else 18-9*y if x == 9 else 2*x-20+y
                                        for x, y in zip(p, u))
                        checks["local_table"] = s == table_s
                    n = canonical_realization(q)
                    actual = None
                    if n is not None:
                        n1 = reverse_add(n)
                        n2 = reverse_add(n1)
                        pal1 = str(n1) == str(n1)[::-1]
                        pal2 = str(n2) == str(n2)[::-1]
                        checks["canonical_realization"] = pair_word(n) == q
                        checks["numeric_first_output"] = n1 == first_value
                        checks["numeric_second_output"] = n2 == second_value
                        checks["second_palindrome_iff_small"] = pal2 == all(x <= 9 for x in p)
                        if high(s):
                            checks["return_first_output_safe"] = not pal1
                            checks["return_positive_safety_iff_high_coefficient"] = ((not pal1 and not pal2) == any(x >= 10 for x in p))
                        actual = {"n": str(n), "n1": str(n1), "n2": str(n2), "pal1": pal1, "pal2": pal2}
                    record = {"width": width, "q": q, "p": p, "carry": carries,
                              "incoming_sum": u, "s": s, "returns": high(s),
                              "conditions": conditions, "actual": actual, "checks": checks}
                    raw.write((json.dumps(record, separators=(",", ":")) + "\n").encode())
                    counts["abstract_words"] += 1
                    counts["returns"] += int(high(s))
                    counts["canonical_words"] += int(n is not None)
                    counts["actual_returns"] += int(n is not None and high(s))
                    counts["outer_18_words"] += int(outer == 18)
                    counts["whole_neutral_p_words"] += int(all(x == 9 for x in p))
                    counts["second_overflow_words"] += int(carries[-1] != 0)
                    counts["actual_safe_returns"] += int(n is not None and high(s) and not actual["pal1"] and not actual["pal2"])
                    for key, ok in checks.items():
                        counts["check_" + key] += 1
                        if not ok:
                            failures.append({"q": q, "check": key})
                    for key, match in {
                        "whole_neutral_actual_return": n is not None and high(s) and all(x == 9 for x in p),
                        "outer18_actual_return": n is not None and high(s) and outer == 18,
                        "outer18_second_overflow": outer == 18 and carries[-1] != 0,
                        "overlap_sum_two_no_return": len(p) % 2 == 1 and u[len(p)//2] == 2 and not high(s),
                        "safe_actual_return": n is not None and high(s) and not actual["pal1"] and not actual["pal2"],
                    }.items():
                        if match and key not in representatives:
                            representatives[key] = record
            by_width[str(width)] = dict(counts)
            totals.update(counts)
    summary = {
        "scope": "FINITE CONTROL ONLY; not a theorem; not a Lean compilation check",
        "max_width": MAX_WIDTH,
        "enumeration": "All symmetric q of widths 1..10 with 10<=q0<=18 and 9<=qi<=18; actual integer checks exactly when the center parity permits canonical realization.",
        "totals": dict(totals), "by_width": by_width, "failures": failures,
        "representatives": representatives,
        "raw_file": raw_path.name,
        "raw_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (HERE / "exact_controls_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"totals": dict(totals), "failures": failures, "raw_sha256": summary["raw_sha256"]}, indent=2))
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
