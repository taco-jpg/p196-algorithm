"""Agent #8: independent implementation of the complementary-bulk quotient.

Source convention: coefficient words are least-significant first.  The quotient
identity is from the repository's 2026-10-15 complementary-bulk note, sections 2-6.
No search result is a proof of decimal Lychrel existence or nonexistence.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

Word = tuple[int, ...]
PHASES = tuple(x for x in range(1, 18) if x != 9)
PERIODIC_PHASES = (2, 4, 6, 8, 10, 12, 14, 16)


def normalize(w: Word, carry: int = 0) -> tuple[Word, int]:
    if carry not in (0, 1) or any(not 0 <= x <= 18 for x in w):
        raise ValueError("invalid coefficients or incoming carry")
    digits = []
    for x in w:
        carry, digit = divmod(x + carry, 10)
        digits.append(digit)
    return tuple(digits), carry


def add_words(a: Word, b: Word) -> Word:
    if len(a) != len(b):
        raise ValueError("word lengths differ")
    return tuple(x + y for x, y in zip(a, b))


def pair(w: Word) -> Word:
    return add_words(w, w[::-1])


def phase(x: int) -> int:
    if x not in PHASES:
        raise ValueError("phase must be in 1,...,17 except 9")
    return 2 * (x - 9 * (x >= 10))


@dataclass(frozen=True, slots=True)
class State:
    c: int
    B: Word = ()
    A: Word = ()
    C: Word = ()

    def check(self, trimmed: bool = True) -> None:
        if self.c not in PHASES:
            raise ValueError("invalid phase")
        if any(not 0 <= x <= 18 for w in (self.B, self.A, self.C) for x in w):
            raise ValueError("invalid coefficient")
        if self.B and not self.B[0] > 0:
            raise ValueError("noncanonical exterior")
        if self.C != self.C[::-1]:
            raise ValueError("asymmetric center")
        if len(self.C) % 2 and self.C[len(self.C)//2] % 2:
            raise ValueError("odd center coefficient")
        d = 18 - self.c
        if trimmed and (self.B and self.B[-1] == self.c
                        or self.A and (self.A[0] == self.c or self.A[-1] == d)
                        or len(self.C) >= 2 and self.C[0] == d):
            raise ValueError("state is not trimmed")

    @property
    def size(self) -> int:
        return 2 * len(self.B) + 2 * len(self.A) + len(self.C)

    def word(self, g: int, h: int) -> Word:
        if g < 0 or h < 0:
            raise ValueError("negative gap")
        cband, dband = (self.c,) * g, (18-self.c,) * h
        return self.B + cband + self.A + dband + self.C + dband + self.A[::-1] + cband + self.B[::-1]

    def as_json(self) -> list:
        return [self.c, list(self.B), list(self.A), list(self.C)]


def trim(c: int, B: Word, A: Word, C: Word) -> tuple[State, int, int]:
    d = 18 - c
    b0, a0, m0 = len(B), len(A), len(C)
    while B and B[-1] == c:
        B = B[:-1]
    va = 0
    while A and A[0] == c:
        A = A[1:]
        va += 1
    ua = 0
    while A and A[-1] == d:
        A = A[:-1]
        ua += 1
    vc = 0
    while len(C) >= 2 and C[0] == d and C[-1] == d:
        C = C[1:-1]
        vc += 1
    state = State(c, B, A, C)
    state.check()
    return state, b0-len(B)+va, ua+vc


def step(s: State) -> tuple[State, int, int, int]:
    """Return (target, delta_g, delta_h, actual overflow)."""
    c, B, A, C = s.c, s.B, s.A, s.C
    d, kc, kd = 18-c, int(c >= 10), int(c <= 8)
    tc, td = c-9*kc, d-9*kd
    DB, e0 = normalize(B, 0)
    DA, e1 = normalize(A, kc)
    DC, e2 = normalize(C, kd)
    DRA, e3 = normalize(A[::-1], kd)
    DRB, gamma = normalize(B[::-1], kc)
    u0, u1, u2, u3 = c+e0-10*kc, d+e1-10*kd, d+e2-10*kd, c+e3-10*kc
    if gamma:
        Br = add_words(DB+(u0,), (1,)+DRB[::-1])
        Ar = add_words(DA+(u1,), (u3,)+DRA[::-1])
        Cr = pair(DC+(u2,))
    else:
        Br = add_words(DB+(u0,), DRB[::-1]+(tc,))
        Ar = add_words((tc,)+DA+(u1,), (u3,)+DRA[::-1]+(td,))
        Cr = pair((td,)+DC+(u2,))
    target, restore_g, restore_h = trim(2*tc, Br, Ar, Cr)
    dg, dh = restore_g-2+gamma, restore_h-2+gamma
    assert target.size + 2*dg + 2*dh == s.size + gamma
    return target, dg, dh, gamma


def direct_pair(w: Word) -> Word:
    """Independent literal-integer normalization, not the quotient transition."""
    n = 0
    for a in reversed(w):
        n = 10*n + a
    if n <= 0:
        raise ValueError("expected positive value")
    digits = []
    while n:
        n, r = divmod(n, 10)
        digits.append(r)
    return pair(tuple(digits))


def realize(w: Word) -> int:
    """Construct one ordinary integer with this canonical mirrored-sum word."""
    if not w or w != w[::-1] or w[0] <= 0:
        raise ValueError("noncanonical mirrored word")
    D = [0]*len(w)
    for i in range(len(w)//2):
        D[-1-i] = min(9, w[i])
        D[i] = w[i]-D[-1-i]
    if len(w)%2:
        if w[len(w)//2]%2:
            raise ValueError("odd center")
        D[len(w)//2] = w[len(w)//2]//2
    n = 0
    for a in reversed(D):
        n = 10*n+a
    return n


def small_states(phases: Iterable[int] = PERIODIC_PHASES) -> Iterable[State]:
    """All trimmed B,A,C of length <= 1 for the supplied phases."""
    for c in phases:
        for B in [()] + [(b,) for b in range(1,19) if b != c]:
            for A in [()] + [(a,) for a in range(19) if a not in (c,18-c)]:
                for C in [()] + [(z,) for z in range(0,19,2)]:
                    yield State(c,B,A,C)
