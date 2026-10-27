#!/usr/bin/env python3
"""Independent audit of a spatial lasso with temporal period eight.

The primary audit imports only the new witness generator.  Supplementary
local-source checks use the unchanged main-branch A120 mirror; no earlier
Agent 106 PR is required.  Local tiles are checked by expanded integer
equations; whole prefix transitions are checked by ordinary integer
arithmetic and decimal string digits, without importing a normalization or
transition routine to produce the reference answer.

For a cut k, L[t] is the lower carry into coefficient x[t,k]; H[t] is the
upper carry leaving that coefficient towards k-1; Y[t] at overflow phases
is the preceding column's normalized upper digit.  An edge to the next cut
with chosen upper input h[t] must satisfy, for every temporal phase t,

  x[t]+L[t] = d[t] + 10 Lnext[t],
  x[t]+h[t] = r[t] + 10 H[t],
  Hnext[t] = h[t],
  x[t+1] = d[t] + (Y[t] if gamma[t]=1 else r[t]),
  Ynext[t] = r[t] at overflow phases.

These equations concatenate in space.  A stem followed by a closed spatial
loop therefore defines an infinite coefficient array; its every finite
prefix returns after eight steps when the high carry at the cut is free.
It does not provide an eventually neutral tail or a finite B certificate.

  python3 calculation/agent-106/infinite_prefix_audit.py
"""

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import infinite_prefix as generator


PERIOD = 8


def require(condition, message):
    if not condition:
        raise ValueError(message)


def as_state(state):
    require(isinstance(state, (tuple, list)) and len(state) == 3, "cut state must have three fields")
    require(all(isinstance(field, (tuple, list)) for field in state), "cut fields must be sequences")
    lower, upper, previous = map(tuple, state)
    require(len(lower) == len(upper) == PERIOD and len(previous) == PERIOD // 2,
            "cut field lengths must be 8,8,4")
    require(all(type(bit) is int and bit in (0, 1) for bit in lower + upper),
            "cut carries must be integer bits")
    require(all(type(digit) is int and 0 <= digit <= 9 for digit in previous),
            "cut previous values must be decimal digits")
    return lower, upper, previous


def integer_edge(word, high_in):
    whole = tuple(word) + (18 * high_in,) + tuple(reversed(word))
    value = sum(coefficient * 10 ** i for i, coefficient in enumerate(whole))
    decimal = str(value)
    paired = tuple(int(decimal[-1 - j]) + int(decimal[j]) for j in range(len(word)))
    return paired, len(decimal) - len(whole)


def check_local_witness(witness, profile):
    require(isinstance(witness, dict), "witness must be a dictionary")
    require(len(profile) == PERIOD and all(len(word) == 3 for word in profile),
            "source profile must contain eight width-three words")
    require(all(type(x) is int and 0 <= x <= 18 for word in profile for x in word),
            "source profile coefficients must lie in 0..18")
    require(all(word[0] > 0 for word in profile), "source profile heads must be positive")
    states = [as_state(state) for state in witness["states"]]
    columns = [tuple(column) for column in witness["columns"]]
    upper_inputs = [tuple(column) for column in witness["next_high"]]
    stem, loop = witness["stem_length"], witness["loop_length"]
    require(type(stem) is int and type(loop) is int and stem >= 0 and loop > 0,
            "lasso stem/loop lengths must be nonnegative/positive integers")
    require(len(columns) == len(upper_inputs) == stem + loop, "lasso edge-label count mismatch")
    require(len(states) == len(columns) + 1, "lasso state count mismatch")
    require(as_state(witness["root"]) == states[0], "lasso root mismatch")
    require(states[-1] == states[stem], "spatial loop does not close")

    initial_lower, initial_upper, initial_previous = states[0]
    # Lower carries are independently obtained by whole-integer division.
    for t, word in enumerate(profile):
        numeric = sum(coefficient * 10 ** i for i, coefficient in enumerate(word))
        require(numeric // (10 ** len(word)) == initial_lower[t], "initial lower carry mismatch")
        require(integer_edge(word, initial_upper[t]) == (profile[(t + 1) % PERIOD], t % 2),
                "initial cut does not realize the source profile")
        if t % 2:
            require((word[-1] + initial_upper[t]) % 10 == initial_previous[t // 2],
                    "initial previous digit mismatch")

    for cut, (column, upper_input) in enumerate(zip(columns, upper_inputs)):
        lower, upper, previous = states[cut]
        next_lower, next_upper, next_previous = states[cut + 1]
        require(len(column) == len(upper_input) == PERIOD, "column/input width mismatch")
        require(all(type(coefficient) is int and 0 <= coefficient <= 18 for coefficient in column),
                "column coefficients must be integers in 0..18")
        require(all(type(bit) is int and bit in (0, 1) for bit in upper_input),
                "column inward carries must be integer bits")
        require(upper_input == next_upper, "next upper carry mismatch")
        for t in range(PERIOD):
            low_digit = column[t] + lower[t] - 10 * next_lower[t]
            high_digit = column[t] + upper_input[t] - 10 * upper[t]
            require(0 <= low_digit <= 9 and 0 <= high_digit <= 9,
                    f"invalid normalized digit at cut={cut}, phase={t}")
            partner = previous[t // 2] if t % 2 else high_digit
            require(column[(t + 1) % PERIOD] == low_digit + partner,
                    f"temporal coefficient equation fails at cut={cut}, phase={t}")
            if t % 2:
                require(next_previous[t // 2] == high_digit,
                        f"next previous digit mismatch at cut={cut}, phase={t}")
    return states, columns


def expand(witness, states, columns, repetitions):
    stem, loop = witness["stem_length"], witness["loop_length"]
    expanded_columns = list(columns[:stem])
    expanded_states = list(states[:stem + 1])
    for _ in range(repetitions):
        require(expanded_states[-1] == states[stem], "spatial repetition starts at wrong state")
        expanded_columns.extend(columns[stem:stem + loop])
        expanded_states.extend(states[stem + 1:stem + loop + 1])
    require(len(expanded_states) == len(expanded_columns) + 1, "expanded state count mismatch")
    return expanded_states, expanded_columns


def integer_prefix_checks(profile, cut_states, columns, selected_cuts=None):
    words = [tuple(profile[t]) + tuple(column[t] for column in columns)
             for t in range(PERIOD)]
    width = len(words[0])
    require(all(len(word) == width for word in words), "expanded phase widths differ")
    require(width <= 10000, "audit width exceeds the explicit resource bound")
    if selected_cuts is not None:
        selected_cuts = set(selected_cuts)
        require(all(type(cut) is int and 1 <= cut <= width for cut in selected_cuts),
                "selected cut lies outside the expanded prefix")
    # Python's optional decimal conversion guard is a resource safeguard,
    # not part of the arithmetic under examination.
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(max(4300, 2 * width + 100))

    initial_high = cut_states[0][1]
    low_values = [0] * PERIOD
    reverse_values = [0] * PERIOD
    power = 1
    checks = 0
    for cut in range(1, width + 1):
        for t in range(PERIOD):
            coefficient = words[t][cut - 1]
            low_values[t] += coefficient * power
            reverse_values[t] = 10 * reverse_values[t] + coefficient
        power *= 10
        if selected_cuts is not None and cut not in selected_cuts:
            continue
        for t in range(PERIOD):
            if cut < 3:
                suffix = profile[t][cut:]
                reversed_value = sum(coefficient * 10 ** i
                                     for i, coefficient in enumerate(reversed(suffix)))
                high_in = (reversed_value + initial_high[t]) // (10 ** len(suffix))
            else:
                high_in = cut_states[cut - 3][1][t]
            require(high_in in (0, 1), "projected boundary carry is not a bit")
            # The middle coefficient 0 or 18 forces high_in, independent of
            # the lower half's carry.  This is an exact ordinary integer.
            value = (low_values[t] + 18 * high_in * power
                     + reverse_values[t] * 10 * power)
            decimal = str(value)
            require(len(decimal) - (2 * cut + 1) == t % 2,
                    f"integer overflow mismatch at cut={cut}, phase={t}")
            actual = tuple(int(decimal[-1 - j]) + int(decimal[j]) for j in range(cut))
            expected = words[(t + 1) % PERIOD][:cut]
            require(actual == expected,
                    f"integer prefix mismatch at cut={cut}, phase={t}, high={high_in}")
            checks += 1
    return width, checks


def malformed_witness_controls(witness, profile):
    bad = deepcopy(witness)
    bad["states"] = bad["states"][:-1]
    bad_length = bad
    bad = deepcopy(witness)
    bad["columns"] = list(bad["columns"])
    changed = list(bad["columns"][0])
    changed[0] = (changed[0] + 1) % 19
    bad["columns"][0] = tuple(changed)
    bad_coefficient = bad
    bad = deepcopy(witness)
    bad["next_high"] = list(bad["next_high"])
    changed = list(bad["next_high"][0])
    changed[0] = 1 - changed[0]
    bad["next_high"][0] = tuple(changed)
    bad_carry = bad
    bad = deepcopy(witness)
    bad["loop_length"] = 0
    bad_loop = bad
    bad = deepcopy(witness)
    bad["next_high"] = bad["next_high"][:-1]
    bad_zip_length = bad
    rejected = 0
    for corrupt in (bad_length, bad_coefficient, bad_carry, bad_loop, bad_zip_length):
        try:
            check_local_witness(corrupt, profile)
        except (ValueError, TypeError, KeyError):
            rejected += 1
        else:
            raise ValueError("malformed witness was accepted")
    return rejected


def local_source_lift_checks(profile, cut_states, columns):
    """Actual A120 sources realizing individual abstract edges, not a cycle."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror

    words = [tuple(profile[t]) + tuple(column[t] for column in columns)
             for t in range(PERIOD)]
    rng = random.Random(106120)
    widths = [1, 2, 3, 4, 8, 16, 32, 64, 128, 256, 512, 1000]
    widths.extend(rng.randrange(1, 1001) for _ in range(64 - len(widths)))
    counts = [0, 0]
    for i, cut in enumerate(widths):
        t = i % PERIOD
        prefix = words[t][:cut]
        require(len(prefix) == cut, "local-lift prefix too short")
        if cut < 3:
            suffix = profile[t][cut:]
            reversed_value = sum(coefficient * 10 ** j
                                 for j, coefficient in enumerate(reversed(suffix)))
            high_in = (reversed_value + cut_states[0][1][t]) // (10 ** len(suffix))
        else:
            high_in = cut_states[cut - 3][1][t]
        exterior = list(prefix) + [18 * high_in]
        center = [18 * (1 - high_in)]
        require(mirror.e1(10, exterior) == high_in, "A120 lift lower carry mismatch")
        require(mirror.e2(10, exterior, center) == 1 - high_in,
                "A120 lift complementary center carry mismatch")
        require(mirror.hyp(10, exterior, center), "A120 lift does not satisfy Hyp")
        raw = mirror.nextB(10, exterior, center)
        expected, expected_gamma = integer_edge(prefix, high_in)
        require(tuple(raw[:cut]) == expected == words[(t + 1) % PERIOD][:cut],
                "A120 lift prefix disagrees with independent integer reference")
        require(mirror.gam(10, exterior, center) == expected_gamma == t % 2,
                "A120 lift overflow mismatch")
        counts[high_in] += 1
    print(f"A120_LOCAL_SOURCE_LIFTS samples={len(widths)} seed=106120 "
          f"width_range={min(widths)}..{max(widths)} high_carry_counts={counts} PASS", flush=True)
    return len(widths)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repetitions", type=int, default=64)
    args = parser.parse_args()
    if not 1 <= args.repetitions <= 128:
        parser.error("--repetitions must be between 1 and 128")
    profile = generator.profile()
    witness = generator.fixed_witness()
    require("loop_length" in witness, f"generator did not return a lasso: {witness}")
    states, columns = check_local_witness(witness, profile)
    rejected = malformed_witness_controls(witness, profile)
    core = {key: witness[key] for key in (
        "root", "stem_length", "loop_length", "states", "columns", "next_high")}
    digest = hashlib.sha256(json.dumps(core, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    print(f"LOCAL_LASSO_AUDIT PASS stem={witness['stem_length']} "
          f"loop={witness['loop_length']} tiles={len(columns)} sha256={digest}", flush=True)
    print(f"malformed_witnesses_rejected={rejected} explicit_validation=True", flush=True)
    repetitions = sorted({0, 1, 2, 5, 16, args.repetitions})
    total = 0
    max_width = 0
    for count in repetitions:
        expanded_states, expanded_columns = expand(witness, states, columns, count)
        width, checks = integer_prefix_checks(profile, expanded_states, expanded_columns)
        total += checks
        max_width = max(max_width, width)
        print(f"INTEGER_PREFIX_AUDIT repetitions={count} every_cut=1..{width} "
              f"phase_edges={checks} PASS", flush=True)
    needed = max(0, (1000 - 3 - witness["stem_length"] + witness["loop_length"] - 1)
                 // witness["loop_length"])
    expanded_states, expanded_columns = expand(witness, states, columns, needed)
    random_cuts = sorted(random.Random(106).sample(range(140, 1000), 63) + [1000])
    _, checks = integer_prefix_checks(profile, expanded_states, expanded_columns, random_cuts)
    total += checks
    max_width = max(max_width, max(random_cuts))
    print(f"RANDOM_INTEGER_DEPTHS seed=106 depths={len(random_cuts)} "
          f"range={min(random_cuts)}..{max(random_cuts)} phase_edges={checks} PASS", flush=True)
    local_source_lift_checks(profile, expanded_states, expanded_columns)
    print(f"INFINITE_PREFIX_AUDIT PASSED integer_phase_edges={total} max_width={max_width}")
    print("SCOPE: arbitrary-depth free-high-carry prefixes; no neutral-tail or finite-B claim")
    print("Each numeric transition has its own middle coefficient; no single whole-integer orbit is constructed")


if __name__ == "__main__":
    main()
