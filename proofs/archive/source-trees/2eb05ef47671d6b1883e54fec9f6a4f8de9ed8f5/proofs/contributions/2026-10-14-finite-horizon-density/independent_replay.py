#!/usr/bin/env python3
"""Independent finite controls for the mirrored-nine block argument.

Run with Python 3; no third-party dependencies.  This checks ordinary
integer iteration, finite counts, and the proposed parameter formulas.
It does not prove all-time avoidance or replace the written counting proof.
"""

from fractions import Fraction
import json
from pathlib import Path
import random


def block_length(horizon):
    assert horizon >= 1
    return min(2 * horizon - 1, 7 * (horizon - 1) // 4 + 2)


def digits(n):
    return [int(c) for c in str(n)[::-1]]


def from_digits(d):
    assert d and 1 <= d[-1] <= 9
    return int("".join(str(x) for x in reversed(d)))


def palindrome(n):
    s = str(n)
    return s == s[::-1]


def step(n):
    return n + int(str(n)[::-1])


def marked(d, horizon):
    width = len(d)
    run = block_length(horizon)
    count = max(width // 2 - 1, 0) // run
    return any(
        all(d[i] == d[width - 1 - i] == 9
            for i in range(1 + j * run, 1 + (j + 1) * run))
        for j in range(count)
    )


def check_safe(n, horizon):
    assert marked(digits(n), horizon), (n, horizon, "unmarked input")
    for time in range(1, horizon + 1):
        n = step(n)
        assert not palindrome(n), (n, horizon, time, "early palindrome")


def longest_eighteen_run(d):
    longest = current = 0
    for a, b in zip(d, reversed(d)):
        current = current + 1 if a + b == 18 else 0
        longest = max(longest, current)
    return longest


def exhaustive_one_step():
    rows = []
    for width in range(1, 6):
        total = 9 * 10 ** (width - 1)
        marker_count = hit_count = initial_palindromes = pal_unmarked = 0
        nonpal_hits = 0
        for n in range(10 ** (width - 1), 10 ** width):
            marker = marked(digits(n), 1)
            initial_pal = palindrome(n)
            hit = palindrome(step(n))
            assert not (marker and hit), (n, "marker hit at time one")
            marker_count += marker
            hit_count += hit
            initial_palindromes += initial_pal
            pal_unmarked += initial_pal and not marker
            nonpal_hits += hit and not initial_pal
        half = width // 2
        blocks = max(half - 1, 0)
        no_marker = Fraction(99, 100) ** blocks
        initial_pal_prob = Fraction(1, 10 ** half)
        pal_no_marker = initial_pal_prob * Fraction(9, 10) ** blocks
        assert Fraction(marker_count, total) == 1 - no_marker
        assert Fraction(initial_palindromes, total) == initial_pal_prob
        assert Fraction(pal_unmarked, total) == pal_no_marker
        assert Fraction(hit_count, total) <= no_marker
        if width >= 2:
            conditional_bound = (no_marker - pal_no_marker) / (1 - initial_pal_prob)
            assert Fraction(nonpal_hits, total - initial_palindromes) <= conditional_bound
        rows.append(dict(width=width, total=total, marked=marker_count,
                         one_step_hits=hit_count, initial_palindromes=initial_palindromes,
                         palindrome_and_unmarked=pal_unmarked))
    return rows


def planted_controls():
    endpoint_center_count = exact_run_count = random_count = 0
    rows = []
    rng = random.Random(1961014)
    for horizon in range(1, 21):
        run = block_length(horizon)
        # All outer digit pairs and all odd center digits.  These include
        # both parity widths and every possible initial outer potential.
        for leading in range(1, 10):
            for trailing in range(10):
                check_safe(int(str(leading) + "9" * (2 * run) + str(trailing)), horizon)
                endpoint_center_count += 1
                for center in range(10):
                    check_safe(int(str(leading) + "9" * run + str(center)
                                   + "9" * run + str(trailing)), horizon)
                    endpoint_center_count += 1

        # Ensure tests really use a longest run of exactly the refined
        # sufficient length: longer accidental runs cannot mask an error.
        for outer_sum in range(1, 19):
            width = 4 * run + 3
            d = [0] * width
            d[-1] = min(9, outer_sum)
            d[0] = outer_sum - d[-1]
            for i in range(1 + run, 1 + 2 * run):
                d[i] = d[width - 1 - i] = 9
            assert longest_eighteen_run(d) == run
            check_safe(from_digits(d), horizon)
            exact_run_count += 1

        minimum_width = 2 * run + 2
        widths = sorted({minimum_width, minimum_width + 1, minimum_width + 2,
                         max(minimum_width, 64), 128, 256})
        for width in widths:
            for _ in range(16):
                d = [rng.randrange(10) for _ in range(width)]
                d[-1] = rng.randrange(1, 10)
                blocks = (width // 2 - 1) // run
                j = rng.randrange(blocks)
                for i in range(1 + j * run, 1 + (j + 1) * run):
                    d[i] = d[width - 1 - i] = 9
                check_safe(from_digits(d), horizon)
                random_count += 1
        rows.append(dict(horizon=horizon, sufficient_run=run,
                         minimum_block_width=minimum_width))
    return dict(endpoint_center_seeds=endpoint_center_count,
                exact_refined_run_seeds=exact_run_count,
                random_background_seeds=random_count,
                random_seed=1961014, maximum_horizon=20,
                maximum_width=256, parameters=rows)


def main():
    result = dict(
        status="all finite controls passed",
        scope="Finite counting and ordinary-integer controls only; no all-time avoidance claim.",
        exhaustive_one_step=exhaustive_one_step(),
        planted_blocks=planted_controls(),
    )
    destination = Path(__file__).with_name("audit.json")
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(status=result["status"],
                          exhaustive_seeds=sum(r["total"] for r in result["exhaustive_one_step"]),
                          planted_blocks={k: v for k, v in result["planted_blocks"].items()
                                          if k != "parameters"}), sort_keys=True))


if __name__ == "__main__":
    main()
