# dump live nodes of a rooted closure as text: id, then per phase a b c d
from pipeline import *
from chain import live_nodes
import sys
g=tuple(int(x) for x in sys.argv[1])
B=int(sys.argv[3]) if len(sys.argv)>3 else 10
r=rooted(B,g,3000000)
n=r['nodes']; el=r['el']; order=r['order']
live,comps,cyc=live_nodes(n,el)
with open(sys.argv[2],'w') as f:
    L=[v for v in range(n) if live[v]]
    f.write('%d %d\n'%(len(g),len(L)))
    f.write(' '.join(map(str,g))+'\n')
    for v in L:
        a,b,c,d=order[v]
        f.write(str(v)+' '+' '.join('%d %d %d %d'%(a[t],b[t],c[t],d[t]) for t in range(len(g)))+'\n')
print('live',len(L))
