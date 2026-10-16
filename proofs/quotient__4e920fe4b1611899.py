"""Independent implementation of the complementary-band quotient (Agent #2).

Reference: ../2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md,
sections 2--6, at integration head a71d6e79b009da691e2d97057f83e108a3fcff4f.
Words are least-significant-column first. No third-party dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

Word = tuple[int, ...]
PHASES = tuple(c for c in range(1, 18) if c != 9)
PERIODIC_PHASES = (2, 4, 6, 8, 10, 12, 14, 16)


def carry_normalize(word: Word, carry: int = 0) -> tuple[Word, int]:
    if carry not in (0, 1) or any(not 0 <= x <= 18 for x in word):
        raise ValueError("invalid coefficient word or incoming carry")
    digits = []
    for x in word:
        carry, digit = divmod(x + carry, 10)
        digits.append(digit)
    return tuple(digits), carry


def pair(word: Word) -> Word:
    return tuple(a + b for a, b in zip(word, reversed(word)))


def add_words(a: Word, b: Word) -> Word:
    if len(a) != len(b):
        raise ValueError("coordinatewise addition requires equal lengths")
    return tuple(x + y for x, y in zip(a, b))


def phase_next(c: int) -> int:
    if c not in PHASES:
        raise ValueError("invalid nonneutral phase")
    return 2 * (c - 9 * int(c >= 10))


@dataclass(frozen=True)
class State:
    c: int
    B: Word = ()
    A: Word = ()
    C: Word = ()

    def __post_init__(self) -> None:
        if self.c not in PHASES:
            raise ValueError("invalid phase")
        if any(not 0 <= x <= 18 for W in (self.B, self.A, self.C) for x in W):
            raise ValueError("invalid coefficient")
        if self.B and self.B[0] == 0:
            raise ValueError("noncanonical exterior")
        if self.C != self.C[::-1]:
            raise ValueError("asymmetric center")
        if len(self.C) % 2 and self.C[len(self.C) // 2] % 2:
            raise ValueError("odd middle coefficient")

    @property
    def interface_width(self) -> int:
        return 2 * len(self.B) + 2 * len(self.A) + len(self.C)

    def word(self, g: int, h: int) -> Word:
        if g < 0 or h < 0:
            raise ValueError("negative band length")
        c, d = self.c, 18 - self.c
        return (self.B + (c,) * g + self.A + (d,) * h + self.C
                + (d,) * h + self.A[::-1] + (c,) * g + self.B[::-1])

    def to_json(self) -> list:
        return [self.c, list(self.B), list(self.A), list(self.C)]


def canonical_trim(state: State) -> tuple[State, int, int]:
    """Move maximal adjacent phase suffixes/prefixes into the two bands."""
    c, d = state.c, 18 - state.c
    B, A, C = state.B, state.A, state.C
    ub = 0
    while B and B[-1] == c:
        ub += 1
        B = B[:-1]
    va = 0
    while A and A[0] == c:
        va += 1
        A = A[1:]
    ua = 0
    while A and A[-1] == d:
        ua += 1
        A = A[:-1]
    vc = 0
    while len(C) >= 2 and C[0] == d and C[-1] == d:
        vc += 1
        C = C[1:-1]
    return State(c, B, A, C), ub + va, ua + vc


def transition(state: State) -> tuple[State, int, int, int]:
    """Return actual next interface, delta_g, delta_h, and overflow.

    For g,h >= 2, G(Q(state,g,h)) equals Q(next,g+delta_g,h+delta_h).
    No future-domain condition or recurrent behavior is assumed.
    """
    c, d = state.c, 18 - state.c
    kc, kd = int(c >= 10), int(d >= 10)
    tc, td = c - 9 * kc, d - 9 * kd
    DB, e0 = carry_normalize(state.B, 0)
    DA, e1 = carry_normalize(state.A, kc)
    DC, e2 = carry_normalize(state.C, kd)
    DRA, e3 = carry_normalize(state.A[::-1], kd)
    DRB, overflow = carry_normalize(state.B[::-1], kc)
    u0, u1 = c + e0 - 10 * kc, d + e1 - 10 * kd
    u2, u3 = d + e2 - 10 * kd, c + e3 - 10 * kc
    if overflow:
        Br = add_words(DB + (u0,), (1,) + DRB[::-1])
        Ar = add_words(DA + (u1,), (u3,) + DRA[::-1])
        Cr = pair(DC + (u2,))
    else:
        Br = add_words(DB + (u0,), DRB[::-1] + (tc,))
        Ar = add_words((tc,) + DA + (u1,), (u3,) + DRA[::-1] + (td,))
        Cr = pair((td,) + DC + (u2,))
    target, gain_g, gain_h = canonical_trim(State(phase_next(c), Br, Ar, Cr))
    dg, dh = gain_g - 2 + overflow, gain_h - 2 + overflow
    assert target.interface_width + 2 * dg + 2 * dh == state.interface_width + overflow
    return target, dg, dh, overflow


def integer_value(word: Word) -> int:
    value = 0
    for x in reversed(word):
        value = 10 * value + x
    return value


def integer_pair_word(value: int) -> Word:
    if value <= 0:
        raise ValueError("expected a positive ordinary integer")
    digits = tuple(map(int, str(value)[::-1]))
    return pair(digits)


def actual_G(word: Word) -> Word:
    """Independent oracle using Python integer evaluation and decimal conversion."""
    return integer_pair_word(integer_value(word))


def realize(word: Word) -> int:
    if not word or word != word[::-1] or word[0] <= 0:
        raise ValueError("expected a nonempty canonical symmetric coefficient word")
    if any(not 0 <= x <= 18 for x in word):
        raise ValueError("invalid coefficient")
    n = len(word)
    digits = [0] * n
    for i in range(n // 2):
        digits[n - 1 - i] = min(word[i], 9)
        digits[i] = word[i] - digits[n - 1 - i]
    if n % 2:
        if word[n // 2] % 2:
            raise ValueError("odd middle coefficient")
        digits[n // 2] = word[n // 2] // 2
    return integer_value(tuple(digits))


def reverse_add(n: int) -> int:
    if n <= 0:
        raise ValueError("expected a positive integer")
    return n + int(str(n)[::-1])


def is_palindrome(n: int) -> bool:
    text = str(n)
    return text == text[::-1]
