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
    p=Path('calculation/decimal_frontier/lattice_formats/agent14_onebit_rec0.txt')
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
if __name__=='__main__':main()
