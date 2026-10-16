#!/usr/bin/env python3
"""Deterministic finite controls and exhaustive bounded exterior graph.

Acyclicity concerns ONLY states whose entire exterior stays within the stated
length cap. An escaping edge is not a proof of eventual divergence.
"""
from __future__ import annotations
from collections import Counter, deque
import hashlib
from itertools import product
import json
from pathlib import Path
from complementary_quotient import PHASES, check_cases, exterior_transition

CLOCK = {2: 1, 4: 5, 8: 7, 16: 8, 14: 4, 10: 2}
PSI = {1: 0, 2: 1, 3: 1, 10: 1,
       **{p: 2 for p in range(4, 10)}, **{p: 3 for p in range(11, 19)}}


def exteriors(cap: int, phases=PHASES):
    for c in phases:
        for k in range(cap + 1):
            for B in product(range(19), repeat=k):
                if (not B or B[0] > 0) and (not B or B[-1] != c):
                    yield c, B


def arithmetic_controls(cap: int = 3) -> dict:
    count = clock_count = 0
    strips = Counter()
    for c, B in exteriors(cap):
        cp, Bp, g, u = exterior_transition(c, B)
        m, mp = sum(B)-c*len(B), sum(Bp)-cp*len(Bp)
        assert (mp-2*m+g*c) % 9 == 0
        if c in CLOCK:
            assert (CLOCK[cp]*mp + g - CLOCK[c]*m) % 9 == 0
            clock_count += 1
        p = B[0] if B else c
        pp = Bp[0] if Bp else cp
        assert 2*g+PSI[pp] <= 1+PSI[p]
        assert p+1 <= pp+10*g
        if g == 0:
            assert len(Bp) >= len(B)
        strips[g, u] += 1
        count += 1
    outer_rows = []
    for p in range(1, 19):
        for e in (0, 1):
            g = (p+e)//10
            pp = 2*p+e if g == 0 else p % 10+1
            assert 2*g+PSI[pp] <= 1+PSI[p]
            assert p+1 <= pp+10*g
            outer_rows.append([p,e,g,pp,PSI[p],PSI[pp]])
    return {"exterior_length_cap": cap, "exteriors_checked": count,
            "unit_phase_clocks_checked": clock_count,
            "strip_histogram": {f"overflow={g},strip={u}": v
                                for (g,u),v in sorted(strips.items())},
            "outer_table_rows": outer_rows}


def bounded_graph(cap: int, phases=PHASES) -> tuple[dict, dict]:
    states = list(exteriors(cap, phases))
    index = {s:i for i,s in enumerate(states)}
    succ = []; reverse = [[] for _ in states]
    rank = [0]*len(states); queue = deque()
    for i,(c,B) in enumerate(states):
        cp,Bp,g,u = exterior_transition(c,B)
        target = index.get((cp,Bp), -1)
        if target == -1:
            assert len(Bp)>cap, ("unexpected missing state", c, B, cp, Bp)
            rank[i]=1; queue.append(i)
        else:
            reverse[target].append(i)
        succ.append(target)
    while queue:
        j=queue.popleft()
        for i in reverse[j]:
            assert rank[i]==0
            rank[i]=rank[j]+1
            queue.append(i)
    unresolved = [i for i,r in enumerate(rank) if r==0]
    assert not unresolved, f"bounded graph contains a cycle: {len(unresolved)} states"
    digest = hashlib.sha256()
    for i,(s,j,r) in enumerate(zip(states,succ,rank)):
        assert j==-1 or rank[j]<r
        digest.update((json.dumps([i,s,j,r],separators=(',',':'))+'\n').encode())
    report={"exterior_length_cap":cap,"phases":list(phases),"states":len(states),
            "internal_edges":sum(j!=-1 for j in succ),
            "escape_edges":sum(j==-1 for j in succ),
            "maximum_steps_to_escape":max(rank),
            "rank_histogram":{str(r):n for r,n in sorted(Counter(rank).items())},
            "canonical_rows_sha256":digest.hexdigest(),
            "status":"acyclic entire bounded graph; no claim after escape"}
    return report, dict(zip(states,rank))


def main() -> None:
    result={"formula_replay":check_cases(),"arithmetic_controls":arithmetic_controls(),
            "bounded_graphs":[bounded_graph(k)[0] for k in (1,2,3)],
            "source_sha256":{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                for name in ('complementary_quotient.py','ExteriorClock.lean')}}
    output=Path(__file__).with_name('audit_results.json')
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
