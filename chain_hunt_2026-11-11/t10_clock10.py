from tools import *
import time, pickle
B=10
g=(1,0)*4
F0=Frame(B,(0,)*8,g)
R=root_node(B,g)
t0=time.time()
starts=expand(F0,R)
print('roots',len(starts))
for H in starts: print('  ',H)
order,edges,ok=closure(F0,starts,maxnodes=300000,verbose=True)
print('nodes',len(order),'complete',ok,'time',time.time()-t0)
live,comps,cyc=live_nodes(len(order),edges)
print('live nodes',sum(live))
cs=[(len(cm),k) for k,cm in enumerate(comps) if cyc[k]]
cs.sort(reverse=True)
print('cyclic comps (size):',[c[0] for c in cs][:40])
pickle.dump((order,edges),open('clock10_p8.pkl','wb'))
