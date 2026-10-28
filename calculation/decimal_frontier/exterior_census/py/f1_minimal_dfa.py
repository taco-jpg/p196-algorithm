#!/usr/bin/env python3
"""Minimal DFA certificate for the decimal F1 cyclic overflow-word language.
The reachable 434-state Boolean-relation recognizer minimizes to 241 states.
Run: python3 calculation/decimal_frontier/exterior_census/py/f1_minimal_dfa.py [/tmp/dfa.json]
"""
from math import gcd
import json,random,sys
b=10;n=2*b-2
E=[]
for g in (0,1):
    row=[]
    for x in range(1,n+1):
        v=0
        for h in (0,1):
            if (x+h)//b!=g:continue
            y=x%b+(1 if g else (x+h)%b)
            if 1<=y<=n:v|=1<<(y-1)
        row.append(v)
    E.append(tuple(row))
def mul(a,z):
    out=[]
    for mask in a:
        m=0
        while mask:
            bit=mask&-mask;mask-=bit;m|=z[bit.bit_length()-1]
        out.append(m)
    return tuple(out)
def accept(r):
    return any((v>>i)&1 for i,v in enumerate(r))
I=tuple(1<<i for i in range(n));states=[I];ids={I:0}
for r in states:
    for g in (0,1):
        s=mul(r,E[g])
        if s not in ids:ids[s]=len(states);states.append(s)
assert len(states)==434
oldnext=[(ids[mul(r,E[0])],ids[mul(r,E[1])]) for r in states]
oldacc=[int(accept(r)) for r in states]
classes=oldacc[:];rounds=[2]
while True:
    sig=[(oldacc[i],classes[a],classes[z]) for i,(a,z) in enumerate(oldnext)]
    keys={s:i for i,s in enumerate(sorted(set(sig)))}
    new=[keys[s] for s in sig]
    rounds.append(len(keys))
    if len(keys)==rounds[-2]:
        classes=new
        break
    classes=new
assert rounds==[2,8,46,124,183,221,234,240,241,241]
rep={}
for i,c in enumerate(classes):rep.setdefault(c,i)
start=classes[0];newid={start:0};queue=[start]
for c in queue:
    i=rep[c]
    for g in (0,1):
        target=classes[oldnext[i][g]]
        if target not in newid:newid[target]=len(queue);queue.append(target)
assert len(queue)==241
rows=[]
for c in queue:
    i=rep[c]
    rows.append((oldacc[i],*(newid[classes[j]] for j in oldnext[i])))
for i,(a,z) in enumerate(oldnext):
    c=newid[classes[i]]
    assert rows[c][0]==oldacc[i]
    assert rows[c][1]==newid[classes[a]]
    assert rows[c][2]==newid[classes[z]]
assert sum(r[0] for r in rows)==104
# Independent direct relation evaluation vs quotient recognizer on random words.
rng=random.Random(9)
for _ in range(12000):
    word=[rng.randrange(2) for _ in range(rng.randrange(65))]
    r=I;s=0
    for g in word:
        r=mul(r,E[g]);s=rows[s][1+g]
    assert int(accept(r))==rows[s][0]
# Exact counting DP on both automata, all lengths 0..60.
old=[0]*len(states);old[0]=1
new=[0]*len(rows);new[0]=1
rooted=[]
for p in range(61):
    a=sum(v for i,v in enumerate(old) if oldacc[i])
    z=sum(v for i,v in enumerate(new) if rows[i][0])
    assert a==z
    rooted.append(a)
    nxt=[0]*len(states);nxt2=[0]*len(rows)
    for i,c in enumerate(old):
        if c:
            j,k=oldnext[i];nxt[j]+=c;nxt[k]+=c
    for i,c in enumerate(new):
        if c:
            _,j,k=rows[i];nxt2[j]+=c;nxt2[k]+=c
    old=nxt;new=nxt2
# Cross-check the already proved power-closure/Burnside totals.
def divs(p):return [d for d in range(1,p+1) if p%d==0]
def phi(q):return sum(gcd(q,i)==1 for i in range(1,q+1))
for p,want in ((36,351150),(40,1943815),(60,11425283484)):
    assert sum(phi(p//d)*rooted[d] for d in divs(p))==p*want
print("states original",len(states),"minimal",len(rows),
      "minimal accepting",sum(row[0] for row in rows))
print("refinement",rounds,"random direct checks 12000; rooted n<=60 identical")
if len(sys.argv)>1:
    with open(sys.argv[1],"w") as f:json.dump({"initial":0,"rows":rows},f)
