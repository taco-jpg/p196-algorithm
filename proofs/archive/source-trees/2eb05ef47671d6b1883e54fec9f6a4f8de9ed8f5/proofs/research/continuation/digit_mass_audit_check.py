"""Independent exact checks for the digit-mass audit.

All arithmetic is ordinary Python integer reverse-and-add.  Enumeration
checks finite instances of independently proved identities; it does not
establish an infinite orbit.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
import json
from pathlib import Path


def digits(n: int) -> list[int]:
    return [int(c) for c in str(n)[::-1]]


def reverse_add(n: int) -> int:
    return n + int(str(n)[::-1])


def digit_sum(n: int) -> int:
    return sum(digits(n))


def is_palindrome(n: int) -> bool:
    s = str(n)
    return s == s[::-1]


def realize(q: list[int]) -> int:
    """Realize a symmetric pair-sum word as an ordinary positive integer."""
    length = len(q)
    assert q == q[::-1] and q[0] > 0
    assert all(0 <= x <= 18 for x in q)
    assert length % 2 == 0 or q[length // 2] % 2 == 0
    ds = [0] * length
    for i in range(length // 2):
        ds[length - 1 - i] = min(9, q[i])
        ds[i] = q[i] - ds[length - 1 - i]
    if length % 2:
        ds[length // 2] = q[length // 2] // 2
    n = int("".join(map(str, ds[::-1])))
    assert len(str(n)) == length
    assert [ds[i] + ds[length - 1 - i] for i in range(length)] == q
    return n


def carry_data(q: list[int]) -> tuple[list[int], list[int]]:
    cs = [0]
    ds = []
    for x in q:
        carry, digit = divmod(x + cs[-1], 10)
        cs.append(carry)
        ds.append(digit)
    if cs[-1]:
        ds.append(cs[-1])
    return cs, ds


def all_q(length: int):
    pairs = length // 2
    if length == 1:
        for center in range(2, 19, 2):
            yield [center]
        return
    for outer in range(1, 19):
        for middle in product(range(19), repeat=pairs - 1):
            left = [outer, *middle]
            if length % 2:
                for center in range(0, 19, 2):
                    yield left + [center] + left[::-1]
            else:
                yield left + left[::-1]


def fill_symmetric(q: list[int], target_mass: int) -> list[int]:
    """Increase an admissible baseline to the requested even total mass."""
    remaining = (target_mass - sum(q)) // 2
    assert target_mass >= sum(q) and (target_mass - sum(q)) % 2 == 0
    for i in range(len(q) // 2):
        increment = min(remaining, 18 - q[i])
        q[i] += increment
        q[-1 - i] += increment
        remaining -= increment
    if len(q) % 2:
        i = len(q) // 2
        increment = min(remaining, (18 - q[i]) // 2)
        q[i] += 2 * increment
        remaining -= increment
    assert remaining == 0 and sum(q) == target_mass
    return q


def carry_free_realization(length: int, mass: int) -> int:
    """For every 1 <= mass <= floor(9*length/2), realize zero carries."""
    assert 1 <= mass <= 9 * length // 2
    if length == 1:
        return mass
    q = [0] * length
    q[0] = q[-1] = 1
    remaining = mass - 1
    for i in range(length // 2):
        increment = min(remaining, 9 - q[i])
        q[i] += increment
        q[-1 - i] += increment
        remaining -= increment
    if length % 2:
        assert remaining <= 4
        q[length // 2] = 2 * remaining
        remaining = 0
    assert remaining == 0
    return realize(q)


def nonincreasing_overflow_realization(length: int, mass: int) -> int:
    """For every mass > floor(9*length/2), overflow with S' <= S."""
    assert 9 * length // 2 < mass <= 9 * length
    if length == 1:
        return mass
    q = [9] * length
    q[0] = q[-1] = 10
    if length % 2:
        if 2 * mass == 9 * length + 1:
            q[length // 2] = 8
            return realize(q)
        q[length // 2] = 10
    return realize(fill_symmetric(q, 2 * mass))


def snapshot(n: int) -> dict:
    ds = digits(n)
    q = [ds[i] + ds[-1 - i] for i in range(len(ds))]
    cs, _ = carry_data(q)
    result = reverse_add(n)
    return {
        "n": n,
        "T_n": result,
        "length": len(ds),
        "digit_sum": sum(ds),
        "output_digit_sum": digit_sum(result),
        "carry_count": sum(cs),
        "overflow": cs[-1],
        "q_low_to_high": q,
        "output_palindrome": is_palindrome(result),
        "strict_ratio_interval": 4 * sum(ds) < 11 * digit_sum(result)
        and digit_sum(result) < 2 * sum(ds),
    }


def main():
    counts = Counter()
    for length in range(1, 9):
        for q in all_q(length):
            n = realize(q)
            value = reverse_add(n)
            cs, ds = carry_data(q)
            assert digits(value) == ds
            mass, next_mass = digit_sum(n), digit_sum(value)
            number_carries, overflow = sum(cs), cs[-1]
            assert next_mass == 2 * mass - 9 * number_carries
            pal = is_palindrome(value)
            exception = overflow == 1 and q[0] == 11 and set(q) <= {0, 11}
            assert pal == (number_carries == 0 or exception)
            if pal:
                assert next_mass == 2 * mass or 11 * next_mass == 4 * mass
                assert number_carries % 2 == 0 and next_mass % 2 == 0
            if pal and overflow:
                assert all(q[i] == 11 * cs[i + 1] for i in range(length))
                assert mass % 11 == 0 and next_mass % 4 == 0
                assert set(ds) <= {0, 1, 2}
                assert ds[0] == ds[-1] == 1
            if 4 * mass < 11 * next_mass and next_mass < 2 * mass:
                assert not pal
                counts["strict_interval_cases"] += 1
            counts["q_words_checked"] += 1
            counts["overflow" if overflow else "no_overflow"] += 1
            if pal:
                counts["palindrome_exception" if exception else "palindrome_no_carry"] += 1

    constructor_counts = Counter()
    for length in range(1, 81):
        for mass in range(1, 9 * length + 1):
            if mass <= 9 * length // 2:
                n = carry_free_realization(length, mass)
                assert digit_sum(n) == mass and len(str(n)) == length
                assert is_palindrome(reverse_add(n))
                assert digit_sum(reverse_add(n)) == 2 * mass
                constructor_counts["carry_free_cells"] += 1
            else:
                n = nonincreasing_overflow_realization(length, mass)
                assert digit_sum(n) == mass and len(str(n)) == length
                assert len(str(reverse_add(n))) == length + 1
                assert digit_sum(reverse_add(n)) <= mass
                constructor_counts["nonincreasing_overflow_cells"] += 1

    # These are exact finite controls and counterexamples, not orbit evidence.
    examples = {str(n): snapshot(n) for n in (39, 132, 59, 154, 605, 3199, 1099)}
    abstract_path = []
    length, mass = 3, 27
    while mass > 9 * length // 2:
        n = nonincreasing_overflow_realization(length, mass)
        row = snapshot(n)
        abstract_path.append(row)
        length += 1
        mass = row["output_digit_sum"]
    abstract_path.append(snapshot(carry_free_realization(length, mass)))
    results = {
        "status": "Finite audit passed; no infinite decimal Lychrel witness established.",
        "enumeration": dict(counts),
        "length_sum_constructor_checks": dict(constructor_counts),
        "examples": examples,
        "abstract_adversarial_path_not_one_actual_orbit": abstract_path,
    }
    path = Path(__file__).with_name("digit_mass_audit_results.json")
    path.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({k: v for k, v in results.items() if k not in {"examples", "abstract_adversarial_path_not_one_actual_orbit"}}, indent=2))
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
