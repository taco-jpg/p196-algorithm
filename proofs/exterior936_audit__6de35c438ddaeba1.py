"""Exact arithmetic conditions for the proposed 24-phase 936 exterior.

This is not a boundary search. The conditions are necessary, compatible,
and do not certify either an exterior or its impossibility.
"""
from pathlib import Path
from fractions import Fraction
from math import gcd
import json

HERE = Path(__file__).parent
B = (9, 3, 6)
W = (9, 3, 8, 10, 4, 10, 8, 3, 9)


def value(word, base):
    return sum(x * base**i for i, x in enumerate(word))


def cyclic(q):
    """Independent periodic carry normalization; no search module imported."""
    n = len(q)
    j = next(i for i, x in enumerate(q) if x != 9)
    a = [None]*n
    b = [None]*n
    a[(j+1) % n] = int(q[j] >= 10)
    b[j] = int(q[j] >= 10)
    for k in range(1, n):
        i = (j+k) % n
        a[(i+1) % n] = (q[i]+a[i])//10
        i = (j-k) % n
        b[i] = (q[i]+b[(i+1) % n])//10
    lo = tuple(q[i]+a[i]-10*a[(i+1) % n] for i in range(n))
    hi = tuple(q[i]+b[(i+1) % n]-10*b[i] for i in range(n))
    return lo, hi


def run():
    rows = []
    q = B
    for t in range(24):
        lo, hi = cyclic(q)
        rows.append({"t": t, "q": q, "lo": lo, "hi": hi,
                     "hi_value": value(hi, 10)})
        h = t % 2
        q = tuple(lo[i]+hi[(i-h) % 3] for i in range(3))
    assert q == B
    even = sum(r["hi_value"] for r in rows if r["t"] % 2 == 0)
    odd = sum(r["hi_value"] for r in rows if r["t"] % 2 == 1)
    coefficient = Fraction(even + 10*odd, 999)
    assert (even, odd, coefficient) == (5994, 5994, 66)

    assert sum(W) == 64 and value(W, -1) == 12
    assert sum(B) == 18 and value(B, -1) == 12
    multiplier = pow(22, 12, 99)
    assert multiplier == 55 and gcd(multiplier-1, 99) == 9
    # Supplementary exact evaluations of the displayed polynomial formulas.
    controls = 0
    for P in ((8,), (8, 12, 9), (8, 12, 9, 0), (8, 3, 10, 0, 14)):
        for m in range(5):
            q = P + B*m + W + B[::-1]*m + P[::-1]
            assert value(q, -1) == 2*value(P, -1)+12*(-1)**len(P)
            assert value(q, 10) % 99 == (2*value(P, 10)+10**len(P)) % 99
            controls += 1
    out = {
        "status": "necessary conditions; no obstruction or exterior obtained",
        "family": "P (936)^m W (639)^m reverse(P)",
        "center": W,
        "mod11_condition": "P(-1)+6*(-1)^p == 0 mod 11, p=len(P)",
        "mod99_q_value": "2*P(10)+10^p mod 99, independent of m",
        "24_step_scalar_mod99": multiplier,
        "rational_tail_hi_even_sum": even,
        "rational_tail_hi_odd_sum": odd,
        "rational_exterior_condition":
            "sum_even H_t(10)+10*sum_odd H_t(10)+12 = 66*10^p",
        "bulk_trace": rows,
        "finite_polynomial_controls": controls,
        "finite_Lychrel_witness": False,
    }
    HERE.joinpath("exterior936_audit.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({k: v for k, v in out.items() if k != "bulk_trace"}, indent=2))


if __name__ == "__main__":
    run()
