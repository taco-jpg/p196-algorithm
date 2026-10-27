#!/usr/bin/env python3
"""Independent arithmetic contract for exterior regular-invariant checking.

The local row is (current coefficient, next-cut symbol, next-time coefficient).
Closed temporal words match outgoing to the following incoming coefficient,
including the final/first seam. FIRST requires positive current coefficients;
every later spatial layer uses the generic relation, including any return to
the numerical root cut. No generator DFA, minimization, or source is imported.

The equations are the original neutral_band/structure/bauto semantics, derived
from the two normalizations in neutral_band_search. Common-width neutral
padding is prior work of Agent7, audited in Agent105 PR401 / Agent116 PR375.
This file supplies arithmetic controls, not a new exterior search or theorem
of nonexistence. Run with ordinary Python or Python -O; checks are explicit.
"""
from __future__ import annotations

import importlib.util
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_base(base):
    require(type(base) is int and 2 <= base <= 62, "supported base is 2..62")


def check_bits(bits):
    bits = tuple(bits)
    require(bool(bits) and all(type(x) is int and x in (0, 1) for x in bits),
            "require a nonempty bit tuple")
    return bits


def encode(base, phase, low, high, previous):
    check_base(base)
    require(type(phase) is int and phase >= 0, "invalid phase")
    require(type(low) is int and low in (0, 1) and
            type(high) is int and high in (0, 1), "carry is not a bit")
    require(type(previous) is int and 0 <= previous < base, "digit outside base")
    symbol = phase * (4 * base) + low * (2 * base) + high * base + previous
    require(symbol < 2**64, "symbol exceeds uint64")
    return symbol


def decode(base, overflow, symbol):
    check_base(base)
    overflow = check_bits(overflow)
    require(type(symbol) is int and 0 <= symbol < 2**64, "invalid symbol")
    phase, local = divmod(symbol, 4 * base)
    require(phase < len(overflow), "symbol phase outside driver")
    low, rest = divmod(local, 2 * base)
    high, previous = divmod(rest, base)
    require(overflow[phase] or previous == 0, "nonoverflow previous digit must be zero")
    return phase, low, high, previous


def symbols(base, overflow):
    check_base(base)
    overflow = check_bits(overflow)
    return tuple(encode(base, t, low, high, previous)
                 for t, g in enumerate(overflow) for low in (0, 1)
                 for high in (0, 1) for previous in (range(base) if g else (0,)))


def root_word(base, overflow):
    overflow = check_bits(overflow)
    return tuple(encode(base, t, 0, g, g) for t, g in enumerate(overflow))


def terminal_word(base, entering, overflow):
    entering, overflow = check_bits(entering), check_bits(overflow)
    require(len(entering) == len(overflow), "driver lengths differ")
    return tuple(encode(base, t, e, 1 - e, (base - 1) * e if g else 0)
                 for t, (e, g) in enumerate(zip(entering, overflow)))


def local_rows(base, overflow, symbol, first=False):
    """Complete exact tile table; the caller supplies a validated bit driver."""
    phase, low, high, previous = decode(base, overflow, symbol)
    rows = []
    for coefficient in range(1 if first else 0, 2 * base - 1):
        next_low, low_digit = divmod(coefficient + low, base)
        for inward in (0, 1):
            actual_high, reverse_digit = divmod(coefficient + inward, base)
            if actual_high != high:
                continue
            successor = low_digit + (previous if overflow[phase] else reverse_digit)
            target = encode(base, phase, next_low, inward,
                            reverse_digit if overflow[phase] else 0)
            rows.append((coefficient, target, successor))
    return tuple(rows)


def equation_rows(base, overflow, symbol, first=False):
    """Independent local oracle: enumerate digits and solve integer equalities."""
    phase, low, high, previous = decode(base, overflow, symbol)
    answer = set()
    for low_digit, reverse_digit, next_low, inward in product(
            range(base), range(base), (0, 1), (0, 1)):
        coefficient = low_digit + base * next_low - low
        if not (int(first) <= coefficient <= 2 * base - 2):
            continue
        if coefficient != reverse_digit + base * high - inward:
            continue
        successor = low_digit + (previous if overflow[phase] else reverse_digit)
        answer.add((coefficient, encode(base, phase, next_low, inward,
                                       reverse_digit if overflow[phase] else 0), successor))
    return answer


def inverse_rows(base, overflow, symbol, first=False):
    """Exact preimage rows, derived from NEW carries without swapping ports.

    Forward a:(x,b,x_next) becomes reverse b:(x,a,x_next). Only old/new
    SYMBOLS are exchanged; temporal coefficient order remains unchanged.
    """
    phase, next_low, inward, next_previous = decode(base, overflow, symbol)
    answer = []
    for coefficient in range(int(first), 2 * base - 1):
        high, reverse_digit = divmod(coefficient + inward, base)
        if overflow[phase] and reverse_digit != next_previous:
            continue
        for low in (0, 1):
            actual_low, low_digit = divmod(coefficient + low, base)
            if actual_low != next_low:
                continue
            for previous in (range(base) if overflow[phase] else (0,)):
                successor = low_digit + (previous if overflow[phase] else reverse_digit)
                old_symbol = encode(base, phase, low, high, previous)
                answer.append((coefficient, old_symbol, successor))
    return tuple(answer)


def value(base, coefficients):
    total = 0
    for x in reversed(coefficients):
        total = total * base + x
    return total


def digits(base, number, width):
    return tuple((number // base**i) % base for i in range(width))


def exterior_step(base, coefficients):
    """Full exterior update from positional integers, including the empty word."""
    check_base(base)
    coefficients = tuple(coefficients)
    require(all(type(x) is int and 0 <= x <= 2 * base - 2 for x in coefficients),
            "coefficient outside exterior domain")
    width, modulus = len(coefficients), base**len(coefficients)
    low_value = value(base, coefficients)
    entering = low_value // modulus
    reverse_value = value(base, coefficients[::-1]) + 1 - entering
    overflow = reverse_value // modulus
    require(entering in (0, 1) and overflow in (0, 1), "normalization carry overflow")
    low_digits = digits(base, low_value, width)
    reverse_digits = digits(base, reverse_value, width)[::-1]
    if overflow:
        left = low_digits + ((base - 1) * (1 - entering),)
        right = (1,) + reverse_digits
    else:
        left, right = low_digits, reverse_digits
    raw = tuple(x + y for x, y in zip(left, right))
    return entering, overflow, raw


def cut_word(base, words, entering, overflow, position):
    """Recover every cut field independently from whole positional values."""
    width = len(words[0])
    require(all(len(word) == width for word in words) and 0 <= position <= width,
            "cut requires one common width")
    out = []
    for phase, word in enumerate(words):
        low = value(base, word[:position]) // base**position
        high = (value(base, word[position:][::-1]) + 1 - entering[phase]) // base**(width - position)
        reverse_value = value(base, word[::-1]) + 1 - entering[phase]
        previous = ((reverse_value // base**(width - position)) % base) if overflow[phase] else 0
        out.append(encode(base, phase, low, high, previous))
    return tuple(out)


def _closed_rows(word, tables, minimum, maximum):
    output = set()

    def walk(i, initial, current, prefix):
        if i == len(word):
            if current == initial:
                output.add(prefix)
            return
        for source, symbol, target in tables[word[i]]:
            if source == current:
                walk(i + 1, initial, target, prefix + (symbol,))

    for coefficient in range(minimum, maximum + 1):
        walk(0, coefficient, coefficient, ())
    return output


def closed_image(base, overflow, word, first=False, inverse=False):
    """Small exhaustive temporal-column oracle, without a DFA representation."""
    rows = inverse_rows if inverse else local_rows
    tables = {symbol: rows(base, overflow, symbol, first) for symbol in word}
    return _closed_rows(word, tables, int(first), 2 * base - 2)


def load_mirror():
    path = Path(__file__).resolve().parents[2] / "calculation/neutral_band_search.py"
    spec = importlib.util.spec_from_file_location("agent111_exterior_mirror_control", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit():
    counts = {"local_tables": 0, "generic_rows": 0, "positive_rows": 0,
              "inverse_local_tables": 0, "inverse_row_checks": 0,
              "cyclic_inverse_cases": 0, "cyclic_forward_pairs": 0,
              "swapped_port_counterexamples": 0,
              "whole_words": 0, "padding_equalities": 0, "legal_trim_equalities": 0,
              "first_language_cases": 0, "source_cycles": 0, "source_edges": 0,
              "source_cut_tiles": 0, "zero_width_terminal_rejections": 0}
    for base in range(2, 13):
        for overflow in ((0,), (1,)):
            alphabet = symbols(base, overflow)
            transposed = {first: {symbol: set() for symbol in alphabet} for first in (False, True)}
            for symbol in alphabet:
                for first in (False, True):
                    actual = local_rows(base, overflow, symbol, first)
                    expected = equation_rows(base, overflow, symbol, first)
                    require(len(actual) == len(set(actual)) and set(actual) == expected,
                            "quotient tile table differs from integer digit equations")
                    require(all(0 <= target <= 2 * base - 2 for _, _, target in actual),
                            "next temporal coefficient escaped its domain")
                    counts["local_tables"] += 1
                    counts["positive_rows" if first else "generic_rows"] += len(actual)
                    for coefficient, target, successor in expected:
                        transposed[first][target].add((coefficient, symbol, successor))
            for first in (False, True):
                for symbol in alphabet:
                    actual = inverse_rows(base, overflow, symbol, first)
                    require(len(actual) == len(set(actual)) and set(actual) == transposed[first][symbol],
                            "direct inverse equations differ from symbol-only transposition")
                    counts["inverse_local_tables"] += 1
                    counts["inverse_row_checks"] += len(actual)

    inverse_cases = [(2, g) for g in ((0,), (1,), (1, 0), (0, 1), (1, 1), (1, 0, 1), (1, 1, 1))]
    inverse_cases += [(3, g) for g in ((1, 0), (0, 1), (1, 1))]
    for base, overflow in inverse_cases:
        alphabet = symbols(base, overflow)
        by_phase = [tuple(s for s in alphabet if decode(base, overflow, s)[0] == t)
                    for t in range(len(overflow))]
        words = list(product(*by_phase))
        forward = {symbol: local_rows(base, overflow, symbol) for symbol in alphabet}
        inverse = {symbol: inverse_rows(base, overflow, symbol) for symbol in alphabet}
        swapped = {symbol: tuple((z, out, x) for x, out, z in rows)
                   for symbol, rows in inverse.items()}
        expected = {word: set() for word in words}
        for word in words:
            for target in _closed_rows(word, forward, 0, 2 * base - 2):
                expected[target].add(word)
                counts["cyclic_forward_pairs"] += 1
        for word in words:
            actual = _closed_rows(word, inverse, 0, 2 * base - 2)
            require(actual == expected[word], "whole cyclic preimage differs from relational inverse")
            counts["cyclic_inverse_cases"] += 1
            if len(word) > 2 and not counts["swapped_port_counterexamples"]:
                bad = _closed_rows(word, swapped, 0, 2 * base - 2)
                if bad != expected[word]:
                    counts["swapped_port_counterexamples"] = 1
    require(counts["swapped_port_counterexamples"] == 1,
            "inverse controls never distinguished the incorrect port reversal")

    mirror = load_mirror()
    for base, maximum in [(b, 4) for b in range(2, 7)] + [(10, 3)]:
        words = [()]
        words.extend((head,) + tail for width in range(1, maximum + 1)
                     for head in range(1, 2 * base - 1)
                     for tail in product(range(2 * base - 1), repeat=width - 1))
        for word in words:
            e, g, raw = exterior_step(base, word)
            # A one-coefficient center realizes exactly the complementary carry.
            center = [base * (1 - e)]
            require(mirror.hyp(base, list(word), center), "autonomous source lacks a legal center lift")
            require((e, g, raw) == (mirror.e1(base, list(word)),
                    mirror.gam(base, list(word), center), tuple(mirror.nextB(base, list(word), center))),
                    "whole-integer exterior differs from the unchanged mirror")
            counts["whole_words"] += 1
            for height in (0, 1, 3):
                padded = word + (base - 1,) * height
                require(exterior_step(base, padded) == (e, g, raw + (base - 1,) * height),
                        "neutral suffix covariance failed")
                counts["padding_equalities"] += 1
            for trim in range(len(raw) + 1):
                if trim and raw[-trim:] != (base - 1,) * trim:
                    continue
                target = raw[:len(raw) - trim]
                width = max(1, len(word), len(target))
                left = exterior_step(base, word + (base - 1,) * (width - len(word)))[2]
                right = target + (base - 1,) * (width - len(target) + g)
                require(left == right, "common-width u=g transport failed")
                counts["legal_trim_equalities"] += 1

    for base in range(2, 7):
        for period in range(1, 6):
            for overflow in product((0, 1), repeat=period):
                root = root_word(base, overflow)
                generic = closed_image(base, overflow, root, False)
                positive = closed_image(base, overflow, root, True)
                if any(overflow):
                    require(generic == positive, "positive-overflow root admits a zero head")
                else:
                    require(generic == {root} and not positive,
                            "zero-overflow FIRST/root distinction failed")
                counts["first_language_cases"] += 1
        for e, g in product((0, 1), repeat=2):
            require(root_word(base, (g,)) != terminal_word(base, (e,), (g,)),
                    "zero-width root was misidentified with a terminal")
            counts["zero_width_terminal_rejections"] += 1

    for base, edges in mirror._lean_certs():
        words = [tuple(edge[0]) for edge in edges]
        entering, overflow = [], []
        for t, edge in enumerate(edges):
            e, g, raw = exterior_step(base, words[t])
            require(tuple(edge[2]) == words[(t + 1) % len(words)] and
                    raw == tuple(edge[2]) + (base - 1,) * edge[4], "source B cycle does not close")
            entering.append(e)
            overflow.append(g)
            counts["source_edges"] += 1
        width = max(1, max(map(len, words)))
        padded = [word + (base - 1,) * (width - len(word)) for word in words]
        cut = cut_word(base, padded, entering, overflow, 0)
        require(cut == root_word(base, overflow), "physical cut differs from root")
        for position in range(width):
            successor = cut_word(base, padded, entering, overflow, position + 1)
            for t in range(len(words)):
                row = (padded[t][position], successor[t], padded[(t + 1) % len(words)][position])
                require(row in local_rows(base, overflow, cut[t], position == 0),
                        "whole-integer source cut violates the local orientation")
                counts["source_cut_tiles"] += 1
            cut = successor
        require(cut == terminal_word(base, entering, overflow), "source cut misses exact terminal")
        for t, word in enumerate(padded):
            e, g, raw = exterior_step(base, word)
            require((e, g) == (entering[t], overflow[t]) and
                    raw == padded[(t + 1) % len(words)] + (base - 1,) * g,
                    "padded source cycle failed complete integer replay")
        counts["source_cycles"] += 1
    return counts


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
