from random import Random
import sys
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
B=[1,5,10,12,13,10,3,7,14,11,4,2,3,9,15,7,9,15,11,14,13,13,14,5,5,13,11,11,9,5,10,10,4,5]
W=(10,14,13,12,9,7,10,4,5)
GAM=(1,0,0,0,1,0,0,0,1,0,0,0)
U6_0=(7,7,9,11,11,9)

def carries(w):
    m=len(w); a=b=None
    for s in (0,1):
        c=s; row=[]
        for x in w: row.append(c); c=(x+c)//10
        if c==s: a=row; break
    for s in (0,1):
        c=s; row=[0]*(m+1); row[m]=s
        for i in range(m-1,-1,-1): row[i]=(w[i]+row[i+1])//10
        if row[0]==s: b=row; break
    assert a is not None and b is not None
    return a,b

def bulk_step(w,g):
    a,b=carries(w); m=len(w); out=[]
    for i in range(m):
        lo=(w[i]+a[i])%10
        hi=((w[(i-1)%m]+b[i])%10) if g else ((w[i]+b[i+1])%10)
        out.append(lo+hi)
    return tuple(out)

def pair_step(P):
    d=[];c=0
    for x in P:
        z=x+c;d.append(z%10);c=z//10
    g=c
    if c:d.append(c)
    return [d[i]+d[-1-i] for i in range(len(d))],g

def source(q,k,J,U,C):
    h=B+list(W)*q+list(J)+list(U)*k
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

def number(d): return int(''.join(map(str,d[::-1])))
def step_digits(d):
    out=[];c=0;n=len(d)
    for i in range(n):
        z=d[i]+d[n-1-i]+c;out.append(z%10);c=z//10
    if c:out.append(c)
    return out

def local_step(H,U,ustart,g):
    n=len(H);low=[0]*n;high=[0]*n;c=0;state=None
    for j in range(6):
        x=U[(n+j-ustart)%6]
        if x!=9:state=int(x>=10);break
    assert state is not None
    for i,x in enumerate(H):z=x+c;low[i]=z%10;c=z//10
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

def insert(P,w,cut):return P[:cut]+list(w)+P[cut:len(P)-cut]+list(w)[::-1]+P[len(P)-cut:]
def make_c(length,seed):
    rng=Random(seed);h=[rng.randrange(19) for _ in range(length//2)]
    return tuple(h+[2*rng.randrange(10)]+h[::-1]) if length%2 else tuple(h+h[::-1])

U6_1=bulk_step(U6_0,GAM[0])
assert U6_1==(17,14,17,1,4,1)
cycle=[U6_1]
for t in range(24): cycle.append(bulk_step(cycle[-1],GAM[(1+t)%12]))
assert cycle[24]==U6_1 and len(set(cycle[:-1]))==24
row=U6_1
for t in range(240):row=bulk_step(row,GAM[(1+t)%12])
assert row==U6_1
assert sum(GAM[(1+t)%12] for t in range(240))==60
# Exact cone and W-loss bounds.
rows=[U6_1]
for t in range(240):rows.append(bulk_step(rows[-1],GAM[(1+t)%12]))
l=r=0
for t in range(240):
    u=rows[t];l+=1+int(u[l%6]==9);r+=1+int(u[(-r-1)%6]==9)-GAM[(1+t)%12]
assert (l,r)==(299,239)
w=W; m0=34+9*24; m=m0;max_loss=0
for t in range(240):
    r9=0
    while w[(m-35-r9)%9]==9:r9+=1
    m-=1+r9-GAM[(1+t)%12]
    max_loss=max(max_loss,m0-m)
    w=bulk_step(w,GAM[(1+t)%12])
assert max_loss==181 and w==W
assert (m0-52-max_loss)==17 and 330-l==31
print('U6_PHASE1_PASS',U6_1,'period=24','240-step return','overflows=60','cone=(299,239)','W_loss=181','W_insert_guard=17','U_insert_guard=31')

# Genuine decimal controls at q=40,80,160; k scaled, with both centre parities represented.
controls=[(40,100,(0,1,18),make_c(2,1)),(80,160,(18,0,9,5),make_c(5,2)),(160,320,(12,0,9),make_c(13,3))]
for q,k,J,C in controls:
    P=source(q,k,J,U6_1,C);d=realize(P);n=number(d)
    root=34+9*q;collar=320;M=root+collar;ustart=root+len(J);H=P[:M];u=U6_1
    for t in range(240):
        g=GAM[(1+t)%12];P2,g2=pair_step(P)
        assert g2==g,(q,k,t,'clock')
        H2=local_step(H,u,ustart,g)
        assert H2==P2[:M],(q,k,t,'local/full mismatch')
        n2=n+int(str(n)[::-1]);d2=step_digits(d)
        assert number(d2)==n2,(q,k,t,'bigint mismatch')
        assert [d2[i]+d2[-1-i] for i in range(len(d2))]==P2,(q,k,t,'digit/pair mismatch')
        assert len(d2)-len(d)==g,(q,k,t,'overflow')
        P,d,n,H,u=P2,d2,n2,H2,bulk_step(u,g)
    assert u==U6_1
    target=B+list(W)*q
    assert P[:34]==B
    restored=P[:len(target)]==target
    print('U6_BIGINT_CONTROL',q,k,'J',J,'U6',U6_1,'C_len',len(C),'W_prefix_restored',restored)
    print('U6_CONTROL_PASS',q,k,'240 steps local/full-pairword/digit-array/bigint agree')

# Phase-1 insertion identities for q=24,k=100 and q=40,k=160, every step of the 240-step epoch.
for q,k,J,C in [(24,100,(0,1,18),make_c(2,11)),(40,160,(18,0,9),make_c(5,12))]:
    Pq=source(q,k,J,U6_1,C);Pq1=source(q+1,k,J,U6_1,C)
    Pk=source(q,k,J,U6_1,C);Pk1=source(q,k+1,J,U6_1,C)
    w=W;u=U6_1;cW=52;cU=34+9*q+len(J)+330
    for t in range(241):
        assert Pq1==insert(Pq,w,cW),(q,k,t,'W insertion')
        assert Pk1==insert(Pk,u,cU),(q,k,t,'U insertion')
        if t<240:
            Pq,g0=pair_step(Pq);Pq1,g1=pair_step(Pq1)
            Pk,g2=pair_step(Pk);Pk1,g3=pair_step(Pk1)
            assert g0==g1==g2==g3==GAM[(1+t)%12],(q,k,t,'insertion clock')
            w=bulk_step(w,GAM[(1+t)%12]);u=bulk_step(u,GAM[(1+t)%12])
print('U6_PHASE1_INSERTION_PASS W/U insertion identities hold through t=0..240')
