#!/usr/bin/env python3
"""Independent integer-arithmetic controls for the autonomous B update.

The bounded graph enumerates complete canonical words, including the empty
word.  Absence here only concerns cycles staying within the stated width.
"""
from collections import Counter
import argparse
import importlib.util
from itertools import product
import json
from pathlib import Path
import subprocess
import sys


def require(test, message):
    if not test:
        raise ArithmeticError(message)


def value(base, word):
    return sum(x * base ** i for i, x in enumerate(word))


def fixed_digits(base, n, width):
    result = []
    for _ in range(width):
        result.append(n % base)
        n //= base
    return result, n


def transition(base, word):
    """Use integer evaluations and fixed-width digit extraction, not carries."""
    word = tuple(word)
    low, entry = fixed_digits(base, value(base, word), len(word))
    reversed_digits, overflow = fixed_digits(
        base, value(base, word[::-1]) + 1 - entry, len(word))
    require(entry in (0, 1) and overflow in (0, 1), 'non-bit exterior carry')
    right = list(reversed(reversed_digits))
    if overflow:
        low.append((base - 1) * (1 - entry))
        right.insert(0, 1)
    raw = tuple(a + b for a, b in zip(low, right))
    target = raw
    while target and target[-1] == base - 1:
        target = target[:-1]
    return target, len(raw) - len(target), entry, overflow, raw


def words(base, width):
    yield ()
    for length in range(1, width + 1):
        for word in product(range(2 * base - 1), repeat=length):
            if word[0] and word[-1] != base - 1:
                yield word


def census(base, width, mirror=None):
    graph = {}
    for word in words(base, width):
        record = transition(base, word)
        if mirror is not None:
            entry = record[2]
            center = [0] if entry else [2 * (base - 1)]
            require(mirror.hyp(base, list(word), center), 'fixture violates Hyp')
            require(tuple(mirror.nextB(base, list(word), center)) == record[4],
                    'integer B update disagrees with mirror')
            require(mirror.gam(base, list(word), center) == record[3],
                    'integer overflow disagrees with mirror')
        graph[word] = record
    visited = set()
    cycles = []
    for start in graph:
        if start in visited:
            continue
        path = []
        positions = {}
        cursor = start
        while cursor in graph and cursor not in visited and cursor not in positions:
            positions[cursor] = len(path)
            path.append(cursor)
            cursor = graph[cursor][0]
        if cursor in positions:
            cycle = tuple(path[positions[cursor]:])
            pivot = min(range(len(cycle)), key=lambda i: cycle[i:] + cycle[:i])
            cycle = cycle[pivot:] + cycle[:pivot]
            cycles.append(cycle)
        visited.update(path)
    cycles.sort(key=lambda c: (len(c), c))
    details = []
    for cycle in cycles:
        records = [graph[word] for word in cycle]
        require(sum(x[1] for x in records) == sum(x[3] for x in records),
                'exterior length telescope failed')
        details.append({'period': len(cycle), 'e': ''.join(str(x[2]) for x in records),
                        'g': ''.join(str(x[3]) for x in records),
                        'u': [x[1] for x in records],
                        'words': [list(word) for word in cycle]})
    return {'base': base, 'width_bound': width, 'canonical_sources': len(graph),
            'cycle_count': len(cycles),
            'period_counts': dict(sorted(Counter(map(len, cycles)).items())),
            'cycle_controls': details,
            'scope': 'complete-word cycles whose canonical widths stay within the bound'}


def power_two_controls():
    for exponent in range(1, 6):
        base = 2 ** exponent
        cycle = [(base,)] + [(2 ** j, 2 ** j - 1) for j in range(exponent)]
        records = [transition(base, word) for word in cycle]
        require(all(record[0] == cycle[(i + 1) % len(cycle)]
                    for i, record in enumerate(records)), 'power-two control does not close')
        g = ''.join(str(record[3]) for record in records)
        e = ''.join(str(record[2]) for record in records)
        require(e == g == '1' + '0' * exponent, 'power-two control stream mismatch')
        print(json.dumps({'positive_base': base, 'period': len(cycle),
                          'e': e, 'g': g, 'words': cycle, 'status': 'PASS'}))


def canonical(base, word):
    word = tuple(word)
    while word and word[-1] == base - 1:
        word = word[:-1]
    return word


def replay_return(base, word, accepted):
    blocks = [tuple(x) for x in accepted['B']]
    require(len(blocks) == len(word), 'returned witness period mismatch')
    for t, block in enumerate(blocks):
        require(not block or block[0] > 0, 'returned witness has zero exterior head')
        require(all(isinstance(x, int) and 0 <= x <= 2 * base - 2 for x in block),
                'returned witness coefficient is invalid')
        target, trim, entry, overflow, _ = transition(base, block)
        require(target == blocks[(t + 1) % len(blocks)], 'returned B words do not close')
        require(trim == accepted['u'][t], 'returned trim count mismatch')
        require(str(entry) == accepted['e'][t] and str(overflow) == word[t],
                'returned carry or overflow mismatch')


def call_solver(solver, base, word, complete):
    command = [str(solver), word, '--base', str(base), '--cap', '1000000',
               '--seconds', '30', '--witness']
    if complete:
        command.append('--all-accepts')
    process = subprocess.run(command, capture_output=True, text=True,
                             check=True, timeout=35)
    result = json.loads(process.stdout)
    require(result['base'] == base and result['g'] == word, 'solver returned wrong input')
    require(result['status'] == 'ACCEPT' and result['accepted'], 'positive control failed')
    if complete:
        require(result['complete'], 'complete positive control graph was capped')
    for accepted in result['accepted']:
        replay_return(base, word, accepted)
    return result


def source_solver_controls(mirror, solver):
    source_edges = returned_edges = cases = 0
    for base, certificate in mirror._lean_certs():
        require(mirror.cycleOK(base, certificate, certificate[0][0], certificate[0][1]),
                'known source certificate no longer passes the mirror')
        blocks = [canonical(base, edge[0]) for edge in certificate]
        g, e = '', ''
        for t, block in enumerate(blocks):
            target, trim, entry, overflow, _ = transition(base, block)
            require(target == blocks[(t + 1) % len(blocks)], 'source B words do not close')
            require(entry == mirror.e1(base, certificate[t][0]), 'source carry mismatch')
            require(overflow == mirror.gam(base, certificate[t][0], certificate[t][1]),
                    'source overflow mismatch')
            g += str(overflow)
            e += str(entry)
            source_edges += 1
        result = call_solver(solver, base, g, False)
        cases += 1
        returned_edges += sum(len(a['B']) for a in result['accepted'])
        print(json.dumps({'source_base': base, 'source_e': e, 'g': g,
                          'solver_e': [a['e'] for a in result['accepted']],
                          'solver_states': result['states'], 'status': 'PASS',
                          'scope': 'source overflow positive control; first accepted e may differ'}))
    require(cases == 8, 'expected exactly eight known source bases')
    print(json.dumps({'known_source_g_cases': cases, 'source_B_edges_replayed': source_edges,
                      'solver_B_edges_replayed': returned_edges, 'status': 'PASS'}))
    for label, word, expected in (
            ('decimal_p11', '11100010000', {'10100110011'}),
            ('decimal_p12', '100010001000',
             {'101010010101'[i:] + '101010010101'[:i] for i in (0, 4, 8)})):
        result = call_solver(solver, 10, word, True)
        observed = {a['e'] for a in result['accepted']}
        require(observed == expected, 'complete decimal e-stream census mismatch')
        print(json.dumps({'case': label, 'accepted_e': sorted(observed),
                          'minimum_widths': sorted(a['depth'] for a in result['accepted']),
                          'solver_states': result['states'], 'complete': True,
                          'integer_B_edges_replayed': sum(len(a['B']) for a in result['accepted']),
                          'status': 'PASS'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mirror', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'neutral_band_search.py')
    parser.add_argument('--solver', type=Path,
                        help='optional compiled exterior_tuple binary for known-source controls')
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('wholeword_mirror', args.mirror)
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    power_two_controls()
    count = 0
    for base in range(2, 7):
        result = census(base, 4, mirror)
        count += result['canonical_sources']
        print(json.dumps(result))
    print(json.dumps({'bounded_integer_transfer_checks': count, 'status': 'PASS'}))
    if args.solver:
        source_solver_controls(mirror, args.solver)
