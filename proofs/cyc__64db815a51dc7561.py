import gzip, struct, sys
from collections import defaultdict, deque
D='/home/claude/w103/proofs/contributions/agent-103/seven1-clock/seven_1/'
FULL='/tmp/claude-0/-home-claude/87768464-fbc9-5ea3-be50-bc4e801c33a1/scratchpad/seven1-full/seven_1/'
import os
def load(w):
    for base in (D,FULL):
        p=base+'branch_width_%02d_recurrent.bin.gz'%w
        if os.path.exists(p): break
    b=gzip.open(p).read(); assert b[:8]==b'P196BRC1'
    W,V,E=struct.unpack('<III',b[8:20]); off=20
    verts=[struct.unpack('<BBBI',b[off+7*i:off+7*i+7]) for i in range(V)]; off+=7*V
    edges=[struct.unpack('<IIB',b[off+9*i:off+9*i+9]) for i in range(E)]
    return W,verts,edges
# parent pointers refer to previous width's RECURRENT graph vertex
cache={}
def get(w):
    if w not in cache: cache[w]=load(w)
    return cache[w]
def prefix(w,v):
    cols=[]
    while True:
        W,verts,edges=get(w)
        ph,last,low,par=verts[v]
        cols.append(last)
        if par==2**32-1: break
        v=par; w-=1
    return ph,cols[::-1]
w=int(sys.argv[1]); W,verts,edges=get(w)
adj=defaultdict(list)
for s,t,l in edges: adj[s].append((t,l))
# find shortest cycles of length 7 (one period) via BFS from each phase-0 vertex
found=0
for s in range(len(verts)):
    if verts[s][0]!=0: continue
    # paths of length 7 back to s
    frontier={s:[]}
    for step in range(7):
        nf={}
        for v,path in frontier.items():
            for t,l in adj[v]:
                if t not in nf: nf[t]=path+[(t,l)]
        frontier=nf
    if s in frontier:
        found+=1
        if found<=3:
            seq=[s]+[t for t,_ in frontier[s]]
            print('7-cycle from',s,'labels',[l for _,l in frontier[s]])
            for v in seq[:7]:
                ph,cols=prefix(w,v); print('  phase',ph,'cols',cols)
print('phase0 vertices',sum(1 for x in verts if x[0]==0),'with 7-cycles',found)
