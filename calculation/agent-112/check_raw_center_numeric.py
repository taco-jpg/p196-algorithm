#!/usr/bin/env python3
"""Finite independent controls for fixed digits and the raw-center formula.

Run with Python or python -O. Every check has an explicit failure branch.
The oracle uses whole integers, fixed-width digit extraction, and direct
positional evaluation; the comparison uses the unchanged column mirror.
Actual-Hyp controls allow nonsymmetric B/C and empty B. The decimal P24
fixture is a CENTER-ONLY return with prescribed streams, not a full B/C
certificate or a decimal Lychrel candidate. No exterior search is performed.

With m=len(C), M=b**m, N=value(C), e=e1, g=gam, Z=N+1-M, and R the
value of the reversed m fixed digits of N+e, the tested signed identity is
Zraw = Z + b**g * (R + e*(M+1) - M), under the actual Hyp carry flip.

The sibling normalization harness supplies only the mirror loader and the
pinned base-20 fixture; this file defines its own arithmetic oracle.
"""

import hashlib
import itertools
import json
import random

import check_normalization_arithmetic as fixtures


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def value(base, word):
    return sum(coefficient * base ** position
               for position, coefficient in enumerate(word))


def fixed_digits(base, width, total):
    """Least-significant first, exactly width digits, with leading zeros."""
    if type(base) is not int or base < 1:
        raise ValueError("base must be a positive integer")
    if type(width) is not int or width < 0:
        raise ValueError("width must be a natural number")
    if type(total) is not int or total < 0:
        raise ValueError("total must be a natural number")
    return [total // base ** position % base for position in range(width)]


def whole_normalization(base, word, incoming):
    total = value(base, word) + incoming
    return fixed_digits(base, len(word), total), total // base ** len(word)


def pair_word(word):
    return [left + right for left, right in zip(word, word[::-1])]


class Audit:
    def __init__(self, mirror):
        self.mirror = mirror
        self.counts = {
            "fixed_digit_cases": 0,
            "base_one_fixed_digit_cases": 0,
            "normalization_cases": 0,
            "equal_width_total_pairs": 0,
            "nonidentical_equal_width_total_pairs": 0,
            "bounded_BC_cases": 0,
            "empty_B_cases": 0,
            "empty_C_cases": 0,
            "nonsymmetric_B_cases": 0,
            "nonsymmetric_C_cases": 0,
            "actual_Hyp_cases": 0,
            "actual_Hyp_empty_B_cases": 0,
            "actual_Hyp_nonsymmetric_C_cases": 0,
            "outside_Hyp_cases": 0,
            "nonflipping_BC_cases": 0,
            "zero_signed_source_BC_cases": 0,
            "flipping_raw_center_cases": 0,
            "flipping_raw_center_g0_cases": 0,
            "flipping_raw_center_g1_cases": 0,
            "zero_signed_raw_images": 0,
            "explicit_trim_cases": 0,
            "maximum_center_width": 0,
        }

    def extractor(self, base, width, total):
        digits = fixed_digits(base, width, total)
        quotient = total // base ** width
        require(self.mirror.norm(base, [0] * width, total) == (digits, quotient),
                "zero-word normalization differs from fixed-width digits")
        require(value(base, digits) == total % base ** width,
                "fixed-width digits have the wrong remainder value")
        self.counts["fixed_digit_cases"] += 1
        self.counts["base_one_fixed_digit_cases"] += int(base == 1)
        return digits, quotient

    def normalization(self, base, word, incoming):
        expected = whole_normalization(base, word, incoming)
        require(self.mirror.norm(base, word, incoming) == expected,
                f"column normalization mismatch: {(base, word, incoming)}")
        self.counts["normalization_cases"] += 1
        return expected

    def same_total_pair(self, base, word, incoming):
        width = len(word)
        total = value(base, word) + incoming
        expected = self.extractor(base, width, total)
        original = self.normalization(base, word, incoming)
        if width:
            other_incoming = total // 2
            residual = total - other_incoming
            other_word = fixed_digits(base, width, residual)
            other_word[-1] += base * (residual // base ** width)
        else:
            other_word, other_incoming = [], total
        require(len(other_word) == width
                and value(base, other_word) + other_incoming == total,
                "same-total control construction failed")
        other = self.normalization(base, other_word, other_incoming)
        require(original == other == expected,
                "same width and value-plus-carry gave different normalization")
        self.counts["equal_width_total_pairs"] += 1
        self.counts["nonidentical_equal_width_total_pairs"] += int(
            (tuple(word), incoming) != (tuple(other_word), other_incoming))

    def flipping_center(self, base, center, incoming, overflow, actual_raw=None):
        require(base >= 2 and incoming in (0, 1) and overflow in (0, 1)
                and all(0 <= c <= 2 * (base - 1) for c in center),
                "raw-center control violates its hypotheses")
        width, power = len(center), base ** len(center)
        number = value(base, center)
        signed = number + 1 - power
        digits, outgoing = self.normalization(base, center, incoming)
        require(outgoing == 1 - incoming, "raw-center control requires a carry flip")
        require(signed != 0 and incoming == int(signed < 0),
                "flipping-center sign condition failed")
        padded = digits + [(base - 1) * incoming] * overflow
        expected_raw = pair_word(padded)
        # This second construction starts from the mirror's column digits.
        column_digits, column_carry = self.mirror.norm(base, center, incoming)
        require(column_carry == 1 - incoming, "mirror center did not flip")
        column_left = column_digits + [(base - 1) * incoming] * overflow
        column_right = [(base - 1) * incoming] * overflow + column_digits[::-1]
        column_raw = [left + right for left, right in zip(column_left, column_right)]
        require(column_raw == expected_raw, "whole-integer and column raw words differ")
        if actual_raw is not None:
            require(actual_raw == expected_raw, "actual Hyp nextC word differs")
        reversal = value(base, digits[::-1])
        raw_number = value(base, expected_raw)
        expected_number = ((number + incoming) % power + base ** overflow * reversal
                           + overflow * (base - 1) * incoming * (power + 1))
        require(raw_number == expected_number, "raw-center positional value formula failed")
        raw_signed = raw_number + 1 - base ** (width + overflow)
        expected_signed = signed + base ** overflow * (
            reversal + incoming * (power + 1) - power)
        require(raw_signed == expected_signed, "raw-center signed formula failed")
        require(len(expected_raw) == width + overflow
                and expected_raw == expected_raw[::-1]
                and all(0 <= c <= 2 * (base - 1) for c in expected_raw),
                "raw-center width/symmetry/alphabet control failed")
        self.counts["flipping_raw_center_cases"] += 1
        self.counts[f"flipping_raw_center_g{overflow}_cases"] += 1
        self.counts["zero_signed_raw_images"] += int(raw_signed == 0)
        self.counts["maximum_center_width"] = max(
            self.counts["maximum_center_width"], width)
        return expected_raw, signed, raw_signed

    def bounded_BC(self, base, exterior, center):
        require(base >= 2 and all(0 <= c <= 2 * (base - 1)
                                 for c in (*exterior, *center)),
                "bounded B/C control violates alphabet bounds")
        _, incoming = self.normalization(base, exterior, 0)
        digits, outgoing = self.normalization(base, center, incoming)
        _, overflow = self.normalization(base, exterior[::-1], outgoing)
        require(incoming in (0, 1) and outgoing in (0, 1) and overflow in (0, 1),
                "bounded B/C normalization produced a nonbit carry")
        require((self.mirror.e1(base, exterior), self.mirror.e2(base, exterior, center),
                 self.mirror.gam(base, exterior, center)) == (incoming, outgoing, overflow),
                "mirror stream labels differ from whole-integer normalization")
        expected_hyp = (not exterior or exterior[0] != 0) and incoming != outgoing
        actual_hyp = self.mirror.hyp(base, exterior, center)
        require(actual_hyp == expected_hyp, "mirror Hyp mismatch")
        raw = self.mirror.nextC(base, exterior, center)
        general_padded = digits + [(base - 1) * (1 - outgoing)] * overflow
        require(raw == pair_word(general_padded),
                "raw nextC definition failed on bounded control")
        signed = value(base, center) + 1 - base ** len(center)
        if signed == 0:
            require(incoming == outgoing and not actual_hyp,
                    "signed-zero center unexpectedly satisfies Hyp")
        counts = self.counts
        counts["bounded_BC_cases"] += 1
        counts["empty_B_cases"] += int(not exterior)
        counts["empty_C_cases"] += int(not center)
        counts["nonsymmetric_B_cases"] += int(exterior != exterior[::-1])
        counts["nonsymmetric_C_cases"] += int(center != center[::-1])
        counts["nonflipping_BC_cases"] += int(incoming == outgoing)
        counts["zero_signed_source_BC_cases"] += int(signed == 0)
        counts["actual_Hyp_cases" if actual_hyp else "outside_Hyp_cases"] += 1
        if actual_hyp:
            counts["actual_Hyp_empty_B_cases"] += int(not exterior)
            counts["actual_Hyp_nonsymmetric_C_cases"] += int(center != center[::-1])
            self.flipping_center(base, center, incoming, overflow, raw)
        return actual_hyp, incoming, outgoing, overflow, raw

    def trim(self, base, raw, target, trim):
        require(type(trim) is int and trim >= 0
                and raw == [base - 1] * trim + list(target) + [base - 1] * trim,
                "prescribed neutral-pair trim failed")
        raw_signed = value(base, raw) + 1 - base ** len(raw)
        target_signed = value(base, target) + 1 - base ** len(target)
        require(raw_signed == base ** trim * target_signed,
                "neutral-pair trim signed-value identity failed")
        self.counts["explicit_trim_cases"] += 1


def arithmetic_controls(audit):
    bases, maximum_width, maximum_total = (1, 2, 3, 10, 26), 6, 128
    for base in bases:
        for width in range(maximum_width + 1):
            for total in range(maximum_total + 1):
                audit.extractor(base, width, total)
    scopes = []
    for base in (1, 2, 3, 10):
        alphabet = sorted({0, 1, base - 1, base, base + 1, 2 * base - 1, base ** 2 + 3})
        carries = sorted({0, 1, 2, base, base ** 2 + 1})
        count = 0
        for width in range(4):
            for word in itertools.product(alphabet, repeat=width):
                for incoming in carries:
                    audit.same_total_pair(base, word, incoming)
                    count += 1
        scopes.append({"base": base, "maximum_width": 3, "alphabet": alphabet,
                       "incoming_carries": carries, "pairs": count})
    generator = random.Random(1120327)
    for _ in range(2000):
        base = generator.choice((1, 2, 3, 5, 10, 20, 26, 97))
        width = generator.randrange(65)
        word = tuple(generator.randrange(base ** 6 + 4) for _ in range(width))
        incoming = generator.randrange(base ** 10 + 4)
        audit.same_total_pair(base, word, incoming)
    require(audit.mirror.norm(10, [1], 0) != audit.mirror.norm(10, [1, 0], 0),
            "width-essential counterexample changed")
    return {"fixed_digits_exhaustive": {"bases": list(bases),
            "maximum_width": maximum_width, "maximum_total": maximum_total,
            "cases": len(bases) * (maximum_width + 1) * (maximum_total + 1)},
            "same_total_exhaustive": scopes, "random_seed": 1120327,
            "sampled_same_total_pairs": 2000, "sampled_maximum_width": 64,
            "sampled_bases": [1, 2, 3, 5, 10, 20, 26, 97],
            "width_essential_counterexample": {"base": 10, "word1": [1],
                                               "word2": [1, 0], "incoming": 0}}


def bounded_controls(audit):
    scopes = []
    for base, maximum_B, maximum_C in ((2, 2, 4), (3, 2, 3), (4, 1, 3), (10, 1, 2)):
        words = lambda maximum: [word for width in range(maximum + 1)
                                 for word in itertools.product(range(2 * base - 1), repeat=width)]
        exteriors, centers = words(maximum_B), words(maximum_C)
        before = audit.counts["actual_Hyp_cases"]
        for exterior in exteriors:
            for center in centers:
                audit.bounded_BC(base, exterior, center)
        scopes.append({"base": base, "maximum_B_width": maximum_B,
                       "maximum_C_width": maximum_C, "pairs": len(exteriors) * len(centers),
                       "actual_Hyp_pairs": audit.counts["actual_Hyp_cases"] - before})
    bases = (2, 3, 4, 5, 10, 11, 17, 20, 26, 32, 97)
    special = 0
    for base in bases:
        for exterior in ((), (1,), (base,), (2 * (base - 1),), (0, base), (1, 0, base)):
            for width in (0, 1, 2, 8):
                for coefficient in (0, base - 1, 2 * (base - 1)):
                    audit.bounded_BC(base, exterior, (coefficient,) * width)
                    special += 1
    generator = random.Random(1120331)
    for _ in range(4000):
        base = generator.choice(bases)
        exterior = tuple(generator.randrange(2 * base - 1)
                         for _ in range(generator.randrange(51)))
        center = tuple(generator.randrange(2 * base - 1)
                       for _ in range(generator.randrange(81)))
        audit.bounded_BC(base, exterior, center)
    # The signed formula substitutes e2=1-e1; it must not be asserted outside Hyp.
    hyp, incoming, outgoing, overflow, raw = audit.bounded_BC(10, (1,), (0,))
    actual_signed = value(10, raw) + 1 - 10 ** len(raw)
    wrongly_extended = -9 + 10 ** overflow * (0 + incoming * 11 - 10)
    require(not hyp and incoming == outgoing == overflow == 0
            and actual_signed == -9 and wrongly_extended == -19,
            "carry-flip-essential counterexample changed")
    return {"exhaustive": scopes, "special_BC_cases": special,
            "random_seed": 1120331, "sampled_BC_cases": 4000,
            "sampled_bases": list(bases), "sampled_maximum_B_width": 50,
            "sampled_maximum_C_width": 80,
            "nonflip_counterexample": {"base": 10, "B": [1], "C": [0],
                                       "e1": 0, "e2": 0, "g": 0,
                                       "actual_raw_signed": actual_signed,
                                       "wrongly_extended_signed": wrongly_extended}}


def known_certificates(audit):
    sources = audit.mirror._lean_certs()
    require({base for base, _ in sources} == {2, 4, 8, 11, 16, 17, 26, 32},
            "main-source certificate set changed")
    sources.append((20, fixtures.base20_fixture()))
    rows = []
    for base, edges in sorted(sources):
        cycle = [(list(b), list(c), list(b2), list(c2), u, v)
                 for b, c, b2, c2, u, v in edges]
        require(audit.mirror.cycleOK(base, cycle, cycle[0][0], cycle[0][1]),
                f"known base-{base} full certificate failed")
        for exterior, center, _, target, _, trim in cycle:
            hyp, _, _, _, raw = audit.bounded_BC(base, exterior, center)
            require(hyp, "known certificate edge did not satisfy Hyp")
            audit.trim(base, raw, target, trim)
        rows.append({"base": base, "edges": len(cycle)})
    return {"cycles": rows, "total_edges": sum(row["edges"] for row in rows),
            "full_mirror_cycles": len(rows), "base20_source": fixtures.BASE20_SOURCE}


def decimal_center_only(audit):
    initial = [9, 14, 13, 18, 13, 14, 9]
    carry_word = "010100110100101011001011"
    overflow_word = "110001001000110001001000"
    trim_word = "100001000000100001000000"
    require(len(carry_word) == len(overflow_word) == len(trim_word) == 24,
            "decimal center fixture stream length changed")
    require(carry_word[12:] == "".join(str(1 - int(bit)) for bit in carry_word[:12])
            and overflow_word[12:] == overflow_word[:12]
            and trim_word[12:] == trim_word[:12],
            "decimal fixture half-period stream relations changed")
    center, states, edges, signed_values, raw_signed_values = initial[:], [], [], [], []
    for incoming, overflow, trim in zip(map(int, carry_word), map(int, overflow_word),
                                        map(int, trim_word)):
        states.append(center[:])
        raw, signed, raw_signed = audit.flipping_center(10, center, incoming, overflow)
        require(2 * trim <= len(raw), "decimal center trim exceeds width")
        target = raw[trim:len(raw) - trim]
        audit.trim(10, raw, target, trim)
        require(target and len(target) == len(center) + overflow - 2 * trim,
                "decimal center target width failed")
        edges.append((center[:], target[:], incoming, overflow, trim))
        signed_values.append(signed)
        raw_signed_values.append(raw_signed)
        center = target
    require(center == initial, "decimal center-only return failed closure")
    require(len({tuple(state) for state in states}) == 24,
            "decimal fixture has repeated center states before its stated return")
    require(all(states[i + 12] == [18 - c for c in states[i]] for i in range(12)),
            "decimal fixture half-period complement changed")
    require(all(signed_values[i + 12] == -signed_values[i] for i in range(12)),
            "decimal fixture signed half-period complement changed")
    encoded = json.dumps(edges, separators=(",", ":")).encode("ascii")
    return {"scope": "CENTER-ONLY: no exterior B and no full B/C certificate claim",
            "source_agent": "Agent 101", "source_PR": "https://github.com/taco-jpg/p196-algorithm/pull/381",
            "source_issue_comment": "https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433181110",
            "manager_comment": "https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433247591",
            "base": 10, "edges": 24, "initial_C": initial, "e": carry_word,
            "g": overflow_word, "v": trim_word, "sum_g": sum(map(int, overflow_word)),
            "sum_v": sum(map(int, trim_word)), "widths": [len(state) for state in states],
            "signed_values": signed_values, "raw_signed_values": raw_signed_values,
            "half_period_coefficient_complement": True,
            "half_period_carry_complement": True,
            "half_period_overflow_and_trim_repeat": True,
            "canonical_center_edges_sha256": hashlib.sha256(encoded).hexdigest()}


def main():
    audit = Audit(fixtures.load_mirror())
    # Check the current decimal center fixture before the larger finite controls.
    decimal = decimal_center_only(audit)
    result = {"status": "COMPUTED", "decimal_center_only": decimal,
              "arithmetic": arithmetic_controls(audit),
              "bounded_controls": bounded_controls(audit),
              "known_certificates": known_certificates(audit), "totals": audit.counts}
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS: fixed digits, normalization determinism, raw-center arithmetic, and center-only P24.")


if __name__ == "__main__":
    main()
