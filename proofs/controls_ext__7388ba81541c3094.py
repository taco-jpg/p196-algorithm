#!/usr/bin/env python3
"""Agent #115 controls for the (Z, rho) factorization of the complementary
exterior map. `outer_next` is a literal translation of
P196.Agent7.Finite.outerNext (proofs/contributions/agent-109/outer-projection-bridge/agent7-deps/OuterFinite.lean).
`predict` computes the successor only from (c, Z, rho): the 10-adic digits of
beta=(Z-c)/9 plus the decimal digits of rho (or rho/10 on overflow), then trims
trailing c'. Exact rational arithmetic (fractions). Finite controls only.
"""
# Agent7 outerNext (translated literally) and the (beta, rho) factorization test
from fractions import Fraction as Fr
import random
def normalize(xs, carry):
    out=[]
    for x in xs:
        out.append((x+carry)%10); carry=(x+carry)//10
    return out, carry
def strip_suffix(c,w):
    w=list(w)
    while w and w[-1]==c: w.pop()
    return w
def outer_next(c,B):
    k=1 if c>=10 else 0
    t=c-9*k
    left=normalize(B,0)
    right=normalize(list(reversed(B)),k)
    u=c+left[1]-10*k
    other = (list(reversed(right[0]))+[t]) if right[1]==0 else ([1]+list(reversed(right[0])))
    raw=[x+y for x,y in zip(left[0]+[u], other)]
    return 2*t, strip_suffix(2*t, raw)
def valid(c,B):
    return all(x<=18 for x in B) and (not B or B[0]>0) and (not B or B[-1]!=c)
def beta9(c,B):   # Z = 9*beta + c  (agent110): 9*sum B_i 10^i - c(10^n - 1)
    n=len(B); return 9*sum(b*10**i for i,b in enumerate(B)) - c*(10**n-1)
def rho(c,B):
    n=len(B); return sum(Fr(b,10**(i+1)) for i,b in enumerate(B)) + Fr(c,9*10**n)
def digits_10adic(Z,c,m):
    # beta = (Z-c)/9 as 10-adic; return first m digits
    num=Z-c  # 9*beta
    # beta = num/9 ; 10-adic digits: solve iteratively
    out=[]; x=Fr(num,9)
    for _ in range(m):
        # digit d with x ≡ d mod 10 in Z_(10) sense: x = a/9, find d in 0..9 with (x-d)/10 in Z_10 (denominator coprime to 10)
        for d in range(10):
            y=(x-d)/10
            if y.denominator%2 and y.denominator%5: break
        out.append(d); x=y
    return out
def digits_real(r,m):
    out=[]
    for _ in range(m):
        r*=10; d=int(r); out.append(d); r-=d
    return out
def predict(c,B):
    k=1 if c>=10 else 0; t=c-9*k; c2=2*t
    n=len(B); m=n+3
    Z=beta9(c,B)
    lam=digits_10adic(Z,c,m)
    r=rho(c,B)
    rr = r if r<1 else r/10
    eta=digits_real(rr,m)
    w=[a+b for a,b in zip(lam,eta)]
    return c2, strip_suffix(c2, w)
if __name__ == '__main__':
    import itertools, json, sys
    PHASES = [2,4,6,8,10,12,14,16]
    # (1) exhaustive: every canonical state with |B| <= 3
    ex_tot = ex_bad = 0
    for c in PHASES:
        for n in range(4):
            for B in itertools.product(range(19), repeat=n):
                B = list(B)
                if not valid(c, B): continue
                ex_tot += 1
                if outer_next(c, B) != predict(c, B): ex_bad += 1
    # (2) seeded random states with 4 <= |B| <= 40
    random.seed(115)
    r_tot = r_bad = 0
    for c in PHASES:
        for _ in range(3000):
            n = random.randint(4, 40)
            B = [random.randint(0, 18) for _ in range(n)]
            if not valid(c, B): continue
            r_tot += 1
            if outer_next(c, B) != predict(c, B): r_bad += 1
    res = {"exhaustive_len_le_3": {"states": ex_tot, "mismatches": ex_bad},
           "random_len_4_to_40_seed115": {"states": r_tot, "mismatches": r_bad}}
    print(json.dumps(res))
    sys.exit(1 if ex_bad or r_bad else 0)
