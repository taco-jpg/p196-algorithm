#!/usr/bin/env python3
"""Exact pair-coefficient normalization study of a neutral/absorbing interface.
Run: python3 small_probe.py hybrid_data.json
"""
import sys,json

def step(P):
    carry=0;O=[]
    for x in P:
        y=x+carry;carry=y//10;O.append(y%10)
    if carry:O.append(carry)
    return [O[i]+O[-1-i] for i in range(len(O))]

def longest(w,symbol):
    cur=best=0
    for x in w:
        cur=(cur+1) if x==symbol else 0
        best=max(cur,best)
    return best

def run(d):
    out=[]; a=20;u=80
    for center in [18,0]:
        lo=d['B'][0]+d['W'][0]*a+[9]*u
        P=lo+[center]+lo[::-1]
        case=[]
        for t in range(4):
            middle=P[:len(P)//2][len(d['B'][0])+a*d['lattice_period']:]
            case.append(dict(step=t,neutral9=longest(middle,9),zero=longest(middle,0),eighteen=longest(middle,18)))
            P=step(P)
        out.append(dict(center=center,measurement=case))
    assert out[0]['measurement'][3]['zero']==79
    assert out[1]['measurement'][1]['eighteen']>=79
    return out
if __name__=='__main__':
    d=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'hybrid_data.json'))
    print(json.dumps(run(d),indent=2))
