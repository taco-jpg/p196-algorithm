# Cross-check: Python reference map enumerated for caps 0..3 (counts + acyclicity + max exit time)
import sys, json
sys.setrecursionlimit(10000)
from outer_ref import outer
import itertools
res=[]
for cap in range(4):
    states=[]
    for c in range(2,17,2):
        for L in range(cap+1):
            for B in itertools.product(range(19),repeat=L):
                if L and (B[0]<1 or B[-1]==c): continue
                states.append((c,B))
    succ={}; ex=0
    for c,B in states:
        c2,Bp,g=outer(c,list(B))
        if len(Bp)>cap: succ[(c,B)]=None; ex+=1
        else: succ[(c,B)]=(c2,tuple(Bp))
    T={}
    def time(s,seen):
        if s in T: return T[s]
        assert s not in seen, "cycle"
        seen.add(s); n=succ[s]; v=1 if n is None else 1+time(n,seen); T[s]=v; return v
    for s in states: time(s,set())
    m=max(T.values())
    res.append(dict(cap=cap,states=len(states),internal=len(states)-ex,exits=ex,max_exit=m,n_max=sum(1 for v in T.values() if v==m)))
print(json.dumps(res))
