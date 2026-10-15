import sys
exec(open('cyc.py').read().split('w=int(sys.argv[1])')[0])
from collections import defaultdict
w=int(sys.argv[1]); W,verts,edges=get(w)
adj=defaultdict(list)
for s,t,l in edges: adj[s].append((t,l))
def find_cycle(s,L=14):
    # DFS for a cycle of length L from s
    stack=[(s,[])]
    while stack:
        v,path=stack.pop()
        if len(path)==L:
            if v==s: return path
            continue
        for t,l in adj[v]: stack.append((t,path+[(t,l)]))
    return None
shown=0
for s in range(len(verts)):
    if verts[s][0]!=0: continue
    cyc=find_cycle(s)
    if cyc:
        seq=[s]+[t for t,_ in cyc][:-1]
        print('cycle start',s,'labels',''.join(str(l) for _,l in cyc))
        for v in seq:
            ph,cols=prefix(w,v); print('  t%-2d ph%d '%(seq.index(v),ph)+' '.join('%2d'%c for c in cols))
        shown+=1
        if shown>=2: break
