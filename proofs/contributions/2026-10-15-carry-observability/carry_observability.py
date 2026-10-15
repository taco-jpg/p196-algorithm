"""Exact carry observations and reconstruction for reverse-and-add.

All words are least-significant-column first. A complete carry word includes
both the initial zero and final overflow bit. Iteration continues after a
palindrome. The decoder reconstructs pair sums, NOT the original digit split.

Ten observations suffice for every positive decimal input by the separately
checked Lean theorem. The algebraic decoder also works in any base >= 2 when
the supplied history has enough nonoverflow steps; no ten-step bound in other
bases is claimed.
"""
from __future__ import annotations

from collections import defaultdict
from itertools import product
from math import comb
from typing import Iterable, Iterator, Sequence

PairWord = tuple[int, ...]
CarryWord = tuple[int, ...]


class InsufficientObservations(ValueError):
    """This decoder's multiplier condition fails; uniqueness may still hold."""


def _check_base(base: int) -> None:
    if type(base) is not int or base < 2:
        raise ValueError("base must be an integer at least two")


def canonical_word(word: Iterable[int], base: int = 10) -> PairWord:
    """Validate precisely the realizable positive finite pair-sum conditions."""
    _check_base(base)
    q = tuple(word)
    if not q or any(type(a) is not int or not 0 <= a <= 2 * base - 2 for a in q):
        raise ValueError("a nonempty word of integer pair sums in range is required")
    if q[0] == 0 or q != q[::-1]:
        raise ValueError("the pair word must be symmetric with positive outside coefficient")
    if len(q) % 2 and q[len(q) // 2] % 2:
        raise ValueError("the center pair sum of an odd-width word must be even")
    return q


def _step(q: PairWord, base: int) -> tuple[PairWord, CarryWord]:
    """Internal arithmetic on a previously validated word."""
    carries = [0]
    digits = []
    for a in q:
        outgoing, digit = divmod(a + carries[-1], base)
        carries.append(outgoing)
        digits.append(digit)
    if carries[-1]:
        digits.append(carries[-1])
    return tuple(a + b for a, b in zip(digits, reversed(digits))), tuple(carries)


def step(word: Iterable[int], base: int = 10) -> tuple[PairWord, CarryWord]:
    """Return the exact next pair word and the current complete carry word."""
    return _step(canonical_word(word, base), base)


def trace(word: Iterable[int], observations: int, base: int = 10) -> list[tuple[PairWord, CarryWord]]:
    if type(observations) is not int or observations < 0:
        raise ValueError("observations must be a nonnegative integer")
    q = canonical_word(word, base)
    result = []
    for _ in range(observations):
        nxt, carries = _step(q, base)
        result.append((q, carries))
        q = nxt
    return result


def carry_history(word: Iterable[int], observations: int = 10, base: int = 10) -> tuple[CarryWord, ...]:
    return tuple(c for _, c in trace(word, observations, base))


def pair_word(n: int, base: int = 10) -> PairWord:
    _check_base(base)
    if type(n) is not int or n <= 0:
        raise ValueError("n must be a positive integer")
    digits = []
    while n:
        n, digit = divmod(n, base)
        digits.append(digit)
    return tuple(a + b for a, b in zip(digits, reversed(digits)))


def reverse_number(n: int, base: int = 10) -> int:
    _check_base(base)
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    result = 0
    while n:
        n, digit = divmod(n, base)
        result = base * result + digit
    return result


def realize(word: Iterable[int], base: int = 10) -> int:
    """Choose one positive ordinary integer realization, without claiming uniqueness."""
    q = canonical_word(word, base)
    digits = [0] * len(q)
    for i in range(len(q) // 2):
        digits[-1 - i] = min(q[i], base - 1)
        digits[i] = q[i] - digits[-1 - i]
    if len(q) % 2:
        digits[len(q) // 2] = q[len(q) // 2] // 2
    result = 0
    for digit in reversed(digits):
        result = base * result + digit
    return result


def word_value(word: Sequence[int], base: int = 10) -> int:
    """For a valid input word this is the next ordinary integer, not a realization."""
    _check_base(base)
    result = 0
    for coefficient in reversed(word):
        result = base * result + coefficient
    return result


def prefix_transition(p: int, q: int, v: int, base: int = 10) -> tuple[tuple[int, int], int]:
    """Necessary two-column map; v is the actual carry at input column L-2.

    Freely selecting v produces an overapproximation, not an actual full orbit.
    Return value is (next outside two coefficients, nonoverflow indicator).
    """
    _check_base(base)
    if not (type(p) is type(q) is type(v) is int and
            1 <= p <= 2 * base - 2 and 0 <= q <= 2 * base - 2 and v in (0, 1)):
        raise ValueError("invalid prefix state or carry bit")
    a = p // base
    u = (q + v) // base
    b = (q + a) // base
    h = (p + u) // base
    if h:
        target = p - base * a + 1, p + q + a + u - base * (b + h)
    else:
        target = 2 * p + u - base * a, 2 * q + a + v - base * (b + u)
    return target, 1 - h


def decode_carries(history: Iterable[Iterable[int]], base: int = 10) -> PairWord:
    """Recover the unique pair word under the multiplier criterion, or raise.

    Structural errors and unrealizable histories raise ValueError.
    InsufficientObservations means only that this particular decoder requires
    a larger multiplier; it does not assert ambiguity of the observations.
    Returned candidates are validated by an exact full-history replay.
    """
    _check_base(base)
    rows = tuple(tuple(row) for row in history)
    if not rows:
        raise ValueError("at least one complete carry word is required")
    initial_width = len(rows[0]) - 1
    if initial_width < 1:
        raise ValueError("a carry word must contain the initial and final carry")
    width = initial_width
    for row in rows:
        if len(row) != width + 1 or row[0] != 0:
            raise ValueError("carry-word length or initial-zero condition is inconsistent")
        if any(type(c) is not int or c not in (0, 1) for c in row):
            raise ValueError("every carry must be the integer zero or one")
        width += row[-1]

    nonoverflows = sum(row[-1] == 0 for row in rows[:-1])
    overflows = len(rows) - 1 - nonoverflows
    scale = 1 << nonoverflows
    if scale <= base - 1:
        raise InsufficientObservations(
            f"multiplier {scale} must exceed the endpoint interval width {base - 1}")

    # Q_K = 2^N (1+x)^H Q_0 + R_K. R_K is determined only by carries.
    remainder = [0] * initial_width
    for row in rows[:-1]:
        length = len(row) - 1
        digit_offsets = [row[i] - base * row[i + 1] for i in range(length)]
        if row[-1]:
            digit_offsets.append(1)
        offset = [a + b for a, b in zip(digit_offsets, reversed(digit_offsets))]
        if row[-1]:
            remainder = [
                (remainder[i] if i < length else 0)
                + (remainder[i - 1] if i > 0 else 0)
                + offset[i]
                for i in range(length + 1)
            ]
        else:
            remainder = [2 * a + b for a, b in zip(remainder, offset)]

    multiplier = [scale * comb(overflows, j) for j in range(overflows + 1)]
    endpoint = rows[-1]
    result: list[int] = []
    for i in range(initial_width):
        known = remainder[i] + sum(
            multiplier[j] * result[i - j] for j in range(1, min(i, overflows) + 1))
        lower = max(0, base * endpoint[i + 1] - endpoint[i])
        upper = min(2 * base - 2, base * endpoint[i + 1] + base - 1 - endpoint[i])
        low_candidate = max(0, -((known - lower) // scale))
        high_candidate = min(2 * base - 2, (upper - known) // scale)
        if low_candidate != high_candidate:
            raise ValueError(f"no uniquely consistent initial coefficient at index {i}")
        result.append(low_candidate)

    candidate = canonical_word(result, base)
    if carry_history(candidate, len(rows), base) != rows:
        raise ValueError("the reconstructed candidate does not realize the full supplied history")
    return candidate


def canonical_words(width: int, base: int = 10) -> Iterator[PairWord]:
    _check_base(base)
    if type(width) is not int or width < 1:
        raise ValueError("width must be a positive integer")
    if width == 1:
        yield from ((2 * digit,) for digit in range(1, base))
        return
    choices = [range(1, 2 * base - 1)] + [range(2 * base - 1)] * (width // 2 - 1)
    for half in product(*choices):
        if width % 2:
            for center in range(0, 2 * base - 1, 2):
                yield half + (center,) + half[::-1]
        else:
            yield half + half[::-1]


def collision_partition(width: int, max_observations: int = 10) -> dict:
    """Exhaust an explicitly fixed width; no all-width injectivity inference."""
    groups = [[(q, q) for q in canonical_words(width)]]
    result = {"width": width, "words": len(groups[0]), "depths": []}
    for depth in range(1, max_observations + 1):
        next_groups = []
        witness = None
        sizes = []
        for group in groups:
            buckets: dict[CarryWord, list[tuple[PairWord, PairWord]]] = defaultdict(list)
            for initial, current in group:
                nxt, row = _step(current, 10)
                buckets[row].append((initial, nxt))
            for bucket in buckets.values():
                if len(bucket) > 1:
                    next_groups.append(bucket)
                    sizes.append(len(bucket))
                    if witness is None:
                        pair = [bucket[i][0] for i in (0, 1)]
                        witness = {"q": pair, "n": [realize(q) for q in pair]}
        result["depths"].append({
            "carry_words": depth, "collision_classes": len(next_groups),
            "ambiguous_words": sum(sizes), "largest_class": max(sizes, default=1),
            "witness": witness})
        groups = next_groups
        if not groups:
            break
    return result
