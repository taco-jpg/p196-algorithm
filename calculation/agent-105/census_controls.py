#!/usr/bin/env python3
"""Independent controls for necklace_head.cpp, using sets and the official mirror.

No primary agent census/filter code is imported.  The manifest is research input,
not a transcript; successful validation prints one JSON object to stdout.
"""
import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import product
import json
from math import comb, gcd
from pathlib import Path
import subprocess


def need(condition, message):
    if not condition:
        raise ArithmeticError(message)


def least_rotation(word):
    return min(word[i:]+word[:i] for i in range(len(word)))


def head_targets(x, g):
    result = set()
    for c in (0, 1):
        if (x+c)//10 == g:
            result.add(2*x+c if g == 0 else x % 10+1)
    return result


def closed_heads(word):
    answer = []
    for initial in range(1, 19):
        possible = {initial}
        for g in map(int, word):
            possible = {y for x in possible for y in head_targets(x, g)}
            if not possible:
                break
        if initial in possible:
            answer.append(initial)
    return answer


def closed_path_counts(word, distinguish_inward_carries=False):
    """Count paths using Python integers, separately from bitset acceptance."""
    answer = {}
    for initial in range(1, 19):
        counts = Counter({initial:1})
        for g in map(int, word):
            next_counts = Counter()
            for x, count in counts.items():
                if distinguish_inward_carries:
                    targets = [2*x+c if g == 0 else x % 10+1
                               for c in (0, 1) if (x+c)//10 == g]
                else:
                    targets = head_targets(x, g)
                for y in targets:
                    next_counts[y] += count
            counts = next_counts
        if counts[initial]:
            answer[initial] = counts[initial]
    return answer


def totient(n):
    return sum(gcd(k, n) == 1 for k in range(1, n+1))


def necklace_count_by_weight(n, weight):
    return sum(totient(d)*comb(n//d, weight//d)
               for d in range(1, gcd(n, weight)+1)
               if n % d == 0 and weight % d == 0)//n


def invoke(executable, n):
    # The manifest goes to stdout; the final line is the JSON census summary.
    output = subprocess.check_output([str(executable), str(n), "/dev/stdout"], text=True)
    lines = output.splitlines()
    return set(lines[:-1]), json.loads(lines[-1])


def enumeration_controls(executable, max_period):
    checked_necklaces = 0
    checked_words = 0
    for n in range(1, max_period+1):
        raw = (''.join(bits) for bits in product('01', repeat=n))
        all_necklaces = {least_rotation(word) for word in raw}
        expected_survivors = {word for word in all_necklaces if closed_heads(word)}
        found, summary = invoke(executable, n)
        need(found == expected_survivors, f"survivor mismatch at period {n}")
        counts = Counter(word.count('1') for word in all_necklaces)
        need(summary['all_necklaces'] == len(all_necklaces), f"necklace count at {n}")
        for weight in range(n+1):
            need(summary['necklaces_by_weight'][weight] == counts[weight]
                 == necklace_count_by_weight(n, weight), f"weight count at {(n, weight)}")
        checked_necklaces += len(all_necklaces)
        checked_words += 1 << n
    return {'periods':max_period, 'binary_words':checked_words,
            'distinct_necklaces':checked_necklaces}


def mirror_controls(path):
    spec = importlib.util.spec_from_file_location('a105_original_mirror', path)
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    # Empty B is represented by virtual head9: its next B is [10].  A trim to
    # empty B likewise had raw lowest coefficient9.  This makes the graph a
    # necessary relaxation even when the genuine B cycle visits empty words.
    need(mirror.hyp(10, [], [18]), 'empty exterior hypothesis')
    need(mirror.gam(10, [], [18]) == 1 and mirror.nextB(10, [], [18]) == [10],
         'empty exterior virtual-head transition')
    need(10 in head_targets(9, 1), 'missing virtual-head transition')
    transition_checks = 0
    seen = set()
    # B=[x,10*c] realizes either required inward bit c at the low coefficient.
    for x in range(1, 19):
        for c in (0, 1):
            bword = [x, 10*c]
            e = mirror.e1(10, bword)
            center = [0] if e else [18]
            need(mirror.hyp(10, bword, center), 'control hypothesis')
            need(mirror.norm(10, bword[:0:-1], 1-e)[1] == c, 'inward carry control')
            g = mirror.gam(10, bword, center)
            y = mirror.nextB(10, bword, center)[0]
            need(g == (x+c)//10, 'overflow formula')
            need(y == (2*x+c if g == 0 else x % 10+1), 'head formula')
            seen.add((x, g, y))
            transition_checks += 1
    graph = {(x, g, y) for x in range(1, 19) for g in (0, 1)
             for y in head_targets(x, g)}
    need(seen == graph, 'some graph edge lacks a genuine mirror realization')
    source_checks = 0
    for width in range(1, 4):
        for x in range(1, 19):
            for tail in product(range(19), repeat=width-1):
                bword = [x, *tail]
                e = mirror.e1(10, bword)
                center = [0] if e else [18]
                need(mirror.hyp(10, bword, center), 'exhaustive source hypothesis')
                g = mirror.gam(10, bword, center)
                y = mirror.nextB(10, bword, center)[0]
                need(y in head_targets(x, g), 'exact mirror transition missing')
                source_checks += 1
    return {'realizing_inward_carry_cases':transition_checks,
            'distinct_graph_edges':len(graph), 'exhaustive_nonempty_exteriors':source_checks,
            'empty_exterior_control':True}


def manifest_controls(path):
    data = path.read_bytes()
    words = data.decode('ascii').splitlines()
    need(words and len(set(words)) == len(words), 'duplicate or empty manifest')
    need(all(len(word) == 23 and set(word) <= {'0', '1'} for word in words), 'bad manifest word')
    need(words == sorted(words, key=lambda word:(word.count('1'), word)), 'manifest order')
    need(all(word == least_rotation(word) for word in words), 'noncanonical manifest word')
    need(all(closed_heads(word) for word in words), 'manifest false survivor')
    counts = Counter(word.count('1') for word in words)
    hard = '10101010101001001110000'
    hard_rotation = least_rotation(hard)
    need(hard_rotation in words, 'hard word missing')
    return {'lines':len(words), 'weights':dict(sorted(counts.items())),
            'sha256':sha256(data).hexdigest(),
            'hard_word_canonical':hard_rotation, 'hard_word_closed_heads':closed_heads(hard),
            'hard_word_closed_head_paths':closed_path_counts(hard),
            'hard_word_closed_head_carry_paths':closed_path_counts(hard, True)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mirror', type=Path, required=True)
    parser.add_argument('--executable', type=Path, default=Path(__file__).with_name('necklace_head'))
    parser.add_argument('--manifest', type=Path, default=Path(__file__).with_name('p23-head-survivors.txt'))
    parser.add_argument('--max-control-period', type=int, default=12)
    args = parser.parse_args()
    if not 1 <= args.max_control_period <= 14:
        parser.error('--max-control-period must lie in 1..14')
    enumeration = enumeration_controls(args.executable.resolve(), args.max_control_period)
    mirrors = mirror_controls(args.mirror)
    manifest = manifest_controls(args.manifest)
    expected_all = sum(necklace_count_by_weight(23, weight) for weight in range(24))
    need(expected_all == (2**23+22*2)//23, 'prime-period necklace formula disagreement')
    print(json.dumps({'status':'PASS', 'small_enumeration':enumeration,
                      'mirror':mirrors, 'manifest':manifest,
                      'p23_all_weights_Burnside_total':expected_all}, sort_keys=True))


if __name__ == '__main__':
    main()
