#!/usr/bin/env python3
"""Independent 8-source calibration of Agent 7 neutral-normal-form arithmetic.

Reads the existing, Lean-checked source files, not the Python search mirror.
This script is a regression AUDIT, not a new proof or certificate checker.
"""
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
POWER=ROOT/'lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean'
KNOWN=ROOT/'lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean'

def coeff(s):
    return [int(v.strip()) for v in s.split(',') if v.strip()]

def original_edges(b, src):
    m=re.search(r'def cert'+str(b)+r'\s*:\s*List Edge\s*:=\s*(.*?)(?=\n\ndef cert\d+|\n\ntheorem)',src,re.S)
    if m is None:raise ValueError('cert missing for base '+str(b))
    body=m.group(1)
    edges=[]
    if b in (2,4,8,16,32):
        pat=r'⟨\[([^\]]*)\],\s*\[([^\]]*)\],\s*\[([^\]]*)\],\s*\[([^\]]*)\],\s*(\d+),\s*(\d+)⟩'
        for a in re.finditer(pat,body):
            edges.append((coeff(a[1]),coeff(a[2]),coeff(a[3]),coeff(a[4]),int(a[5]),int(a[6])))
    else:
        defs={}
        for a in re.finditer(r'def\s+(\w+)\s*:\s*List Nat\s*:=\s*\[([^\]]*)\]',src):
            defs[a[1]]=coeff(a[2])
        pat=r'⟨(\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\d+),\s*(\d+)⟩'
        for a in re.finditer(pat,body):
            edges.append((defs[a[1]],defs[a[2]],defs[a[3]],defs[a[4]],int(a[5]),int(a[6])))
    if not edges:raise ValueError('empty extracted edges at '+str(b))
    return edges

def norm(b,w,c):
    out=[]
    for z in w:
        out.append((z+c)%b)
        c=(z+c)//b
    return out,c

def blocks(b,B,C):
    h=b-1
    db,e=norm(b,B,0)
    dc,f=norm(b,C,e)
    dr,g=norm(b,B[::-1],f)
    x=h*(1-e);y=h*(1-f)
    rev=dr[::-1]
    nB=([a+v for a,v in zip(db+[x],[1]+rev)]
        if g else [a+v for a,v in zip(db,rev)])
    W=dc+[y] if g else dc
    nC=[a+v for a,v in zip(W,W[::-1])]
    return e,f,g,nB,nC

def strip_B(b,B):
    end=len(B)
    while end and B[end-1]==b-1:end-=1
    return len(B)-end,B[:end]

def strip_C(b,C):
    a=0
    while 2*a<len(C) and C[a]==b-1 and C[-1-a]==b-1:a+=1
    return a,C[a:len(C)-a]

def verify_cycle(b,es):
    old_u=old_v=new_u=new_v=overflow=0
    for i,(B,C,B2,C2,u,v) in enumerate(es):
        assert B2==es[(i+1)%len(es)][0] and C2==es[(i+1)%len(es)][1],(b,i,'not cyclic')
        e,f,g,nB,nC=blocks(b,B,C)
        h=b-1
        assert e!=f,(b,i,'bad flip')
        assert nB==B2+[h]*u,(b,i,'invalid original B edge')
        assert nC==[h]*v+C2+[h]*v,(b,i,'invalid original C edge')
        qb,E=strip_B(b,B);qr,F=strip_B(b,B2)
        ac,D=strip_C(b,C);ar,K=strip_C(b,C2)
        U=u+qr-qb;V=v+ar-ac
        assert U>=0 and V>=0,(b,i,'negative normalized trim')
        ee,ff,gg,nb,nc=blocks(b,E,D)
        assert (e,f,g)==(ee,ff,gg),(b,i,'carry/overflow mismatch')
        assert nb==F+[h]*U,(b,i,'invalid normalized B edge')
        assert nc==[h]*V+K+[h]*V,(b,i,'invalid normalized C edge')
        assert not g or (U==0 and V==0),(b,i,'trim on overflow')
        old_u+=u;old_v+=v;new_u+=U;new_v+=V;overflow+=g
    assert (old_u,old_v)==(new_u,new_v),(b,'gain not preserved')
    assert new_u==overflow and new_v*2==overflow,(b,'length balance')
    print('PASS base=%d edges=%d overflow=%d oldUV=%d/%d newUV=%d/%d' %
          (b,len(es),overflow,old_u,old_v,new_u,new_v))
    return len(es)

def main():
    a=POWER.read_text(encoding='utf-8')
    z=KNOWN.read_text(encoding='utf-8')
    n=0
    for b in (2,4,8,11,16,17,26,32):
        n+=verify_cycle(b,original_edges(b,a if b in (2,4,8,16,32) else z))
    assert n==56,n
    print('ALL EIGHT SOURCE-CERTIFICATE CONTROLS PASSED: 56 edges')

if __name__=='__main__':
    main()
