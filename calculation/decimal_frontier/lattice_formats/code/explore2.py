import sys, itertools, collections, time
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import *
from explore1 import run_template
t0=time.time()
for b in (2,3,4):
    for k in (0, 2*(b-1)):
        res = collections.Counter(); cyc=[]
        for lb in range(1,7 if b<4 else 5):
            for B in itertools.product(range(2*b-1), repeat=lb):
                if B[0]==0: continue
                T = Template(b, [('L',B),('B',(k,),0)], ())
                r = run_template(T, 150, 30)
                res[r[0]] += 1
                if r[0]=='cycle': cyc.append((B, r[1], r[3]))
        print('base',b,'band',k,dict(res),'cycles:',cyc[:5], flush=True)
        if time.time()-t0>14: sys.exit()
