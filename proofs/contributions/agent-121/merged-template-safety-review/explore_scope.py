#!/usr/bin/env python3
"""Retained Agent 121 witness search. Experimental data, not an infinite proof.

Search the first positive palindromic iterate through exactly 200 additions.
The selected seed 99770022 is separately certified by Agent121ScopeRegression.lean.
"""
from __future__ import annotations
import json

def first_positive_hit(seed: int, horizon: int = 200) -> dict:
    value=seed
    for step in range(1,horizon+1):
        value+=int(str(value)[::-1])
        if str(value)==str(value)[::-1]:
            return {'outcome':'FOUND_EXPERIMENTALLY','step':step,'value':str(value)}
    return {'outcome':'NO_HIT_IN_FINITE_WINDOW','through':horizon,'beyond_window':'UNKNOWN',
            'last_value':str(value)}

def realize(q: list[int]) -> int:
    if q!=q[::-1] or any(x<0 or x>18 for x in q):
        raise ValueError('Expected a bounded symmetric coefficient word')
    if len(q)%2 and q[len(q)//2]%2:
        raise ValueError('Middle coefficient must be even')
    d=[0]*len(q)
    for i in range(len(q)//2):
        d[i]=max(q[i]-9,0); d[-1-i]=min(q[i],9)
    if len(q)%2: d[len(q)//2]=q[len(q)//2]//2
    return sum(x*10**i for i,x in enumerate(d))

def main() -> None:
    trials=[]
    for n in [11888811,99009911,11999999,118811,19889911]:
        trials.append({'seed':str(n),'group':'preliminary scope examples',
            'palindromic_at_time_zero':str(n)==str(n)[::-1],'result':first_positive_hit(n)})
    for c in range(1,18):
        if c==9: continue
        q=[c]*2+[18-c]*4+[c]*2
        n=realize(q)
        trials.append({'seed':str(n),'phase':c,'B':[],'A':[],'C':[],'g':2,'h':2,
            'pair_coefficients':q,'palindromic_at_time_zero':str(n)==str(n)[::-1],
            'result':first_positive_hit(n)})
    n=99770022; trace=[n]
    for _ in range(4): n+=int(str(n)[::-1]); trace.append(n)
    print(json.dumps({'agent':121,'evidence_class':'EXPERIMENT_ONLY',
        'method':'exact Python integers and decimal string reversal',
        'horizon_positive_steps':200,'trials':trials,
        'selected_kernel_checked_trace':trace,
        'kernel_source':'Agent121ScopeRegression.lean',
        'scope':'Only the selected trace and the explicit Lean boundary witnesses are promoted to LEAN-CHECKED.'},indent=2))
if __name__=='__main__': main()
