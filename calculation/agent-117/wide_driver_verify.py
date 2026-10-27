#!/usr/bin/env python3
"""Independent arithmetic and arbitrary-integer checks for wide B-cut keys.

The frozen P24 module supplies data parsing and whole-word integer arithmetic.
The wide local inverse below directly enumerates temporal coefficient/carry
pairs; it does not use the optimized C++ gap formulas or packed-key code.
Caps are never reported as negative results.  --audit-exhaustion checks graph
metadata and optional independent-MDD counts, not a new full enumeration.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import time

import fixed_driver_verify as frozen
from p24_center_target import integer_norm, require


FORMAT = "agent117-wide-driver-exterior-v1"
BudgetExceeded = frozen.BudgetExceeded


def check_state(base, g, state):
    require(type(base) is int and 2 <= base <= 62, "base outside 2..62")
    frozen.check_bits(g, "overflow stream")
    require(1 <= len(g) <= 63 and sum(g) > 0, "period outside 1..63 or no overflow")
    width = (base - 1).bit_length()
    require(2 * len(g) + width * sum(g) <= 256, "key exceeds 256 bits")
    require(isinstance(state, (list, tuple)) and len(state) == 3, "invalid state shape")
    frozen.check_bits(state[0], "left carry", len(g))
    frozen.check_bits(state[1], "right carry", len(g))
    require(isinstance(state[2], (tuple, list)) and len(state[2]) == sum(g)
            and all(type(x) is int and 0 <= x < base for x in state[2]), "invalid active Y digits")
    return 2 * len(g) + width * sum(g)


def integer_key(base, g, state):
    """One Python integer is the reference; no limb-crossing special cases."""
    bits = check_state(base, g, state)
    p, width = len(g), (base - 1).bit_length()
    value = sum(bit << t for t, bit in enumerate(state[0]))
    value += sum(bit << (p + t) for t, bit in enumerate(state[1]))
    value += sum(digit << (2 * p + width * slot) for slot, digit in enumerate(state[2]))
    require(0 <= value < 1 << bits, "reference key exceeds advertised fields")
    return value


def integer_limbs(base, g, state):
    value = integer_key(base, g, state)
    return [(value >> (64 * i)) & ((1 << 64) - 1) for i in range(4)]


def verify_column(base, g, source, target, column):
    check_state(base, g, source)
    check_state(base, g, target)
    require(isinstance(column, (tuple, list)) and len(column) == len(g)
            and all(type(x) is int and 0 <= x <= 2 * base - 2 for x in column), "invalid coefficient column")
    slot = 0
    for t, coefficient in enumerate(column):
        low_carry, low = divmod(coefficient + source[0][t], base)
        high_carry, high = divmod(coefficient + target[1][t], base)
        require((low_carry, high_carry) == (target[0][t], source[1][t]), "column carry mismatch")
        if g[t]:
            require(target[2][slot] == high, "stored right digit mismatch")
            partner = source[2][slot]
            slot += 1
        else:
            partner = high
        require(column[(t + 1) % len(g)] == low + partner, "temporal coefficient mismatch")


def independent_predecessors(base, g, target, cap=100000, deadline=None):
    check_state(base, g, target)
    require(type(cap) is int and cap > 0, "nonpositive output cap")
    deadline = time.monotonic() + 30 if deadline is None else deadline
    p, slot = len(g), 0
    choices, by_x = [], []
    for t in range(p):
        options = []
        for x in range(2 * base - 1):
            high_carry, high_digit = divmod(x + target[1][t], base)
            if g[t] and high_digit != target[2][slot]:
                continue
            for left in (0, 1):
                new_left, low_digit = divmod(x + left, base)
                if new_left == target[0][t]:
                    options.append((x, left, high_carry, low_digit, high_digit))
        choices.append(options)
        by_x.append({x: [option for option in options if option[0] == x]
                     for x in range(2 * base - 1)})
        slot += g[t]
    if any(not values for values in choices):
        return {}
    row, outputs = [None] * p, {}

    def visit(t):
        if time.monotonic() > deadline:
            raise BudgetExceeded("wide predecessor wall cap")
        current = row[t]
        if t == p - 1:
            valid = (0 <= row[0][0] - current[3] < base) if g[t] else row[0][0] == current[3] + current[4]
            if valid:
                key = (tuple(option[1] for option in row), tuple(option[2] for option in row),
                       tuple(row[(k + 1) % p][0] - row[k][3] for k in range(p) if g[k]))
                frozen.retain_edge(outputs, key, tuple(option[0] for option in row), cap)
            return
        next_xs = range(current[3], current[3] + base) if g[t] else (current[3] + current[4],)
        for x in next_xs:
            for following in by_x[t + 1].get(x, ()):
                row[t + 1] = following
                visit(t + 1)

    for first in choices[0]:
        row[0] = first
        visit(0)
    return outputs


def independent_first_frontier(base, g, cap=100000, seconds=30):
    """Enumerate the actual positive physical first column without bit packing."""
    source = frozen.outer_state(g)
    check_state(base, g, source)
    deadline, p = time.monotonic() + seconds, len(g)
    row, inward, outputs = [0] * p, [0] * p, {}
    slot_at = {t: i for i, t in enumerate(t for t in range(p) if g[t])}

    def visit(t, x, first):
        if time.monotonic() > deadline:
            raise BudgetExceeded("physical first-column wall cap")
        if t == p:
            if x == first:
                target = (tuple(value // base for value in row), tuple(inward),
                          tuple((row[k] + inward[k]) % base for k in slot_at))
                frozen.retain_edge(outputs, target, row, cap)
            return
        if x == 0:
            return
        row[t] = x
        for carry in (0, 1):
            high_out, high_digit = divmod(x + carry, base)
            if high_out != g[t]:
                continue
            inward[t] = carry
            visit(t + 1, x % base + (1 if g[t] else high_digit), first)

    for first in range(1, 2 * base - 1):
        visit(0, first, first)
    for target, column in outputs.items():
        if time.monotonic() > deadline:
            raise BudgetExceeded("physical first-column validation wall cap")
        verify_column(base, g, source, target, column)
        require(all(x > 0 for x in column), "physical first row contains zero")
    return outputs


def verify_record(record, seconds=30, assemble=False):
    require(record.get("format") == FORMAT, "unknown wide record format")
    require(type(record.get("e")) is str and type(record.get("g")) is str, "missing streams")
    base, e, g = record.get("base"), tuple(map(int, record["e"])), tuple(map(int, record["g"]))
    terminal = frozen.terminal_state(base, e, g)
    bits = check_state(base, g, terminal)
    require(record.get("key_bits") == bits and record.get("key_storage_bits") == 256
            and record.get("period") == len(g) and record.get("overflow_count") == sum(g), "key layout metadata mismatch")
    if record.get("mode") == "key-roundtrip":
        state = frozen.unpack_state(record["state"])
        require(record.get("status") == "COMPLETE" and record.get("complete") is True, "key roundtrip incomplete")
        require(record.get("key_limbs") == integer_limbs(base, g, state), "wide limbs differ from arbitrary-integer key")
        return {"status": "KEY_LIMBS_VERIFIED", "key_bits": bits}
    if record.get("mode") == "predecessors":
        require(record.get("status") == "COMPLETE" and record.get("complete") is True, "predecessor relation incomplete")
        target = frozen.unpack_state(record["successor"])
        expected = independent_predecessors(base, g, target, deadline=time.monotonic() + seconds)
        supplied = {}
        for entry in record["predecessors"]:
            source = frozen.unpack_state(entry["state"])
            require(source not in supplied, "duplicate predecessor key")
            verify_column(base, g, source, target, entry["column"])
            supplied[source] = entry["column"]
        require(set(supplied) == set(expected), "exact predecessor sets differ")
        return {"status": "EXACT_PREDECESSOR_SET_VERIFIED", "key_bits": bits, "count": len(expected)}
    if record.get("status") != "ACCEPT":
        raise frozen.NoWitness("no full exterior witness; no negative re-enumerated")
    words = record["B"]
    width = frozen.verify_exterior_words(base, e, g, words)
    require(record.get("width") == width and record.get("u") == list(g), "word metadata mismatch")
    require(len(record["columns"]) == width and len(record["cuts"]) == width + 1, "cut/path length mismatch")
    cuts = list(map(frozen.unpack_state, record["cuts"]))
    require(cuts[0] == frozen.outer_state(g) and cuts[-1] == terminal, "wrong endpoint cut")
    for j, state in enumerate(cuts):
        require(state == frozen.word_cut(base, e, g, words, j), "cut differs from whole-word integer carries")
        if j < width:
            require(record["columns"][j] == [word[j] for word in words], "column transpose mismatch")
            verify_column(base, g, state, cuts[j + 1], record["columns"][j])
    result = {"status": "EXTERIOR_CYCLE_VERIFIED", "base": base, "period": len(g), "width": width,
              "key_bits": bits, "certificate_verified": False, "new_lean_verification": False}
    if assemble:
        from p42_center_target import E, G, assemble_candidate
        require(base == 10 and e == E and g == G, "wrong prescribed P42 driver")
        result = assemble_candidate(words)
    return result


def call_cpp(binary, base, e, g, mode, state=None, seconds=30):
    command = [binary, "--base", str(base), "--e", "".join(map(str, e)), "--g", "".join(map(str, g)),
               "--mode", mode, "--cap", "10000" if state is not None else "100000", "--seconds", str(int(seconds))]
    if state is not None:
        packed = frozen.pack_state(state)
        command += ["--L", packed["L"], "--H", packed["H"], "--Y", ",".join(map(str, packed["Y"]))]
    result = subprocess.run(command, text=True, capture_output=True, timeout=seconds + 5, check=True)
    return json.loads(result.stdout)


def cpp_key_controls(binary):
    cases = [(2, 1, 1), (10, 42, 16), (17, 42, 14), (2, 63, 63),
             (10, 32, 32), (10, 42, 42), (62, 63, 21), (62, 32, 32), (32, 58, 28)]
    counts, tested_bits = 0, set()
    for base, period, overflows in cases:
        g = (1,) * overflows + (0,) * (period - overflows)
        for pattern in range(4):
            if pattern < 2:
                left, right = (pattern,) * period, (1 - pattern,) * period
                digits = (pattern * (base - 1),) * overflows
            else:
                left = tuple((t + pattern) % 2 for t in range(period))
                right = tuple((t * 7 + pattern) % 3 == 0 for t in range(period))
                right = tuple(map(int, right))
                digits = tuple((slot * 13 + pattern * 7) % base for slot in range(overflows))
            state = left, right, digits
            record = call_cpp(binary, base, (0,) * period, g, "key-roundtrip", state)
            require(frozen.unpack_state(record["state"]) == state, "roundtrip state differs from supplied state")
            tested_bits.add(verify_record(record)["key_bits"])
            counts += 1
    rejected = 0
    invalid = [(10, 64, 16), (10, 43, 43), (62, 63, 22), (1, 1, 1), (63, 1, 1), (10, 42, 0)]
    for base, period, overflows in invalid:
        g = (1,) * overflows + (0,) * (period - overflows)
        command = [binary, "--base", str(base), "--e", "0" * period, "--g", "".join(map(str, g)),
                   "--mode", "key-roundtrip", "--L", "0" * period, "--H", "0" * period,
                   "--Y", ",".join("0" for _ in range(overflows)), "--cap", "10", "--seconds", "2"]
        process = subprocess.run(command, text=True, capture_output=True, timeout=5)
        require(process.returncode != 0, "unsupported numeric/key input accepted")
        rejected += 1
    return {"key_controls": "PASS", "exact_limb_cases": counts, "key_bits": sorted(tested_bits),
            "invalid_numeric_guards_rejected": rejected}


def wide_positive_predecessor(binary):
    edges = dict(frozen.load_lean_fixtures())[17]
    original_e = tuple(integer_norm(17, edge[0], 0)[1] for edge in edges)
    original_g = tuple(integer_norm(17, edge[0][::-1], 1 - original_e[t])[1] for t, edge in enumerate(edges))
    e, g = original_e * 7, original_g * 7
    width = max(len(edge[0]) for edge in edges) + 1
    words = [edge[0] + [16] * (width - len(edge[0])) for edge in edges] * 7
    frozen.verify_exterior_words(17, e, g, words)
    successor = frozen.word_cut(17, e, g, words, 1)
    record = call_cpp(binary, 17, e, g, "predecessors", successor)
    result = verify_record(record)
    require(frozen.outer_state(g) in independent_predecessors(17, g, successor), "genuine wide positive predecessor lost")
    result.update({"wide_positive_control": "PASS", "base": 17, "period": len(g), "true_word_width": width})
    return result


def known_cpp_controls(binary, mode):
    summaries = []
    for base, edges in sorted(frozen.load_lean_fixtures()):
        e = tuple(integer_norm(base, edge[0], 0)[1] for edge in edges)
        g = tuple(integer_norm(base, edge[0][::-1], 1 - e[t])[1] for t, edge in enumerate(edges))
        result = verify_record(call_cpp(binary, base, e, g, mode))
        summaries.append({key: result[key] for key in ("base", "period", "width", "key_bits")})
    return {"known_cpp_controls": "PASS", "mode": mode, "fixtures": summaries}


def audit_exhaustion(record, mdd_filename=None):
    require(record.get("format") == FORMAT and record.get("status") == "EXHAUSTED"
            and record.get("complete") is True and record.get("all_e_audit_complete") is True,
            "no completed forward exhaustion with accepting-cut audit")
    base, e, g = record["base"], tuple(map(int, record["e"])), tuple(map(int, record["g"]))
    bits = check_state(base, g, frozen.terminal_state(base, e, g))
    require(record.get("key_bits") == bits and record.get("key_storage_bits") == 256, "key metadata mismatch")
    ff, depth = record["forward_frontiers"], record["forward_complete_depth"]
    require(type(ff) is list and len(ff) == depth + 2 and ff[0] == 1 and ff[-1] == 0
            and all(type(x) is int and x > 0 for x in ff[:-1]), "invalid completed frontier sequence")
    require(sum(ff) == record["forward_visited"] == record["forward_expanded"], "incomplete forward accounting")
    require(record["initial_states"] == ff[1], "initial count mismatch")
    duplicate_count = record["forward_transitions"] - (record["forward_visited"] - 1)
    require(duplicate_count >= 0 and record["all_e_accepts"] == 0 and record["accepted_e_streams"] == []
            and record["accepting_forward_emissions"] == record["accepting_forward_expansions"] == 0,
            "acceptance or emission accounting mismatch")
    mdd_match = False
    if mdd_filename:
        rows = [json.loads(line) for line in Path(mdd_filename).read_text().splitlines() if line.strip()]
        layers = sorted((row for row in rows if row.get("type") == "LAYER"), key=lambda row: row["depth"])
        require([row["depth"] for row in layers] == list(range(len(ff))), "MDD depth sequence mismatch")
        require([int(row["states"]) for row in layers] == ff and all(int(row["accepts"]) == 0 for row in layers),
                "independent MDD layer/acceptance counts disagree")
        result = next(row for row in rows if row.get("type") == "RESULT")
        require(result.get("g") == record["g"] and result.get("period") == len(g)
                and result.get("reason") == "empty_layer", "different or incomplete MDD driver")
        mdd_match = True
    return {"status": "FORWARD_EXHAUSTION_METADATA_AUDITED", "period": len(g), "key_bits": bits,
            "frontiers": ff, "forward_records_including_provenance": sum(ff),
            "duplicate_forward_emissions": duplicate_count, "accepting_streams": 0,
            "independent_mdd_counts_match": mdd_match, "new_full_explicit_enumeration": False,
            "scope": "this temporal period/overflow word; all carry streams and finite widths",
            "new_lean_verification": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*")
    parser.add_argument("--key-controls", metavar="BINARY")
    parser.add_argument("--wide-control", metavar="BINARY")
    parser.add_argument("--known-controls", metavar="BINARY")
    parser.add_argument("--mode", choices=("forward", "search", "bidirectional"), default="bidirectional")
    parser.add_argument("--first-frontier", action="store_true")
    parser.add_argument("--audit-exhaustion", action="store_true")
    parser.add_argument("--mdd", metavar="JSONL")
    parser.add_argument("--assemble-target", action="store_true")
    parser.add_argument("--seconds", type=int, default=30)
    args = parser.parse_args()
    require(1 <= args.seconds <= 1500, "wall limit outside 1..1500")
    try:
        if args.key_controls:
            print(json.dumps(cpp_key_controls(args.key_controls)))
        if args.wide_control:
            print(json.dumps(wide_positive_predecessor(args.wide_control)))
        if args.known_controls:
            print(json.dumps(known_cpp_controls(args.known_controls, args.mode)))
        if args.first_frontier:
            from p42_center_target import G
            started = time.monotonic()
            frontier = independent_first_frontier(10, G, seconds=args.seconds)
            digest = hashlib.sha256(b"".join(integer_key(10, G, state).to_bytes(32, "little")
                                             for state in sorted(frontier, key=lambda state: integer_key(10, G, state)))).hexdigest()
            print(json.dumps({"physical_first_frontier": "COMPLETE", "states": len(frontier), "sha256_sorted_32byte_keys": digest,
                              "all_column_witnesses_replayed": True, "elapsed_seconds": round(time.monotonic() - started, 6)}))
        for filename in args.files:
            record = json.loads(Path(filename).read_text())
            result = audit_exhaustion(record, args.mdd) if args.audit_exhaustion else verify_record(record, args.seconds, args.assemble_target)
            print(json.dumps({"file": filename, **result}))
        if not (args.files or args.key_controls or args.wide_control or args.known_controls or args.first_frontier):
            parser.error("choose a control mode or provide witness JSON")
    except (BudgetExceeded, frozen.NoWitness, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "UNDECIDED", "reason": str(error)}))
        return 2
    except (ValueError, TypeError, KeyError, OSError) as error:
        print(json.dumps({"status": "INVALID", "reason": str(error)}))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
