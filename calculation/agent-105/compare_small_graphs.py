#!/usr/bin/env python3
"""Independent Cartesian-carry BFS versus the compiled exterior solver.

Every carry vector is enumerated before the temporal equations are evaluated.
This deliberately differs from the C++ temporal depth-first enumeration.
The control-only C++ build adds a read-only node getter and renames main;
the solver's original file is not changed.  All reachable states, accepted
streams, shortest acceptance depths, and transition multiplicities are checked.
"""
from __future__ import annotations

import argparse
from collections import deque
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import subprocess
import tempfile
import time

from wholeword_controls import require, transition


def cartesian_graph(base, word, cap=10000, seconds=5):
    g = tuple(map(int, word))
    p = len(g)
    positions = [i for i, bit in enumerate(g) if bit]
    initial = ((0,) * p, g, tuple(g))
    root = (True, initial)
    depths = {root: 0}
    queue = deque([root])
    choices = tuple(product((0, 1), repeat=p))
    accepted = {}
    emitted = 0
    deadline = time.monotonic() + seconds
    while queue:
        require(time.monotonic() <= deadline, 'Python control time cap reached')
        first, state = queue.popleft()
        left, right, previous = state
        depth = depths[first, state]
        if (all(a + b == 1 for a, b in zip(left, right)) and
                all(previous[t] == (base - 1) * left[t] for t in positions)):
            entry_word = ''.join(map(str, left))
            accepted.setdefault(entry_word, depth)
        for inward in choices:
            for initial_coefficient in range(1 if first else 0, 2 * base - 1):
                column = []
                x = initial_coefficient
                for t in range(p):
                    if first and x == 0:
                        break
                    if (x + inward[t]) // base != right[t]:
                        break
                    column.append(x)
                    partner = previous[t] if g[t] else (x + inward[t]) % base
                    x = (x + left[t]) % base + partner
                else:
                    if x != initial_coefficient:
                        continue
                    emitted += 1
                    successor = (
                        tuple((column[t] + left[t]) // base for t in range(p)),
                        inward,
                        tuple((column[t] + inward[t]) % base if g[t] else 0
                              for t in range(p)),
                    )
                    key = False, successor
                    if key not in depths:
                        require(len(depths) < cap, 'Python control state cap reached')
                        depths[key] = depth + 1
                        queue.append(key)
    return depths, accepted, emitted


def necklaces(period):
    for bits in product('01', repeat=period):
        word = ''.join(bits)
        if word == min(word[j:] + word[:j] for j in range(period)):
            yield word


def build_audit_solver(source, directory, compiler):
    original = source.read_text()
    marker = 'public:\n    Search('
    require(original.count(marker) == 1, 'unexpected C++ class layout')
    getter = '''public:
    std::vector<State> states_for_audit() const {
        std::vector<State> result;
        for (const Node& node : nodes) result.push_back(node.state);
        return result;
    }
    Search('''
    copied = original.replace(marker, getter)
    signature = 'int main(int argc, char** argv) {'
    require(copied.count(signature) == 1, 'unexpected C++ main signature')
    copied = copied.replace(signature, 'int original_program_main(int argc, char** argv) {')
    header = directory / 'exterior_inspection.hpp'
    header.write_text(copied)
    harness = directory / 'inspect.cpp'
    harness.write_text(r'''#include "exterior_inspection.hpp"
int main(int argc, char** argv) {
    if (argc != 3) return 2;
    const unsigned b = static_cast<unsigned>(std::stoul(argv[1]));
    const std::string word = argv[2];
    Search search(word, b, 10000, 5, true, true);
    Result result = search.run();
    print(b, word, result);
    const auto states = search.states_for_audit();
    std::cout << "[";
    for (size_t j = 0; j < states.size(); ++j) {
        if (j) std::cout << ",";
        std::cout << "[";
        for (unsigned field = 0; field < 3; ++field) {
            if (field) std::cout << ",";
            const auto& a = field == 0 ? states[j].left :
                            field == 1 ? states[j].right : states[j].previous;
            std::cout << "[";
            for (unsigned t = 0; t < word.size(); ++t)
                std::cout << (t ? "," : "") << unsigned(a[t]);
            for (unsigned t = word.size(); t < MAX_PERIOD; ++t)
                if (a[t]) throw std::runtime_error("nonzero inactive state coordinate");
            std::cout << "]";
        }
        std::cout << "]";
    }
    std::cout << "]\n";
}
''')
    binary = directory / 'inspect'
    subprocess.run([compiler, '-O2', '-std=c++17', str(harness), '-o', str(binary)],
                   check=True, capture_output=True, text=True, timeout=60)
    return binary, hashlib.sha256(original.encode()).hexdigest()


def check_witness(base, word, record):
    blocks = [tuple(b) for b in record['B']]
    require(len(blocks) == len(word), 'wrong witness period')
    for t, block in enumerate(blocks):
        target, trim, entry, overflow, _ = transition(base, block)
        require(target == blocks[(t + 1) % len(blocks)], 'integer B return mismatch')
        require(trim == record['u'][t], 'integer trim mismatch')
        require(str(entry) == record['e'][t], 'integer entry carry mismatch')
        require(str(overflow) == word[t], 'integer overflow mismatch')


def compare(binary):
    cases = states = transitions = acceptances = 0
    largest = None
    for base in range(2, 6):
        for period in range(1, 5):
            for word in necklaces(period):
                depths, expected, emitted = cartesian_graph(base, word)
                process = subprocess.run([str(binary), str(base), word],
                                         capture_output=True, text=True,
                                         timeout=10, check=True)
                lines = process.stdout.splitlines()
                require(len(lines) == 2, 'unexpected inspection output')
                result, records = map(json.loads, lines)
                require(result['complete'], 'C++ control graph was not exhausted')
                actual_states = {(i == 0, tuple(tuple(a) for a in state))
                                 for i, state in enumerate(records)}
                require(actual_states == set(depths),
                        f'FULL STATE SET mismatch: base={base} g={word}')
                actual = {a['e']: a['depth'] for a in result['accepted']}
                require(actual == expected, f'accepted-stream mismatch: base={base} g={word}')
                require(result['states'] == len(depths) == len(records), 'state count mismatch')
                require(result['generated_transitions'] == emitted, 'transition multiplicity mismatch')
                require(result['max_depth'] == max(depths.values()), 'graph depth mismatch')
                for accepted in result['accepted']:
                    check_witness(base, word, accepted)
                cases += 1
                states += len(depths)
                transitions += emitted
                acceptances += len(actual)
                row = len(depths), base, word
                if largest is None or row > largest:
                    largest = row
    return {'status': 'PASS', 'complete_graphs': cases,
            'summed_reachable_states': states, 'column_transitions': transitions,
            'accepted_streams': acceptances, 'largest_graph': largest,
            'full_state_set_mismatches': 0, 'all_controls_complete': True,
            'scope': 'bases 2..5, periods 1..4, every overflow necklace'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solver', type=Path,
                        default=Path(__file__).with_name('exterior_tuple.cpp'))
    parser.add_argument('--compiler', default='g++')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='p196-small-graphs-') as name:
        binary, digest = build_audit_solver(args.solver, Path(name), args.compiler)
        result = compare(binary)
        result['solver_source_sha256'] = digest
        print(json.dumps(result))


if __name__ == '__main__':
    main()
