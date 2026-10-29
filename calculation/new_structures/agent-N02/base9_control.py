#!/usr/bin/env python3
"""Positive regular-induction control, using the independently tracked b9 lattice cycle.
Run from repository root: python3 calculation/new_structures/agent-N02/base9_control.py
"""
from pathlib import Path
import json
from carry_relation import DFA,guard_check,inclusion_counterexample,finite_certificate


def regular_band(B,W,rho,odd,base=9):
    """A finite automaton for B ++ prefix(W^infty,q), where l=2q-odd,
    l>=8, l mod |W| = rho, and l parity = odd. The centre is unbounded.
    This control has |W|=4 and B length=61.
    """
    assert len(W)==4
    limit=12 # first 12 band cells, then count modulo 4 forever
    n=len(B)
    sink=n+limit+4
    alpha=2*base-1
    table=[]
    for s in range(sink+1):
        row=[sink]*alpha
        if s<n:row[B[s]]=s+1
        elif s<sink:
            q=s-n
            next_q=q+1 if q<limit+3 else limit
            row[W[q%4]]=n+next_q
        table.append(row)
    finals=set()
    for q in range(limit+4):
        if (2*q-int(odd))>=8 and (2*q-int(odd))%4==rho and (rho%2==int(odd)):
            finals.add(n+q)
    return DFA(0,finals,table)


def run():
    root=Path(__file__).resolve().parents[3]
    dataset=root/'calculation/decimal_frontier/lattice_formats/cert_b9_rec0.json'
    j=json.loads(dataset.read_text())
    assert j['base']==9 and j['p']==10 and len(j['B_t'][0])==61 and len(j['w_t'][0])==4
    rho=[2]
    for gam in j['gam']:rho.append((rho[-1]+gam)%4)
    assert rho[-1]==2
    automata=[]
    for t in range(10):
        automata.append([regular_band(j['B_t'][t],j['w_t'][t],rho[t],odd,9) for odd in (0,1)])
    result=finite_certificate(automata,9)
    assert result['ok'],result
    for row in automata:
        for d in row:assert guard_check(d,9)
    print('BASE9_REGULAR_INVARIANT_PASS',result,'40 unbounded-word inclusions')
    # This validates the NEW language checker on a known Lean-certified control;
    # it does not purport to discover a new base9 example.

if __name__=='__main__':run()