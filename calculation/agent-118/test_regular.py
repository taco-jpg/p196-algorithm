#!/usr/bin/env python3
"""Independent exact finite-automata tests for typed cyclic segment images.

These tiny models do not import the production automaton or local center rules.
Their epsilon-free NFA image is checked against direct enumeration of choices
over complete input words.  Global language identities use exact subset-product
reachability, never a bound on word length or a comparison of state numbers.

Letters are (phase, local_value), where phase cycles 0, 1, 2.  A local choice
(y_s, c_s) produces the letter (phase_s, (y_s, c_{s+1})), with the final c equal
to the first.  Only positive multiples of three segments belong to the scope.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import itertools
from pathlib import Path
import random
import re
import subprocess


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


class NFA:
    """A small epsilon-free NFA; missing edges mean rejection."""

    def __init__(self, initials=(), finals=()):
        self.initials = frozenset(initials)
        self.finals = frozenset(finals)
        self.edges = defaultdict(lambda: defaultdict(set))

    def add(self, source, letter, target):
        self.edges[source][letter].add(target)

    def states(self):
        return (set(self.initials) | set(self.finals) | set(self.edges)
                | {target for edges in self.edges.values()
                   for targets in edges.values() for target in targets})

    def alphabet(self):
        return {letter for edges in self.edges.values() for letter in edges}

    def step(self, states, letter):
        return frozenset(target for source in states
                         for target in self.edges.get(source, {}).get(letter, ()))

    def accepts(self, word):
        states = self.initials
        for letter in word:
            states = self.step(states, letter)
        return bool(states & self.finals)

    def witness(self):
        """An accepted word, or None iff exact graph reachability finds none."""
        queue = deque(self.initials)
        paths = {state: () for state in self.initials}
        while queue:
            source = queue.popleft()
            if source in self.finals:
                return paths[source]
            for letter, targets in self.edges.get(source, {}).items():
                for target in targets:
                    if target not in paths:
                        paths[target] = paths[source] + (letter,)
                        queue.append(target)
        return None

    def words(self, length, cap=100000):
        """Enumerate an exact finite slice; the cap raises rather than truncates."""
        layer = {(): self.initials}
        for _ in range(length):
            next_layer = {}
            for prefix, states in layer.items():
                letters = {letter for q in states for letter in self.edges.get(q, {})}
                for letter in letters:
                    next_layer[prefix + (letter,)] = self.step(states, letter)
                    require(len(next_layer) <= cap, "finite-word oracle cap exceeded")
            layer = next_layer
        return {word for word, states in layer.items() if states & self.finals}


def finite_language(words):
    """Trie construction, including epsilon precisely when it is in words."""
    words = set(words)
    result = NFA({()}, words)
    for word in words:
        for length, letter in enumerate(word):
            result.add(word[:length], letter, word[:length + 1])
    return result


def positive_blocks(blocks):
    """Recognize (block_1 | ... | block_r)+ without accepting epsilon."""
    blocks = tuple(set(blocks))
    require(blocks and all(blocks), "blocks must be nonempty")
    root, hub = ("root",), ("hub",)
    result = NFA({root}, {hub})
    for block_number, block in enumerate(blocks):
        for index, letter in enumerate(block):
            sources = (root, hub) if index == 0 else ((block_number, index),)
            target = hub if index + 1 == len(block) else (block_number, index + 1)
            for source in sources:
                result.add(source, letter, target)
    return result


def union(left, right):
    result = NFA({(0, q) for q in left.initials} | {(1, q) for q in right.initials},
                 {(0, q) for q in left.finals} | {(1, q) for q in right.finals})
    for tag, automaton in enumerate((left, right)):
        for source, edges in automaton.edges.items():
            for letter, targets in edges.items():
                for target in targets:
                    result.add((tag, source), letter, (tag, target))
    return result


def intersection(left, right):
    initials = set(itertools.product(left.initials, right.initials))
    result = NFA(initials)
    queue, seen, finals = deque(initials), set(initials), set()
    while queue:
        a, b = queue.popleft()
        if a in left.finals and b in right.finals:
            finals.add((a, b))
        for letter in left.edges.get(a, {}).keys() & right.edges.get(b, {}).keys():
            for target in itertools.product(left.edges[a][letter], right.edges[b][letter]):
                result.add((a, b), letter, target)
                if target not in seen:
                    seen.add(target)
                    queue.append(target)
    result.finals = frozenset(finals)
    return result


def difference_witness(left, right, equivalence=True, cap=200000):
    """Exact subset-product test; None means equality (or inclusion if false)."""
    initial = (left.initials, right.initials)
    queue, paths = deque([initial]), {initial: ()}
    letters = left.alphabet() | right.alphabet()
    while queue:
        a, b = queue.popleft()
        accepts_a, accepts_b = bool(a & left.finals), bool(b & right.finals)
        differs = accepts_a != accepts_b if equivalence else accepts_a and not accepts_b
        if differs:
            return paths[(a, b)]
        for letter in letters:
            target = (left.step(a, letter), right.step(b, letter))
            if target not in paths:
                require(len(paths) < cap, "exact language comparison cap exceeded")
                paths[target] = paths[(a, b)] + (letter,)
                queue.append(target)
    return None


def equivalent(left, right):
    return difference_witness(left, right) is None


def cyclic_image(source, tables, close_cycle=True, positive_length=True):
    """Exact image as a finite NFA for ALL supported input word lengths.

    Disabling close_cycle or positive_length is deliberately unsound and is
    used only to reproduce the corresponding regression counterexample.
    """
    require(len(tables) == 3, "oracle requires precisely three segment types")
    domains = [{c for choices in table.values() for _, c in choices} for table in tables]
    initials = {(q, 0, c, c, False) for q in source.initials for c in domains[0]}
    result = NFA(initials)
    queue, seen, finals = deque(initials), set(initials), set()
    while queue:
        state = queue.popleft()
        q, phase, required, first, nonempty = state
        if (q in source.finals and phase == 0 and (nonempty or not positive_length)
                and (not close_cycle or required == first)):
            finals.add(state)
        for (label_phase, old), targets in source.edges.get(q, {}).items():
            if label_phase != phase:
                continue
            next_phase = (phase + 1) % 3
            for y, c in tables[phase].get(old, ()):
                if c != required:
                    continue
                for next_c in domains[next_phase]:
                    label = (phase, (y, next_c))
                    for target_q in targets:
                        target = (target_q, next_phase, next_c, first, True)
                        result.add(state, label, target)
                        if target not in seen:
                            seen.add(target)
                            queue.append(target)
        require(len(seen) <= 100000, "toy image state cap exceeded")
    result.finals = frozenset(finals)
    return result


def explicit_image(words, tables):
    """Definition-level oracle: enumerate choices on each complete input word."""
    result = set()
    for word in words:
        if not word or len(word) % 3 or any(phase != s % 3 for s, (phase, _) in enumerate(word)):
            continue
        choices = [tables[phase].get(old, ()) for phase, old in word]
        for selected in itertools.product(*choices):
            result.add(tuple((s % 3, (y, selected[(s + 1) % len(word)][1]))
                             for s, (y, _) in enumerate(selected)))
    return result


def compare_slices(source, tables, lengths, totals):
    output = cyclic_image(source, tables)
    require(not output.accepts(()), "cyclic image admitted the empty word")
    for length in lengths:
        inputs = source.words(length)
        expected = explicit_image(inputs, tables)
        actual = output.words(length)
        require(actual == expected,
                f"cyclic image mismatch at length {length}: missing={expected - actual}, extra={actual - expected}")
        totals["finite_slices"] += 1
        totals["input_words"] += len(inputs)
        totals["output_words"] += len(expected)
    totals["models"] += 1
    totals["image_states"] += len(output.states())
    return output


def algebra_checks(totals):
    a = tuple((s, 0) for s in range(3))
    b = tuple((s, 1) for s in range(3))
    plus_a, plus_b = positive_blocks([a]), positive_blocks([b])
    both, either = positive_blocks([a, b]), union(plus_a, plus_b)
    require(equivalent(union(plus_a, plus_a), plus_a), "union lost idempotence")
    require(equivalent(union(plus_a, plus_b), union(plus_b, plus_a)), "union lost commutativity")
    require(equivalent(intersection(plus_a, plus_a), plus_a), "intersection lost idempotence")
    require(intersection(plus_a, plus_b).witness() is None, "disjoint languages intersect")
    require(equivalent(intersection(either, both), either), "intersection lost input paths")
    require(difference_witness(either, both, equivalence=False) is None, "valid inclusion rejected")
    require(difference_witness(both, either, equivalence=False) is not None, "strict inclusion missed")
    require(equivalent(union(intersection(both, plus_a), intersection(both, plus_b)), either),
            "intersection/union distribution failed")
    totals["global_algebra_identities"] += 8

    # Same numeric root is no evidence of equality; duplicate initial branches
    # or renamed states are no evidence of inequality.
    first, second = NFA({0}, {1}), NFA({0}, {1})
    first.add(0, (0, "a"), 1)
    second.add(0, (0, "b"), 1)
    require(first.initials == second.initials and not equivalent(first, second),
            "same-root counterexample missing")
    require(equivalent(union(first, first), first), "NFA equivalent duplicate paths differ")
    require(equivalent(finite_language({()}), NFA({77}, {77})), "epsilon equality failed")
    require(difference_witness(NFA(), finite_language({()})) == (), "epsilon difference omitted")
    totals["representation_controls"] += 4

    # Agreeing on a finite prefix of word lengths does not prove equality.
    finite = finite_language({a})
    require(all(finite.words(n) == plus_a.words(n) for n in range(4)), "prefix fixture changed")
    witness = difference_witness(finite, plus_a)
    require(witness is not None and len(witness) == 6, "unbounded comparison missed length-six difference")
    totals["bounded_check_counterexamples"] += 1
    try:
        difference_witness(finite, plus_a, cap=1)
    except RuntimeError as error:
        require("cap exceeded" in str(error), "wrong exact-comparison failure")
    else:
        raise RuntimeError("comparison cap silently certified equality")
    totals["oracle_cap_guards"] += 1


def targeted_models(totals):
    zero = tuple((s, 0) for s in range(3))
    one = tuple((s, 1) for s in range(3))
    identity = [{0: [(0, 0)], 1: [(1, 0)]} for _ in range(3)]
    correlated = positive_blocks([zero, one])
    actual = compare_slices(correlated, identity, (0, 1, 2, 3, 4, 6), totals)
    mixed = ((0, (0, 0)), (1, (1, 0)), (2, (0, 0)))
    relaxed = positive_blocks(itertools.product(*[[(s, 0), (s, 1)] for s in range(3)]))
    require(not actual.accepts(mixed) and cyclic_image(relaxed, identity).accepts(mixed),
            "coordinate-marginal relaxation counterexample missing")
    totals["correlation_counterexamples"] += 1

    # Relational image distributes union for whole infinite languages.  This
    # checks branch merging without replacing correlations by marginals.
    diagonals = [positive_blocks([zero]), positive_blocks([one])]
    joined_image = cyclic_image(union(*diagonals), identity)
    separate_images = union(*(cyclic_image(part, identity) for part in diagonals))
    require(equivalent(joined_image, separate_images), "image/union identity failed")
    totals["global_image_union_identities"] += 1

    tables = [{0: [(5, 0), (8, 1)]}, {0: [(6, 0)]}, {0: [(7, 0)]}]
    source = positive_blocks([zero])
    actual = compare_slices(source, tables, (0, 3, 6, 9), totals)
    wrong = cyclic_image(source, tables, close_cycle=False)
    counterexample = ((0, (5, 0)), (1, (6, 0)), (2, (7, 1)))
    require(wrong.accepts(counterexample) and not actual.accepts(counterexample),
            "cyclic closing counterexample missing")
    require(len(actual.words(3)) == 2 and len(wrong.words(3)) == 4,
            "unexpected cyclic-closing fixture sizes")
    totals["closing_counterexamples"] += 1

    # An accepting old input state can be crossed before the complete word
    # ends.  At the middle ABC boundary the pending guess is 1 whereas c_0=0;
    # requiring closure there would incorrectly eliminate this length-six word.
    six = counterexample + ((0, (8, 0)), (1, (6, 0)), (2, (7, 0)))
    require(actual.accepts(six) and not actual.accepts(six[:3]),
            "intermediate accepting state incorrectly forces cyclic closure")
    require(not positive_blocks(actual.words(3)).accepts(six),
            "length-six fixture no longer distinguishes per-block closure")
    totals["premature_closing_counterexamples"] += 1

    # Correct input-language acceptance is independent of cyclic carry closure.
    even_units = NFA({0}, {6})
    for q in range(6):
        even_units.add(q, (q % 3, 0), q + 1)
    even_units.add(6, (0, 0), 1)
    wrong_endpoints = NFA({0, 3, 6}, {0, 3, 6})
    for q, edges in even_units.edges.items():
        for label, targets in edges.items():
            for target in targets:
                wrong_endpoints.add(q, label, target)
    actual = compare_slices(even_units, identity, (0, 3, 6, 9, 12), totals)
    three = tuple((s, (0, 0)) for s in range(3))
    wrong = cyclic_image(wrong_endpoints, identity)
    require(not actual.accepts(three) and wrong.accepts(three), "start-any/end-any control missing")
    require(wrong_endpoints.accepts(()) and not wrong.accepts(()), "positive-length scope failed")
    wrong_empty = cyclic_image(wrong_endpoints, identity, positive_length=False)
    require(wrong_empty.accepts(()), "omitted-positive-length counterexample missing")
    totals["endpoint_counterexamples"] += 1
    totals["empty_word_controls"] += 2
    totals["empty_word_counterexamples"] += 1

    # Valid empty, dead, duplicated, inactive-sentinel, and malformed-phase inputs.
    for source, tables in [
        (NFA(), identity),
        (positive_blocks([zero]), [{0: []}, {0: [(1, 0)]}, {0: [(2, 0)]}]),
        (positive_blocks([zero]), [{0: [(s, -1), (s, -1)]} for s in range(3)]),
        (finite_language({(), ((1, 0), (2, 0), (0, 0)), ((0, 0),), zero}), identity),
    ]:
        compare_slices(source, tables, (0, 1, 3, 6), totals)


def toy_period_and_tails(totals):
    zero = tuple((s, (0, 0)) for s in range(3))
    one = tuple((s, (1, 0)) for s in range(3))
    start = positive_blocks([zero])
    fixed = [{(0, 0): [(0, 0)]} for _ in range(3)]
    require(equivalent(cyclic_image(start, fixed), start), "toy global fixed point failed")
    # Both whole-language tail checks are necessary even at a fixed point.
    tails = [[{(0, 0): [(0, 0)]} for _ in range(3)] for _ in range(2)]
    tails[0][0] = {}
    tails[1][2] = {}
    for tail in tails:
        require(cyclic_image(start, tail).witness() is None, "toy tail unexpectedly nonempty")
    totals["global_fixedpoints"] += 1
    totals["empty_tail_languages"] += 2

    flip = [{(0, 0): [(1, 0)], (1, 0): [(0, 0)]} for _ in range(3)]
    first = cyclic_image(start, flip)
    second = cyclic_image(first, flip)
    require(equivalent(first, positive_blocks([one])), "period-two first layer changed")
    require(equivalent(second, start) and not equivalent(first, start), "exact period two missed")
    only_one = [{(1, 0): [(1, 0)]}, flip[1], flip[2]]
    require(cyclic_image(start, only_one).witness() is None, "tail should reject class zero")
    require(cyclic_image(first, only_one).witness() is not None, "tail should accept class one")
    totals["global_period_two"] += 1
    totals["omitted_period_class_counterexamples"] += 1

    # The first-layer relation can differ from all later generic layers.  An
    # empty tail at the eventual fixed point says nothing about the initial one.
    initial_only_tail = [{(0, 0): [(0, 0)]} for _ in range(3)]
    eventual_fixed = [{(1, 0): [(1, 0)]} for _ in range(3)]
    require(equivalent(cyclic_image(first, eventual_fixed), first), "eventual fixed point changed")
    require(cyclic_image(first, initial_only_tail).witness() is None,
            "eventual initial-only tail should be empty")
    require(cyclic_image(start, initial_only_tail).witness() is not None,
            "transient tail control lost its positive witness")
    totals["omitted_transient_counterexamples"] += 1


def random_models(totals, count=24):
    rng = random.Random(118369)
    for _ in range(count):
        source = NFA({("root",)}, {(0, 0), (0, 1)})
        for phase in range(3):
            for memory in range(2):
                for old in range(2):
                    for target in range(2):
                        if rng.randrange(4) == 0:
                            source.add((phase, memory), (phase, old), ((phase + 1) % 3, target))
            # Keep a positive backbone while retaining random alternative
            # paths, branch merging, and nondeterministic memory transitions.
            source.add((phase, 0), (phase, 0), ((phase + 1) % 3, 0))
        # The initial copy is nonaccepting, enforcing positive length before a
        # visit to a phase-zero accepting state of this nondeterministic source.
        for letter, targets in source.edges.get((0, 0), {}).items():
            for target in targets:
                source.add(("root",), letter, target)
        tables = [{old: [(rng.randrange(2), rng.choice((-1, 0, 1)))
                         for _ in range(rng.randrange(1 if old == 0 else 0, 3))]
                   for old in range(2)}
                  for _ in range(3)]
        image = compare_slices(source, tables, (3, 6), totals)
        require(image.witness() is not None, "positive random backbone disappeared")
        totals["positive_random_models"] += 1


def abstract_checks():
    totals = Counter()
    algebra_checks(totals)
    targeted_models(totals)
    toy_period_and_tails(totals)
    random_models(totals)
    return dict(sorted(totals.items()))


def fields(line):
    return dict(re.findall(r"(\w+)=([^ ]+)", line))


def production_checks(binary):
    """Full target run, complete P24 comparisons, P48 counts, and cap guards."""
    totals = Counter()
    common = [str(binary), "--states", "200000", "--edges", "3000000",
              "--ops", "100000000"]
    command = [*common, "--layers", "7", "--compare"]
    result = subprocess.run(command, text=True, capture_output=True, timeout=30)
    require(result.returncode == 0 and "UNDECIDED" not in result.stdout + result.stderr,
            f"production did not complete: {command}\n{result.stdout}\n{result.stderr}")
    layers = [fields(line) for line in result.stdout.splitlines() if line.startswith("REG_LAYER ")]
    compares = [fields(line) for line in result.stdout.splitlines() if line.startswith("REG_COMPARE ")]
    tails = [fields(line) for line in result.stdout.splitlines() if line.startswith("REG_TAIL ")]
    completed = [fields(line) for line in result.stdout.splitlines() if line.startswith("REG_DONE ")]
    fixed = [fields(line) for line in result.stdout.splitlines() if line.startswith("REG_FIXED ")]
    expected3 = [1, 1000, 30592, 93376, 116128, 140104, 152584, 152584]
    expected6 = [1, 1000000, 935560192, 8574299136, 8868958208,
                 9157137472, 9312887872, 9312887872]
    require(len(layers) == 8 and len(compares) == 35 and len(tails) == 14,
            "incomplete generic or terminal frontier controls")
    require(len(fixed) == 1 and fixed[0] == {"fixed_at": "6", "method": "exact_dfa_product"},
            "missing exact unrestricted language fixed point")
    require(len(completed) == 1, "missing unique regular-language completion")
    done = completed[0]
    require(done["status"] == "none" and done["scope"] == "all_repetitions_all_widths"
            and done["fixed_at"] == "6" and done["tail_checks"] == "14"
            and done["comparisons"] == "35", "completed target scope or proof counts differ")
    for j, item in enumerate(layers):
        require(int(item["j"]) == j and int(item["counts3"]) == expected3[j],
                "P24 diagnostic count disagrees with established exact frontier")
        require(int(item["counts6"]) == expected6[j] and item["counts_exact"] == "1",
                "P48 diagnostic count disagrees with prior fixed-period MDD")
        require(int(item["comparisons"]) == j, "generic comparison counter differs")
        if j:
            require(0 < int(item["dfa"]) <= int(item["dfa_raw"]), "invalid DFA normalization count")
    for j, item in enumerate(compares[:7]):
        require(item["generic"] == "1" and int(item["j"]) == j,
                "production comparison used the wrong layer or signature")
        require(int(item["input"]) == expected3[j] and int(item["output"]) == expected3[j + 1],
                "complete-frontier comparison size differs")
        require(int(item["comparisons"]) == j + 1, "whole-frontier comparison was skipped")
    first_tail_counts = [0, 0, 0, 0, 0, 88, 0, 90, 0, 94, 0, 94, 0, 94]
    for index, tail in enumerate(tails):
        width, q = index + 1, index // 2
        require(int(tail["width"]) == width and int(tail["generic"]) == q
                and tail["empty"] == "1" and tail["last_dfa"] == "1",
                "terminal parity/transient class missing or nonempty")
        first, last = compares[7 + 2 * index:9 + 2 * index]
        require(first["generic"] == last["generic"] == "0"
                and int(first["j"]) == q and int(last["j"]) == q + 1,
                "terminal comparison used wrong signatures")
        require(int(first["input"]) == expected3[q]
                and int(first["output"]) == first_tail_counts[index]
                and last["input"] == first["output"] and last["output"] == "0",
                "complete terminal frontier differs from its P24 control")
        totals["empty_tail_languages"] += 1
        if first_tail_counts[index]:
            totals["nonempty_intermediate_tail_frontiers"] += 1
    for index, item in enumerate(compares):
        require(int(item["comparisons"]) == index + 1, "frontier comparison counter skipped a step")
        totals["exact_p24_frontier_comparisons"] += 1
        totals["p24_output_tuples_compared"] += int(item["output"])
    totals["p48_count_crosschecks"] += 7
    totals["exact_uniform_fixedpoints"] += 1

    guards = [
        (["--states", "1"], "regular_state_cap"),
        (["--edges", "1"], "regular_edge_cap"),
        (["--ops", "1"], "regular_operation_cap"),
        (["--layers", "1", "--compare", "--compare-cap", "999"],
         "regular_comparison_decode_cap"),
        (["--layers", "1"], "regular_fixedpoint_not_detected"),
    ]
    for arguments, reason in guards:
        run = subprocess.run([str(binary), *arguments], text=True, capture_output=True, timeout=30)
        require(run.returncode == 2 and "UNDECIDED " + reason in run.stdout + run.stderr,
                f"resource guard failed: {arguments}\n{run.stdout}\n{run.stderr}")
        require("REG_DONE" not in run.stdout, "resource guard emitted a complete decision")
        if reason == "regular_fixedpoint_not_detected":
            totals["incomplete_layer_limit_guards"] += 1
        else:
            totals["resource_guards"] += 1
    return dict(sorted(totals.items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, help="optional production center_regular executable")
    args = parser.parse_args()
    print("abstract_regular_oracle", abstract_checks())
    if args.binary:
        print("production_regular_checks", production_checks(args.binary.resolve()))
    print("COMPUTED CHECKS PASSED; no new Lean theorem asserted")


if __name__ == "__main__":
    main()
