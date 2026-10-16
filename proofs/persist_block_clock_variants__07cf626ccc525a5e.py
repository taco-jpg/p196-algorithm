"""Exact exterior search near the concrete eleven-step clock.

The eight-growth schedule repeats(1,1,4,5), then varies one or two segment
lengths. This changes the temporal ansatz, not merely a spatial depth bound.
Only schedules passing the exact outer-pair clock test are searched.
"""
from itertools import combinations,product
from pathlib import Path
import json,time
from persist_block_neutral_timechange import possible_cycle
from continuation_theory_multigrowth import search

def canonical(p):
    return min(p[k:]+p[:k] for k in range(len(p)))

def clocks():
    base=(1,1,4,5)*2
    seen=set()
    for changed in (1,2):
        for positions in combinations(range(8),changed):
            for values in product(range(1,6),repeat=changed):
                if any(values[j]==base[position] for j,position in enumerate(positions)):
                    continue
                p=list(base)
                for position,value in zip(positions,values):p[position]=value
                p=canonical(tuple(p))
                if p in seen:continue
                seen.add(p)
                if possible_cycle(p):yield p

if __name__=='__main__':
    began=time.monotonic();results=[]
    for p in clocks():
        row=search(10,list(p),maxstates=15000,seconds=.3)
        results.append(row)
        if row['accepted'] or len(results)%20==0:
            print(json.dumps(row),flush=True)
        Path('persist_block_clock_variants_results.json').write_text(json.dumps(results,indent=2))
    print(json.dumps({'schedules':len(results),'complete':sum(r['complete'] for r in results),
        'accepting':sum(bool(r['accepted']) for r in results),'seconds':time.monotonic()-began}),flush=True)
