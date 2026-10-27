#!/usr/bin/env python3
"""Independent arithmetic controls for the all-base normalization/sign lemmas.

Run with ordinary Python or python -O; every test uses an explicit failure
branch. Whole-integer quotient/remainder arithmetic is compared with the
unchanged repository mirror's column normalization. The quotient law permits
arbitrary natural coefficients/carries and every positive base, including 1.
The carry-flip sign test is restricted to base >= 2, coefficients <= 2*(b-1),
and incoming carries 0/1. No symmetry or nonempty-word assumption is used.

These finite COMPUTED controls support, but do not replace, Lean verification.
No files from Agent 112's earlier research branches are imported.
"""

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parents[2]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def positional_value(base, word):
    value, weight = 0, 1
    for coefficient in word:
        value += coefficient * weight
        weight *= base
    return value


def integer_normalization(base, word, incoming):
    """Normalize by one whole-integer division, not by propagating carries."""
    if type(base) is not int or base < 1:
        raise ValueError("base must be a positive integer")
    if type(incoming) is not int or incoming < 0:
        raise ValueError("incoming carry must be a natural number")
    if any(type(c) is not int or c < 0 for c in word):
        raise ValueError("coefficients must be natural numbers")
    outgoing, remainder = divmod(positional_value(base, word) + incoming,
                                 base ** len(word))
    digits = []
    for _ in word:
        remainder, digit = divmod(remainder, base)
        digits.append(digit)
    require(remainder == 0, "whole-integer remainder exceeded the fixed width")
    return digits, outgoing


def load_mirror():
    source = ROOT / "calculation/neutral_band_search.py"
    spec = importlib.util.spec_from_file_location("agent112_normalization_mirror", source)
    require(spec is not None and spec.loader is not None, "mirror cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Audit:
    def __init__(self, mirror):
        self.mirror = mirror
        self.counts = {
            "normalization_cases": 0,
            "base_one_cases": 0,
            "incoming_above_one_cases": 0,
            "coefficient_bound_exceeded_cases": 0,
            "bounded_word_cases": 0,
            "bounded_nonsymmetric_words": 0,
            "bounded_empty_words": 0,
            "negative_signed_words": 0,
            "zero_signed_words": 0,
            "positive_signed_words": 0,
            "sign_equivalence_cases": 0,
            "maximum_width": 0,
            "maximum_outgoing_carry": 0,
        }

    def normalization(self, base, word, incoming):
        word = tuple(word)
        expected = integer_normalization(base, word, incoming)
        actual = self.mirror.norm(base, word, incoming)
        context = (base, word, incoming)
        require(actual == expected, f"normalization mismatch: {context}")
        digits, outgoing = actual
        power = base ** len(word)
        total = positional_value(base, word) + incoming
        require(len(digits) == len(word), f"normalization width mismatch: {context}")
        require(all(0 <= d < base for d in digits), f"digit bound failed: {context}")
        require(outgoing == total // power, f"quotient law failed: {context}")
        require(positional_value(base, digits) == total % power,
                f"remainder law failed: {context}")
        require(positional_value(base, digits) + power * outgoing == total,
                f"value conservation failed: {context}")
        counts = self.counts
        counts["normalization_cases"] += 1
        counts["base_one_cases"] += int(base == 1)
        counts["incoming_above_one_cases"] += int(incoming > 1)
        counts["coefficient_bound_exceeded_cases"] += int(any(c > 2 * (base - 1) for c in word))
        counts["maximum_width"] = max(counts["maximum_width"], len(word))
        counts["maximum_outgoing_carry"] = max(counts["maximum_outgoing_carry"], outgoing)
        return actual

    def bounded_word(self, base, word):
        word = tuple(word)
        require(base >= 2 and all(0 <= c <= 2 * (base - 1) for c in word),
                "bounded-word control violated the sign theorem's assumptions")
        value, power = positional_value(base, word), base ** len(word)
        signed = value + 1 - power
        require(value <= 2 * (power - 1), "bounded value estimate failed")
        outputs, flipping = [], []
        for incoming in (0, 1):
            digits, outgoing = self.normalization(base, word, incoming)
            require(outgoing <= 1, "bounded normalization produced a nonbit carry")
            threshold = ((incoming == 0 and power <= value)
                         or (incoming == 1 and value + 1 < power))
            sign_test = ((incoming == 0 and signed > 0)
                         or (incoming == 1 and signed < 0))
            actual_flip = outgoing == 1 - incoming
            require(actual_flip == threshold == sign_test,
                    f"carry-flip sign mismatch: {(base, word, incoming)}")
            if actual_flip:
                flipping.append(incoming)
                expected_value = signed - 1 if signed > 0 else power + signed
                require(positional_value(base, digits) == expected_value,
                        "flipping normalization digit value failed")
            outputs.append((digits, outgoing))
        expected_flipping = [] if signed == 0 else [int(signed < 0)]
        require(flipping == expected_flipping, "flip existence/uniqueness failed")
        if signed == 0:
            require(outputs[0][1] == 0 and outputs[1][1] == 1,
                    "neutral value did not transmit incoming carry")
        counts = self.counts
        counts["bounded_word_cases"] += 1
        counts["bounded_nonsymmetric_words"] += int(word != word[::-1])
        counts["bounded_empty_words"] += int(not word)
        counts["negative_signed_words"] += int(signed < 0)
        counts["zero_signed_words"] += int(signed == 0)
        counts["positive_signed_words"] += int(signed > 0)
        counts["sign_equivalence_cases"] += 2
        return outputs


def exhaustive_bounded(audit):
    scopes = ((2, 6), (3, 5), (4, 4), (5, 4), (10, 3),
              (11, 3), (17, 2), (26, 2), (32, 2))
    rows = []
    for base, maximum_width in scopes:
        count = 0
        for width in range(maximum_width + 1):
            for word in itertools.product(range(2 * base - 1), repeat=width):
                audit.bounded_word(base, word)
                count += 1
        rows.append({"base": base, "maximum_width": maximum_width,
                     "words": count, "incoming_carries": [0, 1]})
    return rows


def general_quotient_controls(audit):
    rows = []
    for base in (1, 2, 3, 5):
        alphabet = sorted({0, 1, base - 1, base, base + 1, 2 * base - 1, base ** 2 + 3})
        carries = sorted({0, 1, 2, base, base ** 2 + 1})
        count = 0
        for width in range(4):
            for word in itertools.product(alphabet, repeat=width):
                for incoming in carries:
                    audit.normalization(base, word, incoming)
                    count += 1
        rows.append({"base": base, "maximum_width": 3, "alphabet": alphabet,
                     "incoming_carries": carries, "normalization_cases": count})
    generator = random.Random(1120312)
    for _ in range(5000):
        base = generator.choice((1, 2, 3, 5, 10, 20, 26, 97))
        width = generator.randrange(65)
        word = tuple(generator.randrange(base ** 6 + 4) for _ in range(width))
        incoming = generator.randrange(base ** 10 + 4)
        audit.normalization(base, word, incoming)
    return {"exhaustive_scopes": rows, "random_seed": 1120312,
            "sampled_cases": 5000, "sampled_maximum_width": 64,
            "sampled_bases": [1, 2, 3, 5, 10, 20, 26, 97]}


def special_and_sampled_bounded(audit):
    bases = (2, 3, 4, 5, 10, 11, 17, 20, 26, 32, 97)
    special_cases = 0
    for base in bases:
        for width in (0, 1, 2, 3, 10, 64):
            for coefficient in (0, base - 1, 2 * (base - 1)):
                audit.bounded_word(base, (coefficient,) * width)
                special_cases += 1
    generator = random.Random(1120326)
    for _ in range(4000):
        base = generator.choice(bases)
        width = generator.randrange(129)
        word = tuple(generator.randrange(2 * base - 1) for _ in range(width))
        audit.bounded_word(base, word)
    # An explicit unbounded-coefficient counterexample prevents extending the
    # sign theorem beyond its stated alphabet merely from the quotient law.
    digits, outgoing = audit.normalization(10, (20,), 0)
    require(outgoing == 2 and outgoing != 1 and positional_value(10, (20,)) + 1 - 10 == 11,
            "coefficient-bound counterexample changed")
    return {"special_word_cases": special_cases,
            "special_families": ["empty", "all_zero", "all_neutral", "maximal_coefficients"],
            "random_seed": 1120326, "sampled_words": 4000, "sampled_maximum_width": 128,
            "sampled_bases": list(bases),
            "unbounded_sign_counterexample": {"base": 10, "word": [20], "incoming": 0,
                                               "signed_value": 11,
                                               "digits": digits, "outgoing": outgoing}}


BASE20_SOURCE = {
    "agent": "Agent 116",
    "pull_request": "https://github.com/taco-jpg/p196-algorithm/pull/356",
    "commit": "b7a718b78d67cf54d362232ba1b8f90fbec23af8",
    "path": "lean/P196/Agent116Base20Certificate/Certificate.lean",
    "canonical_edges_sha256": "14f5c26c2feed05b59e90441d513cd94bc6b1d4b9ced0d2d2cd9fddbbdcf9d6a",
}


def base20_fixture():
    """Reconstruct the pinned source data using whole-integer normalization."""
    exterior = (2, 19, 20, 13, 9, 25, 15, 26, 28, 14, 12, 16, 14, 13, 12, 13, 11, 5, 7, 12, 5, 7, 11, 20, 16, 11, 17, 10, 16, 27, 16, 16, 23, 12, 8, 7, 20, 32, 31, 34, 34, 27, 15, 4, 16, 20, 9, 23, 35, 29, 23, 20, 19, 22, 25, 30, 31, 28, 17, 9, 7, 12, 17, 17, 23, 22, 27, 34, 20, 21, 29, 22, 25, 21, 20, 12, 35, 31, 17, 16, 30, 32, 23, 12, 8, 15, 14, 2, 2, 11, 9)
    center = (28, 26, 26, 9, 13, 22, 13, 17, 31, 35, 35, 32, 23, 23, 32, 35, 35, 31, 17, 13, 22, 13, 9, 26, 26, 28)
    initial = exterior, center
    edges = []
    for phase, (u, v) in enumerate(zip(map(int, "10001000"), map(int, "00000010"))):
        db, e = integer_normalization(20, exterior, 0)
        dc, f = integer_normalization(20, center, e)
        dr, g = integer_normalization(20, exterior[::-1], f)
        require(f == 1 - e, "base20 fixture center failed carry flip")
        require((e, g) == (int("01001011"[phase]), int("00010001"[phase])),
                "base20 fixture driver changed")
        left = db + [19 * (1 - e)] if g else db
        right = [1] + dr[::-1] if g else dr[::-1]
        raw_b = tuple(a + b for a, b in zip(left, right))
        center_digits = dc + [19 * e] if g else dc
        raw_c = tuple(a + b for a, b in zip(center_digits, center_digits[::-1]))
        next_b = raw_b[:-u] if u else raw_b
        next_c = raw_c[v:-v] if v else raw_c
        require(raw_b == next_b + (19,) * u, "base20 exterior trim changed")
        require(raw_c == (19,) * v + next_c + (19,) * v, "base20 center trim changed")
        edges.append((exterior, center, next_b, next_c, u, v))
        exterior, center = next_b, next_c
    require((exterior, center) == initial, "base20 fixture did not close")
    encoded = json.dumps(edges, separators=(",", ":")).encode("ascii")
    require(hashlib.sha256(encoded).hexdigest() == BASE20_SOURCE["canonical_edges_sha256"],
            "base20 fixture differs from the pinned eight source edges")
    return edges


def known_certificates(audit):
    fixtures = audit.mirror._lean_certs()
    require({base for base, _ in fixtures} == {2, 4, 8, 11, 16, 17, 26, 32},
            "eight main-source certificate fixtures were not recovered")
    fixtures.append((20, base20_fixture()))
    rows = []
    for base, edges in sorted(fixtures):
        cycle = [(list(b), list(c), list(b2), list(c2), u, v)
                 for b, c, b2, c2, u, v in edges]
        require(audit.mirror.cycleOK(base, cycle, cycle[0][0], cycle[0][1]),
                f"known base-{base} full mirror certificate failed")
        for index, (exterior, center, next_b, next_c, u, v) in enumerate(cycle):
            bnorm = audit.bounded_word(base, exterior)
            cnorm = audit.bounded_word(base, center)
            rnorm = audit.bounded_word(base, exterior[::-1])
            db, e = bnorm[0]
            dc, f = cnorm[e]
            dr, g = rnorm[f]
            require(f == 1 - e, f"known base-{base} center did not flip")
            left = db + [(base - 1) * (1 - e)] if g else db
            right = [1] + dr[::-1] if g else dr[::-1]
            raw_b = [a + b for a, b in zip(left, right)]
            center_digits = dc + [(base - 1) * e] if g else dc
            raw_c = [a + b for a, b in zip(center_digits, center_digits[::-1])]
            require(raw_b == next_b + [base - 1] * u, "known exterior equation failed")
            require(raw_c == [base - 1] * v + next_c + [base - 1] * v,
                    "known center equation failed")
            require(cycle[(index + 1) % len(cycle)][:2] == (next_b, next_c),
                    "known fixture edge chain is not closed")
        rows.append({"base": base, "edges": len(cycle),
                     "bounded_block_cases": 3 * len(cycle),
                     "explicit_normalization_checks": 6 * len(cycle)})
    return {"fixtures": rows, "total_edges": sum(row["edges"] for row in rows),
            "full_mirror_cycles": len(rows), "additional_base20_source": BASE20_SOURCE}


def main():
    audit = Audit(load_mirror())
    result = {"status": "COMPUTED", "exhaustive_bounded": exhaustive_bounded(audit),
              "general_quotient": general_quotient_controls(audit),
              "special_and_sampled_bounded": special_and_sampled_bounded(audit),
              "known_certificates": known_certificates(audit), "totals": audit.counts}
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS: quotient/remainder and bounded carry-flip laws match independent integer arithmetic.")


if __name__ == "__main__":
    main()
