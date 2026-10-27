#!/usr/bin/env python3
"""Find a spatial lasso extending the saturated temporal period-eight prefix.

Cut state: (L,H,Y), each a full tuple. L is the low carry into the next
column; H is the reverse carry required from that column; Y stores the
previous reverse digit at overflow phases 1,3,5,7. A spatial transition
emits one column x[0..7] and chooses the next inward carries Hnext[0..7].

Any reported lasso is a free-boundary prefix construction, NOT a finite B
cycle or a Lychrel certificate. Limits are reported as UNDECIDED.

    python3 calculation/agent-106/infinite_prefix.py
"""

import argparse
import json
from pathlib import Path
import re
import time


P = 8
G = tuple(t % 2 for t in range(P))
ODD = (1, 3, 5, 7)

# Fixed positive witness: each row is (temporal coefficient column, next H bits).
FIXED_ROOT_HIGH = (1, 0, 0, 0, 0, 1, 1, 0)
FIXED_STEM_LENGTH = 36
FIXED_ROWS = (((10, 2, 2, 4, 6, 13, 12, 5), '10001001'),
 ((10, 1, 3, 7, 11, 2, 6, 14), '01100110'),
 ((9, 9, 11, 2, 9, 9, 12, 4), '01010100'),
 ((7, 15, 5, 12, 5, 11, 1, 3), '01110100'),
 ((9, 18, 15, 11, 5, 10, 3, 6), '01110001'),
 ((7, 14, 14, 9, 2, 4, 5, 10), '00010001'),
 ((4, 9, 4, 10, 1, 2, 6, 12), '10100101'),
 ((11, 3, 13, 6, 7, 15, 8, 17), '10011010'),
 ((11, 4, 7, 15, 12, 5, 11, 3), '10011010'),
 ((11, 4, 8, 16, 13, 8, 13, 8), '11011110'),
 ((16, 14, 9, 18, 16, 14, 13, 8), '10011010'),
 ((10, 1, 6, 12, 12, 5, 10, 2), '00010110'),
 ((2, 5, 6, 12, 6, 13, 9, 0), '01010110'),
 ((5, 11, 7, 14, 8, 17, 12, 5), '10011001'),
 ((12, 4, 6, 13, 9, 9, 7, 16), '01101011'),
 ((9, 9, 14, 8, 12, 5, 15, 11), '01011010'),
 ((7, 16, 6, 14, 13, 7, 12, 5), '10100101'),
 ((13, 7, 14, 9, 4, 10, 8, 17), '11101000'),
 ((15, 12, 10, 1, 11, 2, 3, 7), '10000110'),
 ((9, 0, 3, 7, 8, 18, 11, 2), '10001001'),
 ((11, 3, 3, 7, 14, 9, 8, 18), '01101010'),
 ((8, 18, 12, 4, 11, 4, 14, 9), '10011010'),
 ((14, 9, 8, 18, 13, 7, 11, 4), '10100011'),
 ((9, 0, 10, 0, 9, 9, 16, 14), '10000011'),
 ((10, 1, 1, 3, 3, 7, 16, 14), '01010110'),
 ((6, 14, 6, 12, 6, 12, 10, 1), '10000001'),
 ((9, 9, 4, 9, 2, 5, 8, 17), '10101001'),
 ((10, 0, 10, 0, 10, 0, 5, 11), '00010110'),
 ((2, 6, 6, 13, 4, 9, 10, 0), '10010101'),
 ((10, 0, 6, 12, 7, 14, 4, 9), '01000101'),
 ((4, 10, 1, 2, 5, 11, 7, 14), '10001000'),
 ((11, 3, 4, 8, 10, 1, 3, 6), '11011000'),
 ((15, 12, 6, 12, 11, 3, 4, 9), '11010110'),
 ((15, 11, 5, 10, 4, 9, 13, 6), '01000100'),
 ((9, 9, 2, 4, 5, 11, 1, 3), '01011001'),
 ((8, 17, 8, 17, 12, 5, 7, 14), '01111001'),
 ((8, 16, 15, 11, 10, 1, 6, 12), '01110101'),
 ((9, 18, 16, 14, 7, 15, 7, 15), '01100110'),
 ((5, 11, 11, 3, 8, 17, 14, 9), '11011010'),
 ((17, 15, 8, 18, 12, 5, 13, 7), '10101001'),
 ((11, 4, 10, 1, 10, 1, 6, 13), '10100001'),
 ((12, 6, 10, 2, 3, 7, 8, 17), '10100010'),
 ((11, 3, 9, 0, 2, 4, 11, 3), '01100110'),
 ((4, 9, 13, 7, 7, 15, 10, 1), '01001001'),
 ((5, 11, 1, 3, 10, 0, 6, 13), '10010101'),
 ((12, 5, 7, 14, 8, 17, 8, 17), '10010111'),
 ((10, 1, 6, 12, 8, 16, 15, 11), '01010111'),
 ((7, 15, 7, 15, 9, 18, 16, 14), '01100110'),
 ((8, 17, 14, 9, 5, 11, 11, 3), '10101101'),
 ((12, 5, 13, 7, 17, 15, 8, 18), '10011010'),
 ((10, 1, 6, 13, 11, 4, 10, 1), '00011010'),
 ((3, 7, 8, 17, 12, 6, 10, 2), '00101010'),
 ((2, 4, 11, 3, 11, 3, 9, 0), '01100110'),
 ((7, 15, 10, 1, 4, 9, 13, 7), '10010100'),
 ((10, 0, 6, 13, 5, 11, 1, 3), '01011001'),
 ((8, 17, 8, 17, 12, 5, 7, 14), '01111001'))


def norm(word, incoming):
    out = []
    for x in word:
        out.append((x + incoming) % 10)
        incoming = (x + incoming) // 10
    return tuple(out), incoming


def profile():
    root = Path(__file__).resolve().parents[2]
    path = root / "lean/P196/Agent2SaturatedProfile/Saturated8CycleProfile.lean"
    text = path.read_text().split("def cycleState", 1)[1].split("theorem edge0", 1)[0]
    result = [tuple(map(int, m)) for m in re.findall(r"⟨(\d+),(\d+),(\d+)⟩", text)]
    if len(result) != P or any(len(word) != 3 or not 0 < word[0] <= 18 or
                              any(not 0 <= x <= 18 for x in word) for word in result):
        raise ValueError("invalid source three-column profile")
    return tuple(result)


def prefix_advance(word, high_in):
    low, _ = norm(word, 0)
    high_backwards, overflow = norm(word[::-1], high_in)
    high = high_backwards[::-1]
    if overflow == 0:
        return tuple(a + b for a, b in zip(low, high)), overflow
    return (low[0] + 1,) + tuple(low[i] + high[i - 1]
                                 for i in range(1, len(word))), overflow


def roots(words):
    low = tuple(norm(word, 0)[1] for word in words)
    result = []
    for mask in range(1 << P):
        high = tuple((mask >> t) & 1 for t in range(P))
        if all(prefix_advance(words[t], high[t]) == (words[(t + 1) % P], G[t])
               for t in range(P)):
            previous = tuple((words[t][-1] + high[t]) % 10 for t in ODD)
            result.append((low, high, previous))
    if len(result) != 16 or low != (1, 0, 0, 1, 0, 1, 1, 1):
        raise ValueError("source profile no longer yields the documented cut-3 roots")
    return result


def transitions(state):
    low, high, previous = state
    columns = [0] * P
    inward = [0] * P
    emitted = set()

    def walk(t, x, x0):
        if t == P:
            if x != x0:
                return
            next_low = tuple((columns[j] + low[j]) // 10 for j in range(P))
            next_high = tuple(inward)
            next_previous = tuple((columns[j] + inward[j]) % 10 for j in ODD)
            target = next_low, next_high, next_previous
            if target not in emitted:
                emitted.add(target)
                yield target, tuple(columns), tuple(inward)
            return
        for h in (0, 1):
            if (x + h) // 10 != high[t]:
                continue
            y = (x + low[t]) % 10
            y += previous[t // 2] if G[t] else (x + h) % 10
            assert 0 <= y <= 18
            columns[t], inward[t] = x, h
            yield from walk(t + 1, y, x0)

    for x0 in range(19):
        yield from walk(0, x0, x0)


class LimitReached(Exception):
    pass


def find_lasso(initial, cap, seconds):
    started = time.monotonic()
    colors = {}
    explored_edges = 0
    for root in initial:
        if root in colors:
            continue
        path = [root]
        labels = []
        position = {root: 0}
        colors[root] = 1
        stack = [iter(transitions(root))]
        while stack:
            if len(colors) > cap or time.monotonic() - started > seconds:
                raise LimitReached((len(colors), explored_edges, time.monotonic() - started))
            try:
                target, column, next_high = next(stack[-1])
            except StopIteration:
                finished = path.pop()
                position.pop(finished)
                colors[finished] = 2
                stack.pop()
                if labels:
                    labels.pop()
                continue
            explored_edges += 1
            if colors.get(target) == 1:
                start = position[target]
                edge_labels = labels + [(column, next_high)]
                return {
                    "root": root,
                    "stem_length": start,
                    "loop_length": len(path) - start,
                    "states": path + [target],
                    "columns": [label[0] for label in edge_labels],
                    "next_high": [label[1] for label in edge_labels],
                    "seen_states": len(colors),
                    "explored_edges": explored_edges,
                    "seconds": round(time.monotonic() - started, 6),
                }
            if target not in colors:
                colors[target] = 1
                position[target] = len(path)
                path.append(target)
                labels.append((column, next_high))
                stack.append(iter(transitions(target)))
    return {"status": "ACYCLIC", "seen_states": len(colors),
            "explored_edges": explored_edges,
            "seconds": round(time.monotonic() - started, 6)}


def verify_labels(witness):
    """Fail-closed certificate validation, including under python -O."""
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    def row(value, length, bound, name):
        require(isinstance(value, (tuple, list)) and len(value) == length,
                f"{name}: wrong shape")
        require(all(type(x) is int and 0 <= x <= bound for x in value),
                f"{name}: invalid entry")
        return tuple(value)

    def state(value, name):
        require(isinstance(value, (tuple, list)) and len(value) == 3,
                f"{name}: wrong cut-state shape")
        return (row(value[0], 8, 1, name + ".L"),
                row(value[1], 8, 1, name + ".H"),
                row(value[2], 4, 9, name + ".Y"))

    require(isinstance(witness, dict), "witness must be a dictionary")
    required = {"root", "stem_length", "loop_length", "states", "columns", "next_high"}
    require(required.issubset(witness), "missing witness field")
    for name in ("states", "columns", "next_high"):
        require(isinstance(witness[name], (tuple, list)), name + ": expected finite sequence")
    edge_count = len(witness["columns"])
    stem, loop = witness["stem_length"], witness["loop_length"]
    require(type(stem) is int and stem >= 0 and type(loop) is int and loop > 0,
            "invalid stem/loop lengths")
    require(stem + loop == edge_count, "stem plus loop must equal edge count")
    require(len(witness["states"]) == edge_count + 1 and
            len(witness["next_high"]) == edge_count, "mismatched witness array lengths")
    words = profile()
    if "profile" in witness:
        require(isinstance(witness["profile"], (tuple, list)) and len(witness["profile"]) == P,
                "witness profile: wrong shape")
        require(tuple(row(word, 3, 18, "profile row") for word in witness["profile"]) == words,
                "witness profile disagrees with source")
    require(all(word[0] != 0 for word in words), "prefix head must be nonzero")
    root = state(witness["root"], "root")
    require(root in roots(words), "root is not a legal cut-3 state")
    states = [state(s, f"state {i}") for i, s in enumerate(witness["states"])]
    require(states[0] == root, "initial state disagrees with root")
    for i in range(edge_count):
        column = row(witness["columns"][i], 8, 18, f"column {i}")
        inward = row(witness["next_high"][i], 8, 1, f"next H {i}")
        low, high, previous = states[i]
        nl, nh, ny = states[i + 1]
        require(inward == nh, f"edge {i}: next H disagreement")
        for t in range(P):
            require((column[t] + inward[t]) // 10 == high[t], f"edge {i}/{t}: reverse carry")
            require((column[t] + low[t]) // 10 == nl[t], f"edge {i}/{t}: low carry")
            wanted = (column[t] + low[t]) % 10
            wanted += previous[t // 2] if G[t] else (column[t] + inward[t]) % 10
            require(wanted == column[(t + 1) % P], f"edge {i}/{t}: temporal successor")
        require(ny == tuple((column[t] + inward[t]) % 10 for t in ODD),
                f"edge {i}: next previous-digit slots")
    require(states[-1] == states[stem], "spatial loop does not close")
    return True


def fixed_witness():
    words = profile()
    low = tuple(norm(word, 0)[1] for word in words)
    high = FIXED_ROOT_HIGH
    previous = tuple((words[t][-1] + high[t]) % 10 for t in ODD)
    states = [(low, high, previous)]
    columns, next_high = [], []
    for column, bits in FIXED_ROWS:
        inward = tuple(map(int, bits))
        nl = tuple((column[t] + states[-1][0][t]) // 10 for t in range(P))
        ny = tuple((column[t] + inward[t]) % 10 for t in ODD)
        states.append((nl, inward, ny))
        columns.append(column)
        next_high.append(inward)
    witness = {"root": states[0], "stem_length": FIXED_STEM_LENGTH,
               "loop_length": len(columns) - FIXED_STEM_LENGTH,
               "states": states, "columns": columns, "next_high": next_high,
               "profile": words, "origin": "fixed"}
    verify_labels(witness)
    return witness


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-cap", type=int, default=500000)
    parser.add_argument("--seconds", type=float, default=55)
    parser.add_argument("--search", action="store_true", help="rediscover a lasso instead of reading the fixed data")
    parser.add_argument("--json", action="store_true", help="print every certified cut state and edge")
    args = parser.parse_args()
    if not 0 < args.state_cap <= 500000 or not 0 < args.seconds <= 60:
        parser.error("require state cap in 1..500000 and time limit in (0,60]")
    words = profile()
    initial = roots(words)
    print("initial_cut3_states=" + str(len(initial)), flush=True)
    if args.search:
        try:
            result = find_lasso(initial, args.state_cap, args.seconds)
        except LimitReached as err:
            print("UNDECIDED " + repr(err.args[0]), flush=True)
            return
    else:
        result = fixed_witness()
    if "loop_length" not in result:
        print(json.dumps(result, separators=(",", ":")), flush=True)
        return
    verify_labels(result)
    result["profile"] = words
    print("SPATIAL_LASSO VERIFIED_LOCAL_EQUATIONS "
          f"stem_after_cut3={result['stem_length']} "
          f"spatial_preperiod={3 + result['stem_length']} "
          f"loop_columns={result['loop_length']}", flush=True)
    if args.search:
        print(f"partial_search_seen_states={result['seen_states']} "
              f"partial_search_explored_edges={result['explored_edges']} "
              f"seconds={result['seconds']}", flush=True)
    if args.json:
        print(json.dumps(result, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    main()
