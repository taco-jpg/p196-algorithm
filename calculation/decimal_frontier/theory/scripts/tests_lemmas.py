#!/usr/bin/env python3
"""Exhaustive/random numerical checks of the lemmas used in THEORY.md.  Run: python3 tests_lemmas.py"""
import sys, itertools, random
from fractions import Fraction as F
sys.path.insert(0,'..')
import mirror as m

def val(b,w): return sum(c*b**i for i,c in enumerate(w))

# ---- L1: centre determines e1 :  hyp-valid iff e1==[val C < b^m] ; val C = b^m-1 impossible
def test_L1(b,mmax):
    cnt=0
    for mm in range(1,mmax+1):
        for C in itertools.product(range(2*b-1),repeat=mm):
            C=list(C); v=val(b,C); full=b**mm
            for e in (0,1):
                carry=(v+e)//full
                ok=(carry==1-e)
                pred = (e==(1 if v<full else 0)) and v!=full-1
                assert ok==pred,(b,C,e)
                # also compare to mirror's norm
                assert m.norm(b,C,e)[1]==carry
            cnt+=1
    return cnt

# ---- L2: counter lemma for lowest coefficient of B
def test_L2(b,lmax):
    cnt=0
    for L in range(1,lmax+1):
        for B in itertools.product(range(2*b-1),repeat=L):
            B=list(B)
            if B[0]==0: continue
            e1=m.e1(b,B); e2=1-e1
            DBv=m.DB(b,B); DRv,gm=m.norm(b,B[::-1],e2)
            x=B[0]
            # carry into last position of the normalization of rev B
            c=e2
            for v in B[::-1][:-1]:
                c=(v+c)//b
            k=c
            assert gm==(1 if x+k>=b else 0),(b,B)
            xd=(b-1)*(1-e1)
            nb = m._zw(DBv,DRv[::-1]) if gm==0 else m._zw(DBv+[xd],[1]+DRv[::-1])
            pred = 2*x+k if gm==0 else (x%b)+1
            assert nb[0]==pred,(b,B,nb[0],pred)
            cnt+=1
    return cnt

# ---- L3: real-number identities (limit g->inf)
def frac_of(b,digits,tail):
    v=F(0)
    for i,d in enumerate(digits): v+=F(d,b**i)
    return v+F(tail,b**len(digits))*F(b,b-1)
def XY(b,B):
    e1=m.e1(b,B); e2=1-e1
    DBv=m.DB(b,B); DRv,gm=m.norm(b,B[::-1],e2)
    return DBv,(b-1)*(1-e1),([1] if gm else [])+DRv[::-1],(b-1)*e1,e1,gm
def fwd_carries(b,S):
    """forward carries c_j (j>=1) of normalising S with tail (b-1)^inf and carry e1 at the end: here S includes B only; tail contributes e1/(b-1) b^-m"""
    c=0; cs=[0]
    for v in S:
        c=(v+c)//b; cs.append(c)
    return cs
def test_L3(b,lmax,trials=3000):
    rnd=random.Random(1)
    for _ in range(trials):
        L=rnd.randint(1,lmax)
        B=[rnd.randint(0,2*b-2) for _ in range(L)]
        if B[0]==0: B[0]=1
        X,xd,Y,yd,e1,gm=XY(b,B)
        l=frac_of(b,X,xd); h=frac_of(b,Y,yd)
        V=sum(F(c,b**i) for i,c in enumerate(B))+F(b,b**L)   # B ++ (b-1)^inf  == b^{1-L}
        # next state
        Bn=m.nextB(b,B,[e1] if False else None) if False else None
        # h' = V/b^gam, and V = h_next*b^gam ; l_next=V-(b^2-1)kappa ; check via pair-word value of N_{t+1}: N_{t+1} has low digits X, top digits Y
        assert h==V/b**gm,(b,B,float(h),float(V/b**gm))
        # kappa from forward carries of S=B ++ (b-1)^inf, carry e1 into tail constant
        cs=fwd_carries(b,B)       # cs[j] carry into position j, j=0..L ; cs[L]==e1
        assert cs[L]==e1
        kappa=sum(F(cs[j],b**j) for j in range(1,L+1))+F(e1,b**L)*F(1,b-1)*F(1,1)*1  # tail: positions >L carry e1 each: sum_{j>L} e1 b^-j = e1 b^-L/(b-1)
        # careful: j=L term counted once in the sum above (cs[L]=e1) so tail starts at j=L+1
        kappa=sum(F(cs[j],b**j) for j in range(1,L+1))+F(e1,(b**L)*(b-1))
        # l of N_{t+1} = ?  X is low digit string of N_{t+1}; ι(X)=l
        assert l==V-(b*b-1)*kappa,(b,B,float(l),float(V-(b*b-1)*kappa))
    return trials

if __name__=="__main__":
    for b in (2,3,4,5):
        print("L1 b",b,"cases",test_L1(b,4 if b<=3 else 3))
    for b in (2,3,4,5,6,7,10):
        print("L2 b",b,"cases",test_L2(b,3 if b>=6 else 4))
    for b in (3,4,10,11):
        print("L3 b",b,"trials",test_L3(b,6))
    print("ALL LEMMA TESTS PASSED")
