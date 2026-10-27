#!/usr/bin/env python3
"""Independent coefficient checks for Agent 112's integer center model.

Run from the repository root:
    python3 calculation/agent-112/check_integer_state.py

The reference calculations below normalize coefficient lists column by column;
they do not use the repository Python mirror or the proposed integer recurrence.
Known certificates are read as data from their two existing Lean source files.
No output files, logs, or theorem claims are produced. This is COMPUTED evidence.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import re
from fractions import Fraction
from pathlib import Path

from center_integer import (
    Center,
    decode,
    encode,
    fixed_reverse,
    from_padding_key,
    normalize,
    padding_key,
    step,
)


ROOT = Path(__file__).resolve().parents[2]


def value(base: int, coefficients: tuple[int, ...]) -> int:
    """Horner evaluation, retaining the supplied coefficient width."""
    result = 0
    for coefficient in reversed(coefficients):
        result = base * result + coefficient
    return result


def state(base: int, coefficients: tuple[int, ...]) -> Center:
    return Center(len(coefficients), value(base, coefficients) - base ** len(coefficients) + 1)


def digit_normalization(
    base: int, coefficients: tuple[int, ...], incoming: int
) -> tuple[tuple[int, ...], int]:
    """Fresh direct column arithmetic; no integer model calls."""
    carry = incoming
    digits = []
    for coefficient in coefficients:
        carry, digit = divmod(coefficient + carry, base)
        digits.append(digit)
    return tuple(digits), carry


def trim_center(base: int, coefficients: tuple[int, ...]) -> tuple[tuple[int, ...], int]:
    trim = 0
    end = len(coefficients)
    while trim + 1 < end and coefficients[trim] == coefficients[end - 1] == base - 1:
        trim += 1
        end -= 1
    return coefficients[trim:end], trim


def trim_exterior(base: int, coefficients: tuple[int, ...]) -> tuple[tuple[int, ...], int]:
    end = len(coefficients)
    while end and coefficients[end - 1] == base - 1:
        end -= 1
    return coefficients[:end], len(coefficients) - end


def direct_center(
    base: int, coefficients: tuple[int, ...], incoming: int, overflow: int
) -> tuple[tuple[int, ...], tuple[int, ...], int]:
    digits, outgoing = digit_normalization(base, coefficients, incoming)
    assert outgoing == 1 - incoming
    extended = digits + ((base - 1) * incoming,) if overflow else digits
    raw = tuple(a + b for a, b in zip(extended, reversed(extended)))
    target, trim = trim_center(base, raw)
    return raw, target, trim


def check_word(base: int, coefficients: tuple[int, ...], counts: dict[str, int]) -> None:
    source = state(base, coefficients)
    assert encode(base, coefficients) == source
    assert tuple(decode(base, source)) == coefficients
    canonical, removed = trim_center(base, coefficients)
    canonical_state = state(base, canonical)
    assert normalize(base, source) == (canonical_state, removed)
    key = padding_key(base, source)
    assert key == padding_key(base, canonical_state)
    assert from_padding_key(base, *key) == canonical_state
    counts["words"] += 1
    counts["positive" if source.signed > 0 else "negative" if source.signed < 0 else "zero"] += 1
    if not source.signed:
        for incoming in (0, 1):
            assert digit_normalization(base, coefficients, incoming)[1] == incoming
        for overflow in (0, 1):
            try:
                step(base, source, overflow)
            except ValueError:
                pass
            else:
                raise AssertionError(("zero source accepted", base, source, overflow))
        return
    incoming = int(source.signed < 0)
    assert digit_normalization(base, coefficients, incoming)[1] == 1 - incoming
    other = 1 - incoming
    assert digit_normalization(base, coefficients, other)[1] == other
    for overflow in (0, 1):
        raw, target, trim = direct_center(base, coefficients, incoming, overflow)
        actual = step(base, source, overflow)
        expected_raw, expected_target = state(base, raw), state(base, target)
        assert actual.source == source
        assert actual.incoming == incoming
        assert actual.overflow == overflow
        assert actual.raw == expected_raw, (base, coefficients, overflow, actual, expected_raw)
        assert actual.target == expected_target
        assert actual.trim == trim
        assert actual.next_incoming == (int(expected_target.signed < 0) if expected_target.signed else None)
        assert tuple(decode(base, actual.raw)) == raw
        assert tuple(decode(base, actual.target)) == target
        counts["transitions"] += 1
        counts["raw_zero"] += int(expected_raw.signed == 0)
        counts["trimmed"] += int(trim > 0)
        counts["multi_trim"] += int(trim > 1)
        counts["max_trim"] = max(counts["max_trim"], trim)


def blank_counts() -> dict[str, int]:
    return dict(words=0, positive=0, negative=0, zero=0, transitions=0,
                raw_zero=0, trimmed=0, multi_trim=0, max_trim=0)


def exhaustive() -> dict:
    bounds = ((2, 9), (3, 8), (4, 8), (5, 6), (10, 6),
              (11, 6), (17, 4), (26, 4), (32, 4))
    counts = blank_counts()
    per_base = {}
    for base, maximum_width in bounds:
        before = counts["words"]
        for width in range(1, maximum_width + 1):
            signatures = set()
            half_width = (width + 1) // 2
            for half in itertools.product(range(2 * base - 1), repeat=half_width):
                coefficients = half + half[: width // 2][::-1]
                source = state(base, coefficients)
                assert source.signed not in signatures
                signatures.add(source.signed)
                check_word(base, coefficients, counts)
        per_base[str(base)] = {"maximum_width": maximum_width, "words": counts["words"] - before}
    return {"counts": counts, "scopes": per_base}


def random_checks(seed: int, pairs: int) -> dict:
    rng = random.Random(seed)
    counts = blank_counts()
    max_width = 0
    for _ in range(pairs):
        base = rng.choice((2, 3, 4, 5, 10, 11, 17, 26, 32, 62))
        width = rng.randint(1, 160)
        half = tuple(rng.randrange(2 * base - 1) for _ in range((width + 1) // 2))
        if all(coefficient == base - 1 for coefficient in half):
            half = (base,) + half[1:]
        core = half + half[: width // 2][::-1]
        padding = (base - 1,) * rng.randrange(7)
        coefficients = padding + core + padding
        complement = tuple(2 * base - 2 - coefficient for coefficient in coefficients)
        max_width = max(max_width, len(coefficients))
        assert state(base, coefficients).signed == -state(base, complement).signed != 0
        assert padding_key(base, state(base, core)) == padding_key(base, state(base, coefficients))
        check_word(base, coefficients, counts)
        check_word(base, complement, counts)
        for overflow in (0, 1):
            a = step(base, state(base, coefficients), overflow)
            b = step(base, state(base, complement), overflow)
            assert a.raw.width == b.raw.width and a.raw.signed == -b.raw.signed
            assert a.target.width == b.target.width and a.target.signed == -b.target.signed
            assert a.trim == b.trim
    return {"seed": seed, "pairs": pairs, "maximum_width": max_width, "counts": counts}


def read_known_certificates() -> list[tuple[int, list[tuple]]]:
    files = (
        ROOT / "lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean",
        ROOT / "lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean",
    )
    list_literal = r"\[[^\]]*\]"
    term = rf"({list_literal}|[A-Za-z_][A-Za-z_0-9]*)"
    edge_pattern = re.compile(rf"⟨\s*{term}\s*,\s*{term}\s*,\s*{term}\s*,\s*{term}\s*,\s*(\d+)\s*,\s*(\d+)\s*⟩")
    certificates = []
    for path in files:
        text = path.read_text()
        definitions = {}
        def parse_list(literal: str) -> tuple[int, ...]:
            contents = literal.strip()[1:-1].strip()
            return tuple(map(int, contents.split(","))) if contents else ()
        for match in re.finditer(rf"def\s+(\w+)\s*:\s*List Nat\s*:=\s*({list_literal})", text):
            definitions[match[1]] = parse_list(match[2])
        for match in re.finditer(r"def cert(\d+)\s*:\s*List Edge\s*:=\s*(\[.*?\])\s*\n\n", text, re.S):
            edges = []
            for edge in edge_pattern.finditer(match[2]):
                words = tuple(parse_list(edge[i]) if edge[i].startswith("[") else definitions[edge[i]]
                              for i in range(1, 5))
                edges.append((*words, int(edge[5]), int(edge[6])))
            assert edges, (path, match[1])
            certificates.append((int(match[1]), edges))
    assert {base for base, _ in certificates} == {2, 4, 8, 11, 16, 17, 26, 32}
    assert sum(len(edges) for _, edges in certificates) == 56
    return sorted(certificates)


def direct_edge(base: int, exterior: tuple[int, ...], center: tuple[int, ...]) -> tuple:
    digits_left, incoming = digit_normalization(base, exterior, 0)
    _, center_out = digit_normalization(base, center, incoming)
    assert center_out == 1 - incoming
    digits_right, overflow = digit_normalization(base, exterior[::-1], center_out)
    if overflow:
        left = digits_left + ((base - 1) * (1 - incoming),)
        right = (1,) + digits_right[::-1]
    else:
        left, right = digits_left, digits_right[::-1]
    raw_exterior = tuple(a + b for a, b in zip(left, right))
    raw_center, _, _ = direct_center(base, center, incoming, overflow)
    return raw_exterior, raw_center, incoming, overflow


def known_controls() -> dict:
    rows = []
    for base, edges in read_known_certificates():
        original = normalized = 0
        for index, (exterior, center, exterior2, center2, u, v) in enumerate(edges):
            assert edges[(index + 1) % len(edges)][:2] == (exterior2, center2)
            raw_b, raw_c, incoming, overflow = direct_edge(base, exterior, center)
            assert raw_b == exterior2 + (base - 1,) * u
            assert raw_c == (base - 1,) * v + center2 + (base - 1,) * v
            assert state(base, center).signed != 0
            transition = step(base, state(base, center), overflow)
            assert transition.raw == state(base, raw_c)
            assert transition.incoming == incoming
            assert transition.target == normalize(base, state(base, center2))[0]
            original += 1
            b0, _ = trim_exterior(base, exterior)
            c0, _ = trim_center(base, center)
            b1, _ = trim_exterior(base, exterior2)
            c1, _ = trim_center(base, center2)
            raw_bn, raw_cn, en, gn = direct_edge(base, b0, c0)
            assert en == incoming and gn == overflow
            assert trim_exterior(base, raw_bn)[0] == b1
            assert trim_center(base, raw_cn)[0] == c1
            normalized_transition = step(base, state(base, c0), gn)
            assert normalized_transition.raw == state(base, raw_cn)
            assert normalized_transition.target == state(base, c1)
            normalized += 1
        rows.append({"base": base, "original_edges": original, "normalized_edges": normalized})
    return {"certificates": rows, "original_edges": sum(row["original_edges"] for row in rows),
            "normalized_edges": sum(row["normalized_edges"] for row in rows)}


def explicit_controls() -> dict:
    # Equal signed deviations at different widths are not equivalent states.
    base = 10
    examples = []
    for width in (2, 3, 4):
        coefficients = (base,) + (0,) * (width - 2) + (base,)
        source = state(base, coefficients)
        assert source.signed == base + 1
        raw, target, trim = direct_center(base, coefficients, 0, 0)
        transition = step(base, source, 0)
        assert transition.raw == state(base, raw)
        assert transition.target == state(base, target)
        examples.append({"coefficients": coefficients, "width": width, "signed": source.signed,
                         "target_width": transition.target.width,
                         "target_signed": transition.target.signed, "trim": trim})
    assert [example["target_signed"] for example in examples] == [-88, -979, -9889]
    # Empty and neutral centers are representable, but cannot meet the flip guard.
    zero_controls = blank_counts()
    for base in (2, 10, 26):
        for width in range(13):
            check_word(base, (base - 1,) * width, zero_controls)
    # Fixed-width reversal retains zero padding, unlike ordinary reversal.
    reverse_controls = 0
    for base in (2, 3, 10, 26):
        for width in range(5):
            for number in range(base ** width):
                if number > 2000:
                    break
                quotient = number
                digits = []
                for _ in range(width):
                    quotient, digit = divmod(quotient, base)
                    digits.append(digit)
                expected = value(base, tuple(reversed(digits)))
                assert fixed_reverse(base, number, width) == expected
                reverse_controls += 1
    return {"width_collision": examples, "zero_controls": zero_controls,
            "fixed_reverse_cases": reverse_controls}


def decoder_controls() -> dict:
    """Check the complete bounded scalar domain, including all missing words."""
    accepted = rejected = 0
    scopes = ((2, 7), (3, 5), (10, 4), (26, 2))
    for base, maximum_width in scopes:
        for width in range(maximum_width + 1):
            representable = {}
            for half in itertools.product(range(2 * base - 1), repeat=(width + 1) // 2):
                word = half + half[: width // 2][::-1]
                signed = state(base, word).signed
                assert signed not in representable
                representable[signed] = word
            for signed in range(1 - base ** width, base ** width):
                try:
                    word = tuple(decode(base, Center(width, signed)))
                except ValueError:
                    assert signed not in representable, (base, width, signed)
                    rejected += 1
                else:
                    assert representable.get(signed) == word, (base, width, signed, word)
                    accepted += 1
    invalid_calls = (
        lambda: encode(1, ()),
        lambda: encode(True, ()),
        lambda: encode(10, (-1,)),
        lambda: encode(10, (19,)),
        lambda: encode(10, (True,)),
        lambda: encode(10, (1, 2)),
        lambda: decode(10, (2, 11)),
        lambda: decode(10, Center(-1, 0)),
        lambda: decode(10, Center(1, True)),
        lambda: decode(10, Center(2, 5)),
        lambda: decode(10, Center(0, 1)),
        lambda: decode(10, Center(2, 100)),
        lambda: normalize(10, Center(2, 5)),
        lambda: fixed_reverse(10, 1, -1),
        lambda: fixed_reverse(10, 10, 1),
        lambda: fixed_reverse(10, -1, 1),
        lambda: step(10, Center(2, 11), 2),
        lambda: step(10, Center(2, 11), True),
        lambda: step(10, Center(2, 0), 0),
        lambda: from_padding_key(10, 2, Fraction(1, 2)),
        lambda: from_padding_key(10, 0, Fraction(1, 3)),
        lambda: from_padding_key(10, 0, Fraction(1, 2)),
        lambda: from_padding_key(10, 0, 0.5),
    )
    for call in invalid_calls:
        try:
            call()
        except ValueError:
            pass
        else:
            raise AssertionError("invalid API input was accepted")
    return {"scopes": {str(base): maximum_width for base, maximum_width in scopes},
            "accepted": accepted, "rejected": rejected, "invalid_api_calls": len(invalid_calls)}


def main() -> None:
    if not __debug__:
        raise SystemExit("Assertions are required; run this validation without python -O.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=112)
    parser.add_argument("--random-pairs", type=int, default=2000)
    parser.add_argument("--controls-only", action="store_true")
    args = parser.parse_args()
    assert args.random_pairs >= 0
    output = {"status": "COMPUTED", "known_controls": known_controls(),
              "explicit_controls": explicit_controls(), "decoder_controls": decoder_controls()}
    if not args.controls_only:
        output["exhaustive"] = exhaustive()
        output["random"] = random_checks(args.seed, args.random_pairs)
    print(json.dumps(output, indent=2, sort_keys=True))
    print("PASS: independent coefficient arithmetic agrees with the integer center model.")


if __name__ == "__main__":
    main()
