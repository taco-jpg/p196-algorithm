"""General-base one-band neutral template quotient (exploratory, Python).
Word (pair sums, low->high): B n^g C n^g rev(B), n=b-1, C symmetric.
We compute the actual next pair word for a concrete realization at a few gaps and
extract the new (B',C',g') by maximal trimming of n-runs adjacent to the bands.
Transition validity across gaps is checked numerically on several gaps (exploratory only)."""
import sys, itertools
from functools import lru_cache
def realize(q,b):
    L=len(q); d=[0]*L
    for i in range(L//2):
        hi=min(q[i],b-1); lo=q[i]-hi
        d[L-1-i]=hi; d[i]=lo   # most significant digit hi>0 since q[0]>0
    if L%2: d[L//2]=q[L//2]//2
    return d  # low->high digits
def value(d,b):
    v=0
    for x in reversed(d): v=v*b+x
    return v
def digits(v,b):
    out=[]
    while v: out.append(v%b); v//=b
    return out
def pair_next(q,b):
    d=realize(q,b)
    v=value(d,b)
    r=value(list(reversed(d)),b)  # reverse
    s=v+r
    dd=digits(s,b)
    return tuple(dd[i]+dd[len(dd)-1-i] for i in range(len(dd)))
def ispal_next(q,b):
    d=realize(q,b); v=value(d,b); s=v+value(list(reversed(d)),b); dd=digits(s,b)
    return dd==dd[::-1]
def decompose(q,b):
    """Find (B,C,g): the word must be B n^g C n^g rev(B) with maximal bands; we take the
    longest run of n in the low half as the band."""
    n=b-1; L=len(q); half=L//2
    # find maximal run of n in q[0:half] that is longest
    best=None;i=0
    while i<half:
        if q[i]==n:
            j=i
            while j<half and q[j]==n: j+=1
            if best is None or j-i>best[1]-best[0]: best=(i,j)
            i=j
        else: i+=1
    if best is None: return None
    i,j=best
    B=q[:i]; g=j-i
    C=q[j:L-j]
    if tuple(q[L-j:L-i])!=tuple([n]*g): return None
    return (tuple(B),tuple(C),g)
def search(b, Bmax, Cmax, g0=12, steps=200):
    n=b-1
    found=[]
    for bl in range(0,Bmax+1):
        for B in itertools.product(range(2*b-1),repeat=bl):
            if bl and B[0]==0: continue
            if bl and B[-1]==n: continue
            for cl in range(1,Cmax+1):
                for half in itertools.product(range(2*b-1),repeat=(cl+1)//2):
                    C=half+tuple(reversed(half[:cl//2]))
                    if cl%2 and C[cl//2]%2: continue
                    if C[0]==n: continue
                    q=B+(n,)*g0+C+(n,)*g0+tuple(reversed(B))
                    if not q or q[0]==0: continue
                    # iterate and watch the template
                    seen={}
                    cur=q; ok=True
                    for t in range(steps):
                        if ispal_next(cur,b): ok=False; break
                        nxt=pair_next(cur,b)
                        dec=decompose(nxt,b)
                        if dec is None: ok=False;break
                        Bn,Cn,gn=dec
                        if gn<4 or len(Bn)>Bmax+6 or len(Cn)>Cmax+8: ok=False;break
                        key=(Bn,Cn)
                        if key in seen:
                            t0,g_old=seen[key]
                            if gn>=g_old:
                                found.append((B,C,'cycle period',t+1-t0,'gain',gn-g_old,'interfaces',key))
                            ok=False;break
                        seen[key]=(t+1,gn)
                        cur=nxt
    return found
if __name__=='__main__':
    for b in [int(x) for x in sys.argv[1:]]:
        Bmax,Cmax=(3,5) if b<=3 else ((2,3) if b<=6 else (1,3))
        f=search(b,Bmax,Cmax)
        print('base',b,'Bmax',Bmax,'Cmax',Cmax,'cycles',len(f), f[:3], flush=True)
