#!/usr/bin/env python3
"""Independent local inverse and whole-integer exterior-padding audit.

The optimized inverse formulas are audited exhaustively for decimal local
columns.  Existing Lean certificates supply fixtures only; all normalization,
padding, temporal-column and terminal arithmetic here is independent.
Run: python3 calculation/agent-117/exterior_inverse_audit.py
"""

import itertools
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def norm(base, word, carry):
    value, power = carry, 1
    for coefficient in word:
        value += coefficient * power
        power *= base
    digits = []
    for _ in word:
        value, digit = divmod(value, base)
        digits.append(digit)
    return digits, value


def raw_exterior(base, word):
    lower, incoming_center = norm(base, word, 0)
    reverse, overflow = norm(base, word[::-1], 1 - incoming_center)
    upper = reverse[::-1]
    if overflow:
        lower.append((base - 1) * (1 - incoming_center))
        upper.insert(0, 1)
    return [a + b for a, b in zip(lower, upper)], incoming_center, overflow


def inverse_zero(post_l, post_h, next_coefficient):
    old_l = (next_coefficient - post_h) % 2
    result = set()
    for old_h in (0, 1):
        numerator = next_coefficient - old_l - post_h + 10 * (post_l + old_h)
        if numerator % 2:
            continue
        coefficient = numerator // 2
        if (0 <= coefficient <= 18
                and (coefficient + old_l) // 10 == post_l
                and (coefficient + post_h) // 10 == old_h):
            result.add((coefficient, old_l, old_h))
    return result


def inverse_one(post_l, post_h, post_y, next_coefficient):
    difference = post_y - post_h
    coefficient = difference + 10 * post_l if 0 <= difference <= 8 else 9
    result = set()
    for old_l in (0, 1):
        if (coefficient + old_l) // 10 != post_l:
            continue
        if (coefficient + post_h) % 10 != post_y:
            continue
        old_y = next_coefficient - (coefficient + old_l) % 10
        if 0 <= old_y <= 9:
            result.add((coefficient, old_l, (coefficient + post_h) // 10, old_y))
    return result


def local_inverse_audit():
    zero_truth = {}
    one_truth = {}
    forced_truth = {}
    for coefficient, old_l, post_h in itertools.product(range(19), (0, 1), (0, 1)):
        post_l, lower = divmod(coefficient + old_l, 10)
        old_h, reverse = divmod(coefficient + post_h, 10)
        zero_truth.setdefault((post_l, post_h, lower + reverse), set()).add(
            (coefficient, old_l, old_h))
        forced_truth.setdefault((post_l, post_h, reverse), set()).add(
            (coefficient, old_l, old_h))
        for old_y in range(10):
            one_truth.setdefault((post_l, post_h, reverse, lower + old_y), set()).add(
                (coefficient, old_l, old_h, old_y))
    zero_queries = one_queries = 0
    for post_l, post_h, following in itertools.product((0, 1), (0, 1), range(19)):
        require(inverse_zero(post_l, post_h, following)
                == zero_truth.get((post_l, post_h, following), set()), "nonoverflow inverse mismatch")
        zero_queries += 1
        for post_y in range(10):
            require(inverse_one(post_l, post_h, post_y, following)
                    == one_truth.get((post_l, post_h, post_y, following), set()),
                    "overflow inverse mismatch")
            one_queries += 1
    require(inverse_zero(1, 1, 0), "negative parity-remainder control unexpectedly empty")
    require(len(forced_truth) == 40 and all(len({row[0] for row in rows}) == 1
                                          for rows in forced_truth.values()),
            "overflow coefficient is not uniquely forced")
    branching = sorted(key for key, rows in zero_truth.items() if len(rows) == 2)
    missing = sorted(set(itertools.product((0, 1), (0, 1), range(19))) - set(zero_truth))
    require(branching == [(0, 1, 9), (1, 0, 9)], "nonoverflow branch cases")
    require(missing == [(0, 1, 0), (1, 0, 18)], "nonoverflow empty cases")
    print("inverse_tiles overflow_targets=40 overflow_tiles=%d nonoverflow_branching=%s nonoverflow_empty=%s"
          % (sum(map(len, forced_truth.values())), branching, missing))
    return zero_queries, one_queries, sum(map(len, zero_truth.values())), sum(map(len, one_truth.values()))


def suffix_audit():
    words = padding_cases = edge_conversions = 0
    for width in range(4):
        for values in itertools.product(range(19), repeat=width):
            if values and values[0] == 0:
                continue
            word = list(values)
            raw, incoming_center, overflow = raw_exterior(10, word)
            words += 1
            for added in (1, 2, 3):
                got, e2, g2 = raw_exterior(10, word + [9] * added)
                require((e2, g2) == (incoming_center, overflow), "suffix changed drivers")
                require(got == raw + [9] * added, "raw suffix covariance")
                padding_cases += 1
            neutral = 0
            while neutral < len(raw) and raw[-1 - neutral] == 9:
                neutral += 1
            for trim in range(neutral + 1):
                target = raw[:len(raw) - trim]
                if target and target[0] == 0:
                    continue
                width_bound = max(len(word), len(target), 1)
                left_pad, right_pad = width_bound - len(word), width_bound - len(target)
                changed_trim = trim + left_pad - right_pad
                require(changed_trim == overflow, "constant-width trim is not g")
                got, _, _ = raw_exterior(10, word + [9] * left_pad)
                require(got == target + [9] * right_pad + [9] * overflow,
                        "constant-width edge conversion")
                edge_conversions += 1
    return words, padding_cases, edge_conversions


def literal_cut(base, words, e, g, position):
    lower, higher, partner = [], [], []
    for word, incoming, overflow in zip(words, e, g):
        lower.append(norm(base, word[:position], 0)[1])
        higher.append(norm(base, word[position:][::-1], 1 - incoming)[1])
        if overflow:
            reversed_digits, _ = norm(base, word[::-1], 1 - incoming)
            partner.append(1 if position == 0 else reversed_digits[len(word) - position])
        else:
            partner.append(-1)
    return lower, higher, partner


def verify_column(base, before, after, column, g):
    left, right, partner = before
    new_l, new_h, new_y = after
    for t, coefficient in enumerate(column):
        require((coefficient + left[t]) // base == new_l[t], "column forward carry")
        require((coefficient + new_h[t]) // base == right[t], "column reverse carry")
        reverse_digit = (coefficient + new_h[t]) % base
        following = (coefficient + left[t]) % base + (partner[t] if g[t] else reverse_digit)
        require(following == column[(t + 1) % len(column)], "temporal column closure")
        if g[t]:
            require(reverse_digit == new_y[t], "overflow partner storage")
        if base == 10:
            record = ((coefficient, left[t], right[t], partner[t]) if g[t]
                      else (coefficient, left[t], right[t]))
            candidates = (inverse_one(new_l[t], new_h[t], new_y[t], following) if g[t]
                          else inverse_zero(new_l[t], new_h[t], following))
            require(record in candidates, "local inverse omitted literal column")


def source_controls():
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root / "calculation"))
    from neutral_band_search import _lean_certs  # Fixture extraction only.
    bases, cycles, edges_checked, columns_checked = [], 0, 0, 0
    for base, edges in sorted(_lean_certs()):
        originals = [list(edge[0]) for edge in edges]
        period = len(edges)
        e = [norm(base, word, 0)[1] for word in originals]
        g = [norm(base, word[::-1], 1 - carry)[1] for word, carry in zip(originals, e)]
        for extra in range(3):
            width = max(1, max(map(len, originals))) + extra
            words = [word + [base - 1] * (width - len(word)) for word in originals]
            require(all(word[0] > 0 for word in words), "physical-root positivity")
            for t, word in enumerate(words):
                raw, carry, overflow = raw_exterior(base, word)
                require((carry, overflow) == (e[t], g[t]), "padded driver mismatch")
                require(raw == words[(t + 1) % period] + [base - 1] * overflow,
                        "padded source cycle did not acquire u=g")
                edges_checked += 1
            first = literal_cut(base, words, e, g, 0)
            require(first == ([0] * period, g, [1 if bit else -1 for bit in g]),
                    "physical root interface")
            terminal = literal_cut(base, words, e, g, width)
            require(terminal == (e, [1 - carry for carry in e],
                                 [(base - 1) * e[t] if g[t] else -1 for t in range(period)]),
                    "fixed-driver terminal interface")
            before = first
            for j in range(width):
                after = literal_cut(base, words, e, g, j + 1)
                verify_column(base, before, after, [word[j] for word in words], g)
                before = after
                columns_checked += 1
            cycles += 1
        bases.append((base, period))
    require([base for base, _ in bases] == [2, 4, 8, 11, 16, 17, 26, 32], "source coverage")
    return bases, cycles, edges_checked, columns_checked


def main():
    print("local_inverse zero_queries=%d one_queries=%d zero_records=%d one_records=%d"
          % local_inverse_audit())
    print("suffix words=%d padding_cases=%d constant_width_edge_conversions=%d" % suffix_audit())
    bases, cycles, edges, columns = source_controls()
    print("source_controls", bases, "constant_width_cycles", cycles,
          "temporal_edges", edges, "spatial_columns", columns)
    print("COMPUTED EXTERIOR-INVERSE AUDIT PASSED")


if __name__ == "__main__":
    main()
