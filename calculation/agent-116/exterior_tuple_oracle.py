#!/usr/bin/env python3
"""Whole-word controls for the independent exterior carry-tuple solver.

The oracle uses integer positional values, not the solver's local carry
transitions.  It enumerates every positive-head coefficient word of each
requested width, constructs the partial deterministic fixed-width map,
and finds all its cycles.  The optional solver comparison covers every
binary overflow necklace through the requested period, including repeated
cycles.  This is a bounded differential check, not an all-width proof.
"""

import argparse
import itertools
import json
import pathlib
import subprocess
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exterior_step(base, word):
    """A120 exterior map, evaluated by two whole-integer divisions."""
    width = len(word)
    modulus = base ** width
    value = sum(coefficient * base ** j for j, coefficient in enumerate(word))
    carry = value // modulus
    reverse_value = (sum(coefficient * base ** (width - 1 - j)
                         for j, coefficient in enumerate(word)) + 1 - carry)
    overflow = reverse_value // modulus
    require(carry in (0, 1) and overflow in (0, 1),
            f"nonbinary carry: base={base}, word={word}, e={carry}, g={overflow}")
    low = tuple((value // (base ** j)) % base for j in range(width))
    reverse = tuple((reverse_value // (base ** (width - 1 - j))) % base
                    for j in range(width))
    if overflow:
        low += ((base - 1) * (1 - carry),)
        reverse = (1,) + reverse
    return tuple(a + b for a, b in zip(low, reverse)), carry, overflow


def words(base, width):
    if width == 0:
        yield ()
        return
    for head in range(1, 2 * base - 1):
        for tail in itertools.product(range(2 * base - 1), repeat=width - 1):
            yield (head,) + tail


def padding_checks(base, maximum_width):
    """Include empty B, every legal neutral suffix trim, and both carry bits."""
    h = base - 1
    counts = {"words": 0, "padding_equalities": 0, "trim_equalities": 0}
    carries = set()
    for width in range(maximum_width + 1):
        for word in words(base, width):
            counts["words"] += 1
            raw, e, g = exterior_step(base, word)
            carries.add((e, g))
            for padding in (1, 2):
                padded, ep, gp = exterior_step(base, word + (h,) * padding)
                require((padded, ep, gp) == (raw + (h,) * padding, e, g),
                        f"neutral padding mismatch: base={base}, word={word}, "
                        f"padding={padding}")
                counts["padding_equalities"] += 1
            target = raw
            while True:
                common_width = max(1, width, len(target))
                source_padded = word + (h,) * (common_width - width)
                target_padded = target + (h,) * (common_width - len(target))
                actual, ep, gp = exterior_step(base, source_padded)
                require((actual, ep, gp) == (target_padded + (h,) * g, e, g),
                        f"trim padding mismatch: base={base}, source={word}, "
                        f"target={target}, width={common_width}")
                counts["trim_equalities"] += 1
                if not target or target[-1] != h:
                    break
                target = target[:-1]
    counts["carry_pairs"] = sorted("".join(map(str, pair)) for pair in carries)
    return counts


def fixed_width_cycles(base, width):
    """Enumerate cycles of Q -> F(Q) with exactly g neutral digits removed."""
    transitions = {}
    valid_edges = 0
    for word in words(base, width):
        raw, e, g = exterior_step(base, word)
        if not g or raw[-1] == base - 1:
            target = raw[:-1] if g else raw
            require(len(target) == width and target[0] > 0,
                    f"invalid fixed-width successor: base={base}, "
                    f"source={word}, target={target}")
            transitions[word] = (target, e, g)
            valid_edges += 1
        else:
            transitions[word] = None
    complete = set()
    cycles = []
    for start in transitions:
        if start in complete:
            continue
        path = []
        position = {}
        current = start
        while current not in complete and current not in position:
            position[current] = len(path)
            path.append(current)
            edge = transitions[current]
            if edge is None:
                current = None
                break
            current = edge[0]
        if current in position:
            cycle = path[position[current]:]
            cycles.append(tuple((transitions[word][1], transitions[word][2])
                                for word in cycle))
        complete.update(path)
    return cycles, {"words": len(transitions), "edges": valid_edges,
                    "cycles": len(cycles),
                    "cycle_periods": sorted(len(cycle) for cycle in cycles)}


def periodic_streams(cycles, maximum_period):
    answer = {}
    for cycle in cycles:
        length = len(cycle)
        for period in range(length, maximum_period + 1, length):
            for phase in range(length):
                repeated = tuple(cycle[(phase + j) % length] for j in range(period))
                e = "".join(str(pair[0]) for pair in repeated)
                g = "".join(str(pair[1]) for pair in repeated)
                answer.setdefault(g, set()).add(e)
    return answer


def necklaces(period):
    for bits in itertools.product("01", repeat=period):
        word = "".join(bits)
        if all(word <= word[j:] + word[:j] for j in range(1, period)):
            yield word


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=pathlib.Path,
                        help="path to the compiled exterior_tuple executable")
    parser.add_argument("--bases", default="2,3,4")
    parser.add_argument("--width", type=int, default=3)
    parser.add_argument("--period", type=int, default=6)
    args = parser.parse_args()
    bases = [int(text) for text in args.bases.split(",")]
    if any(base < 2 for base in bases) or args.width < 1 or args.period < 1:
        parser.error("bases must be >=2 and width/period positive")
    started = time.monotonic()
    rows = []
    comparisons = positive = negative = accepted_streams = 0
    for base in bases:
        padding = padding_checks(base, args.width)
        widths = []
        cumulative = {}
        for width in range(1, args.width + 1):
            cycles, counts = fixed_width_cycles(base, width)
            expected = periodic_streams(cycles, args.period)
            for g, values in expected.items():
                for e in values:
                    cumulative.setdefault(g, {}).setdefault(e, width)
            # Neutral padding must preserve every narrower accepted stream.
            require(all(set(values).issubset(expected.get(g, set()))
                        for g, values in cumulative.items()),
                    f"narrower cycle lost under padding: base={base}, width={width}")
            widths.append({"width": width, **counts,
                           "periodic_stream_pairs": sum(len(values)
                                                        for values in expected.values())})
            if args.solver is None:
                continue
            for period in range(1, args.period + 1):
                for g in necklaces(period):
                    command = [str(args.solver.resolve()), str(base), g,
                               "--states", "1000000", "--seconds", "30",
                               "--prefix-width", str(width)]
                    result = subprocess.run(command, text=True, capture_output=True,
                                            check=True, timeout=40)
                    actual = json.loads(result.stdout)
                    require(actual["status"] in ("EXHAUSTED", "BOUNDED_WIDTH_ONLY"),
                            f"incomplete solver control: {actual}")
                    got = {row["e"]: row["width"] for row in actual["accepts"]}
                    want = cumulative.get(g, {})
                    require(got == want, {"base": base, "width": width,
                                          "g": g, "expected": want, "actual": actual})
                    comparisons += 1
                    positive += bool(want)
                    negative += not want
                    accepted_streams += len(want)
        rows.append({"base": base, "padding": padding, "widths": widths})
    print(json.dumps({"status": "PASS", "method": "whole-integer fixed-width graph",
                      "maximum_period": args.period, "results": rows,
                      "solver_comparisons": comparisons, "positive_cases": positive,
                      "negative_cases": negative, "accepted_streams": accepted_streams,
                      "elapsed_seconds": round(time.monotonic() - started, 6)},
                     sort_keys=True))


if __name__ == "__main__":
    main()
