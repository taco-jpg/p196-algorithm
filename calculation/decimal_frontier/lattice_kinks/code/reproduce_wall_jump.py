#!/usr/bin/env python3
"""Agent-5 K2 PAPER PROOF control: unbounded one-step apparent front advance.
Run from any directory: python3 calculation/decimal_frontier/lattice_kinks/code/reproduce_wall_jump.py
This is a source-data arithmetic checker, not a base-10 Lychrel certificate.
"""
from pathlib import Path
import sys

def load(path):
    a=list(map(int,Path(path).read_text().split())); p,nB,m,b=a[:4];off=4
    gamma=a[off:off+p];off+=p
    def rows(nrows,width):
        nonlocal off
        r=[a[off+i*width:off+(i+1)*width] for i in range(nrows)]
        off+=nrows*width
        return r
    W=rows(p,m);C=rows(p,m);B=rows(p,nB)
    assert len(a)==off and b==10
    return p,nB,m,gamma,W,C,B

def pair_step(P):
    z=[];carry=0
    for q in P:
        x=q+carry;z.append(x%10);carry=x//10
    if carry:z.append(carry)
    return [z[i]+z[-1-i] for i in range(len(z))],z

def decimal_replay(P):
    # Give every valid pair word a genuine ordinary integer seed.
    n=len(P); d=[0]*n
    for i in range(n//2):
        x=P[i]; d[i]=min(9,x);d[n-1-i]=x-d[i]
        assert 0<=d[n-1-i]<=9
    assert d[-1]>0
    # Independent schoolbook arithmetic on canonical digits, not pair_step.
    c=0;z=[]
    for i in range(n):
        s=d[i]+d[n-1-i]+c;z.append(s%10);c=s//10
    if c:z.append(c)
    return [z[i]+z[-1-i] for i in range(len(z))]

def main():
    root=Path(__file__).resolve().parents[1]
    path=root/'data'/'lat_p12m9.txt'
    if len(sys.argv)>=2:path=Path(sys.argv[1])
    p,nB,m,gamma,W,C,B=load(path)
    assert (p,nB,m,gamma,W[0],W[1])==(12,34,9,[1,0,0,0]*3,[5,18,4,8,1,15,4,0,5],[10,14,13,12,9,7,10,4,5])
    assert 9 not in W[0] and B[0][-1]==W[0][-1]==5
    # All nine symbolic interior steps; every entry can be checked by hand.
    for r in range(m):
        w=W[0][r];up=(w+C[0][r])%10
        mirror=(W[0][(r-1)%m]+(w>=10))%10
        assert up+mirror==W[1][r],(r,up,mirror,W[1][r])
    assert W[0][3]==8 and W[1][4]==9
    # Exact local invisibility table. The two normalized digit changes at
    # (j,j+1) cancel against the reflected changes when gamma=1.
    invisible={0:(5,14),1:(18,9),2:(4,13),3:(8,17),
               4:(1,10),5:(15,6),6:(4,13),8:(5,14)}
    assert all(W[0][r]==x for r,(x,_) in invisible.items())
    # First full half-width: check the local table for every possible site.
    n=400;H=[B[0][x] if x<nB else W[0][(x-nB)%m] for x in range(n//2)]
    P=H+H[::-1];Q,_=pair_step(P)
    for j in range(35,n//2-2):
        r=(j-nB)%m
        if r not in invisible:continue
        x,y=invisible[r];assert H[j]==x
        H2=H.copy();H2[j]=y
        Q2,_=pair_step(H2+H2[::-1])
        assert Q2==Q,(j,r)
    # Fixed site j=35 is the first bulk site whose two neighbors are lattice
    # coefficients. Its front advance is 165+9*k, unbounded for k>=0.
    js=35
    # All-k proof: length grows by full 9-cell bands in each half, so the
    # already verified nine cases and finite exterior stay identical for k>=0.
    # Runtime checks sample both short and large lengths, independently via digits.
    samples=[0,1,2,3,10,25,100,1000]
    for k in samples:
        n=400+18*k;h=n//2
        H=[B[0][x] if x<nB else W[0][(x-nB)%m] for x in range(h)]
        assert H[js-1:js+2]==[5,18,4]
        P=H+H[::-1]; Hp=H.copy();Hp[js]=9; Qp=Hp+Hp[::-1]
        q,z=pair_step(P);qq,zz=pair_step(Qp)
        assert len(z)==len(zz)==n+1 and qq==q
        assert decimal_replay(P)==q and decimal_replay(Qp)==q
        dif=[i for i in range(n+1) if z[i]!=zz[i]]
        assert dif==[js,js+1,n-1-js,n-js]
        assert [zz[i]-z[i] for i in dif]==[1,-1,1,-1]
        mismatch=[x for x in range(h+1) if q[x]!=(B[1][x] if x<nB else W[1][(x-nB)%m])]
        assert mismatch==[h],(k,mismatch[:5])
        print('k=%d n=%d one-step front jump=%d; Q identical; gamma=1'%(k,n,h-js))
    print('PAPER PROOF finite exterior + nine symbolic residues + eight cancellation sites: OK')

if __name__=='__main__':main()
