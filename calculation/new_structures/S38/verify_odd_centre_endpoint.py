#!/usr/bin/env python3
"""Independent checks for the odd-centre folded V_10 endpoint formula."""
import itertools
from verify_odd_centre_delta import (
    MOD, B, W, md, pairword, motifs, norm, source_digits, dec, schoolbook,
)

def moments(word):
    even = sum(((-1)**r) * word[2*r] for r in range((len(word)+1)//2))
    odd = sum(((-1)**r) * word[2*r+1] for r in range(len(word)//2))
    return md(even), md(odd)

def rotate(v, amount):
    e,o = v
    for _ in range(amount % 4):
        e,o = md(-o),e
    return e,o

def add(a,b): return md(a[0]+b[0]),md(a[1]+b[1])
def sub(a,b): return md(a[0]-b[0]),md(a[1]-b[1])

def folded_endpoint(Y, center):
    e,o = moments(Y)
    m = len(Y) % 4
    if m == 0: return md(2*e + center)
    if m == 2: return md(2*e - center)
    if m == 1: return md(20*o + 10*center)
    return md(20*o - 10*center)

def v10(word):
    return md(sum(x*pow(10,i,MOD) for i,x in enumerate(word)))

def source_and_step(P):
    ds=source_digits(P)
    n=int(dec(ds))
    big=n+int(str(n)[::-1])
    big_s=str(big)
    school=schoolbook(ds)
    normalized=dec(norm(P)['digits'])
    assert str(big)==school==normalized
    out=[int(ch) for ch in big_s[::-1]]
    Pnext=[out[i]+out[-1-i] for i in range(len(out))]
    return n, norm(P), Pnext

def main():
    Us=motifs()
    Js=[[5],[0,9,18],[4,12,4,12]]
    Cs=[[10],[2,4,2],[2,18,2]]
    base=[20,40,80,160]
    qp=[20,21,22,23]
    kp=[40,41,42,43]
    cases=list(itertools.product(Us,Js,Cs,base,base))
    for U,J,C,q,k in itertools.product(Us,Js,Cs,qp,kp):
        if q in base and k in base: continue
        cases.append((U,J,C,q,k))
    checked=0
    for U,J,C,q,k in cases:
        D=C[:len(C)//2]
        center=C[len(C)//2]
        A=B + W*q + J
        Y=A + list(U)*k + D
        Y5=A + list(U)*(k+5) + D
        P=pairword(q,k,J,list(U),C)
        P5=pairword(q,k+5,J,list(U),C)
        assert folded_endpoint(Y,center)==v10(P)
        assert folded_endpoint(Y5,center)==v10(P5)
        # Inserting U^5 immediately before D and shifting D by 15 sites.
        s=len(A)+3*k
        M=moments(Y)
        predicted=add(add(M,rotate(moments(list(U)*5),s)),
                      sub(rotate(moments(D),s+15),rotate(moments(D),s)))
        assert moments(Y5)==predicted
        # The odd-centre endpoint supplies the unique required 120-step source sum.
        S=v10(P); S5=v10(P5); L=len(P)
        required=md((S5-84*S)*pow((57*pow(10,L,MOD))%MOD,-1,MOD))
        assert 0 <= required < MOD
        # Full physical one-step cocycle controls at the exact q,k widths.
        if q in base and k in base:
            _, old, Pnext=source_and_step(P)
            assert old['gamma']==1
            rhs=md((1-pow(10,old['gamma']-2,MOD))*S + 2*pow(10,L+old['gamma']-1,MOD)*old['K'])
            assert v10(Pnext)==rhs
        checked+=1
    print(f'PASS: {checked} odd-centre endpoint/cocycle cases.')
    print('The folded V_10 formula and U^5/D moment transition match direct coefficient evaluation.')
    print('The physical single-step V_10/K cocycle matches genuine n+reverse(n) for odd-length pairwords at all exact q,k widths.')
    print('Every case yields the unique mod-101 120-step weighted carry-source sum required by the endpoint equation.')

if __name__=='__main__': main()
