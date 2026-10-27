#!/usr/bin/env python3
"""General-base neutral-interface normal form (Agent 7, T1).

Standalone exact digit arithmetic + optional positive source controls parsed from
Lean 4 certificate definitions when run inside the actual p196 repo.
Does NOT use Lean or establish any new Lychrel certificate.
"""
from itertools import product
from pathlib import Path
import re


def norm(b,w,e):
    d=[]
    for z in w:
        d.append((z+e)%b)
        e=(z+e)//b
    return d,e

def raw(b,B,C):
    h=b-1
    db,e=norm(b,B,0)
    dc,f=norm(b,C,e)
    dr,g=norm(b,B[::-1],f)
    assert e in (0,1) and f in (0,1) and g in (0,1)
    x=h*(1-e);y=h*(1-f)
    if g:
        wB=[a+c for a,c in zip(db+[x],[1]+dr[::-1])]
        dc=dc+[y]
    else:
        wB=[a+c for a,c in zip(db,dr[::-1])]
    wC=[a+c for a,c in zip(dc,dc[::-1])]
    return e,f,g,wB,wC

def stripB(b,B):
    a=0
    while a<len(B) and B[-1-a]==b-1:a+=1
    return a,B[:len(B)-a]

def stripC(b,C):
    a=0
    while 2*a<len(C) and C[a]==C[-1-a]==b-1:a+=1
    return a,C[a:len(C)-a]

def threshold(b):
    return (b-2)//2,(b-2)%2,(3*b-1)//2,(3*b-1)%2

def bound_checks():
    nb=nc=0
    for b in range(2,13):
        h=b-1;lo,tlo,hi,thi=threshold(b)
        for n in range(4):
            for tup in product(range(2*h+1),repeat=n):
                B=list(tup)
                if B and B[0]==0:continue
                e=norm(b,B,0)[1]
                # A single center digit b (resp. 0) flips incoming carry 0 (resp. 1).
                C=[b] if e==0 else [0]
                e,f,g,nB,nC=raw(b,B,C)
                assert f==1-e
                for a in range(3):
                    ea,fa,ga,ba,ca=raw(b,B+[h]*a,C)
                    assert (ea,fa,ga)==(e,f,g)
                    assert ba==nB+[h]*a
                    nb+=1
                if not B or B[-1]!=h:
                    if nB and nB[-1]==h:
                        assert g==0 and B and (e,B[-1]) in ((0,lo),(1,hi)),(b,B,e,g,nB)
        for n in range(1,5):
            for left in product(range(2*h+1),repeat=(n+1)//2):
                C=list(left)+list(left[:n//2][::-1])
                for e in (0,1):
                    B=[h+1] if e else [1]
                    # e1([1])=0 and e1([h+1])=1.
                    ee,f,g,nB,nC=raw(b,B,C)
                    assert ee==e
                    if f!=1-e:continue
                    for a in range(3):
                        ea,fa,ga,ba,ca=raw(b,B,[h]*a+C+[h]*a)
                        assert (ea,fa,ga)==(e,f,g)
                        assert ca==[h]*a+nC+[h]*a
                        nc+=1
                    if C[0]!=h and nC and nC[0]==h:
                        assert g==0 and (e,C[0]) in ((0,hi),(1,lo)),(b,C,e,g,nC)
    print('ALL CHECKS PASSED: general-base finite bound checks', 'B_pad',nb,'C_pad',nc)


def parse_named(src,b):
    values={}
    for m in re.finditer(r'def\s+(\w+)\s*:\s*List Nat\s*:=\s*\[([^\]]*)\]',src):
        values[m[1]]=[int(i.strip()) for i in m[2].split(',') if i.strip()]
    match=re.search(r'def cert'+str(b)+r'\s*:\s*List Edge\s*:=\s*(.*?)\n\ntheorem cert'+str(b)+r'_ok',src,re.S)
    assert match,('cert missing',b)
    edges=[]
    for m in re.finditer(r'⟨(\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\d+),\s*(\d+)⟩',match[1]):
        edges.append((values[m[1]],values[m[2]],values[m[3]],values[m[4]],int(m[5]),int(m[6])))
    assert edges
    return edges


def positive_control(b,es):
    assert es and es[-1][2:4]==es[0][:2]
    uOld=vOld=uNew=vNew=0
    phases=[]
    for B,C,B2,C2,u,v in es:
        e,f,g,nb,nc=raw(b,B,C)
        h=b-1
        assert e!=f
        assert nb==B2+[h]*u and nc==[h]*v+C2+[h]*v
        p,E=stripB(b,B);q,E2=stripB(b,B2)
        a,D=stripC(b,C);r,D2=stripC(b,C2)
        U=u+q-p;V=v+r-a
        assert U>=0 and V>=0
        ee,ff,gg,nb2,nc2=raw(b,E,D)
        assert (ee,ff,gg)==(e,f,g)
        assert nb2==E2+[h]*U and nc2==[h]*V+D2+[h]*V
        assert g==0 or (U==V==0)
        lo,tlo,hi,thi=threshold(b)
        if U:
            assert E and g==0 and (e,E[-1]) in ((0,lo),(1,hi))
        if V:
            assert D and g==0 and (e,D[0]) in ((0,hi),(1,lo))
        uOld+=u;vOld+=v;uNew+=U;vNew+=V
        phases.append((g,U,V))
    assert (uOld,vOld)==(uNew,vNew)
    print('positive Lean-source control base',b, 'edges',len(es),'passed', 'trim sums',uOld,vOld, 'normalized phases',phases)


def source_controls():
    root=Path(__file__).resolve().parents[2]
    p=root/'lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean'
    if p.exists():
        src=p.read_text(encoding='utf-8')
        for b in (11,17,26):positive_control(b,parse_named(src,b))
    else:
        print('source controls not mounted locally; run from repository checkout to test bases 11/17/26')

if __name__=='__main__':
    bound_checks()
    source_controls()
