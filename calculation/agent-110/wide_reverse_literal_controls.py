#!/usr/bin/env python3
"""Literal full-period controls for the period-64 reverse exterior extension.

This is a validator, not a P48 target search. Whole exterior words are replayed
as positional integers. Repetition never imposes closure at an interior seam.
The base6 two-lap exterior is Agent105's fixture in issue #289 comment6433504667:
https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433504667
Known full certificates remain credited to their existing Lean sources.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
import time

import p24_reverse_certificate as certificate
import p24_reverse_controls as literal
import p24_reverse_reference as reference

BASE6_ROWS = [[4, 7, 7, 8, 3], [9, 3, 4, 5, 8],
              [4, 7, 7, 10, 2, 2], [9, 3, 4, 9]]
BASE6_TRIMS = [0, 0, 2, 0]


def integer_exterior(base, coefficients):
    row = literal.word(base, coefficients)
    literal.require(not row or row[0] > 0, "nonpositive FIRST coefficient")
    modulus = base ** len(row)
    forward = sum(x * base ** j for j, x in enumerate(row))
    e, low = divmod(forward, modulus)
    reversed_value = sum(x * base ** (len(row) - 1 - j) for j, x in enumerate(row)) + 1 - e
    g, high = divmod(reversed_value, modulus)
    d = [(low // base ** j) % base for j in range(len(row))]
    r = [(high // base ** (len(row) - 1 - j)) % base for j in range(len(row))]
    if g:
        d.append((base - 1) * (1 - e))
        r.insert(0, 1)
    return e, g, [a + b for a, b in zip(d, r)]


def partition(g):
    starts = [t for t, bit in enumerate(g) if bit]
    literal.require(bool(starts), "block fixture needs an overflow")
    return [{"start": s, "length": (starts[(j + 1) % len(starts)] - s - 1) % len(g) + 1}
            for j, s in enumerate(starts)]


def block_symbols(g, cut):
    low, high, lag = cut
    answer = []
    for j, block in enumerate(partition(g)):
        start, length = block["start"], block["length"]
        ll = sum(((low >> ((start + k) % len(g))) & 1) << k for k in range(length))
        hh = sum(((high >> ((start + k) % len(g))) & 1) << k for k in range(length))
        answer.append(ll | (hh << length) | (lag[j] << (2 * length)))
    return tuple(answer)


def integer_cuts(base, e, g, rows):
    """Carry cuts from complete positional prefix/suffix integers."""
    e, g = literal.bits(e), literal.bits(g)
    literal.require(len(rows) == len(e) == len(g) and bool(rows), "word period mismatch")
    rows = [literal.word(base, row) for row in rows]
    width = len(rows[0])
    literal.require(width > 0 and all(len(row) == width and row[0] > 0 for row in rows),
                    "expected positive-FIRST equal-width words")
    for t, row in enumerate(rows):
        ee, gg, raw = integer_exterior(base, row)
        literal.require((ee, gg) == (e[t], g[t]) and
                        raw == rows[(t + 1) % len(rows)] + [base - 1] * g[t],
                        "whole-integer exterior edge failed")
    cuts = []
    for j in range(width + 1):
        low, high, lag = [], [], []
        for t, row in enumerate(rows):
            low.append(sum(row[k] * base ** k for k in range(j)) // base ** j)
            high.append((sum(row[k] * base ** (width - 1 - k) for k in range(j, width))
                         + 1 - e[t]) // base ** (width - j))
            if g[t]:
                lag.append(1 if j == 0 else (row[j - 1] + high[-1]) % base)
        cuts.append((sum(x << t for t, x in enumerate(low)),
                     sum(x << t for t, x in enumerate(high)), tuple(lag)))
    literal.require((cuts[0], cuts[-1]) == literal.root_and_terminal(base, e, g),
                    "integer-derived spatial boundaries disagree")
    for j, column in enumerate(zip(*rows)):
        literal.check_column(base, g, cuts[j], cuts[j + 1], column, first=j == 0)
    return cuts


def base6_control():
    e, g = [], []
    for t, row in enumerate(BASE6_ROWS):
        et, gt, raw = integer_exterior(6, row)
        literal.require(raw == BASE6_ROWS[(t + 1) % 4] + [5] * BASE6_TRIMS[t],
                        "Agent105 original base6 edge mismatch")
        e.append(et)
        g.append(gt)
    literal.require(e == g == [0, 1, 0, 1] and BASE6_ROWS[0] != BASE6_ROWS[2],
                    "base6 fixture is not a genuine two-lap exterior")
    padded = literal.padded_rows(6, BASE6_ROWS)
    literal.require(len(padded[0]) == 6, "wrong base6 common width")
    integer_cuts(6, e, g, padded)
    oracle = reference.Oracle(6, "01", "01")
    result, states = reference.backward(oracle, 32, reference.Budget(seconds=30, states=100000), export=True)
    literal.require(result["status"] == "EXHAUSTED" and result["complete"] is True,
                    "one-lap base6 fixed-driver exclusion was not completed")
    return {"status": "EXTERIOR_ONLY", "driver_period": 2, "exterior_period": 4,
            "original_integer_edges": 4, "padded_integer_edges": 4, "common_width": 6,
            "one_lap_status": result["status"], "one_lap_states": len(states),
            "one_lap_completed_layers": result["completed_layers"]}


def center_integer(base, row, e, g, trim):
    row = literal.word(base, row)
    total = sum(x * base ** j for j, x in enumerate(row)) + e
    carry, residue = divmod(total, base ** len(row))
    literal.require(carry == 1 - e, "center carry flip failed")
    digits = [(residue // base ** j) % base for j in range(len(row))]
    literal.require((digits, carry) == literal.mirror.norm(base, row, e), "center mirror normalization differs")
    if g:
        digits.append((base - 1) * e)
    raw = [x + y for x, y in zip(digits, digits[::-1])]
    literal.require(2 * trim <= len(raw), "invalid center trim width")
    if trim:
        literal.require(raw[:trim] == raw[-trim:] == [base - 1] * trim, "invalid neutral center trim")
        raw = raw[trim:-trim]
    return raw


def priority_center_control():
    e, g, v = (literal.bits(value * 2) for value in (literal.P24_E, literal.P24_G, literal.P24_V))
    centers = [literal.P24_C[:]]
    for et, gt, vt in zip(e, g, v):
        centers.append(center_integer(10, centers[-1], et, gt, vt))
    literal.require(centers[0] == centers[24] == centers[48], "repeated priority center failed")
    literal.require(centers[:-1] == literal.center_cycle(10, e, g, v, literal.P24_C),
                    "center replay differs from independent carry scan")
    return {"status": "CENTER_ONLY", "period": 48, "steps_checked": 48,
            "sum_g": sum(g), "sum_v": sum(v), "widths": sorted({len(row) for row in centers})}


def repeated_known_controls():
    examples, total_edges = [], 0
    known = literal.mirror._lean_certs()
    for base, original in known:
        repetitions = math.ceil(33 / len(original))
        rotated = original[1:] + original[:1]
        edges = rotated * repetitions
        rows = literal.padded_rows(base, [edge[0] for edge in edges])
        e = tuple(integer_exterior(base, edge[0])[0] for edge in edges)
        g = tuple(integer_exterior(base, edge[0])[1] for edge in edges)
        integer_cuts(base, e, g, rows)
        joined = literal.join_center(base, e, g, rows, [edge[1] for edge in edges], [edge[5] for edge in edges])
        total_edges += len(joined)
        examples.append({"base": base, "period": len(edges), "width": len(rows[0])})
    base8 = next(edges for base, edges in known if base == 8)
    for period in (48, 64):
        edges = (base8[1:] + base8[:1]) * (period // 8)
        rows = literal.padded_rows(8, [edge[0] for edge in edges])
        e = g = literal.bits("0001" * (period // 4))
        cuts = integer_cuts(8, e, g, rows)
        literal.require(any(mask & (1 << (period - 1)) for cut in cuts for mask in cut[:2]),
                        "high temporal carry bit was not exercised")
        blocks = partition(g)
        literal.require(blocks[-1]["start"] + blocks[-1]["length"] > period,
                        "last block did not cross the phase-zero boundary")
        literal.join_center(8, e, g, rows, [edge[1] for edge in edges], [edge[5] for edge in edges])
        total_edges += period
        examples.append({"base": 8, "period": period, "width": len(rows[0]),
                         "highest_bit": period - 1, "last_block": blocks[-1]})
    return {"accepted_repeated_known_cycles": len(examples), "full_mirror_edges": total_edges,
            "known_cycle_details": examples}


def artificial_column(base, g, column, low, incoming, old_lag):
    p = len(g)
    old_high, new_low, new_lag = [], [], []
    for t, x in enumerate(column):
        high, reverse_digit = divmod(x + incoming[t], base)
        next_low, forward_digit = divmod(x + low[t], base)
        expected = forward_digit + (old_lag[t] if g[t] else reverse_digit)
        literal.require(expected == column[(t + 1) % p], "artificial full-period recurrence failed")
        old_high.append(high)
        new_low.append(next_low)
        new_lag.append(reverse_digit)
    mask = lambda values: sum(x << t for t, x in enumerate(values))
    source = mask(low), mask(old_high), tuple(x for x, gt in zip(old_lag, g) if gt)
    target = mask(new_low), mask(incoming), tuple(x for x, gt in zip(new_lag, g) if gt)
    literal.check_column(base, g, source, target, column)
    data = {"base": base, "e": "0" * p, "g": "".join(map(str, g)),
            "blocks": partition(g), "root": 0,
            "nodes": [{"level": 0, "arcs": []}, {"level": sum(g), "arcs": []}]}
    checker = certificate.Checker(data, certificate.Budget(seconds=30))
    source_labels, target_labels = block_symbols(g, source), block_symbols(g, target)
    for j, block in enumerate(partition(g)):
        start, length = block["start"], block["length"]
        xs = tuple(column[(start + k) % p] for k in range(length))
        tile = xs[0], column[(start + length) % p], source_labels[j], xs
        literal.require(tile in checker.local_tiles(length, target_labels[j]), "wide local block tile omitted")
    return source, target


def reject_half_closure(base, g, source, target, column):
    half = len(g) // 2
    gh = g[:half]
    cut = lambda state: (state[0] & ((1 << half) - 1), state[1] & ((1 << half) - 1), state[2][:sum(gh)])
    try:
        literal.check_column(base, gh, cut(source), cut(target), column[:half])
    except ValueError:
        return
    raise ValueError("artificial path unexpectedly closed at the half-period seam")


def sparse_binary_fixture(period):
    mask = (1 << (period // 2)) | (1 << (period - 1))
    column = tuple(int(t in (period // 2, period - 1)) for t in range(period))
    target = mask, mask, (0,) * period
    expected = set()
    for a, b in itertools.product((0, 1), repeat=2):
        lag = [0] * period
        lag[period // 2 - 1], lag[period - 2] = 1 - a, 1 - b
        expected.add((mask | (a << (period // 2 - 1)) | (b << (period - 2)), mask, tuple(lag)))
    return column, target, expected


def artificial_controls():
    checks, exact_states = [], 0
    for period in (48, 64):
        column, expected_target, expected_predecessors = sparse_binary_fixture(period)
        g = (1,) * period
        source, target = artificial_column(2, g, column, column, column, column[1:] + column[:1])
        literal.require(target == expected_target, "sparse wide target mismatch")
        actual = literal.inverse_columns(2, g, target, cap=16)
        literal.require(set(actual) == expected_predecessors and all(xs == column for xs in actual.values()),
                        "wide exact four-predecessor fixture mismatch")
        reject_half_closure(2, g, source, target, column)
        exact_states += len(actual)
        checks.append({"base": 2, "period": period, "predecessors": len(actual),
                       "highest_carry_bit": period - 1, "half_period_closure": False})
    g = literal.bits(literal.P24_G * 2)
    column, low, incoming, lag = [0] * 48, [0] * 48, [0] * 48, [0] * 48
    for t, x in ((24, 1), (25, 1), (26, 1), (27, 2), (28, 4), (29, 8), (30, 9)):
        column[t] = x
    for t in (23, 29, 30):
        low[t] = 1
    incoming[30] = 1
    source, target = artificial_column(10, g, column, low, incoming, lag)
    reject_half_closure(10, g, source, target, column)
    checks.append({"base": 10, "period": 48, "rotation": 0, "half_period_closure": False})
    for shift in (5, 12):
        rotate = lambda values: tuple(values[(t - shift) % 48] for t in range(48))
        sr, tr = artificial_column(10, rotate(g), rotate(column), rotate(low), rotate(incoming), rotate(lag))
        literal.require(max(sr[0].bit_length(), sr[1].bit_length(), tr[0].bit_length(), tr[1].bit_length()) > 32,
                        "rotated decimal fixture missed high carry bits")
        checks.append({"base": 10, "period": 48, "rotation": shift,
                       "wrapped_last_block": partition(rotate(g))[-1]})
    return {"artificial_status": "INTERIOR_RELATION_ONLY", "artificial_columns": checks,
            "exact_sparse_predecessor_states": exact_states}


def join_witness(witness):
    base = witness["base"]
    e, g = literal.bits(witness["e"]), literal.bits(witness["g"])
    rows = witness.get("B_t", witness.get("B"))
    integer_cuts(base, e, g, rows)
    if "width" in witness:
        literal.require(type(witness["width"]) is int and witness["width"] == len(rows[0]), "wrong witness width")
    if "u" in witness:
        literal.require(all(type(x) is int for x in witness["u"]) and witness["u"] == list(g), "wrong fixed-width trims")
    choices = []
    if base == 10:
        ce, cg, cv = (literal.bits(s) for s in (literal.P24_E, literal.P24_G, literal.P24_V))
        cc = literal.center_cycle(10, ce, cg, cv, literal.P24_C)
        choices.append((ce, cg, cc, cv))
    else:
        for b, edges in literal.mirror._lean_certs():
            if b == base:
                choices.append((tuple(integer_exterior(base, edge[0])[0] for edge in edges),
                                tuple(integer_exterior(base, edge[0])[1] for edge in edges),
                                [edge[1] for edge in edges], tuple(edge[5] for edge in edges)))
    for ce, cg, cc, cv in choices:
        length = math.lcm(len(e), len(ce))
        for rotation in range(len(ce)):
            rotate = lambda values: values[rotation:] + values[:rotation]
            ee, gg = e * (length // len(e)), g * (length // len(g))
            if ee != rotate(ce) * (length // len(ce)) or gg != rotate(cg) * (length // len(cg)):
                continue
            repeated_rows = rows * (length // len(rows))
            centers = rotate(cc) * (length // len(cc))
            trims = rotate(cv) * (length // len(cv))
            integer_cuts(base, ee, gg, repeated_rows)
            edges = literal.join_center(base, ee, gg, repeated_rows, centers, trims)
            return {"status": "CANDIDATE" if base == 10 else "KNOWN_BASE_MIRROR_CYCLE",
                    "verification": "COMPUTED_PYTHON_MIRROR_ONLY", "base": base,
                    "exterior_period": len(e), "joined_period": length, "center_rotation": rotation,
                    "B": repeated_rows[0], "C": centers[0], "edges": edges}
    return {"status": "EXTERIOR_ONLY", "base": base, "period": len(e), "width": len(rows[0])}


def captured_preimages(records):
    total = 0
    for record in records:
        base, g = record["base"], literal.bits(record["g"])
        period = len(g)
        literal.require(base == 2 and period in (48, 64) and g == (1,) * period,
                        "unexpected artificial capture driver")
        literal.require(literal.bits(record["e"]) == (0,) * period, "unexpected capture e stream")
        column, target, expected = sparse_binary_fixture(period)
        literal.require(literal.state(base, g, record["target"]) == target, "capture target mismatch")
        exported = record.get("predecessors", record.get("states"))
        literal.require(isinstance(exported, list), "missing complete captured predecessor set")
        actual = {literal.state(base, g, row) for row in exported}
        literal.require(len(actual) == len(exported) and actual == expected, "captured complete preimage mismatch")
        for source in actual:
            literal.check_column(base, g, source, target, column)
        total += len(actual)
    return {"captured_preimage_sets": len(records), "captured_preimage_states": total}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--witnesses", type=Path, help="one WITNESS object or an array of scientific WITNESS objects")
    args = parser.parse_args()
    started = time.monotonic()
    result = {"base6_two_lap": base6_control(), "priority_center": priority_center_control()}
    result.update(repeated_known_controls())
    result.update(artificial_controls())
    if args.witnesses:
        data = json.loads(args.witnesses.read_text())
        if isinstance(data, dict) and "witnesses" in data:
            result.update(captured_preimages(data.get("preimage_controls", [])))
            data = data["witnesses"]
        elif isinstance(data, dict):
            data = [data]
        result["engine_witnesses"] = []
        result["engine_joined_mirror_edges"] = 0
        for witness in data:
            joined = join_witness(witness)
            if joined["status"] == "CANDIDATE":
                print(json.dumps(joined, separators=(",", ":")), flush=True)
                return 0
            result["engine_joined_mirror_edges"] += len(joined.get("edges", ()))
            joined.pop("edges", None)
            joined.pop("B", None)
            joined.pop("C", None)
            result["engine_witnesses"].append(joined)
        result["total_full_mirror_edges"] = result["full_mirror_edges"] + result["engine_joined_mirror_edges"]
    result.update(status="PASS", seconds=time.monotonic() - started)
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, TypeError, KeyError, IndexError, OSError, AssertionError,
            certificate.Incomplete, reference.Stop) as error:
        print(json.dumps({"status": "UNDECIDED", "reason": str(error)}), flush=True)
        raise SystemExit(2)
