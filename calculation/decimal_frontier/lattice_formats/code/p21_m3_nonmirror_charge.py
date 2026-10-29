#!/usr/bin/env python3
"""Complete decimal p21/m3 non-reflective bulk conserved-charge census."""
import sys
from itertools import product
from collections import Counter,defaultdict
from math import lcm
B,M,G=10,3,'001001010101001010101'
def step(row,bit):
    if row==(9,9,9):return None
    z=next(i for i in range(3) if row[i]!=9)
    a=[0]*3;d=[0]*3
    a[(z+1)%3]=d[(z-1)%3]=int(row[z]>=10)
    for j in (1,2):
        i=(z+j)%3;a[(i+1)%3]=(row[i]+a[i])//10
        i=(z-j)%3;d[(i-1)%3]=(row[i]+d[i])//10
    e=[(row[i]+a[i])%10 for i in range(3)]
    f=[(row[i]+d[i])%10 for i in range(3)]
    return tuple(e[i]+f[(i-bit)%3] for i in range(3)),a,d
def independent(row,bit):
    if row==(9,9,9):return None
    carry=[]
    for rev in (False,True):
        good=[]
        for init in (0,1):
            c=init;v=[0]*3
            for j in range(3):
                i=(-j)%3 if rev else j;v[i]=c;c=(row[i]+c)//10
            if c==init:good.append(v)
        assert len(good)==1,(row,good)
        carry.append(good[0])
    a,d=carry
    return tuple((row[i]+a[i])%10+(row[(i-bit)%3]+d[(i-bit)%3])%10 for i in range(3)),a,d
def block(row):
    for bit in G:
        v=step(row,int(bit))
        if v is None:return None
        row=v[0]
    return row
def cycles():
    seen=set();out=[]
    for r in product(range(19),repeat=3):
        if r in seen:continue
        path=[];index={};v=r
        while v is not None and v not in seen and v not in index:
            index[v]=len(path);path.append(v);v=block(v)
        if v in index:out.append(path[index[v]:])
        seen.update(path)
    return out
def symmetric(r):
    return any(all(r[i]==r[(axis-i)%3] for i in range(3)) for axis in range(3))
def canonical(c):
    n=len(c)
    return min(tuple(tuple(c[(j+t)%n][(i+s)%3] for i in range(3)) for j in range(n))
               for t in range(n) for s in range(3))
def verify(c):
    k=len(c);laps=lcm(k,2);P=21*laps
    assert pow(2,P,9)==1
    row=c[0];initial=row;Q=[0]*3;records=[]
    for t in range(P):
        bit=int(G[t%21]);z=step(row,bit)
        assert z is not None and z==independent(row,bit)
        nxt,a,d=z;cs=[]
        for j in range(3):
            L=a[j];H=(row[j]+d[j])//10;Y=(row[(j-1)%3]+d[(j-1)%3])%10 if bit else 0
            cs.append((L,H,Y));Q[j]+=pow(5,t,9)*(L-H+bit*Y)
        for j in range(3):
            L,H,Y=cs[j];Lp,Hp,Yp=cs[(j+1)%3]
            assert nxt[j]==(row[j]+L)%10+(Y if bit else (row[j]+Hp)%10)
            assert Lp==(row[j]+L)//10 and H==(row[j]+Hp)//10
            if bit:assert Yp==(row[j]+Hp)%10
        records.append((cs[0],bit));row=nxt
    assert row==initial and len({v%9 for v in Q})==1
    q=Q[0]%9
    for s in range(P):
        rot=records[s:]+records[:s]
        qs=sum(pow(5,t,9)*(v[0]-v[1]+bit*v[2]) for t,(v,bit) in enumerate(rot))%9
        assert (qs==0)==(q==0)
    return laps,q
def main():
    allrows=list(product(range(19),repeat=3))
    for r in allrows:
        for bit in (0,1):assert step(r,bit)==independent(r,bit)
    cs=cycles();assert len(cs)==52 and Counter(map(len,cs))=={1:2,2:37,5:6,6:4,8:3}
    nonsym=[c for c in cs if len(set(c[0]))>1 and not any(symmetric(r) for r in c)]
    assert len(nonsym)==28
    hist=Counter();group=defaultdict(list)
    for c in nonsym:
        laps,q=verify(c);hist[(len(c),q)]+=1
        group[canonical(c)].append((len(c),laps,q,c[0]))
    print('ROWS',len(allrows),'DIFFERENTIAL_CARRY_TESTS',len(allrows)*2)
    print('ALL_CYCLES',len(cs),'NONMIRROR_PRIMITIVE_CYCLES',len(nonsym),'FAMILIES',len(group))
    print('HIST',sorted(hist.items()))
    assert len(group)==12
    assert sum(n for (k,q),n in hist.items() if q!=0)==20
    assert sum(n for (k,q),n in hist.items() if q==0)==8
    assert sum(1 for _,v in group.items() if v[0][2]!=0)==8
    path=sys.argv[1] if len(sys.argv)>1 else '/tmp/agent8_p21_m3_nonmirror_cycles.txt'
    with open(path,'w') as f:
        f.write('# k lifts Q r0 r1 r2\n')
        for c in nonsym:
            laps,q=verify(c)
            f.write(f'{len(c)} {laps} {q} '+' '.join(map(str,c[0]))+'\n')
    print('PASS: 8/12 primitive nonsymmetric classes excluded; 4/12 undecided')
if __name__=='__main__':main()
