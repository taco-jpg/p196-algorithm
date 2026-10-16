"""Search variable return clocks for a two-digit binary block encoding.

A return increasing the stable binary parameter by one adds four decimal
digits. Each segment ends with one overflow. There are at most four preceding
nonoverflow steps, so all segment lengths lie in 1..5. The outer pair-sum
automaton filters schedules before the exact arbitrary-width exterior graph.
Graph caps produce INCOMPLETE, never an impossibility conclusion.
"""
from itertools import product
from pathlib import Path
from functools import lru_cache
import argparse
import json
import time
from continuation_theory_multigrowth import search

def nonoverflow(q):
    if 1 <= q <= 8:
        return (2*q,2*q+1)
    if q == 9:
        return (18,)
    return ()

def overflow(q):
    if q == 9:
        return (10,)
    if 10 <= q <= 18:
        return (q-9,)
    return ()

@lru_cache(None)
def segment(q, length):
    states = {q}
    for _ in range(length-1):
        states = {r for s in states for r in nonoverflow(s)}
    return {r for s in states for r in overflow(s)}

def possible_cycle(periods):
    for q in range(1,11):
        states = {q}
        for length in periods:
            states = {r for s in states for r in segment(s,length)}
        if q in states:
            return True
    return False

def schedules(growths=4):
    for periods in product(range(1,6),repeat=growths):
        if periods != min(periods[k:]+periods[:k] for k in range(growths)):
            continue
        if possible_cycle(periods):
            yield periods

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--growths',type=int,default=4)
    parser.add_argument('--seconds',type=float,default=1)
    parser.add_argument('--states',type=int,default=30000)
    parser.add_argument('--stem',default='persist_block_neutral_timechange')
    args=parser.parse_args()
    began = time.monotonic()
    results = []
    for periods in schedules(args.growths):
        result = search(10,list(periods),maxstates=args.states,seconds=args.seconds)
        results.append(result)
        if args.growths<=4 or result['accepted'] or len(results)%25==0:
            print(json.dumps(result),flush=True)
        Path(args.stem+'_results.json').write_text(json.dumps(results,indent=2))
    print(json.dumps({'schedules':len(results),'complete':sum(x['complete'] for x in results),
        'accepting':sum(bool(x['accepted']) for x in results),'seconds':time.monotonic()-began}),flush=True)
