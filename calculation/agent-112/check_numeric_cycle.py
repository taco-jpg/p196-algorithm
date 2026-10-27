#!/usr/bin/env python3
"""Independent finite validation of the numerical center-cycle criterion.

    python3 calculation/agent-112/check_numeric_cycle.py

These are COMPUTED controls, not an exterior search or a Lean certificate.
The references use direct digit/column arithmetic. Small interval graphs also
include numerically admissible states with no symmetric coefficient realization.
The test harness needs assertions; the production criterion is separately tested
under python -O with explicit positive and negative checks.
"""

from __future__ import annotations

import collections
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys

from center_integer import Center
from numeric_cycle import raw_numeric, check_edge, check_cycle, lift_cycle
from check_integer_state import (
    ROOT, digit_normalization, direct_center, direct_edge, read_known_certificates,
    state, trim_center, trim_exterior,
)


def interval_states(base: int, maximum_width: int):
    for width in range(1, maximum_width + 1):
        for signed in range(1 - base ** width, base ** width):
            if signed:
                yield Center(width, signed)


def coefficient_states(base: int, maximum_width: int) -> dict:
    result = {}
    for width in range(1, maximum_width + 1):
        for half in itertools.product(range(2 * base - 1), repeat=(width + 1) // 2):
            word = half + half[: width // 2][::-1]
            source = state(base, word)
            if source.signed:
                key = (width, source.signed)
                assert key not in result
                result[key] = word
    return result


def digit_pair_image(base: int, source: Center, overflow: int) -> tuple[int, ...]:
    """Construct the image using an ordinary fixed-width digit word.

    This never calls the numerical recurrence or a symmetry decoder. For a
    representable source it equals coefficient normalization; for an arbitrary
    interval source it still constructs a bounded symmetric output word.
    """
    incoming = int(source.signed < 0)
    numeral = source.signed - 1 if source.signed > 0 else base ** source.width + source.signed
    digits = []
    for _ in range(source.width):
        numeral, digit = divmod(numeral, base)
        digits.append(digit)
    assert numeral == 0
    if overflow:
        digits.append((base - 1) * incoming)
    return tuple(a + b for a, b in zip(digits, reversed(digits)))


def interval_images() -> dict:
    scopes = ((2, 7), (3, 5), (4, 4), (10, 3), (26, 2))
    total = missing = images = zero_images = 0
    rows = []
    for base, maximum_width in scopes:
        words = coefficient_states(base, maximum_width)
        count = absent = 0
        for source in interval_states(base, maximum_width):
            count += 1
            key = (source.width, source.signed)
            absent += int(key not in words)
            for overflow in (0, 1):
                reference = digit_pair_image(base, source, overflow)
                actual = raw_numeric(base, source, overflow)
                assert reference == reference[::-1]
                assert all(0 <= c <= 2 * base - 2 for c in reference)
                assert actual == state(base, reference)
                if key in words:
                    raw, _, _ = direct_center(base, words[key], int(source.signed < 0), overflow)
                    assert raw == reference
                images += 1
                zero_images += int(actual.signed == 0)
        rows.append({"base": base, "maximum_width": maximum_width,
                     "interval_states": count, "nonrepresentable_sources": absent})
        total += count
        missing += absent
    witness = Center(2, 1)
    assert (2, 1) not in coefficient_states(10, 2)
    image = digit_pair_image(10, witness, 0)
    assert image == (0, 0)
    assert raw_numeric(10, witness, 0) == Center(2, -99)
    assert check_edge(10, witness, Center(2, -99), 0, 0, 0)
    return {"scopes": rows, "interval_states": total, "nonrepresentable_sources": missing,
            "images": images, "zero_images": zero_images,
            "one_step_image_example": {"base": 10, "source": [2, 1], "image": [2, -99],
                                       "image_coefficients": list(image)}}


def strongly_connected(graph: dict) -> list[set]:
    """Independent iterative Kosaraju decomposition of a finite directed graph."""
    nodes = set(graph)
    reverse = {node: set() for node in nodes}
    adjacency = {}
    for node, transitions in graph.items():
        adjacency[node] = {edge[0] for edge in transitions}
        for target in adjacency[node]:
            assert target in nodes
            reverse[target].add(node)
    order, seen = [], set()
    for start in sorted(nodes):
        if start in seen:
            continue
        seen.add(start)
        stack = [(start, iter(adjacency[start]))]
        while stack:
            node, targets = stack[-1]
            try:
                target = next(targets)
            except StopIteration:
                order.append(node)
                stack.pop()
                continue
            if target not in seen:
                seen.add(target)
                stack.append((target, iter(adjacency[target])))
    components, seen = [], set()
    for start in reversed(order):
        if start in seen:
            continue
        component, todo = set(), [start]
        seen.add(start)
        while todo:
            node = todo.pop()
            component.add(node)
            for predecessor in reverse[node]:
                if predecessor not in seen:
                    seen.add(predecessor)
                    todo.append(predecessor)
        components.append(component)
    return components


def cyclic_components(graph: dict) -> list[set]:
    return [component for component in strongly_connected(graph)
            if len(component) > 1 or any(edge[0] == node for node in component for edge in graph[node])]


def component_cycle(graph: dict, component: set) -> list[tuple]:
    """Return one actual labeled circuit, using BFS inside one cyclic SCC."""
    source = min(component)
    first = min(edge for edge in graph[source] if edge[0] in component)
    target = first[0]
    if target == source:
        return [(source, *first)]
    queue = collections.deque([target])
    previous = {target: None}
    while source not in previous:
        node = queue.popleft()
        for edge in sorted(graph[node]):
            nxt = edge[0]
            if nxt in component and nxt not in previous:
                previous[nxt] = (node, edge)
                queue.append(nxt)
    tail, node = [], source
    while node != target:
        predecessor, edge = previous[node]
        tail.append((predecessor, *edge))
        node = predecessor
    return [(source, *first)] + list(reversed(tail))


def cycle_edges(graph: dict, components: list[set]) -> set:
    result = set()
    for component in components:
        for source in component:
            result.update((source, *edge) for edge in graph[source] if edge[0] in component)
    return result


def finite_graphs() -> dict:
    scopes = ((2, 6), (3, 4), (4, 4), (10, 3))
    rows = []
    for base, maximum_width in scopes:
        words = coefficient_states(base, maximum_width)
        numerical = {(s.width, s.signed): set() for s in interval_states(base, maximum_width)}
        coefficient = {node: set() for node in words}
        # Exhaust all arithmetic edges; interval domain and trim range are finite.
        for node in numerical:
            source = Center(*node)
            incoming = int(source.signed < 0)
            for overflow in (0, 1):
                raw = raw_numeric(base, source, overflow)
                for trim in range((raw.width - 1) // 2 + 1):
                    divisor = base ** trim
                    if raw.signed % divisor:
                        continue
                    target = (raw.width - 2 * trim, raw.signed // divisor)
                    if target not in numerical:
                        continue
                    assert check_edge(base, source, Center(*target), incoming, overflow, trim)
                    assert not check_edge(base, source, Center(*target), 1 - incoming, overflow, trim)
                    assert not check_edge(base, source, Center(*target), incoming, 1 - overflow, trim)
                    assert not check_edge(base, source, Center(*target), incoming, overflow, trim + 1)
                    assert not check_edge(base, source, Center(target[0], target[1] + 1), incoming, overflow, trim)
                    numerical[node].add((target, incoming, overflow, trim))
                    assert target in words, ("arithmetic image is not representable", base, node, target)
        # Independently build all literal coefficient-trim edges.
        for node, word in words.items():
            source = Center(*node)
            incoming = int(source.signed < 0)
            for overflow in (0, 1):
                raw, _, _ = direct_center(base, word, incoming, overflow)
                for trim in range((len(raw) - 1) // 2 + 1):
                    if trim and (any(c != base - 1 for c in raw[:trim])
                                 or any(c != base - 1 for c in raw[-trim:])):
                        continue
                    target_word = raw[trim:len(raw) - trim] if trim else raw
                    target_state = state(base, target_word)
                    target = (target_state.width, target_state.signed)
                    if target not in coefficient:
                        continue
                    assert words[target] == target_word
                    coefficient[node].add((target, incoming, overflow, trim))
            assert numerical[node] == coefficient[node], (base, node)
        num_components = cyclic_components(numerical)
        coef_components = cyclic_components(coefficient)
        assert {frozenset(c) for c in num_components} == {frozenset(c) for c in coef_components}
        assert cycle_edges(numerical, num_components) == cycle_edges(coefficient, coef_components)
        checked_cycles, maximum_period = 0, 0
        for component in num_components:
            circuit = component_cycle(numerical, component)
            states = [Center(*edge[0]) for edge in circuit]
            carries = [edge[2] for edge in circuit]
            overflows = [edge[3] for edge in circuit]
            trims = [edge[4] for edge in circuit]
            assert check_cycle(base, states, carries, overflows, trims)
            lifted = lift_cycle(base, states, carries, overflows, trims)
            assert lifted == tuple(words[edge[0]] for edge in circuit)
            checked_cycles += 1
            maximum_period = max(maximum_period, len(circuit))
        rows.append({"base": base, "maximum_width": maximum_width,
                     "numerical_states": len(numerical), "coefficient_states": len(coefficient),
                     "numerical_edges": sum(map(len, numerical.values())),
                     "coefficient_edges": sum(map(len, coefficient.values())),
                     "cyclic_states": sum(map(len, num_components)),
                     "cyclic_edges": len(cycle_edges(numerical, num_components)),
                     "checked_circuits": checked_cycles, "maximum_checked_period": maximum_period})
    return {"scopes": rows, "checked_circuits": sum(row["checked_circuits"] for row in rows)}


def normalized_edges(base: int, edges: list) -> list:
    result = []
    for exterior, center, exterior2, center2, _, _ in edges:
        b0, _ = trim_exterior(base, exterior)
        c0, _ = trim_center(base, center)
        b1, _ = trim_exterior(base, exterior2)
        c1, _ = trim_center(base, center2)
        raw_b, raw_c, _, _ = direct_edge(base, b0, c0)
        actual_b, u = trim_exterior(base, raw_b)
        actual_c, v = trim_center(base, raw_c)
        assert (actual_b, actual_c) == (b1, c1)
        result.append((b0, c0, b1, c1, u, v))
    return result


def consolidate_trims(base: int, edges: list, repetitions: int) -> list:
    """Move every center trim in a repeated cycle to its last transition.

    Padding after t steps is the cumulative original trimming before t. The
    final edge removes that padding, giving one trim equal to the full total.
    The independent exterior and its u values remain the original repeated data.
    """
    repeated = edges * repetitions
    offsets, total = [], 0
    for edge in repeated:
        offsets.append(total)
        total += edge[5]
    result = []
    for index, (exterior, center, exterior2, center2, u, v) in enumerate(repeated):
        before, after = offsets[index], offsets[index + 1] if index + 1 < len(repeated) else 0
        pad0, pad1 = (base - 1,) * before, (base - 1,) * after
        new_v = before + v - after
        assert new_v >= 0
        result.append((exterior, pad0 + center + pad0, exterior2, pad1 + center2 + pad1, u, new_v))
    assert sum(edge[5] for edge in result[:-1]) == 0
    assert result[-1][5] == total
    return result


def load_mirror():
    path = ROOT / "calculation/neutral_band_search.py"
    spec = importlib.util.spec_from_file_location("agent112_known_control_mirror", path)
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    return mirror


def check_known_cycle(base: int, edges: list, mirror) -> tuple[list, list, list, list]:
    states, carries, overflows, trims = [], [], [], []
    for index, (exterior, center, exterior2, center2, u, v) in enumerate(edges):
        assert edges[(index + 1) % len(edges)][:2] == (exterior2, center2)
        raw_b, raw_c, incoming, overflow = direct_edge(base, exterior, center)
        assert raw_b == exterior2 + (base - 1,) * u
        assert raw_c == (base - 1,) * v + center2 + (base - 1,) * v
        source, target = state(base, center), state(base, center2)
        assert check_edge(base, source, target, incoming, overflow, v)
        states.append(source)
        carries.append(incoming)
        overflows.append(overflow)
        trims.append(v)
    assert check_cycle(base, states, carries, overflows, trims)
    lifted = lift_cycle(base, states, carries, overflows, trims)
    assert lifted == tuple(edge[1] for edge in edges)
    replay = []
    for index, edge in enumerate(edges):
        exterior, _, exterior2, _, u, v = edge
        replay.append((list(exterior), list(lifted[index]), list(exterior2),
                       list(lifted[(index + 1) % len(edges)]), u, v))
    assert mirror.cycleOK(base, replay, replay[0][0], replay[0][1])
    wrong_carries = list(carries)
    wrong_carries[0] ^= 1
    assert not check_cycle(base, states, wrong_carries, overflows, trims)
    return states, carries, overflows, trims


def known_controls() -> tuple[dict, tuple]:
    mirror = load_mirror()
    rows, optimized_fixture = [], None
    for base, original in read_known_certificates():
        fixture = check_known_cycle(base, original, mirror)
        if base == 2:
            optimized_fixture = fixture
        normalized = normalized_edges(base, original)
        check_known_cycle(base, normalized, mirror)
        padded_counts = {}
        for repetitions in (3, 5):
            padded = consolidate_trims(base, original, repetitions)
            check_known_cycle(base, padded, mirror)
            assert max(edge[5] for edge in padded) == repetitions
            padded_counts[str(repetitions)] = len(padded)
        rows.append({"base": base, "original_edges": len(original),
                     "normalized_edges": len(normalized), "consolidated_edges_by_repetition": padded_counts})
    result = {"bases": rows, "original_edges": sum(row["original_edges"] for row in rows),
              "normalized_edges": sum(row["normalized_edges"] for row in rows),
              "consolidated_edges": sum(sum(row["consolidated_edges_by_repetition"].values()) for row in rows),
              "mirror_accepted_full_cycles": 4 * len(rows)}
    return result, optimized_fixture


BASE20_SOURCE = {
    "agent": "Agent 116",
    "pull_request": "https://github.com/taco-jpg/p196-algorithm/pull/356",
    "commit": "b7a718b78d67cf54d362232ba1b8f90fbec23af8",
    "path": "lean/P196/Agent116Base20Certificate/Certificate.lean",
    "blob": "de0a77c31c261a2584b35402c961ac833e043b5d",
    "canonical_edges_sha256": "14f5c26c2feed05b59e90441d513cd94bc6b1d4b9ced0d2d2cd9fddbbdcf9d6a",
}


def published_base20_fixture() -> list:
    """Reconstruct exactly Agent 116's published eight-edge positive fixture.

    Initial words and trim data below are transcribed from the pinned Lean
    source identified by BASE20_SOURCE. The independent direct arithmetic
    regenerates all edges, whose canonical-data hash must equal the hash of
    the eight fully parsed source edges. This needs no network or unmerged
    dependency at test time and does not confer Lean status on this checker.
    """
    exterior = (2, 19, 20, 13, 9, 25, 15, 26, 28, 14, 12, 16, 14, 13, 12, 13, 11, 5, 7, 12, 5, 7, 11, 20, 16, 11, 17, 10, 16, 27, 16, 16, 23, 12, 8, 7, 20, 32, 31, 34, 34, 27, 15, 4, 16, 20, 9, 23, 35, 29, 23, 20, 19, 22, 25, 30, 31, 28, 17, 9, 7, 12, 17, 17, 23, 22, 27, 34, 20, 21, 29, 22, 25, 21, 20, 12, 35, 31, 17, 16, 30, 32, 23, 12, 8, 15, 14, 2, 2, 11, 9)
    center = (28, 26, 26, 9, 13, 22, 13, 17, 31, 35, 35, 32, 23, 23, 32, 35, 35, 31, 17, 13, 22, 13, 9, 26, 26, 28)
    initial = (exterior, center)
    us, vs = "10001000", "00000010"
    expected_e, expected_g = "01001011", "00010001"
    edges = []
    for phase, (u, v) in enumerate(zip(map(int, us), map(int, vs))):
        raw_b, raw_c, incoming, overflow = direct_edge(20, exterior, center)
        assert (incoming, overflow) == (int(expected_e[phase]), int(expected_g[phase]))
        following_b = raw_b[:-u] if u else raw_b
        following_c = raw_c[v:-v] if v else raw_c
        assert raw_b == following_b + (19,) * u
        assert raw_c == (19,) * v + following_c + (19,) * v
        edges.append((exterior, center, following_b, following_c, u, v))
        exterior, center = following_b, following_c
    assert (exterior, center) == initial
    encoded = json.dumps(edges, separators=(",", ":")).encode("ascii")
    assert hashlib.sha256(encoded).hexdigest() == BASE20_SOURCE["canonical_edges_sha256"]
    return edges


def published_base20_controls() -> dict:
    """Additional ninth-base controls; the eight main-source fixtures stay separate."""
    original = published_base20_fixture()
    mirror = load_mirror()
    check_known_cycle(20, original, mirror)
    normalized = normalized_edges(20, original)
    check_known_cycle(20, normalized, mirror)
    padded_counts = {}
    for repetitions in (3, 5):
        padded = consolidate_trims(20, original, repetitions)
        check_known_cycle(20, padded, mirror)
        assert max(edge[5] for edge in padded) == repetitions
        padded_counts[str(repetitions)] = len(padded)
    return {"status": "COMPUTED", "source": BASE20_SOURCE,
            "original_edges": len(original), "normalized_edges": len(normalized),
            "consolidated_edges_by_repetition": padded_counts,
            "consolidated_edges": sum(padded_counts.values()),
            "mirror_accepted_full_cycles": 4}


def sign_control() -> dict:
    coefficients = (0, 2, 6, 14, 8, 18, 16, 12, 4, 10)
    states = [state(10, (coefficient,)) for coefficient in coefficients]
    carries = [int(source.signed < 0) for source in states]
    assert check_cycle(10, states, carries, [0] * 10, [0] * 10)
    assert lift_cycle(10, states, carries, [0] * 10, [0] * 10) == tuple((c,) for c in coefficients)
    magnitudes = [abs(source.signed) for source in states]
    assert magnitudes[:5] == magnitudes[5:]
    assert states[5].signed == -states[0].signed
    assert not check_cycle(10, states[:5], carries[:5], [0] * 5, [0] * 5)
    return {"base": 10, "coefficients": coefficients, "signed_period": 10,
            "magnitude_period": 5, "signed_values": [source.signed for source in states],
            "scope": "center-only zero-overflow circuit; no exterior or decimal certificate"}


def malformed_controls(fixture: tuple) -> dict:
    states, carries, overflows, trims = fixture
    source, target = states[0], states[1]
    incoming, overflow, trim = carries[0], overflows[0], trims[0]
    invalid_sources = (Center(0, 0), Center(-1, 1), Center(1, 0), Center(1, 2),
                       Center(True, 1), Center(1, True), Center(1, 0.5), (1, 1), None)
    raw_rejections = edge_rejections = cycle_rejections = lift_rejections = 0
    for bad in invalid_sources:
        try:
            raw_numeric(2, bad, overflow)
        except ValueError:
            raw_rejections += 1
        else:
            raise AssertionError(("malformed raw source accepted", bad))
        assert not check_edge(2, bad, target, incoming, overflow, trim)
        assert not check_edge(2, source, bad, incoming, overflow, trim)
        edge_rejections += 2
    for bad_base in (1, True, 2.0, "2"):
        assert not check_edge(bad_base, source, target, incoming, overflow, trim)
        assert not check_cycle(bad_base, states, carries, overflows, trims)
        edge_rejections += 1
        cycle_rejections += 1
    bad_edge_arguments = ((2, overflow, trim), (True, overflow, trim),
                          (incoming, 2, trim), (incoming, True, trim),
                          (incoming, overflow, -1), (incoming, overflow, True),
                          (incoming, overflow, 0.5))
    for e, g, v in bad_edge_arguments:
        assert not check_edge(2, source, target, e, g, v)
        edge_rejections += 1
    bad_arrays = (
        ([], [], [], []), (states[:-1], carries, overflows, trims),
        (states, carries[:-1], overflows, trims), (states, carries, overflows[:-1], trims),
        (states, carries, overflows, trims[:-1]), (None, carries, overflows, trims),
        (iter(states), carries, overflows, trims), ("bad", carries, overflows, trims),
        (states, [True] + carries[1:], overflows, trims),
        (states, carries, [True] + overflows[1:], trims),
        (states, carries, overflows, [-1] + trims[1:]),
        ([Center(1, 0)] + states[1:], carries, overflows, trims),
        ([states[1]] + states[1:], carries, overflows, trims),
    )
    for arguments in bad_arrays:
        assert not check_cycle(2, *arguments)
        cycle_rejections += 1
        try:
            lift_cycle(2, *arguments)
        except ValueError:
            lift_rejections += 1
        else:
            raise AssertionError("malformed cycle lift accepted")
    return {"raw_rejections": raw_rejections, "edge_rejections": edge_rejections,
            "cycle_rejections": cycle_rejections, "lift_rejections": lift_rejections}


def optimized_controls(fixture: tuple) -> dict:
    states, carries, overflows, trims = fixture
    payload = json.dumps({"states": [[s.width, s.signed] for s in states],
                          "carries": carries, "overflows": overflows, "trims": trims})
    # Deliberately no assert statements: these checks must survive python -O.
    program = r'''
import json,sys
from center_integer import Center
from numeric_cycle import raw_numeric,check_edge,check_cycle,lift_cycle
d=json.load(sys.stdin)
s=[Center(*x) for x in d['states']]
e,g,v=d['carries'],d['overflows'],d['trims']
if not check_cycle(2,s,e,g,v): raise SystemExit('optimized positive rejected')
lifted=lift_cycle(2,s,e,g,v)
if len(lifted)!=len(s): raise SystemExit('optimized lift length failure')
if lifted[0]!=(0,0): raise SystemExit('optimized lift data failure')
bad=list(e);bad[0]^=1
if check_cycle(2,s,bad,g,v): raise SystemExit('optimized wrong carry accepted')
if check_cycle(2,[],[],[],[]): raise SystemExit('optimized empty cycle accepted')
if check_cycle(2,s[:-1],e,g,v): raise SystemExit('optimized lengths accepted')
if check_edge(2,s[0],s[1],e[0],g[0],-1): raise SystemExit('optimized negative trim accepted')
if check_edge(2,s[0],s[1],bool(e[0]),g[0],v[0]): raise SystemExit('optimized boolean carry accepted')
if check_edge(2,Center(1,0),s[1],e[0],g[0],v[0]): raise SystemExit('optimized zero accepted')
try: raw_numeric(2,Center(1,0),0)
except ValueError: pass
else: raise SystemExit('optimized raw zero accepted')
try: lift_cycle(2,s,bad,g,v)
except ValueError: pass
else: raise SystemExit('optimized invalid lift accepted')
print('OPTIMIZED_POSITIVE_AND_NEGATIVE_PASS')
'''
    process = subprocess.run([sys.executable, "-O", "-c", program], cwd=Path(__file__).resolve().parent,
                             input=payload, text=True, capture_output=True, timeout=30)
    assert process.returncode == 0, (process.returncode, process.stdout, process.stderr)
    assert process.stdout.strip() == "OPTIMIZED_POSITIVE_AND_NEGATIVE_PASS"
    return {"returncode": process.returncode, "result": process.stdout.strip()}


def main() -> None:
    if not __debug__:
        raise SystemExit("Run this harness without -O; it separately probes optimized production code.")
    known, fixture = known_controls()
    output = {"status": "COMPUTED", "known_controls": known,
              "published_base20_controls": published_base20_controls(),
              "interval_images": interval_images(), "finite_graphs": finite_graphs(),
              "sign_control": sign_control(), "malformed_controls": malformed_controls(fixture),
              "optimized_controls": optimized_controls(fixture)}
    print(json.dumps(output, indent=2, sort_keys=True))
    print("PASS: numerical cycle acceptance and lifting agree with independent coefficient arithmetic.")


if __name__ == "__main__":
    main()
