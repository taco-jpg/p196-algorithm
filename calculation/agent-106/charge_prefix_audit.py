#!/usr/bin/env python3
"""Independent integer audit of strong-charge completion of prefix edges.

Reference targets come from whole ordinary integers, not a column carry
routine: use the coefficient word B ++ [(2*b-2)*h] ++ reverse(B), obtain
its base-b digits, and add opposite digits.  The middle coefficient forces
the prescribed reverse-entry bit h.  The unchanged A120 mirror supplies an
additional independent comparison for the restored autonomous edge.

The underlying proof is algebraic. With A=alt(B), s=(-1)^n and modulus b+1,
the low and high digit sums satisfy D=A-s*e and R=A+g-s*h. Hence

  g=0: alt(B') = 2*A-s*(e+h),
  g=1: alt(B') = s*(h-e-r_top)                 (mod b+1).

If the source strong charge A-s is zero, zero target charge is equivalent
to e+h=1 and (g=0 or r_top=(b-1)*e).  For g=1 the source-charge premise is
unnecessary: h-e-r_top lies in [-b,1], so its congruence to 1 allows only
the two endpoint cases (h,e,r_top)=(1,0,0),(0,1,b-1).

  python3 calculation/agent-106/charge_prefix_audit.py
  python3 -O calculation/agent-106/charge_prefix_audit.py
  python3 calculation/agent-106/charge_prefix_audit.py --arithmetic-only
"""

import argparse
from collections import Counter
from itertools import product
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import charge_prefix as subject
import neutral_band_search as mirror


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer_value(base, coefficients):
    value = 0
    for coefficient in reversed(coefficients):
        value = base * value + coefficient
    return value


def integer_digits(base, value):
    result = []
    while value:
        value, digit = divmod(value, base)
        result.append(digit)
    return result


def alternating(coefficients):
    return sum(coefficients[::2]) - sum(coefficients[1::2])


def integer_edge(base, source, high):
    source = tuple(source)
    require(type(base) is int and base >= 2, "reference base must be >=2")
    require(source and source[0] > 0, "integer reference needs a positive head")
    require(all(type(x) is int and 0 <= x <= 2 * base - 2 for x in source),
            "reference coefficient outside its valid range")
    require(type(high) is int and high in (0, 1), "reference high carry must be a bit")
    n = len(source)
    scale = base ** n
    low_value = integer_value(base, source)
    reverse_value = integer_value(base, source[::-1])
    e = low_value // scale
    g = (reverse_value + high) // scale
    r_top = (reverse_value + high) % base
    whole = low_value + (2 * base - 2) * high * scale + reverse_value * scale * base
    digits = integer_digits(base, whole)
    require(len(digits) == 2 * n + 1 + g, "whole-integer overflow disagrees")
    target = tuple(digits[i] + digits[-1 - i] for i in range(n))
    sign = 1 if n % 2 == 0 else -1
    source_charge = (low_value - sign) % (base + 1)
    target_charge = (integer_value(base, target) - sign) % (base + 1)
    closed = e + high == 1 and (g == 0 or r_top == (base - 1) * e)
    return {"source": source, "target": target, "e": e, "h": high, "g": g,
            "r_top": r_top, "source_charge": source_charge,
            "target_charge": target_charge, "terminal_closed": closed}


def check_edge(base, source, high, counts=None):
    reference = integer_edge(base, source, high)
    measured = subject.edge_data(base, source, high)
    require(measured == reference, f"integer/core mismatch: base={base}, B={source}, h={high}")
    target, e, g, r_top = (reference[key] for key in ("target", "e", "g", "r_top"))
    sign, modulus = (-1) ** len(source), base + 1
    predicted = (2 * alternating(source) - sign * (e + high) if g == 0
                 else sign * (high - e - r_top))
    require((alternating(target) - predicted) % modulus == 0,
            "independently evaluated charge identity fails")
    if reference["source_charge"] == 0:
        require((reference["target_charge"] == 0) == reference["terminal_closed"],
                "charged-source equivalence fails")
    if g == 1:
        require((reference["target_charge"] == 0) == reference["terminal_closed"],
                "overflow target-only equivalence fails")

    center = [(2 * base - 2) * (1 - e)]
    require(mirror.hyp(base, list(source), center), "A120 comparison source fails Hyp")
    raw = tuple(mirror.nextB(base, list(source), center))
    actual_g = mirror.gam(base, list(source), center)
    restored = raw == target + (base - 1,) * g and actual_g == g
    require(restored == reference["terminal_closed"], "terminal predicate/raw-edge mismatch")
    if counts is not None:
        counts["edges"] += 1
        counts[f"g{g}"] += 1
        counts["charged_source_edges"] += reference["source_charge"] == 0
        counts["charged_target_edges"] += reference["target_charge"] == 0
        counts["terminal_closed_edges"] += reference["terminal_closed"]
    return reference


def arithmetic_audit():
    exhaustive = Counter()
    scopes = [(base, 4) for base in range(2, 8)] + [(10, 3)]
    for base, max_width in scopes:
        for width in range(1, max_width + 1):
            for head in range(1, 2 * base - 1):
                for suffix in product(range(2 * base - 1), repeat=width - 1):
                    source = (head,) + suffix
                    for high in (0, 1):
                        check_edge(base, source, high, exhaustive)
    require(exhaustive["edges"] == 119444, "exhaustive scope count changed")

    sampled = Counter()
    rng = random.Random(106202)
    bases = (2, 3, 4, 5, 7, 8, 10, 11, 16, 20, 26, 32)
    for _ in range(5000):
        base = bases[rng.randrange(len(bases))]
        width = rng.randrange(1, 129)
        source = (rng.randrange(1, 2 * base - 1),) + tuple(
            rng.randrange(2 * base - 1) for _ in range(width - 1))
        for high in (0, 1):
            check_edge(base, source, high, sampled)
    require(sampled["edges"] == 10000, "random scope count changed")
    print("EXHAUSTIVE_INTEGER_EDGES " + repr(dict(sorted(exhaustive.items()))), flush=True)
    print("RANDOM_INTEGER_EDGES seed=106202 widths=1..128 "
          + repr(dict(sorted(sampled.items()))), flush=True)
    return exhaustive, sampled


def negative_controls():
    source_only = check_edge(2, (2,), 1)
    require(source_only["source_charge"] == 0 and source_only["target_charge"] != 0
            and not source_only["terminal_closed"], "source-only negative control changed")
    target_only = check_edge(2, (1,), 0)
    require(target_only["g"] == 0 and target_only["source_charge"] != 0
            and target_only["target_charge"] == 0 and not target_only["terminal_closed"],
            "nonoverflow target-only negative control changed")
    weak = check_edge(3, (4, 1), 0)
    weak_source = (2 * alternating(weak["source"]) + 2) % 4
    weak_target = (2 * alternating(weak["target"]) + 2) % 4
    require(weak_source == weak_target == 0 and weak["source_charge"] == weak["target_charge"] == 2,
            "weak-charge residues changed")
    require(not weak["terminal_closed"] and weak["e"] == weak["h"] == 0 and weak["g"] == 1,
            "weak-charge example no longer refutes closure")
    raw = tuple(mirror.nextB(3, [4, 1], [4]))
    require(raw == (2, 3, 4) and raw != weak["target"] + (2,),
            "weak-charge raw target changed")
    print("NEGATIVE_CONTROLS PASS source_only=base2_width1 "
          "target_only_nonoverflow=base2_width1 weak_doubled_charge=base3_[4,1]", flush=True)


def lasso_audit():
    from infinite_prefix import fixed_witness
    witness = fixed_witness()
    profile = tuple(tuple(word) for word in witness["profile"])
    stem, loop = witness["stem_length"], witness["loop_length"]
    start = 3 + stem
    require((start, loop) == (39, 20), "this audit classifies the fixed 39+20 lasso")
    maximum = start + 128 * loop
    rows = [[] for _ in range(8)]
    boundaries = [witness["states"][0]]
    cursor = 0
    for _ in range(maximum - 3):
        if cursor == len(witness["columns"]):
            cursor = stem
        column = witness["columns"][cursor]
        for t in range(8):
            rows[t].append(column[t])
        boundaries.append(witness["states"][cursor + 1])
        cursor += 1
    words = tuple(profile[t] + tuple(rows[t]) for t in range(8))
    values = [0] * 8
    power = 1
    charges = []
    for width in range(1, maximum + 1):
        for t in range(8):
            values[t] += words[t][width - 1] * power
        sign = -1 if width % 2 else 1
        charges.append(tuple((value - sign) % 11 for value in values))
        power *= 10
    increments = tuple(alternating(words[t][:start + loop]) - alternating(words[t][:start])
                       for t in range(8))
    require(increments == (11, 44, 11, 44, 11, 44, 11, 44), "loop charge increments changed")
    require(all(value % 11 == 0 for value in increments), "loop does not preserve the residues")
    for width in range(start, maximum + 1):
        representative = start + (width - start) % loop
        require(charges[width - 1] == charges[representative - 1], "integer residue periodicity mismatch")

    periodic = charges[start - 1:start + loop - 1]
    proper_periods = [d for d in (1, 2, 4, 5, 10)
                      if all(periodic[i] == periodic[(i + d) % loop] for i in range(loop))]
    require(not proper_periods, "claimed least residue period is not 20")
    require(all(periodic[(i + 5) % loop] == periodic[i][-2:] + periodic[i][:-2]
                for i in range(loop)), "five-column temporal-rotation compression fails")
    zero_histogram = Counter(sum(value == 0 for value in vector) for vector in periodic)
    require(dict(zero_histogram) == {0: 8, 1: 4, 2: 8}, "periodic charged-phase histogram changed")
    require(all(any(value != 0 for value in vector) for vector in charges),
            "an all-phase charged cut unexpectedly appeared")

    primary = subject.lasso_analysis()
    records = primary["preperiod"] + primary["periodic"]
    require(len(records) == start + loop - 1, "primary finite cutoff coverage is incomplete")
    for width, record in enumerate(records, 1):
        vector = charges[width - 1]
        mask = sum(1 << t for t in range(8) if vector[t])
        require(record["cut"] == width and tuple(record["charges"]) == vector
                and record["failure_mask"] == mask, "primary cutoff record mismatch")
    require(tuple(primary["full_cut_increments"]) == increments, "primary loop increments disagree")
    require(primary["charged_cut_representatives"] == [], "primary charged cutoff classification disagrees")

    rng = random.Random(106220)
    selected = sorted({1, 2, 3, 38, 39, 40, 58, 59, 60, 139, 1000, maximum}
                      | set(rng.sample(range(1, maximum + 1), 64)))
    for width in selected:
        given_words, given_high = subject.cutoff_words(width, witness)
        require(given_words == tuple(word[:width] for word in words), "cutoff coefficient expansion disagrees")
        if width < 3:
            expected_high = tuple((integer_value(10, profile[t][width:][::-1])
                                   + witness["root"][1][t]) // (10 ** (3 - width)) for t in range(8))
        else:
            expected_high = tuple(boundaries[width - 3][1])
        require(given_high == expected_high, "cutoff boundary carry expansion disagrees")
    pre_histogram = Counter(sum(value == 0 for value in vector) for vector in charges[:start - 1])
    print(f"LASSO_INTEGER_RESIDUES cuts=1..{maximum} phase_residues={8 * maximum} "
          f"cutoff_api_checks={len(selected)} PASS", flush=True)
    print(f"LASSO_FINITE_CLASSIFICATION preperiod_zero_histogram={dict(sorted(pre_histogram.items()))} "
          f"periodic_zero_histogram={dict(sorted(zero_histogram.items()))} "
          "least_eventual_period=20 all_phase_charged_cuts=0 PASS", flush=True)
    print(f"LASSO_LOOP_INCREMENTS {increments} mod11=0; "
          "five_column_shift=two_phase_right_rotation PASS", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arithmetic-only", action="store_true")
    args = parser.parse_args()
    arithmetic_audit()
    negative_controls()
    if not args.arithmetic_only:
        lasso_audit()
    print("CHARGE_PREFIX_INDEPENDENT_AUDIT PASSED")
    print("SCOPE: algebraic all-base edge theorem plus finite checks; no center or Lychrel certificate")


if __name__ == "__main__":
    main()
