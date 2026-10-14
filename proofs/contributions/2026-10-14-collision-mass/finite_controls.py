#!/usr/bin/env python3
"""Independent finite controls for the proved B H B collision-mass identity."""
from itertools import product
import json
from pathlib import Path


def normalize(q, carry=0):
    digits = []
    for coefficient in q:
        total = coefficient + carry
        digits.append(total % 10)
        carry = total // 10
    return sum(digits) + carry, carry


def initial_nines(q):
    for i, coefficient in enumerate(q):
        if coefficient != 9:
            return i
    return len(q)


blocks = [q for length in range(3) for q in product(range(19), repeat=length)]
checked = strict = maximum_deficit = 0
max_witness = None
for outer in blocks:
    outer_mass, e = normalize(outer)
    for middle in blocks:
        middle_mass, _ = normalize(middle)
        _, h = normalize(middle, e)
        full_mass, _ = normalize(outer + middle + outer)
        deficit = 9 * (e * initial_nines(middle) + h * initial_nines(outer))
        assert full_mass + deficit == 2 * outer_mass + middle_mass
        checked += 1
        strict += deficit > 0
        if deficit > maximum_deficit:
            maximum_deficit = deficit
            max_witness = {"outer": outer, "middle": middle, "deficit": deficit}

seed = 555455
next_value = seed + int(str(seed)[::-1])
assert next_value == 1110010
assert sum(map(int, str(next_value))) == 4
report = {
    "result": "PASS",
    "scope": "Exhaustive B,H lengths 0..2 with coefficients 0..18; finite controls only.",
    "block_pairs_checked": checked,
    "strict_mass_deficit_cases": strict,
    "maximum_deficit": maximum_deficit,
    "maximum_deficit_witness": max_witness,
    "canonical_example": {
        "seed": seed,
        "next_value": next_value,
        "actual_digit_sum": 4,
        "separate_zero_carry_mass": 22,
        "deficit": 18,
    },
}
path = Path(__file__).with_name("finite_controls.json")
path.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
