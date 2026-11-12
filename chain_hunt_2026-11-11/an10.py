from tools import *
import pickle
from collections import deque
B=10
order,edges=pickle.load(open('clock10_p8.pkl','rb'))
n=len(order)
live,comps,cyc=live_nodes(n,edges)
comp_of=[0]*n
for k,cm in enumerate(comps):
    for v in cm: comp_of[v]=k
cyccomps=[k for k in range(len(comps)) if cyc[k]]
print('cyclic comps:',[(k,len(comps[k])) for k in cyccomps])
# reachability between cyclic comps
def reach(src):
    seen=set(src); dq=deque(src)
    while dq:
        v=dq.popleft()
        for w in edges[v]:
            if w not in seen: seen.add(w); dq.append(w)
    return seen
for k in cyccomps:
    r=reach(comps[k])
    print('comp',k,'size',len(comps[k]),'reaches comps',sorted(set(comp_of[v] for v in r if cyc[comp_of[v]])))
# distance from roots (node ids of starts are 0..)
dist=[None]*n
# roots: nodes that are successors of root: they were inserted first; find by BFS from first nodes w/ c==0
roots=[i for i,H in enumerate(order) if all(x==0 for x in H[2])]
print('root-like nodes (c==0):',len(roots), roots[:10])
dq=deque()
for r in roots: dist[r]=0; dq.append(r)
while dq:
    v=dq.popleft()
    for w in edges[v]:
        if dist[w] is None: dist[w]=dist[v]+1; dq.append(w)
for k in cyccomps:
    print('comp',k,'min depth',min(dist[v] for v in comps[k]),'max depth',max(dist[v] for v in comps[k]))
# big SCC: shortest cycle through each node, set of cycle lengths
big=max(cyccomps,key=lambda k:len(comps[k]))
S=set(comps[big])
def shortest_cycle(v):
    d={v:0}; dq=deque([v])
    while dq:
        u=dq.popleft()
        for w in edges[u]:
            if w==v: return d[u]+1
            if w in S and w not in d: d[w]=d[u]+1; dq.append(w)
    return None
sc=[shortest_cycle(v) for v in comps[big]]
from collections import Counter
print('big SCC shortest-cycle-through-node histogram:',sorted(Counter(sc).items()))
outdeg=Counter(sum(1 for w in edges[v] if w in S) for v in comps[big])
print('big SCC out-degree (inside SCC) histogram:',sorted(outdeg.items()))
# 9s present?
has9=sum(1 for v in comps[big] if 9 in psums(order[v]))
print('big SCC nodes having a pair sum 9 at some time:',has9)
for k in cyccomps:
    if k!=big:
        cm=comps[k]
        print('20-cycle comp',k,'has9:',sum(1 for v in cm if 9 in psums(order[v])))
        v=cm[0]; walk=[v]
        while True:
            nx=[w for w in edges[walk[-1]] if comp_of[w]==k][0]
            if nx==v: break
            walk.append(nx)
        print('  pair sums at t=0 along cycle:',[psums(order[u])[0] for u in walk])
        print('  pair sums at t=1 along cycle:',[psums(order[u])[1] for u in walk])
# wires
wires=[i for i,H in enumerate(order) if all(s==9 for s in psums(H))]
print('all-9 nodes:',len(wires))
