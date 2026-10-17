#!/usr/bin/env python3
"""Independent modular-arithmetic replay/audit of Agent114 finite_evidence.json.

Does not import the generating verifier and never forms the reversal via
string slicing. This remains finite evidence rather than Lean verification.
"""
import hashlib
import json
import pathlib
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def reverse_divmod(n):
    reverse = 0
    while n:
        n, digit = divmod(n, 10)
        reverse = reverse * 10 + digit
    return reverse


def audit_one(row, limit):
    r = row["r"]
    x = int(row["canonical_representative"])
    formula = 11 * 10 ** (2 * r + 5) + 18271 * 10 ** (r + 1) + 11
    assert x + reverse_divmod(x) == formula
    assert formula == int(row["first_reverse_add"])
    trace = hashlib.sha256()
    hit = None
    for t in range(1, limit + 1):
        x += reverse_divmod(x)
        digits = str(x)
        trace.update(f"{t}:{digits}\n".encode("ascii"))
        pal = digits == digits[::-1]
        if t <= 11:
            expected = row["first_11_steps"][t - 1]
            assert (t, digits, pal) == (
                expected["t"], expected["value"], expected["palindrome"]
            ), (r, t)
        if pal:
            hit = t
            break
    assert limit == row["horizon_checked"]
    assert hit == row["first_positive_palindrome_through_horizon"]
    assert len(str(x)) == row["last_value_digit_length"]
    assert hashlib.sha256(str(x).encode("ascii")).hexdigest() == row["last_value_sha256"]
    assert trace.hexdigest() == row["trajectory_sha256"]
    return r, hit, trace.hexdigest()


def main():
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).with_name("finite_evidence.json")
    record = json.loads(path.read_text(encoding="utf8"))
    assert record["short_spacer_horizon"] == 3000
    for row in record["short_spacer_records"]:
        assert row["r"] in (1, 2, 3, 4)
        assert audit_one(row, 3000)[1] is None
    assert audit_one(record["r5_boundary_control"], 11)[1] == 11
    print("PASS: 4x3000 exact modular-arithmetic steps, plus r5 boundary t11; trace hashes matched")


if __name__ == "__main__":
    main()
