#!/usr/bin/env python3
"""Independent explicit inverse-column oracle for the exterior automaton.

State JSON is [Lmask,Hmask,[Y at increasing overflow positions]], with time 0
at bit 0.  For target (A,Q,Z), a predecessor column x and old low carry l obey
    (x+l)//b=A, old_h=(x+Q)//b;
    g=0: x_next=(x+l)%b+(x+Q)%b;
    g=1: (x+Q)%b=Z, old_y=x_next-(x+l)%b in [0,b-1].
The oracle enumerates closed paths in these small per-time coefficient graphs.
It uses neither packed automaton keys nor a block/MDD implementation.

The FIRST boundary (0,g,ones) requires every coefficient to be positive.  It
is kept separate from INTERIOR states, even if the same tuple appears later.
Backward layer D is the complete Pre^D({terminal}), including older layers:
the terminal has its neutral self-loop.  Reaching a requested depth is only
UNDECIDED unless an exact fixed point or a replayed exterior witness is found.
Caps, timeout and partial expansions never establish a negative.

--first and --export-layer D export a JSON array of complete state sets.
--preimage reads such an array on stdin and exports its exact interior preimage.
An incomplete export prints an UNDECIDED object instead of a partial array.
"""
import argparse
import ast
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import resource
import subprocess
import sys
import time

TARGET_E = "010100110100101011001011"
TARGET_G = "110001001000110001001000"
ROOT = Path(__file__).resolve().parents[2]


class Stop(Exception):
    pass


class Budget:
    def __init__(self, seconds=60, states=200000):
        self.started = time.monotonic()
        self.seconds = seconds
        self.states = states
        self.nodes = 0

    def check(self):
        if time.monotonic() - self.started >= self.seconds:
            raise Stop("time cap")

    def tick(self):
        self.nodes += 1
        if self.nodes % 1024 == 0:
            self.check()

    def insert(self, container, state, value=None):
        if state in container:
            return False
        if len(container) >= self.states:
            raise Stop("state cap")
        if isinstance(container, dict):
            container[state] = value
        else:
            container.add(state)
        return True


def bits(word):
    return sum(int(digit) << t for t, digit in enumerate(word))


def digest(states):
    """SHA256 of sorted compact JSON state rows, each followed by LF."""
    result = hashlib.sha256()
    for state in sorted(states):
        result.update((json.dumps(state, separators=(",", ":")) + "\n").encode())
    return result.hexdigest()


class Oracle:
    def __init__(self, base, e, g):
        if not 2 <= base <= 62:
            raise ValueError("base must be 2..62")
        if not 1 <= len(g) <= 32 or len(e) != len(g) or set(e + g) - {"0", "1"}:
            raise ValueError("e/g must be equal-length binary words of length 1..32")
        self.base, self.e, self.g = base, e, g
        self.p = len(g)
        self.positions = tuple(t for t, c in enumerate(g) if c == "1")
        self.yindex = {t: j for j, t in enumerate(self.positions)}
        self.start = (0, bits(g), (1,) * len(self.positions))
        self.terminal = (bits(e), ((1 << self.p) - 1) ^ bits(e),
                         tuple((base - 1) * int(e[t]) for t in self.positions))

    def state(self, row):
        if not isinstance(row, (list, tuple)) or len(row) != 3:
            raise ValueError("state must have L,H,Y entries")
        low, high, lag = row
        if type(low) is not int or type(high) is not int or not isinstance(lag, (list, tuple)):
            raise ValueError("invalid state entry types")
        if not 0 <= low < 1 << self.p or not 0 <= high < 1 << self.p:
            raise ValueError("carry mask outside period")
        if len(lag) != len(self.positions) or any(type(x) is not int or not 0 <= x < self.base for x in lag):
            raise ValueError("invalid lag digits")
        return low, high, tuple(lag)

    def inverse_columns(self, target, first=False, budget=None):
        """Yield (predecessor tuple, coefficient column); duplicate tuples possible."""
        b, p = self.base, self.p
        aa, qq, zz = self.state(target)
        allowed = []
        for t in range(p):
            a, q = aa >> t & 1, qq >> t & 1
            by_x = {}
            for x in range(int(first), 2 * b - 1):
                if self.g[t] == "1" and (x + q) % b != zz[self.yindex[t]]:
                    continue
                ls = tuple(l for l in (0, 1) if (x + l) // b == a)
                if ls:
                    by_x[x] = ls
            allowed.append(by_x)
        tables = []
        for t in range(p):
            q = qq >> t & 1
            following = allowed[(t + 1) % p]
            by_x = {}
            for x, ls in allowed[t].items():
                h, digit = divmod(x + q, b)
                options = []
                for l in ls:
                    low_digit = (x + l) % b
                    if self.g[t] == "1":
                        for nx in following:
                            y = nx - low_digit
                            if 0 <= y < b:
                                options.append((nx, l, h, y))
                    else:
                        nx = low_digit + digit
                        if nx in following:
                            options.append((nx, l, h, 0))
                by_x[x] = options
            tables.append(by_x)
        column = [0] * p
        lag = [0] * len(self.positions)
        for initial in allowed[0]:
            # Exact suffix reachability prunes only paths that cannot close.
            viable = [set() for _ in range(p + 1)]
            viable[p].add(initial)
            for t in range(p - 1, -1, -1):
                viable[t] = {x for x, opts in tables[t].items()
                             if any(nx in viable[t + 1] for nx, _, _, _ in opts)}
            if initial not in viable[0]:
                continue

            def visit(t, x, low_mask, high_mask):
                if budget is not None:
                    budget.tick()
                if t == p:
                    yield (low_mask, high_mask, tuple(lag)), tuple(column)
                    return
                column[t] = x
                for nx, l, h, y in tables[t][x]:
                    if nx not in viable[t + 1]:
                        continue
                    if self.g[t] == "1":
                        lag[self.yindex[t]] = y
                    yield from visit(t + 1, nx, low_mask | l << t, high_mask | h << t)

            yield from visit(0, initial, 0, 0)

    def forward_columns(self, source, first=False, budget=None):
        """Independent forward DFS using given old carries and guessed new H."""
        low, high, lag = self.state(source)
        b, p = self.base, self.p
        xs = [0] * p
        ys = [0] * len(self.positions)
        for initial in range(int(first), 2 * b - 1):
            def visit(t, x, new_low, new_high):
                if budget is not None:
                    budget.tick()
                if t == p:
                    if x == initial:
                        yield (new_low, new_high, tuple(ys)), tuple(xs)
                    return
                if first and x == 0:
                    return
                xs[t] = x
                a, digit = divmod(x + (low >> t & 1), b)
                for q in (0, 1):
                    h, reverse_digit = divmod(x + q, b)
                    if h != (high >> t & 1):
                        continue
                    if self.g[t] == "1":
                        ys[self.yindex[t]] = reverse_digit
                        nx = digit + lag[self.yindex[t]]
                    else:
                        nx = digit + reverse_digit
                    yield from visit(t + 1, nx, new_low | a << t, new_high | q << t)
            yield from visit(0, initial, 0, 0)

    def first(self, budget):
        result = {}
        for target, column in self.forward_columns(self.start, True, budget):
            budget.insert(result, target, column)
        return result

    def integer_step(self, word):
        """Whole positional integer arithmetic; no local transition recurrence."""
        b, width = self.base, len(word)
        modulus = b ** width
        value = sum(x * b ** j for j, x in enumerate(word))
        e, residue = divmod(value, modulus)
        reverse_value = sum(x * b ** (width - 1 - j) for j, x in enumerate(word)) + 1 - e
        g, reverse_residue = divmod(reverse_value, modulus)
        low_digits = [(residue // b ** j) % b for j in range(width)]
        high_digits = [(reverse_residue // b ** (width - 1 - j)) % b for j in range(width)]
        if g:
            low_digits.append((b - 1) * (1 - e))
            high_digits.insert(0, 1)
        return tuple(a + c for a, c in zip(low_digits, high_digits)), e, g

    def replay(self, columns):
        words = [tuple(column[t] for column in columns) for t in range(self.p)]
        if not columns or any(word[0] == 0 for word in words):
            raise ValueError("witness violates positive FIRST")
        for t, word in enumerate(words):
            raw, e, g = self.integer_step(word)
            expected = words[(t + 1) % self.p] + (self.base - 1,) * int(self.g[t])
            if (raw, e, g) != (expected, int(self.e[t]), int(self.g[t])):
                raise ValueError("whole-integer exterior witness replay failed")
        return words


def preimage(oracle, targets, budget):
    answer = set()
    for target in sorted(targets):
        budget.check()
        for source, _ in oracle.inverse_columns(target, budget=budget):
            budget.insert(answer, source)
    return answer


def backward(oracle, depth, budget, export=False):
    terminal = oracle.terminal
    first = oracle.first(budget)
    seen = {terminal: None}
    frontier = {terminal}
    layers = [{"depth": 0, "novel": 1, "cumulative": 1, "sha256": digest(seen)}]
    hit = terminal if terminal in first else None
    completed = 0
    partial = False
    reason = "requested backward layer limit"

    def attach_witness(result):
        columns = [first[hit]]
        state = hit
        while seen[state] is not None:
            target, column = seen[state]
            columns.append(column)
            state = target
        result.update(B=oracle.replay(columns), direct_integer_replay=True)

    try:
        while completed < depth and frontier and (export or hit is None):
            fresh = set()
            for target in sorted(frontier):
                budget.check()
                partial = True
                for source, column in oracle.inverse_columns(target, budget=budget):
                    if budget.insert(seen, source, (target, column)):
                        fresh.add(source)
                        if source in first and hit is None:
                            hit = source
                partial = False
            frontier = fresh
            completed += 1
            layers.append({"depth": completed, "novel": len(frontier),
                           "cumulative": len(seen), "sha256": digest(seen)})
            if not export:
                print(json.dumps({"layer": layers[-1]}, sort_keys=True), flush=True)
    except (Stop, MemoryError) as error:
        reason = str(error) or "memory cap"
        result = {"status": "UNDECIDED", "reason": reason, "complete": False,
                  "partial_expansion": partial, "completed_layers": completed,
                  "states": len(seen), "layers": layers}
        # A later resource stop cannot invalidate a concrete earlier witness.
        # Export completeness is still undecided, so never emit a partial array.
        if hit is not None:
            attach_witness(result)
            if not export:
                result.update(status="EXTERIOR_ACCEPT", reason="whole-integer replayed witness before resource stop",
                              stop_reason=reason)
        return result, None
    result = {"status": "UNDECIDED", "reason": reason, "complete": False,
              "partial_expansion": False, "completed_layers": completed,
              "states": len(seen), "first_frontier": len(first), "layers": layers}
    if hit is not None:
        attach_witness(result)
        result.update(status="EXTERIOR_ACCEPT", reason="whole-integer replayed witness",
                      direct_integer_replay=True)
    elif not frontier:
        result.update(status="EXHAUSTED", reason="exact backward fixed point disjoint from FIRST",
                      complete=True)
    return result, set(seen) if completed == depth or not frontier else None


def brute_forward(oracle, source, first):
    """Small-control oracle: enumerate every complete guessed-H word first."""
    low, high, lag = source
    p, b = oracle.p, oracle.base
    result = set()
    for guessed in itertools.product((0, 1), repeat=p):
        for initial in range(int(first), 2 * b - 1):
            x = initial
            target_l = 0
            target_y = []
            for t, q in enumerate(guessed):
                if first and x == 0 or (x + q) // b != (high >> t & 1):
                    break
                target_l |= ((x + (low >> t & 1)) // b) << t
                digit = (x + q) % b
                if oracle.g[t] == "1":
                    target_y.append(digit)
                    nx = (x + (low >> t & 1)) % b + lag[oracle.yindex[t]]
                else:
                    nx = (x + (low >> t & 1)) % b + digit
                x = nx
            else:
                if x == initial:
                    result.add((target_l, sum(q << t for t, q in enumerate(guessed)), tuple(target_y)))
    return result


def positive_controls(budget):
    path = ROOT / "lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean"
    source = path.read_text()
    certificates = columns_checked = integer_edges = 0
    for base in (2, 4, 8, 16, 32):
        block = re.search(r"def cert" + str(base) + r" : List Edge :=(.*?)(?=\ndef |\ntheorem )",
                          source, re.S).group(1)
        rows = re.findall(r"⟨(\[[^\]]*\]),\s*\[[^\]]*\],\s*(\[[^\]]*\]),\s*\[[^\]]*\],\s*(\d+),\s*\d+⟩", block)
        words = [tuple(ast.literal_eval(row[0])) for row in rows]
        placeholder = Oracle(base, "0" * len(words), "0" * len(words))
        streams = []
        for t, (word, row) in enumerate(zip(words, rows)):
            raw, e, g = placeholder.integer_step(word)
            following = tuple(ast.literal_eval(row[1]))
            if following != words[(t + 1) % len(words)] or raw != following + (base - 1,) * int(row[2]):
                raise RuntimeError("literal positive certificate exterior edge failed")
            streams.append((e, g))
            integer_edges += 1
        e = "".join(str(pair[0]) for pair in streams)
        g = "".join(str(pair[1]) for pair in streams)
        oracle = Oracle(base, e, g)
        width = max(map(len, words))
        padded = [word + (base - 1,) * (width - len(word)) for word in words]
        columns = [tuple(word[j] for word in padded) for j in range(width)]
        oracle.replay(columns)
        cuts = []
        for j in range(width + 1):
            lows, highs = [], []
            for t, word in enumerate(padded):
                lows.append(sum(word[k] * base ** k for k in range(j)) // base ** j)
                highs.append((sum(word[k] * base ** (width - 1 - k) for k in range(j, width))
                              + 1 - int(e[t])) // base ** (width - j))
            lag = tuple(1 if j == 0 else (padded[t][j - 1] + highs[t]) % base
                        for t in oracle.positions)
            cuts.append((sum(v << t for t, v in enumerate(lows)),
                         sum(v << t for t, v in enumerate(highs)), lag))
        if cuts[0] != oracle.start or cuts[-1] != oracle.terminal:
            raise RuntimeError("integer-derived positive cut boundary mismatch")
        for j, column in enumerate(columns):
            expected = (cuts[j], column)
            if expected not in set(oracle.inverse_columns(cuts[j + 1], first=j == 0, budget=budget)):
                raise RuntimeError("known positive column missing from inverse relation")
            columns_checked += 1
        certificates += 1
    return {"certificates": certificates, "inverse_columns": columns_checked,
            "direct_integer_edges": integer_edges}


def mdd_query(binary, oracle, flags, budget, targets=None):
    budget.check()
    command = [str(binary.resolve()), str(oracle.base), oracle.e, oracle.g] + flags
    try:
        run = subprocess.run(command, input=None if targets is None else json.dumps(sorted(targets)),
                             text=True, capture_output=True, check=False,
                             timeout=max(0.001, budget.seconds - (time.monotonic() - budget.started)))
    except subprocess.TimeoutExpired as error:
        raise Stop("MDD control subprocess timeout") from error
    if run.returncode != 0:
        raise RuntimeError("MDD control failed: " + run.stderr[:500] + run.stdout[:500])
    rows = json.loads(run.stdout)
    if not isinstance(rows, list):
        raise RuntimeError("MDD export is incomplete or malformed")
    result = {oracle.state(row) for row in rows}
    if len(rows) != len(result):
        raise RuntimeError("MDD export has duplicate states")
    return result


def selftest(budget, mdd=None):
    drivers = states = edges = 0
    mdd_preimages = mdd_first = 0
    for base, maximum_p in ((2, 3), (3, 2), (4, 2)):
        for p in range(1, maximum_p + 1):
            for gg in itertools.product("01", repeat=p):
                oracle = Oracle(base, "0" * p, "".join(gg))
                universe = [(l, h, y) for l in range(1 << p) for h in range(1 << p)
                            for y in itertools.product(range(base), repeat=len(oracle.positions))]
                for first in (False, True):
                    forward = {state: set() for state in universe}
                    for source in universe:
                        budget.check()
                        expected = brute_forward(oracle, source, first)
                        actual = {target for target, _ in oracle.forward_columns(source, first, budget)}
                        if actual != expected:
                            raise RuntimeError("forward DFS differs from complete guessed-H enumeration")
                        for target in expected:
                            forward[target].add(source)
                    for target in universe:
                        actual = {source for source, _ in oracle.inverse_columns(target, first, budget)}
                        if actual != forward[target]:
                            raise RuntimeError("complete small forward/reverse adjacency mismatch")
                        if mdd is not None and oracle.positions and not first:
                            symbolic = mdd_query(mdd, oracle, ["--preimage"], budget, {target})
                            if symbolic != actual:
                                raise RuntimeError("complete singleton-preimage MDD mismatch")
                            mdd_preimages += 1
                        edges += len(actual)
                    states += len(universe)
                if mdd is not None and oracle.positions:
                    symbolic = mdd_query(mdd, oracle, ["--first"], budget)
                    if symbolic != set(oracle.first(budget)):
                        raise RuntimeError("MDD positive-FIRST frontier mismatch")
                    mdd_first += 1
                drivers += 1
    # Inject a stop immediately after a genuine inverse hit, rather than relying
    # on timing or a coincidental set size to exercise partial-positive handling.
    from unittest.mock import patch
    positive = Oracle(2, "1010", "1010")
    first = positive.first(budget)
    hit_edge = next(edge for edge in positive.inverse_columns(positive.terminal)
                    if edge[0] in first)

    for exception in (Stop, MemoryError):
        def hit_then_stop(*args, **kwargs):
            yield hit_edge
            raise exception("injected stop after genuine hit")

        for export in (False, True):
            with patch.object(positive, "inverse_columns", side_effect=hit_then_stop):
                interrupted, output = backward(positive, 1, budget, export=export)
            expected = "UNDECIDED" if export else "EXTERIOR_ACCEPT"
            if (interrupted["status"] != expected or interrupted.get("direct_integer_replay") is not True
                    or not interrupted.get("partial_expansion") or interrupted["complete"] or output is not None):
                raise RuntimeError("interrupted positive was lost or partial export was accepted")
    result = {"status": "PASS", "drivers": drivers, "state_mode_queries": states,
              "directed_edges": edges, "positive_controls": positive_controls(budget),
              "interrupted_positive_controls": 4}
    if mdd is not None:
        target = Oracle(10, TARGET_E, TARGET_G)
        expected = {target.terminal}
        target_layers = []
        for depth in range(3):
            if depth:
                expected = preimage(target, expected, budget)
            actual = mdd_query(mdd, target, ["--export-layer", str(depth)], budget)
            if actual != expected:
                raise RuntimeError("P24 exact backward layer set mismatch")
            target_layers.append({"depth": depth, "states": len(expected), "sha256": digest(expected)})
        expected_first = set(target.first(budget))
        if mdd_query(mdd, target, ["--first"], budget) != expected_first:
            raise RuntimeError("P24 exact FIRST set mismatch")
        result["mdd_controls"] = {"singleton_preimages": mdd_preimages,
                                  "small_first_frontiers": mdd_first,
                                  "zero_overflow_drivers_skipped": 7,
                                  "target_layers": target_layers,
                                  "target_first": len(expected_first),
                                  "target_first_sha256": digest(expected_first)}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", nargs="?", type=int, default=10)
    parser.add_argument("e", nargs="?", default=TARGET_E)
    parser.add_argument("g", nargs="?", default=TARGET_G)
    parser.add_argument("--layers", type=int, default=2)
    parser.add_argument("--states", type=int, default=200000)
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--memory-mib", type=int, default=2048)
    parser.add_argument("--export-layer", type=int)
    parser.add_argument("--preimage", action="store_true")
    parser.add_argument("--first", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--mdd", type=Path, help="with --selftest, compare complete sets against this independent engine")
    args = parser.parse_args()
    if (not math.isfinite(args.seconds) or not 0 < args.seconds <= 1500
            or not 1 <= args.states <= 5000000 or not 64 <= args.memory_mib <= 8192
            or args.layers < 0 or args.export_layer is not None and args.export_layer < 0):
        parser.error("require 0<seconds<=1500, 1<=states<=5000000, 64<=memory-mib<=8192 and nonnegative layers")
    if sum((args.first, args.preimage, args.selftest, args.export_layer is not None)) > 1:
        parser.error("choose at most one export/control mode")
    if args.mdd is not None and not args.selftest:
        parser.error("--mdd requires --selftest")
    budget = Budget(args.seconds, args.states)
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        desired = args.memory_mib * 1024 * 1024
        if hard != resource.RLIM_INFINITY:
            desired = min(desired, hard)
        resource.setrlimit(resource.RLIMIT_AS, (desired, hard))
        oracle = Oracle(args.base, args.e, args.g)
        exported = None
        if args.selftest:
            result = selftest(budget, args.mdd)
        elif args.first:
            exported = set(oracle.first(budget))
            result = {"status": "COMPLETE_FIRST", "states": len(exported)}
        elif args.preimage:
            data = json.load(sys.stdin)
            if not isinstance(data, list):
                raise ValueError("preimage input must be an array of states")
            targets = set()
            for row in data:
                budget.insert(targets, oracle.state(row))
            exported = preimage(oracle, targets, budget)
            result = {"status": "COMPLETE_PREIMAGE", "targets": len(targets), "states": len(exported)}
        else:
            depth = args.layers if args.export_layer is None else args.export_layer
            result, states = backward(oracle, depth, budget, export=args.export_layer is not None)
            if args.export_layer is not None:
                exported = states
        result.update(base=args.base, e=args.e, g=args.g, temporal_nodes=budget.nodes,
                      seconds=time.monotonic() - budget.started)
        if exported is not None:
            result["sha256"] = digest(exported)
            print(json.dumps(result, sort_keys=True), file=sys.stderr)
            print(json.dumps(sorted(exported), separators=(",", ":")))
            return 0
        print(json.dumps(result, sort_keys=True))
        return 2 if result["status"] == "UNDECIDED" else 0
    except (Stop, MemoryError) as error:
        print(json.dumps({"status": "UNDECIDED", "reason": str(error) or "memory cap",
                          "complete": False, "partial_expansion": True,
                          "seconds": time.monotonic() - budget.started}, sort_keys=True))
        return 2
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    sys.exit(main())
