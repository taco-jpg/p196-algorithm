"""Exact collision-front identities and a mass-regenerating gate.

No all-time invariant or Lychrel witness is asserted.  The two global
parameter identities are proved by affine-run normalization for every
M = k+1, k >= 0.  Ordinary integer checks are independent controls only.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "continuation"),
               str(ROOT / "main_existence_attempt" / "defect_family")]
from wall_renewal_check import Len, ONE, canon, expand, normal, add_runs
from symbolic_defects import step


def literals(word):
    return [(x, ONE) for x in word]


def family(z):
    half = canon(literals((1, z, 4)) + [(9, Len(1, 1))]
                 + literals((14, 2, 6)))
    return canon(half + half[::-1])


def as_json(runs):
    # Original parameter M = k+1.
    return [[x, n.a, n.b - n.a] for x, n in runs]


def realize(q):
    """A positive canonical decimal integer with exactly these pair sums."""
    assert tuple(q) == tuple(q)[::-1] and len(q) % 2 == 0
    digits = [0] * len(q)
    for i in range(len(q) // 2):
        digits[i] = max(0, q[i] - 9)
        digits[-1 - i] = q[i] - digits[i]
    assert digits[-1] != 0
    return sum(x * 10**i for i, x in enumerate(digits))


def integer_step(n):
    return n + int(str(n)[::-1])


def pair_sums(n):
    d = tuple(map(int, str(n)[::-1]))
    return tuple(x + y for x, y in zip(d, d[::-1]))


def local(q, a, b, h):
    """Known-window q update with independent carries at its two ends.

    On overflow keep output positions 1,...,L-1: those are the positions
    whose two contributing old columns both belong to the known window.
    """
    lo, _ = normal(q, a)
    hi, _ = normal(q[::-1], b)
    hi = hi[::-1]
    if h:
        from symbolic_defects import take, size
        _, lo = take(lo, ONE)
        hi, _ = take(hi, size(hi) - ONE)
    return add_runs(lo, hi)


def global_identities():
    M = Len(1, 1)
    A0 = family(2)
    A1, h1 = step(A0)
    expected1 = canon(literals((2, 4)) + [(9, M + ONE)]
                     + literals((8, 5, 12, 12, 5, 8))
                     + [(9, M + ONE)] + literals((4, 2)))
    assert A1 == expected1 and h1 == 0
    A2, h2 = step(A1)
    expected2 = canon(literals((4, 8)) + [(18, M + ONE)]
                     + literals((16, 11, 5, 5, 11, 16))
                     + [(18, M + ONE)] + literals((8, 4)))
    assert A2 == expected2 and h2 == 0

    B0 = family(8)
    B1, h1 = step(B0)
    B2, h2 = step(B1)
    B3, h3 = step(B2)
    expectedB2 = canon(literals((5, 12)) + [(9, M + ONE)]
                       + literals((17, 11, 5, 5, 11, 17))
                       + [(9, M + ONE)] + literals((12, 5)))
    expectedB3 = canon(literals((11, 5)) + [(0, M + ONE)]
                       + literals((16, 3, 11, 11, 3, 16))
                       + [(0, M + ONE)] + literals((5, 11)))
    assert B2 == expectedB2 and B3 == expectedB3
    assert (h1, h2, h3) == (0, 0, 0)
    traces = {2: [A0, A1, A2], 8: [B0, B1, B2, B3]}
    # Every state in these exact families has a positive-length odd q
    # coefficient, which rules out a palindromic decimal realization.
    for trace in traces.values():
        assert all(any(x % 2 and n.b > 0 for x, n in q) for q in trace)
    controls = []
    for Mvalue in (1, 2, 3, 7, 23):
        for z, trace in traces.items():
            n = realize(expand(trace[0], Mvalue - 1))
            seed = n
            for t, expected in enumerate(trace):
                assert pair_sums(n) == expand(expected, Mvalue - 1)
                assert str(n) != str(n)[::-1]
                if t + 1 < len(trace):
                    n = integer_step(n)
            controls.append({"M": Mvalue, "z": z, "seed": str(seed),
                             "verified_transitions": len(trace) - 1})
    return {"domain": "every integer M>=1",
            "A": [as_json(q) for q in traces[2]],
            "B": [as_json(q) for q in traces[8]],
            "independent_integer_controls": controls}


def neutral_front_identities():
    """Verify the arbitrary-M formulas, without sampling M."""
    M = Len(1, 1)
    checks = 0
    for x in range(19):
        if x == 9:
            continue
        for a in (0, 1):
            q = canon(literals((x,)) + [(9, M)]
                      + literals((18 - x,)))
            result = local(q, a, 1 - a, 0)
            newx = 2*x + a + 1 if x <= 8 else 2*x + a - 20
            expected = canon(literals((newx,)) + [(9, M)]
                             + literals((18 - newx,)))
            assert result == expected
            newxO = x + 10 if x <= 8 else x - 10
            # Overflow boundaries need one further input symbol to compute.
            # Pad with z,18-z so that those two boundary positions are known.
            # The asserted subwindow is independent of z and outer carries.
            for b in (0, 1):
                for z in (0, 3, 9, 12, 18):
                    padded = canon(literals((z, x)) + [(9, M)]
                                   + literals((18 - x, 18 - z)))
                    resultO = local(padded, a, b, 1)
                    expectedO = canon(literals((newxO,)) + [(9, M - ONE)]
                                      + literals((18 - newxO,)))
                    # local(padded) has length M+3; the desired M+1
                    # output omits the first and last known positions.
                    from symbolic_defects import take, size
                    _, inner = take(resultO, ONE)
                    inner, _ = take(inner, size(inner) - ONE)
                    assert inner == expectedO
                    checks += 1
            checks += 1
    return checks


def collision_dependence():
    records = []
    for z in (1, 8):
        half = (10, 1, z, 2, 16, 18-z, 1)
        q = half + half[::-1]
        n = realize(q)
        nxt = integer_step(n)
        r = pair_sums(nxt)
        assert len(r) == len(q) + 1
        assert q[3:5] == (2, 16)
        expected = (z + 2, 9, 16-z)
        assert r[3:6] == expected
        records.append({"z": z, "seed": str(n), "next_integer": str(nxt),
                        "old_pair": [2, 16], "old_inward_carries": [0, 1],
                        "overflow": 1, "new_front_window": list(expected)})
    return records


def absorbing_wake_controls():
    """Controls supplement the period-four column proof in the report."""
    count = 0
    for k in (1, 2, 3, 8):
        U = (14, 14, 4, 4) * k
        for M in (0, 1, 2, 7):
            q = canon(literals(U + (9,)*M + U))
            out = local(q, 0, 1, 0)
            assert expand(out, 0) == (9,)*(M + 8*k)
            count += 1
    return count


def run():
    result = {"status": "exact component identities; no recurrent family",
              "global_identities": global_identities(),
              "arbitrary_gap_front_checks": neutral_front_identities(),
              "collision_same_state_different_wake": collision_dependence(),
              "absorbing_wake_finite_controls": absorbing_wake_controls(),
              "finite_Lychrel_witness": False}
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"],
                      "domain": result["global_identities"]["domain"],
                      "arbitrary_gap_front_checks": result["arbitrary_gap_front_checks"],
                      "collision_examples": result["collision_same_state_different_wake"]},
                     indent=2))


if __name__ == "__main__":
    run()
