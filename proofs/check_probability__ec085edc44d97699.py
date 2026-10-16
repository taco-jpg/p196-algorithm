"""Exact finite controls for PROBABILITY_RESULT.md; Python standard library only.

This is a checker, not an all-time avoidance search. It writes beside itself.
"""

from collections import Counter
from fractions import Fraction
from pathlib import Path
import json


def step(n):
    return n + int(str(n)[::-1])


def palindrome(n):
    s = str(n)
    return s == s[::-1]


def column_data(n):
    d = [int(x) for x in str(n)[::-1]]
    q = [a + b for a, b in zip(d, d[::-1])]
    c = [0]
    for x in q:
        c.append((x + c[-1]) // 10)
    return d, q, c


def correlated_pair(m):
    """Width 4m; selected match indicators are one common Bernoulli bit."""
    assert m >= 1
    half = [3] * (2 * m)
    for j in range(m):
        half[2 * j] = 3 if j % 2 == 0 else 8
    half[-1] = 11 - half[-2]  # Opposite 3/8 type at the center.
    d = [0] * (4 * m)
    for i, q in enumerate(half):
        d[i], d[-1 - i] = (1, 2) if q == 3 else (4, 4)
    a = int("".join(map(str, d[::-1])))
    b = int("".join(str(x + 1) for x in d[::-1]))
    return a, b


def main():
    out = {"status": "PASS", "decimal_lychrel_existence_proved": False}
    rho = Fraction(64, 125)  # Exactly 0.512.
    cases = []
    for m in range(1, 101):
        a, b = correlated_pair(m)
        selected = list(range(1, 2 * m, 2))
        rows = []
        for n in (a, b):
            d, q, c = column_data(n)
            assert len(d) == 4 * m and c[-1] == 0
            assert not palindrome(n)
            indicators = [int(c[k] == c[len(d) - 1 - k]) for k in selected]
            rows.append({"n": str(n), "Tn": str(step(n)),
                         "carries": c, "indicators": indicators})
        assert rows[0]["indicators"] == [1] * m
        assert rows[1]["indicators"] == [0] * m
        assert palindrome(step(a)) and not palindrome(step(b))
        assert all(int(y) == int(x) + 1 for x, y in zip(str(a), str(b)))
        if m >= 2:
            assert Fraction(1, 2) > rho ** m
        if m <= 3:
            cases.append({"m": m, "width": 4 * m,
                          "positions": selected, "atoms": rows})
    out["decoupling_family"] = {
        "m_checked": [1, 100], "widths_checked": [4, 400],
        "input_eta": "cos(pi/10) < 1", "selected_match_marginals": "1/2",
        "conditional_match_after_any_prior_match": "1",
        "palindrome_probability": "1/2", "rho": str(rho), "examples": cases,
    }

    # Exact counts and first-hit distribution for one fixed seed ensemble.
    seeds = [n for n in range(100, 1000) if not palindrome(n)]
    hits, survivors, outputs = Counter(), [], {}
    for n in seeds:
        x = n
        for t in range(1, 101):
            x = step(x)
            if palindrome(x):
                hits[t] += 1
                break
        else:
            survivors.append(n)
            outputs[n] = x
    expected = [196, 295, 394, 493, 592, 689, 691, 788, 790,
                879, 887, 978, 986]
    assert survivors == expected
    assert len(seeds) == 810 and sum(hits.values()) == 797
    assert hits[1] == 213 and max(hits) == 23
    image_groups = Counter(step(n) for n in survivors)
    assert image_groups == Counter({887: 7, 1675: 4, 1857: 2})
    assert len(set(outputs.values())) == 3
    out["three_digit_ensemble"] = {
        "seed_count": len(seeds), "horizon": 100,
        "first_hit_histogram": dict(sorted(hits.items())),
        "survivors": survivors, "one_step_image_multiplicities": dict(image_groups),
        "survivor_current_min_width": min(len(str(x)) for x in outputs.values()),
        "remaining_all_time_claim": "UNVERIFIED",
    }

    # Independent all-length formulas are proved in the accompanying text.
    # These modest literal controls are separate from root's n < 10^6 audit.
    counts = []
    for L in range(1, 6):
        actual = sum(palindrome(step(n))
                     for n in range(10 ** (L - 1), 10 ** L))
        m = L // 2
        formula = (4 if L == 1 else
                   (5 if L % 2 else 1) * 45 * 55 ** (m - 1)
                   + 8 * 9 ** (m - 1))
        assert actual == formula
        counts.append({"width": L, "one_step_palindrome_count": actual})
    out["one_step_counts"] = counts

    for n in range(1, 10000):
        x = n
        for _ in range(5):
            x = step(x)
        assert len(str(x)) > len(str(n))
    out["five_step_width_control"] = {"seeds": [1, 9999], "passed": True}

    # An event at one time does not upper-bound the event of any future hit.
    assert all(not palindrome(n) and not palindrome(step(n))
               and palindrome(step(step(n))) for n in (57, 58))
    out["union_counterexample"] = {"seeds": [57, 58], "P_hit_step_1": 0,
                                   "P_first_hit_step_2": 1, "P_ever_hit": 1}
    out["scope"] = ("Exact finite arithmetic plus written all-length counterexamples. "
                    "No random-digit hypothesis is assumed for an actual orbit.")
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"status": out["status"], "output": str(path),
                      "decoupling_widths": [4, 400], "three_digit_survivors": 13,
                      "existence_proved": False}, indent=2))


if __name__ == "__main__":
    main()
