#!/usr/bin/env python3
"""Exact universal 33-edge decimal pumping identities for N0=(5346)^q, q>=8.
A word L+w^k+R (|w|=4) has rational-polynomial value A*10^(4k)+B;
the script compares exact integer numerators over common denominator 9999.
"""
D=10**4-1

def orbit(q,steps):
    s='5346'*q
    out=[s]
    for _ in range(steps):
        s=str(int(s)+int(s[::-1]));out.append(s)
    return out

def affine(L,w,R):
    assert len(w)==4
    nR=len(R); a=(D*int(L or '0')+int(w))*10**nR
    b=D*int(R or '0')-int(w)*10**nR
    return a,b

def coeffs(T):
    L,w,R=T
    return affine(L,w,R)

def reverse_coeffs(T):
    L,w,R=T
    return affine(R[::-1],w[::-1],L[::-1])

def synth():
    s8=orbit(8,33);s9=orbit(9,33)
    controls={q:orbit(q,33) for q in (10,11,100)}
    templates=[]
    for t,(s,u) in enumerate(zip(s8,s9)):
        candidates=[i for i in range(len(u)-3) if u[:i]+u[i+4:]==s]
        assert candidates,(t,s,u)
        p=min(candidates,key=lambda i:abs(i-len(u)//2))
        L,w,R=s[:p],u[p:p+4],s[p:]
        assert L+w+R==u
        for q,arr in controls.items():
            assert L+w*(q-8)+R==arr[t],(t,q)
        firstdiff=next((i for i in range(len(s)//2) if s[i]!=s[-i-1]),None)
        assert firstdiff is not None and firstdiff<min(len(L),len(R)),(t,L,w,R,firstdiff)
        templates.append((L,w,R))
    for t in range(33):
        a,b=coeffs(templates[t]);u,v=reverse_coeffs(templates[t]);c,d=coeffs(templates[t+1])
        assert (a+u,b+v)==(c,d),t
    L,w,R=templates[-1]
    assert w=='0000',(L,w,R)
    assert L.endswith('00')
    print('PAPER-PROOF CHECK: 33 exact rational-affine RAA identities in X=10^(4k)')
    print('33 edges universally sound for every integer k>=0 (q=k+8)')
    print('All 34 states nonpalindromic by a mismatch outside the pumped band')
    print('t33 L=',L,'R=',R,'band=00+0000^k')
    return templates
if __name__=='__main__':synth()
