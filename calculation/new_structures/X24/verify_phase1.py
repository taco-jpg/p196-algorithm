from itertools import product
from random import Random
import sys
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)

B=[1,5,10,12,13,10,3,7,14,11,4,2,3,9,15,7,9,15,11,14,13,13,14,5,5,13,11,11,9,5,10,10,4,5]
W=[10,14,13,12,9,7,10,4,5]
GAM=[1,0,0,0,1,0,0,0,1,0,0,0]

def make_u(a,r):
    b=(9,a,18-a); return tuple(b[(r+i)%3] for i in range(3))
US=sorted({make_u(a,r) for a in range(0,19,2) for r in range(3)})

def bulk_carries(w):
    m=len(w); alpha=beta=None
    for s in (0,1):
        c=s; arr=[]
        for x in w: arr.append(c); c=(x+c)//10
        if c==s: alpha=arr; break
    for s in (0,1):
        c=s; arr=[0]*(m+1); arr[m]=c
        for i in range(m-1,-1,-1): arr[i]=(w[i]+arr[i+1])//10
        if arr[0]==s: beta=arr; break
    assert alpha is not None and beta is not None
    return alpha,beta

def bulk_step(w,g):
    a,b=bulk_carries(w); m=len(w); z=[]
    for i in range(m):
        lo=(w[i]+a[i])%10
        hi=((w[(i-1)%m]+b[i])%10) if g else ((w[i]+b[i+1])%10)
        z.append(lo+hi)
    return tuple(z)

def full_pair_step(P):
    d=[];c=0
    for x in P:
        z=x+c;d.append(z%10);c=z//10
    g=c
    if c: d.append(c)
    return [d[i]+d[-1-i] for i in range(len(d))],g

def make_source(q,k,J,U,C):
    h=B+W*q+list(J)+list(U)*k
    return h+list(C)+h[::-1]

def realize(P):
    assert P==P[::-1]
    n=len(P);d=[0]*n
    for i,x in enumerate(P[:n//2]):
        hi=min(9,x);d[i]=x-hi;d[n-1-i]=hi
    if n%2:
        assert P[n//2]%2==0
        d[n//2]=P[n//2]//2
    assert d[-1]>0
    return d

def integer_from_digits(d):
    return int(''.join(map(str,d[::-1])))

def digits_from_integer(n):
    return list(map(int,str(n)[::-1]))

def step_digits(d):
    out=[];c=0;n=len(d)
    for i in range(n):
        z=d[i]+d[n-1-i]+c;out.append(z%10);c=z//10
    if c:out.append(c)
    return out

def local_step(H,U,ustart,g):
    n=len(H); low=[0]*n; high=[0]*n; c=0
    state=None
    for j in range(3):
        x=U[(n+j-ustart)%3]
        if x!=9: state=int(x>=10);break
    assert state is not None
    for i,x in enumerate(H): z=x+c;low[i]=z%10;c=z//10
    for i in range(n-1,-1,-1):
        if not g:
            high[i]=state
            if H[i]!=9: state=int(H[i]>=10)
        else:
            if H[i]!=9: state=int(H[i]>=10)
            high[i]=state
    out=[]
    for i in range(n):
        if not g: out.append(low[i]+(H[i]+high[i])%10)
        elif i==0: out.append(low[i]+1)
        else: out.append(low[i]+(H[i-1]+high[i])%10)
    return out

def insert_pairword(P,w,cut):
    return P[:cut]+list(w)+P[cut:len(P)-cut]+list(w)[::-1]+P[len(P)-cut:]

def make_c(length,seed):
    rng=Random(seed);half=[rng.randrange(19) for _ in range(length//2)]
    if length%2: return tuple(half+[2*rng.randrange(10)]+half[::-1])
    return tuple(half+half[::-1])

assert len(US)==30
assert {bulk_step(u,GAM[0]) for u in US}==set(US), 'phase-0 to phase-1 U map is not a permutation of the 30 motifs'
# Check all U rows have the 120-step clock-phase return at phase 1.
for U0 in US:
    u=U0
    for t in range(120): u=bulk_step(u,GAM[(1+t)%12])
    assert u==U0
# Check local cone against full coefficient pairword and independent bigint/digit-array engines.
controls=[(20,100,(0,1,18),US[0],make_c(2,1)),(40,160,(18,0,9),US[7],make_c(5,2)),(80,320,(5,9,2,9),US[17],make_c(8,3)),(160,640,(12,0,9,18),US[29],make_c(13,4))]
for q,k,J,U0,C in controls:
    P=make_source(q,k,J,U0,C); d=realize(P); n=integer_from_digits(d)
    root=34+9*q; collar=170; M=root+collar; ustart=root+len(J)
    H=P[:M];U=U0
    for t in range(120):
        g=GAM[(1+t)%12]
        P2,g2=full_pair_step(P)
        assert g2==g,(q,k,t,g,g2)
        H2=local_step(H,U,ustart,g)
        assert H2==P2[:M],(q,k,t,'local/full prefix mismatch')
        n2=n+int(str(n)[::-1])
        d2=step_digits(d)
        assert integer_from_digits(d2)==n2,(q,k,t,'bigint/digit mismatch')
        Pfromdigits=[d2[i]+d2[-1-i] for i in range(len(d2))]
        assert Pfromdigits==P2,(q,k,t,'digit/pairword mismatch')
        assert len(d2)-len(d)==g,(q,k,t,'overflow mismatch')
        P,d,n,H,U=P2,d2,n2,H2,bulk_step(U,g)
    assert U==U0
    target=B+W*q
    assert P[:34]==B,(q,k,'root prefix changed')
    assert P[:len(target)]!=target,(q,k,'sample unexpectedly restores W9 endpoint')
    fm=next(i for i,(x,y) in enumerate(zip(P,target)) if x!=y)
    assert 34<=fm<len(target),(q,k,fm,'endpoint mismatch not inside W9')
    print('ENDPOINT_CONTROL',q,k,'first_mismatch_index',fm,'relative_to_WJ_cut',fm-len(target))
    print('CONTROL_PASS',q,k,'Jlen',len(J),'U',U0,'Clen',len(C),'120 phases local/full/bigint/digit-array agree')
# Cone bound at phase 1.
max_left=max_right=0; pairs=set()
for U0 in US:
    rows=[U0]
    for t in range(120): rows.append(bulk_step(rows[-1],GAM[(1+t)%12]))
    l=r=0
    for t in range(120):
        w=rows[t];l+=1+int(w[l%3]==9);r+=1+int(w[(2-r%3)%3]==9)-GAM[(1+t)%12]
    pairs.add((l,r));max_left=max(max_left,l);max_right=max(max_right,r)
print('CONE_PASS phase=1 pairs',sorted(pairs),'max_left',max_left,'max_right',max_right,'center_distance>=300')
print('INDEPENDENT_CHECKS_PASS U=30, phase-1 clock 120, 4 widths q/k=20,40,80,160')

# Phase-1 paired-insertion controls: W copy after two W blocks; U copy after 55 U blocks.
for q,k,J,U0,C in [(20,100,(0,1,18),US[0],make_c(2,11)),(40,160,(18,0,9),US[7],make_c(5,12))]:
    Pq=make_source(q,k,J,U0,C); Pq1=make_source(q+1,k,J,U0,C)
    Pk=make_source(q,k,J,U0,C); Pk1=make_source(q,k+1,J,U0,C)
    u=U0; w=W
    cW=52; cU=34+9*q+len(J)+165
    for t in range(121):
        ph=(1+t)%12
        assert Pq1==insert_pairword(Pq,w,cW),(q,k,t,'W insertion identity')
        assert Pk1==insert_pairword(Pk,u,cU),(q,k,t,'U insertion identity')
        if t<120:
            Pq2,g0=full_pair_step(Pq);Pq12,g1=full_pair_step(Pq1)
            Pk2,g2=full_pair_step(Pk);Pk12,g3=full_pair_step(Pk1)
            assert g0==g1==g2==g3==GAM[ph],(q,k,t,'insertion clock')
            Pq,Pq1,Pk,Pk1=Pq2,Pq12,Pk2,Pk12
            w=bulk_step(w,GAM[ph]);u=bulk_step(u,GAM[ph])
print('PHASE1_INSERTION_PASS representative q/k width pairs: exact W and U paired-insertion identities hold at t=0..120')
