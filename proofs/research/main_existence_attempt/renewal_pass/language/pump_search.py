"""Look for exact unary-prefix loops with terminating class witnesses.

All failed finite probes are retained. A success requires an actual repeated
full configuration and repeated exact observation residual, not extrapolated
palindrome times. No arbitrary observation-depth sweep is performed.
"""
from pathlib import Path
import argparse
import gzip
import itertools
import json
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = ROOT/'main_existence_attempt/correlation_pass/language'
SOURCE = ROOT/'main_existence_attempt/return_pass/language'
sys.path.insert(0, str(OLD))
from correlated_cegar import Stored, Extension


def run(seconds=90, max_prefix=60, max_hit=20):
    started = time.monotonic()
    nfa = json.loads((SOURCE/'safe_image2_nfa.json').read_text())
    d4 = json.loads((SOURCE/'observation_depth4.json').read_text())
    edge = [dict(row) for row in nfa['transitions']]
    machines = [Stored(d4)]
    for depth in range(5, max(10, max_hit-1)+1):
        machines.append(Extension(machines[-1]))

    def config_step(states, q):
        return tuple(sorted({v for u in states for v in edge[u].get(q, ())}))

    def config(p):
        states = tuple(nfa['initial'])
        for q in p:
            states = config_step(states, q)
        return states

    def obs(p, depth):
        state = 0
        for q in p:
            state = machines[depth-4].step(state, q)
        return state

    def integer(p, c):
        return int(''.join(str(min(9, q)) for q in p) +
                   ('' if c is None else str(c//2)) +
                   ''.join(str(max(0, q-9)) for q in reversed(p)))

    def hit(p, c):
        n = integer(p, c)
        for h in range(1, max_hit+1):
            n += int(str(n)[::-1])
            if str(n) == str(n)[::-1]:
                return h
        return None

    targets = [dict(depth=4, pairs=(18,17,17), center=14),
               dict(depth=10, pairs=(3,6,4,6,12,12), center=None)]
    for row in targets:
        row['subset'] = config(row['pairs'])
        row['observer'] = obs(row['pairs'], row['depth'])
        row['observer4'] = obs(row['pairs'], 4)
    prefix_records, tests, certificates = [], [], []
    suffixes = [()] + [(q,) for q in range(19)] + list(itertools.product(range(19), repeat=2))
    suffixes += [tuple(t['pairs'][-3:]) for t in targets]
    for a in range(1,19):
        for q in range(19):
            if time.monotonic()-started >= seconds:
                break
            prefix = (a,)
            states = config(prefix)
            state4 = obs(prefix, 4)
            seen = {}
            cycle = None
            for r in range(max_prefix+1):
                key = states, state4
                if key in seen:
                    cycle = (seen[key], r-seen[key])
                    break
                seen[key] = r
                states = config_step(states, q)
                state4 = d4['delta'][state4][q]
            prefix_records.append(dict(a=a,q=q,cycle=cycle,seen=len(seen)))
            if cycle is None or not states:
                continue
            base, period = cycle
            p = (a,) + (q,)*base
            for suffix in suffixes:
                word = p+suffix
                cfg = config(word)
                s4 = obs(word, 4)
                for target in targets:
                    if cfg != target['subset'] or s4 != target['observer4']:
                        continue
                    depth = target['depth']
                    if obs(word, depth) != target['observer']:
                        continue
                    h = hit(word, target['center'])
                    record = dict(a=a,q=q,base=base,period=period,suffix=suffix,
                                  target_depth=depth,first_hit=h)
                    tests.append(record)
                    if h is None:
                        continue
                    # Enter the eventual cycle of the deeper observation
                    # used to prove the complete finite first-hit time.
                    proof_depth = max(depth, h-1)
                    high_seen = {}
                    for rr in range(base, base+max_prefix+1):
                        if (rr-base)%period:
                            continue
                        pp = (a,) + (q,)*rr
                        key = config(pp), obs(pp, depth), obs(pp, proof_depth)
                        if key in high_seen:
                            start = high_seen[key]
                            loop = rr-start
                            start_prefix = (a,)+(q,)*start
                            ww = start_prefix+suffix
                            hh = hit(ww, target['center'])
                            record['deeper_cycle'] = [start,loop]
                            record['deeper_cycle_first_hit'] = hh
                            if hh is not None and hh-1 <= proof_depth:
                                certificate = dict(prefix=start_prefix,loop=(q,)*loop,
                                    suffix=suffix,center=target['center'],
                                    target_depth=depth,proof_depth=proof_depth,
                                    first_hit=hh,base_integer=str(integer(ww,target['center'])),
                                    target_pairs=target['pairs'],target_subset=cfg)
                                certificates.append(certificate)
                                print(json.dumps(dict(found=certificate,seconds=time.monotonic()-started)),flush=True)
                            break
                        high_seen[key] = rr
                    if certificates:
                        break
                if certificates:
                    break
            if certificates:
                break
        if certificates or time.monotonic()-started >= seconds:
            break
    status = 'EXACT_PUMP_CERTIFICATE_FOUND' if certificates else (
        'UNKNOWN_TIME_CAP' if time.monotonic()-started >= seconds else 'NO_PUMP_IN_FINITE_CATALOG')
    result = dict(status=status,seconds_cap=seconds,max_prefix=max_prefix,max_hit=max_hit,
                  seconds=time.monotonic()-started,targets=targets,
                  unary_prefix_records=prefix_records,terminating_probes=tests,
                  certificates=certificates,positive_invariant_found=False)
    with gzip.open(HERE/'pump_search_result.json.gz','wt') as stream:
        json.dump(result,stream,separators=(',',':'))
    summary = {k:v for k,v in result.items() if k not in ('unary_prefix_records','terminating_probes')}
    summary.update(unary_prefix_count=len(prefix_records),candidate_count=len(tests))
    (HERE/'pump_search_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--seconds',type=float,default=90)
    parser.add_argument('--max-prefix',type=int,default=60)
    parser.add_argument('--max-hit',type=int,default=20)
    a=parser.parse_args()
    run(a.seconds,a.max_prefix,a.max_hit)
