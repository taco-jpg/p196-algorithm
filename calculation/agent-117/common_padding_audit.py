#!/usr/bin/env python3
"""Independent arithmetic audit of simultaneous neutral center padding.

The center arithmetic uses whole integers and digit extraction; the repository
mirror is imported only to obtain the eight existing Lean-source fixtures.
This is a finite COMPUTED audit, not a Lean theorem or a center-cycle solver.

Run: python3 calculation/agent-117/common_padding_audit.py
"""

import itertools
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def normalize_integer(base, coefficients, incoming):
    value = incoming
    power = 1
    for coefficient in coefficients:
        value += coefficient * power
        power *= base
    digits = []
    for _ in coefficients:
        value, digit = divmod(value, base)
        digits.append(digit)
    return digits, value


def padded(base, center, pairs):
    return [base - 1] * pairs + list(center) + [base - 1] * pairs


def valid_center(base, center, incoming):
    return (base >= 2 and incoming in (0, 1)
            and list(center) == list(reversed(center))
            and all(0 <= c <= 2 * base - 2 for c in center)
            and normalize_integer(base, center, incoming)[1] == 1 - incoming)


def image(base, center, incoming, overflow):
    if overflow not in (0, 1) or not valid_center(base, center, incoming):
        return None
    digits, _ = normalize_integer(base, center, incoming)
    if overflow:
        digits.append((base - 1) * incoming)
    return [a + b for a, b in zip(digits, reversed(digits))]


def fixed_trim_step(base, center, incoming, overflow, trim):
    if type(trim) is not int or trim < 0:
        return None
    raw = image(base, center, incoming, overflow)
    if raw is None or len(raw) <= 2 * trim:
        return None
    if any(x != base - 1 for x in raw[:trim] + raw[len(raw) - trim:]):
        return None
    return raw[trim:len(raw) - trim]


def has_flip(base, center):
    return any(valid_center(base, center, incoming) for incoming in (0, 1))


def has_neutral_pair(base, center):
    return len(center) >= 2 and center[0] == center[-1] == base - 1


def covariant_edge(base, center, incoming, overflow, trim, pairs):
    target = fixed_trim_step(base, center, incoming, overflow, trim)
    require(target is not None, "control edge is not valid")
    enlarged = fixed_trim_step(base, padded(base, center, pairs), incoming, overflow, trim)
    require(enlarged == padded(base, target, pairs), "fixed-trim padding covariance")
    if has_flip(base, target):
        for _ in range(pairs):
            require(has_neutral_pair(base, enlarged), "missing target padding")
            enlarged = enlarged[1:-1]
        require(enlarged == target, "common padding removal changed the target")


def exhaustive_covariance():
    words = valid_inputs = raw_checks = edge_checks = inverse_checks = 0
    for base in (2, 3, 4, 10):
        for width in range(1, 7):
            for half in itertools.product(range(2 * base - 1), repeat=(width + 1) // 2):
                center = list(half) + list(half[:width // 2][::-1])
                words += 1
                for incoming in (0, 1):
                    if not valid_center(base, center, incoming):
                        continue
                    valid_inputs += 1
                    for overflow in (0, 1):
                        raw = image(base, center, incoming, overflow)
                        for pairs in (1, 2, 3):
                            require(image(base, padded(base, center, pairs), incoming, overflow)
                                    == padded(base, raw, pairs), "raw padding covariance")
                            raw_checks += 1
                        for trim in range((len(raw) - 1) // 2 + 1):
                            target = fixed_trim_step(base, center, incoming, overflow, trim)
                            if target is None:
                                continue
                            for pairs in (1, 2, 3):
                                covariant_edge(base, center, incoming, overflow, trim, pairs)
                                edge_checks += 1
                            if (has_neutral_pair(base, center) and has_neutral_pair(base, target)
                                    and has_flip(base, target)):
                                require(valid_center(base, center[1:-1], incoming), "invalid stripped source")
                                require(has_flip(base, target[1:-1]), "invalid stripped target")
                                require(fixed_trim_step(base, center[1:-1], incoming, overflow, trim)
                                        == target[1:-1], "inverse fixed-trim covariance")
                                inverse_checks += 1
    return words, valid_inputs, raw_checks, edge_checks, inverse_checks


def short_guards():
    checked = 0
    for base, width, incoming, pairs in itertools.product(range(2, 33), range(9), (0, 1), range(4)):
        center = [base - 1] * width
        require(normalize_integer(base, center, incoming)[1] == incoming, "neutral run changed carry")
        require(not valid_center(base, center, incoming), "all-neutral center passed flip")
        require(not valid_center(base, padded(base, center, pairs), incoming), "all-neutral padding passed flip")
        checked += 1
    return checked


def first_layer_deletion():
    local_cases = neutral_matches = short_cases = 0
    for base in range(2, 63):
        for incoming, overflow, coefficient, inward in itertools.product(
                (0, 1), (0, 1), range(2 * base - 1), (0, 1)):
            if (coefficient + inward) // base != 1 - incoming:
                continue
            left_out = (coefficient + incoming) // base
            predicate = left_out == incoming and inward == 1 - incoming
            require(predicate == (coefficient == base - 1), "deletion removed a non-neutral column")
            if predicate:
                if overflow:
                    require((coefficient + inward) % base == (base - 1) * incoming,
                            "neutral overflow partner digit")
                neutral_matches += 1
            local_cases += 1
        for incoming, coefficient in itertools.product((0, 1), range(2 * base - 1)):
            left_out = (coefficient + incoming) // base
            if left_out == 1 - incoming:  # T_LODD leaves r unchanged.
                require(left_out != incoming, "odd short layer matched deletion")
                short_cases += 1
            inward = left_out          # T_LEVEN identifies the middle carries.
            if (coefficient + inward) // base == 1 - incoming:
                require(not (left_out == incoming and inward == 1 - incoming),
                        "even short layer matched deletion")
                short_cases += 1
    return local_cases, neutral_matches, short_cases


def long_trim_controls():
    checks = 0
    for trim in range(1, 65):
        prefix = ([4] if trim == 1 else [4, 4] if trim == 2
                  else [4, 4] + [9] * (trim - 3) + [14])
        core = [0, 0, 0] if trim == 1 else [10, 0, 10] if trim == 2 else [9, 10, 9]
        source = prefix + core + prefix[::-1]
        for incoming in (0, 1):
            for overflow in (0, 1):
                center = source if incoming else [18 - c for c in source]
                if overflow:
                    center = padded(10, [0 if incoming else 18], trim)
                target = fixed_trim_step(10, center, incoming, overflow, trim)
                require(target is not None and has_flip(10, target), "long-trim control")
                for pairs in (1, 2, 3):
                    covariant_edge(10, center, incoming, overflow, trim, pairs)
                    enlarged_source = padded(10, center, pairs)
                    enlarged_target = padded(10, target, pairs)
                    for _ in range(pairs):
                        enlarged_source = enlarged_source[1:-1]
                        enlarged_target = enlarged_target[1:-1]
                        require(fixed_trim_step(10, enlarged_source, incoming, overflow, trim)
                                == enlarged_target, "long-trim inverse covariance")
                    checks += 1
    return checks


def source_controls():
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root / "calculation"))
    from neutral_band_search import _lean_certs  # Fixtures only, no arithmetic use.
    controls = []
    cycle_checks = edge_checks = removed_pairs = 0
    for base, edges in sorted(_lean_certs()):
        centers = [list(edge[1]) for edge in edges]
        drivers = []
        for exterior, center, _, target, _, trim in edges:
            incoming = normalize_integer(base, exterior, 0)[1]
            overflow = normalize_integer(base, exterior[::-1], 1 - incoming)[1]
            require(fixed_trim_step(base, center, incoming, overflow, trim) == target,
                    "source fixture edge")
            drivers.append((incoming, overflow, trim))
        for pairs in range(4):
            enlarged = [padded(base, center, pairs) for center in centers]
            while True:
                for t, (incoming, overflow, trim) in enumerate(drivers):
                    require(fixed_trim_step(base, enlarged[t], incoming, overflow, trim)
                            == enlarged[(t + 1) % len(edges)], "source cycle lost fixed drivers")
                    edge_checks += 1
                cycle_checks += 1
                if not all(has_neutral_pair(base, center) for center in enlarged):
                    break
                enlarged = [center[1:-1] for center in enlarged]
                removed_pairs += 1
            require(any(center[0] != base - 1 for center in enlarged), "no primitive phase")
        controls.append((base, len(edges)))
    require([b for b, _ in controls] == [2, 4, 8, 11, 16, 17, 26, 32], "source coverage")
    return controls, cycle_checks, edge_checks, removed_pairs


def main():
    print("neutral_short_guards", short_guards())
    print("first_layer cases=%d neutral_matches=%d short_cases=%d" % first_layer_deletion())
    print("exhaustive words=%d valid_inputs=%d raw_covariances=%d fixed_trim_covariances=%d inverse_edges=%d"
          % exhaustive_covariance())
    print("long_trim_covariances", long_trim_controls(), "trim_range=1..64 g=0,1 e=0,1")
    controls, cycles, edges, removed = source_controls()
    print("source_controls", controls, "cycles_checked", cycles, "edges_checked", edges,
          "common_pairs_removed", removed)
    print("COMPUTED COMMON-PADDING AUDIT PASSED")


if __name__ == "__main__":
    main()
