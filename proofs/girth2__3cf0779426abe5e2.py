import sys
exec(open('cyc.py').read().split('w=int(sys.argv[1])')[0])
from collections import defaultdict
for w in map(int, sys.argv[1:]):
    W,verts,edges=get(w)
    adj=defaultdict(list)
    for s,t,l in edges: adj[s].append(t)
    found=[]
    for s in range(len(verts)):
        if verts[s][0]!=0: continue
        cur={s}
        for step in range(1,15):
            cur={t for v in cur for t in adj[v]}
        if s in cur: found.append(s)
    print('width',w,'vertices',len(verts),'phase0 with 14-cycles',len(found), flush=True)
    if found:
        ph,cols=prefix(w,found[0]); print('  example prefix',cols)
