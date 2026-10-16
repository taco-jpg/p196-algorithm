"""Exact complementary-bulk quotient and autonomous outer factor.

Words are least-significant first. Mathematical source: Sections 2--6 of
../2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md at a71d6e7.
Independent Agent #3 implementation. No infinite-orbit claim is made.
"""
from __future__ import annotations
from dataclasses import dataclass

Word = tuple[int, ...]
PHASES = (2, 4, 6, 8, 10, 12, 14, 16)
ADMISSIBLE = tuple(range(1, 9)) + tuple(range(10, 18))


def normalize(w: Word, incoming: int = 0) -> tuple[Word, int]:
    """Normalize coefficients, retaining the same width and a final carry."""
    if incoming not in (0, 1) or any(not 0 <= x <= 18 for x in w):
        raise ValueError("Coefficients must be 0..18 and the carry 0 or 1")
    digits = []
    carry = incoming
    for x in w:
        carry, digit = divmod(x + carry, 10)
        digits.append(digit)
    return tuple(digits), carry


def plus(a: Word, b: Word) -> Word:
    if len(a) != len(b):
        raise ValueError("Coordinatewise addition requires equal widths")
    return tuple(x + y for x, y in zip(a, b))


def pair(digits: Word) -> Word:
    return plus(digits, digits[::-1])


def phase(c: int) -> int:
    if c not in ADMISSIBLE:
        raise ValueError("Phase must be 1..17, excluding 9")
    return 2 * (c - 9 * (c >= 10))


@dataclass(frozen=True)
class State:
    c: int
    B: Word = ()
    A: Word = ()
    C: Word = ()

    def validate(self) -> None:
        phase(self.c)
        if any(not 0 <= x <= 18 for w in (self.B, self.A, self.C) for x in w):
            raise ValueError("Invalid interface coefficient")
        if self.B and self.B[0] == 0:
            raise ValueError("The exterior coefficient must be positive")
        if self.C != self.C[::-1]:
            raise ValueError("The central block must be symmetric")
        if len(self.C) % 2 and self.C[len(self.C) // 2] % 2:
            raise ValueError("An odd-width central coefficient must be even")


@dataclass(frozen=True)
class Edge:
    target: State
    delta_g: int
    delta_h: int
    overflow: int
    strips: tuple[int, int, int, int]


def make_word(s: State, g: int, h: int) -> Word:
    s.validate()
    if g < 0 or h < 0:
        raise ValueError("Gap lengths must be nonnegative")
    c, B, A, C = s.c, s.B, s.A, s.C
    d = 18 - c
    return B + (c,) * g + A + (d,) * h + C + (d,) * h + A[::-1] + (c,) * g + B[::-1]


def actual_step(q: Word) -> Word:
    """Canonical normalization then mirrored digit sum; no quotient formulas."""
    digits, carry = normalize(q)
    if carry:
        digits += (carry,)
    if not digits or digits[-1] == 0:
        raise ValueError("Source does not have a canonical positive exterior")
    return pair(digits)


def _strip_suffix(w: Word, c: int) -> tuple[Word, int]:
    n = len(w)
    while n and w[n - 1] == c:
        n -= 1
    return w[:n], len(w) - n


def outer_step(c: int, B: Word) -> tuple[int, Word, int, int]:
    """Return (new phase, new outer block, actual overflow, suffix strip).

    This depends on no interior interface or gap. B need not be trimmed.
    """
    if c not in ADMISSIBLE or (B and B[0] == 0):
        raise ValueError("Invalid outer state")
    k = int(c >= 10)
    t = c - 9 * k
    db, e0 = normalize(B, 0)
    drb, gamma = normalize(B[::-1], k)
    u0 = c + e0 - 10 * k
    right = (1,) + drb[::-1] if gamma else drb[::-1] + (t,)
    raw = plus(db + (u0,), right)
    target, strips = _strip_suffix(raw, 2 * t)
    return 2 * t, target, gamma, strips


def quotient_step(s: State) -> Edge:
    s.validate()
    c, B, A, C = s.c, s.B, s.A, s.C
    d = 18 - c
    kc, kd = int(c >= 10), int(d >= 10)
    tc, td = c - 9 * kc, d - 9 * kd
    db, e0 = normalize(B)
    da, e1 = normalize(A, kc)
    dc, e2 = normalize(C, kd)
    dra, e3 = normalize(A[::-1], kd)
    drb, gamma = normalize(B[::-1], kc)
    u0, u1 = c + e0 - 10 * kc, d + e1 - 10 * kd
    u2, u3 = d + e2 - 10 * kd, c + e3 - 10 * kc
    if gamma:
        br = plus(db + (u0,), (1,) + drb[::-1])
        ar = plus(da + (u1,), (u3,) + dra[::-1])
        cr = pair(dc + (u2,))
    else:
        br = plus(db + (u0,), drb[::-1] + (tc,))
        ar = plus((tc,) + da + (u1,), (u3,) + dra[::-1] + (td,))
        cr = pair((td,) + dc + (u2,))
    cp, dp = 2 * tc, 2 * td
    br, ub = _strip_suffix(br, cp)
    rev_ar, va = _strip_suffix(ar[::-1], cp)
    ar, ua = _strip_suffix(rev_ar[::-1], dp)
    vc = 0
    while len(cr) >= 2 and cr[0] == dp and cr[-1] == dp:
        cr = cr[1:-1]
        vc += 1
    target = State(cp, br, ar, cr)
    target.validate()
    edge = Edge(target, ub + va - 2 + gamma, ua + vc - 2 + gamma,
                gamma, (ub, va, ua, vc))
    assert outer_step(c, B) == (cp, br, gamma, ub)
    assert 2 * len(br) + 2 * len(ar) + len(cr) + 2 * edge.delta_g + 2 * edge.delta_h == (
        2 * len(B) + 2 * len(A) + len(C) + gamma)
    return edge
