"""Exact universal finite lifetimes for four delayed-overlap gate cores.

This is a stand-alone, standard-library certificate checker.  Sparse
polynomials use monomials x**b * y**a, subsequently y=x**r.  Checking digit
coefficients, exponent collisions, and formal reversal identities proves
the displayed formulas for every integer r in the stated domain.  Separate
ordinary-integer controls are finite implementation checks, not the proof.
"""
from __future__ import annotations

from collections import defaultdict
from itertools import combinations
import json
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(100000)


def poly(terms=()):
    result = defaultdict(int)
    for exponent, coefficient in terms:
        result[exponent] += coefficient
    return {e: c for e, c in result.items() if c}


def add(*polynomials):
    return poly((e, c) for p in polynomials for e, c in p.items())


def shift(p, b):
    return {(a, k+b): c for (a, k), c in p.items()}


def scale(p, coefficient):
    return poly((e, coefficient*c) for e, c in p.items())


def reflect(p, degree_offset):
    """Reflect in degree 2*r + degree_offset."""
    return {(2-a, degree_offset-b): c for (a, b), c in p.items()}


def at_r(p, r):
    return poly((a*r+b, c) for (a, b), c in p.items())


def collision_parameters(p, minimum):
    """All r>=minimum at which distinct affine exponents coincide."""
    result = set()
    for (a, b), (c, d) in combinations(p, 2):
        if a != c and (d-b) % (a-c) == 0:
            r = (d-b) // (a-c)
            if r >= minimum:
                result.add(r)
    return result


def certify_digits(p, minimum, degree_offset):
    assert p.get((2, degree_offset), 0) > 0
    for (a, b), coefficient in p.items():
        # These linear inequalities then hold for every r>=minimum.
        assert 0 <= a <= 2
        assert a*minimum+b >= 0
        assert (2-a)*minimum+degree_offset-b >= 0
        assert 1 <= coefficient <= 9
    for r in collision_parameters(p, minimum):
        assert all(1 <= c <= 9 for c in at_r(p, r).values())


def certify_nonzero(p, minimum):
    assert p
    # Outside this finite set, no terms merge, so a nonzero coefficient
    # remains. Inside it, merge all terms and check directly.
    for r in collision_parameters(p, minimum):
        assert at_r(p, r)


def outer_core(outer, exponent, core):
    """outer . 0**(r-exponent) . core . 0**(r-exponent) . rev(outer)."""
    degree_offset = 2*len(outer)-2*exponent+len(core)-1
    terms = [((0, i), c) for i, c in enumerate(outer)]
    terms += [((1, len(outer)-exponent+i), c)
              for i, c in enumerate(core)]
    terms += [((2, degree_offset-i), c) for i, c in enumerate(outer)]
    return poly(terms)


def certificate(q, carries, degree_offset, minimum, expected_next, hit):
    """D = Q + (x-10)C has the same decimal value as Q.

    If its coefficients are decimal digits with nonzero leading digit,
    uniqueness of base-10 expansion makes D the actual normalization.
    Thus this proof does not assume the asserted C is a valid carry trace.
    """
    c = poly(((a, b), 1) for a, offsets in enumerate(carries) for b in offsets)
    digits = add(q, shift(c, 1), scale(c, -10))
    certify_digits(digits, minimum, degree_offset)
    reversed_digits = reflect(digits, degree_offset)
    successor = add(digits, reversed_digits)
    if expected_next is not None:
        assert successor == expected_next
    difference = add(digits, scale(reversed_digits, -1))
    if hit:
        assert not difference
    else:
        certify_nonzero(difference, minimum)
    return digits


FAST_CORES = {
    (2, 5): ((1, 9, 0, 6, 0, 9, 1), (2, 4, 5)),
    (2, 6): ((1, 9, 9, 2, 9, 9, 1), (2, 3, 4, 5)),
    (3, 5): ((1, 7, 9, 6, 9, 7, 1), (1, 2, 4, 5)),
}

# Q_t = B_t . 0**(r-e_t) . H_t . 0**(r-e_t) . reverse(B_t).
# The last fields are normalization degree minus 2*r, then the carry
# polynomial supports grouped as constant offsets, r+offsets, 2*r+offsets.
ELEVEN_ROWS = (
    ((1, 1), 1, (1, 7, 12, 7, 1), 6, ((), (3,), ())),
    ((2, 2), 1, (2, 15, 4, 15, 2), 6, ((), (2, 4), ())),
    ((4, 4), 1, (5, 10, 10, 10, 5), 6, ((), (2, 3, 4), ())),
    ((8, 8), 1, (11, 1, 2, 1, 11), 6, ((), (1, 5), ())),
    ((16, 16), 2, (1, 2, 3, 4, 3, 2, 1), 7,
     ((0, 1), (), (5, 6))),
    ((7, 14, 7), 3, (1, 3, 5, 7, 7, 5, 3, 1), 7,
     ((1,), (), (6,))),
    ((15, 8, 15), 3, (2, 6, 10, 14, 14, 10, 6, 2), 8,
     ((0, 2), (2, 3, 4, 5), (5, 7))),
    ((6, 14, 14, 6), 4, (2, 8, 7, 6, 10, 6, 7, 8, 2), 8,
     ((1, 2), (4,), (6, 7))),
    ((13, 9, 9, 13), 4, (4, 16, 14, 13, 0, 13, 14, 16, 4), 9,
     ((0, 1, 2, 3), (1, 2, 3, 5, 6, 7), (5, 6, 7, 8))),
    ((4, 4, 0, 4, 4), 5, (4, 11, 12, 9, 4, 4, 9, 12, 11, 4), 9,
     ((), (1, 2, 3, 7, 8), ())),
    ((8, 8, 0, 8, 8), 5, (9, 3, 5, 9, 9, 9, 9, 5, 3, 9), 9,
     ((), (), ())),
)


def prove_templates():
    certificates = 0
    for (u, v), (h, third_carries) in FAST_CORES.items():
        z = u+v
        rows = [
            outer_core((1, 1), 1, (u, z, 2*v, z, u)),
            outer_core((2, 2), 1, (2*u, 2*z+1, 4*v-20, 2*z+1, 2*u)),
            outer_core((4, 4), 1,
                       (4*u+1, 4*z-18, 8*v-38, 4*z-18, 4*u+1)),
        ]
        # This is polynomial addition, including the r=1 edge overlaps.
        rows.append(add(poly((((0, 0), 8), ((0, 1), 8),
                              ((2, 5), 8), ((2, 6), 8))),
                        poly(((1, i), c) for i, c in enumerate(h))))
        carry_sets = [(3,), (2, 4), third_carries, ()]
        for t in range(4):
            certificate(rows[t], ((), carry_sets[t], ()), 6, 1,
                        rows[t+1] if t < 3 else None, t == 3)
            certificates += 1

    rows = [outer_core(b, e, h) for b, e, h, _, _ in ELEVEN_ROWS]
    for t, (_, _, _, degree_offset, carries) in enumerate(ELEVEN_ROWS):
        certificate(rows[t], carries, degree_offset, 5,
                    rows[t+1] if t < 10 else None, t == 10)
        certificates += 1
    return certificates


def initial_word(r, u, v):
    a = (1,) + (0,)*r + (u, v, v, u) + (0,)*r + (1,)
    return tuple(x+y for x, y in zip(a+(0,), (0,)+a))


def realize(q):
    """One ordinary decimal integer having precisely the pair word q."""
    assert q == q[::-1] and 1 <= q[0] <= 18
    assert all(0 <= x <= 18 for x in q)
    d = [0]*len(q)
    for i in range(len(q)//2):
        d[i] = max(0, q[i]-9)
        d[-i-1] = q[i]-d[i]
    if len(q) % 2:
        assert q[len(q)//2] % 2 == 0
        d[len(q)//2] = q[len(q)//2]//2
    return int(''.join(map(str, d[::-1])))


def integer_control(r, u, v, expected_time):
    n = realize(initial_word(r, u, v))
    first = None
    for t in range(1, expected_time+1):
        n += int(str(n)[::-1])
        if str(n) == str(n)[::-1] and first is None:
            first = t
    assert first == expected_time, (r, u, v, first, expected_time)


def main():
    certificates = prove_templates()
    cases = 0
    for r in tuple(range(1, 65)) + (127, 256, 1000):
        for u, v in FAST_CORES:
            integer_control(r, u, v, 4)
            cases += 1
        if r >= 5:
            integer_control(r, 1, 6, 11)
            cases += 1
    print(json.dumps({
        'universal_symbolic_normalization_certificates': certificates,
        'independent_integer_controls': cases,
        'proved': [
            'cores (2,5), (2,6), (3,5): first positive hit 4 for every r>=1',
            'core (1,6): first positive hit 11 for every r>=5',
        ],
        'not_claimed': [
            'classification of core (1,7)',
            'all-time status of core (1,6) at r=1,2,3,4',
            'a finite Lychrel witness or a result for the orbit of 196',
            'Lean verification',
        ],
    }, indent=2))


if __name__ == '__main__':
    main()
