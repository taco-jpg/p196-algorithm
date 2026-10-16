#!/usr/bin/env python3
"""Independent reconstruction of the project's complementary-bulk quotient.

Words are least-significant-column first. This module has no third-party
requirements. Assertions check hypotheses; all arithmetic uses Python integers.
Reference: proofs/contributions/2026-10-15-complementary-bulk-quotient/
METHOD_AND_PROOF.md, main snapshot a71d6e79b009da691e2d97057f83e108a3fcff4f.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

Word = tuple[int, ...]
PHASES = tuple(c for c in range(1, 18) if c != 9)


def normalize(w: Word, incoming: int = 0) -> tuple[Word, int]:
    assert incoming in (0, 1)
    out: list[int] = []
    carry = incoming
    for x in w:
        assert 0 <= x <= 18
        carry, digit = divmod(x + carry, 10)
        out.append(digit)
    return tuple(out), carry


def pair(w: Word) -> Word:
    return tuple(a + b for a, b in zip(w, reversed(w)))


def add(a: Word, b: Word) -> Word:
    assert len(a) == len(b)
    return tuple(x + y for x, y in zip(a, b))


def actual_step(q: Word) -> Word:
    assert q and q[0] > 0 and q == q[::-1]
    assert len(q) % 2 == 0 or q[len(q) // 2] % 2 == 0
    d, carry = normalize(q)
    if carry:
        d += (carry,)
    assert d[-1] > 0
    return pair(d)


def value(w: Word) -> int:
    result = 0
    for x in reversed(w):
        result = 10 * result + x
    return result


def realize(q: Word) -> int:
    """Return one canonical integer whose pair word is q."""
    assert q and q[0] > 0 and q == q[::-1]
    d = [0] * len(q)
    for i in range(len(q) // 2):
        d[-1-i] = min(9, q[i])
        d[i] = q[i] - d[-1-i]
    if len(q) % 2:
        assert q[len(q)//2] % 2 == 0
        d[len(q)//2] = q[len(q)//2] // 2
    assert d[-1] > 0
    return value(tuple(d))


def literal_pair(n: int) -> Word:
    assert n > 0
    d = tuple(map(int, str(n)[::-1]))
    return pair(d)


def reverse_add(n: int) -> int:
    return n + int(str(n)[::-1])


def strip_suffix(w: Word, x: int) -> tuple[Word, int]:
    j = len(w)
    while j and w[j-1] == x:
        j -= 1
    return w[:j], len(w)-j


def strip_prefix(w: Word, x: int) -> tuple[Word, int]:
    j = 0
    while j < len(w) and w[j] == x:
        j += 1
    return w[j:], j


def strip_center(w: Word, x: int) -> tuple[Word, int]:
    assert w == w[::-1]
    j = 0
    while 2*j + 1 < len(w) and w[j] == x:
        j += 1
    return w[j:len(w)-j] if j else w, j


@dataclass(frozen=True)
class State:
    phase: int
    exterior: Word
    interface: Word
    center: Word

    def valid(self) -> bool:
        return (self.phase in PHASES
                and all(0 <= x <= 18 for w in
                        (self.exterior, self.interface, self.center) for x in w)
                and (not self.exterior or self.exterior[0] > 0)
                and self.center == self.center[::-1]
                and (len(self.center) % 2 == 0
                     or self.center[len(self.center)//2] % 2 == 0))

    def word(self, g: int, h: int) -> Word:
        assert self.valid() and g >= 0 and h >= 0
        B, A, C, c = self.exterior, self.interface, self.center, self.phase
        return (B + (c,)*g + A + (18-c,)*h + C + (18-c,)*h
                + A[::-1] + (c,)*g + B[::-1])

    def trimmed(self) -> bool:
        c, d = self.phase, 18-self.phase
        return (self.valid()
                and (not self.exterior or self.exterior[-1] != c)
                and (not self.interface or
                     (self.interface[0] != c and self.interface[-1] != d))
                and (len(self.center) < 2 or self.center[0] != d))


@dataclass(frozen=True)
class Edge:
    target: State
    dg: int
    dh: int
    overflow: int
    strips: tuple[int, int, int, int]


def transition(s: State) -> Edge:
    assert s.valid()
    c, B, A, C = s.phase, s.exterior, s.interface, s.center
    d = 18-c
    kc, kd = int(c >= 10), int(d >= 10)
    tc, td = c-9*kc, d-9*kd
    cp, dp = 2*tc, 2*td
    DB, e0 = normalize(B, 0)
    DA, e1 = normalize(A, kc)
    DC, e2 = normalize(C, kd)
    DRA, e3 = normalize(A[::-1], kd)
    DRB, gamma = normalize(B[::-1], kc)
    u0, u1 = c+e0-10*kc, d+e1-10*kd
    u2, u3 = d+e2-10*kd, c+e3-10*kc
    if gamma:
        Br = add(DB+(u0,), (1,)+DRB[::-1])
        Ar = add(DA+(u1,), (u3,)+DRA[::-1])
        Cr = pair(DC+(u2,))
    else:
        Br = add(DB+(u0,), DRB[::-1]+(tc,))
        Ar = add((tc,)+DA+(u1,), (u3,)+DRA[::-1]+(td,))
        Cr = pair((td,)+DC+(u2,))
    Bp, uB = strip_suffix(Br, cp)
    Ap, vA = strip_prefix(Ar, cp)
    Ap, uA = strip_suffix(Ap, dp)
    Cp, vC = strip_center(Cr, dp)
    out = State(cp, Bp, Ap, Cp)
    dg, dh = uB+vA-2+gamma, uA+vC-2+gamma
    assert out.trimmed()
    assert (2*len(Bp)+2*len(Ap)+len(Cp)+2*dg+2*dh
            == 2*len(B)+2*len(A)+len(C)+gamma)
    return Edge(out, dg, dh, gamma, (uB, vA, uA, vC))


def exterior_transition(c: int, B: Word) -> tuple[int, Word, int, int]:
    """The autonomous exterior factor: next phase, block, overflow, strip."""
    kc = int(c >= 10)
    tc = c-9*kc
    DB, e0 = normalize(B, 0)
    DRB, gamma = normalize(B[::-1], kc)
    u0 = c+e0-10*kc
    Br = add(DB+(u0,), ((1,)+DRB[::-1]) if gamma else (DRB[::-1]+(tc,)))
    Bp, uB = strip_suffix(Br, 2*tc)
    return 2*tc, Bp, gamma, uB


def check_cases(seed: int = 196, count: int = 10000) -> dict[str, int]:
    import random
    rng = random.Random(seed)
    checks = 0
    overflows = 0
    for _ in range(count):
        c = rng.choice(PHASES)
        B = tuple(rng.randrange(19) for _ in range(rng.randrange(7)))
        if B and B[0] == 0:
            B = (rng.randrange(1, 19),)+B[1:]
        A = tuple(rng.randrange(19) for _ in range(rng.randrange(7)))
        half = tuple(rng.randrange(19) for _ in range(rng.randrange(5)))
        middle = (2*rng.randrange(10),) if rng.randrange(2) else ()
        C = half+middle+half[::-1]
        s = State(c, B, A, C)
        e = transition(s)
        assert exterior_transition(c, B) == (
            e.target.phase, e.target.exterior, e.overflow, e.strips[0])
        overflows += e.overflow
        for g,h in ((2,2), (2,3), (3,2), (5,7)):
            q = s.word(g,h)
            qp = e.target.word(g+e.dg,h+e.dh)
            assert actual_step(q) == qp
            n = realize(q)
            assert literal_pair(n) == q
            assert literal_pair(reverse_add(n)) == qp
            assert str(reverse_add(n)) != str(reverse_add(n))[::-1]
            checks += 1
    return {"random_states": count, "literal_integer_checks": checks,
            "overflow_states": overflows, "seed": seed}


if __name__ == '__main__':
    import json
    print(json.dumps(check_cases(), sort_keys=True))
