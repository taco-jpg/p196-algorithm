#!/usr/bin/env python3
"""Independent controls for Agent 104's balanced-width center normalization.

For a valid cycle and W>=2 bounding both centers of every edge, pad a center C
on both sides by a=(W-len(C))//2 neutral coefficients.  The new center trim is
v+a_source-a_target.  Every new width is W-1 or W, and every new trim is 0 or 1.

Fixtures use all eight existing Lean-source certificates and the declared
Agent-104 PR #391 trim_transport.py dependency to create nonbinary source
schedules.  Edge replay is checked both with the exact mirror and with a
separate whole-integer normalization.  No files or logs are written.
Run with python3 -O: all guards use explicit exceptions, never assert.
"""

import copy
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
BASES = {2, 4, 8, 11, 16, 17, 26, 32}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def check_cap(width):
    require(type(width) is int and width >= 2, "W must be a natural integer >=2")


def natural_list(values, label):
    require(isinstance(values, (list, tuple)), label + " must be a sequence")
    require(all(type(value) is int and value >= 0 for value in values),
            label + " must contain natural integers, excluding bool")
    return list(values)


def load_dependencies():
    path = ROOT / "calculation/agent-104/trim_transport.py"
    spec = importlib.util.spec_from_file_location("a104_declared_trim_transport", path)
    require(spec is not None and spec.loader is not None, "cannot load #391 dependency")
    transport = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(transport)
    return transport.load_mirror(), transport


def integer_norm(base, word, carry):
    """Normalize by one whole-integer division, not by column carry recursion."""
    powers = [base ** i for i in range(len(word) + 1)]
    value = carry + sum(coefficient * powers[i] for i, coefficient in enumerate(word))
    final_carry, remainder = divmod(value, powers[-1])
    digits = [(remainder // powers[i]) % base for i in range(len(word))]
    require(value == final_carry * powers[-1]
            + sum(digit * powers[i] for i, digit in enumerate(digits)),
            "whole-integer normalization failed reconstruction")
    return digits, final_carry


def integer_edge(base, edge):
    """Check one complete edge using independent integer-valued normalizations."""
    B, C, B2, C2, u, v = edge
    h = base - 1
    require(base >= 2 and (not B or B[0] > 0), "integer edge has invalid base/head")
    require(all(0 <= coefficient <= 2*h for word in (B, C, B2, C2) for coefficient in word),
            "integer edge has an out-of-range coefficient")
    DB, e = integer_norm(base, B, 0)
    DC, f = integer_norm(base, C, e)
    DR, gamma = integer_norm(base, B[::-1], f)
    require(e in (0, 1) and f == 1-e and gamma in (0, 1),
            "integer edge fails complementary-carry conditions")
    if gamma:
        left, right = DB + [h*(1-e)], [1] + DR[::-1]
        middle_left, middle_right = DC + [h*(1-f)], [h*(1-f)] + DC[::-1]
    else:
        left, right = DB, DR[::-1]
        middle_left, middle_right = DC, DC[::-1]
    require(len(left) == len(right) and len(middle_left) == len(middle_right),
            "integer edge pairing widths disagree")
    raw_B = [x+y for x, y in zip(left, right)]
    raw_C = [x+y for x, y in zip(middle_left, middle_right)]
    require(raw_B == B2 + [h]*u, "integer exterior edge replay failed")
    require(raw_C == [h]*v + C2 + [h]*v, "integer center edge replay failed")
    return e, f, gamma


def checked_edge(mirror, base, edge):
    require(type(base) is int and base >= 2, "base must be a natural integer >=2")
    require(isinstance(edge, (list, tuple)) and len(edge) == 6,
            "an edge must contain six fields")
    words = [natural_list(word, "coefficient word") for word in edge[:4]]
    u, v = natural_list(edge[4:], "trim counts")
    result = (*words, u, v)
    require(mirror.edgeOK(base, result), "source edge fails exact mirror")
    return result


def balance_edge(mirror, base, edge, width):
    check_cap(width)
    B, C, B2, C2, u, v = checked_edge(mirror, base, edge)
    require(len(C) <= width, "W does not bound this edge's source center")
    require(len(C2) <= width, "W does not bound this edge's destination center")
    a, a2 = (width-len(C))//2, (width-len(C2))//2
    new_v = v + a - a2
    require(a >= 0 and a2 >= 0, "negative padding count")
    require(new_v >= 0, "negative transformed trim")
    require(new_v in (0, 1), "transformed trim is not binary")
    h = base - 1
    padded_C = [h]*a + C + [h]*a
    padded_C2 = [h]*a2 + C2 + [h]*a2
    result = (B, padded_C, B2, padded_C2, u, new_v)
    require(len(padded_C) in (width-1, width)
            and len(padded_C2) in (width-1, width), "transformed center width is unbalanced")
    require((result[0], result[2], result[4]) == (B, B2, u), "exterior fields changed")
    source_stream = integer_edge(base, (B, C, B2, C2, u, v))
    new_stream = integer_edge(base, result)
    require(new_stream == source_stream, "integer-replayed carry/overflow stream changed")
    require(new_stream == (mirror.e1(base, B), mirror.e2(base, B, padded_C),
                           mirror.gam(base, B, padded_C)), "integer and mirror streams disagree")
    require(new_v == int(source_stream[2] == 1 and len(padded_C) == width),
            "balanced trim is not the expected overflow/width bit")
    require(mirror.edgeOK(base, result), "transformed edge fails exact mirror")
    return result, new_stream


def balance_cycle(mirror, transport, base, edges, width):
    check_cap(width)
    source = transport.source_edges(mirror, base, edges)
    require(all(len(edge[1]) <= width and len(edge[3]) <= width for edge in source),
            "W does not bound every source and destination phase")
    result, streams = [], []
    for edge in source:
        new_edge, stream = balance_edge(mirror, base, edge, width)
        result.append(new_edge)
        streams.append(stream)
    require(all(result[i][2:4] == result[(i+1) % len(result)][:2]
                for i in range(len(result))), "transformed cycle does not close")
    require(mirror.cycleOK(base, result, result[0][0], result[0][1]),
            "transformed cycle fails exact mirror")
    require(sum(edge[5] for edge in result) == sum(edge[5] for edge in source),
            "total center trim changed")
    require(sum(edge[4] + edge[5] for edge in result)
            == sum(edge[4] + edge[5] for edge in source), "cycle gain changed")
    require(sum(stream[2] for stream in streams) <= sum(edge[4]+edge[5] for edge in result),
            "independent integer replay does not meet the gain condition")
    return result


def length_controls():
    count = 0
    for old_width in range(13):
        for gamma in (0, 1):
            for old_trim in range(7):
                next_width = old_width + gamma - 2*old_trim
                if next_width < 0:
                    continue
                minimum = max(2, old_width, next_width)
                for width in range(minimum, minimum+6):
                    a, a2 = (width-old_width)//2, (width-next_width)//2
                    trim = old_trim + a - a2
                    left, right = old_width + 2*a, next_width + 2*a2
                    require(a >= 0 and a2 >= 0 and trim in (0, 1),
                            "finite length arithmetic produced invalid padding/trim")
                    require(left in (width-1, width) and right in (width-1, width),
                            "finite length arithmetic produced an invalid width")
                    require(left + gamma == right + 2*trim, "balanced length identity fails")
                    require(trim == int(gamma == 1 and left == width),
                            "finite overflow/width trim identity fails")
                    count += 1
    return count


def rejection_controls(mirror, transport, fixtures):
    base, edges = fixtures[0]
    width = max(len(edge[j]) for edge in edges for j in (1, 3))
    bad_u = [(*edge[:4], -1, edge[5]) if i == 0 else edge for i, edge in enumerate(edges)]
    bad_v = [(*edge[:5], -1) if i == 0 else edge for i, edge in enumerate(edges)]
    bool_u = [(*edge[:4], False, edge[5]) if i == 0 else edge for i, edge in enumerate(edges)]
    bad_word = copy.deepcopy(edges)
    bad_word[0][1][0] = -1
    upward = next(((b, edge) for b, es in fixtures for edge in es
                   if len(edge[3]) > max(2, len(edge[1]))), None)
    downward = next(((b, edge) for b, es in fixtures for edge in es
                     if len(edge[1]) > max(2, len(edge[3]))), None)
    require(upward is not None and downward is not None, "missing local width-bound controls")
    tests = [("invalid cap " + repr(cap),
              lambda cap=cap: balance_cycle(mirror, transport, base, edges, cap))
             for cap in (-1, 0, 1, True, 2.0, "5", None, float("nan"))]
    tests += [
        ("global cap too small", lambda: balance_cycle(mirror, transport, base, edges, width-1)),
        ("local destination cap too small", lambda: balance_edge(mirror, upward[0], upward[1],
                                                                 max(2, len(upward[1][1])))),
        ("local source cap too small", lambda: balance_edge(mirror, downward[0], downward[1],
                                                            max(2, len(downward[1][3])))),
        ("negative exterior trim", lambda: balance_cycle(mirror, transport, base, bad_u, width)),
        ("negative center trim", lambda: balance_cycle(mirror, transport, base, bad_v, width)),
        ("boolean trim", lambda: balance_cycle(mirror, transport, base, bool_u, width)),
        ("negative coefficient", lambda: balance_cycle(mirror, transport, base, bad_word, width)),
        ("empty certificate", lambda: balance_cycle(mirror, transport, base, [], width)),
        ("missing certificate", lambda: balance_cycle(mirror, transport, base, None, width)),
        ("malformed edge", lambda: balance_cycle(mirror, transport, base, [edges[0][:5]], width)),
        ("broken return", lambda: balance_cycle(mirror, transport, base, edges[:-1], width)),
        ("invalid base", lambda: balance_cycle(mirror, transport, 1, edges, width)),
    ]
    for name, check in tests:
        try:
            check()
        except RuntimeError:
            continue
        raise RuntimeError("malformed input was accepted: " + name)
    return len(tests)


def source_variants(mirror, transport, base, edges, total):
    period = len(edges)
    targets = {(total,) + (0,)*(period-1), (0,)*(period-1) + (total,)}
    separated = [0]*period
    if total == 1:
        separated[period//2] = 1
    else:
        separated[0] = separated[period//2] = 1
        targets.add((1, 1) + (0,)*(period-2))
    targets.add(tuple(separated))
    yield edges
    for target in sorted(targets):
        variant, _ = transport.transport(mirror, base, edges, target)
        yield variant


def main():
    mirror, transport = load_dependencies()
    fixtures = sorted(mirror._lean_certs())
    require(len(fixtures) == 8 and {b for b, _ in fixtures} == BASES, "known source set changed")
    require(sum(len(edges) for _, edges in fixtures) == 56, "known source edge count changed")
    for base, edges in fixtures:
        transport.source_edges(mirror, base, edges)
        require(sum(edge[5] for edge in edges) == 1, "known source trim total changed")
    for carry in (0, 1):
        require(integer_norm(10, [], carry) == ([], carry), "empty integer normalization fails")
    arithmetic = length_controls()
    rejected = rejection_controls(mirror, transport, fixtures)
    source_count = nonbinary = cycles = edge_count = zero_trims = one_trims = 0
    max_source_trim = max_source_width = max_balanced_width = 0
    for base, original in fixtures:
        for repeat in (1, 2):
            rotations = list(transport.distinct_rotations(original * repeat))
            local_sources = local_cycles = 0
            for rotated in rotations:
                for source in source_variants(mirror, transport, base, rotated, repeat):
                    source_count += 1
                    local_sources += 1
                    nonbinary += int(any(edge[5] > 1 for edge in source))
                    max_source_trim = max(max_source_trim, max(edge[5] for edge in source))
                    maximum = max(len(edge[j]) for edge in source for j in (1, 3))
                    max_source_width = max(max_source_width, maximum)
                    require(maximum >= 2, "known fixture has no admissible tight W>=2")
                    for width in (maximum, maximum+1, maximum+2, maximum+5):
                        balanced = balance_cycle(mirror, transport, base, source, width)
                        cycles += 1
                        local_cycles += 1
                        edge_count += len(balanced)
                        zero_trims += sum(edge[5] == 0 for edge in balanced)
                        one_trims += sum(edge[5] == 1 for edge in balanced)
                        max_balanced_width = max(max_balanced_width, max(len(edge[1]) for edge in balanced))
            require(local_sources == len(rotations)*(4 if repeat == 1 else 5),
                    "fixture schedule coverage mismatch")
            require(local_cycles == 4*local_sources, "width-cap coverage mismatch")
            print("FIXTURE " + json.dumps({"base": base, "repetitions": repeat,
                  "P": len(original)*repeat, "distinct_rotations": len(rotations),
                  "source_variants": local_sources, "balanced_cycles": local_cycles,
                  "cap_offsets": [0, 1, 2, 5]}, sort_keys=True), flush=True)
    require(nonbinary > 0 and max_source_trim > 1, "no nonbinary source trims tested")
    require(zero_trims + one_trims == edge_count, "nonbinary output trim escaped coverage")
    print("BALANCED_WIDTH_PASS " + json.dumps({"status": "COMPUTED", "bases": 8,
          "source_edges": 56, "length_arithmetic_cases": arithmetic,
          "malformed_inputs_rejected": rejected, "source_variants": source_count,
          "nonbinary_source_variants": nonbinary, "balanced_cycles": cycles,
          "transformed_edge_replays": edge_count, "independent_integer_edge_replays": 2*edge_count,
          "zero_output_trims": zero_trims, "one_output_trims": one_trims,
          "max_source_trim": max_source_trim, "max_source_width": max_source_width,
          "max_balanced_width": max_balanced_width, "optimized_python": not __debug__},
          sort_keys=True), flush=True)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print("CHECK FAILED: " + str(error), file=sys.stderr)
        sys.exit(1)
