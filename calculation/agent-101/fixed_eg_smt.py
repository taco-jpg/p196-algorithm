#!/usr/bin/env python3
"""Independent exact bounded exterior solver using bit-vector normalization.

The circuit uses digit comparisons/subtractions, not free carry variables or
the CP-SAT linear equations. A SAT result is an exterior only, never a complete
neutral-band certificate. Every returned exterior is replayed as whole integers.
"""
import argparse
import json
import math
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def valid_request(base, es, gs, width, seconds, memory_mb, fixed_words=None):
    if not isinstance(base, int) or not 2 <= base <= 62:
        return 'supported bases are 2..62'
    if (not isinstance(es, str) or not isinstance(gs, str) or not 1 <= len(es) <= 64
            or len(es) != len(gs) or set(es+gs)-set('01')):
        return 'equal nonempty binary streams of length at most64 required'
    if not isinstance(width, int) or not 1 <= width <= 256:
        return 'supported positive widths are 1..256'
    if not isinstance(seconds, (int, float)) or not math.isfinite(seconds) or not 0 < seconds <= 1500:
        return 'wall budget must lie in (0,1500] seconds'
    if not isinstance(memory_mb, int) or not 64 <= memory_mb <= 8192:
        return 'address-space budget must be 64..8192 MiB'
    if fixed_words is not None:
        if (len(fixed_words) != len(es) or any(len(w) != width for w in fixed_words)
                or any(type(a) is not int or not 0 <= a <= 2*base-2 for w in fixed_words for a in w)):
            return 'fixed fixture must contain one complete bounded word per phase'
    return None


def integer_norm(base, word, carry):
    value = carry + sum(a*base**j for j, a in enumerate(word))
    digits = []
    for _ in word:
        value, digit = divmod(value, base)
        digits.append(digit)
    return digits, value


def replay(base, es, gs, words):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror
    for t, B in enumerate(words):
        if not B or B[0] == 0 or any(type(x) is not int or not 0 <= x <= 2*base-2 for x in B):
            raise ValueError('invalid exterior witness domain')
        d, e = integer_norm(base, B, 0)
        r, g = integer_norm(base, B[::-1], 1-e)
        if (e, g) != (int(es[t]), int(gs[t])):
            raise ValueError('witness does not emit requested streams')
        left, right = (d+[(base-1)*(1-e)], [1]+r[::-1]) if g else (d, r[::-1])
        raw = [a+b for a, b in zip(left, right)]
        if raw != words[(t+1) % len(words)] + [base-1]*g:
            raise ValueError('integer witness transition fails')
        C = [base] if e == 0 else [0]
        if (not mirror.hyp(base, B, C) or mirror.nextB(base, B, C) != raw
                or mirror.gam(base, B, C) != g):
            raise ValueError('Python mirror witness transition fails')
    return {'whole_integer': True, 'python_mirror': True}


def worker(request):
    started = time.monotonic()
    base, es, gs, width = [request[k] for k in ('base', 'e', 'g', 'width')]
    seconds, memory_mb = request['seconds'], request['memory_mb']
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    requested = memory_mb*1024*1024
    if soft != resource.RLIM_INFINITY:
        requested = min(requested, soft)
    if hard != resource.RLIM_INFINITY:
        requested = min(requested, hard)
    resource.setrlimit(resource.RLIMIT_AS, (requested, hard))
    import z3
    period = len(es)
    bits = (2*base-1).bit_length()
    number = lambda x: z3.BitVecVal(x, bits)
    B = [[z3.BitVec(f'B_{t}_{j}', bits) for j in range(width)] for t in range(period)]
    solver = z3.SolverFor('QF_BV')

    def normalize(word, entering):
        carry = number(entering)
        digits = []
        for coefficient in word:
            total = coefficient+carry
            large = z3.UGE(total, number(base))
            digits.append(z3.If(large, total-number(base), total))
            carry = z3.If(large, number(1), number(0))
        return digits, carry

    for t in range(period):
        for variable in B[t]:
            solver.add(z3.ULE(variable, number(2*base-2)))
        solver.add(z3.UGT(B[t][0], number(0)))
        d, low_exit = normalize(B[t], 0)
        r, high_exit = normalize(B[t][::-1], 1-int(es[t]))
        solver.add(low_exit == number(int(es[t])), high_exit == number(int(gs[t])))
        if gs[t] == '1':
            left, right = d+[number((base-1)*(1-int(es[t])))], [number(1)]+r[::-1]
        else:
            left, right = d, r[::-1]
        for j, (x, y) in enumerate(zip(left, right)):
            target = B[(t+1) % period][j] if j < width else number(base-1)
            solver.add(x+y == target)
    if request.get('fixed_words') is not None:
        for t in range(period):
            for j in range(width):
                solver.add(B[t][j] == number(request['fixed_words'][t][j]))
    remaining = seconds-(time.monotonic()-started)
    common = {'base': base, 'e': es, 'g': gs, 'width': width, 'period': period,
              'backend': 'z3_qfbv', 'z3_version': z3.get_version_string(), 'bits_per_coefficient': bits,
              'fixed_words': request.get('fixed_words') is not None}
    if remaining <= 0:
        return dict(common, status='UNDECIDED', reason='construction_timeout')
    solver.set(timeout=max(1, int(remaining*1000)))
    result = solver.check()
    common.update(solver_status=str(result), seconds=time.monotonic()-started,
                  rss_mb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
    if result == z3.unsat:
        if common['fixed_words']:
            return dict(common, status='UNSAT_BOUNDED', scope='additionally pinned coefficient fixture')
        return dict(common, status='UNSAT_BOUNDED', all_widths_at_most=width,
                    scope='fixed E/G, all exterior phase widths at most W, arbitrary natural trims')
    if result != z3.sat:
        return dict(common, status='UNDECIDED', reason=solver.reason_unknown())
    model = solver.model()
    words = [[model.eval(x, model_completion=True).as_long() for x in row] for row in B]
    checks = replay(base, es, gs, words)
    return dict(common, status='SAT_B_ONLY', B=words, replay=checks, actual_certificate=False)


def solve(base, es, gs, width, seconds=60, memory_mb=1024, fixed_words=None):
    error = valid_request(base, es, gs, width, seconds, memory_mb, fixed_words)
    if error:
        return {'status': 'UNDECIDED', 'reason': 'invalid_or_unsupported_input', 'detail': error}
    request = {'base': base, 'e': es, 'g': gs, 'width': width, 'seconds': seconds,
               'memory_mb': memory_mb, 'fixed_words': fixed_words}
    try:
        process = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker',
                                  json.dumps(request)], capture_output=True, text=True,
                                 timeout=seconds+5)
    except subprocess.TimeoutExpired:
        return {'status': 'UNDECIDED', 'reason': 'supervisor_wall_timeout'}
    if process.returncode != 0:
        return {'status': 'UNDECIDED', 'reason': 'worker_failure', 'worker_exit': process.returncode,
                'detail': process.stderr[-500:]}
    try:
        result = json.loads(process.stdout)
    except ValueError:
        return {'status': 'UNDECIDED', 'reason': 'malformed_worker_output'}
    if result.get('status') not in ('SAT_B_ONLY', 'UNSAT_BOUNDED', 'UNDECIDED'):
        return {'status': 'UNDECIDED', 'reason': 'unknown_worker_status'}
    return result


def main():
    if len(sys.argv) == 3 and sys.argv[1] == '--worker':
        try:
            request = json.loads(sys.argv[2])
            error = valid_request(request['base'], request['e'], request['g'], request['width'],
                                  request['seconds'], request['memory_mb'], request.get('fixed_words'))
            result = {'status': 'UNDECIDED', 'reason': error} if error else worker(request)
        except (MemoryError, ImportError, RuntimeError, ValueError, OSError) as error:
            result = {'status': 'UNDECIDED', 'reason': type(error).__name__, 'detail': str(error)[-300:]}
        print(json.dumps(result, sort_keys=True), flush=True)
        return 0
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('base', type=int)
    parser.add_argument('e')
    parser.add_argument('g')
    parser.add_argument('width', type=int)
    parser.add_argument('--seconds', type=float, default=60)
    parser.add_argument('--memory-mb', type=int, default=1024)
    args = parser.parse_args()
    result = solve(args.base, args.e, args.g, args.width, args.seconds, args.memory_mb)
    print(json.dumps(result, sort_keys=True), flush=True)
    return 3 if result['status'] == 'UNDECIDED' else 0


if __name__ == '__main__':
    sys.exit(main())
