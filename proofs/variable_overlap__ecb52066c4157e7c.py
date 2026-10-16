"""One-step classification of variable-depth independent overlap.

This is a bounded exact-closure investigation.  It does not treat finite
nonpalindromic trajectories as evidence of an infinite safe orbit.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import random

from seam_overlap import canonical, literal_step, pair, realize


def shifted_double(a, shift):
    assert shift >= 0
    result = [0] * (len(a) + shift)
    for i, x in enumerate(a):
        result[i] += x
        result[i+shift] += x
    return tuple(result)


def component_digits(a):
    # The value of a pair-sum polynomial is the ordinary successor integer.
    value = sum(x * 10**i for i, x in enumerate(a))
    return tuple(map(int, str(value)[::-1]))


def normalization_carries(raw):
    carry = 0
    count = 0
    for x in raw:
        carry = (x + carry) // 10
        assert carry in (0, 1)
        count += carry
    return count


def check_closure(a, shift):
    q = shifted_double(a, shift)
    if not canonical(q):
        return None
    ga = literal_step(a)
    gq = literal_step(q)
    d = component_digits(a)
    assert pair(d) == ga
    count = normalization_carries(shifted_double(d, shift))
    assert sum(gq) == 2*sum(ga) - 18*count
    forced_shift = len(gq) - len(ga)
    target = shifted_double(ga, forced_shift) if forced_shift >= 0 else None
    closed = target == gq
    assert closed == (count == 0)
    if closed:
        assert forced_shift == shift
        n = realize(a)
        N = realize(q)
        n_next = n + int(str(n)[::-1])
        N_next = N + int(str(N)[::-1])
        assert N_next == (1+10**shift)*n_next
        assert (str(n_next) == str(n_next)[::-1]) == (str(N_next) == str(N_next)[::-1])
    return {"closed": closed, "carry_count": count,
            "forced_shift_change": forced_shift-shift}


def catalog():
    for width in range(1, 5):
        if width == 1:
            for c in range(2, 19, 2):
                yield (c,)
            continue
        half_width = width // 2
        for half in itertools.product(range(19), repeat=half_width):
            if not half[0]:
                continue
            centers = [(2*c,) for c in range(10)] if width % 2 else [()]
            for center in centers:
                yield half + center + half[::-1]


def delayed_return_controls(a, shift, horizon=8):
    q = shifted_double(a, shift)
    if not canonical(q):
        return []
    seed_a, seed_q = a, q
    failed_at = None
    pal_at = None
    returns = []
    for t in range(1, horizon+1):
        n = realize(q)
        successor = n + int(str(n)[::-1])
        if pal_at is None and str(successor) == str(successor)[::-1]:
            pal_at = t
        a, q = literal_step(a), literal_step(q)
        forced_shift = len(q) - len(a)
        target = shifted_double(a, forced_shift) if forced_shift >= 0 else None
        if target != q and failed_at is None:
            failed_at = t
        if target == q and failed_at is not None:
            returns.append({"initial_component": list(seed_a),
                            "initial_shift": shift,
                            "initial_whole": list(seed_q),
                            "first_departure": failed_at,
                            "return_time": t,
                            "return_component": list(a),
                            "return_shift": forced_shift,
                            "first_whole_palindrome_by_return": pal_at,
                            "return_whole": list(q)})
    return returns


def main():
    case_count = 0
    closed_count = 0
    shifted_count = 0
    deferred = []
    for a in catalog():
        for shift in range(len(a)+1):
            result = check_closure(a, shift)
            if result is None:
                continue
            case_count += 1
            closed_count += result["closed"]
            shifted_count += result["forced_shift_change"] != 0
            deferred += delayed_return_controls(a, shift)

    rng = random.Random(202610140937)
    random_count = 0
    for _ in range(3000):
        half = [rng.randrange(1, 10)] + [rng.randrange(10) for _ in range(rng.randrange(10))]
        center = [2*rng.randrange(5)] if rng.randrange(2) else []
        a = tuple(half + center + half[::-1])
        shift = rng.randrange(len(a)+1)
        result = check_closure(a, shift)
        assert result is not None
        random_count += 1
        closed_count += result["closed"]
        shifted_count += result["forced_shift_change"] != 0

    safe_returns = [r for r in deferred if r["first_whole_palindrome_by_return"] is None]
    result = {
        "status": "exact variable-overlap closure classification; no safe recurrent family",
        "complete_small_component_width_max": 4,
        "complete_small_canonical_overlap_cases": case_count,
        "random_additional_cases": random_count,
        "closed_one_step_cases_total": closed_count,
        "cases_with_forced_shift_change_total": shifted_count,
        "finite_delayed_return_horizon": 8,
        "finite_delayed_return_records": len(deferred),
        "finite_delayed_return_records_safe_through_return": len(safe_returns),
        "finite_delayed_return_examples": deferred[:12],
        "safe_finite_delayed_return_examples": safe_returns[:12],
        "all_time_safety": False,
        "finite_Lychrel_witness": False,
    }
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if "examples" not in k}, indent=2))


if __name__ == '__main__':
    main()
