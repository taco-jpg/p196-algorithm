#!/usr/bin/env python3
"""Independent arithmetic controls for the p12 balanced 24-step center map.

Uses the existing exact Python mirror for normalization and known certificates.
No finite control in this file establishes an all-width or all-period negative.
The optional C++ interface is: PROGRAM --map W; stdin IDs; stdout ID NEXT.
"""
import argparse
import json
import random
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror

E = tuple(map(int, "101010010101" * 2))
G = tuple(map(int, "100010001000" * 2))
V = tuple(sum(G[:t + 1]) // 2 - sum(G[:t]) // 2 for t in range(24))
START = 4


def value(word, base):
    result = 0
    for x in reversed(word):
        result = result * base + x
    return result


def center_step(base, center, incoming, overflow, trim, audit=False):
    """Literal finite-word arithmetic; None denotes a failed local guard."""
    center = tuple(center)
    if (not center or center != center[::-1]
            or any(x < 0 or x > 2 * (base - 1) for x in center)):
        return None
    digits, outgoing = mirror.norm(base, center, incoming)
    if audit:
        q, r = divmod(value(center, base) + incoming, base ** len(center))
        if q != outgoing or r != value(digits, base):
            raise RuntimeError("normalization disagrees with integer arithmetic")
    if outgoing != 1 - incoming:
        return None
    output_digits = digits + ([(base - 1) * incoming] if overflow else [])
    raw = tuple(a + b for a, b in zip(output_digits, reversed(output_digits)))
    if audit:
        if value(raw, base) != value(output_digits, base) + value(output_digits[::-1], base):
            raise RuntimeError("raw reflection disagrees with integer arithmetic")
        if raw != raw[::-1] or len(raw) != len(center) + overflow:
            raise RuntimeError("raw symmetry or width mismatch")
    if 2 * trim >= len(raw):
        return None
    if any(raw[i] != base - 1 or raw[-i - 1] != base - 1 for i in range(trim)):
        return None
    result = raw[trim:len(raw) - trim] if trim else raw
    if audit and result != result[::-1]:
        raise RuntimeError("trim broke reflection symmetry")
    return result


def decode(width, number):
    depth = (width - 1) // 2
    half = []
    for _ in range(depth):
        number, digit = divmod(number, 19)
        half.append(digit)
    if number:
        raise ValueError("state ID exceeds its width")
    inside = half + half[:(width - 2) // 2][::-1]
    return tuple([9] + inside + [9])


def encode(center):
    if len(center) < 2 or center[0] != 9 or center[-1] != 9:
        raise ValueError("state lacks forced neutral endpoints")
    half = center[1:1 + (len(center) - 1) // 2]
    return value(half, 19)


def reference_map(width, number, audit=False):
    current = decode(width, number)
    evaluated = 0
    for dt in range(24):
        t = (START + dt) % 24
        following = center_step(10, current, E[t], G[t], V[t], audit)
        evaluated += 1
        if following is None:
            return -1, evaluated
        if len(following) != len(current) + G[t] - 2 * V[t]:
            raise RuntimeError("incorrect step width")
        if len(following) not in (width - 1, width):
            raise RuntimeError("balanced width bound failed")
        current = following
    if len(current) != width or current[0] != 9 or current[-1] != 9:
        return -1, evaluated
    return encode(current), evaluated


def profile_controls():
    opposite = tuple(G[t] - V[t] for t in range(24))
    if any(E[t] != E[(t + 12) % 24] or G[t] != G[(t + 12) % 24]
           or opposite[t] != V[(t + 12) % 24] for t in range(24)):
        raise RuntimeError("phase-12 conjugacy failed")
    for profile, lower in ((V, 0), (opposite, -1)):
        height = 0
        heights = [height]
        for g, v in zip(G, profile):
            height += g - 2 * v
            heights.append(height)
        if height != 0 or set(heights) != {lower, lower + 1}:
            raise RuntimeError("two-width profile failed")
    if not (E[START] == G[START] == V[START] == 1):
        raise RuntimeError("phase four is not the forced-endpoint phase")
    return {"phase_shift": 12, "start_phase": START,
            "v": "".join(map(str, V)), "opposite": "".join(map(str, opposite))}


def arithmetic_controls(rng, samples):
    threshold_cases = 0
    for base in range(2, 63):
        for incoming in (0, 1):
            for a in range(2 * base - 1):
                trimmed = (a + incoming) % base + (base - 1) * incoming == base - 1
                if trimmed != (a == base - 1):
                    raise RuntimeError("forced-endpoint equation failed")
                threshold_cases += 1
    covariance = evaluations = survived = 0
    for i in range(samples):
        width = 2 + i % 29
        number = rng.randrange(19 ** ((width - 1) // 2))
        center = decode(width, number)
        if encode(center) != number:
            raise RuntimeError("independent codec round trip failed")
        inner = center[1:-1]
        for incoming in (0, 1):
            for overflow in (0, 1):
                image = center_step(10, inner, incoming, overflow, 0, True)
                padded = center_step(10, center, incoming, overflow, 0, True)
                if (image is None) != (padded is None):
                    raise RuntimeError("padding changed the carry-flip guard")
                if image is not None:
                    if padded != (9,) + image + (9,):
                        raise RuntimeError("neutral padding covariance failed")
                    covariance += 1
                    if overflow and center_step(10, center, incoming, 1, 1, True) != image:
                        raise RuntimeError("overflow neutral-pair cancellation failed")
        result, count = reference_map(width, number, True)
        evaluations += count
        survived += result >= 0
    known_edges = 0
    for base, edges in mirror._lean_certs():
        if not mirror.cycleOK(base, edges, edges[0][0], edges[0][1]):
            raise RuntimeError("known-source mirror control failed")
        for edge in edges:
            B, C, _, C2, _, trim = edge
            result = center_step(base, C, mirror.e1(base, B), mirror.gam(base, B, C), trim, True)
            if result != tuple(C2):
                raise RuntimeError("known-source center control failed")
            known_edges += 1
    return {"endpoint_equations": threshold_cases, "padded_sources": samples,
            "eligible_padding_edges": covariance, "reference_steps": evaluations,
            "reference_returns": survived, "known_source_edges": known_edges}


def compare_ids(binary, width, numbers):
    expected = {n: reference_map(width, n)[0] for n in numbers}
    command = [str(binary.resolve()), "--map", str(width)]
    run = subprocess.run(command, input="".join(f"{n}\n" for n in numbers),
                         text=True, capture_output=True, timeout=45, check=False)
    if run.returncode:
        raise RuntimeError(f"C++ map failed: {command}: {run.stderr}")
    actual = {}
    for line in run.stdout.splitlines():
        fields = line.split()
        if len(fields) != 2:
            raise RuntimeError(f"bad map output: {line!r}")
        source, target = map(int, fields)
        if source in actual:
            raise RuntimeError("duplicate map output ID")
        actual[source] = target
    if actual != expected:
        mismatch = next((n for n in numbers if actual.get(n) != expected[n]), None)
        raise RuntimeError(f"map mismatch width={width} ID={mismatch}: "
                           f"actual={actual.get(mismatch)} expected={expected.get(mismatch)}")
    return expected


def compare_binary(binary, rng, samples):
    remaining = samples
    summaries = []
    for width in range(2, 15):
        universe = 19 ** ((width - 1) // 2)
        count = universe if width <= 8 else (remaining + 14 - width) // (15 - width)
        if width > 8:
            remaining -= count
        if count == universe:
            numbers = list(range(universe))
        else:
            selected = {0, universe - 1} if count > 1 else {0}
            while len(selected) < count:
                selected.add(rng.randrange(universe))
            numbers = sorted(selected)
        expected = compare_ids(binary, width, numbers)
        summaries.append({"width": width, "states": count,
                          "exhaustive": count == universe,
                          "successful_returns": sum(n >= 0 for n in expected.values())})
    if remaining:
        raise RuntimeError("sample allocation failed")
    # Discovered by the primary census, independently evaluated here from every
    # coefficient. These are successful partial returns, not center cycles.
    groups = {
        1854137: (421084, 421255, 424333, 424504, 482815, 482986, 486064, 486235),
        1944526: (702607, 702778, 705856, 706027, 764338, 764509, 767587, 767758),
    }
    fixtures = {source: target for target, sources in groups.items() for source in sources}
    fixtures.update({target: -1 for target in groups})
    # The fixture expectations themselves must agree with the mirror reference.
    for source, target in fixtures.items():
        if reference_map(11, source, True)[0] != target:
            raise RuntimeError("positive-return fixture arithmetic failed")
    if compare_ids(binary, 11, sorted(fixtures)) != fixtures:
        raise RuntimeError("positive-return fixture C++ comparison failed")
    return {"width_batches": summaries,
            "fixture_states": len(fixtures), "fixture_successful_returns": 16,
            "fixture_dead_end_targets": len(groups),
            "total_map_comparisons": sum(row["states"] for row in summaries) + len(fixtures)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path)
    parser.add_argument("--samples", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=1102404)
    args = parser.parse_args()
    if args.samples < 100:
        parser.error("at least 100 samples are required")
    rng = random.Random(args.seed)
    result = {"profiles": profile_controls(),
              "arithmetic": arithmetic_controls(rng, args.samples)}
    if args.binary:
        result["binary_differential"] = compare_binary(args.binary, rng, args.samples)
    result["status"] = "PASS"
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
