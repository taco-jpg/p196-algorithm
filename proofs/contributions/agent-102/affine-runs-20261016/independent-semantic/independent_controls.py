#!/usr/bin/env python3
"""Finite, independent controls for Agent102's literal affine-run contracts.

The oracle is direct Python list expansion.  The comparison procedure uses
half-open intervals and integer affine endpoints.  This file is not a Lean
proof, does not run Lean, and makes no reverse-add or infinite-orbit claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import random
import time


HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Affine:
    a: int
    b: int

    def at(self, k: int) -> int:
        assert k >= 0
        return self.a * k + self.b

    def positive_part(self) -> "Affine":
        return Affine(0, 0) if self.a < 0 or (self.a == 0 and self.b < 0) else self

    def __add__(self, other: "Affine") -> "Affine":
        return Affine(self.a + other.a, self.b + other.b)


Run = tuple[int, int]
Spec = tuple[int, Affine]
Span = tuple[int, int, int]


def expand(runs: tuple[Run, ...]) -> list[int]:
    assert all(d >= 0 and n >= 0 for d, n in runs)
    return [d for d, n in runs for _ in range(n)]


def spans(runs: tuple[Run, ...]) -> list[Span]:
    out = []
    pos = 0
    for d, n in runs:
        out.append((d, pos, pos + n))
        pos += n
    return out


def positive_intersection(s: Span, t: Span) -> bool:
    return max(s[1], t[1]) < min(s[2], t[2])


def agreement_without_length(left: list[Span], right: list[Span]) -> bool:
    return all(not positive_intersection(s, t) or s[0] == t[0]
               for s in left for t in right)


def interval_equal(left: tuple[Run, ...], right: tuple[Run, ...]) -> bool:
    return (sum(n for _, n in left) == sum(n for _, n in right)
            and agreement_without_length(spans(left), spans(right)))


def at(specs: tuple[Spec, ...], k: int) -> tuple[Run, ...]:
    return tuple((d, max(0, f.at(k))) for d, f in specs)


def endpoints(specs: tuple[Spec, ...]) -> list[Affine]:
    out = [Affine(0, 0)]
    for _, f in specs:
        out.append(out[-1] + f.positive_part())
    return out


def tail_cutoff(left: tuple[Spec, ...], right: tuple[Spec, ...]) -> int:
    # A sufficient (not optimal) explicit bound: every clipped length has
    # stabilized, then every pair of cumulative endpoints has stable order.
    fs = endpoints(left) + endpoints(right)
    lengths = [abs(f.b) + 1 for _, f in left + right]
    differences = [abs(f.b - g.b) + 1 for f in fs for g in fs]
    return max([1] + lengths + differences)


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


def run_checks() -> dict:
    started = time.monotonic()
    stats = {}
    palette = tuple(product(range(3), range(3)))
    catalog = [p for length in range(4) for p in product(palette, repeat=length)]
    cached = [(r, expand(r), spans(r)) for r in catalog]
    assert len(cached) == 820
    coverage_checks = 0
    for runs, word, ss in cached:
        assert word[::-1] == expand(runs[::-1])
        assert all(lo <= hi for _, lo, hi in ss)
        for i in range(-1, len(word) + 1):
            covered = [d for d, lo, hi in ss if lo <= i < hi]
            assert len(covered) == int(0 <= i < len(word))
            if covered:
                assert covered[0] == word[i]
            coverage_checks += 1
        assert (word == word[::-1]) == interval_equal(runs, runs[::-1])
    same_word_different_representation = 0
    pair_checks = 0
    for lr, lw, ls in cached:
        for rr, rw, rs in cached:
            oracle = lw == rw
            criterion = len(lw) == len(rw) and agreement_without_length(ls, rs)
            assert oracle == criterion, (lr, rr, lw, rw)
            same_word_different_representation += int(oracle and lr != rr)
            pair_checks += 1
    stats["literal_runs"] = dict(catalog_size=len(cached), pair_checks=pair_checks,
        palindrome_checks=len(cached), coverage_position_checks=coverage_checks,
        equal_words_with_different_run_lists=same_word_different_representation,
        domain="0..3 runs; digits 0..2; counts 0..2; every pair")

    scalar_checks = 0
    for a in range(-6, 7):
        for b in range(-20, 21):
            f = Affine(a, b)
            bound = abs(b) + 1
            for k in list(range(bound, bound + 41)) + [bound + 1_000_000]:
                assert max(0, f.at(k)) == f.positive_part().at(k)
                assert f.positive_part().at(k) >= 0
                scalar_checks += 1
    functions = [Affine(a, b) for a in range(-3, 4) for b in range(-6, 7)]
    order_checks = 0
    for f in functions:
        for g in functions:
            bound = abs(f.b - g.b) + 1
            expected = sign(f.at(bound) - g.at(bound))
            for delta in [0, 1, 2, 3, 10, 100, 1_000_000]:
                k = bound + delta
                assert sign(f.at(k) - g.at(k)) == expected
                order_checks += 1
    stats["integer_affine"] = dict(clipped_length_checks=scalar_checks,
        ordered_function_pairs=len(functions) ** 2, order_checks=order_checks,
        slope_range=[-6, 6], intercept_range=[-20, 20], negative_slopes_included=True)

    spec_palette = tuple((d, Affine(a, b))
                         for d, a, b in product(range(2), range(-1, 2), range(-1, 2)))
    families = [p for length in range(3) for p in product(spec_palette, repeat=length)]
    assert len(families) == 343
    family_checks = 0
    family_bound_max = 0
    for left in families:
        for right in families:
            bound = tail_cutoff(left, right)
            family_bound_max = max(family_bound_max, bound)
            expected = expand(at(left, bound)) == expand(at(right, bound))
            for delta in [0, 1, 2, 3, 4, 5, 6, 7, 19]:
                k = bound + delta
                lr, rr = at(left, k), at(right, k)
                oracle = expand(lr) == expand(rr)
                assert oracle == expected
                assert interval_equal(lr, rr) == oracle
                family_checks += 1
    palindrome_checks = 0
    for family in families:
        bound = tail_cutoff(family, family[::-1])
        initial = expand(at(family, bound))
        expected = initial == initial[::-1]
        for delta in [0, 1, 2, 3, 4, 5, 6, 7, 19]:
            value = expand(at(family, bound + delta))
            assert (value == value[::-1]) == expected
            palindrome_checks += 1
    stats["affine_families"] = dict(families=len(families), family_pairs=len(families) ** 2,
        equality_checks=family_checks, palindrome_checks=palindrome_checks,
        max_cutoff=family_bound_max,
        domain="0..2 runs; digits 0..1; slopes -1..1; intercepts -1..1; every pair",
        sampled_offsets=[0, 1, 2, 3, 4, 5, 6, 7, 19])

    rng = random.Random(102196)
    random_checks = 0
    for _ in range(12000):
        def one_family():
            return tuple((rng.choice([0, 1, 2, 9, 17, 255]),
                          Affine(rng.randint(-3, 4), rng.randint(-20, 20)))
                         for _ in range(rng.randint(0, 8)))
        left, right = one_family(), one_family()
        bound = tail_cutoff(left, right)
        initial = expand(at(left, bound)) == expand(at(right, bound))
        for delta in [0, 1, 17, 63]:
            lr, rr = at(left, bound + delta), at(right, bound + delta)
            oracle = expand(lr) == expand(rr)
            assert oracle == initial
            assert interval_equal(lr, rr) == oracle
            random_checks += 1
    stats["random_controls"] = dict(seed=102196, family_pairs=12000,
        equality_checks=random_checks, max_runs=8,
        digits=[0, 1, 2, 9, 17, 255], slopes=[-3, 4], intercepts=[-20, 20])

    examples = []
    def record(name, data):
        examples.append(dict(name=name, **data))

    left, right = ((4, 1),), ((4, 2),)
    assert agreement_without_length(spans(left), spans(right))
    assert expand(left) != expand(right)
    record("total_length_is_necessary", dict(left=left, right=right,
        overlap_agreement=True, literal_equality=False))

    left, right = ((1, 1), (9, 0), (1, 1)), ((1, 2),)
    s, t = spans(left)[1], spans(right)[0]
    crossed = s[1] < t[2] and t[1] < s[2]
    assert crossed and not positive_intersection(s, t)
    assert expand(left) == expand(right)
    record("empty_internal_run_invalidates_two_cross_inequalities", dict(
        left=left, right=right, zero_span=s, containing_span=t,
        two_cross_inequalities=True, positive_intersection=False, literal_equality=True))

    s, t = (1, 0, 1), (2, 1, 2)
    assert max(s[1], t[1]) <= min(s[2], t[2])
    assert not positive_intersection(s, t)
    record("touching_endpoints_are_not_positive_intersection", dict(left_span=s, right_span=t))

    for left, right, name in [
        (((2, 1), (2, 2)), ((2, 3),), "adjacent_same_digit"),
        (((2, 1), (7, 0), (2, 2)), ((2, 3),), "zero_run_bridges_same_digit"),
        (((8, 0), (9, 0)), (), "zero_runs_and_empty_word")]:
        assert left != right and expand(left) == expand(right)
        assert interval_equal(left, right)
        record(name, dict(left=left, right=right, literal_equality=True))

    left, right = ((1, 1), (0, 1)), ((1, 1),)
    assert expand(left) != expand(right)
    assert sum(d * 10 ** i for i, d in enumerate(expand(left))) == 1
    record("raw_word_retains_high_zero", dict(left=left, right=right,
        left_word=expand(left), right_word=expand(right),
        both_low_first_numeric_values=1, literal_equality=False))

    f, g = ((1, Affine(1, 0)),), ((1, Affine(0, 10000)),)
    root = 10000
    assert all(expand(at(f, k)) != expand(at(g, k)) for k in range(101))
    assert expand(at(f, root)) == expand(at(g, root))
    assert expand(at(f, root + 1)) != expand(at(g, root + 1))
    bound = tail_cutoff(f, g)
    assert bound > root
    record("isolated_equality_after_10000", dict(root=root, cutoff=bound,
        early_test_range=[0, 100], early_equalities=0, equality_at_root=True))

    family = ((1, Affine(1, 1)), (0, Affine(0, 1)), (1, Affine(0, 10002)))
    root = 10001
    for k, expected in [(0, False), (100, False), (root, True), (root + 1, False)]:
        word = expand(at(family, k))
        assert (word == word[::-1]) == expected
    bound = tail_cutoff(family, family[::-1])
    assert bound > root
    word = expand(at(family, bound))
    assert word != word[::-1]
    record("isolated_palindrome_after_10001", dict(root=root, cutoff=bound,
        at_zero=False, at_root=True, at_root_plus_one=False, tail_palindrome=False))

    family = ((3, Affine(-1, 5001)),)
    assert len(expand(at(family, 0))) == 5001
    assert expand(at(family, 5001)) == []
    assert expand(at(family, 5002)) == []
    record("negative_slope_eventually_disappears", dict(slope=-1, intercept=5001,
        first_empty_parameter=5001, cutoff=tail_cutoff(family, ())))

    stats["diagnostic_examples"] = examples
    stats["runtime_seconds"] = round(time.monotonic() - started, 3)
    return stats


if __name__ == "__main__":
    report = dict(status="PASS", scope="Finite semantic controls only; no Lean execution",
        utc=datetime.now(timezone.utc).isoformat(), python=platform.python_version(),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        results=run_checks())
    (HERE / "independent-controls-result.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))
