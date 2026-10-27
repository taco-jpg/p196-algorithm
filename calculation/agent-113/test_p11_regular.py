#!/usr/bin/env python3
"""Finite-word checks of exported regular center languages.

The independent oracle is Agent113's chronological whole-period tuple
transfer. No Python frontier above 50,000 states is requested. Matching
finite lengths does not prove language equality at every repetition count.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import subprocess
import sys

from center_reachability import CenterProblem, GEN, _Budget, _Limit
from test_center_reachability import source_controls, valid_witness

P11 = (10, '10100110011', '11100010000', '01000010000')
NATIVE_K1 = (35, 83, 243, 563, 755, 755)
NATIVE_K2 = (1225, 7577, 115033, 559193, 960601, 960601)
# Campaign Agents111/118's reported k3 values; only depth1 is re-enumerated here.
REPORTED_K3 = (42875, 657443, 34755075, 414911363, 752450435, 752450435)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


class Undecided(RuntimeError):
    """A resource limit prevented a complete comparison."""


class Language:
    def __init__(self, data):
        self.data = data
        self.depth = int(data['depth'])
        self.base, self.e, self.g, self.v = (data[key] for key in ('base', 'e', 'g', 'v'))
        self.order = data['order']
        self.p = len(self.e)
        require(2 <= self.base <= 62 and self.depth >= 0, 'bad base or depth')
        require(self.p and len(self.g) == len(self.v) == self.p, 'bad unit streams')
        require(all(bit in '01' for bits in (self.e, self.g, self.v) for bit in bits), 'nonbinary stream')
        require(self.g.count('1') == 2*self.v.count('1'), 'unbalanced unit streams')
        require(self.order and sum(map(len, self.order)) == self.p, 'bad segment lengths')
        flat = sum(self.order, [])
        require(flat == [(flat[0]+i) % self.p for i in range(self.p)], 'nonchronological segment order')
        require(all(self.v[segment[-1]] == '1' for segment in self.order), 'bad trim endpoints')
        require(len(self.order) == self.v.count('1'), 'missing trim endpoint')
        self.start_phase = flat[0]
        self.symbols, self.inverse = {}, {}
        for entry in data['alphabet']:
            label, kind, z = entry['label'], int(entry['type']), int(entry['z'])
            cfg = tuple(tuple(row) for row in entry['cfg'])
            require(0 <= kind < len(self.order) and len(cfg) == len(self.order[kind]), 'bad alphabet type')
            require(all(len(row) == 3 for row in cfg), 'bad local tuple shape')
            require(label not in self.symbols, 'duplicate alphabet label')
            key = kind, cfg, z
            require(key not in self.inverse, 'noninjective alphabet encoding')
            self.inverse[key] = label
            self.symbols[label] = key
        dfa = data['dfa']
        self.initial, self.final = int(dfa['initial']), dfa['final']
        require(all(flag in (0, 1) for flag in self.final), 'invalid DFA final flag')
        require(len(dfa['edges']) == len(self.final), 'DFA array mismatch')
        require(0 <= self.initial < len(self.final), 'bad initial state')
        self.edges = []
        for row in dfa['edges']:
            mapping = {}
            for label, target in row:
                require(label in self.symbols and 0 <= target < len(self.final), 'bad DFA edge')
                require(label not in mapping, 'export is not deterministic')
                mapping[label] = target
            self.edges.append(mapping)

    def accepts(self, word):
        state = self.initial
        for label in word:
            if label not in self.edges[state]:
                return False
            state = self.edges[state][label]
        return bool(self.final[state])

    def counts(self, max_k=3):
        active, out = {self.initial: 1}, []
        segments = len(self.order)
        for length in range(1, segments*max_k+1):
            nxt = defaultdict(int)
            for state, number in active.items():
                for target in self.edges[state].values():
                    nxt[target] += number
            active = nxt
            if length % segments == 0:
                out.append(sum(number for state, number in active.items() if self.final[state]))
        return out

    def encode(self, state, k):
        """A_r B_r is chronological: B's phases0,1 belong to unit r+1."""
        require(len(state) == self.p*k, 'bad whole-period tuple length')
        offset, word = self.start_phase, []
        for _ in range(k):
            for kind, times in enumerate(self.order):
                indices = tuple((offset+i) % len(state) for i in range(len(times)))
                require([index % self.p for index in indices] == times, 'phase alignment error')
                cfg = tuple(tuple(state[index][:3]) for index in indices)
                z = state[indices[-1]][3]
                key = kind, cfg, z
                require(key in self.inverse, f'oracle segment absent from alphabet: {key}')
                word.append(self.inverse[key])
                offset += len(times)
        return tuple(word)


def reference_frontier(language, k, cache):
    key = language.base, language.e, language.g, language.v, k
    if key not in cache:
        problem = CenterProblem(language.base, language.e*k, language.g*k, language.v*k)
        cache[key] = problem, [{problem.start}]
    problem, layers = cache[key]
    budget = _Budget(50000, 30)
    while len(layers) <= language.depth:
        j = len(layers)-1
        try:
            layers.append(problem._advance(layers[-1], (GEN,)*problem.p, j == 0, budget))
        except (_Limit, MemoryError, RecursionError) as exc:
            raise Undecided(f'global oracle k={k}, depth={j+1}: {exc}') from exc
    return layers[language.depth]


def generic_state_from_centers(base, es, gs, vs, centers, depth):
    result = []
    for t, center in enumerate(centers):
        width = len(center)
        e = int(es[t])
        def carry(index):
            return (sum(x*base**i for i, x in enumerate(center[:index])) + e) // base**index
        if depth == 0:
            row = e, 1-e, (base-1)*e if gs[t] == '1' else -1, -1
        else:
            value = sum(x*base**i for i, x in enumerate(center)) + e
            high = (value // base**(width-depth)) % base if gs[t] == '1' else -1
            z = centers[(t+1) % len(centers)][depth-1] if vs[t] == '1' else -1
            row = carry(depth), carry(width-depth), high, z
        result.append(row)
    return tuple(result)


def known_positive_check(language, controls):
    control = controls.get(language.base)
    if control is None or tuple(control[:3]) != (language.e, language.g, language.v):
        return 0
    depth, base = language.depth, language.base
    centers = [(base-1,)*depth + c + (base-1,)*depth for c in control[3]]
    valid_witness(base, language.e, language.g, language.v, centers, len(centers[0]))
    state = generic_state_from_centers(base, language.e, language.g, language.v, centers, depth)
    require(language.accepts(language.encode(state, 1)), 'known positive generic prefix was rejected')
    return 1


def check_dump(data, cache, controls):
    language = Language(data)
    counts = language.counts()
    unit = language.base, language.e, language.g, language.v
    if unit == P11 and 1 <= language.depth <= 6:
        j = language.depth-1
        expected = [NATIVE_K1[j], NATIVE_K2[j], REPORTED_K3[j]]
        require(counts == expected, f'finite native/report count mismatch: {counts} != {expected}')
    checked, members = [], 0
    for k in range(1, 4):
        if (k == 2 and language.depth > 2) or (k == 3 and language.depth > 1):
            continue
        frontier = reference_frontier(language, k, cache)
        words = {language.encode(state, k) for state in frontier}
        require(len(words) == len(frontier), 'segment encoding lost a global coordinate')
        require(counts[k-1] == len(frontier), f'global-oracle cardinality mismatch at k={k}')
        require(all(language.accepts(word) for word in words), f'global-oracle membership mismatch at k={k}')
        checked.append(k); members += len(words)
    positive = known_positive_check(language, controls)
    print(json.dumps(dict(status='PASS', depth=language.depth, base=language.base,
                          count_by_k=counts, exact_set_k=checked, memberships=members,
                          known_positive_generic_controls=positive,
                          dfa_states=len(language.edges)), sort_keys=True), flush=True)
    return members, positive


def engine_dump(binary, unit, depth, seconds):
    command = [str(binary), *map(str, unit), '--generic-only', '--depth', str(depth),
               '--dump-depth', str(depth), '--states', '1000000', '--edges', '20000000',
               '--ops', '1000000000', '--seconds', str(seconds), '--count-k', '3']
    try:
        run = subprocess.run(command, text=True, capture_output=True, timeout=seconds+10)
    except subprocess.TimeoutExpired as exc:
        raise Undecided('regular-language engine timed out') from exc
    events = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
    if any(event.get('status') == 'UNDECIDED' for event in events):
        raise Undecided(f'regular-language engine resource limit: {events[-1:]}')
    dumps = [event for event in events if event.get('event') == 'dump']
    require(run.returncode == 0 and len(dumps) == 1,
            f'engine did not produce complete dump: {events[-1:]}, stderr={run.stderr[-300:]}')
    require(dumps[0]['depth'] == depth, 'wrong engine dump depth')
    require(tuple(dumps[0][key] for key in ('base', 'e', 'g', 'v')) == tuple(unit),
            'engine dump does not describe the requested problem')
    return dumps[0]


def positive_tail(binary, base, control, seconds):
    es, gs, vs, _ = control
    command = [str(binary), str(base), es, gs, vs, '--depth', '12',
               '--states', '1000000', '--edges', '20000000', '--ops', '1000000000',
               '--seconds', str(seconds)]
    try:
        run = subprocess.run(command, text=True, capture_output=True, timeout=seconds+10)
    except subprocess.TimeoutExpired as exc:
        raise Undecided(f'base {base} production positive test timed out') from exc
    events = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
    require(events, 'production engine emitted no events')
    result = events[-1]
    if result.get('status') == 'UNDECIDED':
        raise Undecided(f'base {base} production positive test: {result}')
    require(run.returncode == 0 and result.get('status') == 'CENTER_LANGUAGE_ACCEPTS',
            f'known positive base {base} was not accepted: {result}')
    width, k = result['initial_width'], result['repetitions']
    require(isinstance(width, int) and width > 0 and isinstance(k, int) and k > 0,
            'invalid positive width or repetition count')
    problem = CenterProblem(base, es*k, gs*k, vs*k)
    witness = problem.fixed_width(width, cap=50000, seconds=30, witness=True)
    if witness['status'] == 'UNDECIDED':
        raise Undecided(f'base {base} independent positive reconstruction: {witness["reason"]}')
    require(witness['status'] == 'FEASIBLE', 'independent oracle contradicts positive tail')
    valid_witness(base, es*k, gs*k, vs*k, witness['centers'], width)
    branch = events[-2]
    require(branch.get('event') in ('short_width', 'tail') and branch['empty'] is False,
            'positive result lacks matching nonempty branch')
    print(json.dumps(dict(status='PASS', test='production_positive_tail', base=base,
                          initial_width=width, repetitions=k, branch=branch['event'],
                          depth=branch.get('depth'), parity=branch.get('parity'),
                          replayed_edges=len(witness['centers'])), sort_keys=True), flush=True)
    return branch['event']


def guard_tests(binary):
    invalid = [
        ('base', (1, *P11[1:]), []),
        ('nonbinary', (10, '20100110011', *P11[2:]), []),
        ('unbalanced', (*P11[:3], '0'*11), []),
        ('unit_length', (10, '0'*33, '11'+'0'*31, '1'+'0'*32), []),
        ('integer_range', P11, ['--depth', '4294967296']),
    ]
    limited = [('states', ['--states', '1']), ('edges', ['--edges', '1']),
               ('operations', ['--ops', '1']), ('depth', ['--depth', '1']),
               ('wall_time', ['--seconds', '1', '--states', '1000000',
                              '--edges', '20000000', '--ops', '1000000000'])]
    cases = [(name, unit, flags, 'INVALID', 2) for name, unit, flags in invalid]
    cases += [(name, P11, flags, 'UNDECIDED', 3) for name, flags in limited]
    for name, unit, flags, expected, code in cases:
        try:
            run = subprocess.run([str(binary), *map(str, unit), *flags],
                                 text=True, capture_output=True, timeout=15)
        except subprocess.TimeoutExpired as exc:
            raise Undecided(f'guard test {name} did not terminate') from exc
        events = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
        statuses = [event for event in events if 'status' in event]
        require(len(statuses) == 1 and events[-1] is statuses[0],
                f'guard {name} did not emit one unambiguous final status')
        require(run.returncode == code and statuses[0]['status'] == expected,
                f'guard {name} returned {run.returncode}, {statuses[0]}')
        print(json.dumps(dict(status='PASS', test='guard', case=name,
                              engine_status=expected, reason=statuses[0].get('reason')),
                         sort_keys=True), flush=True)
    return len(cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', type=Path)
    parser.add_argument('--depths', type=int, nargs='+', default=[1, 2, 5])
    parser.add_argument('--base', type=int, default=10)
    parser.add_argument('--e', default=P11[1]); parser.add_argument('--g', default=P11[2])
    parser.add_argument('--v', default=P11[3])
    parser.add_argument('--dump', action='append', default=[], help='JSONL path or - for stdin')
    parser.add_argument('--seconds', type=int, default=120)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--positive-tails', action='store_true',
                       help='run production acceptance and independent integer replay instead of generic dumps')
    modes.add_argument('--guards', action='store_true', help='check invalid inputs and fail-closed limits')
    parser.add_argument('--positive-bases', type=int, nargs='+', default=[2, 4, 8, 26])
    args = parser.parse_args()
    require(bool(args.engine or args.dump), 'provide --engine or --dump')
    controls, cache, comparisons, memberships, positive = source_controls(), {}, 0, 0, 0
    positive_tails, guards, branches = 0, 0, set()
    def check(data):
        nonlocal comparisons, memberships, positive
        number, controls_count = check_dump(data, cache, controls)
        comparisons += 1; memberships += number; positive += controls_count
    if args.guards:
        require(args.engine, '--guards requires --engine')
        guards = guard_tests(args.engine)
    elif args.positive_tails:
        require(args.engine, '--positive-tails requires --engine')
        for base in args.positive_bases:
            require(base in controls, 'no source certificate for requested positive base')
            branches.add(positive_tail(args.engine, base, controls[base], args.seconds))
            positive_tails += 1
    elif args.engine:
        for depth in args.depths:
            check(engine_dump(args.engine, (args.base, args.e, args.g, args.v), depth, args.seconds))
    for filename in args.dump:
        stream = sys.stdin if filename == '-' else open(filename)
        try:
            for line in stream:
                event = json.loads(line)
                if event.get('event') == 'dump':
                    check(event)
        finally:
            if stream is not sys.stdin:
                stream.close()
    require(comparisons+positive_tails+guards > 0, 'no language dump, positive tail or guard tested')
    print(f'FINITE LANGUAGE TESTS PASSED dumps={comparisons} memberships={memberships} '
          f'known_positive_generic_controls={positive} positive_tails={positive_tails} '
          f'positive_branches={",".join(sorted(branches))} guards={guards}; '
          'no arbitrary-k theorem follows from finite comparisons')


if __name__ == '__main__':
    try:
        main()
    except Undecided as exc:
        print(f'UNDECIDED: {exc}', file=sys.stderr)
        raise SystemExit(3)
    except (AssertionError, RuntimeError) as exc:
        print(f'FAILED: {exc}', file=sys.stderr)
        raise SystemExit(1)
