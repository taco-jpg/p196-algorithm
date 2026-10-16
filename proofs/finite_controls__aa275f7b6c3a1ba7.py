#!/usr/bin/env python3
import json
from pathlib import Path

def step_q(q):
    carry=0
    digits=[]
    carries=[carry]
    for x in q:
        carry,digit=divmod(x+carry,10)
        digits.append(digit)
        carries.append(carry)
    if carry: digits.append(carry)
    return [a+b for a,b in zip(digits,digits[::-1])],digits,carries

def realize(q):
    size=len(q)
    d=[0]*size
    for i,x in enumerate(q):
        j=size-1-i
        d[i]=x-9 if i<j else min(x,9) if j<i else x//2
        d[i]=max(0,d[i])
    n=sum(x*10**i for i,x in enumerate(d))
    return n,d

results=[]
for k in range(0,25):
    for r in range(0,25):
        source=[1]+[9]*k+[1,10]+[9]*(2*r)+[10,1]+[9]*k+[1]
        expected=[2]+[18]*k+[3,1]+[0]*(2*r)+[1,3]+[18]*k+[2]
        target,digits,carries=step_q(source)
        n,d=realize(source)
        rev=int(str(n)[::-1])
        actual_digits=list(map(int,str(n+rev)[::-1]))
        actual_target=[a+b for a,b in zip(actual_digits,actual_digits[::-1])]
        assert len(source)==2*k+2*r+6
        assert target==expected==actual_target
        assert digits==actual_digits and carries[-1]==0
        assert source==[a+b for a,b in zip(d,d[::-1])]
        assert all(0<x<18 for x in source)
        assert target.count(0)==2*r and target.count(18)==2*k
        results.append({'k':k,'r':r,'width':len(source),'new_zero':2*r,'new_eighteen':2*k})
report={'scope':'finite controls only; formal theorem handles all parameters', 'cases':len(results),'k_range':[0,24],'r_range':[0,24],'all_checks_pass':True,'example':{'k':1,'r':1,'source':[1,9,1,10,9,9,10,1,9,1],'target':[2,18,3,1,0,0,1,3,18,2]},'results':results}
Path(__file__).with_name('finite_controls.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
