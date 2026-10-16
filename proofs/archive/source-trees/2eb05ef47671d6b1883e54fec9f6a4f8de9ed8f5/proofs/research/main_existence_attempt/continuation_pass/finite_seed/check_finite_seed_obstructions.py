#!/usr/bin/env python3
"""Exact finite audits for the written finite-seed extraction obstructions.

The artificial map below is deliberately NOT reverse-and-add.  It preserves
specified exact arithmetic features, and every one of its orbits terminates.
The all-parameter arguments are in FINITE_SEED_OBSTRUCTIONS.md.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


def reverse10(n: int) -> int:
    return int(str(n)[::-1])


def raa(n: int) -> int:
    return n + reverse10(n)


def palindrome(n: int) -> bool:
    s = str(n)
    return s == s[::-1]


def bad(n: int) -> bool:
    """Exact true RAA next-palindrome predecessor classification."""
    ds = tuple(map(int, str(n)))
    qs = tuple(a + b for a, b in zip(ds, ds[::-1]))
    return all(q <= 9 for q in qs) or (
        qs[0] == 11 and all(q in (0, 11) for q in qs)
    )


def pair_word(n: int) -> tuple[int, ...]:
    ds = tuple(map(int, str(n)))
    return tuple(a + b for a, b in zip(ds, ds[::-1]))


def chain(a: int, j: int) -> int:
    assert a >= 3 and j >= 0
    return 10 ** (a + j) + 10 * a + 9


def chain_label(n: int, ell) -> tuple[int, int] | None:
    width = len(str(n))
    rem = n - 10 ** (width - 1) - 9
    if rem < 0 or rem % 10:
        return None
    a = rem // 10
    j = width - a - 1
    if a >= 3 and 0 <= j <= ell(a):
        assert chain(a, j) == n
        return a, j
    return None


def pair_chain_label(n: int, ell) -> tuple[int, int] | None:
    """Recognize the entire mirrored-pair class of a sparse chain node."""
    qs = pair_word(n)
    width = len(qs)
    if width < 4 or qs[0] != 10:
        return None
    half = (width - 2) // 2
    if any(q > 9 for q in qs[1 : half + 1]):
        return None
    a = sum(q * 10**i for i, q in enumerate(qs[1 : half + 1]))
    j = width - a - 1
    if a >= 3 and 0 <= j <= ell(a) and qs == pair_word(chain(a, j)):
        return a, j
    return None


def model_step(n: int, ell=lambda a: a, class_detector=chain_label) -> int:
    """A fully terminating counterdynamics, not a proposed RAA theorem."""
    assert n > 0
    if bad(n):
        return raa(n)
    label = class_detector(n, ell)
    if label is not None:
        a, j = label
        if j < ell(a):
            return chain(a, j + 1)
        return 10 ** (a + ell(a) + 1) + 2
    width = len(str(n))
    if width == 1:
        return 19
    if width == 2:
        return 109
    return chain(width, 0)


def first_positive_hit(n: int, step, cap: int) -> tuple[int | None, list[int]]:
    trace = [n]
    for t in range(1, cap + 1):
        n = step(n)
        trace.append(n)
        if palindrome(n):
            return t, trace
    return None, trace


def exact_bad_count(width: int) -> int:
    if width == 1:
        return 4
    m = width // 2
    if width % 2:
        return 225 * 55 ** (m - 1) + 8 * 9 ** (m - 1)
    return 45 * 55 ** (m - 1) + 8 * 9 ** (m - 1)


def weighted_predecessor(a: int, m: int) -> int:
    s = str(a)
    assert len(s) == m - 1
    comp = "".join(str(9 - int(d)) for d in s[::-1])
    return int(s + "99" + comp)


def main() -> None:
    output = {"status": "PASS", "claims_are_written_not_Lean": True}
    hist = Counter()
    width_counts = Counter()
    chain_counts = Counter()
    checksum = hashlib.sha256()
    checked = 0
    for n in range(1, 100_000):
        actual_bad = palindrome(raa(n))
        assert bad(n) == actual_bad
        out = model_step(n)
        width = len(str(n))
        assert n < out < 11 * n
        assert width <= len(str(out)) <= width + 1
        assert palindrome(out) == actual_bad
        if actual_bad:
            assert out == raa(n)
            width_counts[width] += 1
        if chain_label(n, lambda a: a) is not None:
            chain_counts[width] += 1
        checksum.update(f"{n},{out}\n".encode())
        checked += 1
        if n < 10_000:
            time, trace = first_positive_hit(n, model_step, 30)
            assert time is not None
            hist[time] += 1
            for t, x in enumerate(trace):
                assert len(str(x)) >= width + t // 5
            if width >= 3 and not bad(n) and chain_label(n, lambda a: a) is None:
                assert time == width + 3
    for width in range(1, 6):
        assert width_counts[width] == exact_bad_count(width)
        expected = sum(1 for a in range(3, width) if width - a - 1 <= a)
        assert chain_counts[width] == expected
    output["exhaustive_model"] = {
        "integer_range": [1, 99_999],
        "checked": checked,
        "sha256_n_and_model_image": checksum.hexdigest(),
        "bad_counts_by_width": dict(sorted(width_counts.items())),
        "sparse_chain_counts_by_width": dict(sorted(chain_counts.items())),
        "first_hit_histogram_1_through_9999": dict(sorted(hist.items())),
    }

    examples = []
    for seed in (5, 19, 109, 196, 198, 1039, 10_039, 19_998, 999_990):
        hit, trace = first_positive_hit(seed, model_step, 100)
        assert hit is not None
        examples.append({"seed": seed, "first_positive_hit": hit, "trace": trace})
    output["countermodel_example_traces"] = examples

    finite_seed_controls = []
    for horizon in list(range(65)) + [128, 256]:
        exponent = (7 * horizon) // 4 + 1
        n = 2 * (10**exponent - 1)
        assert not palindrome(n)
        initial = n
        for _ in range(horizon):
            n = model_step(n)
            assert not palindrome(n)
        hit, _ = first_positive_hit(initial, model_step, len(str(initial)) + 5)
        assert hit is not None and hit > horizon
        finite_seed_controls.append({
            "horizon": horizon,
            "seed_width": len(str(initial)),
            "model_first_hit": hit,
        })
    output["same_explicit_C_R_family"] = finite_seed_controls

    long_horizon_controls = []
    square_ell = lambda a: a * a
    for width in range(3, 16):
        seed = 10 ** (width - 1) + 9
        assert not bad(seed) and chain_label(seed, square_ell) is None
        hit, _ = first_positive_hit(seed, lambda n: model_step(n, square_ell), width**2 + 4)
        assert hit == width**2 + 3
        long_horizon_controls.append({"width": width, "first_hit": hit})
    output["quadratic_delay_variant"] = long_horizon_controls

    # A strengthened countermap also preserves dependence on the complete
    # mirrored-pair word: all seeds with the same word have the same output.
    pair_model = lambda n: model_step(n, class_detector=pair_chain_label)
    pair_outputs = {}
    pair_class_counts = Counter()
    pair_hist = Counter()
    for n in range(1, 100_000):
        qs = pair_word(n)
        out = pair_model(n)
        assert n < out < 11 * n
        assert palindrome(out) == bad(n)
        assert len(str(n)) <= len(str(out)) <= len(str(n)) + 1
        if qs in pair_outputs:
            assert pair_outputs[qs] == out
        else:
            pair_outputs[qs] = out
        label = pair_chain_label(n, lambda a: a)
        if label is not None:
            pair_class_counts[len(str(n))] += 1
        if n < 10_000:
            hit, _ = first_positive_hit(n, pair_model, 30)
            assert hit is not None
            pair_hist[hit] += 1
            if len(str(n)) >= 3 and not bad(n) and label is None:
                assert hit == len(str(n)) + 3
    for width in range(1, 6):
        expected = 0
        for a in range(3, width):
            if width - a - 1 <= a:
                cardinality = 9
                for d in str(a):
                    cardinality *= int(d) + 1
                expected += cardinality
        assert pair_class_counts[width] == expected
    output["pair_word_preserving_countermodel"] = {
        "integer_range": [1, 99_999],
        "distinct_pair_words_checked": len(pair_outputs),
        "exceptional_pair_class_counts_by_width": dict(sorted(pair_class_counts.items())),
        "first_hit_histogram_1_through_9999": dict(sorted(pair_hist.items())),
    }

    inverse_fibers = []
    for m in range(2, 7):
        y = 10 ** (2 * m) + 99 * 10 ** (m - 1) - 1
        assert not palindrome(y) and not bad(y)
        seen = set()
        digest = hashlib.sha256()
        smallest = largest = None
        for a in range(10 ** (m - 2), 10 ** (m - 1)):
            n = weighted_predecessor(a, m)
            assert not palindrome(n) and not bad(n)
            assert n < y and raa(n) == y
            seen.add(n)
            smallest = n if smallest is None else min(smallest, n)
            largest = n if largest is None else max(largest, n)
            digest.update(f"{n}\n".encode())
        expected = 9 * 10 ** (m - 2)
        assert len(seen) == expected
        inverse_fibers.append({
            "m": m,
            "safe_target_y": y,
            "distinct_safe_predecessors_checked": len(seen),
            "smallest_predecessor": smallest,
            "largest_predecessor": largest,
            "sha256_predecessors": digest.hexdigest(),
            "monotone_weight_ratio_lower_bound": expected,
        })
    output["true_RAA_safe_inverse_fibers"] = inverse_fibers

    output["scope"] = (
        "The countermodel is not reverse-and-add and proves no decimal Lychrel witness. "
        "It refutes extraction based only on the properties it preserves. "
        "The weighted obstruction is an actual RAA theorem, restricted to positive "
        "nonincreasing seed-size weights and a uniform pointwise incoming-weight bound."
    )
    path = Path(__file__).with_name("check_finite_seed_obstructions.json")
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({
        "status": "PASS",
        "model_inputs": checked,
        "terminating_trajectories": 9_999,
        "safe_inverse_fiber_inputs": sum(x["distinct_safe_predecessors_checked"] for x in inverse_fibers),
        "saved": str(path),
    }, indent=2))


if __name__ == "__main__":
    main()
