#!/usr/bin/env python3
"""Independent Python arbitrary-integer replay with direct digit-array control."""
import sys,random
sys.set_int_max_str_digits(100000)
from probe import templ,realize,step,pair,US
def bigint(d):return int(''.join(str(x) for x in d[::-1]))
def replay(q,k,J,U,C):
    src=templ(q,k,J,U,C);d=realize(src);n=bigint(d)
    for t in range(120):
        s=str(n)
        n=n+int(s[::-1])
        d2=step(d)
        if n!=bigint(d2):raise AssertionError((q,k,t))
        d=d2
    got=pair(d);target=templ(q,k+5,J,U,C)
    r=122+len(C)+30;h=len(got)//2
    return len(got)==len(target),got[h-r:h+r+1]==target[h-r:h+r+1],len(got)-len(src)
def main():
    r=random.Random(230715)
    widths=[(14,100),(20,80),(40,160),(80,320),(160,640)]
    for u in US:
        for length in (7,8,11,12,13,14):
            half=[r.randrange(19) for _ in range(length//2)]
            C=half+([2*r.randrange(10)] if length%2 else [])+half[::-1]
            for q,k in widths:
                l,ret,delta=replay(q,k,[5],u,C)
                assert l and delta==30
                print('CHECK',u,'C_len',length,'q',q,'k',k,'len+30',l,'central_return',ret)
if __name__=='__main__':main()
