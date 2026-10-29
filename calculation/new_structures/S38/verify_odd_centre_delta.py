#!/usr/bin/env python3
"""Independent Python-bigint verifier for S38 odd-centre K-delta lemma.

Builds canonical decimal sources, verifies real n+reverse(n) against a separate
fresh-buffer schoolbook digit adder and coefficient normalization, then checks
the exact mod-101 five-copy carry-source identity. The finite grid is control
coverage only; all-width scope comes from the symbolic carry-reset proof.
"""
import itertools
import sys
sys.set_int_max_str_digits(0)

B = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W = [5,18,4,8,1,15,4,0,5]
MOD = 101

def md(x): return x % MOD
def xpow(i): return pow(-10, i, MOD)
def repeat(w, n): return w*n
def pairword(q,k,J,U,C):
    H = B + repeat(W,q) + J + repeat(U,k)
    return H + C + H[::-1]

def source_digits(P):
    assert P and P == P[::-1] and all(0 <= x <= 18 for x in P)
    n, h = len(P), len(P)//2
    d = [0]*n
    for i in range(h):
        d[i] = max(P[i]-9,0)
        d[n-1-i] = P[i]-d[i]
    if n%2:
        assert P[h]%2 == 0
        d[h] = P[h]//2
    assert d[-1] > 0 and all(0 <= x <= 9 for x in d)
    assert [d[i]+d[n-1-i] for i in range(n)] == P
    return d

def dec(ds): return ''.join(str(x) for x in ds[::-1]).lstrip('0') or '0'
def norm(P):
    carry, out, carry_out, K = 0, [], [], 0
    for i,x in enumerate(P):
        v = x + carry
        out.append(v % 10)
        carry = v // 10
        carry_out.append(carry)
        K = md(K + carry*xpow(i+1))
    if carry: out.append(carry)
    return {'digits':out,'carry_out':carry_out,'K':K,'gamma':carry}

def schoolbook(ds):
    carry, out = 0, []
    for i in range(len(ds)):
        v = ds[i] + ds[-1-i] + carry
        out.append(v%10)
        carry = v//10
    if carry: out.append(carry)
    return dec(out)

def block(w, incoming):
    c, a = incoming, 0
    for i,x in enumerate(w):
        c = (x+c)//10
        a = md(a + c*xpow(i+1))
    return c,a

def segment_K(carries, lo, hi):
    return md(sum(carries[i]*xpow(i+1) for i in range(lo,hi)))

def predict(q,k,J,U,C,old):
    V=U[::-1]
    a=len(B)+9*q+len(J)
    s=a+3*k
    t=s+len(C)
    z=t+3*k
    bu,bv=block(U,0)[0],block(V,0)[0]
    assert bu==block(U,1)[0] and bv==block(V,1)[0]
    AU=block(U,bu)[1]
    b=old['carry_out'][t-1]
    AV0, AVstar=block(V,b)[1],block(V,bv)[1]
    assert block(V,b)[0]==bv==block(V,bv)[0]
    KC=segment_K(old['carry_out'],s,s+len(C))
    KZ=segment_K(old['carry_out'],z,len(old['carry_out']))
    G=md(sum(pow(10,r,MOD) for r in range(k)))
    return md(xpow(s)*AU + 9*KC + xpow(t)*(9*AV0 + md(1-2*G)*AVstar) - 2*KZ)

def motifs():
    return sorted({tuple((lambda a,r: ([9,a,18-a][r:]+[9,a,18-a][:r]))(a,r))
                   for a in range(0,19,2) for r in range(3)})

def check_physical(P):
    ds=source_digits(P)
    n=int(dec(ds))
    big=str(n+int(str(n)[::-1]))
    school=schoolbook(ds)
    normalized=dec(norm(P)['digits'])
    assert big==school==normalized
    return norm(P)

def main():
    Us=motifs()
    assert len(Us)==30
    Js=[[5],[0,9,18],[4,12,4,12]]
    Cs=[[10],[2,4,2],[2,18,2]]
    base_widths=[20,40,80,160]
    q_phase=[20,21,22,23]
    k_phase=[40,41,42,43]
    cases=[]
    # Full 3x3 collar/centre cross-product at exact required widths.
    cases.extend(itertools.product(Us,Js,Cs,base_widths,base_widths))
    # Independent off-diagonal phase sweep: all 16 q/k mod-4 classes,
    # all U motifs, all J collars, and all odd-centre types.
    for U,J,C,q,k in itertools.product(Us,Js,Cs,q_phase,k_phase):
        if q in base_widths and k in base_widths:
            continue
        cases.append((U,J,C,q,k))
    checked=0
    for U,J,C,q,k in cases:
        assert len(C)%2==1 and C==C[::-1] and C[len(C)//2]%2==0
        P=pairword(q,k,J,list(U),C)
        P5=pairword(q,k+5,J,list(U),C)
        old=check_physical(P)
        nxt=check_physical(P5)
        assert old['gamma']==nxt['gamma']==1
        actual=md(nxt['K']-old['K'])
        predicted=predict(q,k,J,list(U),C,old)
        assert actual==predicted, (q,k,J,U,C,actual,predicted)
        checked+=1
    print(f'PASS: {checked} cases; 8,370 independent controls: all 3 J x 3 odd centres at every q,k pair in {20,40,80,160}, plus the off-diagonal 4x4 phase grid q=20..23, k=40..43 across all 30 U motifs, J collars, and odd centres.')
    print('Python arbitrary-precision n+reverse(n), fresh-buffer schoolbook addition, and coefficient normalization agree for both source and k+5 target.')
    print('Every predicted mod-101 carry-source delta equals direct K(P(q,k+5))-K(P(q,k)).')

if __name__=='__main__': main()
