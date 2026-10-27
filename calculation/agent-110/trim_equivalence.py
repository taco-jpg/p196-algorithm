#!/usr/bin/env python3
"""Construct prescribed trims for an existing neutral-band certificate.

Neutral padding is Agent 7's lemma; schedule equivalence is Agent 107's
formulation. Agent 110 supplies this independent checked transformation,
balanced schedules, full integer controls, 和 malformed-input rejection.

Run: python3 calculation/agent-110/trim_equivalence.py selftest
No new certificate search or Lean verification is claimed.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
import copy
import json
import random
import sys


def _nat(value, name):
    if type(value) is not int or value < 0:
        raise ValueError(f"{name}: expected a nonnegative integer")
    return value


def _base(base):
    if _nat(base, "base") < 2:
        raise ValueError("base must be at least 2")


def _word(base, word, name):
    if not isinstance(word, (tuple, list)):
        raise ValueError(f"{name}: expected a coefficient list")
    for value in word:
        if _nat(value, name) > 2 * (base - 1):
            raise ValueError(f"{name}: coefficient exceeds 2*(base-1)")


def _bit(value, name):
    if _nat(value, name) > 1:
        raise ValueError(f"{name}: expected a bit")


def normalize(base, word, carry):
    """Independent scalar carry normalization, with explicit domain checks."""
    _base(base)
    _word(base, word, "word")
    _bit(carry, "carry")
    digits = []
    for coefficient in word:
        carry, digit = divmod(coefficient + carry, base)
        digits.append(digit)
    return digits, carry


def neutral_pad(base, word, count):
    _base(base)
    _word(base, word, "word")
    _nat(count, "padding")
    return [base - 1] * count + list(word) + [base - 1] * count


def center_step(base, center, incoming, overflow):
    """Raw center image; the carry-flip condition is mandatory."""
    _bit(overflow, "overflow")
    digits, outgoing = normalize(base, center, incoming)
    if outgoing != 1 - incoming:
        raise ValueError("center does 不 flip its incoming carry")
    if overflow:
        digits.append((base - 1) * incoming)
    return [left + right for left, right in zip(digits, reversed(digits))]


@dataclass(frozen=True)
class CycleData:
    carry: tuple
    overflow: tuple
    outer_trim: tuple
    center_trim: tuple
    exterior: tuple


def validate_cycle(base, edges):
    """Check the full cycle independently of the repository Python mirror."""
    _base(base)
    if not isinstance(edges, (tuple, list)) or not edges:
        raise ValueError("a cycle must contain at least one edge")
    normalized = []
    for index, edge in enumerate(edges):
        if not isinstance(edge, (tuple, list)) or len(edge) != 6:
            raise ValueError(f"edge {index}: expected B,C,B2,C2,u,v")
        B, C, B2, C2, u, v = edge
        for name, word in (("B", B), ("C", C), ("B2", B2), ("C2", C2)):
            _word(base, word, name)
        _nat(u, "u")
        _nat(v, "v")
        if B and B[0] == 0:
            raise ValueError(f"edge {index}: zero exterior head")
        normalized.append((list(B), list(C), list(B2), list(C2), u, v))
    carries, overflows = [], []
    for index, edge in enumerate(normalized):
        B, C, B2, C2, u, v = edge
        successor = normalized[(index + 1) % len(normalized)]
        if (B2, C2) != (successor[0], successor[1]):
            raise ValueError(f"edge {index}: broken cyclic link")
        low_digits, e = normalize(base, B, 0)
        _, e2 = normalize(base, C, e)
        if e2 != 1 - e:
            raise ValueError(f"edge {index}: carry flip failed")
        high_digits, g = normalize(base, list(reversed(B)), e2)
        high_digits.reverse()
        if g:
            low_digits.append((base - 1) * (1 - e))
            high_digits.insert(0, 1)
        raw_B = [left + right for left, right in zip(low_digits, high_digits)]
        if raw_B != B2 + [base - 1] * u:
            raise ValueError(f"edge {index}: exterior equation failed")
        if center_step(base, C, e, g) != neutral_pad(base, C2, v):
            raise ValueError(f"edge {index}: center equation failed")
        carries.append(e)
        overflows.append(g)
    us = tuple(edge[4] for edge in normalized)
    vs = tuple(edge[5] for edge in normalized)
    if sum(overflows) > sum(us) + sum(vs):
        raise ValueError("cycle gain condition failed")
    if sum(us) != sum(overflows) or 2 * sum(vs) != sum(overflows):
        raise ValueError("closed-cycle length identities failed")
    return CycleData(tuple(carries), tuple(overflows), us, vs,
                     tuple(tuple(edge[0]) for edge in normalized))


def redistribute_cycle(base, edges, target):
    """Return (new_edges, padding); the additive padding offset is minimal."""
    original = validate_cycle(base, edges)
    if not isinstance(target, (tuple, list)) or len(target) != len(edges):
        raise ValueError("target schedule length must equal the cycle period")
    for value in target:
        _nat(value, "target trim")
    if sum(target) != sum(original.center_trim):
        raise ValueError("source 和 target trim totals must agree")
    prefix = [0]
    for old, new in zip(original.center_trim, target):
        prefix.append(prefix[-1] + old - new)
    offset = -min(prefix)
    padding = [offset + partial for partial in prefix[:-1]]
    transformed = _padded_edges(base, edges, padding, target)
    result = validate_cycle(base, transformed)
    if (result.carry, result.overflow, result.outer_trim, result.exterior) != (
            original.carry, original.overflow, original.outer_trim, original.exterior):
        raise ValueError("transformation changed a required invariant")
    return transformed, padding


def _padded_edges(base, edges, padding, target):
    centers = [neutral_pad(base, edge[1], amount)
               for edge, amount in zip(edges, padding)]
    transformed = []
    for i, edge in enumerate(edges):
        transformed.append((list(edge[0]), centers[i], list(edge[2]),
                            centers[(i + 1) % len(edges)], edge[4], target[i]))
    return transformed


def balanced_schedule(overflows, parity=0):
    """Choose trims so center lengths occupy at most 两 consecutive values."""
    _bit(parity, "parity")
    if not isinstance(overflows, (tuple, list)) or not overflows:
        raise ValueError("overflow stream must be nonempty")
    for value in overflows:
        _bit(value, "overflow")
    if sum(overflows) % 2:
        raise ValueError("a closed center requires an even overflow total")
    total, result = parity, []
    for value in overflows:
        result.append((total + value) // 2 - total // 2)
        total += value
    return result


def lift_to_cap(base, edges, width):
    """Pad every center to its largest parity-compatible length <= width.

    Each output length is width or width-1. This preserves a uniform width
    cap, unlike an arbitrary prescribed schedule. Padding is explicitly
    (target_length - original_length)//2 at every phase.
    """
    original = validate_cycle(base, edges)
    _nat(width, "width cap")
    lengths = [len(edge[1]) for edge in edges]
    if width < max(lengths):
        raise ValueError("width cap is smaller than a source center")
    targets = [width - ((width - length) % 2) for length in lengths]
    padding = [(target - old) // 2 for target, old in zip(targets, lengths)]
    parity = int((width - lengths[0]) % 2 == 0)
    trims = balanced_schedule(original.overflow, parity)
    transformed = _padded_edges(base, edges, padding, trims)
    result = validate_cycle(base, transformed)
    if (result.carry, result.overflow, result.outer_trim, result.exterior) != (
            original.carry, original.overflow, original.outer_trim, original.exterior):
        raise ValueError("cap lift changed a required invariant")
    if [len(edge[1]) for edge in transformed] != targets:
        raise ValueError("cap lift missed its prescribed widths")
    return transformed, padding


def _require(condition, message):
    if not condition:
        raise RuntimeError(message)


def _value(base, word):
    value = 0
    for coefficient in reversed(word):
        value = value * base + coefficient
    return value


def _integer_norm(base, word, carry):
    value = _value(base, word) + carry
    digits = []
    for _ in word:
        value, digit = divmod(value, base)
        digits.append(digit)
    return digits, value


def _integer_reverse(base, value):
    result = 0
    while value:
        value, digit = divmod(value, base)
        result = base * result + digit
    return result


def _integer_cycle_check(base, edges):
    info = validate_cycle(base, edges)
    gap = 2 + sum(info.overflow)
    current = None
    for i, (B, C, B2, C2, u, v) in enumerate(edges):
        word = B + [base - 1] * gap + C + [base - 1] * gap + B[::-1]
        value = _value(base, word)
        if current is not None:
            _require(value == current, "ordinary integer chain broke")
        reverse = _integer_reverse(base, value)
        _require(value != reverse, "a certified phase was palindromic")
        gap += u + v - info.overflow[i]
        next_word = B2 + [base - 1] * gap + C2 + [base - 1] * gap + B2[::-1]
        current = _value(base, next_word)
        _require(current == value + reverse, "ordinary reverse-add mismatch")
    return len(edges)


def selftest():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror
    certs = mirror._lean_certs()
    _require({base for base, _ in certs} == {2, 4, 8, 16, 32, 11, 17, 26}
             and len(certs) == 8, "expected the eight source certificates")
    stats = dict(original_certificates=8, binary_targets=0, balanced_targets=0,
                 cap_lifts=0, max_width_preserved=0,
                 repeated_concentrated=0, concentrated_to_binary=0,
                 repeated_random=0, ordinary_integer_edges=0,
                 padding_inputs=0, padding_identities=0,
                 normalization_integer_checks=0, malformed_rejected=0)
    rng = random.Random(110)

    def test_transform(base, edges, target, category):
        before = copy.deepcopy(edges)
        transformed, padding = redistribute_cycle(base, edges, target)
        _require(edges == before, "input certificate was mutated")
        _require(min(padding) == 0, "padding offset is 不 minimal")
        _require(mirror.cycleOK(base, transformed, transformed[0][0], transformed[0][1]),
                 "secondary repository mirror rejected transformation")
        stats[category] += 1
        stats["ordinary_integer_edges"] += _integer_cycle_check(base, transformed)
        return transformed

    for base, edges in certs:
        info = validate_cycle(base, edges)
        _require(mirror.cycleOK(base, edges, edges[0][0], edges[0][1]),
                 "repository source certificate failed its mirror")
        period, weight = len(edges), sum(info.center_trim)
        for positions in combinations(range(period), weight):
            target = [int(i in positions) for i in range(period)]
            test_transform(base, edges, target, "binary_targets")
        for parity in (0, 1):
            target = balanced_schedule(info.overflow, parity)
            changed = test_transform(base, edges, target, "balanced_targets")
            lengths = [len(edge[1]) for edge in changed]
            _require(max(lengths) - min(lengths) <= 1, "center widths are 不 balanced")
            maximum = max(len(edge[1]) for edge in edges)
            _require(max(lengths) <= maximum + 1, "balanced lift widened the cap by >1")
            if parity == int((maximum - len(edges[0][1])) % 2 == 0):
                _require(max(lengths) == maximum, "best parity changed the maximum width")
                stats["max_width_preserved"] += 1
        maximum = max(len(edge[1]) for edge in edges)
        for width in (maximum, maximum + 1, maximum + 4):
            changed, padding = lift_to_cap(base, edges, width)
            lengths = [len(edge[1]) for edge in changed]
            _require(max(lengths) == width and min(lengths) >= width - 1,
                     "cap lift did 不 attain the correct adjacent lengths")
            _require(mirror.cycleOK(base, changed, changed[0][0], changed[0][1]),
                     "secondary mirror rejected cap lift")
            stats["cap_lifts"] += 1
            stats["ordinary_integer_edges"] += _integer_cycle_check(base, changed)
        for repeat in (2, 3):
            repeated = edges * repeat
            total = repeat * weight
            for position in range(len(repeated)):
                target = [0] * len(repeated)
                target[position] = total
                concentrated = test_transform(base, repeated, target, "repeated_concentrated")
                binary = [1] * total + [0] * (len(repeated) - total)
                test_transform(base, concentrated, binary, "concentrated_to_binary")
            for _ in range(50):
                target = [0] * len(repeated)
                for _ in range(total):
                    target[rng.randrange(len(repeated))] += 1
                test_transform(base, repeated, target, "repeated_random")

    bases = (2, 3, 4, 8, 10, 11, 16, 17, 26, 32)
    while stats["padding_inputs"] < 10_000:
        base, incoming = rng.choice(bases), rng.randrange(2)
        center = [rng.randrange(2 * base - 1) for _ in range(rng.randrange(1, 21))]
        digits, outgoing = normalize(base, center, incoming)
        if outgoing != 1 - incoming:
            continue
        amount = rng.randrange(9)
        padded = neutral_pad(base, center, amount)
        padded_digits, padded_out = normalize(base, padded, incoming)
        h = base - 1
        _require(padded_out == outgoing and padded_digits == (
            [h * (1 - incoming)] * amount + digits + [h * incoming] * amount),
            "neutral carry transport failed")
        for word in (center, padded):
            _require(normalize(base, word, incoming) == _integer_norm(base, word, incoming),
                     "independent integer normalization mismatch")
            stats["normalization_integer_checks"] += 1
        for overflow in (0, 1):
            _require(center_step(base, padded, incoming, overflow) == neutral_pad(
                base, center_step(base, center, incoming, overflow), amount),
                "center padding conjugacy failed")
            stats["padding_identities"] += 1
        stats["padding_inputs"] += 1

    base, edges = certs[0]
    target = [edge[5] for edge in edges]
    negatives = [lambda: validate_cycle(base, []), lambda: validate_cycle(1, edges),
                 lambda: redistribute_cycle(base, edges, target[:-1]),
                 lambda: redistribute_cycle(base, edges, [0] * len(edges)),
                 lambda: balanced_schedule([1]), lambda: balanced_schedule([2, 0]),
                 lambda: balanced_schedule([0, 0], True),
                 lambda: neutral_pad(base, [], -1),
                 lambda: lift_to_cap(base, edges, max(len(e[1]) for e in edges) - 1)]
    for bad in (-1, 1.5, True):
        schedule = target[:]
        schedule[0] = bad
        negatives.append(lambda s=schedule: redistribute_cycle(base, edges, s))
    for bad in (-1, 2 * base - 1, True):
        malformed = copy.deepcopy(edges)
        malformed[0][1][0] = bad
        negatives.append(lambda es=malformed: validate_cycle(base, es))
    malformed = copy.deepcopy(edges)
    malformed[0] = malformed[0][:-1]
    negatives.append(lambda: validate_cycle(base, malformed))
    for operation in negatives:
        try:
            operation()
        except ValueError:
            stats["malformed_rejected"] += 1
        else:
            raise RuntimeError("malformed input was accepted")
    _require(stats["binary_targets"] == 56, "binary schedule count changed")
    _require(stats["balanced_targets"] == 16, "balanced schedule count changed")
    print("COMPUTED PASS " + json.dumps(stats, sort_keys=True))
    return stats


if __name__ == "__main__":
    if sys.argv[1:] not in ([], ["selftest"]):
        raise SystemExit("usage: trim_equivalence.py [selftest]")
    selftest()
