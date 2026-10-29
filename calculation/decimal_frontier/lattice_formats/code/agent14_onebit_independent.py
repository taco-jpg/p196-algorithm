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
    lines=(R/'agent14_onebit_kernel.txt').read_text().splitlines()
    D=int(lines[0]);v=list(map(int,lines[1].split(',')))
    assert len(v)==M and D>0
    for j in range(M):
        F=16*sum((1,4,6,4,1)[r]*v[(j-r)%M] for r in range(5))
        assert v[j]-F==(D if j==0 else 0)
    assert math.gcd(D,*v)==1
    return D,v
def get_rows():
    txt=(R/'agent14_onebit_rec0.txt').read_text().splitlines()
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
if __name__=='__main__':main()
