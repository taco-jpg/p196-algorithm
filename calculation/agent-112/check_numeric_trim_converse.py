#!/usr/bin/env python3
"""Complete finite controls for the signed-value neutral-trim converse.

For every bounded symmetric word in each declared base/width range, test every
natural v with 2*v <= width. Divisibility of Z by b**v must be equivalent to
literal neutral padding at both ends. On every successful premise, check the
middle's width, bounds, symmetry, exact signed quotient, and literal recovery.
Complete fixed-width middle dictionaries also check uniqueness in those finite
domains. Source values use direct positional sums; middle values use Horner.

The known nine full-certificate fixtures and Agent 101's decimal P24 CENTER-ONLY
fixture supply additional actual trim edges. The latter supplies no exterior B
or full decimal certificate. Four failed-premise examples are word arithmetic
only; invalid Hyp inputs are never passed through the mirror's next-step code.
These are finite COMPUTED controls, not an all-width proof. There is no sampling.
All checks use explicit failure branches and remain active under python -O.
"""

import itertools
import json

import check_normalization_arithmetic as fixtures
import check_raw_center_numeric as center_fixture


SCOPES = ((2, 14), (3, 10), (4, 8), (5, 6), (10, 8), (11, 6),
          (17, 4), (20, 4), (26, 4), (32, 4), (97, 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def value_sum(base, word):
    return sum(coefficient * base ** position
               for position, coefficient in enumerate(word))


def value_horner(base, word):
    result = 0
    for coefficient in reversed(word):
        result = base * result + coefficient
    return result


def signed_sum(base, word):
    return value_sum(base, word) + 1 - base ** len(word)


def signed_horner(base, word):
    return value_horner(base, word) + 1 - base ** len(word)


def literal_middle(base, word, trim):
    """Return the only possible literal middle, or None if padding is absent."""
    if 2 * trim > len(word):
        return None
    middle = tuple(word[trim:len(word) - trim])
    padding = (base - 1,) * trim
    return middle if tuple(word) == padding + middle + padding else None


class Audit:
    def __init__(self):
        self.counts = {
            "finite_base_width_scopes": 0,
            "finite_symmetric_words": 0,
            "finite_empty_words": 0,
            "finite_base2_words": 0,
            "finite_composite_base_words": 0,
            "finite_zero_Z_words": 0,
            "finite_negative_Z_words": 0,
            "finite_positive_Z_words": 0,
            "finite_allowed_v_queries": 0,
            "finite_v_zero_queries": 0,
            "finite_divisible_queries": 0,
            "finite_nondivisible_queries": 0,
            "finite_positive_v_divisible_queries": 0,
            "finite_zero_Z_divisible_queries": 0,
            "finite_negative_Z_divisible_queries": 0,
            "finite_positive_Z_divisible_queries": 0,
            "finite_empty_middle_queries": 0,
            "finite_positive_v_full_trims": 0,
            "finite_unique_middle_dictionary_checks": 0,
            "literal_middle_recovery_checks": 0,
            "known_certificate_trim_edges": 0,
            "decimal_center_only_trim_edges": 0,
            "selected_positive_v_trim_edges": 0,
            "maximum_tested_word_width": 0,
            "maximum_tested_trim": 0,
        }

    def trim(self, base, word, trim, signed=None):
        word = tuple(word)
        require(base >= 2 and word == word[::-1]
                and all(0 <= c <= 2 * (base - 1) for c in word)
                and type(trim) is int and 0 <= 2 * trim <= len(word),
                "trim control violates base/bounds/symmetry/width premises")
        if signed is None:
            signed = signed_sum(base, word)
            require(signed == signed_horner(base, word), "source evaluations disagree")
        divisor = base ** trim
        divisible = signed % divisor == 0
        middle = literal_middle(base, word, trim)
        require(divisible == (middle is not None),
                f"numerical/literal trim mismatch: {(base, word, trim, signed)}")
        if not divisible:
            return None
        require(middle is not None and len(middle) == len(word) - 2 * trim
                and middle == middle[::-1]
                and all(0 <= c <= 2 * (base - 1) for c in middle),
                "trimmed middle width/bounds/symmetry failed")
        quotient = signed // divisor
        require(signed_horner(base, middle) == quotient
                and divisor * signed_horner(base, middle) == signed,
                "trimmed middle signed quotient failed")
        # Check both endpoint removals and an independent one-pair-at-a-time peel.
        padding = (base - 1,) * trim
        require(word[trim:] == middle + padding
                and word[:len(word) - trim] == padding + middle,
                "literal middle cancellation failed")
        peeled = word
        for _ in range(trim):
            require(len(peeled) >= 2 and peeled[0] == peeled[-1] == base - 1,
                    "successive neutral-pair removal failed")
            peeled = peeled[1:-1]
        require(peeled == middle, "successive and indexed middle recovery differ")
        self.counts["literal_middle_recovery_checks"] += 1
        self.counts["maximum_tested_word_width"] = max(
            self.counts["maximum_tested_word_width"], len(word))
        self.counts["maximum_tested_trim"] = max(self.counts["maximum_tested_trim"], trim)
        return middle


def complete_controls(audit):
    rows = []
    for base, maximum_width in SCOPES:
        alphabet_size = 2 * base - 1
        middle_dictionaries = []
        words_by_width, queries_by_width, divisible_by_width = [], [], []
        positive_trim_count = 0
        composite = any(base % divisor == 0 for divisor in range(2, base))
        for width in range(maximum_width + 1):
            dictionary = {}
            middle_dictionaries.append(dictionary)
            successful_by_v = [0] * (width // 2 + 1)
            word_count = query_count = 0
            for half in itertools.product(range(alphabet_size), repeat=(width + 1) // 2):
                word = half + half[:width // 2][::-1]
                require(len(word) == width and word == word[::-1],
                        "complete symmetric enumeration failed")
                signed = signed_sum(base, word)
                require(signed == signed_horner(base, word), "source evaluation oracles disagree")
                require(signed not in dictionary,
                        "fixed-width middle dictionary has a signed-value collision")
                dictionary[signed] = word
                counts = audit.counts
                counts["finite_zero_Z_words"] += int(signed == 0)
                counts["finite_negative_Z_words"] += int(signed < 0)
                counts["finite_positive_Z_words"] += int(signed > 0)
                for trim in range(width // 2 + 1):
                    middle = audit.trim(base, word, trim, signed)
                    query_count += 1
                    counts["finite_v_zero_queries"] += int(trim == 0)
                    if middle is None:
                        counts["finite_nondivisible_queries"] += 1
                        continue
                    successful_by_v[trim] += 1
                    quotient = signed // base ** trim
                    target_width = width - 2 * trim
                    require(middle_dictionaries[target_width].get(quotient) == middle,
                            "complete target dictionary does not identify the unique middle")
                    counts["finite_unique_middle_dictionary_checks"] += 1
                    counts["finite_positive_v_divisible_queries"] += int(trim > 0)
                    counts["finite_zero_Z_divisible_queries"] += int(signed == 0)
                    counts["finite_negative_Z_divisible_queries"] += int(signed < 0)
                    counts["finite_positive_Z_divisible_queries"] += int(signed > 0)
                    counts["finite_empty_middle_queries"] += int(not middle)
                    counts["finite_positive_v_full_trims"] += int(trim > 0 and not middle)
                    positive_trim_count += int(trim > 0)
                word_count += 1
            expected_words = alphabet_size ** ((width + 1) // 2)
            expected_successes = [alphabet_size ** ((width - 2 * trim + 1) // 2)
                                  for trim in range(width // 2 + 1)]
            require(word_count == len(dictionary) == expected_words
                    and query_count == expected_words * (width // 2 + 1)
                    and successful_by_v == expected_successes,
                    "complete trim-scope cardinalities failed")
            words_by_width.append(word_count)
            queries_by_width.append(query_count)
            divisible_by_width.append(sum(successful_by_v))
            audit.counts["finite_base_width_scopes"] += 1
            audit.counts["finite_empty_words"] += int(width == 0)
        word_count, query_count, successes = (sum(words_by_width), sum(queries_by_width),
                                             sum(divisible_by_width))
        audit.counts["finite_symmetric_words"] += word_count
        audit.counts["finite_allowed_v_queries"] += query_count
        audit.counts["finite_divisible_queries"] += successes
        audit.counts["finite_base2_words"] += word_count if base == 2 else 0
        audit.counts["finite_composite_base_words"] += word_count if composite else 0
        rows.append({"base": base, "composite_base": composite,
                     "coefficient_maximum": 2 * (base - 1), "minimum_width": 0,
                     "maximum_width": maximum_width, "words_by_width": words_by_width,
                     "queries_by_width": queries_by_width, "divisible_by_width": divisible_by_width,
                     "words": word_count, "all_allowed_v_queries": query_count,
                     "divisible_queries": successes,
                     "positive_v_divisible_queries": positive_trim_count})
    require(audit.counts["finite_allowed_v_queries"]
            == audit.counts["finite_divisible_queries"] + audit.counts["finite_nondivisible_queries"],
            "trim query partition failed")
    require(audit.counts["finite_v_zero_queries"] == audit.counts["finite_symmetric_words"]
            and audit.counts["finite_negative_Z_words"] == audit.counts["finite_positive_Z_words"]
            and audit.counts["finite_negative_Z_divisible_queries"]
            == audit.counts["finite_positive_Z_divisible_queries"],
            "zero-trim or signed-complement counts failed")
    return rows


def premise_controls():
    rows = []
    cases = (("symmetry", (9, 0), 1, -90),
             ("coefficient_bound", (19, 19), 1, 110),
             ("width", (), 1, 0),
             ("divisibility", (10, 10), 1, 11))
    for failed, word, trim, expected_signed in cases:
        signed = signed_sum(10, word)
        require(signed == signed_horner(10, word) == expected_signed,
                "failed-premise example value changed")
        premises = {"symmetry": word == word[::-1],
                    "coefficient_bound": all(0 <= c <= 18 for c in word),
                    "width": 2 * trim <= len(word), "divisibility": signed % 10 ** trim == 0}
        require([name for name, valid in premises.items() if not valid] == [failed]
                and literal_middle(10, word, trim) is None,
                "failed-premise example no longer isolates its stated condition")
        rows.append({"base": 10, "word": list(word), "v": trim, "signed_value": signed,
                     "only_failed_premise": failed, "premises": premises,
                     "literal_neutral_padding_exists": False})
    return rows


def known_certificate_trims(audit, mirror):
    sources = mirror._lean_certs()
    require({base for base, _ in sources} == {2, 4, 8, 11, 16, 17, 26, 32},
            "main-source certificate set changed")
    sources.append((20, fixtures.base20_fixture()))
    rows = []
    for base, edges in sorted(sources):
        cycle = [(list(b), list(c), list(b2), list(c2), u, v)
                 for b, c, b2, c2, u, v in edges]
        require(mirror.cycleOK(base, cycle, cycle[0][0], cycle[0][1]),
                f"known base-{base} full certificate failed")
        positives = 0
        for exterior, center, _, target, _, trim in cycle:
            raw = mirror.nextC(base, exterior, center)
            middle = audit.trim(base, raw, trim)
            require(middle == tuple(target), "known certificate center trim failed recovery")
            audit.counts["known_certificate_trim_edges"] += 1
            audit.counts["selected_positive_v_trim_edges"] += int(trim > 0)
            positives += int(trim > 0)
        rows.append({"base": base, "edges": len(cycle), "positive_v_edges": positives})
    return {"cycles": rows, "full_mirror_cycles": len(rows),
            "total_edges": sum(row["edges"] for row in rows),
            "base20_source": fixtures.BASE20_SOURCE}


def decimal_center_only_trims(audit, mirror):
    # Reuse the attributed fixture, then replay the exact prescribed trim schedule.
    metadata = center_fixture.decimal_center_only(center_fixture.Audit(mirror))
    center = tuple(metadata["initial_C"])
    initial = center
    for phase, (incoming, overflow, trim) in enumerate(zip(
            map(int, metadata["e"]), map(int, metadata["g"]), map(int, metadata["v"]))):
        width, power = len(center), 10 ** len(center)
        outgoing, remainder = divmod(value_sum(10, center) + incoming, power)
        digits = [remainder // 10 ** position % 10 for position in range(width)]
        require(outgoing == 1 - incoming and mirror.norm(10, center, incoming) == (digits, outgoing),
                "decimal center-only fixture normalization/flip failed")
        padded = digits + [9 * incoming] * overflow
        raw = tuple(a + b for a, b in zip(padded, padded[::-1]))
        require(signed_sum(10, center) == metadata["signed_values"][phase]
                and signed_sum(10, raw) == metadata["raw_signed_values"][phase],
                "decimal center-only fixture signed values changed")
        target = audit.trim(10, raw, trim)
        require(target is not None and len(target) == width + overflow - 2 * trim,
                "decimal center-only target recovery failed")
        audit.counts["decimal_center_only_trim_edges"] += 1
        audit.counts["selected_positive_v_trim_edges"] += int(trim > 0)
        center = target
    require(center == initial, "decimal center-only fixture failed closure")
    return {"scope": "CENTER-ONLY: no exterior B or full decimal certificate",
            "source_agent": metadata["source_agent"], "source_PR": metadata["source_PR"],
            "source_issue_comment": metadata["source_issue_comment"],
            "edges": metadata["edges"], "positive_v_edges": sum(int(v) > 0 for v in metadata["v"]),
            "e": metadata["e"], "g": metadata["g"], "v": metadata["v"],
            "initial_C": metadata["initial_C"],
            "canonical_center_edges_sha256": metadata["canonical_center_edges_sha256"]}


def main():
    audit = Audit()
    mirror = fixtures.load_mirror()
    result = {"status": "COMPUTED", "sampling": "none; all words and allowed v in declared scopes",
              "failed_premise_controls": premise_controls(),
              "complete_scopes": complete_controls(audit),
              "known_certificate_trims": known_certificate_trims(audit, mirror),
              "decimal_center_only_trims": decimal_center_only_trims(audit, mirror),
              "totals": audit.counts}
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS: complete finite numeric-trim converse, unique middle recovery, and attributed trim edges.")


if __name__ == "__main__":
    main()
