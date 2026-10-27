#!/usr/bin/env python3
"""Independent controls for the variable-gap exterior block MDD.

The tuple transition oracle lives in saturation_oracle.py.  This file adds
variable-length block encoding, original-phase rotation checks, terminal carry
filters, and a separately reconstructed 24-phase center fixture.

The fixture is CENTER-ONLY until an exterior with exactly the same g/e streams
is supplied.  `couple_target_exterior` performs the actual mirror cycleOK gate
on such a supplied exterior before returning full certificate edges.
"""

import argparse
import json
from pathlib import Path
import random
import subprocess
import sys
import time

import saturation_oracle as oracle

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror


TARGET_G = "110001001000110001001000"
TARGET_E = "010100110100101011001011"
TARGET_V = "100001000000100001000000"
CENTER_PHASES = [
    [9, 14, 13, 18, 13, 14, 9],
    [4, 9, 13, 13, 9, 4],
    [14, 14, 3, 8, 3, 14, 14],
    [9, 9, 7, 16, 7, 9, 9],
    [9, 9, 16, 12, 16, 9, 9],
    [9, 9, 13, 6, 13, 9, 9],
    [9, 3, 10, 10, 3, 9],
    [9, 8, 1, 1, 8, 9],
    [9, 17, 2, 2, 17, 9],
    [9, 7, 10, 4, 10, 7, 9],
    [9, 16, 0, 10, 0, 16, 9],
    [9, 12, 2, 0, 2, 12, 9],
    [9, 4, 5, 0, 5, 4, 9],
    [14, 9, 5, 5, 9, 14],
    [4, 4, 15, 10, 15, 4, 4],
    [9, 9, 11, 2, 11, 9, 9],
    [9, 9, 2, 6, 2, 9, 9],
    [9, 9, 5, 12, 5, 9, 9],
    [9, 15, 8, 8, 15, 9],
    [9, 10, 17, 17, 10, 9],
    [9, 1, 16, 16, 1, 9],
    [9, 11, 8, 14, 8, 11, 9],
    [9, 2, 18, 8, 18, 2, 9],
    [9, 6, 16, 18, 16, 6, 9],
]


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def center_successor(center, incoming, overflow):
    """Independent decimal center arithmetic, before neutral-pair trimming."""
    carry = incoming
    digits = []
    for coefficient in center:
        carry, digit = divmod(coefficient + carry, 10)
        digits.append(digit)
    require(carry == 1 - incoming, "Center fails the complementary-carry condition")
    if overflow:
        first = digits + [9 * incoming]
        second = [9 * incoming] + digits[::-1]
    else:
        first, second = digits, digits[::-1]
    return [left + right for left, right in zip(first, second)]


def integer_value(coefficients):
    value = 0
    for coefficient in reversed(coefficients):
        value = 10 * value + coefficient
    return value


def decimal_reverse(number):
    reverse = 0
    while number:
        number, digit = divmod(number, 10)
        reverse = 10 * reverse + digit
    return reverse


def template_value(exterior, center, gap):
    return integer_value(exterior + [9] * gap + center + [9] * gap + exterior[::-1])


def validate_target_center():
    require(len(TARGET_G) == len(TARGET_E) == len(TARGET_V) == len(CENTER_PHASES) == 24,
            "Target fixture period mismatch")
    synthetic = {(0, 0): [1], (0, 1): [10, 0], (1, 0): [1, 10], (1, 1): [10]}
    integer_checks = 0
    for phase, center in enumerate(CENTER_PHASES):
        incoming, overflow, trim = int(TARGET_E[phase]), int(TARGET_G[phase]), int(TARGET_V[phase])
        raw = center_successor(center, incoming, overflow)
        following = CENTER_PHASES[(phase + 1) % 24]
        require(raw == [9] * trim + following + [9] * trim,
                ("Center fixture trim mismatch", phase))
        require(center == center[::-1] and all(0 <= value <= 18 for value in center),
                ("Malformed center fixture", phase))
        require(CENTER_PHASES[(phase + 12) % 24] == [18 - value for value in center],
                ("Center half-period complement mismatch", phase))
        exterior = synthetic[incoming, overflow]
        require(mirror.hyp(10, exterior, center), ("Mirror Hyp mismatch", phase))
        require(mirror.e1(10, exterior) == incoming and mirror.gam(10, exterior, center) == overflow,
                ("Synthetic exterior stream mismatch", phase))
        require(mirror.nextC(10, exterior, center) == raw, ("Independent center oracle mismatch", phase))
        edge = (exterior, center, mirror.nextB(10, exterior, center), following, 0, trim)
        require(mirror.edgeOK(10, edge), ("Synthetic full edge rejected", phase))
        for padding in (0, 1, 4):
            padded = exterior + [9] * padding
            next_exterior = mirror.nextB(10, padded, center)
            for gap in (2, 3, 7):
                value = template_value(padded, center, gap)
                target = template_value(next_exterior, following, gap - overflow + trim)
                require(value + decimal_reverse(value) == target,
                        ("Integer center-edge control failed", phase, padding, gap))
                integer_checks += 1
    require(sum(map(int, TARGET_G)) == 2 * sum(map(int, TARGET_V)) == 8,
            "Center length telescoping mismatch")
    return {"phase_count": 24, "widths": sorted(set(map(len, CENTER_PHASES))),
            "overflow_total": 8, "center_trim_total": 4,
            "mirror_edges": 24, "padded_integer_edges": integer_checks,
            "status": "CENTER_ONLY_PASS"}


def couple_target_exterior(words):
    """Accept only a supplied B witness matching this exact center's streams.

    The returned edge list is a genuine Python-mirror candidate certificate.
    It still needs the user's required Lean decide theorem and verify.py gate.
    This function performs no searches or publication actions.
    """
    validate_target_center()
    require(len(words) == 24, "Supplied exterior witness must have 24 phases")
    words = [list(word) for word in words]
    carry = tuple(map(int, TARGET_E))
    oracle.mirror_check_witness(10, TARGET_G, carry, words)
    edges = []
    for phase, exterior in enumerate(words):
        next_exterior = words[(phase + 1) % 24]
        center = CENTER_PHASES[phase][:]
        next_center = CENTER_PHASES[(phase + 1) % 24][:]
        raw = mirror.nextB(10, exterior, center)
        exterior_trim = len(raw) - len(next_exterior)
        require(exterior_trim >= 0, "Negative exterior trim")
        edge = (exterior, center, next_exterior, next_center, exterior_trim, int(TARGET_V[phase]))
        require(mirror.edgeOK(10, edge), ("Coupled edge rejected", phase))
        edges.append(edge)
    require(mirror.cycleOK(10, edges, words[0], CENTER_PHASES[0]),
            "Coupled Python cycleOK rejected")
    return edges


def rotate_state(state, bits, shift):
    """Rotate any temporal cut, including its sparse overflow partners."""
    period = len(bits)
    shift %= period
    sparse_shift = sum(bits[:shift])
    low, high, partners = state
    return (low[shift:] + low[:shift], high[shift:] + high[:shift],
            partners[sparse_shift:] + partners[:sparse_shift])


def block_layout(pattern):
    bits = oracle.checked_pattern(10, pattern)
    require(any(bits), "Variable-block controls require at least one overflow")
    offset = bits.index(1)
    rotated = bits[offset:] + bits[:offset]
    starts = [index for index, bit in enumerate(rotated) if bit]
    lengths = [right - left for left, right in zip(starts, starts[1:] + [len(bits)])]
    require(all(1 <= length <= 5 for length in lengths), "Unsupported gap in differential control")
    return bits, offset, starts, lengths


def encode_cut(state, pattern):
    bits, offset, starts, lengths = block_layout(pattern)
    low, high, partners = rotate_state(state, bits, offset)
    return tuple(
        sum(low[start + phase] << phase for phase in range(length))
        + (sum(high[start + phase] << phase for phase in range(length)) << length)
        + (partner << (2 * length))
        for start, length, partner in zip(starts, lengths, partners)
    )


def engine_command(binary, pattern, wanted_e=None):
    command = [binary, pattern, "2000000", "100000000", "120", "30"]
    if wanted_e is not None:
        command += ["--e", wanted_e]
    return command


def checked_engine_case(binary, pattern, wanted_e=None):
    """Compare every exact frontier set, including original-phase carry filters."""
    bits, offset, _, _ = block_layout(pattern)
    command = engine_command(binary, pattern, wanted_e)
    completed = subprocess.run(command + ["--witness"], text=True, capture_output=True,
                               timeout=35, check=True)
    records = [json.loads(line) for line in completed.stdout.splitlines()]
    result = next(record for record in records if record["type"] == "RESULT")
    require(result["status"] != "UNDECIDED", ("Incomplete small engine control", pattern, result))
    require(result["g"] == pattern and result["phase_rotation"] == offset,
            "Engine original-phase metadata mismatch")
    require(result["requested_e"] == (wanted_e or ""), "Engine carry filter metadata mismatch")
    layers = [record for record in records if record["type"] == "LAYER"]
    period = len(bits)
    frontier = {((0,) * period, bits, (1,) * sum(bits))}
    counts = []
    compared_records = 0
    repeat_snapshot = None
    for layer in layers:
        depth = layer["depth"]
        require(depth == len(counts), "Layer indices are not consecutive")
        require(len(frontier) <= 1000000, "Small control exceeds finite export budget")
        counts.append(len(frontier))
        accepted = sum(
            oracle.is_accepting(10, bits, state)
            and (wanted_e is None or state[0] == tuple(map(int, wanted_e)))
            for state in frontier
        )
        require(len(frontier) == int(layer["states"]) and accepted == int(layer["accepts"]),
                ("Variable-block layer-count mismatch", pattern, wanted_e, depth, layer))
        exported = subprocess.run(command + ["--export-layer", str(depth)], text=True,
                                  capture_output=True, timeout=35, check=True)
        actual = {tuple(word) for word in json.loads(exported.stdout.strip().splitlines()[-1])}
        expected = {encode_cut(state, pattern) for state in frontier}
        require(actual == expected, ("Variable-block full-set mismatch", pattern, wanted_e, depth))
        compared_records += len(frontier)
        if depth == result["cycle_start"]:
            repeat_snapshot = frontier.copy()
        if depth + 1 < len(layers):
            frontier = {
                target
                for state in frontier
                for target in oracle._successor_columns(10, bits, state, depth == 0)
            }
    if result["reason"] == "empty_layer":
        require(not frontier, "Engine false empty-layer outcome")
    if result["reason"] == "exact_layer_repeat":
        require(repeat_snapshot is not None and frontier == repeat_snapshot,
                "Engine false exact-layer recurrence")
    mirror_edges = 0
    integer_edges = 0
    for witness in (record for record in records if record["type"] == "WITNESS"):
        require(witness["g"] == pattern, "Witness overflow phase mismatch")
        if wanted_e is not None:
            require(witness["e"] == wanted_e, "Witness target carry phase mismatch")
        carry = tuple(map(int, witness["e"]))
        replay = oracle.mirror_check_witness(10, bits, carry, witness["B_t"])
        mirror_edges += replay["edges"]
        integer_edges += oracle.integer_witness_controls(10, bits, carry, witness["B_t"])
    output = {"g": pattern, "e": wanted_e, "status": result["status"],
              "depth": result["depth"], "cycle_start": result["cycle_start"],
              "layers": len(layers), "layer_state_records": compared_records,
              "mirror_edges": mirror_edges, "integer_edges": integer_edges,
              "exact_sets": "PASS"}
    print("FRONTIER_CASE", json.dumps(output, sort_keys=True), flush=True)
    return output


def image_differentials(binary):
    generator = random.Random(1082408)
    patterns = ("1", "10", "100", "1000", "10000", "110", "10100", "110000",
                "10000100", "01100001", "0010100", "11100010000", "100010001000", TARGET_G)
    cases = 0
    memberships = 0
    rotations = 0
    for pattern in patterns:
        bits, _, _, _ = block_layout(pattern)
        period = len(bits)
        initial = ((0,) * period, bits, (1,) * sum(bits))
        reached = sorted(oracle.successor_columns(10, bits, initial, first=True))
        arbitrary = [
            (tuple(generator.randrange(2) for _ in bits),
             tuple(generator.randrange(2) for _ in bits),
             tuple(generator.randrange(10) for _ in range(sum(bits))))
            for _ in range(5)
        ]
        selections = [set(), {initial}, set(generator.sample(reached, min(5, len(reached)))) | set(arbitrary)]
        for sources in selections:
            for first in (False, True):
                expected_cuts = {
                    target
                    for source in sources
                    for target in oracle.successor_columns(10, bits, source, first)
                }
                expected = {encode_cut(cut, pattern) for cut in expected_cuts}
                encoded_sources = sorted(encode_cut(source, pattern) for source in sources)
                payload = str(len(encoded_sources)) + "\n" + "".join(
                    " ".join(map(str, word)) + "\n" for word in encoded_sources)
                completed = subprocess.run([binary, "--image", pattern, str(int(first))],
                                           input=payload, text=True, capture_output=True,
                                           timeout=35, check=True)
                actual = {tuple(word) for word in json.loads(completed.stdout)}
                require(actual == expected, ("Variable-block finite-image mismatch", pattern, first))
                cases += 1
                memberships += len(expected)
                for shift in sorted({1 % period, (period - 1) % period}):
                    rotated_bits = bits[shift:] + bits[:shift]
                    rotated_sources = {rotate_state(source, bits, shift) for source in sources}
                    rotated_targets = {
                        target
                        for source in rotated_sources
                        for target in oracle.successor_columns(10, rotated_bits, source, first)
                    }
                    require(rotated_targets == {rotate_state(target, bits, shift) for target in expected_cuts},
                            ("Arbitrary temporal rotation mismatch", pattern, shift))
                    rotations += 1
    print(f"FINITE_IMAGES cases={cases} output_memberships={memberships} "
          f"temporal_rotations={rotations} PASS", flush=True)
    return cases, memberships, rotations


def input_guards(binary):
    resources = ["100", "100", "1", "1"]
    cases = [
        ([binary, ""] + resources, None, 2, "ERROR"),
        ([binary, "10x"] + resources, None, 2, "ERROR"),
        ([binary, "1", "1", "100", "1", "1"], None, 2, "ERROR"),
        ([binary, "1", "100", "0", "1", "1"], None, 2, "ERROR"),
        ([binary, "1", "100", "100", "1", "0"], None, 2, "ERROR"),
        ([binary, "1"] + resources + ["--e", "00"], None, 2, "ERROR"),
        ([binary, "100000"] + resources, None, 3, "UNDECIDED"),
        ([binary, "000"] + resources, None, 3, "UNDECIDED"),
        ([binary, "1" * 97] + resources, None, 3, "UNDECIDED"),
        ([binary, "1" * 41] + resources, None, 3, "UNDECIDED"),
        ([binary, "--image", "10", "0"], "1\n4000\n", 2, "ERROR"),
        ([binary, "--image", "10", "2"], "0\n", 2, "ERROR"),
    ]
    for command, payload, expected_code, expected_status in cases:
        completed = subprocess.run(command, input=payload, text=True, capture_output=True, timeout=10)
        record = json.loads(completed.stderr.strip().splitlines()[-1])
        require(completed.returncode == expected_code and record["status"] == expected_status,
                ("Engine input status mismatch", command, completed.returncode, record))
    print(f"INPUT_GUARDS cases={len(cases)} malformed_vs_unsupported=PASS", flush=True)


def global_controls(binary):
    print("TARGET_CENTER", json.dumps(validate_target_center(), sort_keys=True), flush=True)
    input_guards(binary)
    image_differentials(binary)
    cases = [
        ("1", None), ("10", None), ("100", None), ("1000", None), ("10000", None),
        ("11", None), ("110", None), ("10100", None), ("110000", None),
        ("10000100", None), ("11001000", None), ("01100001", None), ("0010100", None),
        ("11100010000", None), ("100010001000", None),
        ("11100010000", "10100110011"),
        ("00011100010", "01110100110"),
        ("100010001000", "101010010101"),
        ("001000100010", "101001010110"),
        ("100010001000", "000000000000"),
    ]
    totals = {"cases": 0, "layers": 0, "layer_state_records": 0,
              "mirror_edges": 0, "integer_edges": 0}
    for pattern, carry in cases:
        result = checked_engine_case(binary, pattern, carry)
        totals["cases"] += 1
        for key in ("layers", "layer_state_records", "mirror_edges", "integer_edges"):
            totals[key] += result[key]
    print("GENERAL_ENGINE_CONTROLS", json.dumps(totals, sort_keys=True), "PASS", flush=True)


def target_frontiers(seconds=600, memory_mib=3072, state_cap=750000):
    """Standalone independent P24 all-carry search with hard memory/time bounds.

    Only the current and next exact tuple frontiers are retained.  Empty frontier
    proves the fixed 24-step overflow word has no finite accepting B interface;
    every resource interruption remains UNDECIDED.  No MDD or production binary
    is consulted by this computation.
    """
    import resource
    require(0 < seconds <= 600, "Target oracle seconds must be in 1..600")
    require(0 < memory_mib <= 3072, "Target oracle memory budget must be at most 3072 MiB")
    require(state_cap > 0, "Target oracle state cap must be positive")
    budget = memory_mib * 1024 * 1024
    _, prior_hard = resource.getrlimit(resource.RLIMIT_AS)
    if prior_hard != resource.RLIM_INFINITY:
        budget = min(budget, prior_hard)
    resource.setrlimit(resource.RLIMIT_AS, (budget, budget))
    started = time.monotonic()
    deadline = started + seconds
    bits = tuple(map(int, TARGET_G))
    wanted = tuple(map(int, TARGET_E))
    period = len(bits)
    frontier = {((0,) * period, bits, (1,) * sum(bits))}
    next_frontier = set()
    counts = []
    local_records = 0
    status = "UNDECIDED"
    reason = "depth_cap"
    try:
        for depth in range(101):
            if time.monotonic() >= deadline:
                raise oracle.SearchDeadline
            counts.append(len(frontier))
            terminal_cuts = [state for state in frontier if oracle.is_accepting(10, bits, state)]
            print("TARGET_TUPLE_LAYER", json.dumps(
                {"depth": depth, "states": len(frontier), "accepted_any_e": len(terminal_cuts),
                 "accepted_target_e": sum(state[0] == wanted for state in terminal_cuts),
                 "seconds": round(time.monotonic() - started, 3)}, sort_keys=True), flush=True)
            if terminal_cuts:
                status, reason = "B_TERMINAL_REACHED", "terminal"
                print("TARGET_TERMINAL_CUT", json.dumps(terminal_cuts[0]))
                break
            if not frontier:
                status, reason = "EXHAUSTED_NO_B", "empty_layer"
                break
            if depth == 100:
                break
            next_frontier = set()
            for index, state in enumerate(frontier):
                if index % 128 == 0 and time.monotonic() >= deadline:
                    raise oracle.SearchDeadline
                successors = oracle._successor_columns(
                    10, bits, state, depth == 0, deadline, min(state_cap, 200000))
                local_records += len(successors)
                next_frontier.update(successors)
                if len(next_frontier) > state_cap:
                    raise oracle.LocalRelationCap
            frontier = next_frontier
            next_frontier = set()
    except oracle.SearchDeadline:
        reason = "time_cap"
    except oracle.LocalRelationCap:
        reason = "state_cap"
    except MemoryError:
        reason = "memory_cap"
        frontier.clear()
        next_frontier.clear()
    result = {"g": TARGET_G, "period": period, "status": status, "reason": reason,
              "complete_layer_counts": counts, "layer_state_records": sum(counts),
              "local_successor_records": local_records,
              "seconds": round(time.monotonic() - started, 6),
              "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "memory_limit_mib": budget // (1024 * 1024)}
    print("TARGET_TUPLE_RESULT", json.dumps(result, sort_keys=True), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("center", "engine", "target-frontiers"))
    parser.add_argument("--binary")
    parser.add_argument("--seconds", type=int, default=600)
    parser.add_argument("--memory-mib", type=int, default=3072)
    parser.add_argument("--state-cap", type=int, default=750000)
    args = parser.parse_args()
    if args.mode == "center":
        print(json.dumps(validate_target_center(), sort_keys=True))
    elif args.mode == "target-frontiers":
        target_frontiers(args.seconds, args.memory_mib, args.state_cap)
    elif args.binary is None:
        parser.error("engine requires --binary")
    else:
        global_controls(args.binary)


if __name__ == "__main__":
    main()
