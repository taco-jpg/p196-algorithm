#!/usr/bin/env python3
"""AC16 physical bigint, full-pairword vs collar, cone and band insertion audit.
Run from repository root. This is an INDEPENDENT check of the shared C++ engine.
"""
from pathlib import Path
from random import Random
import sys
sys.set_int_max_str_digits(0)
rows=Path("calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt").read_text().splitlines()
assert tuple(map(int,rows[0].split()))==(12,34,9,10)
G=tuple(map(int,rows[1].split()))
W=[tuple(map(int,rows[2+i].split())) for i in range(12)]
B=[tuple(map(int,rows[26+i].split())) for i in range(12)]
US=sorted({tuple((9,a,18-a)[(r+j)%3] for j in range(3))
           for a in range(0,19,2) for r in range(3)})
assert len(US)==30

def bulk(w,g):
    n=len(w)
    for s in (0,1):
        a=[s]
        for x in w:a.append((x+a[-1])//10)
        if a[-1]==s:break
    else:raise AssertionError("low cyclic carry")
    for s in (0,1):
        b=[0]*(n+1);b[n]=s
        for i in range(n-1,-1,-1):b[i]=(w[i]+b[i+1])//10
        if b[0]==s:break
    else:raise AssertionError("high cyclic carry")
    return tuple((w[i]+a[i])%10 +
                 ((w[(i-1)%n]+b[i]) if g else (w[i]+b[i+1]))%10
                 for i in range(n))

def source(q,k,j,u,c):
    h=list(B[7])+list(W[7])*q+list(j)+list(u)*k
    return h+list(c)+h[::-1]

def pair_step(p):
    d=[];carry=0
    for x in p:
        z=x+carry;d.append(z%10);carry=z//10
    if carry:d.append(carry)
    return [d[i]+d[-1-i] for i in range(len(d))],carry

def local_step(h,u,ustart,g):
    n=len(h);low=[];carry=0
    for x in h:
        z=x+carry;low.append(z%10);carry=z//10
    state=None
    for j in range(3):
        x=u[(n+j-ustart)%3]
        if x!=9:state=int(x>=10);break
    assert state is not None
    high=[0]*n
    for i in range(n-1,-1,-1):
        if g:
            if h[i]!=9:state=int(h[i]>=10)
            high[i]=state
        else:
            high[i]=state
            if h[i]!=9:state=int(h[i]>=10)
    if g:return [low[i]+(1 if i==0 else (h[i-1]+high[i])%10) for i in range(n)]
    return [low[i]+(h[i]+high[i])%10 for i in range(n)]

def digits(p):
    d=[0]*len(p)
    for i in range(len(p)//2):
        lo=min(9,p[i]);hi=p[i]-lo
        if i==0 and hi==0:lo-=1;hi=1
        d[i]=lo;d[-1-i]=hi
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]>0
    return d

def digit_step(d):
    out=[];carry=0
    for i in range(len(d)):
        z=d[i]+d[-1-i]+carry
        out.append(z%10);carry=z//10
    if carry:out.append(carry)
    return out

def insert(p,w,cut):
    return p[:cut]+list(w)+p[cut:len(p)-cut]+list(w)[::-1]+p[len(p)-cut:]

def main():
    assert all(G[i]==int(B[i][0]>=10) and
               bulk(W[i],G[i])==W[(i+1)%12] for i in range(12))
    losses=set()
    for u in US:
        phase=[u]
        for t in range(120):phase.append(bulk(phase[-1],G[(7+t)%12]))
        assert phase[-1]==u
        l=r=0
        for t in range(120):
            row=phase[t]
            l+=1+int(row[l%3]==9)
            r+=1+int(row[(-r-1)%3]==9)-G[(7+t)%12]
        losses.add((l,r))
    assert losses=={(149,120),(150,119),(151,121)}
    cut=34+9*14;old=cut
    for t in range(120):
        w=W[(7+t)%12];extra=0
        while w[(cut-35-extra)%9]==9:extra+=1
        cut-=1+extra-G[(7+t)%12]
    assert old-cut==91
    assert 170-max(x[0] for x in losses)==19
    assert 300+3-170-max(x[1] for x in losses)==12
    print("PASS: phase-7 W loss=91, U cones",sorted(losses),"positive collar margins")

    rng=Random(161607)
    for case in range(120):
        j=tuple(rng.randrange(19) for _ in range(3+case%2))
        u=US[rng.randrange(30)]
        c=(4,14,4) if case%2 else (4,4)
        p=source(14,100,j,u,c)
        cap=34+9*14+170;prefix=p[:cap];row=u
        for t in range(120):
            nextp,g=pair_step(p)
            assert g==G[(7+t)%12]
            nxt=local_step(prefix,row,34+9*14+len(j),g)
            assert nxt==nextp[:cap],("collar",case,t)
            prefix=nxt;p=nextp;row=bulk(row,g)
        assert row==u
        target=source(14,105,j,u,c)
        assert len(p)==len(target)
        assert p[:160]!=target[:160]
    print("PASS: 120 deterministic random full-word/collar cases, both centre parities, all 120 phases")

    controls=[(14,100,(0,0,0),US[0],(4,4)),
              (20,80,(1,17,9),US[11],(4,14,4)),
              (40,160,(17,0,9,18),US[19],(4,4)),
              (80,320,(8,9,2),US[26],(4,14,4)),
              (160,640,(12,0,9,18),US[29],(4,4))]
    for q,k,j,u,c in controls:
        d=digits(source(q,k,j,u,c))
        n=int("".join(map(str,d[::-1])))
        for t in range(120):
            n2=n+int(str(n)[::-1])
            d2=digit_step(d)
            assert n2==int("".join(map(str,d2[::-1])))
            assert len(d2)-len(d)==G[(7+t)%12]
            n,d=n2,d2
        end=[d[i]+d[-1-i] for i in range(len(d))]
        assert end[:34+9*q]!=source(q,k+5,j,u,c)[:34+9*q]
    print("PASS: genuine Python bigint / independent digit-array 120-step controls q=14,20,40,80,160")

    for q,k,j,u,c in [(14,100,(1,2,3),US[0],(4,4)),
                      (20,160,(8,2,16,9),US[21],(4,14,4))]:
        a=source(q,k,j,u,c);ap=source(q+1,k,j,u,c)
        b=source(q,k,j,u,c);bp=source(q,k+1,j,u,c)
        row=u
        for t in range(121):
            assert ap==insert(a,W[(7+t)%12],52),("W insertion",t)
            assert bp==insert(b,row,34+9*q+len(j)+165),("U insertion",t)
            if t<120:
                a,g0=pair_step(a);ap,g1=pair_step(ap)
                b,g2=pair_step(b);bp,g3=pair_step(bp)
                assert g0==g1==g2==g3==G[(7+t)%12]
                row=bulk(row,g0)
        assert row==u
    print("PASS: all 120 physical edges commute with paired W/U insertion in both parity controls")
    print("AC16_VALIDATION_PASS")

if __name__=="__main__":
    main()
