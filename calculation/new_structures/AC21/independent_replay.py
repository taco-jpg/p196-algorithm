#!/usr/bin/env python3
"""AC21 independent three-representation decimal differential replay."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"Z11"))
import independent_replay as v
def decode(n):
    j=[0]*5
    for i in range(4,-1,-1): j[i],n=n%19,n//19
    assert n==0
    return j
v.US=[(2,16,9),(9,10,8),(16,9,2)]
v.JS={
 (2,16,9):[decode(n) for n in (0,27436,419223)],
 (9,10,8):[decode(n) for n in (0,20691,627230)],
 (16,9,2):[decode(n) for n in (0,16387,426494)]}
v.CENTRES=[[4,4],[4,12,4]]
if __name__=="__main__": v.main()
