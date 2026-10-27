#!/usr/bin/env python3
"""Independent finite-word tests for backward regular exterior languages.

The oracle derives old carries from a proposed coefficient trajectory using
integer division; it imports no generator or reverse-automaton arithmetic.
All cyclic correlations are retained in complete temporal tuples.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from itertools import product
import json
from pathlib import Path
import re
import subprocess
import sys
import time

P24 = (10, '010100110100101011001011', '110001001000110001001000')
ROOT = Path(__file__).resolve().parents[2]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


class Undecided(RuntimeError):
    pass


class Budget:
    def __init__(self, cap=350000, seconds=120):
        self.cap, self.deadline, self.nodes = cap, time.monotonic()+seconds, 0

    def tick(self):
        self.nodes += 1
        if self.nodes % 1024 == 0 and time.monotonic() >= self.deadline:
            raise Undecided('independent oracle time limit')

    def size(self, count):
        if count > self.cap:
            raise Undecided('independent oracle state cap')
        if time.monotonic() >= self.deadline:
            raise Undecided('independent oracle time limit')


class ExteriorProblem:
    def __init__(self, base, e, g):
        require(2 <= base <= 62 and e and len(e) == len(g), 'bad base or unit lengths')
        require(set(e+g) <= {'0', '1'}, 'nonbinary driver')
        self.base, self.e, self.g, self.p = base, e, g, len(e)
        self.rows = {(l, h, y): (l, h, y) for l, h, y in product((0, 1), (0, 1), range(base))}
        self.tables = {}

    def terminal(self, k=1):
        return tuple(self.rows[(int(e), 1-int(e), (self.base-1)*int(e) if g == '1' else 0)]
                     for e, g in zip(self.e*k, self.g*k))

    def physical_root(self, k=1):
        return tuple(self.rows[(0, int(g), int(g))] for g in self.g*k)

    def phase_table(self, target, overflow, first):
        key = target, overflow, first
        if key in self.tables:
            return self.tables[key]
        b, (new_l, new_h, new_y) = self.base, target
        require(new_l in (0, 1) and new_h in (0, 1) and 0 <= new_y < b, 'bad cut symbol')
        require(overflow or new_y == 0, 'noncanonical unused partner digit')
        table = [[] for _ in range(2*b-1)]
        for x in range(int(first), 2*b-1):
            old_h, high = divmod(x+new_h, b)
            if overflow and high != new_y:
                continue
            for old_l in (0, 1):
                carry, low = divmod(x+old_l, b)
                if carry != new_l:
                    continue
                for old_y in range(b) if overflow else (0,):
                    following = low+(old_y if overflow else high)
                    table[x].append((following, self.rows[(old_l, old_h, old_y)]))
        self.tables[key] = table
        return table

    def predecessors(self, target, budget, first=False, columns=False):
        """Yield complete old cuts; the coefficient at time P equals time 0."""
        require(len(target) % self.p == 0, 'partial temporal word')
        period, domain = len(target), 2*self.base-1
        tables = [self.phase_table(row, self.g[t % self.p] == '1', first)
                  for t, row in enumerate(target)]
        # A suffix bit mask records all possible final coefficients. It only
        # prunes impossible closures; no old cut coordinate is projected away.
        reach = [None]*(period+1)
        reach[period] = [1 << x for x in range(domain)]
        for t in range(period-1, -1, -1):
            reach[t] = [0]*domain
            for x, choices in enumerate(tables[t]):
                for following, _ in choices:
                    reach[t][x] |= reach[t+1][following]
        path, coefficients = [None]*period, [None]*period
        def walk(t, x, closing):
            budget.tick()
            if t == period:
                yield (tuple(path), tuple(coefficients)) if columns else tuple(path)
                return
            coefficients[t] = x
            for following, row in tables[t][x]:
                if reach[t+1][following] & closing:
                    path[t] = row
                    yield from walk(t+1, following, closing)
        for x in range(int(first), domain):
            if reach[0][x] & (1 << x):
                yield from walk(0, x, 1 << x)

    def previous_layer(self, frontier, budget):
        result = set()
        for state in frontier:
            for old in self.predecessors(state, budget):
                result.add(old)
                if len(result) > budget.cap:
                    raise Undecided('independent oracle state cap')
            budget.size(len(result))
        return result


def integer_step(base, word):
    """Autonomous exterior step from whole positional integers, before trim."""
    word = tuple(word)
    require(all(0 <= x <= 2*base-2 for x in word), 'coefficient outside base range')
    require(not word or word[0] > 0, 'zero physical first coefficient')
    modulus = base**len(word)
    e, forward = divmod(sum(x*base**i for i, x in enumerate(word)), modulus)
    g, backward = divmod(sum(x*base**i for i, x in enumerate(reversed(word)))+1-e, modulus)
    require(e in (0, 1) and g in (0, 1), 'unexpected carry')
    low, high = [], []
    for _ in word:
        forward, digit = divmod(forward, base); low.append(digit)
        backward, digit = divmod(backward, base); high.append(digit)
    high.reverse()
    if g:
        low.append((base-1)*(1-e)); high.insert(0, 1)
    return e, g, tuple(a+b for a, b in zip(low, high))


def trim_neutral(base, word):
    word = tuple(word)
    while word and word[-1] == base-1:
        word = word[:-1]
    return word


def verify_cycle(base, e, g, words):
    require(len(words) == len(e) == len(g), 'wrong exterior cycle length')
    for t, word in enumerate(words):
        actual_e, actual_g, following = integer_step(base, word)
        require((actual_e, actual_g) == (int(e[t]), int(g[t])), f'integer driver mismatch at phase {t}')
        require(trim_neutral(base, following) == trim_neutral(base, words[(t+1) % len(words)]),
                f'integer exterior cycle mismatch at phase {t}')


def integer_cut(problem, words, position, width):
    """Carries and partner digits from complete positional integers."""
    result = []
    for t, original in enumerate(words):
        word = tuple(original)+(problem.base-1,)*(width-len(original))
        entry = int(problem.e[t % problem.p])
        low = sum(x*problem.base**i for i, x in enumerate(word[:position])) // problem.base**position
        reverse = sum(x*problem.base**i for i, x in enumerate(reversed(word[position:])))+1-entry
        high = reverse // problem.base**(width-position)
        partner = ((word[position-1]+high) % problem.base if position else 1)
        result.append((low, high, partner if problem.g[t % problem.p] == '1' else 0))
    return tuple(result)


class Language:
    def __init__(self, data, unit, depth):
        require(data.get('format') == 'p196-exterior-dfa-v1' and data.get('direction') == 'backward',
                'wrong language format or direction')
        require(data.get('role') == 'frontier' and data.get('depth') == depth, 'wrong frontier role or depth')
        require(tuple(data[key] for key in ('base', 'e', 'g')) == tuple(unit), 'wrong requested problem')
        self.base, self.e, self.g = unit
        self.p = len(self.e)
        require(data['unit_period'] == self.p, 'wrong unit period')
        self.symbols = {}
        for row in data['alphabet']:
            label, phase, l, h, y = (row[key] for key in ('label', 'phase', 'L', 'H', 'Y'))
            require(all(isinstance(x, int) for x in (label, phase, l, h, y)), 'noninteger alphabet metadata')
            require(0 <= phase < self.p and l in (0, 1) and h in (0, 1) and 0 <= y < self.base,
                    'invalid cut symbol')
            require(self.g[phase] == '1' or y == 0, 'noncanonical unused partner digit')
            require(label == phase*(4*self.base)+l*(2*self.base)+h*self.base+y, 'incorrect symbol encoding')
            require(label not in self.symbols, 'duplicate symbol ID')
            self.symbols[label] = (phase, (l, h, y))
        expected = sum(4*self.base if bit == '1' else 4 for bit in self.g)
        require(len(self.symbols) == expected, 'incomplete phase alphabet')
        self.initial = data['start']
        self.final = set(data['finals'])
        self.edges = []
        size = len(data['transitions'])
        require(0 <= self.initial < size and all(0 <= q < size for q in self.final), 'invalid DFA states')
        require(len(self.final) == len(data['finals']), 'duplicate final state')
        for row in data['transitions']:
            edges = {}
            for label, target in row:
                require(label in self.symbols and 0 <= target < size and label not in edges,
                        'invalid or nondeterministic DFA edge')
                edges[label] = target
            self.edges.append(edges)
        require(self.initial not in self.final, 'epsilon must not represent a positive repetition')

    def encode(self, state):
        return tuple((t % self.p)*(4*self.base)+l*(2*self.base)+h*self.base+y
                     for t, (l, h, y) in enumerate(state))

    def decode(self, word):
        require(word and len(word) % self.p == 0, 'incomplete positive cut word')
        result = []
        for t, label in enumerate(word):
            require(label in self.symbols and self.symbols[label][0] == t % self.p, 'wrong word chronology')
            result.append(self.symbols[label][1])
        return tuple(result)

    def accepts(self, word):
        state = self.initial
        for label in word:
            if label not in self.edges[state]:
                return False
            state = self.edges[state][label]
        return state in self.final

    def counts(self, max_k=3):
        active, results = {self.initial: 1}, []
        for length in range(1, self.p*max_k+1):
            following = defaultdict(int)
            for state, number in active.items():
                for target in self.edges[state].values():
                    following[target] += number
            active = following
            if length % self.p == 0:
                results.append(sum(number for state, number in active.items() if state in self.final))
        return results


def invoke(command, seconds):
    try:
        return subprocess.run(list(map(str, command)), text=True, capture_output=True, timeout=seconds+5)
    except subprocess.TimeoutExpired as exc:
        raise Undecided('external engine timeout') from exc


def events_from(run):
    events = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
    statuses = [event for event in events if 'status' in event]
    require(len(statuses) == 1 and events[-1] is statuses[0], 'missing or ambiguous final status')
    return events, statuses[0]


def engine_dump(binary, unit, depth, seconds):
    command = [binary, *unit, '--depth', depth, '--dump-depth', depth, '--count-k', 3,
               '--states', 1000000, '--edges', 20000000, '--ops', 1000000000, '--seconds', seconds]
    run = invoke(command, seconds)
    events, result = events_from(run)
    if result['status'] == 'UNDECIDED':
        raise Undecided(f'engine dump: {result}')
    dumps = [event for event in events if event.get('event') == 'dump']
    require(run.returncode == 0 and result['status'] == 'DUMPED' and len(dumps) == 1, 'missing completed dump')
    return Language(dumps[0], unit, depth)


def compare_set(language, frontier, k, counts):
    require(counts[k-1] == len(frontier), f'cardinality mismatch at k={k}: {counts[k-1]} != {len(frontier)}')
    # The checked symbol formula is injective in every complete tuple.
    require(all(language.accepts(language.encode(state)) for state in frontier), f'membership mismatch at k={k}')
    return len(frontier)


def p24_tests(args):
    problem, front = ExteriorProblem(*P24), None
    budget = Budget(args.oracle_cap, args.seconds)
    front = {problem.terminal()}
    memberships = 0
    for depth in range(4):
        if depth:
            front = problem.previous_layer(front, budget)
        require(len(front) == (1, 2304, 62001, 259645)[depth], 'P24 predecessor fixture mismatch')
        language = engine_dump(args.engine, P24, depth, args.seconds)
        counts = language.counts()
        memberships += compare_set(language, front, 1, counts)
        print(json.dumps(dict(status='PASS', test='p24', depth=depth, exact_set_k=[1],
                              count_by_k=counts, memberships=len(front), dfa_states=len(language.edges)),
                         sort_keys=True), flush=True)
    print(f'P24 EXACT SETS PASSED languages=4 memberships={memberships} oracle_nodes={budget.nodes}', flush=True)


def tiny_tests(args):
    units = comparisons = memberships = 0
    for base in (2, 3):
        for period in (1, 2):
            bits = [''.join(row) for row in product('01', repeat=period)]
            for e, g in product(bits, repeat=2):
                unit = base, e, g
                problem, budget = ExteriorProblem(*unit), Budget(50000, args.seconds)
                fronts = [{problem.terminal(k)} for k in (1, 2, 3)]
                for depth in range(4):
                    language = engine_dump(args.engine, unit, depth, args.seconds)
                    counts = language.counts()
                    for k in (1, 2, 3):
                        if depth:
                            fronts[k-1] = problem.previous_layer(fronts[k-1], budget)
                        memberships += compare_set(language, fronts[k-1], k, counts)
                        comparisons += 1
                units += 1
    print(f'TINY EXACT SETS PASSED units={units} languages={comparisons} memberships={memberships}', flush=True)


def source_controls():
    paths = [ROOT/'lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean',
             ROOT/'lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean']
    controls = {}
    for path in paths:
        source = path.read_text()
        definitions = {m[1]: tuple(map(int, m[2].split(','))) if m[2].strip() else ()
                       for m in re.finditer(r'def (\w+)\s*:\s*List Nat\s*:=\s*\[([^\]]*)\]', source)}
        def word(token):
            if token.startswith('['):
                return tuple(map(int, token[1:-1].split(','))) if token[1:-1].strip() else ()
            return definitions[token]
        for match in re.finditer(r'def cert(\d+)\s*:\s*List Edge\s*:=\s*(\[.*?\])\n\n', source, re.S):
            base, es, gs, words = int(match[1]), '', '', []
            for fields in re.findall(r'⟨(.*?)⟩', match[2], re.S):
                tokens = re.findall(r'\[[^\]]*\]|[A-Za-z_]\w*|\d+', fields)
                require(len(tokens) == 6, 'unexpected Lean source edge')
                exterior, following, trim = word(tokens[0]), word(tokens[2]), int(tokens[4])
                e, g, raw = integer_step(base, exterior)
                require(raw == following+(base-1,)*trim, 'source exterior edge failed integer replay')
                es += str(e); gs += str(g); words.append(exterior)
            verify_cycle(base, es, gs, words)
            controls[base] = es, gs, words
    require(set(controls) == {2, 4, 8, 11, 16, 17, 26, 32}, 'missing original source controls')
    return controls


def production_hit(args, unit, depth):
    run = invoke([args.engine, *unit, '--depth', depth, '--states', 1000000,
                  '--edges', 20000000, '--ops', 1000000000, '--seconds', args.seconds], args.seconds)
    _, result = events_from(run)
    if result['status'] == 'UNDECIDED':
        raise Undecided(f'positive production control: {result}')
    require(run.returncode == 0 and result['status'] == 'CUT_INTERSECTION', 'known positive cut was not found')
    require(result.get('integer_replay_required') is True, 'cut intersection was overstated as an integer witness')
    return result


def reconstruct_hit(problem, language, hit, budget):
    depth, k = hit['backward_depth'], hit['repetitions']
    require(hit['padded_columns'] == depth+1 and len(hit['word']) == problem.p*k, 'wrong intersection dimensions')
    current = language.decode(hit['word'])
    layers = [{problem.terminal(k)}]
    for _ in range(depth):
        layers.append(problem.previous_layer(layers[-1], budget))
    require(current in layers[-1], 'positive cut missing from exact finite predecessor layer')
    root, columns = problem.physical_root(k), []
    for old, coefficients in problem.predecessors(current, budget, first=True, columns=True):
        if old == root:
            columns.append(coefficients)
            break
    require(columns and all(x > 0 for x in columns[0]), 'physical FIRST has no positive coefficient trajectory')
    for remaining in range(depth, 0, -1):
        found = False
        for target in sorted(layers[remaining-1]):
            for old, coefficients in problem.predecessors(target, budget, columns=True):
                if old == current:
                    current = target; columns.append(coefficients); found = True
                    break
            if found:
                break
        require(found, 'cannot reconstruct a predecessor witness')
    require(current == problem.terminal(k), 'reconstructed path does not reach the terminal cut')
    words = [tuple(column[t] for column in columns) for t in range(problem.p*k)]
    verify_cycle(problem.base, problem.e*k, problem.g*k, words)
    for t, word in enumerate(words):
        _, g, raw = integer_step(problem.base, word)
        require(raw == words[(t+1) % len(words)]+(problem.base-1,)*g,
                'fixed-width integer witness does not close with the required neutral suffix')
    return words


def positive_tests(args):
    controls = source_controls()
    prefixes = source_edges = replayed_edges = 0
    for base, (e, g, words) in controls.items():
        problem = ExteriorProblem(base, e, g)
        source_edges += len(words)
        width = max(map(len, words))
        if integer_cut(problem, words, width, width) != problem.terminal():
            width += 1
        require(integer_cut(problem, words, 0, width) == problem.physical_root(), 'source root cut mismatch')
        require(integer_cut(problem, words, width, width) == problem.terminal(), 'source terminal cut mismatch')
        for depth in (1, 2):
            language = engine_dump(args.engine, (base, e, g), depth, args.seconds)
            cut = integer_cut(problem, words, width-depth, width)
            require(language.accepts(language.encode(cut)), f'known base {base} source prefix rejected at depth {depth}')
            prefixes += 1
            if depth == 1 and base in (2, 4, 8, 16, 32):
                hit = production_hit(args, (base, e, g), 1)
                replayed_edges += len(reconstruct_hit(problem, language, hit, Budget(50000, args.seconds)))
    # Agent105's integer-replayable counterexample has driver unit 01, but the
    # exterior closes after TWO units. No center certificate is asserted.
    unit = (6, '01', '01')
    words = [(4, 7, 7, 8, 3), (9, 3, 4, 5, 8), (4, 7, 7, 10, 2, 2), (9, 3, 4, 9)]
    verify_cycle(6, '0101', '0101', words)
    problem, budget = ExteriorProblem(*unit), Budget(50000, args.seconds)
    fronts = [{problem.terminal(k)} for k in (1, 2, 3)]
    expected = ((1, 2, 4, 6, 8, 10), (1, 4, 10, 25, 47, 65), (1, 8, 28, 114, 161, 175))
    memberships, first_hits = 0, []
    for depth in range(6):
        language = engine_dump(args.engine, unit, depth, args.seconds)
        counts = language.counts()
        hits = []
        for k in (1, 2, 3):
            if depth:
                fronts[k-1] = problem.previous_layer(fronts[k-1], budget)
            require(len(fronts[k-1]) == expected[k-1][depth], 'period-descent count fixture mismatch')
            memberships += compare_set(language, fronts[k-1], k, counts)
            root = problem.physical_root(k)
            hits.append(any(root in set(problem.predecessors(state, budget, first=True)) for state in fronts[k-1]))
        first_hits.append(hits)
    require(first_hits == [[False, False, False]]*5+[[False, True, False]], 'wrong multi-unit FIRST closure')
    hit = production_hit(args, unit, 5)
    require((hit['backward_depth'], hit['padded_columns'], hit['repetitions']) == (5, 6, 2),
            'period-descent production fixture changed')
    replayed_edges += len(reconstruct_hit(problem, language, hit, Budget(50000, args.seconds)))
    for base in (2, 3, 10):
        require(integer_step(base, ()) == (0, 1, (base,)), 'empty exterior integer boundary changed')
    print(f'POSITIVE TESTS PASSED source_cycles=8 source_edges={source_edges} source_prefixes={prefixes} '
          f'production_integer_edges={replayed_edges} period_descent_languages=18 '
          f'period_descent_memberships={memberships} empty_boundary_cases=3', flush=True)


def guard_tests(args):
    invalid = [('base', (1, *P24[1:]), []), ('nonbinary', (10, '2'+P24[1][1:], P24[2]), []),
               ('length_mismatch', (10, P24[1][:-1], P24[2]), []),
               ('unit_length', (10, '0'*257, '0'*257), []),
               ('integer_range', P24, ['--depth', '4294967296'])]
    limited = [('states', ['--states', '1']), ('edges', ['--edges', '1']),
               ('operations', ['--ops', '1']), ('depth', ['--depth', '0']),
               ('wall_time', ['--seconds', '1', '--depth', '20', '--states', '5000000',
                              '--edges', '100000000', '--ops', '10000000000'])]
    cases = [(name, unit, flags, 'INVALID', 2) for name, unit, flags in invalid]
    cases += [(name, P24, flags, 'UNDECIDED', 3) for name, flags in limited]
    for name, unit, flags, status, code in cases:
        run = invoke([args.engine, *unit, *flags], 15)
        _, result = events_from(run)
        require(run.returncode == code and result['status'] == status,
                f'guard {name} returned {run.returncode}: {result}')
        print(json.dumps(dict(status='PASS', test='guard', case=name, engine_status=status,
                              reason=result.get('reason')), sort_keys=True), flush=True)
    for unit, depth, states, edges in (((2, '00', '10'), 0, 3, 3), ((4, '01', '10'), 3, 17, 31)):
        run = invoke([args.engine, *unit, '--depth', 8, '--seconds', args.seconds], args.seconds)
        events, result = events_from(run)
        first = [event for event in events if event.get('event') == 'positive_first']
        require(run.returncode == 0 and result['status'] == 'NO_EXTERIORS_ALL_REPETITIONS' and
                result.get('reason') == 'exact_backward_fixed_point', 'fixed-point control took wrong branch')
        require((result['depth'], result['dfa_states'], result['dfa_edges']) == (depth, states, edges),
                'fixed-point control dimensions changed')
        require(len(first) == 1 and all(int(n) > 0 for n in first[0]['count_by_k']),
                'fixed-point control must have a nonempty positive FIRST language')
        print(json.dumps(dict(status='PASS', test='fixed_point_branch', base=unit[0], e=unit[1], g=unit[2],
                              depth=depth, dfa_states=states, dfa_edges=edges), sort_keys=True), flush=True)
    run = invoke([args.engine, 2, '00', '00', '--depth', 8, '--seconds', args.seconds], args.seconds)
    events, result = events_from(run)
    first = [event for event in events if event.get('event') == 'positive_first']
    require(run.returncode == 0 and result['status'] == 'NO_EXTERIORS_ALL_REPETITIONS' and
            result.get('reason') == 'empty_positive_first', 'empty FIRST control took wrong branch')
    require(len(first) == 1 and all(int(n) == 0 for n in first[0]['count_by_k']), 'FIRST was not empty')
    print('GUARDS PASSED invalid=5 resource_undecided=5 fixed_point_controls=2 empty_first_controls=1', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', type=Path)
    parser.add_argument('--suite', choices=('oracle', 'p24', 'tiny', 'positives', 'guards', 'all'), default='all')
    parser.add_argument('--oracle-depth', type=int, default=1)
    parser.add_argument('--oracle-cap', type=int, default=350000)
    parser.add_argument('--seconds', type=int, default=120)
    args = parser.parse_args()
    if args.suite != 'oracle':
        require(args.engine, 'provide --engine for regular-language comparisons')
        if args.suite in ('p24', 'all'):
            p24_tests(args)
        if args.suite in ('tiny', 'all'):
            tiny_tests(args)
        if args.suite in ('positives', 'all'):
            positive_tests(args)
        if args.suite in ('guards', 'all'):
            guard_tests(args)
        print('EXTERIOR BACKWARD TESTS PASSED; finite tests do not establish an all-k exclusion')
        return
    problem = ExteriorProblem(*P24)
    budget = Budget(args.oracle_cap, args.seconds)
    front = {problem.terminal()}
    for depth in range(args.oracle_depth+1):
        if depth:
            front = problem.previous_layer(front, budget)
        print(json.dumps(dict(depth=depth, k=1, count=len(front), nodes=budget.nodes)), flush=True)


if __name__ == '__main__':
    try:
        main()
    except (Undecided, MemoryError, RecursionError) as exc:
        print(f'UNDECIDED: {exc}', file=sys.stderr)
        raise SystemExit(3)
    except (AssertionError, RuntimeError, ValueError, OSError) as exc:
        print(f'FAILED: {exc}', file=sys.stderr)
        raise SystemExit(1)
