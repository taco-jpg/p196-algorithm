#!/usr/bin/env python3
"""Independent full-decimal replay for Z11 phase-zero J5 slice 2/12.

Three representations are cross-checked at every genuine step: Python
arbitrary-precision N + reverse(N), a separate LSD-first digit-array adder,
and folded pairword normalization/mirroring. The SIMD census uses a separate
centre-free two-sided carry cone. Both legal centre parities are represented.
"""
import sys
sys.set_int_max_str_digits(0)
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
CASES={
 (0,18,9): [([0,4,0,0,0],[0,0]),([9,1,2,5,6],[4,12,4])],
 (9,6,12): [([0,3,0,8,7],[0,0]),([4,13,10,4,7],[4,12,4])],
 (14,9,4): [([0,2,7,7,9],[0,0]),([4,6,5,8,4],[4,12,4])],
}
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
    assert d[-1]!=0 and pairword(d)==P
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
    assert odd_indices[0] is not None
    for t in range(120):
        assert pairword(d)==P,(q,k,J,U,C,t,'pre-step pairword')
        s=str(n);n2=n+int(s[::-1])
        d2=digit_step(d)
        assert value_lsd(d2)==n2,(q,k,J,U,C,t,'bigint vs digit-array')
        P2=pair_step(P)
        assert pairword(d2)==P2,(q,k,J,U,C,t,'pairword vs digit-array')
        g=len(str(n2))-len(s)
        assert g in (0,1)
        gammas.append(g)
        odd_indices.append(next((i for i,x in enumerate(P2) if x%2),None))
        n,d,P=n2,d2,P2
    assert gammas==[1 if t%4==0 else 0 for t in range(120)],(q,k,J,U,C,'clock')
    assert all(i is not None for i in odd_indices),(q,k,J,U,C,'odd guard')
    targetH=B+W*q+list(J)+list(U)*(k+5)
    target=targetH+list(C)+targetH[::-1]
    first_any=next((i for i,(x,y) in enumerate(zip(P,target)) if x!=y),None)
    if first_any is None and len(P)!=len(target):first_any=min(len(P),len(target))
    cut=len(B)+9*q
    first_w=next((i for i in range(len(B),cut) if P[i]!=target[i]),None)
    assert first_w is not None,(q,k,J,U,C,'W9 restored')
    assert first_any==first_w,(q,k,J,U,C,'mismatch outside W9')
    assert first_w-cut in range(-25,-8),(q,k,J,U,C,first_w,'unexpected W9 offset')
    return first_w,sum(gammas),len(str(n)),odd_indices[-1]
def main():
    count=0
    for U,cases in CASES.items():
        for J,C in cases:
            rows=[]
            for q,k in WIDTHS:
                first,gs,digits,odd=run(q,k,J,U,C)
                rows.append((q,k,first,gs,digits,odd));count+=1
            offsets=[r[2]-(len(B)+9*r[0]) for r in rows]
            assert len(set(offsets))==1,(U,J,C,rows)
            print(f'U={U} J={J} C={C} rows={rows} invariant_W_offset={offsets[0]}',flush=True)
    print(f'INDEPENDENT_BIGINT_DIGIT_ARRAY_PAIRWORD_PASS cases={count} widths={WIDTHS} steps_each=120 centres=even+odd',flush=True)
if __name__=='__main__':main()
