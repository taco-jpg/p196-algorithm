#!/usr/bin/env python3
"""Independent exact complementary-band quotient (decimal, LS-first words).

Implements equations (3), (6), (7), (10) of the existing written proof.
No finite computation here establishes a Lychrel witness.
"""
from __future__ import annotations
from dataclasses import dataclass

Word = tuple[int, ...]
PHASES = tuple(x for x in range(1, 18) if x != 9)


def phase(c: int) -> int:
    if c not in PHASES:
        raise ValueError("phase must lie in {1,...,17} minus {9}")
    return 2 * (c - 9 * (c >= 10))


def normalize(word: Word, incoming: int = 0) -> tuple[Word, int]:
    if incoming not in (0, 1) or any(x not in range(19) for x in word):
        raise ValueError("invalid coefficient word or carry")
    out = []
    carry = incoming
    for x in word:
        carry, digit = divmod(x + carry, 10)
        out.append(digit)
    return tuple(out), carry


def plus(x: Word, y: Word) -> Word:
    if len(x) != len(y):
        raise ValueError("coordinatewise sum requires equal widths")
    return tuple(a+b for a, b in zip(x, y))


def pairs(d: Word) -> Word:
    return plus(d, d[::-1])


def strip_suffix(word: Word, symbol: int) -> tuple[Word, int]:
    j = len(word)
    while j and word[j-1] == symbol:
        j -= 1
    return word[:j], len(word)-j


def strip_prefix(word: Word, symbol: int) -> tuple[Word, int]:
    j = 0
    while j < len(word) and word[j] == symbol:
        j += 1
    return word[j:], j


def strip_center(word: Word, symbol: int) -> tuple[Word, int]:
    j = 0
    while 2*j+1 < len(word) and word[j] == symbol and word[-1-j] == symbol:
        j += 1
    return word[j:len(word)-j] if j else word, j


@dataclass(frozen=True)
class State:
    c: int
    B: Word = ()
    A: Word = ()
    C: Word = ()

    def validate(self) -> None:
        phase(self.c)
        if any(x not in range(19) for w in (self.B, self.A, self.C) for x in w):
            raise ValueError("coefficient outside [0,18]")
        if self.B and self.B[0] == 0:
            raise ValueError("zero exterior")
        if self.C != self.C[::-1] or (len(self.C) % 2 and self.C[len(self.C)//2] % 2):
            raise ValueError("noncanonical center")

    def size(self) -> int:
        return 2*len(self.B) + 2*len(self.A) + len(self.C)

    def word(self, g: int, h: int) -> Word:
        self.validate()
        if g < 0 or h < 0:
            raise ValueError("negative gap")
        c, d = self.c, 18-self.c
        return (self.B + (c,)*g + self.A + (d,)*h + self.C + (d,)*h
                + self.A[::-1] + (c,)*g + self.B[::-1])

    def trimmed(self) -> bool:
        return ((not self.B or self.B[-1] != self.c)
                and (not self.A or (self.A[0] != self.c and self.A[-1] != 18-self.c))
                and (len(self.C) < 2 or self.C[0] != 18-self.c))


def step(s: State) -> tuple[State, int, int, int]:
    """Return the exact next interface, g increment, h increment, and overflow."""
    s.validate()
    c, d = s.c, 18-s.c
    kc, kd = int(c >= 10), int(d >= 10)
    tc, td = c-9*kc, d-9*kd
    DB, e0 = normalize(s.B, 0)
    DA, e1 = normalize(s.A, kc)
    DC, e2 = normalize(s.C, kd)
    DRA, e3 = normalize(s.A[::-1], kd)
    DRB, gamma = normalize(s.B[::-1], kc)
    u0, u1, u2, u3 = c+e0-10*kc, d+e1-10*kd, d+e2-10*kd, c+e3-10*kc
    if gamma == 0:
        Br = plus(DB+(u0,), DRB[::-1]+(tc,))
        Ar = plus((tc,)+DA+(u1,), (u3,)+DRA[::-1]+(td,))
        Cr = pairs((td,)+DC+(u2,))
    else:
        Br = plus(DB+(u0,), (1,)+DRB[::-1])
        Ar = plus(DA+(u1,), (u3,)+DRA[::-1])
        Cr = pairs(DC+(u2,))
    cp, dp = phase(c), phase(d)
    B, uB = strip_suffix(Br, cp)
    A, vA = strip_prefix(Ar, cp)
    A, uA = strip_suffix(A, dp)
    C, vC = strip_center(Cr, dp)
    dg, dh = uB+vA-2+gamma, uA+vC-2+gamma
    dest = State(cp, B, A, C)
    dest.validate()
    assert dest.trimmed()
    assert dest.size() + 2*dg + 2*dh == s.size()+gamma
    return dest, dg, dh, gamma


def outer_step(c: int, B: Word) -> tuple[int, Word, int, int]:
    """Independent exterior subsystem: (next phase, next B, stripped count, overflow)."""
    kc = int(c >= 10)
    tc = c-9*kc
    DB, e = normalize(B, 0)
    DRB, gamma = normalize(B[::-1], kc)
    u = c+e-10*kc
    Br = plus(DB+(u,), ((1,)+DRB[::-1]) if gamma else (DRB[::-1]+(tc,)))
    Bp, uB = strip_suffix(Br, phase(c))
    return phase(c), Bp, uB, gamma


def value(word: Word) -> int:
    out = 0
    for x in reversed(word):
        out = 10*out+x
    return out


def digits(n: int) -> Word:
    if n <= 0:
        raise ValueError("positive value required")
    out = []
    while n:
        n, d = divmod(n, 10)
        out.append(d)
    return tuple(out)


def realize(q: Word) -> int:
    if not q or q != q[::-1] or q[0] <= 0:
        raise ValueError("not a canonical pair word")
    n = [0]*len(q)
    for j in range(len(q)//2):
        n[j] = max(0, q[j]-9)
        n[-1-j] = q[j]-n[j]
    if len(q) % 2:
        if q[len(q)//2] % 2:
            raise ValueError("odd middle")
        n[len(q)//2] = q[len(q)//2]//2
    return value(tuple(n))


def audit_instance(s: State, g: int, h: int) -> None:
    if min(g,h) < 2:
        raise ValueError("source gaps must be at least two")
    q = s.word(g,h)
    n = realize(q)
    m = n + int(str(n)[::-1])
    assert m == value(q)
    assert str(m) != str(m)[::-1]
    t,dg,dh,gamma = step(s)
    assert pairs(digits(m)) == t.word(g+dg,h+dh)
    assert len(digits(m)) == len(q)+gamma
    oc,oB,_,ogamma = outer_step(s.c,s.B)
    assert (oc,oB,ogamma) == (t.c,t.B,gamma)
