#!/usr/bin/env python3
"""Independent integer-only proof checker, plus base9/base13 positive controls.
Run from repository root: python3 calculation/decimal_frontier/lattice_formats/code/agent14_onebit_independent.py
No Fraction, Sympy, linear solver, or primary source import.
"""
import math,json,re
from pathlib import Path
M=20;G=(1,0)*4
R=Path('calculation/decimal_frontier/lattice_formats')
def check_kernel():
    lines=(R/'hamming4/kernel.txt').read_text().splitlines()
    D=int(lines[0]);v=list(map(int,lines[1].split(',')))
    assert len(v)==M and D>0
    for j in range(M):
        F=16*sum((1,4,6,4,1)[r]*v[(j-r)%M] for r in range(5))
        assert v[j]-F==(D if j==0 else 0)
    assert math.gcd(D,*v)==1
    return D,v
def get_rows():
    txt=(R/'hamming4/rows.txt').read_text().splitlines()
    W=[[int(c,19) for c in row] for row in txt]
    assert len(W)==8 and all(len(r)==M for r in W)
    return {'rec0':W,'rec1':[[W[(t-6)%8][(j-5)%M] for j in range(M)] for t in range(8)]}
def baseline(w):
    a=[];d=[]
    for start in (0,1):
        c=start;vs=[]
        for val in w:vs.append(c);c=(val+c)//10
        if c==start:a.append(vs)
        x=[0]*M;x[-1]=start
        for j in range(M-2,-1,-1):x[j]=(w[j+1]+x[j+1])//10
        if (w[0]+x[0])//10==start:d.append(x)
    assert len(a)==len(d)==1
    return a[0],d[0]
def residues(A,B,D):
    g=math.gcd(A,D)
    if B%g:return None
    m=D//g
    if m==1:return 0,1
    return (-B//g)*pow(A//g,-1,m)%m,m
def recurrences(a,d):
    v=[0]*M;u=[0]*M
    for t in range(8):
        newV=[];newU=[]
        for j in range(M):
            k=(j-G[t])%M
            newV.append(v[j]+v[k]+a[t][j]+d[t][k])
            newU.append(u[j]+u[k]-a[t][(j+1)%M]-d[t][(k-1)%M])
        v,u=newV,newU
    return v,u
def classify(name,W,D,K):
    base=[baseline(w) for w in W];counts={'first':0,'second':0,'pair':0}
    for side in range(2):
        for time in range(8):
            for col in range(M):
                a=[[int(z) for z in row[0]] for row in base]
                d=[[int(z) for z in row[1]] for row in base]
                (a if side==0 else d)[time][col]^=1
                v,u=recurrences(a,d)
                A0=sum(K[(-k)%M]*u[k] for k in range(M))
                B0=sum(K[(-k)%M]*v[k] for k in range(M))
                r0=residues(A0,B0,D)
                if r0 is None:counts['first']+=1;continue
                A1=sum(K[(1-k)%M]*u[k] for k in range(M))
                B1=sum(K[(1-k)%M]*v[k] for k in range(M))
                r1=residues(A1,B1,D)
                if r1 is None:counts['second']+=1;continue
                assert (r0[0]-r1[0])%math.gcd(r0[1],r1[1])!=0,(name,side,time,col,r0,r1)
                counts['pair']+=1
    print(name,'independent exact-integer obstruction',counts)
    return counts
def step(P,b):
    carry=0;O=[]
    for z in P:
        q=z+carry;O.append(q%b);carry=q//b
    if carry:O.append(carry)
    return [O[i]+O[-1-i] for i in range(len(O))],carry
def controls():
    cert=json.loads((R/'cert_b9_rec0.json').read_text())
    assert cert['base']==9 and cert['nB']==61 and cert['m']==4
    size=cert['l0']
    for t in range(10):
        B=cert['B_t'][t];w=cert['w_t'][t]
        P=B+[w[i%4] for i in range(size)]+B[::-1]
        U,g=step(P,9);assert g==cert['gam'][t]
        size+=g
        B2=cert['B_t'][(t+1)%10];w2=cert['w_t'][(t+1)%10]
        assert U==B2+[w2[i%4] for i in range(size)]+B2[::-1]
    print('POSITIVE base9 g1100011000 m4 |B|61: 10/10')
    for file,sz,start in [('Base13.lean',75,16),('Base13b.lean',55,8)]:
        source=(Path('lean/P196/AbsorbingBand')/file).read_text()
        B={int(k):[int(x) for x in nums.split(',')] for k,nums in re.findall(r'def B(\d+) : List Nat := \[([^\]]+)\]',source)}
        assert len(B)==10 and all(len(row)==sz for row in B.values())
        size=100;gam=[]
        for t in range(10):
            w=start if t%2==0 else 24-start
            U,g=step(B[t]+[w]*size+B[t][::-1],13)
            gam.append(g);size+=g
            w2=start if (t+1)%2==0 else 24-start
            assert U==B[(t+1)%10]+[w2]*size+B[(t+1)%10][::-1]
        assert gam==[1,0,1,0,0,1,0,0,0,0]
        print(f'POSITIVE base13 g1010010000 |B|{sz}: 10/10')
def main():
    D,K=check_kernel();W=get_rows()
    out={name:classify(name,rows,D,K) for name,rows in W.items()}
    assert out=={'rec0':{'first':94,'second':56,'pair':170},'rec1':{'first':90,'second':55,'pair':175}}
    controls()
    print('ALL 640 ONE-BIT NO-GO CASES & POSITIVE CONTROLS PASSED')



# Independent rational matrix inversion, impulse response, and real-base witnesses.
from fractions import Fraction
from itertools import combinations
from math import comb

def _inverse_h3():
    table=[]
    for i in range(M):
        row=[Fraction(int(i==j)) for j in range(M)]
        for k,c in enumerate((1,4,6,4,1)):row[(i-k)%M]-=16*c
        table.append(row+[Fraction(int(i==j)) for j in range(M)])
    for i in range(M):
        other=next(j for j in range(i,M) if table[j][i])
        table[i],table[other]=table[other],table[i]
        z=table[i][i];table[i]=[x/z for x in table[i]]
        for j in range(M):
            if j==i:continue
            z=table[j][i]
            if z:table[j]=[a-z*b for a,b in zip(table[j],table[i])]
    return [row[M:] for row in table]

_HINV=_inverse_h3()

def _numeric(u,v,D):
    A=[];B=[]
    for i in range(M):
        a=D*sum(_HINV[i][j]*u[j] for j in range(M))
        b=D*sum(_HINV[i][j]*v[j] for j in range(M))
        assert a.denominator==b.denominator==1
        A.append(int(a));B.append(int(b))
    return tuple(A),tuple(B)

def _impulse(side,t0,j0,ref):
    p=[0]*M;q=[0]*M
    sign=1-2*ref[t0][side][j0]
    for t,g in enumerate(G):
        P=[p[j]+p[(j-g)%M] for j in range(M)]
        Q=[q[j]+q[(j-g)%M] for j in range(M)]
        if t==t0:
            if side==0:P[j0]+=sign;Q[(j0-1)%M]-=sign
            else:P[(j0+g)%M]+=sign;Q[(j0+g+1)%M]-=sign
        p,q=P,Q
    return q,p

def _merge(x,y):
    a,m=x;b,n=y;g=math.gcd(m,n)
    if (b-a)%g:return None
    z=n//g
    u=((b-a)//g*pow(m//g,-1,z))%z if z>1 else 0
    return (a+m*u)%(m*z),m*z

def _no_base(A,B,mask,ref,D):
    C=[(aa.copy(),dd.copy()) for aa,dd in ref]
    for q in mask:C[(q%160)//M][q//160][q%M]^=1
    u=list(A);v=list(B)
    for t,g in enumerate(G):
        aa,dd=C[t]
        for j in range(M):
            X=[(u[j],v[j]),(2*D-u[j],-2*D-v[j])]
            for inc,out in ((aa[j],aa[(j+1)%M]),(dd[j],dd[(j-1)%M])):
                X.append((D-u[j],-v[j]-D*(1+inc)) if out==0 else (u[j]-D,v[j]+D*inc))
            if any(s<=0 and 2*s+c<0 for s,c in X):return True
        u=[u[j]+u[(j-g)%M]-D*(aa[(j+1)%M]+dd[(j-g-1)%M]) for j in range(M)]
        v=[v[j]+v[(j-g)%M]+D*(aa[j]+dd[(j-g)%M]) for j in range(M)]
    assert u==list(A) and v==list(B)
    return False


from exception import contradiction
import os
def hamming4_independent(name,source,D):
    ref=[baseline(row) for row in source]
    v0,u0=recurrences([x[0] for x in ref],[x[1] for x in ref])
    A0,B0=_numeric(u0,v0,D)
    impulses=[]
    for side in range(2):
        for t in range(8):
            for j in range(20):
                impulses.append(_numeric(*_impulse(side,t,j,ref),D))
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
                return (A0[j]+sum(impulses[z][0][j] for z in mask),
                        B0[j]+sum(impulses[z][1][j] for z in mask))
            a0,b0=val(0);a1,b1=val(1)
            if (a0*b1-a1*b0)%D:continue
            counts[1]+=1
            r=residues(a0,b0,D);s=residues(a1,b1,D)
            if r is None or s is None:continue
            r=_merge(r,s)
            if r is None:continue
            counts[2]+=1
            A=[];B=[]
            for j in range(20):
                aa,bb=val(j)
                if j>=2:
                    q=residues(aa,bb,D)
                    if q is None:break
                    r=_merge(r,q)
                    if r is None:break
                A.append(aa);B.append(bb)
            else:
                counts[3]+=1
                if _no_base(A,B,mask,ref,D):counts[4]+=1
                elif contradiction(name,mask,A,B,source,D,baseline):counts[4]+=1
                else:raise AssertionError((name,mask))
        total=[x+y for x,y in zip(total,counts)]
        print('INDEPENDENT CHECKPOINT',name,i,*counts,flush=True)
    expected={'rec0':[428761520,221226,137575,16631,16631],
              'rec1':[428761520,219985,137013,16631,16631]}
    print('INDEPENDENT TOTAL',name,start,stop,*total,flush=True)
    if start==0 and stop==320:assert total==expected[name],(name,total)
if __name__=='__main__':
    D,_=check_kernel()
    for name,source in get_rows().items():hamming4_independent(name,source,D)
    controls()
