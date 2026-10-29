# Exact, core-independent two-ended pairword prefix transducer.
# The sole nondeterminism is one physical carry from the untracked centre.
from collections import deque
import sys

def successors(P,base=10):
    k=len(P)
    low=[0]*(k+1)
    for i in range(k): low[i+1]=(P[i]+low[i])//base
    for entering in (0,1):
        hi=[0]*k
        hi[-1]=entering
        for i in range(k-1,0,-1):hi[i-1]=(P[i]+hi[i])//base
        gam=(P[0]+hi[0])//base
        dig=[(P[i]+low[i])%base for i in range(k)]
        if gam==0: result=tuple(dig[i]+(P[i]+hi[i])%base for i in range(k))
        else: result=tuple([dig[0]+1]+[dig[i]+(P[i-1]+hi[i-1])%base for i in range(1,k)])
        yield entering,gam,result

def explore(k,limit):
    initial=(7,)+(18,)*(k-1)
    visited={initial:0};q=deque([initial]);first_bad=[]; max_depth=0
    while q and len(visited)<limit:
        p=q.popleft();depth=visited[p];max_depth=max(max_depth,depth)
        if all(v%2==0 for v in p):
            first_bad.append((depth,p))
            break
        for h,gam,po in successors(p):
            if po not in visited:visited[po]=depth+1;q.append(po)
    print('k',k,'visited',len(visited),'queue',len(q),'maxDepth',max_depth,'bad',first_bad[:1]);
    return visited

if __name__=='__main__':
    for k in map(int,sys.argv[1:]):explore(k,500000)
