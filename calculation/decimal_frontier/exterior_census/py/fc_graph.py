# First-coordinate NFA for base b: states q in 1..2b-2 (B_t[0]); edge labelled g.
import sys
from fractions import Fraction
def edges(b):
    E=[]  # (q,q2,g,h)
    for q in range(1,2*b-1):
        for h in (0,1):
            if q+h<b:   # no overflow
                q2=2*q+h
                if q2<=2*b-2: E.append((q,q2,0,h))
            else:       # overflow: q+h>=b
                q2=(q%b)+1
                if q2<=2*b-2: E.append((q,q2,1,h))
    return E
def minmax_cycle_mean(b):
    E=edges(b); n=2*b-2
    # Karp on weights g, both min and max, via simple DP on closed walks length up to n*? use Bellman style
    import itertools
    INF=10**9
    res={}
    for sign,name in ((1,'min'),(-1,'max')):
        # d[k][v] = best weight of walk length k ending at v, starting anywhere (all start 0)
        d=[[0]*(n+1)]
        for k in range(1,n+2):
            row=[INF]*(n+1)
            for (q,q2,g,h) in E:
                if d[-1][q]<INF: row[q2]=min(row[q2], d[-1][q]+sign*g)
            d.append(row)
        best=None
        for v in range(1,n+1):
            if d[n+1][v]>=INF: continue
            m=None
            for k in range(0,n+1):
                if d[k][v]>=INF: continue
                val=Fraction(d[n+1][v]-d[k][v], n+1-k)
                m=val if m is None else max(m,val)
            if m is not None: best=m if best is None else min(best,m)
        res[name]=sign*best
    return res
if __name__=='__main__':
    b=int(sys.argv[1]) if len(sys.argv)>1 else 10
    E=edges(b)
    print('edges',len(E))
    print(minmax_cycle_mean(b))
