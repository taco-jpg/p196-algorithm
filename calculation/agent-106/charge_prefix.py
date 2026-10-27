#!/usr/bin/env python3
"""Strong alternating charge completes an exact free-prefix B edge.

For fixed positive width n, put R(B)=alt(B)-(-1)^n modulo b+1. Given
an exact free-prefix edge B -> B', if R(B)=0, then R(B')=0 exactly when
the incoming high carry is complementary and the omitted overflow digit
is neutral. This certifies an autonomous exterior edge, not a center or
a full Lychrel certificate. Odd bases require the full strong residue.

    python3 calculation/agent-106/charge_prefix.py
    python3 -O calculation/agent-106/charge_prefix.py --lasso-json

The arithmetic core is independent. Existing main-branch certificate data
are read for positive controls. The optional lasso application uses the
separate fixed-witness artifact infinite_prefix.py in this directory.
"""

import argparse
from collections import Counter
from itertools import product
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _base(base):
    require(type(base) is int and base >= 2, "base must be an integer >= 2")


def _word(base, word, nonempty=False):
    _base(base)
    require(isinstance(word, (tuple, list)), "word must be a finite tuple/list")
    require(not nonempty or len(word) > 0, "prefix width must be positive")
    require(all(type(x) is int and 0 <= x <= 2 * (base - 1) for x in word),
            "coefficient outside 0..2*(base-1)")
    return tuple(word)


def normalize(base, word, incoming):
    word = _word(base, word)
    require(type(incoming) is int and incoming in (0, 1), "incoming carry must be a bit")
    digits = []
    for coefficient in word:
        incoming, digit = divmod(coefficient + incoming, base)
        digits.append(digit)
    return tuple(digits), incoming


def alt(word):
    return sum(coefficient if i % 2 == 0 else -coefficient
               for i, coefficient in enumerate(word))


def charge(base, word):
    word = _word(base, word)
    return (alt(word) - (-1) ** len(word)) % (base + 1)


def edge_data(base, word, inward):
    word = _word(base, word, nonempty=True)
    require(type(inward) is int and inward in (0, 1), "inward carry must be a bit")
    low, outgoing = normalize(base, word, 0)
    reverse_digits, overflow = normalize(base, word[::-1], inward)
    high = reverse_digits[::-1]
    if overflow == 0:
        target = tuple(low[i] + high[i] for i in range(len(word)))
    else:
        target = (low[0] + 1,) + tuple(low[i] + high[i - 1]
                                      for i in range(1, len(word)))
    r_top = reverse_digits[0]
    closed = inward + outgoing == 1 and (overflow == 0 or r_top == (base - 1) * outgoing)
    return {"source": word, "target": target, "e": outgoing, "h": inward,
            "g": overflow, "r_top": r_top,
            "source_charge": charge(base, word), "target_charge": charge(base, target),
            "terminal_closed": closed}


def prefix_step(base, word, inward):
    edge = edge_data(base, word, inward)
    return edge["target"], edge["g"]


def autonomous_raw(base, word):
    """Untrimmed A120 B arithmetic, with complementary entry forced."""
    word = _word(base, word)
    low, outgoing = normalize(base, word, 0)
    reverse_digits, overflow = normalize(base, word[::-1], 1 - outgoing)
    high = reverse_digits[::-1]
    if overflow:
        low = low + ((base - 1) * (1 - outgoing),)
        high = (1,) + high
    return tuple(low[i] + high[i] for i in range(len(low))), outgoing, overflow


def audit_edge(base, word, inward):
    edge = edge_data(base, word, inward)
    source, target = edge["source"], edge["target"]
    e, h, g, d = edge["e"], edge["h"], edge["g"], edge["r_top"]
    sign, modulus = (-1) ** len(source), base + 1
    predicted = 2 * alt(source) - sign * (e + h) if g == 0 else sign * (h - e - d)
    require((alt(target) - predicted) % modulus == 0, "free-prefix residue identity failed")
    if edge["source_charge"] == 0:
        require((edge["target_charge"] == 0) == edge["terminal_closed"],
                "charged-source boundary equivalence failed")
    if g == 1:
        require((edge["target_charge"] == 0) == edge["terminal_closed"],
                "overflow target-only boundary equivalence failed")
        if edge["target_charge"] == 0:
            require(source[-1] == base - 1, "overflow charged target lacks neutral source end")
    if edge["terminal_closed"]:
        raw, actual_e, actual_g = autonomous_raw(base, source)
        require((actual_e, actual_g) == (e, g), "restored autonomous carries disagree")
        require(raw == target + (base - 1,) * g, "restored autonomous edge equation failed")
    return edge


def verify_fixed_width_cycle(base, words, high_inputs):
    """Verify a charged free-prefix cycle and return its exact B-only data."""
    require(isinstance(words, (tuple, list)) and len(words) > 0, "cycle must be nonempty")
    require(isinstance(high_inputs, (tuple, list)) and len(high_inputs) == len(words),
            "one high input is required per phase")
    phases = tuple(_word(base, word, nonempty=True) for word in words)
    width = len(phases[0])
    require(all(len(word) == width and word[0] > 0 for word in phases),
            "cycle needs a common positive width and nonzero heads")
    require(all(charge(base, word) == 0 for word in phases), "cycle has a nonzero strong charge")
    edges = []
    for t in range(len(phases)):
        edge = audit_edge(base, phases[t], high_inputs[t])
        require(edge["target"] == phases[(t + 1) % len(phases)], "prefix cycle does not close")
        require(edge["terminal_closed"], "cycle edge lacks terminal closure")
        edges.append(edge)
    total = sum(edge["g"] for edge in edges)
    require(total > 0, "positive-head exterior cycle cannot have zero overflows")
    return {"base": base, "B": phases, "e": tuple(edge["e"] for edge in edges),
            "g": tuple(edge["g"] for edge in edges),
            "u": tuple(edge["g"] for edge in edges), "width": width,
            "total_overflows": total, "scope": "B-only; no center certificate"}


def cutoff_words(width, witness=None):
    """Eight coefficient prefixes and their supplied inward carries at a cut."""
    require(type(width) is int and width >= 1, "cutoff must be a positive integer")
    if witness is None:
        from infinite_prefix import fixed_witness
        witness = fixed_witness()
    from infinite_prefix import verify_labels
    verify_labels(witness)
    profile = tuple(tuple(word) for word in witness["profile"])
    if width < 3:
        incoming = tuple(normalize(10, profile[t][width:][::-1], witness["root"][1][t])[1]
                         for t in range(8))
        return tuple(word[:width] for word in profile), incoming
    extra = width - 3
    stem, period = witness["stem_length"], witness["loop_length"]
    if extra <= stem:
        columns = witness["columns"][:extra]
        boundary = witness["states"][extra]
    else:
        repetitions, remainder = divmod(extra - stem, period)
        loop = witness["columns"][stem:]
        columns = witness["columns"][:stem] + loop * repetitions + loop[:remainder]
        boundary = witness["states"][stem + remainder]
    words = tuple(profile[t] + tuple(column[t] for column in columns) for t in range(8))
    require(all(len(word) == width for word in words), "lasso cutoff width mismatch")
    return words, tuple(boundary[1])


def lasso_analysis():
    from infinite_prefix import fixed_witness
    witness = fixed_witness()
    start = 3 + witness["stem_length"]
    period = witness["loop_length"]
    require(period % 2 == 0, "this application uses an even spatial loop")
    loop = witness["columns"][witness["stem_length"]:]
    loop_alt = tuple(alt(tuple(column[t] for column in loop)) for t in range(8))
    increments = tuple((-1) ** start * value for value in loop_alt)
    residues = tuple(value % 11 for value in increments)
    # Full cut state and parity repeat. The explicit loop sum completes the
    # residue proof; sampling alone is not used to infer infinite repetition.
    require(all(value == 0 for value in residues), "lasso needs the longer 220-column residue period")
    records = []
    closed_cuts = []
    for width in range(1, start + period):
        words, high = cutoff_words(width, witness)
        charges = tuple(charge(10, word) for word in words)
        edges = [audit_edge(10, words[t], high[t]) for t in range(8)]
        require(all(edges[t]["target"] == words[(t + 1) % 8] and edges[t]["g"] == t % 2
                    for t in range(8)), "lasso free-prefix transition mismatch")
        fail_mask = sum(1 << t for t in range(8) if charges[t] != 0)
        records.append({"cut": width, "charges": charges, "failure_mask": fail_mask,
                        "failed_phases": tuple(t for t in range(8) if charges[t] != 0)})
        if fail_mask == 0:
            closed_cuts.append(verify_fixed_width_cycle(10, words, high))
    periodic = records[start - 1:]
    require(len(periodic) == period, "periodic cutoff table incomplete")
    return {"spatial_preperiod": start, "spatial_period": period,
            "loop_alternating_sums": loop_alt, "full_cut_increments": increments,
            "increment_mod11": residues, "residue_period_divides": period,
            "preperiod": records[:start - 1], "periodic": periodic,
            "failure_count_histogram_periodic": dict(sorted(Counter(len(x["failed_phases"])
                                                                     for x in periodic).items())),
            "charged_cut_representatives": [x["cut"] for x in records if x["failure_mask"] == 0],
            "B_only_cycles_if_any": closed_cuts}


def exhaustive_controls():
    counts = Counter()
    for base in range(2, 17):
        for width in range(1, 4):
            for word in product(range(2 * base - 1), repeat=width):
                counts["words"] += 1
                for high in (0, 1):
                    edge = audit_edge(base, word, high)
                    counts["edges"] += 1
                    counts["charged_source_edges"] += edge["source_charge"] == 0
                    counts["charged_target_edges"] += edge["target_charge"] == 0
                    counts["terminal_closed_edges"] += edge["terminal_closed"]
                    counts["overflow_edges"] += edge["g"]
    # In odd bases, zero doubled charge must not replace the strong residue.
    edge = audit_edge(3, (4, 1), 0)
    doubled = lambda word: (2 * alt(word) + 2 * (-1) ** len(word)) % 4
    require(doubled(edge["source"]) == doubled(edge["target"]) == 0,
            "weak-charge counterexample changed")
    require(edge["source_charge"] == edge["target_charge"] == 2 and
            not edge["terminal_closed"], "weak-charge counterexample does not fail closure")
    counts["odd_base_weak_charge_counterexamples"] = 1
    return dict(sorted(counts.items()))


def known_cycle_controls():
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root / "calculation"))
    import neutral_band_search as mirror
    cases = []
    for base, original in mirror._lean_certs():
        require(mirror.cycleOK(base, original, original[0][0], original[0][1]),
                "existing certificate fixture fails unchanged mirror")
        width = max(len(edge[0]) for edge in original) + 2
        words = tuple(tuple(edge[0]) + (base - 1,) * (width - len(edge[0])) for edge in original)
        high = tuple(1 - normalize(base, word, 0)[1] for word in words)
        result = verify_fixed_width_cycle(base, words, high)
        cases.append({"base": base, "edges": len(words), "padded_width": width,
                      "overflows": result["total_overflows"]})
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lasso-json", action="store_true")
    parser.add_argument("--lasso-only", action="store_true")
    args = parser.parse_args()
    if not args.lasso_only:
        print("EXHAUSTIVE_CONTROLS " + json.dumps(exhaustive_controls(), sort_keys=True), flush=True)
        cases = known_cycle_controls()
        print("KNOWN_B_CYCLE_CONTROLS " + json.dumps(cases, separators=(",", ":")), flush=True)
    result = lasso_analysis()
    print("LASSO_CHARGE_CLASSIFICATION " + json.dumps({key: result[key] for key in
          ("spatial_preperiod", "spatial_period", "full_cut_increments", "increment_mod11",
           "residue_period_divides", "failure_count_histogram_periodic", "charged_cut_representatives")},
          separators=(",", ":")), flush=True)
    print("FINITE_PREFIX_FAILURE_MASKS " + str([x["failure_mask"] for x in result["preperiod"]]), flush=True)
    print("PERIODIC_FAILURE_MASKS " + str([x["failure_mask"] for x in result["periodic"]]), flush=True)
    if args.lasso_json:
        print(json.dumps(result, separators=(",", ":")), flush=True)
    print("CHARGE_PREFIX_CHECK PASSED", flush=True)


if __name__ == "__main__":
    main()
