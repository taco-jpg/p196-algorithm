"""Exact controls for the universal carry-blind polynomial quotient.

Run with Python 3; no third-party packages or imported research modules.
This script is a control for the accompanying algebraic proof, not a proof
of decimal Lychrel existence or of any all-time claim about 196.
"""
from collections import Counter
from itertools import product
import json
import random


def trim(a):
    a = list(a)
    while a and not a[-1]:
        a.pop()
    return a


def add(a, b):
    return trim([(a[i] if i < len(a) else 0)
                 + (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def scale(a, k):
    return trim([k*x for x in a])


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out)


P = [1, -20, 1]
G = [9, 9]


def step(q):
    carry = 0
    digits, carries = [], []
    for x in q:
        z = x + carry
        digits.append(z % 10)
        carry = z // 10
        carries.append(carry)
    if carry:
        digits.append(carry)
    nq = tuple(x+y for x, y in zip(digits, reversed(digits)))
    return nq, tuple(carries), carry, tuple(digits)


def residue(a):
    """Q(1), formal derivative Q'(1), Q(-1), in the stated rings."""
    return (sum(a) % 9,
            sum(i*x for i, x in enumerate(a)) % 9,
            sum((-1)**i*x for i, x in enumerate(a)) % 22)


def defect(q):
    nq, cs, h, digits = step(q)
    factor = [1, 1] if h else [2]
    return sub(nq, mul(q, factor)), nq, cs, h, digits


def verify(q):
    assert q == q[::-1] and 0 < q[0] <= 18
    assert all(0 <= x <= 18 for x in q)
    assert not len(q) % 2 or q[len(q)//2] % 2 == 0
    delta, nq, cs, h, digits = defect(q)
    cstar = cs[::-1]
    difference = sub(cs, cstar)
    # S=(C-C*)/(x-1), with zero-padding to the known degree L-1.
    cumulative = 0
    ss = []
    for i in range(len(q)-1):
        cumulative += (cs[i]-cstar[i])
        ss.append(-cumulative)
    ss = trim(ss)
    assert mul([-1, 1], ss) == difference
    if h:
        cert = add(mul(P, ss), mul(G, sub(ss, cstar)))
    else:
        assert cstar[0] == 0
        cert = add(mul(P, add(cstar[1:], ss)), mul(G, ss))
    assert delta == cert, (q, delta, cert)
    u, v, w = residue(q)
    predicted = (2*u % 9, (2*v + h*u) % 9,
                 0 if h else 2*w % 22)
    assert residue(nq) == predicted
    # Reciprocity removes the apparently additional derivative coordinate.
    assert 2*sum(i*x for i, x in enumerate(q)) == (len(q)-1)*sum(q)
    assert sum(q) % 2 == 0
    assert len(q) % 2 or residue(q)[2] == 0
    return h


def low_target(L, u, b):
    assert L >= 5 and L % 2 and 1 <= u <= 10 and 0 <= b <= 9
    a = min(u, 9)
    c = u-a
    q = [0]*L
    for i, v in [(0, a), (1, b), (2, c)]:
        q[i] += v
        q[L-1-i] += v
    return tuple(q)


def signature(q):
    return (sum(q)//2 % 9,
            sum((-1)**i*x for i, x in enumerate(q))//2 % 11)


def target_controls():
    records = []
    for L in [5, 7, 9, 11, 51]:
        multiplicities = Counter()
        for u in range(1, 11):
            for b in range(10):
                q = low_target(L, u, b)
                _, _, h, digits = step(q)
                assert h == 0 and digits == digits[::-1]
                assert signature(q) == ((u+b) % 9, (u-b) % 11)
                multiplicities[signature(q)] += 1
        assert set(multiplicities) == set(product(range(9), range(11)))
        assert sorted(multiplicities.values()) == [1]*98+[2]
        records.append({"length": L, "carry_free_classes": len(multiplicities)})
    for L in [2, 4, 6, 18, 50]:
        classes = set()
        for a in range(1, 10):
            q = tuple([a]+[0]*(L-2)+[a])
            _, _, h, digits = step(q)
            assert h == 0 and digits == digits[::-1]
            classes.add(signature(q))
        assert classes == set(product(range(9), [0]))
        records.append({"length": L, "carry_free_classes": len(classes)})
    for L in [18, 19, 20, 21, 50, 51]:
        classes = set()
        m = L//2
        for k in range(1, 10):
            left = [11]*k + [0]*(m-k)
            q = tuple(left + ([0] if L % 2 else []) + left[::-1])
            _, _, h, digits = step(q)
            assert h == 1 and digits == digits[::-1]
            classes.add(signature(q))
        assert classes == set(product(range(9), [0]))
        records.append({"length": L, "overflow_target_classes": len(classes)})
    return records


def main():
    # Actual nonpalindromic inputs 150, 109, 159 generate the entire ideal.
    d150 = defect((1, 10, 1))[0]
    d109 = defect((10, 0, 10))[0]
    d159 = defect((10, 10, 10))[0]
    assert d150 == P
    assert sub(d159, d109) == scale(mul([0, 1], G), -1)
    # 198 belongs to the ideal, the key step in the CRT decomposition.
    assert sub(scale(P, 9), mul([-21, 1], G)) == [198]
    # There are exactly 9*9*22 distinct CRT coordinates for a+b*x.
    quotient_classes = {
        ((a+b) % 9, b % 9, (a-b) % 22)
        for a in range(198) for b in range(198)
    }
    assert len(quotient_classes) == 1782
    cases = Counter()
    exhaustive = 0
    for L in range(1, 8):
        for half in product(range(19), repeat=(L+1)//2):
            if half[0] == 0 or (L % 2 and half[-1] % 2):
                continue
            q = half+half[-2::-1] if L % 2 else half+half[::-1]
            h = verify(q)
            cases[f"parity_{L%2}_overflow_{h}"] += 1
            exhaustive += 1
    rng = random.Random(196)
    randomized = 10000
    for _ in range(randomized):
        L = rng.randrange(2, 200)
        half = [rng.randrange(19) for _ in range((L+1)//2)]
        half[0] = rng.randrange(1, 19)
        if L % 2:
            half[-1] = 2*rng.randrange(10)
        q = tuple(half+half[-2::-1]) if L % 2 else tuple(half+half[::-1])
        h = verify(q)
        cases[f"parity_{L%2}_overflow_{h}"] += 1
    assert exhaustive == 75447
    print(json.dumps({
        "claim": "Universal carry-defect ideal and target saturation controls",
        "all_time_lychrel_claim": False,
        "exhaustive_canonical_words_lengths_1_to_7": exhaustive,
        "seeded_random_canonical_words_lengths_2_to_199": randomized,
        "four_cases": dict(sorted(cases.items())),
        "universal_quotient_size": len(quotient_classes),
        "target_saturation": target_controls(),
    }, indent=2))


if __name__ == "__main__":
    main()
