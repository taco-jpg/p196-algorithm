#!/usr/bin/env python3
"""All-width mod-9 P=42 root obstruction for primitive reflective decimal p21/m3 bulk.
Exhaustive 19^3 rows. No external modules or state caps.
"""
from collections import Counter
from itertools import product
B,M,G=10,3,'001001010101001010101'
P=2*len(G)
assert pow(2,P,9)==1 and G.count('1')==9
W=[pow(2,-t,9) for t in range(P)]

def anchored(r,g):
    if r==(9,9,9):return None
    z=next(i for i,v in enumerate(r) if v!=9)
    a=[0]*3;d=[0]*3
    a[(z+1)%3]=d[(z-1)%3]=int(r[z]>=10)
    for j in (1,2):
        i=(z+j)%3;a[(i+1)%3]=(r[i]+a[i])//10
        i=(z-j)%3;d[(i-1)%3]=(r[i]+d[i])//10
    e=[(r[i]+a[i])%10 for i in range(3)]
    f=[(r[i]+d[i])%10 for i in range(3)]
    return tuple(e[i]+f[(i-g)%3] for i in range(3)),a,d

def fixed_carries(r):
    answer=[]
    for reverse in (False,True):
        good=[]
        for init in (0,1):
            c=init;z=[0]*3
            for j in range(3):
                i=(-j)%3 if reverse else j
                z[i]=c;c=(r[i]+c)//10
            if c==init:good.append(z)
        assert len(good)==1
        answer.append(good[0])
    return answer

def independent(r,g):
    if r==(9,9,9):return None
    a,d=fixed_carries(r)
    return tuple((r[i]+a[i])%10+(r[(i-g)%3]+d[(i-g)%3])%10
                 for i in range(3)),a,d

def block(r):
    for z in G:
        a=anchored(r,int(z))
        if a is None:return None
        r=a[0]
    return r

def cycles(nodes):
    done=set();out=[]
    for r in nodes:
        if r in done:continue
        path=[];index={};u=r
        while u is not None and u not in done and u not in index:
            index[u]=len(path);path.append(u);u=block(u)
        if u in index:out.append(path[index[u]:])
        done.update(path)
    return out

def mirror(r):
    return any(all(r[i]==r[(axis-i)%3] for i in range(3)) for axis in range(3))

def cuts(r):
    rec=[]
    for t in range(P):
        g=int(G[t%21])
        v=anchored(r,g);z=independent(r,g)
        assert v is not None and v==z
        r2,a,d=v
        c=[]
        for k in range(3):
            L=a[k];H=(r[k]+d[k])//10
            Y=(r[(k-1)%3]+d[(k-1)%3])%10 if g else 0
            c.append((L,H,Y))
        for k in range(3):
            L,H,Y=c[k];Lp,Hp,Yp=c[(k+1)%3];x=r[k]
            assert (x+L)%10+(Y if g else (x+Hp)%10)==r2[k]
            assert (x+L)//10==Lp and (x+Hp)//10==H
            if g:assert (x+Hp)%10==Yp
        rec.append((c,g));r=r2
    return rec,r

def q(rec,k):
    return sum(W[t]*(v[k][0]-v[k][1]+g*v[k][2])
               for t,(v,g) in enumerate(rec))%9

def main():
    rows=list(product(range(19),repeat=3))
    for r in rows:
        for g in (0,1):assert anchored(r,g)==independent(r,g)
    cy=cycles(rows)
    assert len(cy)==52 and Counter(map(len,cy))=={1:2,2:37,5:6,6:4,8:3}
    charge=Counter();n=0
    for c in cy:
        if len(c)!=2 or len(set(c[0]))==1 or not mirror(c[0]):continue
        for r in c:
            rec,last=cuts(r);assert last==r
            qs=[q(rec,k) for k in range(3)]
            assert qs[0]==qs[1]==qs[2] and qs[0] in (3,6)
            charge[qs[0]]+=1
            for shift in range(P):
                assert q(rec[shift:]+rec[:shift],0) in (3,6)
            n+=1
    assert n==30 and charge=={3:15,6:15}
    print('PASS: rows=6859, independent_carry_controls=13718')
    print('PASS: 15 primitive reflective temporal-42 cycles, 30 phase starts')
    print('PASS: Q3=15 Q6=15; 1260 nonzero time-rotated charges')
    print('PAPER PROOF: root Q=0, edge Q conserved; temporal-42 root reachability excluded at all widths')
    print('UNDECIDED: repetitions n divisible by 3, spatial-m3 temporal-168 family')
if __name__=='__main__':main()
