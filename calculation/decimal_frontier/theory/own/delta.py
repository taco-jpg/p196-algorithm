# distribution of width change over one lap for lap-survivors, using the Python mirror semantics (exact)
import sys, itertools, collections
sys.path.insert(0,'/home/claude/research/w2_theory'); sys.path.insert(0,'/home/claude/research/w2_theory/scripts')
import lib, mirror as m
from parse_bw import parse_bw
line=[l for l in open('/home/claude/research/w2_theory/out2/bauto_p11_w.txt') if 'ACCEPT' in l][0]
b,p,g,e,Bs=parse_bw(line)
def lap(C):
    cur=C; trims=[]
    for t in range(p):
        r=m.step(b,Bs[t],list(cur))
        if r is None or len(r[3])==0: return None
        cur=r[3]; trims.append(r[5])
    return cur,trims
W=int(sys.argv[1])
cnt=collections.Counter(); ex=[]
for L in range(1,W+1):
    h=(L+1)//2
    for half in itertools.product(range(2*b-1),repeat=h):
        if L%2==1 and half[-1]%2: continue
        if L>=2 and half[0]==b-1: continue
        C=list(half)+list(half[:L//2][::-1])
        # quick prefilter: first step survives?
        r=lap(C)
        if r is None: continue
        img,tr=r
        cnt[(L,len(img)-L,sum(tr))]+=1
        if len(img)<=L and len(ex)<20: ex.append((C,img,tr))
print(sorted(cnt.items()))
for x in ex: print(x)
