import sys
from fc_graph import edges
from fractions import Fraction
b=int(sys.argv[1]); target=Fraction(int(sys.argv[2]),int(sys.argv[3]))   # target mean of g
E=edges(b); n=2*b-2
# edges on some cycle of mean == target: use potentials w = g - target; extremal cycle mean 0 => find potentials, tight edges, then SCCs
# Bellman-Ford with weights (g-target) maximizing (target is the max mean => all cycles <=0)
sign = 1 if target>=Fraction(1,3) else -1
def tight_edges(sign):
    w=lambda g: sign*(g-target)
    pot=[0]*(n+1)
    for _ in range(n+3):
        ch=False
        for (q,q2,g,h) in E:
            # want pot(q2) >= pot(q)+w  ; with max-mean cycles = 0 sign chosen so all cycles <= 0 -> longest path well defined
            pass
        break
    # use longest-path potentials with weight -w (so cycles >= 0): pot(q2) <= pot(q) + (-w)... simpler: Floyd-style on small graph
    INF=None
    import itertools
    d={}
    for (q,q2,g,h) in E:
        k=(q,q2); v=w(g)
        d[k]=max(d.get(k,-10**9),v)
    # longest walk weights via Floyd-Warshall (no positive cycles when target is extremal)
    NEG=-10**9
    D=[[NEG]*(n+1) for _ in range(n+1)]
    for (q,q2),v in d.items(): D[q][q2]=max(D[q][q2],v)
    for k in range(1,n+1):
        for i in range(1,n+1):
            if D[i][k]==NEG: continue
            for j in range(1,n+1):
                if D[k][j]==NEG: continue
                if D[i][k]+D[k][j]>D[i][j]: D[i][j]=D[i][k]+D[k][j]
    res=[]
    for (q,q2,g,h) in E:
        # edge lies on a cycle of weight 0 iff w(e)+D[q2][q] == 0 (D[q2][q] longest path q2->q)
        if D[q2][q]!=NEG and w(g)+D[q2][q]==0: res.append((q,q2,g,h))
    return res
res=tight_edges(sign)
print('critical edges (mean %s):'%target, len(res))
for e in sorted(res): print(e)
