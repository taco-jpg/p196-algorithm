#!/usr/bin/env python3
"""Concrete soundness regressions and independent arithmetic controls.

Run from a full repository checkout after placing these files together:
python3 calculation/manager/two_run_checker_review/test_two_run_checker.py \
  --source reports/REPORT_213.md

The parent harness runs the same checks in normal and optimized Python and
requires byte-identical results.  Its checks remain enabled with python -O.
"""
import argparse
import ast
import json
import random
import subprocess
import sys
from pathlib import Path

import two_run_checker as checker


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def known_families(path):
    text = Path(path).read_text()
    code = text.split('```python', 1)[1].split('```', 1)[0]
    result = {}
    for node in ast.parse(code).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ('P11', 'P17', 'P26'):
                    result[int(target.id[1:])] = ast.literal_eval(node.value)
    require(set(result) == {11, 17, 26}, 'known control tables missing')
    return result


def worker(source):
    families = known_families(source)
    good = families[26]
    negative = [
        ('empty cycle', [], 10),
        ('nonsequence cycle', None, 10),
        ('string cycle', '12345', 10),
        ('zero base', good, 0),
        ('unary base', good, 1),
        ('negative base', good, -10),
        ('unsupported alphabet base', good, 37),
        ('boolean base', good, True),
        ('floating base', good, 26.0),
        ('string base', good, '26'),
        ('short phase', [('1', '2', '', '3')], 10),
        ('long phase', [('1', '2', '', '3', '4', '5')], 10),
        ('nonstring phase field', [('1', 2, '', '3', '4')], 10),
        ('empty leading block', [('', '2', '', '3', '4')], 10),
        ('empty trailing block', [('1', '2', '', '3', '')], 10),
        ('empty repeated digit', [('1', '', '', '3', '4')], 10),
        ('multiple repeated digits', [('1', '22', '', '3', '4')], 10),
        ('invalid symbol', [('1', '?', '', '3', '4')], 10),
        ('off-base repeated digit', [('1', 'A', '', '3', '4')], 10),
        ('off-base fixed digit', [('A', '2', '', '3', '4')], 10),
        ('invalid fixed middle digit', [('1', '2', 'A', '3', '4')], 10),
        ('leading zero', [('01', '2', '', '3', '4')], 10),
        ('missing outer mismatch', [('12', '3', '', '4', '21')], 10),
        ('false decimal seed 12', [('1', '0', '', '0', '2')], 10),
    ]
    for name, phases, base in negative:
        accepted, reason = checker.inspect(phases, base)
        require(accepted is False and bool(reason), f'false acceptance: {name}')
        require(checker.check(phases, base) is False, f'API disagreement: {name}')

    controls, mutations = 0, 0
    for base, phases in families.items():
        require(checker.check(phases, base) is True, f'positive base {base}')
        for i, phase in enumerate(phases):
            target = phases[(i + 1) % len(phases)]
            for n in (0, 1, 2, 3, 10, 100, 301):
                u, x, middle, y, v = phase
                w = u + x*n + middle + y*n + v
                tu, tx, tm, ty, tv = target
                m = n + int(i == len(phases)-1)
                following = tu + tx*m + tm + ty*m + tv
                require(int(w, base) + int(w[::-1], base) == int(following, base), 'integer control')
                require(w != w[::-1], 'positive control palindrome')
                controls += 1
            changed = list(phases)
            u, x, middle, y, v = phase
            digit = checker.ALPHABET[(checker.DIGIT[middle[0]] + 1) % base]
            changed[i] = (u, x, digit + middle[1:], y, v)
            require(checker.check(changed, base) is False, 'mutated center accepted')
            mutations += 1

    # Direct positional sums are independent of the closed coefficient formula.
    rng = random.Random(305)
    for _ in range(10000):
        base = rng.randint(2, 36)
        def digits(n):
            return ''.join(checker.ALPHABET[rng.randrange(base)] for _ in range(n))
        phase = (checker.ALPHABET[rng.randrange(1, base)] + digits(rng.randrange(5)),
                 digits(1), digits(rng.randrange(5)), digits(1), digits(1+rng.randrange(5)))
        n = rng.randrange(16)
        u, x, middle, y, v = phase
        w = u + x*n + middle + y*n + v
        t = base ** n
        for q, actual_word in ((phase, w), (checker._reversed_phase(phase), w[::-1])):
            a, b, c = checker._coefficients(q, base)
            actual = sum(checker.DIGIT[symbol] * base**j for j, symbol in enumerate(reversed(actual_word)))
            require(a*t*t + b*t + c == (base-1)*actual, 'coefficient identity')
    return {'negative_regressions': len(negative), 'known_positive_bases': sorted(families),
            'ordinary_integer_phase_controls': controls, 'rejected_center_mutations': mutations,
            'random_polynomial_cases_both_orders': 10000}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='reports/REPORT_213.md')
    parser.add_argument('--worker', action='store_true')
    args = parser.parse_args()
    source = str(Path(args.source).resolve())
    if args.worker:
        print(json.dumps(worker(source), sort_keys=True))
        return
    script = str(Path(__file__).resolve())
    command = [script, '--worker', '--source', source]
    normal = subprocess.run([sys.executable] + command, capture_output=True, text=True, check=True)
    optimized = subprocess.run([sys.executable, '-O'] + command, capture_output=True, text=True, check=True)
    require(normal.stdout == optimized.stdout, 'normal/optimized behavior differs')
    require(not normal.stderr and not optimized.stderr, 'unexpected stderr')
    print(normal.stdout.strip())
    print('NORMAL_AND_OPTIMIZED_IDENTICAL True')


if __name__ == '__main__':
    main()
