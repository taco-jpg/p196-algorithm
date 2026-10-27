#!/usr/bin/env python3
"""Complete fixed-weight binary-necklace coverage for exterior B searches.

Default scope: decimal period 25, total overflow 8.  Generate the least
rotation of every binary necklace with the specified weight, including
imprimitive words.  Apply the audited necessary head relation from the
Agent 116 period-20 review; survival does not imply an exterior B cycle.

Coverage is checked independently by Burnside's fixed-rotation formula,
by every representative's rotations, and by total labelled-word coverage.
The recurrence and empty/all-neutral interpretation are credited to
Agent 4 (#290/#323) and the independent Agent 116 review (#375).
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb, gcd
from pathlib import Path
import time

from p20_coverage import HEAD, full_b_successors, require, surviving_heads


def fixed_weight_necklaces(n, weight):
    """FKM recursion with exact-weight pruning; no primitive-period filter."""
    require(n >= 1 and 0 <= weight <= n, "invalid necklace parameters")
    a = [0] * (n + 1)

    def visit(t, period, ones):
        remaining = n - t + 1
        if ones > weight or ones + remaining < weight:
            return
        if t > n:
            if n % period == 0:
                yield tuple(a[1:])
            return
        a[t] = a[t - period]
        yield from visit(t + 1, period, ones + a[t])
        if a[t - period] == 0:
            a[t] = 1
            yield from visit(t + 1, t, ones + 1)

    yield from visit(1, 1, 0)


def burnside_weight_count(n, weight):
    """Average fixed words over all n rotations, separately from FKM."""
    fixed_sum = 0
    for shift in range(n):
        cycles = gcd(n, shift)
        cycle_length = n // cycles
        if weight % cycle_length == 0:
            fixed_sum += comb(cycles, weight // cycle_length)
    require(fixed_sum % n == 0, "Burnside numerator is not divisible by n")
    return fixed_sum // n


def brute_necklaces(n, weight):
    """Small independent labelled-subset enumeration; used only in controls."""
    representatives = set()
    for occupied in combinations(range(n), weight):
        word = [0] * n
        for position in occupied:
            word[position] = 1
        word = tuple(word)
        representatives.add(min(word[j:] + word[:j] for j in range(n)))
    return sorted(representatives)


def selftest():
    cases = necklace_total = 0
    for n in range(1, 11):
        for weight in range(n + 1):
            generated = list(fixed_weight_necklaces(n, weight))
            require(generated == brute_necklaces(n, weight),
                    f"fixed-weight generator mismatch: n={n}, weight={weight}")
            require(len(generated) == burnside_weight_count(n, weight),
                    f"Burnside mismatch: n={n}, weight={weight}")
            cases += 1
            necklace_total += len(generated)
    require((0, 1) * 4 in list(fixed_weight_necklaces(8, 4)),
            "imprimitive alternating control was omitted")
    require((0, 0, 0, 1) * 3 in list(fixed_weight_necklaces(12, 3)),
            "imprimitive period-four control was omitted")

    states = edges = 0
    for width in range(3):
        for word in product(range(19), repeat=width):
            if word and word[0] == 0:
                continue
            source = word[0] if word else 9
            states += 1
            for overflow, following in full_b_successors(word):
                target = following[0] if following else 9
                require(HEAD[overflow][source - 1] & (1 << (target - 1)),
                        "head recurrence disagrees with direct B arithmetic")
                edges += 1
    for text in ("11100010000", "100010001000"):
        word = tuple(map(int, text))
        require(all(surviving_heads(word[j:] + word[:j])
                    for j in range(len(word))),
                "a known B driver or one of its rotations was rejected")
    return {"status": "PASS", "fixed_weight_brute_cases": cases,
            "necklaces_compared_to_brute": necklace_total,
            "explicit_imprimitive_controls": 2,
            "direct_B_states": states, "all_trim_edges": edges,
            "max_direct_width": 2, "known_positive_drivers": 2}


def census(n, weight, max_necklaces, deadline):
    expected = burnside_weight_count(n, weight)
    require(expected <= max_necklaces,
            f"scope requires {expected} necklaces, above cap {max_necklaces}")
    words, selected = [], []
    periods, selected_periods = Counter(), Counter()
    labelled_coverage = 0
    for index, coefficients in enumerate(fixed_weight_necklaces(n, weight)):
        if index % 256 == 0 and time.monotonic() > deadline:
            raise TimeoutError("coverage census exceeded its time limit")
        word = "".join(map(str, coefficients))
        require(len(word) == n and word.count("1") == weight,
                "generator produced a word outside the requested scope")
        require(not words or words[-1] < word,
                "generator is not strictly ordered or duplicated a word")
        rotations = {word[j:] + word[:j] for j in range(n)}
        require(word == min(rotations), "word is not its least cyclic rotation")
        least_period = len(rotations)
        require(n % least_period == 0,
                "rotation orbit size does not divide the temporal period")
        require(word == word[:least_period] * (n // least_period),
                "rotation orbit size is not the least word period")
        words.append(word)
        periods[least_period] += 1
        labelled_coverage += least_period
        if surviving_heads(coefficients):
            selected.append(word)
            selected_periods[least_period] += 1
    require(time.monotonic() <= deadline, "coverage census exceeded its time limit")
    require(len(words) == expected, "necklace count disagrees with Burnside")
    require(labelled_coverage == comb(n, weight),
            "rotation orbits do not cover every labelled word of this weight")
    require(len(set(words)) == len(words), "duplicate necklace representatives")
    payload = "".join(word + "\n" for word in selected)
    all_payload = "".join(word + "\n" for word in words)
    result = {"status": "COMPUTED_NECESSARY_HEAD_FILTER", "base": 10,
              "period": n, "overflow_weight": weight,
              "all_necklaces": len(words), "burnside_necklaces": expected,
              "labelled_words_covered": labelled_coverage,
              "surviving_necklaces": len(selected),
              "all_counts_by_least_period": dict(sorted(periods.items())),
              "surviving_counts_by_least_period": dict(sorted(selected_periods.items())),
              "every_representative_rotation_checked": True,
              "imprimitive_words_included": True,
              "all_lexicographic_lf_sha256": sha256(all_payload.encode("ascii")).hexdigest(),
              "selected_lexicographic_lf_sha256": sha256(payload.encode("ascii")).hexdigest()}
    return result, all_payload, payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--period", type=int, default=25)
    parser.add_argument("--weight", type=int, default=8)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--max-necklaces", type=int, default=1000000)
    parser.add_argument("--seconds", type=float, default=1200)
    parser.add_argument("--output", type=Path, help="surviving g words, one per line")
    parser.add_argument("--all-output", type=Path, help="every necklace, one per line")
    args = parser.parse_args()
    if not 1 <= args.period <= 32 or not 0 <= args.weight <= args.period:
        parser.error("require 1 <= period <= 32 and 0 <= weight <= period")
    if args.max_necklaces < 1 or not 0 < args.seconds <= 1200:
        parser.error("require max-necklaces >= 1 and 0 < seconds <= 1200")
    begin = time.monotonic()
    try:
        tests = selftest() if args.selftest else None
        result, all_payload, payload = census(
            args.period, args.weight, args.max_necklaces, begin + args.seconds)
        if args.output is not None:
            args.output.write_text(payload, encoding="ascii")
        if args.all_output is not None:
            args.all_output.write_text(all_payload, encoding="ascii")
        if tests is not None:
            result["selftest"] = tests
        result["elapsed_seconds"] = round(time.monotonic() - begin, 6)
        print(json.dumps(result, sort_keys=True))
    except (ValueError, TimeoutError) as error:
        print(json.dumps({"status": "UNDECIDED", "reason": str(error),
                          "period": args.period, "overflow_weight": args.weight},
                         sort_keys=True))
        raise SystemExit(2) from error


if __name__ == "__main__":
    main()
