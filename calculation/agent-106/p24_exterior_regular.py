#!/usr/bin/env python3
"""Exact exterior cut languages for every repetition of a fixed driver.

The default driver is the priority P24 center itinerary.  A language word
contains ALL temporal phases of k laps, k >= 1.  Each spatial image closes
the coefficient only at the end of that entire word.  Intermediate final
states keep their outgoing transitions.  Limits always mean UNDECIDED.

The first controlled pilot is:
  python3 calculation/agent-106/p24_exterior_regular.py
True positive reconstruction controls:
  python3 calculation/agent-106/p24_exterior_regular.py --selftest-positive

An accepted terminal word is a B-only lead until all spatial predecessors
have been reconstructed and independently replayed.  No center, Lean, or
decimal Lychrel conclusion follows from a language frontier alone.
"""

import argparse
from collections import deque
from dataclasses import dataclass
import json
import math
from pathlib import Path
import resource
import sys
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Driver:
    base: int
    g: tuple
    e: tuple

    def __post_init__(self):
        require(type(self.base) is int and 2 <= self.base <= 62, "base must be in 2..62")
        require(type(self.g) is tuple and type(self.e) is tuple and
                1 <= len(self.g) <= 128 and len(self.e) == len(self.g),
                "driver words must be tuples of equal length in 1..128")
        require(all(type(x) is int and x in (0, 1) for x in self.g + self.e),
                "driver entries must be bits")

    @property
    def period(self):
        return len(self.g)

    @property
    def ports(self):
        return 2 * self.base - 1

    def encode(self, phase, low, high, previous=0):
        require(type(phase) is int and 0 <= phase < self.period, "invalid phase")
        require(type(low) is int and low in (0, 1) and
                type(high) is int and high in (0, 1), "invalid carry bit")
        require(type(previous) is int and 0 <= previous < self.base and
                (self.g[phase] or previous == 0), "invalid previous digit")
        return phase * (4 * self.base) + low * (2 * self.base) + high * self.base + previous

    def decode(self, symbol):
        require(type(symbol) is int and 0 <= symbol < self.period * 4 * self.base,
                "symbol outside driver alphabet")
        phase, local = divmod(symbol, 4 * self.base)
        low, local = divmod(local, 2 * self.base)
        high, previous = divmod(local, self.base)
        require(self.g[phase] or previous == 0, "nonoverflow symbol has a previous digit")
        return phase, low, high, previous

    def alphabet(self):
        return tuple(self.encode(t, low, high, previous)
                     for t in range(self.period) for low in (0, 1) for high in (0, 1)
                     for previous in range(self.base if self.g[t] else 1))

    def terminal_word(self):
        return tuple(self.encode(t, e, 1 - e, (self.base - 1) * e if self.g[t] else 0)
                     for t, e in enumerate(self.e))


G = tuple(map(int, "110001001000110001001000"))
E = tuple(map(int, "010100110100101011001011"))
DEFAULT = Driver(10, G, E)
HEAD12 = (9, 10, 1, 2, 5, 11, 2, 5, 10, 1, 2, 4)
HEAD_HIGH12 = (1, None, 0, 1, 1, None, 1, 0, None, 0, 0, 1)


@dataclass(frozen=True)
class DFA:
    start: int
    finals: frozenset
    transitions: tuple

    @property
    def nodes(self):
        return len(self.transitions)

    @property
    def edges(self):
        return sum(len(row) for row in self.transitions)


@dataclass(frozen=True)
class NFA:
    initials: frozenset
    finals: frozenset
    transitions: tuple


class Limited(Exception):
    pass


class Budget:
    def __init__(self, seconds=60.0, nfa_cap=500000, dfa_cap=500000,
                 edge_cap=5000000, operation_cap=50000000, product_cap=2000000):
        require(isinstance(seconds, (int, float)) and math.isfinite(seconds) and seconds > 0,
                "seconds must be positive and finite")
        for value in (nfa_cap, dfa_cap, edge_cap, operation_cap, product_cap):
            require(type(value) is int and value > 0, "all resource caps must be positive integers")
        self.started = time.monotonic()
        self.seconds = seconds
        self.nfa_cap, self.dfa_cap = nfa_cap, dfa_cap
        self.edge_cap, self.operation_cap = edge_cap, operation_cap
        self.product_cap = product_cap
        self.operations = 0
        self.peak_nfa = self.peak_dfa = self.peak_nfa_edges = self.peak_dfa_edges = 0
        self.peak_product_slots = self.peak_product_live = 0
        self.last_completed_width = 0
        self.last_terminal_checked_width = 0
        self.layers = []

    def check(self):
        if time.monotonic() - self.started > self.seconds:
            raise Limited("time_cap")

    def tick(self, amount=1):
        old = self.operations
        self.operations += amount
        if self.operations > self.operation_cap:
            raise Limited("operation_cap")
        if (old >> 10) != (self.operations >> 10):
            self.check()

    def size(self, kind, nodes, edges=0):
        self.check()
        if kind == "nfa":
            self.peak_nfa = max(self.peak_nfa, nodes)
            self.peak_nfa_edges = max(self.peak_nfa_edges, edges)
            cap = self.nfa_cap
        else:
            self.peak_dfa = max(self.peak_dfa, nodes)
            self.peak_dfa_edges = max(self.peak_dfa_edges, edges)
            cap = self.dfa_cap
        if nodes > cap:
            raise Limited(kind + "_state_cap")
        if edges > self.edge_cap:
            raise Limited(kind + "_edge_cap")

    def summary(self):
        return {"seconds": round(time.monotonic() - self.started, 6),
                "operations": self.operations, "peak_nfa": self.peak_nfa,
                "peak_dfa": self.peak_dfa, "peak_nfa_edges": self.peak_nfa_edges,
                "peak_dfa_edges": self.peak_dfa_edges,
                "peak_product_slots": self.peak_product_slots,
                "peak_product_live": self.peak_product_live,
                "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                "last_completed_width": self.last_completed_width,
                "last_terminal_checked_width": self.last_terminal_checked_width}


def _budget(budget):
    return budget if budget is not None else Budget()


def empty_dfa():
    return DFA(0, frozenset(), ({},))


def validate_dfa(dfa):
    require(isinstance(dfa, DFA) and type(dfa.transitions) is tuple and dfa.nodes > 0,
            "invalid DFA container")
    require(type(dfa.start) is int and 0 <= dfa.start < dfa.nodes, "invalid DFA start")
    require(isinstance(dfa.finals, frozenset) and
            all(type(q) is int and 0 <= q < dfa.nodes for q in dfa.finals), "invalid DFA finals")
    for row in dfa.transitions:
        require(type(row) is dict and all(type(a) is int and a >= 0 and type(q) is int and
                                        0 <= q < dfa.nodes for a, q in row.items()),
                "invalid DFA transition")
    return True


def accepts(dfa, word):
    q = dfa.start
    for symbol in word:
        q = dfa.transitions[q].get(symbol)
        if q is None:
            return False
    return q in dfa.finals


def pattern_language(choices):
    require(len(choices) > 0 and all(len(row) > 0 for row in choices), "empty pattern")
    period = len(choices)
    rows = [{} for _ in range(period + 1)]
    for i, symbols in enumerate(choices):
        rows[i] = {symbol: i + 1 for symbol in symbols}
    rows[period] = dict(rows[0])
    return DFA(0, frozenset((period,)), tuple(rows))


def physical_root_language(driver=DEFAULT):
    return pattern_language(tuple((driver.encode(t, 0, g, 1 if g else 0),)
                                  for t, g in enumerate(driver.g)))


def first_language():
    choices = []
    for t in range(24):
        x, high = HEAD12[t % 12], HEAD_HIGH12[t % 12]
        options = (0, 1) if high is None else (high,)
        choices.append(tuple(DEFAULT.encode(t, x // 10, h, (x + h) % 10 if G[t] else 0)
                             for h in options))
    return pattern_language(choices)


def tiles(symbol, coefficient, driver=DEFAULT):
    phase, low, high, previous = driver.decode(symbol)
    require(type(coefficient) is int and 0 <= coefficient < driver.ports, "invalid coefficient")
    base = driver.base
    result = []
    for inward in (0, 1):
        if (coefficient + inward) // base != high:
            continue
        low_next, digit = divmod(coefficient + low, base)
        reflected = (coefficient + inward) % base
        successor = digit + (previous if driver.g[phase] else reflected)
        output = driver.encode(phase, low_next, inward, reflected if driver.g[phase] else 0)
        result.append((output, successor))
    return tuple(result)


def trim_dfa(dfa, budget=None):
    budget = _budget(budget)
    validate_dfa(dfa)
    reachable = {dfa.start}
    queue = deque((dfa.start,))
    reverse = [[] for _ in range(dfa.nodes)]
    while queue:
        q = queue.popleft()
        for v in dfa.transitions[q].values():
            budget.tick()
            reverse[v].append(q)
            if v not in reachable:
                reachable.add(v)
                queue.append(v)
    live = set(dfa.finals & reachable)
    queue = deque(live)
    while queue:
        for q in reverse[queue.popleft()]:
            budget.tick()
            if q not in live:
                live.add(q)
                queue.append(q)
    if dfa.start not in live:
        return empty_dfa()
    ids = {q: i for i, q in enumerate(sorted(live))}
    rows = tuple({a: ids[v] for a, v in dfa.transitions[q].items() if v in live}
                 for q in sorted(live))
    return DFA(ids[dfa.start], frozenset(ids[q] for q in dfa.finals if q in live), rows)


def validate_quotient(source, target, mapping, budget=None):
    """Check finals and EVERY outgoing arc, including absent labels."""
    budget = _budget(budget)
    require(len(mapping) == source.nodes and mapping[source.start] == target.start,
            "invalid quotient start/map")
    require(set(mapping) == set(range(target.nodes)), "quotient map is not onto")
    for q, row in enumerate(source.transitions):
        budget.tick(1 + len(row))
        require((q in source.finals) == (mapping[q] in target.finals), "quotient final mismatch")
        expected = {a: mapping[v] for a, v in row.items()}
        require(expected == target.transitions[mapping[q]], "quotient transition/absence mismatch")
    return True


def minimize(dfa, budget=None, return_map=False):
    """Exact sparse Moore refinement; missing labels go to the implicit dead state."""
    budget = _budget(budget)
    source = trim_dfa(dfa, budget)
    blocks = tuple(int(q in source.finals) for q in range(source.nodes))
    while True:
        signatures, next_blocks = {}, []
        for q, row in enumerate(source.transitions):
            budget.tick(1 + len(row))
            signature = (q in source.finals, tuple((a, blocks[v]) for a, v in sorted(row.items())))
            if signature not in signatures:
                signatures[signature] = len(signatures)
            next_blocks.append(signatures[signature])
        next_blocks = tuple(next_blocks)
        if next_blocks == blocks:
            break
        blocks = next_blocks
    representatives = {}
    for q, block in enumerate(blocks):
        representatives.setdefault(block, q)
    # Canonical BFS numbering uses the full, stable integer symbol alphabet.
    start = blocks[source.start]
    ids = {start: 0}
    order = [start]
    rows = []
    finals = set()
    for block in order:
        q = representatives[block]
        if q in source.finals:
            finals.add(ids[block])
        row = {}
        for a, v in sorted(source.transitions[q].items()):
            target = blocks[v]
            if target not in ids:
                ids[target] = len(order)
                order.append(target)
            row[a] = ids[target]
        rows.append(row)
    result = DFA(0, frozenset(finals), tuple(rows))
    mapping = tuple(ids[block] for block in blocks)
    validate_quotient(source, result, mapping, budget)
    budget.size("dfa", result.nodes, result.edges)
    return (source, result, mapping) if return_map else result


def trim_nfa(nfa, budget):
    reverse = [[] for _ in nfa.transitions]
    for q, row in enumerate(nfa.transitions):
        for _, target in row:
            budget.tick()
            reverse[target].append(q)
    live = set(nfa.finals)
    queue = deque(live)
    while queue:
        for q in reverse[queue.popleft()]:
            budget.tick()
            if q not in live:
                live.add(q)
                queue.append(q)
    if not (nfa.initials & live):
        return NFA(frozenset(), frozenset(), ())
    ids = {q: i for i, q in enumerate(sorted(live))}
    rows = tuple(tuple((a, ids[v]) for a, v in nfa.transitions[q] if v in live)
                 for q in sorted(live))
    # A discarded state cannot be final or have an edge into the retained set.
    for q, row in enumerate(nfa.transitions):
        if q not in live:
            require(q not in nfa.finals and all(v not in live for _, v in row),
                    "NFA coaccessibility trim failed")
    return NFA(frozenset(ids[q] for q in nfa.initials if q in live),
               frozenset(ids[q] for q in nfa.finals), rows)


def validate_determinization(nfa, dfa, subsets, budget=None):
    budget = _budget(budget)
    require(len(subsets) == dfa.nodes and subsets[dfa.start] == nfa.initials,
            "determinization initial subset mismatch")
    for q, subset in enumerate(subsets):
        expected = {}
        for old in subset:
            for a, v in nfa.transitions[old]:
                budget.tick()
                expected.setdefault(a, set()).add(v)
        require((q in dfa.finals) == bool(subset & nfa.finals), "determinization final mismatch")
        require(expected.keys() == dfa.transitions[q].keys(), "determinization missing/extra label")
        require(all(frozenset(vs) == subsets[dfa.transitions[q][a]] for a, vs in expected.items()),
                "determinization target subset mismatch")
    return True


def determinize(nfa, budget=None):
    budget = _budget(budget)
    if not nfa.initials:
        return empty_dfa()
    subsets = [nfa.initials]
    ids = {nfa.initials: 0}
    rows, finals, edge_count = [], set(), 0
    for subset in subsets:
        q = len(rows)
        if subset & nfa.finals:
            finals.add(q)
        targets = {}
        for old in subset:
            for a, v in nfa.transitions[old]:
                budget.tick()
                targets.setdefault(a, set()).add(v)
        row = {}
        for a, vs in sorted(targets.items()):
            target = frozenset(vs)
            if target not in ids:
                ids[target] = len(subsets)
                subsets.append(target)
                if len(subsets) > budget.dfa_cap:
                    budget.size("dfa", len(subsets), edge_count)
            row[a] = ids[target]
        rows.append(row)
        edge_count += len(row)
        if edge_count > budget.edge_cap or q % 1024 == 0:
            budget.size("dfa", len(subsets), edge_count)
    result = DFA(0, frozenset(finals), tuple(rows))
    budget.size("dfa", result.nodes, edge_count)
    validate_determinization(nfa, result, subsets, budget)
    return result


def coaccessibility_masks(dfa, local, budget=None, driver=DEFAULT, first=False):
    """Exact final-coefficient masks on the smaller product (DFA node, port).

    Bit a is present at (q,x) iff some suffix from q reaches an input-final
    node with coefficient a.  It includes the zero-length suffix at finals.
    Initial-port a can therefore retain (q,a,x) exactly when this bit is set.
    Output labels are ignored ONLY in this existential coaccessibility test.
    """
    budget = _budget(budget)
    ports = driver.ports
    slots = dfa.nodes * ports
    budget.peak_product_slots = max(budget.peak_product_slots, slots)
    if slots > budget.product_cap:
        raise Limited("coaccessibility_product_cap")
    reverse = [[] for _ in range(dfa.nodes)]
    for q, row in enumerate(dfa.transitions):
        for symbol, target in row.items():
            budget.tick()
            reverse[target].append((q, symbol))
    inverse = {}
    for symbol, by_coefficient in local.items():
        row = [set() for _ in range(ports)]
        for x, options in enumerate(by_coefficient):
            budget.tick()
            if first and x == 0:
                continue
            for _, successor in options:
                row[successor].add(x)
        inverse[symbol] = tuple(tuple(sorted(xs)) for xs in row)
    masks, processed = [0] * slots, [0] * slots
    queued = bytearray(slots)
    queue = deque()
    for q in dfa.finals:
        for a in range(1 if first else 0, ports):
            budget.tick()
            index = q * ports + a
            masks[index] = 1 << a
            queued[index] = 1
            queue.append(index)
    while queue:
        budget.tick()
        index = queue.popleft()
        queued[index] = 0
        delta = masks[index] & ~processed[index]
        processed[index] |= delta
        q, current = divmod(index, ports)
        for previous_q, symbol in reverse[q]:
            budget.tick()
            for x in inverse[symbol][current]:
                budget.tick()
                previous = previous_q * ports + x
                if delta & ~masks[previous]:
                    masks[previous] |= delta
                    if not queued[previous]:
                        queued[previous] = 1
                        queue.append(previous)
    budget.peak_product_live = max(budget.peak_product_live, sum(x != 0 for x in masks))
    budget.check()
    return masks


def image(dfa, first=False, budget=None, driver=DEFAULT, pretrim=True):
    """Exact cyclic rational image; per-lap boundaries NEVER reset the port."""
    budget = _budget(budget)
    validate_dfa(dfa)
    local = {}
    for symbol in {a for row in dfa.transitions for a in row}:
        budget.tick(driver.ports)
        budget.check()
        local[symbol] = tuple(tiles(symbol, x, driver) for x in range(driver.ports))
    masks = coaccessibility_masks(dfa, local, budget, driver, first) if pretrim else None
    states, ids, rows, initials, finals = [], {}, [], set(), set()
    def intern(state):
        if masks is not None:
            q, initial, current = state
            if not (masks[q * driver.ports + current] & (1 << initial)):
                return None
        if state not in ids:
            ids[state] = len(states)
            states.append(state)
            if len(states) > budget.nfa_cap:
                budget.size("nfa", len(states))
        return ids[state]
    for initial in range(1 if first else 0, driver.ports):
        index = intern((dfa.start, initial, initial))
        if index is not None:
            initials.add(index)
    edge_count = 0
    for q, initial, current in states:
        index = len(rows)
        if q in dfa.finals and current == initial:
            finals.add(index)
        outgoing = set()
        if not first or current > 0:
            for a, target_q in dfa.transitions[q].items():
                for output, successor in local[a][current]:
                    budget.tick()
                    target = intern((target_q, initial, successor))
                    if target is not None:
                        outgoing.add((output, target))
        row = tuple(sorted(outgoing))
        rows.append(row)
        edge_count += len(row)
        if edge_count > budget.edge_cap or index % 1024 == 0:
            budget.size("nfa", len(states), edge_count)
    budget.size("nfa", len(states), edge_count)
    nfa = trim_nfa(NFA(frozenset(initials), frozenset(finals), tuple(rows)), budget)
    if pretrim:
        require(len(nfa.transitions) == len(states), "coaccessibility masks retained a dead NFA state")
    return minimize(determinize(nfa, budget), budget)


def equivalent(left, right, budget=None):
    """Exact DFA-product symmetric-difference emptiness, with an implicit sink."""
    budget = _budget(budget)
    validate_dfa(left)
    validate_dfa(right)
    initial = (left.start, right.start)
    seen, queue = {initial}, deque((initial,))
    while queue:
        p, q = queue.popleft()
        if (p in left.finals) != (q in right.finals):
            return False
        prow = left.transitions[p] if p >= 0 else {}
        qrow = right.transitions[q] if q >= 0 else {}
        for a in prow.keys() | qrow.keys():
            budget.tick()
            target = (prow.get(a, -1), qrow.get(a, -1))
            if target not in seen:
                seen.add(target)
                queue.append(target)
                if len(seen) > budget.nfa_cap:
                    raise Limited("equivalence_product_cap")
    return True


def terminal_intersection(dfa, driver=DEFAULT, budget=None):
    """Return the least positive lap count accepted in Q+, or None exactly."""
    budget = _budget(budget)
    q, laps, seen = dfa.start, 0, {dfa.start}
    terminal = driver.terminal_word()
    while True:
        for a in terminal:
            budget.tick()
            q = dfa.transitions[q].get(a)
            if q is None:
                return None
        laps += 1
        if q in dfa.finals:
            return laps
        if q in seen:
            return None
        seen.add(q)


def export_payload(dfa, driver, width, kind="frontier"):
    """Pure interchange data; creates no file and makes no completeness claim."""
    validate_dfa(dfa)
    require(isinstance(driver, Driver), "invalid export driver")
    require(type(width) is int and width >= 1, "export width must be positive")
    require(kind in ("frontier", "invariant"), "invalid export kind")
    for row in dfa.transitions:
        for symbol in row:
            driver.decode(symbol)
    return {"schema": "p196-exterior-dfa-v1", "base": driver.base,
            "g": "".join(map(str, driver.g)), "e": "".join(map(str, driver.e)),
            "width": width, "kind": kind, "start": dfa.start,
            "finals": sorted(dfa.finals),
            "transitions": [sorted(row.items()) for row in dfa.transitions]}


def preimage_witness(source, output_word, driver=DEFAULT, first=False, budget=None):
    """Bounded exact whole-word DP; return one input word and physical column."""
    budget = _budget(budget)
    validate_dfa(source)
    require(isinstance(output_word, (tuple, list)) and len(output_word) > 0 and
            len(output_word) % driver.period == 0, "invalid output-word length")
    if len(output_word) > budget.edge_cap:
        raise Limited("reconstruction_word_cap")
    for t, symbol in enumerate(output_word):
        budget.tick()
        require(driver.decode(symbol)[0] == t % driver.period, "output word has wrong phase order")
    local = {}
    for symbol in {a for row in source.transitions for a in row}:
        budget.tick(driver.ports)
        local[symbol] = tuple(tiles(symbol, x, driver) for x in range(driver.ports))
    current = {(source.start, a, a) for a in range(1 if first else 0, driver.ports)}
    initial = set(current)
    parents = []
    total_states = len(current)
    for wanted in output_word:
        following = {}
        for state in sorted(current):
            q, a, x = state
            if first and x == 0:
                continue
            for symbol, target_q in source.transitions[q].items():
                for output, successor in local[symbol][x]:
                    budget.tick()
                    if output != wanted:
                        continue
                    target = (target_q, a, successor)
                    if target not in following:
                        following[target] = (state, symbol, x)
                        total_states += 1
                        if total_states > budget.nfa_cap:
                            raise Limited("reconstruction_state_cap")
        parents.append(following)
        current = following.keys()
        if not following:
            return None
    accepted = [state for state in current if state[0] in source.finals and state[1] == state[2]]
    if not accepted:
        return None
    state = min(accepted)
    input_word, column = [], []
    for layer in reversed(parents):
        state, symbol, x = layer[state]
        input_word.append(symbol)
        column.append(x)
    require(state in initial, "backtracking did not reach an initial port")
    input_word, column = tuple(reversed(input_word)), tuple(reversed(column))
    require(accepts(source, input_word), "reconstructed input word is rejected")
    require(len(input_word) == len(column) == len(output_word), "reconstructed word lengths disagree")
    for t in range(len(column)):
        symbol, x = input_word[t], column[t]
        budget.tick()
        require((output_word[t], column[(t + 1) % len(column)]) in tiles(symbol, x, driver),
                "reconstructed tile or whole-word closure fails")
        require(not first or x > 0, "reconstructed first coefficient is zero")
    return {"input_word": input_word, "column": column}


def _normalize(base, word, incoming):
    digits = []
    for coefficient in word:
        incoming, digit = divmod(coefficient + incoming, base)
        digits.append(digit)
    return tuple(digits), incoming


def replay_exterior(words, driver=DEFAULT, budget=None):
    """Replay by ordinary whole-word normalization, independently of cut tiles."""
    budget = _budget(budget)
    require(isinstance(words, (tuple, list)) and len(words) > 0 and
            len(words) % driver.period == 0, "invalid exterior period")
    require(all(isinstance(word, (tuple, list)) and len(word) > 0 for word in words),
            "exteriors must have positive width")
    width, base = len(words[0]), driver.base
    require(all(len(word) == width and word[0] > 0 and
                all(type(x) is int and 0 <= x <= 2 * base - 2 for x in word)
                for word in words), "invalid exterior coefficients/heads/widths")
    carries, overflows = [], []
    for t, word in enumerate(words):
        budget.tick(1 + 2 * len(word))
        low, e = _normalize(base, word, 0)
        reverse, g = _normalize(base, word[::-1], 1 - e)
        high = reverse[::-1]
        if g:
            low = low + ((base - 1) * (1 - e),)
            high = (1,) + high
        raw = tuple(low[i] + high[i] for i in range(len(low)))
        require((e, g) == (driver.e[t % driver.period], driver.g[t % driver.period]),
                "reconstructed driver disagrees with normalization")
        require(raw == tuple(words[(t + 1) % len(words)]) + (base - 1,) * g,
                "reconstructed raw exterior edge or u=g fails")
        carries.append(e)
        overflows.append(g)
    require(sum(overflows) > 0, "positive-head exterior cycle has no overflow")
    return {"e": tuple(carries), "g": tuple(overflows), "u": tuple(overflows)}


PRIORITY_V = tuple(map(int, "100001000000100001000000"))
PRIORITY_C0 = (9, 14, 13, 18, 13, 14, 9)


def priority_center_cycle():
    """Reconstruct and check Agent101's credited exact center fixture."""
    centers, center = [], PRIORITY_C0
    for t in range(24):
        centers.append(center)
        digits, outgoing = _normalize(10, center, E[t])
        require(outgoing == 1 - E[t], "priority center does not flip the carry")
        if G[t]:
            endpoint = 9 * E[t]
            left, right = digits + (endpoint,), (endpoint,) + digits[::-1]
        else:
            left, right = digits, digits[::-1]
        raw = tuple(left[i] + right[i] for i in range(len(left)))
        trim = PRIORITY_V[t]
        center = raw[trim:len(raw) - trim] if trim else raw
        require(raw == (9,) * trim + center + (9,) * trim,
                "priority center lacks its prescribed neutral trim")
    require(center == PRIORITY_C0, "priority center fixture does not close")
    return tuple(centers)


def _main_mirror():
    import importlib.util
    path = Path(__file__).resolve().parents[1] / "neutral_band_search.py"
    spec = importlib.util.spec_from_file_location("agent106_main_mirror", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def join_priority_center(words):
    """Return full edges ONLY after the unchanged Python cycleOK accepts them."""
    require(len(words) > 0 and len(words) % 24 == 0, "priority B period is not a positive lap count")
    require(all(isinstance(word, (tuple, list)) and len(word) > 0 and word[0] > 0 and
                all(type(x) is int and 0 <= x <= 18 for x in word) for word in words),
            "priority exterior contains invalid natural coefficients")
    centers = priority_center_cycle()
    edges = []
    for t, word in enumerate(words):
        edges.append((list(word), list(centers[t % 24]), list(words[(t + 1) % len(words)]),
                      list(centers[(t + 1) % 24]), G[t % 24], PRIORITY_V[t % 24]))
    mirror = _main_mirror()
    require(mirror.cycleOK(10, edges, edges[0][0], edges[0][1]),
            "reconstructed full priority cycle fails unchanged mirror")
    return tuple(edges)


def reconstruct(frontiers, laps, driver=DEFAULT, budget=None):
    """Recover all B rows from completed exact frontiers; never infer a Lean proof."""
    budget = _budget(budget)
    require(isinstance(frontiers, (tuple, list)) and len(frontiers) > 0,
            "all positive-width frontiers are required")
    require(type(laps) is int and laps > 0, "lap count must be positive")
    period, width = driver.period * laps, len(frontiers)
    if period * width > budget.edge_cap:
        raise Limited("reconstruction_coefficient_cap")
    target = driver.terminal_word() * laps
    require(accepts(frontiers[-1], target), "terminal word is not in the last frontier")
    columns = [None] * width
    for level in range(width, 0, -1):
        source = physical_root_language(driver) if level == 1 else frontiers[level - 2]
        witness = preimage_witness(source, target, driver, first=(level == 1), budget=budget)
        require(witness is not None, "frontier chain lacks a claimed spatial predecessor")
        columns[level - 1] = witness["column"]
        target = witness["input_word"]
    root_unit = tuple(driver.encode(t, 0, g, 1 if g else 0) for t, g in enumerate(driver.g))
    require(target == root_unit * laps, "backtracking did not recover the physical root")
    words = tuple(tuple(column[t] for column in columns) for t in range(period))
    replay = replay_exterior(words, driver, budget)
    result = {"status": "B_RECONSTRUCTED", "base": driver.base, "width": width,
              "laps": laps, "period": period, "B": words, **replay,
              "scope": "COMPUTED exterior cycle; center and Lean verification still required"}
    if driver == DEFAULT:
        result["edges"] = join_priority_center(words)
        result["status"] = "CANDIDATE_MIRROR_OK"
        result["scope"] = "COMPUTED full decimal candidate accepted by Python cycleOK; not Lean-verified"
    return result


def reconstruction_controls(budget=None):
    """True generic positives, followed by full B+C replay in the main mirror."""
    mirror = _main_mirror()
    results = []
    for base, fixture in mirror._lean_certs():
        if base not in (2, 4):
            continue
        driver = Driver(base, tuple(mirror.gam(base, edge[0], edge[1]) for edge in fixture),
                        tuple(mirror.e1(base, edge[0]) for edge in fixture))
        control_budget = budget if budget is not None else Budget(seconds=30)
        lead = run(driver, control_budget, max_layers=8)
        require(lead["status"] == "TERMINAL_LEAD", "known positive driver has no terminal lead")
        recovered = reconstruct(lead["frontiers"], lead["laps"], driver, control_budget)
        words, p = recovered["B"], len(fixture)
        edges = [(list(word), fixture[t % p][1], list(words[(t + 1) % len(words)]),
                  fixture[t % p][3], driver.g[t % p], fixture[t % p][5])
                 for t, word in enumerate(words)]
        require(mirror.cycleOK(base, edges, edges[0][0], edges[0][1]),
                "known-control reconstructed B+C cycle fails unchanged mirror")
        results.append({"base": base, "width": recovered["width"], "laps": recovered["laps"],
                        "edges": len(edges), "mirror_cycleOK": True})
    require(len(results) == 2, "missing base2/base4 positive controls")
    centers = priority_center_cycle()
    probes = {(0, 0): [1], (0, 1): [9], (1, 0): [1, 10], (1, 1): [10]}
    for t, center in enumerate(centers):
        probe = probes[E[t], G[t]]
        require(mirror.e1(10, probe) == E[t] and mirror.e2(10, probe, list(center)) == 1 - E[t]
                and mirror.gam(10, probe, list(center)) == G[t], "center-only probe carry mismatch")
        require(mirror.nextC(10, probe, list(center)) == [9] * PRIORITY_V[t] +
                list(centers[(t + 1) % 24]) + [9] * PRIORITY_V[t],
                "priority center transition disagrees with unchanged mirror")
    return results


def first_control(budget, driver=DEFAULT, pretrim=True):
    actual = image(physical_root_language(driver), first=True, budget=budget, driver=driver, pretrim=pretrim)
    if driver == DEFAULT:
        expected = minimize(first_language(), budget)
        require(equivalent(actual, expected, budget), "closed-form first language disagrees with root image")
        require(actual.nodes == 25, "unexpected default first-language size")
    return actual


def run(driver=DEFAULT, budget=None, max_layers=64, on_layer=None, pretrim=True):
    budget = _budget(budget)
    require(type(max_layers) is int and max_layers > 0, "max_layers must be positive")
    require(on_layer is None or callable(on_layer), "on_layer must be callable")
    layer = first_control(budget, driver, pretrim)
    history = []
    for width in range(1, max_layers + 1):
        budget.last_completed_width = width
        entry = {"width": width, "dfa_nodes": layer.nodes, "dfa_edges": layer.edges,
                 "terminal_status": "PENDING"}
        budget.layers.append(entry)
        laps = terminal_intersection(layer, driver, budget)
        budget.last_terminal_checked_width = width
        entry["terminal_status"] = "LEAD" if laps is not None else "EMPTY"
        if laps is not None:
            entry["minimum_laps"] = laps
            # Preserve the exact lead and all completed languages for an independent
            # backwards extraction.  A lead is not relabelled as an exhausted run.
            return {"status": "TERMINAL_LEAD", "width": width, "laps": laps,
                    "scope": "unreconstructed B-only terminal word; not cycleOK",
                    "driver": driver, "frontiers": tuple(history + [layer])}
        if on_layer is not None:
            on_layer(width, layer, entry)
        if not layer.finals:
            return {"status": "EXHAUSTED_NO_B", "reason": "empty_language", "width": width}
        for prior_width, prior in enumerate(history, 1):
            # Full canonical structures, not counts or hashes, establish equality.
            if layer.finals == prior.finals and layer.transitions == prior.transitions:
                require(equivalent(layer, prior, budget), "canonical equality failed product check")
                return {"status": "EXHAUSTED_NO_B", "reason": "exact_language_return",
                        "first_width": prior_width, "return_width": width}
        history.append(layer)
        if width == max_layers:
            raise Limited("layer_cap")
        layer = image(layer, budget=budget, driver=driver, pretrim=pretrim)
    raise RuntimeError("unreachable layer loop")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=int, default=10)
    parser.add_argument("--g", default="".join(map(str, G)))
    parser.add_argument("--e", default="".join(map(str, E)))
    parser.add_argument("--seconds", type=float, default=60.0)
    parser.add_argument("--nfa-cap", type=int, default=500000)
    parser.add_argument("--dfa-cap", type=int, default=500000)
    parser.add_argument("--edge-cap", type=int, default=5000000)
    parser.add_argument("--operation-cap", type=int, default=50000000)
    parser.add_argument("--product-cap", type=int, default=2000000)
    parser.add_argument("--max-layers", type=int, default=64)
    parser.add_argument("--memory-mib", type=int, default=2048)
    parser.add_argument("--selftest-positive", action="store_true")
    parser.add_argument("--no-pretrim", action="store_true")
    args = parser.parse_args()
    budget = None
    try:
        require(args.g and args.e and set(args.g + args.e) <= {"0", "1"}, "e/g must be nonempty bit strings")
        require(math.isfinite(args.seconds) and 0 < args.seconds <= 1500, "seconds must be in (0,1500]")
        require(64 <= args.memory_mib <= 8192, "memory-mib must be in 64..8192")
        require(1 <= args.max_layers <= 4096, "max-layers must be in 1..4096")
        driver = Driver(args.base, tuple(map(int, args.g)), tuple(map(int, args.e)))
        budget = Budget(args.seconds, args.nfa_cap, args.dfa_cap, args.edge_cap,
                        args.operation_cap, args.product_cap)
        limit = args.memory_mib * 1024 * 1024
        _, hard = resource.getrlimit(resource.RLIMIT_AS)
        resource.setrlimit(resource.RLIMIT_AS, (min(limit, hard) if hard >= 0 else limit, hard))
        if args.selftest_positive:
            result = {"status": "POSITIVE_RECONSTRUCTION_CONTROLS_PASS",
                      "controls": reconstruction_controls(budget), "priority_center_edges": 24,
                      "resources": budget.summary()}
            print(json.dumps(result, separators=(",", ":")), flush=True)
            return 0
        result = run(driver, budget, args.max_layers, pretrim=not args.no_pretrim)
        if result["status"] == "TERMINAL_LEAD":
            lead = {k: v for k, v in result.items() if k not in ("driver", "frontiers")}
            lead["terminal_unit"] = driver.terminal_word()
            try:
                recovered = reconstruct(result["frontiers"], result["laps"], driver, budget)
                result = recovered
            except Exception as exc:
                # A bounded reconstruction failure does not erase an already
                # completed positive terminal-language finding.
                lead["reconstruction_status"] = "UNDECIDED" if isinstance(exc, (Limited, MemoryError)) else "FAILED"
                lead["reconstruction_reason"] = "memory_cap" if isinstance(exc, MemoryError) else str(exc)
                result = lead
        result["layers"] = budget.layers
        result["resources"] = budget.summary()
        print(json.dumps(result, separators=(",", ":")), flush=True)
        return 0 if result["status"] in ("EXHAUSTED_NO_B", "B_RECONSTRUCTED", "CANDIDATE_MIRROR_OK") else 3
    except (Limited, MemoryError) as exc:
        result = {"status": "UNDECIDED", "reason": str(exc) if isinstance(exc, Limited) else "memory_cap"}
        if budget is not None:
            result["layers"] = budget.layers
            result["resources"] = budget.summary()
        print(json.dumps(result, separators=(",", ":")), flush=True)
        return 2
    except ValueError as exc:
        print(json.dumps({"status": "INVALID_INPUT", "reason": str(exc)}, separators=(",", ":")), flush=True)
        return 2


if __name__ == "__main__":
    sys.exit(main())
