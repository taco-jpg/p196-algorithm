import os
import sys,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from ext_transfer import cell_transitions
b=int(sys.argv[1]); s=tuple(int(c) for c in sys.argv[2]); Lmax=int(sys.argv[3]); tl=float(sys.argv[4])
p=len(s); shifted=[t for t in range(p) if s[t]]
layer={(tuple([0]*p),tuple(s),tuple([1]*len(shifted))):1}
t0=time.time(); sizes=[]
for j in range(Lmax):
    nxt={}
    for st in layer:
        cw,dw,T=st
        for ns,qo in cell_transitions(b,p,s,cw,dw,T,first=(j==0)):
            nxt[ns]=1
    layer=nxt; sizes.append(len(layer))
    hits=[st for st in layer if all(st[1][t]==1-st[0][t] for t in range(p)) and all(st[2][i]==(b-1)*st[0][t] for i,t in enumerate(shifted))]
    if hits: print('layer',j+1,'closing states',len(hits)); 
    if not layer: print('DIED at layer',j+1); break
    if time.time()-t0>tl: print('time limit at layer',j+1); break
print('sizes',sizes[:5],'...',sizes[-5:],'final',len(layer),'t=%.1f'%(time.time()-t0))
