#!/usr/bin/env python3
"""Independent ordinary-integer counterexample to Q03's universal gate table."""
def pairword(n):
    s = str(n)
    return [int(s[-1-i]) + int(s[i]) for i in range(len(s))]
def reverse_add(n):
    return n + int(str(n)[::-1])
def schoolbook_reverse_add(n):
    digits = list(map(int, str(n)[::-1]))
    out, carry = [], 0
    for i, digit in enumerate(digits):
        z = digit + digits[-1-i] + carry
        out.append(z % 10); carry = z // 10
    if carry: out.append(carry)
    return sum(d * 10**i for i, d in enumerate(out))
def canonical_from_pairword(p):
    assert p == p[::-1] and p[0] > 0 and all(0 <= x <= 18 for x in p)
    d = [0] * len(p)
    for i in range(len(p)//2):
        d[i] = max(0, p[i] - 9); d[-1-i] = min(9, p[i])
    if len(p) % 2:
        assert p[len(p)//2] % 2 == 0
        d[len(p)//2] = p[len(p)//2] // 2
    assert d[-1] > 0
    return sum(x * 10**i for i, x in enumerate(d))
def carry_trace(p):
    c = [0]
    for x in p: c.append((x + c[-1]) // 10)
    return c
def main():
    P=[10,18,18,9,6,10,6,9,18,18,10]
    R=[10,18,9,9,6,10,6,9,9,18,10]
    j,jp=2,8
    assert P==P[::-1] and R==R[::-1] and P[:j]==R[:j]
    assert P[j]==18 and R[j]==9 and P[jp]==18 and R[jp]==9 and P[j-1]==18!=9
    N,M=canonical_from_pairword(P),canonical_from_pairword(R)
    assert N==99996500991 and M==99996500091 and pairword(N)==P and pairword(M)==R
    c,d=carry_trace(P),carry_trace(R)
    assert c[-1]==d[-1]==1
    cL,cU,dU=c[j],c[jp],d[jp]
    assert (cL,cU,dU)==(1,0,0)
    S,T=reverse_add(N),reverse_add(M)
    assert S==schoolbook_reverse_add(N) and T==schoolbook_reverse_add(M)
    QS,QT=pairword(S),pairword(T)
    assert len(QS)==len(QT)==12 and QS[:j]==QT[:j]==[1,10]
    assert QS[j]==18 and QT[j]==8 and QS[:j+1]!=QT[:j+1]
    print("P =",P); print("R =",R)
    print("N =",N,"reverse-add =",S,"overflow =",c[-1])
    print("M =",M,"reverse-add =",T,"overflow =",d[-1])
    print("j,j' =",j,jp,"cL,cU,dU =",cL,cU,dU)
    print("successor pairwords:",QS); print("                 ",QT)
    print("FIRST MISMATCH: j=2 despite published cL:any")
    print("CORRECTION: 18 -> 9 requires cL=0; cU arbitrary and dU=0 remain compatible.")
if __name__=="__main__": main()
