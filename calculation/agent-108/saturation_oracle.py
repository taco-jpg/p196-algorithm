#!/usr/bin/env python3
"""Independent tuple-valued positional oracle for neutral exterior cycles.

Cut state: (L, H, Y), with two period-length carry tuples and one base-b digit
per overflow time.  A column is a closed path in a layered graph of coefficient
values 0..2b-2.  This implementation builds those local graphs, computes suffix
reachability bitsets, then enumerates compatible labelled paths.  It does not
copy the production temporal DFS or its packed representation.

Both initial and ordinary visits to an identical cut are represented separately:
only the first column requires every phase coefficient to be nonzero.  Searches
which stop at a resource limit explicitly report an undecided status.

Public differential interface:
    successor_columns(base, pattern, state, first=False)
returns {next_cut: one_witness_column}.  Distinct columns inducing the same cut
are intentionally coalesced.  `brute_successor_columns` is a separate tiny-case
full-binary-carry oracle.  Neither uses packed integer cut keys.

CLI examples:
    python3 calculation/agent-108/saturation_oracle.py selftest
    python3 calculation/agent-108/saturation_oracle.py controls
    python3 calculation/agent-108/saturation_oracle.py search --g 100010001000

An accepted exterior witness is B-ONLY.  It supplies no common center cycle and
is not a decimal cycleOK certificate or a Lean proof.
"""

import argparse
from collections import deque
from functools import lru_cache
from itertools import product
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import time


class SearchDeadline(Exception):
    pass


class LocalRelationCap(Exception):
    pass


def checked_pattern(base, pattern):
    if type(base) is not int or not 2 <= base <= 36:
        raise ValueError("base must be an integer in 2..36")
    if isinstance(pattern, str):
        if not pattern or any(bit not in "01" for bit in pattern):
            raise ValueError("overflow pattern must be a nonempty binary string")
        bits = tuple(int(bit) for bit in pattern)
    elif isinstance(pattern, (tuple, list)):
        if not pattern or any(type(bit) is not int or bit not in (0, 1) for bit in pattern):
            raise ValueError("overflow pattern entries must be integer bits")
        bits = tuple(pattern)
    else:
        raise ValueError("overflow pattern must be a binary string or bit sequence")
    if len(bits) > 128:
        raise ValueError("this bounded oracle supports periods at most 128")
    return bits


def checked_state(base, bits, state):
    if not isinstance(state, (tuple, list)) or len(state) != 3:
        raise ValueError("cut must contain (L,H,Y)")
    if any(not isinstance(part, (tuple, list)) for part in state):
        raise ValueError("cut components must be sequences")
    low, high, partners = map(tuple, state)
    if len(low) != len(bits) or len(high) != len(bits) or len(partners) != sum(bits):
        raise ValueError("cut dimensions do not match overflow pattern")
    if any(type(bit) is not int or bit not in (0, 1) for bit in low + high):
        raise ValueError("carry entries must be integer bits")
    if any(type(digit) is not int or not 0 <= digit < base for digit in partners):
        raise ValueError("partner digits must lie in 0..base-1")
    return low, high, partners


@lru_cache(maxsize=None)
def local_arcs(base, low, required_high, overflow, partner, first):
    """Layer arcs indexed by the current coefficient.

    Arc label: (next coefficient, new reverse carry, new forward carry,
                reverse digit emitted by this coefficient).
    """
    table = []
    for coefficient in range(2 * base - 1):
        arcs = []
        if not first or coefficient != 0:
            forward_carry, forward_digit = divmod(coefficient + low, base)
            for incoming_reverse in (0, 1):
                outgoing_reverse, reverse_digit = divmod(coefficient + incoming_reverse, base)
                if outgoing_reverse == required_high:
                    next_coefficient = forward_digit + (partner if overflow else reverse_digit)
                    arcs.append((next_coefficient, incoming_reverse, forward_carry, reverse_digit))
        table.append(tuple(arcs))
    return tuple(table)


def _successor_columns(base, bits, state, first, deadline=None, local_cap=None):
    low, high, partners = state
    period = len(bits)
    layers = []
    partner_index = 0
    for phase, overflow in enumerate(bits):
        partner = partners[partner_index] if overflow else 0
        partner_index += overflow
        layers.append(local_arcs(base, low[phase], high[phase], overflow, partner, first))

    # suffix[t][x] is a bitset of final coefficients reachable from x at t.
    # This backward relation is independent of all labels accumulated later.
    coefficient_count = 2 * base - 1
    suffix = [None] * (period + 1)
    suffix[period] = tuple(1 << coefficient for coefficient in range(coefficient_count))
    for phase in range(period - 1, -1, -1):
        later = suffix[phase + 1]
        row = []
        for arcs in layers[phase]:
            reachable = 0
            for target, _, _, _ in arcs:
                reachable |= later[target]
            row.append(reachable)
        suffix[phase] = tuple(row)

    result = {}
    column = [0] * period
    new_low = [0] * period
    new_high = [0] * period
    new_partners = [0] * sum(bits)
    overflow_index = []
    count = 0
    for overflow in bits:
        overflow_index.append(count)
        count += overflow
    visits = 0

    def extend(phase, coefficient, starting_bit):
        nonlocal visits
        visits += 1
        if deadline is not None and visits % 256 == 0 and time.monotonic() >= deadline:
            raise SearchDeadline
        if phase == period:
            cut = tuple(new_low), tuple(new_high), tuple(new_partners)
            if local_cap is not None and cut not in result and len(result) >= local_cap:
                raise LocalRelationCap
            result.setdefault(cut, tuple(column))
            return
        column[phase] = coefficient
        for target, reverse_carry, forward_carry, reverse_digit in layers[phase][coefficient]:
            if not suffix[phase + 1][target] & starting_bit:
                continue
            new_low[phase] = forward_carry
            new_high[phase] = reverse_carry
            if bits[phase]:
                new_partners[overflow_index[phase]] = reverse_digit
            extend(phase + 1, target, starting_bit)

    for start in range(coefficient_count):
        if suffix[0][start] & (1 << start):
            extend(0, start, 1 << start)
    return result


def successor_columns(base, pattern, state, first=False):
    """Validated exact local relation; suitable for production differential tests."""
    bits = checked_pattern(base, pattern)
    cut = checked_state(base, bits, state)
    if type(first) is not bool:
        raise ValueError("first must be Boolean")
    return _successor_columns(base, bits, cut, first)


def brute_successor_columns(base, pattern, state, first=False):
    """Tiny-case oracle: enumerate the entire binary reverse-carry word first."""
    bits = checked_pattern(base, pattern)
    low, high, partners = checked_state(base, bits, state)
    if type(first) is not bool:
        raise ValueError("first must be Boolean")
    if len(bits) > 8:
        raise ValueError("full binary-carry oracle is restricted to period <=8")
    result = {}
    for carries in product((0, 1), repeat=len(bits)):
        for start in range(2 * base - 1):
            column = []
            coefficient = start
            partner_index = 0
            valid = True
            for phase, overflow in enumerate(bits):
                if first and coefficient == 0:
                    valid = False
                    break
                if (coefficient + carries[phase]) // base != high[phase]:
                    valid = False
                    break
                column.append(coefficient)
                other_digit = (coefficient + carries[phase]) % base
                if overflow:
                    other_digit = partners[partner_index]
                    partner_index += 1
                coefficient = (coefficient + low[phase]) % base + other_digit
            if not valid or coefficient != start:
                continue
            target = (
                tuple((value + low[phase]) // base for phase, value in enumerate(column)),
                carries,
                tuple((column[phase] + carries[phase]) % base
                      for phase, overflow in enumerate(bits) if overflow),
            )
            result.setdefault(target, tuple(column))
    return result


def is_accepting(base, bits, state):
    low, high, partners = state
    return (all(a + b == 1 for a, b in zip(low, high))
            and partners == tuple((base - 1) * low[phase]
                                  for phase, overflow in enumerate(bits) if overflow))


def reconstruct(base, period, parents, node):
    columns = []
    while parents[node][0] is not None:
        previous, column, _ = parents[node]
        columns.append(column)
        node = previous
    columns.reverse()
    words = [[column[phase] for column in columns] for phase in range(period)]
    for word in words:
        while word and word[-1] == base - 1:
            word.pop()
    return words


def mirror_check_witness(base, pattern, carry_pattern, words):
    """Replay a B-only witness with centers supplying the required carry.

    Those synthetic centers are independent per phase, so this check deliberately
    makes no claim about a shared center cycle or cycleOK acceptance.
    """
    bits = checked_pattern(base, pattern)
    if len(carry_pattern) != len(bits) or len(words) != len(bits):
        raise ValueError("witness dimensions do not match period")
    if any(type(carry) is not int or carry not in (0, 1) for carry in carry_pattern):
        raise ValueError("witness carry entries must be integer bits")
    if any(not isinstance(word, (tuple, list)) for word in words):
        raise ValueError("witness exterior words must be sequences")
    if any(type(value) is not int or not 0 <= value <= 2 * (base - 1)
           for word in words for value in word):
        raise ValueError("witness exterior coefficients must be bounded natural numbers")
    words = [list(word) for word in words]
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror
    trim_total = 0
    for phase, word in enumerate(words):
        expected_carry = carry_pattern[phase]
        center = [2 * (base - 1) if expected_carry == 0 else 0]
        if not mirror.hyp(base, word, center):
            raise RuntimeError(("Invalid witness source", phase, word))
        if mirror.e1(base, word) != expected_carry:
            raise RuntimeError(("Witness carry mismatch", phase))
        if mirror.gam(base, word, center) != bits[phase]:
            raise RuntimeError(("Witness overflow mismatch", phase))
        raw = mirror.nextB(base, word, center)
        target = words[(phase + 1) % len(bits)]
        trim = len(raw) - len(target)
        if trim < 0 or raw != target + [base - 1] * trim:
            raise RuntimeError(("Witness exterior transition mismatch", phase, raw, target))
        trim_total += trim
    if trim_total != sum(bits):
        raise RuntimeError("Closed witness violates exterior length telescoping")
    return {"edges": len(bits), "overflow_total": sum(bits), "exterior_trim_total": trim_total}


def search(base, pattern, state_cap=150000, depth_cap=200, seconds=30.0,
           stop_after=0, validate_witnesses=True):
    bits = checked_pattern(base, pattern)
    if type(state_cap) is not int or state_cap < 1:
        raise ValueError("state_cap must be a positive integer")
    if type(depth_cap) is not int or depth_cap < 0:
        raise ValueError("depth_cap must be a nonnegative integer")
    if seconds is not None and (type(seconds) not in (int, float)
                                or not math.isfinite(seconds) or seconds < 0):
        raise ValueError("seconds must be finite nonnegative or None")
    if type(stop_after) is not int or stop_after < 0:
        raise ValueError("stop_after must be a nonnegative integer")
    start_time = time.monotonic()
    deadline = None if seconds is None else start_time + seconds
    period = len(bits)
    initial_cut = ((0,) * period, bits, (1,) * sum(bits))
    initial = (initial_cut, True)
    parents = {initial: (None, None, 0)}
    frontier = deque([initial])
    accepted = {}
    processed = 0
    transitions = 0
    deepest = 0
    status = "EXHAUSTED"
    cap_kind = None
    while frontier:
        if deadline is not None and time.monotonic() >= deadline:
            status = "TIMEOUT"
            break
        node = frontier.popleft()
        state, first = node
        depth = parents[node][2]
        deepest = max(deepest, depth)
        processed += 1
        if is_accepting(base, bits, state) and state[0] not in accepted:
            words = reconstruct(base, period, parents, node)
            replay = mirror_check_witness(base, bits, state[0], words) if validate_witnesses else None
            accepted[state[0]] = {"depth": depth, "words": words, "mirror": replay}
            if stop_after and len(accepted) >= stop_after:
                status = "FOUND"
                break
        if depth >= depth_cap:
            status = "DEPTH_CAPPED"
            break
        try:
            successors = _successor_columns(base, bits, state, first, deadline, state_cap)
        except SearchDeadline:
            status = "TIMEOUT"
            break
        except LocalRelationCap:
            status = "STATE_CAPPED"
            cap_kind = "local_relation"
            break
        transitions += len(successors)
        for target, column in successors.items():
            target_node = (target, False)
            if target_node in parents:
                continue
            if len(parents) >= state_cap:
                status = "STATE_CAPPED"
                cap_kind = "visited_states"
                break
            parents[target_node] = (node, column, depth + 1)
            frontier.append(target_node)
        if status != "EXHAUSTED":
            break
    return {
        "base": base, "g": "".join(map(str, bits)), "status": status,
        "states": len(parents), "processed": processed, "depth": deepest,
        "transitions": transitions, "seconds": round(time.monotonic() - start_time, 6),
        "cap_kind": cap_kind,
        "accepted": {"".join(map(str, carry)): data for carry, data in sorted(accepted.items())},
        "ordinary_start_revisited": (initial_cut, False) in parents,
    }


def selftest():
    compared = 0
    initial_predecessor_checks = 0
    for base, max_period in ((2, 3), (3, 2)):
        for period in range(1, max_period + 1):
            for bits in product((0, 1), repeat=period):
                for low in product((0, 1), repeat=period):
                    for high in product((0, 1), repeat=period):
                        for partners in product(range(base), repeat=sum(bits)):
                            state = low, high, partners
                            for first in (False, True):
                                actual = successor_columns(base, bits, state, first)
                                brute = brute_successor_columns(base, bits, state, first)
                                if actual.keys() != brute.keys():
                                    raise RuntimeError(("Local differential mismatch", base, bits, state, first))
                                initial_cut = ((0,) * period, bits, (1,) * sum(bits))
                                zero_cut = ((0,) * period, (0,) * period, (0,) * sum(bits))
                                if (initial_cut in actual or zero_cut in actual) and state != zero_cut:
                                    raise RuntimeError("Unexpected initial/zero-cut predecessor")
                                initial_predecessor_checks += 1
                                compared += 1
    malformed = [
        lambda: checked_pattern(1, "1000"),
        lambda: checked_pattern(True, "1000"),
        lambda: checked_pattern(10, ""),
        lambda: checked_pattern(10, "1002"),
        lambda: checked_pattern(10, [1, 0.0]),
        lambda: checked_state(10, (1,), ((0,), (1,), (10,))),
        lambda: checked_state(10, (1,), ((2,), (1,), (1,))),
        lambda: checked_state(10, (1,), ((0, 1), (1,), (1,))),
        lambda: search(10, "1000", state_cap=0),
        lambda: search(10, "1000", depth_cap=-1),
        lambda: search(10, "1000", seconds=-1),
        lambda: search(10, "1000", seconds=float("nan")),
        lambda: search(10, "1000", seconds=float("inf")),
        lambda: mirror_check_witness(10, "1", (0,), [[-1]]),
    ]
    for invalid in malformed:
        try:
            invalid()
        except ValueError:
            pass
        else:
            raise RuntimeError("Malformed input was accepted")
    capped = search(10, "100010001000", state_cap=1)
    depth_limited = search(10, "1000", depth_cap=0)
    timed_out = search(10, "1000", seconds=0)
    if (capped["status"], depth_limited["status"], timed_out["status"]) != (
            "STATE_CAPPED", "DEPTH_CAPPED", "TIMEOUT"):
        raise RuntimeError("Resource-limit status regression")
    print(f"SELFTEST local_relations={compared} initial_predecessor_checks={initial_predecessor_checks} "
          f"malformed_rejections={len(malformed)} "
          "limit_statuses=STATE_CAPPED,DEPTH_CAPPED,TIMEOUT PASS")


def print_result(result, show_words=False):
    output = dict(result)
    if not show_words:
        output["accepted"] = {
            carry: {"depth": data["depth"], "widths": list(map(len, data["words"])),
                    "mirror": data["mirror"]}
            for carry, data in result["accepted"].items()
        }
    print(json.dumps(output, sort_keys=True), flush=True)


def controls(seconds, cap):
    for blocks in range(1, 6):
        result = search(10, "1000" * blocks, state_cap=cap, seconds=seconds)
        print_result(result)
        if result["status"] == "EXHAUSTED":
            expected_states = {1: 30, 2: 366, 3: 136653, 4: 13170, 5: 44160}
            if result["states"] != expected_states[blocks] or result["ordinary_start_revisited"]:
                raise RuntimeError("Unexpected saturated control reachability")
        if blocks == 3 and result["status"] == "EXHAUSTED":
            reference = "101010010101"
            expected = {reference[shift:] + reference[:shift] for shift in (0, 4, 8)}
            if set(result["accepted"]) != expected:
                raise RuntimeError("Unexpected p12 carry streams")
    result = search(10, "11100010000", state_cap=cap, seconds=seconds, stop_after=1)
    print_result(result)
    if result["status"] == "FOUND" and set(result["accepted"]) != {"10100110011"}:
        raise RuntimeError("Unexpected p11 carry stream")


def rotate_cut(state, blocks):
    """Rotate phase tuples by four times, overflow-partner tuple by one block."""
    low, high, partners = state
    shift = (4 * blocks) % len(low)
    partner_shift = blocks % len(partners)
    return (low[shift:] + low[:shift], high[shift:] + high[:shift],
            partners[partner_shift:] + partners[:partner_shift])


def replay_column(base, bits, source, target, column, first):
    """Independent explicit membership check for a chosen local witness."""
    low, high, partners = source
    next_low, reverse_carries, next_partners = target
    partner_index = 0
    for phase, coefficient in enumerate(column):
        if first and coefficient == 0:
            raise RuntimeError("Zero initial column coefficient")
        if (coefficient + reverse_carries[phase]) // base != high[phase]:
            raise RuntimeError("Column reverse carry mismatch")
        if (coefficient + low[phase]) // base != next_low[phase]:
            raise RuntimeError("Column forward carry mismatch")
        reverse_digit = (coefficient + reverse_carries[phase]) % base
        if bits[phase]:
            partner = partners[partner_index]
            if next_partners[partner_index] != reverse_digit:
                raise RuntimeError("Column partner mismatch")
            partner_index += 1
        else:
            partner = reverse_digit
        next_coefficient = (coefficient + low[phase]) % base + partner
        if next_coefficient != column[(phase + 1) % len(bits)]:
            raise RuntimeError("Column time-closure mismatch")


def production_differential(binary):
    """Compare the C++ --step relation, rotation equivariance and lifted witness."""
    generator = random.Random(1083208)
    relation_cases = 0
    rotation_cases = 0
    column_checks = 0
    nonempty_cases = 0
    for blocks in (1, 2, 3, 4, 5, 8, 10):
        bits = (1, 0, 0, 0) * blocks
        period = len(bits)
        initial = ((0,) * period, bits, (1,) * blocks)
        cases = [(initial, True), (initial, False)]
        first_successors = successor_columns(10, bits, initial, True)
        reachable = sorted(first_successors)
        samples = generator.sample(reachable, min(8, len(reachable)))
        cases.extend((state, False) for state in samples)
        if blocks <= 5:
            for state in samples[:2]:
                deeper = sorted(successor_columns(10, bits, state))
                cases.extend((cut, False) for cut in generator.sample(deeper, min(2, len(deeper))))
        for _ in range(12):
            state = (tuple(generator.randrange(2) for _ in bits),
                     tuple(generator.randrange(2) for _ in bits),
                     tuple(generator.randrange(10) for _ in range(blocks)))
            cases.append((state, bool(generator.randrange(2))))
        for state, first in cases:
            expected = successor_columns(10, bits, state, first)
            low_number = sum(bit << index for index, bit in enumerate(state[0]))
            high_number = sum(bit << index for index, bit in enumerate(state[1]))
            command = [binary, "--step", str(blocks), str(low_number), str(high_number),
                       ",".join(map(str, state[2])), str(int(first))]
            completed = subprocess.run(command, text=True, capture_output=True, timeout=10, check=True)
            decoded = json.loads(completed.stdout)
            actual = {
                (tuple((low >> index) & 1 for index in range(period)),
                 tuple((high >> index) & 1 for index in range(period)), tuple(partners))
                for low, high, partners in decoded
            }
            if actual != expected.keys():
                raise RuntimeError(("Production local-relation mismatch", command))
            relation_cases += 1
            nonempty_cases += bool(expected)
            for target, column in expected.items():
                replay_column(10, bits, state, target, column, first)
                column_checks += 1
            for shift in sorted({0, 1 % blocks, (blocks - 1) % blocks}):
                rotated = successor_columns(10, bits, rotate_cut(state, shift), first)
                predicted = {rotate_cut(target, shift) for target in expected}
                if rotated.keys() != predicted:
                    raise RuntimeError(("Rotational equivariance mismatch", blocks, shift, state))
                if is_accepting(10, bits, state) != is_accepting(10, bits, rotate_cut(state, shift)):
                    raise RuntimeError("Accepting predicate is not rotation invariant")
                rotation_cases += 1

    completed = subprocess.run(
        [binary, "3", "200000", "200", "20", "--quotient", "--witness"],
        text=True, capture_output=True, timeout=25, check=True)
    result = json.loads(completed.stdout.strip().splitlines()[-1])
    expected_carries = {"101010010101", "100101011010", "010110101001"}
    if result["status"] != "EXHAUSTED" or set(result["e"]) != expected_carries:
        raise RuntimeError("Production p12 quotient control did not exhaust expected streams")
    witness_rotations = 0
    witnessed_carries = set()
    for witness in result["witnesses"]:
        carry = tuple(map(int, witness["e"]))
        words = witness["B_t"]
        for shift in (0, 4, 8):
            rotated_carry = carry[shift:] + carry[:shift]
            rotated_words = words[shift:] + words[:shift]
            mirror_check_witness(10, "100010001000", rotated_carry, rotated_words)
            witnessed_carries.add("".join(map(str, rotated_carry)))
            witness_rotations += 1
    if witnessed_carries != expected_carries:
        raise RuntimeError("Lifted quotient witnesses miss a known carry rotation")
    print(f"PRODUCTION_DIFFERENTIAL local_relations={relation_cases} nonempty={nonempty_cases} "
          f"column_memberships={column_checks} rotation_relations={rotation_cases} "
          f"p12_lifted_witness_rotations={witness_rotations} PASS")


def block_word(state):
    """Encode a tuple cut as four-time MDD symbols, without losing correlations."""
    low, high, partners = state
    return tuple(
        sum(low[4 * block + phase] << phase for phase in range(4))
        + 16 * sum(high[4 * block + phase] << phase for phase in range(4))
        + 256 * partner
        for block, partner in enumerate(partners)
    )


def integer_witness_controls(base, pattern, carry_pattern, words):
    """Actual integer one-step checks, with multiple exterior/gap paddings.

    Synthetic centers supply the carry for each separate edge.  No center
    trajectory is being asserted.
    """
    bits = checked_pattern(base, pattern)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror

    def value(coefficients):
        total = 0
        for coefficient in reversed(coefficients):
            total = total * base + coefficient
        return total

    def reverse(number):
        result = 0
        while number:
            number, digit = divmod(number, base)
            result = base * result + digit
        return result

    def template(exterior, center, gap):
        neutral = [base - 1] * gap
        return value(exterior + neutral + center + neutral + exterior[::-1])

    checks = 0
    for phase, word in enumerate(words):
        center = [2 * (base - 1) if carry_pattern[phase] == 0 else 0]
        following = words[(phase + 1) % len(words)]
        for padding in (0, 1, 4):
            exterior = word + [base - 1] * padding
            target = following + [base - 1] * padding
            raw = mirror.nextB(base, exterior, center)
            trim = len(raw) - len(target)
            if trim < 0 or raw != target + [base - 1] * trim:
                raise RuntimeError("Padded B witness transition mismatch")
            next_center = mirror.nextC(base, exterior, center)
            for gap in (2, 5):
                current = template(exterior, center, gap)
                next_value = template(target, next_center, gap - bits[phase] + trim)
                if current + reverse(current) != next_value:
                    raise RuntimeError("Ordinary integer padded witness mismatch")
                checks += 1
    return checks


def mdd_differential(binary):
    """Complete reachable layer-set comparison for G1..5, through first accept.

    These layers retain cuts reached at different widths instead of globally
    deleting previously visited cuts.  This exactly matches MDD image semantics.
    """
    checked_layers = 0
    checked_words = 0
    integer_checks = 0
    mirror_edges = 0
    for blocks in range(1, 6):
        bits = (1, 0, 0, 0) * blocks
        command = [binary, str(blocks), "2000000", "100000000", "200", "30"]
        completed = subprocess.run(command + ["--witness"], text=True, capture_output=True,
                                   timeout=35, check=True)
        records = [json.loads(line) for line in completed.stdout.splitlines()]
        layers = [record for record in records if record["type"] == "LAYER"]
        result = next(record for record in records if record["type"] == "RESULT")
        expected_status = "FEASIBLE" if blocks == 3 else "EXHAUSTED_NO_B"
        if result["status"] != expected_status:
            raise RuntimeError(("Unexpected MDD control status", blocks, result))
        period = 4 * blocks
        frontier = {((0,) * period, bits, (1,) * blocks)}
        counts = []
        for layer in layers:
            depth = layer["depth"]
            if depth != len(counts):
                raise RuntimeError("MDD layer order mismatch")
            counts.append(len(frontier))
            accepted = sum(is_accepting(10, bits, state) for state in frontier)
            if len(frontier) != int(layer["states"]) or accepted != int(layer["accepts"]):
                raise RuntimeError(("MDD layer-count mismatch", blocks, depth, len(frontier), layer))
            exported = subprocess.run(command + ["--export-layer", str(depth)], text=True,
                                      capture_output=True, timeout=35, check=True)
            words = {tuple(word) for word in json.loads(exported.stdout.strip().splitlines()[-1])}
            expected_words = {block_word(state) for state in frontier}
            if words != expected_words:
                raise RuntimeError(("MDD complete layer-set mismatch", blocks, depth))
            checked_layers += 1
            checked_words += len(frontier)
            if depth + 1 < len(layers):
                frontier = {
                    target
                    for state in frontier
                    for target in _successor_columns(10, bits, state, depth == 0)
                }
        for witness in (record for record in records if record["type"] == "WITNESS"):
            carry = tuple(map(int, witness["e"]))
            words = witness["B_t"]
            for shift in (0, 4, 8):
                rotated_carry = carry[shift:] + carry[:shift]
                rotated_words = words[shift:] + words[:shift]
                replay = mirror_check_witness(10, bits, rotated_carry, rotated_words)
                mirror_edges += replay["edges"]
                integer_checks += integer_witness_controls(10, bits, rotated_carry, rotated_words)
        print(f"MDD_LAYERS G={blocks} counts={counts} exact_sets=PASS", flush=True)
    print(f"MDD_DIFFERENTIAL layers={checked_layers} layer_state_records={checked_words} "
          f"witness_mirror_edges={mirror_edges} padded_integer_transitions={integer_checks} PASS")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("selftest", "controls", "search", "differential", "mdd-differential"))
    parser.add_argument("--base", type=int, default=10)
    parser.add_argument("--g")
    parser.add_argument("--cap", type=int, default=150000)
    parser.add_argument("--depth", type=int, default=200)
    parser.add_argument("--seconds", type=float, default=30.0)
    parser.add_argument("--stop-after", type=int, default=0)
    parser.add_argument("--words", action="store_true")
    parser.add_argument("--binary")
    args = parser.parse_args()
    try:
        if args.mode == "selftest":
            selftest()
        elif args.mode == "controls":
            controls(args.seconds, args.cap)
        elif args.mode == "differential":
            if args.binary is None:
                parser.error("differential requires --binary")
            production_differential(args.binary)
        elif args.mode == "mdd-differential":
            if args.binary is None:
                parser.error("mdd-differential requires --binary")
            mdd_differential(args.binary)
        elif args.g is None:
            parser.error("search requires --g")
        else:
            print_result(search(args.base, args.g, args.cap, args.depth, args.seconds,
                                args.stop_after), show_words=args.words)
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
