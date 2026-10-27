#!/usr/bin/env python3
"""Independent integer oracle and positive controls for T1.p24-center-two-lap-B.

The arithmetic evaluates whole positional integers.  It does not import the
mirror's normalizer or transition functions.  The unchanged mirror is loaded
only by selftest, after the independent checks, for a final comparison.

Public interfaces: target_center(laps=2), known_controls(), exterior_step(),
and brute_exterior_cycles().  Coefficients and phases are least significant
first.  All checks use explicit exceptions, including under python -O.
"""

import argparse
import ast
import importlib.util
import itertools
import json
from pathlib import Path
import re
import resource
import sys
import time


REPO = Path(__file__).resolve().parents[2]
TARGET_C0 = (9, 14, 13, 18, 13, 14, 9)
TARGET_E = tuple(map(int, "010100110100101011001011"))
TARGET_G = tuple(map(int, "110001001000110001001000"))
TARGET_V = tuple(map(int, "100001000000100001000000"))
KNOWN_BASES = (2, 4, 8, 11, 16, 17, 26, 32)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def value(base, word):
    """A positional polynomial, allowing coefficients larger than a digit."""
    require(base >= 2, "base must be at least two")
    return sum(coefficient * base ** position
               for position, coefficient in enumerate(word))


def integer_norm(base, word, incoming):
    """Normalize through one whole integer, with no column-carry recurrence."""
    require(incoming in (0, 1), "incoming carry is not a bit")
    require(all(isinstance(q, int) and 0 <= q <= 2 * base - 2 for q in word),
            "coefficient outside the allowed range")
    number = value(base, word) + incoming
    digits = tuple((number // base ** i) % base for i in range(len(word)))
    outgoing = number // base ** len(word)
    require(outgoing in (0, 1), "outgoing carry is not a bit")
    return digits, outgoing


def exterior_raw(base, B):
    """Return (raw next exterior, e, g), assuming the center flips e."""
    require(not B or B[0] != 0, "exterior starts with zero")
    left, e = integer_norm(base, B, 0)
    right, g = integer_norm(base, tuple(reversed(B)), 1 - e)
    if g:
        left += ((base - 1) * (1 - e),)
        right = (1,) + tuple(reversed(right))
    else:
        right = tuple(reversed(right))
    return tuple(x + y for x, y in zip(left, right)), e, g


def center_raw(base, C, e, g):
    """Return raw next center; reject a failed complementary-carry condition."""
    require(g in (0, 1), "overflow is not a bit")
    digits, outgoing = integer_norm(base, C, e)
    require(outgoing == 1 - e, "center does not flip the incoming carry")
    left = digits
    right = tuple(reversed(digits))
    if g:
        neutral_digit = (base - 1) * e
        left += (neutral_digit,)
        right = (neutral_digit,) + right
    return tuple(x + y for x, y in zip(left, right))


def center_trim(base, raw, v):
    require(isinstance(v, int) and 0 <= 2 * v <= len(raw), "invalid center trim")
    if v:
        require(raw[:v] == raw[-v:] == (base - 1,) * v,
                "center trim is not neutral")
        return raw[v:-v]
    return raw


def check_edge(base, edge):
    B, C, B2, C2, u, v = (tuple(x) if i < 4 else x
                          for i, x in enumerate(edge))
    require(isinstance(u, int) and u >= 0, "invalid exterior trim")
    require(isinstance(v, int) and v >= 0, "invalid center trim")
    raw_B, e, g = exterior_raw(base, B)
    raw_C = center_raw(base, C, e, g)
    require(raw_B == B2 + (base - 1,) * u, "exterior equation failed")
    require(raw_C == (base - 1,) * v + C2 + (base - 1,) * v,
            "center equation failed")
    require(len(B2) == len(B) + g - u, "exterior length equation failed")
    require(len(C2) == len(C) + g - 2 * v, "center length equation failed")
    return e, g


def check_cycle(base, edges):
    require(bool(edges), "empty cycle")
    es, gs = [], []
    for i, edge in enumerate(edges):
        e, g = check_edge(base, edge)
        es.append(e)
        gs.append(g)
        successor = edges[(i + 1) % len(edges)]
        require(tuple(edge[2]) == tuple(successor[0]), "exterior cycle does not close")
        require(tuple(edge[3]) == tuple(successor[1]), "center cycle does not close")
    require(sum(edge[4] + edge[5] for edge in edges) >= sum(gs),
            "cycle has insufficient gap gain")
    return tuple(es), tuple(gs)


def reverse_integer(base, number):
    require(number > 0, "integer reversal requires a positive number")
    reverse = 0
    while number:
        number, digit = divmod(number, base)
        reverse = base * reverse + digit
    return reverse


def integer_transition_fixture(base, B, C, gap=3):
    """Check a full template transition by ordinary integer reverse-and-add."""
    raw_B, e, g = exterior_raw(base, B)
    raw_C = center_raw(base, C, e, g)
    require(gap >= g, "gap too short")
    h = base - 1
    before = tuple(B) + (h,) * gap + tuple(C) + (h,) * gap + tuple(reversed(B))
    after = raw_B + (h,) * (gap - g) + raw_C + (h,) * (gap - g) + tuple(reversed(raw_B))
    number = value(base, before)
    require(number + reverse_integer(base, number) == value(base, after),
            "whole-integer reverse-and-add fixture failed")


def target_center(laps=2):
    """The supplied C24 repeated laps times, independently checked on every edge."""
    require(isinstance(laps, int) and 1 <= laps <= 100,
            "laps must be in 1..100")
    es, gs, vs = TARGET_E * laps, TARGET_G * laps, TARGET_V * laps
    C = TARGET_C0
    phases = []
    # These short exteriors realize the four incoming-carry/overflow pairs.
    representatives = {(0, 0): (1,), (0, 1): (9,),
                       (1, 0): (1, 10), (1, 1): (10,)}
    for e, g, v in zip(es, gs, vs):
        require(C == C[::-1] and (len(C) % 2 == 0 or C[len(C) // 2] % 2 == 0),
                "center is not a symmetric folded coefficient word")
        phases.append(C)
        raw = center_raw(10, C, e, g)
        next_C = center_trim(10, raw, v)
        require(len(next_C) == len(C) + g - 2 * v, "target center length law failed")
        B = representatives[e, g]
        raw_B, actual_e, actual_g = exterior_raw(10, B)
        require((actual_e, actual_g) == (e, g), "representative has wrong streams")
        check_edge(10, (B, C, raw_B, next_C, 0, v))
        integer_transition_fixture(10, B, C)
        C = next_C
    require(C == TARGET_C0, "target center does not close")
    require(tuple(phases) == tuple(phases[:24]) * laps, "center laps differ")
    return {"base": 10, "period": len(phases), "C": tuple(phases),
            "e": es, "g": gs, "v": vs}


def load_lean_certificates():
    """Load explicit data, not executable Lean or the Python mirror."""
    paths = (
        REPO / "lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean",
        REPO / "lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean",
    )
    certificates = {}
    for path in paths:
        source = path.read_text()
        definitions = {name: tuple(ast.literal_eval(literal)) for name, literal in
                       re.findall(r"def\s+(\w+)\s*:\s*List Nat\s*:=\s*(\[[^\]]*\])", source)}
        pattern = r"def\s+cert(\d+)\s*:\s*List Edge\s*:=\s*(\[.*?\])\s*\n\n"
        for base_text, body in re.findall(pattern, source, re.S):
            edges = []
            for fields_text in re.findall(r"⟨([^⟩]+)⟩", body):
                fields = re.findall(r"\[[^\]]*\]|\w+", fields_text)
                require(len(fields) == 6, "unexpected Lean edge data")
                words = []
                for field in fields[:4]:
                    words.append(tuple(ast.literal_eval(field)) if field.startswith("[")
                                 else definitions[field])
                edges.append(tuple(words) + (int(fields[4]), int(fields[5])))
            base = int(base_text)
            require(base not in certificates and bool(edges), "duplicate or empty Lean certificate")
            certificates[base] = tuple(edges)
    require(tuple(sorted(certificates)) == KNOWN_BASES, "did not load all eight known bases")
    return certificates


def known_controls():
    """Pad every B phase to its cycle's maximum width, giving constant u=g."""
    controls = []
    for base, original in sorted(load_lean_certificates().items()):
        original_e, original_g = check_cycle(base, original)
        width = max(len(edge[0]) for edge in original)
        edges = []
        for edge, g in zip(original, original_g):
            B, C, B2, C2, u, v = edge
            pad = width - len(B)
            next_pad = width - len(B2)
            require(u + pad - next_pad == g, "constant-width trim identity failed")
            padded_B = B + (base - 1,) * pad
            padded_B2 = B2 + (base - 1,) * next_pad
            new_edge = (padded_B, C, padded_B2, C2, g, v)
            edges.append(new_edge)
            integer_transition_fixture(base, padded_B, C)
        es, gs = check_cycle(base, edges)
        require((es, gs) == (original_e, original_g), "padding changed the streams")
        controls.append({"base": base, "period": len(edges), "width": width,
                         "B": tuple(edge[0] for edge in edges),
                         "C": tuple(edge[1] for edge in edges),
                         "e": es, "g": gs, "u": gs,
                         "v": tuple(edge[5] for edge in edges), "edges": tuple(edges)})
    return tuple(controls)


def exterior_step(base, B):
    """One exact constant-width u=g step, or None if its trim is impossible."""
    raw, e, g = exterior_raw(base, tuple(B))
    if g:
        if raw[-1] != base - 1:
            return None
        successor = raw[:-1]
    else:
        successor = raw
    if successor and successor[0] == 0:
        return None
    require(len(successor) == len(B), "constant-width step changed width")
    return successor, e, g


def brute_exterior_cycles(base, width, period, es=None, gs=None):
    """Exhaust all starts in a tiny finite box; rotations are counted separately.

    Cycles need only have period dividing period.  Optional streams are fixed
    phase by phase.  This is a small oracle, not the production search.
    """
    require(2 <= base <= 4 and 0 <= width <= 4 and 1 <= period <= 12,
            "brute-force controls restricted to base<=4, width<=4, period<=12")
    require(es is None or len(es) == period, "wrong incoming-carry stream length")
    require(gs is None or len(gs) == period, "wrong overflow stream length")
    answer = []
    for B0 in itertools.product(range(2 * base - 1), repeat=width):
        if B0 and B0[0] == 0:
            continue
        B = B0
        phases = []
        for t in range(period):
            step = exterior_step(base, B)
            if step is None:
                break
            successor, e, g = step
            if (es is not None and es[t] != e) or (gs is not None and gs[t] != g):
                break
            phases.append(B)
            B = successor
        if len(phases) == period and B == B0:
            answer.append(tuple(phases))
    return tuple(answer)


def selftest():
    started = time.perf_counter()
    target = target_center(2)
    controls = known_controls()
    mirror_path = REPO / "calculation/neutral_band_search.py"
    spec = importlib.util.spec_from_file_location("a115_unchanged_mirror", mirror_path)
    require(spec is not None and spec.loader is not None, "cannot load unchanged mirror")
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    mirror_edge_count = 0
    for control in controls:
        mutable = [tuple(list(x) if i < 4 else x for i, x in enumerate(edge))
                   for edge in control["edges"]]
        require(mirror.cycleOK(control["base"], mutable, mutable[0][0], mutable[0][1]),
                "mirror rejects padded known positive control")
        mirror_edge_count += len(mutable)
    # The representatives verify isolated center edges, not an exterior cycle.
    reps = {(0, 0): [1], (0, 1): [9], (1, 0): [1, 10], (1, 1): [10]}
    for t, C in enumerate(target["C"]):
        e, g, v = target["e"][t], target["g"][t], target["v"][t]
        B = reps[e, g]
        raw_B, actual_e, actual_g = exterior_raw(10, tuple(B))
        next_C = target["C"][(t + 1) % target["period"]]
        edge = (B, list(C), list(raw_B), list(next_C), 0, v)
        require((actual_e, actual_g) == (e, g) and mirror.edgeOK(10, edge),
                "mirror rejects isolated target center edge")
        mirror_edge_count += 1
    # Exhaust the full coefficient/carry domain at small bases and widths.
    normalization_cases = 0
    for base in (2, 3, 4):
        for width in range(5):
            for word in itertools.product(range(2 * base - 1), repeat=width):
                for incoming in (0, 1):
                    digits, outgoing = integer_norm(base, word, incoming)
                    require((list(digits), outgoing) == mirror.norm(base, word, incoming),
                            "whole-integer and mirror normalizers differ")
                    normalization_cases += 1
    tiny_counts = {}
    for base in (2, 3):
        for width in range(1, 4):
            tiny_counts[f"b{base}_w{width}"] = {
                str(period): len(brute_exterior_cycles(base, width, period))
                for period in range(1, 9)}
    print(json.dumps({"status": "PASS", "center_period": target["period"],
                      "center_lap_period": 24, "center_lengths": [len(C) for C in target["C"][:24]],
                      "center_overflows": sum(target["g"]), "center_trims": sum(target["v"]),
                      "known_controls": [{k: c[k] for k in ("base", "period", "width", "e", "g")}
                                         for c in controls],
                      "integer_transition_fixtures": 48 + sum(c["period"] for c in controls),
                      "mirror_edges": mirror_edge_count,
                      "exhaustive_normalization_cases": normalization_cases,
                      "tiny_exterior_counts": tiny_counts,
                      "wall_seconds": round(time.perf_counter() - started, 6),
                      "max_rss_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                                     // (1024 if sys.platform == "darwin" else 1)},
                     sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="?", choices=("selftest", "target", "controls"),
                        default="selftest")
    parser.add_argument("--laps", type=int, default=2,
                        help="target laps, in 1..100; applies only to target")
    args = parser.parse_args()
    if args.command == "selftest":
        selftest()
    elif args.command == "target":
        print(json.dumps(target_center(args.laps), sort_keys=True))
    else:
        print(json.dumps(known_controls(), sort_keys=True))


if __name__ == "__main__":
    main()
