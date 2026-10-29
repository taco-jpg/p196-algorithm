#!/usr/bin/env python3
"""Independent full-decimal replay for Z11's p12/m9 |J|=5 census samples.

Three representations are cross-checked at every one of 120 genuine steps:
  (1) Python arbitrary-precision integer N + int(str(N)[::-1]);
  (2) a separate LSD-first schoolbook digit-array implementation;
  (3) folded pairword normalization followed by mirrored pairing.
The fixed C++ SIMD census uses a centre-free two-sided carry cone, so the
replays deliberately include even and odd legal palindromic centres.
"""
import sys
sys.set_int_max_str_digits(0)
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
US=[(9,0,18),(12,6,9)]
JS={
 (9,0,18):[[0,2,7,7,9],[3,5,3,4,16]],
 (12,6,9):[[0,2,16,7,9],[18,0,18,12,7]],
}
CENTRES=[[0,0],[4,12,4]]
WIDTHS=[(14,100),(20,100),(40,200),(80,400),(160,800)]
def template(q,k,J,U,C):
    H=B+W*q+list(J)+list(U)*k
    P=H+list(C)+H[::-1]
    assert P==P[::-1] and P[0]>0 and all(0<=x<=18 for x in P)
    assert len(C)%2==0 or C[len(C)//2]%2==0
    return H,P
def realize(P):
    assert P==P[::-1]
    d=[0]*len(P)
    for i in range(len(P)//2):
        hi=min(P[i],9);lo=P[i]-hi
        assert 0<=lo<=9 and 0<=hi<=9
        d[i]=lo;d[-1-i]=hi
    if len(P)%2:
        assert P[len(P)//2]%2==0
        d[len(P)//2]=P[len(P)//2]//2
    assert d[-1]!=0
    assert pairword(d)==P
    return d
def pairword(d):
    return [d[i]+d[-1-i] for i in range(len(d))]
def value_lsd(d):
    n=0
    for x in reversed(d):n=10*n+x
    return n
def digit_step(d):
    out=[];carry=0;L=len(d)
    for i in range(L):
        z=d[i]+d[L-1-i]+carry
        out.append(z%10);carry=z//10
    if carry:out.append(carry)
    assert out[-1]!=0
    return out
def pair_step(P):
    out=[];carry=0
    for x in P:
        z=x+carry;out.append(z%10);carry=z//10
    if carry:out.append(carry)
    return [out[i]+out[-1-i] for i in range(len(out))]
def run(q,k,J,U,C):
    H,P=template(q,k,J,U,C)
    d=realize(P);n=value_lsd(d)
    assert int(''.join(map(str,d[::-1])))==n
    gammas=[];odd_indices=[next((i for i,x in enumerate(P) if x%2),None)]
    assert odd_indices[0] is not None,(q,k,J,U,C,'initial odd guard absent')
    for t in range(120):
        assert pairword(d)==P,(q,k,J,U,C,t,'pre-step pairword')
        s=str(n); n2=n+int(s[::-1])
        d2=digit_step(d)
        assert value_lsd(d2)==n2,(q,k,J,U,C,t,'bigint vs digit-array')
        P2=pair_step(P)
        assert pairword(d2)==P2,(q,k,J,U,C,t,'pairword vs digit-array')
        g=len(str(n2))-len(s)
        assert g in (0,1)
        gammas.append(g)
        odd=next((i for i,x in enumerate(P2) if x%2),None)
        odd_indices.append(odd)
        n,d,P=n2,d2,P2
    expected_gamma=[1 if t%4==0 else 0 for t in range(120)]
    assert gammas==expected_gamma,(q,k,J,U,C,'overflow clock mismatch')
    assert all(i is not None for i in odd_indices),(q,k,J,U,C,'odd guard lost before t=120')
    targetH=B+W*q+list(J)+list(U)*(k+5)
    target=targetH+list(C)+targetH[::-1]
    first_any=next((i for i,(x,y) in enumerate(zip(P,target)) if x!=y),None)
    if first_any is None and len(P)!=len(target):first_any=min(len(P),len(target))
    cut=len(B)+9*q
    first_w=next((i for i in range(len(B),cut) if P[i]!=target[i]),None)
    assert first_w is not None,(q,k,J,U,C,'W9 restored in independent replay')
    assert first_any==first_w,(q,k,J,U,C,'unexpected mismatch before/after W9')
    assert first_w-(len(B)+9*q) in range(-25,-10),(q,k,J,U,C,first_w,'unexpected W9 offset')
    return first_any,first_w,sum(gammas),len(str(n)),odd_indices[-1]
def main():
    count=0
    for U in US:
        for J in JS[U]:
            for C in CENTRES:
                rows=[]
                for q,k in WIDTHS:
                    first,fw,gs,digits,odd=run(q,k,J,U,C)
                    rows.append((q,k,first,fw,gs,digits,odd))
                    count+=1
                offsets=[r[3]-(len(B)+9*r[0]) for r in rows]
                assert len(set(offsets))==1,(U,J,C,rows)
                print(f'U={U} J={J} C={C} rows={rows} invariant_W_offset={offsets[0]}',flush=True)
    print(f'INDEPENDENT_BIGINT_DIGIT_ARRAY_PAIRWORD_PASS cases={count} widths={WIDTHS} steps_each=120 centres=even+odd midpoint-even',flush=True)
if __name__=='__main__':main()
