#!/usr/bin/env python3
"""Randomized independent actual big-integer control, 2400 instances."""
import json,random,sys
from pathlib import Path
sys.set_int_max_str_digits(0)
ph=json.loads((Path(__file__).resolve().parent/"phase.json").read_text())
def integer(P):
    assert P==P[::-1]
    ds=[0]*len(P)
    for i in range(len(P)//2):
        p=P[i];ds[i]=p//2;ds[-1-i]=p-p//2
    if len(P)%2:
        assert P[len(P)//2]%2==0
        ds[len(P)//2]=P[len(P)//2]//2
    return int("".join(str(d) for d in ds[::-1]))
def step_pairs(P):
    n=integer(P)
    s=str(n);result=str(n+int(s[::-1]))
    return [int(result[i])+int(result[-1-i]) for i in range(len(result))]
def run():
    rng=random.Random(1919610);count=0
    for t in range(8):
        b=ph["phase_B"][t];w=ph["phase_W"][t]
        nw=ph["phase_W"][(t+1)%8]
        for k in (1,2,3):
            for i in range(100):
                h=[rng.randrange(19) for _ in range(rng.randrange(20))]
                C=h+([2*rng.randrange(10)] if i%2 else [])+h[::-1]
                border=b+w*k
                P=border+C+border[::-1]
                IP=P[:39]+w+P[39:-39]+w[::-1]+P[-39:]
                q=step_pairs(P);iq=step_pairs(IP)
                expected=q[:39]+nw+q[39:-39]+nw[::-1]+q[-39:]
                assert iq==expected,(t,k,i)
                count+=1
    print(f"PASS {count} random genuine decimal integer cases,"
          " every phase and both centre parities")
if __name__=="__main__":run()
