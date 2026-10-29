#!/usr/bin/env python3
"""Independent fixed-point carry and physical-cut verifier of every m9 cycle record."""
from collections import Counter
import sys,math
G='001001010101001010101'
M=9;B=10
def one(r,g):
    if all(x==9 for x in r):return None
    ad=[]
    for rev in (False,True):
        matches=[]
        for cin in range(2):
            c=cin;d=[0]*M
            for j in range(M):
                i=(-j)%M if rev else j
                d[i]=c;c=(r[i]+c)//B
            if c==cin:matches.append(d)
        assert len(matches)==1,(r,rev,matches)
        ad.append(matches[0])
    a,d=ad
    e=[(r[i]+a[i])%B for i in range(M)]
    f=[(r[i]+d[i])%B for i in range(M)]
    return tuple(e[i]+f[(i-g)%M] for i in range(M)),a,d
def check(lines):
    hist=Counter();tested=0;units=0;triples=0;zero=0;phases=0
    for line in lines:
        if not line.strip() or line.startswith('#'):continue
        cells=list(map(int,line.split()));blocks,Qexpected=cells[:2];row=tuple(cells[2:]);assert len(row)==9
        assert blocks%2==0 and blocks>=2
        original=row;charges=[0]*9;records=[]
        for t in range(blocks*21):
            g=int(G[t%21]);step=one(row,g);assert step is not None
            after,a,d=step
            cut=[(a[j],(row[j]+d[j])//10,(row[(j-1)%9]+d[(j-1)%9])%10 if g else 0) for j in range(9)]
            for j in range(9):
                l,h,y=cut[j];lp,hp,yp=cut[(j+1)%9];x=row[j]
                assert (x+l)%10+(y if g else (x+hp)%10)==after[j]
                assert (x+l)//10==lp and (x+hp)//10==h
                if g:assert (x+hp)%10==yp
                charges[j]+=pow(5,t,9)*(l-h+g*y)
            records.append((cut[0],g))
            row=after;tested+=1
        assert row==original
        qq={v%9 for v in charges};assert qq=={Qexpected},(blocks,charges,Qexpected)
        for shift in range(blocks*21):
            rot=records[shift:]+records[:shift]
            q=sum(pow(5,t,9)*(l-h+g*y) for t,((l,h,y),g) in enumerate(rot))%9
            assert (q==0)==(Qexpected==0)
            phases+=1
        hist[(blocks,Qexpected)]+=1
        if Qexpected==0:zero+=1
        elif math.gcd(Qexpected,9)==1:units+=1
        else:triples+=1
    assert sum(hist.values())==23 and (zero,units,triples)==(5,12,6)
    assert sum(v for (k,q),v in hist.items() if k==2)==5
    print('independent checker PASS: cycles=23, zero=5, Q-unit=12, Q-order3=6')
    print('exact row steps=',tested,'temporal phase audits=',phases)
    for (k,q),n in sorted(hist.items()):print(f'  k={k} Q={q} count={n}')
if __name__=='__main__':check(open(sys.argv[1]))
