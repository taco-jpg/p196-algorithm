#!/usr/bin/env python3
"""Complete all-base 1-carry-bit perturbation classification (p8/m20 rec0,rec1).
Run from repo root: python3 calculation/decimal_frontier/lattice_formats/code/agent14_onebit_main.py
Only Python standard library.
"""
import math,re
from pathlib import Path
from fractions import Fraction as F
G=(1,0)*4;M=20
def rows():
    p=Path('calculation/decimal_frontier/lattice_formats/hamming4/rows.txt')
    rr=[[int(x,19) for x in line] for line in p.read_text().splitlines() if line]
    assert len(rr)==8 and all(len(v)==M for v in rr)
    out={'rec0':rr,'rec1':[[rr[(t-6)%8][(j-5)%M] for j in range(M)] for t in range(8)]}
    canonical=Path('calculation/decimal_frontier/lattice_formats/p8_scc.txt').read_text().splitlines()
    for k,line in enumerate(x for x in canonical if x.startswith('SCC p=8')):
      if k>1:break
      cols=[[int(y) for y in z.split(',')] for z in re.findall(r'\[([0-9,]+)\]',line.split(' cyc=')[1])]
      assert len(cols)==M and [[c[t] for c in cols] for t in range(8)]==out[f'rec{k}']
    return out
def cyclic_carries(w):
    l=[];d=[]
    for z in (0,1):
        c=z;v=[]
        for P in w:v.append(c);c=int(P+c>=10)
        if c==z:l.append(v)
        R=[0]*M;R[-1]=z
        for j in range(M-2,-1,-1):R[j]=int(w[j+1]+R[j+1]>=10)
        if z==int(w[0]+R[0]>=10):d.append(R)
    assert len(l)==len(d)==1
    return l[0],d[0]
def inverse():
    h=[]
    for j in range(M):
        a=[F(0)]*M;a[j]=F(1)
        for k,c in enumerate((1,4,6,4,1)):a[(j-k)%M]-=16*c
        h.append(a+[F(int(i==j)) for i in range(M)])
    for i in range(M):
        z=next(j for j in range(i,M) if h[j][i])
        h[i],h[z]=h[z],h[i]
        v=h[i][i];h[i][i:]=[x/v for x in h[i][i:]]
        for j in range(M):
            if j!=i and h[j][i]:
                v=h[j][i];h[j][i:]=[x-v*y for x,y in zip(h[j][i:],h[i][i:])]
    return [x[M:] for x in h]
def rhs(a,d):
    c=[0]*M;s=[0]*M
    for t,g in enumerate(G):
        aa=a[t];dd=d[t]
        c=[c[j]+c[(j-g)%M]+aa[j]+dd[(j-g)%M] for j in range(M)]
        s=[s[j]+s[(j-g)%M]-aa[(j+1)%M]-dd[((j-g)%M-1)%M] for j in range(M)]
    return c,s
def solve1(u,v):
    den=math.lcm(u.denominator,v.denominator)
    a=int(u*den);z=int(v*den);g=math.gcd(a,den)
    if z%g:return None
    m=den//g
    if m==1:return 0,1
    return (-z//g)*pow(a//g,-1,m)%m,m
def crt(p,q):
    r,m=p;s,n=q;g=math.gcd(m,n)
    if (s-r)%g:return None
    k=n//g
    v=((s-r)//g*pow(m//g,-1,k))%k if k>1 else 0
    return (r+m*v)%(m*k),m*k
def main():
    H=inverse();counts={}
    for name,W in rows().items():
        base=[cyclic_carries(w) for w in W]
        why={'first':0,'second':0,'pair':0}
        for side in (0,1):
            for t in range(8):
                for j in range(M):
                    a=[list(x[0]) for x in base];d=[list(x[1]) for x in base]
                    (a if side==0 else d)[t][j]^=1
                    bc,bs=rhs(a,d)
                    c0=sum(H[0][k]*bc[k] for k in range(M));s0=sum(H[0][k]*bs[k] for k in range(M))
                    first=solve1(s0,c0)
                    if first is None:
                        why['first']+=1;continue
                    c1=sum(H[1][k]*bc[k] for k in range(M));s1=sum(H[1][k]*bs[k] for k in range(M))
                    second=solve1(s1,c1)
                    if second is None:why['second']+=1
                    else:
                        assert crt(first,second) is None,(name,side,t,j,first,second)
                        why['pair']+=1
        counts[name]=why
        print(name,why,'out of',2*8*M,'exact one-bit itineraries')
    assert counts=={'rec0':{'first':94,'second':56,'pair':170},'rec1':{'first':90,'second':55,'pair':175}},counts
    print('ALL 640 ALL-BASE INTEGER-NOGO CHECKS PASSED (first two coefficients only)')



# Complete radius-three stability search, after the independently checked one-bit framework above.
from itertools import combinations
from math import comb
_H3=Path('calculation/decimal_frontier/lattice_formats/hamming4')
_D=int((_H3/'kernel.txt').read_text().splitlines()[0])
_K=list(map(int,(_H3/'kernel.txt').read_text().splitlines()[1].split(',')))
assert len(_K)==M and all(_K[j]-16*sum(c*_K[(j-k)%M] for k,c in enumerate((1,4,6,4,1)))==(_D if j==0 else 0) for j in range(M))

def _coeff(a,d):
    v,u=rhs(a,d)
    return (tuple(sum(_K[(j-k)%M]*u[k] for k in range(M)) for j in range(M)),
            tuple(sum(_K[(j-k)%M]*v[k] for k in range(M)) for j in range(M)))

def _eq(A,B):
    gg=math.gcd(A,_D)
    if B%gg:return None
    m=_D//gg
    return ((-B//gg)*pow(A//gg,-1,m)%m if m>1 else 0),m

def _physical_exclusion(mask,source,A,B):
    C=[tuple(list(side) for side in cyclic_carries(w)) for w in source]
    for q in mask:
        side=q//160;t=(q%160)//M;j=q%M
        C[t][side][j]^=1
    u=list(A);v=list(B)
    for t,g in enumerate(G):
        aa,dd=C[t]
        for j in range(M):
            conditions=[(u[j],v[j]),(2*_D-u[j],-2*_D-v[j])]
            for incoming,outgoing in ((aa[j],aa[(j+1)%M]),(dd[j],dd[(j-1)%M])):
                if outgoing==0:conditions.append((_D-u[j],-v[j]-_D*(incoming+1)))
                else:conditions.append((u[j]-_D,v[j]+_D*incoming))
            if any((s<0 and 2*s+c<0) or (s==0 and c<0) for s,c in conditions):
                return True
        u=[u[j]+u[(j-g)%M]-_D*(aa[(j+1)%M]+dd[(j-g-1)%M]) for j in range(M)]
        v=[v[j]+v[(j-g)%M]+_D*(aa[j]+dd[(j-g)%M]) for j in range(M)]
    assert u==list(A) and v==list(B)
    return False


from exception import contradiction
import os
def hamming4(name,source):
    base=[carries(row) for row in source]
    a=[list(z[0]) for z in base];d=[list(z[1]) for z in base]
    U0,V0=_coeff(a,d)
    impulse=[]
    for q in range(320):
        aa=[z.copy() for z in a];dd=[z.copy() for z in d]
        (aa if q<160 else dd)[(q%160)//20][q%20]^=1
        u,v=_coeff(aa,dd)
        impulse.append((tuple(u[j]-U0[j] for j in range(20)),
                        tuple(v[j]-V0[j] for j in range(20))))
    start=int(os.environ.get('P196_H4_START','0'))
    stop=int(os.environ.get('P196_H4_STOP','320'))
    assert 0<=start<=stop<=320
    total=[0,0,0,0,0]
    for i in range(start,stop):
        counts=[0,0,0,0,0]
        for triple in combinations(range(i+1,320),3):
            mask=(i,)+triple
            counts[0]+=1
            def val(j):
                return (U0[j]+sum(impulse[z][0][j] for z in mask),
                        V0[j]+sum(impulse[z][1][j] for z in mask))
            a0,b0=val(0);a1,b1=val(1)
            if (a0*b1-a1*b0)%DEN:continue
            counts[1]+=1
            r=_eq(a0,b0);s=_eq(a1,b1)
            if r is None or s is None:continue
            r=combine(r,s)
            if r is None:continue
            counts[2]+=1
            A=[];B=[]
            for j in range(20):
                aa,bb=val(j)
                if j>=2:
                    q=_eq(aa,bb)
                    if q is None:break
                    r=combine(r,q)
                    if r is None:break
                A.append(aa);B.append(bb)
            else:
                counts[3]+=1
                if _physical_exclusion(mask,source,A,B):counts[4]+=1
                elif contradiction(name,mask,A,B,source,DEN,carries):counts[4]+=1
                else:raise AssertionError((name,mask))
        total=[x+y for x,y in zip(total,counts)]
        print('PRIMARY CHECKPOINT',name,i,*counts,flush=True)
    expected={'rec0':[428761520,221226,137575,16631,16631],
              'rec1':[428761520,219985,137013,16631,16631]}
    print('PRIMARY TOTAL',name,start,stop,*total,flush=True)
    if start==0 and stop==320:assert total==expected[name],(name,total)
if __name__=='__main__':
    for name,source in rows().items():hamming4(name,source)
