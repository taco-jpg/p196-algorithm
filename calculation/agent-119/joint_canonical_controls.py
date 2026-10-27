#!/usr/bin/env python3
"""Finite controls for joint exterior/center canonicalization of A120 edges.

Compose maximal neutral exterior-suffix stripping with maximal neutral center-
pair stripping.  Both trims are recomputed from actual raw successors.  The
unchanged neutral_band_search mirror checks accepted edges and complete cycles;
a local adapter supplies its missing chainOK entry point.  Integer division of
whole coefficient-word values independently checks the raw carry computation.

All preservation, commutation, deterministic-successor, and retraction controls
are conditional on accepted input.  Targets need not satisfy Hyp.  Malformed
seams and trims can be repaired, so there is no arbitrary-input acceptance iff.
An additional, explicitly separate Nat-arithmetic witness refutes unrestricted
idempotence: outside Hyp, the Python mirror's signed subtraction can differ
from Lean's Nat subtraction.  Formula/mirror agreement is asserted only on
accepted sources.  These are finite controls, not proofs or new certificates.
Run with Python 3, normally or with -O; explicit require checks stay active.
"""

from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror


KNOWN_BASES = {2, 4, 8, 11, 16, 17, 26, 32}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def suffix_pad(base, amount, word):
    return word + [max(0, base - 1)] * amount


def center_pad(base, amount, word):
    return [max(0, base - 1)] * amount + suffix_pad(base, amount, word)


def strip_suffix(base, word):
    end = len(word)
    while end and word[end - 1] == max(0, base - 1):
        end -= 1
    return word[:end], len(word) - end


def strip_center(base, word):
    start, end = 0, len(word)
    while end - start >= 2 and word[start] == word[end - 1] == max(0, base - 1):
        start += 1
        end -= 1
    return word[start:end], start


def strip_oracle(base, word):
    neutral = max(0, base - 1)
    leading = next((i for i, value in enumerate(word) if value != neutral), len(word))
    trailing = next((i for i, value in enumerate(reversed(word)) if value != neutral), len(word))
    paired = min(leading, trailing, len(word) // 2)
    return (word[:len(word) - trailing], trailing), (word[paired:len(word) - paired], paired)


def canonical_state(base, exterior, center):
    core_b, depth_b = strip_suffix(base, exterior)
    core_c, depth_c = strip_center(base, center)
    return core_b, core_c, depth_b, depth_c


def mirror_raw(base, exterior, center):
    return (mirror.nextB(base, exterior, center), mirror.nextC(base, exterior, center),
            (mirror.e1(base, exterior), mirror.e2(base, exterior, center),
             mirror.gam(base, exterior, center)))


def integer_norm(base, word, carry):
    value = carry + sum(coefficient * base ** i for i, coefficient in enumerate(word))
    return [value // base ** i % base for i in range(len(word))], value // base ** len(word)


def integer_raw(base, exterior, center):
    """Raw formulas using whole-word integer division and exact Nat subtraction."""
    require(base >= 2, "The integer raw control requires a valid base")
    db, e1 = integer_norm(base, exterior, 0)
    dc, e2 = integer_norm(base, center, e1)
    dr, gamma = integer_norm(base, exterior[::-1], e2)
    if gamma == 0:
        raw_b = [db[i] + dr[len(dr) - 1 - i] for i in range(len(db))]
        raw_c = [dc[i] + dc[len(dc) - 1 - i] for i in range(len(dc))]
    else:
        x, y = (base - 1) * max(0, 1 - e1), (base - 1) * max(0, 1 - e2)
        raw_b = [p + q for p, q in zip(db + [x], [1] + dr[::-1])]
        raw_c = [p + q for p, q in zip(dc + [y], [y] + dc[::-1])]
    return raw_b, raw_c, (e1, e2, gamma)


def exterior_normalize(base, edge, raw=mirror_raw):
    exterior, center, target_b, target_c, _, v = edge
    core_b, _ = strip_suffix(base, exterior)
    target_core, _ = strip_suffix(base, target_b)
    _, new_u = strip_suffix(base, raw(base, core_b, center)[0])
    return core_b, center, target_core, target_c, new_u, v


def center_normalize(base, edge, raw=mirror_raw):
    exterior, center, target_b, target_c, u, _ = edge
    core_c, _ = strip_center(base, center)
    target_core, _ = strip_center(base, target_c)
    _, new_v = strip_center(base, raw(base, exterior, core_c)[1])
    return exterior, core_c, target_b, target_core, u, new_v


def joint_normalize(base, edge, raw=mirror_raw):
    return center_normalize(base, exterior_normalize(base, edge, raw), raw)


def padded_edge(base, edge, source_depths, target_depths):
    exterior, center, target_b, target_c, u, v = edge
    a, c = source_depths
    a2, c2 = target_depths
    new_u, new_v = u + a - a2, v + c - c2
    require(min(a, c, a2, c2, new_u, new_v) >= 0, "Unbalanced natural padding schedule")
    return (suffix_pad(base, a, exterior), center_pad(base, c, center),
            suffix_pad(base, a2, target_b), center_pad(base, c2, target_c), new_u, new_v)


def chain_ok(base, edges, exterior, center):
    """A120Certificate.chainOK adapter, using the unchanged mirror.edgeOK."""
    for edge in edges:
        if (edge[0], edge[1]) != (exterior, center) or not mirror.edgeOK(base, edge):
            return False
        exterior, center = edge[2:4]
    return True


def freeze(edge):
    return tuple(tuple(word) for word in edge[:4]) + tuple(edge[4:])


def totals(base, edges):
    return (sum(mirror.gam(base, edge[0], edge[1]) for edge in edges),
            sum(edge[4] for edge in edges), sum(edge[5] for edge in edges),
            sum(edge[4] + edge[5] for edge in edges))


def template(base, exterior, center, gap):
    return exterior + [base - 1] * gap + center + [base - 1] * gap + exterior[::-1]


class Controls:
    def __init__(self):
        self.counts = Counter()
        self.examples = defaultdict(dict)

    def edge(self, base, edge, label):
        require(mirror.edgeOK(base, edge), f"Expected an accepted edge: {label}")
        exterior, center, target_b, target_c, u, v = edge
        core_b, core_c, a, c = canonical_state(base, exterior, center)
        end_b, end_c, a2, c2 = canonical_state(base, target_b, target_c)
        exterior_first = exterior_normalize(base, edge)
        center_first = center_normalize(base, edge)
        normalized = center_normalize(base, exterior_first)
        require(normalized == exterior_normalize(base, center_first),
                f"Accepted normalizations do not commute: {label}")
        require(all(mirror.edgeOK(base, item) for item in (exterior_first, center_first, normalized)),
                f"Normalization lost acceptance: {label}")
        raw_b, raw_c, stream = integer_raw(base, core_b, core_c)
        next_b, actual_u = strip_oracle(base, raw_b)[0]
        next_c, actual_v = strip_oracle(base, raw_c)[1]
        expected = (core_b, core_c, next_b, next_c, actual_u, actual_v)
        require(normalized == expected == mirror.step(base, core_b, core_c),
                f"Canonical edge is not the unique computed successor: {label}")
        require((next_b, next_c) == (end_b, end_c), f"Canonical target differs: {label}")
        require(integer_raw(base, exterior, center) == mirror_raw(base, exterior, center) and
                (raw_b, raw_c, stream) == mirror_raw(base, core_b, core_c),
                f"Integer raw formula differs from mirror on an accepted source: {label}")
        require(stream == mirror_raw(base, exterior, center)[2], f"Carry/overflow stream changed: {label}")
        require(a + actual_u == u + a2 and c + actual_v == v + c2,
                f"Exterior or center depth balance failed: {label}")
        require(padded_edge(base, normalized, (a, c), (a2, c2)) == edge,
                f"Canonical edge did not reconstruct its accepted input: {label}")
        require(joint_normalize(base, normalized) == normalized, f"Accepted idempotence failed: {label}")
        fixed = a == c == a2 == c2 == 0
        require((normalized == edge) == fixed, f"Retraction on fully stripped edges failed: {label}")
        require(mirror.hyp(base, core_b, core_c), f"Canonical source lost Hyp: {label}")
        target_hyp = mirror.hyp(base, target_b, target_c)
        require(mirror.hyp(base, end_b, end_c) == target_hyp, f"Target Hyp Boolean changed: {label}")
        require(len(target_b) + u == len(exterior) + stream[2] and
                len(target_c) + 2 * v == len(center) + stream[2],
                f"Accepted edge length accounting failed: {label}")
        for old_b, old_c, new_b, new_c, db, dc in (
                (exterior, center, core_b, core_c, a, c),
                (target_b, target_c, end_b, end_c, a2, c2)):
            require(len(new_b) <= len(old_b) and len(new_c) <= len(old_c),
                    f"A component width increased: {label}")
            require(2 * len(new_b) + len(new_c) + 2 * (db + dc) ==
                    2 * len(old_b) + len(old_c), f"Interface width balance failed: {label}")
            for gap in (0, 2):
                require(template(base, old_b, old_c, gap) ==
                        template(base, new_b, new_c, gap + db + dc),
                        f"Literal template reconstruction failed: {label}")
                self.counts["template_controls"] += 1
        raw_original_b, raw_original_c, _ = mirror_raw(base, exterior, center)
        self.counts["edge_controls"] += 1
        self.counts["edge_fixed_retractions"] += fixed
        self.counts["edge_nonfixed_inputs"] += not fixed
        self.counts["edge_empty_exterior"] += not exterior
        self.counts["edge_nonsymmetric_center"] += center != center[::-1]
        self.counts["edge_target_hyp_false"] += not target_hyp
        self.counts["edge_nonmaximal_u"] += u < strip_suffix(base, raw_original_b)[1]
        self.counts["edge_nonmaximal_v"] += v < strip_center(base, raw_original_c)[1]
        self.counts["edge_u_changed"] += u != actual_u
        self.counts["edge_v_changed"] += v != actual_v
        self.counts["integer_raw_controls"] += 2
        key = (tuple(core_b), tuple(core_c))
        examples = self.examples[base].setdefault(key, [])
        if examples:
            require(normalized == examples[0][1], f"Equal canonical sources disagree: {label}")
            self.counts["same_source_repeat_controls"] += 1
        if len(examples) < 2 and all(freeze(edge) != freeze(old) for old, _ in examples):
            examples.append((edge, normalized))
        return normalized

    def chain(self, base, edges, exterior, center, label):
        require(chain_ok(base, edges, exterior, center), f"Expected an accepted chain: {label}")
        normalized = [self.edge(base, edge, (label, i)) for i, edge in enumerate(edges)]
        core_b, core_c, a, c = canonical_state(base, exterior, center)
        require(chain_ok(base, normalized, core_b, core_c), f"Normalized chain failed: {label}")
        end_b, end_c = edges[-1][2:4] if edges else (exterior, center)
        final_b, final_c, a2, c2 = canonical_state(base, end_b, end_c)
        require((normalized[-1][2:4] if normalized else (core_b, core_c)) == (final_b, final_c),
                f"Canonical chain endpoint differs: {label}")
        old_g, old_u, old_v, old_gain = totals(base, edges)
        new_g, new_u, new_v, new_gain = totals(base, normalized)
        require(new_g == old_g and new_u + a == old_u + a2 and new_v + c == old_v + c2 and
                new_gain + a + c == old_gain + a2 + c2, f"Chain telescope failed: {label}")
        require(len(normalized) == len(edges) and
                [mirror_raw(base, edge[0], edge[1])[2] for edge in normalized] ==
                [mirror_raw(base, edge[0], edge[1])[2] for edge in edges],
                f"Listed length or ordered stream changed: {label}")
        require([joint_normalize(base, edge) for edge in normalized] == normalized,
                f"Accepted chain idempotence failed: {label}")
        self.counts["chain_controls"] += 1
        self.counts["chain_empty_controls"] += not edges
        return normalized

    def cycle(self, base, edges, label):
        exterior, center = edges[0][:2]
        require(mirror.cycleOK(base, edges, exterior, center), f"Original cycle failed: {label}")
        normalized = self.chain(base, edges, exterior, center, label)
        core_b, core_c, _, _ = canonical_state(base, exterior, center)
        require(mirror.cycleOK(base, normalized, core_b, core_c), f"Normalized cycle failed: {label}")
        # U and V are checked separately; this finite check is stronger than
        # merely testing their combined gain and is not a claimed Lean endpoint.
        require(totals(base, normalized) == totals(base, edges), f"Closed totals changed: {label}")
        old_widths = [2 * len(edge[0]) + len(edge[1]) for edge in edges]
        new_widths = [2 * len(edge[0]) + len(edge[1]) for edge in normalized]
        require(max(new_widths) <= max(old_widths), f"Maximum cycle width increased: {label}")
        self.counts["cycle_controls"] += 1
        self.counts["cycle_listed_edges"] += len(edges)
        self.counts["cycle_strictly_narrowed"] += sum(new_widths) < sum(old_widths)

    def source_equivalence(self):
        for base, classes in self.examples.items():
            samples = [item for examples in classes.values() for item in examples]
            self.counts["canonical_source_classes"] += len(classes)
            for (edge, normalized), (other, other_normalized) in combinations(samples, 2):
                same_source = canonical_state(base, *edge[:2])[:2] == canonical_state(base, *other[:2])[:2]
                require((normalized == other_normalized) == same_source,
                        "Normalized-edge equality differs from canonical-source equality")
                self.counts["source_equivalence_pairs"] += 1
                self.counts["source_equivalence_equal"] += same_source
                self.counts["source_equivalence_different"] += not same_source


def word_controls(checks):
    for base in (0, 1, 2, 3, 10):
        neutral = max(0, base - 1)
        for length in range(6):
            for word in product(sorted({0, neutral, 2 * neutral + 1}), repeat=length):
                word = list(word)
                suffix, center = strip_suffix(base, word), strip_center(base, word)
                require((suffix, center) == strip_oracle(base, word), "Independent strip formulas disagree")
                require(suffix_pad(base, suffix[1], suffix[0]) == word and
                        center_pad(base, center[1], center[0]) == word, "Strip reconstruction failed")
                require(strip_suffix(base, suffix[0]) == (suffix[0], 0) and
                        strip_center(base, center[0]) == (center[0], 0), "Word retraction failed")
                checks.counts["strip_word_controls"] += 1


def certificate_controls(checks, controls):
    for base, edges in controls:
        checks.counts["known_bases"] += 1
        checks.counts["known_edges"] += len(edges)
        checks.cycle(base, edges, ("original", base))
        for depths in ((1, 0), (0, 1), (2, 3)):
            checks.cycle(base, [padded_edge(base, edge, depths, depths) for edge in edges],
                         ("uniform", base, depths))
        gain_b = next(i for i, edge in enumerate(edges) if edge[4] > 0)
        gain_c = next(i for i, edge in enumerate(edges) if edge[5] > 0)
        for floor_b, floor_c in ((0, 0), (2, 1)):
            phases_b, phases_c = [floor_b] * len(edges), [floor_c] * len(edges)
            phases_b[(gain_b + 1) % len(edges)] += 1
            phases_c[(gain_c + 1) % len(edges)] += 1
            padded = [padded_edge(base, edge, (phases_b[i], phases_c[i]),
                                  (phases_b[(i + 1) % len(edges)], phases_c[(i + 1) % len(edges)]))
                      for i, edge in enumerate(edges)]
            checks.cycle(base, padded, ("phase", base, floor_b, floor_c))
            checks.counts["cycle_phase_dependent"] += 1
        padded, depths = [], (2, 2)
        for i, edge in enumerate(edges * 3):
            target_depths = (0, 0) if i == 0 else (min(2, depths[0] + edge[4]), min(2, depths[1] + edge[5]))
            padded.append(padded_edge(base, edge, depths, target_depths))
            depths = target_depths
        require(depths == (2, 2) and min(padded[0][4:]) >= 2, "Large-trim schedule did not close")
        checks.cycle(base, padded, ("phase-three-copies", base))
        checks.counts["cycle_phase_dependent"] += 1
        for length in (0, 1, len(edges) - 1):
            checks.chain(base, edges[:length], *edges[0][:2], ("prefix", base, length))


def directed_controls(checks):
    sources = ((2, [], [2]), (2, [], [0, 2]), (2, [2], [0, 1]),
               (3, [3], [0, 2]), (10, [], [0, 10]), (10, [10], [0, 9]),
               (2, [1, 0], [1, 2]), (3, [], [2, 4]), (10, [1], [10]))
    shifts = ((0, 0), (1, 0), (1, 1), (3, 0), (3, 2))
    for base, exterior, center in sources:
        seed = mirror.step(base, exterior, center)
        require(seed is not None, "A directed source must satisfy Hyp")
        checks.chain(base, [seed], exterior, center, ("directed-terminal-allowed", base, seed))
        for (a, a2), (c, c2) in product(shifts, repeat=2):
            checks.edge(base, padded_edge(base, seed, (a, c), (a2, c2)), ("directed", base, a, a2, c, c2))
            checks.counts["directed_edge_controls"] += 1


def boundary_controls(checks, controls):
    edges = next(edges for base, edges in controls if base == 2)
    malformed = [padded_edge(2, edges[0], (1, 1), (1, 1))] + edges[1:]
    require(all(mirror.edgeOK(2, edge) for edge in malformed), "Seam witness needs valid local edges")
    require(not chain_ok(2, malformed, *malformed[0][:2]) and
            not mirror.cycleOK(2, malformed, *malformed[0][:2]), "Malformed seam was accepted")
    repaired = [checks.edge(2, edge, ("seam-witness", i)) for i, edge in enumerate(malformed)]
    require(repaired == edges and chain_ok(2, repaired, *repaired[0][:2]) and
            mirror.cycleOK(2, repaired, *repaired[0][:2]), "Joint normalization did not repair the seam")
    checks.counts["boundary_repaired_seams"] += 1
    for field in (4, 5):
        bad = list(edges[0])
        bad[field] += 1
        bad = tuple(bad)
        require(not mirror.edgeOK(2, bad) and mirror.edgeOK(2, joint_normalize(2, bad)),
                "Incorrect-trim acceptance-iff counterexample failed")
        checks.counts["boundary_repaired_trims"] += 1
    for field in (2, 3):
        bad = list(edges[0])
        bad[field] = [bad[field][0] + 5] + bad[field][1:]
        bad = tuple(bad)
        require(not mirror.edgeOK(2, bad) and not mirror.edgeOK(2, joint_normalize(2, bad)),
                "A genuinely changed target coefficient should still be rejected")
        checks.counts["boundary_rejected_targets"] += 1
    terminal = ([1], [10], [3], [0], 0, 0)
    require(mirror.edgeOK(10, terminal) and joint_normalize(10, terminal) == terminal and
            not mirror.hyp(10, terminal[2], terminal[3]) and mirror.step(10, terminal[2], terminal[3]) is None,
            "Decimal source-Hyp/target-not-Hyp witness failed")
    checks.counts["boundary_decimal_terminal"] += 1
    outside_hyp = ([4], [1, 0, 1], [], [], 0, 0)
    first = joint_normalize(2, outside_hyp, integer_raw)
    second = joint_normalize(2, first, integer_raw)
    require(not mirror.hyp(2, *outside_hyp[:2]) and first[4] == 0 and second[4] == 2 and first != second,
            "Exact Nat-arithmetic outside-Hyp idempotence counterexample failed")
    require(mirror_raw(2, *outside_hyp[:2]) != integer_raw(2, *outside_hyp[:2]),
            "Expected the documented signed-subtraction mirror boundary")
    checks.counts["boundary_outside_hyp_nat"] += 1
    return [
        "NO_ARBITRARY_ACCEPTANCE_IFF base=2 local_edges=4 before_chain=False after_chain=True "
        "before_cycle=False after_cycle=True repaired_wrong_trims=2",
        "TARGET_HYP_BOUNDARY base=10 edge=([1],[10],[3],[0],0,0) source_hyp=True "
        "target_hyp=False edge_accepted=True canonical_fixed=True next_step=None",
        "NAT_OUTSIDE_HYP_IDEMPOTENCE_BOUNDARY base=2 B=[4] C=[1,0,1] first_u=0 second_u=2 "
        "idempotent=False mirror_raw_disagrees=True",
    ]


def main():
    controls = mirror._lean_certs()
    require(len(controls) == 8 and {base for base, _ in controls} == KNOWN_BASES and
            all(edges for _, edges in controls), "Expected all eight existing source certificates")
    checks = Controls()
    word_controls(checks)
    certificate_controls(checks, controls)
    directed_controls(checks)
    witnesses = boundary_controls(checks, controls)
    checks.source_equivalence()
    for key in ("edge_fixed_retractions", "edge_nonfixed_inputs", "edge_empty_exterior",
                "edge_nonsymmetric_center", "edge_target_hyp_false", "edge_nonmaximal_u",
                "edge_nonmaximal_v", "edge_u_changed", "edge_v_changed", "cycle_strictly_narrowed",
                "cycle_phase_dependent", "chain_empty_controls", "source_equivalence_equal",
                "source_equivalence_different"):
        require(checks.counts[key] > 0, f"Missing required coverage: {key}")
    print("JOINT CANONICALIZATION FINITE CONTROLS PASS (not a mathematical proof)")
    for prefix in ("known_", "strip_", "integer_", "template_", "edge_", "chain_", "cycle_",
                   "directed_", "canonical_", "same_", "source_", "boundary_"):
        print(" ".join(f"{key}={checks.counts[key]}" for key in sorted(checks.counts) if key.startswith(prefix)))
    for witness in witnesses:
        print(witness)


if __name__ == "__main__":
    main()
