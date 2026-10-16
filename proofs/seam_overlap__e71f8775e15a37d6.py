"""Exact context-sensitive collision identities; no Lychrel existence claim.

All words are low-to-high symmetric decimal pair sums.  The proof for
arbitrary finite words is in STATUS.md.  This file supplies independent
ordinary-integer controls and exact finite counterexamples, not a search
for long palindrome-free trajectories.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import random
import sys

sys.set_int_max_str_digits(100000)


def normal(q, carry=0):
    digits = []
    for coefficient in q:
        total = coefficient + carry
        digits.append(total % 10)
        carry = total // 10
    return tuple(digits), carry


def pair(d):
    return tuple(a + b for a, b in zip(d, d[::-1]))


def step(q):
    d, h = normal(q)
    return pair(d + ((1,) if h else ())), h


def canonical(q):
    return (bool(q) and q == q[::-1] and 1 <= q[0] <= 18
            and all(0 <= x <= 18 for x in q)
            and (len(q) % 2 == 0 or q[len(q) // 2] % 2 == 0))


def realize(q):
    assert canonical(q)
    d = [0] * len(q)
    for i in range(len(q) // 2):
        d[i] = max(0, q[i] - 9)
        d[-1-i] = q[i] - d[i]
    if len(q) % 2:
        d[len(q) // 2] = q[len(q) // 2] // 2
    return int("".join(map(str, d[::-1])))


def literal_step(q):
    """No carry routine or motif identity is used in this control."""
    n = realize(q)
    successor = n + int(str(n)[::-1])
    return pair(tuple(map(int, str(successor)[::-1])))


def high_reset_radius(q):
    """The neutral prefix before the first carry-1 reset."""
    assert canonical(q)
    for i, x in enumerate(q):
        if x != 9:
            assert x >= 10
            return i
    raise AssertionError("The all-9 transfer is not a constant carry-1 map")


def overlap(words):
    """Add shared endpoint coefficients; do not normalize or clip them."""
    assert words
    result = list(words[0])
    for word in words[1:]:
        result[-1] += word[0]
        result.extend(word[1:])
    return tuple(result)


def prediction(motifs):
    """Universal high-reset seam formula, including every boundary."""
    assert motifs and tuple(motifs) == tuple(motifs)[::-1]
    radii = [high_reset_radius(a) for a in motifs]
    q = tuple(itertools.chain.from_iterable(motifs))
    length = len(q)
    local = []
    for a in motifs:
        b, h = step(a)
        assert h == 1
        local.append(b)
    raw = overlap(local)
    assert len(raw) == length + 1

    # H = (x-10) sum_{j>=2} x^s_j (1+...+x^(r_j-1)).
    h_poly = [0] * (length + 1)
    start = 0
    for j, (a, radius) in enumerate(zip(motifs, radii)):
        if j:
            for k in range(radius):
                h_poly[start+k] -= 10
                h_poly[start+k+1] += 1
        start += len(a)
    correction = tuple(a + b for a, b in zip(h_poly, h_poly[::-1]))
    result = tuple(a + b for a, b in zip(raw, correction))
    return result, raw, correction, radii


def check_case(motifs):
    predicted, raw, correction, radii = prediction(motifs)
    q = tuple(itertools.chain.from_iterable(motifs))
    actual = literal_step(q)
    assert actual == predicted
    assert canonical(actual)
    assert len(actual) == len(q) + 1
    assert sum(actual) == sum(raw) - 18 * sum(radii[1:])
    for a in motifs:
        assert literal_step(a) == step(a)[0]
    if not any(radii):
        assert actual == raw and not any(correction)
    return actual


def random_motif(rng):
    radius = rng.randrange(0, 12)
    half = [rng.randrange(10, 19)]
    half += [rng.randrange(19) for _ in range(rng.randrange(0, 9))]
    center = [2*rng.randrange(10)] if rng.randrange(2) else []
    core = tuple(half + center + half[::-1])
    return (9,)*radius + core + (9,)*radius


def long_radius_family(r):
    assert r >= 1
    a = (9,)*r + (10, 10) + (9,)*r
    out = ((10,) + (9,)*(r-1) + (0, 2, 1)
           + (0,)*(2*r-1) + (1, 2, 0) + (9,)*(r-1) + (10,))
    assert check_case((a, a)) == out
    _, raw, correction, _ = prediction((a, a))
    seam = len(a)
    expected = [0] * len(out)
    expected[seam] = -20
    for j in range(1, r):
        expected[seam-j] = expected[seam+j] = -9
    expected[seam-r] = expected[seam+r] = 1
    assert correction == tuple(expected)
    assert sum(raw) - sum(out) == 18*r
    return {"r": r, "input_length": 2*len(a), "output_length": len(out),
            "maximum_nonzero_correction_distance": r,
            "pair_sum_mass_correction": -18*r}


def two_step_constant_family(a, m):
    assert 14 <= a <= 17 and m >= 2
    p = a - 9
    q = (a,)*m
    if len(q) % 2 and a % 2:
        return False
    first = (p,) + (2*p,)*(m-1) + (p,)
    if m == 2:
        second = (2*p+1, 4*p-20, 2*p+1)
    else:
        second = ((2*p+1, 4*p-19) + (4*p-18,)*(m-3)
                  + (4*p-19, 2*p+1))
    assert literal_step(q) == first
    assert literal_step(first) == second
    assert canonical(second)
    return True


def independent_overlap_failure(a):
    """Track the proposed independently evolved splice until first failure."""
    component, h = step((a,))
    assert h == 1
    actual = overlap((component, component))
    assert canonical(actual)
    records = []
    for t in range(1, 6):
        actual_next = literal_step(actual)
        component_next = literal_step(component)
        proposed = overlap((component_next, component_next))
        records.append({"updates_after_first_splice": t,
                        "actual": list(actual_next),
                        "independent_target": list(proposed),
                        "component_overflow": len(component_next)-len(component),
                        "equal": actual_next == proposed})
        if actual_next != proposed:
            return {"atom": a, "first_failure": t,
                    "failure_type": ("length" if len(actual_next) != len(proposed)
                                     else "coefficients"), "steps": records}
        component, actual = component_next, actual_next
    raise AssertionError("A duplicated component cannot have five exact updates")


def main():
    cases = 0
    # Every ordered outer/central choice from a small all-reset catalog.
    catalog = [(x, x) for x in range(10, 19)]
    catalog += [(9,)*r + (x, x) + (9,)*r
                for r in range(1, 4) for x in range(10, 19)]
    for a, b in itertools.product(catalog, repeat=2):
        check_case((a, b, a))
        cases += 1
    rng = random.Random(202610140731)
    zero_radius = 0
    for _ in range(6000):
        left = [random_motif(rng) for _ in range(rng.randrange(0, 5))]
        center = [random_motif(rng)] if rng.randrange(2) or not left else []
        motifs = tuple(left + center + left[::-1])
        check_case(motifs)
        zero_radius += not any(high_reset_radius(a) for a in motifs)
        cases += 1
    radius_controls = [long_radius_family(r) for r in range(1, 65)]
    radius_controls += [long_radius_family(r) for r in (127, 256, 1000)]
    constant_controls = sum(two_step_constant_family(a, m)
                            for a in range(14, 18) for m in range(2, 130))
    failures = [independent_overlap_failure(a) for a in (10, 12, 14, 16, 18)]
    minimal_q = (14, 14)
    minimal_seed = realize(minimal_q)
    assert minimal_seed == 95
    minimal_orbit = [minimal_seed]
    for _ in range(3):
        minimal_orbit.append(minimal_orbit[-1] + int(str(minimal_orbit[-1])[::-1]))
    assert minimal_orbit == [95, 154, 605, 1111]

    result = {
        "status": "exact seam correction; fixed independent splice is not recurrent",
        "all_time_safety": False,
        "finite_Lychrel_witness": False,
        "new_Lean_theorem": False,
        "arbitrary_motif_integer_controls": cases,
        "random_zero_radius_controls": zero_radius,
        "long_radius_integer_controls": len(radius_controls),
        "long_radius_selected": [radius_controls[i] for i in (0, 1, 15, 63, 64, 65, 66)],
        "two_step_constant_family_controls": constant_controls,
        "independent_overlap_failures": failures,
        "minimal_singleton_even_atom_two_step_failure": {
            "atom": 14, "number_of_copies": 2,
            "ordinary_seed": minimal_seed, "ordinary_orbit": minimal_orbit,
            "first_pair_output": [5, 10, 5],
            "actual_second_pair_output": [11, 0, 11],
            "independent_overlap_second_target": [10, 20, 10]},
    }
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('independent_overlap_failures', 'long_radius_selected')},
                     indent=2))


if __name__ == '__main__':
    main()
