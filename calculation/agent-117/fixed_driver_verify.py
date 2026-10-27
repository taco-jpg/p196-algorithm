#!/usr/bin/env python3
"""Independent arithmetic audit of fixed-target exterior spatial inverses.

This is an inverse of the column-transfer automaton, NOT an inverse step of
the autonomous B-word dynamics.  No C++/bauto code is imported.  A predecessor
is enumerated by choosing coefficient/carry pairs in temporal order, directly
from the two base-b division equations and the shifted coefficient identity.

CLI examples:
  python3 calculation/agent-117/fixed_driver_verify.py --selftest
  python3 calculation/agent-117/fixed_driver_verify.py --known-controls
  python3 calculation/agent-117/fixed_driver_verify.py --predecessors --base 10 \
    --g 110001001000110001001000 --L 010100110100101011001011 \
    --H 101011001011010100110100 --Y 0,9,0,0,9,0,9,9

A resource limit is reported as UNDECIDED.  It is never a negative result.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys
import time

from p24_center_target import integer_norm, require


class BudgetExceeded(RuntimeError):
    pass


class NoWitness(ValueError):
    pass


def check_bits(values, name, length=None):
    require(isinstance(values, (tuple, list)) and bool(values)
            and all(type(x) is int and x in (0, 1) for x in values)
            and (length is None or len(values) == length), "invalid " + name)


def check_state(base, g, state):
    require(type(base) is int and 2 <= base <= 62, "base outside 2..62")
    check_bits(g, "overflow stream")
    require(len(g) <= 32, "reference implementation supports periods at most 32")
    require(isinstance(state, (tuple, list)) and len(state) == 3, "invalid cut shape")
    left, right, stored = state
    check_bits(left, "left carry", len(g))
    check_bits(right, "right carry", len(g))
    require(isinstance(stored, (tuple, list)) and len(stored) == sum(g)
            and all(type(x) is int and 0 <= x < base for x in stored), "invalid stored digits")


def unpack_state(record):
    require(type(record) is dict and set(record) == {"L", "H", "Y"}, "invalid serialized cut")
    def carry(value):
        if type(value) is str:
            require(bool(value) and set(value) <= {"0", "1"}, "invalid carry bitstring")
            return tuple(map(int, value))
        require(type(value) is list and all(type(x) is int for x in value), "invalid carry array")
        return tuple(value)
    require(type(record["Y"]) is list, "invalid digit array")
    return carry(record["L"]), carry(record["H"]), tuple(record["Y"])


def pack_state(state):
    return {"L": "".join(map(str, state[0])), "H": "".join(map(str, state[1])),
            "Y": list(state[2])}


def terminal_state(base, e, g):
    check_bits(e, "carry stream", len(g))
    return tuple(e), tuple(1 - x for x in e), tuple((base - 1) * e[t] for t in range(len(g)) if g[t])


def outer_state(g):
    return (0,) * len(g), tuple(g), (1,) * sum(g)


def verify_column(base, g, source, target, column):
    """Direct scalar divisions plus the temporal coefficient equation."""
    check_state(base, g, source)
    check_state(base, g, target)
    require(isinstance(column, (tuple, list)) and len(column) == len(g)
            and all(type(x) is int and 0 <= x <= 2 * base - 2 for x in column),
            "invalid coefficient row")
    old_l, old_h, old_y = source
    new_l, new_h, new_y = target
    slot = 0
    for t, x in enumerate(column):
        out_l, low_digit = divmod(x + old_l[t], base)
        out_h, high_digit = divmod(x + new_h[t], base)
        require(out_l == new_l[t] and out_h == old_h[t], f"phase {t}: carry equation")
        if g[t]:
            require(new_y[slot] == high_digit, f"phase {t}: stored output digit")
            partner = old_y[slot]
            slot += 1
        else:
            partner = high_digit
        require(column[(t + 1) % len(g)] == low_digit + partner,
                f"phase {t}: temporal coefficient equation")


def retain_edge(outputs, key, column, cap):
    """Keep a physical first-column witness before deduplicating its cut.

    A zero-containing row reaching the physical outer cut can occur in the
    interior.  It must not hide a later row whose every phase is positive.
    """
    if key not in outputs:
        if len(outputs) >= cap:
            raise BudgetExceeded("per-predecessor output cap reached before insertion")
        outputs[key] = tuple(column)
    elif all(x > 0 for x in column) and not all(x > 0 for x in outputs[key]):
        outputs[key] = tuple(column)


def independent_predecessors(base, g, successor, cap=300000, deadline=None):
    """Return all predecessor cuts with one verified coefficient row per cut.

    For each phase choose (x,old_L), with x in 0..2b-2, and use integer
    division to test new_L.  The supplied new_H determines old_H.  At g=1
    it also fixes the emitted digit new_Y.  Connect adjacent choices by
    x_next=low+high (g=0), or old_Y=x_next-low in 0..b-1 (g=1).
    The final connection closes time.  No gap-factorization formulas are
    used, so this can serve as a separate implementation of that method.
    """
    check_state(base, g, successor)
    require(type(cap) is int and cap > 0, "output cap must be positive")
    deadline = time.monotonic() + 60 if deadline is None else deadline
    new_l, new_h, new_y = successor
    period = len(g)
    options, by_x = [], []
    slot = 0
    for t in range(period):
        if time.monotonic() > deadline:
            raise BudgetExceeded("predecessor wall cap")
        values = []
        for x in range(2 * base - 1):
            high_out, high_digit = divmod(x + new_h[t], base)
            if g[t] and high_digit != new_y[slot]:
                continue
            for old_l in (0, 1):
                low_out, low_digit = divmod(x + old_l, base)
                if low_out == new_l[t]:
                    values.append((x, old_l, high_out, low_digit, high_digit))
        options.append(values)
        by_x.append({x: [option for option in values if option[0] == x]
                     for x in range(2 * base - 1)})
        slot += g[t]
    if any(not values for values in options):
        return {}
    selected = [None] * period
    outputs = {}

    def connect(t, current, following):
        if g[t]:
            return 0 <= following[0] - current[3] < base
        return following[0] == current[3] + current[4]

    def visit(t):
        if time.monotonic() > deadline:
            raise BudgetExceeded("predecessor wall cap")
        current = selected[t]
        if t + 1 == period:
            if not connect(t, current, selected[0]):
                return
            key = (tuple(option[1] for option in selected),
                   tuple(option[2] for option in selected),
                   tuple(selected[(k + 1) % period][0] - selected[k][3]
                         for k in range(period) if g[k]))
            retain_edge(outputs, key, [option[0] for option in selected], cap)
            return
        if g[t]:
            next_xs = range(current[3], current[3] + base)
        else:
            next_xs = (current[3] + current[4],)
        for x in next_xs:
            for following in by_x[t + 1].get(x, ()):
                selected[t + 1] = following
                visit(t + 1)

    for first in options[0]:
        selected[0] = first
        visit(0)
    return outputs


def independent_successors(base, g, source):
    """Small-case forward reference: enumerate inward carries in time."""
    check_state(base, g, source)
    old_l, old_h, old_y = source
    period = len(g)
    slots = {t: i for i, t in enumerate(t for t in range(period) if g[t])}
    column, new_h = [0] * period, [0] * period
    outputs = {}

    def visit(t, x, first):
        if t == period:
            if x != first:
                return
            new_l = tuple((column[k] + old_l[k]) // base for k in range(period))
            new_y = tuple((column[k] + new_h[k]) % base for k in slots)
            retain_edge(outputs, (new_l, tuple(new_h), new_y), column, 1000000)
            return
        column[t] = x
        for inward in (0, 1):
            out_h, right_digit = divmod(x + inward, base)
            if out_h != old_h[t]:
                continue
            new_h[t] = inward
            partner = old_y[slots[t]] if g[t] else right_digit
            nxt = (x + old_l[t]) % base + partner
            visit(t + 1, nxt, first)

    for first in range(2 * base - 1):
        visit(0, first, first)
    return outputs


def state_universe(base, g):
    for left in itertools.product((0, 1), repeat=len(g)):
        for right in itertools.product((0, 1), repeat=len(g)):
            for digits in itertools.product(range(base), repeat=sum(g)):
                yield left, right, digits


def reciprocal_selftest():
    states_checked = edge_pairs = positive_pairs = 0
    cases = [(base, period) for base in (2, 3) for period in (1, 2)] + [(10, 1)]
    for base, period in cases:
        for g in itertools.product((0, 1), repeat=period):
            universe = list(state_universe(base, g))
            expected = {state: {} for state in universe}
            for source in universe:
                for target, column in independent_successors(base, g, source).items():
                    verify_column(base, g, source, target, column)
                    expected[target][source] = all(x > 0 for x in column)
            for target in universe:
                actual = independent_predecessors(base, g, target)
                require(set(actual) == set(expected[target]), "forward/inverse predecessor mismatch")
                for source, column in actual.items():
                    verify_column(base, g, source, target, column)
                    require(all(x > 0 for x in column) == expected[target][source],
                            "positive first-column witness lost during deduplication")
                states_checked += 1
                edge_pairs += len(actual)
                positive_pairs += sum(expected[target].values())
    # Check that exceeding a real branching frontier cannot be labelled complete.
    overflow = False
    for target in state_universe(3, (1, 1)):
        if len(independent_predecessors(3, (1, 1), target)) > 1:
            try:
                independent_predecessors(3, (1, 1), target, cap=1)
            except BudgetExceeded:
                overflow = True
            break
    require(overflow, "output-cap control did not exercise a truncated frontier")
    return {"selftest": "PASS", "successor_cuts_checked": states_checked,
            "predecessor_pairs_checked": edge_pairs, "positive_pairs_checked": positive_pairs,
            "cap_control": "UNDECIDED", "new_lean_verification": False}


def exterior_raw(base, word, e, g):
    low, carry = integer_norm(base, word, 0)
    high, overflow = integer_norm(base, word[::-1], 1 - e)
    require(carry == e and overflow == g, "exterior stream mismatch")
    if g:
        return [x + y for x, y in zip(low + [(base - 1) * (1 - e)], [1] + high[::-1])]
    return [x + y for x, y in zip(low, high[::-1])]


def verify_exterior_words(base, e, g, words):
    require(type(base) is int and 2 <= base <= 62, "base outside 2..62")
    check_bits(g, "overflow stream")
    check_bits(e, "carry stream", len(g))
    require(isinstance(words, (tuple, list)) and len(words) == len(g), "wrong exterior count")
    require(bool(words[0]), "fixed-width exterior is empty")
    width = len(words[0])
    for t, word in enumerate(words):
        require(len(word) == width and word[0] > 0
                and all(type(x) is int and 0 <= x <= 2 * base - 2 for x in word),
                f"phase {t}: invalid exterior word")
        raw = exterior_raw(base, word, e[t], g[t])
        require(raw == list(words[(t + 1) % len(words)]) + [base - 1] * g[t],
                f"phase {t}: fixed-width exterior edge mismatch")
    return width


def word_cut(base, e, g, words, j):
    left, right, stored = [], [], []
    for t, word in enumerate(words):
        left.append(integer_norm(base, word[:j], 0)[1])
        right.append(integer_norm(base, word[j:][::-1], 1 - e[t])[1])
        if g[t]:
            if j == 0:
                stored.append(1)
            else:
                incoming = right[-1]
                stored.append((word[j - 1] + incoming) % base)
    return tuple(left), tuple(right), tuple(stored)


def load_mirror():
    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("agent117_fixture_loader", root / "calculation/neutral_band_search.py")
    loader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loader)
    return loader


def load_lean_fixtures():
    """Use the mirror solely as a parser for existing Lean constants."""
    loader = load_mirror()
    fixtures = loader._lean_certs()
    require(sorted(base for base, _ in fixtures) == [2, 4, 8, 11, 16, 17, 26, 32],
            "known fixture coverage incomplete")
    return fixtures


def known_controls(seconds=60):
    deadline = time.monotonic() + seconds
    summaries, columns_checked, edges_checked = [], 0, 0
    for base, edges in sorted(load_lean_fixtures()):
        e = tuple(integer_norm(base, edge[0], 0)[1] for edge in edges)
        g = tuple(integer_norm(base, edge[0][::-1], 1 - e[t])[1] for t, edge in enumerate(edges))
        width = max(len(edge[0]) for edge in edges) + 1
        words = [list(edge[0]) + [base - 1] * (width - len(edge[0])) for edge in edges]
        for t, edge in enumerate(edges):
            require(edge[2] == edges[(t + 1) % len(edges)][0], "known fixture exterior does not chain")
            require(exterior_raw(base, edge[0], e[t], g[t]) == edge[2] + [base - 1] * edge[4],
                    "known fixture original exterior edge mismatch")
        verify_exterior_words(base, e, g, words)
        cuts = [word_cut(base, e, g, words, j) for j in range(width + 1)]
        require(cuts[0] == outer_state(g), "known fixture physical boundary mismatch")
        require(cuts[-1] == terminal_state(base, e, g), "known fixture fixed target mismatch")
        predecessor_counts = []
        for j in range(width):
            row = tuple(word[j] for word in words)
            verify_column(base, g, cuts[j], cuts[j + 1], row)
            predecessors = independent_predecessors(base, g, cuts[j + 1], deadline=deadline)
            require(cuts[j] in predecessors, "known fixture missing from exact inverse")
            verify_column(base, g, cuts[j], cuts[j + 1], predecessors[cuts[j]])
            if j == 0:
                require(all(x > 0 for x in predecessors[cuts[j]]), "known positive first row lost")
            predecessor_counts.append(len(predecessors))
            columns_checked += 1
        edges_checked += len(edges)
        summaries.append({"base": base, "period": len(edges), "fixed_width": width,
                          "e": "".join(map(str, e)), "g": "".join(map(str, g)),
                          "inverse_frontier_counts": predecessor_counts})
    return {"known_controls": "PASS", "fixtures": summaries, "exterior_edges": edges_checked,
            "spatial_columns_checked": columns_checked, "new_lean_verification": False}


def reverse_layers(base, e, g, depth, cap=100000, seconds=30):
    """Fresh independent backward BFS; report only completed layers."""
    require(type(depth) is int and depth >= 0, "negative reverse depth")
    require(type(cap) is int and cap > 0, "nonpositive global state cap")
    target = terminal_state(base, e, g)
    check_state(base, g, target)
    started = time.monotonic()
    deadline = started + seconds
    seen, frontier, sizes, arcs = {target}, {target}, [1], []
    try:
        for _ in range(depth):
            following, count = set(), 0
            for state in frontier:
                predecessors = independent_predecessors(base, g, state, cap, deadline)
                count += len(predecessors)
                for predecessor in predecessors:
                    if time.monotonic() > deadline:
                        raise BudgetExceeded("reverse BFS wall cap")
                    if predecessor not in seen:
                        if len(seen) >= cap:
                            raise BudgetExceeded("global reverse-state cap before insertion")
                        seen.add(predecessor)
                        following.add(predecessor)
            arcs.append(count)
            frontier = following
            sizes.append(len(frontier))
        return {"status": "COMPLETE_REVERSE_LAYERS", "base": base, "period": len(g),
                "new_layer_sizes": sizes, "arcs_per_completed_layer": arcs, "visited": len(seen),
                "elapsed_seconds": round(time.monotonic() - started, 6),
                "full_graph_exhausted": not frontier, "exterior_existence_decided": False}
    except BudgetExceeded as error:
        return {"status": "UNDECIDED", "reason": str(error), "completed_new_layer_sizes": sizes,
                "arcs_per_completed_layer": arcs, "visited_including_partial_layer": len(seen),
                "elapsed_seconds": round(time.monotonic() - started, 6)}


def verify_record(record, cap=300000, seconds=60, assemble_target=False):
    require(type(record) is dict and record.get("format") == "agent117-fixed-driver-exterior-v1",
            "unknown exterior record format")
    base = record.get("base")
    require(type(record.get("e")) is str and type(record.get("g")) is str,
            "missing driver bitstrings")
    e, g = tuple(map(int, record["e"])), tuple(map(int, record["g"]))
    check_bits(e, "carry stream", len(g))
    check_state(base, g, terminal_state(base, e, g))
    if record.get("mode") == "predecessors":
        if record.get("status") != "COMPLETE" or record.get("complete") is not True:
            raise NoWitness("incomplete predecessor enumeration; no relation completeness certified")
        successor = unpack_state(record["successor"])
        check_state(base, g, successor)
        expected = independent_predecessors(base, g, successor, cap, time.monotonic() + seconds)
        supplied = {}
        require(type(record.get("predecessors")) is list, "missing predecessor array")
        for entry in record["predecessors"]:
            require(type(entry) is dict and set(entry) == {"state", "column"}, "invalid predecessor entry")
            source = unpack_state(entry["state"])
            require(source not in supplied, "duplicate predecessor state")
            verify_column(base, g, source, successor, entry["column"])
            supplied[source] = entry["column"]
        require(set(expected) == set(supplied), "incomplete or extraneous predecessor-key set")
        return {"status": "EXACT_PREDECESSOR_SET_VERIFIED", "base": base, "period": len(g),
                "count": len(expected), "all_supplied_columns_verified": True,
                "exterior_existence_decided": False, "new_lean_verification": False}
    if record.get("status") != "ACCEPT":
        raise NoWitness("status=" + str(record.get("status")) + "; no exterior word supplied; no negative verified")
    words = record.get("B")
    width = verify_exterior_words(base, e, g, words)
    require(record.get("width") == width and record.get("u") == list(g), "width or trim metadata mismatch")
    columns, cut_records = record.get("columns"), record.get("cuts")
    require(type(columns) is list and len(columns) == width, "incorrect column count")
    require(type(cut_records) is list and len(cut_records) == width + 1, "incorrect cut count")
    cuts = list(map(unpack_state, cut_records))
    require(cuts[0] == outer_state(g), "wrong physical outer boundary")
    require(cuts[-1] == terminal_state(base, e, g), "wrong fixed terminal boundary")
    for j in range(width + 1):
        require(cuts[j] == word_cut(base, e, g, words, j), "cut differs from whole-word carries")
        if j < width:
            require(columns[j] == [word[j] for word in words], "column/exterior transpose mismatch")
            verify_column(base, g, cuts[j], cuts[j + 1], columns[j])
    result = {"status": "EXTERIOR_CYCLE_VERIFIED", "base": base, "period": len(g),
              "width": width, "sum_g": sum(g), "whole_integer_edges_checked": len(g),
              "spatial_columns_checked": width, "center_cycle_checked": False,
              "certificate_verified": False, "new_lean_verification": False}
    if assemble_target:
        from p24_center_target import CENTERS, E, G, V, replay_centers
        require(base == 10 and e == E and g == G, "exterior does not have the Agent101 target driver")
        replay_centers()
        edges = [(list(words[t]), list(CENTERS[t]), list(words[(t + 1) % len(g)]),
                  list(CENTERS[(t + 1) % len(g)]), g[t], V[t]) for t in range(len(g))]
        mirror = load_mirror()
        require(mirror.cycleOK(base, edges, edges[0][0], edges[0][1]), "Python mirror rejects assembled certificate")
        result.update({"status": "PYTHON_CERTIFICATE_CANDIDATE", "center_cycle_checked": True,
                       "python_mirror_cycleOK": True, "certificate_verified": False,
                       "lean_verified": False, "edges": edges})
    return result


def cpp_controls(binary, seconds=30, mode="search"):
    """Validate actual optimized-search witnesses for all eight known bases."""
    require(seconds >= 1, "C++ controls require at least one second per invocation")
    cpp_seconds = int(seconds)
    summaries = []
    for base, edges in sorted(load_lean_fixtures()):
        e = tuple(integer_norm(base, edge[0], 0)[1] for edge in edges)
        g = tuple(integer_norm(base, edge[0][::-1], 1 - e[t])[1] for t, edge in enumerate(edges))
        command = [binary, "--base", str(base), "--e", "".join(map(str, e)),
                   "--g", "".join(map(str, g)), "--cap", "100000", "--seconds", str(cpp_seconds),
                   "--mode", mode]
        process = subprocess.run(command, text=True, capture_output=True, timeout=cpp_seconds + 5, check=True)
        record = json.loads(process.stdout)
        result = verify_record(record)
        summaries.append({"base": base, "period": len(g), "width": result["width"],
                          "reverse_visited": record["reverse_visited"]})
    return {"cpp_positive_controls": "PASS", "mode": mode, "fixtures": summaries,
            "whole_integer_and_cut_path_replay": True, "new_lean_verification": False}


def audit_completed_depths(record):
    """Audit capped-search metadata; this does not rerun the large graph.

    In the reviewed bidirectional loop, complete_depth=d is written only
    after every node at depth d has been expanded, and discovery of d+1 is
    therefore complete.  Intersections are checked before deduplication and
    before allocation caps.  Disjoint complete radii f,r exclude paths of
    length <=f+r, conditional on correctness of that search implementation.
    """
    require(record.get("format") == "agent117-fixed-driver-exterior-v1"
            and record.get("mode") == "bidirectional", "not a bidirectional record")
    require(type(record.get("e")) is str and type(record.get("g")) is str, "missing driver bitstrings")
    e, g = tuple(map(int, record["e"])), tuple(map(int, record["g"]))
    check_state(record.get("base"), g, terminal_state(record.get("base"), e, g))
    if record.get("complete") is True and record.get("status") == "EXHAUSTED":
        require(record.get("decision") == "NO_B_CYCLE", "inconsistent exhausted decision")
        depth = record.get("forward_complete_depth")
        frontiers = record.get("forward_frontiers")
        require(type(depth) is int and depth >= 0 and type(frontiers) is list
                and len(frontiers) == depth + 2 and frontiers[0] == 1 and frontiers[-1] == 0
                and all(type(x) is int and x > 0 for x in frontiers[:-1]),
                "forward exploration was not completely exhausted")
        visited, expanded, transitions = (record.get("forward_" + name)
                                          for name in ("visited", "expanded", "transitions"))
        require(all(type(x) is int and x >= 0 for x in (visited, expanded, transitions)),
                "invalid forward counts")
        require(visited == expanded == sum(frontiers), "full-forward state/expansion accounting mismatch")
        require(record.get("initial_states") == frontiers[1], "initial frontier accounting mismatch")
        require(transitions >= visited - 1, "fewer emissions than inserted forward states")
        duplicates = transitions - (visited - 1)
        observed_accepts = None
        if "all_e_audit_complete" in record:
            require(record["all_e_audit_complete"] is True, "accepting-cut audit marked incomplete despite forward exhaustion")
            observed_accepts = record.get("all_e_accepts")
            streams = record.get("accepted_e_streams")
            require(type(observed_accepts) is int and observed_accepts >= 0 and type(streams) is list
                    and observed_accepts == len(streams) == len(set(streams))
                    and all(type(s) is str and len(s) == len(record["g"]) and set(s) <= {"0", "1"}
                            for s in streams), "accepting-stream audit count mismatch")
            emissions, expansions = (record.get("accepting_forward_" + name) for name in ("emissions", "expansions"))
            require(type(emissions) is int and emissions >= 0 and type(expansions) is int and expansions >= 0,
                    "invalid accepting-cut counters")
            if observed_accepts == 0:
                require(emissions == expansions == 0, "empty accepting-stream set has nonzero occurrences")
            if duplicates == 0:
                require(observed_accepts == 0, "accepting neutral cut contradicts zero-duplicate self-loop lemma")
        return {"status": "FORWARD_EXHAUSTION_METADATA_AUDITED", "last_nonempty_depth": depth,
                "forward_states_including_provenance": visited, "forward_transitions": transitions,
                "duplicate_forward_emissions": duplicates,
                "direct_accepting_stream_count": observed_accepts,
                "every_carry_stream_excluded_conditional_on_search_correctness": duplicates == 0 or observed_accepts == 0,
                "scope": "this exact period and overflow stream; no claim for higher temporal multiples",
                "independent_full_graph_replay": False, "new_lean_verification": False}
    require(record.get("complete") is False and record.get("decision") == "UNDECIDED"
            and record.get("status") in {"STATE_CAP", "LOCAL_GAP_CAP", "OPERATION_CAP",
                                         "TIMEOUT", "DEPTH_CAP"}, "not an auditable capped record")
    fd, rd = record.get("forward_complete_depth"), record.get("complete_depth")
    require(type(fd) is int and fd >= 0 and type(rd) is int and rd >= -1,
            "initial positive frontier was not completed")
    ff, rf = record.get("forward_frontiers"), record.get("reverse_frontiers")
    for frontiers, depth in ((ff, fd), (rf, rd)):
        require(type(frontiers) is list and len(frontiers) == depth + 2 and frontiers[0] == 1
                and all(type(x) is int and x > 0 for x in frontiers), "inconsistent completed frontier array")
    require(record.get("initial_states") == ff[1], "positive initial frontier count mismatch")
    completed_f, completed_r = sum(ff), sum(rf)
    fv, rv = record.get("forward_visited"), record.get("reverse_visited")
    fe, re = record.get("forward_expanded"), record.get("reverse_expanded")
    require(all(type(x) is int and x >= 0 for x in (fv, rv, fe, re)), "invalid visited/expanded metadata")
    require(fv >= completed_f and rv >= completed_r, "visited count below completed layers")
    require(not (fv > completed_f and rv > completed_r), "both directions claim a partial current layer")
    require(sum(ff[:-1]) <= fe <= completed_f and sum(rf[:-1]) <= re <= completed_r,
            "expanded count inconsistent with completed layers")
    require(fv + rv <= record.get("cap", 0), "state cap exceeded")
    return {"status": "SEARCH_DEPTH_METADATA_AUDITED", "completed_forward_radius": fd + 1,
            "completed_reverse_radius": rd + 1, "completed_forward_states_including_provenance": completed_f,
            "completed_reverse_states": completed_r, "partial_forward_discoveries": fv - completed_f,
            "partial_reverse_discoveries": rv - completed_r,
            "partial_forward_expanded_sources": fe - sum(ff[:-1]),
            "partial_reverse_expanded_sources": re - sum(rf[:-1]),
            "excluded_width_conditional_on_search_correctness": fd + rd + 2,
            "independent_full_graph_replay": False, "all_width_exterior_decision": False,
            "new_lean_verification": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="C++ predecessor/search JSON files")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--known-controls", action="store_true")
    parser.add_argument("--predecessors", action="store_true")
    parser.add_argument("--reverse-layers", type=int)
    parser.add_argument("--cpp-controls", metavar="BINARY")
    parser.add_argument("--cpp-mode", choices=("search", "bidirectional"), default="search")
    parser.add_argument("--assemble-target", action="store_true")
    parser.add_argument("--audit-depths", action="store_true", help="audit completed search layers/counts; no full graph replay")
    parser.add_argument("--base", type=int, default=10)
    parser.add_argument("--g")
    parser.add_argument("--e")
    parser.add_argument("--L")
    parser.add_argument("--H")
    parser.add_argument("--Y", default="")
    parser.add_argument("--cap", type=int, default=300000)
    parser.add_argument("--seconds", type=float, default=60)
    args = parser.parse_args()
    require(0 < args.seconds <= 1800, "wall limit must be in (0,1800]")
    try:
        if args.selftest:
            print(json.dumps(reciprocal_selftest()))
        if args.known_controls:
            print(json.dumps(known_controls(args.seconds)))
        if args.cpp_controls:
            print(json.dumps(cpp_controls(args.cpp_controls, args.seconds, args.cpp_mode)))
        if args.reverse_layers is not None:
            require(args.e is not None and args.g is not None, "reverse layers require e/g")
            result = reverse_layers(args.base, tuple(map(int, args.e)), tuple(map(int, args.g)),
                                    args.reverse_layers, args.cap, args.seconds)
            print(json.dumps(result))
            if result["status"] == "UNDECIDED":
                return 2
        if args.predecessors:
            require(all(value is not None for value in (args.g, args.L, args.H)), "missing g/L/H")
            g = tuple(map(int, args.g))
            successor = unpack_state({"L": args.L, "H": args.H,
                                      "Y": list(map(int, args.Y.split(","))) if args.Y else []})
            started = time.monotonic()
            predecessors = independent_predecessors(args.base, g, successor, args.cap, started + args.seconds)
            for source, row in predecessors.items():
                verify_column(args.base, g, source, successor, row)
            print(json.dumps({"status": "COMPLETE_PREDECESSORS", "base": args.base,
                              "g": list(g), "target": pack_state(successor), "count": len(predecessors),
                              "predecessors": [{"state": pack_state(state), "column": list(column)}
                                               for state, column in sorted(predecessors.items())],
                              "elapsed_seconds": round(time.monotonic() - started, 6)}))
        for filename in args.files:
            record = json.loads(Path(filename).read_text())
            result = (audit_completed_depths(record) if args.audit_depths else
                      verify_record(record, args.cap, args.seconds, args.assemble_target))
            print(json.dumps({"file": filename, **result}))
        if not (args.selftest or args.known_controls or args.predecessors or args.files
                or args.cpp_controls or args.reverse_layers is not None):
            parser.error("choose a verification mode or supply witness JSON")
    except NoWitness as error:
        print(json.dumps({"status": "NO_WITNESS_VERIFIED", "reason": str(error)}))
        return 2
    except BudgetExceeded as error:
        print(json.dumps({"status": "UNDECIDED", "reason": str(error)}))
        return 2
    except subprocess.SubprocessError as error:
        print(json.dumps({"status": "CONTROL_PROCESS_FAILED", "reason": str(error)}))
        return 2
    except (ValueError, TypeError, KeyError) as error:
        print(json.dumps({"status": "INVALID", "reason": str(error)}))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
