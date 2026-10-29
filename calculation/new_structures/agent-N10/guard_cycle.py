#!/usr/bin/env python3
"""Exact finite phase/residue automaton for guaranteed one/two-site erosion."""
import json,sys
from pathlib import Path
p=json.loads((Path(__file__).resolve().parent/"phase.json").read_text())
def compute(H):
    assert H>=0
    phase,residue=0,19
    seen={};losses=[];total=0
    while (phase,residue) not in seen:
        seen[phase,residue]=(len(losses),total)
        d=2 if p["phase_W"][phase][residue]==9 else 1
        losses.append(d);total+=d
        phase=(phase+1)%8;residue=(residue-d)%20
    start,pre=seen[phase,residue]
    period=len(losses)-start;weight=total-pre
    assert start==0 and period==136 and weight==140,(start,period,weight)
    q,rem=divmod(H,period)
    loss=q*weight+sum(losses[:rem])
    # Require at least one complete W band through t=H.
    k=loss//20+2 if loss%20 else loss//20+1
    assert 20*k-loss>=20
    return dict(horizon=H,state_period=period,period_loss=weight,
                loss=loss,safe_copies=k,seed_digits=78+40*k,
                guaranteed_cols=39+20*k-loss)
if __name__=="__main__":
    for H in [0,8,80,800,20000,int(sys.argv[1]) if len(sys.argv)>1 else 20000]:
        print(compute(H))
