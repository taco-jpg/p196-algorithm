"""Agent #101: independent exterior factor (c,B) -> (c',B',gamma) for the
complementary-bulk quotient (METHOD_AND_PROOF.md eqs (3),(4),(6),(7), sec. 6),
plus a literal-integer cross-check that does not use those formulas."""
import random, sys

def N(W, e):
    D = []
    for w in W:
        s = w + e
        D.append(s % 10); e = s // 10
    return D, e

def step(c, B):
    k = 1 if c >= 10 else 0
    t = c - 9 * k
    DB, e0 = N(B, 0)
    u0 = c + e0 - 10 * k
    DRB, g = N(B[::-1], k)
    left = DB + [u0]
    right = (DRB[::-1] + [t]) if g == 0 else ([1] + DRB[::-1])
    Br = [x + y for x, y in zip(left, right)]
    cp = 2 * t
    while Br and Br[-1] == cp:
        Br.pop()
    return cp, tuple(Br), g

# ---- literal check: build Q with A,C empty, evaluate, re-pair, read exterior
def literal(c, B, g=25, h=25):
    d = 18 - c
    Q = list(B) + [c] * g + [d] * h + [d] * h + [c] * g + list(B[::-1])
    v = sum(q * 10 ** i for i, q in enumerate(Q))       # = T(n) exactly
    s = str(v)[::-1]                                     # low-to-high digits
    L = len(s)
    P = [int(s[i]) + int(s[L - 1 - i]) for i in range(L)]
    gam = L - len(Q)
    assert gam in (0, 1)
    k = 1 if c >= 10 else 0
    cp = 2 * (c - 9 * k)
    # exterior = prefix before first run of >=10 copies of cp
    i = 0
    while True:
        if P[i:i + 10] == [cp] * 10:
            break
        i += 1
    return cp, tuple(P[:i]), gam

if __name__ == "__main__":
    rnd = random.Random(101)
    phases = [x for x in range(1, 18) if x != 9]
    n = 0
    # exhaustive |B|<=2 over all 16 phases, plus random longer B
    cases = [()]
    cases += [(a,) for a in range(1, 19)]
    cases += [(a, b) for a in range(1, 19) for b in range(19)]
    for c in phases:
        for B in cases:
            assert step(c, list(B)) == literal(c, B), (c, B)
            n += 1
    for _ in range(20000):
        c = rnd.choice(phases)
        b = rnd.randint(3, 9)
        B = (rnd.randint(1, 18),) + tuple(rnd.randint(0, 18) for _ in range(b - 1))
        assert step(c, list(B)) == literal(c, B), (c, B)
        n += 1
    print("literal exterior controls passed:", n)
