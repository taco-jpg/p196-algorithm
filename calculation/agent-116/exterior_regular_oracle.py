#!/usr/bin/env python3
"""Independent controls for typed exterior-block regular-language searches.

Uses the Python standard library only. Local tiles are obtained by enumerating
every reverse-carry bit word. Regular-language checks use an explicit NFA
product with the returned DFA, so agreement is over all words, not a finite
sample. These controls do not themselves establish the research negative.
"""

import argparse
import collections
import functools
import hashlib
import io
import itertools
import json
import random
import subprocess
import time


OPTIMIZATION_MODES = tuple(itertools.product((False, True), repeat=2))


def optimization_flags(streaming, bisimulation):
    return (["--stream-anchors"] if streaming else []) + (["--nfa-bisim"] if bisimulation else [])


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_tiles(base, length, source, start, first):
    """Unoptimized exhaustive inward-carry words; no block-engine import."""
    mask = (1 << length) - 1
    low = source & mask
    high = (source >> length) & mask
    lag = source >> (2 * length)
    result = []
    for inward_word in range(1 << length):
        coefficient = start
        target_low = 0
        target_lag = None
        coefficients = []
        for position in range(length):
            if first and coefficient == 0:
                break
            inward = (inward_word >> position) & 1
            reverse_total = coefficient + inward
            if reverse_total // base != (high >> position) & 1:
                break
            low_total = coefficient + ((low >> position) & 1)
            target_low |= (low_total // base) << position
            reverse_digit = reverse_total % base
            if position == 0:
                target_lag = reverse_digit
            coefficients.append(coefficient)
            coefficient = low_total % base + (lag if position == 0 else reverse_digit)
            require(0 <= coefficient <= 2 * base - 2,
                    "local recurrence left the coefficient alphabet")
        else:
            target = target_low | (inward_word << length) | (target_lag << (2 * length))
            result.append((target, coefficient, tuple(coefficients)))
    return sorted(result)


def check_tiles(executable):
    rows = []
    specifications = [(10, length) for length in range(1, 6)]
    specifications += [(base, length) for base in (2, 3) for length in range(1, 4)]
    for base, length in specifications:
        for first in (False, True):
            command = [executable, str(base), str(length), "--dump", "--witness"]
            if first:
                command.append("--first")
            run = subprocess.run(command, capture_output=True, text=True,
                                 check=True, timeout=60)
            output = io.StringIO(run.stdout)
            count = 0
            digest = hashlib.sha256()
            for source in range(base * 4 ** length):
                for start in range(2 * base - 1):
                    for target, ending, coefficients in local_tiles(base, length, source, start, first):
                        expected = (source, start, target, ending) + coefficients
                        line = output.readline()
                        require(bool(line), ("missing local tile", base, length, first, expected))
                        actual = tuple(map(int, line.split()))
                        require(actual == expected,
                                ("local tile mismatch", base, length, first, expected, actual))
                        digest.update((" ".join(map(str, expected)) + "\n").encode())
                        count += 1
            require(not output.read().strip(), ("unexpected extra tiles", base, length, first))
            rows.append({"base": base, "length": length, "first": first,
                         "tiles": count, "sha256_with_coefficients": digest.hexdigest()})
    return {"status": "PASS", "queries": len(rows),
            "tiles_compared": sum(row["tiles"] for row in rows), "results": rows}


def nfa(states, initial, final, edges):
    require(all(0 <= q < states for q in list(initial) + list(final)), "invalid NFA boundary")
    require(all(0 <= source < states and 0 <= target < states and symbol >= 0
                for source, symbol, target in edges), "invalid NFA edge")
    return {"states": states, "initial": set(initial), "final": set(final), "edges": list(edges)}


def nfa_adjacency(machine):
    adjacency = [collections.defaultdict(set) for _ in range(machine["states"])]
    for source, symbol, target in machine["edges"]:
        adjacency[source][symbol].add(target)
    return adjacency


def read_dfa(output):
    payload = json.loads(output)
    require(payload["status"] == "OK", payload)
    machine = payload["dfa"]
    states = machine["states"]
    require(states and 0 <= machine["start"] < len(states), "invalid DFA start")
    for row in states:
        require(isinstance(row["final"], bool), "DFA final marker is not Boolean")
        symbols = [symbol for symbol, _ in row["edges"]]
        require(len(symbols) == len(set(symbols)), "nondeterministic DFA output")
        require(all(0 <= target < len(states) for _, target in row["edges"]), "invalid DFA target")
    return machine


def nfa_dfa_equivalent(expected, actual):
    """Exact subset/product traversal, including an implicit rejecting sink."""
    adjacency = nfa_adjacency(expected)
    dfa_edges = [dict(row["edges"]) for row in actual["states"]]
    first = (frozenset(expected["initial"]), actual["start"])
    queue = collections.deque([(first, ())])
    seen = {first}
    while queue:
        (subset, state), word = queue.popleft()
        left_final = bool(subset & expected["final"])
        right_final = state is not None and actual["states"][state]["final"]
        require(left_final == right_final,
                {"language_mismatch_at": word, "expected": left_final, "actual": right_final})
        symbols = set()
        for source in subset:
            symbols.update(adjacency[source])
        if state is not None:
            symbols.update(dfa_edges[state])
        for symbol in sorted(symbols):
            target_subset = frozenset(target for source in subset
                                      for target in adjacency[source].get(symbol, ()))
            target_state = None if state is None else dfa_edges[state].get(symbol)
            pair = (target_subset, target_state)
            if pair not in seen:
                seen.add(pair)
                queue.append((pair, word + (symbol,)))
    return len(seen)


def encode_nfa(machine):
    initial, final = sorted(machine["initial"]), sorted(machine["final"])
    lines = [f'N {machine["states"]} {len(initial)} {len(final)} {len(machine["edges"])}',
             " ".join(map(str, initial)), " ".join(map(str, final))]
    lines.extend(f"{source} {symbol} {target}" for source, symbol, target in machine["edges"])
    return "\n".join(lines) + "\n"


def permute_nfa(machine):
    permutation = list(reversed(range(machine["states"])))
    return nfa(machine["states"], [permutation[q] for q in machine["initial"]],
               [permutation[q] for q in machine["final"]],
               [(permutation[q], a, permutation[r]) for q, a, r in reversed(machine["edges"])])


def explicit_cyclic_product(input_dfa, controls, tiles):
    """Dense NFA product (anchor coefficient, input state, live coefficient)."""
    size = len(input_dfa["states"])

    def index(anchor, state, current):
        return (anchor * size + state) * controls + current

    initial = [index(anchor, input_dfa["start"], anchor) for anchor in range(controls)]
    final = [index(anchor, state, anchor) for anchor in range(controls)
             for state, row in enumerate(input_dfa["states"]) if row["final"]]
    edges = []
    for anchor in range(controls):
        for state, row in enumerate(input_dfa["states"]):
            for input_symbol, target in row["edges"]:
                for tile_input, output, entering, leaving in tiles:
                    if tile_input == input_symbol:
                        edges.append((index(anchor, state, entering), output,
                                      index(anchor, target, leaving)))
    return nfa(size * controls * controls, initial, final, edges)


def encode_model(input_dfa, controls, tiles):
    states = input_dfa["states"]
    final = [q for q, row in enumerate(states) if row["final"]]
    edges = [(q, a, r) for q, row in enumerate(states) for a, r in row["edges"]]
    lines = [f'A {len(states)} {input_dfa["start"]} {len(final)} {len(edges)}',
             " ".join(map(str, final))]
    lines.extend(f"{q} {a} {r}" for q, a, r in edges)
    lines.append(f"T {controls} {len(tiles)}")
    lines.extend(" ".join(map(str, tile)) for tile in tiles)
    return "\n".join(lines) + "\n"


def dfa_accepts(machine, word):
    state = machine["start"]
    for symbol in word:
        state = dict(machine["states"][state]["edges"]).get(symbol)
        if state is None:
            return False
    return machine["states"][state]["final"]


def check_regular(executable):
    fixtures = [
        nfa(1, [0], [], []),
        nfa(1, [0], [0], []),
        nfa(2, [], [1], [(0, 1, 1)]),
        nfa(2, [0], [1], [(0, 1, 1), (1, 1, 1)]),
        nfa(3, [0], [1], [(0, 1, 1), (1, 2, 2), (2, 2, 1)]),
        nfa(4, [0, 1], [2], [(0, 1, 0), (0, 1, 2), (1, 2, 2),
                              (2, 1, 3), (3, 2, 2), (2, 3, 2)]),
        nfa(3, [0], [0, 1, 2], [(0, 1, 1), (1, 1, 2)]),
        nfa(4, [0], [0, 1, 2, 3], [(0, 1, 1), (1, 1, 2), (2, 1, 3)]),
        nfa(2, [0], [0, 1], [(0, 1, 1), (1, 1, 0)]),
        nfa(3, [0], [0, 1, 2], [(0, 1, 1), (1, 1, 2), (2, 1, 0),
                                 (0, 2, 0), (2, 2, 1)]),
    ]
    rng = random.Random(116)
    for _ in range(18):
        size = rng.randrange(2, 7)
        initial = [q for q in range(size) if rng.randrange(3) == 0]
        final = [q for q in range(size) if rng.randrange(3) == 0]
        edges = [(q, symbol, r) for q in range(size) for symbol in range(3)
                 for r in range(size) if rng.randrange(5) == 0]
        fixtures.append(nfa(size, initial, final, edges))
    duplicate_targets = nfa(7, [0], [6],
        [(0, 1, 1), (0, 1, 2), (1, 2, 3), (1, 2, 3),
         (2, 2, 4), (2, 2, 5), (3, 3, 6), (4, 3, 6), (5, 3, 6)])
    duplicate_targets["expected_bisim_states"] = 4
    language_equal_not_bisimilar = nfa(7, [0], [6],
        [(0, 4, 1), (0, 4, 2), (1, 1, 3), (1, 1, 4), (2, 1, 5),
         (3, 2, 6), (4, 3, 6), (5, 2, 6), (5, 3, 6)])
    language_equal_not_bisimilar["expected_bisim_states"] = 7
    fixtures.extend([duplicate_targets, language_equal_not_bisimilar])
    products = 0
    bisimulation_counts = 0
    for fixture in fixtures:
        canonical = None
        for machine in (fixture, permute_nfa(fixture)):
            for streaming, bisimulation in OPTIMIZATION_MODES:
                command = [executable, "--automata"] + optimization_flags(streaming, bisimulation)
                run = subprocess.run(command, input=encode_nfa(machine),
                                     capture_output=True, text=True, check=True, timeout=60)
                actual = read_dfa(run.stdout)
                products += nfa_dfa_equivalent(machine, actual)
                if canonical is None:
                    canonical = actual
                else:
                    require(actual == canonical,
                            "minimized DFA depends on state numbering or an optimization")
                if bisimulation and "expected_bisim_states" in fixture:
                    payload = json.loads(run.stdout)
                    require(payload["bisim_before"] == 7 and
                            payload["bisim_after"] == fixture["expected_bisim_states"],
                            ("incorrect strong-bisimulation quotient", payload,
                             fixture["expected_bisim_states"]))
                    bisimulation_counts += 1

    plus = {"start": 0, "states": [
        {"final": False, "edges": [[1, 1]]},
        {"final": True, "edges": [[1, 1]]},
    ]}
    models = []
    for controls in (2, 3):
        tiles = [(1, 10, q, (q + 1) % controls) for q in range(controls)]
        models.append((plus, controls, tiles, controls))
    models.append((plus, 2, [(1, 10, 0, 1)], None))
    models.append((plus, 2, [(1, 10, 0, 1), (1, 11, 1, 0), (1, 12, 0, 0)], None))
    models.append((plus, 2, [(1, 10, 0, 0), (1, 10, 1, 1)], None))
    models.append((plus, 2, [(1, 10, q, r) for q in range(2) for r in range(2)]
                            + [(1, 10, 0, 1)], None))
    typed = {"start": 0, "states": [
        {"final": False, "edges": [[1, 1]]},
        {"final": False, "edges": [[2, 2]]},
        {"final": True, "edges": [[1, 1]]},
    ]}
    models.append((typed, 2, [(1, 10, 0, 1), (1, 10, 1, 0),
                              (2, 20, 0, 0), (2, 20, 1, 1)], None))
    for _ in range(12):
        size = rng.randrange(2, 5)
        states = [{"final": bool(rng.randrange(2)),
                   "edges": [[symbol, rng.randrange(size)] for symbol in range(3)
                             if rng.randrange(3)]} for _ in range(size)]
        controls = rng.randrange(1, 4)
        tiles = [(a, out, q, r) for a in range(3) for out in range(3)
                 for q in range(controls) for r in range(controls)
                 if rng.randrange(7) == 0]
        models.append(({"start": 0, "states": states}, controls, tiles, None))
    for machine, controls, tiles, divisor in models:
        expected = explicit_cyclic_product(machine, controls, tiles)
        canonical = None
        for streaming, bisimulation in OPTIMIZATION_MODES:
            command = [executable, "--model"] + optimization_flags(streaming, bisimulation)
            run = subprocess.run(command, input=encode_model(machine, controls, tiles),
                                 capture_output=True, text=True, check=True, timeout=60)
            actual = read_dfa(run.stdout)
            products += nfa_dfa_equivalent(expected, actual)
            if canonical is None:
                canonical = actual
            else:
                require(actual == canonical, "an optimization changes the canonical image language")
            if divisor is not None:
                for length in range(10):
                    require(dfa_accepts(actual, (10,) * length) ==
                            (length > 0 and length % divisor == 0),
                            "cyclic coefficient closure was imposed at a unit boundary")
    return {"status": "PASS", "nfa_fixtures": len(fixtures),
            "optimization_modes": len(OPTIMIZATION_MODES),
            "nfa_queries_including_renumbering": 2 * len(OPTIMIZATION_MODES) * len(fixtures),
            "cyclic_models": len(models), "cyclic_model_queries": len(OPTIMIZATION_MODES) * len(models),
            "optimization_canonical_comparisons": (len(OPTIMIZATION_MODES) - 1) * len(models),
            "strong_bisimulation_quotient_count_checks": bisimulation_counts,
            "exact_product_pairs": products,
            "intermediate_accepting_boundary_controls": [2, 3]}


def whole_integer_step(base, word):
    """Independent fixed-length positional-value evaluation of A120 nextB."""
    length = len(word)
    modulus = base ** length
    value = sum(coefficient * base ** j for j, coefficient in enumerate(word))
    e = value // modulus
    reverse = sum(coefficient * base ** (length - 1 - j)
                  for j, coefficient in enumerate(word)) + 1 - e
    g = reverse // modulus
    low = tuple((value // base ** j) % base for j in range(length))
    high = tuple((reverse // base ** (length - 1 - j)) % base for j in range(length))
    if g:
        low += ((base - 1) * (1 - e),)
        high = (1,) + high
    return tuple(x + y for x, y in zip(low, high)), e, g


@functools.lru_cache(maxsize=None)
def fixed_word_graph(base, width):
    graph = {}
    for head in range(1, 2 * base - 1):
        for tail in itertools.product(range(2 * base - 1), repeat=width - 1):
            word = (head,) + tail
            raw, e, g = whole_integer_step(base, word)
            if g and raw[-1] != base - 1:
                graph[word] = None
            else:
                graph[word] = (raw[:-1] if g else raw, e, g)
    return graph


def whole_word_return(base, width, e, g):
    if width == 0:
        return False
    graph = fixed_word_graph(base, width)
    for initial in graph:
        current = initial
        for carry, overflow in zip(e, g):
            edge = graph[current]
            if edge is None or edge[1:] != (carry, overflow):
                break
            current = edge[0]
        else:
            if current == initial:
                return True
    return False


def initial_tuple(g):
    return (0, sum(bit << t for t, bit in enumerate(g)), tuple(g))


def terminal_tuple(base, e, g):
    return (sum(bit << t for t, bit in enumerate(e)),
            sum((1 - bit) << t for t, bit in enumerate(e)),
            tuple((base - 1) * carry if overflow else 0 for carry, overflow in zip(e, g)))


def temporal_successors(base, g, state, first):
    """Unblocked full-time coefficient trajectories; no regular operations."""
    low, high, lag = state
    result = set()
    period = len(g)
    for initial in range(1 if first else 0, 2 * base - 1):
        stack = [(0, initial, 0, 0, ())]
        while stack:
            t, coefficient, target_low, target_high, target_lag = stack.pop()
            if first and coefficient == 0:
                continue
            for inward in (0, 1):
                reverse_total = coefficient + inward
                if reverse_total // base != ((high >> t) & 1):
                    continue
                low_total = coefficient + ((low >> t) & 1)
                digit = reverse_total % base
                following = low_total % base + (lag[t] if g[t] else digit)
                next_low = target_low | ((low_total // base) << t)
                next_high = target_high | (inward << t)
                next_lag = target_lag + (digit if g[t] else 0,)
                if t + 1 == period:
                    if following == initial:
                        result.add((next_low, next_high, next_lag))
                else:
                    stack.append((t + 1, following, next_low, next_high, next_lag))
    return result


def finite_layers(base, e, g, depth):
    frontier = {initial_tuple(g)}
    answer = []
    terminal = terminal_tuple(base, e, g)
    for width in range(depth + 1):
        accepted = terminal in frontier if width else False
        require(accepted == whole_word_return(base, width, e, g),
                ("tuple/whole-word acceptance mismatch", base, e, g, width))
        answer.append({"count": len(frontier), "accepted": accepted})
        if width < depth:
            frontier = {target for source in frontier
                        for target in temporal_successors(base, g, source, width == 0)}
    return answer


def check_layers(executable):
    cases = [(2, "10", "10", 3, None), (4, "100", "100", 3, None),
             (16, "10000", "10000", 2, None), (3, "10", "10", 3, None),
             (4, "100", "100", 3, 2)]
    rows = []
    comparisons = 0
    for base, carry, overflow, maximum_depth, fixed_k in cases:
        expected = {}
        for k in range(1, 4):
            if fixed_k is None or fixed_k == k:
                expected[k] = finite_layers(base, tuple(map(int, carry * k)),
                                            tuple(map(int, overflow * k)), maximum_depth)
        command = [executable, str(base), carry, overflow,
                   "--layers", str(maximum_depth), "--ignore-target", "--dump-dfa", "--seconds", "30",
                   "--memory-mib", "1024", "--nfa-cap", "100000", "--dfa-cap", "100000",
                   "--edge-cap", "1000000", "--ops-cap", "10000000"]
        if fixed_k is not None:
            command += ["--finite-k", str(fixed_k)]
        canonical = None
        for streaming, bisimulation in OPTIMIZATION_MODES:
            run = subprocess.run(command + optimization_flags(streaming, bisimulation),
                                 capture_output=True, text=True, timeout=40)
            require(run.returncode in (0, 2), ("layer command failed", run.stderr))
            records = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
            result = next(row for row in records if row.get("event") == "result")
            require(result["status"] in ("DIAGNOSTIC_ONLY", "DEPTH_CAP_UNDECIDED"), result)
            layers = [row for row in records if row.get("event") == "layer"]
            require([row["depth"] for row in layers] == list(range(maximum_depth + 1)),
                    ("missing diagnostic layer", records))
            if canonical is None:
                canonical = [row["dfa"] for row in layers]
            else:
                require([row["dfa"] for row in layers] == canonical,
                        "an optimization changes a canonical spatial-layer language")
            for row in layers:
                depth = row["depth"]
                want = [expected[k][depth]["count"] if k in expected else 0 for k in range(1, 4)]
                require(list(map(int, row["k_counts"])) == want,
                        ("regular/tuple layer count mismatch", base, carry, overflow, fixed_k, row, want))
                hit = row["target_hit_k"]
                accepted = [k for k in expected if expected[k][depth]["accepted"]]
                if hit is None:
                    require(not accepted, ("missed terminal word", row, accepted))
                elif hit <= 3:
                    require(hit in accepted, ("spurious terminal word", row, accepted))
                comparisons += 3
        rows.append({"base": base, "e": carry, "g": overflow, "finite_k": fixed_k,
                     "depth": maximum_depth, "counts": [row["k_counts"] for row in layers],
                     "target_hit_k": [row["target_hit_k"] for row in layers]})
    return {"status": "PASS", "cases": len(cases),
            "optimization_modes": len(OPTIMIZATION_MODES),
            "engine_queries": len(OPTIMIZATION_MODES) * len(cases),
            "optimization_canonical_layer_comparisons":
                (len(OPTIMIZATION_MODES) - 1) * sum(depth + 1 for _, _, _, depth, _ in cases),
            "finite_k_layer_counts": comparisons,
            "whole_integer_acceptance_checks": sum((depth + 1) * (3 if k is None else 1)
                                                    for _, _, _, depth, k in cases),
            "results": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    tiles = subparsers.add_parser("tiles")
    tiles.add_argument("--block-tool", required=True)
    regular = subparsers.add_parser("regular")
    regular.add_argument("--regular-tool", required=True)
    layers = subparsers.add_parser("layers")
    layers.add_argument("--regular-tool", required=True)
    args = parser.parse_args()
    started = time.monotonic()
    if args.command == "tiles":
        result = check_tiles(args.block_tool)
    elif args.command == "regular":
        result = check_regular(args.regular_tool)
    else:
        result = check_layers(args.regular_tool)
    result["elapsed_seconds"] = round(time.monotonic() - started, 6)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
