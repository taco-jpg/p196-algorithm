#!/usr/bin/env python3
"""Exact bounded exterior cycles with prescribed entry and overflow streams.

Usage: fixed_eg_cpsat.py BASE E G WIDTH [--seconds 60] [--memory-mb 1024]
                                      [--workers 1] [--charge] [--tables]
Every phase has WIDTH coefficients; overflow removes exactly one neutral
coefficient (u=g). SAT_B_ONLY is an exterior witness, not a cycle certificate.
Only CP-SAT INFEASIBLE yields UNSAT_BOUNDED. All other unsuccessful runs are
UNDECIDED. A worker subprocess has an address-space limit and a wall supervisor;
--seconds includes worker imports and model construction, with 3 seconds of
supervisor grace. Supported: base 2..1000000, period <=4096, P*WIDTH <=262144.

Importable API: solve(base, e, g, width, seconds=60, memory_mb=1024,
                      workers=1, fixed_words=None, charge=False,
                      tables=False) -> dict.
fixed_words, if supplied, must contain P already padded words of exact WIDTH.
Optional charge pruning uses the existing cycle invariant modulo base+1;
it is omitted explicitly when G has no positive overflow.
Optional tables replace normalization equations by their complete truth tables;
table encoding is supported only through base 62. Both options default off.
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


class InputError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InputError(message)


def validate(base, e, g, width, seconds, memory_mb, workers, fixed_words, charge=False,
             tables=False):
    require(type(base) is int and 2 <= base <= 1000000, 'base must be 2..1000000')
    require(type(width) is int and width >= 1, 'width must be a positive integer')
    require(isinstance(e, str) and isinstance(g, str) and len(e) == len(g)
            and 1 <= len(e) <= 4096 and set(e+g) <= {'0', '1'},
            'E and G must be nonempty equal-length bit strings of period <=4096')
    require(len(e)*width <= 262144, 'model exceeds 262144 coefficient cells')
    require(type(seconds) in (int, float) and math.isfinite(seconds)
            and 0 < seconds <= 1500, 'seconds must be in (0,1500]')
    require(type(memory_mb) is int and 1 <= memory_mb <= 8192,
            'memory budget must be 1..8192 MiB')
    require(type(workers) is int and 1 <= workers <= 4, 'workers must be 1..4')
    require(type(charge) is bool, 'charge must be a boolean')
    require(type(tables) is bool, 'tables must be a boolean')
    require(not tables or base <= 62, 'table encoding supports bases only through 62')
    if fixed_words is not None:
        require(isinstance(fixed_words, (list, tuple)) and len(fixed_words) == len(e),
                'fixed_words must contain one padded word per phase')
        for word in fixed_words:
            require(isinstance(word, (list, tuple)) and len(word) == width,
                    'fixed word has the wrong padded width')
            require(all(type(x) is int and 0 <= x <= 2*base-2 for x in word)
                    and word[0] >= 1, 'fixed word is outside the exterior domain')


def integer_normalize(base, word, entry):
    # Independent positional-integer replay, not the model's column equations.
    value = entry + sum(x*base**j for j, x in enumerate(word))
    digits = []
    for _ in word:
        value, digit = divmod(value, base)
        digits.append(digit)
    return digits, value


def replay(base, e, g, width, words):
    validate(base, e, g, width, 1, 1, 1, words)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror
    for phase, source in enumerate(words):
        entry, growth = int(e[phase]), int(g[phase])
        target = words[(phase+1) % len(words)]
        left, actual_entry = integer_normalize(base, source, 0)
        reverse, actual_growth = integer_normalize(base, source[::-1], 1-entry)
        require(actual_entry == entry and actual_growth == growth,
                f'integer replay carry mismatch at phase {phase}')
        if growth:
            left = left+[(base-1)*(1-entry)]
            right = [1]+reverse[::-1]
        else:
            right = reverse[::-1]
        raw = [a+b for a, b in zip(left, right)]
        expected = target+[base-1]*growth
        require(raw == expected, f'integer replay transition mismatch at phase {phase}')
        # This one-coefficient auxiliary center forces e2=1-e; it does not
        # purport to form a center cycle or the user's target center word.
        auxiliary_center = [base] if entry == 0 else [0]
        require(mirror.hyp(base, source, auxiliary_center)
                and mirror.e1(base, source) == entry
                and mirror.gam(base, source, auxiliary_center) == growth
                and mirror.nextB(base, source, auxiliary_center) == expected,
                f'Python mirror replay mismatch at phase {phase}')
    return {'whole_integer': True, 'python_mirror': True}


def worker_model(payload, started):
    from ortools.sat.python import cp_model
    import ortools
    base, e, g, width = (payload[k] for k in ('base', 'e', 'g', 'width'))
    period = len(e)
    model = cp_model.CpModel()
    normalization_rows = None
    if payload['tables']:
        # Every coefficient and both incoming carry bits occur exactly once.
        # Row order: a, L_in, H_in, d, r, L_out, H_out (76 rows in base 10).
        normalization_rows = [(a, li, hi, (a+li) % base, (a+hi) % base,
                               (a+li)//base, (a+hi)//base)
                              for a in range(2*base-1)
                              for li in (0, 1) for hi in (0, 1)]
    coefficients = [[model.NewIntVar(0, 2*base-2, f'a_{t}_{j}')
                     for j in range(width)] for t in range(period)]
    for t, source in enumerate(coefficients):
        entry, growth = int(e[t]), int(g[t])
        model.Add(source[0] >= 1)
        if payload['charge'] and '1' in g:
            # Existing invariant, not a discovery here: Agent107 PR363 gives
            # the uniform-width charge relation; Agent108 PR360 formalizes
            # the decimal case, and Agent104 supplies positive overflow.
            # For any base, a cycle containing overflow has alt(B)=(-1)^W
            # modulo base+1. Use an integer quotient, not signed remainder.
            quotient = model.NewIntVar(-2*base*width, 2*base*width, f'charge_{t}')
            alternating = sum((1 if j % 2 == 0 else -1)*source[j]
                              for j in range(width))
            model.Add(alternating == (1 if width % 2 == 0 else -1)
                      + (base+1)*quotient)
        forward = [model.NewBoolVar(f'L_{t}_{j}') for j in range(width+1)]
        inward = [model.NewBoolVar(f'H_{t}_{j}') for j in range(width+1)]
        low = [model.NewIntVar(0, base-1, f'd_{t}_{j}') for j in range(width)]
        high = [model.NewIntVar(0, base-1, f'r_{t}_{j}') for j in range(width)]
        model.Add(forward[0] == 0)
        model.Add(forward[width] == entry)
        model.Add(inward[width] == 1-entry)
        model.Add(inward[0] == growth)
        for j in range(width):
            if normalization_rows is not None:
                model.AddAllowedAssignments(
                    [source[j], forward[j], inward[j+1], low[j], high[j],
                     forward[j+1], inward[j]], normalization_rows)
            else:
                model.Add(source[j]+forward[j] == low[j]+base*forward[j+1])
                model.Add(source[j]+inward[j+1] == high[j]+base*inward[j])
        target = coefficients[(t+1) % period]
        if growth:
            model.Add(target[0] == low[0]+1)
            for j in range(1, width):
                model.Add(target[j] == low[j]+high[j-1])
            model.Add((base-1)*(1-entry)+high[width-1] == base-1)
        else:
            for j in range(width):
                model.Add(target[j] == low[j]+high[j])
        if payload['fixed_words'] is not None:
            for j, value in enumerate(payload['fixed_words'][t]):
                model.Add(source[j] == value)
    validation = model.Validate()
    if validation:
        return {'status': 'UNDECIDED', 'reason': 'model_invalid',
                'detail': validation[:400]}
    remaining = payload['seconds']-(time.monotonic()-started)
    if remaining <= 0:
        return {'status': 'UNDECIDED', 'reason': 'wall_budget_during_construction'}
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = remaining
    solver.parameters.num_search_workers = payload['workers']
    solver.parameters.log_search_progress = False
    solver.parameters.log_to_stdout = False
    status = solver.Solve(model)
    result = {'solver_status': solver.StatusName(status),
              'ortools_version': ortools.__version__,
              'solver_seconds': solver.WallTime(),
              'conflicts': solver.NumConflicts(), 'branches': solver.NumBranches()}
    if status == cp_model.INFEASIBLE:
        result['status'] = 'UNSAT_BOUNDED'
    elif status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        words = [[solver.Value(x) for x in row] for row in coefficients]
        try:
            result['replay'] = replay(base, e, g, width, words)
        except Exception as error:
            return {'status': 'UNDECIDED', 'reason': 'witness_replay_failed',
                    'detail': str(error)[:400]}
        result.update(status='SAT_B_ONLY', B=words, certificate=False)
    else:
        result.update(status='UNDECIDED', reason='solver_did_not_decide')
    return result


def worker_main(seconds, memory_mb):
    started = time.monotonic()
    try:
        validate(2, '0', '0', 1, seconds, memory_mb, 1, None)
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        limit = memory_mb*1024*1024
        if soft != resource.RLIM_INFINITY:
            limit = min(limit, soft)
        if hard != resource.RLIM_INFINITY:
            limit = min(limit, hard)
        resource.setrlimit(resource.RLIMIT_AS, (limit, hard))
        raw = sys.stdin.buffer.read(16*1024*1024+1)
        require(len(raw) <= 16*1024*1024, 'worker payload exceeds 16 MiB')
        payload = json.loads(raw)
        require(payload['seconds'] == seconds and payload['memory_mb'] == memory_mb,
                'worker resource limits disagree')
        validate(**payload)
        result = worker_model(payload, started)
    except MemoryError:
        os.write(1, b'{"status":"UNDECIDED","reason":"memory_limit"}\n')
        return 0
    except ImportError as error:
        result = {'status': 'UNDECIDED', 'reason': 'dependency_unavailable',
                  'detail': str(error)[:400]}
    except Exception as error:
        result = {'status': 'UNDECIDED', 'reason': 'worker_error',
                  'detail': str(error)[:400]}
    print(json.dumps(result, separators=(',', ':')))
    return 0


def solve(base, e, g, width, seconds=60, memory_mb=1024, workers=1, fixed_words=None,
          charge=False, tables=False):
    started = time.monotonic()
    try:
        validate(base, e, g, width, seconds, memory_mb, workers, fixed_words, charge, tables)
    except (InputError, OverflowError, TypeError) as error:
        return {'status': 'UNDECIDED', 'reason': 'invalid_or_unsupported_input',
                'detail': str(error), 'charge_pruning': False, 'table_encoding': False}
    payload = dict(base=base, e=e, g=g, width=width, seconds=seconds,
                   memory_mb=memory_mb, workers=workers, fixed_words=fixed_words,
                   charge=charge, tables=tables)
    environment = os.environ.copy()
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS'):
        environment[key] = '1'
    command = [sys.executable, str(Path(__file__).resolve()), '--_worker',
               str(seconds), str(memory_mb)]
    try:
        process = subprocess.run(command, input=json.dumps(payload), text=True,
                                 capture_output=True, timeout=seconds+3,
                                 env=environment, check=False)
        if process.returncode != 0:
            result = {'status': 'UNDECIDED', 'reason': 'worker_terminated',
                      'returncode': process.returncode,
                      'detail': process.stderr[-400:]}
        else:
            result = json.loads(process.stdout)
            if result.get('status') not in ('SAT_B_ONLY', 'UNSAT_BOUNDED', 'UNDECIDED'):
                raise ValueError('worker returned an invalid status')
    except subprocess.TimeoutExpired:
        result = {'status': 'UNDECIDED', 'reason': 'supervisor_wall_timeout'}
    except (OSError, ValueError, TypeError) as error:
        result = {'status': 'UNDECIDED', 'reason': 'worker_protocol_error',
                  'detail': str(error)[:400]}
    result.update(base=base, e=e, g=g, u=g, width=width, period=len(e),
                  fixed_words=fixed_words is not None,
                  charge_pruning=charge and '1' in g,
                  table_encoding=tables,
                  scope=('fixed E/G, constant padded exterior width W, u=g'
                         + (', coefficients additionally pinned' if fixed_words is not None else '')),
                  elapsed_seconds=round(time.monotonic()-started, 6))
    if charge and '1' not in g:
        result['charge_pruning_note'] = 'omitted: G has no positive overflow'
    return result


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise InputError(message)


def main():
    if len(sys.argv) == 4 and sys.argv[1] == '--_worker':
        try:
            return worker_main(float(sys.argv[2]), int(sys.argv[3]))
        except (ValueError, OverflowError) as error:
            print(json.dumps({'status': 'UNDECIDED',
                              'reason': 'invalid_or_unsupported_input', 'detail': str(error),
                              'charge_pruning': False, 'table_encoding': False}))
            return 2
    parser = Parser(description=__doc__)
    parser.add_argument('base', type=int)
    parser.add_argument('e')
    parser.add_argument('g')
    parser.add_argument('width', type=int)
    parser.add_argument('--seconds', type=float, default=60)
    parser.add_argument('--memory-mb', type=int, default=1024)
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--charge', action='store_true')
    parser.add_argument('--tables', action='store_true')
    try:
        arguments = parser.parse_args()
        result = solve(**vars(arguments))
    except (InputError, ValueError, OverflowError) as error:
        result = {'status': 'UNDECIDED', 'reason': 'invalid_or_unsupported_input',
                  'detail': str(error)}
    result.setdefault('charge_pruning', False)
    result.setdefault('table_encoding', False)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] in ('SAT_B_ONLY', 'UNSAT_BOUNDED') else 2


if __name__ == '__main__':
    sys.exit(main())
