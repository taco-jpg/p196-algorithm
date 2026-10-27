#!/usr/bin/env python3
"""Independent integer oracle for Agent 101's review of the prefix/center graph.

The exterior oracle realizes each unresolved carry with a concrete extra
coefficient, then performs full positional-integer normalization. It does not
reuse the C++ column recurrence. Graph positives are projection witnesses only.
"""
import argparse
import itertools
import json
import random
import subprocess
import sys
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def normalized(word, entry, base=10):
    value = entry + sum(coefficient * base**i for i, coefficient in enumerate(word))
    digits = []
    for _ in word:
        value, digit = divmod(value, base)
        digits.append(digit)
    return tuple(digits), value


def exterior(word, base=10):
    left, entry = normalized(word, 0, base)
    right, growth = normalized(word[::-1], 1-entry, base)
    if growth:
        left = left + ((base-1)*(1-entry),)
        right = (1,) + right[::-1]
    else:
        right = right[::-1]
    return tuple(a+b for a, b in zip(left, right)), entry, growth


def pad_prefix(word, width, base=10):
    return (tuple(word) + (base-1,)*width)[:width]


@lru_cache(maxsize=None)
def prefix_edges(word):
    edges = set()
    for unknown in (0, 1):
        # A final 0 forces forward carry 0 and inward reverse carry 0;
        # a final 18 forces forward carry 1 and inward reverse carry 1.
        raw, _, growth = exterior(word + (18*unknown,))
        edges.add((raw[:len(word)], growth))
    return frozenset(edges)


def admissible(center, even_middle=False, base=10):
    return (bool(center) and center == center[::-1]
            and all(0 <= x <= 2*base-2 for x in center)
            and any(x != base-1 for x in center)
            and (not even_middle or len(center) % 2 == 0
                 or center[len(center)//2] % 2 == 0))


def center_edges(center, growth, bound=None, even_middle=False, base=10):
    edges = set()
    for entry in (0, 1):
        digits, carry = normalized(center, entry, base)
        if carry != 1-entry:
            continue
        word = digits + ((base-1)*entry,) if growth else digits
        raw = tuple(a+b for a, b in zip(word, word[::-1]))
        trim = 0
        while raw:
            if ((bound is None or len(raw) <= bound)
                    and admissible(raw, even_middle, base)):
                edges.add((raw, entry, trim))
            if len(raw) < 2 or raw[0] != base-1 or raw[-1] != base-1:
                break
            raw = raw[1:-1]
            trim += 1
    return edges


def centers(bound, even_middle):
    for length in range(1, bound+1):
        alphabets = [range(19)] * ((length+1)//2)
        if even_middle and length % 2:
            alphabets[-1] = range(0, 19, 2)
        for half in itertools.product(*alphabets):
            word = half + half[:length//2][::-1]
            if any(x != 9 for x in word):
                yield word


def prefixes(width):
    return ((a,)+tail for a in range(1, 19)
            for tail in itertools.product(range(19), repeat=width-1))


def factor_check(engine, width, bound, even_middle):
    remaining_prefix = set(prefixes(width))
    remaining_center = set(centers(bound, even_middle))
    prefix_count, center_count = len(remaining_prefix), len(remaining_center)
    prefix_arcs, center_arcs = Counter(), Counter()
    command = [engine, '--prefix', str(width), '--center', str(bound),
               '--dump-factors', '--seconds', '120', '--memory-mb', '1024']
    if not even_middle:
        command.append('--all-middles')
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True)
    metadata = []
    try:
        for line in process.stdout:
            row = json.loads(line)
            if row.get('kind') not in ('prefix', 'center'):
                metadata.append(row)
                continue
            word = tuple(row['word'])
            if row['kind'] == 'prefix':
                require(word in remaining_prefix, f'Duplicate/invalid prefix {word}')
                remaining_prefix.remove(word)
                actual = {(tuple(edge['target']), edge['g']) for edge in row['edges']}
                require(len(actual) == len(row['edges']), 'Duplicate prefix transitions')
                require(actual == prefix_edges(word), f'Prefix factor mismatch {word}')
                for edge in row['edges']:
                    require(edge['boundary_carry'] in (0, 1), 'Invalid reverse carry')
                    raw, _, growth = exterior(word+(18*edge['boundary_carry'],))
                    require((raw[:width], growth) == (tuple(edge['target']), edge['g']),
                            'Recorded reverse carry does not realize prefix edge')
                    prefix_arcs[edge['g']] += 1
            else:
                require(word in remaining_center, f'Duplicate/invalid center {word}')
                remaining_center.remove(word)
                entries = [e for e in (0, 1) if normalized(word, e)[1] == 1-e]
                require(entries == [row['e']], f'Incorrect center carry {word}')
                actual = {(tuple(edge['target']), edge['g'], edge['v'])
                          for edge in row['edges']}
                expected = {(target, g, trim) for g in (0, 1)
                            for target, _, trim in center_edges(word, g, bound, even_middle)}
                require(len(actual) == len(row['edges']), 'Duplicate center transitions')
                require(actual == expected, f'Center factor mismatch {word}')
                for _, growth, _ in actual:
                    center_arcs[growth] += 1
        stderr = process.stderr.read()
        require(process.wait(timeout=10) == 0, f'Factor export failed: {stderr[:500]}')
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
    require(not remaining_prefix and not remaining_center, 'Incomplete factor enumeration')
    arcs = sum(prefix_arcs[g]*center_arcs[g] for g in (0, 1))
    return {'status': 'PASS', 'prefix_width': width, 'center_bound': bound,
            'even_middle': even_middle, 'prefixes': prefix_count, 'centers': center_count,
            'prefix_arcs': dict(prefix_arcs), 'center_arcs': dict(center_arcs),
            'product_vertices': prefix_count*center_count, 'product_arcs': arcs,
            'factor_metadata': metadata}


def witness_check(result):
    # Accommodate a standalone witness object or its graph-result wrapper.
    witness = result.get('projected_cycle', result.get('cycle', result))
    edges = witness.get('edges', []) if isinstance(witness, dict) else witness
    require(edges, 'No projected cycle to validate')
    growth_sum, trim_sum = 0, 0
    for index, edge in enumerate(edges):
        source = tuple(edge['prefix'])
        target = tuple(edge['next_prefix'])
        center = tuple(edge['C'])
        next_center = tuple(edge['next_C'])
        growth, trim = edge['g'], edge['v']
        require(source and 1 <= source[0] <= 18 and all(0 <= a <= 18 for a in source),
                'Invalid exterior-prefix domain')
        require(len(target) == len(source) and admissible(center), 'Invalid product vertex')
        require((target, growth) in prefix_edges(source), 'Invalid projected exterior edge')
        if 'boundary_carry' in edge:
            require(edge['boundary_carry'] in (0, 1), 'Invalid witnessed cut carry')
            raw, _, overflow = exterior(source+(18*edge['boundary_carry'],))
            require((raw[:len(source)], overflow) == (target, growth),
                    'Witnessed cut carry does not realize the edge')
        require((next_center, edge['e'], trim) in center_edges(center, growth),
                'Invalid complete center edge')
        following = edges[(index+1) % len(edges)]
        require(target == tuple(following['prefix']) and next_center == tuple(following['C']),
                'Projected edge list fails to close')
        require(not len(center) % 2 or center[len(center)//2] % 2 == 0,
                'Closed center cycle violates even middle')
        growth_sum += growth
        trim_sum += trim
    require(growth_sum == 2*trim_sum, 'Closed center lengths fail to telescope')
    return {'status': 'PASS', 'projected_cycle_edges': len(edges),
            'sum_g': growth_sum, 'sum_v': trim_sum, 'actual_certificate': False}


def arithmetic_controls():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror
    counts = Counter()
    rng = random.Random(101)

    def check_exterior(word):
        raw, entry, growth = exterior(word)
        center = [10] if entry == 0 else [0]
        require(mirror.hyp(10, list(word), center), 'Exterior control violates Hyp')
        require(list(raw) == mirror.nextB(10, list(word), center), 'Whole-word normalization differs')
        require(growth == mirror.gam(10, list(word), center), 'Whole-word overflow differs')
        allowed = prefix_edges(pad_prefix(word, 3))
        for trim in range(len(raw)+1):
            if trim and raw[-trim:] != (9,)*trim:
                break
            target = raw[:-trim] if trim else raw
            require((pad_prefix(target, 3), growth) in allowed,
                    'An actual exterior suffix trim is missing from the projection')
            counts['exterior_trim_projections'] += 1
        counts['exterior_words'] += 1

    check_exterior(())
    for length in range(1, 5):
        for word in prefixes(length):
            check_exterior(word)
    for _ in range(10000):
        length = rng.randrange(1, 81)
        word = (rng.randrange(1, 19),)+tuple(rng.randrange(19) for _ in range(length-1))
        check_exterior(word+(9,)*rng.randrange(16))
    for center in centers(6, False):
        for growth in (0, 1):
            expected = set()
            for entry in (0, 1):
                digits, carry = mirror.norm(10, list(center), entry)
                if carry != 1-entry:
                    continue
                word = digits+[9*entry] if growth else digits
                raw = tuple(x+y for x, y in zip(word, reversed(word)))
                trim = 0
                while raw:
                    if admissible(raw):
                        expected.add((raw, entry, trim))
                    if len(raw) < 2 or raw[0] != 9 or raw[-1] != 9:
                        break
                    raw = raw[1:-1]
                    trim += 1
            require(center_edges(center, growth) == expected, 'Center integer/column mismatch')
            require(all(not len(c) % 2 or c[len(c)//2] % 2 == 0 for c, _, _ in expected),
                    'A center edge violates even-middle target invariance')
            counts['center_cases'] += 1
    for base, edges in mirror._lean_certs():
        require(mirror.cycleOK(base, edges, edges[0][0], edges[0][1]), 'Known source rejected')
        for word, center, target, next_center, outer_trim, inner_trim in edges:
            raw, entry, growth = exterior(tuple(word), base)
            require(raw == tuple(target)+(base-1,)*outer_trim, 'Known exterior arithmetic differs')
            require((tuple(next_center), entry, inner_trim)
                    in center_edges(tuple(center), growth, base=base), 'Known center arithmetic differs')
            counts['known_edges'] += 1
    return {'status': 'PASS', 'arithmetic_controls': dict(counts)}


def guard_checks(engine):
    # require() stays active under python -O; a resource cap is never a negative.
    ordinary = ['--prefix', '1', '--center', '4']
    cases = [
        ('zero_prefix', ['--prefix', '0', '--center', '4'], 2,
         {'invalid_or_unsupported_input'}),
        ('unsupported_prefix', ['--prefix', '4', '--center', '4'], 2,
         {'invalid_or_unsupported_input'}),
        ('unsupported_center', ['--prefix', '1', '--center', '8'], 2,
         {'invalid_or_unsupported_input'}),
        ('unknown_option', ordinary+['--unknown', '1'], 2,
         {'invalid_or_unsupported_input'}),
        ('missing_value', ordinary+['--seconds'], 2,
         {'invalid_or_unsupported_input'}),
        ('noninteger_value', ['--prefix', '1', '--center', '1.5'], 2,
         {'invalid_or_unsupported_input'}),
        ('uint64_overflow', ordinary+['--seconds', str(2**64)], 2,
         {'invalid_or_unsupported_input'}),
        ('oversized_wall_limit', ordinary+['--seconds', '1801'], 2,
         {'invalid_or_unsupported_input'}),
        ('oversized_memory_limit', ordinary+['--memory-mb', '8193'], 2,
         {'invalid_or_unsupported_input'}),
        ('graph_memory_budget', ['--prefix', '3', '--center', '7',
                                 '--memory-mb', '64', '--seconds', '10'], 3,
         {'graph arrays exceed memory budget', 'memory_limit'}),
        ('witness_path_cap', ['--prefix', '2', '--center', '6', '--all-middles',
                              '--witness-cap', '1', '--memory-mb', '128',
                              '--seconds', '10'], 3,
         {'projected witness path cap'}),
        ('wall_timeout', ['--prefix', '3', '--center', '7',
                          '--seconds', '1', '--memory-mb', '4096'], 3,
         {'wall_timeout'}),
    ]
    results = []
    for name, arguments, code, reasons in cases:
        process = subprocess.run([engine]+arguments, capture_output=True,
                                 text=True, timeout=20, check=False)
        require(process.returncode == code,
                f'{name}: exit {process.returncode}, expected {code}; '
                f'stderr={process.stderr[:300]}')
        result = json.loads(process.stdout)
        require(result.get('status') == 'UNDECIDED',
                f'{name}: a rejected or capped run was treated as a terminal result')
        require(result.get('reason') in reasons,
                f'{name}: unexpected rejection reason {result.get("reason")}')
        results.append({'case': name, 'returncode': process.returncode,
                        'reason': result['reason']})
    return {'status': 'PASS', 'guards': len(results), 'guard_results': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine')
    parser.add_argument('--factors', nargs=2, type=int, metavar=('PREFIX', 'CENTER'))
    parser.add_argument('--all-middles', action='store_true')
    parser.add_argument('--witness', type=Path)
    parser.add_argument('--guards', action='store_true')
    args = parser.parse_args()
    started = time.monotonic()
    if args.guards:
        require(args.engine is not None, '--guards requires --engine')
        require(not args.factors and not args.witness,
                '--guards cannot be combined with a factor or witness check')
        result = guard_checks(args.engine)
    elif args.factors:
        require(args.engine is not None, '--factors requires --engine')
        width, bound = args.factors
        require(1 <= width <= 3 and 1 <= bound <= 7, 'Unsupported factor check bounds')
        result = factor_check(args.engine, width, bound, not args.all_middles)
    elif args.witness:
        result = witness_check(json.loads(args.witness.read_text()))
    else:
        result = arithmetic_controls()
    result['seconds'] = round(time.monotonic()-started, 3)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (CheckFailure, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        print(json.dumps({'status': 'FAIL', 'reason': str(error)}))
        sys.exit(1)
