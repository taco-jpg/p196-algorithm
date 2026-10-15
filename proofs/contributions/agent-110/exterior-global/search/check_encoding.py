#!/usr/bin/env python3
"""Direct arithmetic assignments independently evaluate every generated clause.

This is finite encoding QA, not an all-width proof of the SAT reduction.
Includes satisfiable open transitions and failed-tail controls, so rejection
alone is not used to validate a cyclic encoding.
"""
import json
from pathlib import Path
import random
from encode import build, normalize, next_phase, trim, original_outer_step

HERE = Path(__file__).resolve().parent


def set_onehot(assignment, row, picked):
    assignment.update({v: i == picked for i, v in enumerate(row)})


def check_one(c, B):
    W = len(B)
    formula, m = build(W, 1, c, cyclic=False, require_overflow=False)
    k = int(c >= 10)
    low, lc = normalize(B, 0)
    rev, rc_rev = normalize(B[::-1], k)
    high, rc = rev[::-1], rc_rev[::-1]
    gamma = rc[0]
    rhs = [1] + high if gamma else high + [c - 9 * k]
    raw = [a + b for a, b in zip(low + [c + lc[-1] - 10 * k], rhs)]
    expected_fit = raw[-1] == next_phase(c)
    assignment = {}
    for j in range(W):
        set_onehot(assignment, m["B_variables"][0][j], B[j])
        set_onehot(assignment, m["B_variables"][1][j], raw[j])
        set_onehot(assignment, m["low_digit_variables"][0][j], low[j])
        set_onehot(assignment, m["high_digit_variables"][0][j], high[j])
    assignment.update({v: bool(e) for v, e in zip(m["low_carry_variables"][0], lc)})
    assignment.update({v: bool(e) for v, e in zip(m["high_carry_variables"][0], rc)})
    assert len(assignment) == formula.variables
    passed = all(any(assignment[abs(x)] == (x > 0) for x in clause)
                 for clause in formula.clauses)
    assert passed == expected_fit
    if expected_fit:
        original = original_outer_step(c, trim(c, B))
        assert original == (next_phase(c), trim(next_phase(c), raw[:-1]), gamma)
        # A changed successor with unchanged computed carry/digit assignments
        # must fail at least one exact transition clause.
        mutate = dict(assignment)
        set_onehot(mutate, m["B_variables"][1][0], (raw[0] + 1) % 19)
        assert not all(any(mutate[abs(x)] == (x > 0) for x in clause)
                       for clause in formula.clauses)
    return expected_fit, gamma


def main():
    rng = random.Random(11020261015)
    counts = {"accepted_tail": 0, "rejected_tail": 0, "overflow": 0,
              "nonoverflow": 0, "cases": 0}
    samples = []
    for c in range(2, 18, 2):
        for width in range(1, 6):
            words = [[c] * width]
            words += [[rng.randrange(1, 19)] + [rng.randrange(19) for _ in range(width - 1)]
                      for _ in range(64)]
            for B in words:
                fits, g = check_one(c, B)
                counts["cases"] += 1
                counts["accepted_tail" if fits else "rejected_tail"] += 1
                counts["overflow" if g else "nonoverflow"] += 1
                if len(samples) < 16:
                    samples.append({"phase": c, "B": B, "fits": fits, "overflow": g})
    out = {"status": "PASS", "scope": "finite all-clause assigned-transition QA",
           "seed": 11020261015, "counts": counts, "samples": samples}
    (HERE / "encoding-controls.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out["counts"]))


if __name__ == "__main__":
    main()
