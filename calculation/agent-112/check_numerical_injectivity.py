#!/usr/bin/env python3
"""Complete finite dictionary controls for bounded numerical word encodings.

For each declared base and every width from zero through the declared maximum,
enumerate every coefficient word in [0,2*(b-1)] and check injectivity of
(forward value, reversed value). Independently enumerate every symmetric word
in the declared symmetric scopes and check injectivity of Z=value+1-b**width.
The zero-Z iff all-neutral equivalence is checked on ALL bounded words in the
first enumeration, without a symmetry assumption, and on the symmetric scopes.

These are finite COMPUTED results, not an all-width/all-base proof. There is no
random sampling, pairwise quadratic comparison, dynamics, or cycle search.
Boundary examples show why width, the reversed value, and coefficient bounds
matter. The above-bound symmetric collision is a known example from Agent 112
PR #349 / prior Agent 5 work; this script makes no sharp-threshold claim.
Every check uses an explicit failure branch, including under python -O.
"""

import itertools
import json


FULL_SCOPES = ((2, 9), (3, 6), (4, 5), (5, 4), (10, 4), (11, 3),
               (17, 3), (20, 3), (26, 2), (32, 2), (97, 2))
SYMMETRIC_SCOPES = ((2, 16), (3, 12), (4, 10), (5, 8), (10, 8), (11, 6),
                    (17, 6), (20, 4), (26, 4), (32, 4), (97, 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def double_value(base, word):
    """Forward evaluation by positional weights, reverse evaluation by Horner."""
    forward, reverse, weight = 0, 0, 1
    for coefficient in word:
        forward += coefficient * weight
        reverse = base * reverse + coefficient
        weight *= base
    return forward, reverse


def signed_value(base, word):
    return double_value(base, word)[0] + 1 - base ** len(word)


def bounded(base, word):
    return base >= 2 and all(0 <= coefficient <= 2 * (base - 1) for coefficient in word)


def complete_word_controls(totals):
    rows = []
    for base, maximum_width in FULL_SCOPES:
        alphabet_size = 2 * base - 1
        counts_by_width = []
        symmetric_count = nonsymmetric_count = zero_count = 0
        for width in range(maximum_width + 1):
            seen = {}
            neutral = (base - 1,) * width
            power = base ** width
            width_count = width_zeros = width_symmetric = 0
            for word in itertools.product(range(alphabet_size), repeat=width):
                key = double_value(base, word)
                previous = seen.get(key)
                if previous is not None:
                    raise RuntimeError(
                        f"bounded double-value collision: b={base}, width={width}, "
                        f"key={key}, words={previous},{word}")
                seen[key] = word
                signed_zero = key[0] + 1 - power == 0
                is_neutral = word == neutral
                require(signed_zero == is_neutral,
                        f"all-word zero characterization failed: {(base, word, key)}")
                is_symmetric = word == word[::-1]
                if is_symmetric:
                    require(key[0] == key[1], "symmetric word has unequal evaluations")
                width_count += 1
                width_zeros += int(signed_zero)
                width_symmetric += int(is_symmetric)
                totals["complete_word_nonsymmetric_zero_states"] += int(
                    signed_zero and not is_symmetric)
            expected_count = alphabet_size ** width
            expected_symmetric = alphabet_size ** ((width + 1) // 2)
            require(width_count == len(seen) == expected_count,
                    "complete word enumeration/dictionary cardinality failed")
            require(width_symmetric == expected_symmetric and width_zeros == 1,
                    "complete word symmetry/neutral cardinality failed")
            counts_by_width.append(width_count)
            symmetric_count += width_symmetric
            nonsymmetric_count += width_count - width_symmetric
            zero_count += width_zeros
            totals["complete_word_width_scopes"] += 1
            totals["complete_word_empty_states"] += int(width == 0)
        states = sum(counts_by_width)
        totals["complete_word_states"] += states
        totals["complete_word_symmetric_states"] += symmetric_count
        totals["complete_word_nonsymmetric_states"] += nonsymmetric_count
        totals["complete_word_zero_equivalence_checks"] += states
        totals["complete_word_zero_states"] += zero_count
        totals["complete_word_base2_states"] += states if base == 2 else 0
        rows.append({"base": base, "coefficient_maximum": 2 * (base - 1),
                     "minimum_width": 0, "maximum_width": maximum_width,
                     "states_by_width": counts_by_width, "states": states,
                     "symmetric_states": symmetric_count,
                     "nonsymmetric_states": nonsymmetric_count,
                     "zero_signed_states": zero_count,
                     "double_value_dictionary_collisions": 0})
    return rows


def complete_symmetric_controls(totals):
    rows = []
    for base, maximum_width in SYMMETRIC_SCOPES:
        alphabet_size = 2 * base - 1
        counts_by_width = []
        zero_count = negative_count = positive_count = 0
        for width in range(maximum_width + 1):
            seen = {}
            power = base ** width
            neutral = (base - 1,) * width
            width_count = width_zeros = 0
            for half in itertools.product(range(alphabet_size), repeat=(width + 1) // 2):
                word = half + half[:width // 2][::-1]
                require(len(word) == width and word == word[::-1],
                        "symmetric enumeration construction failed")
                forward, reverse = double_value(base, word)
                require(forward == reverse, "symmetric evaluations differ")
                signed = forward + 1 - power
                previous = seen.get(signed)
                if previous is not None:
                    raise RuntimeError(
                        f"bounded symmetric signed-value collision: b={base}, width={width}, "
                        f"Z={signed}, words={previous},{word}")
                seen[signed] = word
                require((signed == 0) == (word == neutral),
                        f"symmetric zero characterization failed: {(base, word, signed)}")
                width_count += 1
                width_zeros += int(signed == 0)
                negative_count += int(signed < 0)
                positive_count += int(signed > 0)
            expected_count = alphabet_size ** ((width + 1) // 2)
            require(width_count == len(seen) == expected_count and width_zeros == 1,
                    "complete symmetric enumeration/dictionary cardinality failed")
            counts_by_width.append(width_count)
            zero_count += width_zeros
            totals["complete_symmetric_width_scopes"] += 1
            totals["complete_symmetric_empty_states"] += int(width == 0)
        states = sum(counts_by_width)
        require(negative_count + positive_count + zero_count == states
                and negative_count == positive_count,
                "symmetric signed-state counts failed complement control")
        totals["complete_symmetric_states"] += states
        totals["complete_symmetric_zero_equivalence_checks"] += states
        totals["complete_symmetric_zero_states"] += zero_count
        totals["complete_symmetric_negative_states"] += negative_count
        totals["complete_symmetric_positive_states"] += positive_count
        totals["complete_symmetric_base2_states"] += states if base == 2 else 0
        rows.append({"base": base, "coefficient_maximum": 2 * (base - 1),
                     "minimum_width": 0, "maximum_width": maximum_width,
                     "states_by_width": counts_by_width, "states": states,
                     "zero_signed_states": zero_count,
                     "negative_signed_states": negative_count,
                     "positive_signed_states": positive_count,
                     "signed_value_dictionary_collisions": 0})
    return rows


def boundary_controls(totals):
    forward_left, forward_right = (11, 0), (1, 1)
    require(bounded(10, forward_left) and bounded(10, forward_right)
            and len(forward_left) == len(forward_right) == 2
            and double_value(10, forward_left) == (11, 110)
            and double_value(10, forward_right) == (11, 11),
            "bounded forward-value-only counterexample failed")
    width_left, width_right = (11,), (1, 1)
    require(bounded(10, width_left) and bounded(10, width_right)
            and len(width_left) != len(width_right)
            and double_value(10, width_left) == double_value(10, width_right) == (11, 11),
            "bounded double-value width counterexample failed")
    center_left, center_right = (10, 10), (10, 0, 10)
    require(bounded(10, center_left) and bounded(10, center_right)
            and center_left == center_left[::-1] and center_right == center_right[::-1]
            and len(center_left) != len(center_right)
            and signed_value(10, center_left) == signed_value(10, center_right) == 11,
            "bounded symmetric signed-value width counterexample failed")
    totals["bounded_boundary_counterexamples"] = 3
    symmetric_rows, zero_rows = [], []
    for base in (2, 3, 4, 5, 10, 11, 17, 20, 26, 32, 97):
        bound = 2 * (base - 1)
        coefficient = base ** 2 - base + 1
        left, right = (base, 0, 0, base), (0, coefficient, coefficient, 0)
        require(left != right and left == left[::-1] and right == right[::-1]
                and len(left) == len(right) == 4
                and bounded(base, left) and not bounded(base, right)
                and coefficient > bound
                and double_value(base, left) == double_value(base, right)
                == (base ** 4 + base, base ** 4 + base)
                and signed_value(base, left) == signed_value(base, right) == base + 1,
                "known above-bound symmetric collision failed")
        symmetric_rows.append({"base": base, "bounded_coefficient_maximum": bound,
                               "collision_coefficient_M": coefficient,
                               "M_minus_bound": coefficient - bound,
                               "left": list(left), "right": list(right),
                               "forward_and_reverse_value": base ** 4 + base,
                               "signed_value": base + 1})
        zero_left, zero_right = (2 * base - 1, base - 2), (base - 1, base - 1)
        require(zero_left != zero_right and zero_left != zero_left[::-1]
                and not bounded(base, zero_left) and bounded(base, zero_right)
                and max(zero_left) == bound + 1
                and signed_value(base, zero_left) == signed_value(base, zero_right) == 0
                and double_value(base, zero_left)[1] != double_value(base, zero_right)[1],
                "above-bound nonsymmetric neutral-value collision failed")
        zero_rows.append({"base": base, "bounded_coefficient_maximum": bound,
                          "collision_coefficient_maximum": bound + 1,
                          "nonsymmetric_word": list(zero_left), "neutral_word": list(zero_right),
                          "forward_value": base ** 2 - 1, "signed_value": 0,
                          "reversed_values_differ": True})
    totals["above_bound_symmetric_collision_examples"] = len(symmetric_rows)
    totals["above_bound_zero_collision_examples"] = len(zero_rows)
    return {
        "forward_value_alone": {"base": 10, "width": 2,
                                "left": list(forward_left), "right": list(forward_right),
                                "left_VH": [11, 110], "right_VH": [11, 11]},
        "double_value_requires_width": {"base": 10, "left": list(width_left),
                                        "right": list(width_right), "shared_VH": [11, 11]},
        "symmetric_signed_value_requires_width": {"base": 10, "left": list(center_left),
                                                  "right": list(center_right), "shared_Z": 11},
        "above_bound_symmetric_collisions": {
            "scope": "known explicit failures beyond the tested bound; no sharp classification claim",
            "source": "Agent 112 PR349 PAPER / prior Agent 5 decimal example", "examples": symmetric_rows},
        "above_bound_nonsymmetric_zero_collisions": {
            "scope": "zero characterization fails when bound is increased by one; reversed values differ",
            "examples": zero_rows},
    }


def main():
    totals = {
        "complete_word_width_scopes": 0, "complete_word_states": 0,
        "complete_word_symmetric_states": 0, "complete_word_nonsymmetric_states": 0,
        "complete_word_empty_states": 0, "complete_word_base2_states": 0,
        "complete_word_zero_equivalence_checks": 0, "complete_word_zero_states": 0,
        "complete_word_nonsymmetric_zero_states": 0,
        "complete_symmetric_width_scopes": 0, "complete_symmetric_states": 0,
        "complete_symmetric_empty_states": 0, "complete_symmetric_base2_states": 0,
        "complete_symmetric_zero_equivalence_checks": 0,
        "complete_symmetric_zero_states": 0, "complete_symmetric_negative_states": 0,
        "complete_symmetric_positive_states": 0,
    }
    result = {"status": "COMPUTED", "sampling": "none; every declared width is complete",
              "boundaries": boundary_controls(totals),
              "complete_arbitrary_word_scopes": complete_word_controls(totals),
              "complete_symmetric_word_scopes": complete_symmetric_controls(totals),
              "totals": totals}
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS: complete finite double-value/symmetric-Z dictionaries and all-word zero characterization.")


if __name__ == "__main__":
    main()
