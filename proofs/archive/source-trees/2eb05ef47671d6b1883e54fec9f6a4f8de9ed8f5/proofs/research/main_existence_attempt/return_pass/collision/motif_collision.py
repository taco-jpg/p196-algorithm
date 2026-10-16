"""Exact arbitrary-word collision coordinates for the S reservoir family.

This supplies a finite, variable-time collision identity, not a recurrent
family.  No infinite nonpalindromic orbit is asserted.
All words are symmetric pair sums, in low-to-high decimal order.
"""
from __future__ import annotations

from itertools import groupby
from pathlib import Path
import json
import random
import sys

sys.set_int_max_str_digits(100000)


def normal(q, carry=0):
    d = []
    for x in q:
        v = x + carry
        d.append(v % 10)
        carry = v // 10
    return tuple(d), carry


def pair_word(d):
    return tuple(x + y for x, y in zip(d, d[::-1]))


def step(q):
    d, h = normal(q)
    if h:
        d += (1,)
    return pair_word(d), h, d == d[::-1]


def A0():
    return (9, 9) + (18,) * 5 + (9, 9)


def B0(m):
    return (9, 9) + (18,) * m + (9, 9)


def separated(a, b, n):
    assert n >= 0
    return a + (0,) * n + b + (0,) * n + a


def companion(a, b):
    """One exact independent-island update; delta is the gap consumption.

    For n>=1, G(a 0^n b 0^n a) = a' 0^(n-delta) b'
    0^(n-delta) a'.  Both returned motifs have positive end coefficients.
    """
    assert a == a[::-1] and b == b[::-1] and a[0] > 0 and b[0] > 0
    da, h = normal(a)
    db, k = normal(b)
    ea = da + ((1,) if h else ())
    if h:
        eb = db + (k,)
    elif k:
        eb = (0,) + db + (1,)
    else:
        eb = db
    aa, bb = pair_word(ea), pair_word(eb)
    assert aa[0] > 0 and bb[0] > 0
    return aa, bb, max(h, k), h, ea == ea[::-1], eb == eb[::-1]


def collision_step(a, b):
    """Exact seam-coupled update at zero gap, via two carry variants.

    Unlike companion(), carries are passed from A into B and from B into A.
    """
    x, c = normal(a, 0)
    y, c = normal(b, c)
    z, c = normal(a, c)
    d = x + y + z + ((1,) if c else ())
    return pair_word(d), c, d == d[::-1]


def realize(q):
    assert q == q[::-1] and q[0] > 0
    d = [0] * len(q)
    for i in range(len(q) // 2):
        d[i] = max(0, q[i] - 9)
        d[-1-i] = q[i] - d[i]
    if len(q) % 2:
        assert q[len(q)//2] % 2 == 0
        d[len(q)//2] = q[len(q)//2] // 2
    return int(''.join(map(str, d[::-1])))


def literal_q(n):
    d = tuple(map(int, str(n)[::-1]))
    return pair_word(d)


def rle(q):
    return [[x, len(tuple(g))] for x, g in groupby(q)]


def random_word(rng):
    half = [rng.randrange(19) for _ in range(rng.randrange(1, 12))]
    half[0] = rng.randrange(1, 19)
    center = [2*rng.randrange(10)] if rng.randrange(2) else []
    return tuple(half + center + half[::-1])


def independent_controls():
    """Controls use literal integer reversal, not the carry implementation."""
    rng = random.Random(20261014)
    cases = 0
    # Every positive constant symmetric A of length two, every positive even
    # one-column B, and gaps 1..4, then arbitrary longer valid motifs.
    inputs = [((x, x), (y,), n)
              for x in range(1, 19) for y in range(2, 19, 2)
              for n in range(1, 5)]
    inputs += [(random_word(rng), random_word(rng), rng.randrange(1, 8))
               for _ in range(5000)]
    for a, b, n in inputs:
        aa, bb, delta, h, pa, pb = companion(a, b)
        q = separated(a, b, n)
        seed = realize(q)
        out = seed + int(str(seed)[::-1])
        assert literal_q(out) == separated(aa, bb, n-delta)
        assert (str(out) == str(out)[::-1]) == (pa and pb)
        assert len(str(out)) - len(str(seed)) == h
        # Check the carry-coupled zero-gap boundary independently too.
        cq = a + b + a
        cs = realize(cq)
        co = cs + int(str(cs)[::-1])
        predicted, hh, pp = collision_step(a, b)
        assert literal_q(co) == predicted
        assert pp == (str(co) == str(co)[::-1])
        assert hh == len(str(co)) - len(str(cs))
        assert len(aa + bb + aa) - len(predicted) == 2*delta + h-hh
        if delta == 0:
            assert predicted == aa + bb + aa
        else:
            assert len(aa + bb + aa) > len(predicted)
        cases += 1
    return {"independent_integer_separated_cases": cases,
            "independent_integer_zero_gap_cases": cases}


def fixed_companion(m, horizon):
    a, b = A0(), B0(m)
    consumed = 0
    states = [(a, b, consumed)]
    outer_pals, joint_pals = [], []
    center_death = None
    for t in range(1, horizon+1):
        a, b, delta, h, pa, pb = companion(a, b)
        consumed += delta
        if pa:
            outer_pals.append(t)
        if pa and pb:
            joint_pals.append(t)
        if center_death is None and b[len(b)//2] != 18:
            center_death = t
        states.append((a, b, consumed))
    return states, outer_pals, joint_pals, center_death


def main():
    controls = independent_controls()
    states, pals, joint, death = fixed_companion(8, 512)
    outer_death = next(t for t, (a, b, k) in enumerate(states)
                       if t >= 13 and a[len(a)//2] != 18)
    assert death == 14 and outer_death == 42
    examples = []
    literal_transitions = 0
    for n in (7, 8, 16, 23, 24, 32, 64, 128, 240):
        tau = next(t for t, (_, _, k) in enumerate(states) if k == n)
        tau_next = next(t for t, (_, _, k) in enumerate(states) if k == n+1)
        seed = realize(separated(A0(), B0(8), n))
        value = seed
        for t in range(tau+1):
            a, b, k = states[t]
            assert literal_q(value) == separated(a, b, n-k)
            assert str(value) != str(value)[::-1]
            if t < tau:
                value += int(str(value)[::-1])
                literal_transitions += 1
        a, b, k = states[tau]
        actual, h_actual, p = collision_step(a, b)
        aa, bb, delta, h, pa, pb = companion(a, b)
        length_deficit = len(aa + bb + aa) - len(actual)
        coupled_value = value
        for t in range(tau+1, tau_next+1):
            coupled_value += int(str(coupled_value)[::-1])
        target_a, target_b, _ = states[tau_next]
        target = target_a + target_b + target_a
        assert literal_q(coupled_value) != target
        assert len(target) > len(str(coupled_value))
        examples.append({"M": 8, "N": n, "collision_time": tau,
                         "outer_length": len(a), "center_length": len(b),
                         "A": list(a), "B": list(b),
                         "next_gap_consumption": delta,
                         "next_clock": h, "actual_next_clock": h_actual,
                         "independent_continuation_length_excess": length_deficit,
                         "next_parameter_collision_time": tau_next,
                         "proposed_adjacent_return_time": tau_next-tau,
                         "adjacent_return_target_length_excess": len(target)-len(str(coupled_value)),
                         "next_output_palindrome": p})
    result = {
        "status": "exact variable-time collision identity; no recurrent family",
        "companion_horizon": 512,
        "M8_inherited_center_death": death,
        "regenerated_outer_inherited_18_death": outer_death,
        "M8_consumed_at_42": states[42][2],
        "M8_all_N_at_least_collision_after_all_inherited_18_death": states[42][2]+1,
        "outer_output_palindrome_times_through_512": pals,
        "M8_joint_output_palindrome_times_through_512": joint,
        "M8_consumed_at_512": states[-1][2],
        "independent_S8N_integer_transitions": literal_transitions,
        **controls,
        "collision_examples": examples,
        "all_time_safety": False,
        "closed_return": False,
        "finite_Lychrel_witness": False,
    }
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'collision_examples'}, indent=2))


if __name__ == '__main__':
    main()
