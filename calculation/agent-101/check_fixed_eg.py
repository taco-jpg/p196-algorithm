#!/usr/bin/env python3
"""Independent complete-word oracle for the fixed-E/G exterior solvers.

Default: all 60 base-2, period-1/2, width-1..3 stream queries; 32 seeded
queries over complete base-3..5 word graphs; eight padded source fixtures;
eight charged CP-SAT source controls; and eight fail-closed guard cases.
A period-P return need not be primitive.
Use --quick for at most 12 oracle queries plus fixtures and guards.
Every check remains active under python -O. No large target search is run.
"""
import argparse
import importlib.metadata
import itertools
import json
import os
import random
import signal
import sys
import time
from collections import Counter
from functools import lru_cache, partial
from pathlib import Path

import fixed_eg_cpsat
import fixed_eg_smt


class CheckFailure(RuntimeError):
    pass


class OverallLimit(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def integer_digits(base, word, entry):
    """Positional arithmetic, without column carry equations or solver imports."""
    number = entry + sum(x * base**j for j, x in enumerate(word))
    final_carry, residue = divmod(number, base**len(word))
    digits = tuple((residue // base**j) % base for j in range(len(word)))
    return digits, final_carry


def exterior_step(base, word):
    """The deterministic width-preserving exterior step, or None on failure."""
    width = len(word)
    require(width > 0 and type(word[0]) is int and word[0] > 0
            and all(type(x) is int and 0 <= x <= 2*base-2 for x in word),
            'Oracle source lies outside the exterior domain')
    low, entry = integer_digits(base, word, 0)
    opposite, growth = integer_digits(base, word[::-1], 1-entry)
    require(entry in (0, 1) and growth in (0, 1), 'Oracle carry is not binary')
    if growth:
        left = low + ((base-1)*(1-entry),)
        right = (1,) + opposite[::-1]
    else:
        left, right = low, opposite[::-1]
    raw = tuple(a+b for a, b in zip(left, right))
    if growth and raw[-1] != base-1:
        return None
    target = raw[:-1] if growth else raw
    if (len(target) != width or not target[0]
            or any(not 0 <= x <= 2*base-2 for x in target)):
        return None
    return target, entry, growth


@lru_cache(maxsize=None)
def full_graph(base, width):
    result = {}
    for head in range(1, 2*base-1):
        for tail in itertools.product(range(2*base-1), repeat=width-1):
            word = (head,) + tail
            result[word] = exterior_step(base, word)
    return result


@lru_cache(maxsize=None)
def returning_streams(base, width, period):
    """Exhaust every starting word; record all literal P-step return streams."""
    graph = full_graph(base, width)
    result = set()
    for start in graph:
        current = start
        entries, growths = [], []
        for _ in range(period):
            edge = graph[current]
            if edge is None:
                break
            current, entry, growth = edge
            entries.append(str(entry))
            growths.append(str(growth))
        else:
            if current == start:
                result.add((''.join(entries), ''.join(growths)))
    return frozenset(result)


def bitstrings(length):
    return (''.join(bits) for bits in itertools.product('01', repeat=length))


def queries(quick):
    base_two = [(2, e, g, width) for width in range(1, 4)
                for period in (1, 2) for e in bitstrings(period)
                for g in bitstrings(period)]
    require(len(base_two) == 60, 'Wrong exhaustive base-2 query count')
    rng = random.Random(101)
    seeded, seen = [], set()
    while len(seeded) < 32:
        base, width, period = rng.randrange(3, 6), rng.randrange(1, 4), rng.randrange(1, 7)
        positives = sorted(returning_streams(base, width, period))
        if len(seeded) % 2 == 0 and positives:
            e, g = rng.choice(positives)
        else:
            e = ''.join(str(rng.randrange(2)) for _ in range(period))
            g = ''.join(str(rng.randrange(2)) for _ in range(period))
        query = (base, e, g, width)
        if query not in seen:
            seen.add(query)
            seeded.append(query)
    selected = base_two + seeded
    if quick:
        selected = [base_two[i] for i in (0, 1, 4, 7, 20, 29, 40, 54)] + seeded[:4]
    return selected


def replay_words(base, e, g, width, words):
    require(isinstance(words, list) and len(words) == len(e), 'Witness phase count is wrong')
    converted = []
    for word in words:
        require(isinstance(word, (list, tuple)) and len(word) == width,
                'Witness width is wrong')
        converted.append(tuple(word))
    for t, word in enumerate(converted):
        edge = exterior_step(base, word)
        require(edge == (converted[(t+1) % len(e)], int(e[t]), int(g[t])),
                f'Independent integer replay failed at phase {t}')
    return len(words)


def source_fixtures():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror
    certificates = mirror._lean_certs()
    require(len(certificates) == 8, 'Expected the eight source certificates')
    fixtures = []
    for base, edges in certificates:
        width = 1 + max(len(edge[0]) for edge in edges)
        words = [list(edge[0]) + [base-1]*(width-len(edge[0])) for edge in edges]
        entries, growths = [], []
        for t, word in enumerate(words):
            computed = exterior_step(base, tuple(word))
            require(computed is not None, f'Padding lost a base-{base} source edge')
            target, entry, growth = computed
            require(target == tuple(words[(t+1) % len(words)]),
                    f'Padded base-{base} source does not close')
            entries.append(str(entry))
            growths.append(str(growth))
        fixtures.append((base, ''.join(entries), ''.join(growths), width, words))
    return fixtures


def backends(include_charge=False):
    result = (('cp_sat', fixed_eg_cpsat.solve), ('z3_qfbv', fixed_eg_smt.solve))
    if include_charge:
        result += (('cp_sat_charge', partial(fixed_eg_cpsat.solve, charge=True)),)
    return result


def execute_case(query, expected, stats, undecided, fixed_words=None):
    base, e, g, width = query
    for name, solve in backends(fixed_words is not None):
        result = solve(base, e, g, width, seconds=5, memory_mb=1024,
                       fixed_words=fixed_words)
        status = result.get('status')
        stats[name][status] += 1
        require(status in ('SAT_B_ONLY', 'UNSAT_BOUNDED', 'UNDECIDED'),
                f'{name} returned an unrecognized status: {result}')
        if status == 'UNDECIDED':
            undecided.append({'backend': name, 'query': query,
                              'fixture': fixed_words is not None,
                              'reason': result.get('reason'),
                              'detail': result.get('detail')})
            continue
        require((status == 'SAT_B_ONLY') == expected,
                f'{name} contradicts complete-word oracle at {query}: {result}')
        if status == 'SAT_B_ONLY':
            words = result.get('B')
            stats['replay']['edges'] += replay_words(base, e, g, width, words)
            stats['replay']['witnesses'] += 1
            if fixed_words is not None:
                require(words == fixed_words, f'{name} ignored pinned source coefficients')


def guard_checks():
    cases = [
        ('base_below_domain', (1, '0', '0', 1), {}),
        ('zero_width', (2, '0', '0', 0), {}),
        ('nonbinary_stream', (2, '2', '0', 1), {}),
        ('unequal_stream_lengths', (2, '00', '0', 1), {}),
        ('nonfinite_budget', (2, '0', '0', 1), {'seconds': float('nan')}),
        ('excess_memory_budget', (2, '0', '0', 1), {'memory_mb': 8193}),
        ('malformed_fixture', (2, '0', '0', 1), {'fixed_words': [[1, 1]]}),
        ('construction_budget', (2, '0', '0', 1), {'seconds': 1e-8}),
    ]
    results = []
    for label, query, extra in cases:
        for name, solve in backends():
            options = {'seconds': 5, 'memory_mb': 1024}
            options.update(extra)
            result = solve(*query, **options)
            require(result.get('status') == 'UNDECIDED',
                    f'{name} guard {label} became a terminal result: {result}')
            results.append({'case': label, 'backend': name, 'reason': result.get('reason')})
    return {'cases': len(cases), 'backend_checks': len(results), 'results': results}


def deadline(_signum, _frame):
    raise OverallLimit('900-second overall validation limit')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quick', action='store_true')
    parser.add_argument('--no-guards', action='store_true')
    args = parser.parse_args()
    # Both backends start fresh Python workers. Preserve the requested -O
    # level through their inherited environments, so child checks agree.
    os.environ['PYTHONOPTIMIZE'] = str(sys.flags.optimize)
    started = time.monotonic()
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(900)
    selected = queries(args.quick)
    stats = {'cp_sat': Counter(), 'z3_qfbv': Counter(),
             'cp_sat_charge': Counter(), 'replay': Counter()}
    undecided = []
    expected_sat = 0
    for query in selected:
        base, e, g, width = query
        expected = (e, g) in returning_streams(base, width, len(e))
        expected_sat += expected
        execute_case(query, expected, stats, undecided)
    fixtures = source_fixtures()
    for base, e, g, width, words in fixtures:
        execute_case((base, e, g, width), True, stats, undecided, words)
    guards = None if args.no_guards else guard_checks()
    signal.alarm(0)
    output = {
        'status': 'UNDECIDED' if undecided else 'PASS',
        'quick': args.quick,
        'python_optimize': sys.flags.optimize,
        'oracle_queries': len(selected),
        'base_two_queries': sum(q[0] == 2 for q in selected),
        'seeded_queries': sum(q[0] != 2 for q in selected),
        'oracle_expected_sat': expected_sat,
        'oracle_expected_unsat': len(selected)-expected_sat,
        'complete_word_graphs': full_graph.cache_info().currsize,
        'return_stream_queries': returning_streams.cache_info().currsize,
        'source_fixtures': len(fixtures),
        'fixture_bases': [item[0] for item in fixtures],
        'solver_decisions': {key: dict(value) for key, value in stats.items()},
        'guards': guards,
        'undecided': undecided,
        'ortools_version': importlib.metadata.version('ortools'),
        'z3_solver_version': importlib.metadata.version('z3-solver'),
        'seconds': round(time.monotonic()-started, 3),
    }
    print(json.dumps(output, sort_keys=True))
    return 3 if undecided else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except OverallLimit as error:
        signal.alarm(0)
        print(json.dumps({'status': 'UNDECIDED', 'reason': str(error)}))
        sys.exit(3)
    except (CheckFailure, ValueError, KeyError, TypeError, OSError) as error:
        signal.alarm(0)
        print(json.dumps({'status': 'FAIL', 'reason': str(error)}))
        sys.exit(1)
