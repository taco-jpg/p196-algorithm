import os
import sys, itertools
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from ext_transfer import cell_transitions
def probe(b,p,s,Lmax=60):
    shifted=[t for t in range(p) if s[t]]
    layer={(tuple([0]*p),tuple(s),tuple([1]*len(shifted))):1}
    sizes=[]
    for j in range(Lmax):
        nxt={}
        for st in layer:
            cw,dw,T=st
            for ns,qo in cell_transitions(b,p,s,cw,dw,T,first=(j==0)):
                nxt[ns]=1
        layer=nxt
        sizes.append(len(layer))
        if not layer: break
    return sizes
if __name__=='__main__':
    b=int(sys.argv[1]); pmax=int(sys.argv[2])
    for p in range(1,pmax+1):
        out=[]
        for s in itertools.product((0,1),repeat=p):
            if not any(s): continue
            if s!=min(s[i:]+s[:i] for i in range(p)): continue
            sz=probe(b,p,s)
            out.append((''.join(map(str,s)),len(sz) if not sz or sz[-1]==0 else '>60', max(sz)))
        print('base',b,'p',p,'(s, death layer, max layer size):',out)
