#!/usr/bin/env python3
"""Independent arbitrary-precision decimal replay for Z10 slice 11.

This checker deliberately does not share the C++ bit-sliced carry engine.
It constructs a canonical decimal integer and iterates n <- n + reverse10(n).
"""
import argparse, json, sys
from pathlib import Path
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)

def load(path):
    lines=Path(path).read_text().splitlines()
    head=list(map(int,lines[0].split()))
    if head != [12,34,9,10]: raise ValueError(head)
    gamma=list(map(int,lines[1].split()))
    rows=[list(map(int,x.split())) for x in lines[2:]]
    W=rows[:12]; B=rows[24:36]
    return gamma,B[0],W[0]

def templ(B,W,J,U,q,k):
    h=list(B)+list(W)*q+list(J)+list(U)*k
    return h+[2]+h[::-1]

def seed(P):
    d=[0]*len(P)
    for i in range(len(P)//2):
        d[i]=min(9,P[i]); d[-1-i]=P[i]-d[i]
    if len(P)%2:
        if P[len(P)//2]%2: raise ValueError("odd center pair coefficient")
        d[len(P)//2]=P[len(P)//2]//2
    if d[-1]==0: raise ValueError("zero leading digit")
    return int("".join(map(str,d[::-1])))

def pairword(n):
    d=[ord(c)-48 for c in str(n)[::-1]]
    return [d[i]+d[-1-i] for i in range(len(d))]

def reverse10(n): return int(str(n)[::-1])

def replay(gamma,B,W,U,J,q,k):
    p0=templ(B,W,J,U,q,k); n=seed(p0)
    prefix=list(B)+list(W)*q
    target120=templ(B,W,J,U,q,k+5)
    target240=templ(B,W,J,U,q,k+10)
    clock=[]; pals=[]; mismatch=None; ret120=None; ret240=None
    for t in range(241):
        s=str(n)
        if s==s[::-1]: pals.append(t)
        if t==120:
            pw=pairword(n)
            mismatch=next((i-len(prefix) for i,(a,b) in enumerate(zip(pw,prefix)) if a!=b),None)
            if len(pw)<len(prefix): mismatch=len(pw)-len(prefix)
            ret120=(pw==target120)
        if t==240:
            ret240=(pairword(n)==target240)
            break
        nn=n+reverse10(n)
        clock.append(len(str(nn))-len(s))
        n=nn
    expected=[gamma[t%12] for t in range(240)]
    return {"U":list(U),"J":list(J),"q":q,"k":k,"digits":len(str(seed(p0))),
        "clock120_exact":clock[:120]==expected[:120],"clock240_exact":clock==expected,
        "overflow120":sum(clock[:120]),"overflow240":sum(clock),
        "first_W9_mismatch_from_cut":mismatch,"full_return120":ret120,
        "full_return240":ret240,"palindrome_times":pals}

def decode(i):
    d=[0]*5
    for j in range(4,-1,-1): d[j]=i%19; i//=19
    return d

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--lattice",default="calculation/new_structures/Z10/input_lat_p12m9.txt")
    ap.add_argument("--out",default="")
    args=ap.parse_args()
    gamma,B,W=load(args.lattice)
    if gamma != [1,0,0,0,1,0,0,0,1,0,0,0]: raise ValueError("unexpected phase-0 clock")
    Ujs=[((9,2,16),[[0,0,0,0,0],[18,18,18,18,18],[0,2,2,7,8],[2,0,18,9,0]]),
         ((12,9,6),[[0,0,0,0,0],[18,18,18,18,18],[0,2,5,0,18],[5,9,11,2,9]])]
    out=[]
    for U,Js in Ujs:
        for J in Js:
            for q,k in [(14,100),(20,100),(40,200),(80,400),(160,800)]:
                r=replay(gamma,B,W,U,J,q,k)
                if not r["clock120_exact"] or not r["clock240_exact"]: raise AssertionError("clock mismatch: "+repr(r))
                if r["full_return120"] or r["full_return240"]: raise AssertionError("unexpected full return: "+repr(r))
                if q==14 and r["first_W9_mismatch_from_cut"] is None: raise AssertionError("reference prefix matched: "+repr(r))
                out.append(r)
    result={"method":"independent Python arbitrary-precision integers; n <- n + reverse10(n)","cases":len(out),"results":out}
    encoded=json.dumps(result,indent=2)
    if args.out: Path(args.out).write_text(encoded+"\n")
    print(encoded)
if __name__=="__main__": main()
