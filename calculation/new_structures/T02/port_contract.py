#!/usr/bin/env python3
"""Exact all-k zero-loss carry-port criterion for the published p8/m20 exterior.
PAPER PROOF: full two-ended carry-state set reaches a fixed point after one
period-20 band, then induction establishes every k>=1, with arbitrary centre.
No decimal Lychrel existence claim. Python standard library only.
"""
from itertools import product
import random

AL="0123456789ABCDEFGHI"
def dec(s): return tuple(AL.index(x) for x in s)
B=tuple(map(dec,(
"H501D4EC98FGHDH9144B8G09EB9B6DI947HF97D",
"8D5158982IEDFCC7B586AF7A47228AD8EBFE5HB",
"H6B2AGIG5HA8C65G2BGD1BG09E44H17I94C9CF4",
"8E8438GGCD99B9BC949B5397A498C98G8E7339A",
"H8H86HDE680040459A92B6IF09IH49ICI8F6791",
"8GGGEEC9BE804449F00C48FF6A8HCE8CCHECDGA",
"HDEEAA6049H08899A1149HBBE0IF69I56GA68E1",
"8C9A62764E788GI90225E7A4759FCG8EBD87ED6")))
W=tuple(map(dec,(
"H31DHBE3I12073ECF97D",
"CB45CA78CA327A8895HB",
"639B51FH5174F0HGIBF4",
"A9D1767ED68BA68FGB8A",
"2073ECF97DH31DHBE3I1",
"327A8895HBCB45CA78CA",
"74F0HGIBF4639B51FH51",
"8BA68FGB8AA9D1767ED6")))
G=(1,0,1,0,1,0,1,0)
PORT=((0,1),(1,),(0,1),(1,),(0,1),(0,),(0,1),(0,))
assert all(len(x)==39 for x in B) and all(len(x)==20 for x in W)

def transfer(states,src,dst,g):
    """State (low carry, high outgoing carry, previous high digit,
    count of mismatches capped at 2, age since last mismatch capped at 2).
    The high incoming carry is guessed but constrained by its column.
    """
    for x,want in zip(src,dst):
        nxt=set()
        for low,hi,prev,n,age in states:
            for inner in (0,1):
                if (x+inner)//10!=hi: continue
                ld=(x+low)%10
                ud=(x+inner)%10
                got=ld+(ud if g==0 else (1 if prev is None else prev))
                wrong=(got!=want)
                count=min(2,n+int(wrong))
                newage=0 if wrong else min(2,age+1)
                nxt.add(((x+low)//10,inner,ud,count,newage))
        states=frozenset(nxt)
    return frozenset(states)

def all_lengths():
    rows=[]
    for t in range(8):
        start=frozenset({(0,G[t],None,0,2)})
        after_B=transfer(start,B[t],B[(t+1)%8],G[t])
        after_W=transfer(after_B,W[t],W[(t+1)%8],G[t])
        assert len(after_W)==2
        assert after_W==transfer(after_W,W[t],W[(t+1)%8],G[t]),t
        # Since another full band leaves this exact state set unchanged,
        # all k>=1 are covered by mathematical induction, not by a cap.
        assert {s[1] for s in after_W}=={0,1}
        good=tuple(sorted(s[1] for s in after_W if s[3]==0))
        assert good==PORT[t],(t,good)
        for lo,hi,z,count,age in after_W:
            if hi in PORT[t]:
                assert count==0
            else:
                assert count==1 and age==0
        rows.append((t,G[t],good))
    return rows

def decimal_from_pairs(P):
    assert P==P[::-1]
    h=len(P)//2
    high=[min(9,x) for x in P[:h]]
    low=[P[i]-high[i] for i in range(h)]
    middle=[] if len(P)%2==0 else [P[h]//2]
    assert len(P)%2==0 or P[h]%2==0
    digits=low+middle+high[::-1]
    assert digits[-1]>0
    return ''.join(str(d) for d in reversed(digits))

def actual_carries(P):
    c=[0]
    for x in P: c.append((x+c[-1])//10)
    return c

def bigint_control():
    rng=random.Random(20261028)
    counts={(t,u):0 for t in range(8) for u in (0,1)}
    trials=0
    for t,k in product(range(8),(1,2,3,5,8)):
        hword=B[t]+W[t]*k
        for j in range(140):
            left=tuple(rng.randrange(19) for _ in range(j%9))
            C=left+(() if j%2 else (2*rng.randrange(10),))+left[::-1]
            P=hword+C+hword[::-1]
            s=decimal_from_pairs(P)
            n=int(s)
            # Real arbitrary-precision integer reverse/add, not transfer().
            out=list(map(int,str(n+int(s[::-1]))[::-1]))
            Q=tuple(out[i]+out[-i-1] for i in range(len(out)//2))
            c=actual_carries(P)
            u=c[len(P)-len(hword)]
            assert c[-1]==G[t]
            observed=(Q[:len(hword)]==B[(t+1)%8]+W[(t+1)%8]*k)
            expected=u in PORT[t]
            assert observed==expected,(t,k,j,u)
            counts[t,u]+=1
            trials+=1
    assert trials==5600
    assert all(v>0 for v in counts.values())
    return counts

if __name__=="__main__":
    for t,g,good in all_lengths():
        print("phase",t,"overflow",g,"full-band seam carry",good)
    counts=bigint_control()
    print("PASS: complete finite-state induction for all k>=1")
    print("PASS: 5600 ordinary Python bigint reverse+add comparisons")
    print("Actual seam carry class counts:",counts)
    print("No all-time seam realization or decimal Lychrel number is claimed.")
