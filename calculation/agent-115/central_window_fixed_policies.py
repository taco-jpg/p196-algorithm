#!/usr/bin/env python3
"""Replay two safe cycles for fixed local escape policies.

Every local edge also has a separately constructed ordinary-integer one-step
fixture. Those fixtures need not concatenate into an integer trajectory. This
script imports neither the controlled radius census nor its transition code.
All acceptance checks use explicit exceptions and remain active under -O.
"""

from __future__ import annotations

import argparse
import json
import sys


class VerificationError(Exception):
    """A declared local cycle or ordinary-integer fixture failed verification."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


OVERFLOW_CYCLE = (
    (1, 7, 14, 14, 7, 1),
    (8, 12, 10, 12, 8),
    (8, 11, 4, 4, 11, 8),
    (10, 6, 8, 6, 10),
)

NO_OVERFLOW_CYCLE = (
    (3, 10, 7, 13, 13, 7, 10, 3),
    (7, 0, 16, 7, 7, 16, 0, 7),
    (14, 1, 12, 15, 15, 12, 1, 14),
    (8, 4, 5, 12, 12, 5, 4, 8),
    (16, 8, 11, 5, 5, 11, 8, 16),
    (12, 18, 2, 11, 11, 2, 18, 12),
    (5, 17, 6, 3, 3, 6, 17, 5),
    (11, 14, 13, 6, 6, 13, 14, 11),
)

POLICIES = (
    ("g1-c0-z0", 2, 1, OVERFLOW_CYCLE),
    ("g0-c0", 3, 0, NO_OVERFLOW_CYCLE),
)


def validate_window(word: tuple[int, ...], radius: int) -> None:
    require(len(word) in (2 * radius + 1, 2 * radius + 2), "window width")
    require(word == word[::-1], "window symmetry")
    require(all(0 <= x <= 18 for x in word), "window coefficient bound")
    require(not len(word) % 2 or word[len(word) // 2] % 2 == 0,
            "odd central coefficient parity")


def safe(word: tuple[int, ...]) -> bool:
    return max(word) >= 10 and any(x not in (0, 11) for x in word)


def fold(digits: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(digits, reversed(digits)))


def policy_step(word: tuple[int, ...], overflow: int) -> tuple[int, ...]:
    """Local arithmetic with entry carry zero and, when needed, neighbor zero."""
    carry = 0
    digits = []
    for coefficient in word:
        carry, digit = divmod(coefficient + carry, 10)
        digits.append(digit)
    if overflow:
        if len(word) % 2:
            # The extra input coefficient zero emits the final carry of word.
            digits.append(carry)
        else:
            digits = digits[1:]
    return fold(tuple(digits))


def decimal_digits(n: int) -> tuple[int, ...]:
    require(n > 0, "positive integer required")
    return tuple(int(ch) for ch in str(n)[::-1])


def integer_window(n: int, radius: int) -> tuple[int, ...]:
    coefficients = fold(decimal_digits(n))
    size = 2 * radius + (1 if len(coefficients) % 2 else 2)
    require(size <= len(coefficients), "integer too short for window")
    start = (len(coefficients) - size) // 2
    return coefficients[start:start + size]


def realize(coefficients: tuple[int, ...]) -> int:
    """Split every symmetric coefficient into actual decimal digit pairs."""
    require(coefficients == coefficients[::-1], "fixture symmetry")
    require(coefficients[0] > 0, "fixture leading pair must be positive")
    digits = [0] * len(coefficients)
    for i in range((len(coefficients) + 1) // 2):
        j = len(coefficients) - 1 - i
        coefficient = coefficients[i]
        require(0 <= coefficient <= 18, "fixture coefficient bound")
        if i == j:
            require(coefficient % 2 == 0, "fixture central parity")
            digits[i] = coefficient // 2
        else:
            digits[j] = min(coefficient, 9)
            digits[i] = coefficient - digits[j]
    require(all(0 <= d <= 9 for d in digits) and digits[-1] > 0,
            "fixture digits must be canonical")
    n = sum(d * 10 ** i for i, d in enumerate(digits))
    require(fold(decimal_digits(n)) == coefficients, "fixture pair reconstruction")
    return n


def integer_fixture(source: tuple[int, ...], target: tuple[int, ...],
                    radius: int, overflow: int) -> dict:
    # The outside symbol 1/10 forces the desired terminal carry; the next zero
    # resets the entering carry. An odd overflow needs one further neighbor 0.
    prefix = (10 if overflow else 1, 0)
    if overflow and len(source) % 2:
        prefix += (0,)
    coefficients = prefix + source + prefix[::-1]
    seed = realize(coefficients)
    successor = seed + int(str(seed)[::-1])
    require(integer_window(seed, radius) == source, "integer source projection")
    require(integer_window(successor, radius) == target, "integer target projection")
    require(successor != int(str(successor)[::-1]), "safe fixture output must be nonpalindromic")
    require(len(str(successor)) - len(str(seed)) == overflow,
            "integer overflow label")

    # Audit the promised control using the actual input's reconstructed profile.
    carry = [0]
    for coefficient in fold(decimal_digits(seed)):
        carry.append((coefficient + carry[-1]) // 10)
    entry = len(prefix) - (1 if overflow and len(source) % 2 else 0)
    require(carry[entry] == 0, "incoming control carry")
    require(carry[-1] == overflow, "terminal control carry")
    if overflow and len(source) % 2:
        require(coefficients[len(prefix) - 1] == 0, "odd overflow neighbor")
    return {
        "seed": seed,
        "successor": successor,
        "input_coefficients": coefficients,
        "source": source,
        "target": target,
        "overflow": overflow,
        "incoming_carry": 0,
        "odd_neighbor": 0 if overflow and len(source) % 2 else None,
    }


def replay() -> dict:
    results = []
    for name, radius, overflow, cycle in POLICIES:
        require(len(set(cycle)) == len(cycle), "listed policy period must be exact")
        edges = []
        for index, source in enumerate(cycle):
            target = cycle[(index + 1) % len(cycle)]
            validate_window(source, radius)
            validate_window(target, radius)
            require(safe(source) and safe(target), "cycle must remain locally safe")
            require(policy_step(source, overflow) == target, "local policy edge")
            fixture = integer_fixture(source, target, radius, overflow)
            fixture["edge"] = index
            edges.append(fixture)
        results.append({"policy": name, "radius": radius, "period": len(cycle),
                        "safe_states": len(cycle), "integer_fixtures": len(edges),
                        "edges": edges})
    return {
        "classification": "COMPUTED",
        "policy_cycles": results,
        "total_local_edges": sum(x["period"] for x in results),
        "total_integer_fixtures": sum(x["integer_fixtures"] for x in results),
        "scope": ("Counterexamples to these two fixed escape POLICIES only; "
                  "not universal closed sets or actual integer cycles. "
                  "Ordinary-integer fixtures are independent one-step realizations."),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="include all 12 seeds and edges")
    args = parser.parse_args()
    try:
        result = replay()
    except VerificationError as error:
        print(f"VERIFICATION FAILED: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for cycle in result["policy_cycles"]:
            print(" ".join(f"{key}={cycle[key]}" for key in
                           ("policy", "radius", "period", "safe_states", "integer_fixtures")))
        print("ALL CHECKS PASSED: 12 local policy edges; 12 ordinary-integer one-step fixtures.")
        print("COMPUTED: " + result["scope"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
