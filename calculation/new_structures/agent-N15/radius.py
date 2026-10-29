#!/usr/bin/env python3
"""Empirical minimal local radius over the bounded, sampled interior of dyadic level 11.
Not an all-width or global radius theorem.
"""
import json
from dyadic import twinkle,next_pair

W=twinkle(11)
P=[4]+W
P=P+P[::-1]
source=[4]+W

def test_r(P,r):
    L=min(len(P)//2,len(source))
    model={}
    for i in range(50,L-50):
        key=tuple(source[i-r:i+r+1])
        if key in model and model[key]!=P[i]:return False,len(model)
        model[key]=P[i]
    return True,len(model)

out=[]
for t in range(33):
    if t in (0,1,2,3,4,5,6,7,8,10,12,16,20,24,32):
        result=None
        for r in range(21):
            ok,n=test_r(P,r)
            if ok:result={'radius':r,'distinct_windows':n};break
        out.append({'step':t, 'pairword_length':len(P), **(result or {'radius':None})})
    P,_=next_pair(P)
with open('radius_data.json','w') as f:json.dump({'scope':'level h=11; positions 50..min(initial half, current half)-50; radius <=20','table':out},f,indent=2)
for x in out:print(x)
