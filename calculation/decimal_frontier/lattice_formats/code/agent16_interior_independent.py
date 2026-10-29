#!/usr/bin/env python3
"""Independent brute-force bit-carry checker and unbounded inequality audit.
Time recursion enumerates c_t directly; deliberately does not import C++.
"""
import argparse
from functools import lru_cache


def make_state(r,s,j,u,v):
    b=1<<(r+1);p=2*r+4
    g=[int(i in (0,r+1,r+2)) for i in range(p)]
    L=[int(q) for q in ('1'*(r+2)+'0'+'1'*(j+1)+'0'*(r-j))]
    H=[int(q) for q in ((('1'*(j+1)) if s else ('0'+'1'*j))+'0'*(r-j)+str(u)+str(v)+'1'*r+'0')]
    Y={0:b-2+s,r+1:b-(1<<(r-j))-1+u,r+2:b-(1<<(r-j))-1+v}
    assert len(L)==len(H)==p
    return b,p,g,L,H,Y


def count_paths(r,s,j,u,v):
    b,p,g,L,H,Y=make_state(r,s,j,u,v)
    @lru_cache(None)
    def paths(t,x,initial):
        if t==p:return int(x==initial)
        if x<0 or x>2*b-2:return 0
        ans=0
        for c in (0,1):
            if (x+c)//b!=H[t]:continue
            nxt=(x+L[t])%b+(Y[t] if g[t] else (x+c)%b)
            ans+=paths(t+1,nxt,initial)
        return ans
    return sum(paths(0,x0,x0) for x0 in range(2*b-1))


def check_inequality(r,j):
    """Checks inequalities used in proof, not a substitute for all-r algebra."""
    b=1<<(r+1);m=j+1;a=1<<(r-j)
    assert 0<=j<=r-3 and r>=4
    assert (1<<m)*a==b
    deficit_bound=(1<<m)*(a-1)+2
    assert deficit_bound==b-(1<<m)+2>=7*b//8+2
    x_bound=2*b-deficit_bound
    assert 2*(x_bound-b)+1 < b-1
    assert (1<<j)+1 < b


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--max-r',type=int,default=7)
    args=ap.parse_args()
    for r in range(4,args.max_r+1):
        for j in range(r-2):
            check_inequality(r,j)
            for s in (0,1):
                for u in (0,1):
                    for v in (0,1):
                        assert count_paths(r,s,j,u,v)==0,(r,s,j,u,v)
        print(f'PASS independent brute r={r} interior states={8*(r-2)}')
    # Exercise exponent/index boundary inequalities at much larger r with no big-int orbit scan.
    for r in (32,64,128,256,512,1024):
        for j in (0,1,2,r//2,r-4,r-3):
            check_inequality(r,j)
        print('PASS large-exponent bound r=',r)
    print('ALL INDEPENDENT INTERIOR CONTROLS PASSED')

if __name__=='__main__':main()
