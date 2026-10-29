#!/usr/bin/env python3
"""Finite ordinary-digit test of arbitrary-core guarded shells; never an infinite proof.
Run from root:
 python3 calculation/new_structures/agent-X14/shell_probe.py \
   calculation/decimal_frontier/lattice_formats/cert_b9_rec0.json 300 1000
"""
import sys,json

def from_pairword(b,p):
    assert p==p[::-1] and p[0]!=0 and all(0<=x<=2*b-2 for x in p)
    n=len(p);d=[0]*n
    for i in range(n//2):
        hi=min(p[i],b-1);lo=p[i]-hi
        d[i],d[n-1-i]=lo,hi
    if n%2:
        assert p[n//2]%2==0
        d[n//2]=p[n//2]//2
    assert d[-1]>0
    return d

def add_reverse_digits(d,b):
    out=[];carry=0
    for i in range(len(d)):
        x=d[i]+d[-1-i]+carry
        out.append(x%b);carry=x//b
    if carry:out.append(carry)
    return out

def pairword(d):return [d[i]+d[-1-i] for i in range(len(d))]

def normalised_next_pair(p,b):
    d=[];carry=0
    for x in p:
        z=x+carry;d.append(z%b);carry=z//b
    if carry:d.append(carry)
    return pairword(d)

def matched(p,B,W):
    j=0
    while j<len(B) and j<len(p) and p[j]==B[j]:j+=1
    if j<len(B):return j,0
    k=0
    while j+k<len(p) and p[j+k]==W[k%len(W)]:k+=1
    return j,k

def replay(cert,k,steps):
    b=cert['base'];B=cert['B_t'];W=cert['w_t'];period=cert['p']
    assert len(B)==len(W)==period and cert['m']==len(W[0])
    band=[W[0][j%len(W[0])] for j in range(cert['m']*k+cert['l0'])]
    results=[]
    for core in ((),(8,8),(2,4,4,2),(0,0,0,0),(16,16)):
        initial=B[0]+band+list(core)+band[::-1]+B[0][::-1]
        d=from_pairword(b,initial)
        checkpoints=[];outer_fail=0;pal_fail=0;bulk_min=10**9
        for t in range(steps+1):
            p=pairword(d)
            assert p==p[::-1]
            if t<=20:
                assert normalised_next_pair(p,b)==pairword(add_reverse_digits(d,b))
            if d==d[::-1]:pal_fail+=1
            bm,bulk=matched(p,B[t%period],W[t%period])
            if bm<len(B[t%period]):outer_fail+=1
            bulk_min=min(bulk_min,bulk)
            if t in (0,10,100,500,1000):
                checkpoints.append(dict(step=t,digits=len(d),outer_match=bm,bulk_match=bulk))
            if t<steps:d=add_reverse_digits(d,b)
        results.append(dict(core=list(core),outer_failures=outer_fail,
                            palindrome_failures=pal_fail,minimum_bulk_match=bulk_min,
                            checkpoints=checkpoints))
    return dict(label="COMPUTED_FINITE_ONLY",base=b,steps=steps,
                initial_band_len=len(band),results=results)

if __name__=="__main__":
    with open(sys.argv[1]) as f:cert=json.load(f)
    k=int(sys.argv[2]) if len(sys.argv)>2 else 300
    steps=int(sys.argv[3]) if len(sys.argv)>3 else 1000
    output=replay(cert,k,steps)
    assert all(x['outer_failures']==0 and x['palindrome_failures']==0 for x in output['results'])
    print(json.dumps(output,indent=2))
