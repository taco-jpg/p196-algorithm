"""Finite CEGIS for a 600-weight exact-previous-pair positive invariant.

States are START and the 19 possible previous pair sums.  Safety against the
complete palindrome-predecessor language is imposed by exact graph potentials.
Closure is conditional: S(w)>0 implies S(T(w))>0.  Finite sample candidates
are explicitly NOT certificates; an independent all-length check is required.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import lcm
from pathlib import Path
import argparse
import json
import time
import z3
import creative_regular_invariant as r

MEMORY_STATES = 20
TRANSITION_WEIGHTS = MEMORY_STATES * 19
WEIGHTS = TRANSITION_WEIGHTS + MEMORY_STATES * 11

def state(q):
    return q + 1

def features(word):
    pairs, center = word
    previous, result = 0, Counter()
    for q in pairs:
        result[19 * previous + q] += 1
        previous = state(q)
    result[TRANSITION_WEIGHTS + 11 * previous + r.terminal_index(center)] += 1
    return tuple(sorted(result.items()))

def row(weights, feature):
    return z3.Sum([weights[j] * coefficient for j, coefficient in feature])

def evaluate(weights, feature):
    return sum(weights[j] * coefficient for j, coefficient in feature)

def synthesis(orbit_samples=50, cycle=None, mode='196', seconds=10):
    solver = z3.SolverFor('QF_LRA')
    solver.set(timeout=int(seconds * 1000))
    weights = [z3.Real('weight_%d' % j) for j in range(WEIGHTS)]
    # States carry the exact previous q and recognition of the two bad patterns.
    states = [(0, True, True, False)]
    ids = {states[0]: 0}
    transitions, terminals = [], []
    for previous, low, exceptional, started in states:
        u = ids[(previous, low, exceptional, started)]
        for center in [None] + list(range(0, 19, 2)):
            if not started and (center is None or center == 0):
                continue
            bad = (low and (center is None or center <= 9)) or (
                exceptional and started and (center is None or center == 0))
            if bad:
                terminals.append((u, weights[TRANSITION_WEIGHTS + 11 * previous + r.terminal_index(center)]))
        for q in range(0 if started else 1, 19):
            lo = low and q <= 9
            ex = exceptional and (q in (0, 11) if started else q == 11)
            if not (lo or ex):
                continue
            target = (state(q), lo, ex, True)
            if target not in ids:
                ids[target] = len(states)
                states.append(target)
            transitions.append((u, ids[target], weights[19 * previous + q]))
    potential = [z3.Real('safe_%d' % j) for j in range(len(states))]
    solver.add(potential[0] == 0)
    for u, v, cost in transitions:
        solver.add(potential[v] <= potential[u] - cost)
    for u, terminal in terminals:
        solver.add(potential[u] - terminal >= 0)
    positive = []
    if mode in ('196', 'or'):
        orbit, word = [], ((7,), 18)
        for _ in range(orbit_samples):
            orbit.append(row(weights, features(word)) >= 1)
            word = r.qstep(word)
        positive.append(z3.And(orbit))
    if mode in ('cycle', 'or'):
        assert cycle and all(0 <= q <= 18 for q in cycle)
        positive.append(z3.Sum([weights[19 * state(cycle[j-1]) + q]
            for j, q in enumerate(cycle)]) >= 1)
    solver.add(z3.Or(positive))
    return solver, weights, {'safety_states': len(states),
        'safety_edges': len(transitions), 'safety_terminals': len(terminals)}

def samples(maxpairs=3):
    result = []
    for length in range(maxpairs + 1):
        for pairs in product(range(19), repeat=length):
            if pairs and pairs[0] == 0:
                continue
            for center in [None] + list(range(0, 19, 2)):
                word = pairs, center
                if not r.valid(word):
                    continue
                result.append((word, features(word), features(r.qstep(word))))
    return result

def integer_model(model, variables):
    rational = [model.eval(v, model_completion=True) for v in variables]
    values = [Fraction(v.numerator_as_long(), v.denominator_as_long()) for v in rational]
    denominator = lcm(*(v.denominator for v in values))
    return [int(v * denominator) for v in values]

def main(mode='196', cycle=None, orbit_samples=50, seconds=10, rounds=50,
         add_per_round=128, stem='resume_weighted_memory_196', maxpairs=3):
    began = time.monotonic()
    solver, variables, safety = synthesis(orbit_samples, cycle, mode, seconds)
    data = samples(maxpairs)
    history, constrained = [], set()
    configuration = dict(mode=mode, cycle=cycle, orbit_samples=orbit_samples,
        weights=WEIGHTS, memory_states=MEMORY_STATES, samples=len(data),
        maxpairs=maxpairs, seconds_per_solve=seconds, rounds=rounds, **safety)
    print(json.dumps(configuration), flush=True)
    document = dict(configuration=configuration, history=history,
        certification='NO_INVARIANT_CERTIFIED')
    for iteration in range(rounds):
        status = solver.check()
        rec = dict(iteration=iteration, synthesis=str(status), seconds=time.monotonic()-began)
        if status != z3.sat:
            rec['scope'] = 'current finite CEGIS constraints with exact bad-language safety'
            if status == z3.unknown:
                rec['reason'] = solver.reason_unknown()
            history.append(rec)
            print(json.dumps(rec), flush=True)
            break
        values = integer_model(solver.model(), variables)
        bad = [j for j, (_, source, target) in enumerate(data)
            if evaluate(values, source) > 0 and evaluate(values, target) <= 0]
        rec['finite_counterexamples'] = len(bad)
        if bad:
            # Uniform coverage of sample order; duplicate feature constraints
            # add no logical information, so retain each pair only once.
            count = min(add_per_round, len(bad))
            chosen = [bad[j * len(bad) // count] for j in range(count)]
            added = 0
            for j in chosen:
                _, source, target = data[j]
                key = source, target
                if key in constrained:
                    continue
                constrained.add(key)
                solver.add(z3.Or(row(variables, source) <= 0, row(variables, target) >= 1))
                added += 1
            assert added, 'A previous constraint should exclude its integer-model counterexample.'
            rec['constraints_added'] = added
        else:
            rec.update(status='FINITE_SAMPLE_CANDIDATE',
                weights=[values[19*j:19*(j+1)] for j in range(MEMORY_STATES)],
                terminals=[values[TRANSITION_WEIGHTS+11*j:TRANSITION_WEIGHTS+11*(j+1)]
                    for j in range(MEMORY_STATES)])
            history.append(rec)
            print(json.dumps({k:v for k,v in rec.items() if k not in ('weights','terminals')}), flush=True)
            break
        history.append(rec)
        print(json.dumps(rec), flush=True)
        Path(stem+'_results.json').write_text(json.dumps(document, indent=2))
    Path(stem+'_results.json').write_text(json.dumps(document, indent=2))
    if history and history[-1]['synthesis'] == 'unsat':
        Path(stem+'_unsat.smt2').write_text(solver.to_smt2())
    return document

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['196','cycle','or'], default='196')
    parser.add_argument('--cycle', type=str)
    parser.add_argument('--seconds', type=float, default=10)
    parser.add_argument('--rounds', type=int, default=50)
    parser.add_argument('--stem', default='resume_weighted_memory_196')
    args = parser.parse_args()
    main(mode=args.mode, cycle=tuple(map(int,args.cycle.split(','))) if args.cycle else None,
        seconds=args.seconds, rounds=args.rounds, stem=args.stem)
