import sys
sys.argv=[sys.argv[0]]+sys.argv[1:]
exec(open('cyc.py').read().split('w=int(sys.argv[1])')[0])
from collections import defaultdict
for w in map(int, sys.argv[1:]):
    W,verts,edges=get(w)
    adj=defaultdict(set)
    for s,t,l in edges: adj[s].add(t)
    best=None
    starts=[v for v in range(len(verts)) if verts[v][0]==0]
    # matrix-free: for each k, compute for all starts reachability in 7k steps (bitset via python ints per start is heavy); use per-start BFS sets up to K periods
    K=12
    for s in starts:
        cur={s}
        for step in range(1,7*K+1):
            cur={t for v in cur for t in adj[v]}
            if not cur: break
            if step%7==0 and s in cur:
                if best is None or step<best[0]: best=(step,s)
                break
            if best and step>=best[0]: break
    print('width',w,'vertices',len(verts),'shortest cycle',best)
