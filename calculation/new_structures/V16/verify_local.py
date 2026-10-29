#!/usr/bin/env python3
"""Independent Python control: local-collar map vs full pairword and true integers."""
from pathlib import Path
from random import Random

lines=Path('calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt').read_text().splitlines()
p,nb,m,b=map(int,lines[0].split()); gamma=list(map(int,lines[1].split()))
W=[list(map(int,lines[2+i].split())) for i in range(12)]
B=[list(map(int,lines[26+i].split())) for i in range(12)]

def make_u(a,r):
    base=(9,a,18-a);return tuple(base[(r+i)%3] for i in range(3))
Us=sorted({make_u(a,r) for a in range(0,19,2) for r in range(3)})

def bulk_carries(w):
    m=len(w); alpha=beta=None
    for s in (0,1):
        a=[s]
        for x in w:a.append((x+a[-1])//10)
        if a[-1]==s:alpha=a[:-1];break
    for s in (0,1):
        bb=[0]*(m+1);bb[m]=s
        for i in range(m-1,-1,-1):bb[i]=(w[i]+bb[i+1])//10
        if bb[0]==s:beta=bb;break
    assert alpha is not None and beta is not None
    return alpha,beta

def bulk_step(w,g):
    a,b=bulk_carries(w);m=len(w);z=[]
    for i in range(m):
        lo=(w[i]+a[i])%10
        hi=(w[i]+b[i+1])%10 if g==0 else (w[(i-1)%m]+b[i])%10
        z.append(lo+hi)
    return tuple(z)

def full_pair_step(P):
    d=[];c=0
    for x in P:
        z=x+c;d.append(z%10);c=z//10
    g=c
    if c:d.append(c)
    return [d[i]+d[-1-i] for i in range(len(d))],g

def local_step(H,U,ustart,g,lookahead=6):
    ext=list(H)
    while len(ext)<len(H)+lookahead:
        ext.append(U[(len(ext)-ustart)%3])
    n=len(H);low=[0]*n;high=[0]*n;c=0
    for i,x in enumerate(H):
        z=x+c;low[i]=z%10;c=z//10
    state=None
    for x in ext[n:]:
        if x!=9:state=int(x>=10);break
    assert state is not None
    for i in range(n-1,-1,-1):
        if not g:
            high[i]=state
            if H[i]!=9:state=int(H[i]>=10)
        else:
            if H[i]!=9:state=int(H[i]>=10)
            high[i]=state
    out=[]
    for i in range(n):
        if not g:out.append(low[i]+(H[i]+high[i])%10)
        elif i==0:out.append(low[i]+1)
        else:out.append(low[i]+(H[i-1]+high[i])%10)
    return out

def make_source(phase,q,k,J,U,C=(0,0)):
    H=B[phase][:]
    for _ in range(q):H+=W[phase]
    H+=list(J)+list(U)*k
    return H+list(C)+H[::-1]

def digits_from_pair(P):
    n=len(P);d=[0]*n
    for i in range(n//2):
        hi=min(9,P[i]);d[i]=P[i]-hi;d[n-1-i]=hi
    if n%2:
        assert P[n//2]%2==0
        d[n//2]=P[n//2]//2
    assert d[-1]!=0
    return d

def insert_pairword(P,w,cut):
    return P[:cut]+list(w)+P[cut:len(P)-cut]+list(w)[::-1]+P[len(P)-cut:]

def pair_from_digits(d):return [d[i]+d[-1-i] for i in range(len(d))]
def integer_from_digits(d):return sum(x*10**i for i,x in enumerate(d))
def reverse_add_bigint(n):return n+int(str(n)[::-1])
def digit_array_step(d):
    out=[];c=0
    for i in range(len(d)):
        z=d[i]+d[-1-i]+c;out.append(z%10);c=z//10
    if c:out.append(c)
    return out

rng=Random(1603);q=14;k=100;M=34+9*q+170
for case in range(100):
    jlen=3+(case%2);J=tuple(rng.randrange(19) for _ in range(jlen));U0=Us[rng.randrange(len(Us))]
    clen=2+rng.randrange(12); half=[rng.randrange(19) for _ in range(clen//2)]
    if clen%2: C=tuple(half+[2*rng.randrange(10)]+half[::-1])
    else: C=tuple(half+half[::-1])
    P=make_source(3,q,k,J,U0,C);H=P[:M];U=U0;ustart=34+9*q+jlen
    for t in range(120):
        Q,g=full_pair_step(P);assert g==gamma[(3+t)%12],(case,t,g,gamma[(3+t)%12])
        Qloc=local_step(H,U,ustart,g)
        assert Qloc==Q[:M],(case,t,'local/full mismatch')
        P=Q;H=Qloc;U=bulk_step(U,g)
    assert U==U0,(case,'U3 did not return after 120')
print('PASS: 100 random phase-3 J/U/C candidates (both centre parities, lengths 2..13), 120 local steps each; local collar equals full pairword engine at every step.')

for phase in range(12):
    for U0 in Us:
        U=U0
        for t in range(120):U=bulk_step(U,gamma[(phase+t)%12])
        assert U==U0,(phase,U0,'bulk period failure')
print('PASS: all 30 charge-zero U3 words return after 120 bulk steps for all 12 clock phases.')
for ph in range(12):
    assert bulk_step(tuple(W[ph]),gamma[ph])==tuple(W[(ph+1)%12]),(ph,'W9 row transition mismatch')
    assert gamma[ph]==int(B[ph][0]>=10),(ph,'root overflow gate mismatch')
print('PASS: all 12 W9 row transitions and rooted overflow gates.')

def cone_losses(U0,phase):
    rows=[tuple(U0)]
    for t in range(120):rows.append(bulk_step(rows[-1],gamma[(phase+t)%12]))
    m=len(U0);left=right=0
    for t in range(120):
        w=rows[t];left+=1+int(w[left%m]==9);right+=1+int(w[(-right-1)%m]==9)-gamma[(phase+t)%12]
    return left,right
phase3_cones={cone_losses(U0,3) for U0 in Us}
assert phase3_cones=={(149,120),(150,119),(151,121)},phase3_cones
m=34+9*14;start_m=m
for t in range(120):
    row=W[(3+t)%12];r=0
    while row[(m-35-r)%9]==9:r+=1
    m-=1+r-gamma[(3+t)%12]
phase3_w_loss=start_m-m
assert phase3_w_loss==90,phase3_w_loss
assert 9*14-phase3_w_loss>=36 and 165-max(x[0] for x in phase3_cones)>=14 and 135-max(x[1] for x in phase3_cones)>=14
print('PASS: phase-3 120-step cone bounds: W loss=90; U loss pairs={(149,120),(150,119),(151,121)}; 170-cell collar and 55-copy insertion cuts retain reset guards.')

# Exact phase-3 paired-insertion controls at every step, with both centre parities.
for q,k,J,U0,C in [(14,100,(8,2,16),Us[3],(10,)),(20,160,(1,18,0,9),Us[21],(8,8))]:
    pw0=make_source(3,q,k,J,U0,C);pw1=make_source(3,q+1,k,J,U0,C)
    pu0=make_source(3,q,k,J,U0,C);pu1=make_source(3,q,k+1,J,U0,C)
    u=U0;cW=52;cU=34+9*q+len(J)+165
    for t in range(121):
        ph=(3+t)%12
        assert pw1==insert_pairword(pw0,W[ph],cW),(q,k,t,'phase-3 W insertion')
        assert pu1==insert_pairword(pu0,u,cU),(q,k,t,'phase-3 U insertion')
        if t<120:
            pw0,g0=full_pair_step(pw0);pw1,g1=full_pair_step(pw1)
            pu0,g2=full_pair_step(pu0);pu1,g3=full_pair_step(pu1)
            assert g0==g1==g2==g3==gamma[ph],(q,k,t,'insertion clock')
            u=bulk_step(u,gamma[ph])
print('PASS: phase-3 paired W/U insertions commute through t=0..120 in two full-word controls.')

# Independent true-integer and digit-array arithmetic controls across q widths.
controls=[(20,20,(0,1,18),Us[0],(0,0)),(40,40,(18,0,9),Us[7],(10,10,10)),(80,80,(5,9,2,9),Us[17],(4,12,4)),(160,160,(12,0,9,18),Us[29],(8,8))]
for q,k,J,U,C in controls:
    P=make_source(3,q,k,J,U,C);d=digits_from_pair(P);n=integer_from_digits(d)
    assert pair_from_digits(d)==P
    for t in range(120):
        n2=reverse_add_bigint(n)
        d2=digit_array_step(d)
        assert integer_from_digits(d2)==n2,(q,k,t,'bigint/digit mismatch')
        P2,g=full_pair_step(P)
        assert pair_from_digits(d2)==P2,(q,k,t,'pairword/digit mismatch')
        assert g==gamma[(3+t)%12],(q,k,t,'clock mismatch')
        n,d,P=n2,d2,P2
print('PASS: 4 q/k widths (20,40,80,160), 120 true reverse-add steps each, even and odd centres; Python bigint, digit-array, pairword, and phase-3 overflow agree.')
