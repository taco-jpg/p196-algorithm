#!/usr/bin/env python3
"""Exact two-parameter base-10 affine-slope carry chamber engine (standard library)."""
import argparse, hashlib, json, sys
from collections import defaultdict
from dataclasses import dataclass

# Exponent a*q + b*r + c, with independent integer q,r >= Q.
@dataclass(frozen=True)
class Form:
    a: int; b: int; c: int
    def __add__(self,x):
        return Form(self.a,self.b,self.c+x) if isinstance(x,int) else Form(self.a+x.a,self.b+x.b,self.c+x.c)
    def __sub__(self,x):
        return Form(self.a,self.b,self.c-x) if isinstance(x,int) else Form(self.a-x.a,self.b-x.b,self.c-x.c)
    def at(self,q,r):return self.a*q+self.b*r+self.c

# A four-sheet skeleton closed under mirroring about a (3,1)-slope top.
SLOPES=((0,0),(1,0),(2,1),(3,1))
class Sheet:
    def __init__(self): self.G=1;self.iteration=0
    def order(self,keys):
        e=sorted(set(keys),key=lambda x:(SLOPES.index((x.a,x.b)),x.c))
        for x in e:
            assert (x.a,x.b) in SLOPES,('escaped slope sheets',x)
            # no negative digit exponents at G
            s=x.a+x.b
            if s==0:assert x.c>=0,('negative base exponent',x)
            else:self.G=max(self.G, (-x.c + s-1)//s)
        for x,y in zip(e,e[1:]):
            A=y.a-x.a;B=y.b-x.b;C=y.c-x.c
            if A==B==0:
                assert C>=1,('same-form collision',x,y)
            else:
                assert A>=0 and B>=0 and (A+B)>0,('not an orthant chamber',x,y)
                self.G=max(self.G,(1-C + A+B-1)//(A+B))
        return e

def canonical(raw,s):
    coeff=defaultdict(int)
    for e,v in raw.items():coeff[e]+=v
    for _ in range(100):
        todo=[(e,v//10) for e,v in coeff.items() if v>=10]
        if not todo:break
        for e,c in todo:
            coeff[e]-=10*c;coeff[e+1]+=c
    else:raise AssertionError('carry normalization did not terminate')
    out={e:v for e,v in coeff.items() if v!=0}
    assert out and all(0<v<10 for v in out.values())
    s.order(out)
    return out

def next_digits(d,s):
    ordered=s.order(d)
    top=ordered[-1]
    assert (top.a,top.b)==(3,1) and d[top]>0
    raw=defaultdict(int)
    for e,v in d.items():raw[e]+=v;raw[top-e]+=v
    return canonical(raw,s)

def not_pal(d,s):
    top=s.order(d)[-1]
    return any(d.get(top-e,0)!=v for e,v in d.items())

def seed(middle=37):
    # N(q,r) = 88 * 10^(3q+r) + middle * 10^q + 75
    # middle is a two-digit number.
    assert 10<=middle<=99
    raw={Form(3,1,1):8,Form(3,1,0):8,Form(1,0,1):middle//10,Form(1,0,0):middle%10,Form(0,0,1):7,Form(0,0,0):5}
    return raw

def as_int(d,q,r):return sum(v*10**e.at(q,r) for e,v in d.items())
def next_int(x):return x+int(str(x)[::-1])
def sig(d):
    ditems=[(e.a,e.b,e.c,v) for e,v in d.items()]
    return hashlib.sha256(json.dumps(sorted(ditems),separators=(',',':')).encode()).hexdigest()

def run(middle=37,T=264):
    s=Sheet(); d=canonical(seed(middle),s)
    rows=[]; states=[]; pal=[]
    for t in range(T+1):
        states.append(d)
        if not_pal(d,s) is False:pal.append(t)
        counts={f'{a},{b}':sum(1 for e in d if (e.a,e.b)==(a,b)) for a,b in SLOPES}
        rows.append({'t':t,'bound':s.G,'top':s.order(d)[-1].c,'support':len(d),'four_sheets':counts,'signature':sig(d)})
        if t<T:d=next_digits(d,s)
    return s,rows,states,pal

def validate(states,G,qr):
    q,r=qr
    assert min(q,r)>=G,(G,q,r)
    x=as_int(states[0],q,r)
    for i,d in enumerate(states):
        exp=as_int(d,q,r)
        assert exp==x,('integer-mismatch',i,q,r)
        if i+1<len(states):x=next_int(x)
    return {'q':q,'r':r,'steps':len(states)-1,'final_digits':len(str(x)),'final_sha256':hashlib.sha256(str(x).encode()).hexdigest()}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--middle',type=int,default=37);ap.add_argument('--steps',type=int,default=264);ap.add_argument('--output',default='four_sheet_data.json')
    x=ap.parse_args()
    s,rows,states,pal=run(x.middle,x.steps)
    probes=[(s.G+2,s.G+3),(s.G+17,s.G+29),(s.G+50,s.G+2)]
    controls=[validate(states,s.G,ab) for ab in probes]
    data={'scope':'base10, universal q,r>=bound, exactly t=0..steps','seed':f'88*10^(3q+r)+{x.middle}*10^q+75','T':x.steps,'G':s.G,'palindromic_slices':pal,'support_series':[z['support'] for z in rows], 'checkpoints': [rows[i] for i in sorted({0,1,2,3,8,20,44,88,128,x.steps}) if i<=x.steps],'independent_integer_replays':controls}
    with open(x.output,'w') as f:json.dump(data,f,indent=2)
    print(json.dumps({k:v for k,v in data.items() if k not in ('support_series','checkpoints')},indent=2))
