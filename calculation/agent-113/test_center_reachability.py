#!/usr/bin/env python3
"""Independent integer oracle and finite tests for cumulative center reachability.

The arithmetic oracle does not call either carry automaton. Existing Lean
sources supply control data only. All comparisons are COMPUTED regressions,
not a formal verification of either all-width decision procedure.
"""
from __future__ import annotations

import argparse
from itertools import product
import json
from pathlib import Path
import random
import re
import subprocess
import sys

from center_reachability import CenterProblem

ROOT = Path(__file__).resolve().parents[2]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def center_step(base, word, entry, overflow, trim):
    """Normalize a complete positional integer, then form the reflected sums."""
    width = len(word)
    if (not width or tuple(word) != tuple(reversed(word)) or
            any(not isinstance(digit, int) or not 0 <= digit <= 2*base-2 for digit in word)):
        return None
    value = sum(digit * base**index for index, digit in enumerate(word)) + entry
    carry, value = divmod(value, base**width)
    if carry != 1-entry:
        return None
    digits = []
    for _ in word:
        value, digit = divmod(value, base)
        digits.append(digit)
    if overflow:
        digits.append((base-1)*entry)
    raw = tuple(a+b for a, b in zip(digits, reversed(digits)))
    if len(raw) <= 2*trim:
        return None
    if any(digit != base-1 for digit in raw[:trim] + raw[len(raw)-trim:]):
        return None
    return raw[trim:len(raw)-trim]


def valid_witness(base, es, gs, vs, centers, width):
    require(len(centers) == len(es), 'incomplete witness phases')
    require(len(centers[0]) == width, 'incorrect initial witness width')
    for t, center in enumerate(centers):
        actual = center_step(base, center, int(es[t]), int(gs[t]), int(vs[t]))
        expected = tuple(centers[(t+1) % len(es)])
        require(actual == expected, f'invalid integer witness at phase {t}')


def check_result(result, base, es, gs, vs, complete=True):
    status = result.get('status')
    require(status in ('FEASIBLE', 'EXHAUSTED', 'UNDECIDED'), f'bad status: {result}')
    if complete:
        require(status != 'UNDECIDED', f'incomplete finite test: {result}')
    if status == 'FEASIBLE':
        require('centers' in result, 'requested positive witness missing')
        valid_witness(base, es, gs, vs, result['centers'], result['initial_width'])
    return status


def brute_fixed(base, es, gs, vs, width):
    tested, possible = 0, False
    for half in product(range(2*base-1), repeat=(width+1)//2):
        initial = half + half[:width//2][::-1]
        word = initial
        tested += 1
        for e, g, v in zip(es, gs, vs):
            word = center_step(base, word, int(e), int(g), int(v))
            if word is None:
                break
        possible |= word == initial
    return possible, tested


def source_controls():
    """Read the original eight Lean-source certificates; no mirror imports."""
    root = ROOT / 'lean/P196'
    paths = [root/'Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean',
             root/'Agent213KnownBaseMechanisms/KnownBases.lean']
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
            base, es, gs, vs, centers = int(match[1]), '', '', '', []
            for fields in re.findall(r'⟨(.*?)⟩', match[2], re.S):
                tokens = re.findall(r'\[[^\]]*\]|[A-Za-z_]\w*|\d+', fields)
                require(len(tokens) == 6, 'unexpected Lean source edge')
                exterior, center, _, next_center = map(word, tokens[:4])
                e = sum(x*base**i for i, x in enumerate(exterior)) // base**len(exterior)
                g = (sum(x*base**i for i, x in enumerate(reversed(exterior))) + 1-e) // base**len(exterior)
                v = int(tokens[5])
                require(center_step(base, center, e, g, v) == next_center, 'source edge failed integer replay')
                es += str(e); gs += str(g); vs += str(v); centers.append(center)
            valid_witness(base, es, gs, vs, centers, len(centers[0]))
            controls[base] = (es, gs, vs, centers)
    require(set(controls) == {2, 4, 8, 11, 16, 17, 26, 32}, 'missing original source certificates')
    return controls


def bounded_tests():
    streams = cases = words = witnesses = 0
    for base in (2, 3, 4):
        for period in (1, 2, 3):
            bits = [''.join(map(str, row)) for row in product((0, 1), repeat=period)]
            for es, gs, vs in product(bits, repeat=3):
                if gs.count('1') != 2*vs.count('1'):
                    continue
                problem = CenterProblem(base, es, gs, vs)
                streams += 1
                for width in range(1, 5):
                    expected, count = brute_fixed(base, es, gs, vs, width)
                    result = problem.fixed_width(width, witness=True)
                    status = check_result(result, base, es, gs, vs)
                    require((status == 'FEASIBLE') == expected,
                            f'integer disagreement: {(base,es,gs,vs,width,expected,result)}')
                    witnesses += status == 'FEASIBLE'
                    cases += 1
                    words += count
    print(f'bounded streams={streams} fixed_cases={cases} initial_words={words} witnesses={witnesses} PASS')


def invoke(command, timeout=30):
    try:
        return subprocess.run(list(map(str, command)), text=True, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f'UNDECIDED: external test timed out: {command}') from exc


def old_all_widths(binary, base, es, gs, vs):
    command = [binary, base, es, gs, 1, 1, '-v', vs, '-allm', '-w', '-cap', 50000]
    run = invoke(command)
    require(run.returncode == 0, f'baseline failure: {run.stderr[-1000:]}')
    statuses = re.findall(r'\bstatus=(\w+)', run.stdout)
    require(len(statuses) == 1, 'missing baseline completion status')
    witnesses = 0
    for line in run.stdout.splitlines():
        if not line.startswith('FEASIBLE'):
            continue
        width = int(re.search(r'\bm0=(\d+)', line)[1])
        rows = re.findall(r' C(\d+)=\[([^\]]*)\]', line)
        require([int(index) for index, _ in rows] == list(range(len(es))), 'baseline witness indices')
        centers = [tuple(map(int, value.split(','))) if value else () for _, value in rows]
        valid_witness(base, es, gs, vs, centers, width)
        witnesses += 1
    return {'none': 'EXHAUSTED', 'hit': 'FEASIBLE', 'capped': 'UNDECIDED',
            'noperiod': 'UNDECIDED'}[statuses[0]], witnesses


def primary_all_widths(binary, base, es, gs, vs):
    run = invoke([binary, base, es, gs, vs, '--cap', 50000,
                  '--seconds', 30, '--memory-mb', 2048], timeout=35)
    require(run.returncode in (0, 3), f'primary failure: {run.stderr[-1000:]}')
    result = json.loads(run.stdout)
    status = {'NONE': 'EXHAUSTED', 'FEASIBLE': 'FEASIBLE',
              'UNDECIDED': 'UNDECIDED'}.get(result.get('status'))
    require(status is not None, f'unknown primary status: {result}')
    if status == 'FEASIBLE':
        valid_witness(base, es, gs, vs, result['C'], result['m0'])
    return status, int(status == 'FEASIBLE')


def all_width_tests(baseline, primary, count):
    rng = random.Random(113)
    tested = witnesses = skipped = primary_cases = 0
    while tested < count:
        base, period = rng.choice((2, 3, 4, 6, 10, 11)), rng.randint(2, 6)
        es = ''.join(rng.choice('01') for _ in range(period))
        gs = ''.join(rng.choice('01') for _ in range(period))
        weight = gs.count('1')
        if not weight or weight % 2:
            continue
        chosen = set(rng.sample(range(period), weight//2))
        vs = ''.join('1' if t in chosen else '0' for t in range(period))
        expected, old_witnesses = old_all_widths(baseline, base, es, gs, vs)
        if expected == 'UNDECIDED':
            skipped += 1
            require(skipped < 20, 'too many incomplete baseline cases')
            continue
        result = CenterProblem(base, es, gs, vs).all_widths(witness=True)
        actual = check_result(result, base, es, gs, vs)
        require(actual == expected, f'all-width baseline disagreement: {(base,es,gs,vs,result,expected)}')
        witnesses += old_witnesses + (actual == 'FEASIBLE')
        if primary:
            primary_status, primary_witnesses = primary_all_widths(primary, base, es, gs, vs)
            require(primary_status == actual, f'primary disagreement: {(base,es,gs,vs,actual,primary_status)}')
            witnesses += primary_witnesses
            primary_cases += 1
        tested += 1
    print(f'all_widths completed={tested} baseline_undecided_skipped={skipped} primary_comparisons={primary_cases} witnesses={witnesses} PASS')


def zero_overflow_tests(baseline):
    cases = witnesses = 0
    for base in (2, 3, 4):
        for period in (1, 2, 3):
            gs = vs = '0'*period
            for row in product('01', repeat=period):
                es = ''.join(row)
                expected, old_witnesses = old_all_widths(baseline, base, es, gs, vs)
                require(expected != 'UNDECIDED', 'zero-overflow baseline incomplete')
                result = CenterProblem(base, es, gs, vs).all_widths(witness=True)
                status = check_result(result, base, es, gs, vs)
                require(status == expected, f'zero-overflow disagreement: {(base,es,result,expected)}')
                witnesses += old_witnesses + (status == 'FEASIBLE')
                cases += 1
    print(f'zero_overflow_allwidth_cases={cases} witnesses={witnesses} PASS')


def positive_tests():
    controls = source_controls()
    cases = all_width_cases = 0
    for base, (es, gs, vs, centers) in sorted(controls.items()):
        problem = CenterProblem(base, es, gs, vs)
        result = problem.fixed_width(len(centers[0]), witness=True)
        require(check_result(result, base, es, gs, vs) == 'FEASIBLE', f'lost source positive base{base}')
        all_result = problem.all_widths(witness=True)
        require(check_result(all_result, base, es, gs, vs) == 'FEASIBLE', f'lost all-width source base{base}')
        cases += 1; all_width_cases += 1
        print(f'positive source_base={base} fixed_width={len(centers[0])} all_width_witness={all_result["initial_width"]} PASS')
    # Separate newly published control; the original eight-source count stays 56.
    base, es, gs, vs = 20, '10100101', '10001000', '00100000'
    problem = CenterProblem(base, es, gs, vs)
    result = problem.fixed_width(27, witness=True)
    require(check_result(result, base, es, gs, vs) == 'FEASIBLE', 'base20 width27 control lost')
    result = problem.all_widths(witness=True)
    require(check_result(result, base, es, gs, vs) == 'FEASIBLE', 'base20 all-width control lost')
    cases += 1; all_width_cases += 1
    print(f'positive base20 fixed_width=27 all_width_witness={result["initial_width"]} PASS')
    print(f'positive fixed_cases={cases} all_width_cases={all_width_cases} original_source_edges={sum(len(x[3]) for x in controls.values())} PASS')


def resource_tests():
    problem = CenterProblem(10, '10100110011', '11100010000', '11000000000')
    for options in (dict(cap=1), dict(seconds=1e-9)):
        result = problem.all_widths(witness=True, **options)
        require(result['status'] == 'UNDECIDED', f'resource guard mislabels: {result}')
    invalid = [(1, '0', '0', '0'), (63, '0', '0', '0'),
               (2, '', '', ''), (2, 'x', '0', '0'),
               (2, '0', '01', '0'), (2, '00', '11', '00'),
               (2, '0'*129, '0'*129, '0'*129)]
    for args in invalid:
        try:
            CenterProblem(*args)
        except ValueError:
            pass
        else:
            raise AssertionError(f'invalid problem accepted: {args}')
    print(f'resource_undecided=2 invalid_inputs={len(invalid)} PASS')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--primary', type=Path)
    parser.add_argument('--allm-cases', type=int, default=32)
    parser.add_argument('--only', choices=('bounded', 'allm', 'positive', 'guards', 'all'), default='all')
    args = parser.parse_args()
    if args.only in ('all', 'bounded'):
        bounded_tests()
    if args.only in ('all', 'allm') and args.baseline:
        all_width_tests(args.baseline, args.primary, args.allm_cases)
        zero_overflow_tests(args.baseline)
    elif args.only == 'allm':
        parser.error('--only allm requires --baseline')
    if args.only in ('all', 'positive'):
        positive_tests()
    if args.only in ('all', 'guards'):
        resource_tests()
    print('ALL TESTS PASSED (finite COMPUTED regression; no new Lean theorem)')


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, RuntimeError) as exc:
        print(f'FAILED: {exc}', file=sys.stderr)
        raise SystemExit(1)
