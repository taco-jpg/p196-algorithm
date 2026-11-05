#!/usr/bin/env python3
"""W-side inlet analysis: the rooted region [0,J0) = B0 W0^14 evolves as a
function of the 120-bit high-carry inlet sigma_t entering column J0-1 from the
right.  BFS over reachable W-region states (dedup) for the first T steps."""
import sys
B=(10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5)
W=(5,18,4,8,1,15,4,0,5)
J0=34+9*14
def step(p,g,s):
    n=len(p); c=0; d=[]
    for x in p: z=x+c; d.append(z%10); c=z//10
    # high digits: hi[i]=(p[i]+beta_{i+1})%10, beta_n=s; beta_i=T(p[i],beta_{i+1})
    hi=[0]*n; b=s
    for i in range(n-1,-1,-1):
        z=p[i]+b; hi[i]=z%10; b=z//10
    if g: return tuple([d[0]+1]+[d[i]+hi[i-1] for i in range(1,n)]), b
    return tuple(d[i]+hi[i] for i in range(n)), b
def wsigma():
    # periodic W beta at column J0 for pure W continuation: use long W
    p=tuple(B+W*40); out=[]
    for t in range(120):
        g=(t%4==0)
        # beta at J0 computed from pure W far right with arbitrary inlet (resets)
        n=len(p); b=0
        for i in range(n-1,J0-1,-1): b=(p[i]+b)//10
        out.append(b); p,_=step(p,g,0)
    return out
if __name__=='__main__':
    T=int(sys.argv[1])
    sw=wsigma(); print('sigma_W',''.join(map(str,sw)))
    S={tuple(B+W*14)}
    for t in range(T):
        g=(t%4==0); N=set()
        for p in S:
            for s in (0,1):
                q,gg=step(p,g,s)
                if gg!=g: continue
                N.add(q)
        S=N
        print(t+1,len(S),flush=True)
