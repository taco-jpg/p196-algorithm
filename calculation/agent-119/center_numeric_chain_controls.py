#!/usr/bin/env python3
"""Finite controls for signed center trimming and weighted chain arithmetic.

Z(C) = value(C) + 1 - b**len(C).  For an accepted edge, independently compute
e/e2/g by whole-integer quotients and A = b**g*(R_m(value(C)+e)+e*(b**m+1)-b**m).
Check b**v*Z(C2) = Z(C)+A, then the prefix-weighted chain and closed identities.
Empty chains and total trim zero are retained; no quotient by b**V-1 is taken.

The unchanged neutral_band_search mirror supplies acceptance checks.  A local
chain adapter checks all literal B/C seams.  Arithmetic is only a necessary
consequence: explicit wrong-trim, counterfeit-center, and bad-seam controls
are rejected even when their scalar identities hold.  Source Hyp need not
hold at the target.  The decimal P24 fixture is separately labelled CENTER
ONLY, with prescribed e/g and no exterior or full certificate claim.

Only literal fixture data and the pinned base-20 digest are read from Agent112
scripts; none of their arithmetic code is imported or executed.  These finite
controls are not proofs, a numerical cycle-lifting theorem, a driver-only
obstruction, or a new certificate.  Explicit require checks survive python -O.
"""

import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "calculation"))
import neutral_band_search as mirror


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def value(base, word):
    return sum(coefficient * base ** i for i, coefficient in enumerate(word))


def signed(base, center):
    return value(base, center) + 1 - base ** len(center)


def pad(base, amount, center):
    return [max(0, base - 1)] * amount + center + [max(0, base - 1)] * amount


def stream(base, exterior, center):
    e = value(base, exterior) // base ** len(exterior)
    f = (value(base, center) + e) // base ** len(center)
    g = (value(base, exterior[::-1]) + f) // base ** len(exterior)
    return e, f, g


def fixed_reverse(base, width, number):
    """Reverse exactly width low digits, including every zero position."""
    residue, result = number % base ** width, 0
    for _ in range(width):
        residue, digit = divmod(residue, base)
        result = base * result + digit
    require(residue == 0, "Fixed-width reversal left an unconsumed digit")
    return result


def center_data(base, center, e, g):
    width, number = len(center), value(base, center)
    power = base ** width
    digits = [(number + e) // base ** i % base for i in range(width)]
    reversal = fixed_reverse(base, width, number + e)
    require(reversal == value(base, digits[::-1]), "Two fixed-width reversals disagree")
    increment = base ** g * (reversal + e * (power + 1) - power)
    extended = digits + [(base - 1) * e] * g
    raw = [left + right for left, right in zip(extended, extended[::-1])]
    return increment, digits, raw


def numeric_law(base, edge):
    exterior, center, _, target, _, trim = edge
    e, _, g = stream(base, exterior, center)
    increment, _, _ = center_data(base, center, e, g)
    return base ** trim * signed(base, target), signed(base, center) + increment


def chain_ok(base, edges, exterior, center):
    """Adapter of A120Certificate.chainOK; no arithmetic is used for acceptance."""
    for edge in edges:
        if (edge[0], edge[1]) != (exterior, center) or not mirror.edgeOK(base, edge):
            return False
        exterior, center = edge[2:4]
    return True


def weighted_increment(base, terms):
    """Evaluate A0 + b**v0*(A1 + b**v1*(...)) from the end."""
    result = 0
    for trim, increment in reversed(terms):
        result = increment + base ** trim * result
    return result


def divides(divisor, number):
    return number == 0 if divisor == 0 else number % divisor == 0


def literal_data(path, names, function=None):
    body = ast.parse(path.read_text()).body
    if function is not None:
        body = next(node.body for node in body if isinstance(node, ast.FunctionDef) and node.name == function)
    found = {}
    for node in body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in names:
                found[name] = ast.literal_eval(node.value)
    require(set(found) == set(names), f"Missing literal fixture fields: {path.name}")
    return found


def base20_fixture():
    path = ROOT / "calculation/agent-112/check_normalization_arithmetic.py"
    seed = literal_data(path, ("exterior", "center"), "base20_fixture")
    metadata = literal_data(path, ("BASE20_SOURCE",))["BASE20_SOURCE"]
    exterior, center = list(seed["exterior"]), list(seed["center"])
    edges = []
    # Supplied trims of the pinned Agent116 PR356 fixture, not a search.
    for u, v in zip(map(int, "10001000"), map(int, "00000010")):
        require(mirror.hyp(20, exterior, center), "Pinned base-20 source lost Hyp")
        raw_b, raw_c = mirror.nextB(20, exterior, center), mirror.nextC(20, exterior, center)
        target_b = raw_b[:len(raw_b) - u]
        target_c = raw_c[v:len(raw_c) - v]
        edge = (exterior, center, target_b, target_c, u, v)
        require(mirror.edgeOK(20, edge), "Pinned base-20 edge failed")
        edges.append(edge)
        exterior, center = target_b, target_c
    digest = hashlib.sha256(json.dumps(edges, separators=(",", ":")).encode("ascii")).hexdigest()
    require(digest == metadata["canonical_edges_sha256"], "Pinned base-20 source digest changed")
    require(mirror.cycleOK(20, edges, *edges[0][:2]), "Pinned base-20 cycle failed")
    return edges


class Controls:
    def __init__(self):
        self.counts = Counter()

    def edge(self, base, edge, label):
        require(mirror.edgeOK(base, edge), f"edge guard: {label}")
        exterior, center, target_b, target, _, trim = edge
        e, f, g = stream(base, exterior, center)
        require(e in (0, 1) and g in (0, 1) and f == 1 - e, f"Carry-flip hypotheses failed: {label}")
        require((e, f, g) == (mirror.e1(base, exterior), mirror.e2(base, exterior, center),
                              mirror.gam(base, exterior, center)), f"Whole-integer stream differs: {label}")
        increment, digits, raw = center_data(base, center, e, g)
        require(mirror.norm(base, center, e) == (digits, f) and
                raw == mirror.nextC(base, exterior, center), f"Independent raw center differs: {label}")
        require(len(raw) == len(center) + g, f"Raw center width differs: {label}")
        require(signed(base, raw) == signed(base, center) + increment, f"Raw signed identity failed: {label}")
        require(raw == pad(base, trim, target), f"Literal accepted trim failed: {label}")
        require(base ** trim * signed(base, target) == signed(base, center) + increment,
                f"Accepted trimmed signed identity failed: {label}")
        self.counts["edge_controls"] += 1
        self.counts["edge_empty_exterior"] += not exterior
        self.counts["edge_nonsymmetric_center"] += center != center[::-1]
        self.counts["edge_target_hyp_false"] += not mirror.hyp(base, target_b, target)
        self.counts["edge_target_signed_zero"] += signed(base, target) == 0
        self.counts["edge_zero_trim"] += trim == 0
        self.counts["edge_trim_gt_one"] += trim > 1
        self.counts["edge_nonmaximal_trim"] += mirror.trim(base, [], raw)[3] > trim
        self.counts["increment_negative"] += increment < 0
        self.counts["increment_positive"] += increment > 0
        self.counts["increment_zero"] += increment == 0
        return increment

    def chain(self, base, edges, exterior, center, label):
        require(chain_ok(base, edges, exterior, center), f"chain guard: {label}")
        start_z, total_v, weighted, terms = signed(base, center), 0, 0, []
        end_b, end_c = exterior, center
        require(base ** total_v * signed(base, end_c) == start_z + weighted, "Empty prefix identity failed")
        self.counts["prefix_identities"] += 1
        for i, edge in enumerate(edges):
            increment = self.edge(base, edge, (label, i))
            terms.append((edge[5], increment))
            weighted += base ** total_v * increment
            total_v += edge[5]
            end_b, end_c = edge[2:4]
            require(base ** total_v * signed(base, end_c) == start_z + weighted,
                    f"Weighted prefix identity failed: {(label, i)}")
            self.counts["prefix_identities"] += 1
        require(weighted == weighted_increment(base, terms), f"Weighted recursion disagrees: {label}")
        if total_v == 0:
            require(weighted == signed(base, end_c) - start_z, "Zero-trim identity failed")
            self.counts["chain_zero_total_trim"] += 1
            self.counts["chain_zero_trim_open"] += (end_b, end_c) != (exterior, center)
        if end_c == center:
            factor = base ** total_v - 1
            require(weighted == factor * start_z and divides(factor, weighted),
                    f"Closed identity or integer divisibility failed: {label}")
            self.counts["closed_identities"] += 1
            self.counts["closed_zero_factor"] += factor == 0
        self.counts["chain_controls"] += 1
        self.counts["chain_empty_controls"] += not edges
        return total_v, weighted

    def cycle(self, base, edges, label):
        require(bool(edges) and mirror.cycleOK(base, edges, *edges[0][:2]), f"cycle guard: {label}")
        result = self.chain(base, edges, *edges[0][:2], label)
        self.counts["cycle_controls"] += 1
        self.counts["cycle_listed_edges"] += len(edges)
        return result

    def rejected(self, action, guard):
        try:
            action()
        except RuntimeError as error:
            require(str(error).startswith(guard + " guard:"), "Rejected for arithmetic instead of the input guard")
        else:
            raise RuntimeError("A malformed control passed its acceptance guard")
        self.counts[f"rejected_{guard}_guards"] += 1


def padded_edge(base, edge, amount, target_amount):
    exterior, center, target_b, target, u, v = edge
    trim = amount + v - target_amount
    require(min(amount, target_amount, trim) >= 0, "Invalid center padding schedule")
    return exterior, pad(base, amount, center), target_b, pad(base, target_amount, target), u, trim


def padding_controls(checks):
    for base in (1, 2, 3, 10, 20):
        neutral = base - 1
        words = {(), (0,), (neutral,), (neutral, neutral), (0, neutral),
                 (2 * neutral, 0), (neutral, 2 * neutral, neutral), (2 * neutral + 1,)}
        for word in sorted(words):
            for amount in (0, 1, 2, 4):
                require(signed(base, pad(base, amount, list(word))) == base ** amount * signed(base, word),
                        "Unrestricted positive-base padding identity failed")
                checks.counts["padding_controls"] += 1
                checks.counts["padding_base_one"] += base == 1
    require(signed(0, pad(0, 1, [])) == 1 and 0 ** 1 * signed(0, []) == 0,
            "Base-zero padding counterexample changed")
    checks.counts["boundary_base_zero_padding"] += 1
    require(fixed_reverse(10, 3, 12) == fixed_reverse(10, 3, 1012) == 210,
            "Prescribed-width reversal lost a zero position or failed to reduce modulo the width")


def certificate_controls(checks, controls):
    for base, edges in controls:
        checks.counts["fixture_bases"] += 1
        checks.counts["fixture_edges"] += len(edges)
        checks.cycle(base, edges, ("original", base))
        for amount in (1, 3):
            checks.cycle(base, [padded_edge(base, edge, amount, amount) for edge in edges],
                         ("uniform", base, amount))
        gain_index = next(i for i, edge in enumerate(edges) if edge[5] > 0)
        for floor in (0, 2):
            phases = [floor] * len(edges)
            phases[(gain_index + 1) % len(edges)] += 1
            padded = [padded_edge(base, edge, phases[i], phases[(i + 1) % len(edges)])
                      for i, edge in enumerate(edges)]
            checks.cycle(base, padded, ("phase", base, floor))
            checks.counts["cycle_phase_dependent"] += 1
        padded, amount = [], 2
        for i, edge in enumerate(edges * 3):
            target_amount = 0 if i == 0 else min(2, amount + edge[5])
            padded.append(padded_edge(base, edge, amount, target_amount))
            amount = target_amount
        require(amount == 2 and padded[0][5] > 1, "Large-trim phase control did not close")
        checks.cycle(base, padded, ("three-copies", base))
        checks.counts["cycle_phase_dependent"] += 1
        for length in (0, 1, len(edges) - 1):
            checks.chain(base, edges[:length], *edges[0][:2], ("prefix", base, length))


def directed_controls(checks, controls):
    sources = ((2, [], [2]), (2, [], [0, 2]), (2, [2], [0, 1]),
               (3, [3], [0, 2]), (10, [], [0, 10]), (10, [10], [0, 9]),
               (2, [1, 0], [1, 2]), (3, [], [2, 4]), (10, [1], [10]),
               (10, [1], [11]), (10, [1], [0, 10, 10, 18]))
    for base, exterior, center in sources:
        seed = mirror.step(base, exterior, center)
        require(seed is not None, "Directed source lost Hyp")
        checks.chain(base, [seed], exterior, center, ("directed", base, seed))
        for amount in (0, 1, 3):
            for target_amount in range(amount + seed[5] + 1):
                checks.edge(base, padded_edge(base, seed, amount, target_amount),
                            ("directed-padding", base, amount, target_amount))
                checks.counts["directed_edge_controls"] += 1
    original = next(edges for base, edges in controls if base == 2)
    exterior, center = original[0][:2]
    untrimmed = []
    for _ in range(8):
        step = mirror.step(2, exterior, center)
        require(step is not None, "Untrimmed zero-V chain lost Hyp")
        raw_center = mirror.nextC(2, exterior, center)
        edge = exterior, center, step[2], raw_center, step[4], 0
        untrimmed.append(edge)
        exterior, center = edge[2:4]
    total_v, weighted = checks.chain(2, untrimmed, *untrimmed[0][:2], "nonempty-zero-V")
    require(total_v == 0 and weighted != 0, "Zero-V open chain must have a nonzero increment")
    for base in (0, 1, 2, 10):
        for center in ([], [0], [1, 0]):
            require(checks.chain(base, [], [], center, ("empty", base, center)) == (0, 0),
                    "Empty chain changed zero total trim or weighted increment")


def boundary_controls(checks, controls):
    edges = next(edges for base, edges in controls if base == 2)
    bad_u = edges[0][:4] + (edges[0][4] + 1, edges[0][5])
    bad_v_zero = ([1, 0], [1, 2], [2], [], 1, 2)
    bad_scalar = ([1], [0, 10, 10, 18], [3], [11, 0], 0, 1)
    for base, bad, name in ((2, bad_u, "wrong-u"), (2, bad_v_zero, "wrong-v-zero-target"),
                            (10, bad_scalar, "same-width-value-counterfeit")):
        left, right = numeric_law(base, bad)
        require(left == right and not mirror.edgeOK(base, bad), "Scalar insufficiency witness failed")
        checks.rejected(lambda b=base, edge=bad: checks.edge(b, edge, name), "edge")
        checks.counts["boundary_scalar_false_positives"] += 1
    good_scalar = ([1], [0, 10, 10, 18], [3], [1, 1], 0, 1)
    checks.edge(10, good_scalar, "genuine-same-value-target")
    require(value(10, bad_scalar[3]) == value(10, good_scalar[3]) == 11 and
            len(bad_scalar[3]) == len(good_scalar[3]) == 2, "Scalar counterfeit changed its width/value")
    bad_v = edges[0][:5] + (edges[0][5] + 1,)
    require(numeric_law(2, bad_v)[0] != numeric_law(2, bad_v)[1], "Wrong nonzero-target trim should fail arithmetic")
    invalids = ((2, bad_v), (0, edges[0]), (1, edges[0]),
                (10, ([1], [0], [2], [0], 0, 0)),
                (2, ([0] + edges[0][0],) + edges[0][1:]))
    for base, bad in invalids:
        checks.rejected(lambda b=base, edge=bad: checks.edge(b, edge, "invalid-input"), "edge")
    first = edges[0]
    exterior_bad = (first[0] + [1], first[1], first[2] + [1], first[3], first[4], first[5])
    malformed = [exterior_bad] + edges[1:]
    require(all(mirror.edgeOK(2, edge) for edge in malformed), "Malformed seam must have valid local edges")
    terms = [(edge[5], center_data(2, edge[1], *stream(2, *edge[:2])[::2])[0]) for edge in malformed]
    total_v = sum(trim for trim, _ in terms)
    weighted = weighted_increment(2, terms)
    require(weighted == (2 ** total_v - 1) * signed(2, malformed[0][1]),
            "Malformed exterior seam should retain the closed center arithmetic identity")
    center_bad = [padded_edge(2, first, 1, 1)] + edges[1:]
    for bad_chain in (malformed, center_bad):
        require(all(mirror.edgeOK(2, edge) for edge in bad_chain), "Bad-seam edge became locally invalid")
        checks.rejected(lambda es=bad_chain: checks.chain(2, es, *es[0][:2], "bad-seam"), "chain")
        checks.rejected(lambda es=bad_chain: checks.cycle(2, es, "bad-seam"), "cycle")
    checks.counts["boundary_closed_scalar_bad_seam"] += 1
    actual = [mirror.step(10, [1], center) for center in ([10], [11])]
    require(all(edge is not None and mirror.edgeOK(10, edge) for edge in actual), "Driver comparison requires accepted edges")
    drivers = [(stream(10, *edge[:2])[0], stream(10, *edge[:2])[2], edge[5]) for edge in actual]
    increments = [center_data(10, edge[1], drivers[i][0], drivers[i][1])[0] for i, edge in enumerate(actual)]
    require(drivers == [(0, 0, 0), (0, 0, 0)] and increments == [-10, -9], "Driver-only scope witness failed")
    checks.counts["boundary_same_driver_distinct_increment"] += 1


def p24_center_only(checks):
    path = ROOT / "calculation/agent-112/check_raw_center_numeric.py"
    data = literal_data(path, ("initial", "carry_word", "overflow_word", "trim_word"), "decimal_center_only")
    require(len(data["carry_word"]) == len(data["overflow_word"]) == len(data["trim_word"]) == 24,
            "Supplied P24 stream length changed")
    initial, center, total_v, weighted, terms = data["initial"], data["initial"][:], 0, 0, []
    for e, g, v in zip(map(int, data["carry_word"]), map(int, data["overflow_word"]), map(int, data["trim_word"])):
        increment, digits, raw = center_data(10, center, e, g)
        require(mirror.norm(10, center, e) == (digits, 1 - e), "Prescribed center-only source does not flip")
        column_digits, _ = mirror.norm(10, center, e)
        column_digits += [9 * e] * g
        require(raw == [x + y for x, y in zip(column_digits, column_digits[::-1])], "Center-only raw comparison failed")
        target = raw[v:len(raw) - v]
        require(raw == pad(10, v, target) and 10 ** v * signed(10, target) == signed(10, center) + increment,
                "Supplied center-only trim identity failed")
        terms.append((v, increment))
        weighted += 10 ** total_v * increment
        total_v += v
        require(10 ** total_v * signed(10, target) == signed(10, initial) + weighted,
                "Supplied center-only prefix identity failed")
        center = target
        checks.counts["p24_center_only_steps"] += 1
    factor = 10 ** total_v - 1
    require(center == initial and weighted == weighted_increment(10, terms) == factor * signed(10, initial)
            and divides(factor, weighted), "Supplied center-only closed arithmetic identity failed")
    checks.counts["p24_total_trim"] = total_v
    return f"CENTER_ONLY_P24 base=10 steps=24 totalV={total_v} Z0={signed(10, initial)} weighted={weighted} full_BC_claim=False"


def main():
    controls = mirror._lean_certs()
    require(len(controls) == 8 and {base for base, _ in controls} == {2, 4, 8, 11, 16, 17, 26, 32},
            "Expected the eight existing Lean-source certificates")
    controls.append((20, base20_fixture()))
    checks = Controls()
    padding_controls(checks)
    certificate_controls(checks, controls)
    directed_controls(checks, controls)
    boundary_controls(checks, controls)
    p24 = p24_center_only(checks)
    for key in ("padding_base_one", "edge_empty_exterior", "edge_nonsymmetric_center", "edge_target_hyp_false",
                "edge_target_signed_zero", "edge_zero_trim", "edge_trim_gt_one", "edge_nonmaximal_trim",
                "increment_negative", "increment_positive", "chain_zero_trim_open", "chain_empty_controls",
                "closed_zero_factor", "rejected_edge_guards", "rejected_chain_guards", "rejected_cycle_guards"):
        require(checks.counts[key] > 0, f"Missing required finite coverage: {key}")
    print("CENTER NUMERIC CHAIN FINITE CONTROLS PASS (not a mathematical proof)")
    for prefix in ("fixture_", "padding_", "edge_", "increment_", "chain_", "prefix_", "closed_", "cycle_",
                   "directed_", "rejected_", "boundary_", "p24_"):
        print(" ".join(f"{key}={checks.counts[key]}" for key in sorted(checks.counts) if key.startswith(prefix)))
    print("SCALAR_COUNTERFEIT base=10 good_C2=[1,1] bad_C2=[11,0] width=2 value=11 v=1 Z0=9101 A=-9981 lhs=rhs=-880 bad_edgeOK=False")
    print("WRONG_TRIM_ZERO_TARGET base=2 original_v=1 bad_v=2 lhs=rhs=0 bad_edgeOK=False")
    print("CLOSED_CENTER_SCALAR_BAD_SEAM base=2 locally_accepted_edges=4 closed_identity=True chainOK=False cycleOK=False")
    print("SAME_DRIVER_DISTINCT_INCREMENT base=10 B=[1] centers=[10],[11] e=0 g=0 v=0 increments=-10,-9")
    print(p24)


if __name__ == "__main__":
    main()
