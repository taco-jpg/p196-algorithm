#!/usr/bin/env python3
"""R33: independent parity, root-gate and period-10 bulk audit (no search claim)."""
from collections import Counter
from itertools import product
from pathlib import Path
import sys
sys.set_int_max_str_digits(0)

rows=[list(map(int,s.split())) for s in Path(
    "calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt").read_text().splitlines()]
assert rows[0]==[12,34,9,10] and len(rows)==38
g,W,B=rows[1],rows[2:14],rows[26:38]
assert g==[1,0,0,0,1,0,0,0,1,0,0,0]
def alt(v):
    return sum((-1)**i*x for i,x in enumerate(v))
assert (alt(B[0]),alt(W[0]))==(-11,-22)

def protected(t,q,u):
    H=B[t]+W[t]*q
    lo=[];carry=0
    for x in H:
        z=x+carry;lo.append(z%10);carry=z//10
    hi=[];carry=u
    for x in H[::-1]:
        z=x+carry;hi.append(z%10);carry=z//10
    hi=hi[::-1]
    gamma=carry
    out=([lo[0]+1]+[lo[i]+hi[i-1] for i in range(1,len(H))]
         if gamma else [lo[i]+hi[i] for i in range(len(H))])
    return gamma,out

gate=[]
for t in range(12):
    viable=[]
    for u in (0,1):
        if all(protected(t,q,u)==(g[t],B[(t+1)%12]+W[(t+1)%12]*q)
               for q in (1,2,3,4,20,40,80,160)):
            viable.append(u)
    gate.append(tuple(viable))
assert gate==[(0,1),(1,),(0,),(0,),(0,1),(1,),(0,),(1,),
             (0,1),(1,),(0,),(0,)]
print("CONFIRM rooted p12 gate:",gate)

def rowstep(u,gamma):
    n=len(u)
    low=high=None
    for bit in (0,1):
        c=bit;v=[]
        for x in u:
            v.append(c);c=(x+c)//10
        if c==bit:low=v;break
    for bit in (0,1):
        c=bit;v=[0]*n
        for i in range(n-1,-1,-1):
            v[i]=c;c=(u[i]+c)//10
        if c==bit:high=v;break
    assert low is not None and high is not None
    ld=[(x+c)%10 for x,c in zip(u,low)]
    hd=[(x+c)%10 for x,c in zip(u,high)]
    return tuple(ld[i]+hd[(i-gamma)%n] for i in range(n))

def macro(u):
    for gamma in g:
        u=rowstep(u,gamma)
    return u

seen=set();periods=Counter();ten=[]
for seed in product(range(19),repeat=3):
    if seed in seen:continue
    path=[];positions={};x=seed
    while x not in seen and x not in positions:
        positions[x]=len(path);path.append(x);x=macro(x)
    if x in positions:
        cycle=path[positions[x]:]
        periods[len(cycle)]+=1
        if len(cycle)==10:ten.extend(cycle)
    seen.update(path)
assert len(ten)==90 and periods[10]==9
assert Counter(sum(u) for u in ten)=={18:30,27:30,36:30}
expected={(x[i],x[(i+1)%3],x[(i+2)%3])
          for a in range(0,19,2) for x in [(9,a,18-a)] for i in range(3)}
assert {u for u in ten if sum(u)==27}==expected and len(expected)==30
print("CONFIRM 90 primitive period-10 U words, 30 complement-nine words")

def pairword(q,k,C,J=(4,),U=(9,2,16)):
    H=B[0]+W[0]*q+list(J)+list(U)*k
    return H+list(C)+H[::-1]
def decimal_digits(P):
    assert P==P[::-1] and P[0]>0
    h=len(P)//2
    lo=[max(x-9,0) for x in P[:h]]
    hi=[x-y for x,y in zip(P[:h],lo)]
    if len(P)%2:assert P[h]%2==0
    mid=[P[h]//2] if len(P)%2 else []
    d=lo+mid+hi[::-1]
    assert d[-1]>0 and all(0<=x<=9 for x in d)
    return d
def next_digits(d):
    carry=0;out=[]
    for i in range(len(d)):
        z=d[i]+d[-1-i]+carry
        out.append(z%10);carry=z//10
    if carry:out.append(carry)
    return out
def digits_value(d):
    return sum(x*10**i for i,x in enumerate(d))
def pairs(d):
    return [d[i]+d[-1-i] for i in range(len(d))]

J=(4,);U=(9,2,16);C=(12,4,4,12)
assert (alt(U)-alt(C))%11!=0
assert (2*alt(J)+(-1)**len(J)*alt(C))%11!=0
for q,k in product((20,40,80,160),repeat=2):
    P=pairword(q,k,C,J,U)
    d=decimal_digits(P)
    assert pairs(d)==P and alt(P)%11==0
    dn=next_digits(d)
    n=digits_value(d)
    assert digits_value(dn)==n+int(str(n)[::-1])
    assert digits_value(dn)%11==0
    assert len(d)%2==0
print("BREAK blanket mod11 gate: 16 physically realized even-centre controls")
for q in (20,40,80,160):
    d=decimal_digits(pairword(q,q,C,J,U))
    n=digits_value(d)
    for t in range(120):
        oldlen=len(d)
        new=next_digits(d)
        n=n+int(str(n)[::-1])
        assert digits_value(new)==n
        assert len(new)-oldlen==g[t%12]
        d=new
print("CONFIRM 120 genuine physical overflow steps at q=k=20/40/80/160")

for h,c in product(range(5),range(6)):
    for H in product((0,3,11),repeat=h):
        for first in product((0,4,12),repeat=(c+1)//2):
            C0=(list(first)+list(first[:-1][::-1])) if c%2 else (list(first)+list(first[::-1]))
            P=list(H)+C0+list(H[::-1])
            value=2*alt(H)+(-1)**h*alt(C0) if c%2 else 0
            assert len(C0)==c and alt(P)==value
print("PASS parity identity exhaustive short controls; no full return claimed")
