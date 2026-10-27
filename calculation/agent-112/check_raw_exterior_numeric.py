#!/usr/bin/env python3
"""Independent finite controls for the actual A120 exterior numeric step.

The oracle uses whole-integer divisions and fixed-width digits. The comparison
uses the unchanged column mirror. For m=len(B), P=b**m, V=value(B),
H=value(reverse(B)), e=V//P, f=1-e, and g=(H+f)//P, it checks both the raw
word and its forward/reverse values. Direct bounded-B forced-complement
controls are labelled separately from B/C inputs satisfying actual Hyp.

This is one-step arithmetic validation, not an exterior cycle search or a
decimal certificate claim. No B is inferred from a center-only fixture.
Above-bound equal-value examples test generic normalization ONLY: the mirror's
xd uses signed Python subtraction outside its bounded-bit domain, whereas Lean
uses Nat subtraction. All checks have explicit failure branches under -O.
"""

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


def digits_at_width(base, width, number):
    return [number // base ** position % base for position in range(width)]


def reverse_at_width(base, width, number):
    # Evaluate directly from integer digit positions, not by calling the mirror.
    return sum((number // base ** position % base) * base ** (width - 1 - position)
               for position in range(width))


def numeric_step(base, width, forward, reverse):
    """Pure numeric oracle; its bit guards do not claim coefficient feasibility."""
    require(type(base) is int and base >= 2 and type(width) is int and width >= 0
            and type(forward) is int and forward >= 0
            and type(reverse) is int and reverse >= 0,
            "numeric oracle requires natural coordinates in base >= 2")
    power = base ** width
    incoming = forward // power
    require(incoming in (0, 1), "numeric oracle incoming carry is not a bit")
    complement = 1 - incoming
    overflow = (reverse + complement) // power
    require(overflow in (0, 1), "numeric oracle overflow is not a bit")
    left_digits = digits_at_width(base, width, forward)
    right_digits = digits_at_width(base, width, reverse + complement)
    padding = (base - 1) * complement
    left = left_digits + [padding] * overflow
    right = [1] * overflow + right_digits[::-1]
    raw = [a + b for a, b in zip(left, right)]
    raw_forward = (forward % power
                   + base ** overflow * reverse_at_width(base, width, reverse + complement)
                   + overflow * (1 + padding * power))
    raw_reverse = (base ** overflow * reverse_at_width(base, width, forward)
                   + (reverse + complement) % power + overflow * (power + padding))
    return {"m": width, "P": power, "V": forward, "H": reverse,
            "e": incoming, "f": complement, "g": overflow, "x": padding,
            "D": left_digits, "E": right_digits, "raw": raw,
            "raw_forward": raw_forward, "raw_reverse": raw_reverse}


class Audit:
    def __init__(self, mirror):
        self.mirror = mirror
        self.numeric_keys = {}
        self.actual_exteriors = {}
        self.actual_keys = {}
        self.counts = {
            "normalization_comparisons": 0,
            "base_one_normalization_comparisons": 0,
            "generic_equal_data_pairs": 0,
            "generic_equal_data_normalization_pairs": 0,
            "forced_complement_exterior_checks": 0,
            "direct_only_exterior_checks": 0,
            "forced_complement_empty_B_checks": 0,
            "forced_complement_zero_head_B_checks": 0,
            "forced_complement_nonsymmetric_B_checks": 0,
            "forced_complement_g0_checks": 0,
            "forced_complement_g1_checks": 0,
            "same_numeric_key_rechecks": 0,
            "nonidentical_bounded_words_with_same_numeric_key": 0,
            "bounded_BC_cases": 0,
            "actual_Hyp_cases": 0,
            "actual_Hyp_empty_B_cases": 0,
            "actual_Hyp_nonsymmetric_B_cases": 0,
            "actual_Hyp_nonsymmetric_C_cases": 0,
            "outside_Hyp_cases": 0,
            "nonflipping_BC_cases": 0,
            "same_B_new_admissible_C_comparisons": 0,
            "same_actual_numeric_key_comparisons": 0,
            "known_exterior_trim_checks": 0,
            "maximum_B_width": 0,
            "maximum_C_width": 0,
        }

    def normalization(self, base, word, incoming):
        require(type(base) is int and base >= 1
                and type(incoming) is int and incoming >= 0
                and all(type(c) is int and c >= 0 for c in word),
                "normalization control requires positive base and natural data")
        total, width = value(base, word) + incoming, len(word)
        expected = (digits_at_width(base, width, total), total // base ** width)
        require(self.mirror.norm(base, word, incoming) == expected,
                f"whole-integer normalization mismatch: {(base, word, incoming)}")
        require(value(base, expected[0]) == total % base ** width,
                "fixed-width remainder value failed")
        require(value(base, expected[0][::-1]) == reverse_at_width(base, width, total),
                "fixed-width reversed value failed")
        self.counts["normalization_comparisons"] += 1
        self.counts["base_one_normalization_comparisons"] += int(base == 1)
        return expected

    def exterior(self, base, exterior, direct_only=True):
        exterior = tuple(exterior)
        require(base >= 2 and all(0 <= c <= 2 * (base - 1) for c in exterior),
                "exterior control requires the bounded coefficient alphabet")
        width = len(exterior)
        forward, reverse = value(base, exterior), value(base, exterior[::-1])
        data = numeric_step(base, width, forward, reverse)
        digits, incoming = self.normalization(base, exterior, 0)
        reverse_digits, overflow = self.normalization(base, exterior[::-1], 1 - incoming)
        require((digits, reverse_digits, incoming, overflow)
                == (data["D"], data["E"], data["e"], data["g"]),
                "exterior numeric digits/labels differ from column normalization")
        require(self.mirror.e1(base, exterior) == incoming
                and self.mirror.DB(base, exterior) == digits
                and self.mirror.xd(base, exterior) == data["x"],
                "exterior-only mirror definitions differ")
        if overflow == 0:
            column_raw = [a + b for a, b in zip(digits, reverse_digits[::-1])]
        else:
            column_raw = [a + b for a, b in zip(
                digits + [(base - 1) * (1 - incoming)], [1] + reverse_digits[::-1])]
        raw = data["raw"]
        require(raw == column_raw, "raw exterior literal-word formula failed")
        require(value(base, raw) == data["raw_forward"],
                "raw exterior forward-value formula failed")
        require(value(base, raw[::-1]) == data["raw_reverse"],
                "raw exterior reverse-value formula failed")
        require(len(raw) == width + overflow
                and all(0 <= c <= 2 * (base - 1) for c in raw),
                "raw exterior width/alphabet control failed")
        key = (base, width, forward, reverse)
        output = (tuple(raw), incoming, overflow, data["raw_forward"], data["raw_reverse"])
        if key in self.numeric_keys:
            old_word, old_output = self.numeric_keys[key]
            require(output == old_output, "equal numeric exterior data changed output")
            self.counts["same_numeric_key_rechecks"] += 1
            self.counts["nonidentical_bounded_words_with_same_numeric_key"] += int(
                exterior != old_word)
        else:
            self.numeric_keys[key] = (exterior, output)
        counts = self.counts
        counts["forced_complement_exterior_checks"] += 1
        counts["direct_only_exterior_checks"] += int(direct_only)
        counts["forced_complement_empty_B_checks"] += int(not exterior)
        counts["forced_complement_zero_head_B_checks"] += int(bool(exterior) and exterior[0] == 0)
        counts["forced_complement_nonsymmetric_B_checks"] += int(exterior != exterior[::-1])
        counts[f"forced_complement_g{overflow}_checks"] += 1
        counts["maximum_B_width"] = max(counts["maximum_B_width"], width)
        return data

    def actual_BC(self, base, exterior, center):
        exterior, center = tuple(exterior), tuple(center)
        require(base >= 2 and all(0 <= c <= 2 * (base - 1)
                                 for c in (*exterior, *center)),
                "actual-Hyp controls require bounded natural B/C")
        incoming = value(base, exterior) // base ** len(exterior)
        _, actual_outgoing = self.normalization(base, center, incoming)
        expected_hyp = (not exterior or exterior[0] != 0) and incoming != actual_outgoing
        actual_hyp = self.mirror.hyp(base, exterior, center)
        require(actual_hyp == expected_hyp, "actual mirror Hyp disagrees with integer gate")
        counts = self.counts
        counts["bounded_BC_cases"] += 1
        counts["actual_Hyp_cases" if actual_hyp else "outside_Hyp_cases"] += 1
        counts["nonflipping_BC_cases"] += int(incoming == actual_outgoing)
        counts["maximum_C_width"] = max(counts["maximum_C_width"], len(center))
        if not actual_hyp:
            return None
        data = self.exterior(base, exterior, direct_only=False)
        require(actual_outgoing == data["f"]
                and self.mirror.e2(base, exterior, center) == data["f"]
                and self.mirror.gam(base, exterior, center) == data["g"]
                and self.mirror.DR(base, exterior, center) == data["E"],
                "actual Hyp stream/digit labels disagree with exterior data")
        actual_raw = self.mirror.nextB(base, exterior, center)
        require(actual_raw == data["raw"], "actual Hyp nextB literal word differs")
        require((value(base, actual_raw), value(base, actual_raw[::-1]))
                == (data["raw_forward"], data["raw_reverse"]),
                "actual Hyp nextB double-value formulas differ")
        output = (tuple(actual_raw), data["e"], data["g"])
        key = (base, exterior)
        if key in self.actual_exteriors:
            old_output, centers = self.actual_exteriors[key]
            require(output == old_output, "changing an admissible C changed B output")
            if center not in centers:
                counts["same_B_new_admissible_C_comparisons"] += 1
                centers.add(center)
        else:
            self.actual_exteriors[key] = (output, {center})
        numeric_key = (base, data["m"], data["V"], data["H"])
        if numeric_key in self.actual_keys:
            require(self.actual_keys[numeric_key] == output,
                    "same numeric key changed actual Hyp nextB")
            counts["same_actual_numeric_key_comparisons"] += 1
        else:
            self.actual_keys[numeric_key] = output
        counts["actual_Hyp_empty_B_cases"] += int(not exterior)
        counts["actual_Hyp_nonsymmetric_B_cases"] += int(exterior != exterior[::-1])
        counts["actual_Hyp_nonsymmetric_C_cases"] += int(center != center[::-1])
        return data


def direct_exterior_controls(audit):
    scopes = []
    for base, maximum in ((2, 6), (3, 5), (4, 4), (10, 3), (11, 3),
                          (17, 2), (20, 2), (26, 2), (32, 2)):
        count = 0
        for width in range(maximum + 1):
            for exterior in itertools.product(range(2 * base - 1), repeat=width):
                audit.exterior(base, exterior)
                count += 1
        scopes.append({"base": base, "maximum_B_width": maximum, "words": count})
    generator = random.Random(1120401)
    bases = (2, 3, 4, 5, 10, 11, 17, 20, 26, 32, 97)
    for _ in range(4000):
        base = generator.choice(bases)
        exterior = tuple(generator.randrange(2 * base - 1)
                         for _ in range(generator.randrange(101)))
        audit.exterior(base, exterior)
    return {"scope": "bounded B with forced complementary carry; no C feasibility inference",
            "exhaustive": scopes, "random_seed": 1120401, "sampled_words": 4000,
            "sampled_bases": list(bases), "sampled_maximum_B_width": 100}


def actual_hyp_controls(audit):
    scopes = []
    for base, maximum_B, maximum_C in ((2, 2, 4), (3, 2, 3), (4, 1, 3), (10, 1, 2)):
        words = lambda maximum: [word for width in range(maximum + 1)
                                 for word in itertools.product(range(2 * base - 1), repeat=width)]
        exteriors, centers = words(maximum_B), words(maximum_C)
        before = audit.counts["actual_Hyp_cases"]
        for exterior in exteriors:
            for center in centers:
                audit.actual_BC(base, exterior, center)
        scopes.append({"base": base, "maximum_B_width": maximum_B,
                       "maximum_C_width": maximum_C, "BC_cases": len(exteriors) * len(centers),
                       "actual_Hyp_cases": audit.counts["actual_Hyp_cases"] - before})
    bases = (2, 3, 4, 5, 10, 11, 17, 20, 26, 32, 97)
    special = 0
    for base in bases:
        for exterior in ((), (1,), (base,), (2 * (base - 1),), (0, base), (1, 0, base)):
            for width in (0, 1, 2, 8):
                for coefficient in (0, base - 1, 2 * (base - 1)):
                    audit.actual_BC(base, exterior, (coefficient,) * width)
                    special += 1
    generator = random.Random(1120402)
    for _ in range(4000):
        base = generator.choice(bases)
        exterior = tuple(generator.randrange(2 * base - 1)
                         for _ in range(generator.randrange(51)))
        center = tuple(generator.randrange(2 * base - 1)
                       for _ in range(generator.randrange(81)))
        audit.actual_BC(base, exterior, center)
    return {"scope": "all bounded C in each exhaustive range are checked against actual Hyp",
            "exhaustive": scopes, "special_BC_cases": special, "random_seed": 1120402,
            "sampled_BC_cases": 4000, "sampled_bases": list(bases),
            "sampled_maximum_B_width": 50, "sampled_maximum_C_width": 80}


def generic_equal_data_controls(audit):
    rows = []
    for base in (1, 2, 3, 10, 20, 97):
        carries = sorted({0, 1, 2, base + 1, base ** 2 + 3})
        pair_count = normalization_pairs = 0
        for prefix, suffix in (((), ()), ((1,), ()), ((), (2,)), ((3, 1), (4,))):
            left = prefix + (base, 0, base) + suffix
            right = prefix + (0, base ** 2 + 1, 0) + suffix
            require(left != right and len(left) == len(right)
                    and value(base, left) == value(base, right)
                    and value(base, left[::-1]) == value(base, right[::-1]),
                    "generic equal-double-value construction failed")
            require(any(c > 2 * (base - 1) for c in right),
                    "above-bound control unexpectedly lies in the bounded alphabet")
            for incoming in carries:
                for a, b in ((left, right), (left[::-1], right[::-1])):
                    require(audit.normalization(base, a, incoming)
                            == audit.normalization(base, b, incoming),
                            "generic equal-data normalization determinism failed")
                    normalization_pairs += 1
            pair_count += 1
        audit.counts["generic_equal_data_pairs"] += pair_count
        audit.counts["generic_equal_data_normalization_pairs"] += normalization_pairs
        rows.append({"base": base, "word_pairs": pair_count,
                     "incoming_carries": carries, "normalization_pairs": normalization_pairs})
    return {"scope": "generic normalization only; no Hyp or exterior-step assertion",
            "construction": "common padding around [b,0,b] versus [0,b^2+1,0]",
            "rows": rows}


def boundary_controls(audit):
    empty_rows = []
    for base in (2, 3, 4, 5, 10, 11, 17, 20, 26, 32, 97):
        data = audit.actual_BC(base, (), (base,))
        require(data is not None and data["m"] == 0 and data["P"] == 1
                and data["V"] == data["H"] == data["e"] == 0
                and data["f"] == data["g"] == 1 and data["D"] == data["E"] == []
                and data["raw"] == [base]
                and data["raw_forward"] == data["raw_reverse"] == base,
                "empty-B actual-Hyp control failed")
        empty_rows.append({"base": base, "B": [], "C": [base], "raw_B": data["raw"]})
    narrow = audit.actual_BC(10, (11,), (0,))
    wide = audit.actual_BC(10, (1, 1), (10,))
    require(narrow is not None and wide is not None
            and (narrow["V"], narrow["H"]) == (wide["V"], wide["H"]) == (11, 11)
            and (narrow["m"], wide["m"]) == (1, 2)
            and narrow["raw"] == [2, 1] and wide["raw"] == [2, 3],
            "actual-Hyp width-essential counterexample failed")
    reverse_changed = audit.actual_BC(10, (11, 0), (10,))
    require(reverse_changed is not None
            and (reverse_changed["m"], reverse_changed["V"]) == (wide["m"], wide["V"]) == (2, 11)
            and reverse_changed["H"] == 110 and wide["H"] == 11
            and reverse_changed["raw"] == [2, 2, 10] and wide["raw"] == [2, 3],
            "actual-Hyp reverse-value-essential counterexample failed")
    require(audit.actual_BC(10, (1,), (0,)) is None,
            "nonflip counterexample unexpectedly satisfies Hyp")
    forced = audit.exterior(10, (1,))
    require(audit.mirror.nextB(10, (1,), (0,)) == [2] and forced["raw"] == [3],
            "carry-flip-essential counterexample failed")
    return {"empty_B_actual_Hyp": empty_rows,
            "width_essential": {"base": 10, "VH": [11, 11],
                                "B1": [11], "C1": [0], "raw1": narrow["raw"],
                                "B2": [1, 1], "C2": [10], "raw2": wide["raw"]},
            "reverse_value_essential": {"base": 10, "width": 2, "V": 11, "C": [10],
                                        "B1": [11, 0], "H1": 110, "raw1": reverse_changed["raw"],
                                        "B2": [1, 1], "H2": 11, "raw2": wide["raw"]},
            "carry_flip_essential": {"base": 10, "B": [1], "C": [0],
                                     "actual_Hyp": False, "actual_raw": [2],
                                     "wrongly_forced_complement_raw": [3]}}


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
                f"known base-{base} full mirror certificate failed")
        for exterior, center, target, _, trim, _ in cycle:
            data = audit.actual_BC(base, exterior, center)
            require(data is not None and data["raw"] == target + [base - 1] * trim,
                    "known exterior edge/trim differs from numeric step")
            require(value(base, target) + base ** len(target) * (base ** trim - 1)
                    == data["raw_forward"], "known exterior trim forward value failed")
            require(base ** trim * value(base, target[::-1]) + base ** trim - 1
                    == data["raw_reverse"], "known exterior trim reverse value failed")
            audit.counts["known_exterior_trim_checks"] += 1
        rows.append({"base": base, "edges": len(cycle)})
    return {"cycles": rows, "total_edges": sum(row["edges"] for row in rows),
            "full_mirror_cycles": len(rows), "base20_source": fixtures.BASE20_SOURCE}


def main():
    audit = Audit(fixtures.load_mirror())
    result = {"status": "COMPUTED", "boundaries": boundary_controls(audit),
              "direct_exterior": direct_exterior_controls(audit),
              "actual_Hyp": actual_hyp_controls(audit),
              "generic_normalization_only": generic_equal_data_controls(audit),
              "known_certificates": known_certificates(audit)}
    audit.counts["distinct_bounded_numeric_keys_checked"] = len(audit.numeric_keys)
    audit.counts["distinct_actual_Hyp_exteriors_checked"] = len(audit.actual_exteriors)
    audit.counts["actual_Hyp_exteriors_with_multiple_C"] = sum(
        len(centers) > 1 for _, centers in audit.actual_exteriors.values())
    result["totals"] = audit.counts
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS: raw exterior word/double-value formulas and actual-Hyp center independence.")


if __name__ == "__main__":
    main()
