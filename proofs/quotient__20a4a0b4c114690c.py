"""Exact complementary-bulk quotient, independently implemented by Agent #4.

All words are least-significant-column first. This module uses only Python's
standard library. A bounded search is never promoted to an all-state theorem.
Source identities: proofs/contributions/2026-10-15-complementary-bulk-quotient/
METHOD_AND_PROOF.md, sections 2--7 (inspected 2026-10-15).
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from typing import Iterable, Iterator

Word = tuple[int, ...]
PHASES = (2, 4, 6, 8, 10, 12, 14, 16)


def normalize(word: Word, carry: int = 0) -> tuple[Word, int]:
    if carry not in (0, 1) or any(not 0 <= x <= 18 for x in word):
        raise ValueError("Invalid coefficient word or input carry")
    digits = []
    for x in word:
        carry, digit = divmod(x + carry, 10)
        digits.append(digit)
    return tuple(digits), carry


def pair(word: Word) -> Word:
    return tuple(a + b for a, b in zip(word, reversed(word)))


def add_words(x: Word, y: Word) -> Word:
    if len(x) != len(y):
        raise ValueError("Coordinatewise addition requires equal lengths")
    return tuple(a + b for a, b in zip(x, y))


def phase_next(c: int) -> int:
    if c not in range(1, 18) or c == 9:
        raise ValueError("Phase must be in {1,...,17} minus {9}")
    return 2 * (c - 9 * (c >= 10))


@dataclass(frozen=True, slots=True)
class State:
    c: int
    B: Word = ()
    A: Word = ()
    C: Word = ()

    @property
    def d(self) -> int:
        return 18 - self.c

    @property
    def interface_size(self) -> int:
        return 2 * len(self.B) + 2 * len(self.A) + len(self.C)

    def validate(self, *, trimmed: bool = False) -> None:
        phase_next(self.c)
        if any(not 0 <= x <= 18 for W in (self.B, self.A, self.C) for x in W):
            raise ValueError("Coefficient out of range")
        if self.B and self.B[0] == 0:
            raise ValueError("Noncanonical exterior")
        if self.C != self.C[::-1] or (len(self.C) % 2 and self.C[len(self.C)//2] % 2):
            raise ValueError("Noncanonical center")
        if trimmed:
            if self.B and self.B[-1] == self.c:
                raise ValueError("Untrimmed B")
            if self.A and (self.A[0] == self.c or self.A[-1] == self.d):
                raise ValueError("Untrimmed A")
            if len(self.C) >= 2 and self.C[0] == self.d:
                raise ValueError("Untrimmed C")

    def word(self, g: int, h: int) -> Word:
        self.validate()
        if g < 0 or h < 0:
            raise ValueError("Gaps cannot be negative")
        c, d = (self.c,) * g, (self.d,) * h
        return self.B + c + self.A + d + self.C + d + self.A[::-1] + c + self.B[::-1]


@dataclass(frozen=True, slots=True)
class Edge:
    target: State
    dg: int
    dh: int
    overflow: int


def step(s: State) -> Edge:
    """Independent formula evaluation; valid as an actual-map identity for g,h>=2."""
    s.validate()
    c, d = s.c, s.d
    kc, kd = int(c >= 10), int(d >= 10)
    tc, td = c - 9*kc, d - 9*kd
    DB, e0 = normalize(s.B, 0)
    DA, e1 = normalize(s.A, kc)
    DC, e2 = normalize(s.C, kd)
    DRA, e3 = normalize(s.A[::-1], kd)
    DRB, gamma = normalize(s.B[::-1], kc)
    u0, u1 = c+e0-10*kc, d+e1-10*kd
    u2, u3 = d+e2-10*kd, c+e3-10*kc
    if gamma == 0:
        B = add_words(DB+(u0,), DRB[::-1]+(tc,))
        A = add_words((tc,)+DA+(u1,), (u3,)+DRA[::-1]+(td,))
        C = pair((td,)+DC+(u2,))
    else:
        B = add_words(DB+(u0,), (1,)+DRB[::-1])
        A = add_words(DA+(u1,), (u3,)+DRA[::-1])
        C = pair(DC+(u2,))
    cp, dp = 2*tc, 2*td
    ub = va = ua = vc = 0
    while B and B[-1] == cp:
        B = B[:-1]
        ub += 1
    while A and A[0] == cp:
        A = A[1:]
        va += 1
    while A and A[-1] == dp:
        A = A[:-1]
        ua += 1
    while len(C) >= 2 and C[0] == dp and C[-1] == dp:
        C = C[1:-1]
        vc += 1
    t = State(cp, B, A, C)
    t.validate(trimmed=True)
    dg, dh = ub+va-2+gamma, ua+vc-2+gamma
    if t.interface_size + 2*dg + 2*dh != s.interface_size + gamma:
        raise AssertionError("Length conservation failed")
    return Edge(t, dg, dh, gamma)


def evaluate(word: Word) -> int:
    value = 0
    for x in reversed(word):
        value = 10*value + x
    return value


def digits(n: int) -> Word:
    if n <= 0:
        raise ValueError("Only positive ordinary integers are in the canonical domain")
    out = []
    while n:
        n, x = divmod(n, 10)
        out.append(x)
    return tuple(out)


def reverse_add(n: int) -> int:
    return n + evaluate(digits(n)[::-1])


def realize(q: Word) -> int:
    """One canonical ordinary integer n satisfying pair(digits(n))=q."""
    if not q or q[0] <= 0 or q != q[::-1] or any(not 0 <= x <= 18 for x in q):
        raise ValueError("Not a canonical symmetric pair word")
    D = [0] * len(q)
    for i in range(len(q)//2):
        D[i] = max(0, q[i]-9)
        D[-1-i] = q[i]-D[i]
    if len(q) % 2:
        if q[len(q)//2] % 2:
            raise ValueError("Odd middle pair coefficient")
        D[len(q)//2] = q[len(q)//2]//2
    n = evaluate(tuple(D))
    if pair(digits(n)) != q:
        raise AssertionError("Realization failed")
    return n


def integer_control(s: State, g: int, h: int) -> None:
    if g < 2 or h < 2:
        raise ValueError("The source identity requires g,h>=2")
    q = s.word(g, h)
    n = realize(q)
    output = reverse_add(n)
    e = step(s)
    assert output == evaluate(q)
    assert pair(digits(output)) == e.target.word(g+e.dg, h+e.dh)
    assert len(digits(output)) == len(q)+e.overflow
    assert digits(output) != digits(output)[::-1], "Mixed complementary bands must be safe"


def states(max_interface: int, phases: Iterable[int] = PHASES) -> Iterator[State]:
    """Exactly all trimmed canonical states with physical interface size <= cap.

    Cycles can use only the even phases PHASES because every phase image is even.
    No gap is instantiated or bounded here.
    """
    if max_interface < 0:
        raise ValueError("The cap must be nonnegative")
    for c in phases:
        phase_next(c)
        d = 18-c
        for b in range(max_interface//2+1):
            Bs = [B for B in product(range(19), repeat=b)
                  if not B or (B[0] > 0 and B[-1] != c)]
            for a in range((max_interface-2*b)//2+1):
                As = [A for A in product(range(19), repeat=a)
                      if not A or (A[0] != c and A[-1] != d)]
                for m in range(max_interface-2*b-2*a+1):
                    centers = []
                    for half in product(range(19), repeat=m//2):
                        if half and half[0] == d:
                            continue
                        if m % 2:
                            centers.extend(half+(z,)+half[::-1] for z in range(0, 19, 2))
                        else:
                            centers.append(half+half[::-1])
                    for B in Bs:
                        for A in As:
                            for C in centers:
                                yield State(c, B, A, C)
